import pytest
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import compensate_handle_tasks, capital_settlement_tasks, repay_tasks
from biztest.config.easymock.easymock_config import rbiz_mock
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_asset_info_by_item_no
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback
from biztest.interface.rbiz.rbiz_interface import monitor_check
from biztest.util.easymock.rbiz.mozhi_jinmeixin import RepayMozhiJinmeixinMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after
import common.global_const as gc


class TestDcsMozhiJinmeixin(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "mozhi_jinmeixin"
    period_count = 12
    grant_principal = 600000
    first_period_interest = 15541  # 第一期息费

    @classmethod
    def setup_class(cls):
        monitor_check()
        cls.beiyin_mock = RepayMozhiJinmeixinMock(rbiz_mock)

    def setup_method(self):
        self.init(self.env_test)
        self.item_no = 'mzjmx_' + get_item_no()
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, asset_amount=6000, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_mzjmx
    def test_mzjmx_channel_normal_repay(self):
        print("====================第一期正常还款（资方扣全额）====================")
        # setp 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_normal = (1,)
        # step 2 到期日往前推1月 & 主动还款
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest)
        self.beiyin_mock.update_repay_result(int(asset_tran_amount["asset_tran_balance_amount"]), due_bill_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 3 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        check_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq_channel")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq_channel")
        check_trans.check_trans_all()
        check_trans.check_trans_amount()

        print("================清分完成后，补充流程，资方只有正常还款的代扣=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal",
                                                    self.channel, "N", "", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 2)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "")

    @pytest.mark.DCS_test_auto_test_demo
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_mzjmx
    def test_mzjmx_channel_payoff(self):
        print("====================第一期到期日前提前结清（资方代扣成功。我方代扣成功）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_trail(self.grant_principal, 7000)
        # 凑担保费整期,利息整期给资方扣
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest - 9018)
        self.beiyin_mock.update_repay_result(self.grant_principal + self.first_period_interest - 9018, due_bill_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)

        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            check_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq")
            check_final.check_final_all()
            # check_final.check_final_amount(capital)
            check_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', self.channel)
            check_trans.check_trans_all()
            check_trans.check_trans_amount()

        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "N", "",
                                                    get_date_after(expect_operate_at, day=4))
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            check_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "")

    @pytest.mark.DCS_test_auto_test_demo
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_mzjmx
    def test_mzjmx_channel_settle_our_fail_and_compensate(self):
        print("====================第一期到期日提前结清（资方代扣成功。我方代扣失败）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        period_overdue = (1,)
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_trail(self.grant_principal, 1000)
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest - 7000)
        self.beiyin_mock.update_repay_result(self.grant_principal + self.first_period_interest - 7000, due_bill_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_capital = resp_repay["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_capital, 2)
        # 小单和我方代扣部分失败
        order_our = resp_repay["data"]["project_list"][1]["order_no"]
        paysvr_callback(order_our, 3)
        order_noloan = resp_repay["data"]["project_list"][2]["order_no"]
        paysvr_callback(order_noloan, 3)
        self.run_task_after_withhold_callback([order_capital, order_our, order_noloan])
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_overdue)

        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            check_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq")
            check_final.check_final_all()
            # check_final.check_final_amount(capital)
            check_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', self.channel)
            check_trans.check_trans_all()
            check_trans.check_trans_amount()

        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "N", "",
                                                    get_date_after(expect_operate_at, day=4))
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            check_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "")
        # 逾期第1期 代偿第1期 到期日往前推1月
        due_bill_no = get_asset_info_by_item_no(self.item_no)[0]['asset_due_bill_no']
        self.beiyin_mock.update_repay_list(due_bill_no, self.grant_principal, self.first_period_interest,
                                           late_interest=150)

        self.change_asset_due_at(-1, -1)
        # step 2 刷罚息
        self.refresh_late_fee(self.item_no)

        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_overdue)
