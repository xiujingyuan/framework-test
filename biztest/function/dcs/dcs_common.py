import datetime, time, pytest, json, requests
from biztest.config.dcs.url_config import biz_base_url, biz_account_url
from biztest.function.biz.biz_db_function import set_withhold_history, get_central_task_id_by_request_order_no
from biztest.function.dcs.biz_database import get_asset, get_holiday_status, delete_atransaction, delete_null_all, \
    delete_null, get_four_params_rbiz, get_capital_biz
from biztest.function.dcs.database_biz import get_sendmsg
from biztest.function.dcs.dcs_db_function import get_dcs_clean_withdraw_order, get_dcs_clean_generic_deal_order, \
    get_dcs_clean_generic_deal_trade, get_dcs_clean_deposit_withdraw_order, get_dcs_task_capitalAuditCallback
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_order_no
from biztest.interface.rbiz.biz_central_interface import run_type_task_biz_central, run_task_in_biz_central, \
    run_request_order_no_task_biz_central
from biztest.interface.rbiz.biz_central_interface_class import BizInterfaceBase
from biztest.util.tools.tools import get_guid, parse_resp_body
from biztest.interface.rbiz.rbiz_interface import capital_asset_success_to_rbiz
import common.global_const as gc

env_test = gc.ENV


# 检查小单是否进入biz（现在资产是gbiz-rbiz-biz，故只检查biz即可）
def check_asset_grant(item_no):
    # run_type_task_biz_central("AssetImport", item_no)
    # run_type_task_biz_central("AssetWithdrawSuccess", item_no)
    for ii in range(1, 50):  # 检查biz，保证后续的清分
        asset = get_asset(item_no)
        if asset:
            print(f"{item_no} is ready")
            break
        else:
            time.sleep(5)
    for iii in range(1, 50):  # 检查资方还款计划，保证后续的清分
        asset_capital = get_capital_biz(item_no, 1)
        if asset_capital:
            break
        else:
            # time.sleep(5)
            capital_asset_success_to_rbiz(item_no)


# 判断当期是否为工作日，工作日则返回 0，节假日则返回 1
def get_is_holiday(holiday_date):
    db_evn = "biz%s" % env_test
    # db_result 为 int 类型
    db_result = get_holiday_status(db_evn, holiday_date)
    fu_result = datetime.datetime.strptime(holiday_date, "%Y-%m-%d").weekday()
    if db_result == 0:
        return 0
    elif db_result == 1:
        return 1
    else:
        if fu_result in range(0, 5):
            return 0
        else:
            return 1


# 临时的
def delete_null_biz(item_no, serial_no=""):
    if serial_no == "":
        ids = delete_null(item_no)
    else:
        ids = delete_atransaction(serial_no)
    id = []
    if ids:
        for i in range(0, len(ids)):
            id.append(ids[i]["atransaction_id"])
        id_tuple = tuple(id)
        delete_null_all(id_tuple)


# 从数据库获取四要素
def get_four_params_rbiz_db(item_no):
    four_params_rbiz = get_four_params_rbiz(item_no)
    print(type(four_params_rbiz), four_params_rbiz)
    four_params_db = {
        "code": 0,
        "message": "ok",
        "data": {
            "user_name_encrypt": four_params_rbiz.pop("card_acc_name_encrypt"),
            "phone_number_encrypt": four_params_rbiz.pop("card_acc_tel_encrypt"),
            "id_number_encrypt": four_params_rbiz.pop("card_acc_id_num_encrypt"),
            "bank_code_encrypt": four_params_rbiz.pop("card_acc_num_encrypt")
        }
    }
    return four_params_db


