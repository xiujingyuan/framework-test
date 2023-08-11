import importlib
from functools import reduce

from flask import request, jsonify
from app.gbiz_tool import gbiz_tool
from biztest.case.gbiz.gbiz_loan_tool import gbiz_loan_tool, gbiz_route_tool
from biztest.case.global_gbiz.global_gbiz_loan_tool import global_gbiz_loan_tool, global_gbiz_route_tool
from biztest.util.log.log_util import LogUtil
from biztest.function.cmdb.cmdb_common_function import get_total_amount, get_comprehensive_fee
from biztest.function.cmdb.cmdb_db_function import get_root_rate_config_info_by_channel
import decimal
import common.global_const as gc
from biztest.util.tools.tools import get_date
import datetime


@gbiz_tool.route('/')
def hello_world():
    LogUtil.log_info("/hello_world")
    return 'hello world'


@gbiz_tool.route('/gbiz-loan-to-success', methods=['POST'])
def gbiz_loan_to_success():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    env = request_params.get("env", "")
    item_no = request_params.get("item_no", "")
    country = request_params.get("country", "")
    environment = request_params.get("environment", "test")
    status = request_params.get("status", "")

    if env == "" or item_no == "":
        code, message = 1, "参数不能为空"
    elif country == "" or country == "china":
        code, message = gbiz_loan_tool("china", env, environment, item_no)
    else:
        code, message = global_gbiz_loan_tool(country, env, environment, item_no, status)
    resp = {
        "code": code,
        "message": message
    }
    LogUtil.log_info("response: %s" % resp)
    return jsonify(resp)


@gbiz_tool.route('/gbiz-route-success', methods=['POST'])
def gbiz_route_success():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    env = request_params.get("env", "")
    country = request_params.get("country", "")
    channel = request_params.get("channel", "")
    environment = request_params.get("environment", "test")

    if env == "":
        code, message = 1, "env不能为空"
    elif country == "" or country == "china":
        code, message = gbiz_route_tool("china", env, environment, channel)
    else:
        code, message = global_gbiz_route_tool(country, env, environment, channel)
    resp = {
        "code": code,
        "message": message
    }
    LogUtil.log_info("response: %s" %  resp)
    return jsonify(resp)


@gbiz_tool.route('/gbiz-calc-noloan-amount', methods=['POST'])
def gbiz_calc_noloan_amount():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    env = request_params.get("env", "1")
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "test")
    channel = request_params.get("channel", "")
    principal = request_params.get("principal", "")
    period_count = request_params.get("period_count", "")
    period_type = request_params.get("period_type", "month")
    period_term = request_params.get("period_term", 1)
    grant_date = request_params.get("grant_date", "")
    if grant_date == "":
        grant_date = get_date(fmt="%Y-%m-%d")

    gc.init_env(env, country, environment)

    resp = {
        "code": 1,
        "message": "",
        "data": {}
    }
    if principal == "" or period_count == "":
        resp["code"] = 1
        resp["message"] = "参数不能为空"
        return jsonify(resp)

    rate_info = get_root_rate_config_info_by_channel(channel)
    if len(rate_info) == 0:
        resp["code"] = 1
        resp["message"] = "不支持的资方，未找到合适的费率信息"
        return jsonify(resp)

    calculate_type = rate_info[0]['rate_config_calculate_type']
    rate_value = decimal.Decimal(rate_info[0]['rate_config_value']) / 100
    round_type = rate_info[0]['rate_config_carry_mode']
    year_days = rate_info[0]['rate_interest_year_days']
    month_clear_day = rate_info[0]['rate_month_clear_day']
    clear_day = rate_info[0]['rate_clear_day']
    comprehensive_fee = get_comprehensive_fee(principal, period_count, rate_value, calculate_type, round_type, year_days, month_clear_day, clear_day, datetime.datetime.strptime(grant_date, "%Y-%m-%d"))

    apr36 = get_total_amount("apr", principal, period_count)
    irr36 = get_total_amount("irr", principal, period_count)
    apr36_by_day = get_total_amount("aprByDay", principal, period_count, year_days=365, month_clear_day=month_clear_day, clear_day=clear_day, sign_date=grant_date)
    if channel in ['siping_jiliang', 'mozhi_jinmeixin', 'yilian_dingfeng', 'jinmeixin_daqin']:
        apr_rongdan_amount = apr36_by_day - comprehensive_fee
        irr_rongdan_amount = 0
        irr_quanyi_amount = apr36_by_day - comprehensive_fee
    else:
        apr_rongdan_amount = apr36 - comprehensive_fee
        irr_rongdan_amount = irr36 - comprehensive_fee
        irr_quanyi_amount = apr36 - irr36
    resp["code"] = 0
    resp["message"] = "OK"
    resp["data"]["apr融担小单金额"] = int(apr_rongdan_amount)
    resp["data"]["irr融担小单金额"] = int(irr_rongdan_amount)
    resp["data"]["irr权益小单金额"] = int(irr_quanyi_amount)
    resp["data"]["大单综合息费"] = int(comprehensive_fee)
    resp["data"]["APR36（大单+小单总额）"] = int(apr36)
    resp["data"]["APR36_按天（大单+小单总额）"] = int(apr36_by_day)
    resp["data"]["IRR36（大单+irr融担小单）"] = int(irr36)

    return jsonify(resp)


