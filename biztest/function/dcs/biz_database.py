import common.global_const as gc


# env = get_sysconfig("--env")
# db = DataBase("biz%s" % env)
# "biz%s" % gc.ENV = "biz%s" % env
# "gbiz%s" % gc.ENV = "gbiz%s" % env
# "rbiz%s" % gc.ENV = "rbiz%s" % env


# rbiz和gbiz都会用，查看task的执行情况 ， QinnongSingleRepayNotify 暂时不关心
from foundation_test.util.tools.tools import get_guid


def get_task(db_env, item_no):
    sql = "select * from {0}.task where task_order_no='{1}' and task_status!='close' and  task_type not in ('QinnongSingleRepayNotify','QinnongRepayNotify') " \
        .format(db_env, item_no)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]
    else:
        return None


# rbiz会用，获取四要素，有时候直接还款就只能通过数据库获取还款的四要素
def get_four_params_rbiz(item_no):
    sql = "select card_acc_id_num_encrypt,card_acc_tel_encrypt,card_acc_num_encrypt,card_acc_name_encrypt " \
          "from {0}.card inner join {0}.card_asset on card_asset_card_no=card_no " \
          "where card_asset_asset_item_no='{1}' and card_asset_type='repay' " \
        .format("rbiz%s" % gc.ENV, item_no)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]
    else:
        return None


# rbiz会用，查询需要还的钱是多少，注意一次性还多期period的传值
def get_repay_amount_rbiz(item_no, period, amount_type=None):
    if len(period) > 1 and amount_type is None:
        sql = "select sum(asset_tran_balance_amount) as 'asset_tran_balance_amount' from {0}.asset_tran " \
              "where asset_tran_asset_item_no='{1}' and asset_tran_period in {2} " \
            .format("rbiz%s" % gc.ENV, item_no, period)
    elif len(period) > 1 and amount_type:
        sql = "select sum(asset_tran_balance_amount) as 'asset_tran_balance_amount' from {0}.asset_tran " \
              "where asset_tran_asset_item_no='{1}' and asset_tran_period in {2} and asset_tran_type in ('{3}') " \
            .format("rbiz%s" % gc.ENV, item_no, period, amount_type)
    elif len(period) == 1 and amount_type:
        sql = "select sum(asset_tran_balance_amount) as 'asset_tran_balance_amount' from {0}.asset_tran " \
              "where asset_tran_asset_item_no='{1}' and asset_tran_period = {2} and asset_tran_type in ('{3}') " \
            .format("rbiz%s" % gc.ENV, item_no, period[0], amount_type)
    else:
        sql = "select sum(asset_tran_balance_amount) as 'asset_tran_balance_amount' from {0}.asset_tran " \
              "where asset_tran_asset_item_no='{1}' and asset_tran_period = {2}" \
            .format("rbiz%s" % gc.ENV, item_no, period[0])
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]
    else:
        return None


# biz和rbiz都用，修改实际放款时间
def update_grant_at(grant_at, item_no):
    sql_biz = 'update {0}.asset set asset_grant_at="{1}",asset_actual_grant_at="{1}",asset_effect_at="{1}" ' \
              'where asset_item_no="{2}" '.format("biz%s" % gc.ENV, grant_at, item_no)
    sql_rbiz = 'update {0}.asset set asset_grant_at="{1}",asset_actual_grant_at="{1}",asset_effect_at="{1}" ' \
               'where asset_item_no="{2}" '.format("rbiz%s" % gc.ENV, grant_at, item_no)
    gc.BIZ_DB.update(sql_biz)
    gc.BIZ_DB.update(sql_rbiz)


