# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.function.gbiz.gbiz_db_function import *


class ShilongSipingMock(Easymock):
    def update_upload_file_success(self):
        api = "/shilong/v2/siping/UploadFile"
        mode = '''{
    "code": 0,
    "message": "成功",
    "data": {
          "fileId": "@guid",
          "url": "http://shilong.oss-accelerate.aliyuncs.com/d0d26a842d784b8d85f94d4665ed4358.pdf",
        }}'''
        self.update(api, mode)

    def update_upload_file_fail(self):
        api = "/shilong/v2/siping/UploadFile"
        mode = '''{
          "fileId": "",
          "url": "",
        }'''
        self.update(api, mode)

    def update_credit_apply_success(self, item_no):
        api = "/shilong/v2/siping/CreditApply"
        mode = {
            "code": 0000000,
            "message": "成功",
            "data": {
                "status": True,
                "serialNo": item_no
            }
        }
        self.update(api, mode)

    def update_credit_apply_fail(self, item_no):
        api = "/shilong/v2/siping/CreditApply"
        mode = {
            "code": 0000000,
            "message": "成功",
            "data": {
                "status": False,
                "serialNo": item_no
            }
        }
        self.update(api, mode)

    def update_credit_apply_already_exist(self, item_no):
        api = "/shilong/v2/siping/CreditApply"
        mode = {
            "code": 2001008,
            "message": "客户已授信",
            "data": {}
        }
        self.update(api, mode)

    def update_credit_result_not_exist(self):
        api = "/shilong/v2/siping/QueryCreditResult"
        mode = {
            "code": 2001030,
            "message": "授信流水号不存在",
            "data": {}
        }
        self.update(api, mode)

    def update_credit_result_success(self, asset_info):
        api = "/shilong/v2/siping/QueryCreditResult"
        mode = {
            "code": 0000000,
            "message": "成功",
            "data": {
                "productNo": None,
                "creditTotalAmount": asset_info['data']['asset']['amount'],
                "startDate": None,
                "endDate": None,
                "useAmount": None,
                "availAmount": 0,
                "frozenAmount": None,
                "approvalStatus": 2,
                "validStatus": 1,
                "creditApplyId": asset_info['data']['asset']['item_no'],
                "loanInterestRate": "0.016700",
                "currentNumRange": None,
                "reason": None,
                "prodcd": "PD0006",
                "prodde": "test产品",
                "cycflg": "N",
                "expdat": "20200509"
            }}
        self.update(api, mode)

    def update_credit_result_fail(self, asset_info):
        api = "/shilong/v2/siping/QueryCreditResult"
        mode = {
            "code": 0000000,
            "message": "成功",
            "data": {
                "productNo": None,
                "creditTotalAmount": asset_info['data']['asset']['amount'],
                "startDate": None,
                "endDate": None,
                "useAmount": None,
                "availAmount": 0,
                "frozenAmount": None,
                "approvalStatus": 3,
                "validStatus": 1,
                "creditApplyId": asset_info['data']['asset']['item_no'],
                "loanInterestRate": "0.016700",
                "currentNumRange": None,
                "reason": None,
                "prodcd": "PD0006",
                "prodde": "test产品",
                "cycflg": "N",
                "expdat": "20200509"
            }}
        self.update(api, mode)

    def update_credit_result_wait(self, asset_info):
        api = "/shilong/v2/siping/QueryCreditResult"
        mode = {
            "code": 0000000,
            "message": "成功",
            "data": {
                "productNo": None,
                "creditTotalAmount": asset_info['data']['asset']['amount'],
                "startDate": None,
                "endDate": None,
                "useAmount": None,
                "availAmount": 0,
                "frozenAmount": None,
                "approvalStatus": 1,
                "validStatus": 1,
                "creditApplyId": asset_info['data']['asset']['item_no'],
                "loanInterestRate": "0.016700",
                "currentNumRange": None,
                "reason": None,
                "prodcd": "PD0006",
                "prodde": "test产品",
                "cycflg": "N",
                "expdat": "20200509"
            }}
        self.update(api, mode)

    def update_loan_apply_success(self):
        api = "/shilong/v2/siping/LendApply"
        mode = '''{
        "code": 0,
        "message": "成功",
        "data": {"orderNo":"loan@id"}}'''
        self.update(api, mode)

    def update_loan_apply_fail(self):
        api = "/shilong/v2/siping/LendApply"
        mode = '''{
        "code": 0,
        "message": "成功",
        "data": {}}'''
        self.update(api, mode)

    def update_loan_result_success(self, asset_info):
        api = "/shilong/v2/siping/LendApplyQuery"
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        mode = '''{
        "code": 0,
        "message": "成功",
        "data": {
           "applyInfoList": [{
             "orderNo": "%s",
             "applyTime": null,
             "nameEncrypt": "%s",
             "idType": "1",
             "idNoEncrypt": "%s",
             "loanNo": "loan@id",
             "applyAmt": "%s.0",
             "auditAmt": 0,
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
                asset_info['data']['asset']['period_count'])
        self.update(api, mode)

    def update_loan_result_fail(self, asset_info):
        api = "/shilong/v2/siping/LendApplyQuery"
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        mode = '''{
        "code": 0,
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
             "applyStatus": "1008",
             "reason": "放款失败",
             "loanNum": %s,
             "loanAccount": "801115401481053875"
           }]
         }}
         ''' % (alr_info[0]['asset_loan_record_due_bill_no'],
                asset_info['data']['borrower']['idnum_encrypt'],
                asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['period_count'])
        self.update(api, mode)

    def update_loan_result_wait(self, asset_info):
        api = "/shilong/v2/siping/LendApplyQuery"
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        mode = '''{
        "code": 0,
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
        api = "/shilong/v2/siping/QueryRepayPlan"
        asset_info = get_asset_import_data_by_item_no(item_no)
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        alr_info = get_asset_loan_record_by_item_no(item_no)
        mode = {
            "code": 0,
            "message": "成功",
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
        api = "/shilong/v2/siping/LendContractQuery"
        mode = '''  {
        "code": 0,
        "message": "成功",
        "data": {
           "orderNo": function({
             _req
           }) {
             return _req.body.data.orderNo
           },
           "contractList": [{
             "contractNo": "22222",
             "contractType": "2",
             "contractUrl": "http://cashtest-1251122539.cossh.myqcloud.com/2018/11/09/1109_164248_4cc84186-e859-4332-abe5-51f13799583e.jpg"
           },
           {
             "contractNo": "22222",
             "contractType": "4",
             "contractUrl": "http://cashtest-1251122539.cossh.myqcloud.com/2018/11/09/1109_164248_4cc84186-e859-4332-abe5-51f13799583e.jpg"
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
    ShilongSipingMock().update_repay_plan('ph_slsp_8913813921')
