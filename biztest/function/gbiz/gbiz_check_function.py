import json
import time
from biztest.function.gbiz.gbiz_db_function import get_capital_asset_tran_by_item_no, get_asset_event, \
    get_task_by_item_no_and_task_type,  get_task_by_item_no_and_task_type,\
    update_capital_blacklist_expired_at, get_asset_confirm, get_asset_loan_record_by_item_no, \
    get_capital_asset_by_item_no, get_asset_tran_by_item_no, \
    get_capital_tran_period_amount_lt, get_capital_tran_total_amount, get_asset_tran_total_amount, \
    get_asset_tran_period_amount_lt, get_asset_route_log_by_idum, get_confirm_data_by_item_no, get_sendmsg, \
    get_capital_blacklist_data_by_card, get_withdraw_order_by_item_no, get_withdraw_record_by_item_no, \
    get_router_load_record_by_key, get_capital_account_by_item_no_channel, get_capital_account_step_by_item_no_way, \
    get_asset_import_data_by_item_no, get_router_load_record_by_idum, get_latest_circuit_break_record, \
    get_circuit_break_action
from biztest.function.gbiz.gbiz_common_function import run_terminated_task, get_rule_code
from biztest.config.gbiz.gbiz_check_point import request_log_check_point
from biztest.util.asserts.assert_util import Assert
from pprint import pprint
from biztest.interface.cmdb.cmdb_interface import *
from biztest.function.cmdb.cmdb_common_function import get_comprehensive_fee
from biztest.function.cmdb.cmdb_db_function import get_root_rate_config_info, get_rate_info
import pandas as pd
from biztest.util.es.es import ES
import common.global_const as gc
import jsonpath, re, decimal


def check_asset_void_data(item_no):
    """
    检查资产做废后，各个表的数据
    :param item_no:
    :return:
    """
    asset_info = get_asset_info_by_item_no(item_no)
    alr_info = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(asset_info[0]["asset_status"], "void", "资产状态不对")
    Assert.assert_equal(alr_info[0]["asset_loan_record_status"], 5, "alr状态不对")


def check_capital_blacklist_data(asset_info, capital_blacklist_type, message):
    """
    检查加入黑名单之后，表中数据的正确性
    :param item_no:
    :return:
    """
    bankcard_encryt = asset_info['data']['receive_card']['num_encrypt']
    idnum_encrypt = asset_info['data']['borrower']['idnum_encrypt']
    channel = asset_info['data']['asset']['loan_channel']
    if capital_blacklist_type == "bank_card":
        blacklist_data = get_capital_blacklist_data_by_card(bankcard_encryt)
        Assert.assert_equal(blacklist_data[0]["capital_blacklist_value"], bankcard_encryt, "加入黑名单的卡号不对")
        Assert.assert_equal(blacklist_data[0]["capital_blacklist_channel"], channel, "加入黑名单的资金方不正确")
        Assert.assert_equal(blacklist_data[0]["capital_blacklist_type"], capital_blacklist_type, "加入黑名单的type不正确")
        Assert.assert_match(blacklist_data[0]["capital_blacklist_reason"], message, "加入黑名单原因不正确")

    if capital_blacklist_type == "id_card":
        blacklist_data = get_capital_blacklist_data_by_card(idnum_encrypt)
        Assert.assert_equal(blacklist_data[0]["capital_blacklist_value"], idnum_encrypt, "加入黑名单的身份证号不对")
        Assert.assert_equal(blacklist_data[0]["capital_blacklist_channel"], channel, "加入黑名单的资金方不正确")
        Assert.assert_equal(blacklist_data[0]["capital_blacklist_type"], capital_blacklist_type, "加入黑名单的type不正确")
        Assert.assert_match(blacklist_data[0]["capital_blacklist_reason"], message, "加入黑名单原因不正确")
    # 避免因为黑名单路由挡住，这里将黑名单的有效期修改了
    # update_capital_blacklist_expired_at(bankcard_encryt, channel)


def check_task_res(task_res):
    try:
        if task_res['code'] in [0, "0"]:
            return 1
        else:
            raise ("task 执行错误,返回:{0}".format(str(task_res)))
    except AssertionError:
        print("task 执行错误,返回:{0}".format(str(task_res)))


