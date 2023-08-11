import pytest, time
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import capital_settlement_tasks, compensate_handle_tasks, repay_tasks
from biztest.config.easymock.easymock_config import mock_project
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_hami_tianshan_tianbang_config
from biztest.function.dcs.biz_database import get_repay_amount_rbiz, get_capital_biz, get_one_repay_plan
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.interface.rbiz.biz_central_interface import run_type_task_biz_central
from biztest.interface.rbiz.rbiz_interface import paysvr_callback, monitor_check
from biztest.util.easymock.rbiz.paysvr import PaysvrMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after
import common.global_const as gc


class TestDcsHaMiTianShanTianBang(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "hami_tianshan_tianbang"  # hami_tianshan_tianbang , hami_tianshan
    period_count = 12

    @classmethod
    def setup_class(cls):
        monitor_check()
        # 修改哈密天数天邦的配置以及其mock
        update_repay_hami_tianshan_tianbang_config(mock_project['rbiz_auto_test']['id'])

    @classmethod
    def teardown_class(cls):
        update_repay_hami_tianshan_tianbang_config()

    def setup_method(self):
        self.init(self.env_test)
        self.item_no = 'ha_hmtb_' + get_item_no()[:16]
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, count=self.period_count, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hami
    def test_hami_channel_normal_repay(self):
        print("====================第一期正常还款（资方代扣本息／我方代扣费）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_normal = (1,)
        # step 1 到期日往前推一个月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣

        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行rbiz的task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 5 检查biz的帐信（同步代扣记录）
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
        print("=================哈密天山/哈密天邦，正常还款-资方，报表日期（财务应计结算日期）=客户还款当日==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", self.channel, "N", "",
                                                    expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hami
    def test_hami_qsq_normal_repay(self):
        print("====================第一期正常还款（资方代扣失败／切我方代扣全部）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_normal = (1,)
        # step 1 到期日往前推一个月
        self.change_asset_due_at(-1, 0)
        # step 3 发起主动代扣

        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 3)
        self.run_task_after_withhold_callback(order_list)

        # step 6 第二次发起主动代扣
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 7 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 8 检查biz的帐信息
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
        print("=================哈密天山/哈密天邦，我方还款/逾期未还，报表日期（财务应计结算日期）=到期D+4==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = get_date_after(repay_plan[0]["asset_tran_due_at"][:10], day=4)
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "compensate", "qsq", "N", "",
                                                    expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "")

    @pytest.mark.DCS_test_0629
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hami
    def test_hami_channel_overdue_repay(self):
        print("================第一期逾期还款（资方代扣本息／我方代扣费）（哈密D+4代偿）================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_overdue = (1,)
        # step 1 到期日往前推一个月，并刷罚息

        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        # step 2 刷完罚息需要执行biz的task，不然还款计划不完整
        run_type_task_biz_central("AssetChange", self.item_no)
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
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_overdue)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_overdue[0])
        cleck_final = CheckDcsFinal(self.item_no, period_overdue[0], 'repay', "qsq_channel")
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_overdue[0], 'repay', "qsq_channel")
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()
        print("=================哈密天山/哈密天邦，D1-D3还款-资方，报表日期（财务应计结算日期）=客户还款当日==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_overdue[0], period_overdue[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_overdue[0], period_overdue[0], "overdue", self.channel, "N",
                                                    "", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_overdue[0], period_overdue[0], "repay", "")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hami
    def test_hami_qsq_overdue_repay(self):
        print("================第一期逾期还款（资方代扣失败／切我方代扣全部）（哈密D+4代偿）================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_overdue = (1,)
        # step 1 到期日往前推一个月，并刷罚息

        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        # step 3 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_overdue)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_overdue)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 3)  # step 4 执行task和msg

        self.run_task_after_withhold_callback(order_list)

        # step 6 第二次发起主动代扣
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 7 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 8 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_overdue)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_overdue[0])
        cleck_final = CheckDcsFinal(self.item_no, period_overdue[0], 'repay', "qsq")
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_overdue[0], 'repay', "qsq")
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()
        print("=================哈密天山/哈密天邦，我方还款/逾期未还，报表日期（财务应计结算日期）=到期D+4==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_overdue[0], period_overdue[0])
        expect_operate_at = get_date_after(repay_plan[0]["asset_tran_due_at"][:10], day=4)
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_overdue[0], period_overdue[0], "compensate", "qsq", "N", "",
                                                    expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_overdue[0], period_overdue[0], "repay", "")

    @pytest.mark.DCS_test_0629
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hami
    def test_hami_qsq_compensate_repay(self):
        print("================第一期代偿并代偿后还款（哈密D+4代偿）================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_compensate = (1,)
        # step 1 到期日往前推一个月
        self.change_asset_due_at(-1, -4)

        print("================第一期代偿后还款（哈密D+4代偿）（制造先还款再代偿的场景）================")

        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

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
        print("=================哈密天山/哈密天邦，我方还款/逾期未还，报表日期（财务应计结算日期）=到期D+4==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_compensate[0], period_compensate[0])
        expect_operate_at = get_date_after(repay_plan[0]["asset_tran_due_at"][:10], day=4)
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_compensate[0], period_compensate[0], "compensate", "qsq",
                                                    "N", "", expect_operate_at)
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_compensate[0], period_compensate[0], "compensate", "qsq")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hami
    def test_hami_channel_payoff(self):
        print("====================第一期提前结清（资方代扣本息／我方代扣费）====================")
        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)

        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        # step 1 到期日往前推一个月
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行rbiz的task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信（同步代扣记录）
        check_repay_biz(self.item_no)
        # 开始大单还款清分，period_payoff 主要是监控task生成的数量，因为这是资方代扣，会有两条代扣记录，两个bigRepayClearing，就会有24个task
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff * 2)
        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
        print("=================哈密天山/哈密天邦，提前结清，报表日期（财务应计结算日期）=推送T0==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "N", "", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "")
