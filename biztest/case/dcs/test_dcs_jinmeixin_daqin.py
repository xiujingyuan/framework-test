import time, pytest
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import rbiz_mock
from biztest.function.biz.biz_db_function import set_withhold_history
from biztest.function.dcs.capital_database import update_expect_settlement_at_before_one_day, \
    get_clean_capital_settlement_notify_tran, update_notify_tran_at_dcs
from biztest.function.dcs.check_precharge import check_compensate_clean_precharge_clearing_tran, \
    check_clean_precharge_clearing_tran, check_clean_accrual_tran, check_clean_scenes_receive, \
    check_repay_after_compensate_precharge_clearing_tran
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz, get_four_params_rbiz_db, \
    wait_dcs_record_appear, run_dcs_task_until_disappear
from biztest.config.dcs.xxljob_config import capital_settlement_tasks, compensate_handle_tasks, repay_tasks, \
    noloan_compensate_handle_tasks, auto_settlement_handle_tasks, not_received_handle_tasks, buyback_handle_tasks
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan, get_repay_amount_rbiz, \
    update_asset_extend_ref_and_sub_order_type, set_up_the_asset_trans_for_compensate, insert_buyback
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    update_asset_tran_status_by_item_no_and_period
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count, scenes_receive, run_task_in_biz_dcs, \
    run_dcs_task_by_order_no
from biztest.interface.rbiz.rbiz_interface import asset_provision_settle, asset_bill_decrease, \
    combo_active_repay_without_no_loan, paysvr_callback, monitor_check
from biztest.util.easymock.rbiz.qinnong import RepayQinnongMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after, get_date_before_today
import common.global_const as gc


