# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import *


class TielingZhongyiMock(Easymock):
    def update_credit_apply_success(self):
        api = "/data-proxy/pqCreditQuery/create/task"
        mode = '''{
          "code": "0",
          "message": "success",
          "data": {
            "task_id": "011620210201162106000004"
          }
        }'''
        self.update(api, mode)

    def update_credit_query_success(self):
        api = "/data-proxy/pqCreditQuery/query/task"
        mode = '''{
          "code": "0",
          "message": "success",
          "data": {
            "score": 99
          }
        }'''
        self.update(api, mode)

    def update_credit_query_fail(self):
        api = "/data-proxy/pqCreditQuery/query/task"
        mode = '''{
          "code": "100015",
          "message": "中裔分获取失败",
          "data": null
        }'''
        self.update(api, mode)

    def update_loan_apply_success(self):
        api = "/tieling/loan/api/apply"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "transOutput": {
              "version": "01",
              "channelCode": "0030",
              "transCode": null,
              "appId": function({_req}) {return _req.body.key},
              "transDate": null,
              "transTime": null,
              "type": "S",
              "code": "200",
              "msg": "OK"
            },
            "transCode": "T0001"
          }
        }'''
        self.update(api, mode)

    def update_loan_query_success(self, asset_info):
        api = "/tieling/loan/api/queryApply"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "transOutput": {
              "version": "01",
              "channelCode": "0030",
              "transCode": null,
              "appId": function({_req}) {return _req.body.data.assoAppId},
              "transDate": null,
              "transTime": null,
              "type": "S",
              "code": "200",
              "msg": "OK"
            },
            "appId": function({_req}) {return _req.body.data.assoAppId},
            "status": "3",
            "code": null,
            "msg": null,
            "loanCode": "%s",
            "applyAmount": %s,
            "deadline": %s,
            "deadlineType": "1",
            "rate": 7.5,
            "payWay": null,
            "loanTime": "%s"
          }
        }'''% (get_guid(),
                asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['period_count'],
                get_date())
        self.update(api, mode)

    def update_loan_query_fail(self, asset_info):
        api = "/tieling/loan/api/queryApply"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "transOutput": {
              "version": "01",
              "channelCode": "0030",
              "transCode": null,
              "appId": function({_req}) {return _req.body.data.assoAppId},
              "transDate": null,
              "transTime": null,
              "type": "S",
              "code": "200",
              "msg": "OK"
            },
            "appId": function({_req}) {return _req.body.data.assoAppId},
            "status": "9",
            "code": "TR002",
            "msg": "放款失败",
            "loanCode": null,
            "applyAmount": %s,
            "deadline": %s,
            "deadlineType": "1",
            "rate": 7.5,
            "payWay": null,
            "loanTime": null
          }
        }'''% (asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['period_count'])
        self.update(api, mode)

    def update_loan_query_fail_not_exist(self):
        api = "/tieling/loan/api/queryApply"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "transOutput": {
              "version": "01",
              "channelCode": "0030",
              "transCode": null,
              "appId": function({_req}) {return _req.body.data.assoAppId},
              "transDate": null,
              "transTime": null,
              "type": "E",
              "code": "EQ0001",
              "msg": "订单不存在"
            },
            "appId": null,
            "status": null,
            "code": null,
            "msg": null,
            "loanCode": null,
            "applyAmount": null,
            "deadline": null,
            "deadlineType": null,
            "rate": null,
            "payWay": null,
            "loanTime": null
          }
        }'''
        self.update(api, mode)

    def update_repay_plan(self, asset_info):
        api = "/tieling/loan/api/queryRepayPlan"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
          "code": 0,
          "message": "",
          "data": {
            "transOutput": {
              "version": "01",
              "channelCode": "0030",
              "transCode": None,
              "appId": asset_info['data']['asset']['item_no'],
              "transDate": None,
              "transTime": None,
              "type": "S",
              "code": "200",
              "msg": "OK"
            },
            "applyAmount": asset_info['data']['asset']['amount'],
            "deadline": asset_info['data']['asset']['period_count'],
            "deadlineType": "1",
            "payWay": "0",
            "rate": 7.5,
            "totPrincipal": asset_info['data']['asset']['amount'],
            "totIni": "0",
            "totFee": 0,
            "repayPrincipal": None,
            "repayIni": None,
            "repayFee": None,
            "repayAmt": None,
            "repayPlans": []
          }
        }
        repayment_plan_tmp = {
            "currPeriod": 12,
            "repayDate": "2023-01-28",
            "principal": 344.86,
            "ini": 2.16,
            "fee": 0,
            "totAmt": 347.02
          }
        total_ini = 0
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['currPeriod'] = i + 1
            repayment_plan['principal'] = float(fee_info['principal']) / 100
            repayment_plan['ini'] = float(fee_info['interest']) / 100
            repayment_plan['totAmt'] = repayment_plan['principal'] + repayment_plan['ini']
            repayment_plan['repayDate'] = fee_info['date']
            mode['data']['repayPlans'].append(repayment_plan)
            total_ini += repayment_plan['ini']
        mode['data']['totIni'] = total_ini
        self.update(api, mode)


if __name__ == "__main__":
    pass
