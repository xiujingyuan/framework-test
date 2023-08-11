import common.global_const as gc


# 检查 clean_final 会用到
def get_final_all(item_no, period, type):
    sql = "select ci.final_no,ci.asset_item_no,cl.period,cl.biz_type,cl.biz_sub_type,cl.asset_cmdb_no," \
          "cl.asset_loan_channel,cl.compensated,cl.partly,ci.withhold_result_channel," \
          "ci.amount_type,cl.amount as 'total_amount',ci.origin_amount,ci.amount," \
          "cl.actual_finish_time,cl.expect_finish_time,cl.expect_compensate_time,cl.ref_final_no " \
          "from {0}.clean_final_item ci " \
          "left join {0}.clean_final cl on ci.final_no = cl.final_no " \
          "where ci.asset_item_no = '{1}' " \
          "and cl.period = {2} and cl.biz_type = '{3}' order by ci.amount_type,ci.amount" \
        .format(gc.DCS_DB_NAME, item_no, period, type)
    clean_final = gc.DCS_DB.query(sql)
    if clean_final:
        return clean_final
    else:
        return None


def get_final_one(item_no, period, type):
    sql = "select * from {0}.clean_final where asset_item_no = '{1}' and period = {2} and biz_type = '{3}' " \
        .format(gc.DCS_DB_NAME, item_no, period, type)
    clean_final = gc.DCS_DB.query(sql)
    if clean_final:
        return clean_final
    else:
        return None


# ci.amount的类型为bigint，mysql的sum返回的结果是string，需要转化一下 CAST(SUM(ci.amount) AS SIGNED ) AS amount
def get_final_sum(item_no, period, type):
    sql = "select ci.final_no,ci.asset_item_no,cl.period,cl.biz_type,cl.biz_sub_type,cl.asset_cmdb_no," \
          "cl.asset_loan_channel,cl.compensated,cl.partly,ci.withhold_result_channel," \
          "ci.amount_type,cl.amount as 'total_amount',ci.origin_amount,CAST(SUM(ci.amount) AS SIGNED ) AS amount," \
          "cl.actual_finish_time,cl.expect_finish_time,cl.expect_compensate_time " \
          "from {0}.clean_final_item ci " \
          "left join {0}.clean_final cl on ci.final_no = cl.final_no " \
          "where ci.asset_item_no = '{1}' " \
          "and cl.period = {2} and cl.biz_type = '{3}' group by ci.amount_type order by ci.amount_type" \
        .format(gc.DCS_DB_NAME, item_no, period, type)
    clean_final = gc.DCS_DB.query(sql)
    if clean_final:
        return clean_final
    else:
        return None


# 获取 clean_pending 会用到
def get_pending_all(item_no, period, type):
    sql = "select ci.asset_item_no,cl.period,cl.biz_type," \
          "cl.asset_loan_channel,ci.withhold_result_channel," \
          "ci.amount_type,ci.origin_amount,ci.amount," \
          "cl.actual_finish_time,cl.expect_finish_time " \
          "from {0}.clean_pending_item ci " \
          "left join {0}.clean_pending cl on ci.batch_no = cl.batch_no " \
          "where ci.asset_item_no = '{1}' " \
          "and cl.period = {2} and cl.biz_type = '{3}' order by ci.amount_type" \
        .format(gc.DCS_DB_NAME, item_no, period, type)
    clean_pending = gc.DCS_DB.query(sql)
    if clean_pending:
        return clean_pending
    else:
        return None


# 获取 clean_trans 会用到
def get_trans_all(item_no, period, type):
    sql = "select ci.* from {0}.clean_clearing_trans ci " \
          "left join {0}.clean_final cl on ci.final_no = cl.final_no " \
          "where ci.item_no = '{1}' " \
          "and cl.period = {2} and cl.biz_type = '{3}' order by ci.amount_type,ci.amount " \
        .format(gc.DCS_DB_NAME, item_no, period, type)
    clean_trans = gc.DCS_DB.query(sql)
    if clean_trans:
        return clean_trans
    else:
        return None


# 获取 clean_capital_settlement_notify_tran 会用到
def get_clean_capital_settlement_notify_tran(item_no, period, status):
    sql = "select ci.* from {0}.clean_capital_settlement_notify_tran ci " \
          "where ci.asset_item_no = '{1}' " \
          "and ci.period = {2} and amount_type='principal' and status='{3}' " \
        .format(gc.DCS_DB_NAME, item_no, period, status)
    notify_tran = gc.DCS_DB.query(sql)
    if notify_tran:
        return notify_tran
    else:
        return None


