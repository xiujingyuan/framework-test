import pandas as pd
from pandas.io.json import json_normalize

from biztest.function.global_rbiz.rbiz_global_db_function import *
from biztest.util.asserts.assert_util import Assert

"""
rbiz数据检查
想法：横向和纵向均需要做检查，横向指每个表的每个字段，需要单独检查，纵向指多个表之间的数据进行对比
1、check_asset_data
横向：检查account、account_recharge、account_recharge_log、account_repay、account_repay_log、
withhold、withhold_order、withhold_detail、withhold_request表的内容
纵向：对比account_repay、account_repay_log、withhold_detail表内容，包括order_no，tran_no，type，amount，period，
2、check_asset_data

"""


def check_data(data, **kwargs):
    for key, value in kwargs.items():
        Assert.assert_equal(data[key], value, "%s数据有误" % key)


def check_data_withhold_by_sn(serial_no, **kwargs):
    withhold = get_withhold_by_serial_no(serial_no)
    check_data(withhold[0], **kwargs)


def check_json_rs_data(rs, **kwargs):
    check_data(rs, **kwargs)


def check_asset_data(item_no, **kwargs):
    """
    检查资产相关信息
    """
    asset_info = get_asset_info_by_item_no(item_no)[0]
    asset_tran = get_asset_tran(asset_tran_asset_item_no=item_no)

    asset_status = kwargs.get("asset_status", "repay")
    decrease_principal_amount = int(kwargs.get("decrease_principal_amount", 0))
    decrease_interest_amount = int(kwargs.get("decrease_interest_amount", 0))
    decrease_late_amount = int(kwargs.get("decrease_late_amount", 0))
    decrease_fee_amount = int(kwargs.get("decrease_fee_amount", 0))
    total_decrease_amount = decrease_principal_amount + decrease_interest_amount + decrease_late_amount + decrease_fee_amount
    repaid_principal_amount = int(kwargs.get("repaid_principal_amount", 0))
    repaid_interest_amount = int(kwargs.get("repaid_interest_amount", 0))
    repaid_late_amount = int(kwargs.get("repaid_late_amount", 0))
    repaid_fee_amount = int(kwargs.get("repaid_fee_amount", 0))
    total_repaid_amount = repaid_principal_amount + repaid_interest_amount + repaid_late_amount + repaid_fee_amount
    total_balance_amount = asset_info["asset_total_amount"] - total_decrease_amount - total_repaid_amount
    balance_amount = int(kwargs.get("balance_amount", 0))
    repaid_amount = int(kwargs.get("repaid_amount", 0))
    late_amount = int(kwargs.get("late_amount", 0))
    fee_amount = int(kwargs.get("fee_amount", 0))

    # check asset
    Assert.assert_equal(asset_status, asset_info["asset_status"], "asset_status 不正确")
    Assert.assert_equal(balance_amount, total_balance_amount, "balance_amount 不正确")
    Assert.assert_equal(decrease_principal_amount, asset_info["asset_decrease_principal_amount"], "decrease_principal_amount 不正确")
    Assert.assert_equal(decrease_interest_amount, asset_info["asset_decrease_interest_amount"], "decrease_principal_amount 不正确")
    Assert.assert_equal(decrease_late_amount, asset_info["asset_decrease_late_amount"], "decrease_principal_amount 不正确")
    Assert.assert_equal(decrease_fee_amount, asset_info["asset_decrease_fee_amount"], "decrease_principal_amount 不正确")
    Assert.assert_equal(repaid_principal_amount, asset_info["asset_repaid_principal_amount"], "repaid_principal_amount 不正确")
    Assert.assert_equal(repaid_interest_amount, asset_info["asset_repaid_interest_amount"], "repaid_interest_amount 不正确")
    Assert.assert_equal(repaid_late_amount, asset_info["asset_repaid_late_amount"], "repaid_late_amount 不正确")
    Assert.assert_equal(repaid_fee_amount, asset_info["asset_repaid_fee_amount"], "repaid_fee_amount 不正确")
    Assert.assert_equal(balance_amount, asset_info["asset_balance_amount"], "balance_amount 不正确")
    Assert.assert_equal(repaid_amount, asset_info["asset_repaid_amount"], "repaid_amount 不正确")
    Assert.assert_equal(late_amount, asset_info["asset_late_amount"], "late_amount 不正确")
    Assert.assert_equal(fee_amount, asset_info["asset_fee_amount"], "fee_amount 不正确")

    # check asset_tran
    Assert.assert_equal(asset_info["asset_total_amount"], sum([x["asset_tran_total_amount"] for x in asset_tran]), "tran_amount 总金额不对")
    Assert.assert_equal(total_decrease_amount, sum([x["asset_tran_decrease_amount"] for x in asset_tran]), "tran_decrease_amount 总金额不对")
    Assert.assert_equal(decrease_principal_amount, sum([x["asset_tran_decrease_amount"] for x in asset_tran if x["asset_tran_type"] == "repayprincipal"]), "principal_decrease_amount 总金额不对")
    Assert.assert_equal(decrease_interest_amount, sum([x["asset_tran_decrease_amount"] for x in asset_tran if x["asset_tran_type"] == "repayinterest"]), "interest_decrease_amount 总金额不对")
    Assert.assert_equal(decrease_late_amount, sum([x["asset_tran_decrease_amount"] for x in asset_tran if x["asset_tran_type"] == "lateinterest"]), "late_decrease_amount 总金额不对")
    Assert.assert_equal(decrease_fee_amount, sum([x["asset_tran_decrease_amount"] for x in asset_tran if x["asset_tran_type"] == "fin_service"]), "fee_decrease_amount 总金额不对")

    Assert.assert_equal(total_repaid_amount, sum([x["asset_tran_repaid_amount"] for x in asset_tran]), "tran_rapaid_amount 总金额不对")
    Assert.assert_equal(repaid_principal_amount, sum([x["asset_tran_repaid_amount"] for x in asset_tran if x["asset_tran_type"] == "repayprincipal"]), "principal_rapaid_amount 总金额不对")
    Assert.assert_equal(repaid_interest_amount, sum([x["asset_tran_repaid_amount"] for x in asset_tran if x["asset_tran_type"] == "repayinterest"]), "interest_rapaid_amount 总金额不对")
    Assert.assert_equal(repaid_late_amount, sum([x["asset_tran_repaid_amount"] for x in asset_tran if x["asset_tran_type"] == "lateinterest"]), "late_rapaid_amount 总金额不对")
    Assert.assert_equal(repaid_fee_amount, sum([x["asset_tran_repaid_amount"] for x in asset_tran if x["asset_tran_type"] == "fin_service"]), "fee_rapaid_amount 总金额不对")

    Assert.assert_equal(total_balance_amount, sum([x["asset_tran_balance_amount"] for x in asset_tran]), "tran_balance_amount 总金额不对")
    Assert.assert_equal(asset_info["asset_principal_amount"]-asset_info["asset_repaid_principal_amount"],
                        sum([x["asset_tran_balance_amount"] for x in asset_tran if x["asset_tran_type"] == "repayprincipal"]), "principal_balance_amount 总金额不对")
    Assert.assert_equal(asset_info["asset_interest_amount"]-asset_info["asset_repaid_interest_amount"],
                        sum([x["asset_tran_balance_amount"] for x in asset_tran if x["asset_tran_type"] == "repayinterest"]), "interest_balance_amount 总金额不对")
    Assert.assert_equal(asset_info["asset_late_amount"]-asset_info["asset_repaid_late_amount"],
                        sum([x["asset_tran_balance_amount"] for x in asset_tran if x["asset_tran_type"] == "lateinterest"]), "late_balance_amount 总金额不对")
    Assert.assert_equal(asset_info["asset_fee_amount"]-asset_info["asset_repaid_fee_amount"],
                        sum([x["asset_tran_balance_amount"] for x in asset_tran if x["asset_tran_type"] == "fin_service"]), "fee_balance_amount 总金额不对")

    Assert.assert_equal(sum([x["asset_tran_balance_amount"] for x in asset_tran]) +
                        sum([x["asset_tran_repaid_amount"] for x in asset_tran]) +
                        sum([x["asset_tran_decrease_amount"] for x in asset_tran]),
                        sum([x["asset_tran_total_amount"] for x in asset_tran]), "tran_total_amount 总金额不对")


