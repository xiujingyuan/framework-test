from biztest.function.gbiz.gbiz_db_function import get_asset_info_by_item_no
from biztest.util.log.log_util import LogUtil
from biztest.util.tools.tools import *
import common.global_const as gc


def get_biz_asset_info_by_item_no(item_no):
    sql = "select * from asset where asset_item_no='%s'" % item_no
    asset_info = gc.BIZ_DB.query(sql)
    return asset_info


def get_biz_atransaction_by_item_no(item_no):
    sql = "SELECT * FROM atransaction INNER JOIN dtransaction ON atransaction_transaction_id = dtransaction_id " \
          "WHERE atransaction_type = 'repay' AND atransaction_transaction_type = 'dtransaction' AND " \
          "dtransaction_asset_id IN(SELECT asset_id FROM asset WHERE asset_item_no='%s')" % item_no
    a_tran = gc.BIZ_DB.query(sql)
    return a_tran


def get_biz_asset_tran_by_item_no(item_no):
    sql = "select * from asset_tran where asset_tran_asset_item_no='%s' " \
          "order by asset_tran_period" % item_no
    asset_tran = gc.BIZ_DB.query(sql)
    return asset_tran


def get_biz_capital_asset_by_item_no(item_no):
    sql = "select * from capital_asset where capital_asset_item_no='%s'" % item_no
    capital_asset = gc.BIZ_DB.query(sql)
    return capital_asset


def get_biz_capital_asset_tran_by_item_no(item_no):
    sql = "select * from capital_transaction where capital_transaction_asset_item_no='%s'" % item_no
    capital_transaction = gc.BIZ_DB.query(sql)
    return capital_transaction


def get_biz_withhold_result_by_item_no(item_no):
    sql = "select * from withhold_result where withhold_result_asset_item_no='%s'" % item_no
    withhold_result = gc.BIZ_DB.query(sql)
    return withhold_result


def set_capital_loan_condition(channel, period_type, period_count):
    if int(period_count) == 1:
        period_day = 30
    else:
        period_day = 0
    sql = "delete from capital_loan_condition where " \
          "capital_loan_condition_channel='%s' and capital_loan_condition_day='%s' " \
          "and capital_loan_condition_period_count='%s'" % (channel, get_date(fmt="%Y-%m-%d"), period_count)
    gc.BIZ_DB.delete(sql)
    sql = "INSERT INTO `capital_loan_condition` (`capital_loan_condition_day`, " \
          "`capital_loan_condition_channel`, `capital_loan_condition_amount`, `capital_loan_condition_from_system`, " \
          "`capital_loan_condition_sub_type`, `capital_loan_condition_period_count`, " \
          "`capital_loan_condition_period_type`, `capital_loan_condition_period_days`, " \
          "`capital_loan_condition_description`, `capital_loan_condition_update_memo`) " \
          "VALUES ('%s', '%s', 300000000, 'dsq', 'multiple', %s, '%s', '%s', '%s期自动化创建', '自动化创建')" % \
          (get_date(fmt="%Y-%m-%d"), channel, period_count, period_type, period_day, period_count)
    gc.BIZ_DB.insert(sql)


def set_asset_contract_subject(item_no, subject):
    sql = "INSERT INTO asset_contract_subject" \
          "(asset_contract_subject_asset_id, asset_contract_subject_asset_item_no,asset_contract_subject_status, " \
          "asset_contract_subject_part, asset_contract_subject_create_at,asset_contract_subject_update_at, " \
          "asset_contract_subject_current_period,asset_contract_subject_share_benefit_period, " \
          "asset_contract_subject_benefit_company_name,asset_contract_subject_benefit_company_code)" \
          "VALUES (1111, '%s', 'unfinished', '%s', '2019-08-01 18:23:40', '2019-08-01 18:23:40', " \
          "0, 0,'云智对应APP公司', 'v_yunzhi_1')" % (item_no, subject)
    gc.BIZ_DB.insert(sql)


