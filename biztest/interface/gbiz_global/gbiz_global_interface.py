from copy import deepcopy

from biztest.config.global_gbiz.global_gbiz_interface_params_config import *
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_import_data_by_item_no, \
    get_withdraw_order_by_item_no
from biztest.util.http.http_util import Http
from biztest.function.global_gbiz.gbiz_global_db_function import get_withdraw_record_by_item_no, \
    insert_router_load_record
from biztest.util.asserts.assert_util import Assert
import common.global_const as gc

http = Http()


def asset_route(count, days, types, amount, from_system, from_app, source_type, element, key=None, fees=None, late_num=None):
    asset_info = deepcopy(route_locate_info)
    if key:
        asset_info['key'] = key
    else:
        asset_info['key'] = get_guid()
    asset_info['from_system'] = from_system
    # asset_info['data']['asset']['from_system'] = from_system
    asset_info['data']['asset']['from_app'] = from_app
    asset_info['data']['asset']['period_type'] = types
    asset_info['data']['asset']['period_count'] = count
    asset_info['data']['asset']['period_day'] = days
    asset_info['data']['asset']['amount'] = amount
    asset_info['data']['asset']['source_type'] = source_type
    asset_info['data']['asset']['rate_info'] = {
        "late_num": late_num,
        "fees": fees if fees is not None else {}
    } if late_num is not None else None

    asset_info['data']['borrower']['id_num'] = element["data"]["id_number_encrypt"]
    asset_info['data']['borrower']['borrower_uuid'] = element["data"]["id_number"]
    asset_info['data']['borrower']['borrower_card_uuid'] = element["data"]["card_num"]
    asset_info['data']['borrower']['mobile'] = element["data"]["mobile_encrypt"]
    asset_info['data']['borrower']['individual_uuid'] = element["data"]["id_number"]

    asset_route_url = gc.GROUTER_URL + route_locate_url
    resp = Http.http_post(asset_route_url, asset_info)

    Assert.assert_equal(0, resp['code'], "路由接口异常")
    return resp['data']['route_channel']


def asset_import(channel, count, days, types, amount, from_system, from_app, source_type, element, withdraw_type='',
                 item_no='', route_uuid='', insert_router_record=True, rlue_code=None, fees=None, late_num=None):
    if item_no:
        pass
    else:
        item_no = get_item_no()
    asset_info = deepcopy(asset_import_info)
    asset_info['key'] = item_no + channel
    asset_info['from_system'] = from_system
    asset_info['data']['asset']['item_no'] = item_no
    asset_info['data']['asset']['period_type'] = types
    asset_info['data']['asset']['period_count'] = count
    asset_info['data']['asset']['period_day'] = days
    asset_info['data']['asset']['amount'] = amount
    asset_info['data']['asset']['loan_at'] = get_date(timezone=get_tz())
    asset_info['data']['asset']['loan_channel'] = channel
    asset_info['data']['asset']['source_type'] = source_type
    asset_info['data']['asset']['from_app'] = from_app
    asset_info['data']['asset']['from_system'] = from_system
    asset_info['data']['asset']['rate_info'] = {
        "late_num": late_num,
        "fees": fees if fees is not None else {}
    } if late_num is not None else None
    if '_bill' in source_type:
        asset_info['data']['asset']['source_number'] = item_no + "_noloan"
    else:
        asset_info['data']['asset']['source_number'] = ""
    asset_info['data']['borrower']['id_num'] = element["data"]["id_number_encrypt"]
    asset_info['data']['borrower']['borrower_uuid'] = element["data"]["id_number"] + "0"
    asset_info['data']['borrower']['borrower_card_uuid'] = element["data"]["card_num"]
    asset_info['data']['borrower']['mobile'] = element["data"]["mobile_encrypt"]
    asset_info['data']['borrower']['individual_uuid'] = element["data"]["id_number"] + "1"

    asset_info['data']['borrower']['withdraw_type'] = withdraw_type

    if route_uuid:
        asset_info['data']['route_uuid'] = route_uuid
    if gc.COUNTRY == "thailand":
        asset_info['data']['asset']['owner'] = "tailand"
    if insert_router_record:
        if rlue_code:
            pass
        else:
            rlue_code = channel + '_0'
        # 进件前，在路由表插入一条记录
        keys = {"router_load_record_key": item_no,
                "router_load_record_rule_code": rlue_code,
                "router_load_record_principal_amount": amount,
                "router_load_record_status": "routed",
                "router_load_record_channel": channel,
                "router_load_record_sub_type": "multiple",
                "router_load_record_period_count": count,
                "router_load_record_period_type": types,
                "router_load_record_period_days": days,
                "router_load_record_route_day": get_date(fmt="%Y-%m-%d"),
                "router_load_record_idnum": element['data']['id_number_encrypt'],
                "router_load_record_from_system": asset_info['from_system'],
                }
        insert_router_load_record(**keys)

    asset_import_url = gc.GRANT_URL + gbiz_asset_import_url
    resp = Http.http_post(asset_import_url, asset_info)

    if resp['code'] == 0:
        asset_info = get_asset_import_data_by_item_no(item_no)

    return item_no, asset_info