# 更新clean_capital_settlement_notify_tran的版本号
def update_notify_tran_at_dcs(item_no, version, period):
    sql = 'update {0}.clean_capital_settlement_notify_tran set version ="{1}"  ' \
          'where asset_item_no="{2}" and period = {3}' \
        .format(gc.DCS_DB_NAME, version, item_no, period)
    gc.DCS_DB.update(sql)


def get_trans_one(item_no, period):
    sql = "select * from {0}.clean_clearing_trans where item_no = '{1}' and period = {2} " \
        .format(gc.DCS_DB_NAME, item_no, period, )
    clean_trans = gc.DCS_DB.query(sql)
    if clean_trans:
        return clean_trans
    else:
        return None


# 获取清分规则
def get_clearing_rule_value(no, product_code=''):
    if product_code:
        sql = 'select value from {0}.clean_clearing_rule where support_rule_no like "%{1}%" and product_code like "%{2}%" and status = "active" '.format(
            gc.DCS_DB_NAME, no, product_code)
    else:
        sql = 'select value from {0}.clean_clearing_rule where support_rule_no like "%{1}%" and product_code="" and status = "active" '.format(
            gc.DCS_DB_NAME, no)
    clearing_rule = gc.DCS_DB.query(sql)
    if clearing_rule:
        return clearing_rule[0]["value"]
    else:
        return None


# 更新dcs的task的再次执行时间
def update_task_at_dcs(task_type):
    sql = 'update {0}.clean_task set task_status = "open",task_next_run_at = date_sub(now(), INTERVAL 20 MINUTE) where task_status != "close" and task_type = "{1}"' \
        .format(gc.DCS_DB_NAME, task_type)
    gc.DCS_DB.update(sql)


# 更新dcs的task的再次执行时间
def update_dcs_china_task_next_run_at(task_priority=1, status='open'):
    if status == 'open':
        sql1 = "update clean_task set task_priority='%s',task_status = 'open',task_next_run_at =date_sub(now(), INTERVAL 60 MINUTE) where task_status='open'" % task_priority
        task = gc.DCS_DB.update(sql1)
        sql2 = "update clean_task set task_status = 'close' where task_create_at<current_date and task_status = 'open' "
        task = gc.DCS_DB.update(sql2)
    else:
        sql = "update clean_task set task_priority='%s',task_status = 'close' where task_status='open'" % task_priority
        task = gc.DCS_DB.update(sql)
    return task


# 更新dcs的task的再次执行时间
def update_task_at_dcs_by_order_no(item_no):
    sql = 'update {0}.clean_task set task_status = "open",task_next_run_at =date_sub(now(), INTERVAL 20 MINUTE) ' \
          'where task_status != "close" and task_order_no like "%{1}%" ' \
        .format(gc.DCS_DB_NAME, item_no)
    gc.DCS_DB.update(sql)


# 更新clean_withdraw_order的tally_no
def update_clean_withdraw_order_tally_no():
    sql = 'UPDATE  clean_withdraw_order  SET tally_no= concat(tally_no,"_1")  WHERE create_at>CURRENT_DATE' \
        .format(gc.DCS_DB_NAME)
    gc.DCS_DB.update(sql)


# 更新dcs的task的再次执行时间
def update_clean_clearing_trans(item_no):
    sql = 'update {0}.clean_task set task_status = "open",task_next_run_at =date_sub(now(), INTERVAL 20 MINUTE) where task_status != "close" and task_order_no = "{1}"' \
        .format(gc.DCS_DB_NAME, item_no)
    gc.DCS_DB.update(sql)


# 获取task的执行情况
def get_task_memo_dcs(task_type, order_no):
    sql = 'select * from {0}.clean_task where task_type = "{1}" and task_order_no = "{2}"  order by task_id DESC LIMIT 1' \
        .format(gc.DCS_DB_NAME, task_type, order_no)
    task_memo = gc.DCS_DB.query(sql)
    if task_memo:
        return task_memo[0]
    else:
        return None


def get_task_dcs(task_type, order_no, task_request_data="N"):
    if task_request_data == "N":
        sql = 'select task_id from {0}.clean_task where task_type = "{1}" and task_order_no = "{2}" order by task_id desc ' \
            .format(gc.DCS_DB_NAME, task_type, order_no)
        task = gc.DCS_DB.query(sql)
    elif task_request_data == "Settlement":
        sql = 'select task_id from {0}.clean_task where task_type = "{1}" and task_create_at>curdate() order by task_id desc '.format(
            gc.DCS_DB_NAME,
            task_type)
        task = gc.DCS_DB.query(sql)
    else:
        sql = 'select task_id from {0}.clean_task where task_type = "{1}" and task_request_data like "%{2}%" order by task_id desc ' \
            .format(gc.DCS_DB_NAME, task_type, order_no)
        task = gc.DCS_DB.query(sql)
    if task:
        return task
    else:
        return None


