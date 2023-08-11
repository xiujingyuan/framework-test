#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm  
 @time: 2018/10/18
 @file: ClsTmms.py
 @site:
 @email:
"""


class ClsTmms(object):

    def __init__(self, case):
        self.case = case

    def run_case(self):
        """
        发送请求
        :return:
        """
        print("run_case")

    def init_data(self):
        """
        数据准备
        :return:
        """
        print("init_data")

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

