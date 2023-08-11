import jsonpath
import pandas as pd

from biztest.config.rbiz.rbiz_check_point import rbiz_request_log_check_point
from biztest.function.rbiz.rbiz_db_function import *
from biztest.util.asserts.assert_util import Assert
from biztest.util.es.es import ES


def check_data(data, **kwargs):
    for key, value in kwargs.items():
        Assert.assert_equal(data[key], value, "%s数据有误" % key)


def check_withhold_data_by_item_no(item_no, **kwargs):
    rs = get_withhold_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_withhold_data_by_sn(serial_no, **kwargs):
    rs = get_withhold_by_serial_no(serial_no)
    check_data(rs[0], **kwargs)
    return rs


def check_json_rs_data(rs, **kwargs):
    check_data(rs, **kwargs)


def check_task_by_order_no_and_type(order_no, task_type, **kwargs):
    rs = get_task_by_order_no_and_task_type(order_no, task_type)
    check_data(rs[0], **kwargs)


def check_card_by_item_no(item_no, **kwargs):
    rs = get_card_info_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_card_by_card_no(card_no, **kwargs):
    rs = get_card_info_by_card_no(card_no)
    check_data(rs[0], **kwargs)


def check_card_by_card_num(card_num, **kwargs):
    rs = get_card_info_by_card_num(card_num)
    check_data(rs[0], **kwargs)


def check_individual_by_item_no(item_no, **kwargs):
    rs = get_individual_info_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_withhold_card_by_card_num(card_num, **kwargs):
    rs = get_withhold_card_by_card_num(card_num)
    check_data(rs[0], **kwargs)


def check_asset_tran_by_item_no_and_type_and_period(item_no, tran_type, period, **kwargs):
    rs = get_asset_tran_by_item_no_and_type_and_period(item_no, tran_type, period)
    check_data(rs[0], **kwargs)


def check_withhold_request_log(order_no, channel, task_type, merchant_key, operation_index=1):
    """
    检查调用资方接口的请求参数
    """
    # 1.获取asset_info进件数据
    withhold_info = get_withhold_by_serial_no(merchant_key)
    print("withhold_info ", withhold_info)
    scope = {'withhold_info': withhold_info}
    es = ES("repay%s" % gc.ENV)
    for item in rbiz_request_log_check_point[channel][task_type]:
        check_points_lt = item['check_points']
        if check_points_lt:
            # 2.从es拿到请求日志
            api = "/mock/5de5d515d1784d36471d6041/rbiz_auto_test" + item['api']
            req_log = es.get_request_log(task_type, [api], orderNo=order_no, operation_index=operation_index).get(api)
            print(req_log)
            Assert.assert_equal(len(check_points_lt), len(req_log), "接口%s调用次数不正确" % api)
            # 3.断言
            for idx in range(len(check_points_lt)):
                if item['api'] == "/withhold/autoPay":
                    req_data = json.loads(req_log[idx]["http.request"])
                else:
                    req_data = json.loads(req_log[idx]["feign.request"])

                check_points = check_points_lt[idx]
                for k, v in check_points.items():
                    # 实际值，jsonpath解析
                    actual = jsonpath.jsonpath(req_data, k)[0]
                    print("actual ", actual)
                    # 期望值，表达式解析
                    expect = eval(v, scope) if re.search('withhold_info', str(v)) else v
                    Assert.assert_equal(expect, actual,
                                        "log检查错误，request_no：%s, task：%s, 接口：%s, 检查值：%s, 期望：%s, 实际：%s" %
                                        (order_no, task_type, api, k, expect, actual))


def check_request_log_by_channel(item_no, channel):
    for task_type in rbiz_request_log_check_point[channel].keys():
        check_withhold_request_log(item_no, channel, task_type)


