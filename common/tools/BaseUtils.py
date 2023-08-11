# -*- coding: utf-8 -*-
# @Time    : 公元18-11-26 下午4:26
# @Author  : 张廷利
# @Site    :
# @File    : BaseUtils.py
# @Software: IntelliJ IDEA

import json
import datetime
import copy
import jsonpath
import re
import uuid
import traceback
import pytest


def strisnull(func):
    """
    判断方法传入参数为空，如果为空返回错误信息。
    """

    def _deco(*args, **kwargs):

        try:
            for index, key in enumerate(args):
                if BaseUtils.object_is_null(key):
                    ret = "第{0}个参数为空，请检查".format(index)
                    raise ValueError(ret)
            for key,value in kwargs.items():
                if BaseUtils.object_is_null(value):
                    ret = "参数{0}: 为空".format(key)
                    raise ValueError(ret)
        except Exception as err:
            print(err)
        else:
            ret = func(*args, **kwargs)
        return ret

    return _deco


def catch_exception(func):
    '''
    捕获异常的装饰器。统一异常捕获。
    :param func:
    :return:
    '''
    def catch_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            funcation_name = func.__name__
            exception_message ="程序在运行方法：{0} 时，发生异常,异常信息如下: {1}";
            msg = traceback.format_exc()
            #pytest.fail(exception_message.format(funcation_name,msg),False)
            raise Exception
    return catch_function





