# -*- coding: utf-8 -*-
# @Time    : 公元19-02-21 上午11:17
# @Author  : 张廷利
# @Site    : 
# @File    : ProcessFactory.py
# @Software: IntelliJ IDEA

import copy

from bussiness.biz.BizProcess import BizProcess
from bussiness.biz.RbizProcess import RbizProcess
from bussiness.biz.CommonProcess import CommonProcess
from framework.dao.BizProcessDAO import BizProcessDAO
from common.tools.BusTools import BusTools
from common.tools.CommUtils import CommUtils

class ProcessFactory(object):


    @classmethod
    def main_process(self,process,case,vars,setup_type,prev_task_type,run_id):
        prevs = BizProcessDAO().get_prevs_bycaseid(case.case_id,setup_type,prev_task_type)
        copy_prevs = copy.deepcopy(prevs)
        for prev in copy_prevs:
            try:
                CommUtils.wait_exec_time(prev.prev_wait_time)
                self.distribute_processs_func(process,prev.prev_flag,prev,case,vars)
            finally:
                BusTools().write_history_prev(prev,run_id)
        return case

    @classmethod
    def distribute_processs_func(self,*args):
        process=args[0]
        func_name = args[1]
        prev_enitity = args[2]
        case = args[3]
        vars = args[4]
        getattr(process, func_name)(prev_enitity,case,vars)



    @classmethod
    def init_process(cls,case):
        if case.case_from_system=='grant_system':
            return BizProcess()
        elif case.case_from_system=='repay_system':
            return RbizProcess()
        else:
            return CommonProcess()