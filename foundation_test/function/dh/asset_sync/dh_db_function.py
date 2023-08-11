# @Time    : 2020/7/30 2:32 下午
# @Author  : yuanxiujing
# @File    : dh_db_function.py
# @Software: PyCharm
import foundation_test.config.dh.db_const as dc


# env = get_sysconfig("--env")
# db = DataBase("qsq_%s" % env)
# env 传入 fox


# 获取资产信息
def get_asset_info_by_item_no(item_no):
    sql = "select * from asset where asset_item_number='%s'" % item_no
    asset_info = dc.DH_DB.query(sql)
    return asset_info


# 获取客户信息
def get_customer_info_by_from_system_name(asset_from_system_name):
    sql = "select id from original_customer where name = '%s'" % asset_from_system_name
    customer = dc.DH_DB.query(sql)
    return customer


# 获取还款计划
def get_transaction_info_by_asset(item_no):
    sql = "select asset_transaction_type, asset_transaction_amount,asset_transaction_status, asset_transaction_expect_finish_time," \
          "asset_transaction_finish_at, asset_transaction_period,asset_transaction_decrease_amount, asset_transaction_repaid_amount," \
          "IFNULL(asset_transaction_late_status, 0) as asset_transaction_late_status, asset_transaction_late_days " \
          "from asset_transaction " \
          "atr left join asset a on atr.asset_transaction_asset_id = a.asset_id where asset_item_number = '%s'" % item_no
    transaction_info = dc.DH_DB.query(sql)
    print("获取还款计划  ", sql)
    return transaction_info


# 获取债务人信息
def get_debtor_info(original_customer_id, debtor_enc_idnum):
    sql = "select * from debtor where original_customer_id = '%s' and enc_idnum = '%s'" % (
        original_customer_id, debtor_enc_idnum)
    debtor_info = dc.DH_DB.query(sql)
    return debtor_info


# 获取借款人信息，包含亲戚、同事等个人信息
def get_individual_info(individual_enc_idnum):
    sql = "select * from individual where enc_individual_idnum = '%s'" % individual_enc_idnum
    individual_info = dc.DH_DB.query(sql)
    return individual_info


# 获取债务概览信息
def get_debtor_arrears_info(original_customer_id, debtor_enc_idnum):
    sql = "select das.* " \
          "from debtor_arrears das " \
          "left join debtor d on das.debtor_id = d.id " \
          "where d.original_customer_id = '%s' and d.enc_idnum = '%s'" % \
          (original_customer_id, debtor_enc_idnum)
    debtor_arrears_info = dc.DH_DB.query(sql)
    print("获取债务概览信息 ", sql)
    return debtor_arrears_info


# 获取债务主资产信息
def get_main_asset_info(original_customer_id, debtor_enc_idnum):
    sql = "SELECT a.asset_status AS 'status', x.asset_count AS 'asset_count', a.asset_id AS 'asset_id', a.asset_type AS 'asset_type', " \
          "a.asset_late_status AS 'late_status', a.asset_late_days AS 'late_days', aio.state AS 'inner_outer' " \
          "FROM debtor_asset ad " \
          "LEFT JOIN asset a ON ad.asset_id = a.asset_id " \
          "LEFT JOIN(" \
          "SELECT max(a.asset_late_days) AS 'max_late_days',count(1) AS 'asset_count',ad.debtor_id " \
          "FROM debtor_asset ad " \
          "LEFT JOIN debtor d ON d.id = ad.debtor_id " \
          "LEFT JOIN asset a ON ad.asset_id = a.asset_id " \
          "WHERE a.asset_status = 'repay' " \
          "AND d.original_customer_id = '%s' " \
          "AND d.enc_idnum = '%s' " \
          "AND NOT EXISTS (SELECT 1 FROM asset_freeze af WHERE af.asset_item_number = ad.asset_item_number AND af.freeze_status='freezing') " \
          "AND NOT EXISTS (SELECT 1 FROM asset_inner_outer AS aio WHERE aio.asset_id = ad.asset_id AND aio.state='stop')" \
          ") x ON ad.debtor_id = x.debtor_id " \
          "LEFT JOIN asset_inner_outer aio ON aio.asset_id = ad.asset_id " \
          "LEFT JOIN debtor d ON d.id = ad.debtor_id " \
          "WHERE a.asset_status = 'repay' " \
          "AND aio.state<>'stop' " \
          "AND a.asset_late_days = x.max_late_days " \
          "AND d.original_customer_id = '%s' " \
          "AND d.enc_idnum = '%s' " \
          "AND NOT EXISTS (SELECT 1 FROM asset_freeze af WHERE af.asset_item_number = ad.asset_item_number AND af.freeze_status='freezing') " \
          "ORDER BY a.asset_principal_amount DESC limit 1" % (
              original_customer_id, debtor_enc_idnum, original_customer_id, debtor_enc_idnum)
    main_asset_info = dc.DH_DB.query(sql)
    print("获取债务主资产信息 ", sql)
    return main_asset_info


