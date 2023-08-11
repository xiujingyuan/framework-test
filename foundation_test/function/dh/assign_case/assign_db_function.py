import random

import foundation_test.config.dh.db_const as dc
from foundation_test.util.log.log_util import LogUtil

# env = get_sysconfig("--env")
# db = DataBase("arcticfox-india")
# 海外传入 arcticfox-india


def get_overseas_session_id():
    sql = "select * from sys_session_log where sys_user_name = 'yxj' and active = 1 " \
          "and stop_time is null " \
          "and date_add(start_time, interval time_out/1000 second) > now() " \
          "order by create_at desc limit 1"
    session_id_info = dc.DH_DB.query(sql)
    LogUtil.log_info("获取海外登录session_id，SQL=%s" % sql)
    return session_id_info


# 修改未分案的案件天数为99
def update_unassigned_cases(asset_type, begin_late_days, end_late_days):
    sql = "UPDATE debtor_arrears ar " \
          "SET ar.late_days = 99 " \
          "WHERE 1=1 " \
          "AND NOT exists(" \
          "SELECT 1 FROM mission m " \
          "WHERE m.mission_asset_id = ar.asset_id " \
          "AND (m.assigned_sys_user_id is NOT null OR m.assigned_group_id is NOT null)" \
          ")" \
          "AND ar.inner_outer = 'inner' " \
          "AND ar.status = 'repay' " \
          "AND ar.asset_type='%s' " \
          "AND ar.late_days BETWEEN %s AND %s" % (asset_type, begin_late_days, end_late_days)
    LogUtil.log_info("修改未分案的案件天数为99,sql=%s" % sql)
    dc.DH_DB.update(sql)


# 获取业务组在线催员的人数
def get_collector_count(group_name):
    sql = "SELECT a.asset_group_name, count(*) AS collector_num " \
          "FROM asset_type_group a " \
          "LEFT JOIN user_asset_type b ON b.asset_group_id = a.asset_group " \
          "LEFT JOIN sys_user su ON b.sys_user_id = su.id " \
          "LEFT JOIN sys_user_role d ON d.user_id = su.id " \
          "LEFT JOIN sys_role ee ON d.role_id = ee.id " \
          "LEFT JOIN collect_attendance_dtl dtl on dtl.user_id = su.id and dtl.work_day = curdate() " \
          "WHERE dtl.attendance_status_flag = 1 " \
          "AND a.asset_group_name = '%s' " \
          "AND su.del_flag=0 " \
          "AND ee.enname = 'urger' " \
          "GROUP BY a.asset_group_name" % group_name
    collector_count = dc.DH_DB.query(sql)
    LogUtil.log_info("获取业务组在线催员的人数,sql=%s" % sql)
    print("collector_count=", collector_count)
    return collector_count


# 获取业务组在线催员姓名
def get_collector_name(group_name):
    sql = "SELECT su.name,0 as today_assigned_amount " \
          "FROM asset_type_group a " \
          "LEFT JOIN user_asset_type b ON b.asset_group_id = a.asset_group " \
          "LEFT JOIN sys_user su ON b.sys_user_id = su.id " \
          "LEFT JOIN sys_user_role d ON d.user_id = su.id " \
          "LEFT JOIN sys_role ee ON d.role_id = ee.id " \
          "LEFT JOIN collect_attendance_dtl dtl on dtl.user_id = su.id and dtl.work_day = curdate() " \
          "WHERE dtl.attendance_status_flag = 1 " \
          "AND a.asset_group_name = '%s' " \
          "AND su.del_flag=0 " \
          "AND ee.enname = 'urger' " % group_name
    collector_name = dc.DH_DB.query(sql)
    # LogUtil.log_info("获取业务组在线催员的姓名,sql=%s，collector_name=%s" % (sql, collector_name))
    return collector_name


# 获取业务组在线催员的当月分案总金额，以BI数据为准
def get_bi_bf_current_month_assigned_amount(sys_user_id):
    sql = "select sys_user_name as name,assign_total_amount as bf_current_month_assigned_amount " \
          "from bi.mission_assign_statistics " \
          "where create_at between date_add(curdate(), interval - day(curdate()) + 1 day) and curdate() " \
          "and type = 2 " \
          "and sys_user_id in ('%s')" % sys_user_id
    assigned_amount_info = dc.DH_DB.query(sql)
    return assigned_amount_info


