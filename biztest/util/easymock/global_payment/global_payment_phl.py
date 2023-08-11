#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_date


class PaymentPhlMock(Easymock):
    def update_fk_user_info(self, account_type="wallet"):
        """
        :param account_type: wallet/account
        """
        api = "/phl/v1/biz/getUserInfo"
        if account_type == "wallet":
            mode = """{
              "code": 0,
              "data": {
                "accountNoEncrypt": "enc_01_4451542423831065600_136",
                "bankCardCode": "Paymaya",
                "bankCardMethod": 2,
                "birthday": "09/14/1969",
                "civilStatusId": 0,
                "fullnameEncrypt": "enc_04_4451541090847699968_173",
                "gender": "female",
                "idType": "PhiHealth",
                "idcardPicUrl": "https://dxcloud-sg-ph-prod.oss-ap-southeast-1.aliyuncs.com/cnRkalpra1VMVjlR20230421",
                "identificationIdEncrypt": "enc_02_4451543285928309760_200",
                "identificationTypeId": 6,
                "locationEncrypt": "enc_06_4451542138786165760_880",
                "motherMaidenNameEncrypt": "",
                "phoneEncrypt": "enc_01_4451542423831065600_136"
              },
              "msg": "success"
            }"""
        elif account_type == "account":
            mode = """{
                "code": 0,
                "data": {
                    "accountNoEncrypt": "enc_03_4451556541975770112_845",
                    "bankCardCode": "BDO",
                    "bankCardMethod": 1,
                    "birthday": "12/12/1988",
                    "civilStatusId": 0,
                    "fullnameEncrypt": "enc_04_4451543540790998016_826",
                    "gender": "female",
                    "idType": "TIN（Taxpayer Identification Number）",
                    "idcardPicUrl": "https://dxcloud-sg-ph-prod.oss-ap-southeast-1.aliyuncs.com/Um56V3AxaUpKcm1y20230312?Expires=1678617266&OSSAccessKeyId=LTAI5tByrRWsYKgtHrqMNS5j&Signature=adZ1IAQVprCGP7uwd0%2BXrloCG30%3D",
                    "identificationIdEncrypt": "enc_02_4451543285928309760_200",
                    "identificationTypeId": 2,
                    "locationEncrypt": "enc_06_4451543031468274688_294",
                    "motherMaidenNameEncrypt": "",
                    "phoneEncrypt": "enc_01_4451542769307497472_276"
                },
                "msg": "success"
            }"""
        self.update(api, mode)

    def update_fk_user_info_not_exist(self):
        api = "/phl/v1/biz/getUserInfo"
        mode = """{
            "code": 500800500,
            "data": null,
            "msg": "user info not found"
        }"""
        self.update(api, mode)

    def update_paycools_paycode_apply_success(self):
        api = "/paycools/api/v1/paymentCode"
        mode = """{
          "code": 1000,
          "message": "success",
          "data": {
            "mchOrderId": function({
              _req
            }) {
              return _req.body.mchOrderId
            },
            "channelCode": "GCASH_STATIC_VA",
            "guideUrl": "https://api-uat.paycools.com/repayment/static/guide/MmdhZ2xubnBYZ0x3UTVJbkF3aVVLZUlQZFFNSmM2MS9EV3dmWTBlYWVqND0=",
            "referenceNumber2": "PC@id",
            "biller": "PayCools Loan"
          },
          "_res": {
            "status": 200,
            "data": {
              "success": false
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

    def update_paycools_paycode_query_success(self, amount):
        api = "paycools/api/v1/paymentCode/:d/payments"
        mode = """{
          "code": 1000,
          "message": "success",
          "data": [{
            "transactionId": "C1184676427538247215",
            "transactionCreateTime": "2023-02-15 10:18:58",
            "transactionReturnTime": "%s",
            "transactionAmount": %s,
            "channelCode": "7ELEVEN_STATIC_VA",
            "transactionStatus": "COMPLETE", // PENDING、COMPLETE、FAIL
            "remark": null
          }]
        }""" % (get_date(), amount)
        self.update(api, mode)

    def update_paycools_qrcode_apply_success(self):
        api = "/paycools/api/v1/qrcode"
        mode = """{
          "code": 1000,
          "message": "success",
          "data": {
            "mchOrderId": function({
              _req
            }) {
              return _req.body.mchOrderId
            },
            "qrcodeId": "QR@id",
            "qrcodeContent": "00020101021128760011ph.ppmi.p2m0111OPDVPHM1XXX03157771480000000170416529481372394710105030005204601653036085802PH5908PayCools6015City Of Mandalu62310010ph.allbank05062110000803***88310012ph.ppmi.qrph0111OPDVPHM1XXX6304B442",
            "channelCode": "QRPH_HYBRID_QR",
            "status": "ACTIVE",
            "qrLink": "https://a.api-uat.paycools.com/1L9zPnY"
          }
        }"""
        self.update(api, mode)

    def update_paycools_ebank_apply_success(self):
        api = "/paycools/api/v1/qrcode"
        mode = """{
          "code": 1000,
          "message": "success",
          "data": {
            "redirectUrl": "https://a.api-uat.paycools.com/1L9zPp3",
            "transactionStatus": "PENDING",
            "transactionId": "C1184676617337849478"
          }
        }"""
        self.update(api, mode)

    def update_paycools_create_account_success(self, ):
        api = "paycools/api/v1/batch/paymentAccount"
        mode = """{
          "code": 1000,
          "message": "success",
          "data": {
            "paymentAccountList": [{
              "mchOrderId": function({_req}) {return _req.body.mchOrderId},
              "channelCode": "INSTA_TRANSFER_ACC",
              "guideUrl": "https://api-uat.paycools.com/transfer/static/guide/NzFhU1NWR3dIWkIyNklKTmlpRW1YdGg1d3ZIMG50dzVzaWxiYURmMXFsdz0=",
              "receivingBank": "AllBank",
              "accountName": "PayCools",
              "accountNumber": "999000010998"
            }],
            "shortLink": "https://a.api-uat.paycools.com/1L9zPoV"
          }
        }"""
        self.update(api, mode)
