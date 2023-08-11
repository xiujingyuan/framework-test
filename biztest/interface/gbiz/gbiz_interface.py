import json
import time
from datetime import datetime
import requests
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.config.gbiz.gbiz_interface_params_config import *
from biztest.function.gbiz.gbiz_db_function import insert_router_load_record, \
    get_asset_extend_by_item_no, get_asset_import_data_by_item_no, get_withdraw_record_by_item_no
from biztest.function.gbiz.gbiz_util_function import calc_noloan_amount, get_available_capital_rule
import biztest.config.gbiz.gbiz_common_config as gbiz_common_config
from copy import deepcopy
from biztest.util.asserts.assert_util import Assert
from biztest.util.http.http_util import Http as http
from biztest.util.tools.tools import get_item_no, get_random_str
import common.global_const as gc


def monitor_check(timeout=60):
    result = None
    for i in range(timeout):
        url = gc.GRANT_URL + gbiz_monitor_check_url
        try:
            headers = {"Content-Type": "application/json", "Connection": "close"}
            resp = requests.get(url, headers=headers, timeout=10)
            print(resp.status_code)
            if resp.status_code == 200:
                print('monitor check passed')
                result = True
                break
            else:
                result = False
                time.sleep(1)
        except:
            result = False
    return result


def asset_import(channel, element, count, amount, from_system_name='香蕉', source_type='apr36', item_no='',
                 borrower_extend_district='', sub_order_type='', route_uuid='', product_code='',
                 insert_router_record=True, get_info=True):
    if item_no:
        pass
    else:
        item_no = get_item_no()

    if from_system_name == "贷上钱":
        from_system = "dsq"
    elif from_system_name in ("草莓", "重庆草莓", "杭州草莓"):
        from_system = "strawberry"
    elif from_system_name == "香蕉":
        from_system = "banana"
    elif from_system_name == "火龙果":
        from_system = "pitaya"
    else:
        from_system = "dsq"
    if from_system_name == "火龙果" and source_type == "irr36_lexin":
        ref_order_no = item_no + "_lexin"
    elif from_system_name == "火龙果" or "real36" in source_type:
        ref_order_no = ""
    else:
        ref_order_no = item_no + "_noloan"

    asset_info = deepcopy(asset_import_info)
    asset_info['key'] = item_no + channel
    asset_info['from_system'] = from_system
    asset_info['data']['asset']['item_no'] = item_no
    asset_info['data']['asset']['name'] = "tn" + item_no
    if count == 1:
        asset_info['data']['asset']['period_type'] = "day"
        asset_info['data']['asset']['period_count'] = count
        asset_info['data']['asset']['period_day'] = 30
    else:
        asset_info['data']['asset']['period_type'] = "month"
        asset_info['data']['asset']['period_count'] = count
        asset_info['data']['asset']['period_day'] = 0
    asset_info['data']['asset']['amount'] = amount
    asset_info['data']['asset']['grant_at'] = get_date()
    asset_info['data']['asset']['loan_channel'] = channel
    asset_info['data']['asset']['source_type'] = source_type
    # asset_info['data']['asset']['from_system'] = from_system
    # asset_info['data']['asset']['from_system_name'] = from_system_name
    asset_info['data']['asset']['from_app'] = from_system_name
    asset_info['data']['asset']['source_number'] = ref_order_no
    asset_info['data']['asset']['sub_order_type'] = sub_order_type

    asset_info['data']['repay_card']['username_encrypt'] = \
        asset_info['data']['receive_card']['owner_name_encrypt'] = \
        asset_info['data']['receive_card']['account_name_encrypt'] = \
        asset_info['data']['borrower']['name_encrypt'] = \
        asset_info['data']['repayer']['name_encrypt'] = element['data']['user_name_encrypt']

    asset_info['data']['repay_card']['phone_encrypt'] = \
        asset_info['data']['receive_card']['phone_encrypt'] = \
        asset_info['data']['borrower']['tel_encrypt'] = \
        asset_info['data']['borrower']['corp_tel_encrypt'] = \
        asset_info['data']['repayer']['tel_encrypt'] = \
        element['data']['phone_number_encrypt']

    asset_info['data']['repay_card']['individual_idnum_encrypt'] = \
        asset_info['data']['repay_card']['credentials_num_encrypt'] = \
        asset_info['data']['receive_card']['owner_id_encrypt'] = \
        asset_info['data']['borrower']['idnum_encrypt'] = \
        asset_info['data']['repayer']['idnum_encrypt'] = element['data']['id_number_encrypt']

    asset_info['data']['repay_card']['account_num_encrypt'] = \
        asset_info['data']['receive_card']['num_encrypt'] = \
        element['data']['bank_code_encrypt']

    if borrower_extend_district:
        asset_info['data']['borrower_extend']['address_district_code'] = borrower_extend_district
        asset_info['data']['borrower_extend']['device_ip'] = "192.168.1.109"
        asset_info['data']['borrower_extend']['device_mac'] = "00:fdaf:fdas:00"
    if route_uuid:
        asset_info['data']['route_uuid'] = route_uuid
    else:
        asset_info['data']['route_uuid'] = item_no + channel
    # if channel == 'hamitianbang_xinjiang':
    #     asset_info['data']['borrower']['id_addr'] = "新疆伊宁市解放西路380号徐汇苑14号楼1单元201室"
    if channel == 'qinnong':
        asset_info['data']['borrower']['id_addr'] = "陕西省宝鸡市渭滨区经一路62号付1号"
    if channel == 'zhenxing_zhongzhixin_jx':
        asset_info['data']['borrower']['id_addr'] = "辽宁省大连市金州区友谊街道龙王庙村张家屯44号"
    if channel in ['qinnong_jieyi', 'qinnong_dingfeng']:
        asset_info['data']['borrower']['residence'] = "陕西省白水县北塬乡潘村二社"
    if channel in ['lanzhou_haoyue', 'lanzhou_haoyue_zk3']:
        asset_info['data']['borrower']['residence'] = "甘肃省兰州市七里河区土门墩新村451号"
    if channel == "siping_jiliang":
        # 根据特定金额判断是否修改活体照上传时间
        asset_info['data']['receive_card']['bank_code'] = "ABC"
        if amount != 6666:
            asset_info['data']['attachments'][2]['attachment_upload_at'] = "@now"
    if amount != 6666 and channel == 'yixin_rongsheng':
        asset_info['data']['asset_extend']['sub_asset'] = None

    # 进件前，在路由表插入一条记录
    capital_rule = get_available_capital_rule(channel, count, product_code)
    if channel in ('lanhai_zhongshi_qj', 'daxinganling_zhongyi'):
        keys = {"router_load_record_key": item_no + channel,
                "router_load_record_rule_code": capital_rule.get("rule_code"),
                "router_load_record_principal_amount": amount * 100,
                "router_load_record_status": "routed",
                "router_load_record_channel": channel,
                "router_load_record_sub_type": "multiple",
                "router_load_record_period_count": count,
                "router_load_record_period_type": "month",
                "router_load_record_period_days": "0",
                "router_load_record_sub_order_type": sub_order_type,
                "router_load_record_route_day": get_date(fmt="%Y-%m-%d"),
                "router_load_record_idnum": element['data']['id_number_encrypt'],
                "router_load_record_from_system": asset_info['from_system'],
                "router_load_record_product_code": capital_rule.get("rule_product_code", ""),
                "router_load_record_extend_info": "{\"district\":{\"idNumDistrict\":\"四川省\",\"idAddrDistrict\":"
                                                  "\"四川省\",\"residentialDistrict\":\"四川省\",\"workplaceDistrict\":"
                                                  "\"四川省\",\"mobileDistrict\":\"四川省\",\"ipDistrict\":\"\","
                                                  "\"gpsDistrict\":\"\"}}"
                }
    else:
        keys = {"router_load_record_key": item_no + channel,
                "router_load_record_rule_code": capital_rule.get("rule_code"),
                "router_load_record_principal_amount": amount * 100,
                "router_load_record_status": "routed",
                "router_load_record_channel": channel,
                "router_load_record_sub_type": "multiple",
                "router_load_record_period_count": count,
                "router_load_record_period_type": "month",
                "router_load_record_period_days": "0",
                "router_load_record_sub_order_type": sub_order_type,
                "router_load_record_route_day": get_date(fmt="%Y-%m-%d"),
                "router_load_record_idnum": element['data']['id_number_encrypt'],
                "router_load_record_from_system": asset_info['from_system'],
                "router_load_record_product_code": capital_rule.get("rule_product_code", "")
                }
    if insert_router_record:
        insert_router_load_record(**keys)

    # 路由到资方后，再进件
    asset_import_url = gc.GRANT_URL + gbiz_asset_import_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(asset_import_url, asset_info, header)
    Assert.assert_equal(0, resp['code'], resp)

    if resp['code'] == 0 and get_info:
        time.sleep(2)
        asset_info = get_asset_import_data_by_item_no(item_no)

    return item_no, asset_info


