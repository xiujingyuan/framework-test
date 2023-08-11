# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *
from biztest.function.gbiz.gbiz_check_function import get_asset_event


class JiexinTaikangMock(Easymock):
    def update_newuser_openaccount(self):
        '''
        用户开户查询接口（新用户首次开户）
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpAuthResult"
        mode = {
                  "code": "0",
                  "message": "success",
                  "data": []
                }
        self.update(api, mode)

    def update_openaccount_success(self, four_element):
        '''
        用户开户查询接口（老用户开户完成之后）
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpAuthResult"
        mode = {
                "code": "0",
                "message": "success",
                "data": [
                    {
                        "customerBankAccount": four_element['data']['bank_code'],
                        "customerIdCardNumber": four_element['data']['id_number'],
                        "customerName": four_element['data']['user_name'],
                        "customerPhoneNumber": four_element['data']['phone_number'],
                        "agreementId": "@id",
                        "resultExtendInfo": None,
                        "validTo": None
                    }
                ]
            }
        self.update(api, mode)


    def update_newuser_query_insurestatus(self):
        '''
        预审结果查询（投保结果查询）接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpAwardCreditStatus"
        mode = '''{
              "code": "0",
              "message": "success",
              "data": {
                "cappTraceId": "a9168f3490284ea6be1119b44cd8b78e",
                "status": 200,
                "code": 200,
                "value": {
                  "sessionId": function({
                      _req
                    }) {
                      return _req.body.data.sessionId
                    },
                  "status": "NO_AWARD",
                  "contractNo": null,
                  "loanAmount": null,
                  "installmentAmount": null,
                  "term": null,
                  "interestRate": null,
                  "floatRate": null,
                  "dueDay": null,
                  "firstDueDay": null
                }
              }
            }'''
        self.update(api, mode)

    def update_query_insurestatus_process(self):
        '''
        预审结果查询（投保结果查询）接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpAwardCreditStatus"
        mode = '''{
            "code": "0",
            "message": "success",
            "data": {
                "cappTraceId": "a9168f3490284ea6be1119b44cd8b78e",
                "status": 200,
                "code": 200,
                "value": {
                    "sessionId": function({
                      _req
                    }) {
                      return _req.body.data.sessionId
                    },
                    "status": "IN_PROGRESS",
                    "contractNo": null,
                    "loanAmount": null,
                    "installmentAmount": null,
                    "term": null,
                    "interestRate": null,
                    "floatRate": null,
                    "dueDay": null,
                    "firstDueDay": null
                }
            }
        }'''
        self.update(api, mode)

    def update_query_insurestatus_success(self, four_element):
        '''
        预审结果查询（投保结果查询）接口
        :return:
        '''
        number = four_element['data']['phone_number']  # 此为避免写入事件表中的值变更，此接口重复调用会更新事件表中写入的值
        api = "/jiexin/jiexin_taikang/api/checkBpAwardCreditStatus"
        mode = '''{
                "code": "0",
                "message": "success",
                "data": {
                    "cappTraceId": "1bbceb1c9be349be9a7d8ca976910000",
                    "status": 200,
                    "code": 200,
                    "value": {
                        "sessionId": function({
                      _req
                    }) {
                      return _req.body.data.sessionId
                    },
                        "status": "SUCCESS",
                        "contractNo": "%s",
                        "loanAmount": 13000,
                        "installmentAmount": 1229.27,
                        "term": 12,
                        "interestRate": "6.5",
                        "floatRate": "17.5",
                        "dueDay": "26",
                        "firstDueDay": "2022-10-26"
                    }
                }
            }''' % ("KNWZ"+number)
        self.update(api, mode)

    def update_get_sms_success(self):
        '''
        银行卡授权申请（开户获取短信验证码）
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/preBpAuth"
        mode = '''{
                  "code": "0",
                  "message": "success",
                  "data": {
                    "status": "200",
                    "processId": "1663921933421c4c2c",
                    "resultCode": "0000",
                    "resultDescr": "Success",
                    "uniqueCode": "@id",
                    "resultExtendInfo": null
                  }
                }'''
        self.update(api, mode)

    def update_confirm_protocol_success(self):
        '''
        银行卡授权确认(开户校验验证码)
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/confirmBpAuth"
        mode = '''{
                  "code": "0",
                  "message": "success",
                  "data": {
                    "status": "200",
                    "processId":"@id",
                    "resultCode": "0000",
                    "resultDescr": "Success",
                    "agreementId": "xy@id",
                    "resultExtendInfo": null,
                    "validTo": null
                  }
                }'''
        self.update(api, mode)

    def update_pre_confirm_insure_success(self):
        '''
        投保预审-预审申请接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/submitBpApplicationFormInt"
        mode = {
                  "code": "0",
                  "message": "success",
                  "data": {
                    "cappTraceId": "@id",
                    "status": 200,
                    "code": 200,
                    "value": None
                  }
                }
        self.update(api, mode)

    def update_get_insureurl_success(self):
        '''
        投保H5页面获取
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpApplicationFormResultInt"
        mode = {
                  "code": "0",
                  "message": "success",
                  "data": {
                    "cappTraceId": "f54dc5de950b4540b5a238166bf4e4e5",
                    "status": 200,
                    "code": 200,
                    "value": {
                      "status": "SUCCESS",
                      "h5Url": "http://ecuat.tk.cn/channel/nprd/trace-xinbaosys-h5/?content=%7B%22appId%22%3A%2220211213919911215315025920%22%2C%22bankCardNo%22%3A%225522457610948010%22%2C%22bankNames%22%3A%22%E6%B2%B3%E5%8C%97%E9%93%B6%E8%A1%8C%22%2C%22callBackUrl%22%3A%22capp%3A%2F%2Fyuxin_h5_insurance_confirm%22%2C%22certNo%22%3A%22522636199401258808%22%2C%22fundInfos%22%3A%5B%7B%22fundCode%22%3A%22WEBANK%22%2C%22fundLoanAmt%22%3A%2213000.00%22%2C%22insureFee%22%3A%22107.42%22%7D%5D%2C%22insureSeriaNo%22%3A%22KNWZ202209230000000572%22%2C%22loanAmt%22%3A%2213000.00%22%2C%22mobileNo%22%3A%2213910000042%22%2C%22name%22%3A%22%E6%9D%8E%E5%80%A9%22%2C%22sysdata%22%3A%22jiexin%22%7D"
                    }
                  }
                }
        self.update(api, mode)

    def update_get_insureurl_fail(self):
        '''
        投保H5页面获取
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpApplicationFormResultInt"
        mode = {
                "code": "0",
                "message": "success",
                "data": {
                    "cappTraceId": "4ab038bbb6cc4c70b6889eaea6e1c959",
                    "status": 200,
                    "code": 200,
                    "value": {
                        "status": "FAIL",
                        "data": None
                    }
                }
            }
        self.update(api, mode)

    def update_loanpreapply_success(self):
        '''
        预进件-流水号申请接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/startBpApplicationSession"
        mode = {
                  "code": "0",
                  "message": "success",
                  "data": {
                    "cappTraceId": "da00c574e9a3493bb175dc07157d5086",
                    "status": 300,
                    "code": 400,
                    "value": {
                      "sessionId": "@id"
                    }
                  }
                }
        self.update(api, mode)
    def update_loanpreapply_fail(self):
        '''
        预进件-流水号申请接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/startBpApplicationSession"
        mode = {
                  "code": "0",
                  "message": "success",
                  "data": {
                    "cappTraceId": "da00c574e9a3493bb175dc07157d5086",
                    "status": 200,
                    "code": 400,
                    "value": {
                      "sessionId": None
                    }
                  }
                }
        self.update(api, mode)

    def update_loanapplynew_success(self):
        '''
        进件-授信申请接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/submitBpPreApplication"
        mode = {
                  "code": "0",
                  "message": "success",
                  "data": {
                    "cappTraceId": "ee14a8de3db54f64882e58942b248c5c",
                    "status": 200,
                    "code": 200,
                    "value": None
                  }
                }
        self.update(api, mode)

    def update_loanapplynew_fail(self):
        '''
        进件-授信申请接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/submitBpPreApplication"
        mode = {
                  "code": "9999",
                  "message": "mock失败",
                  "data": {
                    "cappTraceId": "ee14a8de3db54f64882e58942b248c5c",
                    "status": 200,
                    "code": 200,
                    "value": None
                  }
                }
        self.update(api, mode)


    def update_loanapplyquery_success(self, creditamount='20000.00', validto='2036-12-12 00:00:00'):
        '''
        授信结果查询接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpPreAfResult"
        mode = {
                  "code": "0",
                  "message": "success",
                  "data": {
                    "cappTraceId": "3bed2b61233f4bbd9502efb515d71bef",
                    "status": 200,
                    "code": 200,
                    "value": {
                      "status": "SUCCESS",
                      "data": {
                        "creditProduct": "F_AL_TK_HB",
                        "creditAmount": creditamount,
                        "creditType": "101",
                        "validTo": validto,
                        "creditNo": "cdn@id"
                      }
                    }
                  }
                }
        self.update(api, mode)

    def update_loanapplyquery_fail(self):
        '''
        授信结果查询接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpPreAfResult"
        mode = {
                "code": "0",
                "message": "success",
                "data": {
                    "cappTraceId": "4ab038bbb6cc4c70b6889eaea6e1c959",
                    "status": 200,
                    "code": 200,
                    "value": {
                        "status": "FAIL",
                        "data": None
                    }
                }
            }
        self.update(api, mode)

    def update_loanapplyconfirm_success(self):
        '''
        用信申请接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/submitBpConfirmation"
        mode = '''{
              "code": "0",
              "message": "success",
              "data": {
                "cappTraceId": "483fd9af4f5443108ca69b85183907c7",
                "status": 200,
                "code": 200,
                "value": {
                  "sessionId": function({
                      _req
                    }) {
                      return _req.body.data.sessionId
                    },
                  "status": "SUCCESS"
                }
              }
            }'''
        self.update(api, mode)


    def update_loanapplyconfirm_fail(self):
        '''
        用信申请接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/submitBpConfirmation"
        mode = '''{
              "code": "0",
              "message": "success",
              "data": {
                "cappTraceId": "483fd9af4f5443108ca69b85183907c7",
                "status": 200,
                "code": 200,
                "value": {
                  "sessionId": function({
                      _req
                    }) {
                      return _req.body.data.sessionId
                    },
                  "status": "FAIL"
                }
              }
            }'''
        self.update(api, mode)


    def update_loanconfirmquery_success(self, asset_info):
        '''
        用信结果查询接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpDisbursementResult"
        mode = '''{
                  "code": "0",
                  "message": "success",
                  "data": {
                    "cappTraceId": "e11a6e133a244f8b83e4ee3f3a130959",
                    "status": 200,
                    "code": 200,
                    "value": {
                      "status": "SUCCESS",
                      "failureReason": null,
                      "disbursementTime": "%s", 
                      "disbursementAmount": %s   //此金额未校验
                    }
                  }
                }''' % (get_date(fmt="%Y-%m-%d")+"T"+get_date(fmt="%H:%M:%S")+"+08:00", (asset_info['data']['asset']['amount']))
        self.update(api, mode)


    def update_loanconfirmquery_fail(self):
        '''
        用信结果查询接口
        :return:
        '''
        api = "/jiexin/jiexin_taikang/api/checkBpDisbursementResult"
        mode = '''{
                  "code": "0",
                  "message": "success",
                  "data": {
                    "cappTraceId": "e11a6e133a244f8b83e4ee3f3a130959",
                    "status": 200,
                    "code": 200,
                    "value": {
                      "status": "FAIL",
                      "failureReason": "mock放款失败",
                      "disbursementTime": null, 
                      "disbursementAmount": null 
                    }
                  }
                }'''
        self.update(api, mode)

    def update_queryrepayplan_success(self, asset_info):
        api = "/jiexin/jiexin_taikang/api/checkBpInstalmentSchedule"
        mode = {
              "code": "0",
              "message": "success",
              "data": {
                "cappTraceId": "8ca0faca587e49a681fb88986a3d7477",
                "status": 200,
                "code": 200,
                "value": {
                  "totalInstallmentNo": asset_info['data']['asset']['period_count'],
                  "caseStatus": "0",
                  "repayPlan": []
                }
              }
            }
        repayment_plan_tmp = {
                          "termNo": "1",
                          "agreedRepaymentDate": "2042-02-28",
                          "agreedPrincipal": 1051.43,
                          "agreedInterest": 68.07,
                          "agreedOInterest": 0,
                          "agreedPenaltyFee": 0,
                          "agreedFee": 107.42,
                          "repaymentDate": None,
                          "paidPrincipal": 0,
                          "paidInterest": 0,
                          "paidOInterest": 0,
                          "paidPenaltyFee": 0,
                          "paidFee": 0
                        }
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['termNo'] = i + 1
            repayment_plan['agreedRepaymentDate'] = fee_info['date']
            repayment_plan['agreedPrincipal'] = str(float(fee_info['principal'])/100)
            repayment_plan['agreedInterest'] = str(float(fee_info['interest'])/100)
            repayment_plan['agreedFee'] = str(float(fee_info['technical_service']) / 100)
            mode['data']['value']['repayPlan'].append(repayment_plan)
        self.update(api, mode)


if __name__ == "__main__":
    pass
