#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.function.deposit.deposit_db_function import get_trade_order_by_order_no, get_trade_by_trade_no
from biztest.util.asserts.assert_util import Assert


def check_data(data, **kwargs):
    for key, value in kwargs.items():
        Assert.assert_equal(value, data[key], "%s数据有误" % key)


def check_trade_order_data(order_no, **kwargs):
    trade_order = get_trade_order_by_order_no(order_no)[0]
    check_data(trade_order, **kwargs)


def check_trade_data(trade_no, **kwargs):
    trade_order = get_trade_by_trade_no(trade_no)[0]
    check_data(trade_order, **kwargs)
