import json
import re

import jsonpath
import pandas as pd

from biztest.config.rbiz.central_check_point import central_request_log_check_point
from biztest.function.biz.biz_db_function import get_capital_notify_by_asset_item_no, get_biz_capital_asset_by_item_no, \
    get_biz_capital_asset_tran_by_item_no, get_capital_notify_req_data_by_item_no
from biztest.util.asserts.assert_util import Assert
from biztest.util.es.es import ES
from biztest.util.tools.tools import get_date
import common.global_const as gc


def check_data(data, **kwargs):
    for key, value in kwargs.items():
        Assert.assert_equal(data[key], value, "%s数据有误" % key)


def check_capital_notify(item_no, withhold_serial_no=None, **kwargs):
    rs = get_capital_notify_by_asset_item_no(item_no, withhold_serial_no)
    check_data(rs[0], **kwargs)


def check_capital_notify_not_exist(item_no, start_period=1, end_period=1,
                                   notify_type=('normal', 'overdue', 'advance', 'early_settlement', 'offline'),
                                   status='open'):
    rs = get_capital_notify_by_asset_item_no(item_no, start_period, end_period, notify_type=notify_type, status=status)
    Assert.assert_equal(rs, False, "%s资产推送生成了推送记录" % item_no)


def check_capital_asset(item_no, **kwargs):
    rs = get_biz_capital_asset_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_capital_transaction_col(item_no, df_capital_tran, col_name, col_value,
                                  start_p, end_p, fee_type_in=(), fee_type_not_in=()):
    if col_value is not None:
        if fee_type_in and isinstance(fee_type_in, tuple):
            col_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                range(start_p, end_p + 1)) & df_capital_tran.cap.isin(fee_type_in), col_name] == col_value
        elif fee_type_not_in and isinstance(fee_type_not_in, tuple):
            col_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                range(start_p, end_p + 1)) & ~df_capital_tran.cap.isin(fee_type_not_in), col_name] == col_value
        else:
            col_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                range(start_p, end_p + 1)), col_name] == col_value
        Assert.assert_equal(col_check.all(), True,
                            f'{item_no}的{col_name}应为{col_value}')


def check_capital_transaction_withhold_result_channel(item_no, df_capital_tran, withhold_result_channel_asset,
                                                      withhold_result_channel_fee_type, start_p, end_p):
    # 判断通道，拆分本息（可能资方扣，可能我方扣），其它费用-我方扣
    if withhold_result_channel_asset is not None:
        withhold_result_channel_asset_checkout = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
            range(start_p, end_p + 1)) & df_capital_tran.capital_transaction_type.isin(
            withhold_result_channel_fee_type),
                                                                     'capital_transaction_withhold_result_channel'] == withhold_result_channel_asset
        Assert.assert_equal(withhold_result_channel_asset_checkout.all(), True,
                            f'{item_no}的capital_transaction_withhold_result_channel应为{withhold_result_channel_asset}')

        withhold_result_channel_paysvr_checkout = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
            range(start_p, end_p + 1)) & ~df_capital_tran.capital_transaction_type.isin(
            withhold_result_channel_fee_type), 'capital_transaction_withhold_result_channel'] == 'qsq'
    else:
        withhold_result_channel_paysvr_checkout = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
            range(start_p, end_p + 1)), 'capital_transaction_withhold_result_channel'] == 'qsq'
    Assert.assert_equal(withhold_result_channel_paysvr_checkout.all(), True,
                        f'{item_no}的capital_transaction_withhold_result_channel应为qsq')


def check_capital_transaction_all(item_no, condition, excepts):
    capital_tran = get_biz_capital_asset_tran_by_item_no(item_no)
    df_capital_tran = pd.DataFrame.from_records(data=capital_tran)
    df_capital_tran.loc[df_capital_tran.capital_transaction_period, []]