def check_change_card_data(item_no, change_status, change_times):
    """
    检查兜底换卡相关数据
    1、alr：状态为5， memo为当前卡交易失败，等待换卡
    2、asset：状态sale，资方xxx
    2、asset_event：每换卡一次，生成一个event
    3、asset_confirm：confirm_status 0:成功,1:失败,2:处理中,3:超时

    :param item_no: 资产编号
    :param change_status：换卡状态
    :param change_times：换卡次数
    :return:
    """
    asset_info = get_asset_info_by_item_no(item_no)
    Assert.assert_equal(asset_info[0]["asset_status"], "sale", "资产状态不对")
    alr_info = get_asset_loan_record_by_item_no(item_no)
    if change_status == 0 or change_status == 1:
        Assert.assert_equal(alr_info[0]["asset_loan_record_status"], 4, "alr状态不对")
        Assert.assert_equal(alr_info[0]["asset_loan_record_memo"], "当前卡交易失败，等待换卡", "alr备注不对")
    elif change_status == 2:
        Assert.assert_equal(alr_info[0]["asset_loan_record_status"], 5, "alr状态不对")
        Assert.assert_equal(alr_info[0]["asset_loan_record_memo"], "当前卡交易失败，等待换卡", "alr备注不对")
    elif change_status == 3:
        Assert.assert_equal(alr_info[0]["asset_loan_record_status"], 4, "alr状态不对")
        Assert.assert_equal(alr_info[0]["asset_loan_record_memo"], "当前卡交易失败，等待换卡", "alr备注不对")
    else:
        raise Exception("changet status 不对")

    event_list = get_asset_event(item_no)
    Assert.assert_equal(len(event_list), change_times, '换卡event次数不对')

    confirm_list = get_asset_confirm(item_no)
    Assert.assert_equal(change_status, confirm_list[0]['asset_confirm_status'], "确认状态不对")


def check_asset_success_data(item_no):
    """
    检查资产放款成功后的数据
    1、asset：状态payoff，资方，放款时间
    2、alr：状态为6，时间
    3、assert_tran：
    4、capital_asset：
    5、capital_assert_tran：
    :param item_no:
    :return:
    """
    asset_info = get_asset_info_by_item_no(item_no)
    pprint(asset_info)
    Assert.assert_equal(asset_info[0]["asset_status"], "repay", "资产状态不对")
    Assert.assert_equal(asset_info[0]["asset_grant_at"][:10], get_date(fmt="%Y-%m-%d"), "asset_grant_at")
    Assert.assert_equal(asset_info[0]["asset_effect_at"][:10], get_date(fmt="%Y-%m-%d"), "asset_effect_at")
    Assert.assert_equal(asset_info[0]["asset_actual_grant_at"][:10], get_date(fmt="%Y-%m-%d"), "asset_actual_grant_at不对")
    if asset_info[0]['asset_period_type'] == "day":
        Assert.assert_equal(asset_info[0]["asset_due_at"][:10],
                            get_date(day=asset_info[0]['asset_product_category'], fmt="%Y-%m-%d"),
                            "asset_due_at")
    elif asset_info[0]['asset_period_type'] == "month":
        Assert.assert_equal(asset_info[0]["asset_due_at"][:10],
                            get_date(month=asset_info[0]['asset_period_count'], fmt="%Y-%m-%d"),
                            "asset_due_at")
    else:
        raise AssertionError

    alr_info = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(alr_info[0]["asset_loan_record_status"], 6, "alr状态不对")
    Assert.assert_equal(alr_info[0]["asset_loan_record_memo"], "", "alr备注不对")