# 计算债务金额
def get_calculate_das_amount(original_customer_id, debtor_enc_idnum):
    sql = "SELECT " \
          "sum(asset_principal_amount) AS principal_amount, sum(asset_interest_amount) AS interest_amount, sum(asset_fee_amount) AS fee_amount, " \
          "sum(asset_penalty_amount) AS penalty_amount, " \
          "sum(asset_principal_amount)+sum(asset_interest_amount)+sum(asset_fee_amount)+sum(asset_penalty_amount) AS arrears_total_amount, " \
          "sum(asset_repaid_principal_amount) AS repaid_principal_amount, sum(asset_repaid_interest_amount) AS repaid_interest_amount, " \
          "sum(asset_repaid_fee_amount) AS repaid_fee_amount, sum(asset_repaid_penalty_amount) AS repaid_penalty_amount, " \
          "sum(asset_repaid_principal_amount) +sum(asset_repaid_interest_amount)+sum(asset_repaid_fee_amount)+sum(asset_repaid_penalty_amount) " \
          "AS repaid_total_amount, " \
          "sum(overdue_principal_amount) AS overdue_principal_amount, sum(overdue_interest_amount) AS overdue_interest_amount, sum(overdue_fee_amount) " \
          "AS overdue_fee_amount, " \
          "sum(overdue_penalty_amount) AS overdue_penalty_amount, " \
          "sum(overdue_principal_amount)+sum(overdue_interest_amount)+sum(overdue_fee_amount)+sum(overdue_penalty_amount) AS overdue_total_amount, " \
          "sum(recovery_principal_amount) AS recovery_principal_amount, sum(recovery_interest_amount) AS recovery_interest_amount, sum(recovery_fee_amount) " \
          "AS recovery_fee_amount, sum(recovery_penalty_amount) AS recovery_penalty_amount, " \
          "sum(recovery_principal_amount)+sum(recovery_interest_amount)+sum(recovery_fee_amount)+sum(recovery_penalty_amount) AS recovery_total_amount " \
          "FROM debtor_asset ad " \
          "LEFT JOIN asset a ON ad.asset_id = a.asset_id " \
          "LEFT JOIN asset_inner_outer aio ON aio.asset_id = ad.asset_id " \
          "LEFT JOIN debtor d ON d.id = ad.debtor_id " \
          "WHERE a.asset_status = 'repay' " \
          "AND aio.state<>'stop' AND d.original_customer_id = '%s' AND d.enc_idnum = '%s' " \
          "AND NOT EXISTS(SELECT 1 FROM asset_freeze af WHERE af.asset_item_number = ad.asset_item_number AND af.freeze_status='freezing')" \
          % (original_customer_id, debtor_enc_idnum)
    calculate_das_amount = dc.DH_DB.query(sql)
    print("计算债务金额 ", sql)
    return calculate_das_amount