def check_withhold_result_without_split(item_no, **kwargs):
    """
    根据检查4张代扣表,拆成1单的情况
    1、withhold：代扣金额，代扣时间，代扣序列号
    2、withhold_detail：
    3、withholg_order：
    4、withhold_request：
    :param item_no:
    :param request_no:
    :return:
    """
    withhold = get_withhold_by_item_no(item_no)
    withhold_detail = get_withhold_detail_by_item_no_and_serial_no(item_no, withhold[0]["withhold_serial_no"])
    withhold_order = get_withhold_order_by_item_no_and_request_no(item_no, withhold[0]["withhold_request_no"])
    withhold_request = get_withhold_request_by_request_no(withhold[0]["withhold_request_no"])
    asset_tran = get_finish_asset_tran_by_item_no(item_no)

    withhold_count = kwargs.get("withhold_count", 1)
    withhold_sign_company = kwargs.get("withhold_sign_company", "tq,tqa,tqb")
    withhold_channel = kwargs.get("withhold_channel", "baidu_tq3_quick")
    withhold_status = kwargs.get("withhold_status", "success")
    withhold_amount = kwargs.get("withhold_amount", 16667)
    coupon_amount = kwargs.get("coupon_amount", 0)

    # 验证withhold表
    actual_sign_company = json.loads(withhold[0]["withhold_extend_info"]).get('paysvrSignCompany', None)
    Assert.assert_equal(withhold_count, len(withhold), f"应该拆成{withhold_count}单，实际拆成了{len(withhold)}")
    Assert.assert_equal(withhold_sign_company, actual_sign_company,
                        f"sign_company应为{withhold_sign_company}，实际为{actual_sign_company}")
    Assert.assert_equal(withhold[0]["withhold_channel"], withhold_channel,
                        f"withhold_channel 应为{withhold_channel}，实际为{withhold[0]['withhold_channel']}")
    Assert.assert_equal(withhold[0]["withhold_amount"], withhold_amount,
                        f"withhold_amount 应为{withhold_amount}，实际为{withhold[0]['withhold_amount']}")
    Assert.assert_equal(withhold[0]["withhold_status"], withhold_status,
                        f"withhold_status 应为{withhold_status}，实际为{withhold[0]['withhold_status']}")

    # 验证withhold_detail表

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

    withhold_detail_status = df_wdetail.loc[withhold[0]["withhold_serial_no"], 'status'] == 'finish'
    Assert.assert_equal(withhold_detail_status.all(), True, 'withhold_detail_status 应finish')
    Assert.assert_equal(df_withhold_amount[withhold[0]["withhold_serial_no"]], withhold[0]["withhold_amount"],
                        "代扣明细总额检查")
    Assert.assert_equal(df_tran_amount[withhold[0]["withhold_serial_no"]],
                        withhold[0]["withhold_amount"] + coupon_amount + coupon_amount,
                        "代扣明细asset_tran_amount总额检查")
    Assert.assert_equal(df_tran_balance_amount[withhold[0]["withhold_serial_no"]],
                        withhold[0]["withhold_amount"] + coupon_amount + coupon_amount,
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
    # check withhold_order
    Assert.assert_equal(withhold_order[0]["withhold_order_serial_no"], withhold[0]["withhold_serial_no"],
                        "withhold_order_serial_no 不对")
    Assert.assert_equal(withhold_order[0]["withhold_order_reference_no"], item_no, "withhold_order_reference_no 不对")
    Assert.assert_equal(withhold_order[0]["withhold_order_withhold_status"], "success",
                        "withhold_order_withhold_status")
    Assert.assert_equal(withhold_order[0]["withhold_order_request_no"], withhold_request[0]["withhold_request_no"],
                        "withhold_order_request_no 不对")
    Assert.assert_equal(withhold_order[0]["withhold_order_req_key"], withhold_request[0]["withhold_request_req_key"],
                        "withhold_order_req_key 不对")


def check_account_recharge_and_repay(id_num, channel_key, start_period=1):
    """
    检查资产还款成功后的账信息
    1、account_recharge
    2、account_recharg_log
    :param id_num:
    :param channel_key:
    :param start_period: 从哪一期开始还款
    :return:
    """
    withhold = get_withhold_by_channel_key(channel_key)
    account = get_account_by_id_num(id_num)
    account_recharge = get_account_recharge_by_channel_key(channel_key)
    account_recharge_log = get_account_recharge_log_by_channel_key(channel_key)
    account_repay = get_account_repay_by_channel_key(channel_key)
    account_repay_log = get_account_repay_log_by_chanel_key(channel_key)
    if not account_recharge:
        raise AssertionError('account_recharge无数据！')
    if not account_recharge_log:
        raise AssertionError('account_recharge_log无数据！')
    if not account_repay:
        raise AssertionError('account_repay无数据！')
    if not account_repay_log:
        raise AssertionError('account_repay_log无数据！')
    # account recharge
    Assert.assert_equal(account_recharge[0]["account_recharge_account_no"], account[0]["account_no"],
                        "account_recharge_account_no 不对")
    Assert.assert_equal(account_recharge[0]["account_recharge_source_type"], "withhold",
                        "account_recharge_source_type 不对")
    Assert.assert_equal(account_recharge[0]["account_recharge_serial_no"], withhold[0]["withhold_channel_key"],
                        "account_recharge_serial_no 不对")
    Assert.assert_equal(account_recharge[0]["account_recharge_trade_at"], withhold[0]["withhold_finish_at"],
                        "account_recharge_trade_at 不对")
    Assert.assert_equal(account_recharge[0]["account_recharge_amount"], withhold[0]["withhold_amount"],
                        "account_recharge_amount 不对")
    Assert.assert_equal(account_recharge_log[0]["account_recharge_log_account_no"], account[0]["account_no"],
                        "account_recharge_log_account_no 不对")
    Assert.assert_equal(account_recharge_log[0]["account_recharge_log_operate_type"], "withhold_recharge",
                        "account_recharge_log_operate_type 不对")
    Assert.assert_equal(account_recharge_log[0]["account_recharge_log_amount"], withhold[0]["withhold_amount"],
                        "account_recharge_log_amount 不对")
    Assert.assert_equal(str(account_repay[0]["account_repay_account_no"]), account[0]["account_no"],
                        "account_repay_account_no 不对")
    Assert.assert_equal(account_repay[0]["account_repay_recharge_serial_no"], withhold[0]["withhold_channel_key"],
                        "account_repay_recharge_serial_no 不对")
    Assert.assert_equal(account_repay[0]["account_repay_order_type"], "asset", "account_repay_order_type 不对")
    Assert.assert_equal(account_repay_log[0]["account_repay_log_repay_no"], account_repay[0]["account_repay_no"],
                        "account_repay_log_repay_no 不对")
    Assert.assert_equal(account_repay_log[0]["account_repay_log_account_no"], account[0]["account_no"],
                        "account_repay_log_account_no 不对")
    Assert.assert_equal(account_repay_log[0]["account_repay_log_operate_type"], "withhold_repay",
                        "account_repay_log_operate_type 不对")
    Assert.assert_equal(account_repay_log[0]["account_repay_log_order_period"], start_period,
                        "account_repay_log_order_period 不对")
    Assert.assert_equal(account_repay_log[0]["account_repay_log_late"], "normal", "account_repay_log_late 不对")
    Assert.assert_equal(str(account_repay_log[0]["account_repay_log_comment"]), "代扣还款", "account_repay_log_comment 不对")
    Assert.assert_equal(int(account[0]["account_balance_amount"]), 0, "账户余额不为0")


def check_asset_tran_repay_one_period(item_no):
    """
    检查资产还款成功后的还款计划数据
    1、asset_tran
    2、asset的几个费用字段
    :param item_no:
    :return:
    """
    asset_info = get_asset_info_by_item_no(item_no)
    asset_tran = get_asset_tran_by_item_no(item_no)

    if not asset_info:
        raise AssertionError('asset_info无数据！')
    if not asset_tran:
        raise AssertionError('asset_tran无数据！')

    Assert.assert_equal(asset_info[0]["asset_status"], "repay", "资产状态不对")

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
    Assert.assert_equal(asset_info[0]['asset_period_count'], atran_period,
                        '期次不相等：asset_period_count %s，asset_tran %s' % (
                            asset_info[0]['asset_period_count'], atran_period))

    # 检查本、息、费总和：asset_tran
    dt_atran = df_atran['amount'].sum(level='category').to_dict()

    # 检查本、息、费总和：asset_tran & asset
    Assert.assert_equal(asset_info[0]['asset_principal_amount'], dt_atran['principal'],
                        '本金总和不相等：asset_principal_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_principal_amount'], dt_atran['principal']))
    Assert.assert_equal(asset_info[0]['asset_principal_amount'], dt_atran['principal'],
                        '本金总和不相等：asset_principal_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_principal_amount'], dt_atran['principal']))
    Assert.assert_equal(asset_info[0]['asset_interest_amount'], dt_atran.get('interest', 0),
                        '利息总和不相等：asset_interest_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_interest_amount'], dt_atran.get('interest', 0)))
    Assert.assert_equal(asset_info[0]['asset_fee_amount'], dt_atran.get('fee', 0),
                        '费用总和不相等：asset_fee_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_fee_amount'], dt_atran.get('fee', 0)))
    Assert.assert_equal(asset_info[0]['asset_total_amount'],
                        dt_atran['principal'] + dt_atran.get('interest', 0) + dt_atran.get('late', 0) + dt_atran.get(
                            'fee', 0),
                        '本息费总和不相等：asset_total_amount %s，asset_tran %s' % (asset_info[0]['asset_total_amount'],
                                                                          dt_atran['principal'] + dt_atran.get(
                                                                              'interest', 0) + dt_atran.get('late',
                                                                                                            0) + dt_atran.get(
                                                                              'fee',
                                                                              0)))

    df_atran = df_atran.sort_values(by=['status', 'finish_at', 'period']).set_index(['period'])
    # 验证第1期还完，第2期后续都未还
    status_period_one = df_atran.loc[1, 'status'] == 'finish'
    finish_at_period_one = df_atran.loc[1, 'finish_at'].str[:10] == get_date(fmt="%Y-%m-%d")
    Assert.assert_equal(status_period_one.all(), True, '第1期应finish')
    Assert.assert_equal(finish_at_period_one.all(), True, '第1期finish了，时间是当天')
    status_period_others = df_atran.loc[2:atran_period, 'status'] == 'nofinish'
    finish_at_period_others = df_atran.loc[2:atran_period, 'finish_at'] <= '2000-01-01 00:00:00'
    Assert.assert_equal(status_period_others.all(), True, '第2期开始应为nofinish')
    Assert.assert_equal(finish_at_period_others.all(), True, '第2期finish_at应小于2000-01-01 00:00:00')


