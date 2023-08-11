#!/usr/bin/python
# -*- coding: UTF-8 -*-
import biztest.config.gbiz.gbiz_common_config as gbiz_common_config
from biztest.function.gbiz.gbiz_db_function import create_attachment_by_item_no,update_router_capital_plan,\
    update_router_capital_rule,update_router_weight, update_task_by_item_no_task_type, insert_router_capital_plan, insert_router_capital_rule, \
    delete_router_capital_rule, delete_router_capital_plan, delete_router_weight, insert_router_weight, \
    delete_router_load_total, insert_router_load_total
from biztest.function.contract.contract_db_function import contract_create_attachment_by_item_no
import biztest.function.gbiz.gbiz_db_function as gbiz_db_function
import biztest.function.biz.biz_db_function as biz_db_function
from biztest.util.tools.tools import get_four_element, date_to_timestamp, get_date
import common.global_const as gc
from biztest.interface.gbiz.gbiz_interface import asset_import
from biztest.util.task.task import GbizTask
from biztest.util.msg.msg import GbizMsg


def prepare_attachment(channel, item_no):
    for item in gbiz_common_config.attachment.get(channel):
        contract_create_attachment_by_item_no(item_no, channel, item[0], item[1], item[2])
        # 云信全互还是读的gbiz附件表
        if channel == "yunxin_quanhu":
            create_attachment_by_item_no(item_no, item[0], item[1], item[2])


def init_capital_plan(channel=None):
    """
    初始化资金计划
    :param channel:
    :return:
    """
    if channel:
        update_capital_plan(gbiz_common_config.capital_plan[channel])
    else:
        delete_router_capital_rule()
        delete_router_capital_plan()
        delete_router_weight()
        for channel in gbiz_common_config.capital_plan:
            update_capital_plan(gbiz_common_config.capital_plan[channel])


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
            "plan_date": get_date(fmt="%Y-%m-%d"),
            "plan_label": rule.get("rule_code"),
            "plan_desc": rule.get("rule_desc"),
            "plan_amount": rule.get("plan_amount", 200000000000)
        }
        update_router_capital_rule(capital_rule)
        update_router_weight(rule_weight)
        update_router_capital_plan(capital_plan)


def run_terminated_task(item_no, task_type, expect_code=0):
    update_task_by_item_no_task_type(item_no, task_type, task_status="open")
    GbizTask().run_task(item_no, task_type, excepts={"code": expect_code})


def get_invoked_api(channel, task, path_prefix):
    return [path_prefix + x for x in gbiz_common_config.invoked_api[channel][task]]


def init_router_rule_data(rule_data_lt):
    delete_router_capital_rule()
    delete_router_capital_plan()
    delete_router_weight()
    delete_router_load_total()
    gc.GRANT_REDIS.flushdb()
    for data in rule_data_lt:
        channel = data['channel']
        period = data['period']
        period_type = data['period_type']
        for rule in data['rule_lt']:
            rule_code = '{}_{}{}_{}'.format(channel, period, period_type, rule['rule_code'])
            rule_limit_type = rule.get('rule_limit_type', 'strict')
            overflow_rate = rule.get('overflow_rate', 0)
            plan_amount = rule.get('plan_amount', 200000000)
            routed_amount = rule.get('routed_amount', 0)
            imported_amount = rule.get('imported_amount', 0)
            insert_router_capital_rule(channel, period, period_type, rule_code, rule_limit_type, overflow_rate)
            insert_router_capital_plan(rule_code, plan_amount)
            insert_router_load_total(rule_code, routed_amount, imported_amount)
            for weight in rule['weight']:
                insert_router_weight(channel, rule_code, weight)
            cache_routed_amount = rule.get('cache_routed_amount', 0)
            cache_imported_amount = rule.get('cache_imported_amount', 0)
            today_timestamp = date_to_timestamp(get_date(fmt="%Y-%m-%d"), fmt="%Y-%m-%d")
            if cache_routed_amount > 0:
                gc.GRANT_REDIS.setex("{}-routed-{}".format(rule_code, today_timestamp), value=cache_routed_amount, time=1800)
            if cache_imported_amount > 0:
                gc.GRANT_REDIS.setex("{}-imported-{}".format(rule_code, today_timestamp), value=cache_imported_amount, time=1800)


def get_rule_code(rule_data_lt, channel_idx, rule_idx=0):
    rule_code = "{}_{}{}_{}".format(rule_data_lt[channel_idx]["channel"],
                                    rule_data_lt[channel_idx]["period"],
                                    rule_data_lt[channel_idx]["period_type"],
                                    rule_data_lt[channel_idx]["rule_lt"][rule_idx]["rule_code"])
    return rule_code


def fake_asset_data(channel, period=12, amount=5000, from_system_name="香蕉", source_type="apr36", status="sale", four_element=None):
    if four_element is None:
        four_element = get_four_element()
    item_no, asset_info = asset_import(channel, four_element, period, amount, from_system_name, source_type)
    GbizTask().run_task(item_no, "AssetImport", excepts={"code": 0})
    GbizMsg().run_msg(item_no, "AssetImportSync", excepts={"code": 0})
    biz_db_function.wait_biz_asset_appear(item_no)
    gbiz_db_function.update_asset_by_item_no(item_no, asset_status=status)
    biz_db_function.set_asset_status(item_no, status)
    return item_no
