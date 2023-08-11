# -*- coding: utf-8 -*-
from biztest.config.payment.url_config import india_razorpay_transfer_channel_name, india_bind_channel_name, \
    indonesia_bind_channel_name, thailand_bind_channel_name, india_cashfree_reconic_channel_name, \
    channel_notify_base_url, global_cashfree_sdk_appid, india_razorpay_reconic_channel_name, \
    global_razorpay_collect_channel_key1, global_razorpay_collect_channel_key2, SPECIAL_NAME, \
    india_paytm_transfer_channel_name, global_amount
from biztest.util.db.db_util import DataBase
import time
import random
import json
from biztest.util.tools.tools import *
import common.global_const as gc


# env = get_sysconfig("--env")
# country = get_sysconfig("--country")
# db = DataBase("global_payment%s_%s" % (env, country))

# sign_companys = {
#     "empty": "内部记录使用，切勿删除",
#     "yomoyo": "用于sino的放还款",
#     "yomoyo2": "用于pioneer的放还款",
#     "yomoyo3": "用于征信和展期代扣",
#     "yomoyo4": "用于展期代扣",
#     "yomoyo5": "用于Anupam放还款",
#     "yomoyo6": "用于F6放还款",
#     "cymo1": "泰国",
#     "amberstar1": "泰国",
#     "cymo2": "用于征信报告",
#     "cymo3": "picocapital",
#     "cymo4": "picocapital plus",
#     "cymo_test": "test",
#     "auto_test": "用于自动化测试"}


# 打开渠道cimb，若没有该渠道，则插入一条
def update_provider(provider, status):
    result = gc.PAYMENT_DB.get_data("provider", provider_code=provider)
    if not result:
        gc.PAYMENT_DB.insert_data("provider", provider_code=provider, provider_name=provider, provider_status=status,
                                  provider_remark="自动化插入")
    else:
        sql = "update provider set provider_status='%s' where provider_code='%s'" % (status, provider)
        gc.PAYMENT_DB.do_sql(sql)


# 打开主体amberstar1，若没有该主体，则插入一条
def update_sign_company(sign_company, status="open"):
    result = gc.PAYMENT_DB.get_data("sign_company", sign_company_code=sign_company)
    if not result:
        gc.PAYMENT_DB.insert_data("sign_company", sign_company_code=sign_company, sign_company_name=sign_company,
                                  sign_company_full_name=sign_company,
                                  sign_company_status=status, sign_company_remark="自动化插入")
    else:
        sql = "update sign_company set sign_company_status='%s' where sign_company_code='%s'" % (status, sign_company)
    gc.PAYMENT_DB.do_sql(sql)


# 打开渠道和主体的关联，若没有，则创建一个，最后的分数默认100分
def update_provider_sign_company(sign_company, provider, status="open"):
    sql = "select * from provider_sign_company " \
          "where provider_sign_company_sign_company_code='%s' and provider_sign_company_provider_code='%s'" % \
          (sign_company, provider)
    result = gc.PAYMENT_DB.do_sql(sql)
    if not result:
        sql = "INSERT INTO `provider_sign_company` (`provider_sign_company_sign_company_code`, " \
              "`provider_sign_company_provider_code`, `provider_sign_company_payment_type`, " \
              "`provider_sign_company_status`, `provider_sign_company_remark`, `provider_sign_company_score`) " \
              "VALUES ('%s', '%s', '1', '%s', '%s', 100);" % \
              (sign_company, provider, status, sign_company + '_' + provider)
    else:
        sql = "update provider_sign_company set provider_sign_company_status='%s', provider_sign_company_score=100 " \
              "where provider_sign_company_sign_company_code='%s' and provider_sign_company_provider_code='%s'" % \
              (status, sign_company, provider)
    gc.PAYMENT_DB.do_sql(sql)


# 打开产品qrcode，若没有，则新建一个
def update_provider_product(sign_company, provider, product, status="open"):
    sql = "select * from provider_product where provider_product_sign_company_code='%s' and " \
          "provider_product_provider_code='%s' and provider_product_type='%s'" % (sign_company, provider, product)
    result = gc.PAYMENT_DB.do_sql(sql)
    if not result:
        sql = "INSERT INTO `provider_product` (" \
              "`provider_product_sign_company_code`, `provider_product_provider_code`," \
              "`provider_product_type`, `provider_product_fee_type`, `provider_product_fee`, " \
              "`provider_product_fee_rate`, `provider_product_card_type`, `provider_product_fee_max`, " \
              "`provider_product_fee_min`, `provider_product_fee_status`, `provider_product_min_amount`, " \
              "`provider_product_max_amount`, `provider_product_settle_type`, `provider_product_use_holiday_plan`, " \
              "`provider_product_loaning_rate`, `provider_product_account_type`, `provider_product_start_at`, " \
              "`provider_product_end_at`, `provider_product_status`) VALUES ('%s', '%s', '%s', 1, 0, 0, 'DC', 0, 0, " \
              "'nofee', 0, 0, 'T1', 'close', 0, 1, now(), now(), '%s');" % \
              (sign_company, provider, product, status)
    else:
        sql = "update provider_product set provider_product_status='%s' " \
              "where provider_product_sign_company_code='%s' and provider_product_provider_code='%s' " \
              "and provider_product_type='%s'" % (status, sign_company, provider, product)
    gc.PAYMENT_DB.do_sql(sql)


# 打开通道cimb_amberstar1_qrcode，若没有，则新建一个
def update_channel_name(sign_company, provider, product, status, channel_type):
    if status == "open":
        channel_status = 1
    else:
        channel_status = 0
    sql = "select * from channel where channel_sign_company_code='%s' and channel_provider_code='%s' " \
          "and channel_provider_product_type='%s'" % (sign_company, provider, product)
    result = gc.PAYMENT_DB.do_sql(sql)
    if not result:
        sql = "INSERT INTO `channel` ( `channel_name`, `channel_alias`, `channel_type`, `channel_status`, " \
              "`channel_verify_priority`, `channel_need_charge_sms`, `channel_need_binding`, " \
              "`channel_need_binding_sms`, `channel_provider_id`, `channel_provider_price_config_type`, " \
              "`channel_support_operator`, `channel_sign_company_code`, " \
              "`channel_provider_code`, `channel_provider_product_type`, `channel_merchant_no`) VALUES " \
              "('%s', '自动化插入', '%s', '%s', 4, 0, 0, 0, 0, 0, 'USER', '%s', '%s', '%s', '12122121');" % \
              (provider + '_' + sign_company + '_' + product, channel_type, channel_status, sign_company, provider,
               product)
    else:
        sql = "update channel set channel_status='%s' where channel_sign_company_code='%s' and channel_provider_code='%s' " \
              "and channel_provider_product_type='%s'" % (channel_status, sign_company, provider, product)
    gc.PAYMENT_DB.do_sql(sql)