class TestDcsJinMeixinDaQin(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "jinmeixin_daqin"
    period_count = 12
    source_type = 'irr36_quanyi'  # irr36_quanyi(这个关联到小单合并还款会有问题) , apr36 , irr36
    principal = 800000
    interest = 5200
    period_one_amount = 16495

    @classmethod
    def setup_class(cls):
        cls.qn_mock = RepayQinnongMock(rbiz_mock)
        set_up_the_asset_trans_for_compensate()

    def setup_method(self):
        monitor_check()
        self.init(self.env_test)
        self.item_no = 'jmdq_' + get_item_no()
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(
            self.channel, self.four_element, self.item_no, count=self.period_count, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_jinmeixin_daqin
    def test_jinmeixin_daqin_qsq_advance_repay(self):
        print("====================提前还款，逾期前还款全部走资方====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_advance = (1,)
        # step 1 到期日往前推10天
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_advance)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_advance)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(merchant_key=order, transaction_status=2, channel_name="jinmeixin_daqin",
                            channel_message="走资方代扣")
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_advance)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_advance[0])
        print("=================清分完成后，提前还款，收取第一期利息，到期日结算==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_advance[0], period_advance[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_advance[0], period_advance[0], "advance", "jinmeixin_daqin",
                                                    "N", "",
                                                    expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # TODO  检查数据没有加，待优化

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_jinmeixin_daqin
    def test_jinmeixin_daqin_channel_normal_repay(self):
        print("====================正常还款，逾期前还款全部走资方====================")
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
        # 更新代扣记录为资方代扣通道
        for order in order_list:
            paysvr_callback(merchant_key=order, transaction_status=2, channel_name="jinmeixin_daqin",
                            channel_message="走资方代扣")
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        print("=================清分完成后，第一期正常还款，资方扣部分，我方扣一部分==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", "jinmeixin_daqin",
                                                    "N", "", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # TODO  检查数据没有加，待优化

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_jinmeixin_daqin
    def test_jinmeixin_daqin_early_settlement(self):
        print("====================第一期到期日提前结清（走资方代扣，biz-central推送提前结清）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        period_overdue = (1,)
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(merchant_key=order, transaction_status=2, channel_name="jinmeixin_daqin",
                            channel_message="走资方代扣")
        self.run_task_after_withhold_callback(order_list)
        # 走我方通道代扣成功
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # 同步到历史库
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_overdue)
        # biz-central推送提前结清
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    "jinmeixin_daqin", "Y", "",
                                                    get_date_after(expect_operate_at, day=4))
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # TODO  检查数据没有加，待优化

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_jinmeixin_daqin
    def test_jinmeixin_daqin_qsq_payoff_compensate(self):
        print("====================第一期到期日提前结清（走我方代扣，biz-central第一期推代偿，剩余期次推提前结清）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        period_overdue = (1,)
        self.change_asset_due_at(1, 3)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # 发起还款请求
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
        repay_run.run_clearing_jobs_post(repay_tasks, period_overdue)

        # biz-central推送第一期代偿
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[0], "compensate",
                                                    "qsq", "N", "",
                                                    get_date_after(expect_operate_at, day=4))
        repay_run.run_capital_settlement_task(capital_settlement_tasks)

        # biz-central推送提前结清，第二期收取部分利息
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[1], period_payoff[-1], "early_settlement",
                                                    "qsq", "Y", "",
                                                    get_date_after(expect_operate_at, day=4))
        # 将第二次推送的版本号改成比第一次的版本号大，不然会有问题
        notify_tran = get_clean_capital_settlement_notify_tran(self.item_no, period_payoff[1], 'new')
        update_notify_tran_at_dcs(self.item_no, notify_tran[0]["version"] - 10, period_payoff[0])
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # TODO 最后trans的数据没有检查

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_jinmeixin_daqin
    def test_jinmeixin_daqin_channel_payoff_last_period(self):
        print("====================最后一期提前结清走资方，biz-central推提前结清 ====================")
        # step 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        self.change_asset_due_at(-5, -10)
        update_asset_tran_status_by_item_no_and_period(self.item_no, period=self.period_count)
        update_asset_tran_status_by_item_no_and_period(self.item_num_no_loan, period=self.period_count)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # 发起还款请求
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(merchant_key=order, transaction_status=2, channel_name="jinmeixin_daqin",
                            channel_message="走资方代扣")
        self.run_task_after_withhold_callback(order_list)

        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 2 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        run_dcs_task_by_count(self.item_no, 15)

        # biz-central最后一期推送代偿
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', 12, 12)
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(12, 12, "early_settlement", "jinmeixin_daqin", "N", "",
                                                    get_date_after(expect_operate_at, day=4))
        repay_run.run_capital_settlement_task(capital_settlement_tasks)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_jinmeixin_daqin
    def test_jinmeixin_daqin_qsq_payoff_last_period(self):
        print("====================最后一期提前结清走我方，biz-central推代偿 ====================")
        # step 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        self.change_asset_due_at(-5, -10)
        update_asset_tran_status_by_item_no_and_period(self.item_no, period=self.period_count)
        update_asset_tran_status_by_item_no_and_period(self.item_num_no_loan, period=self.period_count)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 2 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        run_dcs_task_by_count(self.item_no, 15)

        # biz-central最后一期推送代偿
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', 12, 12)
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(12, 12, "compensate", "qsq", "N", "",
                                                    get_date_after(expect_operate_at, day=4))
        repay_run.run_capital_settlement_task(capital_settlement_tasks)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_jinmeixin_daqin
    def test_jinmeixin_daqin_buyback(self):
        print("====================回购，待更新？？？？====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        # 修改放款日期 到期日
        buyback_period = (3,)
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
        print("================= 回购，报表日期（财务应计结算日期）=银行还款日期日==================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "buyback", "qsq", "Over",
                                                    "", get_date_before_today()[:10])
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 回购后发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, buyback_period)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, buyback_period)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2, "baidu_tq3_quick")
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, buyback_period)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_jinmeixin_daqin
    def test_jinmeixin_daqin_compensate_after_repay(self):
        print("====================第一期到期日代偿（jinmeixin_daqinshi D+3代偿） 代偿后还款====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_overdue = (1,)
        # step 1 到期日往前推1月3天，jinmeixin_daqinshi D+3代偿
        self.change_asset_due_at(-1, -3)
        # step 2 刷罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        print("================开始大单代偿清分（制造先代偿再走资方还款的场景）================")
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_overdue)

        print("================清分完成后，补充流程，由biz-central推送代偿消息=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_overdue[0], period_overdue[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_overdue[0], period_overdue[0], "compensate", "", "N",
                                                    "", get_date_after(expect_operate_at, day=1))

        print("=================先发送代偿的消息，再进行代偿清分，清分后才会生成task==================")
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 2)
        # step 5 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        # 发起还款请求
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # 走我方通道代扣成功
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        set_withhold_history(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_overdue)
        # TODO 最后trans的数据没有检查

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_jinmeixin_daqin
    def test_jinmeixin_daqin_qsq_normal_repay_offline(self):
        print("====================第一期正常还款，资方无法扣款时，白名单走我方全额扣，biz_central推送类型为线下还款offline====================")
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
            paysvr_callback(order, 2, "baidu_tq3_quick")
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        print("=================清分完成后，第一期正常还款，全部走我方==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "offline", "qsq", "N", "",
                                                    expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # TODO 最后trans的数据没有检查

# TODO  1. 可能有贴息(暂没有写贴息案例，等还款)  2.资方代扣部分成功，剩余部分逾期后代偿