# biz和rbiz都用，修改到期日，用户还款计划和资方还款计划
def update_due_at(due_at, item_no, period):
    sql_ctr_biz = 'update {0}.capital_transaction ' \
                  'INNER JOIN {0}.capital_asset on capital_transaction_asset_id = capital_asset_id ' \
                  'set capital_transaction_expect_finished_at = "{1}" ' \
                  'where capital_asset_item_no = "{2}" and capital_transaction_period = {3} '.format("biz%s" % gc.ENV,
                                                                                                     due_at, item_no,
                                                                                                     period)
    sql_dtr_biz = 'update {0}.dtransaction ' \
                  'INNER JOIN {0}.asset on dtransaction_asset_id = asset_id ' \
                  'set dtransaction_expect_finish_time="{1}" ' \
                  'where asset_item_no="{2}" and dtransaction_period={3} '.format("biz%s" % gc.ENV, due_at, item_no,
                                                                                  period)
    sql_ftr_biz = 'update {0}.ftransaction ' \
                  'INNER JOIN {0}.asset on ftransaction_asset_id = asset_id ' \
                  'set ftransaction_expect_finish_time="{1}" ' \
                  'where asset_item_no="{2}" and ftransaction_period={3} '.format("biz%s" % gc.ENV, due_at, item_no,
                                                                                  period)
    sql_ctr_rbiz = 'update {0}.capital_transaction set capital_transaction_expect_finished_at="{1}" ' \
                   'where capital_transaction_item_no="{2}" and capital_transaction_period={3} '.format(
        "rbiz%s" % gc.ENV, due_at, item_no, period)
    sql_rbiz = 'update {0}.asset_tran set asset_tran_due_at="{1}" ' \
               'where asset_tran_asset_item_no="{2}" and asset_tran_period={3} '.format("rbiz%s" % gc.ENV, due_at,
                                                                                        item_no, period)
    # up_dtr_biz = 'update {0}.dtransaction ' \
    #               'INNER JOIN {0}.asset on dtransaction_asset_id = asset_id ' \
    #               'set dtransaction_expect_finish_time==left(dtransaction_expect_finish_time,10)  ' \
    #               'where asset_item_no="{1}" '.format("biz%s" % gc.ENV, item_no)
    # up_ftr_biz = 'update {0}.ftransaction ' \
    #               'INNER JOIN {0}.asset on ftransaction_asset_id = asset_id ' \
    #               'set ftransaction_expect_finish_time=left(ftransaction_expect_finish_time,10) ' \
    #               'where asset_item_no="{1}" '.format("biz%s" % gc.ENV, item_no)
    gc.BIZ_DB.update(sql_ctr_biz)
    gc.BIZ_DB.update(sql_dtr_biz)
    gc.BIZ_DB.update(sql_ftr_biz)
    gc.BIZ_DB.update(sql_ctr_rbiz)
    gc.BIZ_DB.update(sql_rbiz)
    # gc.BIZ_DB.update(up_dtr_biz)
    # gc.BIZ_DB.update(up_ftr_biz)


# biz用，修改代扣通道
def update_withhold_channel_biz(value, item_no, period):
    sql_re = "update {0}.withhold_result set withhold_result_channel='{1}' " \
             "where withhold_result_channel_key = (" \
             "select atransaction_serial_no from {0}.atransaction " \
             "INNER JOIN {0}.dtransaction on atransaction_transaction_id = dtransaction_id " \
             "left join {0}.asset on dtransaction_asset_id = asset_id " \
             "where atransaction_transaction_type='dtransaction' and dtransaction_type='repayprincipal' " \
             "AND `asset_item_no`='{2}' and dtransaction_period={3})".format("biz%s" % gc.ENV, value, item_no, period)
    sql_his = "update {0}.withhold_history set withhold_result_channel='{1}' " \
              "where withhold_result_channel_key = (" \
              "select atransaction_serial_no from {0}.atransaction " \
              "INNER JOIN {0}.dtransaction on atransaction_transaction_id = dtransaction_id " \
              "left join {0}.asset on dtransaction_asset_id = asset_id " \
              "where atransaction_transaction_type='dtransaction' and dtransaction_type='repayprincipal' " \
              "AND `asset_item_no`='{2}' and dtransaction_period={3})".format("biz%s" % gc.ENV, value, item_no, period)
    gc.BIZ_DB.update(sql_re)
    gc.BIZ_DB.update(sql_his)


def uodate_biz_withhold_to_channel(channel, item_no):
    sql1 = "update  {0}.withhold_result  set withhold_result_channel='{1}' where withhold_result_asset_item_no='{2}' " \
        .format("biz%s" % gc.ENV, channel, item_no)
    sql2 = "INSERT INTO {0}.withhold_history ( withhold_result_id, withhold_result_asset_id, withhold_result_asset_item_no, withhold_result_asset_type, " \
           "withhold_result_asset_period, withhold_result_amount, withhold_result_user_name, withhold_result_user_phone, withhold_result_user_id_card, " \
           "withhold_result_user_bank_card, withhold_result_type, withhold_result_status, withhold_result_channel, withhold_result_serial_no, " \
           "withhold_result_create_at, withhold_result_channel_key, withhold_result_channel_fee, withhold_result_finish_at, " \
           "withhold_history_sync_at, withhold_result_user_name_encrypt, withhold_result_user_phone_encrypt, withhold_result_user_id_card_encrypt, " \
           "withhold_result_user_bank_card_encrypt) SELECT  withhold_result_id, withhold_result_asset_id, withhold_result_asset_item_no, withhold_result_asset_type," \
           " withhold_result_asset_period, withhold_result_amount, withhold_result_user_name, withhold_result_user_phone, withhold_result_user_id_card, " \
           "withhold_result_user_bank_card, withhold_result_type, withhold_result_status, withhold_result_channel, withhold_result_serial_no, withhold_result_create_at," \
           " withhold_result_channel_key, withhold_result_channel_fee, withhold_result_finish_at, now(), withhold_result_user_name_encrypt, " \
           "withhold_result_user_phone_encrypt, withhold_result_user_id_card_encrypt, withhold_result_user_bank_card_encrypt FROM   {0}.withhold_result " \
           "WHERE withhold_result_asset_item_no IN ('{2}') " \
        .format("biz%s" % gc.ENV, channel, item_no)
    sql3 = "update  {0}.withhold_history  set withhold_result_channel='{1}' where withhold_result_asset_item_no='{2}'" \
        .format("biz%s" % gc.ENV, channel, item_no)
    withhold_info = gc.BIZ_DB.update(sql1)
    withhold_history_info3 = gc.BIZ_DB.update(sql2)
    withhold_history_info = gc.BIZ_DB.update(sql3)
    return withhold_info, withhold_history_info, withhold_history_info3


