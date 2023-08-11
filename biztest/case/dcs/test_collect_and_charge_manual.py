import pytest
from biztest.config.dcs.dcs_nacos_config import update_nacos_dcs_generic_deal, update_nacos_dcs_payment_cost_config
from biztest.config.easymock.easymock_config import global_payment_easy_mock_phl
from biztest.function.dcs.biz_database import update_payment_withdrawAndreceipt_status, update_deposit_order_notexsit
from biztest.function.dcs.capital_database import update_dcs_china_task_next_run_at
from biztest.function.dcs.dcs_common import check_CleanWithdrawOrder, check_deal_orderAndtrade, \
    check_CleanDepositWithdrawOrder, check_task_capitalAuditCallback, check_asset_grant
from biztest.function.dcs.dcs_db_function import get_dcs_clean_generic_deal_trade
from biztest.interface.cmdb.cmdb_interface import monitor_check
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count, manual_collect, manual_settlement, \
    update_deposit_orderandtrade_and_run_task, manual_recharge, get_item_no
import common.global_const as gc
from biztest.util.easymock.dcs_mock import DcsMock
from biztest.util.tools.tools import get_date, get_four_element

"""
    手动发起资金归集（已）：华通、齐商（手动归集生成clean_withdraw_order前会有异名代付校验）
    1.手动归集的通过KV配置可设置单笔代付成本
    手动发起支付通道充值（已）：华通、齐商
    易宝支付通道充值时会额外调用payment系统/withhold/recharge接口获取remit_comment字段，在调用存管系统/trade/loan接口时需要将remit_comment字段作为memo传入
    1. 调支付走的mock（注意检查nacos的biz-dcs1.properties 配置）
    2. 存管未mock(需要保证存管测试环境的数据不会被删)
    author: fangchangfang
    date: 2020-04-13
    update：2022-12-01全部调试通过
"""


