import json, pytest, time
# capital7环境就用 xxljob_config ，capital6环境就用 xxljob_config2 。
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import buyback_handle_tasks, capital_settlement_tasks, compensate_handle_tasks, \
    repay_tasks
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import  update_repay_paysvr_config
from biztest.function.dcs.biz_database import get_capital_biz, insert_buyback, get_one_repay_plan, get_repay_amount_rbiz
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, get_four_params_rbiz_db, check_repay_biz, delete_null_biz
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.interface.rbiz.rbiz_interface import asset_bill_decrease, combo_active_repay_without_no_loan, \
    paysvr_callback, monitor_check
from biztest.util.easymock.rbiz.weishenma_daxinganling import RepayWeishenmaMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_before_today
import common.global_const as gc


class TestDcsWeiShenMaDaXingAnLing(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "weishenma_daxinganling"
    period_count = 6

    @classmethod
    def setup_class(cls):
        # 更新kv
        monitor_check()
        update_repay_weishenma_config(mock_project['rbiz_auto_test']['id'])
        cls.wsmmock = RepayWeishenmaMock(rbiz_mock)

    @classmethod
    def teardown_class(cls):
        update_repay_weishenma_config()

    def setup_method(self):
        self.init(self.env_test)
        self.item_no = 'wsm_' + get_item_no()[:16]
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, count=self.period_count, script_system='dcs')

        advance_time_limit = {"startTime": "00:00:00", "endTime": "22:00:00"}
        normal_time_limit = {"startTime": "00:00:00", "endTime": "22:00:00"}
        settle_time = "00:00:00,22:00:00"
        update_repay_weishenma_config(mock_project['rbiz_auto_test']['id'], settle_time=settle_time,
                                      normal_time_limit=normal_time_limit, advance_time_limit=advance_time_limit)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_daxinganling_chargeback(self):
        print("====================退单====================")
        # self.item_no, self.item_num_no_loan = "hei_2020162475536332_wsm", "hei_2020162475536332_wsm_noloan"
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        buyback_period = (1, 2, 3, 4, 5, 6)
        # step 1 到期日往前推2天
        self.change_asset_due_at(0, -2)
        # 直接往 buyback 表插入数据
        insert_buyback(self.item_no, self.period_count, 800000, buyback_period[0], self.channel, type='chargeback')
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
        print("=================微神马，退单，报表日期（财务应计结算日期）=退单当日==================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "chargeback", "qsq", "Y",
                                                    "guarantee", get_date_before_today()[:10])
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(buyback_period[0], capital_i, "compensate", "guarantee")

    @pytest.mark.DCS_test_0629
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_daxinganling_buyback(self):
        print("====================回购====================")
        # self.item_no, self.item_num_no_loan = "hei_2020162475560422_wsm", "hei_2020162475560422_wsm_noloan"
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        # 修改放款日期 到期日
        buyback_period = (3, 4, 5, 6)
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
        print("=================微神马，回购，报表日期（财务应计结算日期）=银行还款日期日==================")
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
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_channel_advance_repay(self):
        print("====================第一期提前还款（资方代扣本息／我方代扣费）====================")
        period_advance = (1,)
        # step 1 检查大小单放款情况
        check_asset_grant(self.item_no)
        # step 2 微神马发起单期代扣请求
        self.wsmmock.active_repay_apply_success(self.item_no, period_advance[0])
        # step 3 放款日往前推10天
        self.change_asset_due_at(0, -10)
        # step 4 微神马代扣查询，状态为1表示成功
        repay_principal_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_advance[0], period_advance[-1])
        repay_interest_plan = get_one_repay_plan(self.item_no, 'repayinterest', period_advance[0], period_advance[-1])
        capital_amount = repay_principal_plan[0]["asset_tran_amount"] + repay_interest_plan[0][
            "asset_tran_amount"]
        self.wsmmock.update_active_repay_query("1", str(capital_amount))
        # step 5 发起代扣申请
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_advance)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_advance)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 6 执行rbiz的task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 7 检查biz的帐信（同步代扣记录）
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_advance)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_advance[0])
        cleck_final = CheckDcsFinal(self.item_no, period_advance[0], 'repay', "qsq_channel")
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_advance[0], 'repay', "qsq_channel")
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()
        print("=================微神马，客户提前还款-资方通道，报表日期（财务应计结算日期）=还款计划到期日==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_advance[0], period_advance[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_advance[0], period_advance[0], "advance", self.channel, "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_advance[0], period_advance[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_channel_normal_repay(self):
        print("====================第一期正常还款（资方代扣本息／我方代扣费）====================")
        period_normal = (1,)
        normal_time_limit = {"startTime": "00:00:00", "endTime": "23:00:00"}
        update_repay_weishenma_config(mock_project['rbiz_auto_test']['id'], normal_time_limit=normal_time_limit)
        # step 1 检查大小单放款情况
        check_asset_grant(self.item_no)
        # step 2 微神马发起单期代扣请求
        self.wsmmock.active_repay_apply_success(self.item_no, period_normal[0])
        # step 3 放款日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 4 微神马代扣查询，状态为1表示成功
        repay_principal_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[-1])
        repay_interest_plan = get_one_repay_plan(self.item_no, 'repayinterest', period_normal[0], period_normal[-1])
        capital_amount = repay_principal_plan[0]["asset_tran_amount"] + repay_interest_plan[0][
            "asset_tran_amount"]
        self.wsmmock.update_active_repay_query("1", str(capital_amount))
        # step 5 发起代扣申请
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 6 执行rbiz的task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 7 检查biz的帐信（同步代扣记录）
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
        print("=================微神马，客户正常还款-资方通道，报表日期（财务应计结算日期）=还款计划到期日==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", self.channel, "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.DCS_test_0629
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_qsq_normal_repay(self):
        print("====================第一期正常还款（资方代扣失败／全部我方代扣）====================")
        period_normal = (1,)

        check_asset_grant(self.item_no)
        # step 2 微神马发起单期代扣请求
        self.wsmmock.active_repay_apply_success(self.item_no, period_normal[0])
        # step 3 放款日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 4 微神马代扣查询，状态为2表示失败
        repay_principal_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[-1])
        repay_interest_plan = get_one_repay_plan(self.item_no, 'repayinterest', period_normal[0], period_normal[-1])
        capital_amount = repay_principal_plan[0]["asset_tran_amount"] + repay_interest_plan[0][
            "asset_tran_amount"]
        self.wsmmock.update_active_repay_query("2", str(capital_amount))
        # step 5 发起代扣申请
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 3)
        self.run_task_after_withhold_callback(order_list)
        # step 8 第二次发起主动代扣
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 9 执行rbiz的task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 7 检查biz的帐信（同步代扣记录）
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
        print("=================微神马，客户正常还款-我方通道，报表日期（财务应计结算日期）=还款计划到期日==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", "qsq", "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_channel_payoff(self):
        print("====================第一期提前结清====================")
        # self.item_no, self.item_num_no_loan = "hei_2020162475528492_wsm", "hei_2020162475528492_wsm_noloan"
        # self.four_element = get_four_params_rbiz_db(self.item_no)
        period_payoff = (1, 2, 3, 4, 5, 6)

        # step 1 检查大小单放款情况
        check_asset_grant(self.item_no)
        # step 2 微神马发起提前结清请求
        self.wsmmock.early_settle_apply_success(self.item_no, period_payoff[0])
        # step 3 放款日往前推10天
        self.change_asset_due_at(0, -10)
        # step 4 微神马提前结清试算
        principal_amount = 800000
        capital_withhold_amount = 801000
        self.wsmmock.update_active_settle_trail(principal_amount, capital_withhold_amount)
        # step 4 微神马代扣查询，状态为1表示成功
        self.wsmmock.update_active_repay_query("1", str(capital_withhold_amount))
        # step 5 发起代扣申请
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 6 执行rbiz的task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 7 检查biz的帐信（同步代扣记录）
        check_repay_biz(self.item_no)
        # 开始大单还款清分，period_payoff 主要是监控task生成的数量，因为这是资方代扣，会有两条代扣记录，两个bigRepayClearing，就会有12个task
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff * 2)
        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_final.check_final_all()
            # cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
        print("=================微神马，提前结清-资方通道，报表日期（财务应计结算日期）=银行还款日期==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "Y", "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "guarantee")

    @pytest.mark.DCS_test_0629
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_channel_qsq_fail_payoff(self):
        print("====================第一期提前结清，资方代扣成功，我方代扣失败，担保费清分从代偿变为提前结清====================")

        period_payoff = (1, 2, 3, 4, 5, 6)

        # step 1 检查大小单放款情况
        check_asset_grant(self.item_no)
        # step 2 微神马发起提前结清请求
        self.wsmmock.early_settle_apply_success(self.item_no, period_payoff[0])
        # step 3 放款日往前推10天
        self.change_asset_due_at(0, -10)
        principal_amount = 800000
        capital_withhold_amount = 801000
        self.wsmmock.update_active_settle_trail(principal_amount, capital_withhold_amount)
        # step 4 微神马代扣查询，状态为1表示成功
        self.wsmmock.update_active_repay_query("1", str(capital_withhold_amount))
        # step 5 发起代扣申请
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_no_capital = resp_repay["data"]["project_list"][0]["order_no"]
        order_no_our = resp_repay["data"]["project_list"][1]["order_no"]
        order_no_noloan = resp_repay["data"]["project_list"][2]["order_no"]
        paysvr_callback(order_no_capital, 2)
        paysvr_callback(order_no_our, 3)
        paysvr_callback(order_no_noloan, 3)
        # step 6 执行rbiz代扣失败后的task
        self.run_task_after_withhold_callback([order_no_capital, order_no_our, order_no_noloan])
        self.run_all_msg_after_repay_success

        # step 7 检查biz的帐信（同步代扣记录）
        check_repay_biz(self.item_no)
        # 开始大单还款清分，period_payoff 主要是监控task生成的数量，因为我方代扣失败，就只有1条代扣记录，1个bigRepayClearing，就会有6个task
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)
        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_final.check_final_all()
            # cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_trans.check_trans_all()
            # cleck_trans.check_trans_amount()
        period_compensate = (1,)
        # step 1 使第一期逾期
        self.change_asset_due_at(-1, -1)
        # step 2 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_compensate)
        # 暂时不检查代偿的数据，但是此时需要人工检查一下利息的代偿金额
        print("==========================微神马，担保费清分从代偿变为提前结清========================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "Y", "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_compensate[0], period_compensate[0], "compensate",
                                                     "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_channel_payoff_capital(self):
        print("====================第一期提前结清，需要给资方补贴利息====================")
        period_payoff = (1, 2, 3, 4, 5, 6)

        # step 1 检查大小单放款情况
        check_asset_grant(self.item_no)
        # step 2 微神马发起提前结清请求
        self.wsmmock.early_settle_apply_success(self.item_no, period_payoff[0])
        # step 3 放款日往前推10天
        self.change_asset_due_at(0, -10)
        # step 4 微神马提前结清试算
        principal_amount = 800000
        capital_withhold_amount = 801000
        self.wsmmock.update_active_settle_trail(principal_amount, capital_withhold_amount)
        # step 4 微神马代扣查询，状态为1表示成功
        self.wsmmock.update_active_repay_query("1", str(capital_withhold_amount))
        # step 5 发起代扣申请
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 6 执行rbiz的task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 7 检查biz的帐信（同步代扣记录）
        check_repay_biz(self.item_no)
        # 开始大单还款清分，period_payoff 主要是监控task生成的数量，因为这是资方代扣，会有两条代扣记录，两个bigRepayClearing，就会有12个task
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff * 2)
        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_final.check_final_all()
            # cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
        print("=================微神马，提前结清-资方通道，报表日期（财务应计结算日期）=特殊==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "Y", "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_channel_payoff_inter(self):
        print("====================第一期提前结清，需要退我方补贴利息====================")
        period_payoff = (1, 2, 3, 4, 5, 6)

        # step 1 检查大小单放款情况
        check_asset_grant(self.item_no)
        # step 2 微神马发起提前结清请求
        self.wsmmock.early_settle_apply_success(self.item_no, period_payoff[0])
        # step 3 放款日往前推10天
        self.change_asset_due_at(0, -10)
        # step 4 微神马提前结清试算
        principal_amount = 800000
        capital_withhold_amount = 802500
        self.wsmmock.update_active_settle_trail(principal_amount, capital_withhold_amount)
        # step 4 微神马代扣查询，状态为1表示成功
        self.wsmmock.update_active_repay_query("1", str(capital_withhold_amount))
        # step 5 发起代扣申请
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 6 执行rbiz的task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 7 检查biz的帐信（同步代扣记录）
        check_repay_biz(self.item_no)
        # 开始大单还款清分，period_payoff 主要是监控task生成的数量，因为这是资方代扣，会有两条代扣记录，两个bigRepayClearing，就会有12个task
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff * 2)
        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_final.check_final_all()
            # cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq_channel")
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
        print("=================微神马，提前结清-资方通道，报表日期（财务应计结算日期）=特殊==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement",
                                                    self.channel, "Y", "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据，这个第一期的数据先人工检查一下，后续再补充
        for capital_i in range(period_payoff[1], period_payoff[-1] + 1):
            cleck_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_wsm_decrease_normal_repay(self):
        print("====================（第一期减免部分费用 本金未还完 用户第2次还完 推还款的场景）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)

        # step 2 减免后应还为750332
        asset_bill_decrease(self.item_no, 750332)
        # step 3 执行还款的msg
        self.run_task_after_loan_repay(self.item_no)
        self.run_account_msg_after_repaid()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)

        # 还款-还剩余部分
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        self.four_element = get_four_params_rbiz_db(self.item_no)
        resp_repay = self.repay_only_one_project_success(asset_tran_amount["asset_tran_balance_amount"], self.item_no)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 4 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)

        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        cleck_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()
        print("=================微神马，客户正常还款-我方通道，报表日期（财务应计结算日期）=还款计划到期日==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", "qsq", "N",
                                                    "guarantee", expect_operate_at)
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        cleck_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_weishenma
    def test_weishenma_overdue_repay_and_compensate(self):
        print("====================第一期逾期还款 然后代偿====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_overdue = (1,)

        self.change_asset_due_at(-1, -1)
        # step 2 刷罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_overdue)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_overdue)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 6 执行rbiz的task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 7 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_overdue)
        # 检查清分的数据 逾期后资方代扣
        capital = get_capital_biz(self.item_no, period_overdue[0])
        check_final = CheckDcsFinal(self.item_no, period_overdue[0], 'repay', "qsq")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_overdue[0], 'repay', "qsq")
        check_trans.check_trans_all()
        check_trans.check_trans_amount()

        print("================清分完成后，补充流程，代偿第1期=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_overdue[0], period_overdue[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_overdue[0], period_overdue[0], "compensate", "", "N",
                                                    "guarantee", expect_operate_at)

        print("================开始大单代偿清分（制造先还款再代偿的场景）================")
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

        print("=================先发送代偿的消息，再进行代偿清分，清分后才会生成task==================")
        # step 3 执行task
        repay_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_overdue[0], period_overdue[0], "compensate", "guarantee")