def check_capital_transaction_for_fee_type(item_no, pd_recharge_list, expect_cols):
    """
    根据其次和费用类型同时检查需要检查的列的值
    :param item_no: 资产编号
    :param pd_recharge_list:还款信息pd
    :param expect_cols:check的列名
    :return:
    """
    fee_type_set = set(pd_recharge_list.capital_transaction_type)
    for fee_type in fee_type_set:
        user_repay_and_channel_period = list(set(pd_recharge_list.loc[pd_recharge_list.capital_transaction_type ==
                                                                      fee_type, 'capital_transaction_period']))
        check_capital_transaction(item_no, start_p=user_repay_and_channel_period[0],
                                  end_p=user_repay_and_channel_period[-1],
                                  fee_type=fee_type,
                                  expect_data=pd_recharge_list,
                                  expect_cols=expect_cols)
    return list(fee_type_set)


def check_capital_transaction(item_no, **kwargs):
    capital_tran = get_biz_capital_asset_tran_by_item_no(item_no)

    # capital_tran数据准备：dict-->DataFrame
    df_capital_tran = pd.DataFrame.from_records(data=capital_tran)
    # df_capital_tran['capital_transaction_user_repay_at'] = df_capital_tran.capital_transaction_user_repay_at.apply(
    #     lambda x: x[:10])
    # df_capital_tran = df_capital_tran.sort_values(by=['capital_transaction_period']).set_index(
    #     ['capital_transaction_period'])
    # 获取参数
    start_p = kwargs.get("start_p", 1)
    end_p = kwargs.get("end_p", 12)
    fee_type = kwargs.get('fee_type', None)
    expect_cols = kwargs.get("expect_cols", None)
    expect_data = kwargs.get("expect_data", None)
    # 开始校验

    # withhold_result_channel_asset不为None,表示要检查withhold_result_channel
    # withhold_result_channel_fee_type为资方代扣费用类型集合，为None表示都是走的我方代扣
    if expect_cols is not None:
        expect_value = expect_data.loc[expect_data.capital_transaction_period.isin(range(start_p, end_p + 1)) &
                                       (expect_data.capital_transaction_type == fee_type), expect_cols]
        actual_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
            range(start_p, end_p + 1)) & (df_capital_tran.capital_transaction_type == fee_type), expect_cols]

    else:
        expect_value = expect_data.loc[df_capital_tran.capital_transaction_period.isin(
            range(start_p, end_p + 1)), expect_cols]
        actual_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
            range(start_p, end_p + 1)), expect_cols]
    res = expect_value.values == actual_check.values
    Assert.assert_equal(res.all(), True,
                        f'{item_no}的{expect_value[res == True]}应为{actual_check[res == True]}')


def check_capital_push_request_log(item_no, channel, task_type, operation_index=0, capital_notify_info=None):
    """
    检查调用资方接口的请求参数
    """
    # 1.获取capital_notify_info推送数据
    if capital_notify_info is None:
        capital_notify_info = get_capital_notify_req_data_by_item_no(item_no)
    scope = {'capital_notify_info': capital_notify_info}
    es = ES("biz-central-%s" % gc.ENV)

    for item in central_request_log_check_point[channel][task_type]:
        check_points_lt = item['check_points']
        if check_points_lt:
            # 2.从es拿到请求日志
            api = "/mock/5de5d515d1784d36471d6041/rbiz_auto_test" + item['api']
            req_log = es.get_request_log(task_type, [api], orderNo=item_no, operation_index=operation_index).get(api)
            print("req_log", req_log)
            Assert.assert_equal(len(check_points_lt), len(req_log), "接口%s调用次数不正确" % api)
            # 3.断言
            for idx in range(len(check_points_lt)):
                req_data = json.loads(req_log[idx]["feign.request"])
                check_points = check_points_lt[idx]
                for k, v in check_points.items():
                    # 实际值，jsonpath解析
                    actual = jsonpath.jsonpath(req_data, k)[0]
                    # 期望值，表达式解析
                    expect = eval(v, scope) if re.search('capital_notify_info', str(v)) else v
                    Assert.assert_equal(expect, actual,
                                        "log检查错误，资产编号：%s, task：%s, 接口：%s, 检查值：%s, 期望：%s, 实际：%s" %
                                        (item_no, task_type, api, k, expect, actual))


def check_capital_push_request_log_by_channel(item_no, channel):
    for task_type in central_request_log_check_point[channel].keys():
        check_capital_push_request_log(item_no, channel, task_type)