def asset_import_noloan(asset_info, source_type="", sub_order_type="", amount=None):
    asset_info_noloan = deepcopy(asset_info)
    loan_channel = asset_info["data"]["asset"]["loan_channel"]
    item_no = asset_info['data']['asset']['item_no']
    item_no_noloan = asset_info['data']['asset']['source_number']
    if loan_channel in ["yixin_hengrun", "yixin_rongsheng"] and asset_info['data']['asset']['amount'] == 6666:
        asset_info_noloan['data']['asset']['period_count'] = \
            asset_info["data"]["asset_extend"]["sub_asset"]["period_count"]
    if source_type == "lieyin":
        item_no_noloan = item_no + "_quanyi"
        asset_info_noloan['data']['asset']['period_count'] = 5
    # 小单的sub_order_type需要与大单保持一致,获取大单的sub_order_type
    sub_order_type = get_asset_extend_by_item_no(item_no)[0]["asset_extend_sub_order_type"]
    if source_type:
        source_type = source_type
    elif asset_info['data']['asset']['source_type'] == "" or len(asset_info['data']['asset']['source_type']) == 0:
        source_type = "normal"
    else:
        source_type = asset_info['data']['asset']['source_type'] + "_split"
    asset_info_noloan['key'] = item_no_noloan
    asset_info_noloan['data']['asset']['item_no'] = item_no_noloan
    asset_info_noloan['data']['asset']['name'] = item_no_noloan
    asset_info_noloan['data']['asset']['source_number'] = item_no
    asset_info_noloan['data']['asset']['amount'] = \
        str(calc_noloan_amount(item_no, source_type)) if amount is None else amount
    asset_info_noloan['data']['asset']['source_type'] = source_type
    asset_info_noloan['data']['asset']['loan_channel'] = 'noloan'
    asset_info_noloan['data']['asset']['sub_order_type'] = sub_order_type
    asset_info_noloan['data']['dtransactions'] = []
    asset_info_noloan['data']['fees'] = []

    asset_import_url = gc.BASE_URL['china']['grant'].format(gc.ENV) + gbiz_asset_import_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(asset_import_url, asset_info_noloan, header)
    Assert.assert_equal(0, resp['code'], resp)

    if resp['code'] == 0:
        time.sleep(2)
        asset_info_noloan = get_asset_import_data_by_item_no(item_no_noloan)
    return asset_info_noloan['data']['asset']['item_no'], asset_info_noloan


