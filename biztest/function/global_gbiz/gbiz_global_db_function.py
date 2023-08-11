from biztest.util.tools.tools import *
from copy import deepcopy
import common.global_const as gc


def update_asset_status_all():
    sql = "update asset set asset_status='payoff'"
    gc.GRANT_DB.update(sql)


def get_asset_info_by_item_no(item_no):
    sql = "select * from asset where asset_item_no='%s'" % item_no
    asset_info = gc.GRANT_DB.query(sql)
    return asset_info


def get_global_confirm_data_by_item_no(item_no, asset_confirm_type):
    sql = "select * from asset_confirm where asset_confirm_item_no='%s' and asset_confirm_type=" \
          "'%s';" % (item_no, asset_confirm_type)
    confirm_data = gc.GRANT_DB.query(sql)
    return confirm_data


def get_asset_loan_record_by_item_no(item_no):
    sql = "select * from asset_loan_record where asset_loan_record_asset_item_no='%s'" % item_no
    asset_loan_record = gc.GRANT_DB.query(sql)
    return asset_loan_record


def get_global_asset_loan_record_by_item_no(item_no):
    sql = "select * from asset_loan_record where asset_loan_record_asset_item_no='%s'" % item_no
    asset_loan_record = gc.GRANT_DB.query(sql)
    return asset_loan_record


