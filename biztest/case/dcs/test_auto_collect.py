import pytest

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.dcs_nacos_config import update_nacos_dcs_payment_cost_config, update_nacos_dcs_deposit_config, \
    update_nacos_dcs_collect_rule
from biztest.config.dcs.xxljob_config import compensate_handle_tasks, repay_tasks, capital_settlement_tasks
from biztest.config.easymock.easymock_config import rbiz_mock, mock_project, global_payment_easy_mock_phl
from biztest.function.biz.biz_db_function import set_withhold_history
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan, insert_buyback
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.capital_database import update_dcs_china_task_next_run_at, \
    update_clean_withdraw_order_tally_no
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz, check_CleanWithdrawOrder, \
    check_deal_orderAndtrade
from biztest.function.dcs.dcs_db_function import get_dcs_clean_deposit_withdraw_order, get_dcs_clean_generic_deal_trade, \
    get_dcs_clean_withhold_concentration_info, get_dcs_clean_withhold_concentration_info_by_item_no
from biztest.function.dcs.dcs_run_xxljob_china import DcsRunXxlJobChina
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_info_by_item_no, \
    get_asset_tran_balance_amount_by_item_no_and_period, update_asset_tran_status_by_item_no_and_period, time
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count, update_deposit_orderandtrade_and_run_task
from biztest.interface.rbiz.rbiz_interface import paysvr_callback, monitor_check
from biztest.util.easymock.dcs_mock import DcsMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after, get_date_before_today
import common.global_const as gc

"""
    自动归集流程： 1.获取代扣记录 2.归集：记账、代付
    自动归集相关表：clean_withhold_concentration、clean_withdraw_order、clean_generic_deal_order、clean_generic_deal_trade
    大小单分归集：大单ht_tengqiao归集金额80502、小单qs_qianjingjing归集金额10318、默认归集没有成本
    author: fangchangfang
    date: 2022-12-23
"""


