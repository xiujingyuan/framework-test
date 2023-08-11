# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *
import time


class HaishengtongDaqinMock(Easymock):
    def update_queryProtocolstatus_need_openaccount(self):
        api = "/quanhu/haishengtong_daqin/protocolBinding/queryProtocolInfo"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "status": {
                      "isSuccess": true,
                      "requestId": "reqid@id",
                      "responseMessage": "成功",
                      "responseCode": "0000",
                      "warningMessage": null
                    },
                    "protocolInfos": [{
                      "channel": "1",
                      "signNo": "",
                      "signStatus": 0, //0．申请成功但未确认绑定成功 1．申请成功且确定绑定成功
                      "signTime": "2021-09-24 14:11:21",
                      "transactionNo": ""
                    }]
                  }
                }'''
        self.update(api, mode)

    def update_getProtocolsms_success(self):
        api = "/quanhu/haishengtong_daqin/protocolBinding/getBankContractId"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "status": {
                      "isSuccess": true,
                      "requestId": "reqid@id",
                      "responseMessage": "成功",
                      "responseCode": "0000",
                      "warningMessage": "预签约成功 [0000] 交易成功"
                    },
                    "transactionNo": "@id"
                  }
                }'''
        self.update(api, mode)


    def update_Protocolconfirm_success(self):
        api = "/quanhu/haishengtong_daqin/protocolBinding/uploadVerificationCode"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "status": {
                      "isSuccess": true,
                      "requestId": "reqid@id",
                      "responseMessage": "成功",
                      "responseCode": "0000",
                      "warningMessage": "签约成功 [0000] 交易成功"
                    },
                    "signNo": "1202109241411533810002012714"
                  }
                }'''
        self.update(api, mode)

    def update_querybalance_success(self,BalanceControl=False):
        balance=0 if BalanceControl==True else 88888.88
        api = "/quanhu/haishengtong_daqin/dedicatedAccount/queryingBalance"
        mode = '''{
                      "code": 0,
                      "message": "",
                      "data": {
                        "status": {
                          "isSuccess": true,
                          "requestId": "reqid@id",
                          "responseMessage": "成功",
                          "responseCode": "0000", //“0000”:操作成功、"0020":操作失败”、0040”操作失败，系统异常，非成功的code会发送报错信息到TV里面
                          "warningMessage": null
                        },
                        "data": {
                          "productCode": function({
                            _req
                          }) {
                            return _req.body.productCode
                          },
                          "accountNo": function({
                            _req
                          }) {
                            return _req.body.accountNo
                          },
                          "releaseBalance": %s,
                          "queryDateTime": "2021-09-23 11:31:09", //目前没有校验这个时间
                          "enabled": true,
                          "canPay": true
                        }
                      }
                    }
                '''%(balance)
        self.update(api, mode)


    def update_apply_success(self, asset_info):
        api = "/quanhu/haishengtong_daqin/applyLoan/commitApplyLoanInfo"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "status": {
                      "isSuccess": true,
                      "requestId": "reqid@id",
                      "responseMessage": "成功",
                      "responseCode": "0000",
                      "warningMessage": null
                    },
                    "approvalAmount": %s,
                    "orderId": "@id", //存入dueBillNo
                    "subAccount": null
                  }
                }''' % (asset_info['data']['asset']['amount'])
        self.update(api, mode)

    def update_apply_fail(self,asset_info):
        api = "/quanhu/haishengtong_daqin/applyLoan/commitApplyLoanInfo"
        mode = '''{
                          "code": 0,
                          "message": "",
                          "data": {
                            "status": {
                              "isSuccess": false,
                              "requestId": "reqid@id",
                              "responseMessage": "mock操作失败，系统异常",
                              "responseCode": "0040",
                              "warningMessage": null
                            },
                            "approvalAmount": %s,
                            "orderId": "@id", //存入dueBillNo
                            "subAccount": null
                          }
                        }''' % (asset_info['data']['asset']['amount'])
        self.update(api, mode)

    def update_applyquery_success(self):
        api = "/quanhu/haishengtong_daqin/applyLoan/riskAuditResult"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "status": {
                      "isSuccess": true,
                      "requestId": "reqid@id",
                      "responseMessage": "查询成功",
                      "responseCode": "0000",
                      "warningMessage": null
                    },
                    "auditStatus": 8, //1-风险控制未通过，5-审核未通过，8-待放款（当授信成功处理），其他-处理中
                    "actExcutedTime": null,
                    "uniqueId": null
                  }
                }'''
        self.update(api, mode)

    def update_applyquery_fail(self):
        api = "/quanhu/haishengtong_daqin/applyLoan/riskAuditResult"
        mode = '''{
                          "code": 0,
                          "message": "",
                          "data": {
                            "status": {
                              "isSuccess": true,
                              "requestId": "reqid@id",
                              "responseMessage": "审核未通过",
                              "responseCode": "0000",
                              "warningMessage": null
                            },
                            "auditStatus": 5, //1-风险控制未通过，5-审核未通过，8-待放款（当授信成功处理），其他-处理中
                            "actExcutedTime": null,
                            "uniqueId": null
                          }
                        }'''
        self.update(api, mode)

    def update_applyquery_code_fail(self):
        '''
        异常情况，若资方未返回auditStatus，返回的code和isSuccess任意1个是失败的情况，找资方确认后可以根据这种错误切资方
        :return:
        '''
        api = "/quanhu/haishengtong_daqin/applyLoan/riskAuditResult"
        mode = '''{
                             "code": 0,
                             "message": "",
                             "data": {
                               "status": {
                                 "isSuccess": true,
                                 "requestId": "reqid@id",
                                 "responseMessage": "mock操作失败,参数错误",
                                 "responseCode": "0020",
                                 "warningMessage": null
                               },
                               "auditStatus": null,
                               "actExcutedTime": null,
                               "uniqueId": null
                             }
                           }'''
        self.update(api, mode)

    def update_applyconfirm_success(self):
        api = "/quanhu/haishengtong_daqin/applyLoan/confirmPayment"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "status": {
                      "isSuccess": true,
                      "requestId": "reqid@id",
                      "responseMessage": "处理成功",
                      "responseCode": "0000",
                      "warningMessage": null
                    }
                  }
                }'''
        self.update(api, mode)

    def update_applyconfirm_fail(self):
        api = "/quanhu/haishengtong_daqin/applyLoan/confirmPayment"
        mode = '''{
                          "code": 0,
                          "message": "",
                          "data": {
                            "status": {
                              "isSuccess": true,
                              "requestId": "reqid@id",
                              "responseMessage": "mock操作失败,参数错误",
                              "responseCode": "0020",
                              "warningMessage": null
                            }
                          }
                        }'''
        self.update(api, mode)

    def update_applyconfirmquery_success(self):
        api = "/quanhu/haishengtong_daqin/applyLoan/riskAuditResult"
        mode = '''{
                    "code": 0,
                    "message": "",
                    "data": {
                        "status": {
                            "isSuccess": true,
                            "requestId": "reqid@id",
                            "responseMessage": "查询成功",
                            "responseCode": "0000",
                            "warningMessage": null
                        },
                        "auditStatus": 6,  //6-放款成功，7-放款失败，其他-处理中
                        "actExcutedTime": "%s",
                        "uniqueId": "@id" //存入tradeNo ,若是资金方联测，该值与due_bill_no一样
                    }}''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, mode)

    def  update_applyconfirmquery_fail(self):
        api = "/quanhu/haishengtong_daqin/applyLoan/riskAuditResult"
        mode ='''{
                    "code": 0,
                    "message": "",
                    "data": {
                        "status": {
                            "isSuccess": true,
                            "requestId": "reqid@id",
                            "responseMessage": "放款失败",
                            "responseCode": "0000",
                            "warningMessage": null
                        },
                        "auditStatus": 7,  //6-放款成功，7-放款失败，其他-处理中
                        "actExcutedTime": "%s",
                        "uniqueId": "@id" //存入tradeNo ,若是资金方联测，该值与due_bill_no一样
                    }}''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, mode)

    def update_applyconfirmquery_code_fail(self):
        api = "/quanhu/haishengtong_daqin/applyLoan/riskAuditResult"
        mode = '''{
                            "code": 0,
                            "message": "",
                            "data": {
                                "status": {
                                    "isSuccess": true,
                                    "requestId": "reqid@id",
                                    "responseMessage": "mock返回非文档中错误码",
                                    "responseCode": "0050",
                                    "warningMessage": null
                                },
                                "auditStatus": null,  //6-放款成功，7-放款失败，其他-处理中
                                "actExcutedTime": "%s",
                                "uniqueId": "@id" //存入tradeNo ,若是资金方联测，该值与due_bill_no一样
                            }}''' % (get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, mode)

    def update_repayplan_success(self, asset_info):
        api = "/quanhu/haishengtong_daqin/repayment/paymentSchedule"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        trade_no = alr_info[0]['asset_loan_record_trade_no']
        mode = {
                  "code": 0,
                  "message": "",
                  "data": {
                    "status": {
                      "isSuccess": True,
                      "requestId": "reqid@id",
                      "responseMessage": "成功",
                      "responseCode": "0000",
                      "warningMessage": None
                    },
                    "repayScheduleList": []}}
        repayment_plan_tmp = {
                            "repaySeqId": 6562,
                            "contractNumber": "20210924XD047418",
                            "repayDate": "2021-10-24 00:00:00",
                            "repayAmount": 535.58,
                            "principal": 475.58,
                            "interest": 60,
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
                            "term": "1"
                          }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['term'] = i + 1
            repayment_plan['principal'] = float(fee_info['principal']) / 100
            repayment_plan['interest'] = float(fee_info['interest']) / 100
            repayment_plan['repayAmount'] = float('%.2f' % (repayment_plan['principal'] + repayment_plan['interest']))
            #repayment_plan['repayDate'] = fee_info['date']
            repayment_plan['repayDate'] = get_date(month=i + 1, fmt="%Y-%m-%d %H:%M:%S")
            repayment_plan['contractNumber'] = trade_no
            mode['data']['repayScheduleList'].append(repayment_plan)
        self.update(api, mode)

    def update_contract_success(self):
        api = "/quanhu/haishengtong_daqin/applyLoan/getContractFile"
        mode = '''{
                    "code": 0,
                    "message": "",
                    "data": {
                        "status": {
                            "isSuccess": true,
                            "requestId": "4a45b672fcbc41889b1f98b190aded27",
                            "responseMessage": "成功",
                            "responseCode": "0000",
                            "warningMessage": null
                        },
                        "signStatus": "4",
                        "fileImageUrl": "http://jbimages.oss-cn-shanghai.aliyuncs.com/1550801179351921b515.pdf"
                    }
                }'''
        self.update(api, mode)
