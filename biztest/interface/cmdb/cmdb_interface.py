from copy import deepcopy

import requests

from biztest.config.cmdb.cmdb_interface_params_config import rate_route_v6_info, rate_loan_calculate_v6_info, \
    rate_repay_calculate_v6_info
from biztest.config.cmdb.cmdb_interface_url_config import *
from biztest.function.gbiz.gbiz_db_function import get_asset_extend_by_item_no, get_asset_info_by_item_no, \
    get_asset_cmdb_product_number
from biztest.util.tools.tools import get_date, get_guid
from biztest.util.http.http_util import Http as http
import common.global_const as gc


def monitor_check(timeout=60):
    result = None
    for i in range(timeout):
        url = gc.CMDB_URL + cmdb_monitor_check_url
        try:
            headers = {"Content-Type": "application/json", "Connection": "close"}
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                result = True
                break
            else:
                result = False
        except Exception as e:
            print(e)
            result = False
    return result


def cmdb_rate_route_v6(from_system, source_type, period_count, amount, loan_channel=None, risk_level=1):
    rate_route_body = deepcopy(rate_route_v6_info)
    rate_route_body['key'] = get_guid()
    rate_route_body['data']['scope'] = source_type
    rate_route_body['data']['principal'] = str(amount) + "00"
    rate_route_body['data']['condition']['risk_level'] = risk_level
    rate_route_body['data']['condition']['source_type'] = source_type
    rate_route_body['data']['condition']['from_system'] = from_system
    if period_count == 1:
        rate_route_body['data']['period_count'] = 1
        rate_route_body['data']['period_term'] = 30
        rate_route_body['data']['period_type'] = 'day'
    else:
        rate_route_body['data']['period_count'] = period_count
        rate_route_body['data']['period_term'] = 1
        rate_route_body['data']['period_type'] = 'month'
    if loan_channel:
        rate_route_body['data']['loan_channel'] = loan_channel
    cmdb_url = gc.CMDB_URL + rate_route_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, rate_route_body, header)
    return resp


def cmdb_rate_loan_calculate_v6(asset_info):
    rate_loan_calculate_body = deepcopy(rate_loan_calculate_v6_info)
    rate_loan_calculate_body['key'] = get_guid()
    rate_loan_calculate_body['data']['itemNo'] = asset_info['data']['asset']['item_no']
    rate_loan_calculate_body['data']['sign_date'] = get_date(fmt="%Y-%m-%d")
    rate_loan_calculate_body['data']['apply_amount'] = str(int(asset_info['data']['asset']['amount'])) + '00'
    rate_loan_calculate_body['data']['period_count'] = asset_info['data']['asset']['period_count']
    rate_loan_calculate_body['data']['period_type'] = asset_info['data']['asset']['period_type']
    rate_loan_calculate_body['data']['loan_channel'] = asset_info['data']['asset']['loan_channel']
    if asset_info['data']['asset']['period_count'] == 1:
        rate_loan_calculate_body['data']['period_term'] = 30
    else:
        rate_loan_calculate_body['data']['period_term'] = 1
    if rate_loan_calculate_body['data']['loan_channel'] in ['lanzhou_haoyue', 'zhongke_lanzhou']:
        rate_loan_calculate_body['data']['product_number'] = str(
            get_asset_cmdb_product_number(asset_info['data']['asset']['item_no']))
    else:
        rate_loan_calculate_body['data']['product_number'] = asset_info['data']['asset']['cmdb_product_number']
    rate_loan_calculate_body['data']['scope'] = asset_info['data']['asset']['source_type']
    cmdb_url = gc.CMDB_URL + rate_loan_calculate_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, rate_loan_calculate_body, header)
    return resp


