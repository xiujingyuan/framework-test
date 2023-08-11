# -*- coding: utf-8 -*-
from datetime import datetime, time
import time
from dateutil.relativedelta import relativedelta
import uuid
import json
import pytest
import requests
import collections
import re
import random
from decimal import Decimal
from dateutil import tz
from faker import Faker


def get_tz(country=None):
    if country is None:
        country = get_sysconfig("--country")
    if country == "india":
        timezone = tz.gettz("Asia/Kolkata")
    elif country == "indonesia":
        timezone = tz.gettz("Asia/Jakarta")
    elif country == "thailand":
        timezone = tz.gettz("Asia/Bangkok")
    elif country == "philippines":
        timezone = tz.gettz("Asia/Manila")
    elif country == "mexico":
        timezone = tz.gettz("America/Mexico_City")
    elif country == "pakistan":
        timezone = tz.gettz("Asia/Karachi")
    else:
        timezone = tz.gettz("Asia/Shanghai")
    return timezone


def get_date(year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S", timezone=None, hour=0, minute=0, second=0):
    if timezone is None:
        timezone = get_tz()
    return (datetime.now(timezone) + relativedelta(years=year, months=month, days=day,
                                                   hours=hour, minutes=minute, seconds=second)).strftime(fmt)


def get_date_timestamp(year=0, month=0, day=0):
    return int((datetime.now() + relativedelta(years=year, months=month, days=day)).timestamp())


def get_date_by_old_date(old_date, date_form, year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S"):
    return (datetime.strptime(old_date, date_form) + relativedelta(years=year, months=month, days=day)).strftime(fmt)


def get_item_no():
    return "A" + re.sub("[- :.]", "", str(datetime.now()))


def get_random_str(num=10):
    data = '1234567890abcdefghijklmnopqrstuvwxyz'
    result = ''
    for i in range(num):
        result = result + random.choice(list(data))
    return result


def get_random_num():
    return str(random.randint(100000000, 10000000000000))


def get_timestamp():
    return str(datetime.now().timestamp()).replace('.', '')


def date_to_timestamp(date_str, fmt="%Y-%m-%d %H:%M:%S"):
    # 返回毫秒级的时间戳
    return int(datetime.strptime(date_str, fmt).timestamp()) * 1000


def get_guid():
    return str(uuid.uuid1())


def get_guid4():
    return str(uuid.uuid4())


def get_four_element(bank_name=None, bank_code_begin=None, bank_code_suffix=None, min_age=25, max_age=45, gender="F",
                     id_num_begin=None, encrypt=True):
    fake = Faker("zh_CN")
    id_number = get_id_num(fake, min_age, max_age, gender, id_num_begin)
    phone_number = fake.phone_number()
    user_name = fake.name()
    bank_code = get_bank_code(bank_name, bank_code_begin, bank_code_suffix)
    response = {
        "code": 0,
        "message": "success",
        "data": {
            "bank_code": bank_code,
            "phone_number": phone_number,
            "user_name": user_name,
            "id_number": id_number,

        }
    }
    if encrypt:
        response["data"]["bank_code_encrypt"] = encry_data("card_number", bank_code)
        response["data"]["id_number_encrypt"] = encry_data("idnum", id_number)
        response["data"]["phone_number_encrypt"] = encry_data("mobile", phone_number)
        response["data"]["user_name_encrypt"] = encry_data("name", user_name)
    print("四要素获取完成，姓名：%s，身份证：%s，银行卡：%s，电话：%s" % (user_name, id_number, bank_code, phone_number))
    return response


def get_four_element_in_payment(bank_name=None, bank_code_suffix=None):
    # 获取四要素
    four_element_resp = get_four_element(bank_name, bank_code_suffix)
    four_element = {"bank_code_encrypt": four_element_resp["data"]["bank_code_encrypt"],
                    "id_number_encrypt": four_element_resp["data"]["id_number_encrypt"],
                    "phone_number_encrypt": four_element_resp["data"]["phone_number_encrypt"],
                    "user_name_encrypt": four_element_resp["data"]["user_name_encrypt"],
                    "bank_code": four_element_resp["data"]["bank_code"],
                    "id_number": four_element_resp["data"]["id_number"],
                    "phone_number": four_element_resp["data"]["phone_number"],
                    "user_name": four_element_resp["data"]["user_name"]
                    }
    return four_element


def get_id_num(fake, min_age, max_age, gender, id_num_begin):
    id_number = "999999999"
    if id_num_begin is not None:
        for i in range(5000):
            id_number_temp = fake.ssn(min_age=min_age, max_age=max_age, gender=gender)
            if id_number_temp.startswith(id_num_begin):
                id_number = id_number_temp
                break
            else:
                continue
        if id_number == "999999999":
            id_number = fake.ssn(min_age=min_age, max_age=max_age, gender=gender)
    else:
        id_number = fake.ssn(min_age=min_age, max_age=max_age, gender=gender)
    return id_number


def get_bank_code(bank_name="中国银行", bank_code_begin=None, bank_code_suffix=None):
    bank_map = [("中国银行", "621394"),
                ("工商银行", "621761"),
                ("招商银行", "622598"),
                ("建设银行", "552245"),
                ("民生银行", "622618"),
                ("工商银行1", "621670")]
    bank_code_bin = "621394"
    for bank in bank_map:
        if bank[0] == bank_name:
            bank_code_bin = bank[1]
            break
    # 生成需要的银行卡并返回
    bank_code = None
    for _ in range(500):
        bank_code = gen_card_num(bank_code_bin, 16)
        if bank_code_begin is not None and bank_code_suffix is None and bank_code.startswith(bank_code_begin):
            break
        elif bank_code_begin is None and bank_code_suffix is not None and bank_code.endswith(bank_code_suffix):
            break
        elif bank_code_begin is not None and bank_code_suffix is not None \
                and bank_code.startswith(bank_code_begin) \
                and bank_code.endswith(bank_code_suffix):
            break
        else:
            continue
    return bank_code


def gen_card_num(start_with, total_num):
    result = start_with

    # 随机生成前N-1位
    while len(result) < total_num - 1:
        result += str(random.randint(0, 9))

    # 计算前N-1位的校验和
    s = 0
    card_num_length = len(result)
    for _ in range(2, card_num_length + 2):
        t = int(result[card_num_length - _ + 1])
        if _ % 2 == 0:
            t *= 2
            s += t if t < 10 else t % 10 + t // 10
        else:
            s += t

    # 最后一位当做是校验位，用来补齐到能够整除10
    t = 10 - s % 10
    result += str(0 if t == 10 else t)
    return result


# 银行卡校验
def luhn(card_num):
    s = 0
    card_num_length = len(card_num)
    for _ in range(1, card_num_length + 1):
        t = int(card_num[card_num_length - _])
        if _ % 2 == 0:
            t *= 2
            s += t if t < 10 else t % 10 + t // 10
        else:
            s += t
    return s % 10 == 0


def get_four_element_global(id_num_begin=None):
    four_element = get_four_element(id_num_begin=id_num_begin, encrypt=False)
    response = {
        "code": 0,
        "message": "success",
        "data": {
            "bank_account": four_element["data"]["bank_code"],
            "card_num": four_element["data"]["bank_code"],
            "mobile": four_element["data"]["phone_number"],
            "user_name": "Craltonliu",
            "id_number": four_element["data"]["id_number"],
            "address": "Floor 8 TaiPingYang Building TianFuSanGai Chengdu,Sichuan,China",
            "email": four_element["data"]["phone_number"] + "@qq.com",
            "upi": four_element["data"]["phone_number"] + "@upi"
        }
    }
    body = [{"type": 1,
             "plain": response["data"]["mobile"]},
            {"type": 2,
             "plain": response["data"]["id_number"]},
            {"type": 3,
             "plain": response["data"]["card_num"]},
            {"type": 3,
             "plain": response["data"]["upi"]},
            {"type": 4,
             "plain": response["data"]["user_name"]},
            {"type": 5,
             "plain": response["data"]["email"]},
            {"type": 6,
             "plain": response["data"]["address"]}]
    resp = requests.post(url="http://encryptor-test.k8s-ingress-nginx.kuainiujinke.com/encrypt/", json=body).json()

    response["data"]["mobile_encrypt"] = resp["data"][0]["hash"]
    response["data"]["id_number_encrypt"] = resp["data"][1]["hash"]
    response["data"]["card_num_encrypt"] = resp["data"][2]["hash"]
    response["data"]["upi_encrypt"] = resp["data"][3]["hash"]
    response["data"]["user_name_encrypt"] = resp["data"][4]["hash"]
    response["data"]["email_encrypt"] = resp["data"][5]["hash"]
    response["data"]["address_encrypt"] = resp["data"][6]["hash"]
    response["data"]["bank_account_encrypt"] = resp["data"][2]["hash"]
    return response


def encry_four_element(card_number, id_num, mobile, name):
    response = {
        "code": 0,
        "message": "success",
        "data": {
            "bank_code": card_number,
            "phone_number": mobile,
            "user_name": name,
            "id_number": id_num,
            "bank_code_encrypt": encry_data("card_num", card_number),
            "id_number_encrypt": encry_data("idnum", id_num),
            "phone_number_encrypt": encry_data("mobile", mobile),
            "user_name_encrypt": encry_data("name", name)
        }
    }
    return response


def encry_data(data_type, value):
    if data_type == "idnum":
        data = {"type": 2, "plain": value}
    elif data_type == "mobile":
        data = {"type": 1, "plain": value}
    elif data_type == "card_number":
        data = {"type": 3, "plain": value}
    elif data_type == "name":
        data = {"type": 4, "plain": value}
    elif data_type == "email":
        data = {"type": 5, "plain": value}
    elif data_type == "address":
        data = {"type": 6, "plain": value}
    else:
        data = None
    url = "http://encryptor-test.k8s-ingress-nginx.kuainiujinke.com/encrypt/"
    headers = {'content-type': 'application/json'}
    new_data = [data]
    req = requests.post(url, data=json.dumps(new_data), headers=headers, timeout=10)
    result = req.json()
    if result['code'] == 0:
        return result['data'][0]['hash']
    return req.json()


def encry_data_except(data_type, value):
    if data_type == "id_number":
        data = {"type": 2, "plain": value}
    elif data_type == "phone_number":
        data = {"type": 1, "plain": value}
    elif data_type == "bank_code":
        data = {"type": 3, "plain": value}
    elif data_type == "user_name":
        data = {"type": 4, "plain": value}
    elif data_type == "email":
        data = {"type": 5, "plain": value}
    elif data_type == "address":
        data = {"type": 6, "plain": value}
    else:
        data = None
    url = "http://encryptor-test.k8s-ingress-nginx.kuainiujinke.com/encrypt/"
    headers = {'content-type': 'application/json'}
    new_data = [data]
    req = requests.post(url, data=json.dumps(new_data), headers=headers, timeout=10)
    result = req.json()
    if result['code'] == 0:
        return result['data'][0]['hash']
    return req.json()


def global_encry_data(data_type, value):
    if data_type == "idnum":
        data = {"type": 2, "plain": value}
    elif data_type == "mobile":
        data = {"type": 1, "plain": value}
    elif data_type == "card_number":
        data = {"type": 3, "plain": str(value)}
    elif data_type == "name":
        data = {"type": 4, "plain": value}
    elif data_type == "email":
        data = {"type": 5, "plain": value}
    elif data_type == "address":
        data = {"type": 6, "plain": value}
    else:
        data = None
    url = "http://encryptor-test.k8s-ingress-nginx.kuainiujinke.com/encrypt/"
    headers = {'content-type': 'application/json'}
    new_data = [data]
    req = requests.post(url, data=json.dumps(new_data), headers=headers, timeout=10)
    result = req.json()
    if result['code'] == 0:
        return result['data'][0]['hash']
    return req.json()


def decrypt_data(value):
    url = "http://encryptor-test.k8s-ingress-nginx.kuainiujinke.com/decrypt/plain/"
    headers = {'content-type': 'application/json'}
    data = {"hash": value}
    new_data = [data]
    req = requests.post(url, data=json.dumps(new_data), headers=headers, timeout=10)
    result = req.json()
    if result['code'] == 0:
        return result['data'][value]
    return req.json()


def global_decrypt_data(value):
    url = "http://encryptor-test.k8s-ingress-nginx.kuainiujinke.com/decrypt/plain/"
    headers = {'content-type': 'application/json'}
    data = {"hash": value}
    new_data = [data]
    req = requests.post(url, data=json.dumps(new_data), headers=headers, timeout=10)
    result = req.json()
    if result['code'] == 0:
        return result['data'][value]
    return req.json()


def get_sysconfig(option):
    return str(pytest.config.getoption(option)) if hasattr(pytest, 'config') else 1


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
    try:
        request = json.loads(resp.request.body)
    except Exception as e:
        request = resp.request.body
    resp = {
        "status_code": resp.status_code,
        "content": content,
        "headers": resp.headers,
        "cookies": requests.utils.dict_from_cookiejar(resp.cookies),
        "reason": resp.reason,
        "req": request
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

    :param year: 正数 往后推1年，负数往前推1年
    :param month: 正数 往后推1月，负数往前推1月
    :param day: 正数 往后推1天，负数往前推1天
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


def get_timestamp_by_now(length=13):
    t = datetime.now().timestamp()
    if length == 10:
        return int(t)
    elif length == 13:
        return int(round(t * 1000))
    elif length == 16:
        return int(round(t * 1000000))
    else:
        return t


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


def generate_sql(sql_param, split):
    sql = ""
    if isinstance(sql_param, dict):
        for key, value in sql_param.items():
            sql += str(key) + "='" + str(value) + "' " + str(split) + " "
    return sql[:(-len(split) - 1)]


def get_calc_date(base_time, year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S", is_str=True):
    """
    :param base_time: 正数 往后推1年，负数往前推1年
    :param year: 正数 往后推1年，负数往前推1年
    :param month: 正数 往后推1月，负数往前推1月
    :param day: 正数 往后推1天，负数往前推1天
    :param fmt: 时间格式化
    :param is_str: 是否返回字符串
    :return:
    """
    ret = base_time + relativedelta(years=year, months=month, days=day)
    return ret.strftime(fmt) if is_str else ret


if __name__ == "__main__":
    from pprint import pprint

    print(get_four_element(bank_name='工商银行', bank_code_begin="621670"))
    # print(get_four_element_global())
    # # pprint(get_four_element())
    # pprint(get_four_element_global())
    # print(decrypt_data("enc_02_4117877493238079488_250"))
    # print(global_decrypt_data("enc_03_4154896192994025472_360"))
    # print(global_encry_data("card_number", global_decrypt_data("enc_03_2907707556133085184_449")))