def check_asset_tran_data(item_no):
    """
    检查资产放款成功后的还款计划数据
    1、asset_tran，与cmdb数据比较
    2、asset的几个费用字段
    3、capital_asset
    4、capital_transaction
    :param item_no:
    :return:
    """
    asset_info = get_asset_info_by_item_no(item_no)
    asset_tran = get_asset_tran_by_item_no(item_no)
    capital_asset = get_capital_asset_by_item_no(item_no)
    capital_tran = get_capital_asset_tran_by_item_no(item_no)
    cmdb_tran = cmdb_rate_repay_calculate_v6_by_item_no(item_no)

    if not asset_info:
        raise AssertionError('asset_info无数据！')
    if not asset_tran:
        raise AssertionError('asset_tran无数据！')
    if not capital_asset:
        raise AssertionError('capital_asset无数据！')
    if not capital_tran:
        raise AssertionError('capital_transaction无数据！')
    if cmdb_tran['code'] != 0:
        raise AssertionError('cmdb数据异常！')

    # asset_tran数据准备：dict-->DataFrame
    df_atran = pd.DataFrame.from_records(data=asset_tran,
                                         columns=['asset_tran_period', 'asset_tran_type', 'asset_tran_amount',
                                                  'asset_tran_due_at', 'asset_tran_category'])
    mapper = {
        'asset_tran_period': 'period',
        'asset_tran_type': 'type',
        'asset_tran_amount': 'amount',
        'asset_tran_due_at': 'due_at',
        'asset_tran_category': 'category'
    }
    df_atran.rename(columns=mapper, inplace=True)
    df_atran['due_at'] = df_atran.due_at.apply(lambda x: x[:10])
    df_atran['type'] = df_atran.type.replace(['repayinterest', 'repayprincipal'], ['interest', 'principal'])
    df_atran = df_atran.sort_values(by=['category', 'type', 'period']).set_index(['category', 'type'])

    # capital_tran数据准备：dict-->DataFrame
    df_ctran = pd.DataFrame.from_records(data=capital_tran,
                                         columns=['capital_transaction_period', 'capital_transaction_type',
                                                  'capital_transaction_origin_amount', 'capital_transaction_expect_finished_at'])
    mapper = {
        'capital_transaction_period': 'period',
        'capital_transaction_type': 'type',
        'capital_transaction_origin_amount': 'amount',
        'capital_transaction_expect_finished_at': 'due_at'
    }
    df_ctran.rename(columns=mapper, inplace=True)
    df_ctran['due_at'] = df_ctran.due_at.apply(lambda x: x[:10])
    df_ctran['category'] = df_ctran.type.apply(lambda x: 'grant' if x == 'grant' else 'principal' if x == 'principal' else 'interest' if x == 'interest' else 'fee')
    df_ctran = df_ctran.sort_values(by=['category', 'type', 'period']).set_index(['category', 'type'])

    # cmdb数据准备：dict-->DataFrame
    df_cmdb_grant = pd.DataFrame(cmdb_tran['data']['calculate_result']['grant'], index=[0])
    df_cmdb_principal = pd.DataFrame(cmdb_tran['data']['calculate_result']['principal'])
    df_cmdb_interest = pd.DataFrame(cmdb_tran['data']['calculate_result']['interest'])
    df_cmdb_grant['type'] = 'grant'
    df_cmdb_principal['type'] = 'principal'
    df_cmdb_interest['type'] = 'interest'
    df_cmdb_fee = pd.DataFrame()
    fee = cmdb_tran['data']['calculate_result']['fee']
    for key in fee.keys():
        df_tmp = pd.DataFrame(fee[key])
        df_tmp['type'] = key
        df_cmdb_fee = df_cmdb_fee.append(df_tmp)
    df_cmdb = pd.concat([df_cmdb_grant, df_cmdb_principal, df_cmdb_interest, df_cmdb_fee], axis=0, sort=False)
    df_cmdb['category'] = df_cmdb.type.apply(lambda x: 'grant' if x == 'grant' else 'principal' if x == 'principal' else 'interest' if x == 'interest' else 'fee')
    df_cmdb = df_cmdb[['period', 'type', 'amount', 'date', 'category']]
    df_cmdb = df_cmdb.sort_values(by=['category', 'type', 'period']).set_index(['category', 'type'])

    # 检查期次：asset & asset_tran & oa
    atran_period = df_atran[['period']].max().values[0]
    cmdb_period = df_cmdb[['period']].max().values[0]
    Assert.assert_equal(asset_info[0]['asset_period_count'], atran_period, '期次不相等：asset_period_count %s，asset_tran %s' % (asset_info[0]['asset_period_count'], atran_period))
    Assert.assert_equal(atran_period, cmdb_period, '期次不相等：asset_tran %s，oa %s' % (atran_period, cmdb_period))

    # 检查本、息、费总和：asset_tran & oa
    dt_atran = df_atran['amount'].sum(level='category').to_dict()
    dt_cmdb = df_cmdb['amount'].sum(level='category').to_dict()
    Assert.assert_equal(dt_atran, dt_cmdb, '本、息、费总和不相等：\n -----asset_tran----\n%s\n -----oa----\n%s' % (dt_atran, dt_cmdb))
    # 检查本、息、费总和：asset_tran & asset
    Assert.assert_equal(asset_info[0]['asset_granted_principal_amount'], dt_atran['grant'], '本金总和不相等：asset_granted_principal_amount %s，asset_tran %s' % (asset_info[0]['asset_granted_principal_amount'], dt_atran['principal']))
    Assert.assert_equal(asset_info[0]['asset_principal_amount'], dt_atran['principal'], '本金总和不相等：asset_principal_amount %s，asset_tran %s' % (asset_info[0]['asset_principal_amount'], dt_atran['principal']))
    Assert.assert_equal(asset_info[0]['asset_interest_amount'], dt_atran['interest'], '利息总和不相等：asset_interest_amount %s，asset_tran %s' % (asset_info[0]['asset_interest_amount'], dt_atran['interest']))
    Assert.assert_equal(asset_info[0]['asset_fee_amount'], dt_atran.get('fee', 0), '费用总和不相等：asset_fee_amount %s，asset_tran %s' % (asset_info[0]['asset_fee_amount'], dt_atran.get('fee', 0)))
    Assert.assert_equal(asset_info[0]['asset_total_amount'], dt_atran['principal']+dt_atran['interest']+dt_atran.get('fee', 0), '本息费总和不相等：asset_total_amount %s，asset_tran %s' % (asset_info[0]['asset_total_amount'], dt_atran['principal']+dt_atran['interest']+dt_atran.get('fee', 0)))

    # 检查单期的本、息、费、日期：asset_tran & oa
    res = df_atran.values == df_cmdb.values
    Assert.assert_equal(res.all(), True, '单期的本、息、费、日期不相等：\n -----asset_tran-----\n%s \n -----oa----\n%s' % (df_atran[res == False], df_cmdb[res == False]))

    # 检查单期的本、息、费、日期：asset_tran & capital_transaction
    df_atran_2 = df_atran.loc[['principal', 'interest', 'fee', 'due_at'], :]
    df_ctran_2 = df_ctran.loc[['principal', 'interest', 'fee', 'due_at'], :]
    res_2 = df_atran_2.values == df_ctran_2.values
    Assert.assert_equal(res_2.all(), True, '单期的本、息、费、日期不相等：\n -----asset_tran-----\n%s \n -----capital_transaction----\n%s' % (df_atran_2[res_2 == False], df_ctran_2[res_2 == False]))

    # 检查capital_asset
    Assert.assert_equal(asset_info[0]['asset_period_count'], capital_asset[0]['capital_asset_period_count'], '期次不相等：asset_period_count %s，capital_asset_period_count %s' % (asset_info[0]['asset_period_count'], capital_asset[0]['capital_asset_period_count']))
    Assert.assert_equal(asset_info[0]['asset_granted_principal_amount'], capital_asset[0]['capital_asset_granted_amount'], '放款金额不相等：asset_granted_principal_amount %s，capital_asset_granted_amount %s' % (asset_info[0]['asset_granted_principal_amount'], capital_asset[0]['capital_asset_granted_amount']))
    Assert.assert_equal(asset_info[0]['asset_actual_grant_at'][:10], capital_asset[0]['capital_asset_granted_at'][:10], '放款时间不相等：asset_actual_grant_at %s，capital_asset_granted_at %s' % (asset_info[0]['asset_actual_grant_at'][:10], capital_asset[0]['capital_asset_granted_at'][:10]))
    Assert.assert_equal(asset_info[0]['asset_due_at'], capital_asset[0]['capital_asset_due_at'], '到期时间不相等：asset_due_at %s，capital_asset_due_at %s' % (asset_info[0]['asset_due_at'], capital_asset[0]['capital_asset_due_at']))
    Assert.assert_equal('repay', capital_asset[0]['capital_asset_status'], 'capital_asset_status状态不对！')

    # 检查总费用
    check_comprehensive_fee(item_no)