def insert_withhold_result(item_no):
    sql = "INSERT INTO `withhold_result` (`withhold_result_asset_id`, `withhold_result_asset_item_no`, " \
          "`withhold_result_asset_type`, `withhold_result_asset_period`, `withhold_result_amount`, " \
          "`withhold_result_user_name`, `withhold_result_user_phone`, `withhold_result_user_id_card`, " \
          "`withhold_result_user_bank_card`, `withhold_result_user_bank_card_code`, `withhold_result_type`, " \
          "`withhold_result_status`, `withhold_result_channel`, `withhold_result_serial_no`, " \
          "`withhold_result_comment`, `withhold_result_custom_code`, `withhold_result_request_data`, " \
          "`withhold_result_response_data`, `withhold_result_creator`, `withhold_result_operator`, " \
          "`withhold_result_run_times`, `withhold_result_execute_time`, `withhold_result_create_at`, " \
          "`withhold_result_update_at`, `withhold_result_channel_key`, `withhold_result_channel_fee`, " \
          "`withhold_result_finish_at`, `withhold_result_error_code`, `withhold_result_rbiz_process`, " \
          "`withhold_result_owner`, `withhold_result_user_name_encrypt`, `withhold_result_user_phone_encrypt`, " \
          "`withhold_result_user_id_card_encrypt`, `withhold_result_user_bank_card_encrypt`, " \
          "`withhold_result_channel_message`, `withhold_result_capital_receive_at`) VALUES (34298900, '%s', " \
          "'paydayloan', 1, 76108, NULL, NULL, NULL, NULL, 'CCB', 'manual', 'success', 'arbitration', '%s', " \
          "'', '', NULL, NULL, 'BIZ', 'BIZ', 1, now(), now(), now(), '%s', 0, now(), '', 1, 'KN', " \
          "'enc_04_2679724001475432448_626', 'enc_01_2494943587037874176_393', 'enc_02_3209082092994955264_264', " \
          "'enc_03_3209083805898378240_938', '', now())" % (item_no, "Autotest" + item_no, "Autotest" + item_no)
    gc.BIZ_DB.insert(sql)


def set_withhold_history(item_no, wait_time=20):
    for i in range(wait_time):
        withhold_result = get_biz_withhold_result_by_item_no(item_no)
        if withhold_result is not None and len(withhold_result) > 0:
            break
        else:
            time.sleep(1)

    gc.BIZ_DB.delete("delete from withhold_history where withhold_result_asset_item_no='%s'" % item_no)
    time.sleep(1)
    sql = "INSERT INTO `withhold_history` ( `withhold_result_id`, `withhold_result_asset_id`, " \
          "`withhold_result_asset_item_no`, `withhold_result_asset_type`, `withhold_result_asset_period`, " \
          "`withhold_result_amount`, `withhold_result_user_name`, `withhold_result_user_phone`, " \
          "`withhold_result_user_id_card`, `withhold_result_user_bank_card`, `withhold_result_type`, " \
          "`withhold_result_status`, `withhold_result_channel`, `withhold_result_serial_no`, " \
          "`withhold_result_create_at`, `withhold_result_channel_key`, `withhold_result_channel_fee`, " \
          "`withhold_result_finish_at`, `withhold_history_sync_at`, `withhold_result_user_name_encrypt`, " \
          "`withhold_result_user_phone_encrypt`, `withhold_result_user_id_card_encrypt`, " \
          "`withhold_result_user_bank_card_encrypt`) SELECT `withhold_result_id`, `withhold_result_asset_id`, " \
          "`withhold_result_asset_item_no`, `withhold_result_asset_type`, `withhold_result_asset_period`, " \
          "`withhold_result_amount`, `withhold_result_user_name`, `withhold_result_user_phone`, " \
          "`withhold_result_user_id_card`, `withhold_result_user_bank_card`, `withhold_result_type`, " \
          "`withhold_result_status`, `withhold_result_channel`, `withhold_result_serial_no`, " \
          "`withhold_result_create_at`, `withhold_result_channel_key`, `withhold_result_channel_fee`, " \
          "`withhold_result_finish_at`, now(), `withhold_result_user_name_encrypt`, " \
          "`withhold_result_user_phone_encrypt`, `withhold_result_user_id_card_encrypt`, " \
          "`withhold_result_user_bank_card_encrypt`FROM withhold_result WHERE " \
          "withhold_result_asset_item_no='%s' and withhold_result_status='success'" % item_no
    gc.BIZ_DB.insert(sql)


