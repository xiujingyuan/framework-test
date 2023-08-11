# -*- coding: utf-8 -*-
import string

from biztest.function.dcs.biz_database import get_deposit_tasks, \
    update_deposit_orderAndtrade_status, update_payment_withdrawAndreceipt_status, \
    update_deposit_status_to_success_by_order_no
from biztest.function.dcs.capital_database import get_task_dcs, update_task_at_dcs_by_order_no
from biztest.function.rbiz.database_operation import *
from biztest.util.asserts.assert_util import Assert
from biztest.util.http.http_util import Http
import common.global_const as global_const


def get_timestamp():
    """
    获取20位的随机数
    :return:
    """
    return '2020' + str(datetime.now().timestamp()).replace('.', '')


"""
biz dcs系统的主要接口
"""

dcs_base_url = global_const.BASE_URL[global_const.COUNTRY]['biz-dcs'].format(global_const.ENV)
header = {"Content-Type": "application/json"}


def run_task_in_biz_dcs(task_type, order_no, excepts=None):
    task_ids = get_task_dcs(task_type, order_no)
    run_task_in_biz_dcs_by_task_id(task_ids, excepts)


def run_task_in_biz_dcs_by_task_id(task_ids, excepts=None):
    url = dcs_base_url + "/task/run"
    id_lists = []
    if isinstance(task_ids, int):
        id_lists = [task_ids]
    else:
        for ii in range(0, len(task_ids)):
            id_lists.append(task_ids[ii]["task_id"])
    ret = Http.http_post(url, id_lists, header)
    if excepts is not None:
        Assert.assert_match_json(excepts, ret, "task运行结果校验不通过，task_id:{0}".format(task_ids))


def run_dcs_task_by_order_no(order_no, wait_time=1, excepts=None):
    time.sleep(wait_time)
    update_task_at_dcs_by_order_no(order_no)
    url = dcs_base_url + "/job/runTaskLikeOrderNo?orderNo=" + str(order_no)
    ret = Http.http_post(url, {}, header)
    if excepts is not None:
        Assert.assert_match_json(excepts, ret[0], "task运行结果校验不通过，order_no:%s" % order_no)


def run_dcs_task_by_count(order_no, count=2):
    for c in range(count):
        run_dcs_task_by_order_no(order_no)


def scenes_receive(item_no, source_type="lieyin"):  # 目前只有leiyin模式会领取权益
    req = {
        "from_system": "banana",
        "key": get_guid(),
        "type": "ScenesReceive",
        "data": {
            "asset_item_no": item_no,
            "receive_time": get_date(),
            "source_type": source_type,
            "is_auto_receive": "N"
        }
    }
    url = dcs_base_url + "/dsq/scenes-receive"
    return Http.http_post(url, req, header)


def deposit_run_task_by_order_no():
    deposit_tasks = get_deposit_tasks()
    for task in deposit_tasks:
        order_no = task["task_order_no"]
        url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-deposit/task/run?orderNo=" + order_no
        ret = Http.http_get(url, header)
        print(ret, url)
        update_deposit_status_to_success_by_order_no(order_no)  # 这一步如果deposit没有执行task会报错


def update_deposit_orderandtrade_and_run_task(status=2):
    deposit_tasks = get_deposit_tasks()
    for task in deposit_tasks:
        order_no = task["task_order_no"]
        url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-deposit/task/run?orderNo=" + order_no
        ret = Http.http_get(url, header)
        print(ret, url)
    update_deposit_orderAndtrade_status(status)  # 这一步如果deposit没有执行task会报错


def update_deposit_order_trade_tofail():
    deposit_tasks = get_deposit_tasks()
    for task in deposit_tasks:
        order_no = task["task_order_no"]
        url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-deposit/task/run?orderNo=" + order_no
        ret = Http.http_get(url, header)
        print(ret, url)
        update_payment_withdrawAndreceipt_status(order_no)  # 这一步如果deposit没有执行task会报错


def generate_random_str(randomlength=16):
    """
  生成一个指定长度的随机字符串，其中
  string.digits=0123456789
  string.ascii_letters=abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
  """
    str_list = [random.choice(string.digits + string.ascii_letters) for i in range(randomlength)]
    random_str = ''.join(str_list)
    return random_str


def manual_collect(channel="qsq_sumpay_tq_protocol", deposit="jining", channelCode="account_201812282234242608_jining",
                   amount="1111"):
    request_body = {
        "from_system": "biz",
        "type": "Concentration",
        "key": generate_random_str(10),
        "data": {
            "auditId": random.randint(1, 10),
            "orderNo": "ZJGJ_" + generate_random_str(10),
            "paymentChannel": channel,
            "deposit": deposit,
            "channelCode": channelCode,
            "amount": amount,  # 固定的值1111不能改，有断言检查
            "memo": "手动发起的资金归集"
        }
    }
    url = dcs_base_url + "/collect/manual"
    # return Http.http_post(url, req, header)
    return request_body, Http.http_post(url, request_body)


def manual_settlement(loan_type="BIG", batch_no="MZ_JMX511187211000155541",
                      transfer_in="v_hefei_weidu_reserve", transfer_out="v_mozhi_jinmeixin_gj"):
    request_body = {
        "from_system": "capital",
        "type": "ManualSettlement",
        "key": generate_random_str(10),
        "data": {
            "loan_type": loan_type,
            "batch_no": batch_no,
            "comment": "手动结算备注",
            "transfer_in": transfer_in,
            "transfer_out": transfer_out,
            "audit_id": 66002
        }
    }
    url = dcs_base_url + "/settlement/manual"
    # return Http.http_post(url, req, header)
    return request_body, Http.http_post(url, request_body)


def manual_recharge(paymentChannel="qsq_sumpay_qjj_protocol", deposit="qs_qianjingjing",
                    depositChannelCode="v_hefei_weidu_reserve", amount="1100000000"):
    request_body = {
        "from_system": "biz",
        "type": "DepositWithdraw",
        "key": generate_random_str(10),
        "data": {
            "auditId": generate_random_str(10),
            "orderNo": generate_random_str(10),
            "paymentChannel": paymentChannel,
            "deposit": deposit,
            "depositChannelCode": depositChannelCode,
            "amount": amount
        }
    }
    url = dcs_base_url + "/depositWithdraw/manual"
    return request_body, Http.http_post(url, request_body)
