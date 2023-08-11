import time, pytest
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import rbiz_mock
from biztest.function.biz.biz_db_function import set_withhold_history
from biztest.function.dcs.capital_database import update_expect_settlement_at_before_one_day, \
    update_loan_expect_settlement_at_before_one_day, update_noloan_expect_settlement_at_before_one_day
from biztest.function.dcs.check_precharge import check_compensate_clean_precharge_clearing_tran, \
    check_clean_precharge_clearing_tran, check_clean_accrual_tran, check_clean_scenes_receive, \
    check_repay_after_compensate_precharge_clearing_tran
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz, get_four_params_rbiz_db, \
    wait_dcs_record_appear, run_dcs_task_until_disappear
from biztest.config.dcs.xxljob_config import capital_settlement_tasks, compensate_handle_tasks, repay_tasks, \
    noloan_compensate_handle_tasks, auto_settlement_handle_tasks, not_received_handle_tasks
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan, get_repay_amount_rbiz, \
    update_asset_extend_ref_and_sub_order_type, set_up_the_asset_trans_for_compensate
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_db_function import get_clean_clearing_trans_settlement_info
from biztest.function.dcs.dcs_run_xxljob_china import DcsRunXxlJobChina
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count, scenes_receive, run_task_in_biz_dcs, \
    run_dcs_task_by_order_no, update_deposit_orderandtrade_and_run_task
from biztest.interface.rbiz.rbiz_interface import asset_provision_settle, asset_bill_decrease, \
    combo_active_repay_without_no_loan, paysvr_callback, monitor_check
from biztest.util.easymock.rbiz.qinnong import RepayQinnongMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after
import common.global_const as gc


class TestDcsLoanClearingAndSettlement(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "yixin_rongsheng"
    period_count = 6
    source_type = 'apr36'  # irr36_quanyi(这个关联到小单合并还款会有问题) , apr36 , irr36
    principal = 800000
    interest = 5200
    period_one_amount = 16495

    @classmethod
    def setup_class(cls):
        cls.qn_mock = RepayQinnongMock(rbiz_mock)
        # set_up_the_asset_trans_for_compensate()

    def setup_method(self):
        monitor_check()
        self.init(self.env_test)
        self.item_no = 'auto_dcs_' + get_item_no()
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success \
            (self.channel, self.four_element, self.item_no, count=self.period_count, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong_loan
    def test_loan_and_noloan_auto_settlement(self):
        print("====================（大小单还款后清分+大小单自动结算只有转账，没有做check-用于辅助测试）====================")
        # 2023.3.28调试成功
        check_asset_grant(self.item_no)
        run_dcs_task_by_count(self.item_num_no_loan, 1)
        period_advance = (1,)
        # 尽量造逾期的数据-减少走资方的可能
        self.change_asset_due_at(-1, -3)
        # 刷罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        # 大小单合并代扣-发起还款
        asset_tran_amount_loan = get_repay_amount_rbiz(self.item_no, period_advance)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_advance)
        resp_repay = self.repay_apply_success(asset_tran_amount_loan, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2, "baidu_tq3_quick")
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # 同步代扣记录到历史库
        set_withhold_history(self.item_no)
        set_withhold_history(self.item_num_no_loan)
        # 为后面JOB执行task和结算job做准备
        repay_run = DcsRunXxlJobChina(self.item_no, self.channel)
        # 执行task-进行清分
        for i in range(20):
            time.sleep(1)
            repay_run.run_clearing_jobs_post("dbTaskJob")

        print("============开始大单开始自动结算-只有转账-大单结算表clean_settlement==============")
        update_loan_expect_settlement_at_before_one_day(self.item_no)
        print("============开始结算==============")
        repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob")

        # 大单自动结算只有转账-请求到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        for i in range(10):
            repay_run.run_clearing_jobs_post("dbTaskJob")

        # TODO 转账完成，检查结算状态
        # trans_info = get_clean_clearing_trans_settlement_info(self.item_no)
        # check_clean_settlement()
        # 每次只检查最新的一笔的状态，记账后代付、转账后提现 :clean_generic_deal_order、clean_generic_deal_trade  通用流程可以沿用之前的检查?

        print("============开始小单自动结算-只有转账-小单结算表clean_precharge_clearing_tran==============")
        update_noloan_expect_settlement_at_before_one_day(self.item_num_no_loan)
        repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob", loanType="PRECHARGE")
        # 执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        for i in range(10):
            repay_run.run_clearing_jobs_post("dbTaskJob", loanType="PRECHARGE")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong_noloan
    def test_noloan_clearing_and_auto_settlement(self):
        print("====================（先领取权益 再还款的场景 分润给场景方）====================")
        check_asset_grant(self.item_no)
        update_asset_extend_ref_and_sub_order_type("lieyin", "",
                                                   self.item_num_no_loan)  # 放款成功后根据需要更新ref_and_sub_order_type

        # 权责分配
        wait_dcs_record_appear(
            "select * from clean_task where task_order_no='%s' and task_type='accrualAllocated'" % self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)

        scenes_receive(self.item_num_no_loan)
        # 领取权益
        wait_dcs_record_appear(
            "select * from clean_task where task_order_no='%s' and task_type='scenesReceiveSave'" % self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)

        # 开始小单清分
        run_dcs_task_by_count(self.item_num_no_loan, 1)
        period_advance = (1,)
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_advance)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_advance)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        set_withhold_history(self.item_num_no_loan)

        print("============开始小单自动结算-只有转账-小单结算表clean_precharge_clearing_tran==============")
        update_noloan_expect_settlement_at_before_one_day(self.item_num_no_loan)
        repay_run = DcsRunXxlJobChina(self.item_no, self.channel)
        repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob", loanType="PRECHARGE")
        # 执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        for i in range(10):
            repay_run.run_clearing_jobs_post("dbTaskJob")

    def test_qinnong_qsq_payoff(self):
        # 大单资方本息自动对账结算
        print("====================第一期到期日 提前结清走我方====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        self.qn_mock.update_repay_trail(self.principal, self.interest)
        asset_tran_amount["asset_tran_balance_amount"] = self.principal + self.period_one_amount
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_task_after_loan_repay(self.item_no)
        self.run_all_msg_after_repay_success()

        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)
        print("=================清分完成后，秦农提前结清，收取第一期利息，还款次日结算==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement", "qsq", "N",
                                                    "", "2022-08-22")
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)

