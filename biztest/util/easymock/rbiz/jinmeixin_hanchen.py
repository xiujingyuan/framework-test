# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayJinmeixinHanchenMock(Easymock):
    # /chongtian/jinmeixin_hanchen/repayplan/query 崇天待还款查询
    # /chongtian/jinmeixin_hanchen/repay/request 崇天主动还款
    # /chongtian/jinmeixin_hanchen/repay/queryStatus 崇天还款结果查询
    # /chongtian/jinmeixin_hanchen/repay/calc 崇天试算
    # /chongtian/jinmeixin_hanchen/repay/resultNotify 崇天推送

    def mock_jinmeixin_hanchen_repay_query_success(self, loan_no, order_id, pay_order_id, prin_amt=226.84,
                                                   int_amt=48.33,
                                                   fee_amt=3.74, repay_status='SUCCESS', term_no=1):
        # loan_no 资产编号
        # order_id 代扣序列号
        # pay_order_id 代扣channel_key
        # repay_status 有SUCCESS和PART
        repay_amt = round(prin_amt + int_amt + fee_amt, 2)
        api = "/chongtian/jinmeixin_hanchen/repay/queryStatus"
        mode = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "orderId": order_id,
                "repayStatus": repay_status,
                "repayResult": "normal还款成功" + repay_status,
                "failCode": None,
                "repayPlanList": [{
                    "loanOrderNo": "TN" + loan_no,
                    "termNo": term_no,
                    "payOrderId": pay_order_id,
                    "repayStatus": repay_status,
                    "repayResult": "normal还款成功" + repay_status,
                    "repayAmt": repay_amt,
                    "repayPrin": prin_amt,
                    "repayInt": int_amt,
                    "repayPen": 0,
                    "repayFee": fee_amt,
                    "repayTime": get_date()
                }]
            }
        }
        self.update(api, mode)

    def mock_jinmeixin_hanchen_repay_query_settle_success(self, loan_no, order_id, pay_order_id, prin_amt=226.84,
                                                          int_amt=48.33, fee_amt=3.74, repay_status='SUCCESS'):
        # loan_no 资产编号
        # order_id 代扣序列号
        # pay_order_id 代扣channel_key
        # 提前结清，返回的是每一期的list
        repay_amt = prin_amt + int_amt + fee_amt
        api = "/chongtian/jinmeixin_hanchen/repay/queryStatus"
        mode = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "orderId": order_id,
                "repayStatus": repay_status,
                "repayResult": "settle全额还款成功",
                "failCode": None,
                "repayPlanList": [{
                    "loanOrderNo": "TN" + loan_no,
                    "termNo": 1,
                    "payOrderId": pay_order_id,
                    "repayStatus": repay_status,
                    "repayResult": "settle全额还款成功",
                    "repayAmt": repay_amt,
                    "repayPrin": prin_amt,
                    "repayInt": int_amt,
                    "repayPen": 0,
                    "repayFee": fee_amt,
                    "repayTime": get_date()
                },
                    {
                        "termNo": 2,
                        "repayAmt": 230.81,
                        "repayPrin": 230.81,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 3,
                        "repayAmt": 234.85,
                        "repayPrin": 234.85,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 4,
                        "repayAmt": 238.96,
                        "repayPrin": 238.96,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 5,
                        "repayAmt": 243.14,
                        "repayPrin": 243.14,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 6,
                        "repayAmt": 247.39,
                        "repayPrin": 247.39,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 7,
                        "repayAmt": 251.73,
                        "repayPrin": 251.73,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 8,
                        "repayAmt": 256.13,
                        "repayPrin": 256.13,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 9,
                        "repayAmt": 260.61,
                        "repayPrin": 260.61,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 10,
                        "repayAmt": 265.17,
                        "repayPrin": 265.17,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 11,
                        "repayAmt": 269.82,
                        "repayPrin": 269.82,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 12,
                        "repayAmt": 274.55,
                        "repayPrin": 274.55,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    }
                ]
            }
        }
        self.update(api, mode)

    def mock_jinmeixin_hanchen_repay_notify(self, notify_flag="Y"):
        api = "/chongtian/jinmeixin_hanchen/repay/resultNotify"
        mode = {
            "code": "000000",
            "message": "自动化测试repaynotify",
            "data": {
                "notifyFg": notify_flag
            }
        }
        self.update(api, mode)

    def mock_jinmeixin_hanchen_repay_trial(self, loan_no, prin_amt=226.84, int_amt=48.33, fee_amt=3.74,
                                           repay_type="DO", term_no=1):
        # 正常还款试算和仅剩fee的试算
        repay_amt = round(prin_amt + int_amt + fee_amt, 2)
        repay_plan_list = [
            {
                "termNo": term_no,
                "repayDate": get_date(month=1, fmt="%Y%m%d"),
                "repayAmt": repay_amt,
                "repayPrin": prin_amt,
                "repayInt": int_amt,
                "repayPen": 0,
                "repayFee": fee_amt
            }
        ]
        if repay_type == "DO":
            repay_term = [term_no]
        else:
            repay_term = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
            pre_repay_plan = [
                {
                    "termNo": 2,
                    "repayDate": get_date(month=2, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 3,
                    "repayDate": get_date(month=3, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 4,
                    "repayDate": get_date(month=4, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 5,
                    "repayDate": get_date(month=5, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 6,
                    "repayDate": get_date(month=6, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 7,
                    "repayDate": get_date(month=7, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 8,
                    "repayDate": get_date(month=8, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 9,
                    "repayDate": get_date(month=9, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 10,
                    "repayDate": get_date(month=10, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 11,
                    "repayDate": get_date(month=11, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                },
                {
                    "termNo": 12,
                    "repayDate": get_date(month=12, fmt="%Y%m%d"),
                    "repayAmt": 0,
                    "repayPrin": 0,
                    "repayInt": 0,
                    "repayPen": 0,
                    "repayFee": 0
                }]
            repay_plan_list = repay_plan_list + pre_repay_plan
        api = "/chongtian/jinmeixin_hanchen/repay/calc"
        mode = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "loanOrderNo": "TN" + loan_no,
                "repayType": repay_type,
                "repayTerm": repay_term,
                "repayAmt": repay_amt,
                "repayPrin": prin_amt,
                "repayInt": int_amt,
                "repayPen": 0,
                "repayFee": fee_amt,
                "bankCardList": [
                    {}
                ],
                "repayPlanList": repay_plan_list
            }
        }
        self.update(api, mode)

    def mock_jinmeixin_hanchen_repay_trial_settle(self, loan_no, prin_amt=226.84, int_amt=48.33, fee_amt=3.74,
                                                  total_prin_amt=3000):
        # 提前结清试算
        repay_amt = round(prin_amt + int_amt + fee_amt, 2)
        total_repay_amt = round(total_prin_amt + int_amt + fee_amt, 2)
        api = "/chongtian/jinmeixin_hanchen/repay/calc"
        mode = {
            "code": "000000",
            "msg": "成功",
            "data": {
                "loanOrderNo": "TN" + loan_no,
                "repayType": "PRE",
                "repayTerm": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7,
                    8,
                    9,
                    10,
                    11,
                    12
                ],
                "repayAmt": total_repay_amt + int_amt + fee_amt,
                "repayPrin": total_prin_amt,
                "repayInt": int_amt,
                "repayFee": fee_amt,
                "repayPen": 0,
                "bankCardList": [{},
                                 {}
                                 ],
                "repayPlanList": [{
                    "termNo": 1,
                    "repayDate": get_date(month=1, fmt="%Y%m%d"),
                    "repayAmt": repay_amt,
                    "repayPrin": prin_amt,
                    "repayInt": int_amt,
                    "repayPen": 0,
                    "repayFee": fee_amt
                },
                    {
                        "termNo": 2,
                        "repayDate": get_date(month=2, fmt="%Y%m%d"),
                        "repayAmt": 230.81,
                        "repayPrin": 230.81,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 3,
                        "repayDate": get_date(month=3, fmt="%Y%m%d"),
                        "repayAmt": 234.85,
                        "repayPrin": 234.85,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 4,
                        "repayDate": get_date(month=4, fmt="%Y%m%d"),
                        "repayAmt": 238.96,
                        "repayPrin": 238.96,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 5,
                        "repayDate": get_date(month=5, fmt="%Y%m%d"),
                        "repayAmt": 243.14,
                        "repayPrin": 243.14,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 6,
                        "repayDate": get_date(month=6, fmt="%Y%m%d"),
                        "repayAmt": 247.39,
                        "repayPrin": 247.39,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 7,
                        "repayDate": get_date(month=7, fmt="%Y%m%d"),
                        "repayAmt": 251.73,
                        "repayPrin": 251.73,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 8,
                        "repayDate": get_date(month=8, fmt="%Y%m%d"),
                        "repayAmt": 256.13,
                        "repayPrin": 256.13,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 9,
                        "repayDate": get_date(month=9, fmt="%Y%m%d"),
                        "repayAmt": 260.61,
                        "repayPrin": 260.61,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 10,
                        "repayDate": get_date(month=10, fmt="%Y%m%d"),
                        "repayAmt": 265.17,
                        "repayPrin": 265.17,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 11,
                        "repayDate": get_date(month=11, fmt="%Y%m%d"),
                        "repayAmt": 269.82,
                        "repayPrin": 269.82,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    },
                    {
                        "termNo": 12,
                        "repayDate": get_date(month=12, fmt="%Y%m%d"),
                        "repayAmt": 274.55,
                        "repayPrin": 274.55,
                        "repayInt": 0,
                        "repayPen": 0,
                        "repayFee": 0
                    }
                ]
            }
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
