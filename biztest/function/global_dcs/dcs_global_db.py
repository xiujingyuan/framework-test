import json

import common.global_const as gc
from biztest.config.rbiz.url_config import global_refund_online_path
from biztest.interface.dcs.biz_dcs_interface import dcs_base_url, time, get_guid, parse_resp_body, requests, LogUtil
from biztest.util.asserts.assert_util import Assert
from biztest.util.http.http_util import Http


def get_asset_withdraw_info_by_item_no(item_no):
    sql = "SELECT  *  FROM  asset_withdraw WHERE order_no='%s'" % item_no
    asset_withdraw = gc.GLOBAL_DCS_DB.query(sql)
    return asset_withdraw


def get_dcs_asset_info_by_item_no(item_no):
    sql = "SELECT  *  FROM  asset WHERE item_no='%s'" % item_no
    asset_info = gc.GLOBAL_DCS_DB.query(sql)
    return asset_info


def get_capital_asset_info(item_no):
    sql = "SELECT  *  FROM  capital_asset WHERE asset_item_no='%s'" % item_no
    asset_info = gc.GLOBAL_DCS_DB.query(sql)
    return asset_info


def get_account_log_info(item_no):
    sql = "SELECT  *  FROM  account_log WHERE comment='%s' and  business_table='asset'" % item_no
    asset_info = gc.GLOBAL_DCS_DB.query(sql)
    return asset_info


def get_account_balance_available(identity):
    sql = "SELECT  *  FROM  account WHERE identity='%s'" % identity
    asset_info = gc.GLOBAL_DCS_DB.query(sql)
    return asset_info


def get_dcs_refund_result_info_by_merchant_key(merchant_key):
    sql = "SELECT  *  FROM  refund_result WHERE withhold_serial_no='%s'" % merchant_key
    refund_result_info = gc.GLOBAL_DCS_DB.query(sql)
    return refund_result_info


def get_capital_tran_info(item_no):
    sql = "SELECT  *  FROM  capital_tran WHERE item_no='%s' order by type desc " % item_no
    asset_info = gc.GLOBAL_DCS_DB.query(sql)
    return asset_info


def get_dcs_asset_tran_by_item_no(item_no):
    sql = "SELECT  *  FROM  asset_tran WHERE asset_item_no='%s'" % item_no
    asset_tran = gc.GLOBAL_DCS_DB.query(sql)
    return asset_tran


def get_dcs_asset_tran_by_item_no(item_no):
    sql = "SELECT  *  FROM  asset_tran WHERE asset_item_no='%s' order by type desc" % item_no
    asset_info = gc.GLOBAL_DCS_DB.query(sql)
    return asset_info


def update_dcs_global_task_open(item_no):
    sql = "update task set task_status = 'open',task_next_run_at =date_sub(now(), INTERVAL 80 MINUTE) where task_status != 'close' and task_order_no = '%s'" % item_no
    task = gc.GLOBAL_DCS_DB.update(sql)
    return task


def get_dcs_asset_tran_due_at(item_no):
    sql = "SELECT  *  FROM  asset_tran WHERE asset_item_no='%s' AND  TYPE='repayprincipal'" % item_no
    asset_tran = gc.GLOBAL_DCS_DB.update(sql)
    return asset_tran


def update_dcs_global_task_next_run_at(task_priority=1, status='open'):
    if status == 'open':
        sql = "update task set task_priority='%s',task_status = 'open',task_next_run_at =date_sub(now(), INTERVAL 80 MINUTE) where task_status='open'" % task_priority
        task = gc.GLOBAL_DCS_DB.update(sql)
    else:
        sql = "update task set task_priority='%s',task_status = 'close',task_next_run_at =date_sub(now(), INTERVAL 80 MINUTE) where task_status='open'" % task_priority
        task = gc.GLOBAL_DCS_DB.update(sql)
    return task


def update_clearing_tran_create_at(item_no):
    sql = "update clearing_tran set create_at = date_sub(now(), INTERVAL 1 DAY ) where asset_item_no = '%s'" % item_no
    clearing_tran = gc.GLOBAL_DCS_DB.update(sql)
    return clearing_tran


def get_task_capital_asset_sync(item_no):
    sql = "SELECT * FROM  task WHERE task_status = 'open' and task_request_data LIKE '%%%s%%'" % item_no
    task_info = gc.GLOBAL_DCS_DB.update(sql)
    return task_info


def get_dcs_account_repay_info_by_item_no(item_no):
    sql = "SELECT  *  FROM  account_repay WHERE order_no='%s' ORDER BY id DESC" % item_no
    final_master_info = gc.GLOBAL_DCS_DB.query(sql)
    return final_master_info