def update_sign_company_provider_product(sign_company, provider, product, status, channel_type=2):
    update_provider(provider, status)
    update_sign_company(sign_company, status)
    update_provider_sign_company(sign_company, provider, status)
    update_provider_product(sign_company, provider, product, status)
    update_channel_name(sign_company, provider, product, status, channel_type)
    # update_channel_otherclose(sign_company, provider, product, status)


def update_channel_otherclose(sign_company, provider, product, status):
    if status == 'close':
        sql = "update channel set channel_status=0 where channel_name<>'%s_%s_%s' and channel_name like '%%%s%%' " % (
            provider, sign_company, product, product)
    else:
        # sql = "update channel set channel_status=1 where channel_name<>'%s_%s_%s' and channel_name like '%%%s%%' " % (
        #     provider, sign_company, product, product)
        sql = "update channel set channel_status=1 where channel_name like '%%%s%%' " % (product)
    return gc.PAYMENT_DB.do_sql(sql)


def update_channel_error(provider, error_code, error_msg, error_status, error_type):
    sql_query = "select * from channel_error " \
                "where channel_error_provider_code='%s' and channel_error_code='%s'" % (provider, error_code)
    result_query = gc.PAYMENT_DB.do_sql(sql_query)
    if not result_query:
        sql = "INSERT INTO `channel_error` (`channel_error_provider_code`, `channel_error_code`, " \
              "`channel_error_msg`, `channel_error_status`, `channel_error_type`) " \
              "VALUES " \
              "('%s', '%s', '%s', %s, '%s');" % (provider, error_code, error_msg, error_status, error_type)
    elif not result_query[0]["channel_error_type"].__contains__(error_type):
        error_type = result_query[0]["channel_error_type"] + ",%s" % error_type
        sql = "update channel_error set channel_error_status='%s', channel_error_msg='%s', channel_error_type='%s' " \
              "where channel_error_provider_code='%s' and channel_error_code='%s' " % \
              (error_status, error_msg, error_type, provider, error_code)
    else:
        sql = "update channel_error set channel_error_status='%s', channel_error_msg='%s' " \
              "where channel_error_provider_code='%s' and channel_error_code='%s' " \
              "and channel_error_type like '%%%s%%'" % \
              (error_status, error_msg, provider, error_code, error_type)
    gc.PAYMENT_DB.do_sql(sql)


