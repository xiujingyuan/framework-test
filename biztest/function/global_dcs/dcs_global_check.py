from biztest.function.gbiz.gbiz_db_function import get_asset_info_by_item_no
from biztest.function.global_dcs.dcs_global_db import get_asset_withdraw_info_by_item_no, get_dcs_asset_info_by_item_no, \
    get_dcs_asset_tran_by_item_no, get_capital_asset_info, get_capital_tran_info, get_account_log_info, \
    get_account_balance_available, get_dcs_refund_result_info_by_merchant_key, get_dcs_final_master_info_by_item_no, \
    get_dcs_final_tran_info_by_item_no, get_dcs_clearing_tran_info_by_item_no, get_dcs_account_repay_info_by_item_no, \
    get_dcs_settlement_info_by_batch_no, get_dcs_account_transfer_info_by_settlement_id
from biztest.util.asserts.assert_util import Assert


def check_dcs_asset_data(item_no, item_no_noloan):
    # gbiz放款数据检查
    asset = get_asset_info_by_item_no(item_no)
    asset[0]["asset_status"] == "repay"
    asset_noloan = get_asset_info_by_item_no(item_no_noloan)
    asset_noloan[0]["asset_status"] == "repay"
    # 放款成功大单开始记账 1.dcs.asset_withdraw表同步生成数据
    asset_withdraw = get_asset_withdraw_info_by_item_no(item_no)
    print(asset_withdraw[0]["order_no"])
    Assert.assert_equal(asset_withdraw[0]["order_no"], item_no, 'asset_withdraw数据落地失败')
    Assert.assert_equal(asset_withdraw[0]["channel"], "autotest_channel", '放款资方错误')
    Assert.assert_equal(asset_withdraw[0]["status"], "success", 'asset_withdraw状态错误')
    Assert.assert_equal(asset_withdraw[0]["type"], "withdraw", 'asset_withdraw类型错误')
    # TODO 这里后面可能需要加上执行rbiz的msg
    # rbiz执行sendmsg=AssetWithdrawSuccess，dcs. asset、asset_tran表同步落地数据，同时生成task： grantAccountBalanceManagement
    asset = get_dcs_asset_info_by_item_no(item_no)
    asset[0]["status"] == "repay"
    asset_tran = get_dcs_asset_tran_by_item_no(item_no)
    Assert.assert_equal(asset_tran[0]["type"], "repayprincipal", 'asset_tran类型错误')  # 目前只检查本金和利息，默认只有1期，以后有变动需要改
    Assert.assert_equal(asset_tran[1]["type"], "repayinterest", 'asset_tran类型错误')
    Assert.assert_equal(asset_tran[0]["status"], "nofinish", 'asset_tran状态错误')


def check_dcs_asset_and_tran(item_no):
    # 资方还款计划（目前没用）先只粗略检查
    capital_asset_info = get_capital_asset_info(item_no)
    Assert.assert_equal(capital_asset_info[0]["status"], "repay", 'capital_asset状态错误')

    capital_tran_info = get_capital_tran_info(item_no)
    Assert.assert_equal(capital_tran_info[0]["type"], "principal",
                        'capital_tran类型错误')  # 目前只检查本金和利息，默认只有1期，以后有变动需要改
    Assert.assert_equal(capital_tran_info[1]["type"], "interest", 'capital_tran类型错误')


def check_dcs_account_log(item_no, balance_available):
    asset_info = get_dcs_asset_info_by_item_no(item_no)
    granted_principal_amount = asset_info[0]["granted_principal_amount"]
    account_log_info = get_account_log_info(item_no)
    # TODO 更新nacos KV 配置
    Assert.assert_equal(account_log_info[0]["identity"], "v_pico_principal_gbpay",
                        '支出账户错误')  # KV:dcs_channel_config中写死配置account_channel对应的放款出户为 v_pico_principal_gbpay
    Assert.assert_equal(account_log_info[0]["type"], 1, '支出类型错误')
    Assert.assert_equal(int(account_log_info[0]["amount"]), int(granted_principal_amount), '支出金额错误')
    # 查询原始账户余额
    account_info = get_account_balance_available(
        "v_pico_principal_gbpay")  # KV:dcs_channel_config中写死配置account_channel对应的放款出户为 v_pico_principal_gbpay
    Assert.assert_equal(int(account_log_info[0]["balance_amount"]),
                        int(balance_available) - int(granted_principal_amount), '剩余金额错误')
    Assert.assert_equal(int(account_log_info[0]["balance_amount"]), int(account_info[0]["balance_available"]), '剩余金额错误')


