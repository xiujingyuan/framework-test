#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

import common.global_const as gc
import biztest.config.gbiz.gbiz_common_config as gbiz_common_config
from biztest.function.cmdb.cmdb_db_function import get_root_rate_config_info_by_channel
from biztest.function.gbiz.gbiz_db_function import get_asset_info_by_item_no
from biztest.function.cmdb.cmdb_common_function import get_total_amount
import decimal


def get_available_capital_rule(channel, period_count, product_code):
    """
    获取可用的资金规则
    :param channel:
    :param period_count:
    :param product_code:
    :return:
    """
    if channel in gbiz_common_config.capital_plan:
        available_rule = [x for x in gbiz_common_config.capital_plan[channel]
                          if str(period_count) in x.get("rule_content")
                          and (product_code == x.get("rule_product_code", "") if product_code != "" else 1)
                          ]
    else:
        raise Exception("gbiz_common_config not found {0}".format(channel))
    if len(available_rule) > 0:
        return available_rule[0]
    else:
        raise Exception("没有可用的资金计划！")


def calc_noloan_amount(item_no, noloan_source_type):
    """
    计算小单金额
    APR融担小单金额 = APR36总额 - 大单总额
    IRR融担小单金额 = IRR36总额 - 大单总额
    IRR权益小单金额 = APR36总额 - IRR36总额
    :param item_no:
    :param noloan_source_type:
    :return:
    """
    asset = get_asset_info_by_item_no(item_no)
    loan_principal_amount = asset[0]["asset_principal_amount"]
    loan_period_count = int(asset[0]["asset_period_count"])
    loan_total_amount = asset[0]["asset_total_amount"]
    loan_channel = asset[0]["asset_loan_channel"]
    # channel_config = json.loads(gc.NACOS.get_config("grant%s" % gc.ENV, "KV", "gbiz_capital_" + loan_channel)['content'])
    # irr_limit = channel_config["task_config_map"]["RongDanIrrTrial"]["execute"]["trail_irr_limit"] \
    #     if "RongDanIrrTrial" in channel_config["task_config_map"].keys() else 36
    rongdan_irrtrial_channel = ['zhongyuan_zunhao', 'lanzhou_haoyue_qinjia', 'lanzhou_haoyue', 'jinmeixin_hanchen',
                                'beiyin_daqin', 'yixin_rongsheng', 'lanhai_zhilian', 'weipin_zhongwei',
                                'jincheng_hanchen']
    if loan_channel in rongdan_irrtrial_channel:
        irr_limit = 35.99
    else:
        irr_limit = 36
    # 默认值
    noloan_amount = loan_principal_amount / 80

    if noloan_source_type == "rongdan":
        noloan_amount = get_total_amount("apr", loan_principal_amount, loan_period_count) \
                        - loan_total_amount
    elif noloan_source_type == "rongdan_irr":
        noloan_amount = get_total_amount("irr", loan_principal_amount, loan_period_count, interest_rate=irr_limit) \
                        - loan_total_amount
    elif noloan_source_type == "lieyin":
        noloan_amount = get_total_amount("apr", loan_principal_amount, loan_period_count) \
                        - get_total_amount("irr", loan_principal_amount, loan_period_count)

    # rate_info = get_root_rate_config_info_by_channel(loan_channel)
    # calculate_type = rate_info[0]['rate_config_calculate_type']
    # rate_value = decimal.Decimal(rate_info[0]['rate_config_value']) / 100
    # round_type = rate_info[0]['rate_config_carry_mode']
    # year_days = rate_info[0]['rate_interest_year_days']
    # month_clear_day = rate_info[0]['rate_month_clear_day']
    # clear_day = rate_info[0]['rate_clear_day']
    # if loan_channel in ['siping_jiliang', 'mozhi_jinmeixin', 'yilian_dingfeng', 'jinmeixin_daqin']:
    #     if noloan_source_type == "rongdan":
    #         noloan_amount = get_total_amount("aprByDay", loan_principal_amount, loan_period_count, year_days=365,
    #                                          month_clear_day=month_clear_day, clear_day=clear_day) \
    #                         - loan_total_amount
    #     elif noloan_source_type == "rongdan_irr":
    #         noloan_amount = 0
    #     elif noloan_source_type == "lieyin":
    #         noloan_amount = get_total_amount("aprByDay", loan_principal_amount, loan_period_count, year_days=365,
    #                                          month_clear_day=month_clear_day, clear_day=clear_day) \
    #                         - loan_total_amount
    # else:
    #     if noloan_source_type == "rongdan":
    #         noloan_amount = get_total_amount("apr", loan_principal_amount, loan_period_count) \
    #                         - loan_total_amount
    #     elif noloan_source_type == "rongdan_irr":
    #         noloan_amount = get_total_amount("irr", loan_principal_amount, loan_period_count) \
    #                         - loan_total_amount
    #     elif noloan_source_type == "lieyin":
    #         noloan_amount = get_total_amount("apr", loan_principal_amount, loan_period_count) \
    #                         - get_total_amount("irr", loan_principal_amount, loan_period_count)
    return noloan_amount / 100
