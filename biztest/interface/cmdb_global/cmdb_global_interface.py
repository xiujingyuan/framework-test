from copy import deepcopy

import requests

from biztest.config.cmdb.cmdb_interface_params_config import rate_loan_calculate_v6_info, rate_route_v6_info, \
    rate_repay_calculate_v6_info
from biztest.config.cmdb.cmdb_interface_url_config import rate_route_v6_url, cmdb_monitor_check_url, \
    rate_loan_calculate_v6_url, rate_repay_calculate_v6_url, cmdb_capital_query_v6_url
from biztest.util.http.http_util import Http as http
from biztest.util.tools.tools import get_guid, get_date
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


def cmdb_rate_route_v6(amount, source_type, from_system_name, risk_level, period_count):
    rate_route_body = deepcopy(rate_route_v6_info)
    rate_route_body['key'] = get_guid()
    rate_route_body['data']['scope'] = source_type
    rate_route_body['data']['principal'] = str(amount)
    rate_route_body['data']['condition']['risk_level'] = risk_level
    rate_route_body['data']['condition']['source_type'] = source_type
    rate_route_body['data']['condition']['from_system_name'] = from_system_name
    if period_count == 1:
        rate_route_body['data']['period_count'] = 1
        rate_route_body['data']['period_term'] = 30
        rate_route_body['data']['period_type'] = 'day'
    else:
        rate_route_body['data']['period_count'] = period_count
        rate_route_body['data']['period_term'] = 1
        rate_route_body['data']['period_type'] = 'month'
    cmdb_url = gc.CMDB_URL + rate_route_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, rate_route_body, header)
    return resp


def cmdb_rate_loan_calculate_v6(asset_info):
    rate_loan_calculate_body = deepcopy(rate_loan_calculate_v6_info)
    rate_loan_calculate_body['key'] = get_guid()
    rate_loan_calculate_body['data']['itemNo'] = asset_info['data']['asset']['item_no']
    rate_loan_calculate_body['data']['sign_date'] = get_date(fmt="%Y-%m-%d")
    rate_loan_calculate_body['data']['apply_amount'] = str(asset_info['data']['asset']['amount'])
    rate_loan_calculate_body['data']['period_count'] = asset_info['data']['asset']['period_count']
    rate_loan_calculate_body['data']['period_type'] = asset_info['data']['asset']['period_type']
    if asset_info['data']['asset']['period_count'] == 1:
        rate_loan_calculate_body['data']['period_term'] = 30
    else:
        rate_loan_calculate_body['data']['period_term'] = 1
    rate_loan_calculate_body['data']['product_number'] = asset_info['data']['asset']['cmdb_product_number']
    rate_loan_calculate_body['data']['scope'] = asset_info['data']['asset']['source_type']
    rate_loan_calculate_body['data']['loan_channel'] = asset_info['data']['asset']['loan_channel']
    cmdb_url = gc.CMDB_URL + rate_loan_calculate_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, rate_loan_calculate_body, header)
    return resp


def cmdb_rate_repay_calculate_v6(asset_info):
    rate_repay_calculate_body = deepcopy(rate_repay_calculate_v6_info)
    rate_repay_calculate_body['key'] = get_guid()
    rate_repay_calculate_body['data']['itemNo'] = asset_info['data']['asset']['item_no']
    rate_repay_calculate_body['data']['sign_date'] = asset_info['data']['asset']['loan_at'][0:10]
    rate_repay_calculate_body['data']['apply_amount'] = str(asset_info['data']['asset']['amount'])
    rate_repay_calculate_body['data']['period_count'] = asset_info['data']['asset']['period_count']
    rate_repay_calculate_body['data']['period_type'] = asset_info['data']['asset']['period_type']
    rate_repay_calculate_body['data']['period_term'] = asset_info['data']['asset']['period_day']
    rate_repay_calculate_body['data']['product_number'] = asset_info['data']['asset']['cmdb_product_number']
    rate_repay_calculate_body['data']['scope'] = asset_info['data']['asset']['source_type']
    rate_repay_calculate_body['data']['loan_channel'] = asset_info['data']['asset']['loan_channel']
    cmdb_url = gc.CMDB_URL + rate_repay_calculate_v6_url
    header = {"Content-Type": "application/json"}
    resp = http.http_post(cmdb_url, rate_repay_calculate_body, header)
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


if __name__ == "__main__":
    cmdb_rate_route_v6(300000, "game_bill", "贷上钱", '4', 3)