def asset_route(element, count, amount, from_system_name='香蕉', source_type='apr36', channel='',
                borrower_extend_district='', key=None, id_addr='甘肃省天水市秦州区岷玉路罗玉小区市31幢3单元501室'):
    if from_system_name == "贷上钱":
        from_system = "dsq"
    elif from_system_name == "草莓":
        from_system = "strawberry"
    elif from_system_name == "香蕉":
        from_system = "banana"
    else:
        from_system = "dsq"

    asset_info = deepcopy(asset_route_info)
    if key:
        asset_info['key'] = key
    else:
        asset_info['key'] = get_item_no() + 'route'
    if channel:
        asset_info['data']['asset']['loan_channel'] = channel
    asset_info['from_system'] = from_system
    asset_info['data']['asset']['item_no'] = ""
    asset_info['data']['asset']['name'] = ""
    if count == 1:
        asset_info['data']['asset']['period_type'] = "day"
        asset_info['data']['asset']['period_count'] = count
        asset_info['data']['asset']['period_day'] = 30
    else:
        asset_info['data']['asset']['period_type'] = "month"
        asset_info['data']['asset']['period_count'] = count
        asset_info['data']['asset']['period_day'] = 0
    asset_info['data']['asset']['amount'] = amount
    asset_info['data']['asset']['grant_at'] = get_date()
    asset_info['data']['asset']['loan_channel'] = ""
    asset_info['data']['asset']['source_type'] = source_type
    asset_info['data']['asset']['from_system'] = from_system
    asset_info['data']['asset']['from_system_name'] = from_system_name
    asset_info['data']['asset']['from_app'] = from_system_name
    asset_info['data']['asset']['source_number'] = ""

    asset_info['data']['repay_card']['username_encrypt'] = \
        asset_info['data']['receive_card']['owner_name_encrypt'] = \
        asset_info['data']['receive_card']['account_name_encrypt'] = \
        asset_info['data']['borrower']['name_encrypt'] = \
        asset_info['data']['repayer']['name_encrypt'] = element['data']['user_name_encrypt']

    asset_info['data']['repay_card']['phone_encrypt'] = \
        asset_info['data']['receive_card']['phone_encrypt'] = \
        asset_info['data']['borrower']['tel_encrypt'] = \
        asset_info['data']['repayer']['tel_encrypt'] = \
        element['data']['phone_number_encrypt']

    asset_info['data']['repay_card']['individual_idnum_encrypt'] = \
        asset_info['data']['repay_card']['credentials_num_encrypt'] = \
        asset_info['data']['receive_card']['owner_id_encrypt'] = \
        asset_info['data']['borrower']['idnum_encrypt'] = \
        asset_info['data']['repayer']['idnum_encrypt'] = element['data']['id_number_encrypt']

    asset_info['data']['repay_card']['account_num_encrypt'] = \
        asset_info['data']['receive_card']['num_encrypt'] = \
        element['data']['bank_code_encrypt']

    asset_info['data']['borrower']['id_addr'] = id_addr

    if borrower_extend_district:
        asset_info['data']['borrower_extend']['address_district_code'] = borrower_extend_district

    asset_route_url = gc.GROUTER_URL + gbiz_asset_route_url_new
    header = {"Content-Type": "application/json"}
    resp = http.http_post(asset_route_url, asset_info, header)

    Assert.assert_equal(0, resp['code'], "路由接口异常")
    return resp['data']['route_channel']


