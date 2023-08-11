from biztest.util.easymock.easymock import Easymock


class RepayQinnongMock(Easymock):
    def update_repay_trail(self, pre_principal=735683, pre_interest=100):
        api = "/qinnong/std/repayment/calculate"
        total_amount = int(pre_principal) + int(pre_interest)
        mode = '''{
              "code": 0,
              "message": "success",
              "data": {
                "assets": [{
                  "total_amount": %s,
                  "compensate": 0,
                  "principal": %s,
                  "interest": %s,
                  "extend_interest": 0,
                  "penalty_interest": 0,
                  "asset_item_no": function({
                    _req
                  }) {
                    return _req.body.assets[0].asset_item_no
                  },
                  "loan_order_no": function({
                    _req
                  }) {
                    return _req.body.assets[0].loan_order_no
                  }
                }],
                "__v": 1598249388.570562
              }
            }''' % (total_amount, pre_principal, pre_interest)
        self.update(api, mode)
