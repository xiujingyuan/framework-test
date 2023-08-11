#!/usr/bin/python
# -*- coding: UTF-8 -*-
from foundation_test.function.contractsvr.contractsvr_db_function import *
from foundation_test.util.asserts.assert_util import Assert


def check_contract_apply(apply_id, status):
    contract_apply = get_contract_apply_by_apply_id(apply_id)
    Assert.assert_equal(status, contract_apply[0]['status'], "contract_apply_status不正确")


def check_contract_status(contract_id, status):
    contract = get_contract_by_contract_id(contract_id)
    Assert.assert_equal(status, contract[0]['contract_status'], "contract_status")