def check_asset_delay_data(serial_no, apply_amount, pay_amount, pay_status, delay_status, balance_amount=0, check_account=True):
    asset_delays = get_asset_delay(asset_delay_withhold_serial_no=serial_no)
    trade = get_trade_by_serial_no(serial_no)[0]
    trade_tran = get_trade_tran(trade_tran_serial_no=serial_no)
    withhold = get_withhold(withhold_serial_no=serial_no)[0]
    withhold_orders = get_withhold_order(withhold_order_serial_no=serial_no)
    account = get_account_by_id_num(withhold["withhold_user_idnum"])[0]
    status_temp = {"open": {"withhold_status": "process",
                            "delay_status": delay_status,
                            "trade_status": "open",
                            "trade_tran_status": "open"},
                   "fail": {"withhold_status": "fail",
                            "delay_status": delay_status,
                            "trade_status": "void",
                            "trade_tran_status": "fail"},
                   "success": {"withhold_status": "success",
                               "delay_status": delay_status,
                               "trade_status": "payoff" if delay_status == "success" else "void",
                               "trade_tran_status": "success" if delay_status == "success" else "fail"},
                   "cancel": {"withhold_status": "fail",
                              "delay_status": delay_status,
                              "trade_status": "void",
                              "trade_tran_status": "fail"}}
    # 校验asset_delay
    for asset_delay in asset_delays:
        asset = get_asset(asset_item_no=asset_delay["asset_delay_item_no"])[0]
        Assert.assert_equal(withhold["withhold_finish_at"]
                            if status_temp[pay_status]["delay_status"] == "success" else "1000-01-01 00:00:00",
                            asset_delay["asset_delay_pay_at"], "asset_delay_pay_at")
        Assert.assert_equal(status_temp[pay_status]["delay_status"],
                            asset_delay["asset_delay_status"], "asset_delay_status不正确")
        # if asset["asset_loan_channel"] != "noloan":
        #     Assert.assert_equal(apply_amount if status_temp[pay_status]["delay_status"] == "success" else 0,
        #                         asset_delay["asset_delay_amount"], "asset_delay_amount不正确")
        #     Assert.assert_equal(apply_amount, asset_delay["asset_delay_apply_amount"], "asset_delay_apply_amount不正确")
        # if asset["asset_loan_channel"] == "noloan":
        #     Assert.assert_equal(0, asset_delay["asset_delay_amount"], "asset_delay_amount不正确")
        #     Assert.assert_equal(0, asset_delay["asset_delay_apply_amount"], "asset_delay_apply_amount不正确")
    # 校验trade
    Assert.assert_equal(status_temp[pay_status]["trade_status"], trade["trade_status"], "trade_status不正确")
    Assert.assert_equal(apply_amount, trade["trade_amount"], "trade_amount不正确")
    Assert.assert_equal(pay_amount, trade["trade_pay_amount"], "trade_pay_amount不正确")
    # 检验trade_tran
    Assert.assert_equal(status_temp[pay_status]["trade_tran_status"], trade_tran[0]["trade_tran_status"],
                        "trade_tran_status不正确")
    Assert.assert_equal(pay_amount, trade_tran[0]["trade_tran_amount"], "trade_tran_amount不正确")
    # 校验withhold
    Assert.assert_equal(status_temp[pay_status]["withhold_status"], withhold["withhold_status"], "withhold_status不正确")
    Assert.assert_equal(pay_amount, withhold["withhold_amount"], "withhold_amount不正确")
    # 校验withhold_order
    withhold_order_amount = sum(withhold_order["withhold_order_withhold_amount"] for withhold_order in withhold_orders)
    Assert.assert_equal(pay_amount - balance_amount, withhold_order_amount, "withhold_order_withhold_amount不正确")
    if check_account:
        # 校验account
        Assert.assert_equal(balance_amount, account["account_balance_amount"], "account_balance_amount不正确")


