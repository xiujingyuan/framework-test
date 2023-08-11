import json

from flask import request, Response

from app.tool import common_tool
from biztest.util.tools.tools import get_four_element_global, get_four_element, encry_data, decrypt_data, \
    global_decrypt_data
import common.global_const as gc


def get_method(class_name):
    test_func = []
    all_func = dir(globals()[class_name]) if class_name in globals() else []
    for func in all_func:
        if func.startswith("test_"):
            test_func.append(func)
    return test_func


def formatter(src: str, firstUpper: bool = True):
    """
    将下划线分隔的名字,转换为驼峰模式
    :param src:
    :param firstUpper: 转换后的首字母是否指定大写(如
    :return:
    """
    arr = src.split('_')
    res = ''
    for i in arr:
        res = res + i[0].upper() + i[1:]
    if not firstUpper:
        res = res[0].lower() + res[1:]
    return res


@common_tool.route('/encry-data', methods=['POST'])
def encryt_data_tool():
    request_params = request.json
    response = {"code": 0,
                "data": {},
                "msg": "success"}
    if "card_number" in request_params.keys():
        response["data"]["card_number"] = encry_data("card_number", request_params["card_number"])
    if "idnum" in request_params.keys():
        response["data"]["idnum"] = encry_data("idnum", request_params["idnum"])
    if "mobile" in request_params.keys():
        response["data"]["mobile"] = encry_data("mobile", request_params["mobile"])
    if "name" in request_params.keys():
        response["data"]["name"] = encry_data("name", request_params["name"])
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')


@common_tool.route('/decrypt-data', methods=['POST'])
def decrypt_data_tool():
    request_params = request.json
    response = {"code": 0,
                "data": {},
                "msg": "success"}
    if "card_number" in request_params.keys():
        response["data"]["card_number"] = decrypt_data(request_params["card_number"])
    if "idnum" in request_params.keys():
        response["data"]["idnum"] = decrypt_data(request_params["idnum"])
    if "mobile" in request_params.keys():
        response["data"]["mobile"] = decrypt_data(request_params["mobile"])
    if "name" in request_params.keys():
        response["data"]["name"] = decrypt_data(request_params["name"])
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')


@common_tool.route('/fourelement', methods=['POST', 'GET'])
def four_element():
    request_params = request.json
    bank = request_params["bank"] if "bank" in request_params.keys() else "中国银行"
    bank_code_suffix = request_params["bank_code_suffix"] if "bank_code_suffix" in request_params.keys() else None
    bank_code_begin = request_params["bank_code_begin"] if "bank_code_begin" in request_params.keys() else None
    min_age = request_params["min_age"] if "min_age" in request_params.keys() else "22"
    max_age = request_params["max_age"] if "max_age" in request_params.keys() else "50"
    gender = request_params["gender"] if "gender" in request_params.keys() else "F"
    id_num_begin = request_params["id_num_begin"] if "id_num_begin" in request_params.keys() else None
    result = get_four_element(bank, bank_code_begin, bank_code_suffix, int(min_age), int(max_age), gender, id_num_begin)
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')


@common_tool.route('/global-fourelement', methods=['POST', 'GET'])
def global_four_element():
    result = get_four_element_global()
    return Response(json.dumps(result, ensure_ascii=False), mimetype='application/json')


@common_tool.route('/global-decrypt-data', methods=['POST'])
def global_decrypt_data_tool():
    request_params = request.json
    response = {"code": 0,
                "data": {},
                "msg": "success"}
    if "card_number" in request_params.keys():
        response["data"]["card_number"] = global_decrypt_data(request_params["card_number"])
    if "idnum" in request_params.keys():
        response["data"]["idnum"] = global_decrypt_data(request_params["idnum"])
    if "mobile" in request_params.keys():
        response["data"]["mobile"] = global_decrypt_data(request_params["mobile"])
    if "name" in request_params.keys():
        response["data"]["name"] = global_decrypt_data(request_params["name"])
    return Response(json.dumps(response, ensure_ascii=False), mimetype='application/json')
