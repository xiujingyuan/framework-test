#!/usr/bin/python
# -*- coding: UTF-8 -*-
from foundation_test.interface.contractsvr.contractsvr_interface import *
from foundation_test.function.contractsvr.contractsvr_check_function import *
from foundation_test.function.contractsvr.contractsvr_db_function import *

import uuid
import pytest
import time


@pytest.mark.contractsvr
def test_sign_apply_success():
    apply_id = str(uuid.uuid1())
    # 申请签约
    sign_apply(apply_id)
    contract_id = get_contract_id_by_apply_id(apply_id)
    time.sleep(2)
    check_contract_status(contract_id, 1)


@pytest.mark.contractsvr
def test_sign_apply_seal_error():
    apply_id = str(uuid.uuid1())
    # 申请签约
    sign_apply(apply_id)
    contract_id = get_contract_id_by_apply_id(apply_id)
    # 增加一个签章
    add_seal_log(contract_id)
    time.sleep(2)
    check_contract_status(contract_id, 20)