def check_asset_tran_payoff(item_no):
    """
    检查资产还款成功后的还款计划数据
    1、asset_tran
    2、asset的几个费用字段
    :param item_no:
    :return:
    """
    asset_info = get_asset_info_by_item_no(item_no)
    asset_tran = get_asset_tran_by_item_no(item_no)

    if not asset_info:
        raise AssertionError('asset_info无数据！')
    if not asset_tran:
        raise AssertionError('asset_tran无数据！')

    Assert.assert_equal(asset_info[0]["asset_status"], "payoff", "资产状态不对")

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
    Assert.assert_equal(asset_info[0]['asset_period_count'], atran_period,
                        '期次不相等：asset_period_count %s，asset_tran %s' % (
                            asset_info[0]['asset_period_count'], atran_period))

    # 检查本、息、费总和：asset_tran
    dt_atran = df_atran['amount'].sum(level='category').to_dict()

    # 检查本、息、费总和：asset_tran & asset
    Assert.assert_equal(asset_info[0]['asset_principal_amount'], dt_atran['principal'],
                        '本金总和不相等：asset_principal_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_principal_amount'], dt_atran['principal']))
    Assert.assert_equal(asset_info[0]['asset_principal_amount'], dt_atran['principal'],
                        '本金总和不相等：asset_principal_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_principal_amount'], dt_atran['principal']))
    Assert.assert_equal(asset_info[0]['asset_interest_amount'], dt_atran.get('interest', 0),
                        '利息总和不相等：asset_interest_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_interest_amount'], dt_atran.get('interest', 0)))
    Assert.assert_equal(asset_info[0]['asset_fee_amount'], dt_atran.get('fee', 0),
                        '费用总和不相等：asset_fee_amount %s，asset_tran %s' % (
                            asset_info[0]['asset_fee_amount'], dt_atran.get('fee', 0)))

    Assert.assert_equal(asset_info[0]['asset_total_amount'],
                        dt_atran['principal'] + dt_atran.get('interest', 0) + dt_atran.get('late', 0) + dt_atran.get(
                            'fee', 0),
                        '本息费总和不相等：asset_total_amount %s，asset_tran %s' % (asset_info[0]['asset_total_amount'],
                                                                          dt_atran['principal'] + dt_atran.get(
                                                                              'interest', 0) + dt_atran.get('late',
                                                                                                            0) + dt_atran.get(
                                                                              'fee', 0)))

    df_atran = df_atran.sort_values(by=['period', 'status', 'finish_at']).set_index(['period'])
    # 验证所有期次都已还清
    status_periods = df_atran.loc[1:atran_period, 'status'] == 'finish'
    finish_at_periods = df_atran.loc[1:atran_period, 'finish_at'].str[:10] == get_date(fmt="%Y-%m-%d")
    Assert.assert_equal(status_periods.all(), True, '第1期开始应为finish')
    Assert.assert_equal(finish_at_periods.all(), True, f'第1期到第{atran_period}期完成时间是今天')


