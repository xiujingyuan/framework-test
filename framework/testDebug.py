# -*- coding: utf-8 -*-
# @Time    : 公元19-03-26 上午9:23
# @Author  : 张廷利
# @Site    : 
# @File    : testDebug.py
# @Software: IntelliJ IDEA
import time,allure,pytest,copy

from bussiness.biz.FinlabCaseBiz import FinlabCaseBiz
from bussiness.biz.HistoryCaseBiz import HistoryCaseBiz
from models.framework.RunCaseDb import RunCase
from bussiness.biz.CaseRunBiz import CaseRunBiz
from framework.FactoryBusiness import FactoryBusiness
from common.tools.BaseUtils import BaseUtils
from initial.InitMysql import init_mysql
from conftest import USER_OPTIONS


def get_system_and_module():
     """
     通过pytest参数传递获取本次运行的系统和模块
     :return:
     """
     user_options = {}
     for option in USER_OPTIONS:
         user_options[option[2:]] = pytest.config.getoption(option, default=None)
     return user_options

USER_OPTIONS = get_system_and_module()

class TestDebug(object):







    def test_secial_case(self):

        #case_id = USER_OPTIONS["case_ids"]
        ip = USER_OPTIONS["ip"]
        port = USER_OPTIONS["port"]
        user = USER_OPTIONS["user"]
        pwd = USER_OPTIONS["pwd"]
        database = USER_OPTIONS["database"]
        init_mysql(ip, port, user, pwd, database)
        case_id = 24828
        # ip ="127.0.0.1"
        # port ="3306"
        # user ="root"
        # pwd ="Coh8Beyiusa7"
        # database = "gaea_framework"
        # init_mysql(ip, port, user, pwd, database)
        origin_case = FinlabCaseBiz.Query_Case_By_Id(int(case_id))
        case = copy.deepcopy(origin_case)
        history = HistoryCaseBiz.query_history_bycaseid(case_id)
        trd = TestRunDebug()
        trd.run_cases(case,BaseUtils.transfer_string_to_dict(history.history_case_vars))



class TestRunDebug(object):


    # 功能块，具有相同feature或story的用例将规整到相同模块下,执行时可用于筛选
    def run_cases(self, case,case_vars):
        """
        :param case: 本次执行的用例内容，类FinlabCase的一个实例
        :return:{0}
        """.format(case)
        case, name = case , case.case_name
        name = 'case_id: ' +str(case.case_id) + ' case_name:' +name
        print("---------------------{0}------------------".format(name))
        # 实例化对应的业务类

        global RUN_ID
        business_obj = FactoryBusiness.init_business(case,0,case_vars,1)

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





    @allure.step("第一步，数据准备, {2}")
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


if __name__ =="__main__":
    pytest.main(" TestDebug.py --capture=no --project_system_name=framework-test --env=dev")
