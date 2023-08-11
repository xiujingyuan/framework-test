from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import get_sysconfig
import common.global_const as gc

# env = get_sysconfig("--env")
# db = DataBase("biz%s" % env)
# "biz%s" % gc.ENV = "biz%s" % env
# "gbiz%s" % gc.ENV = "gbiz%s" % env
# "rbiz%s" % gc.ENV = "rbiz%s" % env


# 检查task的执行情况
def get_task_close_biz(task_type, item_no):
    sql = 'select * from {0}.task where task_type = "{1}" and task_status != "close" and task_request_data like "%{2}%" order by task_id desc '\
        .format("biz%s" % gc.ENV, task_type, item_no)
    task_close = gc.BIZ_DB.query(sql)
    if task_close:
        return task_close
    else:
        return None
# 更新task的再次执行时间
def update_task_at_biz(task_type, item_no):
    sql = 'update {0}.task set task_status = "open",task_next_run_date = now() where task_status != "close" and task_type = "{1}" and task_request_data like "%{2}%" '\
        .format("biz%s" % gc.ENV, task_type, item_no)
    gc.BIZ_DB.update(sql)
# 关闭多余的task
def update_task_close_biz(item_no):
    sql = 'update {0}.task set task_status = "close" where task_status not in ("close","terminated") and task_request_data not like "%{1}%" '\
        .format("biz%s" % gc.ENV, item_no)
    gc.BIZ_DB.update(sql)



# gbiz放款的时候用，查sendmsg_content组装进件和放款基础参数
def get_sendmsg_content(test_db, item_no, type):
    sql = "select sendmsg_content from {0}.sendmsg where sendmsg_order_no='{1}' and sendmsg_type='{2}'"\
        .format(test_db, item_no, type)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list[0]["sendmsg_content"]
    else:
        return None

# gbiz放款的时候用，修改大单的放款时间和状态
def update_asset_status_gbiz(grant_at, item_no):
    sql = "update {0}.asset set asset_status='repay',asset_actual_grant_at='{1}',asset_effect_at='{1}' where asset_item_no='{2}'"\
        .format("gbiz%s" % gc.ENV, grant_at, item_no)
    gc.BIZ_DB.update(sql)

# rbiz会用，查看sendmsg的执行情况
def get_sendmsg(item_no, type):
    sql = "select * from {0}.sendmsg where sendmsg_order_no = '{1}' and sendmsg_type = '{2}' order by sendmsg_id desc limit 3 "\
        .format("rbiz%s" % gc.ENV, item_no, type)
    result_list = gc.BIZ_DB.query(sql)
    if result_list:
        return result_list
    else:
        return None

