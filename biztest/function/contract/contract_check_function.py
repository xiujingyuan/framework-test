#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.function.contract.contract_db_function import *
from biztest.util.asserts.assert_util import Assert
import json
import time


def check_contract(item_no, opportunity, expect_contract_types, expect_subject=None, expect_status='SUCCESS'):
    """
    检查合同
    1、合同数量
    2、合同类型
    3、合同状态=SUCCESS
    4、合同url不为空
    5、合同主体
    :param item_no:
    :param opportunity:
    :param expect_contract_types:
    :param expect_subject: 期望的合同主体
    :param expect_status: 期望的合同状态
    :return:
    """
    time.sleep(2)
    contract_lt = get_contract_by_item_no_opportunity(item_no, opportunity, expect_status)
    Assert.assert_equal(len(expect_contract_types), len(contract_lt), "contract数量不正确")
    for contract in contract_lt:
        Assert.assert_in(contract['contract_type'], expect_contract_types, "contract_type不正确")
        Assert.assert_equal(expect_status, contract['contract_status'], "contract_status不正确")
        Assert.assert_not_equal("", contract['contract_url'], "contract_url不正确")
        if expect_subject is not None:
            Assert.assert_equal(expect_subject, contract['contract_subject'], "contract_subject不正确")


def check_contract_info(item_no, opportunity, contract_type, **kwargs):
    latest_contract = get_contract(item_no, opportunity, contract_type)[-1]
    for key, value in kwargs.items():
        Assert.assert_equal(latest_contract[key], value, "%s数据有误" % key)


def check_sendmsg_data(item_no, **kwargs):
    latest_msg = get_sendmsg(item_no, 'ContractSignSuccess')[-1]
    data = json.loads(latest_msg['sendmsg_content'])['body']['data']
    for key, value in kwargs.items():
        Assert.assert_equal(value, data[key], "%s数据有误" % key)


def check_task_not_exist(item_no, task_type):
    rs = get_open_task_by_item_no_and_task_type(item_no, task_type)
    Assert.assert_equal(len(rs), 0, "数据有误")
