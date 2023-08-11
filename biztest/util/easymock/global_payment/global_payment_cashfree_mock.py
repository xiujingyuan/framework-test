from biztest.config.payment.url_config import global_amount
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_date


class CashfreMock(Easymock):
    # 用户中心mock
    def update_fk_userinfo(self, fullname, ifsc=None, account_number=None, upi=None):
        api = "/individual/GetUserInfoByUserUUID"
        mode = {"code": 0,
                "msg": "success",
                "data": {"individual_fullname_encrypt": fullname,
                         "individual_phone_encrypt": "enc_01_3661371380442079232_501",
                         "individual_email_encrypt": "enc_05_3661371818730070016_189",
                         "individual_address_encrypt": "enc_02_2995064743557341184_180",
                         "individual_aadhaar_encrypt": "enc_02_2995064743557341184_180",
                         "individual_pan_encrypt": "enc_02_2995064743557341184_180",
                         "bank_card_ifsc_code": ifsc,
                         "bank_card_account_number_encrypt": account_number,
                         "bank_card_no_encrypt": "enc_03_2916465672853135360_415",
                         "bank_card_name_encrypt": "enc_04_3660259551133310976_563",
                         "bank_card_upi_encrypt": upi}}
        # self.update(api, mode)
        self.update_by_api_id("618a1d27c78b2c0020cd8e11", api, mode, "post")

    # 获取token mock
    def update_gettoken(self, status):
        api = "/payout/v1/authorize"
        if status == "200":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Token generated",
                    "data": {
                        "token": "ab9JCVXpkI6ICc5RnIsICN4MzUIJiOicGbhJye.ab0nIIRVVB9VSQFEVV9UWBBlI6IiY1NnIsgDOwEzNxYzM2EjOiQXYpJCL4gjNxcTM2MjNxojIwhXZiwiI2YjL54iNxEjL3QjI6ICcpJCLlNHbhZmOis2Ylh2QlJXd0Fmbnl2ciwyMzkDMzEjOiQWS05WdvN2YhJCLicETHRVRU90M0MlSChkREZETUVzQwUDM1ATMGNkI6ICZJRnbllGbjJye.ab-w6Xs5_C1gk_87sPyNTnuJPYT-uflpzk-CVtmuhWHCWyE63ab6JiZdGQXS4b0Bf6",
                        "expiry": 1636171688}}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode)
    # 获取token mock
    def update_gettoken_collect(self, status):
        api = "/cac/v1/authorize"
        if status == "success":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Token generated",
                    "data": {
                        "token": "ab9JCVXpkI6ICc5RnIsICN4MzUIJiOicGbhJye.ab0nIIRVVB9VSQFEVV9UWBBlI6IiY1NnIsgDOwEzNxYzM2EjOiQXYpJCL4gjNxcTM2MjNxojIwhXZiwiI2YjL54iNxEjL3QjI6ICcpJCLlNHbhZmOis2Ylh2QlJXd0Fmbnl2ciwyMzkDMzEjOiQWS05WdvN2YhJCLicETHRVRU90M0MlSChkREZETUVzQwUDM1ATMGNkI6ICZJRnbllGbjJye.ab-w6Xs5_C1gk_87sPyNTnuJPYT-uflpzk-CVtmuhWHCWyE63ab6JiZdGQXS4b0Bf6",
                        "expiry": 1636171688}}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode)

    # bankaccount绑卡验证
    def update_verify_bankDetails(self, status, name=""):
        api = "/payout/v1.2/validation/bankDetails"
        if status == "success":
            # 以前 status=SUCCESS且data.accountExists=YES(表示打款成功）
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Bank Account details verified successfully",
                    "accountStatus": "VALID",
                    "accountStatusCode": "ACCOUNT_IS_VALID",
                    "data": {"nameAtBank": name,
                             "amountDeposited": "0",
                             "refId": "@id",
                             "bankName": "YES BANK",
                             "utr": "1636103528233633",
                             "city": "GREATER BOMBAY",
                             "branch": "SANTACRUZ, MUMBAI",
                             "micr": 400532038}}
        elif status == "invalid":
            # 此时实际上不会返回nameAtBank，以下只是mock
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "IFSC code is invalid",
                    "accountStatus": "INVALID",
                    "accountStatusCode": "INVALID_IFSC",
                    "data": {"nameAtBank": name,
                             "refId": "@id"}}
        elif status == "not_name":
            # 没有返回nameAtBank，会当作失败处理
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Bank Account details verified successfully",
                    "accountStatus": "VALID",
                    "accountStatusCode": "ACCOUNT_IS_VALID",
                    "data": {"refId": "@id"}}
        elif status == "fail":
            mode = {"status": "ERROR",
                    "subCode": "520",
                    "message": "Verification attempt failed"}
            # mode = {"status": "ERROR",
            #         "subCode": "422",
            #         "message": "Please provide a valid IFSC code"}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode)

    # UPI绑卡验证
    def update_verify_upiDetails(self, status, name=""):
        api = "/payout/v1/validation/upiDetails"
        if status == "success":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "VPA verification successful",
                    "data": {"nameAtBank": name,
                             "accountExists": "YES"
                             }}
        elif status == "invalid":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "VPA verification NO",
                    "data": {"nameAtBank": name,
                             "accountExists": "NO"
                             }}
        elif status == "not_name":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "VPA verification successful",
                    "data": {"accountExists": "YES"}}
        elif status == "fail":
            mode = {"status": "ERROR",
                    "subCode": "422",
                    "message": "Please provide a valid Virtual Payee Address."}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode)

    # 查询受益人
    def update_beneficiary(self, status, card_uuid=""):
        api = "/payout/v1/getBeneficiary/" + str(card_uuid)
        if status == "success":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Details of beneficiary",
                    "data": {"beneId": card_uuid,
                             "name": "JOHN DOE",
                             "email": "test001@163.com",
                             "phone": "2255880085",
                             "address1": "568018527148",
                             "address2": "",
                             "city": "",
                             "state": "",
                             "pincode": "",
                             "bankAccount": "00011020001772",
                             "ifsc": "HDFC0000001",
                             "status": "VERIFIED",
                             "maskedCard": None,
                             "vpa": "",
                             "addedOn": "2021-11-06 09:12:19"}}
        elif status == "fail":
            mode = {"status": "ERROR",
                    "subCode": "404",
                    "message": "Beneficiary not found with given bank account details"}
        else:
            mode = {"_res": {"status": 500}}
        self.update_by_api_id("5e48214fd53ef1165b9824a2", api, mode, "get")

    # 添加受益人
    def update_add_beneficiary(self, status):
        api = "/payout/v1/addBeneficiary"
        if status == "success":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Beneficiary added successfully"}
        elif status == "fail":
            mode = {"status": "ERROR",
                    "subCode": "412",
                    "message": "Post data is empty or not a valid JSON"}
        elif status == "exit":
            mode = {"status": "ERROR",
                    "subCode": "409",
                    "message": "Entered bank Account is already registered"}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode)

    # 余额查询
    def update_balance(self, status):
        api = "/payout/v1/getBalance"
        if status == "success":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Ledger balance for the account",
                    "data": {"balance": "199988.94",
                             "availableBalance": "199988.94"}}
        elif status == "no":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Ledger balance for the account",
                    "data": {"balance": "0",
                             "availableBalance": "0"}}
        elif status == "fail":
            mode = {"status": "ERROR",
                    "subCode": "403",
                    "message": "Token is not valid"}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode)

    # 代付状态查询
    def update_transfer_status(self, status, channel_key="test000000001", amount=global_amount/100, mode="BANK"):
        api = "/payout/v1/getTransferStatus"
        if status == "not_exit":
            mode = {"status": "ERROR",
                    "subCode": "404",
                    "message": "transferId is invalid or does not exist"}
        elif status == "success":
            # "message": "Details of transfer with transferId %s" % channel_key,
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Details of transfer with transferId test",
                    "data": {"transfer": {"referenceId": "inner" + channel_key[4:],
                                          "bankAccount": "00011020001772",
                                          "ifsc": "HDFC0000001",
                                          "beneId": "35292403541383110",
                                          "amount": amount,
                                          "status": "SUCCESS",
                                          "utr": "1636278035550000",
                                          "addedOn": "2021-11-07 15:10:35",
                                          "processedOn": get_date(),
                                          "transferMode": mode,
                                          "acknowledged": 1,
                                          "phone": "2255880085"}}}
        elif status == "error":
            mode = {"status": "ERROR",
                    "subCode": "403",
                    "message": "Token is not valid"}
        elif status == "fail":  # REVERSED
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Details of transfer with transferId %s" % channel_key,
                    "data": {"transfer": {"referenceId": "inner" + channel_key[4:],
                                          "bankAccount": "00011020001772",
                                          "ifsc": "HDFC0000001",
                                          "beneId": "35292403541383110",
                                          "amount": amount,
                                          "status": "FAILED",
                                          "utr": "1636278035550000",
                                          "addedOn": "2021-11-07 15:10:35",
                                          "processedOn": get_date(),
                                          "reason": "test_BENEFICIARY_BANK_OFFLINE",
                                          "transferMode": mode,
                                          "acknowledged": 0,
                                          "phone": "2255880085"}}}
        elif status == "process":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Details of transfer with transferId %s" % channel_key,
                    "data": {"transfer": {"referenceId": "inner" + channel_key[4:],
                                          "bankAccount": "00011020001772",
                                          "ifsc": "HDFC0000001",
                                          "beneId": "35292403541383110",
                                          "amount": amount,
                                          "status": "PENDING",
                                          "utr": "1636278035550000",
                                          "addedOn": "2021-11-07 15:10:35",
                                          "processedOn": get_date(),
                                          "reason": "test_PENDING",
                                          "transferMode": mode,
                                          "acknowledged": 0,
                                          "phone": "2255880085"}}}
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            mode = {"status": status,
                    "subCode": "200",
                    "message": "Details of transfer with transferId test",
                    "data": {"transfer": {"referenceId": "inner" + channel_key[4:],
                                          "bankAccount": "00011020001772",
                                          "ifsc": "HDFC0000001",
                                          "beneId": "35292403541383110",
                                          "amount": amount,
                                          "status": "SUCCESS",
                                          "utr": "1636278035550000",
                                          "addedOn": "2021-11-07 15:10:35",
                                          "processedOn": get_date(),
                                          "transferMode": mode,
                                          "acknowledged": 1,
                                          "phone": "2255880085"}}}
        self.update(api, mode)

    # 代付
    def update_transfer(self, status, channel_key=""):
        api = "/payout/v1/requestTransfer"
        if status == "success":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Transfer completed successfully",
                    "data": {"referenceId": "inner" + channel_key[4:],
                             "utr": "1636278035550000",
                             "acknowledged": 1}}
        elif status == "success_201":  # 这是根据文档提供的code模拟的
            mode = {"status": "SUCCESS",
                    "subCode": "201",
                    "message": "Transfer Scheduled for next working day",
                    "data": {"referenceId": "inner" + channel_key[4:],
                             "utr": "1636278035552222",
                             "acknowledged": 1}}
        elif status == "process":  # 这是根据文档提供的code模拟的
            mode = {"status": "PENDING",
                    "subCode": "201",
                    "message": "Transfer request pending at the bank.",
                    "data": {"referenceId": "inner" + channel_key[4:],
                             "utr": "1636278035553333",
                             "acknowledged": 1}}
        elif status == "process_202":  # 这是根据文档提供的code模拟的
            mode = {"status": "PENDING",
                    "subCode": "202",
                    "message": "Request received. Please check status after some time",
                    "data": {"referenceId": "inner" + channel_key[4:],
                             "utr": "1636278035553333",
                             "acknowledged": 1}}
        elif status == "fail":  # 这是根据文档提供的code模拟的
            mode = {"status": "ERROR",
                    "subCode": "422",
                    "message": "Transfer request to paytm wallet failed"}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode)

    # 代扣
    def update_order(self, status):
        api = "/pg/orders"  # 以下mock只mock使用到的参数
        if status == "success":
            mode = {"order_expiry_time": get_date(fmt="%Y-%m-%d") + "T11:11:11+05:30",
                    "order_status": "ACTIVE",
                    "payment_link": "https://payments-test.cashfree.com/order/#HzpObilOcFw7bIWnYZyA"}
        elif status == "fail":
            mode = {"order_expiry_time": get_date(fmt="%Y-%m-%d") + "T22:22:22+05:30",
                    "order_status": "ACTIVE"}
        elif status == "error":
            mode = {"order_status": "ACTIVE",
                    "payment_link": "https://payments-test.cashfree.com/order/#HzpObilOcFw7bIWnYZyA"}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode)

    # 代扣状态查询
    def update_order_status(self, status, channel_key="test000000001"):
        api = "/pg/orders/" + str(channel_key)
        if status == "process":
            mode = {"order_status": "ACTIVE",
                    "order_expiry_time": get_date(fmt="%Y-%m-%d") + "T23:59:59+05:30"}
        elif status == "expired_status":
            mode = {"order_status": "EXPIRED",
                    "order_expiry_time": get_date(fmt="%Y-%m-%d") + "T00:00:00+05:30"}
        elif status == "expired_at":
            expired_at = get_date(hour=-2, minute=-31)  # fmt="%Y-%m-%d %H:%M:%S"  注意有时差
            mode = {"order_status": "ACTIVE",
                    "order_expiry_time": expired_at[:10] + "T" + expired_at[9:] + "+05:30"}
        elif status == "success":
            mode = {"order_status": "PAID",
                    "order_expiry_time": get_date(fmt="%Y-%m-%d") + "T23:59:59+05:30"}
        else:
            mode = {"_res": {"status": 500}}
        self.update_by_api_id("61a07b3dc78b2c0020cd8e36", api, mode, "get")

    # 账单状态查询
    def update_payments_status(self, status, channel_key="test000000001", amount=global_amount/100):
        api = "/pg/orders/" + str(channel_key) + "/payments"
        if status == "success":
            mode = [{"order_id": channel_key,
                     "payment_time": get_date(fmt="%Y-%m-%d") + "T15:15:15+05:30",
                     "payment_status": "SUCCESS",
                     "payment_message": "TESTMOCK SUCCESS",
                     "payment_amount": amount,
                     "payment_method": {
                         "card": {"card_type": "credit_card"}
                     }}]
        elif status == "null_list":
            mode = []
        elif status == "fail_list":
            mode = [{"order_id": channel_key,
                     "payment_time": get_date(fmt="%Y-%m-%d") + "T23:23:23+05:30",
                     "payment_status": "FAILED",
                     "payment_message": "TESTMOCK FAILED",
                     "payment_amount": amount},
                    {"order_id": channel_key,
                     "payment_time": get_date(fmt="%Y-%m-%d") + "T13:13:13+05:30",
                     "payment_status": "FAILED",
                     "payment_message": "TESTMOCK FAILED",
                     "payment_amount": amount}]
        else:
            mode = {"_res": {"status": 500}}
        self.update_by_api_id("61a0a1ffc78b2c0020cd8e37", api, mode, "get")

    # collect开户
    def update_register(self, status, vpa=""):
        api = "/cac/v1/createVA"
        if status == "success":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Virtual account added successfully",
                    "data": {"vpa": "cashme8t1w{0}@yesbankltd".format(vpa)}}
        elif status == "exit":
            mode = {"status": "ERROR",
                    "subCode": "409",
                    "message": "Virtual account Id already exists"}
        elif status == "fail":
            mode = {"status": "ERROR",
                    "subCode": "412",
                    "message": "Please provide either Virtual Account or VPA"}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode)

    # collect创建二维码
    def update_register_qrcode(self, status):
        api = "/cac/v1/createDynamicQRCode"
        if status == "success":
            mode = {"status": "SUCCESS",
                    "subCode": "200",
                    "message": "Dynamic QR Code generated succesfully",
                    "qrCode": "data:image/png;base64,iVEHjx795JNPsHjx795JNPsHjx795JNPsUI=)",
                    "virtualVPA": "cashmetest@yesbankltd"}
        elif status == "fail":
            mode = {"status": "ERROR",
                    "subCode": "400",
                    "message": "VPA does not exist for the account provided"}
        else:
            mode = {"_res": {"status": 500}}
        self.update(api, mode, "get")


