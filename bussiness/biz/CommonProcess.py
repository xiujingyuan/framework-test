# -*- coding: utf-8 -*-
# @Time    : 公元19-02-21 上午11:01
# @Author  : 张廷利
# @Site    : 
# @File    : CommonProcess.py
# @Software: IntelliJ IDEA
import copy

from framework.dao.BizProcessDAO import BizProcessDAO
from common.tools.CommUtils import CommUtils
from common.tools.BaseUtils import BaseUtils
from common.tools.HttpUtils import HttpUtils
from common.tools.BusTools import BusTools
from framework.dao.FrameworkDAO import FrameworkDAO
from common.tools.FinlabAssert import FinlabAssert

class CommonProcess(object):
    def __init__(self):
        self.biz_dao = BizProcessDAO()
        self.dao = FrameworkDAO()
        self.common_util = CommUtils()
        self.bustools = BusTools()
        self.http_util = HttpUtils()




    def prev_run_task(self,case,vars,setup_type,run_id=0):
        #运行task，这里面的task 包含gbiz的task 也包含rbiz的task 类型
        prev_data= self.get_prev_data(case,setup_type)
        copy_prev_data = copy.deepcopy(prev_data)
        if BaseUtils.object_is_null(copy_prev_data):
            return

        for prev in copy_prev_data:
            print(prev.prev_id)
            self.common_util.wait_exec_time(prev.prev_wait_time)
            prev_task_type = prev.prev_task_type
            if prev_task_type =="task":
                common_task = self.prev_get_taskmsg_id(prev,vars)
                for task in common_task:
                    if prev.prev_flag.lower()==task.task_type.lower():
                        try:
                            temp_prev=None
                            temp_prev = copy.deepcopy(prev)
                            task_result = self.process_prev_request(temp_prev,task,vars,prev_task_type,prev.prev_sql_database)
                        finally:
                            self.bustools.write_history_prev(temp_prev,run_id)
                        if task_result is not None and task_result!=True:
                            #BaseUtils.set_casestatus_fail("task="+prev.prev_flag+" prev_id = " +str(prev.prev_id))
                            raise Exception("task="+prev.prev_flag+" prev_id = " +str(prev.prev_id))
            elif prev_task_type=="msg":
                common_task = self.prev_get_taskmsg_id(prev,vars)
                for msg in common_task:
                    if prev.prev_flag.lower()==msg.sendmsg_type.lower():
                        try:
                            temp_prev=None
                            temp_prev = copy.deepcopy(prev)
                            msg_result = self.process_prev_request(temp_prev,msg,vars,prev_task_type,prev.prev_sql_database)
                        finally:
                            self.bustools.write_history_prev(temp_prev,run_id)
                        if msg_result !=True:
                            #BaseUtils.set_casestatus_fail("msg="+prev.prev_flag +" prev_id = " +str(prev.prev_id))
                            raise Exception("msg="+prev.prev_flag +" prev_id = " +str(prev.prev_id))



    def prev_get_taskmsg_id(self,prev,vars):
        sql_statement = self.bustools.repalce_system_params(prev.prev_sql_statement,vars=vars)
        sql_database = prev.prev_sql_database
        sql_params = BaseUtils.transfer_string_to_dict(prev.prev_sql_params)
        key_value = self.bustools.repalce_system_params(prev.prev_sql_expression,vars=vars)
        sql_params = BaseUtils.extend_value_target(vars,sql_params,key_value)
        sql_params = self.bustools.repalce_system_params(sql_params,vars=vars)
        sql_database = self.bustools.repalce_system_params(sql_database,vars=vars)
        task = self.dao.exec_common_query(sql_statement,sql_database,sql_params)
        prev.prev_sql_statement=sql_statement
        prev.prev_sql_database = sql_database
        prev.prev_sql_params=sql_params
        return task


    def get_prev_data(self,case,setup_type):
        prev_data = []
        task_type_array=[]
        msg_type_array=[]
        task_type=''
        msg_type=''
        if BaseUtils.object_is_notnull(case.case_next_task):
            task_type=case.case_next_task
        if BaseUtils.object_is_notnull(case.case_next_msg):
            msg_type = case.case_next_msg
        case_id = case.case_id
        if BaseUtils.object_is_notnull(task_type):
            task_type_array = task_type.split(",")
        if BaseUtils.object_is_notnull(msg_type):
            msg_type_array = msg_type.split(",")

        for _task_type in task_type_array:
            task_prev = self.biz_dao.get_prev_condition_by_tasktype(case_id,_task_type,setup_type)
            if BaseUtils.object_is_null(task_prev):
                task_prev = self.biz_dao.get_prev_condition_by_tasktype(0,_task_type,setup_type)
            if BaseUtils.object_is_notnull(task_prev):
                for task in task_prev:
                    prev_data.append(task)
        for _msg_type in msg_type_array:
            msg_prev = self.biz_dao.get_prev_condition_by_tasktype(case_id,_msg_type,setup_type)
            if BaseUtils.object_is_null(msg_prev):
                msg_prev =self.biz_dao.get_prev_condition_by_tasktype(-1,_msg_type,setup_type)
            if BaseUtils.object_is_notnull(msg_prev):
                for msg in msg_prev:
                    prev_data.append(msg)

        task_prev = self.biz_dao.gettaskandmsg_bycase_id(case_id,setup_type)
        if BaseUtils.object_is_notnull(task_prev):
            for task in task_prev:
                prev_data.append(task)

        return prev_data


    def process_prev_request(self,prev,task,case_vars,task_type,env,retry_times=0):
        #task_id = task.task_id
        url = prev.prev_api_address
        method = prev.prev_api_method
        header= prev.prev_api_header
        params = self.bustools.repalce_system_params(prev.prev_api_params,vars=case_vars)
        #key_value = prev.prev_api_expression
        except_value = BaseUtils.transfer_string_to_dict(prev.prev_except_value)
        url = self.bustools.repalce_system_params(url,vars=case_vars)
        url_get_param = BaseUtils.extend_value_target(BaseUtils.transfer_entity_to_dict(task),params,prev.prev_api_expression)
        url = self.bustools.replace_user_params(url,url_get_param)
        result = self.http_util.http_request(url,params,method,header)
        result_entity = BaseUtils.transfer_string_to_dict(result)
        env = self.bustools.repalce_system_params(env,vars=case_vars)
        prev.prev_api_address=url
        prev.prev_api_params = params
        #FinlabAssert.assert_result(except_value,result_entity)
        result =True

        for key_path ,key_value in except_value.items():
            except_code_value = BaseUtils.get_josn_firstvalue(result_entity,key_path)
            if except_code_value != key_value and retry_times>0:
                try:
                    if task_type =="task":
                        self.biz_dao.update_task_by_taskid(task.task_id,env)
                    else:
                        self.biz_dao.update_msg_by_taskid(task.sendmsg_id,env)
                    retry_times = retry_times - 1
                    self.process_prev_request(prev,task,case_vars,task_type,env,retry_times)
                except Exception as e:
                    print(e)
                finally:
                    retry_times = retry_times - 1
                    self.process_prev_request(prev,task,case_vars,task_type,env,retry_times)
                    break
            if except_code_value != key_value:
                return False

        return result

    def prev_actual_value(self,prev_entity,case,vars):
        if self.judge_prev_exists(case):
            actual_value = case.actual_value
            actual_value_dict = self.process_string_todict(actual_value)
            case.actual_value = BaseUtils.transfer_dict_to_string(actual_value_dict)
        return case

    def process_string_todict(self,value):
        actual_value_dict = BaseUtils.transfer_string_to_dict(value)
        if isinstance(actual_value_dict,list):
            for actual_value_dict_single in actual_value_dict:
                for key ,value in list(actual_value_dict_single.items()):
                    value = BaseUtils.transfer_string_to_dict(value)
                    actual_value_dict_single[key]=value
        else:
            for key ,value in list(actual_value_dict.items()):
                value =BaseUtils.transfer_string_to_dict(value)
                actual_value_dict[key] =value
        return BaseUtils.transfer_dict_to_string(actual_value_dict)


    def judge_prev_exists(self,case):
        prev_entity = self.biz_dao.judge_prev_exists(case.case_id)
        if prev_entity is None or len(prev_entity)==0:
            return False
        elif prev_entity is not None and len(prev_entity)>0:
            return True

    def four_important_element(self,prev_entity,case,vars):
        params = case.case_api_params
        keyvalue= prev_entity.prev_expression
        params = BaseUtils.extend_value_target(vars,params,keyvalue)
        params = self.bustools.repalce_system_params(params,vars=vars)
        user_params = prev_entity.prev_params
        case.case_api_params = self.bustools.replace_user_params(params,user_params)
        return case

    def prev_except_response_value(self,prev_entity,case,vars):
        return self.common_extend_params(prev_entity,case,vars)

    def common_extend_params(self,prev_entity,case,vars):
        expression = prev_entity.prev_except_expression
        request_params = case.case_except_value
        request_params = self.bustools.repalce_system_params(request_params,vars=vars)
        request_params = BaseUtils.extend_value_target(vars,request_params,expression)
        case.case_except_value = BaseUtils.transfer_dict_to_string(request_params)
        return case


    def prev_except_value(self,prev_entity,case,vars):
        return self.common_extend_params(prev_entity,case,vars)



    def extend_mainresponse_torequestbody(self,prev_entity,case,vars):
        key_value = prev_entity.prev_expression
        request_params = case.case_api_params
        request_params = self.bustools.repalce_system_params(request_params,vars=vars)
        request_params_dict = BaseUtils.extend_value_target(vars,request_params,key_value)
        case.case_api_params = BaseUtils.transfer_dict_to_string(request_params_dict)
        return case



    def test_example_prev(self,prev_entity,case,vars):
        request_params = case.case_api_params
        key_value = prev_entity.prev_expression
        result = self.biz_dao.get_withhold_amount("201231213","gbiz9")
        request_params_dict = BaseUtils.extend_value_target(result,request_params,key_value)
        case.case_api_params = BaseUtils.transfer_dict_to_string(request_params_dict)
        return case


    def prev_login_easymock(self,prev_entity,case,vars):
        url = self.bustools.repalce_system_params(prev_entity.prev_api_address,vars=vars)
        params = self.bustools.repalce_system_params(prev_entity.prev_api_params,vars=vars)
        method = self.bustools.repalce_system_params(prev_entity.prev_api_method,vars=vars)
        header = self.bustools.repalce_system_params(prev_entity.prev_api_header,vars=vars)
        expression = self.bustools.repalce_system_params(prev_entity.prev_api_expression,vars=vars)
        params_dict = BaseUtils.extend_value_target(vars,params,expression)
        result = self.http_util.http_request(url,params_dict,method,header)
        token = "Bearer "+BaseUtils.get_josn_firstvalue(result,"$.data.token")
        token_dict = {
            "Authorization":token
        }
        case.case_vars_name = "easy_mock"
        BaseUtils.set_vars("em_req",token_dict,case,vars)




    def update_easymock(self,prev_entity,case,vars):
        #登陆easymock
        url = self.bustools.repalce_system_params("#{easymock_url}",vars=vars)
        params = self.bustools.repalce_system_params("#{easymock_login_default_params}",vars=vars)
        method = "POST"
        header = {"Content-Type":"application/json"}
        result = self.http_util.http_request(url,params,method,header)
        token = "Bearer "+BaseUtils.get_josn_firstvalue(result,"$.data.token")
        token_dict = {
            "Authorization":token
        }
        if BaseUtils.object_is_null(case.case_vars_name):
            case.case_vars_name = "easy_mock"
        path = "$.{0}_{1}.Authorization".format(case.case_vars_name,"em_req")
        BaseUtils.set_vars("em_req",token_dict,case,vars)
        update_header = BaseUtils.get_josn_firstvalue(vars,path)
        header['Authorization'] = update_header
        easymock_url = self.bustools.repalce_system_params(prev_entity.prev_api_address,vars=vars)
        easymock_params = self.bustools.repalce_system_params(prev_entity.prev_api_params,vars=vars)
        easymock_method = self.bustools.repalce_system_params(prev_entity.prev_api_method,vars=vars)
        easymock_expression = self.bustools.repalce_system_params(prev_entity.prev_api_expression,vars=vars)
        if BaseUtils.object_is_notnull(easymock_expression):
            easymock_params = BaseUtils.extend_value_target(vars,easymock_params,easymock_expression)
            easymock_params = BaseUtils.transfer_string_to_dict(easymock_params)
            easymock_params['mode'] = BaseUtils.transfer_dict_to_string(easymock_params['mode'])
        result = self.http_util.http_request(easymock_url,easymock_params,easymock_method,header)
        result_dict = BaseUtils.transfer_string_to_dict(result)
        if(result_dict['code']!=200 or result_dict['success']==False):
            #BaseUtils.set_casestatus_fail("update easymock fail"+str(result))
            raise Exception("运行前置处理{0}失败,msg:{1}".format("update easymock",str(result)) )


    def add_easymock(self,prev_entity,case,vars):
        #登陆easymock
        url = self.bustools.repalce_system_params("#{easymock_url}",vars=vars)
        params = self.bustools.repalce_system_params("#{easymock_login_default_params}",vars=vars)
        method = "POST"
        header = {"Content-Type":"application/json"}
        result = self.http_util.http_request(url,params,method,header)
        token = "Bearer "+BaseUtils.get_josn_firstvalue(result,"$.data.token")
        token_dict = {
            "Authorization":token
        }
        if BaseUtils.object_is_null(case.case_vars_name):
            case.case_vars_name = "easy_mock"
        path = "$.{0}_{1}.Authorization".format(case.case_vars_name,"em_req")
        BaseUtils.set_vars("em_req",token_dict,case,vars)
        update_header = BaseUtils.get_josn_firstvalue(vars,path)
        header['Authorization'] = update_header
        easymock_url = self.bustools.repalce_system_params(prev_entity.prev_api_address,vars=vars)
        easymock_params = self.bustools.repalce_system_params(prev_entity.prev_api_params,vars=vars)
        easymock_method = self.bustools.repalce_system_params(prev_entity.prev_api_method,vars=vars)
        easymock_expression = self.bustools.repalce_system_params(prev_entity.prev_api_expression,vars=vars)
        if BaseUtils.object_is_notnull(easymock_expression):
            easymock_params = BaseUtils.extend_value_target(vars,easymock_params,easymock_expression)
            easymock_params = BaseUtils.transfer_string_to_dict(easymock_params)
            easymock_params['mode'] = BaseUtils.transfer_dict_to_string(easymock_params['mode'])
        result = self.http_util.http_request(easymock_url,easymock_params,easymock_method,header)
        result_dict = BaseUtils.transfer_string_to_dict(result)
        if(result_dict['code']!=200 or result_dict['success']==False):
            if result_dict['message']=="请检查接口是否已经存在":
                return
            #BaseUtils.set_casestatus_fail("add_easymock fail")
            raise Exception("运行前置处理{0}失败,msg:{1}".format("add_easymock fail",str(result)) )





    def add_params_tovars_bysql(self,prev_entity,case,vars):
        sql_statement = self.bustools.repalce_system_params(prev_entity.prev_sql_statement,vars=vars)
        sql_params = self.bustools.repalce_system_params(prev_entity.prev_sql_params,vars=vars)
        database = self.bustools.repalce_system_params(prev_entity.prev_sql_database,vars=vars)
        expression = self.bustools.repalce_system_params(prev_entity.prev_sql_expression,vars=vars)
        params_dict = BaseUtils.extend_value_target(vars,sql_params,expression)
        result = self.dao.exec_common_query_dict(sql_statement,database,params_dict)
        BaseUtils.set_vars("sql_prev_response",result,case,vars)
        return result


    def add_params_tovars_byhttp(self,prev_entity,case,vars):
        url = self.bustools.repalce_system_params(prev_entity.prev_api_address,vars=vars)
        params = self.bustools.repalce_system_params(prev_entity.prev_api_params,vars=vars)
        method = self.bustools.repalce_system_params(prev_entity.prev_api_method,vars=vars)
        header = self.bustools.repalce_system_params(prev_entity.prev_api_header,vars=vars)
        expression = self.bustools.repalce_system_params(prev_entity.prev_api_expression,vars=vars)
        params_dict = BaseUtils.extend_value_target(vars,params,expression)
        result = self.http_util.http_request(url,params_dict,method,header)

        BaseUtils.set_vars("http_prev_response",result,case,vars)
        return result

    def exec_prev_api(self,prev_entity,case,vars):
        url = self.bustools.repalce_system_params(prev_entity.prev_api_address,vars=vars)
        if BaseUtils.object_is_notnull(url):
            except_value = self.bustools.repalce_system_params(prev_entity.prev_except_value,vars=vars)
            acutal_value = self.add_params_tovars_byhttp(prev_entity,case,vars)
            FinlabAssert.assert_result(except_value,acutal_value,vars)

    def exec_prev_sql(self,prev_entity,case,vars):
        sql_statement = self.bustools.repalce_system_params(prev_entity.prev_sql_statement,vars=vars)
        if BaseUtils.object_is_notnull(sql_statement):
            except_value = self.bustools.repalce_system_params(prev_entity.prev_except_value,vars=vars)
            acutal_value = self.add_params_tovars_bysql(prev_entity,case,vars)
            FinlabAssert.assert_result(except_value,acutal_value,vars)

    def exec_prev_reqeust(self,prev_entity,case,vars):
        url = self.bustools.repalce_system_params(prev_entity.prev_api_address,vars=vars)
        sql_statement = self.bustools.repalce_system_params(prev_entity.prev_sql_statement,vars=vars)
        if BaseUtils.object_is_notnull(url):
            self.exce_prev_api(prev_entity,case,vars)
        if BaseUtils.object_is_notnull(sql_statement):
            self.exce_prev_sql(prev_entity,case,vars)



