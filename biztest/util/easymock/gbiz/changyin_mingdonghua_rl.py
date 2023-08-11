# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_event_by_item_no_event_type
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy

from biztest.util.tools.tools import get_date


class ChangyinMingdonghuaRlMock(Easymock):

    def update_card_query(self):
        """
        签约查询(新用户开户)
        """
        api = "/runlou/changyin_mingdonghua_rl/loan.assis.cy.bind.card.query"
        body = {
          "code": "0",
          "message": "Success",
          "data": {
            "resultCode": "0000",
            "resultMsg": "此卡号尚未签约，请发起签约申请"
          }
        }
        self.update(api, body)


    def update_card_query_old_user(self):
        """
        签约查询(新用户开户)
        """
        api = "/runlou/changyin_mingdonghua_rl/loan.assis.cy.bind.card.query"
        body = {
          "code": "0",
          "message": "Success",
          "data": {
            "resultCode": "1000",
            "resultMsg": "此卡号与长银平台已经签约",
            "agrSeq": "@id"
          }
        }
        self.update(api, body)



    def update_card_sign(self):
        """
        签约申请
        """
        api = "/runlou/changyin_mingdonghua_rl/loan.assis.cy.bind.card.sign"
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "resultCode": "0000"
              }
            }
        self.update(api, body)

    def update_card_sign_check(self):
        """
        签约确认
        """
        api = "/runlou/changyin_mingdonghua_rl/loan.assis.cy.bind.card.sign.check"
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "resultCode": "1002",
                "agrSeq": "@id"
              }
            }
        self.update(api, body)

    def update_credit_apply(self, status='P'):
        """
        授信申请
        """
        api = "/runlou/changyin_mingdonghua_rl/loan.assis.cy.credit.apply"
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "applyNo": "@id",
                "businessNo": "AP0LB62VHV1c1670556023bf4d09",  #申请不会校验这个字段，放在查询处校验
                "status": status
              }
            }
        self.update(api, body)

    def update_credit_query(self, itemNo, status='S', outRiskMsg=None, baseLimit=100000):
        """
        授信查询
        """
        event_data = get_asset_event_by_item_no_event_type(itemNo, 'CY_MDH_RL_CREDIT_APPLY')
        businessNo = eval(event_data[0]['asset_event_no']).get('businessNo')
        applyNo = eval(event_data[0]['asset_event_no']).get('applyNo')
        api = '/runlou/changyin_mingdonghua_rl/loan.assis.cy.credit.query'
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "status": status,
                "businessNo": businessNo,
                "applyNo": applyNo,
                "openId": "@id",
                "baseLimit": baseLimit,
                "contractNo": "HT" + itemNo,
                "isUnion": "N",
                "outRiskMsg":outRiskMsg
              }
            }
        self.update(api, body)

    def update_credit_query_notorder(self):
        """
        授信查询
        """
        api = '/runlou/changyin_mingdonghua_rl/loan.assis.cy.credit.query'
        body = {
              "code": "E2000001",
              "message": "授信申请不存在",
              "data": None
            }
        self.update(api, body)

    def update_disbursement_apply(self, status='P'):
        """
        放款申请
        """
        api = '/runlou/changyin_mingdonghua_rl/loan.assis.cy.disbursement.apply'
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "status": status,
                "businessNo": "AP0LB62VHV1l167057346738ad2f",  # 不需要校验
                "applyNo": "@id",
                "loanSeq": "24233042816127581202"
              }
            }
        self.update(api, body)

    def update_disbursement_query(self, itemNo, status='S', payMsg='放款成功'):
        """
        借款结果查询
        """
        loanTime = get_date(fmt="%Y-%m-%d %H:%M:%S")
        event_data = get_asset_event_by_item_no_event_type(itemNo, 'CY_MDH_RL_LOAN_APPLY')
        businessNo = eval(event_data[0]['asset_event_no'].replace('null','None')).get('businessNo')
        loanSeq = eval(event_data[0]['asset_event_no'].replace('null','None')).get('loanSeq')
        api = '/runlou/changyin_mingdonghua_rl/loan.assis.cy.disbursement.query'
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "status": status,
                "businessNo": businessNo,
                "dnAmt": 10000,
                "contractNo": "HT"+itemNo,
                "loanNo": "HT" + itemNo,
                "loanActvDt": "2033-04-28",
                "loanActvTime": loanTime,
                "payMsg": payMsg
              }
            }
        self.update(api, body)
    def update_disbursement_query_fail(self):
        """
        借款结果查询
        """
        api = '/runlou/changyin_mingdonghua_rl/loan.assis.cy.disbursement.query'
        body = {
              "code": "E2000001",
              "message": "借款申请不存在",
              "data": None
            }
        self.update(api, body)

    def update_repayment_schedule_query(self, asset_info):
        """
        还款计划查询
        """

        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/runlou/changyin_mingdonghua_rl/loan.assis.cy.repayment.schedule.query'
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "repaymentPlanList": [
                    {
                        "perdNo": 0,
                        "dueDt": "2033-04-28",
                        "psPrcpAmt": 0,
                        "psNormIntAmt": 0,
                        "psOdIntAmt": 0,
                        "psCommOdInt": 0,
                        "psFeeAmt": 0,
                        "setlPrcp": 0,
                        "setlNormInt": 0,
                        "setlCommOdInt": 0,
                        "setlFeeAmt": 0,
                        "prodPrcpAmt": 0,
                        "prodIntAmt": 0,
                        "prodCommIntAmt": 0,
                        "psOdInd": "N",
                        "intRate": 0.085,
                        "odIntRate": 0.1275,
                        "psRemPrcp": 10000,
                        "setlInd": "N",
                        "psInstmAmt": 0,
                        "ppErInd": "N",
                        "lastSetlDt": "",
                        "setlOdIntAmt": 0
                    }
                ]
              }
            }
        repayplan = {
                    "perdNo": 0,
                    "dueDt": "2033-04-28",
                    "psPrcpAmt": 0,
                    "psNormIntAmt": 0,
                    "psOdIntAmt": 0,
                    "psCommOdInt": 0,
                    "psFeeAmt": 0,
                    "setlPrcp": 0,
                    "setlNormInt": 0,
                    "setlCommOdInt": 0,
                    "setlFeeAmt": 0,
                    "prodPrcpAmt": 0,
                    "prodIntAmt": 0,
                    "prodCommIntAmt": 0,
                    "psOdInd": "N",
                    "intRate": 0.085,
                    "odIntRate": 0.1275,
                    "psRemPrcp": 10000,
                    "setlInd": "N",
                    "psInstmAmt": 0,
                    "ppErInd": "N",
                    "lastSetlDt": "",
                    "setlOdIntAmt": 0
                  }

        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplan)
            repayment_plan['perdNo'] = i + 1
            repayment_plan['psPrcpAmt'] = float(fee_info['principal'])/100
            repayment_plan['psNormIntAmt'] = float(fee_info['interest'])/100
            repayment_plan['psInstmAmt'] = float(fee_info['principal'] + fee_info['interest'])/100
            repayment_plan['dueDt'] = fee_info['date']
            body['data']['repaymentPlanList'].append(repayment_plan)
        self.update(api, body)

    def update_image_download(self):
        """
        合同查询
        """
        api = '/runlou/changyin_mingdonghua_rl/loan.assis.cy.image.download'
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "status": "S",
                "content": {
                  "data": "dGVzdGV0c3RldHN0",
                  "fileName": "个人借款合同"
                }
              }
            }
        self.update(api, body)

    def update_business_apply(self):
        """
        担保方信息推送
        """
        api = '/mingdonghua/changyin_mingdonghua_rl/business/apply'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "errcode": "0",
                "errmsg": "保存成功",
                "traceId": "3562.102.@id"
            }
        }
        self.update(api, body)

    def update_loan_assis_cy_settlement_cert_apply(self):
        """
        担保方信息推送
        """
        api = '/runlou/changyin_mingdonghua_rl/loan.assis.cy.settlement.cert.apply'
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "status": "S",
                "statusDesc": "接收成功"
              }
            }
        self.update(api, body)

    def update_loan_assis_cy_settlement_cert_query(self):
        """
        担保方信息推送
        """
        api = '/runlou/changyin_mingdonghua_rl/loan.assis.cy.settlement.cert.query'
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "status": "S",
                "imgUrl": "/writable/cyxf/30/2035/04/06/14234102517128281666/loan_clear_certificate.pdf"
              }
            }
        self.update(api, body)