#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.function.global_gbiz.gbiz_global_db_function import update_task_by_item_no_task_type, \
    get_asset_import_data_by_item_no, insert_router_load_record
from biztest.util.task.task import TaskGlobal
import biztest.config.global_gbiz.global_gbiz_common_config as global_gbiz_common_config
from biztest.function.global_gbiz.gbiz_global_db_function import update_router_weight, update_router_capital_rule, \
    update_router_capital_plan, delete_router_capital_rule, delete_router_capital_plan, delete_router_weight, \
    delete_router_load_total, insert_router_capital_rule, insert_router_capital_plan, insert_router_load_total, \
    insert_router_weight
from biztest.util.tools.tools import *
import common.global_const as gc


def run_terminated_task(item_no, task_type, expect_code=0):
    update_task_by_item_no_task_type(item_no, task_type, task_status="open")
    task = TaskGlobal()
    task.run_task(item_no, task_type, excepts={"code": expect_code})


def init_capital_plan(country, channel=None):
    if channel:
        # 只初始化指定资方的资金计划
        capital_plan = []
        channel_list = \
            [channel_config.get('channel') for channel_config in global_gbiz_common_config.capital_plan[country]]
        if channel not in channel_list:
            raise Exception("资方%s错误，不在配置中，配置资方：%s" % (channel, str(channel_list)))
        for channel_config in global_gbiz_common_config.capital_plan[country]:
            if channel_config.get('channel') == channel:
                capital_plan.append(channel_config)
                break
        update_capital_plan(capital_plan)
    else:
        # 删除所有资金计划，重新初始化
        delete_router_capital_rule()
        delete_router_capital_plan()
        delete_router_weight()
        update_capital_plan(global_gbiz_common_config.capital_plan[country])


def update_capital_plan(capital_plan_lt):
    for rule in capital_plan_lt:
        capital_rule = {
            "rule_code": rule.get("rule_code"),
            "rule_desc": rule.get("rule_desc"),
            "rule_family": rule.get("rule_family", rule.get("channel")),
            "rule_content": rule.get("rule_content"),
            "rule_type": rule.get("rule_type", "supply"),
            "rule_activation_group": rule.get("rule_activation_group", ""),
            "rule_limit_type": rule.get("rule_limit_type", "strict"),
            "rule_weight": rule.get("rule_weight", 0),
            "rule_allow_overflow_rate": rule.get("rule_allow_overflow_rate", 0),
            "rule_product_code": rule.get("rule_product_code", "")
        }
        rule_weight = {
            "weight_type": "channel",
            "weight_code": rule.get("channel"),
            "weight_desc": rule.get("rule_desc"),
            "weight_rule_content": "finalRuleList.contains(\\\'{}\\\')".format(rule.get("rule_code")),
            "weight_value": rule.get("weight_value", 0),
            "weight_status": rule.get("weight_status", "active"),
            "weight_first_route_status": rule.get("weight_first_route_status", "active"),
            "weight_second_route_status": rule.get("weight_second_route_status", "active")
        }
        capital_plan = {
            "plan_date": get_date(fmt="%Y-%m-%d", timezone=get_tz(gc.COUNTRY)),
            "plan_label": rule.get("rule_code"),
            "plan_desc": rule.get("rule_desc"),
            "plan_amount": rule.get("plan_amount", 200000000000)
        }
        update_router_capital_rule(capital_rule)
        update_router_weight(rule_weight)
        update_router_capital_plan(capital_plan)


def init_router_rule_data(rule_data_lt):
    delete_router_capital_rule()
    delete_router_capital_plan()
    delete_router_weight()
    delete_router_load_total()
    for data in rule_data_lt:
        channel = data['channel']
        period = data['period']
        period_day = data['period_day']
        period_type = data['period_type']
        for rule in data['rule_lt']:
            rule_code = '{}_{}'.format(channel, rule['rule_code'])
            rule_limit_type = rule.get('rule_limit_type', 'strict')
            overflow_rate = rule.get('overflow_rate', 0)
            plan_amount = rule.get('plan_amount', 200000000)
            routed_amount = rule.get('routed_amount', 0)
            imported_amount = rule.get('imported_amount', 0)
            insert_router_capital_rule(channel, period, period_day, period_type, rule_code, rule_limit_type,
                                       overflow_rate)
            insert_router_capital_plan(rule_code, plan_amount)
            insert_router_load_total(rule_code, routed_amount, imported_amount)
            for weight in rule['weight']:
                insert_router_weight(channel, rule_code, weight)


def get_rule_code(rule_data_lt, channel_idx, rule_idx=0):
    rule_code = "{}_{}".format(rule_data_lt[channel_idx]["channel"],
                               rule_data_lt[channel_idx]["rule_lt"][rule_idx]["rule_code"])

    return rule_code


def insert_router_record(item_no):
    asset_info = get_asset_import_data_by_item_no(item_no)
    count = asset_info["data"]["asset"]["period_count"]
    days = asset_info["data"]["asset"]["period_day"]
    types = asset_info["data"]["asset"]["period_type"]
    amount = asset_info["data"]["asset"]["amount"]
    channel = asset_info["data"]["asset"]["loan_channel"]
    id_num = asset_info["data"]["borrower"]["id_num"]

    # 进件前，在路由表插入一条记录
    keys = {"router_load_record_key": item_no,
            "router_load_record_rule_code": channel + "_" + str(count) + "_" + str(days) + types[:1],
            "router_load_record_principal_amount": amount,
            "router_load_record_status": "routed",
            "router_load_record_channel": channel,
            "router_load_record_sub_type": "multiple",
            "router_load_record_period_count": count,
            "router_load_record_period_type": types,
            "router_load_record_period_days": days,
            "router_load_record_route_day": get_date(fmt="%Y-%m-%d"),
            "router_load_record_idnum": id_num,
            "router_load_record_from_system": asset_info['from_system'],
            }
    insert_router_load_record(**keys)


def get_payment_account_config(city, min_balance_amount, skip_balance_query):
    # 重新组装gbiz_payment_config 下的paysvr_subject节点
    paysvr_subject = {}
    paysvr_date = []
    for channel_config in global_gbiz_common_config.capital_plan[city]:
        channel = channel_config.get('channel')
        account = channel_config.get('account')
        channel_date = {
            "name": channel,
            "account": account,
            "paysvr_system": "paysvr",
            "warn_amount": min_balance_amount,
            "skip_balance_query": skip_balance_query
        }
        data = dict.fromkeys([channel + '_withdraw'], channel_date)
        paysvr_date.append(data)
    for ls in paysvr_date:
        for key in ls.keys():
            paysvr_subject[key] = ls.get(key)
    return paysvr_subject


def get_channle_apr_rule(city, channel):
    rule = ''
    for channel_config in global_gbiz_common_config.capital_plan[city]:
        if channel_config.get('channel') == channel:
            rule = channel_config.get('rule')
    return rule
