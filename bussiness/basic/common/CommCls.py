# -*- coding: utf-8 -*-
# @Title: CommCls
# @ProjectName framework-test
# @Description: TODO
# @author fyi zhang
# @date 2018/11/2922:29

import copy
import time
from common.tools.HttpUtils import HttpUtils
from common.tools.BaseUtils import BaseUtils
from common.tools.CommUtils import CommUtils
from common.tools.BusTools import BusTools
from framework.dao.FrameworkDAO import FrameworkDAO
from bussiness.biz.BizProcess import BizProcess
class CommCls(object):

    def __init__(self):
        self.http = HttpUtils()
        self.comm_utils = CommUtils()
        self.bustools = BusTools()
        self.dao = FrameworkDAO()
        self.biz_process = BizProcess()
        self.actual_value =None
        self.except_value = None



    def run_sub_case(self, case, case_vars):
        if case.case_check_method.lower()=='except':
            url = self.bustools.repalce_system_params(case.case_api_address,vars=case_vars)
            params = self.bustools.repalce_system_params(case.case_api_params,vars=case_vars)
            BaseUtils.set_vars("request", params, case,case_vars)
            method = self.bustools.repalce_system_params(case.case_api_method,vars=case_vars)
            header = self.bustools.repalce_system_params(case.case_api_header,vars=case_vars)
            self.except_value = self.get_except_value(case)
            key_value = case.case_replace_expression
            url = self.process_request_url(url,method,params,key_value,case_vars)
            self.actual_value = self.http.http_request(url,params,method,header,case.case_mock_flag,case.case_id)
            case.case_api_params = BaseUtils.transfer_dict_to_string(params)
            case.case_api_address=url

        elif case.case_check_method.lower() == 'database':
            self.actual_value = self.get_actual_value(case,case_vars)
            self.except_value = self.get_except_value(case)
            self.except_value = self.bustools.repalce_system_params(self.except_value,vars=case_vars)
            case.case_except_value = BaseUtils.transfer_dict_to_string(self.except_value)
            case.actual_value = BaseUtils.transfer_dict_to_string(self.actual_value)



    def replace_sql_params(self,case,case_vars):
        keyvalue = self.bustools.repalce_system_params(case.case_replace_expression,vars=case_vars)
        param=self.bustools.repalce_system_params(case.case_sql_params,vars=case_vars)
        sql_params = BaseUtils.extend_value_target(case_vars,param,keyvalue)
        case.case_sql_params = sql_params
        return sql_params




    def process_request_url(self, url,method,param,keyvalue,vars):
        url = self.bustools.repalce_system_params(url,vars=vars)
        if method.lower() == "get" and BaseUtils.object_is_notnull(param):
            user_params = BaseUtils.extend_value_target(vars, param, keyvalue)
            url = self.bustools.replace_user_params(url,user_params)
        return url



    def get_actual_value(self,case,case_vars):
        result =''
        sql_params = self.replace_sql_params(case,case_vars)
        sql_statement = self.bustools.repalce_system_params(case.case_sql_actual_statement,vars=case_vars)
        sql_actual_database = self.bustools.repalce_system_params(case.case_sql_actual_database,vars=case_vars)
        #sql_reference_name = self.bustools.repalce_system_params(case.case_sql_reference_name,vars=case_vars)
        if BaseUtils.object_is_notnull(sql_params):
            sql_params = BaseUtils.transfer_string_to_dict(sql_params)
        if BaseUtils.object_is_notnull(sql_statement):
            sqlentity = self.dao.get_actual_sqlentity(sql_statement,sql_params,sql_actual_database)
            result = self.dao.queryallBySqlEntity(sqlentity,sql_actual_database)
        # elif BaseUtils.object_is_notnull(sql_reference_name):
        #     except_sql_reference_name_dict = BaseUtils.transfer_dict_to_entity(BaseUtils.transfer_string_to_dict(sql_reference_name))
        #     file_name = except_sql_reference_name_dict.file_name
        #     sql_name = except_sql_reference_name_dict.sql_name
        #     sqlentity = self.dao.get_complete_sqlentity(file_name,sql_name,sql_statement)
        #     result = self.dao.queryallBySqlEntity(sqlentity,sql_actual_database)
        return BaseUtils.transfer_dict_to_string(result)



    def get_sub_cases(self,case):
        sub_cases = self.dao.get_sub_case(case)
        return sub_cases



    #初始化数据
    def exec_init_or_teardown(self,case,case_vars,init_type,run_id=0):
        case_id = case.case_id
        #获取初始化数据
        old_case_inits = self.get_init_bycase_init_id(case,init_type)
        case_inits = self.dao.get_init_bycaseid(case_id,init_type)
        case_inits.extend(old_case_inits)
        case_copy_inits = copy.deepcopy(case_inits)
        for init in case_copy_inits:
            try:
                self.exec_api_byinit(init,case_vars,case)
                self.exec_sql_byinit(init,case_vars,case)
            finally:
                self.bustools.write_history_init(init,run_id)

    def get_init_bycase_init_id(self,case,init_type):
        case_inits=[]
        case_init_ids = case.case_init_id
        if BaseUtils.object_is_null(case_init_ids):
            return case_inits
        ids = BaseUtils.transfer_string_to_dict(case_init_ids)

        if isinstance(ids,list):
            for id in ids:
                inits = self.dao.get_init_byinitid(int(id),init_type)
                for init in inits:
                    case_inits.append(init)
        else:
            inits = self.dao.get_init_byinitid(int(ids),init_type)
            for init in inits:
                case_inits.append(init)
        return case_inits


    def exec_api_byinit(self,init,case_vars,case):
        url = init.case_init_api_address
        if BaseUtils.object_is_null(url):
            return
        method = init.case_init_api_method
        params = self.bustools.repalce_system_params(init.case_init_api_params,vars=case_vars)
        header = init.case_init_api_header
        key_value = self.bustools.repalce_system_params(init.case_init_api_expression,vars=case_vars)
        url = self.process_request_url(url,method,params,case_vars,key_value)
        params = BaseUtils.extend_value_target(case_vars,params,key_value)
        BaseUtils.set_vars("initapi_request", params,case,case_vars)
        actual_result = self.http.http_request(url,params,method,header)
        BaseUtils.set_vars("initapi_response", actual_result,case,case_vars)
        init.case_init_api_address = url
        init.case_init_api_params=params

        return actual_result



    def exec_sql_byinit(self,init,case_vars,case):
        sql_statement = self.bustools.repalce_system_params(init.case_init_sql,vars=case_vars)
        if BaseUtils.object_is_null(sql_statement):
            return
        sql_param = self.bustools.repalce_system_params(init.case_init_sql_params,vars=case_vars)
        sql_exec_database = self.bustools.repalce_system_params(init.case_init_sql_database,vars=case_vars)
        sql_express = self.bustools.repalce_system_params(init.case_init_sql_expression,vars=case_vars)
        sql_param = BaseUtils.extend_value_target(case_vars,sql_param,sql_express)
        result = self.dao.exec_init_sql(sql_statement,sql_exec_database,sql_param)
        BaseUtils.set_vars("initsql_request", sql_param,case,case_vars)
        init.case_init_sql = sql_statement
        init.case_init_sql_params=sql_param
        init.case_init_sql_database = sql_exec_database
        return result


    def wait_time_exec(self,case):
        second = case.case_wait_time
        if BaseUtils.object_is_null(second):
            return
        time.sleep(second)

    def get_except_value(self,case):
        check_style = case.case_check_method.lower()
        if check_style =="except":
            return BaseUtils.transfer_string_to_dict(self.bustools.repalce_system_params(case.case_except_value))
        elif check_style =="database":
            except_value =  self.bustools.repalce_system_params(case.case_except_value)
            return BaseUtils.transfer_string_to_dict(except_value)
            #TODO DataBase预留值
        else:
            pass
            #TODO API 获取预期值

    # def process_prev_request(self,prev):
    #     url = prev.prev_api_address
    #     method = prev.prev_api_method
    #     header= prev.prev_api_header
    #     params = prev.prev_api_params
    #     key_value = prev.prev_api_expression
    #     except_value = BaseUtils.transfer_string_to_dict(prev.prev_except_value)
    #     url = self.process_request_url(url,method,params,key_value)
    #     result = HttpUtils.http_request(url,params,method,header)
    #     FinlabAssert.assert_result(except_value,result)












