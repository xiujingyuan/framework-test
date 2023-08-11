#!/usr/bin/python
# -*- coding: UTF-8 -*-
from foundation_test.util.db.db_util import DataBase

db = DataBase("oa")


def get_root_rate_config_info(rate_number):
    sql = "select * from rate_config where rate_config_rate_number = '%s' and rate_config_parent_id = 0" % rate_number
    result = db.query(sql)
    return result