def check_withhold_success_data(serial_no, **kwargs):
    """
    检查某一个代扣订单的数据
    """
    # 获取数据
    withhold = get_withhold_by_serial_no(serial_no)[0]
    channel_key = withhold["withhold_channel_key"]

    account = get_account_by_id_num(withhold["withhold_user_idnum"])[0]
    account_recharge = get_account_recharge_by_serial_no(channel_key)[0]
    account_recharge_log = get_account_recharge_log_by_serial_no(channel_key)[0]
    account_repay = get_account_repay_by_serial_no_inner_join_asset_tran(channel_key)  # 有可能多个
    account_repay_log = get_account_repay_log_by_serial_no(channel_key)  # 有可能多个

    withhold_detail = get_withhold_detail_by_serial_no_inner_join_asset_tran(serial_no)  # 有可能多个
    withhold_order = get_withhold_order_by_serial_no(serial_no)  # 有可能多个
    withhold_request = get_withhold_request_by_serial_no(serial_no)[0]

    asset_delay = get_asset_delay(asset_delay_withhold_serial_no=serial_no)
    trade = get_trade_by_serial_no(serial_no)
    trade_tran = get_trade_tran(trade_tran_serial_no=serial_no)  # 有可能多个

    # 解析入参
    withhold_channel = kwargs.get("withhold_channel", "auto_india_channel")
    withhold_sub_status = kwargs.get("withhold_sub_status", "normal")
    withhold_payment_type = kwargs.get("payment_type", "ebank")
    withhold_card_num = kwargs.get("withhold_card_num", None)
    withhold_amount = int(kwargs.get("withhold_amount", 0))
    balance_amount = int(kwargs.get("balance_amount", 0))  # 充值后未还款金额，称之为剩余金额
    trade_amount = int(kwargs.get("trade_amount", 0))
    sign_company = kwargs.get("sign_company", "cymo5")
    detail_repay_type = kwargs.get("repay_type", "normal")
    request_trade_type = kwargs.get("trade_type", "COMBINE_WITHHOLD")
    order_operate_type = kwargs.get("order_operate_type", "active")
    withhold_third_serial_no = kwargs.get("withhold_third_serial_no", None)

    # check asset_delay
    if len(asset_delay) > 0:
        Assert.assert_equal(asset_delay[0]["asset_delay_amount"],
                            0 if asset_delay[0]["asset_delay_status"] != "success" else trade_amount,
                            "asset_delay_amount 不正确")
        Assert.assert_equal(asset_delay[0]["asset_delay_apply_amount"], trade_amount, "asset_delay_apply_amount 不正确")

    # check trade
    if len(trade) > 0:
        Assert.assert_equal(trade[0]["trade_status"], "payoff", "trade_type 不正确")
        Assert.assert_equal(trade[0]["trade_type"], "asset_delay", "trade_type 不正确")
        Assert.assert_equal(trade[0]["trade_amount"], trade_amount, "trade_amount 不正确")
        Assert.assert_equal(trade[0]["trade_pay_amount"], withhold_amount, "trade_pay_amount 不正确")
        Assert.assert_equal(trade[0]["trade_pay_at"], withhold["withhold_finish_at"], "trade_pay_at 不正确")

    # check trade_tran
    if len(trade_tran) > 0:
        Assert.assert_equal(trade_tran[0]["trade_tran_ref_type"], "withhold_result", "trade_tran_ref_type 不正确")
        Assert.assert_equal(trade_tran[0]["trade_tran_type"], "pay", "trade_tran_type 不正确")
        Assert.assert_equal(trade_tran[0]["trade_tran_status"], "success", "trade_tran_status 不正确")
        Assert.assert_equal(trade_tran[0]["trade_tran_amount"], trade_amount, "trade_tran_amount 不正确")

    # check withhold 海外的代扣数据较简单
    Assert.assert_equal(withhold["withhold_status"], "success", "withhold状态不对")
    Assert.assert_equal(withhold["withhold_amount"], withhold_amount, "withhold amount is not correct")
    Assert.assert_equal(withhold["withhold_channel"], withhold_channel, "withhold_channel is not correct")
    Assert.assert_equal(withhold["withhold_sub_status"], withhold_sub_status, "withhold_sub_status is not correct")
    Assert.assert_equal(withhold["withhold_card_num"], withhold_card_num, "withhold_card_num is not correct")
    Assert.assert_equal(withhold["withhold_payment_type"], withhold_payment_type, "withhold_payment_type is not correct")
    Assert.assert_equal(withhold["withhold_third_serial_no"], withhold_third_serial_no, "withhold_third_serial_no is not correct")
    actual_sign_company = json.loads(withhold["withhold_extend_info"]).get('paysvrSignCompany', None)
    Assert.assert_equal(sign_company, actual_sign_company, f"sign_company应为{sign_company}，实际为{actual_sign_company}")
    Assert.assert_equal(withhold["withhold_request_no"], withhold_request["withhold_request_no"],
                        "withhold_request_no不对")

    # check withhold_detail
    if len(withhold_detail) > 0:
        # 线上还款不可能即还展期又还共债，但是线下可以
        if withhold["withhold_payment_type"] == "collect":
            Assert.assert_equal(sum([x["withhold_order_withhold_amount"] for x in withhold_order]) -
                                (0 if len(trade_tran) == 0 else sum([x["trade_tran_amount"] for x in trade_tran])),
                                sum([x["withhold_detail_withhold_amount"] for x in withhold_detail]),
                                "detail金额为order金额减去trade金额")
        else:
            Assert.assert_equal(sum([x["withhold_order_withhold_amount"] for x in withhold_order]),
                                sum([x["withhold_detail_withhold_amount"] for x in withhold_detail]),
                                "detail金额为order金额减去trade金额")
        Assert.assert_equal(["finish"],
                            list(set([x["withhold_detail_status"] for x in withhold_detail])), "detail状态不对")
        Assert.assert_equal([detail_repay_type],
                            list(set([x["withhold_detail_repay_type"] for x in withhold_detail])), "detail_repay_type状态不对")

    # check withhold_order
    Assert.assert_equal([withhold["withhold_request_no"]],
                        list(set([x["withhold_order_request_no"] for x in withhold_order])), "order_request_no不对")
    Assert.assert_equal([withhold_request["withhold_request_req_key"]],
                        list(set([x["withhold_order_req_key"] for x in withhold_order])), "order_req_key不对")
    Assert.assert_equal(withhold_amount - balance_amount,
                        sum([x["withhold_order_withhold_amount"] for x in withhold_order]), "order_amount总金额不对")
    Assert.assert_equal(["success"],
                        list(set([x["withhold_order_withhold_status"] for x in withhold_order])), "order_status不对")
    # Assert.assert_equal(["normal"],
    #                     list(set([x["withhold_order_withhold_sub_status"] for x in withhold_order])), "order_sub_status不对")
    Assert.assert_equal([order_operate_type],
                        list(set([x["withhold_order_operate_type"] for x in withhold_order])), "order_operate_type不对")

    # check withhold_request
    Assert.assert_equal(request_trade_type, withhold_request["withhold_request_trade_type"], "request_trade_type 不对")

    # check account_recharge
    Assert.assert_equal(account_recharge["account_recharge_account_no"], account["account_no"],
                        "account_recharge_account_no 不对")
    Assert.assert_equal(account_recharge["account_recharge_source_type"], "withhold",
                        "account_recharge_source_type 不对")
    Assert.assert_equal(account_recharge["account_recharge_serial_no"], withhold["withhold_channel_key"],
                        "account_recharge_serial_no 不对")
    Assert.assert_equal(account_recharge["account_recharge_trade_at"], withhold["withhold_finish_at"],
                        "account_recharge_trade_at 不对")
    Assert.assert_equal(account_recharge["account_recharge_amount"], withhold["withhold_amount"],
                        "account_recharge_amount 不对")

    # check account_recharge_log
    Assert.assert_equal(account_recharge_log["account_recharge_log_account_no"], account["account_no"],
                        "account_recharge_log_account_no 不对")
    Assert.assert_equal(account_recharge_log["account_recharge_log_operate_type"], "withhold_recharge",
                        "account_recharge_log_operate_type 不对")
    Assert.assert_equal(account_recharge_log["account_recharge_log_amount_beginning"], 0,
                        "account_recharge_log_amount_beginning 不对")
    Assert.assert_equal(account_recharge_log["account_recharge_log_amount"], withhold["withhold_amount"],
                        "account_recharge_log_amount 不对")
    Assert.assert_equal(account_recharge_log["account_recharge_log_amount_ending"], withhold["withhold_amount"],
                        "account_recharge_log_amount_ending 不对")

    print("==================================df_account_repay start============================")
    df_account_repay = pd.DataFrame.from_records(data=account_repay, columns=['account_repay_order_no',
                                                                              'account_repay_tran_no',
                                                                              'account_repay_amount',
                                                                              'asset_tran_period',
                                                                              'asset_tran_type'])
    mapper = {
        'account_repay_order_no': 'order_no',
        'account_repay_tran_no': 'tran_no',
        'account_repay_amount': 'amount',
        'asset_tran_period': 'period',
        'asset_tran_type': 'tran_type'
    }
    df_account_repay.rename(columns=mapper, inplace=True)
    df_account_repay = df_account_repay.sort_values(by=['order_no', 'tran_no']).set_index(['order_no'])
    print(df_account_repay)
    print("==================================df_account_repay end============================")

    print("==================================df_account_repay_log start============================")
    df_account_repay_log = pd.DataFrame.from_records(data=account_repay_log, columns=['account_repay_log_order_no',
                                                                                      'account_repay_log_tran_no',
                                                                                      'account_repay_log_amount',
                                                                                      'account_repay_log_order_period',
                                                                                      'account_repay_log_tran_type'])
    mapper = {
        'account_repay_log_order_no': 'order_no',
        'account_repay_log_tran_no': 'tran_no',
        'account_repay_log_amount': 'amount',
        'account_repay_log_order_period': 'period',
        'account_repay_log_tran_type': 'tran_type'
    }
    df_account_repay_log.rename(columns=mapper, inplace=True)
    df_account_repay_log = df_account_repay_log.sort_values(by=['order_no', 'tran_no']).set_index(['order_no'])
    print(df_account_repay_log)
    print("==================================df_account_repay_log end============================")

    print("==================================df_wdetail start============================")
    df_wdetail = pd.DataFrame.from_records(data=withhold_detail,
                                           columns=['withhold_detail_asset_item_no',
                                                    'withhold_detail_asset_tran_no',
                                                    'withhold_detail_withhold_amount',
                                                    'withhold_detail_period',
                                                    'asset_tran_type'])
    mapper = {
        'withhold_detail_asset_item_no': 'order_no',
        'withhold_detail_asset_tran_no': 'tran_no',
        'withhold_detail_withhold_amount': 'amount',
        'withhold_detail_period': 'period',
        'asset_tran_type': 'tran_type'
    }
    df_wdetail.rename(columns=mapper, inplace=True)
    df_wdetail = df_wdetail.sort_values(by=['order_no', 'tran_no']).set_index(['order_no'])
    print(df_wdetail)
    print("==================================df_wdetail end============================")

    res = df_account_repay.values == df_wdetail.values
    Assert.assert_equal(res.all(), True, '不相等：\n -----df_account_repay-----\n%s \n -----df_wdetail----\n%s' % (
        df_account_repay[res == False], df_account_repay[res == False]))
    res = df_account_repay_log.values == df_wdetail.values
    Assert.assert_equal(res.all(), True, '不相等：\n -----df_account_repay_log-----\n%s \n -----df_wdetail----\n%s' % (
        df_account_repay[res == False], df_account_repay_log[res == False]))