# 检查还款信息，若没有数据，那再重发一次账消息
def check_repay_biz(item_no):
    # delete_asset_tran_by_item_no(item_no)
    # delete_dtransaction_by_item_no(item_no)
    # delete_ftransaction_by_item_no(item_no)
    # delete_fee_by_item_no(item_no)
    # delete_withhold_result_transaction_by_item_no(item_no)
    # insert_withhold_result(item_no)
    # 执行central_task，代扣经常会同步失败
    # run_request_order_no_task_biz_central(item_no)
    set_withhold_history(item_no)
    # 不管成功与否，都再重新发一次消息，避免漏消息的情况
    # msg_type = ["account_change_account_update", "account_change_tran_repay"]
    # for ii in range(0, len(msg_type)):
    #     account_content = get_sendmsg(id_number_encrypt, msg_type[ii])
    #     for account_i in range(0, len(account_content)):
    #         account_content_dict = json.loads(account_content[account_i]["sendmsg_content"])
    #         account_params = account_content_dict["body"]
    #         # 换个key更保险
    #         account_params["key"] = get_guid()
    #         # 直接调用biz的接口
    #         account_update_rurl = biz_base_url + biz_account_url
    #         resp = parse_resp_body(requests.request(
    #             method='post', url=account_update_rurl, headers={"Content-Type": "application/json"},
    #             json=account_params))
    #         f"执行第{account_i}个{msg_type[ii]}，返回结果{resp['content']}"
    sql = "select * from clean_task where task_order_no='%s' and task_type='accountChangeNotifySync'" % item_no
    wait_dcs_record_appear(sql)


def wait_dcs_record_appear(record_sql, wait_time=120):
    result = False
    for i in range(wait_time):
        asset_tran = gc.DCS_DB.query(record_sql)
        if asset_tran is not ():
            result = True
            break
        else:
            time.sleep(2)
    return result


def run_dcs_task_until_disappear(item_no, wait_time=120):
    result = False
    open_task = "select * from clean_task where task_order_no='%s' and task_status='open'" % item_no
    for i in range(wait_time):
        tasks = gc.DCS_DB.query(open_task)
        if tasks is not ():
            run_dcs_task_by_order_no(item_no, 2)
            time.sleep(1)
            continue
        else:
            result = True
            break
    return result


def run_dcs_task_by_type_until_disappear(task_type, wait_time=120):
    result = False
    open_task = "select * from clean_task where task_type='%s' and task_status='open' and task_create_at>curdate()" % task_type
    for i in range(wait_time):
        tasks = gc.DCS_DB.query(open_task)
        for task in tasks:
            run_dcs_task_by_order_no(task["task_order_no"], 2)
            time.sleep(0.5)
            continue
        else:
            result = True
            break
    return result


def check_CleanWithdrawOrder(business_no, status='success', tally_status='success', withdraw_status='success',
                             payment_channel='', channel_code='', deposit='', operate_type='manual', loan_channel='',
                             withhold_channel='', ref_order_no='', retry_order_no='', memo='', amount=1111):
    clean_withdraw_order_info = get_dcs_clean_withdraw_order(business_no)
    # 资金归集 检查clean_withdraw_order
    assert clean_withdraw_order_info[0]["order_no"] == business_no, '和传入一致'
    # assert withdraw_order_info[0]["tally_no"] == tally_no, '和传入一致'
    assert clean_withdraw_order_info[0]["status"] == status, '和传入一致'
    assert clean_withdraw_order_info[0]["amount"] == amount, '和传入一致'
    assert clean_withdraw_order_info[0]["loan_channel"] == loan_channel, '和传入一致'
    assert clean_withdraw_order_info[0]["withhold_channel"] == withhold_channel, '和传入一致'
    assert clean_withdraw_order_info[0]["payment_channel"] == payment_channel, '和传入一致'
    assert clean_withdraw_order_info[0]["channel_code"] == channel_code, '和传入一致'
    assert clean_withdraw_order_info[0]["deposit"] == deposit, '和传入一致'
    assert clean_withdraw_order_info[0]["tally_status"] == tally_status, '和传入一致'
    assert clean_withdraw_order_info[0]["withdraw_status"] == withdraw_status, '和传入一致'
    # assert clean_withdraw_order_info[0]["message"] == message, '和传入一致'
    assert clean_withdraw_order_info[0]["operate_type"] == operate_type, '和传入一致'
    assert clean_withdraw_order_info[0]["ref_order_no"] == ref_order_no, '上一个order_no'
    assert clean_withdraw_order_info[0]["retry_order_no"] == retry_order_no, '重试order_no'
    # assert clean_withdraw_order_info[0]["finish_at"] == finish_at, '和传入一致'
    assert clean_withdraw_order_info[0]["memo"] == memo, '和传入一致'
    assert clean_withdraw_order_info[0]["biz_type"] == 'collecting', '和传入一致'
    if amount == 1011:  # 默认手动归集金额1111，代付成本若配置了就是100
        assert clean_withdraw_order_info[0]["settlement_cost_amount"] == 0, '手动归集代扣手续费为0'
        assert clean_withdraw_order_info[0]["withdraw_cost_amount"] == 100, '手动归集代付成功为100分'
    else:
        assert clean_withdraw_order_info[0]["settlement_cost_amount"] == 0, '手动归集代扣手续费为0'
        assert clean_withdraw_order_info[0]["withdraw_cost_amount"] == 0, '手动归集代付成功为0分'


