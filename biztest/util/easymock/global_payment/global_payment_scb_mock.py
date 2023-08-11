
from biztest.util.easymock.easymock import Easymock


class ScbMock(Easymock):
    # 用户中心mock
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

    # 获取token mock
    def update_gettoken(self, status):
        api = "/partners/v1/oauth/token"
        if status == "success":
            mode = {
                "status ": {
                    "code": 1000,
                    "description": "Success"
                },
                "data": {
                    "accessToken": "16659ae7-84c6-4125-8442-f6659c5ce02c",
                    "tokenType": "Bearer",
                    "expiresIn": 3600,
                    "expiresAt": 1530544107
                }
            }
        else:
            mode = {
                "status ": {
                    "code": 9700,
                    "description": "Generic Business Error"
                }
            }
        self.update(api, mode)

    # 验证付款信息并创建订单
    def update_withdraw_initiate(self, status):
        api = "/partners/v2/payment/transfer/credit/initiate"
        if status == "success":
            mode = {
                "status": {
                    "code": 1000,
                    "description": "Success"
                },
                "data": [{
                    "tokenizerId": "D014917201627108",
                    "transactionDateTime": "2021-06-09T14:49:38.754+07:00",
                    "customerRefNum": "123456789012345678901234567890"
                }]
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            mode = {
                "status": {
                    "code": 401,
                    "description": "FAILED"
                },
                "data": [{
                    "tokenizerId": "D014917201627108",
                    "transactionDateTime": "2021-06-09T14:49:38.754+07:00",
                    "customerRefNum": "123456789012345678901234567890"
                }]
            }
        self.update(api, mode)

    # 如果Confirm返回异常，可通过此接口查询订单状态
    def update_withdraw_inquiry(self, status):
        api = "/partners/v1/payment/transfer/inquiry"
        if status == "success":
            mode = {
                "status": {
                    "code": 1000,
                    "description": "Success"
                },
                "data": [{
                    "paymentInformation": [{
                        "originalPaymentInformationAndStatus": [{
                            "transactionInformation": {
                                "transactionStatus": "ACCC",  # ACCC是成功，PDNG是处理中需要调用确认接口
                                "errorCode": "000",
                                "errorDescription": "Success",
                                "businessTransactionReference": "1234567890"
                            }
                        }]
                    }]
                }]
            }
        elif status == "process":
            mode = {
                "status": {
                    "code": 1000,
                    "description": "Success"
                },
                "data": [{
                    "paymentInformation": [{
                        "originalPaymentInformationAndStatus": [{
                            "transactionInformation": {
                                "transactionStatus": "PDNG",  # ACCC是成功，PDNG是处理中需要调用确认接口
                                "errorCode": "000",
                                "errorDescription": "Success",
                                "businessTransactionReference": "1234567890"
                            }
                        }]
                    }]
                }]
            }
        elif status == "fail":
            mode = {
                "status": {
                    "code": 1000,
                    "description": "Success"
                },
                "data": [{
                    "paymentInformation": [{
                        "originalPaymentInformationAndStatus": [{
                            "transactionInformation": {
                                "transactionStatus": "RJCT",  # ACCC是成功，PDNG是处理中需要调用确认接口
                                "errorCode": "001",
                                "errorDescription": "RJCT fail",
                                "businessTransactionReference": "1234567890"
                            }
                        }]
                    }]
                }]
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    # 确认放款结果，返回成功则代表放款成功
    def update_withdraw_confirm(self, status):
        api = "/partners/v2/payment/transfer/confirm"
        if status == "success":
            mode = {
                "status": {
                    "code": 1000,
                    "description": "Success"
                },
                "data": [{
                    "tokenizerId": "D014917201627108",
                    "transactionDateTime": "2021-09-17T14:49:42.489+07:00"
                }]
            }
        else:
            pass
        self.update(api, mode)

    def update_scb_sdk_token_generate_success(self):
        api = "/v1/oauth/token"
        mode = {
            "status": {
                "code": 1000,
                "description": "Success"
            },
            "data": {
                "accessToken": "34362373-66e8-4db0-80e5-0755b67e51f9",
                "tokenType": "Bearer",
                "expiresIn": 1800,
                "expiresAt": 1550133185,
                "refreshToken": "9e80be84-5eb7-4e8c-a885-a36ff3eb6684",
                "refreshExpiresIn": 3600,
                "refreshExpiresAt": 1550134985
            }
        }
        self.update(api, mode)

    def update_scb_sdk_token_generate_failed(self):
        api = "/v1/oauth/token"
        mode = {
            "status": {
                "code": 9300,
                "description": "Invalid authorization method for current credentials"
            },
            "data": None
        }
        self.update(api, mode)

    def update_scb_sdk_generate_success(self):
        api = "/v3/deeplink/transactions"
        mode = {
            "status": {
                "code": 1000,
                "description": "Deeplink successfully created"
            },
            "data": {
                "transactionId": "2143a72e-46b4-44a6-ad5e-1e2e8a6cc1f9",
                "deeplinkUrl": "scbeasysim://purchase/2143a72e-46b4-44a6-ad5e-1e2e8a6cc1f9",
                "userRefId": "l765674b1b4d664bdfae7f260db219e2f1"
            }
        }
        self.update(api, mode)

    def update_scb_sdk_generate_failed(self):
        api = "/v3/deeplink/transactions"
        mode = {
            "status": {
                "code": 4101,
                "description": "The feature is not supported"
            },
            "data": None
        }
        self.update(api, mode)

    def update_scb_sdk_generate_service_error(self):
        api = "/v3/deeplink/transactions"
        mode = {
            "status": {
                "code": 500,
                "description": "service error"
            }
        }
        self.update(api, mode)

    def update_scb_sdk_query_service_error(self):
        """statusCode = "500" => service error"""
        transaction_id = "2143a72e-46b4-44a6-ad5e-1e2e8a6cc1f9"
        api = "/v2/transactions/%s" % transaction_id
        mode = {
            "status": {
                "code": 500,
                "description": "service error"
            }
        }
        self.update(api, mode)

    def update_scb_sdk_query_success(self):
        """statusCode = "1" => paid"""
        transaction_id = "2143a72e-46b4-44a6-ad5e-1e2e8a6cc1f9"
        api = "/v2/transactions/%s" % transaction_id
        mode = {
            "status": {
                "code": 1000,
                "description": "Success"
            },
            "data": {
                "partnerId": "l7c73ac7f144fb4d22ac15371d9ba34666",
                "transactionMethod": "BP",
                "updatedTimestamp": "2021-01-15T09:05:58+07:00",
                "fee": 0,
                "statusCode": 1,
                "transactionSubType": [
                    "BP"
                ],
                "userRefId": "l7c73ac7f144fb4d22ac15371d9ba34666",
                "sessionValidityPeriod": 300,
                "transactionId": transaction_id,
                "transactionType": "PURCHASE",
                "billPayment": {
                    "receiverBankCode": "014",
                    "senderAccountValue": "8843410001",
                    "receiverAccountType": "BANKAC",
                    "receiverName": "biller name with len 25ha",
                    "senderProxyValue": "8843410001",
                    "receiverAccountValue": "0987654321",
                    "ref2": "161035588610220",
                    "senderBankCode": "014",
                    "ref1": "161035588610220",
                    "receiverProxyValue": "137613415414240",
                    "paymentAmount": 39,
                    "accountFrom": "8843410001",
                    "senderAccountType": "BANKAC",
                    "accountTo": "137613415414240",
                    "senderName": "Jasmine Golubeva",
                    "receiverProxyType": "BILLERID",
                    "ref3": "161035588610220",
                    "countryCode": "EN",
                    "senderProxyType": "ACCOUNT",
                    "currency": "764"
                },
                "partnerName": "AforT No.1",
                "errorMessage": None,
                "merchantMetaData": {
                    "merchantInfo": {
                        "name": "KNKNT"
                    },
                    "deeplinkUrl": "scbeasysim://purchase/f1a65e5b-1579-4777-aa72-a1483ccad9ce",
                    "callbackUrl": "http://cn.bing.com"
                },
                "paidAmount": 39,
                "accountFrom": "8843410001",
                "createdTimestamp": "2021-01-15T09:05:14+07:00"
            }
        }
        self.update(api, mode)

    def update_scb_sdk_query_pending(self):
        """
        statusCode = 0 => pending
        """
        transaction_id = "2143a72e-46b4-44a6-ad5e-1e2e8a6cc1f9"
        api = "/v2/transactions/%s" % transaction_id
        mode = {
            "status": {
                "code": 1000,
                "description": "Success"
            },
            "data": {
                "partnerId": "l7c73ac7f144fb4d22ac15371d9ba34666",
                "transactionMethod": None,
                "updatedTimestamp": "2021-01-17T09:34:30+07:00",
                "statusCode": 0,
                "transactionSubType": [
                    "BP"
                ],
                "userRefId": "l7c73ac7f144fb4d22ac15371d9ba34666",
                "transactionId": transaction_id,
                "transactionType": "PURCHASE",
                "sessionValidityPeriod": 300,
                "billPayment": {
                    "accountTo": "137613415414240",
                    "ref2": " 161035588610235",
                    "ref1": "161035588610235",
                    "paymentAmount": 39,
                    "ref3": "161035588610235",
                    "accountFrom": None
                },
                "partnerName": "AforT No.1",
                "errorMessage": None,
                "merchantMetaData": {
                    "merchantInfo": {
                        "name": "KNKNT"
                    },
                    "deeplinkUrl": "scbeasysim://purchase/936bedd9-50c6-4102-980f-c7acf7e94e51",
                    "callbackUrl": "http://cn.bing.com"
                },
                "paidAmount": 0,
                "createdTimestamp": "2021-01-17T09:34:30+07:00",
                "accountFrom": None
            }
        }
        self.update(api, mode)

    def update_scb_sdk_query_expired(self):
        """statusCode = 5 => expired"""
        transaction_id = "2143a72e-46b4-44a6-ad5e-1e2e8a6cc1f9"
        api = "/v2/transactions/%s" % transaction_id
        mode = {
            "status": {
                "code": 1000,
                "description": "Success"
            },
            "data": {
                "partnerId": "l765674b1b4d664bdfae7f260db219e2f1",
                "transactionMethod": None,
                "updatedTimestamp": "2021-01-13T15:33:11+07:00",
                "creditCardFullAmount": {
                    "orderReference": "000000000000002",
                    "terminalId": "589432760047346",
                    "paymentAmount": 700,
                    "merchantId": "915815844712810"
                },
                "statusCode": 5,
                "transactionSubType": [
                    "BP"
                ],
                "userRefId": "l765674b1b4d664bdfae7f260db219e2f1",
                "sessionValidityPeriod": 300,
                "transactionId": transaction_id,
                "transactionType": "PURCHASE",
                "billPayment": {
                    "accountTo": "851737440782289",
                    "ref2": "000000000000002",
                    "ref1": "000000000000002",
                    "paymentAmount": 700,
                    "ref3": "000000000000002",
                    "accountFrom": None
                },
                "partnerName": "My Test App",
                "errorMessage": None,
                "merchantMetaData": {
                    "merchantInfo": {
                        "name": "KN TEST ENV"
                    },
                    "deeplinkUrl": "scbeasysim://purchase/2143a72e-46b4-44a6-ad5e-1e2e8a6cc1f9",
                    "callbackUrl": "http://cn.bing.com"
                },
                "paidAmount": 0,
                "accountFrom": None,
                "createdTimestamp": "2021-01-13T15:27:09+07:00"
            }
        }
        self.update(api, mode)

if __name__ == "__main__":
    pass