def update_asset_loan_record_by_item_no(item_no, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "" + key + "='" + value + "', "
    sql = "update asset_loan_record set %s where asset_loan_record_asset_item_no ='%s'" % (sql_params[:-2], item_no)
    gc.GRANT_DB.update(sql)


def get_asset_tran_by_item_no(item_no):
    sql = "select * from asset_tran where asset_tran_asset_item_no='%s' " \
          "order by asset_tran_period,asset_tran_amount" % item_no
    asset_tran = gc.GRANT_DB.query(sql)
    return asset_tran


def get_capital_asset_by_item_no(item_no):
    sql = "select * from capital_asset where capital_asset_item_no='%s'" % item_no
    capital_asset = gc.GRANT_DB.query(sql)
    return capital_asset


def get_task_list_by_item_no(item_no):
    sql = "select * from task where task_order_no='%s' order by task_id desc" % item_no
    task_list = gc.GRANT_DB.query(sql)
    return task_list


def update_task_by_item_no_task_type(item_no, task_types, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update task set %s where task_order_no='%s' and task_type='%s'" % (sql_params[:-2], item_no, task_types)
    gc.GRANT_DB.update(sql)


def update_terminated_task(**kwargs):
    sql = "update task set %s where task_status='terminated'" % generate_sql(kwargs, ",")
    gc.GRANT_DB.do_sql(sql)


def update_last_task_by_item_no_task_type(item_no, task_types, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update task set %s where task_order_no='%s' and task_type='%s' order by task_id desc limit 1" \
          % (sql_params[:-2], item_no, task_types)
    gc.GRANT_DB.update(sql)


def get_task_by_item_no_and_task_type(item_no, task_type, num=None):
    """
    获取指定task内容，默认获取到最新的一个 task
    :param item_no: 资产编号
    :param task_type: task类型
    :param num: 同名task可能有多个，指定获取第几个
    :return:
    """
    sql = "select * from task where task_order_no='%s' order by task_id asc" % item_no
    task_list = gc.GRANT_DB.query(sql)
    ret = None
    if not task_list:
        return None
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


def get_global_by_item_no_and_task_type(item_no, task_type, num=None):
    """
    获取指定task内容，默认获取到最新的一个task
    :param item_no: 资产编号
    :param task_type: task类型
    :param num: 同名task可能有多个，指定获取第几个
    :return:
    """
    sql = "select * from task where task_order_no='%s' order by task_id asc" % item_no
    task_list = gc.GRANT_DB.query(sql)
    ret = None
    if not task_list:
        return None
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


def get_withdraw_by_asset_item_no(item_no):
    sql = "select * from withdraw where withdraw_asset_item_no='%s' order by withdraw_id" % item_no
    withdraw_list = gc.GRANT_DB.query(sql)
    return withdraw_list


def update_router_capital_plan(capital_plan):
    sql = "delete from router_capital_plan where router_capital_plan_date='%s' and router_capital_plan_label='%s'" \
          % (capital_plan["plan_date"], capital_plan["plan_label"])
    gc.GRANT_DB.delete(sql)
    sql = "INSERT INTO router_capital_plan(router_capital_plan_date, router_capital_plan_label, " \
          "router_capital_plan_desc, router_capital_plan_amount, router_capital_plan_update_memo) " \
          "VALUES ('%s', '%s', '%s', '%s', '自动化脚本插入')" \
          % (capital_plan["plan_date"], capital_plan["plan_label"],
             capital_plan["plan_desc"], capital_plan["plan_amount"])
    gc.GRANT_DB.insert(sql)


def insert_router_capital_plan(rule_code, amount=200000000000000):
    date = get_date(fmt="%Y-%m-%d", timezone=get_tz(gc.COUNTRY))
    sql = "INSERT INTO router_capital_plan(router_capital_plan_date, router_capital_plan_label, " \
          "router_capital_plan_desc, router_capital_plan_amount, router_capital_plan_update_memo, " \
          "router_capital_plan_create_at, router_capital_plan_update_at) " \
          "VALUES ('%s', '%s', '%s', '%s', '自动化脚本插入', NOW(), NOW())" \
          % (date, rule_code, rule_code, amount)
    gc.GRANT_DB.insert(sql)


def delete_router_capital_plan():
    date = time.strftime("%Y-%m-%d")
    sql = "delete from router_capital_plan"
    gc.GRANT_DB.delete(sql)


def update_router_capital_rule(capital_rule):
    sql = "delete from router_capital_rule where router_capital_rule_code='%s'" % (capital_rule["rule_code"])
    gc.GRANT_DB.delete(sql)
    sql = "INSERT INTO router_capital_rule (router_capital_rule_code, router_capital_rule_desc, " \
          "router_capital_rule_family, router_capital_rule_type, router_capital_rule_activation_group, " \
          "router_capital_rule_limit_type, router_capital_rule_weight, router_capital_rule_allow_overflow_rate, " \
          "router_capital_rule_content, router_capital_rule_status, router_capital_rule_product_code) " \
          "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', 'release', '%s')" \
          % (capital_rule["rule_code"], capital_rule["rule_desc"], capital_rule["rule_family"],
             capital_rule["rule_type"], capital_rule["rule_activation_group"], capital_rule["rule_limit_type"],
             capital_rule["rule_weight"], capital_rule["rule_allow_overflow_rate"], capital_rule["rule_content"],
             capital_rule["rule_product_code"])
    gc.GRANT_DB.insert(sql)


def insert_router_capital_rule(channel, period_count, period_day, period_type, rule_code, rule_limit_type, overflow_rate=0):
    sql = "INSERT INTO router_capital_rule (router_capital_rule_code, router_capital_rule_desc, " \
          "router_capital_rule_family, router_capital_rule_type, router_capital_rule_weight, " \
          "router_capital_rule_content, router_capital_rule_status, router_capital_rule_create_at, " \
          "router_capital_rule_update_at, router_capital_rule_limit_type, router_capital_rule_allow_overflow_rate) " \
          "VALUES ('%s', '%s', '%s', 'supply', 0, " \
          "'{\\\"name\\\":\\\"%s\\\",\\\"rules\\\":[{\\\"name\\\":\\\"%s期产品\\\",\\\"rule\\\":" \
          "\\\"asset.periodType==\\\'%s\\\' and asset.periodCount==%s and asset.periodDay==\\\'%s\\\'\\\"}]," \
          "\\\"output\\\":{\\\"key\\\":\\\"channel\\\",\\\"value\\\":\\\"%s\\\"}}', " \
          "'release', NOW(), NOW(), '%s', '%s')" \
          % (rule_code, rule_code, channel, rule_code, period_count, period_type,
             int(period_count), period_day, channel, rule_limit_type, overflow_rate)
    gc.GRANT_DB.insert(sql)


def delete_router_capital_rule():
    sql = "delete from router_capital_rule"
    gc.GRANT_DB.delete(sql)


def update_router_weight(rule_weight):
    sql = "delete from router_weight where router_weight_desc = '%s'" % rule_weight["weight_desc"]
    gc.GRANT_DB.delete(sql)
    sql = "INSERT INTO router_weight (router_weight_type, router_weight_code, router_weight_desc, " \
          "router_weight_rule_content, router_weight_value, router_weight_status, router_weight_first_route_status, " \
          "router_weight_second_route_status, router_weight_create_name) " \
          "VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '自动化脚本插入')" \
          % (rule_weight["weight_type"], rule_weight["weight_code"], rule_weight["weight_desc"],
             rule_weight["weight_rule_content"], rule_weight["weight_value"], rule_weight["weight_status"],
             rule_weight["weight_first_route_status"], rule_weight["weight_second_route_status"])
    gc.GRANT_DB.insert(sql)


def insert_router_weight(channel, rule_code, weight=2000, status='active', first_route_status='active', second_route_status='active'):
    sql = "INSERT INTO router_weight (router_weight_type, router_weight_code, router_weight_desc, " \
          "router_weight_rule_content, router_weight_value, router_weight_status, router_weight_first_route_status, " \
          "router_weight_second_route_status, router_weight_create_at, router_weight_update_at, " \
          "router_weight_create_name, router_weight_update_name) " \
          "VALUES ('channel', '%s', '%s', 'finalRuleList.contains(\\'%s\\')', '%s', " \
          "'%s', '%s', '%s', NOW(), NOW(), '自动化脚本插入', '自动化脚本插入')" \
          % (channel, rule_code, rule_code, weight, status, first_route_status, second_route_status)
    gc.GRANT_DB.insert(sql)


def delete_router_weight():
    sql = "delete from router_weight"
    gc.GRANT_DB.delete(sql)


def update_router_weight_by_channel(channel, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update router_weight set %s where router_weight_code='%s'" % (sql_params[:-2], channel)
    gc.GRANT_DB.update(sql)


def insert_router_load_total(rule_code,routed_amount=0, imported_amount=0):
    date = time.strftime("%Y-%m-%d")
    sql = "INSERT INTO router_load_total (router_load_total_rule_code, router_load_total_count, " \
          "router_load_total_routed_amount, router_load_total_imported_amount, router_load_total_route_day) " \
          "VALUES ('%s', 1, '%s', '%s', '%s')" \
          % (rule_code, routed_amount, imported_amount, date)
    gc.GRANT_DB.insert(sql)


def delete_router_load_total():
    date = time.strftime("%Y-%m-%d")
    sql = "delete from router_load_total"
    gc.GRANT_DB.delete(sql)


def update_router_load_total(rule_code, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "" + key + "='" + str(value) + "', "
    sql = "update router_load_total set %s " \
          "where router_load_total_rule_code ='%s' and router_load_total_route_day = '%s'" \
          % (sql_params[:-2], rule_code, time.strftime("%Y-%m-%d"))
    gc.GRANT_DB.update(sql)


def get_router_load_record_by_key(key):
    sql = "select * from router_load_record where router_load_record_key = '%s'" % key
    result = gc.GRANT_DB.query(sql)
    return result


def update_router_load_record_by_key(route_key, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "" + key + "='" + str(value) + "', "
    sql = "update router_load_record set %s " \
          "where router_load_record_key ='%s'" \
          % (sql_params[:-2], route_key)
    gc.GRANT_DB.update(sql)


def update_manual_account_plan(day, card_no):
    sql1 = "delete from manual_account_plan where manual_account_plan_day = '%s'" % day
    sql2 = "INSERT INTO manual_account_plan (manual_account_plan_day, manual_account_plan_card_no, " \
           "manual_account_plan_count, manual_account_plan_create_at, manual_account_plan_update_at)" \
           "VALUES ('%s', '%s', 0, now(), now())" % (day, card_no)
    gc.GRANT_DB.delete(sql1)
    gc.GRANT_DB.insert(sql2)


def update_all_channel_amount():
    # today = time.strftime("%Y-%m-%d", time.localtime())
    today = get_date(fmt="%Y-%m-%d", timezone=get_tz(gc.COUNTRY))
    sql = "UPDATE router_capital_plan set router_capital_plan_amount=3333333333  where  router_capital_plan_date='%s'" \
          "; " % today
    gc.GRANT_DB.update(sql)


def update_router_capital_plan_amount_all_to_zero(capital_channel):
    # today = time.strftime("%Y-%m-%d", time.localtime())
    today = get_date(fmt="%Y-%m-%d", timezone=get_tz(gc.COUNTRY))
    sql = "UPDATE router_capital_plan set router_capital_plan_amount=0  where router_capital_plan_label " \
          " not like '%{}%' and router_capital_plan_date='{}';".format(capital_channel, today)
    gc.GRANT_DB.update(sql)


def update_router_capital_plan_by_rule_code(rule_code, amount=200000000):
    date = time.strftime("%Y-%m-%d")
    sql = "update router_capital_plan set router_capital_plan_amount = '%s' where router_capital_plan_label = '%s'" \
          "and router_capital_plan_date = '%s'" % (amount, rule_code, date)
    gc.GRANT_DB.update(sql)


def get_manual_asset_by_item_no(item_no):
    sql = "select * from manual_asset where manual_asset_item_no='%s'" % item_no
    rs = gc.GRANT_DB.query(sql)
    return rs


def get_asset_borrower_by_item_no(item_no):
    sql = "select * from asset_borrower where asset_borrower_item_no='%s'" % item_no
    rs = gc.GRANT_DB.query(sql)
    return rs


def get_asset_event_by_item_no_event_type(item_no, event_type):
    sql = "select * from asset_event where asset_event_item_no='%s' and asset_event_type = '%s'" % (item_no, event_type)
    rs = gc.GRANT_DB.query(sql)
    return rs


def get_sendmsg_by_item_no(item_no, msg_type):
    sql = "select * from sendmsg where sendmsg_order_no ='%s' and sendmsg_type = '%s'" % (item_no, msg_type)
    rs = gc.GRANT_DB.query(sql)
    return rs


def get_order_no(item_no):
    sql = "select * from withdraw_order where withdraw_order_asset_item_no='%s' order by withdraw_order_id desc" % item_no
    rs = gc.GRANT_DB.query(sql)
    return rs[0]["withdraw_order_no"]


def get_withdraw_order_by_item_no(item_no):
    sql = "select * from withdraw_order where withdraw_order_asset_item_no='%s' order by withdraw_order_id desc" % item_no
    rs = gc.GRANT_DB.query(sql)
    return rs


def get_withdraw_record_by_item_no(item_no):
    order_no = get_order_no(item_no)
    sql = "select * from withdraw_record where withdraw_record_order_no='%s'" % order_no
    rs = gc.GRANT_DB.query(sql)
    return rs


def get_asset_import_data_by_item_no(item_no):
    task_info = get_task_by_item_no_and_task_type(item_no, 'AssetImport')
    asset_info = None
    if task_info is not None:
        asset_info = json.loads(task_info['task_request_data'])['data']
    return asset_info


# 脚本mock放款成功消息
def get_asset_from_asset(item_no):
    sql = "SELECT asset_item_no,asset_type `type`,asset_sub_type sub_type,asset_period_type period_type," \
          "asset_period_count period_count,asset_product_category product_category,asset_cmdb_product_number " \
          "cmdb_product_number,asset_grant_at grant_at,asset_effect_at effect_at,now() actual_grant_at," \
          "asset_due_at due_at,asset_payoff_at payoff_at,asset_from_system from_system,'repay' `status`," \
          "asset_principal_amount principal_amount,asset_principal_amount granted_principal_amount,asset_loan_channel " \
          "loan_channel,asset_alias_name alias_name,asset_interest_amount interest_amount,asset_fee_amount " \
          "fee_amount,asset_balance_amount balance_amount,asset_repaid_amount repaid_amount,asset_total_amount " \
          "total_amount,unix_timestamp(now())*99 version,6.500 interest_rate,0 charge_type,asset_source_number " \
          "ref_order_no,asset_source_type ref_order_type,'' sub_order_type,0 overdue_guarantee_amount, '' info," \
          "asset_owner `owner`,'' risk_level,''product_name,asset_from_app from_app,asset_from_system_name " \
          "from_system_name FROM asset  WHERE asset_item_no='%s'" % item_no
    asset = gc.GRANT_DB.query(sql)
    return asset


def get_trans_from_asset_tran(item_no):
    sql = "SELECT asset_tran_asset_item_no asset_item_no ,asset_tran_type `type`,asset_tran_description description," \
          "asset_tran_amount amount, asset_tran_decrease_amount decrease_amount,asset_tran_repaid_amount " \
          "repaid_amount,asset_tran_balance_amount balance_amount,asset_tran_total_amount total_amount, " \
          "asset_tran_status `status`,asset_tran_due_at due_at,now(), asset_tran_finish_at finish_at," \
          "asset_tran_period period,asset_tran_late_status late_status,asset_tran_remark remark," \
          "asset_tran_repay_priority repay_priority,asset_tran_trade_at trade_at,asset_tran_category category FROM " \
          "asset_tran WHERE asset_tran_asset_item_no='%s' " % item_no
    asset_tran = gc.GRANT_DB.query(sql)
    return asset_tran


def get_loan_record_from_asset(item_no):
    sql = "SELECT asset_item_no,asset_principal_amount AS amount,0 AS withholding_amount,asset_loan_channel channel," \
          "6 AS `status`,asset_item_no AS identifier,asset_item_no AS trade_no,asset_item_no AS due_bill_no," \
          "0 commission_amount,0 pre_fee_amount,0 service_fee_amount,'' is_deleted,now() finish_at,'' trans_property," \
          "0 pre_interest,0 commission_amt_interest,now() grant_at,now() push_at FROM asset WHERE asset_item_no='%s'" % item_no
    loan_record = gc.GRANT_DB.query(sql)
    return loan_record


def get_borrower_from_asset_card(item_no):
    sql = "SELECT asset_borrower_uuid borrower_uuid,asset_borrower_id_num id_num,asset_borrower_mobile mobile," \
          "asset_borrower_card_uuid borrower_card_uuid,asset_borrower_individual_uuid individual_uuid,''risk_level " \
          "FROM  asset_borrower WHERE asset_borrower_item_no='%s'" % item_no
    borrower = gc.GRANT_DB.query(sql)
    return borrower


# 资方还款计划
def get_capital_transaction_principal_from_asset_tran(item_no):
    sql = "SELECT asset_tran_period period, asset_tran_category `type`,0 amount,0.00000000 rate," \
          "asset_tran_asset_item_no  item_no,1 period_term, 'month' period_type,asset_tran_due_at expect_finished_at," \
          "'acpi' repayment_type, now() create_at,now() update_at,asset_tran_amount origin_amount,'1000-01-01 " \
          "00:00:00' user_repay_at,'' user_repay_channel,'' actual_finished_at,'grant' operate_type FROM asset_tran " \
          "WHERE asset_tran_asset_item_no='%s' AND asset_tran_type  IN ('repayprincipal','repayinterest')" % item_no
    asset_tran = gc.GRANT_DB.query(sql)
    return asset_tran


def get_capital_transaction_fees_from_asset_tran(item_no):
    sql = "SELECT asset_tran_period period, asset_tran_type `type`,0 amount,0.00000000 rate," \
          "asset_tran_asset_item_no  item_no,1 period_term, 'month' period_type,asset_tran_due_at expect_finished_at," \
          "'acpi' repayment_type, now() create_at,now() update_at,asset_tran_amount origin_amount,'1000-01-01 " \
          "00:00:00' user_repay_at,'' user_repay_channel,'' actual_finished_at,'grant' operate_type FROM asset_tran " \
          "WHERE asset_tran_asset_item_no='%s' AND asset_tran_type NOT IN ('repayprincipal'," \
          "'repayinterest','grant');" % item_no
    asset_tran = gc.GRANT_DB.query(sql)
    return asset_tran


def update_withdraw_order(item_no, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update withdraw_order set %s where withdraw_order_asset_item_no='%s'" % (sql_params[:-2], item_no)
    gc.GRANT_DB.update(sql)


def insert_router_load_record(**kwargs):
    sql_keys = ""
    sql_values = ""
    for key, value in kwargs.items():
        sql_keys += "`" + key + "`, "
        sql_values += "'" + str(value) + "', "
    sql = "INSERT INTO `router_load_record` (%s) VALUES (%s);" % (sql_keys[:-2], sql_values[:-2])
    gc.GRANT_DB.do_sql(sql)


def insert_manual_asset(item_no, channel, amount, receiver_card_no):
    sql = "INSERT INTO `manual_asset` (`manual_asset_item_no`, `manual_asset_type`, `manual_asset_channel`, " \
          "`manual_asset_amount`, `manual_asset_status`, `manual_asset_apply_at`, `manual_asset_finish_at`, " \
          "`manual_asset_order_no`, `manual_asset_account_card_no`, `manual_asset_account_card_type`, " \
          "`manual_asset_receiver_card_no`, `manual_asset_receiver_account_type`, " \
          "`manual_asset_receiver_card_branch_name`, `manual_asset_charge_fee`, `manual_asset_comment`) VALUES (" \
          "'%s', 'paydayloan', '%s', %s, 'repay', '%s', '%s', '5000004', 'enc_03_4114921277314572288_639', " \
          "'Easypaisa', '%s', 'JazzCash', '', 0, '放款成功');" % \
          (item_no, channel, amount, get_date(), get_date(), receiver_card_no)
    gc.GRANT_DB.do_sql(sql)


def update_manual_asset(item_no, **kwargs):
    sql = "update manual_asset set %s where manual_asset_item_no='%s'" % (generate_sql(kwargs, ","), item_no)
    gc.GRANT_DB.update(sql)


def update_confirm_data_by_item_no(item_no):
    sql = "update asset_confirm set asset_confirm_create_at = DATE_SUB(now(), interval 48 hour) where " \
          "asset_confirm_item_no = '%s' and asset_confirm_type='WITHDRAW_FINAL_FAIL_UPDATE_CARD';" % (item_no)
    gc.GRANT_DB.update(sql)


def insert_asset_confirm(item_no, channel, type, status):
    sql = "INSERT INTO asset_confirm (asset_confirm_item_no, asset_confirm_channel, asset_confirm_type, " \
          "asset_confirm_status, asset_confirm_memo) " \
          "VALUES ('%s', '%s', '%s', '%s', '')" \
          % (item_no, channel, type, status)
    gc.GRANT_DB.insert(sql)