def capital_withdraw(item_no):
    withdraw_body = deepcopy(withdraw_info)
    withdraw_body['key'] = item_no + get_random_str()
    withdraw_body['data']['item_no'] = item_no
    withdraw_url = gc.BASE_URL['china']['grant'].format(gc.ENV) + gbiz_withdraw_url
    header = {"Content-Type": "application/json"}
    return http.http_post(withdraw_url, withdraw_body, header)


def capital_withdraw_query(item_no):
    withdraw_query_body = deepcopy(withdraw_query_info)
    withdraw_query_body['key'] = item_no + get_random_str()
    withdraw_query_body['data']['item_no'] = item_no
    withdraw_query_url = gc.GRANT_URL + gbiz_withdraw_query_url
    header = {"Content-Type": "application/json"}
    return http.http_post(withdraw_query_url, withdraw_query_body, header)


def capital_regiest(channel, element, item_no='121212', from_system='strawberry', action_type='', way='', step_type='',
                    seq='', code='111111'):
    regiest_body = deepcopy(regiest_info)
    regiest_body['key'] = item_no + get_random_str()
    regiest_body['from_system'] = from_system
    regiest_body['type'] = action_type
    regiest_body['data']['channel'] = channel
    regiest_body['data']['item_no'] = item_no
    regiest_body['data']['way'] = way
    regiest_body['data']['step_type'] = step_type
    regiest_body['data']['action_type'] = action_type
    regiest_body['data']['mobile_encrypt'] = element['data']['phone_number_encrypt']
    regiest_body['data']['id_num_encrypt'] = element['data']['id_number_encrypt']
    regiest_body['data']['username_encrypt'] = element['data']['user_name_encrypt']
    regiest_body['data']['card_num_encrypt'] = element['data']['bank_code_encrypt']
    regiest_body['data']['extend']['seq'] = seq
    regiest_body['data']['extend']['code'] = code
    regiest_url = gc.GRANT_URL + gbiz_capital_regiest_url
    header = {"Content-Type": "application/json"}
    ret = http.http_post(regiest_url, regiest_body, header)
    return ret


def capital_regiest_query(channel, element, item_no='121212', from_system='strawberry'):
    regiest_query_body = deepcopy(regiest_query_info)
    regiest_query_body['key'] = item_no + get_random_str()
    regiest_query_body['from_system'] = from_system
    regiest_query_body['type'] = "AccountRegisterQuery"
    regiest_query_body['data']['channel'] = channel
    regiest_query_body['data']['item_no'] = item_no
    regiest_query_body['data']['id_num_encrypt'] = element['data']['id_number_encrypt']
    regiest_query_body['data']['card_num_encrypt'] = element['data']['bank_code_encrypt']
    regiest_query_body['data']['mobile_encrypt'] = element['data']['phone_number_encrypt']
    regiest_query_body['data']['username_encrypt'] = element['data']['user_name_encrypt']
    regiest_url = gc.GRANT_URL + gbiz_capital_regiest_url_query_url
    header = {"Content-Type": "application/json"}
    ret = http.http_post(regiest_url, regiest_query_body, header)
    return ret


def get_sms_verifycode(channel, element, item_no='121212', source_type='youxi_bill'):
    get_sms_body = deepcopy(get_sms_verifycode_info)
    get_sms_body['key'] = item_no + get_random_str()
    get_sms_body['data']['channel'] = channel
    get_sms_body['data']['item_no'] = item_no
    get_sms_body['data']['source_type'] = source_type
    get_sms_body['data']['username_encrypt'] = element['data']['user_name_encrypt']
    get_sms_body['data']['id_num_encrypt'] = element['data']['id_number_encrypt']
    get_sms_body['data']['card_num_encrypt'] = element['data']['bank_code_encrypt']
    get_sms_body['data']['mobile_encrypt'] = element['data']['phone_number_encrypt']
    regiest_url = gc.GRANT_URL + gbiz_get_sms_verifycode_url
    header = {"Content-Type": "application/json"}
    ret = http.http_post(regiest_url, get_sms_body, header)
    return ret