def check_asset_tran_data(item_no, period_list=[1], finish_time=get_date(fmt="%Y-%m-%d"), asset_status='payoff'):
    """
    检查资产放款成功后的还款计划数据
    1、asset_tran
    2、asset的几个费用字段
    :param asset_status:
    :param period_list:
    :param item_no:
    :param finish_time:
    :return:
    """
    """
       检查资产还款成功后的还款计划数据
       1、asset_tran
       2、asset的几个费用字段
       :param item_no:
       :return:
    """
    asset_info = get_asset_info_by_item_no(item_no)
    asset_tran = get_asset_tran_by_item_no(item_no, period_list)

    if not asset_info:
        raise AssertionError('asset_info无数据！')
    if not asset_tran:
        raise AssertionError('asset_tran无数据！')

    Assert.assert_equal(asset_info[0]["asset_status"], asset_status, "资产状态不对")

    # asset_tran数据准备：dict-->DataFrame
    df_atran = pd.DataFrame.from_records(data=asset_tran,
                                         columns=['asset_tran_period', 'asset_tran_type', 'asset_tran_amount',
                                                  'asset_tran_due_at', 'asset_tran_category', 'asset_tran_finish_at',
                                                  'asset_tran_status'])
    mapper = {
        'asset_tran_period': 'period',
        'asset_tran_type': 'type',
        'asset_tran_amount': 'amount',
        'asset_tran_due_at': 'due_at',
        'asset_tran_category': 'category',
        'asset_tran_finish_at': 'finish_at',
        'asset_tran_status': 'status'
    }
    df_atran.rename(columns=mapper, inplace=True)
    df_atran['due_at'] = df_atran.due_at.apply(lambda x: x[:10])
    df_atran['type'] = df_atran.type.replace(['repayinterest', 'repayprincipal'], ['interest', 'principal'])
    df_atran = df_atran.sort_values(by=['category', 'type', 'period']).set_index(['category', 'type'])

    # 检查期次：asset & asset_tran
    atran_period = df_atran[['period']].max().values[0]
    # Assert.assert_equal(asset_info[0]['asset_period_count'], atran_period,
    #                     '期次不相等：asset_period_count %s，asset_tran %s' % (
    #                         asset_info[0]['asset_period_count'], atran_period))

    # 检查本、息、费总和：asset_tran
    dt_atran = df_atran['amount'].sum(level='category').to_dict()

    # 检查本、息、费总和：asset_tran & asset
    # Assert.assert_equal(asset_info[0]['asset_granted_principal_amount'], dt_atran['principal'],
    #                     '本金总和不相等：asset_granted_principal_amount %s，asset_tran %s' % (
    #                         asset_info[0]['asset_granted_principal_amount'], dt_atran['principal']))
    # Assert.assert_equal(asset_info[0]['asset_principal_amount'], dt_atran['principal'],
    #                     '本金总和不相等：asset_principal_amount %s，asset_tran %s' % (
    #                         asset_info[0]['asset_principal_amount'], dt_atran['principal']))
    # Assert.assert_equal(asset_info[0]['asset_interest_amount'], dt_atran.get('interest', 0),
    #                     '利息总和不相等：asset_interest_amount %s，asset_tran %s' % (
    #                         asset_info[0]['asset_interest_amount'], dt_atran.get('interest', 0)))
    # Assert.assert_equal(asset_info[0]['asset_fee_amount'], dt_atran.get('fee', 0),
    #                     '费用总和不相等：asset_fee_amount %s，asset_tran %s' % (
    #                         asset_info[0]['asset_fee_amount'], dt_atran.get('fee', 0)))

    Assert.assert_equal(asset_info[0]['asset_repaid_principal_amount'], dt_atran['principal'],
                        '本金总和不相等：asset_repaid_principal_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_repaid_principal_amount'], dt_atran['principal']))
    Assert.assert_equal(asset_info[0]['asset_repaid_interest_amount'], dt_atran.get('interest', 0),
                        '本金总和不相等：asset_repaid_interest_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_repaid_interest_amount'], dt_atran.get('interest', 0)))
    Assert.assert_equal(asset_info[0]['asset_repaid_fee_amount'], dt_atran.get('fee', 0),
                        '本金总和不相等：asset_repaid_fee_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_repaid_fee_amount'], dt_atran.get('fee', 0)))
    Assert.assert_equal(asset_info[0]['asset_repaid_late_amount'], dt_atran.get('late', 0),
                        '本金总和不相等：asset_repaid_late_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_repaid_late_amount'], dt_atran.get('late', 0)))

    Assert.assert_equal(asset_info[0]['asset_repaid_amount'],
                        dt_atran.get('principal') + dt_atran.get('interest', 0) +
                        dt_atran.get('late', 0) + dt_atran.get('fee', 0),
                        '本息费总和不相等：asset_repaid_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_repaid_amount'],
                            dt_atran.get('principal') + dt_atran.get('interest', 0) +
                            dt_atran.get('late', 0) + dt_atran.get('fee', 0)))
    df_atran_p = df_atran.loc['principal'].set_index('period')
    # 验证所有期次都已还清
    status_periods = df_atran_p.loc[1:atran_period, 'status'] == 'finish'
    finish_at_periods = df_atran_p.loc[1:atran_period, 'finish_at'].str[:10] == finish_time
    Assert.assert_equal(status_periods.all(), True, '第1期开始应为finish')
    Assert.assert_equal(finish_at_periods.all(), True, f'第1期到第{atran_period}期完成时间是今天')


