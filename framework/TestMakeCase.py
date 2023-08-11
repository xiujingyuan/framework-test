# -*- coding: utf-8 -*-
# @ProjectName:    framework-test$
# @Package:        $
# @ClassName:      TestMakeCase$
# @Description:    描述
# @Author:         Fyi zhang
# @CreateDate:     2019/3/4$ 21:49$
# @UpdateUser:     更新者
# @UpdateDate:     2019/3/4$ 21:49$
# @UpdateRemark:   更新内容
# @Version:        1.0
import pytest

from bussiness.biz.FinlabCaseBiz import FinlabCaseBiz
from common.tools.BaseUtils import BaseUtils
from initial.InitMysql import init_mysql
class TestMakeCase(object):

    def test_case(self):

        ip ="127.0.0.1"
        port ="3306"
        user ="root"
        pwd ="Coh8Beyiusa7"
        database = "gaea_framework"
        init_mysql(ip, port, user, pwd, database)
        case_ids = '''[22171,22172,22173,22174,22175,22176,22177,22178,22191,22192,22200,22201,22202,22205,22206,22207,22210,22234,22235,22236,22237,22238,22239,22240,22241,22250]'''
        case_ids_dict = BaseUtils.transfer_string_to_dict(case_ids)
        for case_id in case_ids_dict:
            case_except_value_new_dict={}
            case = FinlabCaseBiz.Query_Case_By_Id(int(case_id))
            case_except_value = case.case_except_value
            case_except_value_dict = BaseUtils.transfer_string_to_dict(case_except_value)
            for key ,value in case_except_value_dict.items():
                case_except_value_new_dict[value] = key
            case.case_except_value = BaseUtils.transfer_dict_to_string(case_except_value_new_dict)
            # case = FinlabCaseBiz.Query_Case_By_Id(int(case_id))
            # case_except_value = case.case_except_value
            # case_except_value_dict = BaseUtils.transfer_string_to_dict(case_except_value)
            # for key ,value in case_except_value_dict.items():
            #      if '$.data.' in value :
            #          value = ''
            #FinlabCaseBiz.Update_Case(case,case.case_id)




if __name__ =="__main__":
    pytest.main(" TestMakeCase.py --capture=no --project_system_name=framework-test")