def set_asset_status(item_no, status):
    sql = "update asset set asset_status = '%s' where asset_item_no = '%s'" % (status, item_no)
    gc.BIZ_DB.update(sql)


def delete_capital_asset_by_item_no(item_no, channel='noloan'):
    sql = "delete from capital_asset where " \
          "capital_asset_item_no='%s' and capital_asset_channel='%s'" % (item_no, channel)
    gc.BIZ_DB.delete(sql)


def delete_capital_transaction_by_item_no(item_no, channel='noloan'):
    sql = "DELETE FROM capital_transaction WHERE capital_transaction_asset_id IN (SELECT capital_asset_id FROM " \
          "capital_asset  WHERE capital_asset_item_no='%s' and capital_asset_channel='%s')" % (item_no, channel)
    gc.BIZ_DB.delete(sql)


def create_attachment(item_no, attachment_type, attachment_name, attachment_url):
    sql = "INSERT INTO `asset_attachment` (" \
          "`asset_attachment_asset_item_no`, `asset_attachment_type`, `asset_attachment_contract_code`, " \
          "`asset_attachment_type_text`, `asset_attachment_url`, " \
          "`asset_attachment_status`, `asset_attachment_from_system`) " \
          "VALUES ('%s', %s, '%s', '%s', '%s', 1, 'contract')" % \
          (item_no, attachment_type, get_random_str(10), attachment_name, attachment_url)
    result = gc.BIZ_DB.insert(sql)
    return result


def set_asset_loan_channel(item_no, channel):
    sql = "update asset set asset_loan_channel = '%s' where asset_item_no = '%s'" % (channel, item_no)
    gc.BIZ_DB.update(sql)


