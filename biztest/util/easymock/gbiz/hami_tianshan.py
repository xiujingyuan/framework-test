# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *
import time


class HamiTianShanMock(Easymock):
    def update_apply_success(self):
        api = "/hamitianshan/A002"
        mode = '''{
                  "rtnCode": "SUCCESS",
                  "rtnMsg": "支支mock测试",
                  "subCode": "SUCCESS",
                  "errCode": "000000", 
                  "errMsg": "mock测试",
                  "bizContent": "{\\"status\\":0}", 
                  "nonceStr": "9QJ7tYTafcwFyfBIihIvdwXjgwFU58K9",
                  "sign": "B5489883C09BA4CC086564ABED801322"
                }'''
        self.update(api, mode)

    def update_apply_retry(self):
        api = "/hamitianshan/A002"
        mode = '''{
                  "rtnCode": "SUCCESS",
                  "rtnMsg": "支支mock测试",
                  "subCode": "SUCCESS",
                  "errCode": "000001", 
                  "errMsg": "mock测试",
                  "bizContent": "{\\"status\\":0}", 
                  "nonceStr": "9QJ7tYTafcwFyfBIihIvdwXjgwFU58K9",
                  "sign": "B5489883C09BA4CC086564ABED801322"
                }'''
        self.update(api, mode)

    def update_applyquery_success(self, asset_info):
        api = "/hamitianshan/A003"
        mode = '''{
                  "rtnCode": "SUCCESS",
                  "rtnMsg": "服务调用成功",
                  "subCode": "SUCCESS",
                  "errCode": "000000",
                  "errMsg": "交易成功",
                  "bizContent": function({
                    _req
                  }) {
                    var data = {
                      "status": 1,
                      "traceNo": "%s",
                      "creditAmt": %s
                    };
                    return JSON.stringify(data)
                  },
                  "nonceStr": "n0Lc8YNWJuVFHinNAH39a9SwjwVsY1aK",
                  "sign": "EDA270B23280C953E9EA336539D89E65"
                }''' % (get_random_num(), asset_info['data']['asset']['amount'])
        self.update(api, mode)

    def update_applyquery_fail(self, asset_info):
        api = "/hamitianshan/A003"
        mode = '''{
                  "rtnCode": "SUCCESS",
                  "rtnMsg": "服务调用成功",
                  "subCode": "SUCCESS",
                  "errCode": "000000",
                  "errMsg": "交易成功",
                  "bizContent": function({
                    _req
                  }) {
                    var data = {
                      "status": 2,
                      "traceNo": "%s",
                      "creditAmt": %s
                    };
                    return JSON.stringify(data)
                  },
                  "nonceStr": "n0Lc8YNWJuVFHinNAH39a9SwjwVsY1aK",
                  "sign": "EDA270B23280C953E9EA336539D89E65"
                }''' % (get_random_num(), asset_info['data']['asset']['amount'])
        self.update(api, mode)

    def update_postapply_success(self):
        api = "/hamitianshan/A014"
        biz_content = r'{\"status\":1,\"downloadUrl\":\"http://paydayloandevv4-1251122539.cossh.myqcloud.com/20190422/e43d5bb369463bdbb36c4bdda2c086ef.pdf\",\"viewUrl\":\"https://testapi.fadada.com:8443/api//viewdocs.action?app_id\=403120\&timestamp\=20200702140827\&v\=2.0\&msg_digest\=NzNBMzU1MzkxREYxRTJBRDFFQUJGQjYzNjY0REVEQjZFRDZDRUQyMA\=\=\&transaction_id\=476068775838486528\&send_app_id\=null\"}'
        mode = '''{
                        "rtnCode": "SUCCESS",
                        "rtnMsg": "服务调用成功",
                        "subCode": "SUCCESS",
                        "errCode": "000000",
                        "errMsg": "交易成功",
                        "bizContent": "%s",
                        "nonceStr": "biGAyNQ90oWhFTBjSdfV50Dy2nCLOSSg",
                        "sign": "B216E62D54757099AB2FE305F90870BE"
                        }''' % (biz_content)

        self.update(api, mode)

    def update_loanapplyconfirm_success(self):
        api = "/hamitianshan/A004"
        mode = '''{
                  "rtnCode": "SUCCESS",
                  "rtnMsg": "服务调用成功",
                  "subCode": "SUCCESS",
                  "errCode": "000000", 
                  "errMsg": "交易成功",
                  "bizContent": "{\\"status\\":0}", 
                  "nonceStr": "cGXSK7F4mSCbeW5KNwOXek2ppMFJAWdq",
                  "sign": "B52D122417AD893D9DB0C83E515D4802"
                }'''
        self.update(api, mode)

    def update_loanconfirmquery_success(self, asset_info):
        nowtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        api = "/hamitianshan/A005"
        mode = '''{
                  "rtnCode": "SUCCESS",
                  "rtnMsg": "服务调用成功",
                  "subCode": "SUCCESS",
                  "errCode": "000000",
                  "errMsg": "交易成功",
                  "bizContent": function({
                    _req
                  }) {
                    var data = {
                      "traceNo": "%s",
                      "traceAmt": %s,
                      "dueBillNo": "%s",
                      "status": 1,
                      "dateTime": "%s",
                      "schedules": [
                      ]
                    };
                    return JSON.stringify(data)
                  },
                  "nonceStr": "giJeZBQXMgG550zPXuw0nZcSqwvdSi71",
                  "sign": "CD64D768D91A6913B23189FB3678C8A0"
                }
                ''' % (get_random_num(), asset_info['data']['asset']['amount'], get_random_num(), nowtime)

        self.update(api, mode)

    def update_loanconfirmquery_fail(self, asset_info):
        nowtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        api = "/hamitianshan/A005"
        mode = '''{
                          "rtnCode": "SUCCESS",
                          "rtnMsg": "服务调用成功",
                          "subCode": "SUCCESS",
                          "errCode": "000000",
                          "errMsg": "交易成功",
                          "bizContent": function({
                            _req
                          }) {
                            var data = {
                              "traceNo": "%s",
                              "traceAmt": %s,
                              "dueBillNo": "%s",
                              "status": 2,
                              "dateTime": "%s",
                              "schedules": [
                              ]
                            };
                            return JSON.stringify(data)
                          },
                          "nonceStr": "giJeZBQXMgG550zPXuw0nZcSqwvdSi71",
                          "sign": "CD64D768D91A6913B23189FB3678C8A0"
                        }
                        ''' % (get_random_num(), asset_info['data']['asset']['amount'],  get_random_num(), nowtime)

        self.update(api, mode)

    def update_capitalrepayplanquery_success(self, asset_info):
        api = "/hamitianshan/A005"
        nowtime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        dueBillNo = alr_info[0]['asset_loan_record_due_bill_no']
        repay_plan_temp = {
            "totalTerm": 12,
            "term": 12,
            "beginDate": "20210422",
            "endDate": "20210522",
            "shouldRepayPrincipal": 523.07,
            "shouldRepayInterest": 4.36,
            "penalty": 0,
            "cmpdintst": 0,
            "service": 0,
            "state": 2,
            "prdtNo": "1569292325162",
            "graceDay": 5,
            "coreStatus": 3,
            "overdue": "N"
        }
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        data_temp = []
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repay_plan_temp)
            repayment_plan['shouldRepayPrincipal'] = round((fee_info['principal'] / 100), 2)
            repayment_plan['shouldRepayInterest'] = round((fee_info['interest'] / 100), 2)
            repayment_plan['beginDate'] = get_date(month=i, fmt="%Y%m%d")
            repayment_plan['endDate'] = get_date(month=i + 1, fmt="%Y%m%d")
            repayment_plan['termStartTime'] = get_date_timestamp()
            repayment_plan['totalTerm'] = asset_info['data']['asset']['period_count']
            repayment_plan['term'] = i + 1
            data_temp.append(repayment_plan)
        plan_data = data_temp
        Content = {
            "traceNo": get_random_num(),
            "traceAmt": 8000,
            "dueBillNo": dueBillNo,
            "status": 1,
            "dateTime": nowtime,
            "schedules": plan_data,
            "nonceStr": "giJeZBQXMgG550zPXuw0nZcSqwvdSi71",
            "sign": "CD64D768D91A6913B23189FB3678C8A0"
        }
        bizContent = json.dumps(Content)
        mode = {
            "rtnCode": "SUCCESS",
            "rtnMsg": "服务调用成功",
            "subCode": "SUCCESS",
            "errCode": "000000",
            "errMsg": "交易成功",
            "bizContent": bizContent
        }
        self.update(api, mode)

    # 提前结清试算接口
    def update_settle_payoff_trail_mock(self, principal, interest):
        api = "/hami_tianshan/A007"
        mode = '''{
          "schedules": [{
            "totalTerm": 12,
            "term": 1,
            "beginDate": "2020-05-02",
            "endDate": "2020-05-02",
            "shouldRepayPrincipal": {},
            "shouldRepayInterest": {}
          }]
        }'''.format(principal, interest)
        self.update(api, mode)

    # 资方还款通知接口
    def update_capital_repay_notify_mock(self, notify_status="SUCCESS"):
        api = "/hami_tianshan/B002"
        mode = '''{
          "rtnCode": "SUCCESS",
          "rtnMsg": "服务调用成功",
          "subCode": "{}",
          "errCode": "000000",
          "errMsg": "自动化测试",
          "bizContent": "{\"status\": 1,\"traceNo\": \"12345\", \"dateTime\": \"{}\"}",
          "nonceStr": "bTTeVoxoz6Ff8jIoI5GVE4tAc6mTfzu1",
          "sign": "6FB9B54DC7B0520EBC5D03069D22F7A8"
        }'''.format(notify_status, get_date())
        self.update(api, mode)


if __name__ == "__main__":
    pass
