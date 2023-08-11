import pytest
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import compensate_handle_tasks, repay_tasks, capital_settlement_tasks, \
    buyback_handle_tasks
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_zhongke_hegang_config
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan, uodate_biz_withhold_to_channel, \
    insert_buyback
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.capital_database import update_notify_tran_at_dcs, get_clean_capital_settlement_notify_tran
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    update_asset_tran_status_by_item_no_and_period
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count
from biztest.interface.rbiz.rbiz_interface import paysvr_callback, monitor_check
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after
import common.global_const as gc
from biztest.util.tools.tools import get_date_before_today


class TestDcshongkeegang(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    country = gc.COUNTRY
    channel = "zhongke_hegang"
    period_count = 12
    grant_principal = 800000
    first_period_interest = 16940  # 第一期息费

    def setup_method(self):
        monitor_check()
        self.init(self.env_test)
        self.item_no = 'zkhg_' + get_item_no()
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_channel_normal_repay(self):
        print("====================第一期正常还款（资方扣全额）====================")
        # setp 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_normal = (1,)
        # step 2 到期日往前推1月 & 主动还款
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        # 发起还款请求
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        check_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "zhongke_hegang")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "zhongke_hegang")
        # 先不检查，因为consult和reserve的出户不一样是v_zhongke_hegang_baofu_hk
        # check_trans.check_trans_all()
        check_trans.check_trans_amount()

        print("================清分完成后，补充流程，提前还款走资方推normal ================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal",
                                                    "zhongke_hegang", "N", "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 2)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")
        # TODO 如何检查咨询服务费和风险保障金的出户是唯渡："repay_before_compensate_transfer_out":"v_zhongke_hegang_baofu_hk"

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_qsq_normal_repay(self):
        print("====================第一期正常还款（我方扣全额）====================")
        # setp 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_normal = (1,)
        # step 2 到期日往前推1月 & 主动还款
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        # 发起还款请求 加白名单走我方扣
        update_repay_zhongke_hegang_config(self.item_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        check_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        check_trans.check_trans_all()  # 走我方的出户都是充值户
        check_trans.check_trans_amount()

        print("================清分完成后，补充流程，提前还款走我方推compensate  =================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "compensate",
                                                    "qsq", "N", "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 2)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_qsq_advance_repay_compensate(self):
        print("====================第一期提前还款（中科鹤岗提前还款全部走我方）====================")
        # setp 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_normal = (1,)
        # step 2 到期日往前推1月 & 主动还款
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        # 发起还款请求 加白名单走我方扣
        update_repay_zhongke_hegang_config(self.item_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # 走我方通道代扣成功
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        check_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        check_trans.check_trans_all()  # 走我方的出户都是充值户
        check_trans.check_trans_amount()

        print("================清分完成后，补充流程，提前还款走我方推compensate，出户是拨备  =================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        # 提前还款  如果到期日是工作日且走我方，推线下还款offline
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "compensate",
                                                    "qsq", "N", "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 2)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")
        # TODO 最后trans的数据没有检查，提前还款走我方推compensate，出户是拨备

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_qsq_advance_repay_offline(self):
        print("====================第一期提前还款（中科鹤岗提前还款全部走我方）====================")
        # setp 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_normal = (1,)
        # step 2 到期日往前推1月 & 主动还款
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        # 发起还款请求 加白名单走我方扣
        update_repay_zhongke_hegang_config(self.item_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # 走我方通道代扣成功
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        # capital = get_capital_biz(self.item_no, period_normal[0])
        # check_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        # check_final.check_final_all()
        # check_final.check_final_amount(capital)
        # check_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        # check_trans.check_trans_all()  # 走我方的出户都是充值户
        # check_trans.check_trans_amount()

        print("================清分完成后，补充流程，提前还款走我方推offline，出户是归集户  =================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        # 提前还款  如果到期日是工作日且走我方，推线下还款offline
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "offline",
                                                    "qsq", "N", "guarantee", expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 2)
        # step 4 检查数据
        # check_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")
        # TODO 最后trans的数据没有检查，提前还款走我方推offline，出户是归集户

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_compensate_after_repay(self):
        print("====================第一期到期日代偿 代偿后还款====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_overdue = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, -1)
        # step 2 刷罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        print("================开始大单代偿清分（制造先代偿再走资方还款的场景）================")
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_overdue)
        # 检查代偿清分的数据
        capital = get_capital_biz(self.item_no, period_overdue[0])
        check_final = CheckDcsFinal(self.item_no, period_overdue[0], 'compensate', 'qsq')
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_overdue[0], 'compensate', 'qsq')
        check_trans.check_trans_all()
        check_trans.check_trans_amount()

        print("================清分完成后，补充流程，由biz-central推送代偿消息=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_overdue[0], period_overdue[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_overdue[0], period_overdue[0], "compensate", "", "N",
                                                    "guarantee", get_date_after(expect_operate_at, day=1))

        print("=================先发送代偿的消息，再进行代偿清分，清分后才会生成task==================")
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 2)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_overdue[0], period_overdue[0], "compensate", "guarantee")

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
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_overdue)
        # TODO 最后trans的数据没有检查

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_qsq_payoff(self):
        print("====================第一期到期日提前结清（走我方代扣，biz-central推送提前结清）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        period_overdue = (1,)
        self.change_asset_due_at(0, -10)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # 发起还款请求 加白名单走我方扣
        update_repay_zhongke_hegang_config(self.item_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
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

        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            check_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq")
            check_final.check_final_all()
            # check_final.check_final_amount(capital)
            check_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', self.channel)
            check_trans.check_trans_all()
            check_trans.check_trans_amount()
        # biz-central推送提前结清
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    "qsq", "N", "guarantee",
                                                    get_date_after(expect_operate_at, day=4))
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            check_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "guarantee")
        # TODO 最后trans的数据没有检查

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_qsq_payoff_compensate(self):
        print("====================第一期到期日提前结清（走我方代扣，biz-central先推代偿再推提前结清）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        period_overdue = (1,)
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # 发起还款请求 加白名单走我方扣
        update_repay_zhongke_hegang_config(self.item_no)
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

        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            check_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq")
            check_final.check_final_all()
            # check_final.check_final_amount(capital)
            check_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq")
            check_trans.check_trans_all()
            check_trans.check_trans_amount()

        # biz-central推送第一期代偿
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[0], "compensate",
                                                    "qsq", "N", "guarantee",
                                                    get_date_after(expect_operate_at, day=4))
        repay_run.run_capital_settlement_task(capital_settlement_tasks)

        # biz-central推送提前结清，第二期收取部分利息
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[1], period_payoff[-1], "early_settlement",
                                                    "qsq", "Y", "guarantee",
                                                    get_date_after(expect_operate_at, day=4))
        # 将第二次推送的版本号改成比第一次的版本号大，不然会有问题
        notify_tran = get_clean_capital_settlement_notify_tran(self.item_no, period_payoff[1], 'new')
        update_notify_tran_at_dcs(self.item_no, notify_tran[0]["version"] - 10, period_payoff[0])
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # TODO 最后trans的数据没有检查

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_channel_payoff_last_period(self):
        print("====================最后一期提前结清走资方，biz-central推提前结清 ====================")
        # step 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        self.change_asset_due_at(-11, -10)
        update_asset_tran_status_by_item_no_and_period(self.item_no)
        update_asset_tran_status_by_item_no_and_period(self.item_num_no_loan)
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
        advanced_clearing.capital_settlement_notify(12, 12, "early_settlement", "zhongke_hegang", "N", "guarantee",
                                                    get_date_after(expect_operate_at, day=4))
        repay_run.run_capital_settlement_task(capital_settlement_tasks)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_qsq_payoff_last_period(self):
        print("====================最后一期提前结清走我方，biz-central推代偿，不确定是否有贴息，目前有贴息流程会无法继续，需要修改配置才可以 ====================")
        # step 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        self.change_asset_due_at(-11, -10)
        update_asset_tran_status_by_item_no_and_period(self.item_no)
        update_asset_tran_status_by_item_no_and_period(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # 发起还款请求 加白名单走我方扣
        update_repay_zhongke_hegang_config(self.item_no)
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
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, 12)
        check_final = CheckDcsFinal(self.item_no, 12, 'repay', 'qsq')
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, 12, 'repay', 'qsq')
        check_trans.check_trans_all()
        check_trans.check_trans_amount()

        # biz-central最后一期推送代偿
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', 12, 12)
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(12, 12, "compensate", "qsq", "N", "guarantee",
                                                    get_date_after(expect_operate_at, day=4))
        repay_run.run_capital_settlement_task(capital_settlement_tasks)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_qsq_payoff_chargeback(self):
        print("====================  退单后走我方代扣  ====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        buyback_period = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        # step 1 到期日往前推2天
        self.change_asset_due_at(0, -2)
        # 直接往 buyback 表插入数据
        insert_buyback(self.item_no, self.period_count, self.grant_principal, buyback_period[0], self.channel,
                       type='chargeback')
        # 执行 退单脚本
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(buyback_handle_tasks, buyback_period)
        # 检查数据
        for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'compensate', 'qsq')
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'compensate', 'qsq')
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
        print("=================  退单日期？导入的时间  ==================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "chargeback", "qsq", "Y",
                                                    "guarantee", get_date_before_today()[:10])
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(buyback_period[0], capital_i, "compensate", "guarantee")

        # 退单后走我方提前结清，这时候属于代偿后还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # 发起主动代扣 加白名单的方式
        update_repay_zhongke_hegang_config(self.item_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        run_dcs_task_by_count(self.item_no, 15)
        # TODO 校验

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_channel_and_qsq_payoff(self):
        print("====================第一期到期日前提前结清（资方代扣成功。我方代扣成功）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # TODO 等还款上线后调整

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_qsq_payoff_chargeback2(self):
        print("====================  退单后走我方代扣  ====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        buyback_period = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        # step 1 到期日往前推2天
        self.change_asset_due_at(0, -2)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # 发起主动代扣 白名单的方式
        update_repay_zhongke_hegang_config(self.item_no)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        run_dcs_task_by_count(self.item_no, 15)

        # 直接往 buyback 表插入数据
        insert_buyback(self.item_no, self.period_count, self.grant_principal, buyback_period[0], self.channel,
                       type='chargeback')
        # 执行 退单脚本
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(buyback_handle_tasks, buyback_period)
        # 检查数据
        for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'compensate', 'qsq')
            # cleck_final.check_final_all()
            # cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'compensate', 'qsq')
            # cleck_trans.check_trans_all()
            # cleck_trans.check_trans_amount()
        print("=================  退单日期？导入的时间  ==================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "chargeback", "qsq", "Y",
                                                    "guarantee", get_date_before_today()[:10])
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_zhongke_hegang
    def test_zhongke_hegang_repay_compensate_fail(self):
        print("==================== 第一期到期日代偿失败：跑代偿时rbiz已经还款，但数据还没有同步到biz，应不生成代偿====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_overdue = (1,)
        # step 1 到期日改为当天
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        # 发起还款请求
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        #不执行任务就是为了不同步到biz，让biz和rbiz两边状态不一致
        self.run_task_after_withhold_callback(order_list)

        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, -1)
        print("================ 跑代偿时rbiz已经还款，但数据还没有同步到biz，应不生成代偿 ================")
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_overdue)
        # 检查代偿清分的数据
        # capital = get_capital_biz(self.item_no, period_overdue[0])
        # check_final = CheckDcsFinal(self.item_no, period_overdue[0], 'compensate', 'qsq')
        # check_final.check_final_all()
        # check_final.check_final_amount(capital)
        # check_trans = CheckDcsTrans(self.item_no, period_overdue[0], 'compensate', 'qsq')
        # check_trans.check_trans_all()
        # check_trans.check_trans_amount()