def capital_regiest_with_sms_verifycode(channel, element, seq, code, item_no='121212', source_type='youxi_bill'):
    regiest_body = deepcopy(regiest_info)
    regiest_body['key'] = item_no + get_random_str()
    regiest_body['type'] = "ProtocolSign"
    regiest_body['data']['channel'] = channel
    regiest_body['data']['item_no'] = item_no
    regiest_body['data']['seq'] = seq
    regiest_body['data']['code'] = code
    regiest_body['data']['source_type'] = source_type
    regiest_body['data']['username_encrypt'] = element['data']['user_name_encrypt']
    regiest_body['data']['id_num_encrypt'] = element['data']['id_number_encrypt']
    regiest_body['data']['card_num_encrypt'] = element['data']['bank_code_encrypt']
    regiest_body['data']['mobile_encrypt'] = element['data']['phone_number_encrypt']
    regiest_url = gc.GRANT_URL + gbiz_capital_regiest_url
    header = {"Content-Type": "application/json"}
    ret = http.http_post(regiest_url, regiest_body, header)
    return ret


def preloan_confirm(asset_info, element):
    confirm_body = deepcopy(preloan_confirm_info)
    confirm_body['key'] = asset_info['data']['asset']['item_no'] + get_random_str()
    confirm_body['data']['item_no'] = asset_info['data']['asset']['item_no']
    confirm_body['data']['asset_extend']['amount'] = str(asset_info['data']['asset']['amount']) + "00"
    confirm_body['data']['asset_extend']['channel'] = asset_info['data']['asset']['loan_channel']
    confirm_body['data']['user_factor']['user_name_encrypt'] = element['data']['user_name_encrypt']
    confirm_body['data']['user_factor']['id_num_encrypt'] = element['data']['id_number_encrypt']
    confirm_body['data']['user_factor']['card_num_encrypt'] = element['data']['bank_code_encrypt']
    confirm_body['data']['user_factor']['mobile_encrypt'] = element['data']['phone_number_encrypt']
    regiest_url = gc.GRANT_URL + gbiz_preloan_confirm_url
    header = {"Content-Type": "application/json"}
    ret = http.http_post(regiest_url, confirm_body, header)
    return ret


# def postloan_confirm(asset_info, element):
#     confirm_body = deepcopy(postloan_confirm_info)
#     confirm_body['key'] = asset_info['data']['asset']['item_no'] + get_random_str()
#     confirm_body['data']['item_no'] = asset_info['data']['asset']['item_no']
#     confirm_body['data']['asset_extend']['amount'] = str(asset_info['data']['asset']['amount']) + "00"
#     confirm_body['data']['asset_extend']['channel'] = asset_info['data']['asset']['loan_channel']
#     confirm_body['data']['user_factor']['user_name_encrypt'] = element['data']['user_name_encrypt']
#     confirm_body['data']['user_factor']['id_num_encrypt'] = element['data']['id_number_encrypt']
#     confirm_body['data']['user_factor']['card_num_encrypt'] = element['data']['bank_code_encrypt']
#     confirm_body['data']['user_factor']['mobile_encrypt'] = element['data']['phone_number_encrypt']
#     regiest_url = gc.BASE_URL['china']['grant'] + gbiz_postloan_confirm_url
#     header = {"Content-Type": "application/json"}
#     return http.http_post(regiest_url, confirm_body, header)


def postloan_confirm(asset_info):
    confirm_body = deepcopy(postloan_confirm_info)
    confirm_body['key'] = asset_info['data']['asset']['item_no'] + get_random_str()
    confirm_body['data']['item_no'] = asset_info['data']['asset']['item_no']
    confirm_body['data']['asset_extend']['amount'] = str(asset_info['data']['asset']['amount']) + "00"
    confirm_body['data']['asset_extend']['channel'] = asset_info['data']['asset']['loan_channel']
    confirm_body['data']['user_factor']['user_name_encrypt'] = asset_info['data']['borrower']['name_encrypt']
    confirm_body['data']['user_factor']['user_name_encrypt'] = asset_info['data']['borrower']['idnum_encrypt']
    confirm_body['data']['user_factor']['user_name_encrypt'] = asset_info['data']['receive_card']['bank_code']
    confirm_body['data']['user_factor']['user_name_encrypt'] = asset_info['data']['borrower']['tel_encrypt']
    regiest_url = gc.GRANT_URL + gbiz_postloan_confirm_url
    header = {"Content-Type": "application/json"}
    ret = http.http_post(regiest_url, confirm_body, header)
    return ret


def userloan_confirm(asset_info, amount=None, action=None, sub_action=None):
    confirm_body = deepcopy(userloan_confirm_info)
    confirm_body['key'] = asset_info['data']['asset']['item_no'] + get_random_str()
    if amount:
        confirm_body['data']['asset']['amount'] = amount
    else:
        confirm_body['data']['asset']['amount'] = asset_info['data']['asset']['amount'] * 100
    confirm_body['data']['asset']['channel'] = asset_info['data']['asset']['loan_channel']
    confirm_body['data']['item_no'] = asset_info['data']['asset']['item_no']
    if action == "OTP_INTERACTION":
        confirm_body['data']['action'] = action
        confirm_body['data']['extra_data']["sub_action"] = sub_action
    regiest_url = gc.GRANT_URL + gbiz_userloan_confirm_url
    header = {"Content-Type": "application/json"}
    ret = http.http_post(regiest_url, confirm_body, header)
    return ret