# 检查代扣流水的同步情况（避免代扣流水尚未同步完成就执行后续操作）
def get_withhold_count_biz(item_no, period):
    sql = "select * from {0}.withhold_history where withhold_result_asset_item_no='{1}' and withhold_result_asset_period={2}" \
        .format(gc.BIZ_DB, item_no, period)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


# 检查dtr和ftr还款计划
def get_dtr_ftr_biz(item_no, period):
    sql = "select asset_item_no,dtransaction_period,dtransaction_id,dtransaction_status,dtransaction_type," \
          "dtransaction_expect_finish_time,dtransaction_finish_at,dtransaction_amount_f,dtransaction_repaid_amount_f," \
          "dtransaction_decrease_amount from {0}.dtransaction left join {0}.asset on dtransaction_asset_id=asset_id " \
          "where asset_item_no='{1}' and dtransaction_period in ({2}) " \
          " UNION ALL " \
          "select asset_item_no,ftransaction_period,ftransaction_id,ftransaction_status,fee_type,ftransaction_expect_finish_time," \
          "ftransaction_finish_at,ftransaction_amount_f,ftransaction_repaid_amount_f,ftransaction_decrease_amount " \
          "from {0}.ftransaction left join {0}.asset on ftransaction_asset_id=asset_id left join {0}.fee on fee_id=ftransaction_fee_id " \
          "where asset_item_no='{1}' and ftransaction_period in ({2}) " \
        .format("biz%s" % gc.ENV, item_no, period)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


# 检查atr还款明细
def get_atr_biz(item_no, period):
    sql = "select asset_item_no,dtransaction_period,dtransaction_type,atransaction_id,atransaction_amount_f," \
          "atransaction_create_at,atransaction_transaction_id,atransaction_serial_no from {0}.atransaction " \
          "INNER JOIN {0}.dtransaction on atransaction_transaction_id=dtransaction_id " \
          "left join {0}.asset on dtransaction_asset_id=asset_id " \
          "where atransaction_transaction_type='dtransaction' and asset_item_no='{1}' and dtransaction_period in ({2}) " \
          " UNION all " \
          "select asset_item_no,ftransaction_period,fee_type,atransaction_id,atransaction_amount_f,atransaction_create_at," \
          "atransaction_transaction_id,atransaction_serial_no from {0}.atransaction " \
          "INNER JOIN {0}.ftransaction on atransaction_transaction_id=ftransaction_id " \
          "left join {0}.asset on ftransaction_asset_id=asset_id left join {0}.fee on fee_id=ftransaction_fee_id " \
          "where atransaction_transaction_type='ftransaction' and asset_item_no='{1}' and ftransaction_period in ({2}) " \
        .format("biz%s" % gc.ENV, item_no, period)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


# 获取资产的资方还款计划
def get_capital_biz(item_no, period):
    sql = 'select * from {0}.capital_transaction INNER JOIN {0}.capital_asset on capital_transaction_asset_id = capital_asset_id ' \
          'where capital_asset_item_no = "{1}" and capital_transaction_period = {2} ' \
        .format("biz%s" % gc.ENV, item_no, period)
    capital = gc.BIZ_DB.query(sql)
    if capital:
        return capital
    else:
        return None


# 修改atr的还款日期
def update_atransaction(finished_at, item_no, period):
    # sql_dtr_atr = "update {0}.atransaction INNER JOIN {0}.dtransaction on atransaction_transaction_id=dtransaction_id " \
    #               "INNER JOIN {0}.asset on dtransaction_asset_id=asset_id " \
    #               "set atransaction_create_at='{1}' where atransaction_transaction_type='dtransaction' " \
    #               "AND asset_item_no='{2}' and dtransaction_period={3} ".format("biz%s" % gc.ENV, finished_at, item_no, period)
    # sql_ftr_atr = "update {0}.atransaction INNER JOIN {0}.ftransaction on atransaction_transaction_id=ftransaction_id " \
    #               "INNER JOIN {0}.asset on ftransaction_asset_id=asset_id INNER JOIN {0}.fee on fee_id=ftransaction_fee_id " \
    #               "set atransaction_create_at='{1}' where atransaction_transaction_type='ftransaction' " \
    #               "AND asset_item_no='{2}' and ftransaction_period={3} ".format("biz%s" % gc.ENV, finished_at, item_no, period)
    sql_ftr = "update {0}.ftransaction INNER JOIN {0}.asset on ftransaction_asset_id=asset_id " \
              "INNER JOIN {0}.fee on fee_id=ftransaction_fee_id set ftransaction_finish_at='{1}' " \
              "where asset_item_no='{2}' and ftransaction_period={3} and ftransaction_finish_at != '1000-01-01 00:00:00' ".format(
        "biz%s" % gc.ENV, finished_at, item_no, period)
    sql_dtr = "update {0}.dtransaction INNER JOIN {0}.asset on dtransaction_asset_id=asset_id " \
              "set dtransaction_finish_at='{1}' " \
              "where asset_item_no='{2}' and dtransaction_period={3} and dtransaction_finish_at != '1000-01-01 00:00:00' ".format(
        "biz%s" % gc.ENV, finished_at, item_no, period)
    # gc.BIZ_DB.update(sql_dtr_atr)
    # gc.BIZ_DB.update(sql_ftr_atr)
    gc.BIZ_DB.update(sql_dtr)
    gc.BIZ_DB.update(sql_ftr)


