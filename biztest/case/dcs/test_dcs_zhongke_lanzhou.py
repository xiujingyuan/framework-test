import json, pytest, time
# capital7环境就用 xxljob_config ，capital6环境就用 xxljob_config2 。
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import capital_settlement_tasks, compensate_handle_tasks, repay_tasks
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_lanzhou_config
from biztest.function.biz.biz_db_function import set_withhold_history
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan, update_atransaction, \
    get_repay_amount_rbiz, update_asset_extend_ref_and_sub_order_type, set_up_the_asset_trans_for_compensate
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.capital_database import get_clean_capital_settlement_notify_tran, update_notify_tran_at_dcs, \
    get_open_task_dcs_by_order_no, update_dcs_china_task_next_run_at
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz
from biztest.function.dcs.dcs_run_xxljob_china import DcsRunXxlJobChina
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count, scenes_receive
from biztest.interface.rbiz.rbiz_interface import paysvr_callback, asset_provision_settle, monitor_check, \
    asset_bill_decrease
from biztest.util.easymock.rbiz.lanzhou_haoyue import RepayLanzhouMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_before_today, get_date_after
import common.global_const as gc


# 20210629
class TestDcsZhongKeLanZhou(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "zhongke_lanzhou"  # zhongke_lanzhou、lanzhou_dingsheng_zkbc2、lanzhou_haoyue(走资方还款需要修改配置，建议重新加一套自动化)
    period_count = 12

    @classmethod
    def setup_class(cls):
        monitor_check()
        set_up_the_asset_trans_for_compensate()
        cls.lanzhou_mock = RepayLanzhouMock(rbiz_mock)
        update_repay_lanzhou_config()
        update_dcs_china_task_next_run_at(status='close')


    @classmethod
    def teardown_class(cls):
        update_repay_lanzhou_config()

    def setup_method(self):
        self.init(self.env_test)
        self.item_no = 'ck_lz_' + get_item_no()[:16]
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, count=self.period_count, script_system='dcs')
        normal_time_limit = {"startTime": "00:00:00", "endTime": "22:30:00"}
        fail_times = {"auto": {"times": 1, "calByDay": False}, "active": {"times": 1, "calByDay": False},
                      "manual": {"times": 1, "calByDay": False}}
        update_repay_lanzhou_config()

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_lanzhou
    def test_lanzhou_channel_normal_repay(self):
        print("====================第一期正常还款（资方扣本息和担保费，我方扣剩余费）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 5 检查biz的帐信息
        check_repay_biz(self.item_no)

        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        cleck_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq_channel")
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq_channel")
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()
        print("=================兰州，正常还款-资方，报表日期（财务应计结算日期）=客户还款当日==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", self.channel, "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_lanzhou
    def test_lanzhou_qsq_normal_repay(self):
        print("====================第一期正常还款（全部我方代扣）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 0 修改配置使只能我方代扣
        normal_time_limit = {"startTime": "00:00:00", "endTime": "00:30:00"}
        update_repay_lanzhou_config()
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 5 检查biz的帐信息
        check_repay_biz(self.item_no)
        #

        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        cleck_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()

        print("=================兰州，到期D+2为工作日，报表日期（财务应计结算日期）=还款计划到期日==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        # advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "offline", "qsq", "N", "guarantee", get_date_after(expect_operate_at, day=3))
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "offline", "qsq", "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_lanzhou
    def test_lanzhou_qsq_overdue_repay_and_compensate(self):
        print("====================第一期线下还款（全部我方代扣）然后代偿 ====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_overdue = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, -1)
        # step 2 刷罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_overdue)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_overdue)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 5 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分-执行task
        job_run = DcsRunXxlJobChina(self.item_no, "")
        for i in range(20):
            time.sleep(1)
            job_run.run_clearing_jobs_post("dbTaskJob")
        # 检查清分的数据
        # capital = get_capital_biz(self.item_no, period_overdue[0])
        # cleck_final = CheckDcsFinal(self.item_no, period_overdue[0], 'repay', "qsq")
        # cleck_final.check_final_all()
        # cleck_final.check_final_amount(capital)
        # cleck_trans = CheckDcsTrans(self.item_no, period_overdue[0], 'repay', "qsq")
        # cleck_trans.check_trans_all()
        # cleck_trans.check_trans_amount()
        print("================清分完成后，兰州补充流程，我方代扣宽限期还款需要推线下还款=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_overdue[0], period_overdue[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_overdue[0], period_overdue[0], "offline", "qsq", "N",
                                                    "guarantee", get_date_after(expect_operate_at, day=3))
        print("================开始大单代偿清分（制造先还款再代偿的场景）================")
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_overdue)
        # 检查代偿清分的数据
        # capital = get_capital_biz(self.item_no, period_overdue[0])
        #         # cleck_final = CheckDcsFinal(self.item_no, period_overdue[0], 'compensate', 'qsq')
        #         # cleck_final.check_final_all()
        #         # cleck_final.check_final_amount(capital)
        #         # cleck_trans = CheckDcsTrans(self.item_no, period_overdue[0], 'compensate', 'qsq')
        #         # cleck_trans.check_trans_all()
        #         # cleck_trans.check_trans_amount()
        print("=================先发送代偿的消息，再进行代偿清分，清分后才会生成task==================")
        # step 3 执行task
        # repay_run.run_capital_settlement_task(capital_settlement_tasks)
        for i in range(10):
            time.sleep(1)
            job_run.run_clearing_jobs_post("dbTaskJob")
        # step 4 检查数据
        # cleck_trans.check_settlement_notify_clearing(period_overdue[0], period_overdue[0], "compensate", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_lanzhou
    def test_lanzhou_qsq_payoff(self):
        print("====================第一期到期日提前结清（全方我方代扣）====================")
        # self.item_no, self.item_num_no_loan = "hei_lz_2020162476572928", "noloan_hei_lz_2020162476572928"
        normal_time_limit = {"startTime": "00:00:00", "endTime": "00:30:00"}
        update_repay_lanzhou_config()
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.lanzhou_mock.update_repay_apply()
        self.lanzhou_mock.update_repay_query()
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 5 检查biz的帐信息
        check_repay_biz(self.item_no)
        check_repay_biz(self.item_num_no_loan)

        # 开始大单还款清分，period_payoff 主要是监控task生成的数量，因为这是我方代扣，只有1条代扣记录，1个bigRepayClearing，就会有12个task
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)
        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq")
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq")
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
        print("================兰州，提前结清，报表日期（财务应计结算日期）=推送T0=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[0], "offline", "qsq", "N",
                                                    "guarantee", get_date_after(expect_operate_at, day=3))
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_payoff[0], period_payoff[0], "repay", "guarantee")

        print("================兰州，提前结清，报表日期（财务应计结算日期）=推送T0=================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[1], period_payoff[-1], "early_settlement", "qsq", "Y",
                                                    "guarantee", get_date_after(expect_operate_at, day=4))
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[1], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[1], capital_i, "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_lanzhou
    def test_lanzhou_early_settlement_payoff(self):
        print("====================第一期内提前结清（全方我方代扣）====================")
        normal_time_limit = {"startTime": "00:00:00", "endTime": "00:30:00"}
        update_repay_lanzhou_config()
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.lanzhou_mock.update_repay_apply()
        self.lanzhou_mock.update_repay_query()
        # step 1 到期日往前推1月
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 5 检查biz的帐信息
        check_repay_biz(self.item_no)

        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)
        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq")
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq")
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
        print("================兰州，提前结清，报表日期（财务应计结算日期）=推送T0=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement", "qsq", "Y",
                                                    "guarantee", get_date_after(expect_operate_at, day=2))
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_lanzhou
    def test_lanzhou_channel_normal_repay_channel_fail_compensate(self):
        print("====================第一期正常还款（资方扣本息失败／我方扣费成功）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        repay_apply = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 使用回调使部分成功部分使失败，这个顺序使固定的？？？
        order_no = repay_apply["data"]["project_list"][0]["order_no"]
        order_no_our = repay_apply["data"]["project_list"][1]["order_no"]
        order_no_noloan = repay_apply["data"]["project_list"][2]["order_no"]
        paysvr_callback(order_no, 3)
        paysvr_callback(order_no_our, 2)
        paysvr_callback(order_no_noloan, 2)
        # step 4 执行回调task
        self.task.run_task_by_order_no_count(self.item_no)
        self.task.run_task_by_order_no_count(self.item_num_no_loan)
        self.task.run_task_by_order_no_count(order_no)
        self.task.run_task_by_order_no_count(order_no_our)
        self.task.run_task_by_order_no_count(order_no_noloan)
        # step 5 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 5 检查biz的帐信息
        check_repay_biz(self.item_no)

        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查还款清分的数据，部分还款不检查金额
        print("=================到期日资产代扣失败，本息需要代偿==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "compensate", "qsq", "N",
                                                    "guarantee", expect_operate_at)
        print("=================代偿本息==================")
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, -1)
        update_atransaction(get_date_before_today(day=1), self.item_no, period_normal[0])
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_normal)
        # 检查代偿清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        cleck_final = CheckDcsFinal(self.item_no, period_normal[0], 'compensate', 'qsq')
        cleck_final.check_final_all()
        # cleck_final.check_final_amount(capital) 部分还款不检查金额
        cleck_trans = CheckDcsTrans(self.item_no, period_normal[0], 'compensate', 'qsq')
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()
        print("=================检查补充流程==================")
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "compensate", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_lanzhou
    def test_lanzhou_channel_normal_repay_qsq_fail_compensate(self):
        print("====================第一期正常还款（资方扣本息成功／我方扣费失败）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        repay_apply = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 使用回调使部分成功部分使失败，这个顺序使固定的？？？
        order_no = repay_apply["data"]["project_list"][0]["order_no"]
        order_no_our = repay_apply["data"]["project_list"][1]["order_no"]
        order_no_noloan = repay_apply["data"]["project_list"][2]["order_no"]
        paysvr_callback(order_no, 2, self.channel)
        paysvr_callback(order_no_our, 3)
        paysvr_callback(order_no_noloan, 3)
        # step 4 执行回调task
        self.task.run_task_by_order_no_count(self.item_no)
        self.task.run_task_by_order_no_count(self.item_num_no_loan)
        self.task.run_task_by_order_no_count(order_no)
        self.task.run_task_by_order_no_count(order_no_our)
        self.task.run_task_by_order_no_count(order_no_noloan)
        # step 5 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        check_repay_biz(self.item_no)

        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查还款清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        cleck_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', 'qsq_channel')
        cleck_final.check_final_all()
        # cleck_final.check_final_amount(capital) 部分还款不检查金额
        cleck_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', 'qsq_channel')
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()
        print("=================代偿费==================")
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, -1)
        update_atransaction(get_date_before_today(day=1), self.item_no, period_normal[0])
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_normal)
        # 部分还款不检查金额
        print("=================到期日我方代扣失败，费的部分需要代偿==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", self.channel, "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_lanzhou
    def test_lanzhou_qsq_normal_repay_compensate_and_offline(self):
        print("====================第一期正常还款（资方扣失败／切我方扣成功 compensate和offline并存时应该报错提醒）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 0 修改配置使只能我方代扣
        normal_time_limit = {"startTime": "00:00:00", "endTime": "00:30:00"}
        update_repay_lanzhou_config()
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 5 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        cleck_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()

        print("================清分完成后，兰州补充流程，我方代扣正常还款需要推线下还款=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "compensate", "qsq", "N",
                                                    "guarantee", expect_operate_at)

        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

        # 再推一次线下还款offline
        # step 5 模拟biz_central调用接口
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "offline", "qsq", "N",
                                                    "guarantee", get_date_after(expect_operate_at, day=3))

        run_dcs_task_by_count(self.item_no, 2)
        # 执行task应报错提醒
        capitalSettlementClearing_task = get_open_task_dcs_by_order_no("capitalSettlementClearing", self.item_no)
        assert capitalSettlementClearing_task[0][
                   "task_response_data"] == "{\"code\":2,\"message\":\"推送了多种repay_type,[compensate, offline]\",\"data\":null}"
        # offline的数据不能落地到trans
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_lanzhou
    def test_lanzhou_provision_repay_compensate(self):
        print("====================（第一期拨备结清推代偿的场景）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 拨备结清第1期
        asset_provision_settle(self.item_no, 1)
        # step 3 执行还款的task和msg
        self.run_task_after_loan_repay(self.item_no)
        self.run_account_msg_after_repaid()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)

        # 开始大单还款清分
        run_dcs_task_by_count(self.item_no, 10)
        run_dcs_task_by_count(self.item_no, 10)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        cleck_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()

        print("================清分完成后，兰州补充流程，我方代扣正常还款需要推线下还款=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "compensate", "qsq", "N",
                                                    "guarantee", expect_operate_at)

        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.DCS_test_lanzhou
    def test_noloan_partrepay(self):
        print("====================（先领取权益，再部分还款触发代偿的场景，目前只有lieyin需要领取权益）====================")
        check_asset_grant(self.item_no)

        self.change_asset_due_at(0, -1)
        period_payoff = (1, 2, 3, 4, 5, 6)
        update_asset_extend_ref_and_sub_order_type("lieyin", "",
                                                   self.item_num_no_loan)  # 放款成功后根据需要更新ref_and_sub_order_type
        run_dcs_task_by_count(self.item_num_no_loan, 3)
        scenes_receive(self.item_num_no_loan, "lieyin")
        run_dcs_task_by_count(self.item_num_no_loan, 3)
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        # 拨备结清以实现部分还款
        asset_bill_decrease(self.item_num_no_loan, 931768)  # 注意1000是需要拨备结清的钱，而且期次是还到最后一期的，不是第一期
        time.sleep(10)
        self.run_task_after_loan_repay(self.item_num_no_loan)
        self.run_account_msg_after_repaid()
        set_withhold_history(self.item_num_no_loan)
        run_dcs_task_by_count(self.item_num_no_loan, 8)
        # 数据没有检查