class BaseUtils(object):

    @classmethod
    def object_is_null(cls,params):
        ret = False
        if params is None:
            ret= True
        elif isinstance(params,int):
            if params <=0:
                ret= True
            else:
                ret= False
        elif isinstance(params,str):
            if params=='':
                ret= True
            else:
                ret= False
        elif isinstance(params,(list,tuple,set)):
            if len(params)==0:
                ret = True
            else:
                ret = False
        return ret


    @classmethod
    def object_is_notnull(clc,params):
        ret=False
        if params is None:
            ret= False
        elif isinstance(params,str):
            if params !='' and params is not None:
                ret= True
        elif isinstance(params,int):
            if params > 0:
                ret= True
        elif isinstance(params,(list,tuple,set)):
            if len(params)>0:
                ret = True
            else:
                ret = False
        else:
            ret= True
        return ret


    @classmethod
    def transfer_dict_to_string(cls,source_dict):
        '''
        字段转换成字符串
        :return:
        '''
        if source_dict is None or (isinstance(source_dict,(int,float))==False and len(source_dict)==0) :
            return ""
        if isinstance(source_dict,dict):
            return json.dumps(source_dict)
        elif isinstance(source_dict,tuple):
            return json.dumps(source_dict)
        elif isinstance(source_dict,list):
            return json.dumps(source_dict)
        else:
            return source_dict

    @classmethod
    def date_to_datetime(cls,date_time=None):
        if date_time is None:
            date_time = datetime.now()
        return date_time.strftime("%Y-%m-%d %H:%M:%S")

    @classmethod
    def string_to_datetime(cls,date_string):
        return datetime.strptime(date_string,"%Y-%m-%d %H:%M:%S")

    @classmethod
    def get_uuid(cls):
        return str(uuid.uuid1())

    @classmethod
    @catch_exception
    def transfer_string_to_dict(cls,source_string):
        try:
            if cls.object_is_null(source_string):
                return {}
            if isinstance(source_string, bytes):
                source_string = source_string.decode()
            if isinstance(source_string, dict):
                return source_string
            elif isinstance(source_string, list):
                return source_string
            elif isinstance(source_string, tuple):
                return list(source_string)
            elif isinstance(source_string, datetime.datetime):
                return source_string
            elif isinstance(source_string, (int, float)):
                return source_string
            else:
                return json.loads(source_string, encoding='utf-8')
        except Exception as e:
            if isinstance(source_string, (str, bytes)):
                return source_string
            else:
                raise Exception("字符串转字典失败")

    @classmethod
    def transfer_entity_to_dict(cls,entity):
        if BaseUtils.object_is_notnull(entity):
            return entity.__dict__

    @classmethod
    def transfer_dict_to_entity(cls,param_dict):
        if BaseUtils.object_is_null(param_dict):
            return param_dict
        param_dict = BaseUtils.transfer_string_to_dict(param_dict)
        if isinstance(param_dict,dict):
            comm = CommonEntity(param_dict)
            return copy.deepcopy(comm)
        if isinstance(param_dict,(set,list,tuple)):
            objects=[]
            for p in param_dict:
                comm = CommonEntity(p)
                temp = copy.deepcopy(comm)
                del comm
                objects.append(temp)
            return objects

    @classmethod
    @catch_exception
    def get_josn_firstvalue(cls, json_dict, json_path):

        # value_dict = cls.transfer_string_to_dict(json_dict)
        # try:
        #     value = jsonpath.jsonpath(value_dict, json_path)[0]
        # except Exception as ke:
        #     # raise Exception("在目标json中没有对应的key:{0} 在目标字典:{1} "
        #     #                 "没有找到".format(json_path,cls.transfer_dict_to_string(dict)))
        #     value = "在目标json中没有对应的key:{0} 在目标字典:{1} 没有找到".format(json_path, json_dict, ke)
        # else:
        #     value = None
        # return value

        value=None
        dict = cls.transfer_string_to_dict(json_dict)
        try:
            value = jsonpath.jsonpath(dict,json_path)[0]
        except Exception as ke :
            if value is None:
                split_data=str(json_path).split('^',1)
                split_json_data=split_data[0]
                tmp_value=jsonpath.jsonpath(dict,split_json_data)[0]
                try:
                    tmp_value=json.loads(tmp_value)
                    new_json_path="$"+str(split_data[1])
                    value=jsonpath.jsonpath(tmp_value, new_json_path)[0]
                except:
                    raise Exception("在目标json中没有对应的key:{0} 在目标字典:{1} "
                                    "没有找到".format(json_path, cls.transfer_dict_to_string(dict)))


        return value

    @classmethod
    def get_json_allvalue(cls,json_dict,json_path):
        value=None
        dict = cls.transfer_string_to_dict(json_dict)
        try:
            value = jsonpath.jsonpath(json_dict,json_path)
        except KeyError as e:
            raise Exception("在目标json中没有对应的key:{0} 在目标字典:{1} "
                            "没有找到".format(json_path,cls.transfer_dict_to_string(dict)))
        return value


    @classmethod
    def extend_value_target(cls,from_params,params,key_value):
        from_params_dict = cls.transfer_string_to_dict(from_params)
        params_dict = cls.transfer_string_to_dict(params)
        key_value_dict = cls.transfer_string_to_dict(key_value)
        for key_path,value_path in key_value_dict.items():
            value = cls.get_josn_firstvalue(from_params_dict,key_path)
            if isinstance(value_path,list):
                for path in value_path:
                    cls.set_value_for_jsonpath(params_dict,path,value)
            else:
                cls.set_value_for_jsonpath(params_dict,value_path,value)
        return cls.transfer_dict_to_string(params_dict)


    @classmethod
    def set_value_for_jsonpath(cls,target_dict,path,value):

        paths = cls.get_path_dict(path)
        for i in range(0,len(paths)-1,1):
            target_dict = target_dict[paths[i]]
            ++i
        endpath = paths[len(paths)-1]
        target_dict[endpath] =value
        return cls.transfer_dict_to_string(target_dict)

    #TODO

    @classmethod
    def get_path_dict(cls,json_path):
        '''
        将jsonpath 解析成数组，仅仅只能解析简单的jsonpath 路径
        所以如果需要设置一个复杂的jsonpath 路径，将会报错
        :param json_path:
        :return:
        '''
        resultpaths = []
        if "$.$" in json_path:
            resultpaths.append(json_path[2:])
            return resultpaths
        # 解析正常的json path 路径为数组
        paths = json_path.split('.')
        paths.remove("$")
        for path in paths:
            if path.endswith("]"):
                for array in path.split('['):
                    if array =="":
                        continue
                    if array.endswith("]"):
                        array = array.replace("]","")
                        resultpaths.append(int(array))
                        continue
                    else:
                        resultpaths.append(array)
            else:
                resultpaths.append(path)
        return resultpaths

    @classmethod
    def set_casestatus_fail(cls,task_name):
        exception_message ="程序在运行方法{0}时，失败";
        pytest.fail(exception_message.format(task_name),True)

    def is_contains_var(cls,param,flag="user"):
        '''
        判断字符中是否判断系统变量或者用户变量
        :param param: 需要判断的字符串
        :param flag: system ：系统变量，user ：用户变量
        :return: bool
        '''
        pattern =None
        if flag =="user":
            pattern = re.compile(r'{{.+?}}')
        else:
            pattern = re.compile(r'#{.+?}')

        result= pattern.findall(param)
        if cls.object_is_null(result):
            return False
        else:
            return True


    @classmethod
    def set_vars(cls, key, value, case,case_vars):
        if BaseUtils.object_is_notnull(value) and BaseUtils.object_is_notnull(case.case_vars_name):
            value_dict = BaseUtils.transfer_string_to_dict(value)
            key = case.case_vars_name+"_"+key
            if key not in case_vars.keys():
                case_vars[key] = value_dict


class CommonEntity(object):
    def __init__(self,param_dict):
        self.__dict__.update(param_dict)

