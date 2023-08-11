# -*- coding: utf-8 -*-
# @Time    : 公元18-11-28 下午6:38
# @Author  : 张廷利
# @Site    : 
# @File    : testHttpUtils.py
# @Software: IntelliJ IDEA

import pytest
from common.tools.HttpUtils import HttpUtils
from models.framework.HttpMockDb import HttpMockDb
from common.tools.BaseUtils import BaseUtils,catch_exception



class TestHttpUtils(object):



    def test_http_post_json(self):
        header = {"content-type":"application/json"}
        url = "http://api.biz6.biztest.so/fox/decrease-op"
        req_data = '''{
                        "key":"12123123123123123123",
                        "type":"DecreaseService",
                        "from_system":"Fox",
                        "data":{
                            "asset_item_no":"ss_test_201802_06_3",
                            "period":1,
                            "amount":100
                        }
                }'''
        http = HttpUtils()
        init_data = {"case_mock_flag":"N","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        res = http.http_post(url,req_data,case,header)
        assert res!=""

    @catch_exception
    def test_http_post_json_mock(self):
        header = {"content-type":"application/json"}
        url = "http://api.biz6.biztest.so/fox/decrease-op"
        req_data = '''{
                        "key":"12123123123123123123",
                        "type":"DecreaseService",
                        "from_system":"Fox",
                        "data":{
                            "asset_item_no":"ss_test_201802_06_3",
                            "period":1,
                            "amount":100
                        }
                }'''
        init_data = {"case_mock_flag":"Y","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        http = HttpUtils()
        res = http.http_post(url,req_data,case,header)
        assert res =="ok"

    def test_http_post_formdata(self):
        header = {"content-type":"application/x-www-form-urlencoded"}
        url = "http://lan-testing3.kuainiujinke.com/v1/query/report-order"
        req_data = '''{
                            "apply_source":"meitu",
                            "id_card":"342401199311239271",
                            "product_period_count":"3",
                            "apply_amount":"300000",
                            "apply_id":"342401199311239271",
                            "apply_code":"342401199311239271",
                            "credit_id":"1490",
                            "type":"1"
                    }'''
        init_data = {"case_mock_flag":"N","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        http = HttpUtils()
        res = http.http_post(url,req_data,case,header)
        print(res)

    def test_http_post_formdata(self):
        header = {"content-type":"application/form-data"}
        url = "http://lan-testing3.kuainiujinke.com/v1/query/report-order"
        req_data = '''{
                            "apply_source":"meitu",
                            "id_card":"342401199311239271",
                            "product_period_count":"3",
                            "apply_amount":"300000",
                            "apply_id":"342401199311239271",
                            "apply_code":"342401199311239271",
                            "credit_id":"1490",
                            "type":"1"
                    }'''
        init_data = {"case_mock_flag":"N","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        http = HttpUtils()
        res = http.http_post(url,req_data,case,header)
        result = BaseUtils.transfer_dict_to_entity(res)
        assert result.code == 10000

    def test_http_get(self):
        url = "http://gate2.python.api.so/qiannniu/loanQuery"
        header = {"content-type":"application/form-data"}
        http = HttpUtils()
        init_data = {"case_mock_flag":"N","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        res = http.http_get(url,header,case)
        result = BaseUtils.transfer_dict_to_entity(res)
        assert result.code == 200
        pass

    def test_http_get_mock(self):
        url = "http://gate2.python.api.so/qiannniu/loanQuery"
        header = {"content-type":"application/form-data"}
        http = HttpUtils()
        init_data = {"case_mock_flag":"Y","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        res = http.http_get(url,header,case)
        assert res =="ok"



    def test_http_put(self):
        url ="http://easy.mock.biztest.so/mock/5bffd160c2c04c0020a97eb2/gaea_framework_test/put-test"
        header = {"content-type":"application/form-data"}
        http =HttpUtils()
        init_data = {"case_mock_flag":"N","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        res = http.http_put(url,None,header,case)
        result = BaseUtils.transfer_dict_to_entity(res)
        assert result.message =="emssage"
        pass

    def test_http_put(self):
        url ="http://easy.mock.biztest.so/mock/5bffd160c2c04c0020a97eb2/gaea_framework_test/put-test"
        header = {"content-type":"application/form-data"}
        http =HttpUtils()
        init_data = {"case_mock_flag":"Y","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        res = http.http_put(url,None,header,case)
        assert res =="ok"




    def test_http_delete_mock(self):
        url = "http://easy.mock.biztest.so/mock/5bffd160c2c04c0020a97eb2/gaea_framework_test/delete-test";
        header = {"content-type":"application/form-data"}
        http =HttpUtils()
        init_data = {"case_mock_flag":"Y","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        res = http.http_delete(url,None,header,case)
        assert res =="ok"

    def test_http_delete(self):
        url = "http://easy.mock.biztest.so/mock/5bffd160c2c04c0020a97eb2/gaea_framework_test/delete-test";
        header = {"content-type":"application/form-data"}
        http =HttpUtils()
        init_data = {"case_mock_flag":"N","case_id":1}
        case = BaseUtils.transfer_dict_to_entity(init_data)
        res = http.http_delete(url,None,header,case)
        result = BaseUtils.transfer_dict_to_entity(res)
        assert result.code ==0




if __name__=="__main__":
    pytest.main(" testHttpUtils.py --capture=no")