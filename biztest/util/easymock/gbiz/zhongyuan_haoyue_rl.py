# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy

from biztest.util.tools.tools import get_date


class ZhongyuanHaoyueRlMock(Easymock):

    def update_apply(self):
        '''
        准入接口
        :return:
        '''
        # 01 可授信
        # 02 本渠道已授信
        # 03 其他渠道已授信
        # 00 拒绝
        api = ''
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "status": "01",
                "queryTime": "2023-06-21",
                "remark": "可授信"
            }
        }
        self.update(api, body)

    def update_credit_apply(self, itemno, status='P'):
        """
        进件，授信申请接口
        credit_status 授信状态
                P 授信中
                S 授信成功
                F 授信拒绝
        """
        api = "/runlou/zhongyuan_haoyue_rl/rl.assis.credit.apply"
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": status,
                "applyNo": "CA1HQRM3MR2M1OG"
            }
        }
        self.update(api, body)

    def update_credit_query(self, itemno, status='S'):
        """
        授信查询接口
        credit_status 授信状态
                P-授信中
                S-授信成功
                F-授信拒绝
        """
        api = "/runlou/zhongyuan_haoyue_rl/rl.assis.credit.query"
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": status,
                "applyNo": "CA1HQRM3MR2M1OG",
                "bindType": "2",
                "creditAmount": "",
                "limitType": "02",
                "availableAmount": "",
                "minLoanAmount": "",
                "rate": "",
                "fileList": [
                    # 这里面的没用到
                ]
            }
        }
        # 资方返回查询订单不存在demo
        # {
        #     "code": "E2000001",
        #     "message": "授信申请不存在",
        #     "data": null
        # }
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

    def update_bind_card_sign(self, status='S'):
        """
        银行卡签约申请
        """
        api = "/runlou/zhongyuan_haoyue_rl/rl.assis.bind.card.sign"
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": "29414d89ffd04685b9b0af2ea5419853",
                "status": status
            }
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
        api = "/runlou/zhongyuan_haoyue_rl/rl.assis.loan.apply"
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": status,
                "loanNo": "LA1HQRPUYQCYAYO"
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
        api = '/runlou/zhongyuan_haoyue_rl/rl.assis.loan.query'
        date = get_date(fmt="%Y%m%d")
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": status,
                "loanNo": "LA1HQRPUYQCYAYO",
                "loanAmount": "10000.00",
                "loanRate": "8.00",
                "loanDate": date,
                "loanTime": "2023-06-20 16:50:25",
                "firstRepayDate": "",
                "lastRepayDate": "",
                "contractNo": "CTI" + itemno
            }
        }

        # {
        #     "code": "0",
        #     "message": "Success",
        #     "data": {
        #         "cause": "测试放款失败",
        #         "businessNo": "W2023041687327539",
        #         "status": "F",
        #         "loanNo": "LA1HQUWI7P7P4W0"
        #     }
        # }
        self.update(api, body)

    def update_no_order(self):
        api = '/runlou/zhongyuan_haoyue_rl/rl.assis.loan.query'
        body = {
                "code": "E2000001",
                "message": "借款申请不存在",
                "data": None
            }
        self.update(api, body)

    def update_repayment_plan_query(self, itemno, asset_info):
        """
        还款计划查询
        """
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/runlou/zhongyuan_haoyue_rl/rl.assis.repayment.plan.query'
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": itemno,
                "status": "S",
                "repayPlanList": [],
                "loanNo": "LA1HQRPUYQCYAYO"
            }
        }
        repayplan = {
                    "startDate": "2025-02-25",
                    "dueDate": "2025-03-25",
                    "graceDate": "2025-03-28",
                    "period": "1",
                    "planStatus": "0",
                    "repayPrincipal": 808.51,
                    "repayInterest": 61.37,
                    "repayDefaultInterest": 0,
                    "repayFee": 0,
                    "repayLateFee": 0,
                    "actualRepayPrincipal": 0,
                    "actualRepayInterest": 0,
                    "actualRepayDefaultInterest": 0,
                    "actualRepayFee": 0,
                    "actualRepayLateFee": 0,
                    "reduceAmount": 0,
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


    def update_certify_apply(self, itemno):
        """
        下载结清证明
        """
        api = '/runlou/zhongyuan_haoyue_rl/rl.assis.loan.certify.apply'
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": "ca" + str(itemno),
                "status": "S"
            }
        }
        self.update(api, body)

    def update_certify_query(self, itemno):
        """
        结清证明查询
        """
        api = '/runlou/zhongyuan_haoyue_rl/rl.assis.loan.certify.apply'
        body = {
            "code": "0",
            "message": "Success",
            "data": {
                "businessNo": "ca" + str(itemno),
                "status": "S",
                "filePath": "/writable/aggregation/cash/out/20250122/certification_LA1HUND22IML2WW_01.pdf"
            }
        }
        self.update(api, body)