class TestDcsAutoCollect(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "zhongbang_haoyue_rl" #hebei_jiahexing_ts
    period_count = 12
    source_type = 'apr36'  # irr36_quanyi(这个关联到小单合并还款会有问题) , apr36 , irr36
    principal = 800000
    interest = 5200
    period_one_amount = 16495

    # 每个类的前置条件
    @classmethod
    def setup_class(self):
        monitor_check()
        # 支付走mock
        self.dcs_mock = DcsMock(global_payment_easy_mock_phl)
        self.withhold_channel = "sumpay_qjj_protocol"
        self.collect_channel = "qsq_sumpay_qjj_protocol"
        self.query_paysvr_commnet_channel = "qsq_yeepay_hange_protocol"
        self.ht_channelCode = "v_qjj_hk_ht_tengqiao"
        self.qs_channelCode = "v_tengqiao_hk_qs_tengqiao"
        self.ht_deposit = "ht_tengqiao"
        self.qs_deposit = "qs_tengqiao"
        self.qs_qjj_deposit = "qs_qianjingjing"

    def setup_method(self):
        self.init(self.env_test)
        self.item_no = 'auto_dcs_' + get_item_no()
        self.four_element = get_four_element()
        update_dcs_china_task_next_run_at(status='close')
        update_nacos_dcs_payment_cost_config(payment_channel="test")  # 默认归集没有成本
        update_nacos_dcs_collect_rule()  # 归集存管指定
        update_nacos_dcs_deposit_config()  # 将qsq_sumpay_qjj_protocol配置为非异名代付
        update_clean_withdraw_order_tally_no()  # 修改clean_withdraw_order.tally_no保证同一天可以重跑
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, count=self.period_count, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_auto_collect
    def test_auto_collect_success(self):
        # TODO 检查为什么小单没有channel_code
        print("====================造代扣成功后大小单-自动归集的数据  2022.12.23调试成功====================")
        # setp 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        period_normal = (1,)
        # step 2 到期日往前推1月 & 主动还款
        # self.change_asset_due_at(-1, 0)
        # 尽量造逾期的数据-减少走资方的可能
        self.change_asset_due_at(-1, -5)  # 尽量造逾期的数据-减少走资方的可能
        # self.change_asset_due_at(0, -10)  # 代偿前还款
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2, channel_name=self.withhold_channel)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # 同步代扣记录到历史库
        set_withhold_history(self.item_no)
        set_withhold_history(self.item_num_no_loan)
        dcs_run = DcsRunXxlJobChina(self.item_no, self.channel)
        # 执行task
        for i in range(20):
            dcs_run.run_clearing_jobs_post("dbTaskJob")

        print("============代扣成功开始资金归集（大单默认归集的是华通存管只代付不记账、小单是qs存管代付且记账）==============")
        update_nacos_dcs_payment_cost_config(payment_channel="test")  # 默认归集没有成本
        dcs_run = DcsRunXxlJobChina(self.item_no, self.channel)
        dcs_run.run_clearing_jobs_post("biz_dcs_CollectD1Job")
        # 执行task
        today_orderno = get_date_before_today()[:10]
        run_dcs_task_by_count(today_orderno, count=5)
        # 开始执行大单自动归集-ht_tengqiao-只代付不记账
        clean_withhold_concentration_info = get_dcs_clean_withhold_concentration_info_by_item_no(self.item_no)
        orderNo = clean_withhold_concentration_info[0]["withdraw_order_no"]
        run_dcs_task_by_count(orderNo, count=4)
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(orderNo)
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(orderNo, count=4)
        # 归集完成，检查归集表状态
        check_CleanWithdrawOrder(business_no=orderNo, status='success', tally_status='init',
                                 withdraw_status='success', payment_channel=self.collect_channel,
                                 channel_code="v_tengqiao_hk_ht_tengqiao", deposit=self.ht_deposit, operate_type="auto",
                                 loan_channel="MergeWithdraw", withhold_channel=self.withhold_channel, memo="",
                                 amount=157614)
        # 每次只检查最新的一笔的状态，记账+代付、转账+提现
        check_deal_orderAndtrade(business_no=orderNo, status='success', from_business='COLLECT',
                                 order_type='paymentWithdraw',
                                 serial_no=deal_trade_info[0]["trade_no"])
        # 开始执行小单自动归集-qs_qianjingjing-先记账后代付
        clean_withhold_concentration_info = get_dcs_clean_withhold_concentration_info_by_item_no(self.item_num_no_loan)
        noloan_orderNo = clean_withhold_concentration_info[0]["withdraw_order_no"]
        run_dcs_task_by_count(noloan_orderNo, count=4)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(noloan_orderNo, count=4)
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(noloan_orderNo)
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(noloan_orderNo, count=4)
        # 归集完成，检查归集表状态
        check_CleanWithdrawOrder(business_no=noloan_orderNo, status='success', tally_status='init',
                                 withdraw_status='success', payment_channel=self.collect_channel,
                                 channel_code="v_tengqiao_hk_ht_tengqiao", deposit=self.ht_deposit, operate_type="auto",
                                 loan_channel="MergeWithdraw", withhold_channel=self.withhold_channel, memo="",
                                 amount=157614)
        # 每次只检查最新的一笔的状态，记账后代付、转账后提现
        check_deal_orderAndtrade(business_no=noloan_orderNo, status='success', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])

    def test_auto_collect_manual_find_asset(self):
        # 使用该用例时，需要指定大单和小单的资产编号--2022.12.23调试成功
        # 1.需要将大小单资产编号替换 2.删除大小单中clean_withhold_concentration对应记录 3.修改clean_withdraw_order.tally_no保证唯一
        print("============代扣成功开始资金归集（大单默认归集的是华通存管只代付不记账、小单是qs存管代付且记账）==============")
        update_nacos_dcs_payment_cost_config(payment_channel="test")  # 默认归集没有成本
        dcs_run = DcsRunXxlJobChina(self.item_no, self.channel)
        dcs_run.run_clearing_jobs_post("biz_dcs_CollectD1Job")
        # 执行task
        today_orderno = get_date_before_today()[:10]
        run_dcs_task_by_count(today_orderno, count=5)
        # 开始执行大单自动归集-ht_tengqiao-只代付不记账
        clean_withhold_concentration_info = get_dcs_clean_withhold_concentration_info_by_item_no(
            "auto_dcs_20221223151949953380")
        orderNo = clean_withhold_concentration_info[0]["withdraw_order_no"]
        run_dcs_task_by_count(orderNo, count=4)
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(orderNo)
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(orderNo, count=4)
        # 归集完成，检查归集表状态
        check_CleanWithdrawOrder(business_no=orderNo, status='success', tally_status='init',
                                 withdraw_status='success', payment_channel=self.collect_channel,
                                 channel_code="v_tengqiao_hk_ht_tengqiao", deposit=self.ht_deposit, operate_type="auto",
                                 loan_channel="MergeWithdraw", withhold_channel=self.withhold_channel, memo="",
                                 amount=80502)
        # 每次只检查最新的一笔的状态，记账+代付、转账+提现
        check_deal_orderAndtrade(business_no=orderNo, status='success', from_business='COLLECT',
                                 order_type='paymentWithdraw',
                                 serial_no=deal_trade_info[0]["trade_no"])
        # 开始执行小单自动归集-qs_qianjingjing-先记账后代付
        clean_withhold_concentration_info = get_dcs_clean_withhold_concentration_info_by_item_no(
            "auto_dcs_20221223151949953380_noloan")
        noloan_orderNo = clean_withhold_concentration_info[0]["withdraw_order_no"]
        run_dcs_task_by_count(noloan_orderNo, count=4)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(noloan_orderNo, count=4)
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(noloan_orderNo)
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(noloan_orderNo, count=4)
        # 归集完成，检查归集表状态

        check_CleanWithdrawOrder(business_no=noloan_orderNo, status='success', tally_status='success',
                                 withdraw_status='success', payment_channel=self.collect_channel,
                                 channel_code="", deposit=self.qs_qjj_deposit, operate_type="auto",
                                 loan_channel="MergeWithdraw", withhold_channel=self.withhold_channel, memo="",
                                 amount=10318)
        # 每次只检查最新的一笔的状态，记账后代付、转账后提现
        check_deal_orderAndtrade(business_no=noloan_orderNo, status='success', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_auto_collect
    def test_auto_collect_fail_retry_success(self):
        # TODO 待根据test_auto_collect_success用例调试
        print("====================造可以自动归集的数据====================")

        print("============开始资金归集==============")

        print("====================记账撤销成功后通过job#biz_dcs_CollectFailRetryJob重新归集，仅支持自动归集====================")
        # clean_deposit_withdraw_order = get_dcs_clean_deposit_withdraw_order(business_no)
        # retry_id = retry_id
        # repay_run = DcsRunXxlJobChina(self.item_no, self.channel，retry_id)
        # repay_run.run_clearing_jobs_post("biz_dcs_CollectFailRetryJob")

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_buyback
    def test_buyback_success(self):
        print("====================造回购后-后还款的数据  2023.5.5调试成功====================")
        # 一笔6期资产从第一期开始回购，流程：模拟rbiz手动插入buyback数据 --> dcs执行回购job --> biz-cenrtal推送补充流程 -->再跑代偿后还款与清分
        # 1.回购流程与代偿基本一致，从回购期次开始全部会写一条代偿记录，回购的资产还款全部入拨备

        # setp 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        buyback_period = (1,)  # 从第一期开始回购
        # 尽量造逾期的数据-减少走资方的可能
        self.change_asset_due_at(-1, -90)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        # 查询本金，然后直接往 buyback 表插入数据 （固定设置从第1期开始回购）
        principal_plan = get_one_repay_plan(self.item_no, 'repayprincipal', 1, buyback_period[-1])
        principal_amount = 0
        for ii in range(0, len(principal_plan)):
            if principal_plan[ii]["asset_tran_period"] in buyback_period:
                principal_amount = principal_amount + principal_plan[ii]["asset_tran_amount"]
        # 手动插入buyback数据
        insert_buyback(self.item_no, self.period_count, principal_amount, buyback_period[0], self.channel)

        # dcs执行回购job-生成task-capitalBuybackFlow执行后生成asyncChainExecutable(task_order_no=资产编号)
        # 1.clean_final、clean_final_item写入数据
        for i in range(2):
            #多跑一次JOB，检查是否有异常
            dcs_run = DcsRunXxlJobChina(self.item_no, self.channel)
            dcs_run.run_clearing_jobs_post("biz_dcs_BuybackToPendingJob")

        print("================= 回购，报表日期（财务应计结算日期）=银行还款日期日==================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        #hebei_jiahexing_ts需要推送担保费
        # advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "buyback", "qsq", "N", "guarantee", get_date_before_today()[:10])
        advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "buyback", "qsq", "Y", "", get_date_before_today()[:10])

        # 回购后发起主动代扣-进入还款清分-回购后还款入拨备
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2, channel_name=self.withhold_channel)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # 同步代扣记录到历史库
        set_withhold_history(self.item_no)
        set_withhold_history(self.item_num_no_loan)
        dcs_run = DcsRunXxlJobChina(self.item_no, self.channel)
        # 执行task
        for i in range(20):
            dcs_run.run_clearing_jobs_post("dbTaskJob")

        # TODO 没有检查 clean_final、clean_final_item、clean_clearing_trans、clean_capital_settlement_notify_tran、clean_capital_settlement_pending


    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hebei_jiahexing_ts
    def test_hebei_jiahexing_ts_success(self):
        print("====================hebei_jiahexing_ts走资方代扣后清分====================")
        # setp 1 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        buyback_period = (1,)  # 从第一期开始回购
        # 尽量造逾期的数据-减少走资方的可能
        self.change_asset_due_at(-1, -5)  #80天内都走资方代扣
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        # 查询本金，然后直接往 buyback 表插入数据 （固定设置从第1期开始回购）
        principal_plan = get_one_repay_plan(self.item_no, 'repayprincipal', 1, buyback_period[-1])
        principal_amount = 0
        for ii in range(0, len(principal_plan)):
            if principal_plan[ii]["asset_tran_period"] in buyback_period:
                principal_amount = principal_amount + principal_plan[ii]["asset_tran_amount"]

        print("=================补充流程推送=================")
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        #hebei_jiahexing_ts需要推送担保费
        # advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "normal", "hebei_jiahexing_ts", "N", "guarantee", get_date_before_today()[:10])
        advanced_clearing.capital_settlement_notify(buyback_period[0], buyback_period[-1], "normal", "qsq", "N", "", get_date_before_today()[:10])

        # 发起主动代扣-进入还款清分
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2, channel_name=self.withhold_channel)
        self.run_task_after_withhold_callback(order_list)
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # 同步代扣记录到历史库
        set_withhold_history(self.item_no)
        set_withhold_history(self.item_num_no_loan)
        dcs_run = DcsRunXxlJobChina(self.item_no, self.channel)
        # 执行task
        for i in range(20):
            dcs_run.run_clearing_jobs_post("dbTaskJob")

        # TODO 没有检查 clean_final、clean_final_item、clean_clearing_trans、clean_capital_settlement_notify_tran、clean_capital_settlement_pending