def change_asset_due_at_in_biz(advance_month, item_no, item_no_x, is_grant_day=False, advance_day=-1,
                               compensate_time=None):
    """
    修改资产放款时间及资产还款计划的到日期
    :param advance_month: 提前多少个月, 负数，推后是正数
    :param advance_day: 提前多少天, 负数，推后是正数
    :param item_no: 大单资产编号
    :param item_no_x: 小单资产编号
    :param compensate_time: 资方还款计划代偿日
    :param is_grant_day: 是否是放款日
    :return:
    """
    asset = get_asset_info_by_item_no(item_no)
    count = int(asset[0]["asset_period_count"])
    period_day = int(asset[0]["asset_product_category"])
    if count == 1:
        grant_time = get_calc_date_base_today(day=0) if is_grant_day else \
            get_calc_date_base_today(day=advance_day)
    else:
        grant_time = get_calc_date_base_today(month=advance_month) if is_grant_day else \
            get_calc_date_base_today(month=advance_month, day=advance_day)
    for period in range(1, count + 1):
        due_delay_month = period + advance_month
        if count == 1:
            due_time = get_calc_date_base_today(day=period_day, fmt="%Y-%m-%d") if is_grant_day else \
                get_calc_date_base_today(day=period_day + advance_day, fmt="%Y-%m-%d")
        else:
            due_time = get_calc_date_base_today(month=due_delay_month, fmt="%Y-%m-%d") if is_grant_day else \
                get_calc_date_base_today(month=due_delay_month, day=advance_day, fmt="%Y-%m-%d")
            cap_due_time = due_time[:-2] + compensate_time if compensate_time else due_time
        for item in (item_no, item_no_x):
            # 更新asset记录
            if item:
                if period == 1:
                    item_no_str = 'update asset set asset_grant_at = "{0}", asset_effect_at = ' \
                                  '"{0}", asset_actual_grant_at = "{0}"' \
                                  ' where asset_item_no = "{1}"'.format(grant_time,
                                                                        item)
                    gc.BIZ_DB.update(item_no_str)
                    # 更新capital_asset
                    capital_asset_str = 'update capital_asset set capital_asset_granted_at = "{0}" where ' \
                                        'capital_asset_item_no = "{1}"'.format(grant_time, item)
                    gc.BIZ_DB.update(capital_asset_str)
                # 更新asset_tran记录
                item_no_period_first_dt = 'update dtransaction set dtransaction_expect_finish_time = "{0}" WHERE ' \
                                          'dtransaction_asset_id IN(SELECT asset_id FROM asset WHERE ' \
                                          'asset_item_no="{1}") and dtransaction_period = {2}'.format(due_time,
                                                                                                      item, period)
                item_no_period_first_ft = 'update ftransaction set ftransaction_expect_finish_time = "{0}" WHERE ' \
                                          'ftransaction_asset_id IN(SELECT asset_id FROM asset WHERE ' \
                                          'asset_item_no="{1}") and ftransaction_period = {2}'.format(due_time,
                                                                                                      item, period)
                gc.BIZ_DB.update(item_no_period_first_dt)
                gc.BIZ_DB.update(item_no_period_first_ft)

                item_no_period_first = 'update asset_tran set asset_tran_due_at = "{0}"  ' \
                                       'where asset_tran_asset_item_no = "{1}" and ' \
                                       'asset_tran_period = {2}'.format(due_time, item, period)
                gc.BIZ_DB.update(item_no_period_first)

                capital_tran = 'UPDATE capital_transaction SET capital_transaction_expect_finished_at = "{0}" ' \
                               'WHERE capital_transaction_asset_id in (SELECT capital_asset_id FROM capital_asset ' \
                               'WHERE capital_asset_item_no= "{1}") AND capital_transaction_period = {2}'.format(
                    cap_due_time, item, period)
                gc.BIZ_DB.update(capital_tran)

    return item_no, item_no_x, ""


def wait_biz_asset_appear(item_no, wait_time=120):
    result = False
    for i in range(wait_time):
        asset = get_biz_asset_info_by_item_no(item_no)
        if asset is not None and len(asset) > 0:
            result = True
            break
        else:
            time.sleep(2)
    return result


def wait_biz_asset_tran_appear(item_no, wait_time=120, check_index=0):
    result = False
    for i in range(wait_time):
        asset_tran = get_biz_asset_tran_by_item_no(item_no)
        if asset_tran is not None and asset_tran[check_index]["asset_tran_status"] == "finish":
            result = True
            break
        else:
            time.sleep(2)
    return result


def update_asset(item_no, **kwargs):
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update asset set %s where asset_item_no='%s'" % (sql_params[:-2], item_no)
    gc.BIZ_DB.update(sql)


def update_asset_extend_by_item_no(item_no, **kwargs):
    asset = get_biz_asset_info_by_item_no(item_no)
    sql_params = ""
    for key, value in kwargs.items():
        sql_params = sql_params + "`" + key + "`='" + value + "', "
    sql = "update asset_extend set %s where asset_extend_asset_id='%s'" % (sql_params[:-2], asset[0]['asset_id'])
    gc.BIZ_DB.update(sql)


def wait_central_task_appear(order_no, task_type, timeout=60, is_one=False):
    task_list = []
    for i in range(timeout):
        task_list = gc.BIZ_DB.query("select task_id, task_type, task_status "
                                    "from central_task where task_order_no='{0}' and task_status ='open' "
                                    "and task_type = '{1}'"
                                    " order by task_id desc".format(order_no, task_type))
        if task_list:
            return task_list
        time.sleep(0.1)
    if not task_list:
        raise Exception("no task found, task_order_no:%s, task_type:%s" % (order_no, task_type))
    if len(task_list) > 1 and is_one:
        raise ValueError("must need one task,but there found more than one with order is :{0}"
                         ", type is :{1}".format(order_no, task_type))


