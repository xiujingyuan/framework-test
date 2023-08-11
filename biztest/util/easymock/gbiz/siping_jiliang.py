# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_repay_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.function.gbiz.gbiz_db_function import *


class SiPingJiLiangMock(Easymock):

    def update_bind_card_result_query_success(self):
        api = "/shilong/v3/siping_jiliang/BindCardResultQuery"
        modo = {
            "code": "-1",
            "message": "failed:BF00134绑定关系不存在",
            "data": None,
            "success": False
        }
        self.update(api, modo)

    def update_pre_bind_card_success(self):
        api = "/shilong/v3/siping_jiliang/PreBindCard"
        modo = {
            "code": "0000000",
            "message": "成功",
            "data": {
                "status": "0",
                "uniqueCode": "@id",
                "failureCode": None,
                "failureMsg": "success"
            },
            "success": True
        }
        self.update(api, modo)

    def update_bind_card_confirm_success(self):
        api = "/shilong/v3/siping_jiliang/BindCardConfirm"
        modo = {
            "code": "0000000",
            "message": "成功",
            "data": {
                "status": "0",
                "protocolNo": "@id",
                "failureCode": None,
                "failureMsg": "success"
            },
            "success": True
        }
        self.update(api, modo)

    def update_upload_file_success(self):
        api = "/shilong/v3/siping_jiliang/UploadFile"
        mode = {
            "code": "0000000",
            "message": "成功",
            "data": {
                "fileId": "6687375a-fb5f-4300-9221-c14b98ea59e8.png",
                "url": "http://shilong.oss-accelerate.aliyuncs.com/6687375a-fb5f-4300-9221-c14b98ea59e8.png?Expires=1631255096&OSSAccessKeyId=LTAI4Fd796zA78iigXVH6ceS&Signature=Fwd8PuKv1KaoRqtEPgWSe918sWg%3D"
            },
            "success": True
        }
        self.update(api, mode)

    def update_upload_file_fail(self):
        api = "/shilong/v2/siping_jiliang/UploadFile"
        mode = {
            "code": "0000000",
            "message": "成功",
            "data": {
                "fileId": ""},
            "success": True
        }
        self.update(api, mode)

    def update_credit_apply_success(self, item_no):
        api = "/shilong/v3/siping_jiliang/CreditApply"
        mode = {
            "code": "0000000",
            "message": "成功",
            "data": {
                "status": True,
                "serialNo": item_no
            },
            "success": True
        }
        self.update(api, mode)

    def update_credit_apply_fail(self, item_no):
        api = "/shilong/v3/siping_jiliang/CreditApply"
        mode = {
            "code": "0000000",
            "message": "成功",
            "data": {
                "status": False,
                "serialNo": item_no
            },
            "success": True
        }
        self.update(api, mode)

    def update_credit_apply_already_exist(self, item_no):
        api = "/shilong/v3/siping_jiliang/CreditApply"
        mode = {
            "code": "2001008",
            "message": "客户已授信",
            "data": {}
        }
        self.update(api, mode)

    def update_credit_result_not_exist(self):
        api = "/shilong/v3/siping_jiliang/QueryCreditResult"
        mode = {
            "code": "2001030",
            "message": "授信流水号不存在",
            "data": {}
        }
        self.update(api, mode)

    def update_credit_result_success(self, asset_info):
        api = "/shilong/v3/siping_jiliang/QueryCreditResult"
        mode = {
            "code": "0000000",
            "message": "成功",
            "success": True,
            "data": {
                "productNo": None,
                "approvalStatus": 2,  # 0-未审核 1-审核中 2-审核成功 3-审核拒绝 4-人工审核 5-审核失败 6-待处理 7-处理中
                "validStatus": 1,
                "reason": "成功",
                "creditTotalAmount": asset_info['data']['asset']['amount'],
                "startDate": "2022-02-09 16:00:00",
                "endDate": "2023-02-09 16:00:00",
                "prodcd": None,
                "prodde": None,
                "cycflg": None,
                "expdat": None,
                "useAmount": 0,
                "availAmount": asset_info['data']['asset']['amount'],
                "frozenAmount": 0,
                "creditApplyId": asset_info['data']['asset']['item_no'],
                "loanInterestRate": "",
                "currentNumRange": ""
            }
        }
        self.update(api, mode)

    def update_credit_result_fail(self, asset_info):
        api = "/shilong/v3/siping_jiliang/QueryCreditResult"
        mode = {
            "code": "0000000",
            "message": "成功",
            "success": True,
            "data": {
                "productNo": None,
                "approvalStatus": 3,
                "validStatus": 1,
                "reason": "mock approvalStatus失败",
                "creditTotalAmount": asset_info['data']['asset']['amount'],
                "startDate": "2022-02-09 16:00:00",
                "endDate": "2023-02-09 16:00:00",
                "prodcd": None,
                "prodde": None,
                "cycflg": None,
                "expdat": None,
                "useAmount": 0,
                "availAmount": asset_info['data']['asset']['amount'],
                "frozenAmount": 0,
                "creditApplyId": asset_info['data']['asset']['item_no'],
                "loanInterestRate": "",
                "currentNumRange": ""
            }}
        self.update(api, mode)

    def update_credit_result_wait(self, asset_info):
        api = "/shilong/v3/siping_jiliang/QueryCreditResult"
        mode = {
            "code": "0000000",
            "message": "成功",
            "success": True,
            "data": {
                "productNo": None,
                "approvalStatus": 1,
                "validStatus": 1,
                "reason": "成功",
                "creditTotalAmount": asset_info['data']['asset']['amount'],
                "startDate": "2022-02-09 16:00:00",
                "endDate": "2023-02-09 16:00:00",
                "prodcd": None,
                "prodde": None,
                "cycflg": None,
                "expdat": None,
                "useAmount": 0,
                "availAmount": asset_info['data']['asset']['amount'],
                "frozenAmount": 0,
                "creditApplyId": asset_info['data']['asset']['item_no'],
                "loanInterestRate": "",
                "currentNumRange": ""
            }}
        self.update(api, mode)

    def update_querylpr_success(self):
        api = "/shilong/v3/siping_jiliang/QueryLpr"
        mode = {
            "code": "0000000",
            "message": "success",
            "data": {
                "lprCode": [{
                    "lprTerm": "1",
                    "lprValue": 5.15,
                    "lprPublishDate": "2022-07-20 00:00:00",
                    "lprActiveDate": "2022-07-21 00:00:00"
                }
                ]
            },
            "success": True
        }

        self.update(api, mode)

    def update_querylpr_fail(self):
        api = "/shilong/v3/siping_jiliang/QueryLpr"
        mode = {
            "code": "0000000",
            "message": "success",
            "data": {
                "lprCode": [{
                }
                ]
            },
            "success": True
        }

        self.update(api, mode)

    def update_loan_apply_success(self):
        api = "/shilong/v3/siping_jiliang/LendApply"
        mode = {
            "code": "0000000",
            "message": "成功",
            "data": {
                "orderNo": "loan@id"
            },
            "success": True
        }
        self.update(api, mode)

    def update_loan_apply_fail(self):
        api = "/shilong/v3/siping_jiliang/LendApply"
        mode = {
            "code": "1111111",
            "message": "这是mockcode返回失败",
            "data": {
            },
            "success": True
        }
        self.update(api, mode)

    def update_loan_result_success(self, asset_info):
        api = "/shilong/v3/siping_jiliang/LendApplyQuery"
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        mode = '''{
        "code": "0000000",
        "message": "success",
        "data": {
           "applyInfoList": [{
             "orderNo": "%s",
             "applyTime": null,
             "nameEncrypt": "%s",
             "idType": "1",
             "idNoEncrypt": "%s",
             "loanNo": "loan@id",
             "applyAmt": "%s.0",
             "auditAmt": %s.0,
            "interestDate": "20200515",
            "maturityDate": "20210514",
            "loanAccount": "",
            "loanNum": %s,
            "loanpaytime": "@now",
            "applyStatus": "1007",
            "reason": ""
           }]
         }}
         ''' % (alr_info[0]['asset_loan_record_due_bill_no'],
                asset_info['data']['borrower']['name_encrypt'],
                asset_info['data']['borrower']['idnum_encrypt'],
                asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['period_count'])

        self.update(api, mode)

    def update_loan_result_fail(self, asset_info):
        api = "/shilong/v3/siping_jiliang/LendApplyQuery"
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        mode = '''{
        "code": "0000000",
        "message": "成功",
        "data": {
           "applyInfoList": [{
             "orderNo": "%s",
             "applyTime": null,
             "name": "test",
             "idType": "1",
             "idNo": "%s",
             "loanNo": "loan@id",
             "applyAmt": "%s",
             "auditAmt": %s,
             "loanpaytime": "@now",
             "applyStatus": "1008", 
             "reason": "放款失败",
             "loanNum": %s,
             "loanAccount": "801115401481053875"
           }]
         }}
         ''' % (alr_info[0]['asset_loan_record_due_bill_no'],
                asset_info['data']['borrower']['idnum_encrypt'],
                asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['period_count'])
        self.update(api, mode)

    def update_loan_result_wait(self, asset_info):
        api = "/shilong/v3/siping_jiliang/LendApplyQuery"
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        mode = '''{
        "code": "0000000",
        "message": "成功",
        "data": {
           "applyInfoList": [{
             "orderNo": "%s",
             "applyTime": null,
             "name": "test",
             "idType": "1",
             "idNo": "%s",
             "loanNo": "loan@id",
             "applyAmt": "%s",
             "auditAmt": 0,
             "loanpaytime": "@now",
             "applyStatus": "1006",
             "reason": "成功",
             "loanNum": %s,
             "loanAccount": "801115401481053875"
           }]
         }}
         ''' % (alr_info[0]['asset_loan_record_due_bill_no'],
                asset_info['data']['borrower']['idnum_encrypt'],
                asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['period_count'])
        self.update(api, mode)

    def update_repay_plan(self, item_no):
        api = "/shilong/v3/siping_jiliang/QueryRepayPlan"
        asset_info = get_asset_import_data_by_item_no(item_no)
        rate_info = cmdb_rate_repay_calculate_v6(asset_info)
        alr_info = get_asset_loan_record_by_item_no(item_no)
        mode = {
            "code": "0000000",
            "message": "success",
            "data": {
                "resultList": [{
                    "loanNo": alr_info[0]['asset_loan_record_trade_no'],
                    "repayPlanList": []
                }]
            }}
        repayment_plan_tmp = {
            "currentNum": 1,
            "preRepayAmount": 2093.27,
            "preRepayPrincipal": 1928.94,
            "preRepayInterest": 164.33,
            "preRepayOverdueFee": 0.00,
            "repayRepayAmount": 2093.27,
            "repayRepayPrincipal": 1928.94,
            "repayRepayInterest": 164.33,
            "repayRepayOverdueFee": 0.00,
            "preRepayDate": "2020-07-24",
            "repayPlanStatus": "4",
            "lastRepayDate": ""
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['currentNum'] = i + 1
            repayment_plan['preRepayPrincipal'] = float(fee_info['principal']) / 100
            repayment_plan['preRepayInterest'] = float(fee_info['interest']) / 100
            repayment_plan['preRepayAmount'] = float(
                '%.2f' % (repayment_plan['preRepayPrincipal'] + repayment_plan['preRepayInterest']))
            repayment_plan['preRepayDate'] = fee_info['date']
            mode['data']['resultList'][0]['repayPlanList'].append(repayment_plan)
        self.update(api, mode)

    def update_contract_success(self):
        api = "/shilong/v3/siping_jiliang/LendContractQuery"
        mode = '''  {
        "code": "0000000",
        "message": "success",
        "success":true,
        "data": {
           "orderNo": function({
             _req
           }) {
             return _req.body.orderNo
           },
           "contractList": [{
             "contractNo": "",
             "contractType": "2",
             "contractUrl": "http://shilong.oss-accelerate.aliyuncs.com/dfcb04e6940b4e11ba9e6747653043bdguacont-01.pdf?Expires=1947374726&OSSAccessKeyId=LTAI4Fd796zA78iigXVH6ceS&Signature=rTLWDEFuec%2B6wQxrXRDcfq5HLq8%3D"
           },
           {
             "contractNo": "",
             "contractType": "4",
             "contractUrl": "http://shilong.oss-accelerate.aliyuncs.com/8379aee4c607457e9feaf402ba07126floaninfo-01.pdf?Expires=1947374723&OSSAccessKeyId=LTAI4Fd796zA78iigXVH6ceS&Signature=L%2B2fgLR%2F%2FN2tB57KtGRrEUG3VNA%3D"
           }]
         }}
        '''
        self.update(api, mode)

    def update_pre_repay_trial(self, trade_no):
        api = "/shilong/siping/PreRepayTrial"
        mode = '''{
              "body": {
                "receiptNo": "%s", ///取值于biz的alr表的trade_no
                "preRepayPrincipal": 4000,
                "preRepayInterest": 28.33,
                "overdueFee": 0.00,
                "totalAmt": 4028.33
              },
              "message": {
                "returnCode": "0000000", //非0000000---失败重试；0000000---成功
                "returnMsg": "支支mock"
              }
            }
         ''' % trade_no
        self.update(api, mode)


if __name__ == "__main__":
    pass
    # ShilongSipingMock().update_repay_plan('ph_slsp_8913813921')
