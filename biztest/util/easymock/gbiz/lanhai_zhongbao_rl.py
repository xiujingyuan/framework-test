# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy

from biztest.util.tools.tools import get_date


class LanhaiZhongbaoRlMock(Easymock):

    def bind_card_sign(self):
        api = "/runlou/lanhai_zhongbao_rl/rl.assis.bind.card.sign"
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": "c62018c50039493c9c8bc7cc8adaa409",
                "status": "S",
                "authTransNbr": "@id"
            }
        }
        self.update(api, body)

    def bind_card_sign_check(self):
        api = "/runlou/lanhai_zhongbao_rl/rl.assis.bind.card.sign.code.check"
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": "@id",
                "status": "S"
            }
        }
        self.update(api, body)

    def update_credit_apply(self, itemno, status='P'):
        """
        进件，授信申请接口-
        credit_status 授信状态
                P 授信中
                S 授信成功
                F 授信拒绝
        """
        api = "/runlou/lanhai_zhongbao_rl/rl.assis.credit.apply"
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": status,
                "applyNo": "CA1HN" + str(itemno)  # 有唯一性
            }
        }
        self.update(api, body)

    def update_credit_query(self, itemno, status='S', availableAmount=20000, creditEndDate='2036-12-12'):
        """
        授信查询接口
        credit_status 授信状态
                P-授信中
                S-授信成功
                F-授信拒绝
        """
        api = "/runlou/lanhai_zhongbao_rl/rl.assis.credit.query"
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": status,
                "applyNo": "CA1HN" + str(itemno),   #CA1HN9IY0GR30G0
                "bindType": "1",
                "creditAmount": "10000.00",
                "creditStartDate": "2023-05-10",
                "creditEndDate": creditEndDate,
                "limitType": "01",
                "availableAmount": availableAmount,
                "minLoanAmount": "",
                "rate": "8.90",
                "fileList": [
                    {
                        "fileId": "F1HN9IY0MXBZ7K",
                        "filePath": "1"
                    },
                    {
                        "fileId": "F1HN9IY0MXBZ7L",
                        "filePath": "2"
                    },
                    {
                        "fileId": "F1HN9IY0MXBZ7M",
                        "filePath": "3"
                    },
                    {
                        "fileId": "F1HN9IY0MXBZ7N",
                        "filePath": "5"
                    },
                    {
                        "fileId": "F1HN9IY0MXBZ7O",
                        "filePath": "6"
                    },
                    {
                        "fileId": "F1HN9IY0MXBZ7P",
                        "filePath": "8"
                    },
                    {
                        "fileId": "F1HN9IY0MXBZ7Q",
                        "filePath": "29"
                    },
                    {
                        "fileId": "F1HN9JA479XON4",
                        "filePath": "1"
                    },
                    {
                        "fileId": "F1HN9JA479XON5",
                        "filePath": "2"
                    },
                    {
                        "fileId": "F1HN9JA479XON6",
                        "filePath": "3"
                    },
                    {
                        "fileId": "F1HN9JA479XON7",
                        "filePath": "5"
                    },
                    {
                        "fileId": "F1HN9JA479XON8",
                        "filePath": "6"
                    },
                    {
                        "fileId": "F1HN9JA479XON9",
                        "filePath": "8"
                    },
                    {
                        "fileId": "F1HN9JA479XONA",
                        "filePath": "29"
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
        api = "/runlou/lanhai_zhongbao_rl/rl.assis.credit.query"
        body = {
            "code": "E2000001",
            "message": "授信申请不存在",
            "data": None
        }
        self.update(api, body)

    def update_disbursement_apply(self, itemno, status='P'):
        """
        用信申请
        loan_status 借款状态
            P-处理中
            S-成功
            F-失败
        """
        api = "/runlou/lanhai_zhongbao_rl/rl.assis.loan.apply"
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": status,
                "loanNo": "LA1HN" + str(itemno)
            }
        }
        self.update(api, body)

    def update_disbursement_query(self, itemno, status='S'):
        """
        用信查询
        loan_status 借款状态
            P-处理中
            S-成功
            F-失败
        """
        api = '/runlou/lanhai_zhongbao_rl/rl.assis.loan.query'
        date = get_date(fmt="%Y-%m-%d")
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": status,
                "loanNo": "LA1HN" + str(itemno),
                "loanAmount": "5000.00",
                "loanRate": "8.90",
                "loanDate": date,  # 资方未返回时分秒
                "loanTime": "2023-12-09 14:02:49",
                "firstRepayDate": "",
                "lastRepayDate": "2024-12-09",
                "fileList": [{
                    "fileId": "F1HN9JLCPSH7GG",
                    "filePath": "7"
                },
                    {
                        "fileId": "F1HN9JLCPSH7GH",
                        "filePath": "9"
                    },
                    {
                        "fileId": "F1HN9JLCPSH7GI",
                        "filePath": "10"
                    }
                ]
            }
        }
        self.update(api, body)

    def update_repayment_plan_query(self, itemno, asset_info):
        """
        还款计划查询
        """
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/runlou/lanhai_zhongbao_rl/rl.assis.repayment.plan.query'
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": "S",
                "loanNo": "LA1HN" + str(itemno),
                "repayPlanList": []
            }}
        repayplan = {
            "startDate": "2023-12-09",
            "dueDate": "2024-01-09",
            "period": "1",
            "planStatus": "0",
            "repayPrincipal": "799.88",
            "repayInterest": "74.17",
            "repayDefaultInterest": "0.0",
            "repayFee": "0",
            "repayLateFee": "0",
            "actualRepayPrincipal": "0.00",
            "actualRepayInterest": "0.00",
            "actualRepayDefaultInterest": "0.0",
            "actualRepayFee": "0",
            "actualRepayLateFee": "0",
            "reduceAmount": "0",
            "overdueDays": "0"
        }

        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplan)
            repayment_plan['period'] = i + 1
            repayment_plan['repayPrincipal'] = float(fee_info['principal']) / 100
            repayment_plan['repayInterest'] = float(fee_info['interest']) / 100
            repayment_plan['dueDate'] = fee_info['date']
            body['data']['repayPlanList'].append(repayment_plan)
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