def check_comprehensive_fee(item_no):
    """
    检查年化综合息费：asset_total_fee与根据cmdb_rate_number计算出的年化综合息费比较
    :param item_no:
    :return:
    """
    asset_info = get_asset_info_by_item_no(item_no)
    rate_number = asset_info[0]['asset_cmdb_product_number']
    principal = asset_info[0]['asset_principal_amount']
    period = asset_info[0]['asset_period_count']
    asset_total_fee = asset_info[0]['asset_total_amount']
    # 获取费率信息
    rate_info = get_rate_info(rate_number)
    year_days = rate_info[0]['rate_interest_year_days']
    month_clear_day = rate_info[0]['rate_month_clear_day']
    clear_day = rate_info[0]['rate_clear_day']

    rate_config_info = get_root_rate_config_info(rate_number)
    calculate_type = rate_config_info[0]['rate_config_calculate_type']
    rate_value = decimal.Decimal(rate_config_info[0]['rate_config_value']) / 100
    round_type = rate_config_info[0]['rate_config_carry_mode']
    # 计算年化综合息费
    comprehensive_fee = get_comprehensive_fee(principal, period, rate_value, calculate_type, round_type, year_days, month_clear_day, clear_day)
    if comprehensive_fee != -1:
        Assert.assert_equal(comprehensive_fee, asset_total_fee, "年化综合息费不等")