# 还款通知的提前结清的数据检查 clean_settle_reduce
def get_settle_reduce_status(item_no):
    sql = 'select status from {0}.clean_settle_reduce where asset_item_no ="{1}"'.format("biz%s" % gc.ENV, item_no)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


# 回购 buyback
def get_buyback_biz(item_no):
    sql = 'select * from {0}.buyback where buyback_asset_item_no ="{1}"'.format("biz%s" % gc.ENV, item_no)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


def insert_buyback(item_no, period_count, amount, period, channel, type='buyback'):
    sql = "INSERT INTO {0}.buyback " \
          "(buyback_asset_item_no,buyback_start_date,buyback_end_date,buyback_create_at," \
          "buyback_total_principal_amount,buyback_total_interest_amount," \
          "buyback_asset_period_count,buyback_asset_granted_principal_amount," \
          "buyback_period,buyback_channel,buyback_category) " \
          "VALUES " \
          "('{1}',now(),now(),now(),{3},{4},{2},{3},{5},'{6}','{7}') " \
        .format("biz%s" % gc.ENV, item_no, period_count, amount, amount / 250, period, channel, type)
    gc.BIZ_DB.update(sql)


# 查看 biz 是否生成了某 task
def get_task_biz(item_no, type):
    sql = 'select * from {0}.task where task_request_data like "%{1}%" and task_type="{2}" '.format("biz%s" % gc.ENV,
                                                                                                    item_no, type)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


# # 获取某个资产的某个费用的用户还款计划
# def get_one_repay_plan(item_no, type, period_min, period_max):
#     sql = 'select * from {0}.dtransaction INNER JOIN {0}.asset ON dtransaction_asset_id = asset_id ' \
#           'where asset_item_no = "{1}" and dtransaction_type = "{2}" ' \
#           'and dtransaction_period>={3} and dtransaction_period<={4} ' \
#           'order by dtransaction_period asc '.format("biz%s" % gc.ENV, item_no, type, period_min, period_max)
#     result_list = gc.BIZ_DB.query(sql)
#     if result_list:
#         return result_list
#     else:
#         return None

# # 获取某个资产的某个费用的用户还款计划
# def get_one_repay_plan_ft(item_no, type, period_min, period_max):
#     sql = 'select * from {0}.ftransaction INNER JOIN {0}.asset ON ftransaction_asset_id = asset_id INNER JOIN {0}.fee on fee_id=ftransaction_fee_id ' \
#           'where asset_item_no="{1}" and fee_type="{2}" ' \
#           'and ftransaction_period>={3} and ftransaction_period<={4} ' \
#           'order by ftransaction_period asc '.format("biz%s" % gc.ENV, item_no, type, period_min, period_max)
#     result_list = gc.BIZ_DB.query(sql)
#     if result_list:
#         return result_list
#     else:
#         return None

# 获取某个资产的某个费用的用户还款计划
def get_one_repay_plan(item_no, type, period_min, period_max):
    sql = 'select * from {0}.asset_tran where asset_tran_asset_item_no = "{1}" and asset_tran_type = "{2}" ' \
          'and asset_tran_period>={3} and asset_tran_period<={4} ' \
          'order by asset_tran_period asc '.format("biz%s" % gc.ENV, item_no, type, period_min, period_max)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


# 获取某个资产的某个费用的用户还款计划
def get_one_repay_plan_ft(item_no, type, period_min, period_max):
    sql = 'select * from {0}.asset_tran where asset_tran_asset_item_no = "{1}" and asset_tran_type = "{2}" ' \
          'and asset_tran_period>={3} and asset_tran_period<={4} ' \
          'order by asset_tran_period asc '.format("biz%s" % gc.ENV, item_no, type, period_min, period_max)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