def check_msg_content_late_fee(msg_no, msg_type, exp_late_interest=180):
    sendmsg_info = get_sendmsg_list_by_order_no_and_type(msg_no, msg_type)
    if not sendmsg_info:
        raise AssertionError('sendmsg_info无数据！')
    asset_sync_data = json.loads(sendmsg_info[0]["sendmsg_content"])
    df_asset_transactions = json_normalize(asset_sync_data["body"]["data"]["asset_transactions"])
    df_asset_transactions = df_asset_transactions.set_index('asset_transaction_type')
    print("==================================df_atran start============================")
    print(df_asset_transactions)
    print("==================================df_atran end============================")
    # 这里只检查了推送消息中的罚息金额和罚息时间
    Assert.assert_equal(df_asset_transactions.loc['lateinterest']['asset_transaction_amount'], exp_late_interest,
                        "罚息金额不对")
    Assert.assert_equal(df_asset_transactions.loc['lateinterest']['asset_transaction_expect_finish_time'],
                        (datetime.now()).strftime("%Y-%m-%d") + " 00:00:00", "罚息时间不对")
    Assert.assert_equal(sendmsg_info[0]["sendmsg_type"], msg_type, "sendmsg_type不对")


def check_late_fee(item_no, exp_late_fee, exp_late_fin=None, period=1):
    late_fee = get_asset_tran_balance_amount_by_item_no(item_no, period, "lateinterest")
    Assert.assert_equal(exp_late_fee, late_fee, "late interest刷的不正确")
    if exp_late_fin is not None:
        late_fin_fee = get_asset_tran_balance_amount_by_item_no(item_no, period, "latefin_service")
        Assert.assert_equal(exp_late_fin, late_fin_fee, "late fin service刷的不正确")