def check_msg_content_late_fee(msg_no, msg_type):
    sendmsg_info = get_sendmsg_list_by_order_no_and_type(msg_no, msg_type)
    late_asset_tran = get_asset_tran_by_item_no_and_type(msg_no, "lateinterest")
    if not sendmsg_info:
        raise AssertionError('sendmsg_info无数据！')
    # 应生成罚息推给fox
    late_fee = {
        "asset_transaction_type": late_asset_tran[0]["asset_tran_type"],
        "asset_transaction_amount": late_asset_tran[0]["asset_tran_amount"],
        "asset_transaction_status": "unfinish",
        "asset_transaction_expect_finish_time": (datetime.now()).strftime("%Y-%m-%d") + " 00:00:00",
        "asset_transaction_finish_at": None,
        "asset_transaction_period": 1,
        "asset_transaction_remark": "",
        "asset_transaction_decrease_amount": 0,
        "asset_transaction_repaid_amount": 0
    }
    asset_sync_data = json.loads(sendmsg_info[0]["sendmsg_content"])
    # 罚息的位置有时候很在第1个节点，有时候在第2个节点
    late_fee_location = 0
    if asset_sync_data["body"]["data"]["asset_transactions"][1]["asset_transaction_type"] == "repaylateinterest":
        late_fee_location = 1
    Assert.assert_equal(sendmsg_info[0]["sendmsg_type"], msg_type, "sendmsg_type不对")
    Assert.assert_match_json(late_fee, asset_sync_data["body"]["data"]["asset_transactions"][late_fee_location],
                             "sendmsg_content的late fee内容不正确")