def get_task_dcs_by_order_no_and_type(task_type, order_no):
    sql = 'select task_id from {0}.clean_task where task_type = "{1}" and task_order_no= "{2}" and task_status="open" order by task_id desc ' \
        .format(gc.DCS_DB_NAME, task_type, order_no)
    task = gc.DCS_DB.query(sql)
    if task:
        return task
    else:
        return None


def get_open_task_dcs_by_order_no(task_type, order_no):
    sql = 'select task_response_data from {0}.clean_task where task_type = "{1}" and task_order_no= "{2}" and task_status="open" order by task_id desc ' \
        .format(gc.DCS_DB_NAME, task_type, order_no)
    task = gc.DCS_DB.query(sql)
    if task:
        return task
    else:
        return None


def get_task_dcs_close(task_type, order_no, task_request_data="N"):
    if task_request_data == "N":
        sql = 'select * from {0}.clean_task where task_type = "{1}" and task_status != "close" and task_order_no = "{2}" order by task_id desc ' \
            .format(gc.DCS_DB_NAME, task_type, order_no)
        task_close = gc.DCS_DB.query(sql)
    elif task_request_data == "Settlement":
        sql = 'select * from {0}.clean_task where task_type = "{1}" and task_status != "close" and task_create_at>curdate() order by task_id desc ' \
            .format(gc.DCS_DB_NAME, task_type)
        task_close = gc.DCS_DB.query(sql)
    else:
        sql = 'select * from {0}.clean_task where task_type = "{1}" and task_status != "close" and task_request_data like "%{2}%" order by task_id desc ' \
            .format(gc.DCS_DB_NAME, task_type, order_no)
        task_close = gc.DCS_DB.query(sql)
    if task_close:
        return task_close
    else:
        return None


# 获取四平提前结清的本金
def get_slsp_early_amount(item_no, amount_type):
    sql = "select sum(cfi.amount) as amount from {0}.clean_final cf " \
          "inner join {0}.clean_final_item cfi on cf.final_no = cfi.final_no " \
          "where cf.asset_item_no = '{1}' and cf.biz_sub_type = 'advance_repay' " \
          "and cfi.amount_type = '{2}' ".format(gc.DCS_DB_NAME, item_no, amount_type)
    result_list = gc.DCS_DB.query(sql)
    if result_list:
        return result_list[0]["amount"]
    else:
        return None


# 检查 clean_early_settlement
def get_early_settlement(item_no, period):
    sql = "select * from {0}.clean_early_settlement where asset_item_no = '{1}' and period = {2} " \
        .format(gc.DCS_DB_NAME, item_no, period)
    result_list = gc.DCS_DB.query(sql)
    if result_list:
        return result_list[0]
    else:
        return None


# 检查 clean_capital_settlement_pending
def get_settlement_pending(item_no, period, type):
    sql = "select * from {0}.clean_capital_settlement_pending where asset_item_no = '{1}' and period = {2} " \
          "and amount_type='{3}' ".format(gc.DCS_DB_NAME, item_no, period, type)
    result_list = gc.DCS_DB.query(sql)
    if result_list:
        return result_list[0]
    else:
        return None


# 检查 clean_buyback
def get_buyback_dcs(item_no, period, channel):
    sql = 'select * from {0}.clean_buyback where asset_item_no = "{1}" and period = {2} and loan_channel = "{3}"' \
        .format(gc.DCS_DB_NAME, item_no, period, channel)
    clean_buyback = gc.DCS_DB.query(sql)
    if clean_buyback:
        return clean_buyback
    else:
        return None


# 删除数据
def delete_data_dcs(item_no, period):
    sql1 = 'delete from {0}.clean_clearing_trans where item_no="{1}" ' \
           'and final_no like "%_new" and final_no not like "%_{2}_new"' \
        .format(gc.DCS_DB_NAME, item_no, period)
    sql2 = 'delete from {0}.clean_final where asset_item_no="{1}" ' \
           'and final_no like "%_new" and final_no not like "%_{2}_new"' \
        .format(gc.DCS_DB_NAME, item_no, period)
    gc.DCS_DB.update(sql1)
    gc.DCS_DB.update(sql2)


