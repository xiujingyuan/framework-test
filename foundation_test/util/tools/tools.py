# -*- coding: utf-8 -*-
import collections
import hashlib
import json
import random
import re
import time
import uuid
from datetime import datetime
from decimal import Decimal

import pandas as pd
import pytest
import requests
from allure_commons.utils import md5
from dateutil.relativedelta import relativedelta
from pymysql import NULL

import foundation_test.config.dh.db_const as dc
from foundation_test.config.dh.url_config import *
from foundation_test.util.http.http_util import Http
from foundation_test.util.log.log_util import LogUtil


def get_date(year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S", timezone=None):
    return (datetime.now(timezone) + relativedelta(years=year, months=month, days=day)).strftime(fmt)


def get_date_timestamp(year=0, month=0, day=0):
    return int((datetime.now() + relativedelta(years=year, months=month, days=day)).timestamp())


def get_before_date(overdue_days, n, fmt="%Y-%m-%d"):
    days_ago = (datetime.now() - relativedelta(days=(overdue_days + 31 * n))).strftime(fmt) + " 00:00:00"
    return days_ago


def get_item_no():
    return '2020' + str(datetime.now().timestamp()).replace('.', '')


def get_random_str(num=10):
    data = '1234567890abcdefghijklmnopqrstuvwxyz'
    result = ''
    for i in range(num):
        result = result + random.choice(list(data))
    return result


def get_random_num():
    return str(random.randint(100000000, 10000000000000))


def get_guid():
    return str(uuid.uuid1())


def get_guid4():
    return str(uuid.uuid4())


def get_four_element(bank_name=None, bank_code_suffix=None):
    url = "http://framework-test.k8s-ingress-nginx.kuainiujinke.com/fourelement"
    data = {"bank": bank_name, "bank_code_suffix": bank_code_suffix}
    header = {"Content-Type": "application/json"}
    resp = Http.http_post(url, data, header)
    return resp


def get_four_element_global():
    url = "http://framework-test.k8s-ingress-nginx.kuainiujinke.com/fourelement"
    header = {"Content-Type": "application/json"}
    resp = Http.http_get(url, header)
    response = {
        "code": 0,
        "message": "success",
        "data": {
            "bank_account": resp["data"]["bank_code"],
            "card_num": resp["data"]["bank_code"],
            "mobile": resp["data"]["phone_number"],
            "user_name": "Craltonliu",
            "id_number": resp["data"]["id_number"],
            "address": "Floor 8 TaiPingYang Building TianFuSanGai Chengdu,Sichuan,China",
            "email": resp["data"]["phone_number"] + "@qq.com"
        }
    }
    body = [{"type": 1,
             "plain": response["data"]["mobile"]},
            {"type": 2,
             "plain": response["data"]["id_number"]},
            {"type": 3,
             "plain": response["data"]["card_num"]},
            {"type": 4,
             "plain": response["data"]["user_name"]},
            {"type": 5,
             "plain": response["data"]["email"]},
            {"type": 6,
             "plain": response["data"]["address"]}]
    resp = requests.post(url=overseas_encrypt_url, json=body).json()

    response["data"]["mobile_encrypt"] = resp["data"][0]["hash"]
    response["data"]["id_number_encrypt"] = resp["data"][1]["hash"]
    response["data"]["card_num_encrypt"] = resp["data"][2]["hash"]
    response["data"]["user_name_encrypt"] = resp["data"][3]["hash"]
    response["data"]["email_encrypt"] = resp["data"][4]["hash"]
    response["data"]["address_encrypt"] = resp["data"][5]["hash"]
    response["data"]["bank_account_encrypt"] = resp["data"][2]["hash"]
    return response


def encry_four_element(card_number, id_num, mobile, name):
    encry_body = {
        "card_number": card_number,
        "idnum": id_num,
        "mobile": mobile,
        "name": name
    }
    url = "http://testing-api.kuainiu.io/encry-data"
    header = {"Content-Type": "application/json"}
    resp = Http.http_post(url, encry_body, header)

    response = {
        "code": 0,
        "message": "success",
        "data": {
            "bank_code": card_number,
            "phone_number": mobile,
            "user_name": name,
            "id_number": id_num,
            "bank_code_encrypt": resp['data']['card_number'],
            "id_number_encrypt": resp['data']['idnum'],
            "phone_number_encrypt": resp['data']['mobile'],
            "user_name_encrypt": resp['data']['name']
        }
    }
    return response


def decry_four_element():
    url = "http://framework-test.k8s-ingress-nginx.kuainiujinke.com/fourelement"
    header = {"Content-Type": "application/json"}
    resp = Http.http_get(url, header)
    return resp


# 国内，获取随机三要素：姓名、手机号、身份证号，返回包含明文、密文、码文
def get_three_element():
    url = jc_mock_url + "/api/dh/getThreeElement"
    # header = {"Content-Type": "application/json"}
    resp = Http.http_get(url)
    return resp


# 海外，获取随机三要素：姓名、手机号、身份证号，返回包含明文、密文、码文
def get_overseas_three_element():
    url = jc_mock_url + "/api/dh/overseas/getThreeElement"
    header = {"Content-Type": "application/json"}
    resp = Http.http_get(url, header)
    return resp


def get_sysconfig(option):
    return str(pytest.config.getoption(option)) if hasattr(pytest, 'config') else 1


def update_kv_config(db, key, value):
    sql = "update keyvalue set keyvalue_value='%s' where keyvalue_key='%s'" % (
        json.dumps(value).encode('utf-8').decode('unicode_escape'), key)
    return db.update(sql)


def get_json_path(source):
    """
    get_path获取到json path的list，然后组装为正在的jsonpath返回
    :param source:
    :return:
    """

    def get_path(source_json):
        paths = []
        if isinstance(source_json, collections.abc.MutableMapping):  # 如果是字典类型
            for k, v in source_json.items():  #
                paths.append([k])  # 先将key添加
                paths += [[k] + x for x in get_path(v)]  # 循环判断value类型
        elif isinstance(source_json, collections.abc.Sequence) and not isinstance(source_json, str):  # 如果是列表或字符串
            for i, v in enumerate(source_json):  # i为顺序，v为值
                paths.append([i])  # 先将key添加
                paths += [[i] + x for x in get_path(v)]  # 循环判断value类型
        return paths

    path_seq = get_path(source)
    path_list = []
    for path in path_seq:
        path_temp = "$"
        for value in path:
            if isinstance(value, str):
                path_temp = path_temp + '.' + str(value)
            elif isinstance(value, int):
                path_temp = path_temp + '[' + str(value) + ']'
            else:
                pass
        path_list.append(path_temp)
    return path_list


def parse_resp_body(resp):
    try:
        content = json.loads(resp.text)
    except Exception as e:
        content = resp.text
    resp = {
        "status_code": resp.status_code,
        "content": content,
        "headers": resp.headers,
        "cookies": requests.utils.dict_from_cookiejar(resp.cookies),
        "reason": resp.reason
    }
    return resp


def get_date_before_today(year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S"):
    return (datetime.now() - relativedelta(years=year, months=month, days=day)).strftime(fmt)


# 按照指定时间倒减时间
def get_date_before(time_old, year=0, month=0, day=0, fmt="%Y-%m-%d"):
    return (datetime.strptime(time_old, "%Y-%m-%d") - relativedelta(years=year, months=month, days=day)).strftime(fmt)


# 按照指定时间添加时间
def get_date_after(time_old, year=0, month=0, day=0, fmt="%Y-%m-%d"):
    return (datetime.strptime(time_old, "%Y-%m-%d") + relativedelta(years=year, months=month, days=day)).strftime(fmt)


def get_date_after_today(year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S"):
    return (datetime.now() + relativedelta(years=year, months=month, days=day)).strftime(fmt)


def get_calc_date_base_today(year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S"):
    """

    :param year: 正数 往前推1年，负数往后推1年
    :param month: 正数 往前推1月，负数往后推1月
    :param day: 正数 往前推1天，负数往后推1天
    :param fmt: 时间格式化
    :return:
    """

    ret = datetime.now()
    if year >= 0:
        ret += relativedelta(years=year)
    else:
        ret -= relativedelta(years=-year)
    if month >= 0:
        ret += relativedelta(months=month)
    else:
        ret -= relativedelta(months=-month)
    if day >= 0:
        ret += relativedelta(days=day)
    else:
        ret -= relativedelta(days=-day)
    return ret.strftime(fmt)


def update_kv_config_new(db, key):
    sql = f'select keyvalue_value from keyvalue where keyvalue_key="{key}"'
    result = db.query_mysql(sql)[0][0]
    result_json = json.loads(result)
    result_json_new = json.loads(result)
    if key == 'rbiz_paysvr_config':
        result_json[
            "payment_url"] = 'https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5de5d515d1784d36471d6041/rbiz_auto_test'
    if key == "rbiz_yunxin_quanhu_config":
        result_json["api_config"][
            "gate_url"] = 'https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5de5d515d1784d36471d6041/rbiz_auto_test/yunxinquanhu/'
    sql_update = "update keyvalue set keyvalue_value='{}' where keyvalue_key='{}'".format(
        json.dumps(result_json).encode('utf-8').decode('unicode_escape'), key)
    db.execute_mysql(sql_update)
    return result_json_new


def reduction_kv_config(db, key, value):
    sql_update = "update keyvalue set keyvalue_value='{}' where keyvalue_key='{}'".format(
        json.dumps(value).encode('utf-8').decode('unicode_escape'), key)
    db.execute_mysql(sql_update)


def string_truncation(string):
    string_new = re.findall(r"\[(.+?)\]", string)
    return string_new


def string_split(string, rule):
    string = str(string).replace(' ', '')
    string = string.split(rule)
    return string


def get_timestamp_by_now():
    times = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    time_array = time.strptime(times, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array)) * 1000
    return time_stamp


# 获取指定时间的时间戳
def get_timestamp_by_datetime(date_old):
    time_array = time.strptime(date_old, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array)) * 1000
    return time_stamp


def quantize(decimal_number, round_type='ROUND_HALF_EVEN', precision='1.'):
    """
    调整精度
    :param decimal_number:
    :param round_type: ROUND_CEILING, ROUND_FLOOR, ROUND_UP, ROUND_DOWN,
                       ROUND_HALF_UP, ROUND_HALF_DOWN, ROUND_HALF_EVEN,
                       ROUND_05UP
    :param precision:
    :return:
    """
    return Decimal(decimal_number).quantize(Decimal(precision), rounding=round_type.upper())


def get_test_token():
    origin_data = "d31d69d0cce30621604986454672fd30" + get_date(fmt="%Y-%m-%d")
    test_token = md5(origin_data) + "101"
    print("test_token", test_token)
    return test_token


def highlight_fail(s):
    return ['background-color: yellow' if v == 'fail' else '' for v in s]


def load_case_data(file):
    df = pd.read_excel(file, keep_default_na=False).to_dict(orient='records')
    return df


def result_to_excel(file, data):
    pd.DataFrame(data).style. \
        apply(highlight_fail, subset=['status']). \
        to_excel(file, index=False, engine='openpyxl')


# 登录fox
def dh_login(country_tag):
    from foundation_test.function.dh.asset_sync.dh_db_function import stop_session
    stop_session("yxj")
    fails = 0
    for i in range(60):
        from foundation_test.function.dh.asset_sync.dh_db_function import get_session_id
        if country_tag == 1:
            fox_url = cn_fox_url
            # 国内，检查是否有可用的session_id
            sys_session_log_info = get_session_id("yxj")
        elif country_tag == 2:
            fox_url = overseas_fox_url
            # 海外，检查是否有可用的session_id
            sys_session_log_info = get_session_id("yxj")
        if sys_session_log_info:
            break
            LogUtil.log_info("#### 登录成功")
        if not sys_session_log_info:
            time.sleep(1)
            fails += 1
            LogUtil.log_info("登录中，等待时间：%s" % fails)
            try_login(fox_url)
    if fails == 60:
        return
        LogUtil.log_info("#### 请检查测试环境是否正常运行。")
    session_id = sys_session_log_info[0]["uuid"]
    return session_id


def try_login(fox_url):
    # 尝试登录前先解除登录限制，避免被影响
    remove_login_failure_cache(fox_url)
    url = fox_url + '/a/login'
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    request_data = {
        "username": "18516031484",
        "password": "IUiFaw6EvbCP0dK287Zm7!?^XB3rynHuR15:6V2{L4O8;lMk[x0%59ceJW9_p|3f",
        "validateCode": "481931",
        "deviceId": "c8d806bb-672b-5b64-8d8f-f72bb17a4037",
        "longinFailures": ""
    }
    resp = requests.post(url, request_data, header)
    LogUtil.log_info(resp)


# 解除登录限制
def remove_login_failure_cache(fox_url):
    url = fox_url + "/api/sys/login/restriction/remove/failure/restriction"
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    request_data = {
        "loginName": "18516031484"
    }
    resp = requests.post(url, request_data, header)
    LogUtil.log_info(resp)


# 国内，内催分案给催员秋分
def assign_asset(debtor_id):
    url = cn_fox_url + "/api/test/assignAsset?userId=1e56501bd6734c528fa2bfcdf9cd543b&debtorIds=%s&assignReason=分新案" % debtor_id
    request_data = {}
    LogUtil.log_info("分案，debtor_id=%s" % debtor_id)
    resp = Http.http_post(url, request_data, None)
    fails = 0
    for i in range(60):
        from foundation_test.function.dh.asset_sync.dh_db_function import get_mission_log_by_debtor_id
        mission_log_info = get_mission_log_by_debtor_id(debtor_id)
        from foundation_test.function.dh.asset_sync.dh_db_function import get_collect_recovery_by_asset_id
        collect_recovery = get_collect_recovery_by_asset_id(mission_log_info[0]["mission_log_asset_id"])
        if mission_log_info[0]["mission_log_operator"] == "assign" and collect_recovery:
            print('分案成功!')
            time.sleep(3)
            break
        else:
            time.sleep(1)
            fails += 1
            print('分案尚未成功，等待中，等待时间：', fails)
    return resp


# 根据逾期天数计算逾期等级
def calculate_late_level(overdue_days):
    late_status = ""
    if overdue_days in range(1, 31):
        late_status = "m1"
    if overdue_days in range(31, 61):
        late_status = "m2"
    if overdue_days in range(61, 91):
        late_status = "m3"
    if overdue_days in range(91, 181):
        late_status = "m4"
    if overdue_days in range(181, 361):
        late_status = "m5"
    if overdue_days in range(361, 721):
        late_status = "m6"
    if overdue_days > 720:
        late_status = "m7"
    return late_status


# 更改str类型日期的显示格式
def change_into_other_date(date):
    # 转为数组
    time_array = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    # 转为其它显示格式
    other_style_time = time.strftime("%Y-%m-%d", time_array)
    return other_style_time


# 国内，内催撤案，按债务人ID撤
def unsigned_asset(debtor_id):
    url = cn_fox_url + "/api/test/cancelAssignMission?debtorIds=%s&unAssignReason=其他" % debtor_id
    request_data = {}
    resp = Http.http_post(url, request_data, None)
    fails = 0
    for i in range(60):
        from foundation_test.function.dh.asset_sync.dh_db_function import get_mission_log_by_debtor_id
        mission_log_info = get_mission_log_by_debtor_id(debtor_id)
        if mission_log_info[i]["mission_log_operator"] == "unassign":
            print('撤案成功!')
            break
        else:
            time.sleep(1)
            fails += 1
            print('撤案尚未成功，等待中，等待时间：', fails)
    return resp


# md5加密
def md5(value):
    m = hashlib.md5()
    m.update(value.encode("utf-8"))
    hash_value = m.hexdigest()
    return hash_value


# 调用fox quartz任务并返回分案行为
def run_quartz(country_tag, job_name):
    if country_tag == 1:
        req_url = cn_fox_url
    if country_tag == 2:
        req_url = overseas_fox_url
    url = req_url + "/api/schedule/startnow?jobGroup=MISSION_STRATEGY&jobName=%s" % job_name
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    request_data = {}
    LogUtil.log_info("#### 开始调用fox quartz任务")
    begin_time = get_date()
    LogUtil.log_info("#### 调用quartz任务的时间=%s" % begin_time)
    Http.http_post(url, request_data, header)

    fails = 0
    for i in range(60):
        # 获取分案结果，quartz任务异步执行，加重试
        from foundation_test.function.dh.assign_case.assign_db_function import get_case_behavior_id
        case_behavior_info = get_case_behavior_id(job_name, begin_time)
        if not case_behavior_info:
            time.sleep(1)
            fails += 1
            LogUtil.log_info("分案尚未完成，等待中，等待时间：%s" % fails)
        if case_behavior_info:
            LogUtil.log_info("分案成功，获取到分案结果：%s" % case_behavior_info)
            break
    if fails == 60:
        print("#### 请检查测试环境fox是否正常运行。")
        return

    return case_behavior_info


# 分案排班，撤案操作
def withdraw_mission(country_tag, sys_user_id, operate_type):
    """
    curl -L -X POST 'http://fox-test1.test.k8s-ingress-nginx.kuainiujinke.com/api/test/withdrawMission
    ?userId=6c6733bef08f48cfa2cf27783981bee3&type=all' \

    country_tag：1国内，2海外
    sys_user_id：催员ID
    operate_type：撤案类型，all撤所有案，currentDay撤当天案
    """
    if country_tag == 1:
        LogUtil.log_info("当前运行环境：国内测试环境fox1")
        req_url = cn_fox_url
    if country_tag == 2:
        LogUtil.log_info("当前运行环境：海外测试环境")
        req_url = overseas_fox_url
    url = req_url + "/api/test/withdrawMission?userId=%s&type=%s&unAssignReason=%s" % (sys_user_id, operate_type, "自动化测试撤案")
    header = {"Content-Type": "application/x-www-form-urlencoded"}
    if operate_type == "all":
        LogUtil.log_info("撤案类型：撤所有案，当前需要执行撤案的催员ID：%s" % sys_user_id)
    if operate_type == "currentDay":
        LogUtil.log_info("撤案类型：撤当天案，当前需要执行撤案的催员ID：%s" % sys_user_id)
    request_data = {}
    from foundation_test.function.dh.assign_case.assign_db_function import get_current_in_hand_case_num
    in_hand_cases = get_current_in_hand_case_num(sys_user_id)
    if in_hand_cases:
        LogUtil.log_info("#### 催员=%s，撤案前在手案件数量=%s" % (sys_user_id, in_hand_cases[0]["assignDebtorNum"]))
    if not in_hand_cases:
        LogUtil.log_info("#### 催员=%s，撤案前当前在手案件数量=0" % sys_user_id)

    fails = 0
    for i in range(60):
        Http.http_post(url, request_data, header)
        # 撤案后，获取当前在手案件数量
        in_hand_cases = get_current_in_hand_case_num(sys_user_id)
        if in_hand_cases:
            time.sleep(1)
            fails += 1
            LogUtil.log_info("#### 撤案尚未完成，等待中，等待时间：%s，催员=%s，在手案件数量=%s" % (fails, sys_user_id, in_hand_cases[0]["assignDebtorNum"]))
        if not in_hand_cases:
            LogUtil.log_info("撤案成功")
            break
    if fails == 60:
        print("#### 请检查测试环境fox是否正常运行。")
        return


# 国内，短账龄分案给业务组
def assign_assets(debtor_id):
    """
    curl -L -X POST 'http://fox-test1.test.k8s-ingress-nginx.kuainiujinke.com/a/mission/assignAssets' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -H 'Cookie: fox.session.id=f42a0b3a8a89467a9c98164bb148cff2' \
    --data-urlencode 'debtorIds=3287250' \
    --data-urlencode 'userId=1e56501bd6734c528fa2bfcdf9cd543b'
    """
    url = cn_fox_url + "/a/asset/assignAsset"
    session_id = dh_login(1)
    header = {"Content-Type": "application/x-www-form-urlencoded", "Cookie": "fox.session.id=" + session_id}
    request_data = {
        "debtorIds": debtor_id,
        "userId": '1e56501bd6734c528fa2bfcdf9cd543b'
    }
    LogUtil.log_info("debtor_id=%s, session_id=%s" % (debtor_id, session_id))
    Http.http_post(url, request_data, header)
    fails = 0
    for i in range(60):
        from foundation_test.function.dh.asset_sync.dh_db_function import get_mission_log_by_debtor_id, get_collect_recovery_by_asset_id
        mission_log_info = get_mission_log_by_debtor_id(debtor_id)
        collect_recovery = get_collect_recovery_by_asset_id(mission_log_info[0]["mission_log_asset_id"])
        if mission_log_info[0]["mission_log_operator"] == "assign" and collect_recovery:
            print('分案成功!')
            time.sleep(3)
            break
        else:
            time.sleep(1)
            fails += 1
            print('分案尚未成功，等待中，等待时间：', fails)
    return session_id


def cn_inner_assign_rule_assign_assets(group_list, unassigned_debtor_amount):
    """
    curl --location --request POST 'http://fox-test1.test.k8s-ingress-nginx.kuainiujinke.com/a/mission/assignAssets' \
    --header 'Cookie: fox.session.id=89a81f50049641eda7c764b4983a8b1f' \
    --header 'Content-Type: application/json' \
    --data-raw '{
      "missionBehaviorBatchNum": "",
      "assetType": "现金贷多期",
      "startLateDays": "7",
      "endLateDays": "7",
      "contactFlag": null,
      "selectedContactLabels": [],
      "arbitrationFlag": null,
      "selectedArbitrationLabels": [],
      "contactLostRepairFlag": null,
      "selectedContactLostRepairLabels": [],
      "restructureFlag": null,
      "selectedRestructureLabels": [],
      "userTypeFlag": false,
      "selectedUserTypeLabels": [],
      "productPeriodFlag": false,
      "selectedProductPeriodLabels": [],
      "assignMissionType": "avg",
      "cCardM1PlusStart": "",
      "cCardM1PlusEnd": "",
      "cCardD3Start": "",
      "cCardD3End": "",
      "assignGroupVos": [
        {
          "userNum": "5",
          "averageNum": "2",
          "group": "12653054dbd24240b7546bef20a404fd",
          "groupName": "自动化测试_A1组"
        },
        {
          "userNum": "6",
          "averageNum": "2",
          "group": "db81b9eb48004247abe7d592f4f01714",
          "groupName": "自动化测试_A2组"
        }
      ],
      "allAmount": "",
      "assignTargetType": "assignToCollector",
      "unAssignedDebtorAmount": 10
    }'
    """
    # 获取各个业务组下的催员人数、组ID
    url = cn_fox_url + "/a/mission/assignAssets"
    session_id = dh_login(1)
    header = {"Content-Type": "application/json", "Cookie": "fox.session.id=" + session_id}
    request_data = {
        "missionBehaviorBatchNum": "",
        "assetType": "现金贷多期",
        "startLateDays": "7",
        "endLateDays": "7",
        "contactFlag": NULL,
        "selectedContactLabels": [],
        "arbitrationFlag": NULL,
        "selectedArbitrationLabels": [],
        "contactLostRepairFlag": NULL,
        "selectedContactLostRepairLabels": [],
        "restructureFlag": NULL,
        "selectedRestructureLabels": [],
        "userTypeFlag": False,
        "selectedUserTypeLabels": [],
        "productPeriodFlag": False,
        "selectedProductPeriodLabels": [],
        "assignMissionType": "avg",
        "cCardM1PlusStart": "",
        "cCardM1PlusEnd": "",
        "cCardD3Start": "",
        "cCardD3End": "",
        "assignGroupVos": [
            {
                "userNum": "5",
                "averageNum": "2",
                "group": "12653054dbd24240b7546bef20a404fd",
                "groupName": "自动化测试_A1组"
            },
            {
                "userNum": "6",
                "averageNum": "2",
                "group": "db81b9eb48004247abe7d592f4f01714",
                "groupName": "自动化测试_A2组"
            }
        ],
        "allAmount": "",
        "assignTargetType": "assignToCollector",
        "unAssignedDebtorAmount": unassigned_debtor_amount
    }
    # LogUtil.log_info("debtor_id=%s, session_id=%s" % (debtor_id, session_id))
    # Http.http_post(url, request_data, header)
    # fails = 0
    # for i in range(60):
    #     from foundation_test.function.dh.asset_sync.dh_db_function import get_mission_log_by_debtor_id
    #     mission_log_info = get_mission_log_by_debtor_id(debtor_id)
    #     collect_recovery = get_collect_recovery_by_asset_id(mission_log_info[0]["mission_log_asset_id"])
    #     if mission_log_info[0]["mission_log_operator"] == "assign" and collect_recovery:
    #         print('分案成功!')
    #         time.sleep(3)
    #         break
    #     else:
    #         time.sleep(1)
    #         fails += 1
    #         print('分案尚未成功，等待中，等待时间：', fails)
    # return session_id


if __name__ == '__main__':
    LogUtil.log_info("1212312321")
    dc.init_dh_env(1, "china", "dev")
    LogUtil.log_info("#### 当前环境env=%s，country=%s，environment=%s"
                     % (dc.ENV, dc.COUNTRY, dc.ENVIRONMENT))
    run_quartz(1, "newAT_abilityCoefficientInHand")
