
import common.global_const as gc


def get_withhold_info_by_card_num(card_num):
    sql = "select * from withhold where withhold_card_num='%s' order by withhold_created_at desc limit 1" % card_num
    withhold_info = gc.PAYMENT_DB.query(sql)
    return withhold_info


def get_withhold_receipt_info_by_card_num(card_num):
    sql = "select * from withhold_receipt where withhold_receipt_card_num='%s' order by withhold_receipt_created_at desc limit 1 " % card_num
    withhold_receipt_info = gc.PAYMENT_DB.query(sql)
    return withhold_receipt_info


def get_withdraw_info_by_card_num(card_num):
    sql = "select * from withdraw where withdraw_receiver_no='%s' order by withdraw_created_at desc limit 1" % card_num
    withdraw_info = gc.PAYMENT_DB.query(sql)
    return withdraw_info


def get_withdraw_info_by_trade_no(trade_no):
    sql = "SELECT * FROM withdraw LEFT JOIN withdraw_receipt ON withdraw_receipt_merchant_key=withdraw_merchant_key  WHERE withdraw_receipt_trade_no='%s'  order by withdraw_created_at desc limit 1" % trade_no
    withdraw_info = gc.PAYMENT_DB.query(sql)
    return withdraw_info


def get_withdraw_receipt_info_by_card_num(card_num):
    sql = "SELECT * FROM withdraw_receipt LEFT JOIN withdraw ON  withdraw_receipt_merchant_key=withdraw_merchant_key WHERE withdraw_receiver_no='%s'order by withdraw_receipt_created_at desc limit 1" % card_num
    withdraw_receipt_info = gc.PAYMENT_DB.query(sql)
    return withdraw_receipt_info


def get_withdraw_receipt_info_by_trade_no(trade_no):
    sql = "SELECT * FROM withdraw_receipt  WHERE withdraw_receipt_trade_no='%s'order by withdraw_receipt_created_at desc limit 1" % trade_no
    withdraw_receipt_info = gc.PAYMENT_DB.query(sql)
    return withdraw_receipt_info


def update_task_next_run_at():
    sql = "update task set task_next_run_at=current_time where task_status in ('open','error') order by task_id desc limit 100"
    run_task = gc.PAYMENT_DB.update(sql)
    return run_task


def get_binding_sms_request_info_by_card_num(card_num):
    sql = "select * from binding_sms_request where binding_sms_request_card_num='%s'order by binding_sms_request_create_at desc limit 1" % card_num
    binding_sms_request = gc.PAYMENT_DB.query(sql)
    return binding_sms_request


def get_binding_request_info_by_card_num(card_num):
    sql = "select * from binding_request where binding_request_card_num='%s'order by binding_request_create_at desc limit 1" % card_num
    binding_request = gc.PAYMENT_DB.query(sql)
    return binding_request


def get_binding_info_by_card_num(card_num):
    sql = "select * from binding where binding_card_num='%s' order by binding_created_at desc limit 1" % card_num
    binding = gc.PAYMENT_DB.query(sql)
    return binding


def get_card_info_by_card_num(card_num):
    sql = "select * from card where card_num='%s' order by card_created_at desc limit 1" % card_num
    card = gc.PAYMENT_DB.query(sql)
    return card


def get_account_info_by_card_num(card_num):
    sql = "select * from account where account_card_num='%s' order by account_created_at desc limit 1" % card_num
    account = gc.PAYMENT_DB.query(sql)
    return account
