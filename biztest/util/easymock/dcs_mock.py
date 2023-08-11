from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_date, get_guid


class DcsMock(Easymock):
    # 代付结果查询
    def update_payment_withdraw_query(self, code=0, status=2, trade_no=''):
        api = "/withdraw/query"
        mode = {
          "code": code,
          "message": "交易完成",
          "data": {
            "account": "qsq_cpcn_tq_quick",
            "amount": 10000,
            "state": status,
            "channel_code": "2000",
            "channel_msg": "OK.",
            "code": "E20000",
            "msg": "交易成功",
            "error_code": None,
            "channel_message": "OK.",
            "channel_key": "@id",
            "created_at": "@now",
            "finished_at": "@now",
            "receiver_type": 1,
            "receiver_name_encrypt": "enc_04_3011130_556",
            "receiver_account_encrypt": "enc_03_3636618672048965632_491",
            "receiver_identity_encrypt": "enc_02_3636618673659578368_981",
            "receiver_bankcode": "BOC",
            "withdraw_receipt_list": [{
              "status": status,
              "channel_name": "qsq_cpcn_tq_quick",
              "channel_key": trade_no,
              "channel_resp_code": "2000",
              "channel_resp_message": "OK.",
              "finished_at": get_date(),
              "trade_no": trade_no
            }]
          }
        }
        self.update(api, mode)

    # 代付结果查询返回交易不存在
    def update_payment_withdraw_query_notexsit(self):
        api = "/withdraw/query"
        mode = {
            "code": 3,
            "message": "交易不存在",
            "data": None
        }
        self.update(api, mode)

    # dcs充值请求支付易宝备注获取
    def update_payment_withhold_recharge_success(self, code=0, remit_comment=""):
        api = "/withhold/recharge"
        mode = {
            "code": code,
            "message": "交易完成",
            "data": {
                "remit_comment": remit_comment,
                "amount": 1111,
                "channel_key": "channel_key_2022",
                "channel_code": "E20002",
                "channel_msg": "OK.",
                "created_at": get_date(),
                "finished_at": get_date()
            }
        }
        self.update(api, mode)