def check_dcs_refund_result(refund_key, merchant_key, withhold_amount, channel, status):
    refund_result_info = get_dcs_refund_result_info_by_merchant_key(merchant_key)
    Assert.assert_equal(refund_result_info[0]["amount"], withhold_amount, '退款金额错误')
    Assert.assert_equal(refund_result_info[0]["withhold_serial_no"], merchant_key, '代扣流水错误merchant_key')
    Assert.assert_equal(refund_result_info[0]["serial_no"], refund_key, '退款流水错误refund_key')
    Assert.assert_equal(refund_result_info[0]["status"], status, '退款流水错误status')
    Assert.assert_equal(refund_result_info[0]["scene"], "repeated_withhold", 'scene错误')
    Assert.assert_equal(refund_result_info[0]["trade_type"], "online", 'trade_type错误')
    print(refund_result_info[0]["out_account"])
    Assert.assert_equal(refund_result_info[0]["out_account"], channel,
                        '代扣/代付退款出户错误；请检查dcs_clearing_config或dcs_grant_config是否配置了对应的退款归集户')


def check_dcs_clearing_tran(item_no, channel, biz_type="repay", status="success"):
    # 清分完成  account_repay、final_tran、final_master、clearing_tran 表数据检查
    account_repay_info = get_dcs_account_repay_info_by_item_no(item_no)
    # 2023-04-14海外清分流程停止：final_master、final_tran不再写入数据、clearing_tran只落地展期的数据
    # final_master_info = get_dcs_final_master_info_by_item_no(item_no, biz_type)
    # final_tran_info = get_dcs_final_tran_info_by_item_no(item_no, biz_type)
    clearing_tran_info = get_dcs_clearing_tran_info_by_item_no(item_no, biz_type)
    # 主要检查状态
    Assert.assert_equal(account_repay_info[0]["clean_status"], status, '正确')
    # Assert.assert_equal(final_master_info[0]["biz_type"], biz_type, '业务类型，repay：还款，compensate：代偿')
    # Assert.assert_equal(final_master_info[0]["partly"], "N", 'partly正确')
    # Assert.assert_equal(final_master_info[0]["compensated"], "N", 'compensated正确')
    # Assert.assert_equal(final_master_info[0]["amount"], amount, '正确')
    # Assert.assert_equal(final_master_info[0]["status"], status, 'final_master_info_status正确')
    # 主要检查状态，final_tran 有多个，暂定小单2种费用，大单三种费用
    # if channel == 'noloan':
    #     Assert.assert_equal(final_tran_info[0]["status"], status, 'final_tran_info_status正确')
    #     Assert.assert_equal(final_tran_info[1]["status"], status, 'final_tran_info_status正确')
    # else:
    #     Assert.assert_equal(final_tran_info[0]["status"], status, '正确')
    #     Assert.assert_equal(final_tran_info[1]["status"], status, '正确')
    #     Assert.assert_equal(final_tran_info[2]["status"], status, '正确')
    # 主要检查状态，clearing_tran 有多个，暂定小单出入户只有1个，大单有2个
    # if channel == 'noloan':
    #     Assert.assert_equal(clearing_tran_info[0]["status"], status, '正确')
    # else:
    #     Assert.assert_equal(clearing_tran_info[0]["status"], status, '正确')
    #     Assert.assert_equal(clearing_tran_info[1]["status"], status, '正确')
    # 清分流水
    # Assert.assert_equal(final_master_info[0]["final_no"], clearing_tran_info[0]["final_no"], 'final_master.final_no正确')
    # Assert.assert_equal(final_tran_info[0]["final_no"], clearing_tran_info[0]["final_no"], 'final_tran.final_no正确')


def check_dcs_settlement(item_no, channel, st_status=2, tf_status='success'):
    # 结算完成  settlement、account_transfer 表数据检查
    clearing_tran_info = get_dcs_clearing_tran_info_by_item_no(item_no)
    # 主要检查状态， 有多个，暂定小单只有1个，大单有2个
    if channel == 'noloan':
        settlement_info1 = get_dcs_settlement_info_by_batch_no(clearing_tran_info[0]["batch_no"])
        account_transfer_info1 = get_dcs_account_transfer_info_by_settlement_id(settlement_info1[0]["id"])
        # 主要检查状态
        Assert.assert_equal(settlement_info1[0]["status"], st_status, '正确')
        Assert.assert_equal(account_transfer_info1[0]["status"], tf_status, '正确')
    else:
        settlement_info1 = get_dcs_settlement_info_by_batch_no(clearing_tran_info[0]["batch_no"])
        settlement_info2 = get_dcs_settlement_info_by_batch_no(clearing_tran_info[1]["batch_no"])
        account_transfer_info1 = get_dcs_account_transfer_info_by_settlement_id(settlement_info1[0]["id"])
        account_transfer_info2 = get_dcs_account_transfer_info_by_settlement_id(settlement_info2[0]["id"])
        # 主要检查状态
        Assert.assert_equal(settlement_info1[0]["status"], st_status, '正确')
        Assert.assert_equal(account_transfer_info1[0]["status"], tf_status, '正确')
        Assert.assert_equal(settlement_info2[0]["status"], st_status, '正确')
        Assert.assert_equal(account_transfer_info2[0]["status"], tf_status, '正确')
