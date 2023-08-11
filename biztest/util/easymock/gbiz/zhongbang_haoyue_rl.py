# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy

from biztest.util.tools.tools import get_date


class ZhongbangHaoyueRlMock(Easymock):

    def update_file_upload(self):
        """
        文件上传
        """
        api = "/runlou/zhongbang_haoyue_rl/loan.zb.assis.file.upload"
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "status": "S",
                "fileId": "ff80808186772b680186df167ea07912 @id"
              }
            }
        self.update(api, body)

    def update_credit_apply(self, status='P'):
        """
        进件，授信申请接口-
        credit_status 授信状态
                P 授信中
                S 授信成功
                F 授信拒绝
        """
        api = "/runlou/zhongbang_haoyue_rl/loan.zb.assis.credit.apply"
        body = {
                "code": "0",
                "message": "Success",
                "data": {
                    "status": status,
                    "applyNo": "CA1HGBDMSIIVGN4" # 没用到
                }
            }
        self.update(api, body)


    def update_credit_query(self, itemno, status='S', availableAmount=20000, creditEndDate='20361212'):
        """
        授信查询接口
        credit_status 授信状态
                P-授信中
                S-授信成功
                F-授信拒绝
        """
        api = "/runlou/zhongbang_haoyue_rl/loan.zb.assis.credit.query"
        body = {
                "code": "0",
                "message": "Success",
                "data": {
                    "status": status,
                    "openId": "openid_" + itemno,  # 资方返回格式：10108ZYDRLJR110101199307289506
                    "custId": "custid_@id",  # 资方返回 1000070026
                    "creditStartDate": "20230123",
                    "creditEndDate": creditEndDate,
                    "creditAmount": 10000,
                    "availableAmount": availableAmount,
                    "rateType": "",
                    "payMethod": "",
                    "termMonth": "12",
                    "rate": "",
                    "creditScore": "",
                    "fileList": [
                        {
                            "fileType": "06",
                            "fileId": "ff80808186772b680186e5123dfd439f" + itemno
                        }
                    ]
                }
            }
        self.update(api, body)

    def update_credit_query_notorder(self):
        """
        授信查询接口
        credit_status 授信状态
                P-授信中
                S-授信成功
                F-授信拒绝
        """
        api = "/runlou/zhongbang_haoyue_rl/loan.zb.assis.credit.query"
        body = {
            "code": "E2000001",
            "message": "授信申请不存在",
            "data": None
        }
        self.update(api, body)


    def update_agree_share_apply(self):
        """
        代扣共享协议号接口
        """
        api = "/runlou/zhongbang_haoyue_rl/loan.zb.assis.agree.share.apply"
        body = {
                "code": "0",
                "message": "Success",
                "data": {
                    "status": "S",
                    "remark": "交易成功"
                }
            }
        self.update(api, body)

    def update_disbursement_apply(self, status='P'):
        """
        用信申请
        loan_status 借款状态
            P-处理中
            S-成功
            F-失败
        """
        api = "/runlou/zhongbang_haoyue_rl/loan.zb.assis.disbursement.apply"
        body = {
                "code": "0",
                "message": "Success",
                "data": {
                    "status": status,
                    "loanNo": "",
                    "valueDate": "20290723",
                    "firstRepayDate": "20290823",
                    "lastRepayDate": "20300723",
                    "loanRate": 9.2,
                    "artificialno": ""
                }
            }
        self.update(api, body)

    def update_disbursement_query(self, status='S'):
        """
        用信查询
        loan_status 借款状态
            P-处理中
            S-成功
            F-失败
        """
        api = '/runlou/zhongbang_haoyue_rl/loan.zb.assis.disbursement.query'
        date=get_date(fmt="%Y%m%d")
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "cause": "",
                "status": status,
                "loanNo": "@id",
                "valueDate": date,  # 资方只返回年月日
                "firstRepayDate": "20290820",
                "lastRepayDate": "20300720",
                "loanRate": "9.2",
                "artificialno": "ZB-NPER-0000053450-10401-002",
                "fileList": [
                    {
                        "fileType": "11",
                        "fileId": "ff80808186772b680186e4a498252cfc CFS20230315174030742"
                    }
                ]
            }
        }
        self.update(api, body)


    def update_repayment_plan_query(self, asset_info):
        """
        还款计划查询
        """
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/runlou/zhongbang_haoyue_rl/loan.zb.assis.repayment.plan.query'
        body = {
            "code":"0",
            "message":"Success",
            "data":{
                "status":"S",
                "repayPlan":[]
            }
        }
        repayplan = {
                        "termNo":"1",
                        "repayDate":"20290820",
                        "principalAmount":"1038.41",
                        "interestAmount":"102.99",
                        "penaltyAmount":"0",
                        "paidPrincipal":"0",
                        "paidInterest":"0",
                        "paidPenaltyAmount":"0",
                        "intefine":"0",
                        "paidIntefine":"0",
                        "isOverdue":"0"
                    }

        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplan)
            repayment_plan['termNo'] = i + 1
            repayment_plan['principalAmount'] = float(fee_info['principal'])/100
            repayment_plan['interestAmount'] = float(fee_info['interest'])/100
            repayment_plan['repayDate'] = fee_info['date']
            body['data']['repayPlan'].append(repayment_plan)
        self.update(api, body)

    def update_file_download(self):
        """
        合同下载
        """
        api = '/runlou/zhongbang_haoyue_rl/loan.zb.assis.file.download'
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "status": "S",
                "busiDate": "20230315",
                "fileId": "ff80808186772b680186e4d93f3739f4 CFS20230315183803073",
                "billType": "e-con",
                "base64": "JVBERi0xLjYKJeLjz9MKMjA2"
              }
            }
        self.update(api, body)

    def update_certificateapply_success(self):
        """
        申请结清证明
        """
        api = '/runlou/zhongbang_haoyue_rl/loan.zb.assis.loan.rcpt.apply'
        body = {
              "code": "0",
              "message": "Success",
              "data": {
                "status": "S",  # S-成功;F-失败
                "imageName": "16873326765409248791.pdf",
                "imagePath": "/httpfiletrans/HttpFileTrans?method=download&FilePath=/UIP/receipt/2023/06/20230621/MM/027008/voucherType/16873326765409248791.pdf",
                "receiptCode": "16873326765409248791",
                "fileList": [
                  {
                    "fileType": "",
                    "fileId": ""
                  }
                ]
              }
            }
        self.update(api, body)


    def update_certificate_download_success(self):
        """
        下载结清证明
        """
        api = '/runlou/zhongbang_haoyue_rl/loan.zb.assis.file.temporary.download'
        body = {
                  "code": "0",
                  "message": "Success",
                  "data": {
                    "status": "S",  # S-成功;F-失败
                    "base64": "testurl"  # base64很难mock
                  }
                }
        self.update(api, body)