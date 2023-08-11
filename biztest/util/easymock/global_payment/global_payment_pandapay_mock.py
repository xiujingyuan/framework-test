
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_random_num


class PandapayMock(Easymock):
    # 用户中心mock
    def update_fk_userinfo(self, id_card_encrypt, full_name_encrypt, no_encrypt):
        api = "/mex/v1/biz/getUserInfo"
        mode = {
            "code": 0,
            "msg": "success",
            "data": {
              "first_name_encrypt": full_name_encrypt,
              "middle_name_encrypt": "enc_04_3544198766255415296_112",
              "last_name_encrypt": "enc_04_3544199020899999744_459",
              "phone_encrypt": "enc_01_3544199284587503616_376",
              "email_encrypt": "enc_05_3544199525894201344_146",
              "bank_card_bank_code": 40012,
              "bank_card_account_no_encrypt": no_encrypt,
              "bank_card_card_type": "1",
              "id_card_number_encrypt": id_card_encrypt
            }
        }
        self.update(api, mode)

    # 下单
    def update_withdraw_createPay(self, status):
        api = "/api/pay/createPay"
        if status == "success":
            mode = {
                "transactionId": "c63f84a7f26a43bbb9719cba334b0d0d",
                "resultado": {
                    "id": int(get_random_num()[:6])
                }
            }
        elif status == "fail": # 账户有问题
            mode = {
                "transactionId": "c63f84a7f26a43bbb9719cba334b0d0d",
                "resultado": {
                    "descripcionError": "El tipo de cuenta 3 es invalido",
                    "id": -11
                }
            }
        elif status == "no_enough":  # 余额不足
            mode = {
                "transactionId": "c63f84a7f26a43bbb9719cba334b0d0d",
                "resultado": {
                    "descripcionError": "Insufficient partner balance",
                    "id": -1
                }
            }
        elif status == "maximum":  # 限流
            mode = {
                "resultado": {
                    "id": -403,
                    "descripcionError": "Maximum request limit"
                }
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            mode = {}
        self.update(api, mode)

    # 查询
    def update_withdraw_getPay(self, channel_key, status):
        api = "/api/pay/getPay"
        if status == "success":
            mode = {
                "resultado": {
                    "result": {
                        "estado": "Success",
                        "folioOrigen": channel_key,
                        "id": int(get_random_num()[:6]),
                        "empresa": "TRANSFER_TO"
                    }
                }
            }
        elif status == "refund":
            mode = {
                "resultado": {
                    "result": {
                        "estado": "Refund",
                        "folioOrigen": channel_key,
                        "id": int(get_random_num()[:6]),
                        "empresa": "TRANSFER_TO"
                    }
                }
            }
        elif status == "cancel":
            mode = {
                "resultado": {
                    "result": {
                        "estado": "Cancel",
                        "folioOrigen": channel_key,
                        "id": int(get_random_num()[:6]),
                        "empresa": "TRANSFER_TO"
                    }
                }
            }
        elif status == "not_exit":  # 订单不存在
            mode = {
                "resultado": {
                    "id": -1,
                    "descripcionError": "Invalid id or claveRastreo"
                }
            }
        elif status == "fail":  # 订单失败
            mode = {
                "resultado": {
                    "result": {
                        "estado": "Fail",
                        "folioOrigen": channel_key,
                        "id": "-1",
                        "empresa": "TRANSFER_TO"
                    }
                }
            }
        elif status == "process":  # 订单处理中
            mode = {
                "resultado": {
                    "result": {
                        "estado": "",
                        "folioOrigen": channel_key,
                        "id": "",
                        "empresa": "TRANSFER_TO"
                    }
                }
            }
        elif status == "maximum":  # 限流
            mode = {
                "resultado": {
                    "id": -403,
                    "descripcionError": "Maximum request limit"
                }
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            mode = {}
        self.update(api, mode)


