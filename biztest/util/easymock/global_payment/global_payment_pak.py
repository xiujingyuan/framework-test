#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.util.easymock.easymock import Easymock


class PaymentPakMock(Easymock):
    def update_fk_user_info(self, account_type="wallet"):
        """
        :param account_type: wallet/account
        """
        api = "/pak/v1/biz/getUserInfo"
        if account_type == "wallet":
            mode = """{
              "code": 0,
              "data": {
                "bank_card_account_encrypt":"",
                "bank_card_bank_code":"EasyPaisa",
                "bank_card_bank_name":"",
                "bank_card_method_id":2,
                "email_encrypt":"enc_05_4167535104639901696_950",
                "father_name_encrypt":"",
                "gender":"male",
                "id_number_create_data":"20/12/2016",
                "id_number_encrypt":"enc_02_4167536021548310528_331",
                "name_encrypt":"enc_04_4106735563552858112_027",
                "bank_card_phone_encrypt":"enc_01_4388097415707112448_073",
                "phone_encrypt":"enc_01_4165716979233595392_332"
              },
              "msg": "success"
            }"""
        elif account_type == "account":
            mode = """{
              "code": 0,
              "data": {
                "bank_card_account_encrypt":"enc_03_4419301113825080320_006",
                "bank_card_bank_code":"MOD",
                "bank_card_bank_name":"Habib Bank Limited",
                "bank_card_method_id":1,
                "email_encrypt":"enc_05_4167535104639901696_950",
                "father_name_encrypt":"",
                "gender":"male",
                "id_number_create_data":"20/12/2016",
                "id_number_encrypt":"enc_02_4167536021548310528_331",
                "name_encrypt":"enc_04_4106735563552858112_027",
                "bank_card_phone_encrypt":"enc_01_4388097415707112448_073",
                "phone_encrypt":"enc_01_4165716979233595392_332"
              },
              "msg": "success"
            }"""
        self.update(api, mode)

    def update_fk_user_info_not_exist(self):
        api = "/pak/v1/biz/getUserInfo"
        mode = """{
            "code": 500800500,
            "data": null,
            "msg": "user info not found"
        }"""
        self.update(api, mode)

    def its_withhold_query_success(self, amount):
        api = "/its/gateway/payin/inquire"
        mode = """{
          "transaction": {
            "id": 1495,
            "orderId": "%s",
            "categoryName": "EWallet",
            "channelName": "EasyPaisa",
            "item": "10coins",
            "amount": %s,
            "msisdn": "03132249615",
            "email": "test@test.com",
            "cnic": "3520221175635",
            "transactionStatus": "success",
            "channelTransactionId": "22326019326",
            "createdDateTime": "2023-06-27T13:35:57.2266667",
            "consumerNumber": ""
          },
          "status": "success",
          "code": "0000",
          "message": "Transaction has been created successfully",
          "timestamp": "2023-06-27T08:35:57.226Z"
        }""" % ("MOCKITS1495", amount)
        self.update(api, mode)

    def its_withhold_query_processing(self):
        api = "/its/gateway/payin/inquire"
        mode = """{
          "transaction": {
            "id": 1495,
            "orderId": "MOCKITS1495",
            "categoryName": "EWallet",
            "channelName": "EasyPaisa",
            "item": "10coins",
            "amount": %s,
            "msisdn": "03132249615",
            "email": "test@test.com",
            "cnic": "3520221175635",
            "transactionStatus": "",
            "channelTransactionId": "22326019326",
            "createdDateTime": "2023-06-27T13:35:57.2266667",
            "consumerNumber": ""
          },
          "status": "success",
          "code": "0000",
          "message": "Transaction has been created successfully",
          "timestamp": "2023-06-27T08:35:57.226Z"
        }"""
        self.update(api, mode)

    def its_withhold_query_not_exist(self):
        api = "/its/gateway/payin/inquire"
        mode = """{
          "transaction": {
            "id": 1495,
            "orderId": "SW1495",
            "categoryName": "EWallet",
            "channelName": "EasyPaisa",
            "item": "10coins",
            "amount": 1,
            "msisdn": "03132249615",
            "email": "test@test.com",
            "cnic": "3520221175635",
            "transactionStatus": "success",
            "channelTransactionId": "22326019326",
            "createdDateTime": "2023-06-27T13:35:57.2266667",
            "consumerNumber": ""
          },
          "status": "success",
          "code": "0000",
          "message": "Transaction has been created successfully",
          "timestamp": "2023-06-27T08:35:57.226Z",
          "_res": {
            "status": 400,
            "data": {
              "transaction": null,
              "status": "failed",
              "code": "00012",
              "message": "Transaction Failed: Record not found!!!",
              "timestamp": "2023-06-29T09:00:15.205Z"
            },
            "cookies": {
              "test": "true"
            },
            "headers": {
              "Power": "easy-mock"
            }
          }
        }"""
        self.update(api, mode)
