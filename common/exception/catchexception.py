# -*- coding: utf-8 -*-
# @Time    : 公元18-12-18 上午8:36
# @Author  : 张廷利
# @Site    : 
# @File    : catchexception.py
# @Software: IntelliJ IDEA
import inspect
import traceback
import sys

class CatchException(object):

    @classmethod
    def funcation_name(cls):
        return inspect.stack()[1][3]

    @classmethod
    def class_name(cls,object):
        return object.__class__.__name__


    @classmethod

    def get_current_error_point(cls,function_mame,object):
        exception_message ="程序在运行类: {0} 的方法：{1} 时，发生异常,异常信息如下: {2}";
        class_name = CatchException.class_name(object)
        msg = traceback.format_exc()
        exception_message = exception_message.format(class_name,function_mame,msg)
        return exception_message