def check_card_bind_info(card_number, **kwargs):
    card_bind_serial_no = kwargs.get("card_bind_serial_no")
    card_bind_channel = kwargs.get("card_bind_channel")
    card_bind_status = kwargs.get("card_bind_status", "success")
    card_bind = get_card_bind_by_card_number(card_number, card_bind_serial_no)

    if not card_bind:
        raise AssertionError('card_bind无数据！')
    Assert.assert_equal(card_bind[0]["card_bind_serial_no"], card_bind_serial_no,
                        f"card_number{card_number}的card_bind_serial_no 不对")
    Assert.assert_equal(card_bind[0]["card_bind_channel"], card_bind_channel,
                        f"card_number{card_number}的card_bind_channel 不对")
    Assert.assert_equal(card_bind[0]["card_bind_status"], card_bind_status,
                        f"card_number{card_number}的card_bind_status 不对")
    # Assert.assert_equal(card_bind[0]["card_bind_req_data"], card_bind_req_data, "trade_tran_amount 不对")
    # Assert.assert_equal(card_bind[0]["card_bind_res_data"], card_bind_res_data, "trade_tran_amount 不对")


# 拆单的代扣检查从这里开始

def check_withhold_split_count_by_request_no(request_no, withhold_count):
    """
    检查代扣成功后的拆单单数,根据withhold_request_no,
    场景1： 检查大小单是否会合并，应不合并。
    场景2： 检查主动代扣是大小单一起扣，但是会拆
    场景3： 自动代扣有多个request_no
    1、withhold：
    :param request_no:
    :param withhold_count:
    :return:
    """
    withhold = get_withhold_data_by_request_no(request_no)
    withhold_order = get_withhold_order_by_request_no(request_no)
    withhold_request = get_withhold_request_by_request_no(request_no)
    Assert.assert_equal(withhold_count, len(withhold),
                        f"代扣request {request_no}应该拆成{withhold_count}单，实际拆成了{len(withhold)}")
    Assert.assert_equal(withhold_count, len(withhold_order),
                        f"代扣request {request_no}应该拆成{withhold_count}单，实际拆成了{len(withhold_order)}")
    Assert.assert_equal(1, len(withhold_request),
                        f"代扣request {request_no}withhold_request应该拆成1单，实际拆成了{len(withhold_request)}")


def check_withhold_split_count_by_item_no_and_request_no(item_no, request_no, withhold_count):
    """
    检查代扣成功后的拆单单数,检查一笔资产在同一个request拆成了几单
    1、withhold：
    :param request_no:
    :param item_no:
    :param withhold_count:
    :return:
    """
    withhold = get_withhold_by_item_no_and_request_no(item_no, request_no)
    withhold_order = get_withhold_order_by_item_no_and_request_no(item_no, request_no)
    withhold_request = get_withhold_request_by_request_no(request_no)
    Assert.assert_equal(withhold_count, len(withhold), f"资产{item_no}应该拆成{withhold_count}单，实际拆成了{len(withhold)}")
    Assert.assert_equal(withhold_count, len(withhold_order),
                        f"资产{item_no}应该拆成{withhold_count}单，实际拆成了{len(withhold_order)}")
    Assert.assert_equal(1, len(withhold_request), f"withhold_request {request_no}应该拆成1单，实际拆成了{len(withhold_request)}")


def check_withhold_sign_company(order_no, sign_company):
    """
        根据代扣流水号检查sign company
        1、withhold：
        :param order_no:
        :param sign_company:
        :return:
    """
    withhold = get_withhold_by_serial_no(order_no)
    actual_sign_company = json.loads(withhold[0]["withhold_extend_info"]).get('paysvrSignCompany', None)
    Assert.assert_equal(sign_company, actual_sign_company,
                        f"order_no{order_no}的sign_company应为{sign_company}，实际为{actual_sign_company}")


def check_withhold_order_by_order_no(order_no, channel='shilong_siping'):
    """
       检查拆成2单的代扣顺序，这是目前还款最多的场景
       1、withhold：
    """
    withhold = get_withhold_by_serial_no(order_no)
    Assert.assert_equal(withhold[0]["withhold_channel"], channel, f'{order_no} withhold_channel应为{channel}')


