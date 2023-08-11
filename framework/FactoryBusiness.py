#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm  
 @time: 2018/10/18
 @file: FactoryBusiness.py
 @site:
 @email:
"""
from bussiness.tmms.ClsTmms import ClsTmms
from bussiness.basic.BaseCls import BaseCls
from bussiness.basic.GroupCls import GroupCls

class FactoryBusiness(object):

    @classmethod
    def init_business(cls, case,run_id,case_vars={},debug_config=0):
        if case.case_executor == "common":
            return BaseCls(case,case_vars,run_id,debug_config)
        elif case.case_executor == "group":
            return GroupCls(case,case_vars,run_id,debug_config)
        elif case.case_executor == "tmms":
            return ClsTmms(case)
        else:
            return None