# 获取清分规则
def get_clearing_rule(db_evn, no):
    sql = 'select value from {0}.clean_clearing_rule where no = "{1}" and status = "active" '.format(db_evn, no)
    clearing_rule = gc.DCS_DB.query(sql)
    if clearing_rule:
        return clearing_rule[0]["value"]
    else:
        return None


# 获取回购信息
def get_buyback(db_evn, item_no, period, channel):
    sql = 'select * from {0}.clean_buyback where asset_item_no = "{1}" and period = {2} and loan_channel = "{3}"' \
        .format(db_evn, item_no, period, channel)
    clean_buyback = gc.DCS_DB.query(sql)
    if clean_buyback:
        return clean_buyback
    else:
        return None


# 获取当前时间
def get_db_time():
    sql = 'select now()'
    db_time = gc.DCS_DB.query(sql)
    return db_time


# 删除数据
def delete_pending_dcs(item_no, period):
    if len(period) > 1:
        sql1 = 'delete from {0}.clean_pending where asset_item_no="{1}" and period in {2} '.format(gc.DCS_DB_NAME,
                                                                                                   item_no, period)
    else:
        sql1 = 'delete from {0}.clean_pending where asset_item_no="{1}" and period={2} '.format(gc.DCS_DB_NAME, item_no,
                                                                                                period)
    gc.DCS_DB.update(sql1)


# 修改小单预计结算时间为昨天、can_settlement也改为Y，小单就可以自动结算了
def update_expect_settlement_at_before_one_day(item_no):
    sql1 = "UPDATE {0}.clean_precharge_clearing_tran SET expect_settlement_at=date_sub(now()," \
           "INTERVAL 1 DAY),can_settlement='Y' WHERE asset_item_no='{1}'".format(gc.DCS_DB_NAME, item_no)
    sql2 = "UPDATE {0}.clean_precharge_clearing_tran SET expect_settlement_at=date_sub(now()," \
           "INTERVAL -10 DAY)WHERE asset_item_no<>'{1}'  where status='new'  ".format(gc.DCS_DB_NAME, item_no)
    gc.DCS_DB.update(sql1)
    gc.DCS_DB.update(sql2)


# 修改大单预计结算时间为昨天、can_settlement也改为Y，大单就可以自动结算了
def update_loan_expect_settlement_at_before_one_day(item_no):
    sql1 = "UPDATE {0}.clean_clearing_trans SET expect_settlement_at=date_sub(now()," \
           "INTERVAL -10 DAY) WHERE item_no<>'{1}' and  status='new' ".format(gc.DCS_DB_NAME, item_no)
    sql2 = "UPDATE {0}.clean_clearing_trans SET expect_settlement_at=date_sub(now()," \
           "INTERVAL 1 DAY),can_settlement='Y' WHERE item_no='{1}'".format(gc.DCS_DB_NAME, item_no)
    sql3 = "UPDATE {0}.clean_clearing_trans SET expect_settlement_at=date_sub(now()," \
           "INTERVAL -10 DAY) WHERE item_no<>'{1}' and  status='new' ".format(gc.DCS_DB_NAME, item_no)
    gc.DCS_DB.update(sql1)
    gc.DCS_DB.update(sql2)
    gc.DCS_DB.update(sql3)


# 修改小单预计结算时间为昨天、can_settlement也改为Y，小单就可以自动结算了
def update_noloan_expect_settlement_at_before_one_day(item_no):
    sql1 = "UPDATE {0}.clean_precharge_clearing_tran SET expect_settlement_at=date_sub(now()," \
           "INTERVAL -10 DAY) WHERE asset_item_no<>'{1}' and  status='new' ".format(gc.DCS_DB_NAME, item_no)
    sql2 = "UPDATE {0}.clean_precharge_clearing_tran SET expect_settlement_at=date_sub(now()," \
           "INTERVAL 1 DAY),can_settlement='Y' WHERE asset_item_no='{1}'".format(gc.DCS_DB_NAME, item_no)
    sql3 = "UPDATE {0}.clean_precharge_clearing_tran SET expect_settlement_at=date_sub(now()," \
           "INTERVAL -10 DAY) WHERE asset_item_no<>'{1}' and  status='new' ".format(gc.DCS_DB_NAME, item_no)
    gc.DCS_DB.update(sql1)
    gc.DCS_DB.update(sql2)
    gc.DCS_DB.update(sql3)


# 修改预计结算时间为昨天
def update_clean_final_item_channel(channel, item_no):
    sql1 = "UPDATE {0}.clean_final_item SET withhold_result_channel='{1}' WHERE asset_item_no='{2}'".format(
        gc.DCS_DB_NAME, channel, item_no)
    gc.DCS_DB.update(sql1)
