from biztest.util.tools.tools import *
from copy import deepcopy
import common.global_const as gc


# env = get_sysconfig("--env")
# country = get_sysconfig("--country")
#
# gc.REPAY_DB.= DataBase("global_rbiz%s_%s" % (env, country))


def get_coupon_info_by_item_no(item_no):
    sql = "SELECT * FROM coupon WHERE coupon_asset_item_no='%s'" % item_no
    coupon_info = gc.REPAY_DB.query(sql)
    return coupon_info


def get_asset_info_by_item_no(item_no):
    sql = "select * from asset where asset_item_no='%s'" % item_no
    asset_info = gc.REPAY_DB.query(sql)
    return asset_info


def update_asset_status_all():
    sql = "update asset set asset_status='payoff'"
    gc.REPAY_DB.update(sql)


def update_asset(asset_item_no, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + key + "='" + str(value) + "', "
    sql = "update asset set %s where asset_item_no='%s'" % (sql_params[:-2], asset_item_no)
    gc.REPAY_DB.do_sql(sql)


def get_asset(**kwargs):
    sql = "select * from asset where %s order by asset_id" % generate_sql(kwargs, "and")
    asset_list = gc.REPAY_DB.do_sql(sql)
    return asset_list


def get_asset_delay(**kwargs):
    sql = "select * from asset_delay where %s order by asset_delay_id" % generate_sql(kwargs, "and")
    asset_delay_list = gc.REPAY_DB.do_sql(sql)
    return asset_delay_list


def get_asset_tran(**kwargs):
    sql = "select * from asset_tran where %s order by asset_tran_id" % generate_sql(kwargs, "and")
    asset_tran_list = gc.REPAY_DB.do_sql(sql)
    return asset_tran_list


def delete_asset_tran(**kwargs):
    sql = "delete from asset_tran where %s" % generate_sql(kwargs, "and")
    gc.REPAY_DB.do_sql(sql)


def get_asset_tran_log(**kwargs):
    sql = "select * from asset_tran_log where %s order by asset_tran_log_id" % generate_sql(kwargs, "and")
    asset_tran_log_list = gc.REPAY_DB.do_sql(sql)
    return asset_tran_log_list


def get_asset_extend(**kwargs):
    sql = "select * from asset_extend where %s order by asset_extend_id" % generate_sql(kwargs, "and")
    asset_tran_list = gc.REPAY_DB.do_sql(sql)
    return asset_tran_list


def delete_asset_extend(**kwargs):
    sql = "delete from asset_extend where %s" % generate_sql(kwargs, "and")
    gc.REPAY_DB.do_sql(sql)


def get_asset_tran_by_item_no(item_no, period_list=[1]):
    if len(period_list) == 1:
        period_list = "(" + str(period_list[0]) + ")"
    else:
        period_list = str(tuple(period_list))
    sql = "SELECT * FROM asset_tran WHERE asset_tran_asset_item_no='%s' AND asset_tran_period in %s ORDER BY asset_tran_period" % (
        item_no, period_list)
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran


def get_asset_tran_by_tran_no(tran_no):
    sql = "SELECT * FROM asset_tran WHERE asset_tran_no='%s' ORDER BY asset_tran_period" % tran_no
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran


def get_asset_tran_log_by_item_no(item_no):
    sql = "SELECT * FROM asset_tran_log WHERE asset_tran_log_asset_item_no='%s' ORDER BY asset_tran_log_id DESC" % item_no
    asset_tran_log = gc.REPAY_DB.query(sql)
    return asset_tran_log


def get_withhold(**kwargs):
    sql = "select * from withhold where %s order by withhold_id" % generate_sql(kwargs, "and")
    withhold_list = gc.REPAY_DB.do_sql(sql)
    return withhold_list


def get_withhold_order(**kwargs):
    sql = "select * from withhold_order where %s order by withhold_order_id" % generate_sql(kwargs, "and")
    withhold_order_list = gc.REPAY_DB.do_sql(sql)
    return withhold_order_list


def get_withhold_success_by_item_no(item_no):
    sql = "SELECT * FROM withhold WHERE withhold_serial_no IN (SELECT withhold_order_serial_no FROM withhold_order " \
          "WHERE withhold_order_reference_no ='%s' and withhold_status='success') order by withhold_id" % item_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_by_item_no(item_no):
    sql = "SELECT * FROM withhold WHERE withhold_serial_no IN (SELECT withhold_order_serial_no FROM withhold_order " \
          "WHERE withhold_order_reference_no ='%s') order by withhold_id" % item_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_order_by_item_no(item_no):
    sql = "SELECT *  FROM withhold_order WHERE withhold_order_reference_no ='%s'" % item_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_by_request_no(request_no):
    sql = "SELECT *  FROM withhold WHERE withhold_request_no ='%s'" % request_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_detail_by_item_no(item_no, serial_no=None):
    sql = "SELECT *  FROM withhold_detail WHERE withhold_detail_asset_item_no ='%s' " % item_no
    if serial_no is not None:
        sql = "SELECT * FROM withhold_detail WHERE withhold_detail_asset_item_no ='%s' and " \
              "withhold_detail_serial_no='%s'" % (item_no, serial_no)
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_request_by_item_no(item_no):
    sql = "SELECT * FROM withhold_request WHERE withhold_request_no IN (SELECT withhold_order_request_no FROM " \
          "withhold_order WHERE withhold_order_reference_no ='%s')" % item_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_by_serial_no(serial_no):
    sql = "SELECT * FROM withhold WHERE withhold_serial_no ='%s'" % serial_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_order_by_serial_no(serial_no):
    sql = "SELECT *  FROM withhold_order WHERE withhold_order_serial_no ='%s'" % serial_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_request_by_serial_no(serial_no):
    sql = "SELECT * FROM withhold_request WHERE withhold_request_no IN (SELECT withhold_order_request_no FROM " \
          "withhold_order WHERE withhold_order_serial_no ='%s')" % serial_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_detail_by_serial_no(serial_no):
    sql = "SELECT *  FROM withhold_detail WHERE withhold_detail_serial_no ='%s'" % serial_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_detail_by_serial_no_inner_join_asset_tran(serial_no):
    sql = "SELECT *  FROM withhold_detail inner join asset_tran on withhold_detail_asset_tran_no=asset_tran_no " \
          "WHERE withhold_detail_serial_no ='%s'" % serial_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_account_recharge_by_serial_no(channel_key):
    sql = "select * from account_recharge where account_recharge_serial_no='%s' order by account_recharge_id" % channel_key
    recharge = gc.REPAY_DB.query(sql)
    return recharge


def get_account_recharge_log_by_serial_no(channel_key):
    sql = 'select * from account_recharge_log where account_recharge_log_recharge_serial_no="{}" order by ' \
          'account_recharge_log_id'.format(channel_key)
    recharge_Log = gc.REPAY_DB.query(sql)
    return recharge_Log


def get_account_repay_by_serial_no(channel_key):
    sql = 'select * from account_repay where account_repay_recharge_serial_no="{}" order by account_repay_id'.format(
        channel_key)
    account_repay = gc.REPAY_DB.query(sql)
    return account_repay


def get_account_repay_by_serial_no_inner_join_asset_tran(channel_key):
    sql = 'select * from account_repay inner join asset_tran on account_repay_tran_no=asset_tran_no ' \
          'where account_repay_recharge_serial_no="{}" order by account_repay_id'.format(channel_key)
    account_repay = gc.REPAY_DB.query(sql)
    return account_repay


def get_account_repay_log_by_serial_no(channel_key):
    sql = 'select * from account_repay_log where account_repay_log_repay_no in (select account_repay_no from ' \
          'account_repay where account_repay_recharge_serial_no="{}") order by account_repay_log_id'.format(channel_key)
    account_repay_log = gc.REPAY_DB.query(sql)
    return account_repay_log


def get_account_by_id_num(id_num):
    sql = 'select * from account where account_user_id_num_encrypt="{}"'.format(id_num)
    account = gc.REPAY_DB.query(sql)
    return account


def get_account_by_item_no(item_no):
    sql = 'select * from individual_asset ' \
          'join individual on individual_asset_individual_no=individual_no ' \
          'where individual_asset_asset_item_no="{}"'.format(item_no)
    id_num = gc.REPAY_DB.query(sql)[0]["individual_id_num_encrypt"]
    account = get_account_by_id_num(id_num)[0]
    return account


def get_trade_by_trade_no(trade_no):
    sql = "SELECT * FROM trade WHERE trade_ref_no='%s'" % trade_no
    trade = gc.REPAY_DB.query(sql)
    return trade


def get_trade_by_serial_no(serial_no):
    sql = "SELECT * FROM trade join trade_tran on trade_no=trade_tran_trade_no " \
          "WHERE trade_tran_serial_no='%s' order by trade_id" % serial_no
    trade = gc.REPAY_DB.query(sql)
    return trade


def get_trade_tran(**kwargs):
    sql = "select * from trade_tran where %s order by trade_tran_id" % generate_sql(kwargs, "and")
    trade_tran_list = gc.REPAY_DB.do_sql(sql)
    return trade_tran_list


def get_trade_tran_by_trade_no(trade_no):
    sql = "SELECT * FROM trade_tran where trade_tran_trade_no in(select trade_no from trade WHERE trade_ref_no='%s')" % trade_no
    trade_tran = gc.REPAY_DB.query(sql)
    return trade_tran


def get_task_list_by_item_no(item_no):
    sql = "select * from task where task_order_no='%s' order by task_id desc" % item_no
    task_list = gc.REPAY_DB.query(sql)
    return task_list


def get_task_by_order_no_and_task_type(order_no, task_type, task_status=None):
    """
    获取指定task内容，默认获取到最新的一个task
    :return:
    """
    if task_status:
        sql = "select * from task where task_order_no='%s' and task_type='%s' and task_status='%s' order by task_id " \
              "desc" % (order_no, task_type, task_status)
    else:
        sql = "select * from task where task_order_no='%s' and task_type='%s' order by task_id desc" % (
            order_no, task_type)
    task_list = gc.REPAY_DB.query(sql)
    return task_list


def update_asset_and_asset_tran_due_at_by_item_no(**kwargs):
    # 将资产改为逾期，应该是指定具体的某一期，逾期多少天，其他的期次按照指定的期次，来调整时间
    # 海外可以按照这个方式来调整，因为类型都是day
    grant_delay_month = kwargs["advance_month"] if "advance_month" in kwargs else 0
    grant_delay_day = kwargs["advance_day"] if "advance_day" in kwargs else 0
    period = kwargs["period"] if "period" in kwargs else 1
    item_no = kwargs["item_no"]
    extend_list = get_asset_extend(asset_extend_asset_item_no=item_no, asset_extend_type="ref_order_no")
    item_no_x = "xxx"
    if extend_list is not None and len(extend_list) > 0:
        item_no_x = extend_list[0]["asset_extend_val"]
    asset_info = get_asset_info_by_item_no(item_no)
    asset_tran = get_asset_tran(asset_tran_asset_item_no=item_no,
                                asset_tran_type="repayprincipal",
                                asset_tran_period=period)
    asset_grant_at = asset_info[0]["asset_actual_grant_at"]
    asset_due_at = asset_info[0]["asset_due_at"]
    due_at = asset_tran[0]["asset_tran_due_at"]
    # 先算出逾期天数
    due_day = (datetime.strptime(get_date(month=grant_delay_month, day=grant_delay_day,
                                          timezone=get_tz(gc.COUNTRY)), "%Y-%m-%d %H:%M:%S") -
               datetime.strptime(due_at, "%Y-%m-%d %H:%M:%S")).days
    # 用逾期天数，倒推放款时间
    sql1 = 'update asset set asset_grant_at = "{0}", asset_effect_at = "{0}", ' \
           'asset_actual_grant_at = "{0}", asset_due_at = "{1}" ' \
           'where asset_item_no in ("{2}", "{3}")'. \
        format(get_date_by_old_date(asset_grant_at, "%Y-%m-%d %H:%M:%S", day=due_day),
               get_date_by_old_date(asset_due_at, "%Y-%m-%d %H:%M:%S", day=due_day),
               item_no, item_no_x)
    gc.REPAY_DB.update(sql1)
    # 修改asset_tran逾期时间，由于海外都是7天，只需要按天倒推
    sql2 = "update `asset_tran` set `asset_tran_due_at`=DATE_SUB" \
           "(`asset_tran_due_at`, interval %s day) where " \
           "`asset_tran_asset_item_no` in ('%s', '%s')" % \
           (-due_day, item_no, item_no_x)
    gc.REPAY_DB.update(sql2)
    # 修改asset_tran_log时间
    sql3 = "update asset_tran_log set asset_tran_log_create_at=DATE_SUB(asset_tran_log_create_at, INTERVAL %s day) " \
           "where asset_tran_log_asset_item_no in ('%s', '%s')" % (-due_day, item_no, item_no_x)
    gc.REPAY_DB.update(sql3)
    # 修改asset_delay时间
    sql4 = "update asset_delay set asset_delay_start_at=DATE_SUB(`asset_delay_start_at`, interval %s day), " \
           "asset_delay_end_at=DATE_SUB(`asset_delay_end_at`, interval %s day) " \
           "where asset_delay_item_no in ('%s', '%s') and asset_delay_status='success'" % \
           (-due_day, -due_day, item_no, item_no_x)
    gc.REPAY_DB.update(sql4)


def update_last_task_by_item_no_task_type(item_no, task_types, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update task set %s where task_order_no='%s' and task_type='%s' order by task_id desc limit 1" \
          % (sql_params[:-2], item_no, task_types)
    gc.REPAY_DB.update(sql)


def update_asset_to_payoff_by_date():
    # 将今天之前的资产状态改为payoff
    sql = "UPDATE asset SET asset_status='payoff' WHERE asset_create_at < date_sub(now(),interval 7 day)"
    gc.REPAY_DB.update(sql)


def update_asset_tran_status_by_item_no_and_type(item_no):
    sql = "update asset_tran set asset_tran_status='finish',asset_tran_balance_amount=0," \
          "asset_tran_repaid_amount=asset_tran_amount where asset_tran_asset_item_no='%s' and asset_tran_type not " \
          "in('repayprincipal')" % item_no
    gc.REPAY_DB.update(sql)


def update_withhold(serial_no, **kwargs):
    sql = "update withhold set %s where withhold_serial_no='%s'" % (generate_sql(kwargs, ","), serial_no)
    gc.REPAY_DB.do_sql(sql)


def update_withhold_detail(serial_no, **kwargs):
    sql = "update withhold_detail set %s where withhold_detail_serial_no='%s'" % (generate_sql(kwargs, ","), serial_no)
    gc.REPAY_DB.do_sql(sql)


def get_task_by_item_no_and_task_type(item_no, task_type, num=None):
    """
    获取指定task内容，默认获取到最新的一个task
    :param item_no: 资产编号
    :param task_type: task类型
    :param num: 同名task可能有多个，指定获取第几个
    :return:
    """
    sql = "select * from task where task_order_no='%s' order by task_id asc" % item_no
    task_list = gc.REPAY_DB.query(sql)
    ret = None
    for task in task_list:
        if task["task_type"] == task_type:
            ret = deepcopy(task)
            if not num:
                continue
            elif num == 1:
                break
            else:
                num = num - 1
    return ret


def get_sendmsg_list_by_order_no_and_type(msg_no, msg_type):
    sql = "select * from sendmsg where sendmsg_order_no='{0}' and sendmsg_type='{1}' order by sendmsg_id desc".format(
        msg_no, msg_type)
    task_list = gc.REPAY_DB.query(sql)
    return task_list


def get_asset_tran_balance_amount_by_item_no(item_no, period=1, asset_tran_type=None):
    if asset_tran_type is None:
        sql = 'select sum(asset_tran_balance_amount) as amount from asset_tran where asset_tran_asset_item_no="{}" and asset_tran_period={}'.format(
            item_no, period)
    else:
        sql = 'select asset_tran_balance_amount as amount from asset_tran where asset_tran_type="{}" and asset_tran_asset_item_no="{}" and asset_tran_period={}'.format(
            asset_tran_type, item_no, period)
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran[0]["amount"]


def get_withhold_lock_by_item_no(item_no):
    sql = "SELECT * FROM withhold_asset_detail_lock WHERE withhold_asset_detail_lock_asset_item_no='%s' ORDER BY " \
          "withhold_asset_detail_lock_id" % item_no
    withhold_lock = gc.REPAY_DB.query(sql)
    return withhold_lock


def get_asset_lock_by_item_no(item_no):
    sql = "SELECT * FROM asset_operation_auth WHERE asset_operation_auth_asset_item_no='%s' ORDER BY " \
          "asset_operation_auth_id" % item_no
    withhold_lock = gc.REPAY_DB.query(sql)
    return withhold_lock


def get_provision(**kwargs):
    sql = "select * from provision where %s" % generate_sql(kwargs, "and")
    provision_list = gc.REPAY_DB.do_sql(sql)
    return provision_list


def delete_provision(**kwargs):
    sql = "delete from provision where %s" % generate_sql(kwargs, "and")
    gc.REPAY_DB.do_sql(sql)


def get_refund_request(**kwargs):
    sql = "select * from refund_request where %s order by refund_request_id" % generate_sql(kwargs, "and")
    refund_request_list = gc.REPAY_DB.do_sql(sql)
    return refund_request_list


def get_refund_result(**kwargs):
    sql = "select * from refund_result where %s order by refund_result_id" % generate_sql(kwargs, "and")
    refund_result_list = gc.REPAY_DB.do_sql(sql)
    return refund_result_list


def get_withdraw(**kwargs):
    sql = "select * from withdraw where %s order by withdraw_id" % generate_sql(kwargs, "and")
    withdraw_list = gc.REPAY_DB.do_sql(sql)
    return withdraw_list


def delete_asset_late_fee_refresh_log(**kwargs):
    sql = "delete from asset_late_fee_refresh_log where %s" % generate_sql(kwargs, "and")
    gc.REPAY_DB.do_sql(sql)


def insert_account_statement_record(amount, trade_date=None, side_account_number=None):
    if trade_date is None or len(trade_date) == 0:
        trade_date = get_date(timezone=get_tz(gc.COUNTRY))
    if side_account_number is None or len(side_account_number) == 0:
        side_account_number = "enc_03_3199140098017331200_347"
    payment_card_num = get_timestamp_by_now(length=10)
    sql = "INSERT INTO `account_statement_record` (" \
          "`account_statement_record_trade_id`, `account_statement_record_trade_date`, " \
          "`account_statement_record_account_number`, `account_statement_record_side_account_number`, " \
          "`account_statement_record_in_amount`, `account_statement_record_currency`, " \
          "`account_statement_record_status`, `account_statement_record_payment_card_number`, " \
          "`account_statement_record_check_row`) VALUES (" \
          "%s, '%s', 'enc_03_1031430_346', '%s', %s, 'CNY', " \
          "'init', '%s', '8069f70015d8e8e289ab1f%s');" % \
          (payment_card_num, trade_date, side_account_number, amount, payment_card_num, payment_card_num)
    gc.REPAY_DB.do_sql(sql)
    return payment_card_num


def insert_account_statement_record_for_india(amount, trade_date=None, side_account_number=None):
    if trade_date is None or len(trade_date) == 0:
        trade_date = get_date(timezone=get_tz(gc.COUNTRY))
    if side_account_number is None or len(side_account_number) == 0:
        side_account_number = "enc_03_3199140098017331200_347"

    sql = "INSERT INTO `account_statement_record` (`account_statement_record_trade_id`, " \
          "`account_statement_record_trade_date`, `account_statement_record_account_number`, " \
          "`account_statement_record_side_account_number`, `account_statement_record_in_amount`, " \
          "`account_statement_record_status`) VALUES " \
          "('885379516555', '%s', '6213941307516331', '3797200779999', '%s', 'init')" % \
          (trade_date, amount)

    payment_card_num = get_timestamp_by_now(length=10)
    sql = "INSERT INTO `account_statement_record` (" \
          "`account_statement_record_trade_id`, `account_statement_record_trade_date`, " \
          "`account_statement_record_account_number`, `account_statement_record_side_account_number`, " \
          "`account_statement_record_in_amount`, `account_statement_record_currency`, " \
          "`account_statement_record_status`, `account_statement_record_payment_card_number`, " \
          "`account_statement_record_check_row`) VALUES (" \
          "%s, '%s', 'enc_03_1031430_346', '%s', %s, 'CNY', " \
          "'init', '%s', '8069f70015d8e8e289ab1f%s');" % \
          (payment_card_num, trade_date, side_account_number, amount, payment_card_num, payment_card_num)
    gc.REPAY_DB.do_sql(sql)
    return payment_card_num


def update_account_statement_record(trade_id, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + key + "='" + str(value) + "', "
    sql = "update account_statement_record set %s where account_statement_record_trade_id='%s'" % (sql_params[:-2], trade_id)
    gc.REPAY_DB.do_sql(sql)


def earease_amount(withhold_amount):
    return withhold_amount - withhold_amount // 1000 * 1000