def check_asset_confirm(item_no, confirm_type, confirm_status):
    asset_confirm = get_asset_confirm(item_no, confirm_type)
    Assert.assert_equal(confirm_status, asset_confirm[0]['asset_confirm_status'], "asset_confirm_status不正确")


def check_wait_change_capital_data(item_no, code=None, message=None, eventtype=None):
    asset_loan_record = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(5, asset_loan_record[0]['asset_loan_record_status'], 'alr状态不对！')
    task = get_task_by_item_no_and_task_type(item_no, 'ChangeCapital')
    task_request_data = json.loads(task['task_request_data'])
    Assert.assert_equal('terminated', task['task_status'], '切资方任务状态不对！')
    if code:
        Assert.assert_equal(code, task_request_data['data']['code'], '切资方任务data.code不对！')
    if eventtype:
        Assert.assert_match(task_request_data['eventType'], eventtype, '资产切换资金方任务eventType不对！')
    if message:
        Assert.assert_match(asset_loan_record[0]['asset_loan_record_memo'], message, 'alr_memo不对！')
        Assert.assert_match(task_request_data['data']['message'], message, '切资方任务data.message不对！')
        Assert.assert_match(task_request_data['data']['message'], message, '资产黑名单任务data.message不对！')

    # 执行切资方，期望能切走
    run_terminated_task(item_no, "ChangeCapital")


def check_wait_assetvoid_data(item_no, code=None, message=None):
    asset_loan_record = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(5, asset_loan_record[0]['asset_loan_record_status'], 'alr状态不对！')
    task = get_task_by_item_no_and_task_type(item_no, 'AssetVoid')
    task_request_data = json.loads(task['task_request_data'])
    Assert.assert_equal('terminated', task['task_status'], '资产取消任务状态不对！')
    if code:
        Assert.assert_equal(code, task_request_data['data']['code'], '资产取消任务data.code不对！')
    if message:
        Assert.assert_match(task_request_data['data']['message'], message, '资产取消任务data.message不对！')
    # 执行资产作废，并检查数据
    run_terminated_task(item_no, "AssetVoid")
    check_asset_void_data(item_no)


def check_wait_blacklistcollect_data(item_no, asset_info, code=None, message=None, capital_blacklist_type="bank_card"):
    asset_loan_record = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(5, asset_loan_record[0]['asset_loan_record_status'], 'alr状态不正确！')
    task = get_task_by_item_no_and_task_type(item_no, 'BlacklistCollect')
    task_request_data = json.loads(task['task_request_data'])
    Assert.assert_equal('terminated', task['task_status'], '资产黑名单任务状态不正确！')
    if code:
        Assert.assert_equal(code, task_request_data['data']['code'], '资产黑名单任务data.code不对！')
    if message:
        Assert.assert_match(task_request_data['data']['message'], message, '资产黑名单任务data.message不对！')
    # 执行资产加入黑名单，并检查数据
    run_terminated_task(item_no, "BlacklistCollect")
    check_capital_blacklist_data(asset_info, capital_blacklist_type, message)

