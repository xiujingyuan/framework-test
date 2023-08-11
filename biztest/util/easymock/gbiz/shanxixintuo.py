# -*- coding: utf-8 -*-
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_loan_record_by_item_no
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from copy import deepcopy
import datetime


class ShanxiXintuoMock(Easymock):

    def get_due_bill_no(self, item_no):
        alr = get_asset_loan_record_by_item_no(item_no)
        bill_no = alr[0].get('asset_loan_record_due_bill_no')
        if bill_no:
            return bill_no
        else:
            return None

    def update_trustplanquery_success(self):
        '''
        信托计划查询
        :return:
        '''
        api = "/shanxixintuo/trustPlanQuery"
        body = {
            "code": 0,
            "message": "调用成功",
            "data": [
                {
                    "bankCode": "allinpay",
                    "receiptBankAccount": "1111111111111111111",
                    "trustCode": "111111",
                    "endDate": "2022-12-19",
                    "rate": 0.154,
                    "trustName": "信托1号",
                    "receiptBankAccountName": "山西信托计划1",
                    "currentBalance": 10000000000,
                    "reserveAmount": 10000,
                    "startDate": "2021-05-19",
                    "receiptBankName": "CBHB"
                },
                {
                    "bankCode": "allinpay",
                    "receiptBankAccount": "22222222222222222222",
                    "trustCode": "222222",
                    "endDate": "2022-12-19",
                    "rate": 0.154,
                    "trustName": "信托2号",
                    "receiptBankAccountName": "山西信托计划2",
                    "currentBalance": 20000000000,
                    "reserveAmount": 10000,
                    "startDate": "2021-05-19",
                    "receiptBankName": "CBHB"
                },
                {
                    "bankCode": "allinpay",
                    "receiptBankAccount": "3333333333333333333",
                    "trustCode": "333333",
                    "endDate": "2022-12-19",
                    "rate": 0.154,
                    "trustName": "信托3号",
                    "receiptBankAccountName": "山西信托计划3",
                    "currentBalance": 30000000000,
                    "reserveAmount": 10000,
                    "startDate": "2021-05-19",
                    "receiptBankName": "CBHB"
                }
            ]
        }
        self.update(api, body)

    def update_signconfirmquery(self):
        '''
        代扣签约列表查询
        :return:
        '''
        api = '/shanxixintuo/signConfirmQuery'
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "agreementNo": "",
                "description": "未签约",
                "expectPayCompanyId": "allInPay",
                "status": "01"
            }
        }
        self.update(api, body)

    def update_signapply(self):
        '''
        代扣签约申请
        :return:
        '''
        api ='/shanxixintuo/signApply'
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "signReqNo": "ac98171933e64049ab19a1714d79997c",
                "description": "申请成功",
                "status": "00"
            }
        }
        self.update(api, body)

    def update_signconfirm(self):
        '''
        代扣签约确认
        :return:
        '''
        api = '/shanxixintuo/signApplyConfirm'
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "signReqNo": "ac98171933e64049ab19a1714d79997c",
                "description": "申请成功",
                "agreementNo": "1213",
                "expectPayCompanyId": "1231",
                "status": "00"
            }
        }
        self.update(api, body)

    def update_creditapply(self, asset_info, status="00", message ="成功"):
        '''
        授信申请
        :return:
        '''
        item_no = asset_info['data']['asset']['item_no']
        api = "/shanxixintuo/creditApply"
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "creditReqNo": "credit_"+str(item_no),
                "description": message,
                "userId": "@id",
                "status": str(status)
            }
        }
        self.update(api, body)

    def update_creditquery(self, asset_info, status="00", message="成功"):
        '''
        授信申请查询
        :return:
        '''

        amount = asset_info['data']['asset']['amount']
        api = "/shanxixintuo/creditQuery"
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "creditExpireDate": "2023-02-11",
                "decision": "A",
                "description":message ,
                "creditAmount": amount,
                "userId": "@id",
                "status": status
            }
        }
        self.update(api, body)

    def update_creditquery_noorder(self):
        api = "/shanxixintuo/creditQuery"
        body = {
                "code": 0,
                "message": "调用成功",
                "data": {
                    "returnCode": "00400",
                    "decision": "R",
                    "description": "流水不存在",
                    "status": "05"
                }
            }
        self.update(api, body)

    def update_loanprecheck(self, asset_info, status="00", message="接收成功"):
        '''
        放款预审
        :return:
        '''
        item_no = asset_info['data']['asset']['item_no']
        loan_no = get_guid()
        api = "/shanxixintuo/loanPreCheck"
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "biddingNo": 8502,
                "loanPactNo": loan_no,
                "contractUrl": "sftp://124.160.116.245:2221/download/information/901042022021180100000001611097/02_001.pdf",
                "contractId": "sxxt-"+str(loan_no)+"-B",
                "description": message,
                "loanReqNo": "apply_"+str(item_no),
                "status": str(status)
            }
        }
        self.update(api, body)

    def update_precheckquery(self, item_no, status="00", message="预审成功"):
        '''
        预审查询
        :return:
        '''
        bill_no = self.get_due_bill_no(item_no)
        api = "/shanxixintuo/preCheckQuery"
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "returnCode": "",
                "loanPactNo": bill_no,
                "contractUrl": "sftp://124.160.116.245:2221/download/information/901042022021180100000001611097/02_001.pdf",
                "description": message,
                "loanReqNo": "apply_"+str(item_no),
                "status": str(status)
            }
        }
        self.update(api, body)

    def update_upload_zip(self, item_no):
        api = '/contract/upload-zip'
        body = {
            "code": 0,
            "message": "成功",
            "data": [
                {
                    "assetItemNo": item_no,
                    "contractCode": None,
                    "url": "http://rg-biz-contract-test-1251122539.cossh.myqcloud.com/202202/14/item_no_1644832850/31501/02_001.pdf.zip",
                    "type": 31501,
                    "typeText": "山西信托-借款协议（待签署版）"
                }
            ]
        }
        self.update(api, body)

    def update_loancontractsign(self, item_no, status="00", message="成功"):
        '''
        合同签约申请
        :return:
        00=成功
        01=失败
        03=已签署
        05=流水不存在
        06=调用太频繁
        99=处理中
        '''
        bill_no = self.get_due_bill_no(item_no)
        api = "/shanxixintuo/loanContractSign"
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "contractId": "sxxt-"+str(bill_no)+"-B",
                "description": message,
                "status": str(status)
            }
        }
        self.update(api, body)

    def update_contractsignconfirm(self, item_no, status="00", message="成功"):
        '''
        合同签约确认
        :return:
        '''
        bill_no = self.get_due_bill_no(item_no)
        api = "/shanxixintuo/contractSignConfirm"
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "contractId": "sxxt-"+str(bill_no)+"-B",
                "description": message,
                "status": str(status)
            }
        }
        self.update(api, body)

    def update_loanconfirm(self, item_no, status="00", message=""):
        '''
        放款确认申请
        :return:
        '''
        bill_no = self.get_due_bill_no(item_no)
        api = "/shanxixintuo/loanConfirm"
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "loanPactNo": bill_no,
                "description": message,
                "status": str(status)
            }
        }
        self.update(api, body)

    def update_loanconfirmquery(self, item_no, status="00", message="放款成功"):
        '''
        放款确认查询
        :return:
        00=放款成功
        01=放款失败
        05=流水不存在
        99=处理中
        '''
        loan_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        bill_no = self.get_due_bill_no(item_no)
        api = '/shanxixintuo/loanConfirmQuery'
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "loanPactNo": bill_no,
                "contractUrl": "sftp://124.160.116.245:2221/download/information/901042022021180100000002404918/02_001_final.pdf",
                "payOrderNo": str(item_no),
                "payTime": loan_date,
                "description": message,
                "status": str(status)
            }
        }
        self.update(api, body)

    def update_queryplan(self, asset_info):
        '''
        还款计划查询
        :return:
        '''
        api = '/shanxixintuo/repayPlanQuery'
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        period_count = asset_info['data']['asset']['period_count']
        body = {
            "code": 0,
            "message": "调用成功",
            "data": {
                "loanPlan": []
            }
        }
        loanPlan = {
            "rpyTerm": 1,
            "shouldDate": "2022-08-11",
            "payPrinAmt": 525.07,
            "payIntAmt": 10.5,
            "payFeeAmt": 0
        }
        for i in range(period_count):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(loanPlan)
            repayment_plan['rpyTerm'] = i + 1
            repayment_plan['payPrinAmt'] = float(fee_info['principal'])/100
            repayment_plan['payIntAmt'] = float(fee_info['interest'])/100
            repayment_plan['shouldDate'] = fee_info['date']
            body['data']['loanPlan'].append(repayment_plan)


        self.update(api, body)

    def update_upload_success(self):
        '''
        文件上传成功
        :return:
        '''
        api = "/capital/ftp/upload/shanxixintuo"
        body = {
                "code": 0,
                "message": "",
                "data": {
                    "dir": "/upload/information/credit_item_no_1644543552/",
                    "name": "01_002.jpg",
                    "type": "mock身份证正反面上传",
                    "result": {
                        "code": 0,
                        "message": "成功"
                    }
                }
            }
        self.update(api, body)