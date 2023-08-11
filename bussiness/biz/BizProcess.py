# -*- coding: utf-8 -*-
# @Title: BizProcess
# @ProjectName framework-test
# @Description: TODO
# @author fyi zhang
# @date 2018/12/12 19:42

from framework.dao.BizProcessDAO import BizProcessDAO
from common.tools.CommUtils import CommUtils
from common.tools.BaseUtils import BaseUtils
from common.tools.HttpUtils import HttpUtils
from common.tools.BusTools import BusTools
from framework.dao.FrameworkDAO import FrameworkDAO
from bussiness.biz.CommonProcess import CommonProcess

class BizProcess(CommonProcess):

    def __init__(self):
        self.biz_dao = BizProcessDAO()
        self.dao = FrameworkDAO()
        self.common_util = CommUtils()
        self.bustools = BusTools()
        self.http_util = HttpUtils()



    def prev_small_order(self,prev_entity,case,vars):
        prev_params = prev_entity.prev_params
        prev_except_expression = prev_entity.prev_except_expression
        request_body = self.bustools.repalce_system_params(case.case_api_params,vars=vars)
        request_body = self.bustools.replace_user_params(request_body,prev_params)
        request_body = BaseUtils.extend_value_target(vars,request_body,prev_except_expression)
        case.case_api_params = request_body
        return case