# asset_loan_record
def get_asset_loan_record(item_no):
    sql = 'select * from {0}.asset inner join {0}.asset_loan_record on asset_loan_record_asset_id = asset_id ' \
          'where asset_item_no = "{1}"'.format("biz%s" % gc.ENV, item_no)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]
    else:
        return None


# 云信全户授信费
def update_capital_amount(time):
    sql = "INSERT INTO {0}.capital_transaction (capital_transaction_asset_id,capital_transaction_channel,capital_transaction_grant_id,capital_transaction_grant_type,capital_transaction_type,capital_transaction_period,capital_transaction_amount) " \
          "SELECT CT1.capital_transaction_asset_id,CT1.capital_transaction_channel,CT1.capital_transaction_grant_id,CT1.capital_transaction_grant_type,'credit_fee',CT1.capital_transaction_period,ftransaction_amount_f " \
          "FROM {0}.fee INNER JOIN {0}.ftransaction ON fee_id=ftransaction_fee_id INNER JOIN {0}.asset ON asset_id=fee_asset_id INNER JOIN {0}.capital_asset ON capital_asset_item_no=asset_item_no " \
          "INNER JOIN {0}.capital_transaction CT1 ON CT1.capital_transaction_asset_id=capital_asset_id AND CT1.capital_transaction_period=ftransaction_period AND CT1.capital_transaction_type='principal' " \
          "LEFT JOIN {0}.capital_transaction CT2 ON CT2.capital_transaction_asset_id=capital_asset_id AND CT2.capital_transaction_period=ftransaction_period AND CT2.capital_transaction_type='credit_fee' " \
          "WHERE `fee_type` = 'credit_fee' AND `asset_loan_channel` = 'yunxin_quanhu' AND `ftransaction_create_at` >= '{1}' AND CT2.capital_transaction_id IS NULL " \
        .format("biz%s" % gc.ENV, time)
    gc.BIZ_DB.insert(sql)


# 检查并修改rbiz capital_route 的配置
def get_capital_route_rbiz(channel, type):
    sql = 'select capital_route_conditional_value from {0}.capital_route ' \
          'where capital_route_config_code = "{1}" and capital_route_conditional = "{2}" '.format("rbiz%s" % gc.ENV,
                                                                                                  channel, type)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]["capital_route_conditional_value"]
    else:
        return None


def update_capital_route_rbiz(value, channel, type):
    sql = "update {0}.capital_route set capital_route_conditional_value = '{1}' ' \
          'where capital_route_config_code = '{2}' and capital_route_conditional = '{3}' ".format("rbiz%s" % gc.ENV,
                                                                                                  value, channel, type)
    gc.BIZ_DB.update(sql)


# 获取biz的kv，修改kv的时候会用到
def get_kv_biz(db_evn, channel):
    sql = 'select keyvalue_value from {0}.keyvalue where keyvalue_key = "{1}" and keyvalue_status = "active" '.format(
        db_evn, channel)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]["keyvalue_value"]
    else:
        return None


def update_kv_biz(db_evn, value, channel):
    sql = "update {0}.keyvalue set keyvalue_value = '{1}' where keyvalue_key = '{2}' and keyvalue_status = 'active' ".format(
        db_evn, value, channel)
    gc.BIZ_DB.update(sql)


# 更新biz 资方代扣记录的代扣通道
def get_withhold(db_evn, item_no, period):
    sql = 'select * from {0}.withhold_history ' \
          'where withhold_result_asset_item_no = "{1}" and withhold_result_asset_period = {2}' \
        .format(db_evn, item_no, period)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


def update_withhold_channel(db_evn, value, itemo, period):
    sql = 'update {0}.withhold_history set withhold_result_channel = "{1}" ' \
          'where withhold_result_asset_item_no = "{2}" and withhold_result_asset_period = {3} and withhold_result_serial_no not like "AUTO_%"' \
        .format(db_evn, value, itemo, period)
    sql2 = 'update {0}.withhold_result set withhold_result_channel = "{1}" ' \
           'where withhold_result_asset_item_no = "{2}" and withhold_result_asset_period = {3} and withhold_result_serial_no not like "AUTO_%"' \
        .format(db_evn, value, itemo, period)
    gc.BIZ_DB.update(sql)
    gc.BIZ_DB.update(sql2)


def get_asset(item_no):
    sql = 'select * from asset where asset_item_no = "{0}" and asset_status in("repay","payoff")'.format(item_no)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]
    else:
        return None