# 获取 分案前 业务组在线催员姓名、当月已分案金额
def get_bf_current_month_collector_name(group_name, case_behavior_id):
    sql = "SELECT " \
          "su.name,ifnull(sum(ml.assign_overdue_total_amount),0) as bf_current_month_assigned_amount," \
          "ifnull(sum(ml.assign_overdue_total_amount),0)/count(distinct debtor_id) as bf_current_month_assigned_avg " \
          "FROM asset_type_group a " \
          "LEFT JOIN user_asset_type b ON b.asset_group_id = a.asset_group " \
          "LEFT JOIN sys_user su ON b.sys_user_id = su.id " \
          "LEFT JOIN sys_user_role d ON d.user_id = su.id " \
          "LEFT JOIN sys_role ee ON d.role_id = ee.id " \
          "LEFT JOIN mission_log ml on ml.assigned_sys_user_id = su.id and ml.mission_group_name = a.asset_group_name " \
          "WHERE b.asset_line_status = 1 " \
          "AND a.asset_group_name = '%s' " \
          "AND su.del_flag=0 " \
          "AND ee.enname = 'urger' " \
          "AND ml.mission_log_operator = 'assign' " \
          "AND ml.mission_log_assigned_date >= date_add(curdate(), interval - day(curdate()) + 1 day) " \
          "AND (ml.case_behavior_id <> %s or ml.case_behavior_id is null) " \
          "group by ml.assigned_sys_user_id " \
          "order by bf_current_month_assigned_avg " % (group_name, case_behavior_id)
    collector_name = dc.DH_DB.query(sql)
    LogUtil.log_info("获取分案前 业务组在线催员的姓名、本月已分案金额,sql=%s，collector_name=%s，case_behavior_id=%s" % (sql, collector_name, case_behavior_id))
    return collector_name


# 获取 本次分案前 业务组当前在线催员的当月已分案金额
def get_bf_current_month_assigned_amount(group_name, case_behavior_id):
    sql = "SELECT " \
          "su.name,ifnull(sum(ml.assign_overdue_total_amount),0) as bf_current_month_assigned_amount " \
          "FROM asset_type_group a " \
          "LEFT JOIN user_asset_type b ON b.asset_group_id = a.asset_group " \
          "LEFT JOIN sys_user su ON b.sys_user_id = su.id " \
          "LEFT JOIN sys_user_role d ON d.user_id = su.id " \
          "LEFT JOIN sys_role ee ON d.role_id = ee.id " \
          "LEFT JOIN mission_log ml on ml.assigned_sys_user_id = su.id and ml.mission_group_name = a.asset_group_name " \
          "WHERE b.asset_line_status = 1 " \
          "AND a.asset_group_name = '%s' " \
          "AND su.del_flag=0 " \
          "AND ee.enname = 'urger' " \
          "AND ml.mission_log_operator = 'assign' " \
          "AND ml.mission_log_assigned_date >= date_add(curdate(), interval - day(curdate()) + 1 day) " \
          "AND (ml.case_behavior_id <> %s or ml.case_behavior_id is null) " \
          "group by ml.assigned_sys_user_id " % (group_name, case_behavior_id)
    collector_name = dc.DH_DB.query(sql)
    LogUtil.log_info("获取分案前 业务组当前在线催员的当月已分案金额,sql=%s，collector_name=%s，case_behavior_id=%s" % (sql, collector_name, case_behavior_id))
    return collector_name


# 获取催员当月1号截止到今天（包含今天）的在线天数
def get_current_month_online_days(collector_name):
    sql = "SELECT count(*) as online_days " \
          "FROM collect_attendance_dtl b " \
          "LEFT JOIN sys_user su ON b.user_id = su.id " \
          "LEFT JOIN sys_user_role d ON d.user_id = su.id " \
          "LEFT JOIN sys_role ee ON d.role_id = ee.id " \
          "WHERE b.attendance_status_flag = 1 " \
          "AND su.del_flag=0 AND ee.enname = 'urger' " \
          "and b.work_day >= date_add(curdate(), interval - day(curdate()) + 1 day) " \
          "and b.work_day <= curdate() " \
          "and su.name = '%s' " % collector_name
    online_days = dc.DH_DB.query(sql)
    return online_days