@gbiz_tool.route('/capital-manual-grant', methods=['POST'])
def manual_grant_capital():
    ret = {
        "code": 0,
        "message": "success",
        "data": None
    }
    request_params = request.json
    env = request_params.get("env", "1")
    channel = request_params.get("channel", "")
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "env")
    amount = request_params.get("amount", 6000)
    count = request_params.get("count", 12)
    app = request_params.get("app", "香蕉")
    back_code = request_params.get("bank_code", "CCB")
    source_type = request_params.get("source_type", "apr36")
    extend = request_params.get("extend", {})
    gc.init_env(env, country, environment)
    item_no = ''
    meta_class = importlib.import_module('biztest.case.gbiz.test_{0}'.format(channel))
    if channel == 'lanzhou_haoyue_zk3':
        obj = getattr(meta_class, 'TestLanzhouHaoyue')()
    else:
        obj = getattr(meta_class, 'Test' + ''.join(tuple(x.title() for x in channel.split("_"))))()
    obj.init()
    item_no = obj.manual_grant_capital(channel, count, amount, app, source_type, back_code, extend)
    ret['data'] = item_no
    ret['message'] = 'success' if 'item_no' in item_no else 1
    ret['code'] = 0 if 'item_no' in item_no else 1
    return jsonify(ret)


@gbiz_tool.route('/register-after', methods=['POST'])
def register_after():
    ret = {
        "code": 0,
        "message": "success",
        "data": None
    }
    request_params = request.json
    env = request_params.get("env", "1")
    channel = request_params.get("channel", "")
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "env")
    account_action = request_params.get("account_action")
    account_code = request_params.get("account_code")
    item_no = request_params.get("item_no")
    four_element = request_params.get("four_element")
    sms_seq = request_params.get("sms_seq")
    gc.init_env(env, country, environment)
    meta_class = importlib.import_module('biztest.case.gbiz.test_{0}'.format(channel))
    obj = getattr(meta_class, 'Test' + ''.join(tuple(x.title() for x in channel.split("_"))))()
    obj.init()
    ret['data'] = item_no
    try:
        if account_action is not None:
            obj.register(item_no, four_element,  action_type=account_action, smscode=account_code, sms_seq=sms_seq)
        else:
            obj.register(item_no, four_element)
    except Exception as e:
        print(e)
        pass
    ret['message'] = 'success'
    ret['code'] = 0
    return jsonify(ret)
