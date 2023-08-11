# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class MozhiBeiyinMock(Easymock):

    def update_access_success(self):
        api = "/mozhibeiyin/user.access"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "access": true,
                    "failReason": "成功"
                  }
                }'''
        self.update(api, mode)


    def update_access_fail(self):
        api = "/mozhibeiyin/user.access"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "access": false,
                    "failReason": "用户暂时不满足申请条件"
                  }
                }'''
        self.update(api, mode)


    def update_accountquery_nodata(self):
        api = "/mozhibeiyin/bind.bankcard.list"
        mode = '''{
                    "code": 0,
                    "message": "成功",
                    "data": [ ]
                }
                '''
        self.update(api, mode)

    def update_accountquery_success_only_baofu(self, asset_info):
        api = "/mozhibeiyin/bind.bankcard.list"
        mode = ''' {
                  "code": 0,
                  "message": "开户查询msg",
                  "data": [{
                    "bankCardId": "@id", //若有会存到user_key，没有也没有关系，user_key为空
                    "authorizeChannel": "BAOFU_KUAINIU",
                    "bankCardNo": "123456789",//不校验该参数，随便写一个
                    "bankCardNoEncrypt": "%s", //强校验该参数
                    "bankName": "工商银行",
                    "bankCode": "ICBC",
                    "abbreviation": "ICBC",
                    "cardType": "1",
                    "bankBin": "552245",
                    "daysLimit": "1000000",
                    "singleLimit": "1000000"
                  }]
                }
                   ''' % (asset_info['data']['repay_card']['account_num_encrypt'])
        self.update(api, mode)

    def update_accountquery_success(self, asset_info):
        api = "/mozhibeiyin/bind.bankcard.list"
        mode = ''' {
                        "code": 0,
                        "message": "成功",
                        "data": [
                            {
                                "bankCardId": "@id",
                                "authorizeChannel": "BEIYIN",
                                "bankCardNo": "123456789",//不校验该参数，随便写一个
                                "bankCardNoEncrypt": "%s",
                                "bankName": "工商银行",
                                "bankCode": "ICBC",
                                "abbreviation": "ICBC",
                                "cardType": "1",
                                "bankBin": "621226",
                                "daysLimit": "1000000",
                                "singleLimit": "1000000"
                            },
                            {
                                "bankCardId": "@id",
                                "authorizeChannel": "BAOFU_KUAINIU",
                                "bankCardNo": "123456789",//不校验该参数，随便写一个
                                "bankCardNoEncrypt": "%s",
                                "bankName": "工商银行",
                                "bankCode": "ICBC",
                                "abbreviation": "ICBC",
                                "cardType": "1",
                                "bankBin": "621226",
                                "daysLimit": "1000000",
                                "singleLimit": "1000000"
                            }
                        ]
                    }
                   ''' % (asset_info['data']['receive_card']['num_encrypt'], asset_info['data']['receive_card']['num_encrypt'])
        self.update(api, mode)

    def update_get_sms_code_success(self):
        api = "/mozhibeiyin/bind.bankcard"
        mode = '''{
                  "code": 0,
                  "message": "外层测试msg",
                  "data": {
                    "code": 0,
                    "msg": "内层msg,mock测试",
                    "bankCode": "ICBC",
                    "bankBin": "621226",
                    "singleLimit": 1000000,
                    "cardType": "1",
                    "daysLimit": 1000000,
                    "bankName": "中国工商银行",
                    "abbreviation": "ICBC",
                    "bankCardId": "@id" //
                  }
                }'''
        self.update(api, mode)

    def update_verify_sms_success(self):
        api = "/mozhibeiyin/bind.sms.verify"
        mode = '''{
                  "code": 0,//0成功，其他失败
                  "message": "外层msg,验证短信验证码",
                  "data": {
                    "msg": "内层msg",
                    "code": 0//0成功，其他失败
                  }
                }
                '''
        self.update(api, mode)


    def update_user_credit_info_noactive(self):
        api = "/mozhibeiyin/user.credit.info"
        mode = '''{
                    "code": 0,
                    "message": "成功",
                    "data": {
                        "status": "NOTACTIVE"
                    }
                }
                '''
        self.update(api, mode)

    def update_user_credit_info_active(self):
        api = "/mozhibeiyin/user.credit.info"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "limitExpireDate": "20990101",
                    "remainLimit": 2000000, //判断这个字段必须大于等于本金
                    "identity": null,
                    "limitUseErrStatus": null,
                    "creditLimit": 2000000,
                    "limitType": "CIRCLE",
                    "limitUseErrDesc": null,
                    "repayDay": "",
                    "productInfo": {
                      "overdueDayRate": "0.10",
                      "repayMethod": "FIXED_INSTALLMENT",
                      "dayRate": "0.10",
                      "earlyRepay": "Y",
                      "termNum": "3;6;9;12"
                    },
                    "status": "ACTIVE" //ACTIVE/EXPIRED/NOTACTIVE-----成功， APPLYING /AUDITING:----重试 ；REFUSE/FREEZE-----失败切资金方(需要配置进去才可以)
                  }
                }
                '''
        self.update(api, mode)


    def update_user_credit_info_no_amount(self):
        api = "/mozhibeiyin/user.credit.info"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "limitExpireDate": "20990101",
                    "remainLimit": 0, //判断这个字段必须大于等于本金
                    "identity": null,
                    "limitUseErrStatus": null,
                    "creditLimit": 2000000,
                    "limitType": "CIRCLE",
                    "limitUseErrDesc": null,
                    "repayDay": "",
                    "productInfo": {
                      "overdueDayRate": "0.10",
                      "repayMethod": "FIXED_INSTALLMENT",
                      "dayRate": "0.10",
                      "earlyRepay": "Y",
                      "termNum": "3;6;9;12"
                    },
                    "status": "ACTIVE" //ACTIVE/EXPIRED/NOTACTIVE-----成功， APPLYING /AUDITING:----重试 ；REFUSE/FREEZE-----失败切资金方(需要配置进去才可以)
                  }
                }
                '''
        self.update(api, mode)

    def update_user_credit_info_auditing(self):
        api = "/mozhibeiyin/user.credit.info"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "limitExpireDate": "20990101",
                    "remainLimit": 2000000, //判断这个字段必须大于等于本金
                    "identity": null,
                    "limitUseErrStatus": null,
                    "creditLimit": 2000000,
                    "limitType": "CIRCLE",
                    "limitUseErrDesc": null,
                    "repayDay": "",
                    "productInfo": {
                      "overdueDayRate": "0.10",
                      "repayMethod": "FIXED_INSTALLMENT",
                      "dayRate": "0.10",
                      "earlyRepay": "Y",
                      "termNum": "3;6;9;12"
                    },
                    "status": "AUDITING" //ACTIVE/EXPIRED/NOTACTIVE-----成功， APPLYING /AUDITING:----重试 ；REFUSE/FREEZE-----失败切资金方(需要配置进去才可以)
                  }
                }
                '''
        self.update(api, mode)

    def update_user_credit_info_refuse(self):
        api = "/mozhibeiyin/user.credit.info"
        mode = '''{
                   "code": 0,
                   "message": "成功",
                   "data": {
                     "limitExpireDate": "20990101",
                     "remainLimit": 2000000, //判断这个字段必须大于等于本金
                     "identity": null,
                     "limitUseErrStatus": null,
                     "creditLimit": 2000000,
                     "limitType": "CIRCLE",
                     "limitUseErrDesc": null,
                     "repayDay": "",
                     "productInfo": {
                       "overdueDayRate": "0.10",
                       "repayMethod": "FIXED_INSTALLMENT",
                       "dayRate": "0.10",
                       "earlyRepay": "Y",
                       "termNum": "3;6;9;12"
                     },
                     "status": "REFUSE" //ACTIVE/EXPIRED/NOTACTIVE-----成功， APPLYING /AUDITING:----重试 ；REFUSE/FREEZE-----失败切资金方(需要配置进去才可以)
                   }
                 }
                 '''
        self.update(api, mode)


    def update_user_credit_apply(self):
        api = "/mozhibeiyin/limit.apply"
        mode = '''{
                  "code": 0, //0-成功，  其他重试
                  "message": "测试进件",
                  "data": {
                    "outOrderNo": 123 ///无用参数，一般是null
                  }
                }
                '''
        self.update(api, mode)


    def update_user_credit_apply_result_success(self):
        api = "/mozhibeiyin/credit.apply.result"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "limitExpireDate": "20990101",
                    "refuseControlDays": 0,
                    "authorize_server": "KUAINIU_BEIYIN",
                    "remainLimit": "2000000",
                    "applyResult": "PASS", //PASS 通过；REFUSE 拒绝; AUDITING授信中
                    "refuseInfo": null,
                    "creditLimit": "2000000",
                    "limitType": "CIRCLE",
                    "outOrderNo": "TMZ-1017725"
                  }
                }'''
        self.update(api, mode)



    def update_user_credit_apply_result_fail(self):
        api = "/mozhibeiyin/credit.apply.result"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "limitExpireDate": "20990101",
                    "refuseControlDays": 0,
                    "authorize_server": "KUAINIU_BEIYIN",
                    "remainLimit": "2000000",
                    "applyResult": "REFUSE", //PASS 通过；REFUSE 拒绝; AUDITING授信中
                    "refuseInfo": null,
                    "creditLimit": "2000000",
                    "limitType": "CIRCLE",
                    "outOrderNo": "TMZ-1017725"
                  }
                }'''
        self.update(api, mode)

    def update_user_credit_apply_result_no_record(self):
        api = "/mozhibeiyin/credit.apply.result"
        mode = '''{
                    "code": 11002,
                    "message": "没有查询到记录"
                }'''
        self.update(api, mode)

    def update_user_loan_apply_success(self):
        api = "/mozhibeiyin/loan.apply"
        mode = '''{
                      "code": 0, //0-成功，其他重试
                      "message": "成功",
                      "data": {
                        "outOrderNo": "TMZ-1017726"  
                      }
                    }
                    '''
        self.update(api, mode)

    def update_user_loan_result_success(self, asset_info):
        api = "/mozhibeiyin/loan.result"
        effectiveDate = get_date(fmt="%Y%m%d")
        mode = '''{
                  "code": 0,
                  "message": "测试放款查询接口",
                  "data": {
                    "refuseCode": null,
                    "loanTime": %s, //起息/到卡/到虚户时间
                    "repayMethod": "FIXED_INSTALLMENT",
                    "applyResult": "测试哈哈哈哈哈哈哈哈哈11", //记录到alr_memo
                    "dayRate": "0.099",
                    "refuseMsg": null,
                    "outOrderNo": "cs_@id",
                    "applyStatus": "SUCCESS", //成功：code=0+applyStatus =SUCCESS；失败：code=0+applyStatus =FAIL: 失败  /REFUSE: 拒绝 
                    "loanAmount": %s,
                    "effectiveDate": "%s" //需要与loanTime保持同一天
                  }
                }''' % (int(str(time.time()).split('.')[0]), asset_info['data']['asset']['amount']*100, effectiveDate)
        self.update(api, mode)

    def update_user_loan_result_fail(self, asset_info):
        api = "/mozhibeiyin/loan.result"
        mode = '''{
                     "code": 0,
                     "message": "测试放款查询接口",
                     "data": {
                        "applyResult": "借款失败",
                        "outOrderNo": "cs_@id",
                        "applyStatus": "REFUSE", //成功：code=0+applyStatus =SUCCESS；失败：code=0+applyStatus =FAIL: 失败  /REFUSE: 拒绝 
                        "loanAmount": %s
                     }
                   }''' % (asset_info['data']['asset']['amount']*100)
        self.update(api, mode)

    def update_repayPlanquery_success(self, asset_info):
        api = "/mozhibeiyin/loan.record.detail"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        today = get_date(fmt="%Y%m%d")
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        duebillno = alr_info[0]['asset_loan_record_due_bill_no']
        bindcardnoencrypt = asset_info['data']['receive_card']['num_encrypt']
        termnum = asset_info['data']['asset']['period_count']
        loanamount = asset_info['data']['asset']['amount']*100
        mode = {
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "effectiveDate": today,
                    "applyDate": today,
                    "loanAmount": loanamount,
                    "status": "PAYING",
                    "termNum": termnum,
                    "repayMethod": "FIXED_INSTALLMENT",
                    "outOrderNo": duebillno,
                    "contractList": [],
                    "clearTime": 0,
                    "paidAmount": 0,
                    "paidPrinAmount": 0,
                    "paidInterAmount": 0,
                    "paidFeeAmount": 0,
                    "paidPenalty": 0,
                    "paidInsuranceAmount": None,
                    "bindCardNo": "12343456789",
                    "bindCardNoEncrypt": bindcardnoencrypt,
                    "bindBankCode": "CCB",
                    "bindBankName": "中国建设银行",
                    "couponNo": None,
                    "couponType": None,
                    "dayRate": "0.099",
                    "reductionAmount": 0,
                    "prePenalty": 0,
                    "repayPlanItems": [],
                    "extendRepayPlanItems": []}}
        repayment_plan_tmp = {
                        "termNo": 1,
                        "shouldRepayDate": "20210527",
                        "termStatus": "PAYING",
                        "repayCategory": 1,
                        "termAmount": 73766,
                        "termPrincipal": 61886,
                        "termInterest": 11880,
                        "termPrinPenalty": 0,
                        "termInterPenalty": 0,
                        "termInsuranceAmount": 0,
                        "paidTermInsuranceAmount": 0,
                        "termFee": 0,
                        "paidTime": 0,
                        "paidTermAmount": 0,
                        "paidTermPrincipal": 0,
                        "paidTermInterest": 0,
                        "paidTermPrinPenalty": 0,
                        "paidTermInterPenalty": 0,
                        "paidTermFee": 0,
                        "overdueDays": 0,
                        "overdueAmt": 0,
                        "preRepay": "N",
                        "overdue": "N"
                      }
        repayment_plan_tmp2 = {
                        "termNo": 6,
                        "shouldRepayDate": "20211026",
                        "termAmount": 68925,
                        "termPrincipal": 68327,
                        "termInterest": 598,
                        "termFee": 0,
                        "termGuarantee": 0
                      }
        for i in range(asset_info['data']['asset']['period_count']):
                fee_info = get_fee_info_by_period(rate_info, i + 1)
                repayment_plan = deepcopy(repayment_plan_tmp)
                repayment_plan['termNo'] = i + 1
                repayment_plan['termPrincipal'] = float(fee_info['principal'])
                repayment_plan['termInterest'] = float(fee_info['interest']) + float(fee_info['consult']) + float(fee_info['guarantee']) + float(fee_info['after_loan_manage'])
                repayment_plan['termAmount'] = repayment_plan['termPrincipal'] + repayment_plan['termInterest']
                repayment_plan['shouldRepayDate'] = fee_info['date'].replace("-", "")
                mode['data']['repayPlanItems'].append(repayment_plan)

        for i in range(asset_info['data']['asset']['period_count']):
                fee_info = get_fee_info_by_period(rate_info, i + 1)
                repayment_plan2 = deepcopy(repayment_plan_tmp2)
                repayment_plan2['termNo'] = i + 1
                repayment_plan2['termPrincipal'] = float(fee_info['principal'])
                repayment_plan2['termInterest'] = float(fee_info['interest'])
                repayment_plan2['termAmount'] = float(fee_info['principal']) + float(fee_info['interest'])
                repayment_plan2['shouldRepayDate'] = fee_info['date'].replace("-", "")
                mode['data']['extendRepayPlanItems'].append(repayment_plan2)
        self.update(api, mode)

    def update_repayPlanquery_success_tianbang(self, asset_info):
        api = "/mozhibeiyin/loan.record.detail"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        today = get_date(fmt="%Y%m%d")
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        duebillno = alr_info[0]['asset_loan_record_due_bill_no']
        bindcardnoencrypt = asset_info['data']['receive_card']['num_encrypt']
        termnum = asset_info['data']['asset']['period_count']
        loanamount = asset_info['data']['asset']['amount']*100
        mode = {
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "effectiveDate": today,
                    "applyDate": today,
                    "loanAmount": loanamount,
                    "status": "PAYING",
                    "termNum": termnum,
                    "repayMethod": "FIXED_INSTALLMENT",
                    "outOrderNo": duebillno,
                    "contractList": [],
                    "clearTime": 0,
                    "paidAmount": 0,
                    "paidPrinAmount": 0,
                    "paidInterAmount": 0,
                    "paidFeeAmount": 0,
                    "paidPenalty": 0,
                    "paidInsuranceAmount": None,
                    "bindCardNo": "12343456789",
                    "bindCardNoEncrypt": bindcardnoencrypt,
                    "bindBankCode": "CCB",
                    "bindBankName": "中国建设银行",
                    "couponNo": None,
                    "couponType": None,
                    "dayRate": "0.099",
                    "reductionAmount": 0,
                    "prePenalty": 0,
                    "repayPlanItems": [],
                    "extendRepayPlanItems": []}}
        repayment_plan_tmp = {
                        "termNo": 1,
                        "shouldRepayDate": "20210527",
                        "termStatus": "PAYING",
                        "repayCategory": 1,
                        "termAmount": 73766,
                        "termPrincipal": 61886,
                        "termInterest": 11880,
                        "termPrinPenalty": 0,
                        "termInterPenalty": 0,
                        "termInsuranceAmount": 0,
                        "paidTermInsuranceAmount": 0,
                        "termFee": 0,
                        "paidTime": 0,
                        "paidTermAmount": 0,
                        "paidTermPrincipal": 0,
                        "paidTermInterest": 0,
                        "paidTermPrinPenalty": 0,
                        "paidTermInterPenalty": 0,
                        "paidTermFee": 0,
                        "overdueDays": 0,
                        "overdueAmt": 0,
                        "preRepay": "N",
                        "overdue": "N"
                      }
        repayment_plan_tmp2 = {
                        "termNo": 6,
                        "shouldRepayDate": "20211026",
                        "termAmount": 68925,
                        "termPrincipal": 68327,
                        "termInterest": 598,
                        "termFee": 0,
                        "termGuarantee": 0
                      }
        for i in range(asset_info['data']['asset']['period_count']):
                fee_info = get_fee_info_by_period(rate_info, i + 1)
                repayment_plan = deepcopy(repayment_plan_tmp)
                repayment_plan['termNo'] = i + 1
                repayment_plan['termPrincipal'] = float(fee_info['principal'])
                repayment_plan['termInterest'] = float(fee_info['interest']) + float(fee_info['consult']) + float(fee_info['reserve'])
                repayment_plan['termAmount'] = repayment_plan['termPrincipal'] + repayment_plan['termInterest']
                repayment_plan['shouldRepayDate'] = fee_info['date'].replace("-", "")
                mode['data']['repayPlanItems'].append(repayment_plan)

        for i in range(asset_info['data']['asset']['period_count']):
                fee_info = get_fee_info_by_period(rate_info, i + 1)
                repayment_plan2 = deepcopy(repayment_plan_tmp2)
                repayment_plan2['termNo'] = i + 1
                repayment_plan2['termPrincipal'] = float(fee_info['principal'])
                repayment_plan2['termInterest'] = float(fee_info['interest'])
                repayment_plan2['termAmount'] = float(fee_info['principal']) + float(fee_info['interest'])
                repayment_plan2['shouldRepayDate'] = fee_info['date'].replace("-", "")
                mode['data']['extendRepayPlanItems'].append(repayment_plan2)
        self.update(api, mode)

    def update_contractpush_ftp_success(self):
        api = "/capital/ftp/upload/mozhi_beiyin"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "dir": "/agreement/20210531/",
                    "name": "MZ-3547180_guarantee_agreement.pdf",
                    "type": "墨智北银-中裔-委托担保协议",
                    "result": {
                      "code": 0,
                      "message": "成功"
                    }
                  }
                }'''
        self.update(api, mode)


if __name__ == "__main__":
    pass