def update_receive_card(asset_info, new_element, old_element):
    update_info = deepcopy(update_receive_card_info)
    update_info['key'] = asset_info['data']['asset']['item_no'] + get_random_str()
    update_info['from_system'] = asset_info['from_system']
    update_info['data']['project_num'] = asset_info['data']['asset']['item_no']
    update_info['data']['operater'] = asset_info['from_system']
    update_info['data']['card_num_encrypt'] = new_element['data']['bank_code_encrypt']
    update_info['data']['card_phone_encrypt'] = new_element['data']['phone_number_encrypt']
    update_info['data']['card_account_name_encrypt'] = old_element['data']['user_name_encrypt']
    update_url = gc.GRANT_URL + gbiz_update_card_url
    header = {"Content-Type": "application/json"}
    ret = http.http_post(update_url, update_info, header)
    return ret


# def lianlian_reverse_callback(asset_info, element, item_no):
#     callback_body = deepcopy(lianlian_callback_info)
#     callback_body['amount'] = str(asset_info['data']['asset']['amount']) + ".00"
#     idnum_encrypt = element['data']['id_number_encrypt']
#     bank_code_encrypt = element['data']['bank_code_encrypt']
#     # 使用SQL查询到loanId和memberId
#     sql1 = "select capital_account_user_key from gbiz%s.capital_account where capital_account_idnum_encrypt='%s' and " \
#            "capital_account_card_number_encrypt='%s' and capital_account_channel='lianlian';" % (env, idnum_encrypt,
#                                                                                                  bank_code_encrypt)
#     result = db.query(sql1)
#     memberId = result[0]["capital_account_user_key"]
#     sql2 = "select asset_loan_record_due_bill_no from gbiz%s.asset_loan_record where " \
#            "asset_loan_record_asset_item_no = '%s';" % (env, item_no)
#     result = db.query(sql2)
#     loanId = result[0]["asset_loan_record_due_bill_no"]
#     callback_body['loanId'] = loanId
#     callback_body['memberId'] = memberId
#     callback_url = gc.BASE_URL['china']['grant'] + lianlian_callback_url
#     header = {"Content-Type": "application/json"}
#     return http.http_post(callback_url, callback_body, header)


def reverse_callback(asset_info):
    reverse_body = deepcopy(reverse_callback_info)
    reverse_body['key'] = asset_info['data']['asset']['item_no'] + get_random_str()
    reverse_body['data'][0] = asset_info['data']['asset']['item_no']
    reverse_url = gc.GRANT_URL + reverse_callback_url
    header = {"Content-Type": "application/json"}
    return http.http_post(reverse_url, reverse_body, header)


def hamitianshan_zhongji_callback(asset_info):
    hmts_body = deepcopy(hamitianshan_callback_info)
    hmts_body['loanRequestNo'] = asset_info['data']['asset']['item_no']
    hmts_url = gc.GRANT_URL + hamitianshan_callback_url
    header = {"Content-Type": "application/json"}
    return http.http_post(url=hmts_url, req_data=hmts_body, headers=header)


def yixin_rongsheng_reverse_callback(asset_info):
    yxrs_body = deepcopy(yixin_rongsheng_callback_info)
    reverse_data = json.loads(yxrs_body['data'])
    reverse_data['outOrderNo'] = asset_info['data']['asset']['item_no']
    reverse_data['userId'] = "KN_" + asset_info['data']['borrower']['idnum_encrypt']
    yxrs_body['data'] = json.dumps(reverse_data, ensure_ascii=False)
    yxrs_url = gc.GRANT_URL + yxrs_reverse_callback
    header = {"Content-Type": "application/json"}
    return http.http_post(url=yxrs_url, req_data=yxrs_body, headers=header)

def daxinganling_zhongyi_grant_callback_success(asset_info, key=get_guid4()):
    '''
    还款计划起息时间：billingDate 是T+1（工作日+1，遇到节假日顺延，所以自动化在临近节假日时运行，可能时不正确的，回调也是一样的）
    TODO :回调的还款计划没有mock，需要后续修改
    '''
    dxal_body = deepcopy(daxinganling_zhongyi_callback_info)
    dxal_body['key'] = key
    callback_data = json.loads(dxal_body['data'])
    callback_data['contractNo'] = asset_info['data']['asset']['item_no']
    callback_data['merchantOrderNo'] = asset_info['data']['asset']['item_no']
    callback_data['accountingDate'] = get_date(fmt="%Y-%m-%d")
    callback_data['billingDate'] = get_date(day=1, fmt="%Y-%m-%d")
    callback_data['contractSignedDate'] = get_date(fmt="%Y-%m-%d")
    callback_data['loanDate'] = get_date(fmt="%Y-%m-%d")
    callback_data['loanBillingDate'] = get_date(day=1, fmt="%Y-%m-%d")
    dxal_body['data'] = json.dumps(callback_data, ensure_ascii=False)
    dxalzy_url = gc.GRANT_URL + dxal_zy_grant_callback
    header = {"Content-Type": "application/json"}
    return http.http_post(url=dxalzy_url, req_data=dxal_body, headers=header)

