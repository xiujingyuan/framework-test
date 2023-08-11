# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayWeishenmaMock(Easymock):
    def update_active_repay_query(self, pay_status="1", amount="400120"):
        api = "/weishenma_daxinganling/pre-loan/activeRepayQuery"
        mode = '''[{
          "state": "success",
          "code": "",
          "shddh": function({
            _req
          }) {
            return _req.body.shddh_array[0].shddh
          },
          "period_seq": 2,
          "start_date": "@now",
          "end_date": "@now",
          "dk_flag": "%s",
          "dk_amt": "%s",
          "dk_info": "dsfs史蒂夫",
          "repay_remark": function({
            _req
          }) {
            return _req.body.shddh_array[0].repayBehaviorNo
          },
          "serial_number": "@id"
        }]''' % (pay_status, amount)
        self.update(api, mode)

    def update_active_settle_trail(self, rest_principal=400000, total_amount=400120):
        api = "/weishenma_daxinganling/pre-loan/repayTrial"
        mode = '''{
          "state": "success",
          "code": "1002",
          "msg": "查询成功！",
          "shddh": function({
            _req
          }) {
            return _req.body.shddh
          },
          "rest_principal": %s,
          "total_amount": %s
        }''' % (rest_principal, total_amount)
        self.update(api, mode)

    def early_settle_apply_success(self, asset_due_bill_no, asset_period):
        api = "/weishenma_daxinganling/pre-loan/earlySettle"
        state = "success"
        check_point = {
            "path": self.path_prefix + api,
            "body": {
                "shddh": "{}".format(asset_due_bill_no),
                "repay_issue": asset_period
            }
        }
        mode = '''{
                      "state": %s,
                      "error_code": "",
                      "shddh": "%s",

                    }''' % (self.get_mock_result_with_check(state, check_point), asset_due_bill_no)
        self.update(api, mode)

    def active_repay_apply_success(self, asset_due_bill_no, asset_period):
        api = "/weishenma_daxinganling/pre-loan/activeRepay"
        state = "success"
        check_point = {
            "path": self.path_prefix + api,
            "body": {
                "shddh": "{}".format(asset_due_bill_no),
                "repay_qx": "{}".format(asset_period)
            }
        }
        mode = '''{
              "state": %s,
              "error_code": "",
              "shddh": "%s",

            }''' % (self.get_mock_result_with_check(state, check_point), asset_due_bill_no)
        self.update(api, mode)