def check_coupon_withhold_detail_vs_asset_tran(item_no, period=1):
    asset_tran = get_asset_tran_by_item_no(item_no, [period])
    coupon = get_coupon_info_by_item_no(item_no)
    withhold = get_withhold_success_by_item_no(item_no)
    withhold_detail = get_withhold_detail_by_item_no(item_no)

    df_wdetail = pd.DataFrame.from_records(data=withhold_detail,
                                           columns=['withhold_detail_serial_no',
                                                    'withhold_detail_period',
                                                    'withhold_detail_asset_tran_type',
                                                    'withhold_detail_asset_tran_no',
                                                    'withhold_detail_withhold_amount',
                                                    'withhold_detail_asset_tran_amount',
                                                    'withhold_detail_asset_tran_balance_amount',
                                                    'withhold_detail_status'])
    mapper = {
        'withhold_detail_serial_no': 'serial_no',
        'withhold_detail_period': 'period',
        'withhold_detail_asset_tran_type': 'type',
        'withhold_detail_withhold_amount': 'amount',
        'withhold_detail_asset_tran_amount': 'tran_amount',
        'withhold_detail_asset_tran_balance_amount': 'tran_balance_amount',
        'withhold_detail_status': 'status'
    }
    df_wdetail.rename(columns=mapper, inplace=True)
    df_wdetail = df_wdetail.sort_values(by=['serial_no', 'type', 'period']).set_index(['serial_no', 'type'])
    df_withhold_amount = df_wdetail['amount'].sum(level='serial_no').to_dict()
    df_tran_amount = df_wdetail['tran_amount'].sum(level='serial_no').to_dict()
    df_tran_balance_amount = df_wdetail['tran_balance_amount'].sum(level='serial_no').to_dict()
    withhold_detail_status = df_wdetail.loc[withhold[-1]["withhold_serial_no"], 'status'] == 'finish'
    Assert.assert_equal(withhold_detail_status.all(), True, 'withhold_detail_status 应finish')
    Assert.assert_equal(df_withhold_amount[withhold[-1]["withhold_serial_no"]], withhold[-1]["withhold_amount"],
                        "代扣明细总额检查")
    Assert.assert_equal(df_tran_amount[withhold[-1]["withhold_serial_no"]],
                        withhold[-1]["withhold_amount"] + coupon[0]['coupon_amount'] * 2,
                        "代扣明细asset_tran_amount总额检查")
    Assert.assert_equal(df_tran_balance_amount[withhold[-1]["withhold_serial_no"]],
                        withhold[-1]["withhold_amount"] + coupon[0]['coupon_amount'] * 2,
                        "代扣明细asset_tran_balance_amount总额检查")

    # 比较withhold_detail和asset_tran的数据
    # asset_tran数据准备：dict-->DataFrame
    df_atran = pd.DataFrame.from_records(data=asset_tran,
                                         columns=['asset_tran_period', 'asset_tran_type', 'asset_tran_amount',
                                                  'asset_tran_no', 'asset_tran_status'])
    mapper = {
        'asset_tran_period': 'period',
        'asset_tran_type': 'type',
        'asset_tran_amount': 'amount',
        'asset_tran_no': 'tran_no',
        'asset_tran_status': 'status'
    }
    df_atran.rename(columns=mapper, inplace=True)
    df_atran = df_atran.sort_values(by=['type', 'period']).set_index(['type'])

    df_wdetail = pd.DataFrame.from_records(data=withhold_detail,
                                           columns=[
                                               'withhold_detail_period',
                                               'withhold_detail_asset_tran_type',
                                               'withhold_detail_asset_tran_amount',
                                               'withhold_detail_asset_tran_no',
                                               'withhold_detail_status'])
    mapper = {
        'withhold_detail_period': 'period',
        'withhold_detail_asset_tran_type': 'type',
        'withhold_detail_asset_tran_amount': 'amount',
        'withhold_detail_asset_tran_no': 'tran_no',
        'withhold_detail_status': 'status'
    }
    df_wdetail.rename(columns=mapper, inplace=True)
    coupon_withhold_detail = [[0, 'coupon', coupon[0]['coupon_amount'], coupon[0]['coupon_no'], 'finish']]
    df_coupon = pd.DataFrame(coupon_withhold_detail, columns=mapper)
    df_wdetail_coupon = df_wdetail.loc[(df_wdetail['type'].isin(['coupon']))]
    # coupon 的代扣明细验证
    res_coupon = df_coupon.values == df_wdetail_coupon.values
    Assert.assert_equal(res_coupon.all(), True, '不相等：\n -----df_coupon-----\n%s \n -----df_wdetail_coupon----\n%s' % (
        df_coupon[res_coupon == False], df_wdetail_coupon[res_coupon == False]))
    # 非coupon的代扣明细验证
    no_coupon_withhold_type = ['repayprincipal', 'repayinterest', 'fin_service', 'latefin_service', 'lateinterest']
    df_wdetail = df_wdetail.loc[(df_wdetail['type'].isin(no_coupon_withhold_type))]
    df_wdetail = df_wdetail.sort_values(by=['type', 'period']).set_index(['type'])
    print("==================================df_atran start============================")
    print(df_atran)
    print("==================================df_atran end============================")

    print("==================================df_wdetail start============================")
    print(df_wdetail)
    print("==================================df_wdetail end============================")
    res = df_atran.values == df_wdetail.values
    Assert.assert_equal(res.all(), True, '不相等：\n -----asset_tran-----\n%s \n -----df_wdetail----\n%s' % (
        df_atran[res == False], df_wdetail[res == False]))


