# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import *

class JingqueHaikouMock(Easymock):

    def update_getsms_success(self):
        api = "/jingquehaikou/lb/cooperation/bank/bindCard/v1"
        mode = '''{
                      "code": 0,
                      "message": "请求成功",
                      "data": {
                        "retMessage": "成功",
                        "retCode": "0000",
                        "requestNo": "7718576641b149e38cbd72f2073ac157",
                        "status": "TO_VALIDATE"
                      }
                    }'''
        self.update(api, mode)

    def update_protocol_success(self):
        api = "/jingquehaikou/lb/cooperation/bank/bindCardConfirm/v1"
        mode = '''{
                    "code": 0,
                    "message": "请求成功",
                    "data": {
                        "retMessage": "成功",
                        "retCode": "0000",
                        "status": "BIND_SUCCESS"
                    }
                }'''
        self.update(api, mode)


    def update_protocolquery_process(self):
        api = "/jingquehaikou/lb/cooperation/bank/queryCardInfo/v1"
        mode = '''{
                  "code": 0,
                  "message": "请求成功",
                  "data": {
                    "bankCardNo": "6228480469731901978",
                    "retMessage": "成功",
                    "idCardNo": "513021199206092103",
                    "retCode": "0000",
                    "bindStatus": "0"//bindStatus：0-未绑卡，1-已绑卡
                  }
                }'''
        self.update(api, mode)


    def update_protocolquery_success(self):
        api = "/jingquehaikou/lb/cooperation/bank/queryCardInfo/v1"
        mode = '''{
                  "code": 0,
                  "message": "请求成功",
                  "data": {
                    "bankCardNo": "6228480469731901978",
                    "retMessage": "成功",
                    "idCardNo": "513021199206092103",
                    "retCode": "0000",
                    "bindStatus": "1"//bindStatus：0-未绑卡，1-已绑卡
                  }
                }'''
        self.update(api, mode)


    def update_apply_success(self):
        api = "/jingquehaikou/lb/api/loan/submitApplyInfo/v1"
        mode = '''{
                  "code": 0, //非0重试
                  "message": "请求成功",
                  "data": {
                    "retMessage": "成功",
                    "retCode": "0000", //0000成功，0001失败-重试
                    "applicationCode": "@id"
                  }
                }'''
        self.update(api, mode)

    def update_contractpush_success(self):
        api = "/jingquehaikou/lb/app/uploadFile/v1"
        mode = '''{
                  "code": 0, //非0重试
                  "message": "请求成功",
                  "data": {
                    "retMessage": "提交成功",
                    "retCode": "0000" //0000成功，0001失败-重试
                  }
                }'''
        self.update(api, mode)


    def update_applyquery_success(self, asset_info):
        grant_at = get_date(fmt="%Y%m%d")
        count = int(asset_info["data"]["asset"]["period_count"])
        amount = (asset_info["data"]["asset"]["amount"])
        due_at = get_date(month=count, fmt="%Y%m%d")
        api = "/jingquehaikou/lb/app/queryLoanProgress/v1"
        mode = '''{
                  "code": 0,
                  "message": "请求成功",
                  "data": {
                    "endDate": "%s",
                    "retMessage": "成功",
                    "rejectFieldss": [],
                    "coagencyCode": "szjksybl",
                    "approvalTime": "%s",
                    "retCode": "0000", //0000成功 0001失败-重试
                    "approvalPeriod": %s,
                    "applyAmount": %s, //校验的参数
                    "peroidType": "M",
                    "currentStatusCode": "03",
                    // currentStatusCode
                    // 01-待绑卡
                    // 02-放款中
                    // 03-放款成功
                    // 04-放款失败
                    "iouInfos": [{
                      "iouCode": "dbn@id", //存入due_bill_no
                      "lendAmount": %s, //校验的参数，放款成功的时候会校验
                      "lendDate": "%s",
                      "repayType": "2", //1 一次性还本付息；2 等额本息；3 先息后本；4 等本等息
                      "yearRate": 0.085,
                      "failReason": null,
                      "coagencyCode": "szjksybl"
                    }],
                    "approvalAmount": %s,
                    "applyDate": "%s",
                    "applyPeriod": %s, //校验的参数
                    "applicationCode": function({
                      _req
                    }) {
                      return _req.body.applicationCode
                    }, //与我方的asset_loan_record_trade_no校验，若不一致会报错重试
                    "contractCode": "@id", //存入asset_loan_record_identifier中
                    "startDate": "%s"
                  }
                }''' % (due_at, grant_at, count, amount, amount, grant_at, amount, grant_at, count, grant_at)
        self.update(api, mode)


    def update_applyquery_fail(self, asset_info):
        grant_at = get_date(fmt="%Y%m%d")
        count = int(asset_info["data"]["asset"]["period_count"])
        amount = (asset_info["data"]["asset"]["amount"])
        due_at = get_date(month=count, fmt="%Y%m%d")
        api = "/jingquehaikou/lb/app/queryLoanProgress/v1"
        mode = '''{
                  "code": 0,
                  "message": "请求成功",
                  "data": {
                    "endDate": "%s",
                    "retMessage": "成功",
                    "rejectFieldss": [],
                    "coagencyCode": "szjksybl",
                    "approvalTime": "%s",
                    "retCode": "0000", //0000成功 0001失败-重试
                    "approvalPeriod": %s,
                    "applyAmount": %s, //校验的参数
                    "peroidType": "M",
                    "currentStatusCode": "04",
                    // currentStatusCode
                    // 01-待绑卡
                    // 02-放款中
                    // 03-放款成功
                    // 04-放款失败
                    "iouInfos": [{
                      "iouCode": "dbn@id", //存入due_bill_no
                      "lendAmount": %s, //校验的参数，放款成功的时候会校验
                      "lendDate": "%s",
                      "repayType": "2", //1 一次性还本付息；2 等额本息；3 先息后本；4 等本等息
                      "yearRate": 0.085,
                      "failReason": null,
                      "coagencyCode": "szjksybl"
                    }],
                    "approvalAmount": %s,
                    "applyDate": "%s",
                    "applyPeriod": %s, //校验的参数
                    "applicationCode": function({
                      _req
                    }) {
                      return _req.body.applicationCode
                    }, //与我方的asset_loan_record_trade_no校验，若不一致会报错重试
                    "contractCode": "@id", //存入asset_loan_record_identifier中
                    "startDate": "%s"
                  }
                }''' % (due_at, grant_at, count, amount, amount, grant_at, amount, grant_at, count, grant_at)
        self.update(api, mode)


    def update_repayplan_success(self, asset_info):
        api = "/jingquehaikou/lb/cooperation/repaymentplan/search/v1"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
                "code": 0,
                "message": "请求成功",
                "data": {
                    "retMessage": "成功",
                    "planList": [],
                    "retCode": "0000"
                }}
        repayment_plan_tmp = {
                "periodNo": 1,
                "deadlineDate": "2021-05-18",
                "repayInterest": 35.42,
                "repayPrincipal": 400.68,
                "repayAmount": 436.1
            }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['periodNo'] = i + 1
            repayment_plan['repayPrincipal'] = float(fee_info['principal']) / 100
            repayment_plan['repayInterest'] = float(fee_info['interest']) / 100
            repayment_plan['repayAmount'] = float(
                '%.2f' % (repayment_plan['repayPrincipal'] + repayment_plan['repayInterest']))
            repayment_plan['deadlineDate'] = fee_info['date']
            mode['data']['planList'].append(repayment_plan)
        self.update(api, mode)


    def update_contractdown_success(self):
        api = "/jingquehaikou/lb/app/searchContractFile/v1"
        mode = '''{
                      "code": 0,
                      "message": "请求成功",
                      "data": {
                        "retMessage": "成功",
                        "attachList": [{
                            "imagePath": "http://file.jingquedt.com:80/114,8f350e803557f9", //这个地址若是没有pdf后缀，会自动补全，否则合同下载任务会报错
                            "imageName": "JK20210115000002044.pdf",
                            "imageType": "QT1",
                            "tplName": "借款合同"
                          },
                          {
                            "imagePath": "http://file.jingquedt.com:80/114,8f35169a926708",
                            "imageName": "JK20210115000002041.pdf",
                            "imageType": "QT4",
                            "tplName": "个人信用报告查询授权书"
                          }
                        ],
                        "retCode": "0000"
                      }
                    }'''
        self.update(api, mode)




if __name__ == "__main__":
    pass
