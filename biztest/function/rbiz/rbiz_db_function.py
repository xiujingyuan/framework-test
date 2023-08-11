from biztest.util.tools.tools import *
import common.global_const as gc


def get_asset_info_by_item_no(item_no):
    sql = "select * from asset where asset_item_no='%s'" % item_no
    asset_info = gc.REPAY_DB.query(sql)
    return asset_info


def update_asset_due_bill_no(item_no):
    sql = "update  asset  set asset_due_bill_no='DNB20211635737687' where asset_item_no='%s'" % item_no
    asset_info = gc.REPAY_DB.update(sql)
    return asset_info


def get_asset_extend_val_by_item_no(item_no, extend_type='ref_order_no'):
    sql = "select * from asset_extend where asset_extend_asset_item_no='%s' and asset_extend_type='%s'" % (
        item_no, extend_type)
    asset_extend_info = gc.REPAY_DB.query(sql)
    return asset_extend_info


def get_repay_card_by_item_no(item_no):
    sql = "SELECT card.* FROM card_asset INNER JOIN card ON card_no=card_asset_card_no WHERE " \
          "card_asset_asset_item_no='%s' AND card_asset_type='repay'" % item_no
    card_info = gc.REPAY_DB.query(sql)
    return card_info


def get_capital_asset_by_item_no(item_no):
    sql = "select * from capital_asset where capital_asset_item_no='%s'" % item_no
    capital_asset = gc.REPAY_DB.query(sql)
    return capital_asset


def get_capital_asset_tran_by_item_no(item_no):
    sql = "select * from capital_transaction where capital_transaction_item_no='%s'" % item_no
    capital_transaction = gc.REPAY_DB.query(sql)
    return capital_transaction


def get_capital_notify_by_asset_item_no(item_no):
    sql = 'select * from capital_notify where capital_notify_asset_item_no="{}"'.format(item_no)
    capital_notify = gc.REPAY_DB.query(sql)
    return capital_notify


def get_task_info_by_task_id(task_id):
    sql = 'select * from task where task_id={}'.format(task_id)
    task = gc.REPAY_DB.query(sql)
    return task


def get_sendmsg_info_by_order_no_and_type(order_no, type):
    sql = 'select * from sendmsg where sendmsg_order_no="{}" and sendmsg_type="{}"'.format(order_no, type)
    task = gc.REPAY_DB.query(sql)
    return task


def update_capital_notify_plan_at_by_item_no(item_no):
    sql = "update capital_notify set capital_notify_plan_at='%s' where capital_notify_asset_item_no='%s'" % (
        get_date_before_today(day=1), item_no)
    gc.REPAY_DB.update(sql)


def update_asset_loan_channel(item_no, loan_channel):
    sql = 'UPDATE asset SET asset_loan_channel="{}"  WHERE asset_item_no="{}"'.format(
        loan_channel, item_no)
    gc.REPAY_DB.do_sql(sql)


def update_asset_status_all():
    sql = "update asset set asset_status='payoff'"
    gc.REPAY_DB.update(sql)


def update_asset_tran_status_by_item_no_and_period(item_no, period=12):
    sql = "update asset_tran set asset_tran_status='finish',asset_tran_balance_amount=0," \
          "asset_tran_repaid_amount=asset_tran_amount where asset_tran_asset_item_no='%s' and asset_tran_period not " \
          "in(%s)" % (item_no, period)
    gc.REPAY_DB.update(sql)


def update_before_asset_tran_finish_by_item_no_and_period(item_no, period):
    sql = "update asset_tran set asset_tran_status='finish',asset_tran_balance_amount=0," \
          "asset_tran_repaid_amount=asset_tran_amount where asset_tran_asset_item_no='{0}' " \
          "and asset_tran_period < {1}".format(item_no, period)
    gc.REPAY_DB.update(sql)


def get_asset_tran_by_item_no(item_no):
    sql = "SELECT * FROM asset_tran WHERE asset_tran_asset_item_no='%s' ORDER BY asset_tran_period" % item_no
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran


def get_asset_tran_by_item_no_and_type(item_no, tran_type):
    sql = "SELECT * FROM asset_tran WHERE asset_tran_asset_item_no='{}' and asset_tran_type='{}' ORDER BY " \
          "asset_tran_period".format(item_no, tran_type)
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran


def get_asset_tran_by_item_no_and_type_and_period(item_no, tran_type, period):
    sql = "SELECT * FROM asset_tran WHERE asset_tran_asset_item_no='{}' and asset_tran_type='{}' and " \
          "asset_tran_period='{}'".format(item_no, tran_type, period)
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran


def get_asset_tran_by_tran_no(tran_no):
    sql = "SELECT * FROM asset_tran WHERE asset_tran_no='%s' ORDER BY asset_tran_period" % tran_no
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran


def get_asset_tran_balance_amount_by_item_no_and_period(item_no, tran_period=None, before_tran_period=None):
    sql = "SELECT sum(asset_tran_amount) as asset_tran_amount,sum(asset_tran_balance_amount) as " \
          "asset_tran_balance_amount FROM asset_tran WHERE asset_tran_asset_item_no='{}'".format(item_no)
    if tran_period:
        sql = sql + " and asset_tran_period={}".format(tran_period)
    if before_tran_period:
        sql = sql + " and asset_tran_period<={}".format(before_tran_period)
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran[0]


def get_asset_tran_balance_amount_by_item_no_and_type(item_no, tran_type=None, tran_period=None):
    sql = "SELECT sum(asset_tran_amount) as asset_tran_amount,sum(asset_tran_balance_amount) as " \
          "asset_tran_balance_amount FROM asset_tran WHERE asset_tran_asset_item_no='{}' and asset_tran_type='{}'".format(
        item_no, tran_type)
    if tran_period:
        sql = "SELECT sum(asset_tran_amount) as asset_tran_amount,sum(asset_tran_balance_amount) as " \
              "asset_tran_balance_amount FROM asset_tran WHERE asset_tran_asset_item_no='{}' and asset_tran_type='{}' " \
              "and asset_tran_period={}".format(item_no, tran_type, tran_period)
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran[0]


def get_finish_asset_tran_by_item_no(item_no):
    sql = "SELECT * FROM asset_tran WHERE asset_tran_asset_item_no='%s' and asset_tran_status='finish' ORDER BY " \
          "asset_tran_period" % item_no
    asset_tran = gc.REPAY_DB.query(sql)
    return asset_tran


def get_asset_tran_log_by_item_no(item_no):
    sql = "SELECT * FROM asset_tran_log WHERE asset_tran_log_asset_item_no='%s' ORDER BY asset_tran_log_id DESC" % item_no
    asset_tran_log = gc.REPAY_DB.query(sql)
    return asset_tran_log