def lock_data_is_here(item_no):
    """
    检查上锁了
    1、asset_tran
    2、asset的几个费用字段
    :param item_no:
    :return:
    """
    withhold_lock = get_withhold_lock_by_item_no(item_no)
    asset_lock = get_asset_lock_by_item_no(item_no)
    if not withhold_lock:
        raise AssertionError(f'{item_no}无withhold_lock数据，未上锁！')
    if not asset_lock:
        raise AssertionError(f'{item_no}无asset_lock数据，未上锁！')


def lock_data_is_not_here(item_no):
    """
    检查解锁了
    1、withhold_lock
    2、asset_lock
    :param item_no:
    :return:
    """
    withhold_lock = get_withhold_lock_by_item_no(item_no)
    asset_lock = get_asset_lock_by_item_no(item_no)
    if withhold_lock:
        raise AssertionError(f'{item_no} withhold_lock有数据，未解锁！')
    if asset_lock:
        raise AssertionError(f'{item_no} asset_lock有数据，未解锁！')


def check_available_refund_response(actual_content, **kwargs):
    exp_code = kwargs.get("code", 0)
    exp_item_no = kwargs.get("item_no")
    exp_refund_no = kwargs.get("refund_no")
    exp_refund_withhold_serial_no = kwargs.get("refund_withhold_serial_no")
    exp_status = kwargs.get("refund_status", 2)
    Assert.assert_equal(exp_code, actual_content['code'],
                        'code不正确：exp_code is %s，act code is %s' % (exp_code, actual_content['code']))
    Assert.assert_equal(exp_item_no, actual_content['data']['refund_list'][0]['item_no'],
                        'exp item is %s，act item is %s' % (
                            exp_item_no, actual_content['data']['refund_list'][0]['item_no']))
    Assert.assert_equal(exp_refund_withhold_serial_no, actual_content['data']['refund_list'][0]['withhold_serial_no'],
                        'exp refund_withhold_serial_no is %s，act refund_withhold_serial_no is %s' % (
                            exp_refund_withhold_serial_no,
                            actual_content['data']['refund_list'][0]['withhold_serial_no']))
    Assert.assert_equal(exp_refund_no, actual_content['data']['refund_list'][0]['refund_no'],
                        'exp refund_no is %s，act refund_no is %s' % (
                            exp_refund_no, actual_content['data']['refund_list'][0]['refund_no']))
    Assert.assert_equal(exp_status, actual_content['data']['refund_list'][0]['refund_status'],
                        'exp refund_status is %s，act refund_status is %s' % (
                            exp_status, actual_content['data']['refund_list'][0]['refund_status']))