# 获取未分案债务数量
def get_unassigned_cases(asset_type, begin_late_days, end_late_days, quality_type, d3_level, asset_from_app):
    sql = " select ar.debtor_id " \
          "from debtor_arrears ar " \
          "where 1=1 and not exists( " \
          "select 1 from mission m where m.mission_asset_id = ar.asset_id " \
          "and(m.assigned_sys_user_id is not null or m.assigned_group_id is not null)) " \
          "and ar.inner_outer = 'inner' " \
          "and ar.status = 'repay' " \
          "and ar.asset_type='%s' " \
          "and ar.late_days between %s and %s " \
          "and exists(select 1 from asset a where a.asset_id = ar.asset_id and a.asset_from_app = '%s')" \
          % (asset_type, begin_late_days, end_late_days, asset_from_app)
    if quality_type in ("新用户", "老用户"):
        sql = sql + " and exists(select 1 from debtor_asset da " \
                    "left join asset_quality aq on da.asset_item_number = aq.asset_item_number " \
                    "where da.debtor_arrears_id = ar.id and aq.item_cust_flg = '{0}')".format(quality_type)
    if quality_type == "":
        sql = sql + " and exists(select 1 from debtor_asset da " \
                    "left join asset_quality aq on da.asset_item_number = aq.asset_item_number " \
                    "where da.debtor_arrears_id = ar.id and aq.item_cust_flg is null)"
    if d3_level in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
        sql = sql + " and exists(select 1 from debtor_asset da " \
                    "left join c_card cc on da.asset_item_number = cc.asset_item_number " \
                    "where da.debtor_arrears_id = ar.id " \
                    "and cc.d3_level = {0})".format(d3_level)
    if d3_level == "":
        sql = sql + " and exists(select 1 from debtor_asset da " \
                    "left join c_card cc on da.asset_item_number = cc.asset_item_number " \
                    "where da.debtor_arrears_id = ar.id " \
                    "and cc.d3_level is null)"
    unassigned_case_info = dc.DH_DB.query(sql)
    LogUtil.log_info("获取未分案债务数量,SQL=%s，unassigned_case_info=%s" % (sql, unassigned_case_info))
    return unassigned_case_info


# 获取指定行为ID下的催员分案数量分布
def get_assigned_distribution(case_behavior_id):
    sql = "select assigned_sys_user_name,count(distinct debtor_id) as per_assigned_case_num " \
          "from mission_log ml " \
          "where case_behavior_id = %s " \
          "group by assigned_sys_user_name " \
          "order by per_assigned_case_num desc" % case_behavior_id
    # LogUtil.log_info("获取指定行为ID下的催员分案数量分布,sql=%s" % sql)
    assigned_info = dc.DH_DB.query(sql)
    return assigned_info


# 获取分案行为ID
def get_case_behavior_id(job_name, begin_time):
    sql = "select * from case_behavior " \
          "where job_name ='%s' " \
          "and status=1 " \
          "and create_at >= '%s' " \
          "order by id desc " \
          "limit 1" % (job_name, begin_time)
    # LogUtil.log_info("获取分案行为ID，sql=%s" % sql)
    case_behavior_info = dc.DH_DB.query(sql)
    return case_behavior_info


# 获取分案策略
def get_mission_strategy(job_name):
    sql = "select * from mission_strategy " \
          "where enname = '%s' " \
          "and status =0 " \
          "and version =1" % job_name
    strategy_info = dc.DH_DB.query(sql)
    # LogUtil.log_info("获取到分案策略，strategy_info=%s" % strategy_info)
    return strategy_info


# 获取分案结果
def get_assigned_mission_log(case_behavior_id):
    sql = "select * from mission_log where case_behavior_id= %s " % case_behavior_id
    mission_log_info = dc.DH_DB.query(sql)
    return mission_log_info


# 获取染色结果
def get_dye_info(case_behavior_id):
    sql = "select ar.color,ar.type from mission_log ml " \
          "left join debtor_asset da on ml.debtor_id = da.debtor_id and ml.mission_log_asset_id = da.asset_id " \
          "left join asset_ranse ar on da.asset_id = ar.asset_item_number = da.asset_item_number and ar.debtor_id = da.debtor_id " \
          "where ml.case_behavior_id=%s " \
          "and ar.create_at >= ml.mission_log_create_at " \
          "group by ar.color,ar.type" % case_behavior_id
    dye_info = dc.DH_DB.query(sql)
    # LogUtil.log_info("获取染色结果，SQL=%s" % sql)
    return dye_info