def wait_central_task_close_by_id(task_id, timeout=100):
    task_list = []
    for i in range(timeout):
        task_list = gc.BIZ_DB.query(
            "select * from central_task where task_id='{0}' and task_status ='close' ".format(task_id))
        if task_list:
            break
        time.sleep(1)
    if not task_list:
        LogUtil.log_info("no task found, task_id:{0}".format(task_id))
        # raise Exception("no task found, task_id:{0}".format(task_id))


def update_before_capital_tran_finish_by_item_no_and_period(item_no, period):
    sql = "update capital_transaction set capital_transaction_operation_type='compensate', " \
          "capital_transaction_repaid_amount=capital_transaction_origin_amount, " \
          "capital_transaction_status='finished', " \
          "capital_transaction_repaid_amount=capital_transaction_origin_amount" \
          " where capital_transaction_asset_item_no='{0}' " \
          "and capital_transaction_period < {1}".format(item_no, period)
    gc.BIZ_DB.update(sql)


def get_user_at_count(item_no, item_no_loan):
    sql = "select count(1) as count from central_task where task_order_no in ('{0}', '{1}') " \
          "and task_status='open' and task_type='CapitalAssetUserRepay'".format(item_no, item_no_loan)
    return gc.BIZ_DB.query(sql)[0]['count']


def get_central_task_request_data(order_no, task_type):
    task_ret = gc.BIZ_DB.query("select task_id, task_request_data from central_task where task_order_no='{0}' "
                               "and task_type = '{1}' and task_status='open'".format(order_no, task_type))
    for task in task_ret:
        task['repayList'] = json.loads(task['task_request_data'])["repayList"]
        task['assetItemNo'] = json.loads(task['task_request_data'])["assetItemNo"]
        task['rechargeList'] = json.loads(task['task_request_data'])["rechargeList"][0]["serialNo"]
    return task_ret


def get_central_task_id_by_order_no(order_no):
    gc.BIZ_DB.update("update central_task set task_next_run_at = DATE_SUB(now(), interval 20 minute) "
                     "where task_order_no = '%s'" % order_no)
    task_list = gc.BIZ_DB.query("select task_id, task_status "
                                "from central_task where task_order_no='%s' and task_status<>'close' order by task_id desc" % order_no)
    return task_list


def get_central_task_id_by_request_order_no(order_no):
    gc.BIZ_DB.update("update central_task set task_next_run_at = DATE_SUB(now(), interval 20 minute) "
                     "where task_request_data like '%%%s%%'" % order_no)
    task_list = gc.BIZ_DB.query("select task_id, task_status "
                                "from central_task where task_request_data like '%%%s%%' order by task_id desc" % order_no)
    return task_list


def get_central_task_id_by_type(order_no, task_type):
    gc.BIZ_DB.update("update central_task set task_next_run_at = DATE_SUB(now(), interval 20 minute) "
                     "where task_order_no = '{0}' and task_type = '{1}' and task_status='open' ".format(order_no,
                                                                                                        task_type))
    task_list = gc.BIZ_DB.query("select task_id, task_status from central_task where task_order_no = '{0}' "
                                "and task_type = '{1}' and task_status in ('open', 'running') ".format(order_no,
                                                                                                       task_type))
    return task_list


def get_central_msg_id_by_order_no(order_no):
    gc.BIZ_DB.update("update central_sendmsg set sendmsg_next_run_at = DATE_SUB(now(), interval 20 minute) "
                     "where sendmsg_order_no ='%s'" % order_no)
    msg_list = gc.BIZ_DB.query("select * from central_sendmsg where sendmsg_order_no='%s'" % order_no)
    return msg_list


