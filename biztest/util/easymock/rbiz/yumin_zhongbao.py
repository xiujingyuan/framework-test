# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayYuminZhongbaoMock(Easymock):
    # /zhongzhirong/yumin_zhongbao/ym.repay.status	裕民中保还款查询
    # /zhongzhirong/yumin_zhongbao/ym.repay.apply  裕民中保还款申请
    # /zhongzhirong/yumin_zhongbao/ym.card.change 裕民中保还款接口
    # /zhongzhirong/yumin_zhongbao/ym.card.pre.change	裕民中保还款发送短信
    # /zhongzhirong/yumin_zhongbao/ym.repay.trial	裕民中保还款试算

    def mock_yumin_zhongbao_repay_apply(self):
        api = "/zhongzhirong/yumin_zhongbao/ym.repay.apply"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "reqstatus": "Accept"
            }
        }
        self.update(api, mode)

    def mock_yumin_zhongbao_repay_query_success(self, repay_status="Success"):
        api = "/zhongzhirong/yumin_zhongbao/ym.repay.status"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "repaymentMsg": "",
                "repaymentStatus": repay_status
            }
        }
        self.update(api, mode)

    def mock_yumin_zhongbao_repay_trial(self, prin_amt=300000, int_amt=1000):
        repat_amt = prin_amt + int_amt
        api = "/zhongzhirong/yumin_zhongbao/ym.repay.trial"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "guaranteeAmount": 0,
                "loanBalance": prin_amt,
                "loanInterestRate": 781,
                "netAmt": repat_amt,
                "overdueIntAmt": 0,
                "overduePnpAmt": 0,
                "overduePnyInt": 0,
                "penaltyInterestRate": 1171.5,
                "principalAmount": prin_amt,
                "repymtIntAmt": int_amt,
                "repymtPnpAmt": prin_amt,
                "repymtPnyIntAmt": 0,
                "totalAmt": repat_amt
            }
        }
        self.update(api, mode)

    def mock_yumin_zhongbao_repay_plan(self, due_bill_no):
        api = "/zhongzhirong/yumin_zhongbao/ym.repay.plan"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "planList": [
                    {
                        "currentArrears": 0,
                        "interestAmount": 1953,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 24117,
                        "repayDate": get_date(fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "1",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 1796,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 24274,
                        "repayDate": get_date(month=1, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "2",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 1638,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 24432,
                        "repayDate": get_date(month=2, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "3",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 1479,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 24591,
                        "repayDate": get_date(month=3, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "4",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 1318,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 24752,
                        "repayDate": get_date(month=4, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "5",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 1157,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 24913,
                        "repayDate": get_date(month=5, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "6",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 995,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 25075,
                        "repayDate": get_date(month=6, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "7",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 832,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 25238,
                        "repayDate": get_date(month=7, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "8",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 668,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 25402,
                        "repayDate": get_date(month=8, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "9",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 502,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 25568,
                        "repayDate": get_date(month=9, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "10",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 336,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 25734,
                        "repayDate": get_date(month=10, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "11",
                        "totalAmount": 28366,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    },
                    {
                        "currentArrears": 0,
                        "interestAmount": 169,
                        "invalidCouponAmount": 0,
                        "loanNo": due_bill_no,
                        "otsndCmpdIntBal": 0,
                        "otsndIntAmt": 0,
                        "otsndPnpAmt": 0,
                        "otsndPnyIntAmt": 0,
                        "overdueDay": "0",
                        "paymentFlag": "PR",
                        "penaltyIntAmount": 0,
                        "planNo": "",
                        "principalAmount": 25904,
                        "repayDate": get_date(month=11, fmt="%Y%m%d"),
                        "rpyblCmpdInt": 0,
                        "termNo": "12",
                        "totalAmount": 28372,
                        "totalTerm": "12",
                        "unusedCouponAmount": 0,
                        "usedCouponAmount": 0
                    }
                ]
            }
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