def get_repay_biz(item_no):
    sql = 'select asset_item_no,dtransaction_period,dtransaction_type,atransaction_amount_f,atransaction_create_at,' \
          'atransaction_transaction_id,atransaction_serial_no,withhold_result_channel from {0}.atransaction ' \
          'INNER JOIN {0}.dtransaction on atransaction_transaction_id=dtransaction_id ' \
          'INNER JOIN {0}.asset on dtransaction_asset_id=asset_id ' \
          'INNER JOIN {0}.withhold_result on withhold_result_channel_key=atransaction_serial_no ' \
          'where `atransaction_transaction_type`="dtransaction" AND asset_item_no="{1}" ' \
          'UNION all select asset_item_no,ftransaction_period,fee_type,atransaction_amount_f,atransaction_create_at,' \
          'atransaction_transaction_id,atransaction_serial_no,withhold_result_channel from  {0}.atransaction ' \
          'INNER JOIN {0}.ftransaction on atransaction_transaction_id=ftransaction_id ' \
          'INNER JOIN {0}.asset on ftransaction_asset_id=asset_id INNER JOIN {0}.fee on ftransaction_fee_id=fee_id ' \
          'INNER JOIN {0}.withhold_result on withhold_result_channel_key=atransaction_serial_no ' \
          'where `atransaction_transaction_type`="ftransaction" AND asset_item_no="{1}" '.format("biz%s" % gc.ENV,
                                                                                                 item_no)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]
    else:
        return None


# 节假日判断
def get_holiday_status(db_evn, holiday_date):
    sql = 'select holiday_status from {0}.holiday where holiday_date ="{1}"'.format(db_evn, holiday_date)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]["holiday_status"]
    else:
        return None


# 兰州独有流程，兰州要去查询gbiz的开户信息，现在强行插入开户信息
def update_capital_account(itemo, card):
    sql = "INSERT INTO {0}.capital_account " \
          "(capital_account_item_no,capital_account_user_key,capital_account_channel,capital_account_status," \
          "capital_account_card_number_encrypt,capital_account_idnum_encrypt,capital_account_name_encrypt,capital_account_mobile_encrypt) " \
          "VALUES" \
          "('{1}', '104954675444264911', 'zhongke_lanzhou', 0, '{2}', 'enc_03_3118013546618161152_115','enc_04_5606880_529', 'enc_01_3119657648136914944_595')" \
        .format("gbiz%s" % gc.ENV, itemo, card)
    gc.BIZ_DB.update(sql)


def get_capital_account(itemo):
    sql = 'select capital_account_id from {0}.capital_account where capital_account_item_no ="{1}"'.format(
        "gbiz%s" % gc.ENV, itemo)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]["capital_account_id"]
    else:
        return None


def update_capital_account2(itemo, account, card):
    sql = "INSERT INTO {0}.capital_account_card " \
          "(capital_account_card_item_no,capital_account_card_account_id,capital_account_card_memo,capital_account_card_status," \
          "capital_account_card_step,capital_account_card_way,capital_account_card_card_number_encrypt,capital_account_card_serial_no) " \
          "VALUES" \
          "('{1}', {2}, '开户成功', 0, 'PROTOCOL', 'baidu_tq3_quick', '{3}', '104954675444264911')" \
        .format("gbiz%s" % gc.ENV, itemo, account, card)
    gc.BIZ_DB.update(sql)


# 已经取消进件的资金方，想进件
def get_old_asset(channel, period):
    sql = "select asset_loan_record_asset_item_no from {0}.asset_loan_record " \
          "inner join {0}.sendmsg on sendmsg_order_no=asset_loan_record_asset_item_no " \
          "inner join {0}.asset on asset_item_no=asset_loan_record_asset_item_no " \
          "where asset_loan_record_channel ='{1}' and asset_period_count={2} " \
          "and asset_loan_record_status=6 and sendmsg_type ='AssetWithdrawSuccess' " \
          "order by asset_loan_record_id desc" \
        .format("gbiz%s" % gc.ENV, channel, period)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]["asset_loan_record_asset_item_no"]
    else:
        return None


def get_old_asset_noloan(item_no):
    sql = "select asset_extend_ref_order_no from {0}.asset_extend where asset_extend_asset_item_no ='{1}' " \
        .format("gbiz%s" % gc.ENV, item_no)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]["asset_extend_ref_order_no"]
    else:
        return None


def get_old_noloan():
    sql = "select asset_item_no from {0}.asset where asset_loan_channel ='noloan' order by asset_id desc limit 1" \
        .format("rbiz%s" % gc.ENV)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]["asset_item_no"]
    else:
        return None


