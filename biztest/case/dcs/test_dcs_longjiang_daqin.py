import pytest
# capital7环境就用 xxljob_config ，capital6环境就用 xxljob_config2 。
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import repay_tasks, capital_settlement_tasks, compensate_handle_tasks, \
    buyback_handle_tasks
from biztest.config.easymock.easymock_config import rbiz_mock
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan, insert_buyback
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period
from biztest.interface.rbiz.rbiz_interface import paysvr_callback, monitor_check
from biztest.util.easymock.rbiz.longjiang_daqin import RepayLongjiangMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after, get_date_before_today
import common.global_const as gc


class TestDcsLongjiangDaqin(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "longjiang_daqin"
    period_count = 12
    grant_principal = 800000
    first_period_interest = 16940  # 第一期息费

    @classmethod
    def setup_class(cls):
        monitor_check()
        cls.lj_mock = RepayLongjiangMock(rbiz_mock)

    @classmethod
    def teardown_class(cls):
        print("无需初始化")

    def setup_method(self):
        self.init(self.env_test)
        self.item_no = 'lj_' + get_item_no()
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_longjiang
    def test_longjiang_channel_normal_repay(self):
        print("====================第一期正常还款（资方扣全额）====================")
        # setp 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_normal = (1,)
        # step 2 到期日往前推1月 & 主动还款
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
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
        # check_final.check_final_all()
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
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "advance", self.channel, "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_longjiang
    def test_longjiang_channel_payoff(self):
        """
        龙江提前结清，结算给资方的利>我方还款计划的利息，属于贴息的场景
        """
        print("====================第一期提前结清（资方代扣本息／我方代扣费）====================")
        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.lj_mock.update_repayment_calculate(8000)

        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        # step 1 到期日往前推一个月
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
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
            check_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq_channel")
            # check_final.check_final_all()
            check_final.check_final_amount(capital)
            check_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq_channel")
            check_trans.check_trans_all()
            check_trans.check_trans_amount()
        print("=================哈密天山/哈密天邦，提前结清，报表日期（财务应计结算日期）=推送T0==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "Over", "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            check_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_longjiang
    def test_longjiang_qsq_compensate_repay(self):

        """
        龙江代偿，代偿的利息和还款计划的利息一致
        """
        print("================第一期代偿并代偿后还款================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_compensate = (1,)
        # step 1 到期日往前推一个月
        self.change_asset_due_at(-1, -1)

        print("================第一期代偿后还款（制造先还款再代偿的场景）================")
        # step 2 刷罚息，到期日上面已经修改过了

        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        # step 3 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
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
        # # 检查清分的数据
        # capital = get_capital_biz(self.item_no, period_compensate[0])
        # check_final = CheckDcsFinal(self.item_no, period_compensate[0], 'repay', "qsq")
        # check_final.check_final_all()
        # check_final.check_final_amount(capital)
        # check_trans = CheckDcsTrans(self.item_no, period_compensate[0], 'repay', "qsq")
        # check_trans.check_trans_all()
        # check_trans.check_trans_amount()

        print("================开始大单代偿清分（制造先还款再代偿的场景）================")
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_compensate)
        # # 检查代偿清分的数据
        # capital = get_capital_biz(self.item_no, period_compensate[0])
        # check_final = CheckDcsFinal(self.item_no, period_compensate[0], 'compensate', 'qsq')
        # check_final.check_final_all()
        # check_final.check_final_amount(capital)
        # check_trans = CheckDcsTrans(self.item_no, period_compensate[0], 'compensate', 'qsq')
        # check_trans.check_trans_all()
        # check_trans.check_trans_amount()
        print("=================我方还款/逾期未还，报表日期（财务应计结算日期）=到期D+4==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_compensate[0], period_compensate[0])
        expect_operate_at = get_date_after(repay_plan[0]["asset_tran_due_at"][:10], day=1)
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_compensate[0], period_compensate[0], "compensate", "qsq",
                                                    "Over", "guarantee", expect_operate_at)
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        # check_trans.check_settlement_notify_clearing(period_compensate[0], period_compensate[0], "compensate",
        #                                              "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_longjiang
    def test_longjiang_buyback(self):
        print("====================回购====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        # 修改放款日期 到期日
        buyback_period = (3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        # step 1 到期日往前推3月零1天
        self.change_asset_due_at(-3, -1)
        # 查询本金，然后直接往 buyback 表插入数据 （固定设置从第3期开始回购）
        principal_plan = get_one_repay_plan(self.item_no, 'repayprincipal', 1, buyback_period[-1])
        principal_amount = 0
        for ii in range(0, len(principal_plan)):
            if principal_plan[ii]["asset_tran_period"] in buyback_period:
                principal_amount = principal_amount + principal_plan[ii]["asset_tran_amount"]
        insert_buyback(self.item_no, self.period_count, principal_amount, buyback_period[0], self.channel)
        # 执行 回购脚本
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(buyback_handle_tasks, buyback_period)
        # # 检查数据
        # for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
        #     capital = get_capital_biz(self.item_no, capital_i)
        #     cleck_final = CheckDcsFinal(self.item_no, capital_i, 'compensate', 'qsq')
        #     cleck_final.check_final_all()
        #     cleck_final.check_final_amount(capital)
        #     cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'compensate', 'qsq')
        #     cleck_trans.check_trans_all()
        #     cleck_trans.check_trans_amount()
        # print("=================龙江回购，报表日期（财务应计结算日期）=银行还款日期日==================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "buyback", "qsq", "Over",
                                                    "guarantee", get_date_before_today()[:10])
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # # step 4 检查数据
        # for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
        #     cleck_trans.check_settlement_notify_clearing(buyback_period[0], capital_i, "compensate", "guarantee")
