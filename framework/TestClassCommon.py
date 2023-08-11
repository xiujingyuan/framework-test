# -*- coding: utf-8 -*-
# @Title: TestClassCommon
# @ProjectName framework-test
# @Description: TODO
# @author fyi zhang
# @date 2018/12/10 22:43

import pytest
import allure
from .FactoryBusiness import FactoryBusiness
from conftest import USER_OPTIONS
from framework.dao.FrameworkDAO import FramewrokDAO
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
dao = FramewrokDAO()

def get_run_cases():
    """
    获取本次运行的用例集
    :return:返回通过系统和模块查询到的用例集
    """
    project_system_name=USERS_OPTION_DICT["project_system_name"]
    cases = dao.get_cases("qbus")
    return cases


def get_run_cases_name():
    rets = get_run_cases()
    return map(lambda x: x.case_description, rets)



class TestRun(object):
    result = []
    cases = []
    run_total_case = None

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
       pass
    @pytest.fixture(scope="function", params=get_run_cases(), ids=get_run_cases_name())
    def case(self, request):
        ret = request.param
        print("------------------------get case!------------------------------")
        global CASE_CRITICAL, CASE_NAME
        CASE_CRITICAL = ret.case_description
        CASE_NAME = ret.case_name
        print("----------------", CASE_CRITICAL, CASE_NAME, "-----------------------")
        return ret, ret.case_name

    @allure.story("api_push模块测试")  # 功能块，具有相同feature或story的用例将规整到相同模块下,执行时可用于筛选
    def test_run_cases(self, case):
        """
        :param case: 本次执行的用例内容，类FinlabCase的一个实例
        :return:{0}
        """.format(case)
        print("---------------------{0}------------------".format(case))
        case, name = case[0], case[1]
        # 实例化对应的业务类
        business_obj = FactoryBusiness.init_business(case)

        # 数据准备
        print("数据准备")
        self.init_data(business_obj, case.case_description)

        allure.attach('my attach', 'Hello, World')

        # 执行
        print("执行")
        self.run_case(business_obj, case.case_description)
        # 后置数据准备
        print("后置数据准备")
        self.after_init_data(business_obj, case.case_description)
        # 对比结果
        print("对比结果")
        self.compare_result(business_obj, case.case_description)
        assert 2 == 2
        # 存储结果
        case.case_actual_value = len(TestRun.cases)
        print("case.case_actual_value", case.case_actual_value)
        print("TestRun.cases", TestRun.cases)
        print("before case actual value:", TestRun.get_before_case_actual_value())
        # 清理
        print("清理")
        self.clear_data(business_obj, case.case_description)
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

    @classmethod
    def get_before_case_actual_value(cls):
        return TestRun.cases[-1].case_actual_value if TestRun.cases else None


if __name__ == "__main__":
    pytest.main("TestClassCommon.py --capture=no --project_system_name=repay_system")