def check_rollback_changecapital_data(item_no, code=None, message=None, eventtype=None):
    """
    检查取消任务回滚生成的切换资金方任务
    """
    asset_loan_record = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(5, asset_loan_record[0]['asset_loan_record_status'], 'alr状态不正确！')
    task = get_task_by_item_no_and_task_type(item_no, 'ChangeCapital', 'terminated')
    task_request_data = json.loads(task['task_request_data'])
    Assert.assert_equal('terminated', task['task_status'], '资产切换资金方任务状态不正确！')
    if code:
        Assert.assert_equal(code, task_request_data['data']['code'], '资产切换资金方任务data.code不对！')
    if message:
        Assert.assert_match(task_request_data['data']['message'], message, '资产切换资金方任务data.message不对！')
    if eventtype:
        Assert.assert_match(task_request_data['eventType'], eventtype, '资产切换资金方任务eventType不对！')
    # 执行切资方，期望能切走
    run_terminated_task(item_no, "ChangeCapital")

def check_rollback_applycanloan(item_no,channel):
    '''
    ChangeCapital回滚到ApplyCanLoan 任务检查
    '''
    asset_loan_record = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(0, asset_loan_record[0]['asset_loan_record_status'], 'alr状态不正确！')
    task = get_task_by_item_no_and_task_type(item_no, 'ApplyCanLoan', 'open')
    task_request_data = json.loads(task['task_request_data'])
    Assert.assert_equal(channel, task_request_data['loan_channel'], '资金方错误')


def check_capital_transaction(item_no):
    """
    检查资方还款计划，与asset_tran比较：
    1、本息费总额一致
    2、本金总额一致
    3、每一期的本息费总额一致
    :param item_no:
    :return:
    """
    asset_tran = get_asset_tran_by_item_no(item_no)
    capital_tran = get_capital_asset_tran_by_item_no(item_no)

    if not asset_tran:
        raise AssertionError('asset_tran无数据！')
    if not capital_tran:
        raise AssertionError('capital_transaction无数据！')

    # 1、本息费总额一致
    asset_tran_total_amount = get_asset_tran_total_amount(item_no)
    capital_tran_total_amount = get_capital_tran_total_amount(item_no)
    Assert.assert_equal(asset_tran_total_amount, capital_tran_total_amount, "本息费总额不一致")

    # 2、本金总额一致
    asset_tran_principal = get_asset_tran_total_amount(item_no, 'principal')
    capital_tran_principal = get_capital_tran_total_amount(item_no, 'principal')
    Assert.assert_equal(asset_tran_principal, capital_tran_principal, "本金总额不一致")

    # 3、每一期的本息费总额一致
    asset_tran_period_amount = get_asset_tran_period_amount_lt(item_no)
    capital_tran_period_amount = get_capital_tran_period_amount_lt(item_no)
    Assert.assert_equal(asset_tran_period_amount, capital_tran_period_amount, "每期本息费总额不一致")


def check_route_log(idnum_encrypt, loan_channel, message):
    time.sleep(1)
    asset_route_log = get_asset_route_log_by_idum(idnum_encrypt, loan_channel)
    Assert.assert_equal(loan_channel, asset_route_log[0]['asset_route_log_loan_channel'], '目标channel不正确')
    Assert.assert_equal(message, asset_route_log[0]['asset_route_log_message'], '路由日志记录不匹配')


def check_router_load_record_product_code(idnum_encrypt, router_load_record_rule_code, product_code):
    time.sleep(1)
    router_load_record = get_router_load_record_by_idum(idnum_encrypt, router_load_record_rule_code)
    Assert.assert_equal(idnum_encrypt, router_load_record[0]['router_load_record_idnum'],
                        '路由记录的身份证号不正确')
    Assert.assert_equal(router_load_record_rule_code, router_load_record[0]['router_load_record_rule_code'], '路由记录的规则名不正确')
    Assert.assert_equal(product_code, router_load_record[0]['router_load_record_product_code'], '路由记录的产品编号不正确')

