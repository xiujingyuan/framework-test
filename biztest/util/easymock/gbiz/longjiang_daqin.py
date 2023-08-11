# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class LongjiangDaqinMock(Easymock):
    def update_push_attachment_success(self):
        api = "/longjiang/std/attachment/push"
        mode = '''{
                  "code": 0,
                  "message": "OK",
                  "data": {}
                }'''
        self.update(api, mode)

    def update_apply_success(self, asset_info):
        api = "/longjiang/std/loan/apply"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "__v": "@id",
                    "asset_item_no": "@id",
                    "loan_order_no": "%s"
                  }
                }''' % (asset_info['data']['asset']['item_no'])
        self.update(api, mode)

    def update_apply_fail(self, asset_info):
        api = "/longjiang/std/loan/apply"
        mode = '''{
                  "code": 1,
                  "message": "mock失败",
                  "data": {
                    "__v": "@id",
                    "asset_item_no": "@id",
                    "loan_order_no": "%s"
                  }
                }''' % (asset_info['data']['asset']['item_no'])
        self.update(api, mode)


    def update_applyquery_success(self, asset_info):
        api = "/longjiang/std/loan/query"
        grant_at = get_date(fmt="%Y-%m-%d")
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "loan_result_desc": "mock测试",
                    "asset_item_no": "%s",
                    "grant_amount": %s,
                    "__v": "@id",
                    "due_at": "2021-07-11",
                    "loan_order_no": "%s",
                    "asset_status": "pass",
                    "debt_no": "@id",
                    "grant_at": "%s",
                    "period": %s
                  }
                }''' % (asset_info['data']['asset']['item_no'], asset_info['data']['asset']['amount'],
                        asset_info['data']['asset']['item_no'], grant_at, asset_info['data']['asset']['period_count'])
        self.update(api, mode)

    def update_applyquery_fail(self, asset_info):
        api = "/longjiang/std/loan/query"
        grant_at = get_date(fmt="%Y-%m-%d")
        mode = '''{
                   "code": 1,
                   "message": "mock测试失败",
                   "data": {
                     "loan_result_desc": "mock测试",
                     "asset_item_no": "%s",
                     "grant_amount": %s,
                     "__v": "@id",
                     "due_at": "2021-07-11",
                     "loan_order_no": "%s",
                     "asset_status": "pass",
                     "debt_no": "@id",
                     "grant_at": "%s",
                     "period": %s
                   }
                 }''' % (asset_info['data']['asset']['item_no'], asset_info['data']['asset']['amount'],
                         asset_info['data']['asset']['item_no'], grant_at, asset_info['data']['asset']['period_count'])
        self.update(api, mode)

    def update_applyquery_refused(self, asset_info):
        api = "/longjiang/std/loan/query"
        grant_at = get_date(fmt="%Y-%m-%d")
        mode = '''{
                           "code": 0,
                           "message": "成功",
                           "data": {
                             "loan_result_desc": "mock审核不通过",
                             "asset_item_no": "%s",
                             "grant_amount": %s,
                             "__v": "@id",
                             "due_at": "2021-07-11",
                             "loan_order_no": "%s",
                             "asset_status": "refused", //commit 审核中，pass 审核通过，refused 审核不通过
                             "debt_no": "@id",
                             "grant_at": "%s",
                             "period": %s
                           }
                         }''' % (asset_info['data']['asset']['item_no'], asset_info['data']['asset']['amount'],
                                 asset_info['data']['asset']['item_no'], grant_at,
                                 asset_info['data']['asset']['period_count'])
        self.update(api, mode)


    def update_applyquery_not_exist(self):
        api = "/longjiang/std/loan/query"
        mode = '''{
                    "code": 601002,
                    "message": "订单不存在"
                }'''
        self.update(api, mode)

    def update_confirmquery_fail(self,asset_info):
        api = "/longjiang/std/loan/query"
        grant_at = get_date(fmt="%Y-%m-%d")
        mode = '''{
                          "code": 0,
                          "message": "success",
                          "data": {
                            "loan_result_desc": "放款失败",
                            "asset_item_no": "%s",
                            "grant_amount": %s,
                            "__v": "@id",
                            "due_at": "2021-07-11",
                            "loan_order_no": "%s",
                            "asset_status": "failed", //invalid 已失效，failed 放款失败
                            "debt_no": "@id",
                            "grant_at": "%s",
                            "period": %s
                          }
                        }''' % (asset_info['data']['asset']['item_no'], asset_info['data']['asset']['amount'],
                                asset_info['data']['asset']['item_no'], grant_at,
                                asset_info['data']['asset']['period_count'])
        self.update(api, mode)

    def update_comfirm_success(self, asset_info):
        api = "/longjiang/std/loan/grant"

        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "__v": "@id",
                    "loan_order_no": "%s"
                  }
                }''' % (asset_info['data']['asset']['item_no'])
        self.update(api, mode)

    def update_comfirm_fail(self, asset_info):
        api = "/longjiang/std/loan/grant"

        mode = '''{
                  "code": 1,
                  "message": "mock LoanApplyConfirm 失败",
                  "data": {
                    "__v": "@id",
                    "loan_order_no": "%s"
                  }
                }''' % (asset_info['data']['asset']['item_no'])
        self.update(api, mode)

    def update_comfirmquery_success(self, asset_info):
        api = "/longjiang/std/loan/query"
        grant_at = get_date(fmt="%Y-%m-%d")
        mode = '''{
                          "code": 0,
                          "message": "success",
                          "data": {
                            "loan_result_desc": "mock测试放款成功",
                            "asset_item_no": "%s",
                            "grant_amount": %s,
                            "__v": "@id",
                            "due_at": "2021-07-11",
                            "loan_order_no": "%s",
                            "asset_status": "repay",
                            "debt_no": "@id",
                            "grant_at": "%s",//只有年月日，没有时分秒，时分秒会取当前时间补充进去
                            "period": %s
                          }
                        }''' % (asset_info['data']['asset']['item_no'], asset_info['data']['asset']['amount'],
                                asset_info['data']['asset']['item_no'], grant_at,
                                asset_info['data']['asset']['period_count'])
        self.update(api, mode)


    def update_repayplan_success(self, asset_info):
        api = "/longjiang/std/repayment/repay-plan"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "repay_plans": []
            }
        }
        mode_temp = {
            "period": 0,
            "due_day": "2021-07-11",
            "due_extend_day": "2021-07-11",
            "repay_plan_status": "",
            "premium": "",
            "principal": 985.52,
            "interest": 35.00,
            "extend_interest": 12.21,
            "penalty_interest": 0,
            "overdue_status": "",
            "overdue_days": 0,
            "repaid_premium": 0,
            "repaid_principal": 0,
            "repaid_interest": 0,
            "repaid_extend_interest": 0,
            "repaid_penalty_interest": 0,
            "no_repay_premium": 531.86,
            "no_repay_principal": 631.86,
            "no_repay_interest": 11.11,
            "no_repay_extend_interest": 12.21,
            "no_repay_penalty_interest": 0
        }
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        for i in range(asset_info["data"]["asset"]["period_count"]):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            data_temp = deepcopy(mode_temp)
            data_temp["due_day"] = get_date(month=i + 1, fmt="%Y-%m-%d")
            data_temp["period"] = i
            data_temp["principal"] = fee_info['principal'] / 100
            data_temp["interest"] = fee_info['interest'] / 100
            mode["data"]["repay_plans"].append(data_temp)
        self.update(api, mode)


    def update_certificate_apply_fail(self, item_no):
        api = "/longjiang/std/attachment/sync-proof"
        mode = '''{
                    "code": 1,//0：成功，非0：失败
                    "message": "成功",
                    "data": [{ "bizOrder":"%s","desc":"资产未结清" }] //没有请求成功会在这里面，申请成功的话，不会出现在里面
                }''' % item_no
        self.update(api, mode)



    def update_certificate_apply_success(self):
        api = "/longjiang/std/attachment/sync-proof"
        mode = '''{
                    "code": 0,//0：成功，非0：失败
                    "message": "成功",
                    "data": [] //没有请求成功会在这里面，申请成功的话，不会出现在里面
                }'''
        self.update(api, mode)


if __name__ == "__main__":
    pass
