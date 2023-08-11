from biztest.config.payment.url_config import global_rapyd_payment_id, global_rapyd_paid_at, global_amount, \
    xendit_redirect_url, xendit_resp_payment_mode, xendit_ebank_resp_payment_mode
from biztest.util.easymock.easymock import Easymock


class XenditMock(Easymock):

    # 用户中心mock
    def update_fk_userinfo(self, account_no, bank_code="LBP", withdraw_type="bank"):
        api = "/phl/v1/biz/getUserInfo"
        if withdraw_type == "bank":
            mode = {
                "code": 0,
                "data": {
                    "accountNoEncrypt": account_no,  # 线上放款返回的数据
                    "bankCardCode": bank_code,
                    "bankCardMethod": 1,  # 1.Bank Account 2.E-Wallet 3.Cash pickup
                    "birthday": "08/19/1978",
                    "civilStatusId": 0,
                    "fullnameEncrypt": "enc_04_4106598333291175936_741",  # BENGNAN ADELYN ANGID
                    "gender": "female",
                    "idType": "UMID (unified multi-purpose ID)",
                    "idcardPicUrl": "https://dxcloud-sg-ph-prod.oss-ap-southeast-1.aliyuncs.com/20210927/Z3RNVnVWcFhTOXNU",
                    "identificationIdEncrypt": "enc_04_4106600385027252224_080",  # 006008894445
                    "identificationTypeId": 1,
                    "locationEncrypt": "enc_04_4106598701836279808_167",
                    # Luna,Apayao,CAR (Cordillera Administrative Region),Sanisidrosur
                    "motherMaidenNameEncrypt": "enc_04_4106598982485549056_239",  # ANGID
                    "phoneEncrypt": "enc_04_4106599193308045312_519"  # 09450775028
                },
                "msg": "success"
            }
        elif withdraw_type == "Paymaya":
            mode = {
                "code": 0,
                "data": {
                    "accountNoEncrypt": account_no,
                    "bankCardCode": "Paymaya",
                    "bankCardMethod": 2,  # 1.Bank Account 2.E-Wallet 3.Cash pickup
                    "birthday": "03/20/1984",
                    "civilStatusId": 0,
                    "fullnameEncrypt": "enc_04_4106598333291175936_741",  # BENGNAN ADELYN ANGID
                    "gender": "female",
                    "idType": "UMID (unified multi-purpose ID)",
                    "idcardPicUrl": "https://dxcloud-sg-ph-prod.oss-ap-southeast-1.aliyuncs.com/20210927/Z3RNVnVWcFhTOXNU",
                    "identificationIdEncrypt": "enc_04_4106600385027252224_080",  # 006008894445
                    "identificationTypeId": 1,
                    "locationEncrypt": "enc_04_4106598701836279808_167",
                    # Luna,Apayao,CAR (Cordillera Administrative Region),Sanisidrosur
                    "motherMaidenNameEncrypt": "enc_04_4106598982485549056_239",  # ANGID
                    "phoneEncrypt": "enc_04_4106599193308045312_519"  # 09450775028
                },
                "msg": "success"
            }
        elif withdraw_type == "Gcash":
            mode = {
                "code": 0,
                "data": {
                    "accountNoEncrypt": account_no,
                    "bankCardCode": "GCash",
                    "bankCardMethod": 2,  # 1.Bank Account 2.E-Wallet 3.Cash pickup
                    "birthday": "03/20/1984",
                    "civilStatusId": 0,
                    "fullnameEncrypt": "enc_04_4106598333291175936_741",  # BENGNAN ADELYN ANGID
                    "gender": "female",
                    "idType": "UMID (unified multi-purpose ID)",
                    "idcardPicUrl": "https://dxcloud-sg-ph-prod.oss-ap-southeast-1.aliyuncs.com/20210927/Z3RNVnVWcFhTOXNU",
                    "identificationIdEncrypt": "enc_04_4106600385027252224_080",  # 006008894445
                    "identificationTypeId": 1,
                    "locationEncrypt": "enc_04_4106598701836279808_167",
                    # Luna,Apayao,CAR (Cordillera Administrative Region),Sanisidrosur
                    "motherMaidenNameEncrypt": "enc_04_4106598982485549056_239",  # ANGID
                    "phoneEncrypt": "enc_04_4106599193308045312_519"  # 09450775028
                },
                "msg": "success"
            }
        else:
            return
        self.update(api, mode)

    # 代付请求
    def update_xendit_withdraw(self, status, channel_key, channel_inner_key="disb-6a49375d-fc0b-4992-b46c-e04cede8388e"):
        api = "/disbursements"
        if status == "PENDING":
            mode = {
                "id": channel_inner_key,
                "reference_id": channel_key,
                "currency": "PHP",
                "amount": global_amount / 100,
                "channel_code": xendit_resp_payment_mode,
                "description": channel_key,
                "status": "PENDING",
                "created": "2022-12-21T02:32:57.873Z",
                "updated": "2022-12-21T02:32:57.873Z"
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    # 代付结果查询
    def update_xendit_withdraw_query(self, status, channel_key=None, channel_inner_key="disb-6a49375d-fc0b-4992-b46c-e04cede8388e", payment_code="PH_GCASH"):
        api = "/disbursements/reference_id=" + channel_key
        if status == "fail":
            mode = [
                {
                    "id": channel_inner_key,
                    "reference_id": channel_key,
                    "currency": "PHP",
                    "amount": global_amount/100,
                    "channel_code": payment_code,
                    "description": channel_key,
                    "status": "FAILED",
                    "created": "2022-12-14T23:39:56.779Z",
                    "updated": "2022-12-14T23:39:57.174Z",
                    "failure_code": "INSUFFICIENT_BALANCE"  # 放款失败原因
                }
            ]
        elif status == "success":
            mode = [
                {
                    "id": channel_inner_key,
                    "reference_id": channel_key,
                    "currency": "PHP",
                    "amount": global_amount/100,
                    "channel_code": payment_code,
                    "description": channel_key,
                    "status": "COMPLETED",  # "status": "COMPLETED",  #Possible values: FAILED, PENDING, COMPLETED
                    "created": "2022-12-14T23:39:56.779Z",
                    "updated": "2022-12-14T23:39:57.174Z"
                    # ,"failure_code": "INSUFFICIENT_BALANCE"  # 放款失败时才会返回
                }
            ]
        elif status == "not_exit":
            mode = [

            ]
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        # self.update(api, mode)
        self.update_by_api_id("62f38509e7a7d600206d817f", api, mode, "get")

    # 代扣下单，获取付款码
    def update_xendit_paycode_charge(self, status, channel_inner_key, payment_code="CPPERSDSDB5PPH"):
        api = "/payment_codes"
        if status == "success":
            mode = {
                "id": channel_inner_key,
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": "XNDP122035588610511",
                "customer_name": "BENGNAN ADELYN ANGID",
                "payment_code": payment_code,
                "currency": "PHP",
                "amount": global_amount / 100,
                "channel_code": xendit_resp_payment_mode,
                "description": "test description",
                "is_single_use": True,
                "market": "PH",
                "status": "ACTIVE",
                "metadata": {
                    "description": "test description"
                },
                "created_at": "2021-12-10T06:06:27.739173748Z",
                "updated_at": "2021-12-10T06:06:27.739173748Z",
                "expires_at": "2021-12-10T16:00:00Z"
            }
        elif status == "fail":  # 没有返回payment_code
            mode = {
                "id": channel_inner_key,
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": "XNDP122035588610511",
                "customer_name": "BENGNAN ADELYN ANGID",
                # "payment_code": payment_code,
                "currency": "PHP",
                "amount": global_amount / 100,
                "channel_code": xendit_resp_payment_mode,
                "description": "test description",
                "is_single_use": True,
                "market": "PH",
                "status": "error_fail",
                "metadata": {
                    "description": "test description"
                },
                "created_at": "2021-12-10T06:06:27.739173748Z",
                "updated_at": "2021-12-10T06:06:27.739173748Z",
                "expires_at": "2021-12-10T16:00:00Z"
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    # 代扣查询
    def update_xendit_paycode_query(self, status, channel_inner_key, payment_code=None):
        api = "/payment_codes/" + channel_inner_key + "/payments"
        if status == "success":
            mode = [{
                "id": "pymt-af548f2c-bf9f-4f4c-8d24-996e53744fe4",
                "payment_code_id": channel_inner_key,
                "payment_code": payment_code,
                "channel_code": xendit_resp_payment_mode,
                "currency": "PHP",
                "amount": global_amount / 100,
                "status": "COMPLETED",
                "remarks": "payment simulation",
                "created": "2021-12-10T06:09:10.135001Z",
                "updated": "2021-12-10T06:09:10.135001Z"
            }]
        elif status == "fail":
            mode = [{
                "id": "pymt-af548f2c-bf9f-4f4c-8d24-996e53744fe4",
                "payment_code_id": channel_inner_key,
                "payment_code": payment_code,
                "channel_code": xendit_resp_payment_mode,
                "currency": "PHP",
                "amount": global_amount / 100,
                "status": "FAILED",
                "remarks": "payment FAILED",
                # "failure_code": "INSUFFICIENT_BALANCE", #paycode不会返回该字段，即使返回了我方也不会更新
                "created": "2021-12-10T06:09:10.135001Z",
                "updated": "2021-12-10T06:09:10.135001Z"
            }
            ]
        elif status == "process":
            mode = [{
                "id": "pymt-af548f2c-bf9f-4f4c-8d24-996e53744fe4",
                "payment_code_id": channel_inner_key,
                "payment_code": payment_code,
                "channel_code": xendit_resp_payment_mode,
                "currency": "PHP",
                "amount": global_amount / 100,
                "status": "ACTIVE",
                "remarks": "payment simulation",
                "created": "2021-12-10T06:09:10.135001Z",
                "updated": "2021-12-10T06:09:10.135001Z"
            }]
        elif status == "expired":
            mode = [{
                "id": "pymt-af548f2c-bf9f-4f4c-8d24-996e53744fe4",
                "payment_code_id": channel_inner_key,
                "payment_code": payment_code,
                "channel_code": xendit_resp_payment_mode,
                "currency": "PHP",
                "amount": global_amount / 100,
                "status": "EXPIRED",  # EXPIRED表示过期
                "remarks": "payment simulation",
                "created": "2021-12-10T06:09:10.135001Z",
                "updated": "2021-12-10T06:09:10.135001Z"
            }]
        elif status == "none":
            mode = [

            ]
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    # 代扣下单，获取支付链接
    def update_xendit_ebank_charge(self, status, channel_inner_key):
        api = "/ewallets/charges"
        if status == "success":
            mode = {
                "id": channel_inner_key,
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": "XNDE121035588610802",
                "status": "PENDING",
                "currency": "PHP",
                "charge_amount": global_amount / 100,
                "capture_amount": global_amount / 100,
                "refunded_amount": None,
                "checkout_method": "ONE_TIME_PAYMENT",
                "channel_code": xendit_ebank_resp_payment_mode,
                "channel_properties": {
                    "success_redirect_url": "http://www.baidu.com",
                    "failure_redirect_url": "http://www.baidu.com"
                },
                "actions": {
                    "desktop_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=b0d96038-9521-4b4a-a30a-a7a00e0a53d8",
                    "mobile_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=b0d96038-9521-4b4a-a30a-a7a00e0a53d8",
                    "mobile_deeplink_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=b0d96038-9521-4b4a-a30a-a7a00e0a53d8",
                    "qr_checkout_string": None
                },
                "is_redirect_required": True,
                "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_payment1/xendit/callback/xendit_copperstone_ebank",
                "created": "2021-12-13T03:02:37.270739Z",
                "updated": "2021-12-13T03:02:37.270739Z",
                "void_status": None,
                "voided_at": None,
                "capture_now": True,
                "customer_id": None,
                "payment_method_id": None,
                "failure_code": None,
                "basket": None,
                "metadata": {
                    "description": "test description"
                }
            }
        elif status == "fail":  # status<>PENDING直接失败
            mode = {
                "id": "ewc_7a69af9f-c157-42ac-801a-545c1bdb5abc",
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": "XNDE121035588610802",
                "status": "FAILED",
                "currency": "PHP",
                "charge_amount": global_amount / 100,
                "capture_amount": global_amount / 100,
                "refunded_amount": None,
                "checkout_method": "ONE_TIME_PAYMENT",
                "channel_code": xendit_ebank_resp_payment_mode,
                "channel_properties": {
                    "success_redirect_url": "http://www.baidu.com",
                    "failure_redirect_url": "http://www.baidu.com"
                },
                "actions": {
                    "desktop_web_checkout_url": xendit_redirect_url,
                    "mobile_web_checkout_url": xendit_redirect_url,
                    "mobile_deeplink_checkout_url": xendit_redirect_url,
                    "qr_checkout_string": None
                },
                "is_redirect_required": True,
                "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_payment1/xendit/callback/xendit_copperstone_ebank",
                "created": "2021-12-13T03:02:37.270739Z",
                "updated": "2021-12-13T03:02:37.270739Z",
                "void_status": None,
                "voided_at": None,
                "capture_now": True,
                "customer_id": None,
                "payment_method_id": None,
                "failure_code": None,
                "basket": None,
                "metadata": {
                    "description": "test description"
                }
            }

        elif status == "not_supported_channelcode":  # channel_code只能是 PH_PAYMAYA和PH_GCASH还有PH_GRABPAY
            mode = {
                "id": "ewc_7a69af9f-c157-42ac-801a-545c1bdb5abc",
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": "XNDE121035588610802",
                "status": "PENDING",
                "currency": "PHP",
                "charge_amount": global_amount / 100,
                "capture_amount": global_amount / 100,
                "refunded_amount": None,
                "checkout_method": "ONE_TIME_PAYMENT",
                "channel_code": "PH_GCASH23",
                "channel_properties": {
                    "success_redirect_url": "http://www.baidu.com",
                    "failure_redirect_url": "http://www.baidu.com"
                },
                "actions": {
                    "desktop_web_checkout_url": xendit_redirect_url,
                    "mobile_web_checkout_url": xendit_redirect_url,
                    "mobile_deeplink_checkout_url": xendit_redirect_url,
                    "qr_checkout_string": None
                },
                "is_redirect_required": True,
                "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_payment1/xendit/callback/xendit_copperstone_ebank",
                "created": "2021-12-13T03:02:37.270739Z",
                "updated": "2021-12-13T03:02:37.270739Z",
                "void_status": None,
                "voided_at": None,
                "capture_now": True,
                "customer_id": None,
                "payment_method_id": None,
                "failure_code": None,
                "basket": None,
                "metadata": {
                    "description": "test description"
                }
            }
        elif status == "no_inner_key":
            mode = {
                # "id": channel_inner_key,
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": "XNDE121035588610802",
                "status": "PENDING",
                "currency": "PHP",
                "charge_amount": global_amount / 100,
                "capture_amount": global_amount / 100,
                "refunded_amount": None,
                "checkout_method": "ONE_TIME_PAYMENT",
                "channel_code": xendit_ebank_resp_payment_mode,
                "channel_properties": {
                    "success_redirect_url": "http://www.baidu.com",
                    "failure_redirect_url": "http://www.baidu.com"
                },
                "actions": {
                    "desktop_web_checkout_url": xendit_redirect_url,
                    "mobile_web_checkout_url": xendit_redirect_url,
                    "mobile_deeplink_checkout_url": xendit_redirect_url,
                    "qr_checkout_string": None
                },
                "is_redirect_required": True,
                "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_payment1/xendit/callback/xendit_copperstone_ebank",
                "created": "2021-12-13T03:02:37.270739Z",
                "updated": "2021-12-13T03:02:37.270739Z",
                "void_status": None,
                "voided_at": None,
                "capture_now": True,
                "customer_id": None,
                "payment_method_id": None,
                "failure_code": None,
                "basket": None,
                "metadata": {
                    "description": "test description"
                }
            }

        elif status == "no_redirect_url":
            mode = {
                "id": channel_inner_key,
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": "XNDE121035588610802",
                "status": "PENDING",
                "currency": "PHP",
                "charge_amount": global_amount / 100,
                "capture_amount": global_amount / 100,
                "refunded_amount": None,
                "checkout_method": "ONE_TIME_PAYMENT",
                "channel_code": xendit_ebank_resp_payment_mode,
                "channel_properties": {
                    "success_redirect_url": "http://www.baidu.com",
                    "failure_redirect_url": "http://www.baidu.com"
                },
                "actions": {
                    # "desktop_web_checkout_url": xendit_redirect_url,
                    # "mobile_web_checkout_url": xendit_redirect_url,
                    # "mobile_deeplink_checkout_url": xendit_redirect_url,
                    "qr_checkout_string": None
                },
                "is_redirect_required": True,
                "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_payment1/xendit/callback/xendit_copperstone_ebank",
                "created": "2021-12-13T03:02:37.270739Z",
                "updated": "2021-12-13T03:02:37.270739Z",
                "void_status": None,
                "voided_at": None,
                "capture_now": True,
                "customer_id": None,
                "payment_method_id": None,
                "failure_code": None,
                "basket": None,
                "metadata": {
                    "description": "test description"
                }
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)  # 代扣查询

    # xendit_ebank支付结果查询
    def update_xendit_ebank_query(self, status, channel_inner_key, channel_key):
        api = "/ewallets/charges/" + channel_inner_key
        if status == "success":
            mode = {
                "id": channel_inner_key,
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": channel_key,
                "status": "SUCCEEDED",
                "currency": "PHP",
                "charge_amount": global_amount / 100,
                "capture_amount": global_amount / 100,
                "refunded_amount": None,
                "checkout_method": "ONE_TIME_PAYMENT",
                "channel_code": xendit_ebank_resp_payment_mode,
                "channel_properties": {
                    "success_redirect_url": "http://www.baidu.com",
                    "failure_redirect_url": "http://www.baidu.com"
                },
                "actions": {
                    "desktop_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=3e6ab7df-a29c-46f9-820f-60cf7679be4b",
                    "mobile_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=3e6ab7df-a29c-46f9-820f-60cf7679be4b",
                    "mobile_deeplink_checkout_url": None,
                    "qr_checkout_string": None
                },
                "is_redirect_required": True,
                "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_payment1/xendit/callback/xendit_copperstone_ebank",
                "created": "2023-12-13T08:44:15.173719Z",
                # 使用通道返回的created(这里要注意时区的转化)+通道配置中的expire_time时间作为过期时间和当前时间比较，所以created要设置大点
                "updated": "2021-12-13T08:46:58.194499Z",
                "void_status": None,
                "voided_at": None,
                "capture_now": True,
                "customer_id": None,
                "payment_method_id": None,
                "failure_code": None,
                "basket": None,
                "metadata": {
                    "description": "test description"
                }
            }
        elif status == "fail":
            mode = {
                "id": channel_inner_key,
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": channel_key,
                "status": "FAILED",
                "currency": "PHP",
                "charge_amount": global_amount / 100,
                "capture_amount": global_amount / 100,
                "refunded_amount": None,
                "checkout_method": "ONE_TIME_PAYMENT",
                "channel_code": xendit_ebank_resp_payment_mode,
                "channel_properties": {
                    "success_redirect_url": "http://www.baidu.com",
                    "failure_redirect_url": "http://www.baidu.com"
                },
                "actions": {
                    "desktop_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=3e6ab7df-a29c-46f9-820f-60cf7679be4b",
                    "mobile_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=3e6ab7df-a29c-46f9-820f-60cf7679be4b",
                    "mobile_deeplink_checkout_url": None,
                    "qr_checkout_string": None
                },
                "is_redirect_required": True,
                "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_payment1/xendit/callback/xendit_copperstone_ebank",
                "created": "2025-12-13T08:44:15.173719Z",
                # 使用通道返回的created(这里要注意时区的转化)+通道配置中的expire_time时间作为过期时间和当前时间比较，所以created要设置大点
                "updated": "2021-12-13T08:46:58.194499Z",
                "void_status": None,
                "voided_at": None,
                "capture_now": True,
                "customer_id": None,
                "payment_method_id": None,
                "failure_code": "INSUFFICIENT_BALANCE",  # 记录为失败原因
                "basket": None,
                "metadata": {
                    "description": "test description"
                }
            }

        elif status == "pending_timeout":
            mode = {
                "id": channel_inner_key,
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": channel_key,
                "status": "PENDING",
                "currency": "PHP",
                "charge_amount": global_amount / 100,
                "capture_amount": global_amount / 100,
                "refunded_amount": None,
                "checkout_method": "ONE_TIME_PAYMENT",
                "channel_code": xendit_ebank_resp_payment_mode,
                "channel_properties": {
                    "success_redirect_url": "http://www.baidu.com",
                    "failure_redirect_url": "http://www.baidu.com"
                },
                "actions": {
                    "desktop_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=3e6ab7df-a29c-46f9-820f-60cf7679be4b",
                    "mobile_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=3e6ab7df-a29c-46f9-820f-60cf7679be4b",
                    "mobile_deeplink_checkout_url": None,
                    "qr_checkout_string": None
                },
                "is_redirect_required": True,
                "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_payment1/xendit/callback/xendit_copperstone_ebank",
                "created": "2021-12-13T08:44:15.173719Z",
                # 使用通道返回的created(这里要注意时区的转化)+通道配置中的expire_time时间作为过期时间和当前时间比较，所以created要设置小点
                "updated": "2021-12-13T08:46:58.194499Z",
                "void_status": None,
                "voided_at": None,
                "capture_now": True,
                "customer_id": None,
                "payment_method_id": None,
                "failure_code": None,
                "basket": None,
                "metadata": {
                    "description": "test description"
                }
            }
        elif status == "process":
            mode = [

            ]
        elif status == "expired":
            mode = {
                "id": "ewc_36a5fd60-8f5a-4f03-84bb-69c900ed0591",
                "business_id": "619f2789bcee1cbe0f0e3e68",
                "reference_id": "XNDE121035588610928",
                "status": "PENDING",
                "currency": "PHP",
                "charge_amount": global_amount / 100,
                "capture_amount": global_amount / 100,
                "refunded_amount": None,
                "checkout_method": "ONE_TIME_PAYMENT",
                "channel_code": xendit_ebank_resp_payment_mode,
                "channel_properties": {
                    "success_redirect_url": "http://www.baidu.com",
                    "failure_redirect_url": "http://www.baidu.com"
                },
                "actions": {
                    "desktop_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=389fb7b8-f3ed-403c-ad19-59f29ca57052",
                    "mobile_web_checkout_url": "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=389fb7b8-f3ed-403c-ad19-59f29ca57052",
                    "mobile_deeplink_checkout_url": None,
                    "qr_checkout_string": None
                },
                "is_redirect_required": True,
                "callback_url": "https://biz-gateway-proxy.starklotus.com/phl_payment1/xendit/callback/xendit_copperstone_ebank",
                "created": "2021-12-13T09:00:37.892047Z",
                "updated": "2021-12-13T09:00:38.266243Z",
                "void_status": None,
                "voided_at": None,
                "capture_now": True,
                "customer_id": None,
                "payment_method_id": None,
                "failure_code": "INSUFFICIENT_BALANCE",
                "basket": None,
                "metadata": {
                    "description": "test description"
                }
            }
        elif status == "not_exit":
            mode = [

            ]
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)
