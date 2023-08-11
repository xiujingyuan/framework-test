# -*- coding: utf-8 -*-
from copy import deepcopy

from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no


class YunxinQuanhuMock(Easymock):
    def update_sign_apply_success(self):
        api = "/yunxin_quanhu/v2/protocolBinding/getBankContractId"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "isSigned": "1",
                "transactionNo": "@id",
                "signNo": "",
                "status": {
                    "isSuccess": True,
                    "requestId": "@id",
                    "responseCode": "0000",
                    "responseMessage": "成功!",
                    "warningMessage": ""
                }
            }}
        self.update(api, mode)

    def update_sign_apply_fail(self):
        api = "/yunxin_quanhu/v2/protocolBinding/getBankContractId"
        mode = {}
        self.update(api, mode)

    def update_sign_confirm_success(self):
        api = "/yunxin_quanhu/v2/protocolBinding/uploadVerificationCode"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "signNo": "@id",
                "status": {
                    "isSuccess": True,
                    "requestId": "@id",
                    "responseCode": "0000",
                    "responseMessage": "成功!",
                    "warningMessage": ""
                }
            }}
        self.update(api, mode)

    def update_sign_confirm_fail(self):
        api = "/yunxin_quanhu/v2/protocolBinding/uploadVerificationCode"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "status": {
                    "isSuccess": False,
                    "requestId": "@id",
                    "responseCode": "80800032",
                    "responseMessage": "签订确认失败:[绑定失败]",
                    "warningMessage": ""
                }
            }}
        self.update(api, mode)

    def update_query_protocol_success(self):
        api = "/yunxin_quanhu/v2/protocolBinding/queryProtocolInfo"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "protocolInfos": [{
                    "channel": 1,
                    "signNo": "@id",
                    "signStatus": "1",
                    "signTime": get_date(),
                    "transactionNo": "@id",
                }],
                "status": {
                    "isSuccess": True,
                    "requestId": "@id",
                    "responseCode": "0000",
                    "responseMessage": "成功!",
                    "warningMessage": ""
                }
            }}
        self.update(api, mode)

    def update_query_protocol_fail(self):
        api = "/yunxin_quanhu/v2/protocolBinding/queryProtocolInfo"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "protocolInfos": [{
                    "channel": 1,
                    "signNo": "",
                    "signStatus": "0",
                    "signTime": get_date(),
                    "transactionNo": "@id",
                }],
                "status": {
                    "isSuccess": True,
                    "requestId": "@id",
                    "responseCode": "0000",
                    "responseMessage": "成功!",
                    "warningMessage": ""
                }
            }}
        self.update(api, mode)

    def update_query_balance_success(self):
        api = "/yunxin_quanhu/v2/dedicatedAccount/queryingBalance"
        mode = '''{
        "code": "0",
        "message": "",
        "data": {
            "data": {
                "productCode": function({_req}){return _req.body.productCode},
                "accountNo": function({_req}){return _req.body.accountNo},
                "releaseBalance": 100000.000,
                "queryDateTime": "@now",
                "enabled": true,
                "canPay": true
            },
            "status": {
                "isSuccess": true,
                "requestId": "@id",
                "responseCode": "0000",
                "responseMessage": "成功",
                "warningMessage": ""
            }
        }}'''
        self.update(api, mode)

    def update_loan_apply_success(self, amount):
        api = "/yunxin_quanhu/v2/applyLoan/commitApplyLoanInfo"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "orderId": "@id",
                "approvalAmount": amount,
                "subAccount": "",
                "status": {
                    "isSuccess": True,
                    "requestId": "@id",
                    "responseCode": "0000",
                    "responseMessage": "成功",
                    "warningMessage": None
                }
            }}
        self.update(api, mode)

    def update_loan_apply_fail(self):
        api = "/yunxin_quanhu/v2/applyLoan/commitApplyLoanInfo"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "status": {
                    "isSuccess": False,
                    "requestId": "@id",
                    "responseCode": "0021",
                    "responseMessage": "预期借款月利率区间[0.0,0.009000000000000001]",
                    "warningMessage": None
                }
            }}
        self.update(api, mode)

    def update_loan_query_success(self):
        api = "/yunxin_quanhu/v2/applyLoan/riskAuditResult"
        mode = '''{
           "code": "0",
           "message": "",
           "data": {
            "auditStatus": 8,
            "status": {
                "isSuccess": true,
                "requestId": "@id",
                "responseCode": "0000",
                "responseMessage": "查询成功",
                "warningMessage": null
            }}
        }
        // 审核状态
        // 1==风险控制不通过 
        // 2==风险控制通过 
        // 3==待审核 
        // 4==审核通过 
        // 5==审核未通过 
        // 6==放款成功 
        // 7==放款失败 
        // 8==待放款 
        // 9==放款中 '''
        self.update(api, mode)

    def update_loan_query_fail(self):
        api = "/yunxin_quanhu/v2/applyLoan/riskAuditResult"
        mode = '''{
         "code": "0",
         "message": "",
         "data": {
            "auditStatus": 5,
            "status": {
                "isSuccess": true,
                "requestId": "@id",
                "responseCode": "0000",
                "responseMessage": "查询成功",
                "warningMessage": null
            }}
        }
        // 审核状态
        // 1==风险控制不通过 
        // 2==风险控制通过 
        // 3==待审核 
        // 4==审核通过 
        // 5==审核未通过 
        // 6==放款成功 
        // 7==放款失败 
        // 8==待放款 
        // 9==放款中 '''
        self.update(api, mode)

    def update_apply_confirm_success(self):
        api = "/yunxin_quanhu/v2/applyLoan/confirmPayment"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "status": {
                    "isSuccess": True,
                    "requestId": "@id",
                    "responseCode": "0000",
                    "responseMessage": "放款处理中",
                    "warningMessage": None
                }
            }}
        self.update(api, mode)

    def update_apply_confirm_fail(self):
        api = "/yunxin_quanhu/v2/applyLoan/confirmPayment"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "status": {
                    "isSuccess": False,
                    "requestId": "@id",
                    "responseCode": "0021",
                    "responseMessage": "当前订单未到达待放款状态!",
                    "warningMessage": None
                }
            }}
        self.update(api, mode)

    def update_confirm_query_success(self, asset_info):
        api = "/yunxin_quanhu/v2/applyLoan/queryBatchTradingStatus"
        mode = '''{
         "code": "0",
         "message": "",
         "data": {
            "batchPaymentDetails": [{
                "paymentDetails": [{
                    "amount": %s.00,
                    "accountNo": "6222002182922359070",
                    "accountNoEncrypt": "%s",
                    "name": "芦建国",
                    "nameEncrypt": "%s",
                    "detailNo": "1",
                    "bankSerialNo": "405093439905009664",
                    "processStatus": 1,
                    "result": "",
                    "actExcutedTime": "@now"
                }],
                "ynxtLoanContractNumber": null,
                "uniqueId": function({_req}){return _req.body.uniqueIds[0]},
                "orderId": function({_req}){return _req.body.uniqueIds[0]},
                "productCode": "J03400",
                "auditStatus": 2,
                "auditMessage": null
            }],
            "status": {
                "isSuccess": true,
                "requestId": "@id",
                "responseMessage": null,
                "responseCode": "0000",
                "warningMessage": null
            }
        }}
        // processStatus 放款中=0,成功=1,失败=2,业务不执行=3（多目标放款情况下适用）,异常=4（先放后扣情况下适用），放款指令发送失败=9''' \
               % (asset_info['data']['asset']['amount'],
                  asset_info['data']['receive_card']['num_encrypt'],
                  asset_info['data']['borrower']['name_encrypt'])
        self.update(api, mode)

    def update_confirm_query_fail(self, asset_info):
        api = "/yunxin_quanhu/v2/applyLoan/queryBatchTradingStatus"
        mode = '''{
        "code": "0",
        "message": "",
        "data": {
            "batchPaymentDetails": [{
                "paymentDetails": [{
                    "amount": %s.00,
                    "accountNo": "6222002182922359070",
                    "accountNoEncrypt": "%s",
                    "name": "芦建国",
                    "nameEncrypt": "%s",
                    "detailNo": "1",
                    "bankSerialNo": "405093439905009664",
                    "processStatus": 2,
                    "result": "招商返回放款结果为拒绝！(拒绝原因：测试置为失败)",
                    "actExcutedTime": "@now"
                }],
                "ynxtLoanContractNumber": null,
                "uniqueId": function({_req}){return _req.body.uniqueIds[0]},
                "orderId": function({_req}){return _req.body.uniqueIds[0]},
                "productCode": "J03400",
                "auditStatus": 2,
                "auditMessage": null
            }],
            "status": {
                "isSuccess": true,
                "requestId": "@id",
                "responseMessage": null,
                "responseCode": "0000",
                "warningMessage": null
            }}}
        // processStatus 放款中=0,成功=1,失败=2,业务不执行=3（多目标放款情况下适用）,异常=4（先放后扣情况下适用），放款指令发送失败=9''' \
               % (asset_info['data']['asset']['amount'],
                  asset_info['data']['receive_card']['num_encrypt'],
                  asset_info['data']['borrower']['name_encrypt'])
        self.update(api, mode)

    def update_get_contract_success(self):
        api = "/yunxin_quanhu/v2/applyLoan/getContractFile"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "signStatus": "4",
                "fileImageUrl": "http://jbimages.oss-cn-shanghai.aliyuncs.com/1558058010390d779436.pdf",
                "status": {
                    "isSuccess": True,
                    "requestId": "@id",
                    "responseCode": "0000",
                    "responseMessage": "获取成功!",
                    "warningMessage": None
                }
            }}
        self.update(api, mode)

    def update_get_contract_process(self):
        api = "/yunxin_quanhu/v2/applyLoan/getContractFile"
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "signStatus": "8",
                "status": {
                    "isSuccess": False,
                    "requestId": "@id",
                    "responseCode": "6010016",
                    "responseMessage": "签章处理中!",
                    "warningMessage": None
                }
            }}
        self.update(api, mode)

    def update_replay_plan(self, asset_info):
        api = "/yunxin_quanhu/v2/repayment/paymentSchedule"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "repayScheduleList": [
                ],
                "status": {
                    "isSuccess": True,
                    "requestId": None,
                    "responseCode": "0000",
                    "responseMessage": "成功",
                    "warningMessage": None
                }
            }}
        repayment_plan_tmp = {
            "repaySeqId": 2827,
            "contractNumber": "20191225JJ004844",
            "repayDate": "2020-06-25 00:00:00.0",
            "repayAmount": 553.75,
            "principal": 537.64,
            "interest": 16.11,
            "fee": 0,
            "odInterest": 0,
            "payedDate": None,
            "payedAmount": 0,
            "payedPrincipal": 0,
            "payedInterest": 0,
            "payedFee": 0,
            "adOdInterest": 0,
            "overdueDays": 0,
            "repayStatus": "0",
            "term": "6"
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['term'] = i + 1
            repayment_plan['principal'] = float(fee_info['principal']) / 100
            repayment_plan['interest'] = float(fee_info['interest']) / 100
            repayment_plan['repayAmount'] = float('%.2f' % (repayment_plan['principal'] + repayment_plan['interest']))
            repayment_plan['repayDate'] = fee_info['date'] + " 00:00:00.0"
            repayment_plan['contractNumber'] = fee_info['date']
            repayment_plan['contractNumber'] = \
                get_asset_loan_record_by_item_no(
                    asset_info["data"]["asset"]["item_no"])[0]["asset_loan_record_due_bill_no"]
            mode["data"]['repayScheduleList'].append(repayment_plan)
        self.update(api, mode)

    def update_replay_plan_with_diff(self, asset_info, diff_type):
        """
        diff_type='diff_principal'，本金不一致
        diff_type='diff_period'，期次不一致
        diff_type='diff_due_at'，还款日期不一致
        diff_type='diff_interest_tolerable'，利息不一致，容差范围内
        diff_type='diff_interest_intolerable'，利息不一致，超过容差范围
        mock数据都将差别放在第1期
        :param asset_info:
        :param type:
        :return:
        """
        api = "/yunxin_quanhu/v2/repayment/paymentSchedule"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
            "code": "0",
            "message": "",
            "data": {
                "repayScheduleList": [
                ],
                "status": {
                    "isSuccess": True,
                    "requestId": None,
                    "responseCode": "0000",
                    "responseMessage": "成功",
                    "warningMessage": None
                }
            }}
        repayment_plan_tmp = {
            "repaySeqId": 2827,
            "contractNumber": "20191225JJ004844",
            "repayDate": "2020-06-25 00:00:00.0",
            "repayAmount": 553.75,
            "principal": 537.64,
            "interest": 16.11,
            "fee": 0,
            "odInterest": 0,
            "payedDate": None,
            "payedAmount": 0,
            "payedPrincipal": 0,
            "payedInterest": 0,
            "payedFee": 0,
            "adOdInterest": 0,
            "overdueDays": 0,
            "repayStatus": "0",
            "term": "6"
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['term'] = i + 1
            repayment_plan['principal'] = float(fee_info['principal']) / 100
            repayment_plan['interest'] = float(fee_info['interest']) / 100
            repayment_plan['repayAmount'] = float('%.2f' % (repayment_plan['principal'] + repayment_plan['interest']))
            repayment_plan['repayDate'] = fee_info['date'] + " 00:00:00.0"
            repayment_plan['contractNumber'] = fee_info['date']
            repayment_plan['contractNumber'] = \
                get_asset_loan_record_by_item_no(
                    asset_info["data"]["asset"]["item_no"])[0]["asset_loan_record_due_bill_no"]
            mode["data"]['repayScheduleList'].append(repayment_plan)
        # 根据type修改还款数据
        if diff_type == 'diff_principal':
            mode["data"]['repayScheduleList'][0]['principal'] += 0.1
            mode["data"]['repayScheduleList'][0]['repayAmount'] += 0.1
        elif diff_type == 'diff_due_at':
            mode["data"]['repayScheduleList'][0]['repayDate'] = '2020-01-01 00:00:00'
        elif diff_type == 'diff_interest_tolerable':
            mode["data"]['repayScheduleList'][0]['interest'] += 0.01
            mode["data"]['repayScheduleList'][0]['repayAmount'] += 0.01
        elif diff_type == 'diff_interest_intolerable':
            mode["data"]['repayScheduleList'][0]['interest'] -= 1
            mode["data"]['repayScheduleList'][0]['repayAmount'] -= 1
        elif diff_type == 'diff_period':
            mode["data"]['repayScheduleList'].pop(0)

        self.update(api, mode)


if __name__ == "__main__":
    pass