def get_capital_notify_by_asset_item_no(item_no, withhold_serial_no=None):
    sql = 'select * from capital_notify where capital_notify_asset_item_no="{}" '.format(item_no)
    if withhold_serial_no:
        sql = sql + ' and capital_notify_withhold_serial_no="{}"'.format(withhold_serial_no)
    sql = sql + ' order by capital_notify_id DESC'
    capital_notify = gc.BIZ_DB.query(sql)
    return capital_notify


def get_capital_notify_req_data_by_item_no(item_no, withhold_serial_no=None):
    notify_info = get_capital_notify_by_asset_item_no(item_no, withhold_serial_no)
    capital_notify_info = None
    if notify_info is not None:
        capital_notify_info = json.loads(notify_info[0]['capital_notify_req_data'])
    return capital_notify_info


def get_capital_notify_req_data_param_by_item_no(item_no):
    notify_info = get_capital_notify_by_asset_item_no(item_no)
    capital_notify_info_param = None
    if notify_info is not None:
        capital_notify_info = json.loads(notify_info[0]['capital_notify_req_data'])
        capital_notify_info_param = json.loads(capital_notify_info['applyNoticeParam'])
    return capital_notify_info_param


def get_holiday(date):
    sql = 'select holiday_status from holiday where holiday_date = "{0}"'.format(date)
    return gc.BIZ_DB.query(sql)


def get_capital_notify_record(item_no, start_period, end_period, notify_type, status):
    sql = 'select * from capital_notify where capital_notify_asset_item_no="{0}" and capital_notify_period_start={1} ' \
          'and capital_notify_period_start={2} and capital_notify_type in {3} ' \
          'and capital_notify_status={4}'.format(item_no, start_period, end_period, notify_type, status)
    capital_notify = gc.BIZ_DB.query(sql)
    return capital_notify


def get_central_task_by_task_order_no(order_no):
    sql = 'select * from central_task where task_order_no={}'.format(order_no)
    task = gc.BIZ_DB.query(sql)
    return task


def get_central_sendmsg_by_order_no_and_type(order_no, type):
    sql = 'select * from central_sendmsg where sendmsg_order_no="{}" and sendmsg_type="{}"'.format(order_no, type)
    task = gc.BIZ_DB.query(sql)
    return task


def update_capital_notify_plan_at_by_item_no(item_no, count_hour=1):
    sql = "update capital_notify set capital_notify_plan_at=date_sub(now(),interval %s hour) where " \
          "capital_notify_asset_item_no='%s'" % (count_hour, item_no)
    gc.BIZ_DB.update(sql)


def delete_asset_sync_to_rbiz_task(timeout=10):
    for i in range(timeout):
        result = gc.BIZ_DB.query("select * from task where task_type='AssetSyncToRBiz' and task_status='open' limit 5")
        if result:
            break
        else:
            time.sleep(1)
    sql = "delete from task where task_type='AssetSyncToRBiz'"
    gc.BIZ_DB.delete(sql)


def insert_asset(item_no, channel, status):
    sql = "INSERT INTO asset (asset_item_no, asset_type, asset_sub_type, asset_period_type, asset_period_count,  asset_cmdb_product_number, asset_create_at,  asset_grant_at, asset_effect_at, asset_actual_grant_at, asset_due_at, asset_payoff_at, asset_update_at, asset_from_system, asset_status, asset_principal_amount, asset_granted_principal_amount, asset_loan_channel, asset_interest_amount, asset_fee_amount, asset_version, asset_interest_rate, asset_from_system_name, asset_owner, asset_from_app) " \
          "VALUES ('%s', 'paydayloan', 'multiple', 'month', 12, '', '2021-05-06 15:37:15', '2021-05-06 15:37:14', '2021-05-06 15:38:20', '2021-05-06 15:38:20', '2022-05-06 00:00:00', '2022-05-06 00:00:00', '2021-05-06 16:17:30', 'strawberry', '%s', 900000, 900000, '%s', 24564, 52260, 1620289033760, 5.000, '重庆草莓', 'KN', '重庆草莓');" \
          % (item_no, status, channel)
    gc.BIZ_DB.insert(sql)


