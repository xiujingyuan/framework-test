# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class LanzhouHaoyueMock(Easymock):

    def update_file_notice(self):
        api = "/lanzhou/haoyue/fileNotice"
        mode = '''{
                    "transDate": "2021-08-25",
                    "transTime": "10:20:47",
                    "respCode": "0000",
                    "respMsg": "交易接收成功"
                }'''
        self.update(api, mode)

    def update_customer_info_push(self):
        api = "/lanzhou/haoyue/customerInfoPush"
        mode = '''{
                    "transDate": "2021-08-25",
                    "transTime": "10:20:50",
                    "respCode": "0000",
                    "respMsg": "交易接收成功"
                }'''
        self.update(api, mode)

    def update_customer_info_push_fail(self):
        api = "/lanzhou/haoyue/customerInfoPush"
        mode = '''{
                    "transDate": "2021-08-25",
                    "transTime": "10:20:50",
                    "respCode": "9000",
                    "respMsg": "交易接收失败"
                }'''
        self.update(api, mode)

    def update_creditapply_success(self):
        api = "/lanzhou/haoyue/creditApply"
        mode = '''{
                "transDate": "2021-08-25",
                "transTime": "10:26:58",
                "respCode": "0000",
                "respMsg": "交易接收成功"
            }'''
        self.update(api, mode)

    def update_creditapply_fail(self):
        api = "/lanzhou/haoyue/creditApply"
        mode = '''{
                        "transDate": "2021-08-25",
                        "transTime": "10:26:58",
                        "respCode": "9000",
                        "respMsg": "有未使用授信，不可重复授信"
                    }'''
        self.update(api, mode)

    def update_creditapplyquery_success(self, asset_info):
        api = "/lanzhou/haoyue/creditQuery"
        mode = '''{
                    "result": "01",
                    "creditamt": %s,
                    "creditrate": 7.5,
                    "startdate": "%s",
                    "maturityDate": "20310828",
                    "transDate": "%s",
                    "transTime": "10:44:23",
                    "respCode": "9999",
                    "respMsg": "交易处理成功"
                }''' % (asset_info['data']['asset']['amount'],  get_date(fmt="%Y%m%d"), get_date(fmt="%Y-%m-%d"))
        self.update(api, mode)

    def update_creditapplyquery_success_other_rate(self, asset_info, rate):
        api = "/lanzhou/haoyue/creditQuery"
        mode = '''{
                    "result": "01",
                    "creditamt": %s,
                    "creditrate": "%s",
                    "startdate": "%s",
                    "maturityDate": "20310828",
                    "transDate": "%s",
                    "transTime": "10:44:23",
                    "respCode": "9999",
                    "respMsg": "交易处理成功"
                }''' % (asset_info['data']['asset']['amount'], rate, get_date(fmt="%Y%m%d"), get_date(fmt="%Y-%m-%d"))
        self.update(api, mode)

    def update_creditapplyquery_fail(self):
        api = "/lanzhou/haoyue/creditQuery"
        mode = '''{
                     "result": "03",
                     "resultMsg": "mock-测试失败",
                     "creditamt": 0,
                     "creditrate": 7.5,
                     "startdate": "%s",
                     "maturityDate": "20310828",
                     "transDate": "%s",
                     "transTime": "10:44:23",
                     "respCode": "9999",
                     "respMsg": "交易处理成功"
                 }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%Y-%m-%d"))
        self.update(api, mode)

    def update_creditapplyquery_no_order(self):
        api = "/lanzhou/haoyue/creditQuery"
        mode = '''{
                     "result": "02",
                     "resultMsg": "查无此交易",
                     "transTime": "10:44:23",
                     "respCode": "1000",
                     "respMsg": "查无此交易"
                         }'''
        self.update(api, mode)

    def update_customer_face_query_success(self):
        api = "/lanzhou/haoyue/cusFaceQuery"
        mode = '''{
                    "result": "01",
                    "transDate": "2021-08-25",
                    "transTime": "10:21:14",
                    "respCode": "9999",
                    "respMsg": "交易处理成功"
                }'''
        self.update(api, mode)

    def update_customer_face_query_fail(self):
        api = "/lanzhou/haoyue/cusFaceQuery"
        mode = '''{
            "result": "02",
            "resultMsg": "处理失败",
            "transDate": "2020-10-14",
            "transTime": "10:50:14",
            "respCode": "9000",
            "respMsg": "交易处理失败"
        }'''
        self.update(api, mode)

    def update_loan_apply(self):
        api = "/lanzhou/haoyue/loanApply"
        mode = '''{
                    "transDate": "2021-08-25",
                    "transTime": "11:05:11",
                    "respCode": "0000",
                    "respMsg": "交易接收成功"
                }'''
        self.update(api, mode)

    def update_loan_query_success(self, asset_info):
        api = "/lanzhou/haoyue/loanQuery"
        mode = '''{
            "merserno": function({
              _req
            }) {
              return _req.body.merserno
            },
            "contractNo": "66506",
            "loanid": "id_%s",
            "loanamt": %s,
            "loanyrate": 7.5,
            "loanstartdate": "%s",
            "loanenddate": "20211012",
            "loanstate": "04",
            "loanmess": "交易成功",
            "fee": 0,
            "transDate": "%s",
            "transTime": "12:33:20",
            "respCode": "9999",
            "respMsg": "交易处理成功"
        }''' % (get_guid(),
                asset_info['data']['asset']['amount'],
                get_date(fmt="%Y%m%d"),
                get_date(fmt="%Y-%m-%d"))
        self.update(api, mode)

    def update_loan_query_success_other_rate(self, asset_info, rate):
        api = "/lanzhou/haoyue/loanQuery"
        mode = '''{
               "merserno": function({
                 _req
               }) {
                 return _req.body.merserno
               },
               "contractNo": "66506",
               "loanid": "id_%s",
               "loanamt": %s,
               "loanyrate": %s,
               "loanstartdate": "%s",
               "loanenddate": "20211012",
               "loanstate": "04",
               "loanmess": "交易成功",
               "fee": 0,
               "transDate": "%s",
               "transTime": "12:33:20",
               "respCode": "9999",
               "respMsg": "交易处理成功"
           }''' % (get_guid(),
                   asset_info['data']['asset']['amount'],
                   rate,
                   get_date(fmt="%Y%m%d"),
                   get_date(fmt="%Y-%m-%d"))
        self.update(api, mode)

    def update_loan_query_fail(self):
        api = "/lanzhou/haoyue/loanQuery"
        mode = '''{
          "merserno": function({
              _req
            }) {
              return _req.body.merserno
            },
          "contractNo": "127684201014105247",
          "loanstate": "09",
          "fee": 0,
          "transDate": "2020-10-14",
          "transTime": "16:01:23",
          "respCode": "9999",
          "respMsg": "交易处理成功"
        }'''
        self.update(api, mode)

    def update_repay_plan(self, asset_info):
        api = "/lanzhou/haoyue/repaymentPlanQuery"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
            "merserno": asset_info['data']['asset']['item_no'],
            "paymentPlan": [],
            "transDate": "2020-10-12",
            "transTime": "12:44:33",
            "respCode": "9999",
            "respMsg": "交易处理成功"
        }
        repayment_plan_tmp = {
            "tpnum": 1,
            "loanenddate": "20201112",
            "payprincipalamt": 801.37,
            "actualpayprincipalamt": 0,
            "payinterestamt": 70.83,
            "actualpayinterestamt": 0,
            "payprincipalpenaltyamt": 0,
            "actualpayprincipalpenaltyamt": 0,
            "ispreps": "0"
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['tpnum'] = i + 1
            repayment_plan['payprincipalamt'] = float(fee_info['principal']) / 100
            repayment_plan['payinterestamt'] = float(fee_info['interest']) / 100
            repayment_plan['loanenddate'] = fee_info['date'].replace("-", "")
            mode['paymentPlan'].append(repayment_plan)
        self.update(api, mode)


    def update_contract_signature(self):
        api = "/lanzhou/haoyue/loanSignApply"
        mode = {
                  "transDate": get_date(fmt="%Y-%m-%d"),
                  "transTime": get_date(fmt="%H:%M:%S"),
                  "respCode": "1100",
                  "respMsg": "重复记录"
                }
        self.update(api, mode)

    def update_certificate_apply(self):
        api = "/lanzhou/haoyue/loanFinishApply"
        mode = {
                  "transDate": get_date(fmt="%Y-%m-%d"),
                  "transTime": get_date(fmt="%H:%M:%S"),
                  "respCode": "0000",
                  "respMsg": "交易接收成功"
                }
        self.update(api, mode)

    def update_certificate_down(self):
        api = "/lanzhou/haoyue/loanFinishQuery"
        mode = '''{
                "loanNo":  function({
              _req
            }) {
              return _req.body.loanNo
            },
                "loanFinishState": "2",
                "transDate": "%s",
                "transTime": "%s",
                "respCode": "9999",
                "respMsg": "交易处理成功"
            }''' % (get_date(fmt="%Y-%m-%d"), get_date(fmt="%H:%M:%S"))
        self.update(api, mode)

if __name__ == "__main__":
    pass