# 获取债务人资产信息
def get_debtor_asset_by_item_no(item_no):
    sql = "select count(*) as count, da.* from debtor_asset da where asset_item_number='%s' " % item_no
    debtor_asset_info = dc.DH_DB.query(sql)
    return debtor_asset_info


# 获取资产与借款人的关联关系
def get_asset_ref_subject(asset_id):
    sql = "select * from asset_ref_subject where asset_ref_subject_asset_id = '%s'" % asset_id
    asset_ref_subject = dc.DH_DB.query(sql)
    return asset_ref_subject


# 获取最新跟进信息
def get_debtor_collect(debtor_id):
    sql = "select * from debtor_collect where debtor_id = '%s'" % debtor_id
    debtor_collect = dc.DH_DB.query(sql)
    return debtor_collect


# 获取资产的内外状态
def get_inner_outer(item_no):
    sql = "select state from asset_inner_outer where asset_item_num='%s'" % item_no
    state = dc.DH_DB.query(sql)
    return state


# 获取资产的历史信息
def get_asset_history(item_no):
    sql = "select * from asset_history where asset_item_number='%s'" % item_no
    asset_history_info = dc.DH_DB.query(sql)
    return asset_history_info


# 修改债务概览金额
def set_arrears_amount(original_customer_id, debtor_enc_idnum):
    sql = "update debtor_arrears das " \
          "left join debtor d on das.debtor_id = d.id " \
          "set das.overdue_total_amount = 0 " \
          "where d.original_customer_id = '%s' and d.enc_idnum = '%s'" \
          % (original_customer_id, debtor_enc_idnum)
    dc.DH_DB.update(sql)


# 修改资产asset_inner_outer状态
def set_asset_inner_outer(item_no, state):
    sql = "update asset_inner_outer set state = '%s' where asset_item_num = '%s'" % (state, item_no)
    dc.DH_DB.update(sql)


# 新增资产冻结
def set_asset_freeze(item_no):
    sql = "INSERT INTO asset_freeze " \
          "(asset_id, asset_item_number, freeze_at, unfreeze_at, freeze_status, attachment_batch_no, freeze_channel, freeze_type, remark, " \
          "create_at, create_user_id, create_user_name, update_at, update_user_id, update_user_name) " \
          "select asset_id,asset_item_number, curdate(),NULL, 'freezing', '', '贷后白名单', 'FKWhiteList', " \
          "'自动化测试',now(),0,'system',now(),0,'system' " \
          "from asset where asset_item_number = '%s'" % item_no
    dc.DH_DB.insert(sql)


# 新增债务人冻结
def set_asset_borrower_freeze(original_customer_id, enc_name, enc_tel, enc_idnum):
    sql = "INSERT INTO asset_borrower_freeze " \
          "(name, tel, idnum, original_customer_id, freeze_at, unfreeze_at, freeze_status, attachment_batch_no, freeze_type, remark, " \
          "create_at, create_user_id, create_user_name, update_at, update_user_id, update_user_name, freeze_channel, enc_name, code_name, " \
          "enc_tel, code_tel, enc_idnum, code_idnum)" \
          "values" \
          "(NULL, NULL, '', '%s', curdate(), NULL, 'freezing', NULL, '6', '自动化测试', now(), 0, 'system', now(), 0, 'system', '贷后白名单', '%s', " \
          "NULL, '%s', NULL, '%s', NULL)" % (original_customer_id, enc_name, enc_tel, enc_idnum)
    dc.DH_DB.insert(sql)


# 获取国内登录session_id
def get_session_id(sys_user_name):
    sql = "select * from sys_session_log where sys_user_name = '%s' and active = 1 " \
          "and stop_time is null " \
          "and date_add(start_time, interval time_out/1000 second) > now() " \
          "order by create_at desc limit 1" % sys_user_name
    session_id_info = dc.DH_DB.query(sql)
    print("获取国内登录session_id,session_id_info=", session_id_info)
    return session_id_info


