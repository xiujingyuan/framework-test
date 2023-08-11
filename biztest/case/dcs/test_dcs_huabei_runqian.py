import time, pytest
# capital7环境就用 xxljob_config ，capital6环境就用 xxljob_config2 。
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import buyback_handle_tasks, capital_settlement_tasks, compensate_handle_tasks, \
    repay_tasks
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan, insert_buyback
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz, delete_null_biz, get_four_params_rbiz_db
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period
from biztest.interface.rbiz.rbiz_interface import paysvr_callback, monitor_check
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after, get_date_before_today
import common.global_const as gc


class TestDcsHuabeiRunqian(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "huabei_runqian"
    period_count = 12

    def setup_method(self):
        monitor_check()
        self.init(self.env_test)
        self.item_no = 'ha_hbrq_' + get_item_no()[:16]
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, count=self.period_count, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hbrq
    def test_huabeiruiqian_normal_repay(self):
        print("====================第一期正常还款（只会有我方代扣）====================")
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
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 

        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        check_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        check_trans.check_trans_all()
        check_trans.check_trans_amount()
        print("华北润乾，代偿+正常还款，报表日期（财务应计结算日期）=还款计划到期日（节假日后3天为节假日最后一天，节假日前几天为节前最后一个工作日）")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = get_date_after(repay_plan[0]["asset_tran_due_at"][:10], day=0)
        # step 2 模拟biz_central调用接口，这里的compensate表示推送的是代偿
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "compensate", "qsq", "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据，这里的repay表示原本的清分是还款清分
        check_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hbrq
    @pytest.mark.DCS_test_buyback
    def test_huabei_runqian_buyback(self):
        print("====================回购====================")
        buyback_period = (3, 4, 5, 6)
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
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
        # 检查数据
        for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'compensate', 'qsq')
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'compensate', 'qsq')
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
        print("=================华北润乾，回购-本息，报表日期（财务应计结算日期）=回购当日==================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "buyback", "qsq", "Y",
                                                    "guarantee", get_date_before_today()[:10])
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(buyback_period[0], capital_i, "compensate", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hbrq
    def test_huabei_runqian_early_settlement_payoff(self):
        print("=================第一期提前结清=================")
        # 检查放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
        print("================（还款走提前结清的场景）================")
        # 发起主动代扣 提前结清
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 

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
        print("==============华北润乾，提前结清-本息，报表日期（财务应计结算日期）=还款T+1（若T+1大于到期日需做拆分）==============")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement", "qsq", "N",
                                                    "guarantee", get_date_after(expect_operate_at, day=4))
        # 处理biz-central的消息
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "guarantee")

    @pytest.mark.DCS_test_0629
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hbrq
    def test_huabei_runqian_compensate_payoff(self):
        print("=================第一期逾期次日开始提前结清=================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_compensate = (1,)
        period_payoff = (1, 2, 3, 4, 5, 6)

        print("================（制造先还款再代偿的场景）================")
        # step 1 到期日往前推1月零1天
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        # 发起主动代扣 提前结清
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 

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
        print("==============华北润乾，代偿==============")
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_compensate)
        # 检查代偿数据
        capital = get_capital_biz(self.item_no, period_compensate[0])
        cleck_final = CheckDcsFinal(self.item_no, period_compensate[0], 'compensate', 'qsq')
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_compensate[0], 'compensate', 'qsq')
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()
        print("==============华北润乾，先代偿再结清==============")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_compensate[0], period_compensate[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_compensate[0], period_compensate[0], "compensate", "qsq",
                                                    "N", "guarantee", expect_operate_at)
        # 处理biz-central的消息
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_compensate[0], period_compensate[0], "compensate",
                                                     "guarantee")
        print("==============华北润乾，先代偿再结清，代偿收当期全额，结清收当期全额==============")
        # step 1 查找预计结算时间
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[1], period_payoff[-1], "early_settlement", "qsq", "N",
                                                    "guarantee", get_date_after(expect_operate_at, day=4))
        # 处理biz-central的消息
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[1], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[1], capital_i, "repay", "guarantee")
