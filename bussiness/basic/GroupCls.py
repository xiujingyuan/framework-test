#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2018/10/30
 @file: BaseDb.py
 @site:
 @email:
"""
import copy

from bussiness.basic.BaseCls import BaseCls
from bussiness.basic.common.CommCls import CommCls


class GroupCls(object):

    def __init__(self,case,case_vars,run_id,debug_config):
        self.case = case
        self.comm_cls = CommCls()
        self.main_case = case
        self.sub_cases = None
        self.case_vars = case_vars
        self.debug_config = debug_config
        self.run_id = run_id





    def run_case(self):
        """
        发送请求
        :return:
        """
        self._run_main_case()
        self._run_sub_case()




    def _run_main_case(self):
        base_cls = BaseCls(self.main_case,self.case_vars,self.run_id,self.debug_config)
        self._run_base_case(base_cls)


    def _run_sub_case(self):
        for case in self.sub_cases:
            base_cls = BaseCls(case,self.case_vars,self.run_id,self.debug_config)
            self._run_base_case(base_cls)



    def _run_base_case(self,base_cls):
        #初始化数据

        base_cls.init_data()

        # 执行
        print("开始执行用例，case_id = "+str(base_cls.case.case_id) )
        base_cls.run_case()
        # 后置数据准备
        print("做后置的数据准备，case_id = "+str(base_cls.case.case_id) )
        base_cls.after_init_data()
        # 对比结果
        print("开始对比预期值和实际值，case_id = "+str(base_cls.case.case_id) )
        base_cls.compare_result()

        print("开始清理环境，case_id = "+str(base_cls.case.case_id) )
        base_cls.clear_data()




    def init_data(self):
        """
        数据准备
        :return:
        """
        if self.debug_config==0:
            sub_cases = self.comm_cls.get_sub_cases(self.case)
            self.sub_cases = copy.deepcopy(sub_cases)
        else:
            self.sub_cases=[]
        print("init_data")
        # print("init_data", self.sub_cases, self.debug_config)

    def after_init_data(self):
        """
        后置数据准备
        :return:
        """
        print("after_init_data")

    def compare_result(self):
        """
        对比结果
        :return:
        """
        print("compare_result")

    def clear_data(self):
        """
        数据清理
        :return:
        """
        print("clear_data")