def daxinganling_zhongyi_grant_callback_fail(item_no):
    dxal_body = deepcopy(daxinganling_zhongyi_callback_info2)
    dxal_body['key'] = item_no
    callback_data = json.loads(dxal_body['data'])
    callback_data['merchantOrderNo'] = item_no
    dxal_body['data'] = json.dumps(callback_data, ensure_ascii=False)
    dxalzy_url = gc.GRANT_URL + dxal_zy_grant_callback
    header = {"Content-Type": "application/json"}
    return http.http_post(url=dxalzy_url, req_data=dxal_body, headers=header)

def data_cancel(item_no):
    req = {
        "from_system": "BIZ",
        "key": "AssetCancel_" + get_random_str(),
        "type": "AssetCancel",
        "data": {
            "item_no": item_no
        }
    }
    url = gc.GRANT_URL + data_cancel_url
    header = {"Content-Type": "application/json"}
    return http.http_post(url=url, req_data=req, headers=header)


def certificate_apply(item_no):
    req = {
        "from_system": "CRM",
        "key": "CertificateApply_%s" % get_random_str(),
        "type": "CertificateApply",
        "data": {
            "assetItemNoList": [item_no]
        }
    }
    url = gc.GRANT_URL + certificate_apply_url
    header = {"Content-Type": "application/json"}
    return http.http_post(url=url, req_data=req, headers=header)


def circuit_break_update(id, status, clear_cache=True):
    req = {
        "id": id,
        "name": None,
        "status": status,
        "clear_cache": clear_cache
    }
    url = gc.GRANT_URL + circuit_break_update_url
    header = {"Content-Type": "application/json"}
    return http.http_post(url=url, req_data=req, headers=header)


def huabei_audit_callback(asset_info, approvalcode):
    audit_body = deepcopy(huabei_audit_callback_info)
    audit_body_data = json.loads(audit_body['data'])
    audit_body_data['orderNum'] = asset_info['data']['asset']['item_no']
    audit_body_data['approvalCode'] = approvalcode
    audit_body['data'] = json.dumps(audit_body_data, ensure_ascii=False)
    audit_url = gc.GRANT_URL + huabei_audit_callback_url
    header = {"Content-Type": "application/json"}
    return http.http_post(audit_url, audit_body, header)