# 登录前清除session
def stop_session(sys_user_name):
    sql = "update sys_session_log set stop_time = now(),active = 0,stopped=1 where sys_user_name = '%s' and active = 1 " \
          "and stop_time is null " \
          "and date_add(start_time, interval time_out/1000 second) > now()" % sys_user_name
    dc.DH_DB.query(sql)


# 获取asset_summary_recovery总资产变动信息
def get_summary_recovery(item_no):
    sql = "select count(*) as count,id, asset_id, batch_num, serial_num, asset_item_number, sum(principal_amount) as principal_amount, " \
          "sum(recovery_principal_amount) as recovery_principal_amount, " \
          "sum(interest_amount) as interest_amount, sum(recovery_interest_amount) as recovery_interest_amount, " \
          "sum(penalty_amount) as penalty_amount, sum(decrease_penalty_amount) as decrease_penalty_amount, " \
          "sum(recovery_penalty_amount) as recovery_penalty_amount, " \
          "sum(fee_amount) as fee_amount, sum(recovery_fee_amount) as recovery_fee_amount, " \
          "sum(repaid_total_amount) as repaid_total_amount, " \
          "sum(repaid_principal_amount) as repaid_principal_amount, " \
          "sum(repaid_interest_amount) as repaid_interest_amount, " \
          "sum(repaid_fee_amount) as repaid_fee_amount, sum(repaid_penalty_amount) as repaid_penalty_amount, " \
          "late_days, late_status, asset_status, create_at, update_at, repay_date from asset_summary_recovery asr" \
          " where asset_item_number = '%s'" % item_no
    summary_recovery = dc.DH_DB.query(sql)
    print("获取asset_summary_recovery总资产变动信息 ", sql)
    return summary_recovery


# 获取asset_period_recovery资产按期次的变动回款表
def get_period_recovery(item_no):
    sql = "select " \
          "id, asset_summary_recovery_id, asset_id, batch_num, serial_num, asset_item_number, repaid_period, sum(repaid_total_amount) as " \
          "repaid_total_amount, sum(repaid_principal_amount) as repaid_principal_amount, sum(repaid_interest_amount) as repaid_interest_amount, " \
          "sum(repaid_fee_amount) as repaid_fee_amount, sum(repaid_penalty_amount) as repaid_penalty_amount, late_days, late_status, asset_status, " \
          "create_at, update_at, repay_date, period_status " \
          "from asset_period_recovery where asset_item_number = '%s' " \
          "group by repaid_period" % item_no
    period_recovery = dc.DH_DB.query(sql)
    print("获取asset_period_recovery资产按期次的变动回款表 ", sql)
    return period_recovery


# 获取collect_recovery资产催员回款表
def get_collect_recovery(item_no):
    sql = "select count(*) as count," \
          "id, user_id, user_name, assigned_date, asset_id, batch_num, serial_num, asset_item_number, " \
          "principal_amount, interest_amount, penalty_amount, decrease_penalty_amount," \
          "sum(repaid_total_amount) as repaid_total_amount, " \
          "sum(repaid_principal_amount) as repaid_principal_amount, " \
          "sum(repaid_interest_amount) as repaid_interest_amount," \
          "sum(repaid_penalty_amount) as repaid_penalty_amount," \
          "create_at, update_at, late_days, late_status, asset_status, fee_amount, " \
          "sum(repaid_fee_amount) as repaid_fee_amount, " \
          "company_id, company_name, sys_user_id, sys_user_name, group_leader_id, group_leader_name, director_id, director_name,manager_id," \
          "manager_name, mission_log_id, repay_date from collect_recovery cr where asset_item_number = '%s' and serial_num <> ''" \
          "group by repay_date" % item_no
    collect_recovery = dc.DH_DB.query(sql)
    print("获取collect_recovery资产催员回款表 ", sql)
    return collect_recovery


