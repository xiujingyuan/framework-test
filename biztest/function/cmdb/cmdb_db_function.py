#!/usr/bin/python
# -*- coding: UTF-8 -*-
import common.global_const as gc


def get_channel_by_source_type(source_type):
    sql = "select distinct a.rate_capital_code from rate a left join product_rate b " \
          "on a.rate_number = b.product_rate_number where b.product_rate_scope in " \
          "(select product_scope from product where (product_condition like '%{}%' " \
          "or locate('source_type', product_condition)=0) and product_status = 'online') " \
          "and a.rate_status = 'pass' and a.rate_valid_start_date <= now() " \
          "and a.rate_valid_end_date >= now() and a.rate_capital_code != 'noloan'".format(source_type)
    result = gc.CMDB_DB.query(sql)
    channel_list = [x['rate_capital_code'] for x in result]
    return channel_list


def get_rate_info(rate_number):
    sql = "select * from rate where rate_number = '%s'" % rate_number
    result = gc.CMDB_DB.query(sql)
    return result


def get_root_rate_config_info(rate_number):
    sql = "select * from rate_config where rate_config_rate_number = '%s' and rate_config_parent_id = 0" % rate_number
    result = gc.CMDB_DB.query(sql)
    return result


def get_root_rate_config_info_by_channel(channel):
    sql = "select rate_config_value, rate_config_calculate_type, rate_config_carry_mode, rate_interest_year_days, rate_month_clear_day, rate_clear_day from rate left join rate_config on rate_number = rate_config_rate_number " \
          "where rate_status = 'pass' and rate_config_parent_id = 0 and rate_capital_code = '%s' " \
          "order by rate_id desc limit 1" % channel
    result = gc.CMDB_DB.query(sql)
    return result
