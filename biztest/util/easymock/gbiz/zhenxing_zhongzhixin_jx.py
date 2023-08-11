# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy

from biztest.util.tools.tools import get_date


class ZhenxingZhongzhixinJxMock(Easymock):

    def update_accountquery_new_user(self):
        """
        开户查询，没有在资金方开过户的新用户
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/checkBpAuthResult"
        body = {
                  "code": 0,
                  "message": "success",
                  "data": []
                }
        self.update(api, body)

    def update_accountquery_old_user(self, four_element):
        """
        开户查询，已经在资金方开户成功的老用户
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/checkBpAuthResult"
        body = {
                "code": 0,
                "message": "success",
                "data": [
                    {
                        "customerBankCode": "CCB",
                        "customerBankName": "中国建设银行",
                        "customerBankAccount": four_element['data']['bank_code'],
                        "customerIdCardNumber":  four_element['data']['id_number'],
                        "customerName": four_element['data']['user_name'],
                        "customerPhoneNumber":  four_element['data']['phone_number'],
                        "agreementId": "t@id",
                        "resultExtendInfo": None,
                        "validTo": None
                    }
                ]
            }
        self.update(api, body)

    def update_get_sessionid(self):
        """
        获取sessionid
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/startBpApplicationSession"
        body = {
              "code": 0,
              "message": "success",
              "data": {
                "cappTraceId": "3cf49b373c094718a45f48e00dd192ba",
                "status": 200,
                "code": 200,
                "value": {
                  "sessionId": "Se@id"
                }
              }
            }
        self.update(api, body)

    def update_get_uniquecode(self):
        """
        银行卡授权申请接口，获取授权码
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/preBpAuth"
        body = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "status": "200",
                    "processId": "jy@id",
                    "resultCode": "0000",
                    "resultDescr": "Success",
                    "uniqueCode": "Sq@id",
                    "resultExtendInfo": None
                  }
                }
        self.update(api, body)


    def update_confirm_bpauth(self):
        """
        银行卡授权确认接口
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/confirmBpAuth"
        body = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "status": "200",
                    "processId": "pi@id",
                    "resultCode": "0000",
                    "resultDescr": "Success",
                    "agreementId": "xy@id",
                    "resultExtendInfo": None,
                    "validTo": None
                  }
                }
        self.update(api, body)

    def update_ftp_upload(self):
        """
        上传附件接口
        """
        api = "/capital/ftp/upload/jiexin_zhenxing"
        body = {
                  "code": 0,
                  "message": "",
                  "data": {
                    "dir": "/KUAINIU_TEST/APP0/d4d4c0144599432ead74fbf6e5e48088000/",
                    "name": "d4d4c0144599432ead74fbf6e5e48088000-idcardfront.jpg",
                    "type": None,
                    "fileSize": 93824,
                    "fileDigest": "35108ee28e57f66116bb705c26d978b4",
                    "result": {
                      "code": 0,
                      "message": "成功"
                    }
                  }
                }
        self.update(api, body)

    def update_loanapplynew_success(self):
        """
        授信申请接口
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/submitBpPreApplication"
        body = {
              "code": 0,
              "message": "success",
              "data": {
                "cappTraceId": "9616fee0768e4d598ffc3ed9e6dc0604",
                "status": 200,
                "code": 200,
                "value": None
              }
            }
        self.update(api, body)

    def update_loanapplynew_fail(self):
        """
        授信申请接口
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/submitBpPreApplication"
        body = {
            "code": 1,
            "message": "mock 进件失败",
            "data": {
                "cappTraceId": "9616fee0768e4d598ffc3ed9e6dc0604",
                "status": 200,
                "code": 200,
                "value": None
            }
        }
        self.update(api, body)

    def update_loanapplyquery(self, creditamount='20000.00', validto='2036-12-12 00:00:00'):
        """
        授信查询接口
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/checkBpPreAfResult"
        body = {
              "code": 0,
              "message": "success",
              "data": {
                "cappTraceId": "ada45e1da41d422ea82c7e462012274c",
                "status": 200,
                "code": 200,
                "value": {
                  "status": "SUCCESS",
                  "data": {
                    "creditProduct": "F_AL_ZX_NU",
                    "creditAmount": creditamount,
                    "creditType": "101",
                    "validTo": validto,
                    "creditNo": "C@id"
                  }
                }
              }
            }
        self.update(api, body)

    def update_loanapplyquery_fail(self):
        """
        授信查询接口
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/checkBpPreAfResult"
        body = {
                  "code": 0,
                  "message": "mock失败测试",
                  "data": {
                    "cappTraceId": "45e7a27f2c5e4ee2a3b5a7aba4d847f1",
                    "status": 200,
                    "code": 200,
                    "value": {
                      "status": "FAIL",
                      "data": None
                    }
                  }
                }
        self.update(api, body)


    def update_loancreditapply(self):
        """
        预审申请接口
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/submitBpApplicationFormInt"
        body = {
              "code": 0,
              "message": "success",
              "data": {
                "cappTraceId": "d8b11855fcfe44f9b8b2faaa98f2c4fc",
                "status": 200,
                "code": 200,
                "value": None
              }
            }
        self.update(api, body)

    def update_loancreditapply_fail(self):
        """
        预审申请接口
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/submitBpApplicationFormInt"
        body = {
            "code": 1,
            "message": "mock失败测试",
            "data": {
                "cappTraceId": "d8b11855fcfe44f9b8b2faaa98f2c4fc",
                "status": 200,
                "code": 200,
                "value": None
            }
        }
        self.update(api, body)

    def update_loanpostcredit(self, code=0, status='SUCCESS', message='success'):
        """
        增信结果查询接口
        status	状态
            SUCCESS: 可投保/可继续
            FAIL: 不可投保/不可继续
            IN_PROGRESS: 预审进行中
            NO_AWARD: 未查到记录
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/checkBpApplicationFormResultInt"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "cappTraceId": "8bb8ea0ed62946e5965ca5ddd67ba418",
                    "status": 200,
                    "code": 200,
                    "value": {
                        "status": status,
                        "h5Url": ""
                    }
                }
            }
        self.update(api, body)

    def update_loancreditquery(self, asset_info, code=0, status='SUCCESS', message='success'):
        """
        预审结果查询接口
        status	预审结果状态
                SUCCESS: 预审成功
                FAIL: 预审失败
                IN_PROGRESS: 预审进行中
                NO_AWARD: 未查到记录
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/checkBpAwardCreditStatus"
        body = '''{
                "code": %s,
                "message": "%s",
                "data": {
                    "cappTraceId": "ad12f351f5c54f86b0a31926f9bc7cf7",
                    "status": 200,
                    "code": 200,
                    "value": {
                    "sessionId": function({
                      _req
                    }) {
                      return _req.body.data.sessionId
                    },
                        "status": "%s",
                        "contractNo": "Tkn@id",
                        "loanAmount": %s,
                        "installmentAmount": 2180.89,
                        "term": 12,
                        "interestRate": "8.3",
                        "floatRate": "15.7",
                        "dueDay": "10",
                        "firstDueDay": "%s",
                        "urlDetailPage": "https://aldi-web.uat.homecreditcfc.cn/channelingcc?accessToken=Qot6TySTwN54xc0ZRekWbrFAyK4L7r6Hhe0Yy5ZvFkmvrwqwJxAREg4wkaVeP5miSu9eljVXpeOLT5HEwI2jaVmFzwxGcGi_TgmHwys7lpA="
                    }
                }
            }''' % (code, message, status, asset_info['data']['asset']['amount'], get_date(month=1, fmt="%Y-%m-%d"))
        self.update(api, body)

    def update_loanapplyconfirm(self, status='SUCCESS', message='success'):
        """
        用信申请接口
        status	用信请求状态
            SUCCESS: 用信申请成功
            FAIL: 用信申请失败
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/submitBpConfirmation"
        body = '''{
                  "code": 0,
                  "message": "%s",
                  "data": {
                    "cappTraceId": "1e6db6b7c90f4a0880313acf37780d8b",
                    "status": 200,
                    "code": 200,
                    "value": {
                      "sessionId": function({
                      _req
                    }) {
                      return _req.body.data.sessionId
                    },
                      "status": "%s"
                    }
                  }
                }''' % (message, status)
        self.update(api, body)

    def update_loanconfirmquery(self, asset_info, code=0, status='SUCCESS', message='success'):
        """
        用信结果查询接口
        status	放款结果
            SUCCESS: 放款成功
            FAIL: 放款失败
            IN_PROGRESS: 放款中
            NO_AWARD: 未查到记录
        """
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/checkBpDisbursementResult"
        body = {
                  "code": code,
                  "message": message,
                  "data": {
                    "cappTraceId": "ed21a742c9774bc1bdf0bd583f8e4193",
                    "status": 200,
                    "code": 200,
                    "value": {
                      "status": status,
                      "failureReason": None,
                      "disbursementTime": get_date(fmt="%Y-%m-%d")+"T"+get_date(fmt="%H:%M:%S")+"+08:00",
                      "disbursementAmount": asset_info['data']['asset']['amount']
                    }
                  }
                }
        self.update(api, body)

    def update_queryrepayplan_success(self, asset_info):
        api = "/jiexin/zhenxing_zhongzhixin_jx/api/checkBpInstalmentSchedule"
        mode = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "cappTraceId": "eeb1e67964524c5fa8b5d6e6e97861c6",
                    "status": 200,
                    "code": 200,
                    "value": {
                      "totalInstallmentNo": asset_info['data']['asset']['period_count'],
                      "caseStatus": "0",
                      "repayPlan": [

                      ]
                    }
                  }
                }
        repayment_plan_tmp = {
            "termNo": "1",
            "agreedRepaymentDate": "2023-03-01",
            "agreedPrincipal": 2016.79,
            "agreedInterest": 161.39,
            "agreedOInterest": 0,
            "agreedCompoundInterest": 0,
            "agreedPenaltyFee": 0,
            "agreedFee": 185.8,
            "repaymentDate": None,
            "paidPrincipal": 0,
            "paidInterest": 0,
            "paidOInterest": 0,
            "paidCompoundInterest": 0,
            "paidPenaltyFee": 0,
            "paidFee": 0
        }
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['termNo'] = i + 1
            repayment_plan['agreedRepaymentDate'] = fee_info['date']
            repayment_plan['agreedPrincipal'] = str(float(fee_info['principal']) / 100)
            repayment_plan['agreedInterest'] = str(float(fee_info['interest']) / 100)
            repayment_plan['agreedFee'] = str(float(fee_info['technical_service']) / 100)
            mode['data']['value']['repayPlan'].append(repayment_plan)
        self.update(api, mode)