def check_confirm_data(item_no, loan_channel, status, asset_confirm_type):
    confirm_data = get_confirm_data_by_item_no(item_no, asset_confirm_type)
    Assert.assert_equal(item_no, confirm_data[0]['asset_confirm_item_no'], '资产编号不一致')
    Assert.assert_equal(loan_channel, confirm_data[0]['asset_confirm_channel'], '资金方不正确')
    Assert.assert_equal(status, confirm_data[0]['asset_confirm_status'], '状态不正确')
    Assert.assert_equal(asset_confirm_type, confirm_data[0]['asset_confirm_type'], '操作类型不正确')


def check_data(data, **kwargs):
    for key, value in kwargs.items():
        Assert.assert_equal(value, data[key], "%s数据有误" % key)


def check_asset(item_no, **kwargs):
    rs = get_asset_info_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_asset_loan_record(item_no, **kwargs):
    rs = get_asset_loan_record_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_router_load_record_data(route_key, rule_code=None, **kwargs):
    rs = get_router_load_record_by_key(route_key, rule_code)
    check_data(rs[0], **kwargs)


def check_asset_event_exist(item_no, channel, event_type):
    rs = get_asset_event(item_no, channel, event_type)
    Assert.assert_equal(len(rs), 1, "数据有误")


def check_sendmsg_exist(item_no, msg_type):
    rs = get_sendmsg(item_no, msg_type)
    Assert.assert_equal(len(rs), 1, "数据有误")


def check_withdraw_data(item_no, order_status, record_status, order_resp_code="", order_resp_message="", record_resp_code="", record_resp_message=""):
    withdraw_order = get_withdraw_order_by_item_no(item_no)
    withdraw_record = get_withdraw_record_by_item_no(item_no)
    Assert.assert_equal(order_status, withdraw_order[0]["withdraw_order_status"], "数据有误")
    Assert.assert_equal(record_status, withdraw_record[-1]["withdraw_record_status"], "数据有误")
    if order_resp_code:
        Assert.assert_equal(order_resp_code, withdraw_order[-1]["withdraw_order_resp_code"], "数据有误")
    if order_resp_message:
        Assert.assert_equal(order_resp_message, withdraw_order[-1]["withdraw_order_resp_message"], "数据有误")
    if record_resp_code:
        Assert.assert_equal(record_resp_code, withdraw_record[-1]["withdraw_record_resp_code"], "数据有误")
    if record_resp_message:
        Assert.assert_equal(record_resp_message, withdraw_record[-1]["withdraw_record_resp_message"], "数据有误")
    for item in withdraw_record[:-2]:
        Assert.assert_equal("fail", item["withdraw_record_status"], "数据有误")


def check_router_load_record(rule_data_lt, route_key, four_element, amount, expect_route_status, item_no="",
                             hit_channel_idx=0, hit_rule_idx_lt=[0]):
    """
    检查路由记录表
    :param rule_data_lt:
    :param route_key:
    :param four_element:
    :param amount:
    :param hit_channel_idx: 期望命中资方的下标
    :param hit_rule_idx_lt: 期望命中规则的下标列表
    :param item_no:
    :return:
    """
    channel = rule_data_lt[hit_channel_idx]["channel"]
    router_records = get_router_load_record_by_key(route_key)
    # 路由记录条数是否与期望命中规则数一致
    Assert.assert_equal(len(hit_rule_idx_lt), len(router_records), "路由结果异常")
    actual_rule_code_st = set()
    # 逐条检查字段值是否正确记录
    for record in router_records:
        check_data(record,
                   router_load_record_channel=channel,
                   router_load_record_status=expect_route_status,
                   router_load_record_principal_amount=amount * 100,
                   router_load_record_route_day=time.strftime("%Y-%m-%d"),
                   router_load_record_idnum=four_element['data']['id_number_encrypt'],
                   router_load_record_item_no=item_no)
        actual_rule_code_st.add(record["router_load_record_rule_code"])
    # 检查命中的规则是否正确
    expect_rule_code_st = set()
    for rule_idx in hit_rule_idx_lt:
        rule_code = get_rule_code(rule_data_lt, hit_channel_idx, rule_idx)
        expect_rule_code_st.add(rule_code)
    Assert.assert_equal(expect_rule_code_st, actual_rule_code_st, "路由结果异常")