def asset_import_noloan(asset_info):
    asset_info_noloan = deepcopy(asset_info)

    item_no_noloan = asset_info['data']['asset']['source_number']
    asset_info_noloan['key'] = asset_info['data']['asset']['source_number']
    asset_info_noloan['data']['asset']['item_no'] = asset_info['data']['asset']['source_number']
    asset_info_noloan['data']['asset']['name'] = asset_info['data']['asset']['source_number']
    asset_info_noloan['data']['asset']['source_number'] = asset_info['data']['asset']['item_no']
    asset_info_noloan['data']['asset']['amount'] = asset_info['data']['asset']['amount'] / 10
    asset_info_noloan['data']['asset']['source_type'] = asset_info['data']['asset']['source_type'] + "_split"
    asset_info_noloan['data']['asset']['loan_channel'] = 'noloan'
    if "rate_info" in asset_info_noloan['data']['asset'].keys():
        asset_info_noloan['data']['asset']['rate_info']['fees'] = {}
    if item_no_noloan == '':
        return item_no_noloan, asset_info_noloan
    asset_import_url = gc.GRANT_URL + gbiz_asset_import_url
    header = {"Content-Type": "application/json"}
    resp = Http.http_post(asset_import_url, asset_info_noloan, header)
    if resp['code'] == 0:
        asset_info_noloan = get_asset_import_data_by_item_no(item_no_noloan)
    return asset_info_noloan['data']['asset']['item_no'], asset_info_noloan


def update_receive_card(asset_info, time_out, withdraw_type=""):
    update_info = deepcopy(update_receive_card_info)
    update_info['key'] = asset_info['data']['asset']['item_no'] + get_random_str()
    update_info['from_system'] = asset_info['from_system']
    update_info['data']['item_no'] = asset_info['data']['asset']['item_no']
    update_info['data']['id_num'] = asset_info['data']['borrower']['id_num']
    update_info['data']['card_uuid'] = get_random_str()
    update_info['data']['time_out'] = time_out
    update_info['data']['withdraw_type'] = withdraw_type
    update_url = gc.GRANT_URL + gbiz_update_card_url
    header = {"Content-Type": "application/json"}
    return http.http_post(update_url, update_info, header)


def grant_at_update(asset_info, new_grant_at):
    update_info = deepcopy(grant_at_update_info)
    order_info = get_withdraw_order_by_item_no(asset_info['data']['asset']['item_no'] + 'w')[0]
    record_info = get_withdraw_record_by_item_no(asset_info['data']['asset']['item_no'] + 'w')[0]
    update_info['key'] = asset_info['data']['asset']['item_no'] + get_random_str()
    update_info['data']['item_no'] = asset_info['data']['asset']['item_no']
    update_info['data']['grant_at'] = new_grant_at
    update_info['data']['channel_key'] = record_info["withdraw_record_channel_key"]
    update_info['data']['loan_channel'] = order_info["withdraw_order_asset_loan_channel"]
    update_url = gc.GRANT_URL + grant_at_update_url
    header = {"Content-Type": "application/json"}
    return http.http_post(update_url, update_info, header)


