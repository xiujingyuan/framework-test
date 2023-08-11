import common.global_const as gc


# 修改渠道评分
def update_provider_score(score, provider, sign):
    sql = "update provider_sign_company set provider_sign_company_score='%s' " \
          "where provider_sign_company_provider_code='%s' and provider_sign_company_sign_company_code='%s'" \
          % (score, provider, sign)
    gc.PAYMENT_DB.do_sql(sql)


# 获取用户卡信息
def get_carduuid_bycardnum(account_type, card_num):
    sql = "select * from account inner join card on account_card_num=card_num where account_auth_mode='%s' " \
          "and card_auth_mode='%s' and card_account='%s' order by account_id desc limit 1" % (
          account_type, account_type, card_num)
    return gc.PAYMENT_DB.do_sql(sql)


# 修改task的状态和下次执行时间
def update_task_by_task_order_no(task_order_no, status):
    if status == "close":
        sql = "update task set task_status='close' where task_order_no='%s'" % (task_order_no)
    else:
        sql = "update task set task_next_run_at = now(),task_status='open' where task_order_no='%s'" % (task_order_no)
    gc.PAYMENT_DB.do_sql(sql)


# 修改错误码
def update_channel_error(provider, error_code, error_status, error_type, status="insert"):
    sql_query = "select * from channel_error " \
                "where channel_error_provider_code='%s' and channel_error_code='%s'" % (provider, error_code)
    result_query = gc.PAYMENT_DB.do_sql(sql_query)
    if not result_query:
        sql = "INSERT INTO `channel_error` (`channel_error_provider_code`, `channel_error_code`, " \
              "`channel_error_msg`, `channel_error_status`, `channel_error_type`) " \
              "VALUES " \
              "('%s', '%s', '%s', %s, '%s');" % (provider, error_code, "", error_status, error_type)
    else:
        sql = "update channel_error set channel_error_status='%s' " \
              "where channel_error_provider_code='%s' and channel_error_code='%s' " \
              "and channel_error_type like '%%%s%%'" % \
              (error_status, provider, error_code, error_type)
    if status == "delete":
        sql1 = "delete from channel_error " \
               "where channel_error_provider_code='%s' and channel_error_code='%s'" % (provider, error_code)
        gc.PAYMENT_DB.do_sql(sql1)
    gc.PAYMENT_DB.do_sql(sql)


# 修改订单创建时间，主要用在超时关单上，且只有代扣会用到
def update_receipt_created_at(task_order_no, created_at):
    sql = "update withhold_receipt set withhold_receipt_created_at='%s' where withhold_receipt_merchant_key='%s'" % \
          (created_at, task_order_no)
    gc.PAYMENT_DB.do_sql(sql)

# 修改订单过期时间，主要用在超时关单上，且只有代扣会用到
def update_withhold_receipt_expired_at(task_order_no, expired_at):
    sql = "update withhold_receipt set withhold_receipt_expired_at='%s' where withhold_receipt_merchant_key='%s'" % \
          (expired_at, task_order_no)
    gc.PAYMENT_DB.do_sql(sql)


# 查询代付订单
def get_withdraw_receipt_by_channel_key(channel_key):
    sql = "select * from withdraw_receipt where withdraw_receipt_channel_key='%s'" % channel_key
    return gc.PAYMENT_DB.query(sql)


def get_withdraw_by_merchant_key(merchant_key):
    sql = "select * from withdraw where withdraw_merchant_key='%s'" % merchant_key
    rs = gc.PAYMENT_DB.query(sql)
    return rs


def get_withdraw_receipt_by_merchant_key(merchant_key):
    sql = "select * from withdraw_receipt where withdraw_receipt_merchant_key='%s'" % merchant_key
    rs = gc.PAYMENT_DB.query(sql)
    return rs


def get_withhold_by_merchant_key(merchant_key):
    sql = "select * from withhold where withhold_merchant_key='%s'" % merchant_key
    rs = gc.PAYMENT_DB.query(sql)
    return rs


def get_withhold_receipt_by_merchant_key(merchant_key):
    sql = "select * from withhold_receipt where withhold_receipt_merchant_key='%s'" % merchant_key
    rs = gc.PAYMENT_DB.query(sql)
    return rs


def get_binding_by_card_uuid(card_uuid):
    sql = "select * from binding where binding_card_uuid='%s'" % card_uuid
    rs = gc.PAYMENT_DB.query(sql)
    return rs


def get_binding_merchant_request_by_merchant_key(merchant_key):
    sql = "select * from binding_merchant_request where binding_merchant_request_merchant_key='%s'" % merchant_key
    rs = gc.PAYMENT_DB.query(sql)
    return rs


def get_binding_request_by_merchant_key(merchant_key):
    sql = "select * from binding_request where binding_request_merchant_key='%s'" % merchant_key
    rs = gc.PAYMENT_DB.query(sql)
    return rs


def get_fusing_latest(channel_name):
    sql = "select * from fusing where fusing_channel_name='%s' order by fusing_id desc" % channel_name
    rs = gc.PAYMENT_DB.query(sql)
    return rs[0]


def get_fusing_log_by_trace_no(trace_no):
    sql = "select * from fusing_log where fusing_log_trace_no='%s'" % trace_no
    rs = gc.PAYMENT_DB.query(sql)
    return rs


def update_fusing_all_close():
    sql = "update fusing set fusing_status = 'close' where fusing_status = 'open'"
    gc.PAYMENT_DB.do_sql(sql)


def update_fusing_create_at(trace_no, create_at):
    sql = "update fusing set fusing_create_at = '%s' where fusing_trace_no = '%s'" % (create_at, trace_no)
    gc.PAYMENT_DB.do_sql(sql)


def update_withdraw_status(merchant_key, status):
    if status == "success":
        withdraw_status, withdraw_receipt_status = 2, 2
    elif status == "fail":
        withdraw_status, withdraw_receipt_status = 3, 3
    elif status == "new":
        withdraw_status, withdraw_receipt_status = 1, 0
    elif status == "process":
        withdraw_status, withdraw_receipt_status = 1, 1
    sql_1 = "update withdraw set withdraw_status='%s' where withdraw_merchant_key='%s'" % (withdraw_status, merchant_key)
    sql_2 = "update withdraw_receipt set withdraw_receipt_status='%s' where withdraw_receipt_merchant_key='%s'" % \
          (withdraw_receipt_status, merchant_key)
    gc.PAYMENT_DB.do_sql(sql_1)
    gc.PAYMENT_DB.do_sql(sql_2)
