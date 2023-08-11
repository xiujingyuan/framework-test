#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm
 @time: 2018/10/10
 @file: test_class.py
 @site:
 @email:
"""
import os
import shutil
import threading
import time
import copy

import allure
import pytest

from conftest import USER_OPTIONS
from framework.FactoryBusiness import FactoryBusiness
from initial.InitMysql import init_mysql

from models.framework.RunCaseDb import RunCase
from bussiness.biz.FinlabCaseBiz import FinlabCaseBiz
from bussiness.biz.CaseRunBiz import CaseRunBiz
from framework.dao.FrameworkDAO import FrameworkDAO


class CopyReportThread(threading.Thread):
    def __init__(self, src, dst):
        super(CopyReportThread, self).__init__()
        parent_dir = os.path.abspath('..')
        self.src = os.path.join(parent_dir,src)
        self.dst = os.path.join(parent_dir,dst)


    def run(self):
        if os.path.exists(self.dst):
            os.remove(self.dst)
        while True:
            if len(os.listdir(self.src)) >=1:
                shutil.copytree(self.src, self.dst)
                break


def get_system_and_module():
    """
    通过pytest参数传递获取本次运行的系统和模块
    :return:
    """
    user_options = {}
    for option in USER_OPTIONS:
        user_options[option[2:]] = pytest.config.getoption(option, default=None)
    return user_options


USERS_OPTION_DICT = get_system_and_module()
CASE_CRITICAL = "critical11"
CASE_NAME = "CASE_NAME"
global RUN_ID



def get_run_cases():
    """
    获取本次运行的用例集
    :return:返回通过系统和模块查询到的用例集
    """
    ip = USERS_OPTION_DICT["ip"]
    port = USERS_OPTION_DICT["port"]
    user = USERS_OPTION_DICT["user"]
    pwd = USERS_OPTION_DICT["pwd"]
    database = USERS_OPTION_DICT["database"]
    init_mysql(ip, port, user, pwd, database)
    case_ids_str = USERS_OPTION_DICT["case_ids"]
    case_ids = case_ids_str.split(',')
    rets = FinlabCaseBiz.Query_Cases(case_ids)
    return copy.deepcopy(rets)


def get_run_cases_name():
    rets = get_run_cases()
    return map(lambda x: x.case_name, rets)


@allure.feature('{0}系统用例测试'.format(
    USERS_OPTION_DICT["project_system_name"]))  # feature定义功能
class TestRun(object):
    result = []
    cases = []
    run_total_case = None


    @classmethod
    def setup_class(cls):
        """
        用例执行初始化方法,获取用例执行的系统和模块
        :return:
        """

        # 获取参数
        cls.user_options = USERS_OPTION_DICT
        cls.project_system_name = cls.user_options["project_system_name"]
        cls.system_module = cls.user_options["system_module"]

        # 初始化数据库连接
        ip = USERS_OPTION_DICT["ip"]
        port = USERS_OPTION_DICT["port"]
        user = USERS_OPTION_DICT["user"]
        pwd = USERS_OPTION_DICT["pwd"]
        database = USERS_OPTION_DICT["database"]
        init_mysql(ip, port, user, pwd, database)
        print("初始化数据库连接")
        cls.run_total_case = RunCase()
        cls.run_total_case.run_report = ''
        # 保存本次运行的用例情况
        cls.run_total_case.run_from_system = cls.project_system_name
        cls.run_total_case.run_case_count = len(cls.cases)
        cls.run_total_case.run_status = 0
        cls.run_total_case.run_success = 0
        cls.run_total_case.run_fail = 0
        cls.run_total_case.run_skip = 0
        cls.run_total_case.run_success_rate = 0
        cls.run_total_case.run_durations = 0
        cls.start_time = int(round(time.time()*1000))
        global RUN_ID
        RUN_ID = CaseRunBiz.add_run_case(cls.run_total_case)


    @classmethod
    def teardown_class(cls):
        # 报告
        print("------------------------------------报告====================================")

        # 保存报告结果
        save_report = os.path.join("history_report", time.strftime("%Y%m%d_%H%M%S"))
        cls.copy_report_thread = CopyReportThread("report", save_report)

        cls.copy_report_thread.start()
        # 将报告路径放到用例结果中
        # cls.run_total_case.run_report = save_report
        # 保存本次运行的用例情况
        # cls.run_total_case.run_from_system = cls.project_system_name
        # cls.run_total_case.run_case_count = len(cls.cases)
        # cls.run_total_case.run_status = 1
        # cls.run_total_case.run_success = 2
        # cls.run_total_case.run_fail = 0
        # cls.run_tase.run_skip = 0
        # global RUN_ID
        # cls.run_total_case.run_id=RUN_ID
        # cls.run_total_case.run_success_rate = 100.00
        # cls.run_total_case.run_durations = 5
        global RUN_ID
        TestRun.summary_report(cls.cases,RUN_ID,save_report)
        CaseRunBiz.update_run_case(cls.run_total_case,RUN_ID)

    @classmethod
    def summary_report(cls,cases,run_id,path):
        dao = FrameworkDAO()
        result = dao.get_summery_report(run_id)
        total_count = int(result.total_count)
        success_count = int(result.success_count)
        collection_count = len(cases)
        run_status =1
        fail_count = total_count -success_count
        if total_count < collection_count:
            total_count = collection_count
        skip_count =  total_count - success_count - fail_count
        if skip_count + fail_count >0:
            run_status =0
        cls.run_total_case.run_report = path
        # 保存本次运行的用例情况
        cls.run_total_case.run_from_system = cls.project_system_name
        cls.run_total_case.run_case_count = total_count
        cls.run_total_case.run_status = run_status
        cls.run_total_case.run_success = success_count
        cls.run_total_case.run_fail = fail_count
        cls.run_total_case.run_skip = skip_count
        cls.run_total_case.run_id=run_id
        cls.run_total_case.run_success_rate=0
        cls.run_total_case.run_success_rate = success_count / total_count
        cls.run_total_case.run_durations =int(round(time.time()*1000))-cls.start_time


    @pytest.fixture(scope="function", params=get_run_cases(), ids=get_run_cases_name())
    def case(self, request):
        ret = request.param
        print("------------------------get case!------------------------------")
        global CASE_CRITICAL, CASE_NAME
        CASE_CRITICAL = ret.case_description
        CASE_NAME = ret.case_name
        print("----------------", CASE_CRITICAL, CASE_NAME, "-----------------------")
        return ret, ret.case_name

    # 功能块，具有相同feature或story的用例将规整到相同模块下,执行时可用于筛选
    def test_run_cases(self, case):
        """
        :param case: 本次执行的用例内容，类FinlabCase的一个实例
        :return:{0}
        """.format(case)
        case, name = case[0], case[1]
        name = 'case_id: ' +str(case.case_id) + ' case_name:' +name
        print("---------------------{0}------------------".format(name))
        # 实例化对应的业务类
        global RUN_ID
        business_obj = FactoryBusiness.init_business(case,RUN_ID,{})

        # 数据准备
        print("数据准备")
        self.init_data(business_obj, name)
        # 执行
        print("执行")
        self.run_case(business_obj, name)
        # 后置数据准备
        print("后置数据准备")
        self.after_init_data(business_obj, name)
        # 对比结果
        print("对比结果")
        self.compare_result(business_obj, name)
        print("清理")
        self.clear_data(business_obj, name)
        # 保存执行后的用例s
        TestRun.cases.append(case)





    @pytest.allure.step("第一步，数据准备, {2}")
    def init_data(self, business, case_description):
        print(case_description)
        business.init_data()

    @allure.step("第二步，执行用例, {2}")
    def run_case(self, business, case_description):
        print(case_description)
        business.run_case()

    @allure.step("第三步，后置数据准备, {2}")
    def after_init_data(self, business, case_description):
        print(case_description)
        business.after_init_data()

    @allure.step("第四步，对比, {2}")
    def compare_result(self, business, case_description):
        print(case_description)
        business.compare_result()

    @allure.step("第五步，清理环境, {2}")
    def clear_data(self, business, case_description):
        print(case_description)
        business.clear_data()



if __name__ == "__main__":
    pytest.main("TestClass.py --capture=no --project_system_name=tmms")