def insert_asset_extend(item_no):
    asset = get_biz_asset_info_by_item_no(item_no)[0]
    sql = "INSERT INTO asset_extend (asset_extend_asset_id, asset_extend_loan_usage, asset_extend_charge_type, asset_extend_creditor, asset_extend_ref_item_no, asset_extend_ref_order_type, asset_extend_ref_order_no, asset_extend_withholding_amount, asset_extend_risk_level, asset_extend_sub_order_type, asset_extend_product_name, asset_extend_max_late_fee, asset_extend_overdue_guarantee_amount, asset_extend_info) " \
          "VALUES ('%s', 1, 1, '%s', '', 'apr36', 'noloan_%s', 0, '2', '', '', NULL, 0, '')" \
          % (asset["asset_id"], asset["asset_loan_channel"], item_no)
    gc.BIZ_DB.insert(sql)


def delete_asset_tran_by_item_no(item_no):
    sql = "DELETE FROM asset_tran WHERE asset_tran_asset_item_no='%s'" % item_no
    gc.BIZ_DB.delete(sql)


def delete_dtransaction_by_item_no(item_no):
    sql = "DELETE FROM dtransaction WHERE dtransaction_asset_id IN(SELECT asset_id FROM asset WHERE asset_item_no IN ('%s'))" % item_no
    gc.BIZ_DB.delete(sql)


def delete_ftransaction_by_item_no(item_no):
    sql = "DELETE FROM ftransaction WHERE ftransaction_asset_id IN (SELECT asset_id FROM asset WHERE asset_item_no IN ('%s'))" % item_no
    gc.BIZ_DB.delete(sql)


def delete_fee_by_item_no(item_no):
    sql = "DELETE FROM fee WHERE fee_asset_id IN(SELECT asset_id FROM asset WHERE `asset_item_no` IN ('%s'))" % item_no
    gc.BIZ_DB.delete(sql)


def delete_withhold_result_transaction_by_item_no(item_no):
    sql = "DELETE FROM withhold_result_transaction WHERE withhold_result_transaction_withhold_result_id IN (SELECT " \
          "withhold_result_id FROM withhold_result  WHERE `withhold_result_asset_item_no` IN ('%s'))" % item_no
    gc.BIZ_DB.delete(sql)


def insert_asset_loan_record(item_no, channel):
    asset = get_biz_asset_info_by_item_no(item_no)
    sql = "INSERT INTO `asset_loan_record` (`asset_loan_record_asset_id`, `asset_loan_record_amount`, `asset_loan_record_withholding_amount`, `asset_loan_record_channel`, `asset_loan_record_status`, `asset_loan_record_identifier`, `asset_loan_record_trade_no`, `asset_loan_record_due_bill_no`, `asset_loan_record_commission_amount`, `asset_loan_record_pre_fee_amount`, `asset_loan_record_service_fee_amount`, `asset_loan_record_is_deleted`, `asset_loan_record_finish_at`, `asset_loan_record_create_at`, `asset_loan_record_update_at`, `asset_loan_record_trans_property`, `asset_loan_record_pre_interest`, `asset_loan_record_commission_amt_interest`, `asset_loan_record_grant_at`)" \
          "VALUES(%s, %s, 0, '%s', 6, '%s', '%s', '%s', 0, 0, 0, 0, now(), now(), now(), '', 0, 0, now());" \
          % (asset[0]['asset_id'], asset[0]["asset_principal_amount"] * 100, channel, asset[0]["asset_item_no"],
             "TN" + asset[0]["asset_item_no"], "DN" + asset[0]["asset_item_no"])
    gc.BIZ_DB.insert(sql)
