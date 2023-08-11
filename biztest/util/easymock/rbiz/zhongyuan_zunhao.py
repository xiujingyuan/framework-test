# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayZhongyuanZunhaoMock(Easymock):
    # /zhongzhirong/zhongyuan_zunhao/repayTrial 中原樽昊还款试算
    # /zhongzhirong/zhongyuan_zunhao/repayApply 中原樽昊还款申请
    # /zhongzhirong/zhongyuan_zunhao/transQuery 中原樽昊还款结果查询

    def mock_zhongyuan_zunhao_repay_query_success(self, due_bill_no, withhold_serial_no, repay_amt=701025):
        # item_no 资产编号
        # withhold_serial_no 代扣序列号
        # paymentSeqNo channel key
        api = "/zhongzhirong/zhongyuan_zunhao/trans.query"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "listApproveInfo": [
                    {
                        "accountSeq": "Ck" + withhold_serial_no,
                        "amt": repay_amt,
                        "applCde": "691001202207161039205647327",
                        "applPk": get_guid(),
                        "applSeq": withhold_serial_no,
                        "applType": "ZDHK",
                        "applyAmt": repay_amt,
                        "applyDt": get_date(),
                        "apprvAmt": repay_amt,
                        "apprvDt": get_date(),
                        "autoDnInd": "",
                        "capitalRepayInt": 0,
                        "capitalRepayPrin": 0,
                        "contNo": "CTI69102022071668845370",
                        "cooppfApplCde": "691001_" + withhold_serial_no,
                        "endMark": "01",
                        "feeAmt": 0,
                        "loanNo": due_bill_no,
                        "otFeeAmt": 0,
                        "outSts": "99",
                        "payNo": "KP"+get_timestamp(),
                        "repayAmt": repay_amt,
                        "repayTime": get_date(),
                        "signDt": get_date(month=-6, fmt="%Y-%m-%d"),
                        "signEndDt": get_date(month=6, fmt="%Y-%m-%d")
                    }
                ]
            }
        }
        self.update(api, mode)

    def mock_zhongyuan_zunhao_repay_trial(self, prin_amt=700000, int_amt=1000):
        repay_amt = prin_amt + int_amt
        api = "/zhongzhirong/zhongyuan_zunhao/repay.trial"
        mode = {
            "code": 0,
            "message": "成功",
            "data": {
                "ppMinVal": repay_amt,
                "ppMaxVal": repay_amt,
                "ppXeVal": 5000000,
                "totalRepayAmt": repay_amt,
                "totalPlanamt": repay_amt,
                "totalPsPrcpAmt": prin_amt,
                "totalPsNormInt": int_amt,
                "totalPsOdIntAmt": 0,
                "totalAmortPrimeAmt": 0,
                "totalPsFeeAmt": 0,
                "penalFeeAmt": 0
            }
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
