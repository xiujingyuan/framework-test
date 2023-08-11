from biztest.util.tools.tools import *
from copy import deepcopy
import common.global_const as gc


def get_asset_info_by_item_no(item_no):
    sql = "select * from asset where asset_item_no='%s'" % item_no
    asset_info = gc.GRANT_DB.query(sql)
    return asset_info


def get_asset_cmdb_product_number(item_no):
    sql = "select asset_cmdb_product_number from asset where asset_item_no='%s'" % item_no
    cmdb_number = gc.GRANT_DB.query(sql)
    return cmdb_number[0]['asset_cmdb_product_number']


def get_capital_blacklist_data_by_card(card):
    sql = "select * from capital_blacklist where capital_blacklist_value='%s'" % card
    data = gc.GRANT_DB.query(sql)
    return data


def get_asset_loan_record_by_item_no(item_no):
    sql = "select * from asset_loan_record where asset_loan_record_asset_item_no='%s' order by asset_loan_record_create_at desc limit 1" % item_no
    asset_loan_record = gc.GRANT_DB.query(sql)
    return asset_loan_record


def update_asset_loan_record_by_item_no(item_no, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "" + key + "='" + value + "', "
    sql = "update asset_loan_record set %s where asset_loan_record_asset_item_no ='%s'" % (sql_params[:-2], item_no)
    gc.GRANT_DB.update(sql)


def get_asset_route_log_by_idum(idnum_encrypt, loan_channel):
    sql = "select * from asset_route_log where asset_route_log_borrower_idnum='%s' " \
          "and asset_route_log_loan_channel = '%s' order " \
          "by asset_route_log_id desc limit 1;" % (idnum_encrypt, loan_channel)
    asset_route_log = gc.GRANT_DB.query(sql)
    return asset_route_log


def get_router_load_record_by_idum(idnum_encrypt, router_load_record_rule_code):
    sql = "select * from router_load_record where router_load_record_idnum='%s' and router_load_record_rule_code='%s'" \
          " order by router_load_record_id desc;" % (idnum_encrypt, router_load_record_rule_code)
    router_load_record = gc.GRANT_DB.query(sql)
    return router_load_record


def get_confirm_data_by_item_no(item_no, asset_confirm_type):
    sql = "select * from asset_confirm where asset_confirm_item_no='%s' and asset_confirm_type=" \
          "'%s';" % (item_no, asset_confirm_type)
    confirm_data = gc.GRANT_DB.query(sql)
    return confirm_data


def update_confirm_data_by_item_no(item_no):
    sql = "update asset_confirm set asset_confirm_create_at = DATE_SUB(now(), interval 600 minute) where " \
          "asset_confirm_item_no = '%s' and asset_confirm_type='WITHDRAW_FINAL_FAIL_UPDATE_CARD';" % (item_no)
    gc.GRANT_DB.update(sql)


def get_asset_extend_by_item_no(item_no):
    sql = "select * from asset_extend where asset_extend_asset_item_no='%s'" % item_no
    asset_extend_info = gc.GRANT_DB.query(sql)
    return asset_extend_info


def get_asset_tran_by_item_no(item_no):
    sql = "select * from asset_tran where asset_tran_asset_item_no='%s' " \
          "order by asset_tran_period,asset_tran_amount" % item_no
    asset_tran = gc.GRANT_DB.query(sql)
    return asset_tran


# 脚本mock放款成功消息
def get_asset_from_asset_and_asset_extend(item_no, version, source_type=None):
    # irr36_quanyi 大单关联的小单为空
    if source_type == "irr36_quanyi":
        sql = "SELECT asset_item_no,asset_type `type`,asset_sub_type sub_type,asset_period_type period_type," \
              "asset_period_count period_count,asset_product_category product_category,asset_cmdb_product_number " \
              "cmdb_product_number,asset_grant_at grant_at,asset_effect_at effect_at,asset_grant_at actual_grant_at," \
              "asset_due_at due_at,asset_payoff_at payoff_at,asset_from_system from_system,'repay' `status`," \
              "asset_principal_amount principal_amount,asset_principal_amount granted_principal_amount,asset_loan_channel " \
              "loan_channel,asset_alias_name alias_name,asset_interest_amount interest_amount,asset_fee_amount " \
              "fee_amount,asset_balance_amount balance_amount,asset_repaid_amount repaid_amount,asset_total_amount " \
              "total_amount,%s version,5 interest_rate,1 charge_type," \
              "0 withholding_amount,0 overdue_guarantee_amount, asset_owner `owner`,'' ref_order_no," \
              "asset_extend_ref_order_type ref_order_type,'' sub_order_type,asset_extend_risk_level risk_level," \
              "asset_from_app from_app,'' info,''product_name," \
              "asset_from_system_name from_system_name FROM asset INNER JOIN asset_extend ON " \
              "asset_item_no=asset_extend_asset_item_no WHERE asset_item_no='%s'" % (version, item_no)
    else:
        sql = "SELECT asset_item_no,asset_type `type`,asset_sub_type sub_type,asset_period_type period_type," \
              "asset_period_count period_count,asset_product_category product_category,asset_cmdb_product_number " \
              "cmdb_product_number,asset_grant_at grant_at,asset_effect_at effect_at,asset_grant_at actual_grant_at," \
              "asset_due_at due_at,asset_payoff_at payoff_at,asset_from_system from_system,'repay' `status`," \
              "asset_principal_amount principal_amount,asset_principal_amount granted_principal_amount,asset_loan_channel " \
              "loan_channel,asset_alias_name alias_name,asset_interest_amount interest_amount,asset_fee_amount " \
              "fee_amount,asset_balance_amount balance_amount,asset_repaid_amount repaid_amount,asset_total_amount " \
              "total_amount,%s version,5 interest_rate,1 charge_type," \
              "0 withholding_amount,0 overdue_guarantee_amount, asset_owner `owner`,asset_extend_ref_order_no ref_order_no," \
              "asset_extend_ref_order_type ref_order_type,'' sub_order_type,asset_extend_risk_level risk_level," \
              "asset_from_app from_app,'' info,''product_name," \
              "asset_from_system_name from_system_name FROM asset INNER JOIN asset_extend ON " \
              "asset_item_no=asset_extend_asset_item_no WHERE asset_item_no='%s'" % (version, item_no)
    asset = gc.GRANT_DB.query(sql)
    return asset


def get_dtransactions_grant_from_asset_tran(item_no):
    sql = "SELECT asset_tran_asset_item_no asset_item_no ,asset_tran_type `type`,asset_tran_description description," \
          "asset_tran_amount amount, asset_tran_decrease_amount decrease_amount,asset_tran_repaid_amount " \
          "repaid_amount,asset_tran_balance_amount balance_amount,asset_tran_total_amount total_amount, " \
          "'finish' `status`," \
          "asset_tran_due_at due_at,now() finish_at,asset_tran_period period, asset_tran_late_status late_status," \
          "asset_tran_remark remark,asset_tran_repay_priority repay_priority,asset_tran_trade_at trade_at," \
          "asset_tran_category category FROM asset_tran WHERE asset_tran_asset_item_no='%s' AND asset_tran_type IN(" \
          "'grant')" % item_no
    asset_tran = gc.GRANT_DB.query(sql)
    return asset_tran


def get_dtransactions_principal_and_interest_from_asset_tran(item_no):
    sql = "SELECT asset_tran_asset_item_no asset_item_no ,asset_tran_type `type`,asset_tran_description description," \
          "asset_tran_amount amount, asset_tran_decrease_amount decrease_amount,asset_tran_repaid_amount " \
          "repaid_amount,asset_tran_balance_amount balance_amount,asset_tran_total_amount total_amount, 'nofinish' " \
          "`status`," \
          "asset_tran_due_at due_at,asset_tran_finish_at finish_at,asset_tran_period period, asset_tran_late_status " \
          "late_status,asset_tran_remark remark,asset_tran_repay_priority repay_priority,asset_tran_trade_at " \
          "trade_at,asset_tran_category category FROM asset_tran WHERE asset_tran_asset_item_no='%s' AND " \
          "asset_tran_type IN('repayprincipal','repayinterest')" % item_no
    asset_tran = gc.GRANT_DB.query(sql)
    return asset_tran


def get_fees_from_asset_tran(item_no):
    sql = "SELECT asset_tran_asset_item_no asset_item_no ,asset_tran_type `type`,asset_tran_description description," \
          "asset_tran_amount amount, asset_tran_decrease_amount decrease_amount,asset_tran_repaid_amount " \
          "repaid_amount,asset_tran_balance_amount balance_amount,asset_tran_total_amount total_amount, 'nofinish' " \
          "`status`," \
          "asset_tran_due_at due_at,asset_tran_finish_at finish_at,asset_tran_period period, asset_tran_late_status " \
          "late_status,asset_tran_remark remark,asset_tran_repay_priority repay_priority,asset_tran_trade_at " \
          "trade_at,asset_tran_category category FROM asset_tran WHERE asset_tran_asset_item_no='%s' AND " \
          "asset_tran_type not IN('grant','repayprincipal','repayinterest')" % item_no
    asset_tran = gc.GRANT_DB.query(sql)
    return asset_tran


def get_loan_record_from_asset(item_no):
    sql = "SELECT asset_item_no,asset_principal_amount AS amount,0 AS withholding_amount,asset_loan_channel AS " \
          "channel, 6 AS `status`,asset_item_no AS identifier,concat('TN',asset_item_no) AS trade_no,concat('DN'," \
          "asset_item_no) as due_bill_no, now() AS finish_at,now() AS grant_at,now() AS push_at,0 commission_amount," \
          "0 pre_fee_amount, 0 service_fee_amount,'' is_deleted,'' trans_property,0 pre_interest," \
          "'' commission_amt_interest,'KN1-CL-HLJ' product_code FROM asset WHERE asset_item_no='%s'" % item_no
    asset_tran = gc.GRANT_DB.query(sql)
    return asset_tran


def get_asset_card(**kwargs):
    sql = "select * from asset_card where %s" % generate_sql(kwargs, "and")
    asset_card = gc.GRANT_DB.query(sql)
    return asset_card


def get_repay_card_from_asset_card(item_no):
    sql = "SELECT asset_card_account_card_number_encrypt account_num_encrypt,'debit' account_type," \
          "asset_card_account_bank_code bank_code,asset_card_account_branch_name bankname," \
          "asset_card_account_idnum_encrypt credentials_num_encrypt,0 credentials_type," \
          "asset_card_account_idnum_encrypt individual_idnum_encrypt, asset_card_account_tel_encrypt phone_encrypt," \
          "asset_card_account_name_encrypt username_encrypt FROM asset_card WHERE " \
          "asset_card_asset_item_no='%s' AND asset_card_type='repay'" % item_no
    repay_card = gc.GRANT_DB.query(sql)
    return repay_card


def get_receive_card_from_asset_card(item_no):
    sql = "SELECT asset_card_account_name_encrypt account_name_encrypt,asset_card_account_branch_name bank," \
          "asset_card_account_bank_code bank_code, asset_card_account_branch_name `name`," \
          "asset_card_account_card_number_encrypt num_encrypt,  asset_card_account_idnum_encrypt owner_id_encrypt," \
          "asset_card_account_name_encrypt owner_name_encrypt,'individual' `type`,asset_card_account_tel_encrypt " \
          "phone_encrypt,4 factor_by FROM asset_card WHERE asset_card_asset_item_no='%s' AND " \
          "asset_card_type='receive'" % item_no
    repay_card = gc.GRANT_DB.query(sql)
    return repay_card


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


def get_capital_asset_by_item_no(item_no):
    sql = "select * from capital_asset where capital_asset_item_no='%s'" % item_no
    capital_asset = gc.GRANT_DB.query(sql)
    return capital_asset


def get_capital_asset_tran_by_item_no(item_no):
    sql = "select * from capital_transaction where capital_transaction_item_no='%s'" % item_no
    capital_transaction = gc.GRANT_DB.query(sql)
    return capital_transaction


def get_capital_account_by_idnum_encrypt(idnum_encrypt, channel):
    sql = "select * from `capital_account` where capital_account_idnum_encrypt='%s' and capital_account_channel='%s'" % \
          (idnum_encrypt, channel)
    capital_account = gc.GRANT_DB.query(sql)
    return capital_account


def get_capital_account_card_by_idnum_encrypt(idnum_encrypt, channel):
    sql = "select * from `capital_account_card` " \
          "inner join `capital_account` on `capital_account_id`=`capital_account_card_account_id` " \
          "where capital_account_idnum_encrypt='%s' and capital_account_channel='%s'" % \
          (idnum_encrypt, channel)
    capital_account = gc.GRANT_DB.query(sql)
    return capital_account


def create_attachment(asset_info, attachment_type, attachment_name, attachment_url):
    sql = "INSERT INTO `asset_attachment` (" \
          "`asset_attachment_asset_item_no`, `asset_attachment_type`, `asset_attachment_contract_code`, " \
          "`asset_attachment_type_text`, `asset_attachment_url`, " \
          "`asset_attachment_status`, `asset_attachment_from_system`) " \
          "VALUES ('%s', %s, '%s', '%s', '%s', 1, 'contract');" % \
          (asset_info['data']['asset']['item_no'], attachment_type, get_random_str(10), attachment_name, attachment_url)
    result = gc.GRANT_DB.insert(sql)
    return result


def create_attachment_by_item_no(item_no, attachment_type, attachment_name, attachment_url):
    sql = "INSERT INTO `asset_attachment` (" \
          "`asset_attachment_asset_item_no`, `asset_attachment_type`, `asset_attachment_contract_code`, " \
          "`asset_attachment_type_text`, `asset_attachment_url`, " \
          "`asset_attachment_status`, `asset_attachment_from_system`) " \
          "VALUES ('%s', %s, '%s', '%s', '%s', 1, 'contract');" % \
          (item_no, attachment_type, get_random_str(10), attachment_name, attachment_url)
    result = gc.GRANT_DB.insert(sql)
    return result


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


def update_last_task_by_item_no_task_type(item_no, task_types, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update task set %s where task_order_no='%s' and task_type='%s' order by task_id desc limit 1" \
          % (sql_params[:-2], item_no, task_types)
    gc.GRANT_DB.update(sql)


def get_task_by_item_no_and_task_type(item_no, task_type, task_status=None, num=None):
    """
    获取指定task内容，默认获取到最新的一个task
    :param task_status:
    :param item_no: 资产编号
    :param task_type: task类型
    :param num: 同名task可能有多个，指定获取第几个
    :return:
    """
    if task_status:
        sql = "select * from task where task_order_no='%s' and task_status='%s' order by task_id asc" % (
        item_no, task_status)
    else:
        sql = "select * from task where task_order_no='%s' order by task_id asc" % item_no
    task_list = gc.GRANT_DB.query(sql)
    if not task_list:
        return None
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


def get_msg_by_item_no_and_msg_type(item_no, msg_type, num=None):
    """
    获取指定msg内容，默认获取到最新的一个task
    :param item_no: 资产编号
    :param msg_type: task类型
    :param num: 同名task可能有多个，指定获取第几个
    :return:
    """
    sql = "select * from sendmsg where sendmsg_order_no='%s' order by sendmsg_id asc" % item_no
    msg_list = gc.GRANT_DB.query(sql)
    ret = None
    for msg in msg_list:
        if msg["sendmsg_type"] == msg_type:
            ret = deepcopy(msg)
            if not num:
                continue
            elif num == 1:
                break
            else:
                num = num - 1
    return ret


def get_capital_withdraw_by_item_no(item_no):
    sql = "select capital_withdraw_status from capital_withdraw where " \
          "capital_withdraw_item_no='{0}' order by capital_withdraw_create_at desc".format(item_no)
    withdraw_info = gc.GRANT_DB.query(sql)
    return withdraw_info


def insert_withdraw(item_no, element):
    """

    :param item_no: 资产编号
    :param element: 四要素
    :return:
    """
    sql = "INSERT INTO `withdraw` (`withdraw_merchant_id`, `withdraw_asset_item_no`, `withdraw_merchant_key`, " \
          "`withdraw_status`, `withdraw_channel`, `withdraw_version`, `withdraw_account`, `withdraw_amount`, " \
          "`withdraw_receiver_type`, `withdraw_create_at`, `withdraw_receiver_name_encrypt`, " \
          "`withdraw_receiver_account_encrypt`, `withdraw_receiver_identity_encrypt`) " \
          "VALUES (3, '%s1', '%s1_JN1', 'fail', 'tongrongmiyang', '5.1', 'tongrongmiyang', 400000, 1, " \
          "'%s', '%s', '%s', '%s')" \
          % (item_no, item_no, get_date(), element['data']['user_name_encrypt'], element['data']['bank_code_encrypt'],
             element['data']['id_number_encrypt'])
    return gc.GRANT_DB.insert(sql)


def get_asset_confirm(item, confim_type='', confim_status=''):
    sql = "select * from asset_confirm where "
    if item != '':
        sql = sql + "asset_confirm_item_no='%s' " % item
    if confim_type != '':
        sql = sql + " and asset_confirm_type='%s' " % confim_type
    if confim_status != '':
        sql = sql + " and asset_confirm_status='%s' " % confim_status
    asset_confirm_info = gc.GRANT_DB.query(sql)
    return asset_confirm_info


def insert_asset_confirm(item_no, channel, type, status):
    sql = "INSERT INTO asset_confirm (asset_confirm_item_no, asset_confirm_channel, asset_confirm_type, " \
          "asset_confirm_status, asset_confirm_memo) " \
          "VALUES ('%s', '%s', '%s', '%s', '')" \
          % (item_no, channel, type, status)
    gc.GRANT_DB.insert(sql)


def get_asset_event(item, channel, event_type=''):
    sql = "select * from asset_event where "
    if item != '':
        sql = sql + "asset_event_item_no='%s' and asset_event_channel = '%s'" % (item, channel)
    if event_type != '':
        sql = sql + "and asset_event_type='%s' " % event_type
    asset_confirm_info = gc.GRANT_DB.query(sql)
    return asset_confirm_info


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


def delete_router_capital_plan():
    date = time.strftime("%Y-%m-%d")
    sql = "delete from router_capital_plan"
    gc.GRANT_DB.delete(sql)


def insert_router_capital_plan(rule_code, amount=200000000):
    date = time.strftime("%Y-%m-%d")
    sql = "INSERT INTO router_capital_plan(router_capital_plan_date, router_capital_plan_label, " \
          "router_capital_plan_desc, router_capital_plan_amount, router_capital_plan_update_memo, " \
          "router_capital_plan_create_at, router_capital_plan_update_at) " \
          "VALUES ('%s', '%s', '%s', '%s', '自动化脚本插入', NOW(), NOW())" \
          % (date, rule_code, rule_code, amount)
    gc.GRANT_DB.insert(sql)


def update_router_capital_plan_by_rule_code(rule_code, amount=200000000):
    date = time.strftime("%Y-%m-%d")
    sql = "update router_capital_plan set router_capital_plan_amount = '%s' where router_capital_plan_label = '%s'" \
          "and router_capital_plan_date = '%s'" % (amount, rule_code, date)
    gc.GRANT_DB.update(sql)


def delete_router_load_total():
    date = time.strftime("%Y-%m-%d")
    sql = "delete from router_load_total"
    gc.GRANT_DB.delete(sql)


def insert_router_load_total(rule_code, routed_amount=0, imported_amount=0):
    date = time.strftime("%Y-%m-%d")
    sql = "INSERT INTO router_load_total (router_load_total_rule_code, router_load_total_count, " \
          "router_load_total_routed_amount, router_load_total_imported_amount, router_load_total_route_day) " \
          "VALUES ('%s', 1, '%s', '%s', '%s')" \
          % (rule_code, routed_amount, imported_amount, date)
    gc.GRANT_DB.insert(sql)


def update_router_load_total(rule_code, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "" + key + "='" + str(value) + "', "
    sql = "update router_load_total set %s " \
          "where router_load_total_rule_code ='%s' and router_load_total_route_day = '%s'" \
          % (sql_params[:-2], rule_code, time.strftime("%Y-%m-%d"))
    gc.GRANT_DB.update(sql)


def get_router_capital_rule(rule_code):
    sql = "select * from router_capital_rule where router_capital_rule_code = '%s'" % rule_code
    result = gc.GRANT_DB.query(sql)
    return result


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


def delete_router_capital_rule():
    sql = "delete from router_capital_rule"
    gc.GRANT_DB.delete(sql)


def insert_router_capital_rule(channel, period_count, period_type, rule_code, rule_limit_type, overflow_rate=0):
    sql = "INSERT INTO router_capital_rule (router_capital_rule_code, router_capital_rule_desc, " \
          "router_capital_rule_family, router_capital_rule_type, router_capital_rule_weight, " \
          "router_capital_rule_content, router_capital_rule_status, router_capital_rule_create_at, " \
          "router_capital_rule_update_at, router_capital_rule_limit_type, router_capital_rule_allow_overflow_rate) " \
          "VALUES ('%s', '%s', '%s', 'supply', 0, " \
          "'{\\\"name\\\":\\\"%s\\\",\\\"rules\\\":[{\\\"name\\\":\\\"%s期产品\\\",\\\"rule\\\":\\\"asset.periodType==\\\'%s\\\' and asset.periodCount==%s\\\"}],\\\"output\\\":{\\\"key\\\":\\\"channel\\\",\\\"value\\\":\\\"%s\\\"}}', " \
          "'release', NOW(), NOW(), '%s', '%s')" \
          % (rule_code, rule_code, channel, rule_code, period_count, period_type, period_count, channel,
             rule_limit_type, overflow_rate)
    gc.GRANT_DB.insert(sql)


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


def delete_router_weight():
    sql = "delete from router_weight"
    gc.GRANT_DB.delete(sql)


def insert_router_weight(channel, rule_code, weight=2000, status='active', first_route_status='active',
                         second_route_status='active'):
    sql = "INSERT INTO router_weight (router_weight_type, router_weight_code, router_weight_desc, " \
          "router_weight_rule_content, router_weight_value, router_weight_status, router_weight_first_route_status, " \
          "router_weight_second_route_status, router_weight_create_at, router_weight_update_at, " \
          "router_weight_create_name, router_weight_update_name) " \
          "VALUES ('channel', '%s', '%s', 'finalRuleList.contains(\\'%s\\')', '%s', " \
          "'%s', '%s', '%s', NOW(), NOW(), '自动化脚本插入', '自动化脚本插入')" \
          % (channel, rule_code, rule_code, weight, status, first_route_status, second_route_status)
    gc.GRANT_DB.insert(sql)


def open_sendmsg_by_item_no(item_no, sendmsg_type):
    sql = "update sendmsg set sendmsg_status='open' where sendmsg_order_no = '%s' and sendmsg_type = '%s'" % (
        item_no, sendmsg_type)
    gc.GRANT_DB.update(sql)


def get_asset_import_data_by_item_no(item_no):
    task_info = get_task_by_item_no_and_task_type(item_no, 'AssetImport')
    asset_info = None
    if task_info is not None:
        asset_info = json.loads(task_info['task_request_data'])['data']
    return asset_info


def update_asset_by_item_no(item_no, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "" + key + "='" + value + "', "
    sql = "update asset set %s where asset_item_no ='%s'" % (sql_params[:-2], item_no)
    gc.GRANT_DB.update(sql)


def update_router_capital_plan_amount(amount, today, channel):
    sql = "UPDATE router_capital_plan set router_capital_plan_amount={} where router_capital_plan_label " \
          "like '%{}%' and router_capital_plan_date='{}'; ".format(amount, channel, today)
    gc.GRANT_DB.update(sql)


def update_router_capital_plan_amount_all_to_zero(capital_channel):
    today = time.strftime("%Y-%m-%d", time.localtime())
    sql = "UPDATE router_capital_plan set router_capital_plan_amount=0  where router_capital_plan_label " \
          " not like '%{}%' and router_capital_plan_date='{}';".format(capital_channel, today)
    gc.GRANT_DB.update(sql)


def update_router_cp_amount_all_to_zero():
    today = time.strftime("%Y-%m-%d", time.localtime())
    sql = "UPDATE router_capital_plan set router_capital_plan_amount=0  where router_capital_plan_date='%s'; " % today
    gc.GRANT_DB.update(sql)


def update_all_channel_amount():
    today = time.strftime("%Y-%m-%d", time.localtime())
    sql = "UPDATE router_capital_plan set router_capital_plan_amount=3333333333 where router_capital_plan_date='%s';" \
          % today
    gc.GRANT_DB.update(sql)


def update_router_weight_inactive(capital_channel):
    sql = "update router_weight set router_weight_status='inactive' where router_weight_code='%s'; " % capital_channel
    gc.GRANT_DB.update(sql)


def update_router_weight_active(capital_channel):
    sql = "update router_weight set router_weight_status='active' where router_weight_code='%s'; " % capital_channel
    gc.GRANT_DB.update(sql)


def update_router_weight_first_route_status_inactive(capital_channel):
    sql = "update router_weight set router_weight_first_route_status='inactive' where router_weight_code='%s'; " \
          % (capital_channel)
    gc.GRANT_DB.update(sql)


def update_router_weight_first_route_status_active(capital_channel):
    sql = "update router_weight set router_weight_first_route_status='active' where router_weight_code='%s'; " \
          % (capital_channel)
    gc.GRANT_DB.update(sql)


def update_router_weight_by_channel(channel, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update router_weight set %s where router_weight_code='%s'" % (sql_params[:-2], channel)
    gc.GRANT_DB.update(sql)


def delete_capital_rule_code(capital_channel):
    sql = "DELETE FROM router_capital_rule " \
          "WHERE router_capital_rule_code like '{}_%'".format(capital_channel)
    gc.GRANT_DB.delete(sql)


def router_capital_rule_notrelease(capital_channel):
    sql = "update router_capital_rule set router_capital_rule_status='draft' " \
          "where router_capital_rule_code like '{}_%'".format(capital_channel)
    gc.GRANT_DB.update(sql)


def router_capital_rule_release(capital_channel):
    sql = "update router_capital_rule set router_capital_rule_status='release' where router_capital_rule_code in" \
          "('%s_6month','%s_6m','%s_12month','%s_12m'); " % (capital_channel, capital_channel, capital_channel,
                                                             capital_channel)
    gc.GRANT_DB.update(sql)


def get_asset_tran_total_amount(item_no, type=None):
    sql = "select sum(asset_tran_amount) as amount from asset_tran " \
          "where asset_tran_asset_item_no = '%s' and asset_tran_category != 'grant'" % item_no
    if type is not None:
        sql += " and asset_tran_category = '%s'" % type
    result = gc.GRANT_DB.query(sql)
    return result[0]['amount']


def get_capital_tran_total_amount(item_no, type=None):
    sql = "select sum(capital_transaction_origin_amount) as amount from capital_transaction " \
          "where capital_transaction_item_no = '%s'" % item_no
    if type is not None:
        sql += " and capital_transaction_type = '%s'" % type
    result = gc.GRANT_DB.query(sql)
    return result[0]['amount']


def get_asset_tran_period_amount_lt(item_no):
    sql = "select asset_tran_period as period, sum(asset_tran_amount) as amount from asset_tran " \
          "where asset_tran_asset_item_no = '%s' and asset_tran_category != 'grant' " \
          "group by asset_tran_period" % item_no
    result = gc.GRANT_DB.query(sql)
    return result


def get_capital_tran_period_amount_lt(item_no):
    sql = "select capital_transaction_period as period, sum(capital_transaction_origin_amount) as amount " \
          "from capital_transaction where capital_transaction_item_no = '%s' " \
          "group by capital_transaction_period" % item_no
    result = gc.GRANT_DB.query(sql)
    return result


def get_asset_import_data_from_sendmsg_by_item_no(item_no):
    msg_info = get_msg_by_item_no_and_msg_type(item_no, 'AssetImportSync')
    asset_info = json.loads(msg_info['sendmsg_content'])["body"]
    return asset_info


def get_capital_account_by_item_no(item_no):
    sql = "select * from capital_account where capital_account_item_no = '%s'" % item_no
    result = gc.GRANT_DB.query(sql)
    return result


def get_capital_account_by_item_no_channel(four_element, channel):
    sql = "select * from capital_account  where capital_account_idnum_encrypt ='%s' and " \
          "capital_account_card_number_encrypt='%s'and capital_account_name_encrypt='%s' and " \
          "capital_account_mobile_encrypt='%s'  and capital_account_channel ='%s'; " \
          % (four_element['data']['id_number_encrypt'], four_element["data"]["bank_code_encrypt"],
             four_element["data"]["user_name_encrypt"], four_element["data"]["phone_number_encrypt"], channel)
    result = gc.GRANT_DB.query(sql)
    return result


def get_capital_account_step_by_item_no_way(four_element, channel, item_no, way):
    sql = "select * from capital_account_step where capital_account_step_account_id in (select capital_account_id " \
          "from capital_account  where capital_account_idnum_encrypt ='%s' and capital_account_card_number_encrypt='%s'" \
          "and capital_account_name_encrypt='%s' and capital_account_mobile_encrypt='%s'and " \
          "capital_account_channel ='%s') and capital_account_step_item_no='%s' and capital_account_step_way='%s';" \
          % (four_element['data']['id_number_encrypt'], four_element["data"]["bank_code_encrypt"],
             four_element["data"]["user_name_encrypt"], four_element["data"]["phone_number_encrypt"], channel, item_no, way)
    result = gc.GRANT_DB.query(sql)
    return result


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


def set_withdraw_order_status(item_no, status):
    sql = "update withdraw_order set withdraw_order_status = '%s', withdraw_order_finish_at = NOW()" \
          " where withdraw_order_asset_item_no = '%s'" % (status, item_no)
    gc.GRANT_DB.update(sql)


def set_withdraw_record_status(item_no, status):
    sql = "update withdraw_record set withdraw_record_status='%s',withdraw_record_finish_at = NOW() where" \
          " withdraw_record_order_no in (select withdraw_order_no from withdraw_order where " \
          "withdraw_order_asset_item_no = '%s') order by withdraw_record_create_at desc limit 1; " % (status, item_no)
    gc.GRANT_DB.update(sql)


def update_withdraw_code_msg(resp_code, resp_message, item_no):
    sql = "update withdraw_record set withdraw_record_resp_code='%s', withdraw_record_resp_message='%s' " \
          "where withdraw_record_order_no in (select withdraw_order_no from withdraw_order where " \
          "withdraw_order_asset_item_no ='%s') order by withdraw_record_create_at desc limit 1;" \
          % (resp_code, resp_message, item_no)
    gc.GRANT_DB.update(sql)


def get_sendmsg(item_no, msg_type):
    sql = "select * from sendmsg where sendmsg_order_no = '%s' and sendmsg_type = '%s'" % (item_no, msg_type)
    result = gc.GRANT_DB.query(sql)
    return result


def insert_router_load_record(**kwargs):
    sql_keys = ""
    sql_values = ""
    for key, value in kwargs.items():
        sql_keys += "`" + key + "`, "
        sql_values += "'" + str(value) + "', "
    sql = "INSERT INTO `router_load_record` (%s) VALUES (%s);" % (sql_keys[:-2], sql_values[:-2])
    gc.GRANT_DB.do_sql(sql)



def get_router_load_record_by_key(key, rule_code=None):
    if rule_code:
        sql = "select * from router_load_record where router_load_record_key = '%s' " \
              "and router_load_record_rule_code = '%s'" % (key, rule_code)
    else:
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


def update_asset_create_time(item_no):
    update_time = "update gbiz%s.asset set asset_create_at=DATE_SUB(NOW(),INTERVAL 5 hour)   where asset_item_no='%s';" \
                  % (gc.ENV, item_no)
    gc.GRANT_DB.update(update_time)


def update_capital_blacklist_expired_at(card, channel):
    sql = "update capital_blacklist set capital_blacklist_expired_at=DATE_SUB(now(), interval 10 minute) where " \
          "capital_blacklist_value='%s' and capital_blacklist_channel='%s';" \
          "; " % (card, channel)
    gc.GRANT_DB.update(sql)


def update_withdraw_order(item_no, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update withdraw_order set %s where withdraw_order_asset_item_no='%s'" % (sql_params[:-2], item_no)
    gc.GRANT_DB.update(sql)


def insert_asset(item_no, four_element, channel, status):
    sql = "INSERT INTO asset (asset_item_no, asset_type, asset_sub_type, asset_period_type, asset_period_count,  " \
          "asset_cmdb_product_number, asset_create_at,  asset_grant_at, asset_effect_at, asset_actual_grant_at, " \
          "asset_due_at, asset_payoff_at, asset_update_at, asset_from_system, asset_status, asset_principal_amount, " \
          "asset_granted_principal_amount, asset_loan_channel, asset_alias_name, asset_interest_amount, " \
          "asset_fee_amount, asset_balance_amount, asset_repaid_amount, asset_total_amount, asset_version, " \
          "asset_interest_rate, asset_from_system_name, asset_owner, asset_idnum_encrypt, asset_from_app) " \
          "VALUES ('%s', 'paydayloan', 'multiple', 'month', 12, '', '2021-05-06 15:37:15', '2021-05-06 15:37:14', " \
          "'2021-05-06 15:38:20', '2021-05-06 15:38:20', '2022-05-06 00:00:00', '2022-05-06 00:00:00', '2021-05-06 " \
          "16:17:30', 'strawberry', '%s', 900000, 900000, '%s', 'S2021050682555764510', 24564, 52260, 0, 976824, " \
          "976824, 1620289033760, 5.000, '重庆草莓', 'KN', '%s', '重庆草莓');" \
          % (item_no, status, channel, four_element['data']['id_number_encrypt'])
    gc.GRANT_DB.insert(sql)


def insert_asset_individual(item_no, four_element):
    sql = "INSERT INTO `asset_individual` (`asset_individual_type`, `asset_individual_id_addr`, " \
          "`asset_individual_id_type`, `asset_individual_id_post_code`, `asset_individual_gender`, " \
          "`asset_individual_education`, `asset_individual_income_lft`, `asset_individual_income_rgt`, " \
          "`asset_individual_credit_type`, `asset_individual_credit_score`, `asset_individual_residence`, " \
          "`asset_individual_corp_name`, `asset_individual_corp_tel`, `asset_individual_corp_trade`, " \
          "`asset_individual_residence_tel`, `asset_individual_residence_status`, `asset_individual_workplace`, " \
          "`asset_individual_marriage`, `asset_individual_duty`, `asset_individual_relative_relation`, " \
          "`asset_individual_enrollment_time`, `asset_individual_school_place`, `asset_individual_school_name`, " \
          "`asset_individual_create_at`, `asset_individual_create_user_name`, `asset_individual_update_at`, " \
          "`asset_individual_update_user_name`, `asset_individual_second_relative_relation`, " \
          "`asset_individual_name_encrypt`, `asset_individual_idnum_encrypt`, `asset_individual_tel_encrypt`, " \
          "`asset_individual_account_name_encrypt`, `asset_individual_mate_name_encrypt`, " \
          "`asset_individual_mate_tel_encrypt`, `asset_individual_relative_name_encrypt`, " \
          "`asset_individual_relative_tel_encrypt`, `asset_individual_workmate_name_encrypt`, " \
          "`asset_individual_workmate_tel_encrypt`, `asset_individual_second_relative_name_encrypt`, " \
          "`asset_individual_second_relative_tel_encrypt`, `asset_individual_asset_item_no`, " \
          "`asset_individual_nation`, `asset_individual_email`, `asset_individual_income_source`, " \
          "`asset_individual_province_code`, `asset_individual_city_code`, `asset_individual_province_name`, " \
          "`asset_individual_city_name`) " \
          "VALUES ('borrow', '吉林省通榆县团结乡建设村四社社', 1, '', 'f', 9, 5001, 8000, 0, 0, '吉林省白城市通榆县小城花园21栋楼', " \
          "'中国平安人寿保险股份有限公司碧水东城', '', 8, '', 0, '吉林省白城市通榆县碧水东城商业街', 2, 0, '4', '1000-01-01 00:00:00', '', '', " \
          "'2021-05-07 09:34:13', 'system', '2021-05-07 09:34:13', 'system', '8', '%s', '%s', '%s', " \
          "'enc_04_2213800_675', '', '', 'enc_04_259710_725', 'enc_01_11006859400_801', '', '', " \
          "'enc_04_3394563211180640256_369', 'enc_01_18881607700_272', '%s', '汉', '15834645656@139.com', 1, 220000, " \
          "220800, '吉林省', '白城市')" \
          % (four_element['data']['user_name_encrypt'],
             four_element['data']['id_number_encrypt'],
             four_element['data']['phone_number_encrypt'],
             item_no)
    gc.GRANT_DB.insert(sql)


def get_four_element_by_item_no(item_no):
    asset_card = get_asset_card(asset_card_asset_item_no=item_no, asset_card_type="receive")[0]
    four_element = {
        "code": 0,
        "message": "success",
        "data": {
            "bank_code": decrypt_data(asset_card["asset_card_account_card_number_encrypt"]),
            "phone_number": decrypt_data(asset_card["asset_card_account_tel_encrypt"]),
            "user_name": decrypt_data(asset_card["asset_card_account_name_encrypt"]),
            "id_number": decrypt_data(asset_card["asset_card_account_idnum_encrypt"]),
            "bank_code_encrypt": asset_card["asset_card_account_card_number_encrypt"],
            "id_number_encrypt": asset_card["asset_card_account_idnum_encrypt"],
            "phone_number_encrypt": asset_card["asset_card_account_tel_encrypt"],
            "user_name_encrypt": asset_card["asset_card_account_name_encrypt"]
        }
    }
    return four_element


def wait_task_appear(item_no, task_type, wait_time=120):
    result = False
    for i in range(wait_time):
        task = get_task_by_item_no_and_task_type(item_no, task_type, 'open')
        if task is not None and len(task) > 0:
            result = True
            break
        else:
            time.sleep(1)
    return result


def get_latest_circuit_break_record(name):
    sql = "select * from circuit_break_record where circuit_break_record_name='%s' " \
          "order by circuit_break_record_id desc limit 1" % name
    result = gc.GRANT_DB.query(sql)
    return result


def get_circuit_break_action(circuit_break_id, action_type):
    sql = "select * from circuit_break_action where circuit_break_action_circuit_break_id=%s " \
          "and circuit_break_action_type = '%s'" % (circuit_break_id, action_type)
    result = gc.GRANT_DB.query(sql)
    return result


def clear_circuit_break_record():
    sql = "update circuit_break_record set circuit_break_record_status='close' " \
          "where circuit_break_record_status != 'close'"
    result = gc.GRANT_DB.update(sql)
    return result


def clear_terminated_task():
    sql = "update task set task_status='close', task_memo='自动化测试脚本更新' where task_status = 'terminated'"
    result = gc.GRANT_DB.update(sql)
    return result


def update_asset_due_bill_no(item_no):
    sql = "update asset_loan_record set asset_loan_record_due_bill_no=MD5(rand()*10000) where " \
          "asset_loan_record_asset_item_no='%s';" % (item_no)
    result = gc.GRANT_DB.update(sql)
    return result


def update_capital_account_step_update_time(four_element, channel, item_no):
    sql = "update capital_account_step set capital_account_step_update_at= DATE_SUB(now(), interval 2 DAY) where " \
          "capital_account_step_account_id in (select capital_account_id from capital_account  where " \
          "capital_account_idnum_encrypt ='%s' and capital_account_card_number_encrypt='%s' and " \
          "capital_account_name_encrypt='%s' and capital_account_mobile_encrypt='%s' " \
          "and capital_account_channel ='%s') and capital_account_step_item_no='%s';" \
          % (four_element['data']['id_number_encrypt'], four_element["data"]["bank_code_encrypt"],
             four_element["data"]["user_name_encrypt"], four_element["data"]["phone_number_encrypt"], channel, item_no)
    result = gc.GRANT_DB.update(sql)
    return result


def update_asset_individual_extend_info(item_no):
    '''
    目前就jiexin_taikang资金方使用
    :param item_no:
    :return:
    '''
    sql = "update asset_individual_extend set asset_individual_extend_info='{\"agreement\":\"Y\",\"idnum_begin_day\":" \
          "\"2016-09-23\",\"idnum_expire_day\":\"长期\",\"idnum_cert_office\":\"榆中县公安局\",\"address_district_code\":" \
          "\"12345678\",\"residence_district\":\"榆中县\",\"device_ip\":\"192.168.1.109\",\"device_mac\":" \
          "\"00:fdaf:fdas:00\",\"device_sys\":\"android\",\"face_recog_score\":\"12\",\"channel_risk_level\":\"C\"," \
          "\"a_card_level_score\":\"594\"}' where asset_individual_extend_asset_item_no='%s';" %(item_no)
    gc.GRANT_DB.update(sql)


def create_task_loancreditcancel(asset_item_no):
    '''
    目前仅裕民中保使用
    :param asset_item_no:
    :return:
    '''
    sql = "INSERT INTO `task` ( `task_order_no`, `task_type`, `task_request_data`, `task_response_data`, `task_memo`, " \
          "`task_status`, `task_next_run_at`, `task_create_at`, `task_update_at`, `task_version`, `task_priority`, " \
          "`task_retrytimes`)VALUES ('%s', 'LoanCreditCancel', '{\n  \"cancelable\" : false,\n  " \
          "\"asset_item_no\" : \"%s\",\n  \"loan_channel\" : \"yumin_zhongbao\",\n  \"workflow_node\" :" \
          " \"LoanCreditCancel\"\n}', '', '', 'open', " \
          "now(), now(), now(), 0, 1, 0);" % (asset_item_no, asset_item_no)
    result = gc.GRANT_DB.insert(sql)
    return result

def create_asset_event(asset_item_no, channel, asset_event_no, asset_event_memo='裕民中保授信成功',asset_event_type='YMZB_CREDIT_SUCCESS'):
    '''
    创建事件表记录
    '''
    if asset_event_no:
        pass
    else:
        asset_event_no = "ym" + get_random_str(10)
    sql = "INSERT INTO `asset_event` ( `asset_event_item_no`, `asset_event_channel`, `asset_event_no`, " \
          "`asset_event_create_at`, `asset_event_update_at`, `asset_event_memo`, `asset_event_type`) VALUES " \
          "('%s', '%s', '%s', now(), now(), '%s', '%s');" % (asset_item_no, channel, asset_event_no,
                                                             asset_event_memo, asset_event_type)
    result = gc.GRANT_DB.insert(sql)
    return result

def update_asset_loan_record_extend_info(item_no):
    '''
    目前众邦昊悦润楼结清证明时使用
    '''
    sql = "update asset_loan_record set asset_loan_record_extend_info='{\n  \"openId\" : \"123456789test001\"}' where " \
          "asset_loan_record_asset_item_no='%s';" %(item_no)
    gc.GRANT_DB.update(sql)