# 获取分案金额统计结果
def get_mission_log_total_amount(case_behavior_id):
    sql = "select assigned_sys_user_name as name,sum(assign_overdue_total_amount) as today_assigned_amount from mission_log " \
          "where case_behavior_id=%s " \
          "group by assigned_sys_user_id " \
          "order by sum(assign_overdue_total_amount)" % case_behavior_id
    mission_log_amount_info = dc.DH_DB.query(sql)
    # LogUtil.log_info("获取分案金额统计结果，mission_log_amount_info=%s" % mission_log_amount_info)
    return mission_log_amount_info


# 获取分案后，当月分案金额
def get_af_current_month_assigned_amount(mission_group_name):
    sql = "select assigned_sys_user_name as name,ifnull(sum(assign_overdue_total_amount),0) as af_current_month_assigned_amount from mission_log " \
          "where mission_log_operator = 'assign' " \
          "and mission_log_assigned_date >= date_add(curdate(), interval - day(curdate()) + 1 day) " \
          "and mission_group_name = '%s' " \
          "group by assigned_sys_user_id " \
          "order by 2" % mission_group_name
    mission_log_amount_info = dc.DH_DB.query(sql)
    # LogUtil.log_info("获取分案金额统计结果，mission_log_amount_info=%s" % mission_log_amount_info)
    return mission_log_amount_info


# 获取指定染色类型的染色结果
def get_extract_dye_info(dye_type, dye_color, begin_time, source_type):
    if source_type == "asset_quality":
        sql = "SELECT if(aq.item_cust_flg is null,'null',aq.item_cust_flg) as quality_type, ar.type, ar.color, count(distinct ar.debtor_id) AS count " \
              "FROM asset_ranse ar " \
              "left join asset_quality aq on ar.asset_item_number = aq.asset_item_number " \
              "WHERE ar.type = '%s' and ar.color= '%s' " \
              "AND ar.create_at >= '%s' " \
              "GROUP BY quality_type, ar.type,ar.color" % (dye_type, dye_color, begin_time)
    if source_type == "c_card":
        sql = "SELECT if(cc.d3_level is null,-1,cc.d3_level) as quality_type, ar.type, ar.color, count(distinct ar.debtor_id) AS count " \
              "FROM asset_ranse ar " \
              "left join c_card cc on ar.asset_item_number = cc.asset_item_number " \
              "WHERE ar.type = '%s' and ar.color= '%s' " \
              "AND ar.create_at >= '%s' " \
              "GROUP BY quality_type, ar.type,ar.color" % (dye_type, dye_color, begin_time)
    if source_type is None or source_type == "":
        sql = "SELECT ar.type, ar.color, count(distinct ar.debtor_id) AS count " \
              "FROM asset_ranse ar " \
              "WHERE ar.type = '%s' and ar.color= '%s' " \
              "AND ar.create_at >= '%s' " \
              "GROUP BY ar.type,ar.color" % (dye_type, dye_color, begin_time)
    extract_dye_info = dc.DH_DB.query(sql)
    # LogUtil.log_info("获取指定染色类型的染色结果，SQL=%s，结果=%s" % (sql, extract_dye_info))
    return extract_dye_info


# 按业务组、用户类型分组 获取分案结果
def get_assigned_by_group_quality(case_behavior_id):
    sql = "select " \
          "pp.mission_group_name as assigned_group_name, " \
          "sum(if(pp.item_cust_flg='新用户',1,0)) as assigned_count_new, " \
          "sum(if(pp.item_cust_flg='老用户',1,0)) as assigned_count_old " \
          "from(select " \
                "ml.mission_group_name,aq.item_cust_flg " \
                "from mission_log ml " \
                "left join debtor_asset da on da.debtor_id = ml.debtor_id " \
                "left join asset a on a.asset_id = da.asset_id " \
                "left join asset_quality aq on da.asset_item_number = aq.asset_item_number " \
                "where ml.case_behavior_id =%s " \
                "group by assigned_sys_user_name,ml.debtor_id) pp " \
          "group by pp.mission_group_name,pp.item_cust_flg " \
          "order by pp.mission_group_name" % case_behavior_id
    mission_info = dc.DH_DB.query(sql)
    LogUtil.log_info("按业务组、用户类型分组 获取分案结果，sql=%s" % sql)
    # print("mission_info=", mission_info)
    return mission_info