def insert_old_asset_noloan(old_item_no, item_no):
    sql = "INSERT INTO {0}.`asset` " \
          "( `asset_no`, `asset_item_no`, `asset_type`, `asset_sub_type`, `asset_period_type`, `asset_period_count`, " \
          "`asset_product_category`, `asset_cmdb_product_number`, `asset_grant_at`, `asset_effect_at`, " \
          "`asset_actual_grant_at`, `asset_due_at`, `asset_payoff_at`, `asset_from_system`, `asset_status`, " \
          "`asset_principal_amount`, `asset_granted_principal_amount`, `asset_decrease_principal_amount`, " \
          "`asset_loan_channel`, `asset_alias_name`, `asset_interest_amount`, `asset_decrease_interest_amount`, " \
          "`asset_fee_amount`, `asset_decrease_fee_amount`, `asset_balance_amount`, `asset_repaid_amount`, " \
          "`asset_total_amount`, `asset_interest_rate`, `asset_create_at`, `asset_rbiz_create_at`, " \
          "`asset_update_at`, `asset_rbiz_update_at`, `asset_last_sync_time`, `asset_channel_id`, " \
          "`asset_from_system_name`, `asset_owner`, `asset_actual_payoff_at`, `asset_late_amount`, " \
          "`asset_due_bill_no`, `asset_repaid_principal_amount`, `asset_repaid_interest_amount`, " \
          "`asset_repaid_fee_amount`, `asset_repaid_late_amount`, `asset_decrease_late_amount`, `asset_from_app`, " \
          "`asset_repayment_app`, `asset_last_late_at`, `asset_full_late_flag`) " \
          "(select `asset_no`, '{1}', `asset_type`, `asset_sub_type`, " \
          "`asset_period_type`, `asset_period_count`, `asset_product_category`, `asset_cmdb_product_number`, " \
          "`asset_grant_at`, `asset_effect_at`, `asset_actual_grant_at`, `asset_due_at`, `asset_payoff_at`, " \
          "`asset_from_system`, `asset_status`, `asset_principal_amount`, `asset_granted_principal_amount`, " \
          "`asset_decrease_principal_amount`, `asset_loan_channel`, `asset_alias_name`, `asset_interest_amount`, " \
          "`asset_decrease_interest_amount`, `asset_fee_amount`, `asset_decrease_fee_amount`, `asset_balance_amount`, " \
          "`asset_repaid_amount`, `asset_total_amount`, `asset_interest_rate`, `asset_create_at`, `asset_rbiz_create_at`, " \
          "`asset_update_at`, `asset_rbiz_update_at`, `asset_last_sync_time`, `asset_channel_id`, `asset_from_system_name`, " \
          "`asset_owner`, `asset_actual_payoff_at`, `asset_late_amount`, `asset_due_bill_no`, `asset_repaid_principal_amount`, " \
          "`asset_repaid_interest_amount`, `asset_repaid_fee_amount`, `asset_repaid_late_amount`, `asset_decrease_late_amount`, " \
          "`asset_from_app`, `asset_repayment_app`, `asset_last_late_at`, `asset_full_late_flag` " \
          "from  {0}.`asset` where `asset_item_no`='{2}'); ".format("rbiz%s" % gc.ENV, item_no, old_item_no)
    gc.BIZ_DB.update(sql)


# 删除多余的 atransaction ，同时构造还款失败的景象
def delete_null(item):
    sql = "select atransaction_id from atransaction " \
          "INNER JOIN dtransaction on atransaction_transaction_id = dtransaction_id " \
          "left join asset on dtransaction_asset_id = asset_id " \
          "where atransaction_transaction_type = 'dtransaction' AND asset_item_no = '{1}' " \
          "and atransaction_serial_no is null UNION all select atransaction_id from atransaction " \
          "INNER JOIN ftransaction on atransaction_transaction_id = ftransaction_id " \
          "left join asset on ftransaction_asset_id = asset_id " \
          "left join fee on fee_id = ftransaction_fee_id " \
          "where atransaction_transaction_type = 'ftransaction' AND asset_item_no = '{1}' " \
          "and atransaction_serial_no is null".format("biz%s" % gc.ENV, item)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


def delete_atransaction(serial_no):
    sql = "select atransaction_id from atransaction " \
          "INNER JOIN dtransaction on atransaction_transaction_id = dtransaction_id " \
          "left join asset on dtransaction_asset_id = asset_id " \
          "where atransaction_transaction_type = 'dtransaction' AND atransaction_serial_no = '{1}' " \
          "UNION all select atransaction_id from atransaction " \
          "INNER JOIN ftransaction on atransaction_transaction_id = ftransaction_id " \
          "left join asset on ftransaction_asset_id = asset_id " \
          "left join fee on fee_id = ftransaction_fee_id " \
          "where atransaction_transaction_type = 'ftransaction' AND atransaction_serial_no = '{1}' ".format(
        "biz%s" % gc.ENV, serial_no)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None


def delete_null_all(ids):
    if len(ids) > 1:
        sql = "delete from {0}.account_log where account_log_atransaction_id in {1}".format("biz%s" % gc.ENV, ids)
        gc.BIZ_DB.delete(sql)
        sql_2 = "delete from {0}.atransaction where atransaction_id in {1}".format("biz%s" % gc.ENV, ids)
        gc.BIZ_DB.delete(sql_2)
    else:
        sql = "delete from {0}.account_log where account_log_atransaction_id = {1}".format("biz%s" % gc.ENV, ids[0])
        gc.BIZ_DB.delete(sql)
        sql_2 = "delete from {0}.atransaction where atransaction_id = {1}".format("biz%s" % gc.ENV, ids[0])
        gc.BIZ_DB.delete(sql_2)


