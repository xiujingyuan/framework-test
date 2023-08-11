# -*- coding: utf-8 -*-
from copy import deepcopy

from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.config.gbiz.gbiz_interface_params_config import gbiz_base_url
from biztest.util.http.http_util import Http
from biztest.util.tools.tools import get_random_str, get_date


class BaijinMock(Easymock):
    def update_account_open_success(self):
        api = "/personOpenAccount"
        mode = {
            "formUrl": "https://uat-open.b-banker.com/action",
            "formMap": {
                "serviceType": "1",
                "merchantCode": "20000000000000061",
                "data": "mlD4zvJghrudBiyGHQP62iORpU2EHJdjieXqdWZZFgHGDyN74aMjSOZHC4Irz3n1JP8N0dCEIgLShgoy4VcstZ3P4qmqU"
                        "iShSZtMxblkosMI2F7uVWb9ySEMRKdAGqrKmFVzBhBCR7CGuPcs9/OxoGjEGI3Z+h5XvYdfufNQzJUwAC7HUufm+q9aPd"
                        "PhdfmcJSULccNlL7KO2+Xm4gMbuI+eq9KeQvY+z0A3UgKG2nj8m82XgicqRYIu8wb3jGiDHkQNVy04wc0ZK28xY4Kldgk"
                        "2W2XC8Qd6PsNpLS9urBJdPjdxj8ILXr0S7RxuoLhbwWBMj0WO2W5IZlvpmi8hyxzowAG+K9KoWNNPTPQE5qWXu2yH/+US"
                        "qGMn7/L4+tHEU0+k84vMRrezr8XXJzTQbMhiVOXoC/3Xlk4I+iW4VC0d2+qizSD7NKr8u/7WYwdUOijGcTH3/OwdOZy7P3"
                        "XHiZwe3lZOuLN99Ne68NLVOU5hs5tQZmZR31kkTStlUIMi6Mtrknrnns/LRGSfuF6JrVruqNeL3JrkPROQ+OA4rUY=",
                "serviceName": "personOpenAccount",
                "encryptKey": "NS7pY6vcZgCy9dxfTxcYMwu5arKfkxr9ojtABxWoiBjGNrtMfUgeOLhQEjuRarOGh8mtnSpPdlH46oooew4uddF"
                              "VEvdYB/KNMP+bp5qZVQKSQbYnTzIqQYzrUEJLfVc3cZT7IOG0JsPeNjnOs4mT710LpKu6L9/TqxG6TcEogAI=",
                "version": "1.0.0"
            }
        }
        self.update(api, mode)

    def update_account_query_no_account(self):
        api = "/personAccountQuery"
        mode = {
            "code": "500007",
            "message": "用户未开户"
        }
        self.update(api, mode)

    def update_account_query_success(self, element):
        api = "/personAccountQuery"
        mode = '''{
            "code":"000000",
            "message":"成功",
            "serviceName":null,
            "userCode":"UR" + "@integer(100000000000000000000,900000000000000000000)",
            "accountStatus":1,
            "registerMobile":null,
            "registerMobileEncrypt":"%s",
            "name":null,
            "nameEncrypt":function({_req}) {return _req.body.name;},
            "idCardNo":null,
            "idCardNoEncrypt":function({_req}) {return _req.body.idCardNo;},
            "bankCardNo":null,
            "bankCardNoEncrypt":function({_req}) {return _req.body.bankCardNo;},
            "reservedMobile":null,
            "reservedMobileEncrypt":"%s",
            "bankCode":"BKCH"
            }
            // {
            //   "code": "500007",
            //   "message": "用户未开户"
            // }''' % (element['data']['phone_number_encrypt'], element['data']['phone_number_encrypt'])
        self.update(api, mode)

    def update_protocol_sign_apply_success(self):
        api = "/protocolSign"
        mode = {"code": "000000", "orderNo": "PSON19111" + get_random_str().upper(), "message": "成功", "status": 1}
        self.update(api, mode)

    def update_protocol_sing_confirm_success(self):
        api = "/protocolSignConfirm"
        mode = '{"code": "000000", "message": "成功", "status": 1}'
        self.update(api, mode)

    def update_protocol_query_no_protocol(self):
        api = "/protocolStatusQuery"
        mode = {"code": "500028", "message": "协议支付签约记录不存在"}
        self.update(api, mode)

    def update_protocol_query_success(self):
        api = "/protocolStatusQuery"
        mode = {"code": "000000", "message": "成功", "status": 1}
        self.update(api, mode)

    def update_risk_apply_success(self):
        api = "/rmeApplyPerson"
        mode = {"code": "000000", "message": "成功"}
        self.update(api, mode)

    def risk_callback_success(self, asset_info):
        url = gbiz_base_url + "/baijin/callback"
        header = {"Content-Type": "application/json"}
        body = {
            "duration": "30",
            "targetCode": asset_info["data"]["asset"]["item_no"],
            "auditResult": "1",
            "credit": str(asset_info["data"]["asset"]["amount"]) + "00",
            "serviceName": "rmeResult",
            "auditMsg": "111"
        }
        Http.http_post(url, body, header)

    def loan_apply_callback_success(self, asset_info):
        url = gbiz_base_url + "/baijin/callback"
        header = {"Content-Type": "application/json"}
        body = {
            "targetCode": asset_info["data"]["asset"]["item_no"],
            "serviceName": "notifyOrderStatus",
            "status": "8"
        }
        Http.http_post(url, body, header)

    def loan_apply_callback_fail(self, asset_info):
        url = gbiz_base_url + "/baijin/callback"
        header = {"Content-Type": "application/json"}
        body = {
            "targetCode": asset_info["data"]["asset"]["item_no"],
            "serviceName": "notifyOrderStatus",
            "status": "2"
        }
        Http.http_post(url, body, header)

    def confirm_callback_success(self, asset_info):
        url = gbiz_base_url + "/baijin/callback"
        header = {"Content-Type": "application/json"}
        body = {
            "targetCode": asset_info["data"]["asset"]["item_no"],
            "serviceName": "notifyOrderStatus",
            "status": "3"
        }
        Http.http_post(url, body, header)

    def grant_callback_success(self, asset_info):
        url = gbiz_base_url + "/baijin/callback"
        header = {"Content-Type": "application/json"}
        body = {
            "transferStatus": "1",
            "fullTargetDate": get_date(fmt="%Y-%m-%d"),
            "completedTime": get_date(),
            "loanSuccessTime": get_date(),
            "targetCode": asset_info["data"]["asset"]["item_no"],
            "serviceName": "notifyOrderStatus",
            "status": "4"
        }
        Http.http_post(url, body, header)

    def update_loan_apply_success(self):
        api = "/orderPush"
        mode = '''{
            "merchantCode": "20000000000000061",
            "code": "000000",
            "targetCode": function({_req}) {return _req.body.targetCode},
            "message": "成功",
            "status": "4"
            }
            // 4/5 成功
            // 3失败'''
        self.update(api, mode)

    def update_confirm_apply_success(self):
        api = "/orderLoanCheck"
        mode = {
            "formUrl": "https://uat-open.b-banker.com/action",
            "formMap": {
                "serviceType": "1",
                "merchantCode": "20000000000000061",
                "data": "1DTTxkHi8WDYrSwxTExcNfnFgawrxAJAM4WoHGMoqYv7Kk4DbDcV0XsNvK1hWuK9f460z7ECupKd0yZMhtxwT7v2zXllWB"
                        "UuuOnmgpOF4vU4VHfIOPn9bNYTPfVBJSmHxmulNBa2yPCIzYrGoBzT2XM7Cxa4rwUZBGdyQzoHcHYshCfvv5PItg0Exfb7"
                        "B2RHIyOI+TWXc4dFskS492DZ3iqHyU6xwk3lHU+eHfON7jbxwU5TsoRJo9OGf4IXBPOj/Xppq8qOxUZTPAbfeCpzq1Tp+a"
                        "xoeJz61k/T4WVNbzXGNBW5DYOACTKaUQZK525tJa8vWxXvnbDV6FuNii/pxkqZaiosoz6PmsXWT6QhwTkj9pF8Ge//yFFB"
                        "tuZFFUa25absrQAZJzRiGlrlkGVkcg+yj6qZ6Uk38/9I0J/kNGL6xfoivC0+VHDOaW9L9JB5",
                "serviceName": "orderLoanCheck",
                "encryptKey": "rRM1XtphaIjWeln91tVoyL7TNjM27+8DwO3bnMm/xADFM4lXZo+HpqIYuH0Z1g1cRBlKiCQdpS9n/s4Vv9g+pAeV"
                              "v4xaWJz88gNEJqbuwkOm2gGfYALC1MAemAYbPkPRAulUa9P2JYS7FuLvNnGyDLHcU5bx34z7VKEXDA561Ck=",
                "version": "1.0.0"
            }
        }
        self.update(api, mode)
        api = "/orderQuery"
        mode = '''{
            "merchantCode":"20000000000000061",
            "amount":250000,
            "code":"000000",
            "transferStatus":0,
            "targetCode":function({_req}) {return _req.body.targetCode},
            "loanUsage":"个人消费",
            "annualRate":1900,
            "message":"成功",
            "repayType":1,
            "signAuthFlag":2,
            "loanDuration":30,
            "balanceRepayFlag":2,
            "borrowType":1,
            "status":8,
            "raiseEndTime":"@now"
            }'''
        self.update(api, mode)

    def update_confirm_query_success(self):
        api = "/orderQuery"
        mode = '''{
            "merchantCode":"20000000000000061",
            "amount":250000,
            "code":"000000",
            "transferStatus":0,
            "targetCode":function({_req}) {return _req.body.targetCode},
            "loanUsage":"个人消费",
            "annualRate":1900,
            "message":"成功",
            "repayType":1,
            "signAuthFlag":2,
            "loanDuration":30,
            "balanceRepayFlag":2,
            "borrowType":1,
            "applyTime":"@now",
            "status":3,
            "raiseEndTime":"@now"
            }'''
        self.update(api, mode)

    def update_loan_query_success(self, asset_info):
        api = "/orderQuery"
        if asset_info['data']['asset']['period_count'] == 1:
            repayType = 1
        else:
            repayType = 2
        mode = '''{
            "merchantCode": "20000000000000061",
            "finishTime": "@now",
            "amount": %d,
            "code": "000000",
            "transferStatus": 1,
            "loanSuccessTime": "@now",
            "completedTime": "@now",
            "loanUsage": "个人消费",
            "annualRate": 1700,
            "message": "成功",
            "repayType": %s,
            "signAuthFlag": 2,
            "loanDuration": 30,
            "fullTargetDate": "@now(yyyy-MM-dd)",
            "balanceRepayFlag": 2,
            "borrowType": 1,
            "applyTime": "@now",
            "status": 4,
            "raiseEndTime": "@now",
            "targetCode":function({_req}) {return _req.body.targetCode},
            }''' % (int(asset_info['data']['asset']['amount']) * 100, repayType)
        self.update(api, mode)

    def update_replay_plan(self, asset_info):
        api = "/repaymentPlanQuery"
        repayment_plan_tmp = {
            "merchantServiceFee": 0,
            "capital": 132427,
            "totalFee": 2195,
            "interest": 2732,
            "repayTotalAmount": 137354,
            "repayPlanNo": 1,
            "waitRepayDate": "",
            "repayAmt": 0,
            "repayResult": 3,
            "overdueFine": 0,
            "platformServiceFee": 2195
        }
        mode = {
            "merchantCode": "20000000000000061",
            "code": "000000",
            "message": "成功",
            "repayPlanList": [],
            "targetCode": ""
        }

        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['repayPlanNo'] = i + 1
            repayment_plan['capital'] = fee_info['principal']
            repayment_plan['totalFee'] = fee_info['service']
            repayment_plan['interest'] = fee_info['interest']
            repayment_plan['repayTotalAmount'] = fee_info['principal'] + fee_info['interest']
            repayment_plan['platformServiceFee'] = fee_info['service']
            if asset_info['data']['asset']['period_count'] == 1:
                repayment_plan['waitRepayDate'] = get_date(day=29, fmt="%Y-%m-%d")
            else:
                repayment_plan['waitRepayDate'] = get_date(month=i + 1, fmt="%Y-%m-%d")
            mode['repayPlanList'].append(repayment_plan)
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        mode['targetCode'] = alr_info[0]['asset_loan_record_due_bill_no']

        self.update(api, mode)

    def update_contract_temp_download_success(self):
        api = "/queryNotSignContractInfo"
        mode = '''{
            "merchantCode": "20000000000000061",
            "code": "000000",
            "contractUrl": "http://paydayloandevv4-1251122539.cossh.myqcloud.com/20190422/e43d5bb369463bdbb36c4bdda2c086ef.pdf",
            "targetCode": function({_req}) {return _req.body.targetCode},
            "message": "成功"
            }'''
        self.update(api, mode)

    def update_contract_upload_success(self):
        api = "/notifySignContractInfo"
        mode = '''{
            "merchantCode": "20000000000000061",
            "code": "000000",
            "targetCode": function({_req}) {return _req.body.targetCode},
            "message": "成功"
            }'''
        self.update(api, mode)

    def update_contract_download_success(self):
        api = "/queryFilingContractInfo"
        mode = '''{
            "merchantCode": "20000000000000061",
            "code": "000000",
            "contractUrl": "http://paydayloandevv4-1251122539.cossh.myqcloud.com/20190422/e43d5bb369463bdbb36c4bdda2c086ef.pdf",
            "accessoryUrl": "http://cashtest-1251122539.cossh.myqcloud.com/2018/11/09/1109_164248_4cc84186-e859-4332-abe5-51f13799583e.jpg",
            "targetCode": function({_req}) {return _req.body.targetCode},
            "message": "成功"
            }'''
        self.update(api, mode)
