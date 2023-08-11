# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no, get_asset_info_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *
from biztest.function.gbiz.gbiz_check_function import get_asset_event


class YiXinHengRunMock(Easymock):

    def update_user_access_success(self):
        api = "/yixin/yixin_hengrun/user.access"
        mode = {
                "code": "0",
                "message": "成功",
                "data": {
                    "access": True,
                    "failReason": None
                }
            }
        self.update(api, mode)

    def update_query_bankcard_new_user(self):
        api = "/yixin/yixin_hengrun/bind.bankcard.list"
        mode = {
                  "code": "0",
                  "message": "成功",
                  "data": []
                }

        self.update(api, mode)


    def update_query_bankcard_success(self, four_element):
        '''
        bankCardId,实际是随机数，此处为了方便自动化测试，使用了用户手机号
        避免了后续开户绑卡接口等需要重新去数据库查询该字段值
        '''
        api = "/yixin/yixin_hengrun/bind.bankcard.list"
        mode = {
                "code": "0",
                "message": "成功",
                "data": [
                    {
                        "bankCardId": four_element['data']['phone_number'],
                        "bankCardNo": four_element['data']['bank_code'],
                        "bankName": "建设银行",
                        "bankCode": "CCB",
                        "abbreviation": "CCB",
                        "cardType": "1",
                        "bankBin": "552245",
                        "daysLimit": "5000000",
                        "singleLimit": "5000000",
                        "status": "NORMAL"
                    }
                ]
            }

    def update_account_get_msg_code_success(self, four_element):
        api = "/yixin/yixin_hengrun/bind.bankcard"
        mode = {
              "code": "0",
              "message": "成功",
              "data": {
                "code": 0,
                "msg": "成功",
                "bankCardId": four_element['data']['phone_number'],
                "bankName": "建设银行",
                "bankCode": "CCB",
                "abbreviation": "CCB",
                "cardType": "1",
                "bankBin": "552245",
                "daysLimit": "5000000",
                "singleLimit": "5000000"
              }
            }
        self.update(api, mode)

    def update_account_bind_verify(self, four_element):
        api = "/yixin/yixin_hengrun/bind.sms.verify"
        mode = {
                  "code": "0",
                  "message": "成功",
                  "data": {
                    "code": 0,
                    "msg": "成功",
                    "bankCardId": four_element['data']['phone_number']
                  }
                }
        self.update(api, mode)


    def update_loanapplynew_success(self):
        '''
        applyStatus：1成功 -1失败
        '''
        api = "/yixin/yixin_hengrun/loan.apply"
        mode = {
                  "code": "0",
                  "message": "成功",
                  "data": {
                    "applyStatus": 1,
                    "failReason": None
                  }
                }
        self.update(api, mode)


    def update_loanapplynew_fail(self):
        '''
        applyStatus：1成功 -1失败
        '''
        api = "/yixin/yixin_hengrun/loan.apply"
        mode = {
                  "code": "0",
                  "message": "mock失败",
                  "data": {
                    "applyStatus": -1,
                    "failReason": "mock的"
                  }
                }
        self.update(api, mode)

    def update_loanapplyquery_success(self):
        '''
        applyStatus
        CANCELED：进件取消
        APPLYING：申请中
        REFUSE：拒绝
        SIGN_SUCCESS：签约成功  #代表可以进入放款了
        LENDING：放款中
        LEND_FAILED: 放款失败
        LENT：已放款
        '''
        api = "/yixin/yixin_hengrun/loan.result"
        mode = {
                  "code": "0",
                  "message": "成功",
                  "data": {
                    "applyStatus": "SIGN_SUCCESS",
                    "loanTime": None,
                    "msg": None
                  }
                }
        self.update(api, mode)

    def update_loanapplyquery_fail(self):
        api = "/yixin/yixin_hengrun/loan.result"
        mode = {
                  "code": "0",
                  "message": "mock失败",
                  "data": {
                    "applyStatus": "REFUSE",
                    "loanTime": None,
                    "msg": None
                  }
                }
        self.update(api, mode)


    def update_loanapplyconfirm_success(self):
        '''
        status：0：成功，1：失败
        '''
        api = "/yixin/yixin_hengrun/loan.instruction"
        mode = {
                  "code": "0",
                  "message": "成功",
                  "data": {
                    "status": 0,
                    "failReason": "已放款,不能发送放款通知"
                  }
                }
        self.update(api, mode)

    def update_loanapplyconfirm_fail(self):
        '''
        status：0：成功，1：失败
        '''
        api = "/yixin/yixin_hengrun/loan.instruction"
        mode = {
                  "code": "0",
                  "message": "mock 失败",
                  "data": {
                    "status": 1,
                    "failReason": "mock 失败"
                  }
                }
        self.update(api, mode)


    def update_loanconfirmquery_success(self):
        '''
        applyStatus
        CANCELED：进件取消
        APPLYING：申请中
        REFUSE：拒绝
        SIGN_SUCCESS：签约成功  #代表可以进入放款了
        LENDING：放款中
        LEND_FAILED: 放款失败
        LENT：已放款
        '''

        api = "/yixin/yixin_hengrun/loan.result"
        loantime = get_date_timestamp()
        mode = {
                "code": "0",
                "message": "成功",
                "data": {
                    "applyStatus": "LENT",
                    "loanTime": loantime,
                    "msg": None
                }
            }
        self.update(api, mode)

    def update_loanconfirmquery_fail(self):
        api = "/yixin/yixin_hengrun/loan.result"
        loantime = get_date_timestamp()
        mode = {
                "code": "0",
                "message": "mock失败",
                "data": {
                    "applyStatus": "LEND_FAILED",
                    "loanTime": loantime,
                    "msg": "放款失败"
                }
            }
        self.update(api, mode)

    def update_repayplan_success(self, item_no, asset_info):
        api = "/yixin/yixin_hengrun/repay.repaymentPlan"
        asset_data = get_asset_info_by_item_no(item_no)
        asset_info['data']['asset']['amount'] = asset_data[0]['asset_principal_amount']/100
        asset_info['data']['asset']['cmdb_product_number'] = asset_data[0]['asset_cmdb_product_number']
        asset_info['data']['asset']['period_count'] = asset_data[0]['asset_period_count']
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        loanterm = asset_info['data']['asset_extend']['sub_asset']['period_count']
        contbegindate=get_date(month=1, fmt="%Y-%m-%d")
        contenddate = get_date(month=6, fmt="%Y-%m-%d")
        loan_amount = asset_info['data']['asset_extend']['sub_asset']['amount']*100
        mode = {
                  "code": "0",
                  "message": "成功",
                  "data": {
                    "contractAmt": "800000",
                    "loanTerm": loanterm,
                    "contBeginDate": contbegindate,
                    "contEndDate": contenddate,
                    "repayDay": contbegindate,
                    "repayTerm": "0",
                    "extDelayBeginDate": "",
                    "totalDelayCnt": "0",
                    "extDelayTerm": "0",
                    "extDelayDays": "0",
                    "calDefIntEndDate": "",
                    "prestoreAmt": "0",
                    "feePrestoreAmt": "0",
                    "unPaidPreFee": "0",
                    "unPaidPenalty": "0",
                    "totalUnPaidAmt": loan_amount,
                    "totalUnPaidInt": "30605",
                    "totalUnPaidFee": "0",
                    "totalUnpaidFeeList": [],
                    "totalUnPaidDefInt": "0",
                    "totalUnPaidLatAmt": "0",
                    "loanBalance": loan_amount,
                    "recycleFlag": "0",
                    "rpyPlanChgFlag": "00000001",
                    "conDpsFlag": "0",
                    "clearFlag": "",
                    "repayPlanItems": [],
                    "preFeeInfoList": [],
                    "totalUnpaidFeeAmt": "0"
                  }
                }
        repayment_plan_tmp = {
                        "subSection": "1",
                        "repayTerm": "1",
                        "acctFlag": "0",
                        "delayFlag": "1",
                        "repayBeginDate": "2022-08-08",
                        "repayEndDate": "2022-08-08",
                        "repayDate": None,
                        "lnsCurAmt": "129768",
                        "lnsCurInt": "8666",
                        "lnsCurFee": "0",
                        "lnsDefInt": "0",
                        "lnsLatAmt": "0",
                        "lnsFeeAmt": "0",
                        "lnsOthAmt": "0",
                        "lnsRecPrin": "0",
                        "lnsRecInt": "0",
                        "lnsRecFee": "0",
                        "lnsRecDefInt": "0",
                        "lnsRecLatAmt": "0",
                        "lnsRecFeeAmt": "0",
                        "lnsRecOthAmt": "0",
                        "lnsDeartePrin": "0",
                        "lnsDearteInt": "0",
                        "lnsDearteFee": "0",
                        "lnsDearteDefInt": "0",
                        "lnsDearteLatAmt": "0",
                        "lnsDearteFeeAmt": "0",
                        "lnsDearteOthAmt": "0",
                        "unPaidAmt": "129768",
                        "unPaidInt": "8666",
                        "unPaidFee": "0",
                        "unPaidDefInt": "0",
                        "unPaidLatAmt": "0",
                        "unPaidFeeAmt": "0",
                        "unPaidLatOthAmt": "0",
                        "totalUnPaidAmt": "138434",
                        "prepayamt": "808666",
                        "overduePeriods": "0",
                        "overdueDays": "0",
                        "preIsRePay": None,
                        "lnsFeeInfoList": []
                      }
        for i in range(asset_info['data']['asset_extend']['sub_asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['repayTerm'] = i + 1
            repayment_plan['repayBeginDate'] = fee_info['date']
            # 代码里只校验了repayBeginDate ，未校验repayEndDate
            repayment_plan['repayEndDate'] = fee_info['date']
            repayment_plan['lnsCurAmt'] = float(fee_info['principal'])
            repayment_plan['lnsCurInt'] = float(fee_info['interest'])
            # 该字段在代码中实际未校验
            repayment_plan['totalUnPaidAmt'] = float(fee_info['principal']) + float(fee_info['principal'])
            mode['data']['repayPlanItems'].append(repayment_plan)
        self.update(api, mode)


    def update_contractdown_success(self):
        api = "/yixin/yixin_hengrun/loan.queryLoanContract"
        mode = '''{
                  "code": "0",
                  "message": "成功",
                  "data": {
                    "contractName": "刘秀华-合同",
                    "contractNo": "497094425206326551",
                    "contractZipBase64": "ZipBase64url……" //太长了，不好mock
                  }
                }'''
        self.update(api, mode)

    def update_contractpush_success(self):
        api = "/yixin/yixin_hengrun/loan.syncAgreement"
        mode ='''{
                  "code": "0",
                  "message": "成功",
                  "data": {
                    "contractNo": "@id",
                    "status": true,
                    "failReason": null
                
                  }
                }'''
        self.update(api, mode)


if __name__ == "__main__":
    pass