def huabei_grant_callback(asset_info, approvalcode):
    loan_body = deepcopy(huabei_grant_callback_info)
    loan_body_data = json.loads(loan_body['data'])
    loan_body_data['doLoanList'][0]['orderNum'] = asset_info['data']['asset']['item_no']
    loan_body_data['doLoanList'][0]['businessNum'] = asset_info['data']['asset']['item_no'] + get_random_str()
    loan_body_data['doLoanList'][0]['customerName'] = asset_info['data']['borrower']['name_encrypt']
    loan_body_data['doLoanList'][0]['certificateNum'] = asset_info['data']['borrower']['idnum_encrypt']
    loan_body_data['doLoanList'][0]['padUpAmt'] = asset_info['data']['asset']['amount']
    loan_body_data['doLoanList'][0]['loanDate'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    loan_body_data['approvalCode'] = approvalcode
    loan_body['data'] = json.dumps(loan_body_data, ensure_ascii=False)
    loan_url = gc.GRANT_URL + huabei_grant_callback_url
    header = {"Content-Type": "application/json"}
    return http.http_post(loan_url, loan_body, header)


def run_job(job_type, job_params):
    job_url = gc.GRANT_URL + "/job/run?jobType=%s" % job_type
    job_url = job_url + "&param=%s" % json.dumps(job_params)
    return http.http_get(job_url)


def individual_update(element, item_no, channel):
    # 更新活体照接口，其他地方暂时没用到
    ident_num_encrypt = element.get("data").get("borrower").get("idnum_encrypt")
    ident_name_encrypt = element.get("data").get("borrower").get("name_encrypt")
    header = {"Content-Type": "application/json"}
    update_url = gc.GRANT_URL + "/individual/update"
    update_body = {
        "type": "DsqIndividualInfoSync",
        "key": "key_" + item_no,
        "from_system": "DSQ",
        "data":
            {
                "apply_code": item_no,
                "ident_num_encrypt": ident_num_encrypt,
                "ident_addr": "山东省胶州市铺集镇吴家庄村4999号",
                "ident_name_encrypt": ident_name_encrypt,
                "loan_channel": channel,
                "attachments": [
                    {
                        "attachment_type": "29",
                        "attachment_url": "https://bizfiles-10000035.cos.ap-shanghai.myqcloud.com/photo/1611718980y0tzrRabjHA7m0ToVz9N3y.jpeg"
                    }
                ]
            }
    }
    return http.http_post(update_url, update_body, header)


def common_noloan_import(asset_info, irr_rongdan_noloan=False):
    noloan_item_no_lt = []
    loan_source_type = asset_info["data"]["asset"]["source_type"]
    noloan_source_type_lt = gbiz_common_config.source_type_map[loan_source_type]
    for noloan_source_type in noloan_source_type_lt:
        if "irr" in noloan_source_type and irr_rongdan_noloan == False:
            pass
        else:
            noloan_item_no, asset_info_rongdan_noloan = asset_import_noloan(asset_info, noloan_source_type)
            noloan_item_no_lt.append(noloan_item_no)
    return noloan_item_no_lt


def payment_callback(item_no, callback_type="success"):
    # 代付回调
    withdraw_record = get_withdraw_record_by_item_no(item_no)
    if callback_type == "success":
        status = 2
        channel_code = "1"
        channel_message = "处理成功"
        platform_code = "E20000"
        platform_message = "交易成功"
    elif callback_type == "fail":
        status = 3
        channel_code = "KN_REVERSE_ORDER"
        channel_message = ""
        platform_code = "E20001"
        platform_message = "FAILED"
    elif callback_type == "reverse":
        status = 3
        channel_code = "KN_REVERSE_ORDER"
        channel_message = "Refund"
        platform_code = "E20001"
        platform_message = "FAILED"
    body = {
        "from_system": "paysvr",
        "key": "baf38f1318c6715451783a0380fdb29311114",
        "type": "withdraw",
        "data": {
            "merchant_key": item_no,
            "trade_no": withdraw_record[-1]["withdraw_record_trade_no"],
            "channel_key": "qsq_cpcn_tr_quick",
            "status": status,
            "channel_code": channel_code,
            "channel_message": channel_message,
            "platform_code": platform_code,
            "platform_message": platform_message,
            "finished_at": get_date()
        }
    }
    header = {"Content-Type": "application/json"}
    url = gc.GRANT_URL + payment_callback_url
    return http.http_post(url, body, header)


def user_change_product_confirm(asset_info, action, status):
    '''
    宜信恒润目前使用的接口，BC调用确认产品线变更
    :return:
    '''
    confirm_body = deepcopy(change_product_confirm_info)
    # 因为系统key生成有重复，导致脚本一直不成功，所以此处key用资产编号来
    confirm_body['key'] = "Tconfirm" + asset_info['data']['asset']['item_no']
    confirm_body['data']['item_no'] = asset_info['data']['asset']['item_no']
    confirm_body['data']['action'] = action
    confirm_body['data']['channel'] = asset_info['data']['asset']['loan_channel']
    confirm_body['data']['status'] = status
    if asset_info['data']['asset']['loan_channel'] in ['yixin_hengrun', 'yixin_rongsheng']:
        confirm_body['data']['asset']['amount'] = asset_info['data']['asset_extend']['sub_asset']['amount']
        confirm_body['data']['asset']['period_type'] = asset_info['data']['asset_extend']['sub_asset']['period_type']
        confirm_body['data']['asset']['period_day'] = asset_info['data']['asset_extend']['sub_asset']['period_day']
        confirm_body['data']['asset']['period_count'] = asset_info['data']['asset_extend']['sub_asset']['period_count']
    else:
        confirm_body['data']['asset']['amount'] = asset_info['data']['asset']['amount']
        confirm_body['data']['asset']['period_type'] = asset_info['data']['asset']['period_type']
        confirm_body['data']['asset']['period_day'] = asset_info['data']['asset']['period_day']
        confirm_body['data']['asset']['period_count'] = asset_info['data']['asset']['period_count']
    confirm_url = gc.GRANT_URL + gbiz_userloan_confirm_url
    header = {"Content-Type": "application/json"}
    ret = http.http_post(confirm_url, confirm_body, header)
    return ret


if __name__ == "__main__":
    # gc.init_env("4", "china", "dev")
    # resp = circuit_break_update(8, "close")
    # print(resp)
    # run_job("DbMutipleThreadRunTaskJob", {"delay_minute": 0, "select_limit": 100, "morethan_hour": 24, "priority": 1})
    # individual_update(element='',item_no='item_no_1631503090',channel='siping_jiliang')
    run_job("DingfengFileBatchUploadJob", {
        "loan_channel_list": [
            "yilian_dingfeng"
        ],
        "file_type_list": [
            "APPLY_INFO",
            "LOAN_DETAIL",
            "IMAGE"
        ],
        "upload_date": None,
        "start_date": None,
        "end_date": None
    })