def check_withhold_by_serial_no(order_no, **kwargs):
    """
    根据serial_no检查代扣情况，withhold表
    1、withhold：代扣金额，代扣时间，代扣序列号
    2、withhold_detail：
    3、withhold_order：
    4、withhold_request：
    :param order_no:
    :return:
    """
    withhold = get_withhold_by_serial_no(order_no)
    withhold_detail = get_withhold_detail_by_serial_no(order_no)
    withhold_order = get_withhold_order_by_serial_no(order_no)
    withhold_request = get_withhold_request_by_serial_no(order_no)

    withhold_sign_company = kwargs.get("withhold_sign_company", "tq,tqa,tqb")
    withhold_channel = kwargs.get("withhold_channel", "baidu_tq3_quick")
    withhold_status = kwargs.get("withhold_status", "success")
    withhold_amount = kwargs.get("withhold_amount", 401133)
    asset_tran_amount = kwargs.get("asset_tran_amount", 402833)

    # 验证withhold表
    actual_sign_company = json.loads(withhold[0]["withhold_extend_info"]).get('paysvrSignCompany', None)
    Assert.assert_equal(withhold_sign_company, actual_sign_company,
                        f"order_no {order_no}的sign_company应为{withhold_sign_company}，实际为{actual_sign_company}")
    Assert.assert_equal(withhold[0]["withhold_channel"], withhold_channel,
                        f"order_no {order_no}的withhold_channel 应为{withhold_channel}，实际为{withhold[0]['withhold_channel']}")
    Assert.assert_equal(withhold[0]["withhold_amount"], withhold_amount,
                        f"order_no {order_no}的withhold_amount 应为{withhold_amount}，实际为{withhold[0]['withhold_amount']}")
    Assert.assert_equal(withhold[0]["withhold_status"], withhold_status,
                        f"order_no {order_no}的withhold_status 应为{withhold_status}，实际为{withhold[0]['withhold_status']}")

    # 验证withhold_detail表
    df_detail = pd.DataFrame.from_records(data=withhold_detail,
                                          columns=['withhold_detail_serial_no',
                                                   'withhold_detail_period',
                                                   'withhold_detail_type',
                                                   'withhold_detail_asset_tran_no',
                                                   'withhold_detail_withhold_amount',
                                                   'withhold_detail_asset_tran_amount',
                                                   'withhold_detail_asset_tran_balance_amount',
                                                   'withhold_detail_status'])
    mapper = {
        'withhold_detail_serial_no': 'serial_no',
        'withhold_detail_period': 'period',
        'withhold_detail_type': 'type',
        'withhold_detail_asset_tran_no': 'tran_no',
        'withhold_detail_withhold_amount': 'amount',
        'withhold_detail_asset_tran_amount': 'tran_amount',
        'withhold_detail_asset_tran_balance_amount': 'tran_balance_amount',
        'withhold_detail_status': 'status'
    }
    df_detail.rename(columns=mapper, inplace=True)
    df_wdetail = df_detail.sort_values(by=['type', 'period']).set_index(['serial_no', 'type'])
    df_withhold_amount = df_wdetail['amount'].sum(level='serial_no').to_dict()
    df_tran_amount = df_wdetail['tran_amount'].sum(level='serial_no').to_dict()
    df_tran_balance_amount = df_wdetail['tran_balance_amount'].sum(level='serial_no').to_dict()

    withhold_detail_status = df_wdetail.loc[withhold[0]["withhold_serial_no"], 'status'] == 'finish'
    Assert.assert_equal(withhold_detail_status.all(), True, 'order_no {order_no}的 withhold_detail_status 应finish')
    Assert.assert_equal(df_withhold_amount[withhold[0]["withhold_serial_no"]], withhold[0]["withhold_amount"],
                        f"order_no {order_no}的 代扣明细总额检查不通过")
    Assert.assert_equal(df_tran_amount[withhold[0]["withhold_serial_no"]], asset_tran_amount,
                        f"order_no {order_no}的 代扣明细asset_tran_amount总额检查不通过")
    Assert.assert_equal(df_tran_balance_amount[withhold[0]["withhold_serial_no"]], asset_tran_amount,
                        f"order_no {order_no}的 代扣明细asset_tran_balance_amount总额检查不通过")
    # check withhold_order
    Assert.assert_equal(withhold_order[0]["withhold_order_serial_no"], withhold[0]["withhold_serial_no"],
                        f"withhold_order {withhold_order[0]['withhold_order_serial_no']}的 withhold_order_serial_no 不对")
    Assert.assert_equal(withhold_order[0]["withhold_order_reference_no"],
                        withhold_order[0]['withhold_order_reference_no'], "withhold_order_reference_no 不对")
    Assert.assert_equal(withhold_order[0]["withhold_order_withhold_status"], "success",
                        f"order_no {order_no}的  withhold_order_withhold_status")
    Assert.assert_equal(withhold_order[0]["withhold_order_request_no"], withhold_request[0]["withhold_request_no"],
                        f"order_no {order_no}的  withhold_order_request_no 不对")
    Assert.assert_equal(withhold_order[0]["withhold_order_req_key"], withhold_request[0]["withhold_request_req_key"],
                        f"order_no {order_no}的 withhold_order_req_key 不对")


