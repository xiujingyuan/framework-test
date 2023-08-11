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
import pytest

from bussiness.basic.common.CommCls import CommCls
from bussiness.biz.CommonProcess import CommonProcess
from common.tools.FinlabAssert import FinlabAssert
from common.tools.BaseUtils import BaseUtils
from common.tools.BusTools import BusTools
from bussiness.biz.ProcessFactory import ProcessFactory

class BaseCls(object):

    def __init__(self,case,case_vars,run_id,debug_config):
        self.case = case
        self.comm_cls = CommCls()
        self.biz_util = CommonProcess()
        self.case_vars =case_vars
        self.bustools = BusTools()
        self.run_id = run_id
        self.debug_config = debug_config
        self.status = 1


    def run_case(self):
        """
        发送请求
        :return:
        """

        print("开始数据请求，case_id = "+str(self.case.case_id) )
        try:
            self.comm_cls.run_sub_case(self.case,self.case_vars)
        except Exception as error:
            self.case_vars['exception'] = str(error)
            self.bustools.write_history(self.case,self.comm_cls.except_value,self.comm_cls.actual_value,self.case_vars,self.run_id,0)
            pytest.fail(str(error),True)



    def init_data(self):
        """
        数据准备
        :return:
        """
        print("数据初始化开始，case_id = "+str(self.case.case_id) )
        try:
            self.comm_cls.wait_time_exec(self.case)
            self.comm_cls.exec_init_or_teardown(self.case,self.case_vars,'setup',self.run_id)
            ProcessFactory.main_process(ProcessFactory.init_process(self.case),self.case,self.case_vars,'setup','common',self.run_id)
            self.biz_util.prev_run_task(self.case,self.case_vars,'setup',self.run_id)
        except Exception as error:
            self.case_vars['exception'] = str(error)
            self.bustools.write_history(self.case,self.comm_cls.except_value,self.comm_cls.actual_value,self.case_vars,self.run_id,0)
            pytest.fail(str(error),True)

    def after_init_data(self):
        """
        后置数据准备
        :return:
        """
        print("后置数据准备，case_id = "+str(self.case.case_id) )
        try:
            self.case.except_value = self.comm_cls.except_value
            self.case.actual_value = self.comm_cls.actual_value
            ProcessFactory.main_process(ProcessFactory.init_process(self.case),self.case,self.case_vars,'teardown','common',self.run_id)
            self.comm_cls.except_value = self.case.except_value
            self.comm_cls.actual_value = self.case.actual_value
            BaseUtils.set_vars('response',self.case.actual_value,self.case,self.case_vars)
            self.case.case_vars = BaseUtils.transfer_dict_to_string(self.case_vars)
        except Exception as error:
            self.case_vars['exception'] = str(error)
            self.bustools.write_history(self.case,self.comm_cls.except_value,self.comm_cls.actual_value,self.case_vars,self.run_id,0)
            pytest.fail(str(error),True)

    def compare_result(self):
        """
        对比结果
        :return:
        """
        print("对比结果，case_id = "+str(self.case.case_id) )
        try:
            FinlabAssert.assert_result(self.comm_cls.except_value,self.comm_cls.actual_value,self.case_vars)
        except Exception as error:
            self.case_vars['exception'] = str(error)
            self.bustools.write_history(self.case,self.comm_cls.except_value,self.comm_cls.actual_value,self.case_vars,self.run_id,0)
            pytest.fail(str(error),True)
        self.status=1

    def clear_data(self):
        """
        数据清理
        :return:
        """
        try:
            print("清理环境，case_id = "+str(self.case.case_id) )
            self.comm_cls.exec_init_or_teardown(self.case,self.case_vars,'teardown',self.run_id)
            self.biz_util.prev_run_task(self.case,self.case_vars,'teardown',self.run_id)
            # ProcessFactory.main_process(ProcessFactory.init_process(self.case),self.case,self.case_vars,'teardown','common',self.run_id)
        except Exception as error:
            self.bustools.write_history(self.case,self.comm_cls.except_value,self.comm_cls.actual_value,self.case_vars,self.run_id,0)
            pytest.fail(str(error),True)
        self.bustools.write_history(self.case,self.comm_cls.except_value,self.comm_cls.actual_value,self.case_vars,self.run_id,self.status)