def cmdb_rate_repay_calculate_v6(asset_info):
    rate_repay_calculate_body = deepcopy(rate_repay_calculate_v6_info)
    rate_repay_calculate_body['key'] = get_guid()
    rate_repay_calculate_body['data']['itemNo'] = asset_info['data']['asset']['item_no']
    rate_repay_calculate_body['data']['sign_date'] = get_asset_info_by_item_no(asset_info['data']['asset']['item_no'])[0]["asset_actual_grant_at"][0:10]
    rate_repay_calculate_body['data']['apply_amount'] = str(asset_info['data']['asset']['amount']) + '00'
    rate_repay_calculate_body['data']['period_count'] = asset_info['data']['asset']['period_count']
    rate_repay_calculate_body['data']['period_type'] = asset_info['data']['asset']['period_type']
    rate_repay_calculate_body['data']['loan_channel'] = asset_info['data']['asset']['loan_channel']
    if asset_info['data']['asset']['period_count'] == 1:
        rate_repay_calculate_body['data']['period_term'] = 30
    else:
        rate_repay_calculate_body['data']['period_term'] = 1
    if rate_repay_calculate_body['data']['loan_channel'] in ['lanzhou_haoyue', 'zhongke_lanzhou']:
        rate_repay_calculate_body['data']['product_number'] = str(
            get_asset_cmdb_product_number(asset_info['data']['asset']['item_no']))
    else:
        rate_repay_calculate_body['data']['product_number'] = asset_info['data']['asset']['cmdb_product_number']
    rate_repay_calculate_body['data']['scope'] = asset_info['data']['asset']['source_type']
    cmdb_url = gc.CMDB_URL + rate_repay_calculate_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, rate_repay_calculate_body, header)
    return resp


def cmdb_rate_repay_calculate_v6_by_item_no(item_no):
    asset_info = get_asset_info_by_item_no(item_no)
    asset_extend = get_asset_extend_by_item_no(item_no)
    req = {
        'data': {
            'asset': {
                'item_no': item_no,
                'loan_at': asset_info[0]['asset_grant_at'],
                'amount': int(asset_info[0]['asset_principal_amount'] / 100),
                'period_count': asset_info[0]['asset_period_count'],
                'period_day': '1',
                'period_type': 'month',
                'loan_channel': asset_info[0]['asset_loan_channel'],
                'source_type': asset_extend[0]['asset_extend_ref_order_type'],
                'cmdb_product_number': asset_info[0]['asset_cmdb_product_number']
            }
        }
    }
    resp = cmdb_rate_repay_calculate_v6(req)
    return resp


def cmdb_capital_query_v6(source_type):
    req = {
        "from_system": "GBIZ",
        "key": get_guid(),
        "type": "CapitalQuery",
        "data": {
            "scope": source_type
        }
    }
    cmdb_url = gc.CMDB_URL + cmdb_capital_query_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, req, header)
    return resp


def cmdb_rate_loan_calculate(rate_number, principal, period_count, loan_channel):
    req = {
        "from_system": "GBIZ",
        "key": get_guid(),
        "type": "LoanCalculateRepayPlan",
        "data": {
            "itemNo": "hm20200319151848915",
            "sign_date": get_date(),
            "apply_amount": principal,
            "period_count": period_count,
            "period_type": "month",
            "period_term": 1,
            "product_number": rate_number,
            "interest_rate": None,
            "scope": "apr36",
            "loan_channel": loan_channel
        }
    }
    cmdb_url = gc.CMDB_URL + rate_loan_calculate_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, req, header)
    return resp


def cmdb_rate_adjust(rate_number, principal, period_count, adjust_data_lt):
    req = {
        "from_system": "GBIZ",
        "key": get_guid(),
        "type": "RateAdjust",
        "data": {
            "sign_date": get_date(),
            "product_number": rate_number,
            "period_count": period_count,
            "period_type": "month",
            "period_term": 1,
            "principal_amount": principal,
            "capital_result": adjust_data_lt
        }
    }
    cmdb_url = gc.CMDB_URL + cmdb_rate_adjust_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, req, header)
    print(req)
    print(resp)
    return resp


def cmdb_standard_calc_v6(principal_amount, period_count, period_type, period_term, interest_rate, repay_type,
                          interest_year_type="360per_year", month_clear_day="D+0", clear_day="D+0",
                          sign_date=get_date(fmt="%Y-%m-%d"), repay_date_formula="calDateThenSameDay"):
    body = {
        "type": "CalculateStandardRepayPlan",
        "key": "calculate_${key}",
        "from_system": "bc",
        "data": {
            "sign_date": sign_date,
            "principal_amount": principal_amount,
            "period_count": period_count,
            "period_type": period_type,
            "period_term": period_term,
            "interest_rate": interest_rate,
            "repay_type": repay_type,
            "interest_year_type": interest_year_type,
            "month_clear_day": month_clear_day,
            "clear_day": clear_day,
            "repay_date_formula": repay_date_formula,
        }
    }
    cmdb_url = gc.CMDB_URL + cmdb_standard_calc_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, body, header)
    return resp


if __name__ == "__main__":
    cmdb_rate_adjust("trmy_12_1m_20200826", 800000, 12, "tongrongmiyang")