def get_withhold_by_item_no(item_no):
    sql = "SELECT * FROM withhold WHERE withhold_serial_no IN (SELECT withhold_order_serial_no FROM withhold_order " \
          "WHERE withhold_order_reference_no ='%s') and withhold_status not in('fail','cancel') order by withhold_order" % item_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_order_by_item_no(item_no):
    sql = "SELECT *  FROM withhold_order WHERE withhold_order_reference_no ='%s' order by withhold_order_id desc" % item_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_detail_by_item_no(item_no):
    sql = "SELECT *  FROM withhold_detail WHERE withhold_detail_asset_item_no ='%s' order by withhold_detail_id desc " % item_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_request_by_item_no(item_no):
    sql = "SELECT * FROM withhold_request WHERE withhold_request_no IN (SELECT withhold_order_request_no FROM " \
          "withhold_order WHERE withhold_order_reference_no ='%s') order by withhold_request_id desc" % item_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_request_by_request_no(request_no):
    sql = "SELECT * FROM withhold_request WHERE withhold_request_no ='%s'" % request_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_data_by_request_no(request_no):
    sql = "SELECT * FROM withhold WHERE withhold_request_no='%s' order by withhold_order" % request_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_order_by_request_no(request_no):
    sql = "SELECT *  FROM withhold_order WHERE withhold_order_request_no ='%s' order by withhold_order_id desc" % (
        request_no)
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_by_item_no_and_request_no(item_no, request_no):
    sql = "SELECT * FROM withhold WHERE withhold_request_no='%s' and withhold_serial_no IN (SELECT " \
          "withhold_order_serial_no FROM withhold_order WHERE withhold_order_reference_no ='%s') order by " \
          "withhold_order" % (request_no, item_no)
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_order_by_item_no_and_request_no(item_no, request_no):
    sql = "SELECT *  FROM withhold_order WHERE withhold_order_request_no ='%s' and withhold_order_reference_no ='%s' " \
          "order by withhold_order_id desc" % (request_no, item_no)
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_detail_by_item_no_and_serial_no(item_no, serial_no):
    sql = "SELECT * FROM withhold_detail WHERE withhold_detail_serial_no ='%s' and withhold_detail_asset_item_no = " \
          "'%s'order by withhold_detail_id desc" % (serial_no, item_no)
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_detail_by_item_no_and_serial_no_extend(item_no, serial_no):
    sql = "SELECT withhold_detail_create_at, withhold_detail_period, withhold_detail_asset_tran_type, " \
          "withhold_detail_withhold_amount FROM withhold_detail WHERE withhold_detail_serial_no ='{0}' " \
          "and withhold_detail_asset_item_no = '{1}' order by withhold_detail_id".format(serial_no, item_no)
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_by_serial_no(serial_no):
    sql = "SELECT * FROM withhold WHERE withhold_serial_no ='%s' order by withhold_order" % serial_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_by_channel_key(channel_key):
    sql = "SELECT * FROM withhold WHERE withhold_channel_key ='%s' order by withhold_order" % channel_key
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_order_by_serial_no(serial_no):
    sql = "SELECT *  FROM withhold_order WHERE withhold_order_serial_no ='%s' order by withhold_order_id desc" % serial_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_detail_by_serial_no(serial_no):
    sql = "SELECT * FROM withhold_detail WHERE withhold_detail_serial_no ='%s' order by withhold_detail_id desc" % serial_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_withhold_request_by_serial_no(serial_no):
    sql = "SELECT * FROM withhold_request WHERE withhold_request_no IN (SELECT withhold_request_no FROM " \
          "withhold WHERE withhold_serial_no ='%s') order by withhold_request_id desc" % serial_no
    withhold = gc.REPAY_DB.query(sql)
    return withhold


def get_account_recharge_by_channel_key(channel_key):
    sql = "select * from account_recharge where account_recharge_serial_no='%s' order by account_recharge_id" % channel_key
    recharge = gc.REPAY_DB.query(sql)
    return recharge


def get_account_recharge_log_by_channel_key(channel_key):
    sql = 'select * from account_recharge_log where account_recharge_log_recharge_serial_no="{}" order by ' \
          'account_recharge_log_id'.format(channel_key)
    recharge_Log = gc.REPAY_DB.query(sql)
    return recharge_Log


def get_account_repay_by_channel_key(channel_key):
    sql = 'select * from account_repay where account_repay_recharge_serial_no="{}" order by account_repay_id'.format(
        channel_key)
    account_repay = gc.REPAY_DB.query(sql)
    return account_repay


def get_account_repay_log_by_chanel_key(channel_key):
    sql = 'select * from account_repay_log where account_repay_log_repay_no in (select account_repay_no from ' \
          'account_repay where account_repay_recharge_serial_no="{}") order by account_repay_log_id'.format(channel_key)
    account_repay_log = gc.REPAY_DB.query(sql)
    return account_repay_log


def get_account_by_id_num(id_num):
    sql = 'select * from account where account_user_id_num_encrypt="{}"'.format(id_num)
    account = gc.REPAY_DB.query(sql)
    return account


def get_trade_by_trade_no(trade_no):
    sql = "SELECT * FROM trade WHERE trade_ref_no='%s'" % trade_no
    trade = gc.REPAY_DB.query(sql)
    return trade


def get_trade_tran_by_trade_no(trade_no):
    sql = "SELECT * FROM trade_tran where trade_tran_trade_no in(select trade_no from trade WHERE trade_ref_no='%s')" % trade_no
    trade_tran = gc.REPAY_DB.query(sql)
    return trade_tran


def get_task_list_by_item_no(item_no):
    sql = "select * from task where task_order_no='%s' order by task_id desc" % item_no
    task_list = gc.REPAY_DB.query(sql)
    return task_list


