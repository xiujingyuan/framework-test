import json

from biztest.function.cmdb_global.cmdb_global_common_function import get_fee_info_for_data_check
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_info_by_item_no, \
    get_withdraw_order_by_item_no, get_capital_asset_by_item_no, get_asset_loan_record_by_item_no, \
    get_withdraw_record_by_item_no, get_manual_asset_by_item_no, get_asset_event_by_item_no_event_type, \
    get_sendmsg_by_item_no, get_asset_borrower_by_item_no, get_global_confirm_data_by_item_no, \
    get_global_asset_loan_record_by_item_no, get_global_by_item_no_and_task_type, get_router_load_record_by_key
from biztest.function.global_gbiz.gbiz_global_common_function import run_terminated_task, get_rule_code
from biztest.util.asserts.assert_util import Assert
import time
import common.global_const as gc


def check_asset_data(asset_info, withdraw=True):
    asset = get_asset_info_by_item_no(asset_info['data']['asset']['item_no'])
    asset_info['data']['asset']['cmdb_product_number'] = asset[0]["asset_cmdb_product_number"]
    cmdb_data = get_fee_info_for_data_check(asset_info)
    asset_tran_data = gc.GRANT_DB.query("SELECT "
                                        "asset_tran_type AS fee_type, "
                                        "asset_tran_period AS period, "
                                        "asset_tran_amount AS amount, "
                                        "DATE_FORMAT(asset_tran_due_at, '%%Y-%%m-%%d') as due_at "
                                        "FROM asset_tran "
                                        "WHERE asset_tran_asset_item_no = '%s' "
                                        "ORDER BY fee_type, period" % (asset_info['data']['asset']['item_no'],))
    capital_asset_tran_data = gc.GRANT_DB.query("SELECT "
                                                "capital_transaction_type as fee_type, "
                                                "capital_transaction_period as period, "
                                                "capital_transaction_origin_amount as amount, "
                                                "DATE_FORMAT(capital_transaction_expect_finished_at, "
                                                "'%%Y-%%m-%%d') as due_at "
                                                "from capital_transaction "
                                                "where capital_transaction_item_no='%s' "
                                                "order by fee_type, period;" % (
                                                    asset_info['data']['asset']['item_no'],))
    asset_data = get_asset_info_by_item_no(asset_info['data']['asset']['item_no'])
    asset_loan_record_data = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
    capital_asset_data = get_capital_asset_by_item_no(asset_info['data']['asset']['item_no'])
    withdraw_order_data = get_withdraw_order_by_item_no(asset_info['data']['asset']['item_no'] + 'w')
    # 用户还款计划 费率类型 金额 时间 期次校验
    Assert.assert_match_json(asset_tran_data, cmdb_data, "费率正确")
    Assert.assert_match_json(cmdb_data, asset_tran_data, "费率正确")
    # 资方还款计划 费率类型 金额 时间 期次校验
    Assert.assert_match_json(capital_asset_tran_data, cmdb_data, "费率正确")
    # Assert.assert_match_json(cmdb_date, capital_asset_tran_data, "费率正确")

    # 放款时间检查
    Assert.assert_equal(asset_data[0]["asset_effect_at"] == asset_data[0]["asset_actual_grant_at"] ==
                        asset_loan_record_data[0]["asset_loan_record_finish_at"] ==
                        asset_loan_record_data[0]["asset_loan_record_grant_at"] ==
                        capital_asset_data[0]["capital_asset_granted_at"], True, "放款时间正确")
    Assert.assert_equal(asset_data[0]["asset_due_at"] == asset_data[0]["asset_payoff_at"] ==
                        capital_asset_data[0]["capital_asset_due_at"], True, "到期时间正确")
    # 放款金额检查
    Assert.assert_equal(asset_info['data']['asset']['amount'] ==
                        asset_data[0]["asset_principal_amount"] ==
                        asset_loan_record_data[0]["asset_loan_record_amount"] ==
                        capital_asset_data[0]["capital_asset_granted_amount"], True, "总放款金额正确")
    Assert.assert_equal(asset_info['data']['asset']['amount'] ==
                        (asset_data[0]["asset_granted_principal_amount"] +
                         asset_loan_record_data[0]["asset_loan_record_withholding_amount"]),
                        True, "总金额一致")
    if withdraw:
        Assert.assert_equal(asset_data[0]["asset_granted_principal_amount"] ==
                            withdraw_order_data[0]["withdraw_order_amount"], True, "实际放款金额正确")


