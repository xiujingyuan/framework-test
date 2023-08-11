# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayWeipinZhongweiMock(Easymock):
    # /zhongzhirong/weipin_zhongwei/repay.apl.trial 唯品中卫还款试算
    # /zhongzhirong/weipin_zhongwei/repay.apl	 唯品中卫还款申请
    # /zhongzhirong/weipin_zhongwei/repay.apl.query 唯品中卫还款结果查询
    # /zhongzhirong/weipin_zhongwei/repayplan.query	 唯品中卫还款计划查询

    def mock_weipin_zhongwei_repay_apply(self):
        api = "/zhongzhirong/weipin_zhongwei/repay.apl"
        mode = '''
        {
          "code": "0",
          "message": "成功",
          "data": {
            "respCode": "000000",
            "respMessage": "自动化测试",
            "status": "S",
            "userId": "16545892470612460068",
            "creditAppNo": function({
              _req
            }) {
              return _req.body.creditAppNo
            },
            "repaymentAppNo": function({
              _req
            }) {
              return _req.body.repaymentAppNo
            }
          }
        }
        '''
        self.update(api, mode)

    def mock_weipin_zhongwei_repay_query_success(self, item_no, withhold_serial_no, prin_amt=536.76, int_amt=105.0,
                                                 fee_amt=20.12, term_no=1, late_interest=0):
        # item_no 资产编号
        # withhold_serial_no 代扣序列号
        # paymentSeqNo channel key
        repay_amt = prin_amt + int_amt + late_interest
        repay_plan_list = [
            {
                "tenor": 1,
                "principalAmount": prin_amt,
                "interestAmount": int_amt,
                "penaltyAmount": late_interest,
                "feeAmount": 0,
                "compountAmount": 0,
                "delqDays": 0
            }
        ]
        if term_no == 12:
            repay_amt = 7000 + int_amt
            pre_repay_plan = [
                {
                    "tenor": 2,
                    "principalAmount": 544.81,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 3,
                    "principalAmount": 552.98,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 4,
                    "principalAmount": 561.28,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 5,
                    "principalAmount": 569.7,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 6,
                    "principalAmount": 578.24,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 7,
                    "principalAmount": 586.92,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 8,
                    "principalAmount": 595.72,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 9,
                    "principalAmount": 604.66,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 10,
                    "principalAmount": 613.73,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 11,
                    "principalAmount": 622.93,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 12,
                    "principalAmount": 632.27,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                }
            ]
            repay_plan_list = repay_plan_list + pre_repay_plan
        api = "/zhongzhirong/weipin_zhongwei/repay.apl.query"
        mode = {
            "code": 0,
            "message": "成功",
            "data": {
                "respCode": "000000",
                "respMessage": "访问成功",
                "creditAppNo": item_no,
                "userId": "16545892470612460068",
                "repaymentAppNo": withhold_serial_no,
                "paymentSeqNo": "C" + withhold_serial_no,
                "paymentStatus": "0",
                "failReason": None,
                "completeTime": get_date(fmt="%Y%m%d%H%M%S"),
                "guaranteeFee": fee_amt,
                "repaymentList": [{
                    "totalAmount": repay_amt,
                    "preFeeAmount": 0,
                    "planList": repay_plan_list
                }]
            }
        }
        self.update(api, mode)

    def mock_weipin_zhongwei_repay_notify(self, notify_flag="Y"):
        api = "/chongtian/weipin_zhongwei/repay/resultNotify"
        mode = {
            "code": "000000",
            "message": "自动化测试repaynotify",
            "data": {
                "notifyFg": notify_flag
            }
        }
        self.update(api, mode)

    def mock_weipin_zhongwei_repay_trial(self, item_no, prin_amt=536.76, int_amt=105.00, term_no=1, late_interest=0):
        repay_amt = prin_amt + int_amt
        repay_plan_list = [
            {
                "tenor": 1,
                "principalAmount": prin_amt,
                "interestAmount": int_amt,
                "penaltyAmount": late_interest,
                "feeAmount": 0,
                "compountAmount": 0,
                "delqDays": 0
            }
        ]
        if term_no == 12:
            repay_amt = 7000 + int_amt
            pre_repay_plan = [
                {
                    "tenor": 2,
                    "principalAmount": 544.81,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 3,
                    "principalAmount": 552.98,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 4,
                    "principalAmount": 561.28,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 5,
                    "principalAmount": 569.7,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 6,
                    "principalAmount": 578.24,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 7,
                    "principalAmount": 586.92,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 8,
                    "principalAmount": 595.72,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 9,
                    "principalAmount": 604.66,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 10,
                    "principalAmount": 613.73,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 11,
                    "principalAmount": 622.93,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                },
                {
                    "tenor": 12,
                    "principalAmount": 632.27,
                    "interestAmount": 0,
                    "penaltyAmount": 0,
                    "feeAmount": 0,
                    "compountAmount": 0,
                    "delqDays": 0
                }
            ]
            repay_plan_list = repay_plan_list + pre_repay_plan
        api = "/zhongzhirong/weipin_zhongwei/repay.apl.trial"
        mode = {
            "code": 0,
            "message": "成功",
            "data": {
                "respCode": "000000",
                "respMessage": "访问成功",
                "creditAppNo": item_no,
                "userId": "16549585226212947892",
                "repaymentList": [{
                    "totalAmount": repay_amt,
                    "preFeeAmount": None,
                    "planList": repay_plan_list
                }]
            }
        }
        self.update(api, mode)

    def mock_weipin_zhongwei_repay_plan_query(self, item_no, user_id="16545887197922460067"):
        api = "/zhongzhirong/weipin_zhongwei/repayplan.query"
        mode = {
            "code": 0,
            "message": "成功",
            "data": {
                "respCode": "000000",
                "respMessage": "访问成功",
                "creditAppNo": item_no,
                "userId": user_id,
                "planList": [
                    {
                        "tenor": 1,
                        "paymentDueDate": get_date(month=0, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 536.76,
                        "paymentPrincipal": 0,
                        "payableInterest": 105,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 3.62,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "2",
                        "paymentDate": None,
                        "totalAmount": 645.38,
                        "principalAmount": 536.76,
                        "interestAmount": 105,
                        "penaltyIntAmount": 3.62,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 9
                    },
                    {
                        "tenor": 2,
                        "paymentDueDate": get_date(month=1, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 544.81,
                        "paymentPrincipal": 0,
                        "payableInterest": 96.95,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "1",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 544.81,
                        "interestAmount": 96.95,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 3,
                        "paymentDueDate": get_date(month=2, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 552.98,
                        "paymentPrincipal": 0,
                        "payableInterest": 88.78,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 552.98,
                        "interestAmount": 88.78,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 4,
                        "paymentDueDate": get_date(month=3, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 561.28,
                        "paymentPrincipal": 0,
                        "payableInterest": 80.48,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 561.28,
                        "interestAmount": 80.48,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 5,
                        "paymentDueDate": get_date(month=4, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 569.7,
                        "paymentPrincipal": 0,
                        "payableInterest": 72.06,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 569.7,
                        "interestAmount": 72.06,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 6,
                        "paymentDueDate": get_date(month=5, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 578.24,
                        "paymentPrincipal": 0,
                        "payableInterest": 63.52,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 578.24,
                        "interestAmount": 63.52,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 7,
                        "paymentDueDate": get_date(month=6, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 586.92,
                        "paymentPrincipal": 0,
                        "payableInterest": 54.84,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 586.92,
                        "interestAmount": 54.84,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 8,
                        "paymentDueDate": get_date(month=7, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 595.72,
                        "paymentPrincipal": 0,
                        "payableInterest": 46.04,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 595.72,
                        "interestAmount": 46.04,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 9,
                        "paymentDueDate": get_date(month=8, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 604.66,
                        "paymentPrincipal": 0,
                        "payableInterest": 37.1,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 604.66,
                        "interestAmount": 37.1,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 10,
                        "paymentDueDate": get_date(month=9, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 613.73,
                        "paymentPrincipal": 0,
                        "payableInterest": 28.03,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 613.73,
                        "interestAmount": 28.03,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 11,
                        "paymentDueDate": get_date(month=10, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 622.93,
                        "paymentPrincipal": 0,
                        "payableInterest": 18.83,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.76,
                        "principalAmount": 622.93,
                        "interestAmount": 18.83,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    },
                    {
                        "tenor": 12,
                        "paymentDueDate": get_date(month=11, day=-1, fmt="%Y%m%d"),
                        "payablePrincipal": 632.27,
                        "paymentPrincipal": 0,
                        "payableInterest": 9.48,
                        "paymentInterest": 0,
                        "payablePenaltyInterest": 0,
                        "paymentPenaltyInterest": 0,
                        "payableCompoundInterest": 0,
                        "paymentCompoundInterest": 0,
                        "payableFee": 0,
                        "paymentFee": 0,
                        "paymentFlag": "0",
                        "paymentDate": None,
                        "totalAmount": 641.75,
                        "principalAmount": 632.27,
                        "interestAmount": 9.48,
                        "penaltyIntAmount": 0,
                        "compoundAmount": 0,
                        "feeAmount": 0,
                        "exemptAmount": 0,
                        "waivedAmount": 0,
                        "delqDays": 0
                    }
                ]
            }
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