def get_deposit_tasks():
    # 先把今天以前的任务关闭
    update_sql1 = 'update {0}.task set task_status = "close" where task_create_at<current_date and task_status != "close"   ' \
        .format(gc.DEPOSIT_DB_NAME)
    gc.BIZ_DB.update(update_sql1)
    # 找出所有未执行的task，并将执行时间改为当前时间
    sql = 'select task_order_no from {0}.task where task_status != "close" and task_create_at>current_date and task_type in ("TradeNew") ' \
        .format(gc.DEPOSIT_DB_NAME)
    task = gc.BIZ_DB.query(sql)
    update_sql = 'update {0}.task set task_status = "open",task_next_run_at =date_sub(now(), INTERVAL 20 MINUTE) where task_status != "close" ' \
        .format(gc.DEPOSIT_DB_NAME)
    gc.BIZ_DB.update(update_sql)
    return task


# 按order_no更新deposit的记账、转账、提现等状态
def update_deposit_status_to_success_by_order_no(order_no, status=2):
    sql1 = "UPDATE {0}.trade SET STATUS = '{1}',finished_at = now(),response_message='fail or success'  WHERE created_at>curdate() AND `status` IN (0,1) and order_no='{2}' ".format(
        gc.DEPOSIT_DB_NAME, status, order_no)
    sql2 = "UPDATE {0}.trade_order SET STATUS = '{1}',finished_at = now()  WHERE created_at>curdate()AND `status` IN (0,1) and order_no='{2}' ".format(
        gc.DEPOSIT_DB_NAME, status, order_no)
    gc.BIZ_DB.update(sql1)
    gc.BIZ_DB.update(sql2)


# 更新deposit的记账、转账、提现等状态
def update_deposit_orderAndtrade_status(status=2):
    sql1 = "UPDATE {0}.trade SET STATUS = '{1}',finished_at = now(),response_message='fail or success'  WHERE created_at>curdate() AND `status` IN (0,1) ".format(
        gc.DEPOSIT_DB_NAME, status)
    sql2 = "UPDATE {0}.trade_order SET STATUS = '{1}',finished_at = now()  WHERE created_at>curdate()AND `status` IN (0,1) ".format(
        gc.DEPOSIT_DB_NAME, status)
    gc.DEPOSIT_DB.update(sql1)
    gc.DEPOSIT_DB.update(sql2)


# 更新deposit订单为不存在
def update_deposit_order_notexsit(order_no):
    guid=get_guid()
    sql1 = "UPDATE {0}.trade_order SET order_no  ='{2}' WHERE  order_no='{1}' ".format(gc.DEPOSIT_DB_NAME, order_no, guid)
    sql2 = "UPDATE {0}.trade SET order_no ='{2}' WHERE order_no='{1}' ".format(gc.DEPOSIT_DB_NAME, order_no, guid)
    gc.DEPOSIT_DB.update(sql1)
    gc.DEPOSIT_DB.update(sql2)


# 更新payment代付状态
def update_payment_withdrawAndreceipt_status(status=2):
    sql1 = "UPDATE {0}.withdraw SET withdraw_status = '{1}',withdraw_finished_at = now() WHERE  withdraw_status IN (0,1) ".format(
        gc.PAYMENT_DB_NAME, status)
    sql2 = "UPDATE {0}.withdraw_receipt SET withdraw_receipt_status = '{1}',withdraw_receipt_finished_at = now(),withdraw_receipt_channel_resp_message" \
           "='withdraw success or fail message' " \
           " WHERE withdraw_receipt_status IN (0,1)".format(gc.PAYMENT_DB_NAME, status)
    gc.PAYMENT_DB.update(sql1)
    gc.PAYMENT_DB.update(sql2)


def update_noloan_asset_source_type(item_no):
    sql = "UPDATE asset_extend SET asset_extend_ref_order_type='lieyin_bill_split' WHERE asset_extend_asset_id IN (SELECT asset_id FROM asset WHERE asset_item_no='{0}') ".format(
        item_no)
    gc.BIZ_DB.update(sql)


def update_asset_extend_ref_and_sub_order_type(ref_order_type, sub_order_type, item_no):
    sql = "UPDATE asset_extend  SET asset_extend_ref_order_type='{0}',asset_extend_sub_order_type='{1}' WHERE  asset_extend_asset_id  " \
          "IN (SELECT asset_id FROM asset WHERE asset_item_no='{2}')".format(ref_order_type, sub_order_type, item_no)
    gc.BIZ_DB.update(sql)


def set_up_the_asset_trans_for_compensate():
    sql = "UPDATE asset_tran SET asset_tran_finish_at='2020-01-01'  WHERE asset_tran_finish_at >= " \
          "date_add(curdate(), INTERVAL -1 DAY ) AND asset_tran_finish_at <curdate() AND asset_tran_type != " \
          "'GRANT';"
    gc.BIZ_DB.update(sql)
    gc.REPAY_DB.update(sql)
