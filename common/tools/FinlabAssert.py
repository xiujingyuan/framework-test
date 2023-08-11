# -*- coding: utf-8 -*-
# @Title: FinlabAssert
# @ProjectName framework-test
# @Description: TODO
# @author fyi zhang
# @date 2018/11/2922:45

import re

from common.tools.BaseUtils import BaseUtils

class FinlabAssert(object):

    @classmethod
    def assert_result(cls,except_result,actual_result,case_vars):
        '''
            :param actual_value:
            :return:
        '''
        except_result_dict = BaseUtils.transfer_string_to_dict(except_result)
        for except_key,except_value in except_result_dict.items():
            params ={}
            value = None
            operator_style = "eq"
            is_ingnore_case =True
            actual_value_from=""
            except_value_from=""

            if isinstance(except_value,list):
                if len(except_value) ==5:
                    value = except_value[0]
                    operator_style = except_value[1]
                    is_ingnore_case = bool(except_value[2])
                    actual_value_from = except_value[3]
                    except_value_from =except_value[4]
                elif len(except_value)==4:
                    value = except_value[0]
                    operator_style = except_value[1]
                    is_ingnore_case = bool(except_value[2])
                    actual_value_from = except_value[3]
                elif len(except_value) == 3:
                    value = except_value[0]
                    operator_style = except_value[1]
                    is_ingnore_case = bool(except_value[2])
                elif len(except_value)==2:
                    value = except_value[0]
                    operator_style = except_value[1]
                elif len(except_value)==1:
                    value = except_value[0]
            else:
                value = except_value
            if actual_value_from=="vars":
                actual_value = cls.get_special_value(except_key,case_vars)
            else:
                actual_value = cls.get_special_value(except_key,actual_result)
            except_value_tmp = cls.get_special_value(value,case_vars)
            if operator_style is None or operator_style =="":
                operator_style = "eq"
            if is_ingnore_case is None or is_ingnore_case =="":
                is_ingnore_case = False
            cls.assert_match_value(except_value_tmp,actual_value,operator_style,is_ingnore_case,case_vars)



    @classmethod
    def assert_match_value(cls,except_value,actual_value,operator_style,is_ingnore_case,case_vars):
        '''
        -gt 预期值是否大于实际值
        -ge 预期值是否大于等于实际值
        -eq 预期值是否等于实际值
        -ne 预期值是否不等于实际值
        -lt 预期值是否小于实际值
        -le 预期值是否小于等于实际值
        -en 实际值为None 或者空字符串
        -nn 实际值不为None 且不为空字符
        -ec 预期值是否被包含于实际值中
        -nc 预期值不被包含在实际值中
        -rec 实际值是否被包含于逾期值中
        -rnc 实际值不被包含在预期值中
        -re 实际值正则表示匹配预期字符串
    '''
        exception_message = "except_value: {0} ,actual_value: {1} " \
                            "在比对方式:{2} 并且忽略大小写为:{3}" \
                            " 的情况下比对失败".\
                            format(str(except_value),str(actual_value),
                                   operator_style,str(is_ingnore_case))

        if isinstance(except_value,(int,float))==False or isinstance(actual_value,(int,float))==False:
            except_value = str(except_value)
            actual_value = str(actual_value)
        if isinstance(except_value,(int,float)) or isinstance(actual_value,(int,float)):
            is_ingnore_case=False
        except_value,actual_value = cls.transfer_ingnore_case(except_value,actual_value,is_ingnore_case,case_vars)
        if operator_style =="eq" or operator_style=="==":
            assert except_value == actual_value,exception_message
        elif operator_style=="gt" or operator_style==">":
            assert except_value > actual_value,exception_message
        elif operator_style=="ge"  or operator_style==">=":
            assert except_value >= actual_value,exception_message
        elif operator_style =="ne" or operator_style=="!=" or operator_style=="<>":
            assert except_value!=actual_value,exception_message
        elif operator_style =="lt" or operator_style=="<":
            assert except_value<actual_value,exception_message
        elif operator_style=="le" or operator_style=="<=":
            assert except_value <= actual_value,exception_message
        elif operator_style =="en" or operator_style.lower()=="none":
            assert (actual_value is None or actual_value ==""),exception_message
        elif operator_style =="nn"or operator_style.lower()=="not none":
            assert (actual_value is not None and actual_value!=""),exception_message
        elif operator_style=="ec" or operator_style.lower()=="in":
            assert except_value in actual_value ,exception_message
        elif operator_style=="nc" or operator_style.lower()=="not in":
            assert except_value not in actual_value,exception_message
        elif operator_style=="rec" or operator_style.lower()=="rin":
            assert actual_value in except_value ,exception_message
        elif operator_style=="rnc"or operator_style.lower()=="rnot in":
            assert actual_value not in except_value,exception_message
        elif operator_style=="re" or operator_style.lower()=="regex":
            pattern = re.compile(except_value)
            assert re.match(pattern,actual_value) is not None ,exception_message
        else:
            assert except_value == actual_value,exception_message


    @classmethod
    def assert_match_path(cls,key_value,target,actual_result):
        key_value_dict = BaseUtils.transfer_string_to_dict(key_value)
        target_dict = BaseUtils.transfer_string_to_dict(target)
        actual_result_dict = BaseUtils.transfer_string_to_dict(actual_result)
        for except_path,actual_path in key_value_dict.items():
            except_value = BaseUtils.get_josn_firstvalue(target_dict,except_path)
            actual_value = BaseUtils.get_josn_firstvalue(actual_result_dict,actual_path)
            is_ingnore_case = True
            operator_style = "eq"
            cls.assert_match_value(except_value,actual_value,operator_style,is_ingnore_case)


    @classmethod
    def transfer_ingnore_case(cls,except_value,actual_value,is_ingnore_case,case_vars):
        if is_ingnore_case:
            return except_value.lower(),actual_value.lower()
        else:
            return except_value,actual_value

    @classmethod
    def get_special_value(cls,except_value,case_vars):
        if isinstance(except_value,str) and len(except_value)>0:
            if except_value[0]=="$":
                value = BaseUtils.get_josn_firstvalue(case_vars,except_value)
            else:
                value = except_value
        else:
            value = except_value
        return value










