# -*- coding: utf-8 -*-
# @Title: testBizProcess
# @ProjectName framework-test
# @Description: TODO
# @author fyi zhang
# @date 2018/12/13 14:11

from bussiness.biz.BizProcess import BizProcess
from common.tools.BaseUtils import BaseUtils
class TestBizProcess(object):

    def test_distribute_func(self):
        biz = BizProcess()
        case = {"case_id":7107,"case_api_params":"{'data':['zhangtingli']}"};
        vars = {"data":['zhanglina']}
        case = biz.main_process(BaseUtils.transfer_dict_to_entity(case),vars)
        print(case.case_api_params)


if __name__ == "__main__":
    t = TestBizProcess()
    t.test_distribute_func()




