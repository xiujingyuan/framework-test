#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.util.easymock.easymock import Easymock


class PaymentThaMock(Easymock):
    def update_fk_user_info(self, account_type="account"):
        """
        :param account_type: wallet/account
        """
        api = "/tha/individual/getUserInfoByType"
        if account_type == "account":
            mode = """{
              "msg": "success",
              "data": {
                "individual": {
                  "id_card": "11****052830*",
                  "id_card_encrypt": "enc_04_4106516400884424704_297", //1100200528308
                  "full_name": "น*******************ง",
                  "full_name_encrypt": "enc_04_4106516688211025920_279",
                  "email": "h*******f@yahoo.com",
                  "email_encrypt": "enc_04_4106517378224365568_767",
                  "phone": "0********0",
                  "phone_encrypt": "enc_04_4106517663940354048_372",
                  "birthday": "09/02/1990",
                  "gender": "female",
                  "address": "***/*** หมู่ที่ * ต.ท่าธง อ.บางบัวทอง จ.นนทบุรี",
                  "address_encrypt": "enc_04_4106517921000857600_351"
                },
                "bankCard": [{
                  "uuid": "6621061000000005302",
                  "bank_code": "022",
                  "name_encrypt": "enc_04_4106519038396997632_140",
                  "no": "5555****55",
                  "no_encrypt": "enc_04_4106518877084065792_059", // 8000260785
                  // "no_encrypt": "enc_06_3058548273310081024_351",
                  "order": 1,
                  "bank_name": "CIMB",
                  "is_effectived": "Y",
                  "bank_name_thailand": "ธนาคารเกียรตินาคิน จ ากัด (มหาชน)"
                }]
              }
            }"""
        self.update(api, mode)

    def update_fk_user_info_not_exist(self):
        api = "/tha/individual/getUserInfoByType"
        mode = """{
            "code": 500800500,
            "data": null,
            "msg": "user info not found"
        }"""
        self.update(api, mode)
