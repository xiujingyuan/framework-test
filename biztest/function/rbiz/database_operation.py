# -*- coding: utf-8 -*-
from biztest.util.log.log_util import LogUtil
from biztest.util.tools.tools import *
from biztest.util.db.db_util import *
import pytest
import time


def update_database_config(db_prod_rbiz, db_test_rbiz):
    try:
        table_list = ['capital_config', 'capital_route', 'split_order_config', 'split_order_rule',
                      'split_order_rule_express', 'split_order_rule_condition']

        for table in table_list:
            sql_query_prod = "select * from repay.{}".format(table)
            select_result = db_prod_rbiz.query_mysql(sql_query_prod)

            db_test_rbiz.execute_mysql("truncate {}".format(table))

            if table == 'capital_config':
                sql_test = "insert into {} values({})".format(table, '%s,%s,%s,%s,%s,%s,%s,%s')
            elif table == 'capital_route':
                sql_test = "insert into {} values({})".format(table, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s')
            elif table == 'split_order_config':
                sql_test = "insert into {} values({})".format(table, '%s,%s,%s,%s,%s,%s,%s')
            elif table == 'split_order_rule':
                sql_test = "insert into {} values({})".format(table, '%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s')
            elif table == 'split_order_rule_express':
                sql_test = "insert into {} values({})".format(table, '%s,%s,%s,%s,%s,%s,%s')
            elif table == 'split_order_rule_condition':
                sql_test = "insert into {} values({})".format(table, '%s,%s,%s,%s,%s,%s')

            db_test_rbiz.execute_mysql(sql_test, param=select_result)
    except Exception as e:
        raise Exception("同步rbiz测试环境数据库配置失败")


def get_four_element_from_db(db_test_rbiz, id_number_encrypt='enc_02_4873960_571',
                             user_name_encrypt='enc_04_3605630_858', phone_number_encrypt='enc_01_4873980_363',
                             bank_code_encrypt='enc_03_4873970_028'):
    try:
        sql = "SELECT  {} AS id_number_encrypt,{} AS user_name_encrypt,{} AS phone_number_encrypt,{} AS bank_code_encrypt FROM card LIMIT 1".format(
            id_number_encrypt,
            user_name_encrypt,
            phone_number_encrypt,
            bank_code_encrypt)
        result = db_test_rbiz.query(sql)
        return result
    except Exception as e:
        raise Exception("从rbiz数据库获取四要素失败")


def update_grant_or_due_day_in_rbiz(**kwargs):
    grant_day = kwargs.get("grant_day", None)
    due_day = kwargs.get('due_day', None)
    count = kwargs.get('count', None)
    item_no = kwargs.get('item_no', None)
    db_test_rbiz = kwargs.get('db_test_rbiz', None)
    try:
        if grant_day:
            sql_update_grant_day = 'update asset set asset_grant_at="{0}",asset_actual_grant_at="{0}" where asset_item_no="{1}"'.format(
                grant_day, item_no)
            sql_get_grant_day = f'select asset_grant_at from asset where asset_item_no="{item_no}"'
            for x in range(0, 100):
                db_test_rbiz.execute_mysql(sql_update_grant_day)
                grant_day_actual = str(db_test_rbiz.query_mysql(sql_get_grant_day)[0][0])
                if grant_day == grant_day_actual:
                    break
            grant_day_actual = str(db_test_rbiz.query_mysql(sql_get_grant_day)[0][0])
            if grant_day_actual != grant_day:
                raise Exception(f"{item_no}修改rbiz放款时间失败,grant_day={grant_day},grant_day_actual={grant_day_actual}")
        if due_day:
            sql_update_due_day = 'update asset_tran set asset_tran_due_at="{}" where asset_tran_asset_item_no="{}" and asset_tran_period<={}'.format(
                due_day, item_no, count)
            sql_get_due_day = f'select asset_tran_due_at from asset_tran where asset_tran_asset_item_no="{item_no}" and asset_tran_period={count}'
            for x in range(0, 100):
                db_test_rbiz.execute_mysql(sql_update_due_day)
                due_day_actual = str(db_test_rbiz.query_mysql(sql_get_due_day)[0][0])
                if due_day_actual == due_day:
                    break
            due_day_actual = str(db_test_rbiz.query_mysql(sql_get_due_day)[0][0])
            if due_day_actual != due_day:
                raise Exception(f"{item_no}修改rbiz还款到期日失败,due_day={due_day},due_day_actual={due_day_actual}")
    except Exception as e:
        raise Exception(f"更改资产还款日期和放款日期失败:{e}")


def update_due_day_in_biz(**kwargs):
    due_day = kwargs.get('due_day', None)
    count = kwargs.get('count', None)
    item_no = kwargs.get('item_no', None)
    db_test_biz = kwargs.get('db_test_biz', None)
    try:
        sql_update_dran_due_day = 'UPDATE dtransaction SET dtransaction_expect_finish_time="{}"  WHERE `dtransaction_asset_id` IN(SELECT asset_id FROM asset WHERE `asset_item_no` IN ("{}")) AND dtransaction_period<={} AND dtransaction_type <> "grant"'.format(
            due_day, item_no, count)
        sql_update_fran_due_day = 'UPDATE ftransaction SET ftransaction_expect_finish_time="{}"  WHERE `ftransaction_asset_id` IN(SELECT asset_id FROM asset WHERE `asset_item_no` IN ("{}")) AND ftransaction_period<={}'.format(
            due_day, item_no, count)
        db_test_biz.execute_mysql(sql_update_dran_due_day)
        db_test_biz.execute_mysql(sql_update_fran_due_day)
    except Exception as e:
        raise Exception(f"更改资产还款日期和放款日期失败:{e}")


def update_asset_loan_channel_in_rbiz(**kwargs):
    item_no = kwargs.get('item_no', None)
    loan_channel = kwargs.get('loan_channel', None)
    db_test_rbiz = kwargs.get('db_test_rbiz', None)
    try:
        sql_update_loan_channel = 'UPDATE asset SET asset_loan_channel="{}"  WHERE asset_item_no="{}"'.format(
            loan_channel, item_no)
        db_test_rbiz.execute_mysql(sql_update_loan_channel)
    except Exception as e:
        raise Exception(f"更改asset_loan_channel失败:{e}")


def update_asset_extend_source_type_in_rbiz(**kwargs):
    item_no = kwargs.get('item_no', None)
    source_type = kwargs.get('source_type', None)
    db_test_rbiz = kwargs.get('db_test_rbiz', None)
    try:
        sql_update_source_type = 'UPDATE asset_extend SET asset_extend_val="{}"  WHERE asset_extend_asset_item_no="{' \
                                 '}" and asset_extend_type="ref_order_type"'.format(
            source_type, item_no)
        db_test_rbiz.execute_mysql(sql_update_source_type)
    except Exception as e:
        raise Exception(f"update_asset_extend_source_type_in_rbiz失败:{e}")


def update_withhold_create_at_by_serial_no_in_rbiz(**kwargs):
    serial_no = kwargs.get('serial_no', None)
    db_test_rbiz = kwargs.get('db_test_rbiz', None)
    try:
        sql_update_withhold_create_at = 'UPDATE withhold SET withhold_create_at= "{}" WHERE ' \
                                        'withhold_serial_no="{}"'.format(get_date_before_today(day=1), serial_no)
        db_test_rbiz.execute_mysql(sql_update_withhold_create_at)
    except Exception as e:
        raise Exception(f"update_withhold_create_at_by_serial_no_in_rbiz失败:{e}")


def update_withhold_order_operate_type_by_serial_no_in_rbiz(**kwargs):
    serial_no = kwargs.get('serial_no', None)
    db_test_rbiz = kwargs.get('db_test_rbiz', None)
    try:
        sql_update_withhold_order = 'UPDATE withhold_order SET withhold_order_operate_type="auto" WHERE ' \
                                    'withhold_order_serial_no="{}"'.format(serial_no)
        db_test_rbiz.execute_mysql(sql_update_withhold_order)
    except Exception as e:
        raise Exception(f"update_withhold_order_operate_type_by_serial_no_in_rbiz失败:{e}")


def get_request_no_by_serial_no(db, serial_no):
    try:
        sql = 'select withhold_request_no from withhold where withhold_serial_no="{}" order by withhold_create_at desc limit 1'.format(
            serial_no)
        result_list = db.query_mysql(sql)
        return result_list[0][0]
    except Exception as e:
        raise Exception("在withhold表中根据serial_no获取request_no失败")


def get_request_key_by_request_no(db, request_no):
    try:
        sql = 'select withhold_request_req_key from withhold_request where withhold_request_no="{}" limit 1'.format(
            request_no)
        result_list = db.query_mysql(sql)
        return result_list[0][0]
    except Exception as e:
        raise Exception("在withhold_request表中根据request_no获取request_key失败")


def get_serial_no_by_request_no(db, request_no):
    try:
        sql = 'select withhold_serial_no from withhold where withhold_request_no ="{}" order by withhold_order'.format(
            request_no)
        result_list = db.query_mysql(sql)
        serial_no_set = set()
        for result in result_list:
            serial_no_set.add(result[0])
        return list(serial_no_set)
    except Exception as e:
        raise Exception("在withhold表中根据request_no获取serial_no失败")


def get_card_bind_staus_by_serial_no(db, serial_no):
    try:
        sql = 'select card_bind_status from card_bind where card_bind_serial_no="{}"'.format(serial_no)
        card_bind_status = db.query_mysql(sql)[0][0]
        return card_bind_status
    except Exception as e:
        raise Exception("在card_bind表中获取状态失败")


def get_withold_request_by_request_no(db, withhold_request_no):
    sql = 'select count(*), withhold_request_amount,withhold_request_status from withhold_request where withhold_request_no="{}"'.format(
        withhold_request_no)
    result = db.query_mysql(sql)
    count, withhold_request_amount, withhold_request_status = result[0][0], result[0][1], result[0][2]
    return count, withhold_request_amount, withhold_request_status


def get_withhold_order_by_request_no(db, withhold_order_request_no):
    sql = 'select withhold_order_withhold_status from withhold_order where withhold_order_request_no="{}"'.format(
        withhold_order_request_no)
    result_list = db.query_mysql(sql)
    status_list = []
    for result in result_list:
        status_list.append(result[0])
    return status_list


def get_repaid_amount_by_asset_tran(db, item_no, period=None, asset_tran_type=None):
    if asset_tran_type is None and period:
        sql = 'select sum(asset_tran_repaid_amount) from asset_tran where asset_tran_asset_item_no="{}" and asset_tran_period={}'.format(
            item_no, period)
        amount = db.query_mysql(sql)[0][0]
    elif asset_tran_type is None and period is None:
        sql = 'select sum(asset_tran_repaid_amount) from asset_tran where asset_tran_asset_item_no="{}"'.format(
            item_no)
        amount = db.query_mysql(sql)[0][0]
    elif asset_tran_type and period is None:
        sql = 'select sum(asset_tran_repaid_amount) from asset_tran where asset_tran_type ="{}" and asset_tran_asset_item_no="{}"'.format(
            asset_tran_type, item_no)
        amount = db.query_mysql(sql)[0][0]
    elif asset_tran_type and period:
        sql = 'select asset_tran_repaid_amount from asset_tran where asset_tran_type="{}" and asset_tran_asset_item_no="{}" and asset_tran_period={}'.format(
            asset_tran_type, item_no, period)
        amount = db.query_mysql(sql)[0][0]
    else:
        amount = -1

    return int(amount)


def get_repaid_amount_from_asset_tran_where_asset_type_type_is_not_some_type(db, item_no, asset_tran_type, period=None):
    if period is None:
        sql = 'select sum(asset_tran_repaid_amount) from asset_tran where asset_tran_type <>"{}" and asset_tran_asset_item_no="{}"'.format(
            asset_tran_type, item_no)
        amount = db.query_mysql(sql)[0][0]
    elif period:
        sql = 'select asset_tran_repaid_amount from asset_tran where asset_tran_type<>"{}" and asset_tran_asset_item_no="{}" and asset_tran_period={}'.format(
            asset_tran_type, item_no, period)
        amount = db.query_mysql(sql)[0][0]
    else:
        amount = -1

    return int(amount)


def get_balance_amount_by_asset_tran(db, item_no, period, asset_tran_type=None):
    amount = 0
    if asset_tran_type is None:
        sql = 'select sum(asset_tran_balance_amount) from asset_tran where asset_tran_asset_item_no="{}" and asset_tran_period={}'.format(
            item_no, period)
    else:
        sql = 'select asset_tran_balance_amount from asset_tran where asset_tran_type="{}" and asset_tran_asset_item_no="{}" and asset_tran_period={}'.format(
            asset_tran_type, item_no, period)
    for x in range(0, 100):
        result = db.query_mysql(sql)
        if result:
            amount = result[0][0]
            break

    print(sql)
    if amount == 0:
        raise Exception(f"item_no={item_no}获取资产的balance_amount失败,sql={sql}")

    return int(amount)


def get_withhold_by_request_no(db, withold_requst_no):
    sql_count = 'select count(*) from withhold where withhold_request_no="{}"'.format(withold_requst_no)
    sql_withhold_info = 'select withhold_amount ,withhold_status,withhold_channel,withhold_serial_no,withhold_extend_info from withhold where withhold_request_no="{}" order by withhold_order asc'.format(
        withold_requst_no)
    count = db.query_mysql(sql_count)[0][0]
    result_list = db.query_mysql(sql_withhold_info)
    withhold_amount_list = [result[0] for result in result_list]
    withhold_status_list = [result[1] for result in result_list]
    withhold_channel_list = [result[2] for result in result_list]
    withhold_serial_no_list = [result[3] for result in result_list]
    sign_company_list = [json.loads(result[4]).get('paysvrSignCompany', None) for result in result_list if result[4]]
    return count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list


def get_global_withhold_by_request_no(db, withold_requst_no):
    sql_count = 'select count(*) from withhold where withhold_request_no="{}"'.format(withold_requst_no)
    sql_withhold_info = 'select withhold_amount ,withhold_status,withhold_channel,withhold_serial_no,withhold_extend_info,withhold_payment_mode from withhold where withhold_request_no="{}" order by withhold_order asc'.format(
        withold_requst_no)
    count = db.query_mysql(sql_count)[0][0]
    result_list = db.query_mysql(sql_withhold_info)
    withhold_amount_list = [result[0] for result in result_list]
    withhold_status_list = [result[1] for result in result_list]
    withhold_channel_list = [result[2] for result in result_list]
    withhold_serial_no_list = [result[3] for result in result_list]
    sign_company_list = [json.loads(result[4]).get('paysvrSignCompany', None) for result in result_list if result[4]]
    withhold_payment_mode = [result[5] for result in result_list]
    return count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list, withhold_payment_mode


def get_withhold_detail_by_item_no(db, item_no, period, serial_no=None):
    if serial_no:
        sql_sum_amount = 'select sum(withhold_detail_withhold_amount) from withhold_detail where withhold_detail_asset_item_no="{}" and withhold_detail_period between 0 and {} and withhold_detail_serial_no="{}"'.format(
            item_no, period, serial_no)
        sql_status = 'select withhold_detail_status from withhold_detail where withhold_detail_asset_item_no="{}" and withhold_detail_period between 0 and {} and withhold_detail_serial_no="{}"'.format(
            item_no, period, serial_no)
    else:
        sql_sum_amount = 'select sum(withhold_detail_withhold_amount) from withhold_detail where withhold_detail_asset_item_no="{}" and withhold_detail_period between 0 and {}'.format(
            item_no, period)
        sql_status = 'select withhold_detail_status from withhold_detail where withhold_detail_asset_item_no="{}" and withhold_detail_period between 0 and {}'.format(
            item_no, period)
    sum_amount = int(db.query_mysql(sql_sum_amount)[0][0])
    result_list = db.query_mysql(sql_status)
    status_list = [result[0] for result in result_list]
    return sum_amount, status_list


def get_request_no_by_item_no(db, item_no):
    sql = 'select withhold_order_request_no from withhold_order where withhold_order_reference_no="{}" order by withhold_order_create_at desc limit 1'.format(
        item_no)
    result_list = db.query_mysql(sql)
    request_no = result_list[0][0]
    return request_no


def get_request_no_by_item_no_and_capital(db, item_no, capital):
    sql = 'select withhold_order_request_no from withhold_order where withhold_order_reference_no="{0}" and withhold_order_serial_no like "{1}%" order by withhold_order_create_at desc limit 1'.format(
        item_no, capital)
    result_list = db.query_mysql(sql)
    request_no = result_list[0][0]
    return request_no


def get_channel_key_by_request_no(db, request_no):
    sql = 'select withhold_channel_key from withhold where withhold_request_no="{}"'.format(request_no)
    result_list = db.query_mysql(sql)
    channel_key_list = [result[0] for result in result_list]
    return channel_key_list


def get_withhold_amount_by_channel_key(db, channel_key):
    sql = 'select withhold_amount from withhold where withhold_channel_key="{}"'.format(channel_key)
    result_list = db.query_mysql(sql)
    withhold_amount = int(result_list[0][0])
    return withhold_amount


def get_recharge_amount_by_channel_key(db, channel_key):
    sql = 'select account_recharge_amount from account_recharge where account_recharge_serial_no="{}"'.format(
        channel_key)
    result_list = db.query_mysql(sql)
    recharge_amount = int(result_list[0][0])
    return recharge_amount


def get_asset_tran_status_by_item_no(db, item_no, period, tran_type=None):
    if tran_type:
        sql = 'select asset_tran_status from asset_tran where asset_tran_asset_item_no="{}" and asset_tran_period={} and asset_tran_type = "{}" '.format(
            item_no, period, tran_type)
    else:
        for x in range(0, 7000):
            sql = 'select asset_tran_status from asset_tran where asset_tran_asset_item_no="{}" and asset_tran_period={} and asset_tran_type <> "grant" '.format(
                item_no, period)
            result_list1 = db.query_mysql(sql)
            LogUtil.log_info("BIZ asset_tran status is: " + result_list1[0][0])
            if result_list1[0][0] == 'finish':
                break
    result_list = db.query_mysql(sql)
    LogUtil.log_info("get_asset_tran_status_by_item_no Sql is: " + sql)
    status_list = [result[0] for result in result_list]
    return status_list


def get_dtran_status_by_item_no(db, item_no, period, tran_type=None):
    if tran_type:
        sql = 'SELECT dtransaction_status FROM dtransaction WHERE dtransaction_asset_id IN(SELECT asset_id FROM asset WHERE `asset_item_no` IN ("{}")) AND dtransaction_period={} AND dtransaction_type = "{}" '.format(
            item_no, period, tran_type)
    else:
        sql = 'SELECT dtransaction_status FROM dtransaction WHERE dtransaction_asset_id IN(SELECT asset_id FROM asset WHERE `asset_item_no` IN ("{}")) AND dtransaction_period={} AND dtransaction_type <> "grant" '.format(
            item_no, period)
    for x in range(0, 5000):
        result_list = db.query_mysql(sql)
        if result_list[0][0] == 'finish':
            break
    LogUtil.log_info("get_dtran_status_by_item_no Sql is: " + sql)
    LogUtil.log_info("BIZ Dtran status is: " + result_list[0][0])
    status_list = [result[0] for result in result_list]
    return status_list


def get_withhold_result_in_biz_by_serial_no(db, serial_no):
    sql = 'select withhold_result_amount, withhold_result_id,withhold_result_status from withhold_result where withhold_result_serial_no="{}"'.format(
        serial_no)
    result_list = db.query_mysql(sql)
    withhold_result_amount_list = []
    withhold_result_id_list = []
    withhold_result_status = []
    for result in result_list:
        withhold_result_amount_list.append(int(result[0]))
        withhold_result_id_list.append(result[1])
        withhold_result_status.append(result[2])
    return withhold_result_amount_list, withhold_result_id_list, withhold_result_status


def get_withhold_amount_by_serial_no(db, serial_no):
    sql = 'select withhold_amount from withhold where withhold_serial_no="{}"'.format(serial_no)
    result_list = db.query_mysql(sql)
    withhold_amount = int(result_list[0][0])
    return withhold_amount


def get_withhold_transaction_in_biz_by_withhold_result_id(db, withhold_result_id):
    sql = 'select * from withhold_result_transaction where withhold_result_transaction_withhold_result_id={}'.format(
        withhold_result_id)
    result = db.query_mysql(sql)
    return result


def get_serial_no_by_item_no(db, item_no):
    sql = 'select withhold_order_serial_no from withhold_order where withhold_order_reference_no="{}" order by ' \
          'withhold_order_create_at desc limit 1'.format(item_no)
    result_list = db.query_mysql(sql)
    request_no = result_list[0][0]
    return request_no


def get_provision_amount_by_item_no(db, item_no):
    sql = 'select sum(provision_amount) from provision where provision_item_no = "{}"'.format(item_no)
    result_list = db.query_mysql(sql)
    amount = int(result_list[0][0])
    return amount


def get_asset_from_asset_by_item_no(db, item_no):
    sql = 'select asset_status from asset where asset_item_no="{}"'.format(item_no)
    result_list = db.query_mysql(sql)
    asset_status = result_list[0][0]
    return asset_status


def get_withhold_order_by_item_no(db, item_no, serial_no=None):
    if serial_no:
        sql = 'select withhold_order_withhold_status from withhold_order where withhold_order_reference_no="{}" and ' \
              'withhold_order_serial_no="{}"'.format(item_no, serial_no)
    else:
        sql = 'select withhold_order_withhold_status from withhold_order where withhold_order_reference_no="{}" and ' \
              'withhold_order_withhold_status="success"'.format(item_no)

    result_list = db.query_mysql(sql)
    status_list = []
    for result in result_list:
        status_list.append(result[0])
    return status_list


def quanhu_get_unique_id(db, item_no):
    sql = 'select asset_loan_record_trade_no from asset_loan_record where asset_loan_record_asset_id=(select asset_id from asset where asset_item_no="{}")'.format(
        item_no)
    result_list = db.query_mysql(sql)
    unique_id = result_list[0][0]
    return unique_id


def get_msg_status_from_gbiz_by_asset_item_no(db, item_no):
    sql = 'select sendmsg_status from sendmsg where sendmsg_order_no ="{}"'.format(item_no)
    result_list = db.query_mysql(sql)
    if result_list:
        return result_list[0][0]
    else:
        return None


def get_withhold_status_from_rbiz_by_serial_no(db, serial_no):
    sql = 'select withhold_status from withhold where withhold_serial_no="{}"'.format(serial_no)
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_req_key_from_withhold_request_by_request_no(db, request_no):
    sql = 'select withhold_request_req_key from withhold_request where withhold_request_no={}'.format(request_no)
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_asset_operation_auth(db, item_no):
    sql = 'select * from asset_operation_auth where asset_operation_auth_asset_item_no="{}"'.format(item_no)
    result_list = db.query_mysql(sql)
    return result_list


def get_withhold_asset_detail_lock(db, item_no):
    sql = 'select * from withhold_asset_detail_lock where withhold_asset_detail_lock_asset_item_no="{}"'.format(
        item_no)
    result_list = db.query_mysql(sql)
    return result_list


def update_account(db, id_num):
    sql = 'update account set account_balance_amount=100 where account_user_id_num_encrypt="{}"'.format(id_num)
    db.execute_mysql(sql)


def update_asset_to_payoff_by_date(db):
    sql = "UPDATE asset SET asset_status='payoff' WHERE asset_create_at < date_sub(now(),INTERVAL 7 DAY);"
    db.execute_mysql(sql)


def update_capital_route_fail_times(db, channel, times=1):
    fail_times = {"auto": {"times": times, "calByDay": True}, "active": {"times": times, "calByDay": True},
                  "manual": {"times": times, "calByDay": True}}
    sql = "UPDATE capital_route SET capital_route_conditional_value='{}' WHERE capital_route_config_code='{}' AND " \
          "capital_route_conditional='fail_times'".format(json.dumps(fail_times), channel)
    db.execute_mysql(sql)


def get_msg_id_from_rbiz_by_msg_order_no_and_msg_type(db, msg_order_no, msg_type):
    sql = f'select sendmsg_id from sendmsg where sendmsg_order_no="{msg_order_no}" and sendmsg_type="{msg_type}"'
    result_list = db.query_mysql(sql)
    if not result_list:
        for x in range(0, 100):
            result_list = db.query_mysql(sql)
            if result_list:
                break
    result_list = db.query_mysql(sql)
    if not result_list:
        raise Exception(f'获取msg_id失败，sql={sql}')
    return result_list[0][0]


def get_req_key_from_rbiz_by_serial_no(db, serial_no):
    sql = f'select withhold_req_key from withhold where withhold_serial_no="{serial_no}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_trade_no_from_trade_by_trade_no(db, trade_no):
    sql = f'select trade_no from trade where trade_no="{trade_no}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_serial_no_from_trade_tran_by_serial_no(db, serial_no):
    sql = f'select trade_tran_serial_no from trade_tran where trade_tran_serial_no="{serial_no}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_trade_no_from_trade_order_by_trade_no(db, trade_no):
    sql = f'select trade_no from trade_order where trade_no="{trade_no}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_serial_no_from_trade_order_tran_by_serial_no(db, serial_no):
    sql = f'select trade_tran_serial_no from trade_order_tran where trade_tran_serial_no="{serial_no}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_account_from_rbiz_by_id_num(db, id_num):
    sql = f'select account_no from account where account_user_id_num_encrypt="{id_num}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_amount_from_account_recharge_by_account_no(db, account_no):
    sql = f'select account_recharge_amount from account_recharge where account_recharge_account_no={account_no}'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_amount_from_account_recharge_log_by_account_no(db, account_no):
    sql = f'select account_recharge_log_amount from account_recharge_log where account_recharge_log_account_no={account_no}'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_amount_from_account_repay_by_account_no(db, account_no):
    sql = f'select sum(account_repay_amount) from account_repay where account_repay_account_no={account_no}'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_amount_from_account_repay_log_by_account_no(db, account_no):
    sql_begin = f'select account_repay_log_amount_beginning from account_repay_log where account_repay_log_account_no={account_no} order by account_repay_log_amount_beginning desc limit 1'
    result_list_begin = db.query_mysql(sql_begin)
    sql_end = f'select account_repay_log_amount_ending from account_repay_log where account_repay_log_account_no={account_no} order by account_repay_log_amount_ending asc limit 1'
    result_list_end = db.query_mysql(sql_end)
    return result_list_begin[0][0], result_list_end[0][0]


def get_channel_key_from_withhold_by_serial_no(db, serial_no):
    sql = f'select withhold_channel_key from withhold where withhold_serial_no="{serial_no}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_account_balance_amount_from_account_by_id_num(db, id_num):
    sql = f'select account_balance_amount from account where account_user_id_num_encrypt="{id_num}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_serial_no_from_withhold_order_by_item_no(db, item_no):
    sql = 'select withhold_order_serial_no from withhold_order where withhold_order_reference_no="{}"'.format(
        item_no)
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def update_account_balance_by_id_num(db, amount, id_num):
    sql = f'update account set account_balance_amount={amount} where account_user_id_num_encrypt="{id_num}"'
    db.execute_mysql(sql)


def get_serial_no_from_withhold_by_id_num(db, id_num):
    sql = f'select withhold_serial_no from withhold where withhold_user_idnum="{id_num}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def clear_trade_data(db, item_no):
    sql_request = f"delete from withhold_request where withhold_request_req_key in (select withhold_order_req_key from withhold_order where withhold_order_reference_no ='{item_no}')"
    sql_withold = f"delete from withhold where withhold_req_key in(select withhold_order_req_key from withhold_order where withhold_order_reference_no = '{item_no}')"
    sql_order = f"delete from withhold_order where  withhold_order_reference_no='{item_no}'"
    db.execute_mysql(sql_request)
    db.execute_mysql(sql_withold)
    db.execute_mysql(sql_order)


def get_serial_no_from_refund_request_by_serial_no(db, serial_no):
    sql = f'SELECT refund_request_withhold_channel_key FROM refund_request WHERE refund_request_withhold_serial_no="{serial_no}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_serial_no_from_refund_by_serial_no(db, serial_no):
    sql = f'SELECT refund_result_withhold_result_serial_no FROM refund_result WHERE refund_result_withhold_result_serial_no="{serial_no}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_operate_type_from_refund_detail_by_serial_no(db, serial_no):
    sql = f'SELECT refund_detail_operate_type FROM refund_detail WHERE refund_detail_withhold_serial_no="{serial_no}"'
    result_list = db.query_mysql(sql)
    operate_type_list = [result[0] for result in result_list]
    return operate_type_list


def get_withdraw_status_from_withdraw_by_serial_no(db, serial_no):
    sql = f'SELECT withdraw_status FROM withdraw WHERE withdraw_ref_no="{serial_no}"'
    result_list = db.query_mysql(sql)
    return result_list[0][0]


def get_sign_company_in_withhold_by_request_no(db, withold_requst_no):
    withhold_extend_info = 'select withhold_extend_info from withhold where withhold_request_no="{}" order by withhold_id asc'.format(
        withold_requst_no)
    result_list = db.query_mysql(withhold_extend_info)
    sign_company_list = [json.loads(result[0]).get('paysvrSignCompany', None) for result in result_list if result[0]]
    return sign_company_list


def get_alr_trade_no_from_alr_in_biz_by_item_no(db, item_no):
    sql = 'SELECT asset_loan_record_trade_no FROM asset_loan_record WHERE `asset_loan_record_asset_id` IN(SELECT ' \
          'asset_id FROM asset WHERE `asset_item_no` IN ("{}"))'.format(item_no)
    result_list = db.query_mysql(sql)
    asset_loan_record_trade_no = result_list[0][0]
    return asset_loan_record_trade_no
