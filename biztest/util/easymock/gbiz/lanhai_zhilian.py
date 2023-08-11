# -*- coding: utf-8 -*-
from copy import deepcopy

from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class LanhaiZhilianMock(Easymock):
    def update_query_bind_card_new_user(self):
        api = "/lanhai/lanhai_zhilian/bob/querySignChannel.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "sysTime": "2023-01-12 14:21:26",
                    "respCode": "0000",
                    "applySerialNo": "ph_test_2871241637",
                    "seqNo": "1673505157530241637",
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "bizStsCd": "00000000",
                    "bizStsDesc": "成功",
                    "signAcctNo": "6216701020000000010",
                    "userName": "全渠道",
                    "userCertNo": "341126197709218366",
                    "userMobile": "15866383850",
                    "existFlag": "0", //0-不存在已签约通道，1-存在已签约通道
                    "departmentId": "xinzhongjin",
                    "channelName": "新中金签约"
                }
            }
        }'''
        self.update(api, mode)

    def update_query_bind_card_success(self):
        api = "/lanhai/lanhai_zhilian/bob/querySignChannel.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "sysTime": "2023-01-12 14:21:26",
                    "respCode": "0000",
                    "applySerialNo": "ph_test_2871241637",
                    "seqNo": "1673505157530241637",
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "bizStsCd": "00000000",
                    "bizStsDesc": "成功",
                    "signAcctNo": "6216701020000000010",
                    "userName": "全渠道",
                    "userCertNo": "341126197709218366",
                    "userMobile": "15866383850",
                    "existFlag": "1",  //0-不存在已签约通道，1-存在已签约通道
                    "departmentId": "xinzhongjin",
                    "channelName": "新中金签约"
                }
            }
        }'''
        self.update(api, mode)

    def update_sms_send_success(self):
        api = "/lanhai/lanhai_zhilian/bob/protocolSign.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "sysTime": "2023-01-12 14:22:27",
                    "respCode": "0000",
                    "applySerialNo": "ph_test_2871241637",
                    "seqNo": "1673505219039241637",
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "bankSignId": "E1424100000038373",
                    "signStatus": "1", //0-签约；1-预签约；2-签约失败
                    "traceNo": null,
                    "signId": "E@id",
                    "depatementId": null,
                    "signMsg": null,
                    "notityUrl": null,
                    "unionMerId": null,
                    "signTrid": null,
                    "signTokenType": null,
                    "prepareSignDate": null,
                    "prepareSignTime": null,
                    "prepareSignSqNo": null
                }
            }
        }'''
        self.update(api, mode)

    def update_sms_send_fail(self):
        api = "/lanhai/lanhai_zhilian/bob/protocolSign.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "00000001",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "挡板失败",
                    "success": true
                },
                "responseBody": {
                    "signStatus": "2" //0-签约；1-预签约；2-签约失败
                }
            }
        }'''
        self.update(api, mode)

    def update_sms_check_success(self):
        api = "/lanhai/lanhai_zhilian/bob/protocolSign.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "sysTime": "2023-01-12 14:55:30",
                    "respCode": "0000",
                    "applySerialNo": "ph_test_1961061057",
                    "seqNo": "1673507202800061057",
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "bankSignId": null,
                    "signStatus": "0", //0-签约；1-预签约；2-签约失败
                    "traceNo": null,
                    "signId": "E@id",
                    "depatementId": null,
                    "signMsg": null,
                    "notityUrl": null,
                    "unionMerId": null,
                    "signTrid": null,
                    "signTokenType": null,
                    "prepareSignDate": null,
                    "prepareSignTime": null,
                    "prepareSignSqNo": null
                }
            }
        }'''
        self.update(api, mode)

    def update_sms_check_fail(self):
        api = "/lanhai/lanhai_zhilian/bob/protocolSign.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "00000001",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "挡板失败",
                    "success": true
                },
                "responseBody": {
                    "signStatus": "2" //0-签约；1-预签约；2-签约失败
                }
            }
        }'''
        self.update(api, mode)

    def update_creaditapply_success(self):
        api = "/lanhai/lanhai_zhilian/bob/accountBind.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "sysTime": "2023-01-12 15:00:20",
                    "respCode": "0000",
                    "applySerialNo": "ph_test_1961061057",
                    "seqNo": "1673507492000061057",
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "authState": "0" //0-绑卡成功，1-绑卡失败
                }
            }
        }'''
        self.update(api, mode)

    def update_upload_file_success(self):
        api = "/lanhai/lanhai_zhilian/fileUpload/fileUploadByPost.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "sysTime": "2023-01-11 15:41:03",
                    "respCode": "0000",
                    "applySerialNo": "ph_test_9158466310",
                    "seqNo": "1673423532198466310",
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "dealStatus": "1"
                }
            }
        }'''
        self.update(api, mode)


    def update_loanapplynew_success(self):
        api = "/lanhai/lanhai_zhilian/bob/loanApply.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0000",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "creditApplyId": "CA@id",
                    "status": true
                }
            }
        }'''
        self.update(api, mode)

    def update_loanapplynew_success_02(self):
        api = "/lanhai/lanhai_zhilian/bob/loanApply.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0030",
                    "applySerialNo": "ph_test_9158466310",
                    "seqNo": "1673423536242466310",
                    "respMsg": "授信在有效期内，不能重复授信",
                    "success": true
                },
                "responseBody": {
                    "status": false
                }
            }
        }'''
        self.update(api, mode)

    def update_loanapplynew_fail(self):
        api = "/lanhai/lanhai_zhilian/bob/loanApply.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "sysTime": "2023-01-12 10:53:11",
                    "respCode": "0034",
                    "applySerialNo": "ph_test_4453022157",
                    "seqNo": "1673492662933022157",
                    "respMsg": "授信拒绝后未间隔30天再次发起授信",
                    "success": true
                },
                "responseBody": {
                    "status": false
                }
            }
        }'''
        self.update(api, mode)

    def update_loanapplyquery_success(self, asset_info):
        api = "/lanhai/lanhai_zhilian/bob/creditInfo.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0000",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "creditInfo": {
                        "userId": "000UC020000101852",
                        "productNo": "PN00000026",
                        "creditTotalAmount": 20000,
                        "startDate": "2023-01-11 00:00:00",
                        "endDate": "2029-01-11 23:59:59",
                        "useAmount": 0,
                        "availAmount": 20000,
                        "frozenAmount": 0,
                        "approvalStatus": "2", //0-未审核 1-审核中 2-审核成功 3-审核拒绝 4-人工审核
                        "validStatus": "1",
                        "creditApplyId": "CA@id",
                        "reason": null,
                        "loanInterestRate": "0.24",
                        "currentNumRange": "3-12",
                        "address": "上海市上海市长宁区金钟路52号",
                        "email": "",
                        "memberProportion": null,
                        "memberName": null,
                        "memberAddr": null
                    }
                }
            }
        }'''
        self.update(api, mode)

    def update_loanapplyquery_fail(self, asset_info):
        api = "/lanhai/lanhai_zhilian/bob/creditInfo.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "sysTime": "2023-01-11 16:45:45",
                    "respCode": "0000",
                    "applySerialNo": "ph_test_4453022157",
                    "seqNo": "1673427416587022157",
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "creditInfo": {
                        "userId": "000UC020000101854",
                        "productNo": "PN00000026",
                        "creditTotalAmount": 0,
                        "startDate": "2023-01-11 16:46:17",
                        "endDate": "2024-01-11 23:59:59",
                        "useAmount": 0,
                        "availAmount": 0,
                        "frozenAmount": 0,
                        "approvalStatus": "3", //0-未审核 1-审核中 2-审核成功 3-审核拒绝 4-人工审核
                        "validStatus": "0",
                        "creditApplyId": "000CA2023010000000098",
                        "reason": null,
                        "loanInterestRate": null,
                        "currentNumRange": null,
                        "address": "上海市上海市长宁区金钟路52号",
                        "email": "",
                        "memberProportion": null,
                        "memberName": null,
                        "memberAddr": null
                    }
                }
            }
        }'''
        self.update(api, mode)

    def update_loanapplyquery_fail_02(self):
        api = "/lanhai/lanhai_zhilian/bob/creditInfo.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0000",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "creditInfo": {
                        "userId": "000UC020000101852",
                        "productNo": "PN00000026",
                        "creditTotalAmount": 20000,
                        "startDate": "2023-01-11 00:00:00",
                        "endDate": "2029-01-11 23:59:59",
                        "useAmount": 0,
                        "availAmount": 100,
                        "frozenAmount": 0,
                        "approvalStatus": "2", //0-未审核 1-审核中 2-审核成功 3-审核拒绝 4-人工审核
                        "validStatus": "1",
                        "creditApplyId": "CA@id",
                        "reason": null,
                        "loanInterestRate": "0.24",
                        "currentNumRange": "3-12",
                        "address": "上海市上海市长宁区金钟路52号",
                        "email": "",
                        "memberProportion": null,
                        "memberName": null,
                        "memberAddr": null
                    }
                }
            }
        }'''
        self.update(api, mode)

    def update_loanacreditapply_success(self):
        api = "/lanhai/lanhai_zhilian/bob/accountBind.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0000",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "authState": "0"
                }
            }
        }'''
        self.update(api, mode)

    def update_loanapplyconfirm_success(self):
        api = "/lanhai/lanhai_zhilian/bob/loanPurpose.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0000",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "loanApplyId": "LA@id"
                }
            }
        }'''
        self.update(api, mode)

    def update_loanapplyconfirm_success_02(self):
        api = "/lanhai/lanhai_zhilian/bob/loanPurpose.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0041",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "进件数据保存失败。可能是重复发送了请求或者系统网络不稳定",
                    "success": true
                },
                "responseBody": {
                    "loanApplyId": null
                }
            }
        }'''
        self.update(api, mode)

    def update_loanapplyconfirm_fail(self):
        api = "/lanhai/lanhai_zhilian/bob/loanPurpose.json"
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0005",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "支用失败",
                    "success": true
                },
                "responseBody": {
                    "loanApplyId": null
                }
            }
        }'''
        self.update(api, mode)

    def update_loanapplyconfirmquery_success(self, asset_info, item_no):
        api = "/lanhai/lanhai_zhilian/bob/queryloanPurpose.json"
        alr = get_asset_loan_record_by_item_no(item_no)
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0000",
                    "applySerialNo": "%s",
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "applyInfoList": [
                        {
                            "loanApplyId": "%s",
                            "applytime": "%s",
                            "name": "郭柳",
                            "certificateKind": "0",
                            "certificateNo": "370306199907144248",
                            "loanInvoiceId": "LIA@id",
                            "applyAmt": %s,
                            "auditAmt": %s,
                            "loanpaytime": "%s",
                            "applyStatus": "17", //16-放款中；17-已放款；21-放款失败
                            "reason": null,
                            "orderId": null,
                            "repaydate": 11
                        }
                    ]
                }
            }
        }''' % (item_no, alr[0]['asset_loan_record_identifier'],
                get_date(fmt="%Y-%m-%d %H:%M:%S"),
                asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['amount'],
                get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, mode)

    def update_loanapplyconfirmquery_fail(self, asset_info, item_no):
        api = "/lanhai/lanhai_zhilian/bob/queryloanPurpose.json"
        alr = get_asset_loan_record_by_item_no(item_no)
        mode = '''{
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0000",
                    "applySerialNo": function({_req}) {return _req.body.applySerialNo},
                    "seqNo": function({_req}) {return _req.body.seqNo},
                    "respMsg": "响应成功",
                    "success": true
                },
                "responseBody": {
                    "applyInfoList": [
                        {
                            "loanApplyId": "%s",
                            "applytime": "%s",
                            "name": "郭柳",
                            "certificateKind": "0",
                            "certificateNo": "370306199907144248",
                            "loanInvoiceId": "LIA@id",
                            "applyAmt": %s,
                            "auditAmt": %s,
                            "loanpaytime": "%s",
                            "applyStatus": "21", //16-放款中；17-已放款；21-放款失败
                            "reason": "对方行应答RJ01应答信息账号不存在",
                            "orderId": null,
                            "repaydate": 11
                        }
                    ]
                }
            }
        }''' % (alr[0]['asset_loan_record_identifier'],
                get_date(fmt="%Y-%m-%d %H:%M:%S"),
                asset_info['data']['asset']['amount'],
                asset_info['data']['asset']['amount'],
                get_date(fmt="%Y-%m-%d %H:%M:%S"))
        self.update(api, mode)

    def update_queryrepayplan_success(self, item_no, asset_info):
        api = "/lanhai/lanhai_zhilian/bob/queryReplanInfo.json"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        loantnr = asset_info['data']['asset']['period_count']
        loanactvdt =get_date(fmt="%Y%m%d")
        alr = get_asset_loan_record_by_item_no(item_no)
        loanno = alr[0].get('asset_loan_record_due_bill_no')
        dnseq = alr[0].get('asset_loan_record_identifier')
        mode = {
            "code": 0,
            "message": "success",
            "data": {
                "header": {
                    "respCode": "0000",
                    "applySerialNo": "ph_test_9158466310",
                    "seqNo": "1673429860203466310",
                    "respMsg": "响应成功",
                    "success": True
                },
                "responseBody": {
                    "resultList": [
                        {
                            "cooperateId": "000UC010000101718",
                            "loanInvoiceId": loanno,
                            "repayNum": asset_info['data']['asset']['period_count'],
                            "repayAmt": asset_info['data']['asset']['amount'],
                            "repayPlanList": []
                        }
                    ]
                }
            }
        }
        repayment_plan_tmp = {
                            "currentNum": 12,
                            "preRepayAmount": 189.12,
                            "preRepayPrincipal": 185.41,
                            "preRepayInterest": 3.71,
                            "preRepayFee": 0,
                            "preRepayOverdueFee": 0,
                            "repayPlanStatus": "1",
                            "startDate": "2023-12-11 00:00:00",
                            "repayRepayAmount": 189.12,
                            "repayRepayPrincipal": 185.41,
                            "repayRepayInterest": 3.71,
                            "repayRepayFee": 0,
                            "repayRepayOverdueFee": 0,
                            "paidRepayAmount": 0,
                            "paidRepayPrincipal": 0,
                            "paidRepayInterest": 0,
                            "paidRepayFee": 0,
                            "paidRepayOverdueFee": 0,
                            "overDueDays": 0,
                            "preRepayDate": "20240111",
                            "lastRepayDate": None
                        }
        for i in range(asset_info['data']['asset']['period_count']):
                fee_info = get_fee_info_by_period(rate_info, i + 1)
                repayment_plan = deepcopy(repayment_plan_tmp)
                repayment_plan['currentNum'] = i + 1
                repayment_plan['preRepayDate'] = fee_info['date'].replace("-", "")
                repayment_plan['repayRepayAmount'] = float(fee_info['principal']/100) + float(fee_info['interest']/100)
                repayment_plan['repayRepayPrincipal'] = float(fee_info['principal']/100)
                repayment_plan['repayRepayInterest'] = float(fee_info['interest']/100)
                mode['data']['responseBody']['resultList'][0]['repayPlanList'].append(repayment_plan)
        self.update(api, mode)
