# -*- coding: utf-8 -*-
# @Time    : 公元18-12-21 下午8:10
# @Author  : 张廷利
# @Site    : 
# @File    : BusTools.py
# @Software: IntelliJ IDEA

import re
import random
import datetime as dt
import time
import initial.InitMysql as InitMysql

from datetime import datetime
from dateutil.relativedelta import relativedelta
from common.tools.BaseUtils import BaseUtils
from framework.dao.FrameworkDAO import FrameworkDAO
from bussiness.biz.HistoryCaseBiz import HistoryCaseBiz
from models.framework.HistoryFinlabCaseDb import HistoryFinlabCase
from bussiness.biz.HistoryInitBiz import HistoryInitBiz
from bussiness.biz.HistoryPrevBiz import HistoryPrevBiz
from models.framework.HistoryPrevModel import HistoryPrevModel
from models.framework.HistoryInitModel import HistoryInitModel




class BusTools(object):

    def __init__(self):
        self.dao = FrameworkDAO()

    def repalce_system_params(self,params,_datetime=None,vars=None):
        '''
        通过正则表达式，提取params 中的参数所有#{}中的参数
        两个想法：
        1.直接替换传进来的参数。这里面的参数名称是配置参数表中的。
        2.值的话有两种，传进来参数中某个字段的值，如果是时间就是系统时间
        #{system_date} 系统当前时间
        #{system_1_30_day} 系统时间加30天
        #{system_1_month} 系统时间加1个月
        #{system_2_month} 系统时间加2个月
        #{system_3_month} 系统时间加3个月
        #{auto_item_no} 资产编号
        paramsname ,type, value, action
        system_date,day,  0 ,add
        system_30_day ,day,30,add

        :param params:
        :return:
        '''
        if BaseUtils.object_is_null(params):
            return params
        params = self.repalce_regex_params(params,vars)
        params = self.replace_global_params(params,vars)
        pattern = re.compile(r'#{.+?}')
        result= pattern.findall(params)
        all_params = set(result)
        if _datetime is not None :
            now = BaseUtils.string_to_datetime(_datetime)
        else:
            now = datetime.now()
        for r in all_params:
            r_key = r.replace("#{","").replace("}","")
            value = None
            system_key = self.dao.get_special_keyvalue(r_key)
            if  system_key is not None :
                key_config_type = system_key.type
                key_config_value  = system_key.value
                key_config_action = system_key.action
                if key_config_action.lower() == 'add':
                    if key_config_type.lower()=='day':
                        key_config_value = int(key_config_value)
                        delta=dt.timedelta(days=+key_config_value)
                        value = BaseUtils.date_to_datetime(now+delta)
                    elif key_config_type.lower()=='month':
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() + relativedelta(months=+key_config_value)
                        value = BaseUtils.date_to_datetime(value)
                    elif key_config_type.lower()=='datetime':
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() + relativedelta(days=+key_config_value)
                        value = BaseUtils.date_to_datetime(value)
                    elif key_config_type.lower()=='nonedatetime':
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() + relativedelta(days=+key_config_value)
                        value = BaseUtils.date_to_datetime(value)
                    elif key_config_type.lower()=="millisecond":
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() + relativedelta(days=-key_config_value)
                        value = BaseUtils.date_to_datetime(value)
                        value=time.strptime(value,"%Y-%m-%d %H:%M:%S")
                        value=int(time.mktime(value))
                        value=str(value)
                    elif key_config_type.lower()=="enddatetime":
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() + relativedelta(days=+key_config_value)
                        value.strftime("%Y-%m-%d")
                        value=str(value)+" 23:59:59"
                        value=str(value)

                elif key_config_action.lower() =='division':
                    if key_config_type.lower()=='day':
                        key_config_value = int(key_config_value)
                        delta=dt.timedelta(days=-key_config_value)
                        value = BaseUtils.date_to_datetime(now+delta)
                    elif key_config_type.lower()=='month':
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() - relativedelta(months=+key_config_value)
                        value = BaseUtils.date_to_datetime(value)
                    elif key_config_type.lower()=='datetime':
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() - relativedelta(days=+key_config_value)
                        value = BaseUtils.date_to_datetime(value)
                    elif key_config_type.lower()=='nonedatetime':
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() + relativedelta(days=-key_config_value)
                        value = BaseUtils.date_to_datetime(value)
                    elif key_config_type.lower()=="millisecond":
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() + relativedelta(days=-key_config_value)
                        value = BaseUtils.date_to_datetime(value)
                        value=time.strptime(value,"%Y-%m-%d %H:%M:%S")
                        value=int(time.mktime(value))
                        value=str(value)
                    elif key_config_type.lower()=="enddatetime":
                        key_config_value = int(key_config_value)
                        value = datetime.date(now).today() + relativedelta(days=-key_config_value)
                        value.strftime("%Y-%m-%d")
                        value=str(value)+" 23:59:59"
                        value=str(value)

                elif key_config_action.lower() =='replace':
                    if key_config_type=='radom':
                        value = BaseUtils.get_uuid()
                    elif key_config_type=='normal':
                        value = key_config_value
                    elif key_config_type =="radom_num":
                        #并发时不能保证唯一性
                        datestring = now.strftime("%Y%m%d%H%M%S")
                        randomstring = str(random.randint(0,1000))
                        value = datestring +randomstring
            value = str(value)
            p = re.compile(r)
            params =re.sub(p,value,params)
        return params

    def replace_global_params(self,params,vars=None):

        if vars is None:
            return params
        if BaseUtils.object_is_null(params):
            return params
        params = BaseUtils.transfer_dict_to_string(params)
        pattern = re.compile(r'#{{.+?}}')
        result= pattern.findall(params)
        all_params = set(result)

        for single_params in all_params:
            json_path = single_params.replace("#{{","").replace("}}","")
            value = BaseUtils.get_josn_firstvalue(vars,json_path)
            single_params = self.replace_spcial_symbol(single_params)
            p = re.compile(single_params)
            value = str(value)
            params =re.sub(p,value,params)
        return params

    def repalce_regex_params(self,params,vars=None):
        if vars is None:
            return params
        if BaseUtils.object_is_null(params):
            return params
        params = BaseUtils.transfer_dict_to_string(params)
        pattern = re.compile(r'&{.+?}')
        result= pattern.findall(params)
        all_params = set(result)
        vars_string = BaseUtils.transfer_dict_to_string(vars)
        for single_params in all_params:
            regex_list = single_params.replace("&{","").replace("}","").split(',')
            regex = regex_list[0]
            if len(regex_list)==2:
                jsonpath = regex_list[1]
            else:
                jsonpath=None
            single_pattern = re.compile(regex)
            if BaseUtils.object_is_null(jsonpath):
                value = single_pattern.findall(vars_string)
            else:
                value_string = BaseUtils.get_josn_firstvalue(vars,jsonpath)
                replace_string = BaseUtils.transfer_dict_to_string(value_string)
                value = single_pattern.findall(replace_string)
            single_params = self.replace_spcial_symbol(single_params)
            p = re.compile(single_params)
            value = str(value[0])
            params =re.sub(p,value,params)
        return params




    def replace_spcial_symbol(self,params):
        special_symbol =['$','(',')','*','+','[',']','?','^','|','\\']
        for ss in special_symbol:
            if ss in params:
                params = params.replace(ss,'.')
        return params



    def replace_user_params(self,target,key_value):
        '''
        通过正则表达式，提取params 中的参数所有#{}中的参数
        两个想法：
        1.直接替换传进来的参数。这里面的参数名称是配置参数表中的。
        2.值的话有两种，传进来参数中某个字段的值，如果是时间就是系统时间
        #{system_date} 系统当前时间
        #{system_1_30_day} 系统时间加30天
        #{system_1_month} 系统时间加1个月
        #{system_2_month} 系统时间加2个月
        #{system_3_month} 系统时间加3个月
        #{auto_item_no} 资产编号
        paramsname ,type, value, action
        system_date,day,  0 ,add
        system_30_day ,day,30,add
        :param params:
        :return:
        '''
        expression_key_value = None
        #{} 参数替换
        expression_key_value = BaseUtils.transfer_string_to_dict(key_value)
        pattern = re.compile(r'{{.+?}}')
        result = pattern.findall(target)
        all_params = set(result)
        for r in all_params:
            r_key = r.replace("{{","").replace("}}","")
            value = None
            if r_key in expression_key_value:
                value = expression_key_value[r_key]
            else:
                continue
            p = re.compile(r)
            value = str(value)
            target = re.sub(p,value,target)
        return target


    def write_history(self,case,case_except_value,case_actual_value,vars,run_id,status):
        history_case = HistoryFinlabCase()
        
        for case_key in case.get_attrs():
            history_key = "history_{0}".format(case_key)
            value = getattr(case, case_key)
            setattr(history_case, history_key, value)
        history_case.history_case_except_value = BaseUtils.transfer_dict_to_string(case_except_value)
        history_case.history_case_actual_value = BaseUtils.transfer_dict_to_string(case_actual_value)
        history_case.history_case_vars = BaseUtils.transfer_dict_to_string(vars)
        history_case.history_case_result = status
        history_case.run_id= run_id
        history_case.history_case_in_date=datetime.now()
        history_case.history_case_last_date =datetime.now()
        HistoryCaseBiz.add_history_case(history_case)

    def write_history_prev(self,prev_entity,run_id):
        history_prev = HistoryPrevModel()
        history_prev.__dict__.update(BaseUtils.transfer_entity_to_dict(prev_entity))
        history_prev.run_id = run_id
        HistoryPrevBiz.add_history_prev(history_prev)


    def write_history_init(self,init_entity,run_id):
        history_init = HistoryInitModel()
        history_init.__dict__.update(BaseUtils.transfer_entity_to_dict(init_entity))
        history_init.run_id = run_id
        HistoryInitBiz.add_history_init(history_init)