def check_capital_withhold_detail_vs_asset_tran(order_no, capital_withhold_type=['repayprincipal', 'repayinterest']):
    """
    第一期本息给资方扣的场景，验证withhold_detail_and_asset_tran拆单金额
    :param order_no:
    :param period:
    :param capital_withhold_type:拆单时拆给资方的费用类型
    :return:
    """
    withhold_detail = get_withhold_detail_by_serial_no(order_no)
    withhold_order = get_withhold_order_by_serial_no(order_no)
    asset_tran = get_finish_asset_tran_by_item_no(withhold_order[0]['withhold_order_reference_no'])

    # 验证withhold_detail表
    df_detail = pd.DataFrame.from_records(data=withhold_detail,
                                          columns=[
                                              'withhold_detail_period',
                                              'withhold_detail_asset_tran_type',
                                              'withhold_detail_asset_tran_no',
                                              'withhold_detail_withhold_amount',
                                              'withhold_detail_status'])
    mapper = {

        'withhold_detail_period': 'period',
        'withhold_detail_asset_tran_type': 'type',
        'withhold_detail_asset_tran_no': 'tran_no',
        'withhold_detail_withhold_amount': 'tran_amount',
        'withhold_detail_status': 'status'
    }
    df_detail.rename(columns=mapper, inplace=True)
    df_w_detail = df_detail.sort_values(by=['type', 'period']).set_index(['type'])

    print("==================================df_w_detail start============================")
    print(df_w_detail)
    print("==================================df_w_detail end============================")

    # 比较withhold_detail和asset_tran的数据
    # asset_tran数据准备：dict-->DataFrame
    df_atran = pd.DataFrame.from_records(data=asset_tran,
                                         columns=['asset_tran_period', 'asset_tran_type',
                                                  'asset_tran_no', 'asset_tran_amount', 'asset_tran_status'])
    mapper = {
        'asset_tran_period': 'period',
        'asset_tran_type': 'type',
        'asset_tran_no': 'tran_no',
        'asset_tran_amount': 'amount',
        'asset_tran_status': 'status'
    }
    df_atran.rename(columns=mapper, inplace=True)
    df_atran = df_atran.set_index(['type']).loc[capital_withhold_type].sort_values(by=['type'])

    print("==================================df_atran_filter_interest start============================")
    print(df_atran)
    print("==================================df_atran_filter_interest end============================")

    res = df_atran.values == df_w_detail.values
    Assert.assert_equal(res.all(), True, '不相等：\n -----asset_tran-----\n%s \n -----df_wdetail----\n%s' % (
        df_atran[res == False], df_w_detail[res == False]))


def check_settle_payoff_capital_withhold_detail_vs_asset_tran(order_no, interest_amount=None):
    """
    本息拆给资方扣的代扣明细和用户还款计划对比-提前结清拆单的场景，本金全额+占有天数利息给资方扣，
    第一期内提前结清的场景数据检查
    :param order_no:
    :param interest_amount: 第1期占用天数利息
    :return:
    """
    withhold_detail = get_withhold_detail_by_serial_no(order_no)
    withhold_order = get_withhold_order_by_serial_no(order_no)
    asset_tran = get_finish_asset_tran_by_item_no(withhold_order[0]['withhold_order_reference_no'])

    # 验证withhold_detail表
    # 验证withhold_detail表
    df_detail = pd.DataFrame.from_records(data=withhold_detail,
                                          columns=[
                                              'withhold_detail_period',
                                              'withhold_detail_type',
                                              'withhold_detail_asset_tran_no',
                                              'withhold_detail_withhold_amount',
                                              'withhold_detail_status'])
    mapper = {

        'withhold_detail_period': 'period',
        'withhold_detail_type': 'type',
        'withhold_detail_asset_tran_no': 'tran_no',
        'withhold_detail_withhold_amount': 'tran_amount',
        'withhold_detail_status': 'status'
    }
    df_detail.rename(columns=mapper, inplace=True)
    df_w_detail = df_detail.sort_values(by=['type', 'period']).set_index(['type'])

    print("==================================df_w_detail start============================")
    print(df_w_detail)
    print("==================================df_w_detail end============================")

    # 比较withhold_detail和asset_tran的数据
    # asset_tran数据准备：dict-->DataFrame
    df_atran = pd.DataFrame.from_records(data=asset_tran,
                                         columns=['asset_tran_period', 'asset_tran_category',
                                                  'asset_tran_no', 'asset_tran_amount', 'asset_tran_status'])
    mapper = {
        'asset_tran_period': 'period',
        'asset_tran_category': 'type',
        'asset_tran_no': 'tran_no',
        'asset_tran_amount': 'amount',
        'asset_tran_status': 'status'
    }
    df_atran.rename(columns=mapper, inplace=True)
    df_atran_filter_principal = df_atran.loc[
        (df_atran['type'].isin(['principal']))]
    df_atran_filter_interest = df_atran.loc[
        (df_atran['type'].isin(['interest'])) & (df_atran['period'].isin(['1']))]
    if interest_amount is not None:
        df_atran_filter_interest.loc[df_atran_filter_interest['amount'] > 0, 'amount'] = interest_amount
    df_atran = pd.concat([df_atran_filter_principal, df_atran_filter_interest])
    df_atran = df_atran.sort_values(by=['type', 'period']).set_index(['type'])
    print("==================================df_atran_filter_interest start============================")
    print(df_atran)
    print("==================================df_atran_filter_interest end============================")

    res = df_atran.values == df_w_detail.values
    Assert.assert_equal(res.all(), True, '不相等：\n -----asset_tran-----\n%s \n -----df_wdetail----\n%s' % (
        df_atran[res == False], df_w_detail[res == False]))