def check_provision(item_no, provision_type, amount, tran_type):
    provision = get_provision(provision_item_no=item_no, provision_tran_type=tran_type)[0]
    Assert.assert_equal(provision_type, provision["provision_type"], "provision_type不正确")
    Assert.assert_equal(amount, provision["provision_amount"], "provision_amount不正确")


def check_refund_request(refund_sn, **kwargs):
    refund_request = get_refund_request(refund_request_serial_no=refund_sn)[-1]
    withhold = get_withhold_by_serial_no(refund_request["refund_request_withhold_serial_no"])[-1]
    Assert.assert_equal(
        withhold["withhold_channel_key"]
        if "refund_request_withhold_channel_key" not in kwargs.keys() else kwargs[
            "refund_request_withhold_channel_key"],
        refund_request["refund_request_withhold_channel_key"],
        "refund_request_withhold_channel_key不正确")
    Assert.assert_equal(
        'ready' if "refund_request_status" not in kwargs.keys() else kwargs["refund_request_status"],
        refund_request["refund_request_status"],
        "refund_request_status不正确")
    Assert.assert_equal(
        'online' if "refund_request_trade_type" not in kwargs.keys() else kwargs["refund_request_trade_type"],
        refund_request["refund_request_trade_type"],
        "refund_request_trade_type不正确")
    Assert.assert_equal(
        'repeated_withhold' if "refund_request_scene" not in kwargs.keys() else kwargs["refund_request_scene"],
        refund_request["refund_request_scene"],
        "refund_request_scene不正确")
    Assert.assert_equal(
        withhold["withhold_amount"] if "refund_request_amount" not in kwargs.keys() else kwargs[
            "refund_request_amount"],
        refund_request["refund_request_amount"],
        "refund_request_amount不正确")
    Assert.assert_equal(
        withhold["withhold_amount"]
        if "refund_request_withhold_amount" not in kwargs.keys() else kwargs["refund_request_withhold_amount"],
        refund_request["refund_request_withhold_amount"],
        "refund_request_amount不正确")
    Assert.assert_equal(
        "test_channel" if "refund_request_channel" not in kwargs.keys() else kwargs["refund_request_channel"],
        refund_request["refund_request_channel"],
        "refund_request_channel不正确")


def check_refund_result(refund_sn, **kwargs):
    refund_result = get_refund_result(refund_result_serial_no=refund_sn)[-1]
    withhold = get_withhold_by_serial_no(refund_result["refund_result_withhold_result_serial_no"])[-1]
    Assert.assert_equal(
        withhold["withhold_amount"] if "refund_result_amount" not in kwargs.keys() else kwargs["refund_result_amount"],
        refund_result["refund_result_amount"],
        "refund_result_amount不正确")
    Assert.assert_equal(
        'ready' if "refund_result_status" not in kwargs.keys() else kwargs["refund_result_status"],
        refund_result["refund_result_status"],
        "refund_result_status不正确")
    Assert.assert_equal(
        withhold["withhold_serial_no"],
        refund_result["refund_result_withhold_result_serial_no"],
        "refund_result_withhold_result_serial_no不正确")
    Assert.assert_equal(
        'test_channel' if "refund_result_channel" not in kwargs.keys() else kwargs["refund_result_channel"],
        refund_result["refund_result_channel"],
        "refund_result_channel不正确")
    # Assert.assert_equal(
    #     withhold["withhold_channel_key"],
    #     refund_result["refund_result_channel_key"],
    #     "refund_result_channel_key不正确")
    Assert.assert_match(
        refund_result["refund_result_finish_at"],
        get_date(fmt="%Y-%m-%d") if "refund_result_finish_at" not in kwargs.keys() else kwargs[
            "refund_result_finish_at"],
        "refund_result_finish_at不正确")


def check_withdraw(refund_sn, **kwargs):
    refund_request = get_refund_request(refund_request_serial_no=refund_sn)[-1]
    withhold = get_withhold_by_serial_no(refund_request["refund_request_withhold_serial_no"])[-1]
    withdraw = get_withdraw(withdraw_ref_no=refund_sn)[-1]
    Assert.assert_equal(
        withhold["withhold_amount"] if "withdraw_amount" not in kwargs.keys() else kwargs["withdraw_amount"],
        withdraw["withdraw_amount"],
        "withdraw_amount不正确")
    Assert.assert_equal(
        "test_channel" if "withdraw_channel" not in kwargs.keys() else kwargs["withdraw_channel"],
        withdraw["withdraw_channel"],
        "withdraw_channel不正确")
    Assert.assert_equal(
        "退款代付" if "withdraw_reason" not in kwargs.keys() else kwargs["withdraw_reason"],
        withdraw["withdraw_reason"],
        "withdraw_reason不正确")
    Assert.assert_equal(
        "private" if "withdraw_receiver_type" not in kwargs.keys() else kwargs["withdraw_receiver_type"],
        withdraw["withdraw_receiver_type"],
        "withdraw_receiver_type不正确")
    Assert.assert_equal(
        "ready" if "withdraw_status" not in kwargs.keys() else kwargs["withdraw_status"],
        withdraw["withdraw_status"],
        "withdraw_status不正确")
    Assert.assert_match(
        withdraw["withdraw_finish_at"],
        get_date(fmt="%Y-%m-%d") if "withdraw_finish_at" not in kwargs.keys() else kwargs["withdraw_finish_at"],
        "withdraw_finish_at不正确")
    pass
