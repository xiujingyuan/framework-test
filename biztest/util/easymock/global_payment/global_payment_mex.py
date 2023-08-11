#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.util.easymock.easymock import Easymock


class PaymentMexMock(Easymock):
    def update_fk_user_info(self, account_type="account"):
        """
        :param account_type: wallet/account
        """
        api = "/mex/v1/biz/getUserInfo"
        if account_type == "account":
            mode = """{
                "code": 0,
                "data": {
                    "bank_card_account_no_encrypt": "enc_03_4453123900314235904_998",
                    "bank_card_bank_code": 40012,
                    "bank_card_card_type": 1,
                    "email_encrypt": "enc_05_4453124338333791232_624",
                    "first_name_encrypt": "enc_04_3504800177758668800_996",
                    "id_card_number_encrypt": "enc_02_4453124800277656576_368",
                    "last_name_encrypt": "enc_04_4453125062253884416_893",
                    "middle_name_encrypt": "enc_04_4453125062304216064_194",
                    "phone_encrypt": "enc_01_4453125666367878144_444"
                },
                "msg": "success"
            }"""
        self.update(api, mode)

    def update_fk_user_info_not_exist(self):
        api = "/mex/v1/biz/getUserInfo"
        mode = """{
            "code": 500800500,
            "data": null,
            "msg": "user info not found"
        }"""
        self.update(api, mode)
