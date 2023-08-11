from biztest.config.payment.url_config import gbpay_resp_transfer_mode, global_amount
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_date


class GbpayMock(Easymock):
    # 用户中心mock
    def update_fk_userinfo(self, id_card_encrypt, full_name_encrypt, no_encrypt, bank_code="022", card_uuid="6622092000001290502"):
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
                    "address_encrypt": "enc_04_4106517921000857600_351"
                },
                "bankCard": [
                    {
                        "uuid": card_uuid, #"6621061000000005302"
                        "bank_code": bank_code,
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

    # 余额查询（充足／余额不足／500）
    def update_withdraw_balance(self, status):
        api = "/withdraw/balance/v2/transfers"
        if status == "enough":
            mode = {"netAuthorize": 0.00, "netBalance": 363761.7698, "resultCode": "00", "resultMessage": "Success",
                    "authorize": 0}
        elif status == "no_enough":
            mode = {"netAuthorize": 0.00, "netBalance": 0.7698, "resultCode": "00", "resultMessage": "Success",
                    "authorize": 0}
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    # 代付下单（下单成功／下单失败／重复下单／500）
    def update_withdraw(self, status):
        api = "/withdraw/v2/transfers"
        if status == "success":
            mode = {
                "date": get_date(fmt="%d%m%Y"),
                "referenceNo": "@id",
                "transferReferenceNo": "SX00021848",
                "resultCode": "00",
                "gbpReferenceNo": "@id",
                "time": "112233",
                "resultMessage": "Success"
            }
        elif status == "fail":
            mode = {"resultCode": "01", "resultMessage": "Balance is not enough"}
        elif status == "repead":
            mode = {"resultCode": "03", "resultMessage": "Duplicate Transaction"}
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            # pass # 这里不能直接写pass，如果走到这个else里，最后这句就会因为没有给mode赋值而报错
            mode = {"_res": {"status": 500}}
        self.update(api, mode)

    # 订单查询（订单不存在／成功／失败／处理中／500）
    def update_withdraw_query(self, status, channel_key='000000000000307', inner_key='000000000000307', amount=global_amount/100):
        api = "/withdraw/query/v2/transfers"
        if status == "not_exit":
            mode = {"resultCode": "01", "resultMessage": "Transaction Transfer Not Found"}
        elif status == "success":
            mode = {
                "resultCode": "00",
                "resultMessage": "Success",
                "totalRecord": 1,
                "txns": [
                    {
                        "bankAccount": "7007248474",
                        "date": get_date(fmt="%Y-%m-%d"),
                        "bankCode": gbpay_resp_transfer_mode,
                        "amount": amount,
                        "referenceNo": channel_key,
                        "transferReferenceNo": "SX00021782",
                        "resultCode": "00",
                        "accHolderName": "น.ส. สุทธินันท์ ชาญช่าง",
                        "resultMessage": "Success",
                        "gbpReferenceNo": inner_key,
                        "timeline": "0",
                        "merchantDefined5": "",
                        "time": "104858",
                        "merchantDefined3": "",
                        "merchantDefined4": "",
                        "merchantDefined1": "pay",
                        "merchantDefined2": ""
                    }
                ]
            }
        elif status == "fail":
            mode = {
                "resultCode": "00",
                "resultMessage": "Success",
                "totalRecord": 1,
                "txns": [
                    {
                        "bankAccount": "5522454315953007",
                        "bankCode": gbpay_resp_transfer_mode,
                        "amount": "1.00",
                        "referenceNo": channel_key,
                        "transferReferenceNo": "",
                        "resultCode": "90",
                        "accHolderName": "testtest",
                        "resultMessage": "Error",
                        "gbpReferenceNo": inner_key,
                        "timeline": "0",
                        "merchantDefined5": "",
                        "merchantDefined3": "",
                        "merchantDefined4": "",
                        "merchantDefined1": "pay",
                        "merchantDefined2": ""
                    }
                ]
            }
        elif status == "process":
            mode = {
                "resultCode": "00",
                "resultMessage": "Success",
                "totalRecord": 1,
                "txns": [
                    {
                        "bankAccount": "7262838433",
                        "bankCode": gbpay_resp_transfer_mode,
                        "amount": "1800.00",
                        "referenceNo": channel_key,
                        "transferReferenceNo": "",
                        "resultCode": None,
                        "accHolderName": "น.ส. พัชรินทร์ เที่ยงอ่ำ",
                        "resultMessage": None,
                        "gbpReferenceNo": inner_key,
                        "timeline": "0",
                        "merchantDefined5": "",
                        "merchantDefined3": "",
                        "merchantDefined4": "",
                        "merchantDefined1": "payout",
                        "merchantDefined2": ""
                    }
                ]
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    # 代扣下单，获取二维码
    def update_qrcode(self, status):
        api = "/gbp/gateway/qrcode/text"
        if status == "success":
            mode = {
                "referenceNo": "000000000000310",
                "qrcode": "00020101021130830016A000000677010112011501055600681275502180000002011240000910318"
                          "000000000000000310530376454041.005802TH5910GBPrimePay630461D9",
                "resultCode": "00",
                "gbpReferenceNo": "gbp066411567015"
            }
        elif status == "fail":
            mode = {
                "referenceNo": "000000000000307",
                "resultCode": "99",
                "gbpReferenceNo": "gbp@id"
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    # 代扣查询
    def update_qrcode_query(self, status, global_amount=1.01):
        api = "/v1/check_status_txn"
        if status == "success":
            mode = {
                "resultCode": "00",
                "txn": {
                    "date": get_date(fmt="%d%m%Y"),
                    "amount": global_amount/100,
                    "referenceNo": "360446922940509",
                    "gbpReferenceNo": "gbp066411940388",
                    "resultCode": "00",
                    "totalAmount": 1.11,
                    "thbAmount": 0.01,
                    "time": "164002",
                    "currencyCode": "764",
                    "status": "S",
                    "paymentType": "Q"
                }
            }
        elif status == "fail":
            # mode = {
            #     "referenceNo": "360446922940509",
            #     "gbpReferenceNo": "gbp066411940388",
            #     "resultCode": "99"
            # }
            mode = {
                "resultCode": "00",
                "txn": {
                    "amount": 1.12,
                    "referenceNo": "360446922940509",
                    "gbpReferenceNo": "gbp066411940388",
                    "status": "D"
                }
            }
        elif status == "process":
            mode = {
                "resultCode": "00",
                "txn": {
                    "amount": 1.12,
                    "referenceNo": "360446922940509",
                    "gbpReferenceNo": "gbp066411940388",
                    "status": "G"
                }
            }
        elif status == "not_exit":
            mode = {"resultCode": "02", "resultMessage": "Invalid referenceNo."}
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    # 绑卡
    def update_gbpay_bindcard(self, status):
        api = "/v2/transfers"
        if status == "success":
            mode = {"resultCode": "00", "resultMessage": "Success"}
        elif status == "fail":
            mode = {"resultCode": "01", "resultMessage": "Bank account not found"}
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    def update_checkout_token_success(self):
        api = "/v1/tokens"
        mode = {"rememberCard": False,
                "resultCode": "00",
                "card": {"name": None,
                         "number": "498765XXXXXX8769",
                         "expirationMonth": "05",
                         "expirationYear": "21",
                         "securityCode": None,
                         "token": "@guid"}}
        self.update(api, mode)

    def update_checkout_token_fail(self):
        api = "/v1/tokens"
        mode = {"rememberCard": False,
                "resultCode": "54",
                "card": None}
        self.update(api, mode)

    def update_checkout_charge_success(self):
        api = "/v1/tokens/charge"
        mode = {"gbpReferenceNo": "gbp@id",
                "resultCode": "00",
                "amount": 10.00,
                "referenceNo": "RBIZ410267510838604468"}
        self.update(api, mode)

    def update_checkout_charge_fail(self):
        api = "/v1/tokens/charge"
        mode = {"gbpReferenceNo1": "gbp@id",
                "resultCode": "54",
                "amount": 10.00,
                "referenceNo": "RBIZ410267510838604468"}
        self.update(api, mode)

    def update_checkout_3d_secured_success(self):
        api = "/v1/tokens/3d_secured"
        mode = {
            "_res": {
                "status": 201,
                "data": '<!DOCTYPE html> \
                        <html> \
                          <head> \
                            <title>GB Prime Pay</title> \
                          </head> \
                          <body> \
                            <div>Loading...</div> \
                            <div> \
                              <form action="http://simbank.globalprimepay.com/pay/3d_secure" method="post"> \
                                "test" \
                              </form> \
                            </div> \
                          </body> \
                        </html>'}}
        self.update(api, mode)

    def update_checkout_3d_secured_fail(self):
        api = "/v1/tokens/3d_secured"
        mode = {
            "_res": {
                "status": 201,
                "data": "fail"}}
        self.update(api, mode)

    def update_checkout_query_not_exit(self):
        api = "/v1/check_status_txn"
        mode = {"resultCode": "02",
                "resultMessage": "Invalid referenceNo."}
        self.update(api, mode)

    def update_checkout_query_success(self, withhold_receipt):
        amount = round(withhold_receipt[0]["withhold_receipt_amount"] / 100, 2)
        api = "/v1/check_status_txn"
        mode = {"resultCode": "00",
                "txn": {"date": None,
                        "amount": amount,
                        "referenceNo": withhold_receipt[0]["withhold_receipt_channel_key"],
                        "amountPerMonth": ".00",
                        "resultCode": "00",
                        "cardType": None,
                        "issuerBank": None,
                        "cardNo": "498765XXXXXX8769",
                        "selectedCountry": None,
                        "totalAmount": ".00",
                        "payMonth": None,
                        "selectedBank": None,
                        "gbpReferenceNo": "gbp@id",
                        "thbAmount": ".00",
                        "time": None,
                        "currencyCode": "764",
                        "status": "A"}}
        self.update(api, mode)

    def update_checkout_query_fail(self, withhold_receipt):
        amount = round(withhold_receipt[0]["withhold_receipt_amount"] / 100, 2)
        api = "/v1/check_status_txn"
        mode = {"resultCode": "00",
                "txn": {"date": None,
                        "amount": amount,
                        "referenceNo": withhold_receipt[0]["withhold_receipt_channel_key"],
                        "amountPerMonth": ".00",
                        "resultCode": "55",
                        "cardType": None,
                        "issuerBank": None,
                        "cardNo": "498765XXXXXX8769",
                        "selectedCountry": None,
                        "totalAmount": ".00",
                        "payMonth": None,
                        "selectedBank": None,
                        "gbpReferenceNo": "gbp@id",
                        "thbAmount": ".00",
                        "time": None,
                        "currencyCode": "764",
                        "status": "D"}}
        self.update(api, mode)

    def update_checkout_query_process(self, withhold_receipt):
        amount = round(withhold_receipt[0]["withhold_receipt_amount"] / 100, 2)
        api = "/v1/check_status_txn"
        mode = {"resultCode": "00",
                "txn": {"amount": amount,
                        "referenceNo": withhold_receipt[0]["withhold_receipt_channel_key"],
                        "gbpReferenceNo": withhold_receipt[0]["withhold_receipt_channel_inner_key"],
                        "status": "G"}}
        self.update(api, mode)

    def update_checkout_query_500(self):
        api = "/v1/check_status_txn"
        mode = {"_res": {"status": 500}}
        self.update(api, mode)
