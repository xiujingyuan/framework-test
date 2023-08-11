# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy

from biztest.util.tools.tools import get_date


class ZhongbangZhongjiMock(Easymock):

    def update_loanpreapply_success(self):
        """
        上传文件成功
        """
        api = "/zhongbang/zhongbang_zhongji/upload"
        body = {
                "code": 0,
                "message": "外层msg",
                "data": {
                    "code": "000000",
                    "msg": "交易成功!",
                    "result": [
                        {
                            "fileId": "ff80808184ae3b7501858501e3cc036c 10106ZYDKNZN20230106a764d3b9"
                        }
                    ]
                }
            }
        self.update(api, body)

    def update_loanapplynew_success(self):
        """
        进件，授信申请接口-------返回状态0和1都当做成功处理
        credit_status 授信状态
                0 授信中
                1 授信成功
                2 授信拒绝
        """
        api = "/zhongbang/zhongbang_zhongji/cridApplicNew"
        body = '''{
                "code": 0,
                "message": "",
                "data": {
                    "code": "000000",
                    "msg": "SUCCESS",
                    "result": {
                        "credit_status": "0",
                        "fail_msg": "",
                        "open_id": function({
                              _req
                            }) {
                              return _req.body.openId
                            },
                        "cust_id": "",
                        "credit_start_date": "",
                        "credit_end_date": "",
                        "credit_amount": 20000
                    }
                }
            }'''
        self.update(api, body)

    def update_loanapplynew_fail(self):
        """
        进件，授信申请接口-------返回状态0和1都当做成功处理
        credit_status 授信状态
                0 授信中
                1 授信成功
                2 授信拒绝
        """
        api = "/zhongbang/zhongbang_zhongji/cridApplicNew"
        body = '''{
                "code": 0,
                "message": "失败测试",
                "data": {
                    "code": "000000",
                    "msg": "mock 失败",
                    "result": {
                        "credit_status": "2",
                        "fail_msg": "",
                        "open_id": function({
                              _req
                            }) {
                              return _req.body.openId
                            },
                        "cust_id": "",
                        "credit_start_date": "",
                        "credit_end_date": "",
                        "credit_amount": 20000
                    }
                }
            }'''
        self.update(api, body)
    def update_loanapplyquery(self, credit_amount=20000, available_amount=20000, credit_end_date='20361212'):
        """
        授信查询接口
        credit_status 授信状态
                0-授信中
                1-授信成功
                2-授信拒绝
        """
        api = "/zhongbang/zhongbang_zhongji/newGrntCrDtQry"
        body = '''{
                "code": 0,
                "message": "",
                "data": {
                    "code": "000000",
                    "msg": "SUCCESS",
                    "result": {
                        "rate": null,
                        "credit_status": "1",
                        "fail_msg": "",
                        "open_id": function({
                              _req
                            }) {
                              return _req.body.openId
                            },
                        "cust_id": "1000058252",
                        "credit_start_date": "20230101",
                        "credit_end_date": "%s",
                        "credit_amount": %s,
                        "available_amount": %s,
                        "rate_type": "",
                        "pay_method": "",
                        "term_month": "12",
                        "credit_score": "",
                        "file_list": [
                            {
                                "file_type": "06",
                                "file_id": "ff80808184ae3b750185865480a21758 CFS20230106170602906"
                            }
                        ]
                    }
                }
            }''' % (credit_end_date, credit_amount, available_amount)
        self.update(api, body)

    def update_loanapplyquery_fail(self):
        """
        授信查询接口
        credit_status 授信状态
                0-授信中
                1-授信成功
                2-授信拒绝
        """
        api = "/zhongbang/zhongbang_zhongji/newGrntCrDtQry"
        body = '''{
                   "code": 0,
                   "message": "授信查询拒绝",
                   "data": {
                       "code": "000000",
                       "msg": "mock授信查询失败",
                       "result": {
                           "rate": null,
                           "credit_status": "2",
                           "fail_msg": "",
                           "open_id": function({
                              _req
                            }) {
                              return _req.body.openId
                            },
                           "cust_id": "1000058252",
                           "credit_start_date": "20230101",
                           "credit_end_date": "20261212",
                           "credit_amount": "20000",
                           "available_amount": "20000",
                           "rate_type": "",
                           "pay_method": "",
                           "term_month": "12",
                           "credit_score": "",
                           "file_list": [
                           ]
                       }
                   }
               }'''
        self.update(api, body)

    def update_loanpostapply_success(self):
        """
        代扣共享协议号接口，主要是上传协议号
        """
        api = "/zhongbang/zhongbang_zhongji/withAgreeShar"
        body = {
                "code": 0,
                "message": "",
                "data": {
                    "code": "000000",
                    "msg": "SUCCESS",
                    "result": {
                        "RetCd": "000000",
                        "RetInf": "交易成功"
                    }
                }
            }
        self.update(api, body)

    def update_applyconfirm_success(self):
        """
        用信申请
        loan_status 借款状态
            0-打款处理中
            1-打款成功
            2-打款失败
            3-借款失败
        """
        api = "/zhongbang/zhongbang_zhongji/crdtApply"
        body = {
              "code": 0,
              "message": "",
              "data": {
                "code": "000000",
                "msg": "SUCCESS",
                "result": {
                  "loan_status": "0",
                  "fail_msg": "",
                  "partner_loan_no": "",
                  "value_date": get_date(fmt="%Y%m%d"),
                  "first_repay_date": get_date(month=1, fmt="%Y-%m-%d"),
                  "last_repay_date": get_date(month=12, fmt="%Y-%m-%d"),
                  "loan_rate": 9,
                  "artificialno": ""
                }
              }
            }
        self.update(api, body)

    def update_applyconfirm_fail(self):
        """
        用信申请
        loan_status 借款状态
            0-打款处理中
            1-打款成功
            2-打款失败
            3-借款失败
        """
        api = "/zhongbang/zhongbang_zhongji/crdtApply"
        body = {
            "code": 0,
            "message": "失败mock",
            "data": {
                "code": "000000",
                "msg": "mock 用信失败",
                "result": {
                    "loan_status": "2",
                    "fail_msg": "",
                    "partner_loan_no": "",
                    "value_date": "",
                    "first_repay_date": "",
                    "last_repay_date": "",
                    "loan_rate": 9,
                    "artificialno": ""
                }
            }
        }
        self.update(api, body)

    def update_loanconfirm_query_success(self):
        """
        授信查询
        loan_status 借款状态
            0-打款处理中
            1-打款成功，借款合同签署完成
            2-打款失败
            3-借款失败
            4-打款成功，合同签署中
        """
        api = '/zhongbang/zhongbang_zhongji/normLanStsQry'
        body = {
                "code": 0,
                "message": "",
                "data": {
                    "code": "000000",
                    "msg": "SUCCESS",
                    "result": {
                        "artificialno": "ZB-NPER-0000044546-10401-002",
                        "loan_status": "1",
                        "fail_msg": "",
                        "partner_loan_no": "P@id",
                        "value_date": get_date(fmt="%Y%m%d"),
                        "first_repay_date": get_date(month=1, fmt="%Y-%m-%d"),
                        "last_repay_date": get_date(month=12, fmt="%Y-%m-%d"),
                        "loan_rate": 9,
                        "file_list": [
                            {
                                "file_type": "11",
                                "file_id": "ff80808184ae3b750185869a12d01de7 CFS20230106182202267"
                            }
                        ]
                    }
                }
            }
        self.update(api, body)

    def update_loanconfirm_query_fail(self):
        """
        授信查询
        loan_status 借款状态
            0-打款处理中
            1-打款成功，借款合同签署完成
            2-打款失败
            3-借款失败
            4-打款成功，合同签署中
        """
        api = '/zhongbang/zhongbang_zhongji/normLanStsQry'
        body = {
            "code": 0,
            "message": "用信查询失败mock",
            "data": {
                "code": "000000",
                "msg": "mock 放款失败",
                "result": {
                    "artificialno": "ZB-NPER-0000044546-10401-002",
                    "loan_status": "2",
                    "fail_msg": "内层失败mock的",
                    "partner_loan_no": "",
                    "value_date": "",
                    "first_repay_date": "",
                    "last_repay_date": "",
                    "loan_rate": 9,
                    "file_list": [
                    ]
                }
            }
        }
        self.update(api, body)

    def update_loan_query_repayplan(self, asset_info):
        """
        还款计划查询
        """
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/zhongbang/zhongbang_zhongji/normRpymntPlntQry'
        body = {
              "code": 0,
              "message": "",
              "data": {
                "code": "000000",
                "msg": "SUCCESS",
                "result": {
                  "repay_plan": []
                }
              }
            }
        repayplan = {
                  "principal1": 799.51,
                  "interest1": 77.5,
                  "term_no1": "1",
                  "repay_date": "20270924",
                  "penalty_amount1": 0,
                  "paid_principal1": 0,
                  "paid_interest1": 0,
                  "paid_penalty_amount1": 0,
                  "intefine1": 0,
                  "paid_intefine1": 0,
                  "is_overdue": "0"
                }

        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplan)
            repayment_plan['term_no1'] = i + 1
            repayment_plan['principal1'] = float(fee_info['principal'])/100
            repayment_plan['interest1'] = float(fee_info['interest'])/100
            repayment_plan['repay_date'] = fee_info['date']
            body['data']['result']['repay_plan'].append(repayment_plan)
        self.update(api, body)

    def update_contractdown_success(self):
        """
        合同下载
        """
        api = '/zhongbang/zhongbang_zhongji/download'
        body = {
              "code" : 0,
              "message" : "",
              "data" : {
                "code" : "000000",
                "msg" : "交易成功!",
                "result" : [ {
                  "busiDate" : get_date(fmt="%Y%m%d"),
                  "fileId" : "ff80808184ae3b750185869a12d01de7 CFS20230106182202267",
                  "billType" : "e-con",
                  "base64" : ""}]
              }
            }
        self.update(api, body)

    def update_certificateapply_success(self):
        """
        申请结清证明
        """
        api = '/zhongbang/zhongbang_zhongji/loanRcptCrt'
        body = {
                  "code": 0,
                  "message": "",
                  "data": {
                    "code": "000000",
                    "msg": "SUCCESS",
                    "result": {
                      "image_name": "16771466060261539454.pdf",
                      "image_path": "/httpfiletrans/HttpFileTrans?method=download&FilePath=/UIP/receipt/2023/02/20230223/ZX/027008/voucherType/16771466060261539454.pdf",
                      "receipt_cde": "16771466060261539454",
                      "fail_msg": "",
                      "file_list": [{
                        "file_type": "",
                        "file_id": ""
                      }]
                    }
                  }
                }
        self.update(api, body)

    def update_certificatedownload_success(self):
        """
        下载结清证明
        """
        api = '/zhongbang/zhongbang_zhongji/fileDownload'
        body = {
                  "code": 0,
                  "message": "",
                  "data": {
                    "code": "000000",
                    "msg": "交易成功",
                    "result": [{
                      "base64": "testurl"  # 这个base64不好mock，此处不mock
                    }]
                  }
                }
        self.update(api, body)