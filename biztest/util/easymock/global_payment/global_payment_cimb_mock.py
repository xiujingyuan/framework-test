from biztest.util.easymock.easymock import Easymock


class CimbMock(Easymock):
    def update_fk_userinfo(self, id_card_encrypt, full_name_encrypt, no_encrypt):
        api = "/tha/individual/getUserInfoByType"
        mode = {
            "msg": "success",
            "data": {
                "individual": {
                    "id_card": "11****052830*",
                    "id_card_encrypt": id_card_encrypt,
                    "full_name": "น*******************ง",
                    "full_name_encrypt": full_name_encrypt,
                    "email": "h*******f@yahoo.com",
                    "email_encrypt": "enc_04_4106517378224365568_767",
                    "phone": "0********0",
                    "phone_encrypt": "enc_01_3729739132709636096_329",
                    "birthday": "09/02/1990",
                    "gender": "female",
                    "address": "***/*** หมู่ที่ * ต.ท่าธง อ.บางบัวทอง จ.นนทบุรี",
                    "address_encrypt": "enc_06_3058548273310081024_351"
                },
                "bankCard": [
                    {
                        "uuid": "6621061000000005302",
                        "bank_code": "T00007",  # cimb 需要是022这个银行才能成功
                        "name_encrypt": full_name_encrypt,
                        "no": "5555****55",
                        "no_encrypt": no_encrypt,
                        "order": 1,
                        "bank_name": "KIA TN AKIN BANK PUBLIC COMPANY LIMITED",
                        "is_effectived": "Y",
                        "bank_name_thailand": "ธนาคารเกียรตินาคิน จ ากัด (มหาชน)"
                    }
                ]
            }
        }
        self.update(api, mode)