class TestDcsCollectAndCharge():
    env_test = gc.ENV
    environment = gc.ENVIRONMENT

    # 每个类的前置条件
    @classmethod
    def setup_class(self):
        # 支付走mock
        self.dcs_mock = DcsMock(global_payment_easy_mock_phl)
        self.channel = "qsq_sumpay_qjj_protocol"
        self.query_paysvr_commnet_channel = "qsq_yeepay_hange_protocol"
        self.ht_channelCode = "v_qjj_hk_ht_tengqiao"
        self.qs_channelCode = "v_tengqiao_hk_qs_tengqiao"
        self.ht_deposit = "ht_tengqiao"
        self.qs_deposit = "qs_tengqiao"
        self.memo = "remit_comment易宝汇款备注码"
        update_nacos_dcs_payment_cost_config(payment_channel="test")  #默认归集没有成本

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_qs_hange_success(self):
        print("====================（手动归集流程-先记账再代付，如新增qs_hange时指定存管测试）====================")
        # 如洗澡能呢过的华通瀚歌和齐商瀚歌新增配置是否正常走流程，修改KV#biz-dcs1.properties将新增存管配置进来即可，无需再改代码--》client.feign.deposit.sccba - url - mapping[qs_hange]
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, "qs_hange", "v_qishanghange_02_qs_hange")
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=2)
        # 记账完成，检查记账状态。存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='depositTally', serial_no='')
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])

        run_dcs_task_by_count(req["data"]["orderNo"], count=8)
        # 归集完成，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='success', tally_status='success',
                                 withdraw_status='success', payment_channel=self.channel,
                                 channel_code="v_qishanghange_02_qs_hange", deposit="qs_hange", memo=req["data"]["memo"])
        # 每次只检查最新的一笔的状态，记账后代付、转账后提现
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_ht_tq_success(self):
        print("====================（手动归集- ht_tengqiao 特殊归集流程-只代付不记账）====================")
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.ht_deposit, self.ht_channelCode)
        # 依次执行task##flow('flow_trade')、CapitalAuditCallback、GenericDealTransactionNew、GenericDealTransactionApply
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 每次只检查最新的一笔的状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no='')
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        # 依次执行GenericDealTransactionQuery、CollectTallFinish
        run_dcs_task_by_count(req["data"]["orderNo"], count=10)
        # 归集完成，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='success', tally_status='init',
                                 withdraw_status='success', payment_channel=self.channel,
                                 channel_code=self.ht_channelCode,
                                 deposit=self.ht_deposit, memo=req["data"]["memo"])
        # 每次只检查最新的一笔的状态，记账+代付、转账+提现
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_ht_tq_fail(self):
        print("====================（手动归集- ht_tengqiao 特殊归集流程-只代付不记账）====================")
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.ht_deposit, self.ht_channelCode)
        # 依次执行task##flow('flow_trade')、CapitalAuditCallback、GenericDealTransactionNew、GenericDealTransactionApply
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 每次只检查最新的一笔的状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no='')
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=1, status=3, trade_no=deal_trade_info[0]["trade_no"])
        # 依次执行GenericDealTransactionQuery、CollectTallFinish
        run_dcs_task_by_count(req["data"]["orderNo"], count=10)
        # 归集失败，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='fail', tally_status='init',
                                 withdraw_status='fail', payment_channel=self.channel, channel_code=self.ht_channelCode,
                                 deposit=self.ht_deposit, memo=req["data"]["memo"])
        # 每次只检查最新的一笔的状态，记账+代付、转账+提现
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='fail', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])


    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_ht_tq_process(self):
        print("====================（手动归集- ht_tengqiao 特殊归集流程-只代付不记账）====================")
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.ht_deposit, self.ht_channelCode)
        # 依次执行task##flow('flow_trade')、CapitalAuditCallback、GenericDealTransactionNew、GenericDealTransactionApply
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 每次只检查最新的一笔的状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no='')
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=2, status=1, trade_no=deal_trade_info[0]["trade_no"])
        # 依次执行GenericDealTransactionQuery、CollectTallFinish
        run_dcs_task_by_count(req["data"]["orderNo"], count=10)
        # 归集中，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='process', tally_status='init',
                                 withdraw_status='process', payment_channel=self.channel,
                                 channel_code=self.ht_channelCode,
                                 deposit=self.ht_deposit, memo=req["data"]["memo"])
        # 每次只检查最新的一笔的状态，记账+代付、转账+提现
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no='')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_qs_tengqiao_success(self):
        print("====================（手动归集流程-先记账再代付，当前在用的qs_tengqiao）====================")
        # 依次执行manualCollectFlow、AsyncChainExecutable【_#flow('flow_trade')】、AsyncChainExecutable【'CapitalAuditCallback'】、
        # AsyncChainExecutable(有3个GenericDealTransactionNew、GenericDealTransactionApply、GenericDealTransactionQuery)
        # AsyncChainExecutable【CollectTallFinish、#flow('flow_trade')】
        # AsyncChainExecutable(有3个GenericDealTransactionNew、GenericDealTransactionApply、GenericDealTransactionQuery)
        # AsyncChainExecutable【CollectWithdrawFinish】
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.qs_deposit, self.qs_channelCode)
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=2)
        # 记账完成，检查记账状态。存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='depositTally', serial_no='')
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])

        run_dcs_task_by_count(req["data"]["orderNo"], count=8)
        # 归集完成，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='success', tally_status='success',
                                 withdraw_status='success', payment_channel=self.channel,
                                 channel_code=self.qs_channelCode, deposit=self.qs_deposit, memo=req["data"]["memo"])
        # 每次只检查最新的一笔的状态，记账后代付、转账后提现
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_qs_tengqiao_withdraw_process(self):
        print("====================（手动归集流程-先记账再代付，当前在用的qs_tengqiao）====================")
        # 依次执行manualCollectFlow、AsyncChainExecutable【_#flow('flow_trade')】、AsyncChainExecutable【'CapitalAuditCallback'】、
        # AsyncChainExecutable(有3个GenericDealTransactionNew、GenericDealTransactionApply、GenericDealTransactionQuery)
        # AsyncChainExecutable【CollectTallFinish、#flow('flow_trade')】
        # AsyncChainExecutable(有3个GenericDealTransactionNew、GenericDealTransactionApply、GenericDealTransactionQuery)
        # AsyncChainExecutable【CollectWithdrawFinish】
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.qs_deposit, self.qs_channelCode)
        # 依次执行task
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=1)
        # 记账完成，检查记账状态。存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='depositTally', serial_no='')
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=2, status=1, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=8)
        # 归集完成，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='process', tally_status='success',
                                 withdraw_status='process', payment_channel=self.channel,
                                 channel_code=self.qs_channelCode, deposit=self.qs_deposit, memo=req["data"]["memo"])
        # 每次只检查最新的一笔的状态，记账后代付、转账后提现
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no='')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_qs_tengqiao_tally_fail(self):
        print("====================（手动归集流程-先记账再代付，当前在用的qs_tengqiao）====================")
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.qs_deposit, self.qs_channelCode)
        # 依次执行manualCollectFlow、AsyncChainExecutable【_#flow('flow_trade')】、AsyncChainExecutable【'CapitalAuditCallback'】、
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=3)
        run_dcs_task_by_count(req["data"]["orderNo"], count=2)
        # 记账完成，检查记账状态。存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='fail', from_business='COLLECT',
                                 order_type='depositTally', serial_no='')
        # 记账失败+代付未发起，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='fail', tally_status='fail',
                                 withdraw_status='init', payment_channel=self.channel, channel_code=self.qs_channelCode,
                                 deposit=self.qs_deposit, memo=req["data"]["memo"])

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_qs_tengqiao_revoke_success(self):
        print("====================（手动归集流程-先记账再代付，当前在用的qs_tengqiao）====================")
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.qs_deposit, self.qs_channelCode)
        # 依次执行manualCollectFlow、AsyncChainExecutable【_#flow('flow_trade')】、AsyncChainExecutable【'CapitalAuditCallback'】、
        # AsyncChainExecutable(有3个GenericDealTransactionNew、GenericDealTransactionApply、GenericDealTransactionQuery)
        # AsyncChainExecutable【CollectTallFinish、#flow('flow_trade')】
        # AsyncChainExecutable(有3个GenericDealTransactionNew、GenericDealTransactionApply、GenericDealTransactionQuery)
        # AsyncChainExecutable【CollectWithdrawFinish】
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=1)
        # 记账成功，检查记账状态；存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='depositTally', serial_no='')
        # 请求支付代付，代付结果查询走mock
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=1, status=3, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=1)
        # 代付失败，检查代付状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='fail', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=5)
        # 代付失败后执行记账撤销，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账成功+代付失败+记账撤销成功，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='fail', tally_status='revoke_success',
                                 withdraw_status='fail', payment_channel=self.channel, channel_code=self.qs_channelCode,
                                 deposit=self.qs_deposit, memo=req["data"]["memo"])
        # 每次只检查最新的一笔的状态，撤销记账成功；存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='depositTallyRevoke', serial_no='')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_qs_tengqiao_revoke_fail(self):
        print("====================（手动归集流程-先记账再代付，当前在用的qs_tengqiao）====================")
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.qs_deposit, self.qs_channelCode)
        # 依次执行manualCollectFlow、AsyncChainExecutable【_#flow('flow_trade')】、AsyncChainExecutable【'CapitalAuditCallback'】、
        # AsyncChainExecutable(有3个GenericDealTransactionNew、GenericDealTransactionApply、GenericDealTransactionQuery)
        # AsyncChainExecutable【CollectTallFinish、#flow('flow_trade')】
        # AsyncChainExecutable(有3个GenericDealTransactionNew、GenericDealTransactionApply、GenericDealTransactionQuery)
        # AsyncChainExecutable【CollectWithdrawFinish】        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=2)
        # 记账成功，检查记账状态；存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='depositTally', serial_no='')
        # 请求支付代付，代付结果查询走mock
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        run_dcs_task_by_count(req["data"]["orderNo"], count=5)
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=1, status=3, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=2)
        # 代付失败，检查代付状态，每次只检查最新的一笔的状态，撤销记账失败；存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='fail', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])
        # 代付失败后执行记账撤销，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=3)
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账成功+代付失败+记账撤销失败，检查归集表状态；此时CollectTallRevokeFinish会一直卡住等待人工介入处理
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='process', tally_status='revoke_process',
                                 withdraw_status='fail', payment_channel=self.channel, channel_code=self.qs_channelCode,
                                 deposit=self.qs_deposit, memo=req["data"]["memo"])

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_revoke_not_exsit_to_fail(self):
        print("====================（支付返回订单不存在+存管返回订单不存在，配置到KV后置为失败，以齐商-归集为例）====================")
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.qs_deposit, self.qs_channelCode)
        # 依次执行manualCollectFlow、AsyncChainExecutable【_#flow('flow_trade')】、AsyncChainExecutable【'CapitalAuditCallback'】等
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=1)
        # 1、记账成功，检查记账状态；存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='depositTally', serial_no='')
        # 请求支付代付，代付结果查询走mock
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        # 2、模拟查询支付返回订单不存在
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        # 将clean_generic_deal_trade、order_no配置到dcs_generic_deal中
        update_nacos_dcs_generic_deal(deal_trade_info[0]["order_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=1)
        # 2、代付失败，检查代付状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='fail', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no="")
        run_dcs_task_by_count(req["data"]["orderNo"], count=5)
        # 获取最新一条clean_generic_deal_trade
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        # 3、记账撤销失败  使存管返回订单不存在
        update_deposit_order_notexsit(deal_trade_info[0]["order_no"])
        # 将clean_generic_deal_trade、order_no配置到dcs_generic_deal中
        update_nacos_dcs_generic_deal(deal_trade_info[0]["order_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账成功+代付失败+记账撤销失败，检查归集表状态；此时CollectTallRevokeFinish会一直卡住等待人工介入处理
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='process', tally_status='revoke_process',
                                 withdraw_status='fail', payment_channel=self.channel, channel_code=self.qs_channelCode,
                                 deposit=self.qs_deposit, memo=req["data"]["memo"])
        # 每次只检查最新的一笔的状态，撤销记账失败；存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='fail', from_business='COLLECT',
                                 order_type='depositTallyRevoke', serial_no='')

    """
    手动发起支付通道充值流程：华通、齐商
    """
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_recharge
    def test_manual_recharge_qs_success(self):
        print("====================（齐商存管- 手动给支付通道充值，走deposit放款接口）====================")
        req, resp = manual_recharge(paymentChannel=self.channel, deposit=self.qs_deposit,
                                    depositChannelCode=self.qs_channelCode)
        # 依次执行depositWithdrawOrderNew、genericDealTransactionNew、genericDealTransactionApply、genericDealTransactionQuery
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 调存管放款接口，检查处理中状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='DEPOSIT_WITHDRAW',
                                 order_type='depositLoan', serial_no='')
        # 执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=3)
        # 检查回调capital任务是否生成
        check_task_capitalAuditCallback(req["data"]["orderNo"])
        # 存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='DEPOSIT_WITHDRAW',
                                 order_type='depositLoan', serial_no='')
        # 检查支付通道充值表clean_deposit_withdraw_order
        check_CleanDepositWithdrawOrder(business_no=req["data"]["orderNo"], status='success',
                                        payment_channel=self.channel,
                                        deposit=self.qs_deposit, loan_channel=self.qs_channelCode)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_recharge
    def test_manual_recharge_qs_fail(self):
        print("====================（齐商存管- 手动给支付通道充值，走deposit放款接口）====================")
        req, resp = manual_recharge(paymentChannel=self.channel, deposit=self.qs_deposit,
                                    depositChannelCode=self.qs_channelCode)
        # 依次执行depositWithdrawOrderNew、genericDealTransactionNew、genericDealTransactionApply、genericDealTransactionQuery
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 调存管放款接口，检查处理中状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='DEPOSIT_WITHDRAW',
                                 order_type='depositLoan', serial_no='')
        # 执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=3)
        run_dcs_task_by_count(req["data"]["orderNo"], count=3)
        # 检查回调capital任务是否生成
        check_task_capitalAuditCallback(req["data"]["orderNo"])
        # 存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='fail', from_business='DEPOSIT_WITHDRAW',
                                 order_type='depositLoan', serial_no='')
        # 检查支付通道充值表clean_deposit_withdraw_order
        check_CleanDepositWithdrawOrder(business_no=req["data"]["orderNo"], status='fail',
                                        payment_channel=self.channel,
                                        deposit=self.qs_deposit, loan_channel=self.qs_channelCode)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_recharge
    def test_manual_recharge_qs_process(self):
        print("====================（齐商存管- 手动给支付通道充值，走deposit放款接口）====================")
        req, resp = manual_recharge(paymentChannel=self.channel, deposit=self.qs_deposit,
                                    depositChannelCode=self.qs_channelCode)
        # 依次执行depositWithdrawOrderNew、genericDealTransactionNew、genericDealTransactionApply、genericDealTransactionQuery
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 调存管放款接口，检查处理中状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='DEPOSIT_WITHDRAW',
                                 order_type='depositLoan', serial_no='')
        # genericDealTransactionQuery执行5次还是处理中会发TV通知
        run_dcs_task_by_count(req["data"]["orderNo"], count=5)
        # 存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='DEPOSIT_WITHDRAW',
                                 order_type='depositLoan', serial_no='')
        # 检查支付通道充值表clean_deposit_withdraw_order
        check_CleanDepositWithdrawOrder(business_no=req["data"]["orderNo"], status='process',
                                        payment_channel=self.channel,
                                        deposit=self.qs_deposit, loan_channel=self.qs_channelCode)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_recharge
    def test_manual_recharge_ht_success(self):
        print("====================（华通存管- 手动给支付通道充值，走deposit放款接口）====================")
        req, resp = manual_recharge(paymentChannel=self.channel, deposit=self.ht_deposit,
                                    depositChannelCode=self.ht_channelCode)
        # 依次执行depositWithdrawOrderNew、genericDealTransactionNew、genericDealTransactionApply、genericDealTransactionQuery
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 调存管放款接口，检查处理中状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process',
                                 from_business='DEPOSIT_WITHDRAW', order_type='depositLoan', serial_no='')
        # 执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=3)
        # 检查回调capital任务是否生成
        check_task_capitalAuditCallback(req["data"]["orderNo"])
        # 存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success',
                                 from_business='DEPOSIT_WITHDRAW', order_type='depositLoan', serial_no='')
        # 检查支付通道充值表clean_deposit_withdraw_order
        check_CleanDepositWithdrawOrder(business_no=req["data"]["orderNo"], status='success',
                                        payment_channel=self.channel, deposit=self.ht_deposit,
                                        loan_channel=self.ht_channelCode)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_recharge
    def test_manual_recharge_ht_fail(self):
        print("====================（华通存管- 手动给支付通道充值，走deposit放款接口）====================")
        req, resp = manual_recharge(paymentChannel=self.channel, deposit=self.ht_deposit,
                                    depositChannelCode=self.ht_channelCode)
        # 依次执行depositWithdrawOrderNew、genericDealTransactionNew、genericDealTransactionApply、genericDealTransactionQuery
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 调存管放款接口，检查处理中状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process',
                                 from_business='DEPOSIT_WITHDRAW', order_type='depositLoan', serial_no='')
        # 执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=3)
        run_dcs_task_by_count(req["data"]["orderNo"], count=3)
        # 检查回调capital任务是否生成
        check_task_capitalAuditCallback(req["data"]["orderNo"])
        # 存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='fail',
                                 from_business='DEPOSIT_WITHDRAW',
                                 order_type='depositLoan', serial_no='')
        # 检查支付通道充值表clean_deposit_withdraw_order
        check_CleanDepositWithdrawOrder(business_no=req["data"]["orderNo"], status='fail',
                                        payment_channel=self.channel, deposit=self.ht_deposit,
                                        loan_channel=self.ht_channelCode)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_recharge
    def test_manual_recharge_ht_process(self):
        print("====================（华通存管- 手动给支付通道充值，走deposit放款接口）====================")
        req, resp = manual_recharge(paymentChannel=self.channel, deposit=self.ht_deposit,
                                    depositChannelCode=self.ht_channelCode)
        # 依次执行depositWithdrawOrderNew、genericDealTransactionNew、genericDealTransactionApply、genericDealTransactionQuery
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 调存管放款接口，检查处理中状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process',
                                 from_business='DEPOSIT_WITHDRAW', order_type='depositLoan', serial_no='')
        # genericDealTransactionQuery执行5次还是处理中会发TV通知
        run_dcs_task_by_count(req["data"]["orderNo"], count=5)
        # 存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='DEPOSIT_WITHDRAW',
                                 order_type='depositLoan', serial_no='')
        # 检查支付通道充值表clean_deposit_withdraw_order
        check_CleanDepositWithdrawOrder(business_no=req["data"]["orderNo"], status='process',
                                        payment_channel=self.channel, deposit=self.ht_deposit,
                                        loan_channel=self.ht_channelCode)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_recharge
    def test_manual_recharge_yeepay_ht_success(self):
        # 易宝支付通道充值时会额外调用payment系统/withhold/recharge接口获取remit_comment字段，在调用存管系统/trade/loan接口时需要将remit_comment字段作为memo传入
        # 在depositWithdrawOrderNew任务中调用/withhold/recharge接口，这一步只是信息流可以换merchant_key不停的请求，没有使用的备注通道那边最终是会过期的
        # /withhold/recharge没有对应的查询接口，dcs只在支付返回code<>1且remit_comment不为空才会认为获取备注成功，否则depositWithdrawOrderNew任务一直换merchant_key重试
        print("====================（华通存管- 手动给支付通道充值，走deposit放款接口）====================")
        req, resp = manual_recharge(paymentChannel=self.query_paysvr_commnet_channel, deposit=self.ht_deposit,
                                    depositChannelCode=self.ht_channelCode)
        self.dcs_mock.update_payment_withhold_recharge_success(code=2, remit_comment=self.memo)
        # self.dcs_mock.update_payment_withhold_recharge_success(code=0, remit_comment=self.memo)
        # self.dcs_mock.update_payment_withhold_recharge_success(code=0, remit_comment="") # 异常场景测试
        # self.dcs_mock.update_payment_withhold_recharge_success(code=1, remit_comment=self.memo) # 异常场景测试
        # self.dcs_mock.update_payment_withhold_recharge_success(code=1, remit_comment="") # 异常场景测试
        # self.dcs_mock.update_payment_withhold_recharge_success(code=2, remit_comment=self.memo) # 异常场景测试


        # 依次执行depositWithdrawOrderNew、genericDealTransactionNew、genericDealTransactionApply、genericDealTransactionQuery
        run_dcs_task_by_count(req["data"]["orderNo"], count=5)
        # 调存管放款接口，检查处理中状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process',
                                 from_business='DEPOSIT_WITHDRAW', order_type='depositLoan', serial_no='')
        # 执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=3)
        # 检查回调capital任务是否生成
        check_task_capitalAuditCallback(req["data"]["orderNo"])
        # 存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success',
                                 from_business='DEPOSIT_WITHDRAW', order_type='depositLoan', serial_no='')
        # 检查支付通道充值表clean_deposit_withdraw_order
        check_CleanDepositWithdrawOrder(business_no=req["data"]["orderNo"], status='success',
                                        payment_channel=self.query_paysvr_commnet_channel, deposit=self.ht_deposit,
                                        memo=self.memo, loan_channel=self.ht_channelCode)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_cost_ht_tq_success(self):
        print("====================（手动归集：需要扣除成本 - ht_tengqiao 特殊归集流程-只代付不记账）====================")
        # 设置代付成本1笔1元
        update_nacos_dcs_payment_cost_config(payment_channel=self.channel)
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.ht_deposit, self.ht_channelCode)
        # 依次执行task##flow('flow_trade')、CapitalAuditCallback、GenericDealTransactionNew、GenericDealTransactionApply
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 每次只检查最新的一笔的状态
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='process', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no='')
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        # 依次执行GenericDealTransactionQuery、CollectTallFinish
        run_dcs_task_by_count(req["data"]["orderNo"], count=10)
        # 归集完成，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='success', tally_status='init',
                                 withdraw_status='success', payment_channel=self.channel,
                                 channel_code=self.ht_channelCode,
                                 deposit=self.ht_deposit, memo=req["data"]["memo"], amount=1011)
        # 每次只检查最新的一笔的状态，记账+代付、转账+提现
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])
        # TODO 没有检查手续费的清分明细，由拨备-->归集户

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_split_cost_ht_tq_success(self):
        print("====================（手动归集：需要拆单&扣除成本- ht_tengqiao 特殊归集流程-只代付不记账）====================")
        # 设置代付成本1笔1元
        update_nacos_dcs_payment_cost_config(payment_channel=self.channel)
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        # 手动归集1000w，拆成两单500w
        req, resp = manual_collect(self.channel, self.ht_deposit, self.ht_channelCode, "1000000000")
        # 依次执行task##flow('flow_trade')、CapitalAuditCallback、GenericDealTransactionNew、GenericDealTransactionApply
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 请求支付代付，第一笔代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"]+"_0")
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=10)
        # 第二笔代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"]+"_1")
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=10)
        # TODO 拆单场景，暂没有做字段检查

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_cost_qs_tengqiao_success(self):
        print("====================（手动归集流程：需要扣除成本 - 先记账再代付，当前在用的qs_tengqiao）====================")
        # 1.归集金额=代扣总额-结算手续费-代扣手续费
        # 2.记账金额=归集金额
        # 3.代付金额=归集金额+代扣手续费
        # 设置代付成本1笔1元
        update_nacos_dcs_payment_cost_config(payment_channel=self.channel)
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        req, resp = manual_collect(self.channel, self.qs_deposit, self.qs_channelCode)
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=3)
        # 记账完成，检查记账状态。存管不返回serial_no
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='depositTally', serial_no='')
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 请求支付代付，代付结果查询走mock
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"])
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])

        run_dcs_task_by_count(req["data"]["orderNo"], count=8)
        # 归集完成，检查归集表状态
        check_CleanWithdrawOrder(business_no=req["data"]["orderNo"], status='success', tally_status='success',
                                 withdraw_status='success', payment_channel=self.channel,
                                 channel_code=self.qs_channelCode, deposit=self.qs_deposit,
                                 memo=req["data"]["memo"], amount=1011)
        # 检查代付状态，每次只检查最新的一笔的状态，如记账后代付（ or 转账后提现）
        check_deal_orderAndtrade(business_no=req["data"]["orderNo"], status='success', from_business='COLLECT',
                                 order_type='paymentWithdraw', serial_no=deal_trade_info[0]["trade_no"])
        # TODO 没有检查手续费的清分明细，由拨备-->归集户

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_manual_collect
    def test_manual_collect_cost_split_qs_tengqiao_success(self):
        print("====================（手动归集流程：需要扣除成本 - 先记账再代付，当前在用的qs_tengqiao）====================")
        # 1.归集金额=代扣总额-结算手续费-代扣手续费
        # 2.记账金额=归集金额
        # 3.代付金额=归集金额+代扣手续费
        # 设置代付成本1笔1元
        update_nacos_dcs_payment_cost_config(payment_channel=self.channel)
        # 初始化代付查询返回【交易不存在】
        self.dcs_mock.update_payment_withdraw_query_notexsit()
        # 手动归集1000w，拆成两单500w
        req, resp = manual_collect(self.channel, self.qs_deposit, self.qs_channelCode, "1000000000")
        run_dcs_task_by_count(req["data"]["orderNo"], count=6)
        # 记账到存管，执行存管task并更新状态
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_count(req["data"]["orderNo"], count=3)
        run_dcs_task_by_count(req["data"]["orderNo"], count=4)
        # 请求支付代付，代付结果查询走mock，第1笔
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"]+"_0")
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=8)
        # 请求支付代付，代付结果查询走mock，第2笔
        deal_trade_info = get_dcs_clean_generic_deal_trade(req["data"]["orderNo"]+"_1")
        self.dcs_mock.update_payment_withdraw_query(code=0, status=2, trade_no=deal_trade_info[0]["trade_no"])
        run_dcs_task_by_count(req["data"]["orderNo"], count=8)
        # TODO 拆单场景，暂没有做字段检查


    # @pytest.mark.dcs_auto_test
    # @pytest.mark.DCS_test_manual_settlement
    # def test_manual_settlement_qs_success(self):
    #     print("====================（手动结算小单？-capital页面发起）====================")
    #     batch_no = "MZ_JMX511187211000155541"
    #     transfer_in = "v_hefei_weidu_reserve"
    #     transfer_out = "v_mozhi_jinmeixin_gj"
    #     req, resp = manual_settlement(loan_type="BIG", batch_no=batch_no, transfer_in=transfer_in, transfer_out=transfer_out)
    #     # 依次执行
    #     run_dcs_task_by_count(req["data"]["orderNo"], count=6)