def update_channel(channel_name, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + key + "='" + str(value) + "', "
    sql = "update channel set %s where channel_name='%s'" % (sql_params[:-2], channel_name)
    sendmsg_list = gc.PAYMENT_DB.do_sql(sql)
    return sendmsg_list


def get_available_uuid(account_type, card_status):
    sql = "select * from account inner join card on account_card_num=card_num where account_auth_mode='%s' " \
          "and card_auth_mode='%s' and card_status=%s order by account_id desc limit 1" % \
          (account_type, account_type, card_status)
    return gc.PAYMENT_DB.do_sql(sql)


def get_carduuid_bycardnum(account_type, card_num):
    sql = "select * from account inner join card on account_card_num=card_num where account_auth_mode='%s' " \
          "and card_auth_mode='%s' and card_account='%s' order by account_id desc limit 1" % \
          (account_type, account_type, card_num)
    return gc.PAYMENT_DB.do_sql(sql)


def get_binding(card_num, channel_name):
    sql = "select * from binding where binding_card_num='%s' and binding_channel_name='%s'" % (card_num, channel_name)
    return gc.PAYMENT_DB.do_sql(sql)


def delete_binding(card_num, channel_name):
    sql = "delete from binding where binding_card_num='%s' and binding_channel_name='%s'" % (card_num, channel_name)
    return gc.PAYMENT_DB.do_sql(sql)


def get_card_info(**kwargs):
    sql = "select * from card where %s order by card_created_at desc" % generate_sql(kwargs, "and")
    card = gc.PAYMENT_DB.query(sql)
    return card


def get_task(**kwargs):
    sql = "select * from task where 'task_create_at'>'%s' and %s" % (get_date(day=-1), generate_sql(kwargs, "and"))
    task_list = gc.PAYMENT_DB.do_sql(sql)
    return task_list


def get_sendmsg(**kwargs):
    sql = "select * from sendmsg where sendmsg_create_at>'%s' and %s" % (get_date(day=-1), generate_sql(kwargs, "and"))
    sendmsg_list = gc.PAYMENT_DB.do_sql(sql)
    return sendmsg_list


def update_task_by_task_order_no(task_order_no, **kwargs):
    sql = "update task set %s where task_order_no='%s'" % (generate_sql(kwargs, ","), task_order_no)
    sendmsg_list = gc.PAYMENT_DB.do_sql(sql)
    return sendmsg_list


def update_withdraw_receipt_create_at():
    sql1 = "UPDATE  withdraw  SET withdraw_created_at=date_sub(CURRENT_DATE, INTERVAL 1 DAY),withdraw_finished_at=date_sub(CURRENT_DATE, INTERVAL 1 DAY)  WHERE  withdraw_created_at>CURRENT_DATE"
    sql2 = "UPDATE  withdraw_receipt  SET withdraw_receipt_created_at=date_sub(CURRENT_DATE, INTERVAL 1 DAY),withdraw_receipt_finished_at=date_sub(CURRENT_DATE, INTERVAL 1 DAY)  WHERE  withdraw_receipt_created_at>CURRENT_DATE"
    withdraw1 = gc.PAYMENT_DB.do_sql(sql1)
    withdraw2 = gc.PAYMENT_DB.do_sql(sql2)
    return withdraw1, withdraw2


def update_task_by_task_id(task_id, **kwargs):
    sql = "update task set %s where task_id='%s'" % (generate_sql(kwargs, ","), task_id)
    sendmsg_list = gc.PAYMENT_DB.do_sql(sql)
    return sendmsg_list


def delete_task(**kwargs):
    sql = "delete from task where 'task_create_at'>'%s' and %s" % (get_date(day=-1), generate_sql(kwargs, "and"))
    task_list = gc.PAYMENT_DB.do_sql(sql)
    return task_list


def delete_sendmsg(**kwargs):
    sql = "delete from sendmsg where 'sendmsg_create_at'>'%s' and %s" % (get_date(day=-1), generate_sql(kwargs, "and"))
    sendmsg_list = gc.PAYMENT_DB.do_sql(sql)
    return sendmsg_list


def get_channel_reconci(**kwargs):
    sql_params = "'channel_reconci_created_at'>'%s' and " % get_date(day=-1)
    for key, value in kwargs.items():
        sql_params = sql_params + key + "='" + str(value) + "' and "
    sql = "select * from channel_reconci where %s" % sql_params[:-5]
    reconci_list = gc.PAYMENT_DB.do_sql(sql)
    return reconci_list

def get_withdraw_receipt_info_by_merchant_key(merchant_key):
    sql ="SELECT * FROM withdraw_receipt  WHERE withdraw_receipt_merchant_key='%s'order by withdraw_receipt_id desc limit 1" % merchant_key
    withdraw_receipt_info = gc.PAYMENT_DB.do_sql(sql)
    return withdraw_receipt_info

def get_channel_settlement(**kwargs):
    sql_params = "'channel_settlement_created_at'>'%s' and " % get_date(day=-1)
    for key, value in kwargs.items():
        sql_params = sql_params + key + "='" + str(value) + "' and "
    sql = "select * from channel_settlement where %s" % sql_params[:-5]
    reconci_list = gc.PAYMENT_DB.do_sql(sql)
    return reconci_list


def delete_channel_reconci(**kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + key + "='" + str(value) + "' and "
    sql = "delete from channel_reconci where %s" % sql_params[:-5]
    gc.PAYMENT_DB.update(sql)


def delete_channel_settlement(**kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + key + "='" + str(value) + "' and "
    sql = "delete from channel_settlement where %s" % sql_params[:-5]
    gc.PAYMENT_DB.update(sql)


def insert_withhold(**kwargs):
    return gc.PAYMENT_DB.insert_data("withhold", **kwargs)


def get_withhold(**kwargs):
    return gc.PAYMENT_DB.get_data("withhold", **kwargs)


def delete_withhold(**kwargs):
    return gc.PAYMENT_DB.delete_data("withhold", **kwargs)


def update_withhold_by_merchant_key(merchant_key, **kwargs):
    sql = "update withhold set %s where withhold_merchant_key='%s'" % (generate_sql(kwargs, ","), merchant_key)
    gc.PAYMENT_DB.do_sql(sql)


def get_withhold_by_merchant_key(merchant_key):
    sql = "select * from withhold where withhold_merchant_key='%s'" % merchant_key
    withhold_info = gc.PAYMENT_DB.query(sql)
    return withhold_info


def get_withhold_receipt_by_merchant_key(merchant_key):
    sql = "select * from withhold_receipt where withhold_receipt_merchant_key='%s'" % merchant_key
    withhold_receipt_info = gc.PAYMENT_DB.query(sql)
    return withhold_receipt_info


def update_withhold_receipt_create_at(merchant_key, day=0, month=0, year=0):
    sql = "UPDATE withhold_receipt SET withhold_receipt_created_at='%s' WHERE withhold_receipt_merchant_key='%s' " % (
        get_date(year, month, day), merchant_key)
    gc.PAYMENT_DB.do_sql(sql)


def get_withdraw_by_merchant_key(merchant_key):
    sql = "select * from withdraw where withdraw_merchant_key='%s'" % merchant_key
    withdraw_info = gc.PAYMENT_DB.query(sql)
    return withdraw_info


def get_withdraw_receipt_by_merchant_key(merchant_key):
    sql = "select * from withdraw where withdraw_merchant_key='%s'" % merchant_key
    withdraw_receipt_info = gc.PAYMENT_DB.query(sql)
    return withdraw_receipt_info


def get_global_withdraw_info_by_trade_no(trade_no):
    sql = "SELECT * FROM withdraw LEFT JOIN withdraw_receipt ON withdraw_receipt_merchant_key=withdraw_merchant_key  WHERE withdraw_receipt_trade_no='%s'  order by withdraw_created_at desc limit 1" % trade_no
    withdraw_info = gc.PAYMENT_DB.query(sql)
    return withdraw_info


def get_global_sendmsg_info_by_merchant_key(sendmsg_order_no):
    sql = "SELECT * FROM sendmsg  WHERE sendmsg_order_no='%s'  order by sendmsg_create_at desc limit 1" % sendmsg_order_no
    withdraw_info = gc.PAYMENT_DB.query(sql)
    return withdraw_info


def get_global_withdraw_receipt_info_by_trade_no(trade_no):
    sql = "SELECT * FROM withdraw_receipt  WHERE withdraw_receipt_trade_no='%s'order by withdraw_receipt_created_at desc limit 1" % trade_no
    withdraw_receipt_info = gc.PAYMENT_DB.query(sql)
    return withdraw_receipt_info


def insert_global_withhold_razorpay_success_callback_task(merchant_key, channel_name, payment_type="netbanking",
                                                          valid_channel_key="true"):
    """
    payment_type: nb, card, wallet, upi
    """
    withhold_receipt = \
        (gc.PAYMENT_DB.do_sql(
            "select * from withhold_receipt where withhold_receipt_merchant_key='%s'" % merchant_key))[0]
    channel_key = withhold_receipt["withhold_receipt_channel_key"] if valid_channel_key == "true" else \
        withhold_receipt["withhold_receipt_channel_key"] + "fake "
    if payment_type.lower() == "netbanking":
        payment_option_i = "Net Banking"
        method_i = "netbanking"
        payment_mode_i = "FDRL"
    elif payment_type.lower() == "card":
        payment_option_i = "Debit Card"
        method_i = "card"
        payment_mode_i = "Visa"
    elif payment_type.lower() == "wallet":
        payment_option_i = "Wallet"
        method_i = "wallet"
        payment_mode_i = "airtelmoney"
    elif payment_type.lower() == "upi":
        payment_option_i = "Upi"
        method_i = "upi"
        payment_mode_i = None

    callback_task_request = {
        "code": 0,
        "message": "订单交易成功",
        "data": {
            "channel_name": channel_name,
            "channel_key": channel_key,
            "channel_code": "captured",
            "channel_message": None,
            "finish_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "amount": withhold_receipt["withhold_receipt_amount"],
            "ori_trans_no": None,
            "payment_option": payment_option_i,
            "method": method_i,
            "payment_mode": payment_mode_i,
            "service_charge": 1100,
            "service_tax": 198
        },
        "notify_type": None,
        "resp_result": "paid",
        "chargeDto": None
    }
    sql = "INSERT INTO `task` (`task_order_no`, `task_type`, `task_request_data`, `task_response_data`, `task_memo`, `task_status`, `task_next_run_at`," \
          " `task_create_at`, `task_update_at`, `task_version`, `task_priority`, `task_retrytimes`) " \
          "VALUES ('%s', 'withholdCallback', '%s', '', '', 'open', now(), now(), now(), 0, 1, 0);" \
          % (withhold_receipt["withhold_receipt_channel_key"],
             json.dumps(callback_task_request, ensure_ascii=False).replace("\"", "\\\"", 100))
    gc.PAYMENT_DB.do_sql(sql)
    return withhold_receipt["withhold_receipt_channel_key"]


def insert_scb_sdk_success_callback_task(merchant_key, channel_name, valid_channel_key="true"):
    """
    payment_type: 代码层面支持BP和CCFA, 业务层面只支持BP => BP + "", CCFA + Credit card
    """
    withhold_receipt = \
        (gc.PAYMENT_DB.do_sql(
            "select * from withhold_receipt where withhold_receipt_merchant_key='%s'" % merchant_key))[0]
    channel_key = withhold_receipt["withhold_receipt_channel_key"] if valid_channel_key == "true" \
        else withhold_receipt["withhold_receipt_channel_key"] + "fake"

    callback_task_request1 = {
        "code": 0,
        "message": "订单交易成功",
        "data": {
            "channel_name": channel_name,
            "channel_key": channel_key,
            "channel_code": "1",
            "channel_message": "callback PAID",
            "finish_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "amount": withhold_receipt["withhold_receipt_amount"],
            "ori_trans_no": withhold_receipt["withhold_receipt_channel_inner_key"],
            "payment_option": "Domestic Transfers",
            "method": None,
            "payment_mode": None,
            "service_charge": None,
            "service_tax": None,
            "card_dto": None,
            "middle_trans_no": None,
            "channel_names": None
        },
        "notify_type": None,
        "resp_result": {
            "resCode": "00",
            "resDesc": "success",
            "transactionId": withhold_receipt["withhold_receipt_channel_inner_key"],
            "confirmId": channel_key
        },
        "chargeDto": None
    }

    callback_task_request = {
        "code": 0,
        "message": "订单交易成功",
        "data": {
            "channel_name": channel_name,
            "channel_key": channel_key,
            "channel_code": "1",
            "channel_message": "callback PAID",
            "finish_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "amount": withhold_receipt["withhold_receipt_amount"],
            "ori_trans_no": withhold_receipt["withhold_receipt_channel_inner_key"],
            "payment_option": "Domestic Transfers",
            "method": None,
            "payment_mode": None,
            "service_charge": None,
            "service_tax": None,
            "card_dto": None,
            "middle_trans_no": None,
            "channel_names": None
        },
        "notify_type": None,
        "resp_result": "{\"resCode\":\"00\",\"resDesc\":\"success\",\"transactionId\":\"%s\",\"confirmId\":\"%s\"}" % (
            withhold_receipt["withhold_receipt_channel_inner_key"], channel_key),
        "chargeDto": None
    }

    sql = "INSERT INTO `task` (`task_order_no`, `task_type`, `task_request_data`, `task_response_data`, `task_memo`, `task_status`, `task_next_run_at`," \
          " `task_create_at`, `task_update_at`, `task_version`, `task_priority`, `task_retrytimes`) " \
          "VALUES ('%s', 'withholdCallback', '%s', '', '', 'open', now(), now(), now(), 0, 1, 0);" \
          % (withhold_receipt["withhold_receipt_channel_key"],
             json.dumps(callback_task_request, ensure_ascii=False).replace("\"", "\\\"", 100))
    gc.PAYMENT_DB.do_sql(sql)
    return withhold_receipt["withhold_receipt_channel_key"]


def insert_payloro_plwn_success_callback_task(merchant_key, channel_name, valid_channel_key="true"):
    """
    """
    withhold_receipt = \
        (gc.PAYMENT_DB.do_sql(
            "select * from withhold_receipt where withhold_receipt_merchant_key='%s'" % merchant_key))[0]
    channel_key = withhold_receipt["withhold_receipt_channel_key"] if valid_channel_key == "true" \
        else withhold_receipt["withhold_receipt_channel_key"] + "fake"

    callback_task_request = {
        "code": 0,
        "message": "订单交易成功",
        "data": {
            "channel_name": channel_name,
            "channel_key": channel_key,
            "channel_code": "SUCCESS",
            "channel_message": "SUCCESS",
            "finish_at": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            "amount": withhold_receipt["withhold_receipt_amount"],
            "ori_trans_no": withhold_receipt["withhold_receipt_channel_inner_key"],
            "payment_option": None,
            "method": None,
            "payment_mode": "PLWN",
            "service_charge": 11.21,
            "service_tax": None,
            "card_dto": None,
            "middle_trans_no": None,
            "channel_names": None
        },
        "notify_type": None,
        "resp_result": "{\"resCode\":\"00\",\"resDesc\":\"success\",\"transactionId\":\"%s\",\"confirmId\":\"%s\"}" % (
            withhold_receipt["withhold_receipt_channel_inner_key"], channel_key),
        "chargeDto": None
    }

    sql = "INSERT INTO `task` (`task_order_no`, `task_type`, `task_request_data`, `task_response_data`, `task_memo`, `task_status`, `task_next_run_at`," \
          " `task_create_at`, `task_update_at`, `task_version`, `task_priority`, `task_retrytimes`) " \
          "VALUES ('%s', 'withholdCallback', '%s', '', '', 'open', now(), now(), now(), 0, 1, 0);" \
          % (withhold_receipt["withhold_receipt_channel_key"],
             json.dumps(callback_task_request, ensure_ascii=False).replace("\"", "\\\"", 100))
    gc.PAYMENT_DB.do_sql(sql)
    return withhold_receipt["withhold_receipt_channel_key"]


def update_withhold_receipt_clear_inner_key(merchant_key):
    sql = "UPDATE withhold_receipt SET withhold_receipt_channel_inner_key='' WHERE withhold_receipt_merchant_key='%s' LIMIT 1" % merchant_key
    return gc.PAYMENT_DB.do_sql(sql)


def update_global_task_next_run_at(global_db):
    sql = "update task set task_next_run_at=current_time where task_status in ('open','error') order by task_id desc limit 100"
    run_task = global_db.update(sql)
    return run_task


def uptate_global_task_by_order_no_task_type(global_db, order_no, task_type, task_status):
    sql = "update task set task_status='%s' where task_order_no='%s' and task_type='%s'" % (
        task_status, order_no, task_type)
    global_db.update(sql)


def get_global_binding_sms_request_info_by_card_num(global_db, card_num):
    sql = "select * from binding_sms_request where binding_sms_request_card_num='%s'order by binding_sms_request_create_at desc limit 1" % card_num
    binding_sms_request = gc.PAYMENT_DB.query(sql)
    return binding_sms_request


def get_global_binding_request_info_by_card_num(global_db, card_num):
    sql = "select * from binding_request where binding_request_card_num='%s'order by binding_request_create_at desc limit 1" % card_num
    binding_request = gc.PAYMENT_DB.query(sql)
    return binding_request


def get_global_binding_info_by_card_num(global_db, card_num):
    sql = "select * from binding where binding_card_num='%s' order by binding_created_at desc limit 1" % card_num
    binding = gc.PAYMENT_DB.query(sql)
    return binding


def get_global_card_info_by_card_account(global_db, card_account):
    sql = "select * from card where card_account='%s' order by card_created_at desc limit 1" % card_account
    card = gc.PAYMENT_DB.query(sql)
    return card


def get_global_card_info_by_card_uuid(global_db, card_uuid):
    sql = "select * from card where card_num in (select account_card_num from account where account_card_uuid='%s' and account_auth_mode='account')" % card_uuid
    card = gc.PAYMENT_DB.query(sql)
    return card


def get_none_cardandaccount_bycarduuid(global_db, card_uuid):
    sql = "select * from account left join card on card_num=account_card_num where account_card_uuid='%s' order by account_id desc limit 1" % card_uuid
    ebank = gc.PAYMENT_DB.query(sql)
    return ebank


def get_global_account_info_by_card_num(global_db, card_num):
    sql = "select * from account where account_card_num='%s' order by account_created_at desc limit 1" % card_num
    account = gc.PAYMENT_DB.query(sql)
    return account


def get_delete_bindinfo(global_db, card_num):
    sql1 = "delete from binding where binding_card_num='%s'limit 100" % card_num
    sql2 = "delete from account where account_card_num='%s'limit 100" % card_num
    delete_result1 = global_db.delete(sql1)
    delete_result2 = global_db.delete(sql2)
    return delete_result1, delete_result2


def get_delete_bindinginfo(global_db, card_account):
    sql1 = "delete from binding where binding_card_num in (select card_num from card where card_account='%s')limit 100" % card_account
    sql2 = "delete from account where account_card_num in (select card_num from card where card_account='%s')limit 100" % card_account
    sql3 = "delete from card where card_account='%s'limit 100" % card_account  # card必须最后删
    delete_result1 = global_db.delete(sql1)
    delete_result2 = global_db.delete(sql2)
    delete_result3 = global_db.delete(sql3)
    return delete_result1, delete_result2, delete_result3


def get_delete_bindinginfo_by_crduuid(global_db, card_uuid, card_num):
    sql1 = "delete from binding where binding_card_num ='%s'" % card_num
    sql2 = "delete from account where card_uuid='%s' limit 100" % card_uuid
    sql3 = "delete from card where card_num='%s'limit 100" % card_num
    delete_result1 = global_db.delete(sql1)
    delete_result2 = global_db.delete(sql2)
    delete_result3 = global_db.delete(sql3)
    return delete_result1, delete_result2, delete_result3


def get_usable_card_uuid(global_db):  # 先写死代扣cashfree下的通道，该uuid只能用于ebank的代扣，不能用于订阅代扣
    sql = "SELECT  * FROM account LEFT JOIN binding ON account_card_num=binding_card_num  WHERE binding_status=1 and binding_channel_name='%s' " \
          "and account_auth_mode='account' order by account_id desc LIMIT 1" % india_bind_channel_name
    card_uuid = gc.PAYMENT_DB.query(sql)
    return card_uuid


def get_haveclosed_account_no(global_db):  # 先写死代扣cashfree下的通道，该uuid只能用于ebank的代扣，不能用于订阅代扣
    sql = "SELECT  * FROM withhold_account WHERE withhold_account_status='closed' and withhold_account_inner_no like '%va_EcitDZIWwDHn7n%' order by withhold_account_id desc LIMIT 1"
    withhold_account = gc.PAYMENT_DB.query(sql)
    return withhold_account


def get_usable_razorpay_withdraw_carduuid(global_db):  # 查询razorpay已开户成功的一个card_uuid
    sql = "SELECT  * FROM account LEFT JOIN binding ON account_card_num=binding_card_num  WHERE binding_status=1 and binding_channel_name='razorpay_yomoyo_withdraw' and account_auth_mode='account' order by account_id desc LIMIT 1"
    card_uuid = gc.PAYMENT_DB.query(sql)
    return card_uuid


def get_usable_cashfree_withdraw_carduuid(global_db, channel_name):  # 查询cashfree已开户成功的一个card_uuid
    sql = "SELECT  * FROM account LEFT JOIN binding ON account_card_num=binding_card_num  WHERE binding_status=1 and binding_channel_name='%s' and account_auth_mode='account' order by account_id desc LIMIT 1" % channel_name
    card_uuid = gc.PAYMENT_DB.query(sql)
    return card_uuid


def get_usable_subscribe_carduuid(global_db):  # 订阅绑卡是用户自动代扣，当一个card_uuuid有多张卡都订阅绑卡成功时，选account_id小的那一个进行代扣
    sql = "SELECT account_card_uuid FROM account LEFT JOIN binding ON account_card_num=binding_card_num  WHERE binding_status=1 and binding_channel_name='cashfree_yomoyo2_subscribe' and account_auth_mode='card' order by account_id desc LIMIT 1"
    card_uuid = gc.PAYMENT_DB.query(sql)
    return card_uuid


def by_card_carduuid_get_account(global_db,
                                 card_uuid):  # 用于订阅代扣选代扣card_num，当一个uuid对应多张卡时这一步取出来的card_num不一定是代扣的，订阅代扣取account_id小的那一个
    sql = "select * from account  LEFT JOIN binding ON account_card_num=binding_card_num  WHERE binding_status=1 and account_card_uuid='%s'AND binding_channel_name='cashfree_yomoyo2_subscribe' and account_auth_mode='card' order by account_id asc limit 1" % card_uuid
    account = gc.PAYMENT_DB.query(sql)
    return account


def add_withdraw_fail_channel_error(global_db):
    sql = "INSERT INTO `channel_error` (`channel_error_provider_code`, `channel_error_code`, `channel_error_msg`, `channel_error_status`, `channel_error_type`) VALUES  ('cashfree', '400', 'Transfer Id already exists', 1, 'WITHDRAW') ON DUPLICATE KEY UPDATE channel_error_status=1"
    fail_channel_error = global_db.insert(sql)
    return fail_channel_error


def add_withdold_fail_channel_error(global_db):
    sql = "INSERT INTO `channel_error` (`channel_error_provider_code`, `channel_error_code`, `channel_error_msg`, `channel_error_status`, `channel_error_type`) VALUES  ('cashfree', 'FLAGGED-CANCELLED', '组合码', 1, 'CHARGE_QUERY') ON DUPLICATE KEY UPDATE channel_error_status=1"
    fail_channel_error = global_db.insert(sql)
    return fail_channel_error


def get_global_withdraw_channel_request_log_by_channel_key(global_db, channel_key):
    sql = "SELECT * FROM channel_request_log  WHERE channel_request_log_channel_key='%s' and channel_request_log_type='WITHDRAW' order by channel_request_log_id desc limit 1" % channel_key
    channel_request_log_info = gc.PAYMENT_DB.query(sql)
    return channel_request_log_info


def get_global_withhold_channel_request_log_by_channel_key(global_db, channel_key):
    sql = "SELECT * FROM channel_request_log  WHERE channel_request_log_channel_key='%s' and channel_request_log_type in ('CHARGE','CHARGE_SUBSCRIPTION','CHARGE_SDK') order by channel_request_log_id desc limit 1" % channel_key
    channel_request_log_info = gc.PAYMENT_DB.query(sql)
    return channel_request_log_info


def get_global_withholdaccountinfo_by_accountno(global_db, account_no):
    sql = "select * from withhold_account where withhold_account_no='%s' order by withhold_account_id desc limit 1" % account_no
    withhold_account = gc.PAYMENT_DB.query(sql)
    return withhold_account
    return channel_request_log_info


def get_razorpay_accountregister_channelrequestlog_by_customerid(global_db, customer_id):
    sql = "SELECT * FROM channel_request_log  WHERE channel_request_log_channel_key='%s' and channel_request_log_type='ACCOUNT_REGISTER'  order by channel_request_log_id desc limit 1" % customer_id
    channel_request_log_info = gc.PAYMENT_DB.query(sql)
    return channel_request_log_info


def get_razorpay_customerregister_channelrequestlog(global_db):
    # 这里以后可能会有问题，因为razorpay创建联系人没有关键词可以查询，先这样
    sql = "SELECT * FROM channel_request_log  WHERE channel_request_log_type='CUSTOMER_REGISTER'  order by channel_request_log_id desc limit 1"
    channel_request_log_info = gc.PAYMENT_DB.query(sql)
    return channel_request_log_info


def update_withholdaccount_only_one_usableaccount(global_db, withhold_account_inner_no):
    sql = "UPDATE withhold_account SET withhold_account_status='closed' WHERE withhold_account_no NOT IN (SELECT a.withhold_account_no FROM  (SELECT withhold_account_no FROM withhold_account WHERE withhold_account_inner_no='%s' AND withhold_account_status='active' ORDER BY withhold_account_id DESC LIMIT 1  )  AS a )" % withhold_account_inner_no
    withhold_account = global_db.update(sql)
    return withhold_account


def update_withholdaccount_allactive(global_db, withhold_account_inner_no):
    sql = "UPDATE withhold_account SET withhold_account_status='active' WHERE withhold_account_inner_no='%s' " % withhold_account_inner_no
    withhold_account = global_db.update(sql)
    return withhold_account


def delete_razorpay_collect_withholdandreceiptandcard(global_db, global_razorpay_collect_channel_key1,
                                                      global_razorpay_collect_channel_key2,
                                                      global_razorpay_collect_cardnum_encrypt):
    sql1 = "DELETE FROM withhold WHERE withhold_merchant_key='%s' " % global_razorpay_collect_channel_key1
    sql2 = "DELETE FROM withhold WHERE withhold_merchant_key='%s' " % global_razorpay_collect_channel_key2
    sql3 = "DELETE FROM withhold_receipt WHERE withhold_receipt_merchant_key='%s' " % global_razorpay_collect_channel_key1
    sql4 = "DELETE FROM withhold_receipt WHERE withhold_receipt_merchant_key='%s' " % global_razorpay_collect_channel_key2
    sql5 = "DELETE FROM card WHERE card_account='%s' limit 1 " % global_razorpay_collect_cardnum_encrypt
    delete_result1 = global_db.delete(sql1)
    delete_result2 = global_db.delete(sql2)
    delete_result3 = global_db.delete(sql3)
    delete_result4 = global_db.delete(sql4)
    delete_result5 = global_db.delete(sql5)
    return delete_result1, delete_result2, delete_result3, delete_result4, delete_result5


def get_rbiz_collect_callbackurl(global_db):
    sql = "SELECT keyvalue_value FROM keyvalue WHERE keyvalue_key='callback_config'"
    task_order_no = gc.PAYMENT_DB.query(sql)
    return task_order_no


def uppdate_withhold_receipt_status(global_db, merchant_key):
    sql1 = "UPDATE withhold_receipt SET withhold_receipt_status='0' WHERE withhold_receipt_merchant_key='%s' " % merchant_key
    mock_kv1 = global_db.update(sql1)
    return mock_kv1


def delete_withhold_receipt_by_merchantkey(global_db, merchant_key):
    sql1 = "delete from withhold_receipt where withhold_receipt_merchant_key='%s' limit 1" % merchant_key
    delete_result1 = global_db.delete(sql1)
    return delete_result1


def insert_kser_qrcode_callback(global_db, channel_key):
    sql = "INSERT INTO `task` (`task_order_no`, `task_type`, `task_request_data`, `task_status`) VALUES " \
          "('%s', 'withholdCallback', '{\"code\":0,\"message\":\"订单交易成功\",\"data\":" \
          "{\"channel_name\":\"ksher_cymo2_qrcode\",\"channel_key\":\"%s\",\"channel_code\":\"SUCCESS\"," \
          "\"channel_message\":\"SUCCESS\",\"finish_at\":\"%s\",\"amount\":1," \
          "\"ori_trans_no\":\"90020200515163158797150\"," \
          "\"payment_mode\":null},\"resp_result\":\"SUCCESS\",\"chargeDto\":null}', 'open');" % \
          (channel_key, channel_key, get_date())
    result = global_db.insert(sql)
    return result


def by_carduuid_get_ccountandbinding_info(global_db, card_uuid, channel_name):
    sql = "SELECT * FROM account LEFT JOIN binding ON account_card_num=binding_card_num  WHERE binding_status=1 " \
          "AND binding_channel_name='%s' AND  account_card_uuid='%s' AND account_auth_mode='account'" % (
              channel_name, card_uuid)
    account = gc.PAYMENT_DB.query(sql)
    return account


def delete_razorpay_transfer_withdrawandreceipt(global_db, global_razorpay_transfer_id):
    sql1 = "DELETE FROM withdraw WHERE withdraw_merchant_key IN (SELECT withdraw_receipt_merchant_key FROM  withdraw_receipt WHERE withdraw_receipt_channel_inner_key='%s') " % global_razorpay_transfer_id
    sql2 = "DELETE FROM withdraw_receipt WHERE withdraw_receipt_channel_inner_key='%s' " % global_razorpay_transfer_id
    sql3 = "DELETE FROM channel_reconci WHERE channel_reconci_channel_order_no='%s' " % global_razorpay_transfer_id
    delete_result1 = global_db.delete(sql1)
    delete_result2 = global_db.delete(sql2)
    delete_result3 = global_db.delete(sql3)
    return delete_result1, delete_result2, delete_result3


def insert_channel_reconci(global_db, channel_key, merchant_key, amount, fee, service_charge, service_tax):
    sql = "INSERT INTO `channel_reconci` ( `channel_reconci_date`, `channel_reconci_channel_name`, `channel_reconci_channel_key`, " \
          "`channel_reconci_channel_order_no`, `channel_reconci_amount`, `channel_reconci_bank_name`, `channel_reconci_bank_code`, `channel_reconci_account`," \
          " `channel_reconci_user_name`, `channel_reconci_remark`, `channel_reconci_order_created_at`, `channel_reconci_order_finished_at`, " \
          "`channel_reconci_status`, `channel_reconci_type`, `channel_reconci_created_at`, `channel_reconci_updated_at`, `channel_reconci_provider_code`, " \
          "`channel_reconci_merchant_no`, `channel_reconci_settlement_id`, `channel_reconci_settlement_amount`, `channel_reconci_payment_mode`, `channel_reconci_fees`, " \
          "`channel_reconci_service_charge`, `channel_reconci_service_tax`, `channel_reconci_product_type`)" \
          "VALUES ( '2020-04-07', 'razorpay_yomoyo_ebank', '%s', '%s', %s, 'ICIC', '', '', '', '', '1000-01-01 00:00:00', '2020-03-28 08:52:32', 2, " \
          "'WITHHOLD', '2020-04-07 14:12:04', '2020-04-07 14:12:06', 'razorpay', '111', '228075', %s,'card', %s, %s, %s, '')" % \
          (channel_key, merchant_key, amount, amount - fee, fee, service_charge, service_tax)
    channel_reconci = global_db.insert(sql)
    return channel_reconci


def insert_withhold_receipt(global_db, channel_key, merchant_key, amount, service_charge, service_tax):
    sql = "INSERT INTO `withhold_receipt` ( `withhold_receipt_merchant_name`, `withhold_receipt_merchant_key`, `withhold_receipt_channel_name`, `withhold_receipt_channel_key`," \
          " `withhold_receipt_channel_inner_key`, `withhold_receipt_card_num`, `withhold_receipt_amount`, `withhold_receipt_status`, `withhold_receipt_status_stage`," \
          " `withhold_receipt_channel_resp_code`, `withhold_receipt_channel_resp_message`, `withhold_receipt_started_at`, `withhold_receipt_finished_at`, " \
          "`withhold_receipt_created_at`, `withhold_receipt_updated_at`, `withhold_receipt_redirect`, `withhold_receipt_ruleset_code`, `withhold_receipt_payment_mode`," \
          " `withhold_receipt_description`, `withhold_receipt_service_charge`, `withhold_receipt_service_tax`)" \
          "VALUES ('Rbiz', '%s', 'razorpay_yomoyo_ebank', '%s', '', 'enc_03_2771503736404058112_068', %s, 2, 0, 'SUCCESS', '', '2020-05-22 12:58:11', " \
          "'1000-01-01 00:00:00', '2020-05-22 12:58:05', '2020-06-11 13:36:14', '', '', '', '', %s, %s);" % \
          (merchant_key, channel_key, amount, service_charge, service_tax)
    withhold_receipt = global_db.insert(sql)
    return withhold_receipt


def add_transfer_fail_channel_error(global_db):
    # 有则更新，无则创建一条
    sql = "INSERT INTO `channel_error` (`channel_error_provider_code`, `channel_error_code`, `channel_error_msg`, `channel_error_status`, `channel_error_type`) VALUES  " \
          "('razorpay', 'BAD_REQUEST_ERROR', 'BAD_REQUEST_ERROR', 1, 'TRANSFER') ON DUPLICATE KEY UPDATE channel_error_status=1"
    fail_channel_error = global_db.insert(sql)
    return fail_channel_error


def insert_razorpay_ransfer_data(global_db, card_uuid, card_num, channel_name, acct_id, card_account):
    # 有则更新，无则创建一条
    sql1 = "INSERT INTO `account` (`account_card_uuid`, `account_card_num`, `account_created_at`, `account_updated_at`, `account_auth_mode`) " \
           "VALUES ('%s', '%s', '%s', '%s', 'account') ON DUPLICATE KEY UPDATE account_card_uuid='%s' " % \
           (card_uuid, card_num, get_date(), get_date(), card_uuid)
    sql2 = "INSERT INTO `binding` ( `binding_card_num`, `binding_channel_name`, `binding_type`, `binding_status`, `binding_created_at`, `binding_updated_at`," \
           " `binding_info`, `binding_protocol_info`, `binding_register_name`)" \
           "VALUES ('%s', '%s', 4, 1, '%s', '%s','', '{\"acct_id\":\"%s\"}', '')  ON DUPLICATE KEY UPDATE binding_card_num='%s' " % \
           (card_num, channel_name, get_date(), get_date(), acct_id, card_num)
    sql3 = "INSERT INTO `card` (`card_num`, `card_account`, `card_account_mask`, `card_id_num`, `card_id_num_mask`, `card_username`, `card_username_mask`, " \
           "`card_bank_code`, `card_status`, `card_created_at`, `card_updated_at`, `card_auth_mode`)" \
           "VALUES ('%s', '%s', '1111****1111', 'enc_04_2917886558479065088_754', '34****19930705528*'," \
           " 'enc_04_2828155385377464320_484', 'M**********I', 'testtransfer001', 1, '2020-03-25 19:36:06', '2020-06-11 12:21:10', 'account')  ON DUPLICATE KEY UPDATE card_num='%s' " % \
           (card_num, card_account, card_num)
    result1 = global_db.insert(sql1)
    result2 = global_db.insert(sql2)
    result3 = global_db.insert(sql3)
    return result1, result2, result3


def add_withhold_receipt_channel_reconci(global_db, channel_key):
    # 有则更新，无则创建一条
    sql = "INSERT INTO `withhold_receipt` ( `withhold_receipt_merchant_name`, `withhold_receipt_merchant_key`, `withhold_receipt_channel_name`, `withhold_receipt_channel_key`," \
          " `withhold_receipt_channel_inner_key`, `withhold_receipt_card_num`, `withhold_receipt_amount`, `withhold_receipt_status`, `withhold_receipt_status_stage`," \
          " `withhold_receipt_channel_resp_code`, `withhold_receipt_channel_resp_message`, `withhold_receipt_started_at`, `withhold_receipt_finished_at`," \
          " `withhold_receipt_created_at`, `withhold_receipt_updated_at`, `withhold_receipt_redirect`, `withhold_receipt_ruleset_code`, `withhold_receipt_payment_option`," \
          " `withhold_receipt_payment_mode`, `withhold_receipt_description`, `withhold_receipt_service_charge`, `withhold_receipt_service_tax`)" \
          "VALUES ('Rbiz', '%s', 'cashfree_yomoyo2_ebank', '%s', '', 'enc_03_2771503736404058112_068', 400000, 2, 0, " \
          "'SUCCESS', '', '2020-05-22 12:58:11', '1000-01-01 00:00:00', '2020-05-22 12:58:05', '2020-06-11 13:36:14', '', '', '', '', '', 1100, 198)" \
          " ON DUPLICATE KEY UPDATE withhold_receipt_merchant_key='%s' " % (channel_key, channel_key, channel_key)
    withhold_receipt = global_db.insert(sql)
    return withhold_receipt


def uppdate_withholdandreceipt_channel_key(global_db, channel_key1, channel_key2):
    random = get_random_num()
    sql1 = "UPDATE withhold SET withhold_merchant_key='autotest_%s_%s'WHERE withhold_merchant_key='%s' " \
           % (channel_key1, random, channel_key1)
    sql2 = "UPDATE withhold SET withhold_merchant_key='autotest_%s_%s'WHERE withhold_merchant_key='%s' " \
           % (channel_key2, random, channel_key2)
    sql3 = "UPDATE withhold_receipt SET withhold_receipt_merchant_key='autotest_%s_%s',withhold_receipt_channel_key='autotest_%s_%s' WHERE withhold_receipt_merchant_key='%s' " \
           % (channel_key1, random, channel_key1, random, channel_key1)
    sql4 = "UPDATE withhold_receipt SET withhold_receipt_merchant_key='autotest_%s_%s',withhold_receipt_channel_key='autotest_%s_%s' WHERE withhold_receipt_merchant_key='%s' " \
           % (channel_key2, random, channel_key2, random, channel_key2)
    mock_kv1 = global_db.update(sql1)
    mock_kv2 = global_db.update(sql2)
    mock_kv3 = global_db.update(sql3)
    mock_kv4 = global_db.update(sql4)
    return mock_kv1, mock_kv2, mock_kv3, mock_kv4


# 获取kv值
def get_keyvalue_value(keyvalue_key):
    sql = "SELECT keyvalue_value FROM keyvalue WHERE keyvalue_key='%s' " % keyvalue_key
    keyvalue_value = gc.PAYMENT_DB.do_sql(sql)
    return keyvalue_value[0]["keyvalue_value"]


def update_xendit_withhold_receipt_create_at(merchant_key, created_at):
    sql = "UPDATE withhold_receipt SET withhold_receipt_created_at='%s' WHERE withhold_receipt_merchant_key='%s' " % (created_at, merchant_key)
    gc.PAYMENT_DB.do_sql(sql)