def check_withdraw_data(item_no, order_status, record_status, record_resp_code="", record_resp_message=""):
    withdraw_order = get_withdraw_order_by_item_no(item_no + "w")
    withdraw_record = get_withdraw_record_by_item_no(item_no + "w")
    Assert.assert_equal(order_status, withdraw_order[0]["withdraw_order_status"], "数据有误")
    Assert.assert_equal(record_status, withdraw_record[-1]["withdraw_record_status"], "数据有误")
    if record_resp_code:
        Assert.assert_equal(record_resp_code, withdraw_record[-1]["withdraw_record_resp_code"], "数据有误")
    if record_resp_message:
        Assert.assert_equal(record_resp_message, withdraw_record[-1]["withdraw_record_resp_message"], "数据有误")
    for item in withdraw_record[:-2]:
        Assert.assert_equal("fail", item["withdraw_record_status"], "数据有误")


def check_asset_void_data(item_no):
    asset_info = get_asset_info_by_item_no(item_no)
    alr_info = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(asset_info[0]["asset_status"], "void", "资产状态不对")
    Assert.assert_equal(alr_info[0]["asset_loan_record_status"], 5, "alr状态不对")


def check_confirm_data(item_no, loan_channel, status, asset_confirm_type):
    confirm_data = get_global_confirm_data_by_item_no(item_no, asset_confirm_type)
    Assert.assert_equal(item_no, confirm_data[0]['asset_confirm_item_no'], '资产编号不一致')
    Assert.assert_equal(loan_channel, confirm_data[0]['asset_confirm_channel'], '资金方不正确')
    Assert.assert_equal(status, confirm_data[0]['asset_confirm_status'], '状态不正确')
    Assert.assert_equal(asset_confirm_type, confirm_data[0]['asset_confirm_type'], '操作类型不正确')


def check_wait_change_capital_data(item_no, code=None, message=None):
    asset_loan_record = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(5, asset_loan_record[0]['asset_loan_record_status'], 'alr状态不对！')
    task = get_global_by_item_no_and_task_type(item_no, 'ChangeCapital')
    task_request_data = json.loads(task['task_request_data'])
    Assert.assert_equal('terminated', task['task_status'], '切资方任务状态不对！')
    if code:
        Assert.assert_equal(code, task_request_data['data']['code'], '切资方任务data.code不对！')
    if message:
        Assert.assert_match(asset_loan_record[0]['asset_loan_record_memo'], message, 'alr_memo不对！')
        Assert.assert_match(task_request_data['data']['message'], message, '切资方任务data.message不对！')


def check_rollback_changecapital_data(item_no, code=None, message=None, eventtype=None):
    """
    检查取消任务回滚生成的切换资金方任务
    """
    asset_loan_record = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(5, asset_loan_record[0]['asset_loan_record_status'], 'alr状态不正确！')
    task = get_global_by_item_no_and_task_type(item_no, 'ChangeCapital', 2)
    task_request_data = json.loads(task['task_request_data'])
    Assert.assert_equal('terminated', task['task_status'], '资产切换资金方任务状态不正确！')
    if code:
        Assert.assert_equal(code, task_request_data['data']['code'], '资产切换资金方任务data.code不对！')
    if message:
        Assert.assert_match(task_request_data['data']['message'], message, '资产切换资金方任务data.message不对！')
    if eventtype:
        Assert.assert_match(task_request_data['eventType'], eventtype, '资产切换资金方任务eventType不对！')
    # 海外与国内不一样，所以先屏蔽切换资金方任务自动执行吧
    # run_terminated_task(item_no, "ChangeCapital", 1)