# 获取collect_recovery资产催员回款表
def get_count_collect_recovery(item_no):
    sql = "select count(*) as count from collect_recovery cr where asset_item_number = '%s' and serial_num <> ''" % item_no
    cr_count = dc.DH_DB.query(sql)
    return cr_count


# 获取催员回款关联的mission_log信息
def get_mission_log(asset_id, repay_date):
    sql = "select * from mission_log ml " \
          "where 1=1 and ml.mission_log_asset_id = '%s' " \
          "and ml.mission_log_create_at <= '%s' " \
          "and ml.mission_log_operator = 'assign' " \
          "order by ml.mission_log_id desc limit 1" % (asset_id, repay_date)
    mission_log = dc.DH_DB.query(sql)
    return mission_log


# 根据debtor_id获取mission_log信息
def get_mission_log_by_debtor_id(debtor_id):
    sql = "select * from mission_log where debtor_id = %s" % debtor_id
    mission_log = dc.DH_DB.query(sql)
    return mission_log


# 根据asset_id判断是否已分案给催员
def get_collect_recovery_by_asset_id(asset_id):
    sql = "select * from collect_recovery where asset_id = %s and serial_num = '' and repay_date is NULL " \
          "order by id desc " \
          "limit 1" % asset_id
    collect_recovery = dc.DH_DB.query(sql)
    return collect_recovery


# 获取所属催收员公司信息
def get_company():
    sql = "SELECT a.company_id AS company_id, c.name AS company_name FROM sys_user a " \
          "LEFT JOIN sys_office c ON c.id = a.company_id " \
          "LEFT JOIN sys_area ca ON ca.id = c.area_id " \
          "LEFT JOIN sys_office o ON o.id = a.office_id " \
          "LEFT JOIN sys_area oa ON oa.id = o.area_id " \
          "LEFT JOIN sys_user cu ON cu.id = c.primary_person " \
          "LEFT JOIN sys_user cu2 ON cu2.id = c.deputy_person " \
          "LEFT JOIN sys_user ou ON ou.id = o.primary_person " \
          "LEFT JOIN sys_user ou2 ON ou2.id = o.deputy_person " \
          "WHERE a.id ='1e56501bd6734c528fa2bfcdf9cd543b'"
    company_info = dc.DH_DB.query(sql)
    return company_info


# 根据用户id查询上级、上上级、上上上级
def get_user_parents():
    sql = "select su1.id as sys_user_id, su1.name as sys_user_name, " \
          "su2.id as group_leader_id, su2.name as group_leader_name, " \
          "su3.id as director_id, su3.name as director_name, " \
          "su4.id as manager_id, su4.name as manager_name " \
          "from sys_user su1 " \
          "left join sys_office so1 on so1.id=su1.office_id " \
          "left join sys_user su2 on su2.id = so1.PRIMARY_PERSON " \
          "left join sys_office so2 on so1.parent_id = so2.id " \
          "left join sys_user su3 on su3.id = so2.PRIMARY_PERSON " \
          "left join sys_office so3 on so3.id = so2.parent_id " \
          "left join sys_user su4 on so3.PRIMARY_PERSON = su4.id " \
          "where su1.id='1e56501bd6734c528fa2bfcdf9cd543b'"
    user_parents_info = dc.DH_DB.query(sql)
    return user_parents_info


# 根据工具包唯一标识(主包*工具包名*渠道*系统)获取工具包信息
def get_tool_package(hash_value):
    sql = "select * from asset_tool_package where hash = '%s'" % hash_value
    tool_info = dc.DH_DB.query(sql)
    return tool_info


# 清除工具包信息
def del_tool_package():
    sql = "delete from asset_tool_package"
    return dc.DH_DB.delete(sql)