def check_capital_account_data(item_no, four_element, channel, way, account_status, step_status, account_step=None, user_key=None):
    """
    检查开户表数据
    """
    account = get_capital_account_by_item_no_channel(four_element, channel)
    check_data(account[0], capital_account_status=account_status)
    step = get_capital_account_step_by_item_no_way(four_element, channel, item_no, way)
    check_data(step[0], capital_account_step_status=step_status)
    check_data(step[0], capital_account_step_way=way)
    if user_key:
        check_data(step[0], capital_account_step_user_key=user_key)
    if account_step:
        check_data(step[0], capital_account_step_step=account_step)


def check_request_log(item_no, channel, task_type):
    """
    检查调用资方接口的请求参数
    """
    # 1.获取asset_info进件数据
    asset_info = get_asset_import_data_by_item_no(item_no)
    scope = {'asset_info': asset_info}
    es = ES("gbiz%s" % gc.ENV)
    for item in request_log_check_point[channel][task_type]:
        check_points_lt = item['check_points']
        if check_points_lt:
            # 2.从es拿到请求日志
            api = "/mock/5f9bfaf562081c0020d7f5a7/gbiz" + item['api']
            req_log = es.get_request_log(task_type, [api], orderNo=item_no).get(api)
            Assert.assert_equal(len(check_points_lt), len(req_log), "接口%s调用次数不正确" % api)
            # 3.断言
            for idx in range(len(check_points_lt)):
                req_data = json.loads(req_log[idx]["feign.request"])
                check_points = check_points_lt[idx]
                for k, v in check_points.items():
                    # 实际值，jsonpath解析
                    actual = jsonpath.jsonpath(req_data, k)[0]
                    # 期望值，表达式解析
                    expect = eval(v, scope) if re.search('asset_info', str(v)) else v
                    Assert.assert_equal(expect, actual,
                                        "log检查错误，资产：%s, task：%s, 接口：%s, 检查值：%s, 期望：%s, 实际：%s" %
                                        (item_no, task_type, api, k, expect, actual))


def check_request_log_by_channel(item_no, channel):
    for task_type in request_log_check_point[channel].keys():
        check_request_log(item_no, channel, task_type)


def check_circuit_break_data(circuit_break_name, status):
    """
    检查熔断数据
    """
    record = get_latest_circuit_break_record(circuit_break_name)
    #需要检查event表，暂时没写
    action_1 = get_circuit_break_action(record[0]["circuit_break_record_id"], "AlertAction")
    action_2 = get_circuit_break_action(record[0]["circuit_break_record_id"], "SuspendTaskAction")
    if status == "open":
        check_data(record[0], circuit_break_record_status="open")
        check_data(action_1[0], circuit_break_action_status="closed")
        check_data(action_2[0], circuit_break_action_status="open")
    elif status == "close":
        check_data(record[0], circuit_break_record_status="close")
        check_data(action_1[0], circuit_break_action_status="closed")
        check_data(action_2[0], circuit_break_action_status="closed")

def check_asset_tran_valid_status(item_no, grant_status=0, other_status=1):
    """
    检查asset_tran表是否生效状态
    """
    asset_tran = get_asset_tran_by_item_no(item_no)
    for index, data in enumerate(asset_tran):
        if index == 0:
            Assert.assert_equal(grant_status, data['asset_tran_valid_status'],
                                "grant类型费用的asset_tran_valid_status不为0")
        else:
            Assert.assert_equal(other_status, data['asset_tran_valid_status'],
                                "其他类型费用的asset_tran_valid_status不为1")


if __name__ == '__main__':
    gc.init_env("3", "china", "dev")
    # check_request_log("20201621223432182077", "weishenma_daxinganling", "CapitalRepayPlanPush")
    # check_request_log_by_channel("20201621217820224243", "tongrongqianjingjing")
    check_comprehensive_fee("20211634874054789012")