# 清空指定业务组的在线催员
def modify_online_collector(group_name, before_status, after_status):
    sql = "update asset_type_group a " \
          "left join user_asset_type b on b.asset_group_id = a.asset_group " \
          "left join sys_user su on b.sys_user_id = su.id " \
          "left join sys_user_role d on d.user_id = su.id " \
          "left join sys_role ee on d.role_id = ee.id " \
          "left join collect_attendance_dtl dtl on dtl.user_id = su.id and dtl.work_day = curdate() " \
          "set dtl.attendance_status_flag = %s, b.asset_line_status= %s " \
          "where dtl.attendance_status_flag = %s " \
          "and a.asset_group_name = '%s' " \
          "and su.del_flag=0 " \
          "and ee.enname = 'urger'" % (after_status, after_status, before_status, group_name)
    dc.DH_DB.update(sql)
    LogUtil.log_info("清空指定业务组的在线催员，业务组=%s，修改前的在线状态=%s，修改后=%s"
                     % (group_name, before_status, after_status))


# 获取在线催员能力系数分布
def get_collector_level_count(group_name):
    sql = "select ucl.level,count(*) as per_level_num,ucl.level*count(*) as level_sum " \
          "from asset_type_group a " \
          "left join user_asset_type b on b.asset_group_id = a.asset_group " \
          "left join user_collect_level ucl on ucl.sys_user_id = b.sys_user_id " \
          "left join sys_user su on b.sys_user_id = su.id " \
          "left join sys_user_role d on d.user_id = su.id " \
          "left join sys_role ee on d.role_id = ee.id " \
          "where 1=1 and asset_line_status = 1 " \
          "and a.asset_group_name in ({}) " \
          "and su.del_flag=0 " \
          "and ee.enname = 'urger' " \
          "group by ucl.level " \
          "order by ucl.level".format(','.join(["'%s'" % item for item in group_name]))
    collector_level_count_info = dc.DH_DB.query(sql)
    LogUtil.log_info("获取在线催员能力系数分布，collector_level_count_info=%s" % collector_level_count_info)
    return collector_level_count_info


# 获取分案结果，按催员的能力系数分组
def get_assigned_by_level(case_behavior_id):
    sql = "select b.level,count(distinct debtor_id) as assigned_num " \
          "from mission_log ml " \
          "left join user_collect_level b on ml.assigned_sys_user_id = b.sys_user_id " \
          "where case_behavior_id=%s " \
          "group by b.level " \
          "order by b.level" % case_behavior_id
    LogUtil.log_info("获取分案结果，按催员的能力系数分组，sql=%s" % sql)
    assigned_by_level_info = dc.DH_DB.query(sql)
    return assigned_by_level_info


# 获取在线催员的名单
def get_collector_id_list(group_name):
    sql = "SELECT su.id FROM asset_type_group a " \
          "LEFT JOIN user_asset_type b ON b.asset_group_id = a.asset_group " \
          "LEFT JOIN sys_user su ON b.sys_user_id = su.id " \
          "LEFT JOIN sys_user_role d ON d.user_id = su.id " \
          "LEFT JOIN sys_role ee ON d.role_id = ee.id " \
          "WHERE asset_line_status = 1 " \
          "AND a.asset_group_name IN ({}) " \
          "AND su.del_flag=0 " \
          "AND ee.enname = 'urger'".format(','.join(["'%s'" % item for item in group_name]))
    user_list = dc.DH_DB.query(sql)
    # print("获取在线催员的名单，user_list=", user_list)
    return user_list


# 获取催员在手案件数量
def get_current_in_hand_case_num(sys_user_id):
    sql = "SELECT m.assigned_sys_user_id sysUserId, m.assigned_sys_user_name sysUserName, count(da.debtor_id) as assignDebtorNum " \
          "FROM debtor_arrears da " \
          "LEFT JOIN mission m ON da.asset_id = m.mission_asset_id " \
          "where da.status = 'repay' " \
          "AND da.inner_outer = 'inner' " \
          "AND da.asset_id != 0 " \
          "AND m.assigned_sys_user_id is not null " \
          "AND assigned_sys_user_id = '%s' " \
          "group BY m.assigned_sys_user_id " \
          "order by assignDebtorNum desc" % sys_user_id
    LogUtil.log_info("获取催员在手案件数量，sql=%s" % sql)
    in_hand_num = dc.DH_DB.query(sql)
    return in_hand_num
