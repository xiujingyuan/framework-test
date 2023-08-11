# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayYilianDingfengMock(Easymock):

    def mock_yilian_dingfeng_repay_trial(self, loan_no, send_code="0000", send_flag="01", int_amt=10, prin_amt=519.62,
                                         fee_amt=29.26):
        api = "/qingjia/yilian_dingfeng/repayTrial"
        total = int_amt + prin_amt + fee_amt
        mode = {
            "code": 0,
            "message": "",
            "data": {
                "channel": "KN10001",
                "sendflag": send_flag,
                "sendcode": send_code,
                "sendmsg": "自动化测试repayTrial",
                "loanno": loan_no,
                "repaytotal": str(total),
                "repaycapital": str(prin_amt),
                "repayinterest": str(int_amt),
                "repayguarantFee": str(fee_amt),
                "repaydeductFee": "0",
                "repayamerce": "0.00",
                "repayforfeit": "",
                "indeedpenalbond": "",
                "reqSuccess": True,
                "bizSuccess": True,
                "trancode": "QLZS000000102",
                "transerno": "KN10001"+loan_no,
                "respdate": get_date(fmt="%Y%m%d"),
                "resptime": "160144",
                "transtate": "S",
                "errocode": "000000",
                "errormsg": "请求成功"
            }
        }

        # "sendflag": "00:处理中;01:处理成功;02:处理失败"
        self.update(api, mode)

    def mock_yilian_dingfeng_settle_repay_notice(self, tran_code, tran_sn, send_code="9999", send_flag="01",
                                                 tran_state="S"):
        api = "/qingjia/yilian_dingfeng/settleRepayNotice"
        mode = {
            "code": 0,
            "message": "",
            "data": {
                "channel": "KN10001",
                "sendflag": send_flag,
                "sendmsg": "自动化测试settleRepayNotice",
                "sendcode": send_code,
                "reqSuccess": False,
                "bizSuccess": False,
                "trancode": tran_code,
                "transerno": tran_sn,
                "respdate": get_date(fmt="%Y%m%d"),
                "resptime": "164503",
                "transtate": tran_state,
                "errocode": "800117",
                "errormsg": "请求成功"
            }
        }
        self.update(api, mode)

    def mock_yilian_dingfeng_normal_repay_notice(self, tran_code, tran_sn, send_code="9999", send_flag="01",
                                                 tran_state="S"):
        api = "/qingjia/yilian_dingfeng/normalRepayNotice"
        mode = {
            "code": 0,
            "message": "",
            "data": {
                "channel": "KN10001",
                "sendflag": send_flag,
                "sendmsg": "自动化测试normalRepayNotice",
                "sendcode": send_code,
                "reqSuccess": False,
                "bizSuccess": False,
                "trancode": tran_code,
                "transerno": tran_sn,
                "respdate": get_date(fmt="%Y%m%d"),
                "resptime": "164503",
                "transtate": tran_state,
                "errocode": "800117",
                "errormsg": "请求成功"
            }
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