def check_global_wait_assetvoid_data(item_no, code=None, message=None):
    alr_data = get_global_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(alr_data[0]["asset_loan_record_status"], 5, "alr状态不对")
    task = get_global_by_item_no_and_task_type(item_no, "AssetVoid")
    task_request_data = json.loads(task["task_request_data"])
    Assert.assert_equal("terminated", task["task_status"], "资产取消任务状态不对！")
    if code:
        Assert.assert_equal(code, task_request_data["data"]["code"], "资产取消任务data.code不对！")
    if message:
        Assert.assert_match(alr_data[0]["asset_loan_record_memo"], message, "alr_memo不对！")
        Assert.assert_match(task_request_data["data"]["message"], message, '资产取消任务data.message不对！')
    # 执行资产作废，并检查数据
    run_terminated_task(item_no, "AssetVoid", 0)
    check_asset_void_data(item_no)
    check_asset_loan_record(item_no, asset_loan_record_status=5)


def check_wait_assetreverse_data(item_no, code=None, message=None):
    asset_loan_record = get_asset_loan_record_by_item_no(item_no)
    Assert.assert_equal(6, asset_loan_record[0]['asset_loan_record_status'], 'alr状态不对！')
    task = get_global_by_item_no_and_task_type(item_no, 'CapitalAssetReverse')
    task_request_data = json.loads(task['task_request_data'])
    Assert.assert_equal('terminated', task['task_status'], '冲正任务状态不对！')
    if code:
        Assert.assert_equal(code, task_request_data['data']['code'], '冲正任务data.code不对！')
    if message:
        Assert.assert_match(task_request_data['data']['message'], message, '冲正任务data.message不对！')
    # 执行资产作废，并检查数据
    run_terminated_task(item_no, "CapitalAssetReverse", 0)
    run_terminated_task(item_no, "AssetVoid", 0)
    check_asset_void_data(item_no)
    check_asset_loan_record(item_no, asset_loan_record_status=5)


def check_data(data, **kwargs):
    for key, value in kwargs.items():
        Assert.assert_equal(value, data[key], "%s数据有误" % key)


def check_asset_loan_record(item_no, **kwargs):
    rs = get_asset_loan_record_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_manual_asset(item_no, **kwargs):
    rs = get_manual_asset_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_asset_event_exist(item_no, event_type):
    rs = get_asset_event_by_item_no_event_type(item_no, event_type)
    Assert.assert_equal(len(rs), 1, "数据有误")


def check_sendmsg_exist(item_no, msg_type):
    rs = get_sendmsg_by_item_no(item_no, msg_type)
    Assert.assert_equal(len(rs), 1, "数据有误")


def check_asset_borrower(item_no, **kwargs):
    rs = get_asset_borrower_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_router_load_record(rule_data_lt, route_key, four_element, amount, expect_route_status, item_no="",
                             hit_channel_idx=0, hit_rule_idx_lt=None):
    """
    检查路由记录表
    :param expect_route_status:
    :param rule_data_lt:
    :param route_key:
    :param four_element:
    :param amount:
    :param hit_channel_idx: 期望命中资方的下标
    :param hit_rule_idx_lt: 期望命中规则的下标列表
    :param item_no:
    :return:
    """
    if hit_rule_idx_lt is None:
        hit_rule_idx_lt = [0]
    router_records = get_router_load_record_by_key(route_key)
    # 路由记录条数是否与期望命中规则数一致
    Assert.assert_equal(len(hit_rule_idx_lt), len(router_records), "路由结果异常")
    actual_rule_code_st = set()
    # 逐条检查字段值是否正确记录
    channel = rule_data_lt[hit_channel_idx]["channel"]
    for record in router_records:
        check_data(record,
                   router_load_record_channel=channel,
                   router_load_record_status=expect_route_status,
                   router_load_record_principal_amount=amount,
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
