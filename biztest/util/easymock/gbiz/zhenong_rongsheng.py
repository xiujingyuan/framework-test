# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy

from biztest.util.tools.tools import get_date


class ZhenongRongshengMock(Easymock):

    def update_card_query(self):
        """
        开户查询(新用户开户)
        """
        api = "/zhenong/zhenong_rongsheng/pay/card/query"
        body = {
            "code": "0000",
            "message": "请求成功",
            "data": {
                "code": "601301",
                "msg": "查询信息不存在"
            }
        }
        self.update(api, body)

    def update_card_query_list(self,four_element):
        """
        开户查询（开户成功）
        """
        api = "/zhenong/zhenong_rongsheng/pay/card/query"
        body = {
            "code": "0000",
            "message": "请求成功",
            "data": {
                "code": "000000",
                "msg": "",
                "data": [
                    {
                        "name": "建设银行",
                        "cardNo": four_element['data']['bank_code'],
                        "type": "1",
                        "signStatus": "0"
                    },
                    {

                        "name": "建设银行",
                        "cardNo": "5522451540230061",
                        "type": "1",
                        "signStatus": "0"

                    }

                ]
            }
        }
        self.update(api, body)

    def update_card(self):
        """
        绑卡
        """
        api = "/zhenong/zhenong_rongsheng/pay/card"
        body = {
              "code": "0000",
              "message": "请求成功",
              "data": {
                "code": "000000",
                "msg": "绑卡申请成功",
                "data": {
                  "traceNo": "221122099424696586"
                }
              }
            }
        self.update(api, body)

    def update_card_confirm(self):
        """
        绑卡确认
        """
        api = "/zhenong/zhenong_rongsheng/pay/card/confirm"
        body = {
              "code": "0000",
              "message": "请求成功",
              "data": {
                "code": "000000",
                "msg": "绑卡成功"
              }
            }
        self.update(api, body)

    def update_credit_apply(self,itemno, code="000000",msg="申请已受理"):
        """
        授信申请
        """
        assetdata = get_asset_loan_record_by_item_no(itemno)
        creditno = assetdata[0]['asset_loan_record_trade_no']
        api = "/zhenong/zhenong_rongsheng/credit/apply"
        body = {
              "code": "0000",
              "message": "请求成功",
              "data": {
                "code": code,
                "msg": msg,
                "data": {
                  "creditNo": creditno
                }
              }
            }
        self.update(api, body)

    def update_credit_query(self,itemno, code="000000", msg='', status="S" ,availableAmount="50000.00" ,endDate='2023-12-06'):
        """
        授信查询
        """
        assetdata = get_asset_loan_record_by_item_no(itemno)
        creditno = assetdata[0]['asset_loan_record_trade_no']
        api = '/zhenong/zhenong_rongsheng/credit/query'
        body = {
              "code": "0000",
              "message": "请求成功",
              "data": {
                "code": code,
                "msg": msg,
                "data": {
                  "creditNo": creditno,
                  "status": status,
                  "creditAmount": "50000.00",
                  "availableAmount": availableAmount,
                  "remark": "",
                  "startDate": "2022-11-22",
                  "endDate": endDate
                }
              }
            }
        self.update(api, body)

    def update_credit_query_notorder(self, code='000000', msg=''):
        """
        授信查询
        """
        api = '/zhenong/zhenong_rongsheng/credit/query'
        body = {
              "code": "0000",
              "message": "请求成功",
              "data": {
                "code": code,
                "msg": msg
              }
            }
        self.update(api, body)

    def update_loan_apply(self,itemno, code="000000", msg=""):
        """
        用信申请
        """
        api = '/zhenong/zhenong_rongsheng/loan/apply'
        body = {
              "code": "0000",
              "message": "请求成功",
              "data": {
                "code": code,
                "msg": msg,
                "data": {
                  "loanDrawUuid": itemno
                }
              }
            }
        self.update(api, body)

    def update_loan_query_url(self, itemno, status="I", loanAgreementStatus="I"):
        """
        查询签约url
        """
        api = '/zhenong/zhenong_rongsheng/loan/query'
        body = {
              "code": "0000",
              "message": "请求成功",
              "data": {
                "code": "000000",
                "msg": "",
                "data": {
                  "loanDrawUuid": itemno,
                  "loanAgreement": "",
                  "status": status,
                  "loanAmount": "",
                  "paymentTime": "",
                  "totalPeriod": "",
                  "remark": "处理中",
                  "contractInfo": {
                    "loanAgreementUrl": "http://115.238.89.106:8907/signwarn?sdkToken=9ffe7f8f-1abd-4014-b088-f2db6b35dff9&loanDrawUuid=S2022112372633213480",
                    "loanAgreementStatus": loanAgreementStatus,
                    "repayAgreementUrl": "",
                    "repayAgreementStatus": ""
                  },
                  "repayPlan": ""
                }
              }
            }
        self.update(api, body)

    def update_loan_query_status(self, itemno, status="S", remark="放款成功"):
        """
        借款结果查询
        """
        loanTime = get_date(fmt="%Y-%m-%d %H:%M:%S")
        api = '/zhenong/zhenong_rongsheng/loan/query'
        body = {
              "code": "0000",
              "message": "请求成功",
              "data": {
                "code": "000000",
                "msg": "",
                "data": {
                  "loanDrawUuid": itemno,
                  "loanAgreement": "",
                  "status": status,
                  "loanAmount": "5000.00",
                  "paymentTime": loanTime,
                  "totalPeriod": "12",
                  "remark": remark,
                  "contractInfo": {
                    "loanAgreementUrl": "http://115.238.89.106:8907/signwarn?sdkToken=9ffe7f8f-1abd-4014-b088-f2db6b35dff9&loanDrawUuid=S2022112372633213480",
                    "loanAgreementStatus": "S",
                    "repayAgreementUrl": "",
                    "repayAgreementStatus": ""
                  },
                  "repayPlan": ""
                }
              }
            }
        self.update(api, body)
    def update_loan_query_status_fail(self):
        """
        借款结果查询
        """
        api = '/zhenong/zhenong_rongsheng/loan/query'
        body = {
              "code": "0000",
              "message": "请求成功",
              "data": {
                "code": "601044",
                "msg": "授信到期",
                "data": {
                  "loanDrawUuid": "",
                  "loanAgreement": "",
                  "status": "F",
                  "loanAmount": "",
                  "paymentTime": "",
                  "totalPeriod": "",
                  "remark": "",
                  "contractInfo": "",
                  "repayPlan": ""
                }
              }
            }
        self.update(api, body)

    def update_loan_query_repayplan(self, itemno, asset_info):
        """
        还款计划查询
        """
        loanTime = get_date(fmt="%Y-%m-%d %H:%M:%S")
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/zhenong/zhenong_rongsheng/loan/query'
        body = {
          "code": "0000",
          "message": "请求成功",
          "data": {
            "code": "000000",
            "msg": "",
            "data": {
              "loanDrawUuid": itemno,
              "loanAgreement": "http://115.238.89.106:8908/group1/M00/04/6E/rBAikGN-DMWAE43IAAHtsSH3ezQ874.pdf",
              "status": "S",
              "loanAmount": "5000.00",
              "paymentTime": loanTime,
              "totalPeriod": "12",
              "remark": "放款成功",
              "contractInfo": {
                "loanAgreementUrl": "http://file-test.znjf33.cn/group1/M00/04/6E/rBAikGN-DMWAE43IAAHtsSH3ezQ874.pdf?contractName=借款协议&contractNo=借TA-050-20221123-038",
                "loanAgreementStatus": "S",
                "repayAgreementUrl": "",
                "repayAgreementStatus": ""
              },
              "repayPlan": []
            }
          }
        }
        repayplan ={
                  "period": "1",
                  "status": "0",
                  "capital": "372.80",
                  "interest": "100.00",
                  "lateInterest": "0.00",
                  "penaltyInterest": "0.0",
                  "lateDays": "0",
                  "paidCapital": "0.0",
                  "paidInterest": "0.0",
                  "paidLateInterest": "0.00",
                  "paidPenaltyInterest": "0.00",
                  "loanStartDate": "2022-11-24",
                  "loanEndDate": "2022-12-24",
                  "total": "472.80"
                }

        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplan)
            repayment_plan['period'] = i + 1
            repayment_plan['capital'] = float(fee_info['principal'])/100
            repayment_plan['interest'] = float(fee_info['interest'])/100
            repayment_plan['total'] = float(fee_info['principal'] + fee_info['interest'])/100
            repayment_plan['loanEndDate'] = fee_info['date']
            body['data']['data']['repayPlan'].append(repayment_plan)
        self.update(api, body)

    def update_loan_query_contract(self, itemno):
        """
        合同查询
        """
        api = '/zhenong/zhenong_rongsheng/loan/query'
        body = {
          "code": "0000",
          "message": "请求成功",
          "data": {
            "code": "000000",
            "msg": "",
            "data": {
              "loanDrawUuid": itemno,
              "loanAgreement": "http://115.238.89.106:8908/group1/M00/04/6E/rBAikGN-DMWAE43IAAHtsSH3ezQ874.pdf",
              "status": "S",
              "loanAmount": "5000.00",
              "paymentTime": "2022-11-23 20:11:47",
              "totalPeriod": "12",
              "remark": "放款成功",
              "contractInfo": {
                "loanAgreementUrl": "http://file-test.znjf33.cn/group1/M00/04/6E/rBAikGN-DMWAE43IAAHtsSH3ezQ874.pdf?contractName=借款协议&contractNo=借TA-050-20221123-038",
                "loanAgreementStatus": "S",
                "repayAgreementUrl": "",
                "repayAgreementStatus": ""
              },
              "repayPlan": ""
            }
          }
        }
        self.update(api, body)