def get_card_bind_by_card_number(card_number, card_bind_serial_no):
    sql = "SELECT * FROM card_bind WHERE card_bind_card_num_encrypt='%s' and card_bind_serial_no='%s'order by card_bind_id desc" % (
        card_number, card_bind_serial_no)
    task_list = gc.REPAY_DB.query(sql)
    return task_list


def update_card_bind_update_at_by_card_number(card_number, new_date=get_date_before_today(month=1)):
    sql = "update card_bind set card_bind_update_at='%s',card_bind_create_at='%s' WHERE card_bind_card_num_encrypt='%s' " % (
        new_date, new_date, card_number)
    gc.REPAY_DB.update(sql)


def update_last_task_by_item_no_task_type(item_no, task_types, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update task set %s where task_order_no='%s' and task_type='%s' order by task_id desc limit 1" \
          % (sql_params[:-2], item_no, task_types)
    gc.REPAY_DB.update(sql)


def wait_expect_task_appear(item_no, task_type, wait_time=120):
    result = False
    for i in range(wait_time):
        task = get_task_by_order_no_and_task_type(item_no, task_type)
        if task is not None and len(task) > 0:
            result = True
            break
        else:
            time.sleep(1)
    return result


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


def get_sendmsg_list_by_order_no_and_type(msg_no, msg_type):
    sql = "select * from sendmsg where sendmsg_order_no='{0}' and sendmsg_type='{1}' order by sendmsg_id desc".format(
        msg_no, msg_type)
    task_list = gc.REPAY_DB.query(sql)
    return task_list


def get_card_info_by_item_no(item_no):
    sql = "SELECT * FROM card WHERE card_no IN(SELECT card_asset_card_no FROM card_asset WHERE " \
          "card_asset_asset_item_no ='%s');" % item_no
    card = gc.REPAY_DB.query(sql)
    return card


def get_card_info_by_card_num(card_num):
    sql = "SELECT * FROM card WHERE card_acc_num_encrypt ='%s' order by card_id asc" % card_num
    card = gc.REPAY_DB.query(sql)
    return card


def get_card_info_by_card_no(card_no):
    sql = "SELECT * FROM card WHERE card_no ='%s'" % card_no
    card = gc.REPAY_DB.query(sql)
    return card


def get_withhold_card_by_card_num(card_no):
    sql = "SELECT * FROM withhold_card WHERE withhold_card_card_no in (SELECT card_no FROM card WHERE " \
          "card_acc_num_encrypt ='%s')" % card_no
    card = gc.REPAY_DB.query(sql)
    return card


def get_withhold_card_by_individual_no(individual_no):
    sql = "SELECT * FROM withhold_card WHERE withhold_card_individual_no ='%s'" % individual_no
    card = gc.REPAY_DB.query(sql)
    return card


def get_individual_info_by_item_no(item_no):
    sql = "SELECT * FROM individual WHERE individual_no IN(SELECT individual_asset_individual_no FROM " \
          "individual_asset WHERE individual_asset_asset_item_no='%s');" % item_no
    individual = gc.REPAY_DB.query(sql)
    return individual


def get_individual_info_by_id_num(id_num):
    sql = "SELECT * FROM individual WHERE individual_id_num_encrypt='%s'" % id_num
    individual = gc.REPAY_DB.query(sql)
    return individual


def get_qinnong_reserve_amount(item_no, start, end):
    if start == 0:
        sql_start = "select DATE_FORMAT(asset_actual_grant_at, '%%Y-%%m-%%d 00:00:00') as date " \
                    "from asset where asset_item_no='%s'" % item_no
    else:
        sql_start = "select asset_tran_due_at as date from asset_tran where asset_tran_asset_item_no='%s' " \
                    "and asset_tran_period='%s' and asset_tran_type='repayprincipal'" % (item_no, start)
    start_day = datetime.strptime(gc.REPAY_DB.do_sql(sql_start)[0]["date"], "%Y-%m-%d %H:%M:%S")
    sql_end = "select asset_tran_due_at from asset_tran where asset_tran_asset_item_no='%s' " \
              "and asset_tran_period='%s' and asset_tran_type='repayprincipal'" % (item_no, end)
    end_day = datetime.strptime(gc.REPAY_DB.do_sql(sql_end)[0]["asset_tran_due_at"], "%Y-%m-%d %H:%M:%S")
    sql_amount = "select sum(asset_tran_amount) as amount from asset_tran where asset_tran_asset_item_no='%s' " \
                 "and asset_tran_period='%s' and asset_tran_type in ('reserve', 'consult')" % (item_no, end)
    amount_all = gc.REPAY_DB.do_sql(sql_amount)[0]["amount"]
    day_all = (end_day - start_day).days
    stand_day = (datetime.strptime(get_date(fmt="%Y-%m-%d 00:00:00"), "%Y-%m-%d %H:%M:%S") - start_day).days
    return round(int(amount_all) * stand_day / day_all)



def get_zhongbang_zhongji_capital_fee_amount(item_no, end_period):
    '''
    仅适用于众邦中际、蒙商中裔
    当期部分费（算法：实际占用天数/当期总天数 x 当期费用总金额(四舍五入保留2位小数) ）
    '''
    start_day_sql = "select DATE_FORMAT(asset_actual_grant_at, '%%Y-%%m-%%d 00:00:00') as date " \
                "from asset where asset_item_no='%s'" % item_no
    start_day = datetime.strptime(gc.REPAY_DB.do_sql(start_day_sql)[0]["date"], "%Y-%m-%d %H:%M:%S")
    period_due_at = "select asset_tran_due_at from asset_tran where asset_tran_asset_item_no='%s' " \
              "and asset_tran_period='%s' and asset_tran_type='repayprincipal'" % (item_no, end_period)
    end_day = datetime.strptime(gc.REPAY_DB.do_sql(period_due_at)[0]["asset_tran_due_at"], "%Y-%m-%d %H:%M:%S")
    sql_amount = "select sum(asset_tran_amount) as amount from asset_tran where asset_tran_asset_item_no='%s' " \
                 "and asset_tran_period='%s' and asset_tran_type in ('consult', 'reserve')" % (item_no, end_period)
    amount_all = gc.REPAY_DB.do_sql(sql_amount)[0]["amount"]
    capital_use_day = (end_day - start_day).days  # 资金方实际占用天数
    # 当期总天数
    all_day = (datetime.strptime(get_date(fmt="%Y-%m-%d 00:00:00"), "%Y-%m-%d %H:%M:%S") - start_day).days
    return round(capital_use_day/all_day * int(amount_all))


def get_capital_part_fee_amount(item_no, end_period, fee_type):
    '''
    适用于所有资金方
    当期部分费（算法：实际占用天数/当期总天数 x 当期费用总金额(四舍五入保留2位小数) ）
    '''
    start_day_sql = "select DATE_FORMAT(asset_actual_grant_at, '%%Y-%%m-%%d 00:00:00') as date " \
                "from asset where asset_item_no='%s'" % item_no
    start_day = datetime.strptime(gc.REPAY_DB.do_sql(start_day_sql)[0]["date"], "%Y-%m-%d %H:%M:%S")
    period_due_at = "select asset_tran_due_at from asset_tran where asset_tran_asset_item_no='%s' " \
              "and asset_tran_period='%s' and asset_tran_type='repayprincipal'" % (item_no, end_period)
    end_day = datetime.strptime(gc.REPAY_DB.do_sql(period_due_at)[0]["asset_tran_due_at"], "%Y-%m-%d %H:%M:%S")
    sql_amount = "select sum(asset_tran_amount) as amount from asset_tran where asset_tran_asset_item_no='%s' " \
                 "and asset_tran_period='%s' and asset_tran_type in ('%s')" % (item_no, end_period, fee_type)
    amount_all = gc.REPAY_DB.do_sql(sql_amount)[0]["amount"]
    capital_use_day = (end_day - start_day).days  # 资金方实际占用天数
    # 当期总天数
    all_day = (datetime.strptime(get_date(fmt="%Y-%m-%d 00:00:00"), "%Y-%m-%d %H:%M:%S") - start_day).days
    return round(capital_use_day/all_day * int(amount_all))