def get_dcs_final_master_info_by_item_no(item_no, biz_type="repay"):
    if biz_type == "repay":
        sql = "SELECT  *  FROM  final_master WHERE asset_item_no='%s' and  biz_type='repay'  ORDER BY id DESC " % item_no
    else:
        sql = "SELECT  *  FROM  final_master WHERE asset_item_no='%s' and  biz_type='compensate'  ORDER BY id DESC " % item_no
    final_master_info = gc.GLOBAL_DCS_DB.query(sql)
    return final_master_info


def get_dcs_final_tran_info_by_item_no(item_no, biz_type="repay"):
    if biz_type == "repay":
        sql = "SELECT  *  FROM  final_tran WHERE asset_item_no='%s'  and withhold_serial_no<>'' ORDER BY id DESC" % item_no
    else:
        sql = "SELECT  *  FROM  final_tran WHERE asset_item_no='%s'  and withhold_serial_no='' ORDER BY id DESC" % item_no
    final_tran_info = gc.GLOBAL_DCS_DB.query(sql)
    return final_tran_info


def get_dcs_clearing_tran_info_by_item_no(item_no, biz_type="repay"):
    if biz_type == "repay":
        sql = "SELECT  *  FROM  clearing_tran WHERE asset_item_no='%s' and trans_type<>'compensate' ORDER BY id DESC" % item_no
    else:
        sql = "SELECT  *  FROM  clearing_tran WHERE asset_item_no='%s' and trans_type='compensate' ORDER BY id DESC" % item_no
    clearing_tran_info = gc.GLOBAL_DCS_DB.query(sql)
    return clearing_tran_info


def get_dcs_settlement_info_by_batch_no(batch_no):
    sql = "SELECT  *  FROM  settlement WHERE batch_no='%s' ORDER BY id DESC" % batch_no
    settlement_info = gc.GLOBAL_DCS_DB.query(sql)
    return settlement_info


def get_dcs_account_transfer_info_by_settlement_id(settlement_id):
    sql = "SELECT  *  FROM  account_transfer WHERE business_id='%s' ORDER BY id DESC" % settlement_id
    account_transfer_info = gc.GLOBAL_DCS_DB.query(sql)
    return account_transfer_info


def dcs_run_task_by_order_no(order_no, except_json=None):
    wait_task_appear(order_no)
    update_dcs_global_task_open(order_no)
    url = dcs_base_url + "/job/runTaskByOrderNo?orderNo=" + str(order_no)
    resp = Http.http_post(url, {})
    if except_json is not None:
        Assert.assert_match_json(except_json, resp, "task运行不正确，task结果：%s" % str(resp))


def dcs_run_job_by_jobtype(job_type, job_params):
    url = dcs_base_url  + "/job/run"
    # url = "https://biz-gateway-proxy.starklotus.com/tha_dcs1" + "/job/run"
    params = {"jobType": job_type,
              "param": json.dumps(job_params)}
    Http.http_get(url, params=params)


def dcs_run_task_by_task_id(task_id, except_json=None):
    url = dcs_base_url + "/task/run"
    request_body = {task_id}
    resp = Http.http_post(url, request_body)
    if except_json is not None:
        Assert.assert_match_json(except_json, resp, "task运行不正确，task结果：%s" % str(resp))


def wait_task_appear(order_no, timeout=60):
    result = False
    time_start = time.time()
    while (time.time() - time_start) < timeout:
        task_list = gc.GLOBAL_DCS_DB.query(
            "select task_id, task_status from task where task_order_no='%s' order by task_id desc" % order_no)
        for task in task_list:
            if task["task_status"] == 'open':
                result = True
                break
        if result:
            break
        else:
            time.sleep(0.2)
    if not result:
        raise Exception("no task found, task_order_no:%s" % order_no)


def withhold_refund_online(item_no, withhold_serial_no, refund_amount):
    url = gc.REPAY_URL + global_refund_online_path
    req_key = get_guid()
    req_body = {
        "from_system": "biz",
        "key": req_key,
        "type": "OnlineRepeatRefund",
        "data": {
            "item_no": item_no,
            "refund_withhold_serial_no": withhold_serial_no,
            "refund_amount": refund_amount,
            "operator": "auto_test"
        }
    }
    resp = parse_resp_body(
        requests.request(method='post', url=url, headers={"content-type": "application/json"},
                         json=req_body))
    LogUtil.log_info(
        f"线上代扣退款发起成功")
    return resp