def check_response_after_apply_success(self, repay_resp, withhold, withhold_no_loan):
    check_json_rs_data(repay_resp, code=0, message='交易处理中')
    check_json_rs_data(repay_resp['data'], type="BIND_SMS")
    check_json_rs_data(repay_resp['data']['project_list'][0], status=2, memo='处理中',
                       project_num=self.item_num_no_loan, order_no=withhold_no_loan[0]['withhold_serial_no'])
    check_json_rs_data(repay_resp['data']['project_list'][1], status=2, memo='处理中',
                       project_num=self.item_no, order_no=withhold[0]['withhold_serial_no'])


def change_asset_due_at_in_rbiz(advance_month, item_no, item_no_x, is_grant_day=False, advance_day=-1,
                                compensate_time=None):
    """
    修改资产放款时间及资产还款计划的到日期
    :param advance_month: 提前多少个月, 负数，推后是正数
    :param advance_day: 提前多少天, 负数，推后是正数
    :param item_no: 大单资产编号
    :param item_no_x: 小单资产编号
    :param compensate_time: 资方还款计划代偿日
    :param is_grant_day: 是否是放款日
    :return:
    """
    asset = get_asset_info_by_item_no(item_no)
    count = int(asset[0]["asset_period_count"])
    period_day = int(asset[0]["asset_product_category"])
    if count == 1:
        grant_time = get_calc_date_base_today(day=0) if is_grant_day else \
            get_calc_date_base_today(day=advance_day)
    else:
        grant_time = get_calc_date_base_today(month=advance_month) if is_grant_day else \
            get_calc_date_base_today(month=advance_month, day=advance_day)
    for period in range(1, count + 1):
        due_delay_month = period + advance_month
        if count == 1:
            due_time = get_calc_date_base_today(day=period_day, fmt="%Y-%m-%d") if is_grant_day else \
                get_calc_date_base_today(day=period_day + advance_day, fmt="%Y-%m-%d")
        else:
            due_time = get_calc_date_base_today(month=due_delay_month, fmt="%Y-%m-%d") if is_grant_day else \
                get_calc_date_base_today(month=due_delay_month, day=advance_day, fmt="%Y-%m-%d")

            print("compensate_time", compensate_time)
            print("due_time", due_time)
            cap_due_time = due_time[:-2] + str(compensate_time) if compensate_time else due_time
        for item in (item_no, item_no_x):
            # 更新asset记录
            if item:
                if period == 1:
                    item_no_str = 'update asset set asset_grant_at = "{0}", asset_effect_at = ' \
                                  '"{0}", asset_actual_grant_at = "{0}"' \
                                  ' where asset_item_no = "{1}"'.format(grant_time,
                                                                        item)
                    gc.REPAY_DB.update(item_no_str)
                # 更新asset_tran记录
                item_no_period_first = 'update asset_tran set asset_tran_due_at = "{0}" ' \
                                       'where asset_tran_asset_item_no = "{1}" and ' \
                                       'asset_tran_period = {2}'.format(due_time, item, period)
                gc.REPAY_DB.update(item_no_period_first)

                capital_tran = 'UPDATE capital_transaction SET capital_transaction_expect_finished_at = "{0}" ' \
                               'WHERE capital_transaction_item_no = "{1}" AND ' \
                               'capital_transaction_period = {2}'.format(cap_due_time, item, period)
                gc.REPAY_DB.update(item_no_period_first)
                gc.REPAY_DB.update(capital_tran)

    return item_no, item_no_x, ""
