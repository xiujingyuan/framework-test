# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayLongjiangMock(Easymock):
    """
    龙江大秦 还款mock
    """
    def update_repayment_calculate(self, principal=1355.02, interest=8.19):
        total_amount = int(principal) + int(interest)
        api = "/longjiang/std/repayment/calculate"
        mode = '''{
          "code": 0,
          "message": "成功",
          "data": {
            "assets": [{
              "principal": %s,
              "penalty_interest": "50.00",
              "asset_item_no": function({
                _req
              }) {
                return _req.body.assets[0].asset_item_no
              },
              "total_amount": %s,
              "interest": %s,
              "extend_interest": "0.00",
              "loan_order_no": function({
                _req
              }) {
                return _req.body.assets[0].loan_order_no
              },
              "compensate": "0.00"
            }]
          }
        }''' % (principal, total_amount, interest)
        self.update(api, mode)


if __name__ == "__main__":
    pass
