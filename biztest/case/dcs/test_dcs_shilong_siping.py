import datetime
import time, pytest
# capital7环境就用 xxljob_config ，capital6环境就用 xxljob_config2 。
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import capital_settlement_tasks, compensate_handle_tasks, repay_tasks
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import  update_repay_paysvr_config
from biztest.function.dcs.biz_database import get_capital_biz, update_atransaction, get_one_repay_plan, \
    get_repay_amount_rbiz
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz, delete_null_biz
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count
from biztest.interface.rbiz.rbiz_interface import paysvr_callback
from biztest.util.easymock.rbiz.paysvr import PaysvrMock
from biztest.util.tools.tools import get_item_no, get_date_before_today, get_four_element, get_date_after
import common.global_const as gc


class TestDcsShilongsiping(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "shilong_siping"
    period_count = 6

    @classmethod
    def setup_class(cls):
        # 修改paysvr_config配置走mock，并且mock代扣成功
        update_repay_shilong_siping_config(mock_project['rbiz_auto_test']['id'])

    @classmethod
    def teardown_class(cls):
        update_repay_shilong_siping_config()

    def setup_method(self):
        self.init(self.env_test)
        self.item_no = 'ha_slsp' + get_item_no()
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, count=self.period_count, script_system='dcs')
        # 默认将代偿日设置到32号，这样会优先走资方代扣
        update_repay_shilong_siping_config(mock_project['rbiz_auto_test']['id'], "31")
        fail_times = {"auto": {"times": 1, "calByDay": False},
                      "active": {"times": 1, "calByDay": False},
                      "manual": {"times": 1, "calByDay": False}}
        update_repay_shilong_siping_config(mock_project['rbiz_auto_test']['id'], repay_time="00:00:00,23:59:00",
                                           fail_times=fail_times)

    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping
    def test_siping_qsq_normal_repay(self):
        print("====================第一期正常还款（全部为我方代扣）====================")
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
            paysvr_callback(order, 3)
        self.run_task_after_withhold_callback(order_list)

        # step 4 第二次发起主动代扣
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 5 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 6 执行biz的task（这一步也可以不要）
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 7 检查biz的帐信息
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
        print("=================清分完成后，四平没有我方代扣的提前还单期==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", "qsq", "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping
    def test_siping_channel_normal_repay(self):
        print("====================第一期正常还款（资方扣本息／我方扣费）====================")
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
        # step 5 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 6 执行biz的task（这一步也可以不要）
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 7 检查biz的帐信息
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
        print("=================清分完成后，四平没有我方代扣的提前还单期==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", self.channel, "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.DCS_test_auto_test_demo
    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping
    def test_siping_channel_normal_repay_channel_fail_compensate(self):
        print("====================第一期正常还款（资方扣本息失败／我方扣费成功）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 0 修改使代扣失败
        self.paysvr_mock.update_auto_pay_withhold_fail()
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
        # step 6 执行biz的task（这一步也可以不要）
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 部分还款不检查金额

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

    @pytest.mark.DCS_test_auto_test_demo
    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping
    def test_siping_channel_normal_repay_qsq_fail_compensate(self):
        print("====================第一期正常还款（资方扣本息成功／我方扣费失败）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 0 修改使代扣失败
        self.paysvr_mock.update_auto_pay_withhold_fail()
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
        paysvr_callback(order_no, 2)
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
        # step 6 执行biz的task（这一步也可以不要）
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查代偿清分的数据
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

    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping_demo
    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping
    def test_siping_qsq_compensate_repay(self):
        print("================第一期代偿并代偿后还款================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_compensate = (1,)
        # step 1 到期日往前推一个月
        self.change_asset_due_at(-1, -1)

        print("================第一期代偿后还款（制造先还款再代偿的场景）================")
        # time.sleep(2.5)
        # step 2 刷罚息，到期日上面已经修改过了
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        # step 2 刷完罚息需要执行biz的task，不然还款计划不完整
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 3 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_compensate)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_compensate)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 4 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 执行biz的task（这一步也可以不要）
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 5 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_compensate)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_compensate[0])
        cleck_final = CheckDcsFinal(self.item_no, period_compensate[0], 'repay', "qsq")
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_compensate[0], 'repay', "qsq")
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()

        print("=================先发送代偿的消息，再进行代偿清分==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_compensate[0], period_compensate[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_compensate[0], period_compensate[0], "compensate", "qsq",
                                                    "N", "guarantee", expect_operate_at)

        print("================开始大单代偿清分（制造先还款再代偿的场景）================")
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_compensate)
        # 检查代偿清分的数据
        capital = get_capital_biz(self.item_no, period_compensate[0])
        cleck_final = CheckDcsFinal(self.item_no, period_compensate[0], 'compensate', 'qsq')
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_compensate[0], 'compensate', 'qsq')
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()

        print("=================先发送代偿的消息，再进行代偿清分，清分后才会生成task==================")
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_compensate[0], period_compensate[0], "compensate",
                                                     "guarantee")

    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping
    def test_siping_qsq_payoff(self):
        print("====================第一期内提前结清（全部为我方代扣）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6)
        # step 1 到期日往前推10天
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 3)
        # step 3 执行task
        self.run_task_after_withhold_callback(order_list)

        # step 4 第二次发起主动代扣
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

        print("=================清分完成后，四平提前结清，收取一部分利息==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement", "qsq", "Y",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "guarantee")

    @pytest.mark.DCS_test_auto_test_demo
    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping
    def test_siping_channel_payoff(self):
        print("====================第一期内提前结清（资方扣本息／我方扣费）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6)
        # step 1 到期日往前推10天
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 5 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 6 执行biz的task（这一步也可以不要）
        # # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)
        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()

        print("=================清分完成后，四平提前结清，收取一部分利息==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "Y", "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "guarantee")

    @pytest.mark.DCS_test_auto_test_demo
    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping
    def test_siping_channel_normal_payoff_qsq_fail_compensate(self):
        print("====================第一期到期日提前结清（资方扣本息成功／我方扣费失败）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        repay_apply = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # step 3 使用回调使部分成功部分使失败，这个顺序使固定的？？？
        order_no = repay_apply["data"]["project_list"][0]["order_no"]
        order_no_our = repay_apply["data"]["project_list"][1]["order_no"]
        order_no_noloan = repay_apply["data"]["project_list"][2]["order_no"]
        paysvr_callback(order_no, 2)
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
        # step 6 执行biz的task（这一步也可以不要）
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)
        # 检查代偿清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', 'qsq_channel')
            cleck_final.check_final_all()
            # cleck_final.check_final_amount(capital) 部分还款不检查金额
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', 'qsq_channel')
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()

        print("=================代偿费==================")
        period_compensate = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, -1)
        update_atransaction(get_date_before_today(day=1), self.item_no, period_compensate)
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_compensate)
        # 部分还款不检查金额

        print("=================清分完成后，四平到期日提前结清，收取全部利息==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "N", "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        # for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
        cleck_trans.check_settlement_notify_clearing(period_payoff[0], period_payoff[0], "repay", "guarantee")

    @pytest.mark.DCS_test_auto_test_demo
    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_siping
    def test_siping_qsq_normal_payoff(self):
        print("====================第一期到期日提前结清（全部我方代扣）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 3)
        # step 3 执行task
        self.run_task_after_withhold_callback(order_list)

        # step 4 第二次发起主动代扣
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 5 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 6 执行biz的task（这一步也可以不要）
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)
        # 检查代偿清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', 'qsq')
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', 'qsq')
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()

        print("=================清分完成后，四平到期日提前结清，拆分推送之正常还款==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[0], "normal", "qsq", "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_payoff[0], period_payoff[0], "repay", "guarantee")

        print("=================清分完成后，四平到期日提前结清，拆分推送之提前结清==================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[1], period_payoff[-1], "early_settlement", "qsq", "Y",
                                                    "guarantee", get_date_after(expect_operate_at, day=1))
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        for capital_i in range(period_payoff[1], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[1], capital_i, "repay", "guarantee")