def check_CleanDepositWithdrawOrder(business_no, status='success', payment_channel='', deposit='',
                                    operate_type='manual', loan_channel='', memo='', amount=1100000000):
    clean_deposit_withdraw_order = get_dcs_clean_deposit_withdraw_order(business_no)
    # 支付通道充值 检查表 clean_deposit_withdraw_order
    assert clean_deposit_withdraw_order[0]["order_no"] == business_no, '和传入一致'
    assert clean_deposit_withdraw_order[0]["status"] == status, '和传入一致'
    assert clean_deposit_withdraw_order[0]["amount"] == amount, '和传入一致'
    assert clean_deposit_withdraw_order[0]["channel_code"] == loan_channel, '和传入一致'
    assert clean_deposit_withdraw_order[0]["payment_channel"] == payment_channel, '和传入一致'
    assert clean_deposit_withdraw_order[0][
               "mem_acct_no"] == "enc_03_3199134250318694400_325", '和KV#dcs_payment_channel_recharge配置的一致'  # TODO 更新nacos配置
    assert clean_deposit_withdraw_order[0]["mem_name"] == "enc_04_3319648333995707392_308", '和KV#dcs_payment_channel_recharge配置的一致'
    assert clean_deposit_withdraw_order[0][
               "mem_cert_no"] == "enc_02_3322323509338179584_095", '和KV#dcs_payment_channel_recharge配置的一致'
    assert clean_deposit_withdraw_order[0][
               "mem_mobile"] == "enc_01_2433385310_808", '和KV#dcs_payment_channel_recharge配置的一致'
    assert clean_deposit_withdraw_order[0]["deposit"] == deposit, '和传入一致'
    assert clean_deposit_withdraw_order[0]["operate_type"] == operate_type, '和传入一致'
    # assert clean_deposit_withdraw_order[0]["message"] == message, 'message一致'
    # assert clean_deposit_withdraw_order[0]["finish_at"] == finish_at, '重试order_no'
    assert clean_deposit_withdraw_order[0]["memo"] == memo, '和传入一致'


def check_deal_orderAndtrade(business_no, status='success', from_business='COLLECT', order_type='paymentWithdraw',
                             serial_no=''):
    # 通用交易流程数据检查
    deal_order_info = get_dcs_clean_generic_deal_order(business_no)
    deal_trade_info = get_dcs_clean_generic_deal_trade(business_no)
    # 检查clean_generic_deal_order
    assert deal_order_info[0]["business_no"] == business_no, '和传入一致'
    # assert deal_order_info[0]["order_no"] == order_no, '和传入一致' #随机生成的暂无法检查
    assert deal_order_info[0]["order_type"] == order_type, '和传入一致'
    assert deal_order_info[0]["from_business"] == from_business, '和传入一致'
    assert deal_order_info[0]["status"] == status, '和传入一致'
    assert deal_order_info[0]["memo"] == '', '和传入一致'  # 目前order。memo都是空值
    # 检查clean_generic_deal_trade
    assert deal_trade_info[0]["order_no"] == deal_order_info[0]["order_no"], '和传入一致'
    assert deal_trade_info[0]["trade_no"] == deal_order_info[0]["order_no"] + "_1", '和传入一致'
    if serial_no != "":
        assert deal_trade_info[0]["serial_no"] == serial_no, '和传入一致'
    assert deal_trade_info[0]["status"] == status, '和传入一致'
    # assert deal_trade_info[0]["memo"] == memo, '和传入一致'
    assert deal_order_info[0]["finish_at"] == deal_trade_info[0]["finish_at"], 'finish_at一致，暂无检查具体的值'


def check_task_capitalAuditCallback(business_no):
    # 验证生成回调capitalAuditCallback成功
    capitalAuditCallback_info = get_dcs_task_capitalAuditCallback(business_no)
    assert capitalAuditCallback_info[0]["task_order_no"] == business_no, '生成回调capitalAuditCallback成功'
