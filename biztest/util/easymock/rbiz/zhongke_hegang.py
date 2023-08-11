# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayZhongkeHegangMock(Easymock):

    def mock_hegang_repay_query_1000(self, resp_code="1000"):
        api = "/hegang/repayQuery/KN1-CL-HLJ"
        mode = {
            "respCode": resp_code,
            "respMesg": "查无此交易",
            "transDate": get_date(fmt="%Y-%m-%d"),
            "transTime": "18:49:51"
        }
        self.update(api, mode)

    def mock_hegang_repay_query(self, resp_code="9000", result_code="SUCCESS", rpy_status="00", int_amt=44.67,
                                prin_amt=646.44):
        api = "/hegang/repayQuery/KN1-CL-HLJ"
        total = int_amt + prin_amt
        mode = {
            "intAmt": int_amt,
            "ointAmt": 0,
            "prinAmt": prin_amt,
            "respCode": resp_code,
            "respMesg": "自动化测试repayQuery",
            "resultCode": result_code,
            "rpyDate": get_date(fmt="%Y-%m-%d"),
            "rpyDesc": "",
            "rpyStatus": rpy_status,
            "rpyTotalAmt": total,
            "transDate": get_date(fmt="%Y-%m-%d"),
            "transTime": "15:00:55"
        }
        self.update(api, mode)

    def mock_hegang_repay_apply(self, resp_code="0000"):
        api = "/hegang/repayApply/KN1-CL-HLJ"
        mode = {
            "respCode": resp_code,
            "respMesg": "自动化测试repayApply",
            "transDate": get_date(fmt="%Y-%m-%d"),
            "transTime": "14:09:47"
        }
        self.update(api, mode)

    def mock_hegang_repay_trail(self, resp_code="0000"):
        api = "/hegang/preRepayApplyCalc/KN1-CL-HLJ"
        mode = {
            "respCode": resp_code,
            "respMesg": "自动化测试preRepayApplyCalc",
            "transDate": get_date(fmt="%Y-%m-%d"),
            "transTime": "13:34:47"
        }
        self.update(api, mode)

    def mock_hegang_repay_trail_query(self, resp_code="9999", int_amt=10, prin_amt=8000):
        api = "/hegang/repayTrialQuery/KN1-CL-HLJ"
        total = int_amt + prin_amt
        mode = {
            "respCode": resp_code,
            "respMesg": "自动化测试repaymentTrialQuery",
            "tradeAmt": total,
            "tradeCapital": prin_amt,
            "tradeDate": get_date(fmt="%Y-%m-%d"),
            "tradeInt": int_amt,
            "tradeOInt": 0,
            "transDate": get_date(fmt="%Y-%m-%d"),
            "transTime": "14:45:30"
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