def payment_callback(asset_info, status):
    callback_body = deepcopy(payment_callback_info)
    record_info = get_withdraw_record_by_item_no(asset_info['data']['asset']['item_no'] + 'w')
    callback_body['key'] = asset_info['data']['asset']['item_no'] + get_random_str()
    callback_body['data']['amount'] = asset_info['data']['asset']['amount']
    callback_body['data']['status'] = status
    callback_body['data']['channel_key'] = record_info[-1]["withdraw_record_channel_key"]
    callback_body['data']['trade_no'] = record_info[-1]["withdraw_record_trade_no"]
    callback_body['data']['finished_at'] = get_date(timezone=get_tz())
    callback_body['data']['merchant_key'] = asset_info['data']['asset']['item_no'] + "w"
    callback_url = gc.GRANT_URL + payment_callback_url
    header = {"Content-Type": "application/json"}
    return http.http_post(callback_url, callback_body, header)


def asset_cancel(item_no):
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


def run_job_by_api(job_type, job_params):
    # job_url = gc.GRANT_URL + "/job/run"
    job_url = "https://biz-gateway-proxy.starklotus.com/tha_grant1/job/run"
    params = {"jobType": job_type,
              "param": json.dumps(job_params)}
    return Http.http_get(job_url, params=params)


def run_countRouteTotalAmount_by_api():
    job_type = "countRouteTotalAmount"
    job_params = {}
    run_job_by_api(job_type, job_params)


def run_AccountBalanceToCapitalPlanJob_by_api():
    job_type = "AccountBalanceToCapitalPlanJob"
    job_params = {
        "fromSystem": "tha-grant",
        "channelList": [
            {
                "channel": "picocp_ams2",
                "rule_code": "picocp_ams2_balance",
                "add_grant_success_amount": False,
                "subtract_amount": 0
            },
            {
                "channel": "picocp_ams2",
                "rule_code": "picocp_ams2_0",
                "add_grant_success_amount": True,
                "subtract_amount": 10000000
            }
        ]
    }
    # subtract_warn_amount 的含义： 是否减掉支付返回的warnAmount, 默认为：true
    run_job_by_api(job_type, job_params)


def run_RiskGrantPlanSyncJob_by_api():
    job_type = "RiskGrantPlanSyncJob"
    job_params = {
        "desc": "泰国",
        "sync_duration": 8,
        "money_unit_length": 100,
        "warning_duration": 3,
        "warning_emails": [
            "yibingwang@kuainiugroup.com",
            "sidneywang@kuainiugroup.com",
            "fengxiaojun@kuainiugroup.com",
            "nickyuan@kuainiugroup.com",
            "sophieyu@kuainiugroup.com",
            "roxytang@kuainiugroup.com"
        ],
        "rule_alloc_type": "fix",
        "rule_codes": {
            "0": [
                {
                    "rule_code": "pico_bangkok_1",
                    "alloc_rate": 1
                },
                {
                    "rule_code": "picocp_ams1_0",
                    "alloc_rate": 2
                },
                {
                    "rule_code": "picoqr_ams1_bangkok_0",
                    "alloc_amount": 200000000
                },
                {
                    "rule_code": "picoqr_ams1_korat_0",
                    "alloc_amount": 80000000
                },
                {
                    "rule_code": "picoqr_ams1_saraburi_0",
                    "alloc_amount": 20000000
                }
            ]
        }
    }
    run_job_by_api(job_type, job_params)


def run_manualTaskAutoProcessJob_by_api():
    job_type = "manualTaskAutoProcessJob"
    job_params = {
        "taskTypeList": [
            "ChangeCapital",
            "AssetVoid",
            "CapitalAssetReverse",
            "LoanConfirmQuery",
            "PaymentWithdrawQuery"
        ]
    }
    run_job_by_api(job_type, job_params)

def run_bizcircuitbreakJob_by_api(circuit_break_name):
    job_type = "BizCircuitBreakJob"
    job_params = {"breakerNameList": [circuit_break_name]}
    run_job_by_api(job_type, job_params)

if __name__ == "__main__":
    # run_AccountBalanceToCapitalPlanJob_by_api()
    # run_RiskGrantPlanSyncJob_by_api()
    # run_countRouteTotalAmount_by_api()
    run_manualTaskAutoProcessJob_by_api()
    pass
