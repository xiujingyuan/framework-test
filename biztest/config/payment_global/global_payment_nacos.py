from biztest.util.nacos.nacos import Nacos


class PaymentNacos(Nacos):

    # 修改scb代付mock
    def update_scb_withdraw(self, sign_company="amberstar1", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://api-partners-uat.scb.co.th"
        channel_name = "scb_%s_withdraw" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "scb_withdraw",
            "app_key": "l741773e508b6e4cccb339aa809cebc707",
            "app_secret": "3c98c871608840d39510aebb4289a1f3",
            "description": "desc_product",
            "business_purpose": "desc_product",
            "transactionType": "DR",
            "annotation": "annotation",
            "corporate_id": "asta993",
            "channel_code": "asta993",
            "corporate_name": "AMBER STAR CO.,LTD.",
            "payer_account_no": "4681016622",
            "payer_bank_code": "014",
            "payer_tax_id": "0115563013153",
            "product_name": "product_name",
            "token_url": "%s/partners/v1/oauth/token" % url,
            "withdraw_url": "%s/partners/v2/payment/transfer/credit/initiate" % url,
            "withdraw_confirm_url": "%s/partners/v2/payment/transfer/confirm" % url,
            "withdraw_query_url": "%s/partners/v1/payment/transfer/inquiry" % url,
            "withdraw_balance_url": "",
            "secret_key": "123456",
            "mock_balance": 0,
            "double_confirm": False,
            "next_query_time": 10
        }
        self.update_configs("paysvr-test1", channel_name, body)

    # 修改gbpay代付mock
    def update_gbpay_withdraw(self, sign_company="amberstar1", project_id=None):
        if project_id:
            withdraw_balance_url = \
                "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/withdraw/balance/v2/transfers" % project_id
            withdraw_query_url = \
                "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/withdraw/query/v2/transfers" % project_id
            withdraw_url = \
                "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/withdraw/v2/transfers" % project_id
        else:
            withdraw_balance_url = "https://api.globalprimepay.com/v2/transfers"
            withdraw_query_url = "https://api.globalprimepay.com/v2/transfers"
            withdraw_url = "https://api.globalprimepay.com/v2/transfers"
        channel_name = "gbpay_%s_withdraw" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "gbpay_withdraw",
            "app_id": "gbp0664",
            "private_key": "WIHZUxSiVJ8aZK2yHdxVMfpITU2VzxY3",
            "public_key": "BaelqsKoA1kluOfFSKtklPSZLRHYAbxM",
            "withdraw_balance_query_url": withdraw_balance_url,
            "withdraw_query_url": withdraw_query_url,
            "withdraw_url": withdraw_url,
            "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment1"
                            "/gbpay/callback/withdraw/",
            "description": "pay",
            "next_query_time": 20
        }
        self.update_configs("paysvr-test1", channel_name, body)

    # 修改gbpay二维码代扣mock
    def update_gbpay_qrcode(self, sign_company="amberstar1", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://api.globalprimepay.com"
        channel_name = "gbpay_%s_qrcode" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "gbpay_qrcode",
            "app_id": "gbp0664",
            "private_key": "WIHZUxSiVJ8aZK2yHdxVMfpITU2VzxY3",
            "public_key": "BaelqsKoA1kluOfFSKtklPSZLRHYAbxM",
            "customer_key": "fBUEy7WDsHzr7oh9Kh2d5trEG00qV+7e4ABoGV/xVWX8V+9s5vL+KUcrCkhAWlNPFQ+zXFYFaxyXip9XTKSD6eba7qQE7"
                            "+BUQAFAWXms8RYG6vRfI560S3yECng2zbRiW4g0cgCDJPKYoqeg45wO2ZmU32lSshAeq06qBD66xuTVWh++",
            "charge_query_url": "%s/v1/check_status_txn" % url,
            "charge_url": "%s/gbp/gateway/qrcode/text" % url,
            "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment1"
                            "/gbpay/callback/backgroupurl/",
            "expire_time": 15,
            "expiry_period": "0"
        }
        self.update_configs("paysvr-test1", channel_name, body)

    # 修改gbpay绑卡mock
    def update_gbpay_verify(self, sign_company="cymo1", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/v2/transfers" % project_id
        else:
            url = "https://api.globalprimepay.com/v2/transfers"
        channel_name = "gbpay_%s_verify" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "gbpay_verify",
            "app_id": "gbp0664",
            "private_key": "WIHZUxSiVJ8aZK2yHdxVMfpITU2VzxY3",
            "public_key": "BaelqsKoA1kluOfFSKtklPSZLRHYAbxM",
            "verify_url": url
        }
        self.update_configs("paysvr-test1", channel_name, body)

    # 修改pandapay代付mock
    def update_pandapay_withdraw(self, sign_company="alibey", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "http://moxicopay-api-test1.xiaoxinfen.com"
        channel_name = "pandapay_%s_withdraw" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "pandapay_withdraw",
            "client_id": "94353ded08df4178",
            "client_secret": "9d8e772b111844c599b36e88f328ef12",
            "withdraw_url": "%s/api/pay/createPay" % url,
            "withdraw_query_url": "%s/api/pay/getPay" % url,
            "withdraw_balance_query_url": "%s/api/pay/accountBalance" % url,
            "description": "Pago de prueba",
            "merchant_order_prefix": "P000",
            "merchant_card_num": "646180130900000008",
            "merchant_bank_code": 90646,
            "merchant_account_name": "Eduardo",
            "merchant_account_type": 40,
            "merchant_payment_type": 1,
            "next_query_time": 20,
            "notify_run_time": {
                "Refund": 25,
                "Cancel": 15,
                "Success": 5
            }
        }
        self.update_configs("paysvr-test1", channel_name, body)

    # 修改rapyd二维码代扣配置为mock
    def update_rapyd_qrcode(self, sign_company="amberstar1", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://sandboxapi.rapyd.net"
        channel_name = "rapyd_%s_qrcode" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "rapyd_qrcode",
            "access_key": "0EF31D8F9C8BDC724331",
            "secret_key": "5bd6c148a9c8aea57d26e49fa504e43078f1492ed2a13b325efcb2701b61755ee14abefdca985f1f",
            "country": "TH",
            "currency": "THB",
            "language": "en",
            "expire_time": 15,
            "cardholder_preferred_currency": True,
            "server_url": "%s" % url,
            "charge_url": "%s/v1/payments" % url,
            "charge_query_url": "%s/v1/payments/" % url + "%s",
            "callback_url": "https://biz-gateway-proxy.starklotus.com/tha_payment1/rapyd/callback/rapyd_amberstar1_qrcode",
            "payment_method": "th_thaipromptpayqr_bank",
            "description": "thaipromptpayqr"
        }
        self.update_configs("paysvr-test1", channel_name, body)

    # 修改cashfree验卡mock（默认姓名开）
    def update_cashfree_verify(self, sign_company="yomoyo", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://payout-gamma.cashfree.com"
        channel_name = "cashfree_%s_verify" % sign_company
        body = {
            "channel_name": "cashfree_yomoyo_verify",
            "type": "cashfree_verify",
            "client_id": "CF105050C5TLFDFHBJS43OTETGLG",
            "client_secret": "6a508cde3f9710a41ad1b6314726765a6e5f6370",
            "authorize_url": "%s/payout/v1/authorize" % url,
            "verify_bank_account_url": "%s/payout/v1.2/validation/bankDetails" % url,
            "verify_upi_url": "%s/payout/v1/validation/upiDetails" % url,
            "name_match_switch": "true",
            "name_similarity_rate": 0.88,
            "upi_unbind_account_switch": "false",
            "name_not_include": [
                "^006CREDIT \\d+$",
                ".*006CREDIT.*",
                "VALUED CUSTOMER",
                "IMPS CUSTOMER",
                "Cosmos",
                "APNB",
                "TJSB",
                "PJSB",
                "NO NAME",
                "BCB",
                "MBRR",
                "ve·t9",
                "TEST562",
                "NIYO BLUE FUNDING AC",
                "KJSB"
            ]
        }
        self.update_configs("ind-paysvr-test1", channel_name, body)

    # 修改cashfree代付mock
    def update_cashfree_withdraw(self, sign_company="yomoyo", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://payout-gamma.cashfree.com"
        channel_name = "cashfree_%s_withdraw" % sign_company
        body = {
            "channel_name": "cashfree_yomoyo_withdraw",
            "type": "cashfree_withdraw",
            "client_id": "CF105050C5TLFDFHBJS43OTETGLG",
            "client_secret": "6a508cde3f9710a41ad1b6314726765a6e5f6370",
            "secret_key": "6a508cde3f9710a41ad1b6314726765a6e5f6370",
            "authorize_url": "%s/payout/v1/authorize" % url,
            "register_url": "%s/payout/v1/addBeneficiary" % url,
            "register_query_url": "%s/payout/v1/getBeneId" % url,
            "register_query_by_id_url": "%s/payout/v1/getBeneficiary" % url,
            "withdraw_url": "%s/payout/v1/requestTransfer" % url,
            "withdraw_query_url": "%s/payout/v1/getTransferStatus" % url,
            "withdraw_balance_query_url": "%s/payout/v1/getBalance" % url,
            "next_query_time": 60
        }
        self.update_configs("ind-paysvr-test1", channel_name, body)

    # 修改cashfree代扣mock
    def update_cashfree_ebank(self, sign_company="yomoyo", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://sandbox.cashfree.com"
        channel_name = "cashfree_%s_ebank" % sign_company
        body = {
            "channel_name": "cashfree_yomoyo_ebank",
            "type": "cashfree_ebank",
            "app_id": "10354020c4d0b82cee5b355129045301",
            "secret_key": "208137c9ca6cd805a75f7be93f9fd2815dc2cef2",
            "expire_time": 15,
            "expiry_period": 10,
            "charge_url": "{0}/pg/orders".format(url),
            "charge_query_url": "{0}/pg/orders/%s".format(url),
            "payment_query_url": "{0}/pg/orders/%s/payments".format(url),
            "callback_url": "https://biz-gateway-proxy.starklotus.com/ind_payment1/cashfree/callback/"
        }
        self.update_configs("ind-paysvr-test1", channel_name, body)

    # 修改cashfree_yomoyo_collect的mock
    def update_cashfree_collect(self, sign_company="yomoyo", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://cac-gamma.cashfree.com"
        channel_name = "cashfree_%s_collect" % sign_company
        body = {
            "channel_name": "cashfree_yomoyo_collect",
            "type": "cashfree_collect",
            "client_id": "CF105050CITMPUN83MHE6MU",
            "client_secret": "18769dbf65633f6eb3fdd0f4929946d229d97fdb",
            "authorize_url": "{0}/cac/v1/authorize".format(url),
            "collect_create_account_url": "{0}/cac/v1/createVA".format(url),
            "collect_create_account_qrcode_url": "{0}/cac/v1/createDynamicQRCode".format(url),
            "collect_query_account_url": "{0}/cac/v1/va/%s".format(url),
            "collect_change_status_url": "{0}/cac/v1/changeVAStatus".format(url),
            "collect_query_payment_url": "{0}/cac/v1/payments/%s".format(url),
            "collect_period": -560,
            "collect_max_return": 50,
            "collect_expire_time": 560
        }
        self.update_configs("ind-paysvr-test1", channel_name, body)

    # 修改xendit-withdraw为mock
    def update_xendit_withdraw(self, sign_company="copperstone", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
            query_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id + "/disbursements/reference_id=%s"
        else:
            url = "https://api.xendit.co"
            query_url = "https://api.xendit.co/disbursements?reference_id=%s"  # 实际地址是https://api.xendit.co/disbursements?reference_id=XND121000000000801
        channel_name = "xendit_%s_withdraw" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "xendit_withdraw",
            "basic_auth": "xnd_development_X3j1m3fAbgrJTdEVrfErYIioo6XDwO5HgfGluED9wVXUeyJkQUNsKrDx42w8JBJ",
            "callback_token": "rZiLiUtn3rlqBU8a0PyZv5FyiCVcFObUmLu32noi5I6Exbd2",
            "server_url": "%s/disbursements" % url,
            "query_url": query_url,
            "balance_query_url": "%s" % url + "/balances",
            "next_query_time": 360
        }
        self.update_configs("paysvr-test1", channel_name, body)

    # 修改xendit线下还款paycode为mock
    def update_xendit_paycode(self, sign_company="copperstone", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://api.xendit.co"
        channel_name = "xendit_%s_paycode" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "xendit_paycode",
            "expire_time": 120,
            "expiry_period": 10,
            "charge_url": "%s/payment_codes" % url,
            "query_charge_url": "%s" % url + "/payment_codes/%s/payments",
            "basic_auth": "xnd_development_X3j1m3fAbgrJTdEVrfErYIioo6XDwO5HgfGluED9wVXUeyJkQUNsKrDx42w8JBJ",
            "callback_token": "rZiLiUtn3rlqBU8a0PyZv5FyiCVcFObUmLu32noi5I6Exbd2",
            "description": "test description"
        }
        self.update_configs("paysvr-test1", channel_name, body)

    # 修改xendit网关支付ebank为mock
    def update_xendit_ebank(self, sign_company="copperstone", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://api.xendit.co"
        channel_name = "xendit_%s_ebank" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "xendit_ebank",
            "expire_time": 120,
            "expiry_period": 10,
            "charge_url": "%s/ewallets/charges" % url,
            "query_charge_url": "%s/" % url + "ewallets/charges/%s",
            "basic_auth": "xnd_development_X3j1m3fAbgrJTdEVrfErYIioo6XDwO5HgfGluED9wVXUeyJkQUNsKrDx42w8JBJ",
            "callback_token": "rZiLiUtn3rlqBU8a0PyZv5FyiCVcFObUmLu32noi5I6Exbd2",
            "description": "test description"

        }
        self.update_configs("paysvr-test1", channel_name, body)

    # 修改重复放款配置
    def update_auto_withdraw_risk_white(self, enable=None, all_white=None, card_uuid=""):
        if enable == "false":  # enable=false，表示校验规则不启用，即全部放开
            body = {
                "enable": False,
                "limit_num": "1",
                "limit_hours": "1",
                "white_config": [
                    {
                        "merchant_name": "portal",
                        "all_white": False,
                        "limit_num": "8",
                        "limit_hours": "12",
                        "card_uuid": [
                            card_uuid
                        ]
                    }
                ]
            }
        elif enable == "true":  # enable=true，表示校验规则启用，非portal的12小时内2笔交易的限制
            body = {
                "enable": True,
                "limit_num": "2",
                "limit_hours": "12",
                "white_config": [
                    {
                        "merchant_name": "portal",
                        "all_white": False,
                        "limit_num": "8",
                        "limit_hours": "12",
                        "card_uuid": [
                        ]
                    }
                ]
            }
        elif enable == "default":  # 默认针对同一用户进行12小时内4笔交易的限制
            body = {
            }
        elif all_white == "true":
            # 当all_white=true或指定card_uuid在white_config白名单中的card_uuid时，需要放开校验，允许所有交易
            body = {
                "enable": True,
                "limit_num": "1",
                "limit_hours": "1",
                "white_config": [
                    {
                        "merchant_name": "gbiz",
                        "all_white": True,
                        "limit_num": "1",
                        "limit_hours": "1",
                        "card_uuid": [
                            card_uuid
                        ]
                    }
                ]
            }
        elif all_white == "false":
            # 1.当all_white=false且card_uuid为空时，表示校验规则启用，12小时内2笔交易的限制；
            # 2.当all_white=false但card_uuid不为空，那该card_uuid交易没有任何限制
            body = {
                "enable": True,
                "limit_num": "1",
                "limit_hours": "1",
                "white_config": [
                    {
                        "merchant_name": "gbiz",
                        "all_white": False,
                        "limit_num": "2",
                        "limit_hours": "12",
                        "card_uuid": [
                            card_uuid
                        ]
                    }
                ]
            }
        elif all_white == "invalid_card_uuid":
            body = {
                "enable": True,
                "limit_num": "1",
                "limit_hours": "1",
                "invalid_card_uuid": card_uuid,  # 无效卡，不校验
                "white_config": [
                    {
                        "merchant_name": "portal",
                        "all_white": False,
                        "limit_num": "1",
                        "limit_hours": "1",
                        "card_uuid": [
                            "enc_03_3120932859897448448_788"
                        ]
                    },
                    {
                        "merchant_name": "gbiz",
                        "all_white": False,
                        "limit_num": "1",
                        "limit_hours": "1",
                        "card_uuid": [
                            card_uuid
                        ]
                    }
                ]
            }
        elif all_white == "test":
            body = {
                "enable": True,
                "limit_num": "3",
                "limit_hours": "1",
                "invalid_card_uuid": card_uuid,  # 无效卡，不校验
                "white_config": [
                    {
                        "merchant_name": "portal",
                        "all_white": False,
                        "limit_num": "1",
                        "limit_hours": "1",
                        "card_uuid": [
                            "enc_03_3120932859897448448_788"
                        ]
                    },
                    {
                        "merchant_name": "gbiz",
                        "all_white": False,
                        "limit_num": "2",
                        "limit_hours": "1",
                        "card_uuid": [
                            card_uuid
                        ]
                    }
                ]
            }
        else:
            return
        self.update_configs("paysvr-test1", "auto_withdraw_risk_white", body)

    # 修改payloro-ebank为mock
    def update_payloro_ebank(self, sign_company="copperstone", project_id=None):
        if project_id:
            url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % project_id
        else:
            url = "https://api.payloro.tech"
        channel_name = "payloro_%s_ebank" % sign_company
        body = {
            "channel_name": channel_name,
            "type": "payloro_ebank",
            "public_key": "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCHm1JkkXRTGugFvwRYjhFgeYYJ8Y9Ut+irazZfqniC5nXu68300E5OrTdaBqAw/JMxiebWaQhGm1lqxNDa6YbXlS2oMvT8Swq6PcYl3Kbem9HWvyrqPQEE3QoEBbjHjGxZdPg5eZG5JfA16lrqpoQ5OX55KIWh318SKYDSuppwMwIDAQAB",
            "private_key": "MIICeAIBADANBgkqhkiG9w0BAQEFAASCAmIwggJeAgEAAoGBAL0mrCLiZCBNHS0YhEIalegSvC50gAS2nxSvoPPhn39tcp/NSmo64RgF+rJRQzyMEBfa+khCdZk+jcQC+k3L/UUdhZU7JlpPxMhQpBV+nM4qZze9PbGif8q/KwvV33zDshtaAQofAuqXLCokqueGcG6EudkeA+pZYXoIlh4RTg4fAgMBAAECgYEAhUWaQ3n/0kKDLCL6DRluRfXtYU30ZV3G+GxGm499MeuLt8yNggu6TZLo8HsRRLfrHuPLNN6evTq16EWw1t/DspjdXHJHDVP0itsKK4xFcosQB1MRRainUFWqb89fBCTa3NiC2A0MZjhRyF39tqd6Sotb/6Ni/sMyrXTC0qM/6AECQQDepUCrjdIi0b828IeHCohYb1jJdmoOYw5BvafSUMfQuJ4Kc7hQkFMYDp9QSzyRebOOWbPOBpPpouk8564ve4I/AkEA2XzdFBmv8VRwcWbgsTk4bEyR8KBKRfsRTsxGEPVRZtPembXarWzO0l06YFCmq5mrJEm7OcyJ2bzgaSEt2kS8IQJBAND2HjUk/RVK8IEazMhUfVUq5BTpO27XTzkqTEkbIf5mV4YNx+5tFl/c0W9lvan3pCs1S4lRKR+9k9RiyVutOrcCQFEHbVLM0zlljVMi0joVKIlo6cKt5Z43EVa7UquEyqQ18axxDZ0pedD0fQhfZAlxAktN0RySsRVXgoCIpQ26KCECQQDFHtbCart9DlFhcfB5bjnoS1mwVCwgAHfxe355Q7v/pPQWbFRTStPj4axDV8ibJ1CNZc2L4Apc1QhKtc8+amM0",
            "merchant_code": "NO121920285830",
            "default_mail": "default@123.com",
            "fee_type": "0",
            "expire_time": "120",
            "charge_url": "https://api.payloro.tech/api/pay/code",  # payloro发起代扣不能走mock，因为需要从返回的链接中获取过期时间，获取不到会直接代扣失败
            "charge_query_url": "%s/api/pay/query" % url,
            "description": "payloro_ebank"
        }
        self.update_configs("paysvr-test1", channel_name, body)

    def update_nacos_unionbank_withdraw(self, sign_company="copperstone", withdraw_project_id=None,
                                        query_project_id=None):
        channel_name = "unionbank_%s_withdraw" % sign_company
        if withdraw_project_id:
            withdraw_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % withdraw_project_id
            withdraw_query_url = "https://api-uat.unionbankph.com/ubp/external"
            body = {
                "channel_name": channel_name,
                "type": "unionbank_withdraw",
                "client_id": "1a14e08d-72d1-43eb-8ab2-28ac145e8cd1",
                "client_secret": "pK1nT3xR7kQ2fB5aH4pA1fR7xJ4jE5iX0dJ7jU5uC0nW3mQ8aU",
                "authorize_url": "%s/partners/v1/oauth2/token" % withdraw_query_url,
                "withdraw_url": "%s/partners/v3/instapay/transfers/single" % withdraw_url,
                "withdraw_query_url": "%s" % withdraw_query_url + "/partners/v3/instapay/transfers/single/%s",
                "withdraw_balance_query_url": "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5e9807281718270057767a3e/portal/accounts/v1/transactions",
                # unionbank测试环境余额查询接口不通
                "description": "test",
                "partner_id": "4a8f2ae5-129d-45d7-88c5-a47e8236221e",
                "username": "copperstone_lending",
                "password": "c0PP3rston3L3nDi#LFFdDGRtdApsWhd",
                "grant_type": "password",
                "scope": "instapay",
                "sender_name": "Juan Cruz",
                "sender_address_line1": "GRACE",
                "sender_address_line2": "PARK CALOOCAN CITY",
                "sender_address_city": "Caloocan",
                "sender_address_province": 142,
                "sender_address_zip_code": 1900,
                "beneficiary_address_zip_code": 1900,
                "sender_address_country": 204,
                "next_query_time": 360
            }
        elif query_project_id:
            withdraw_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % query_project_id
            withdraw_query_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s" % query_project_id
            body = {
                "channel_name": channel_name,
                "type": "unionbank_withdraw",
                "client_id": "1a14e08d-72d1-43eb-8ab2-28ac145e8cd1",
                "client_secret": "pK1nT3xR7kQ2fB5aH4pA1fR7xJ4jE5iX0dJ7jU5uC0nW3mQ8aU",
                "authorize_url": "%s/partners/v1/oauth2/token" % withdraw_query_url,
                "withdraw_url": "%s/partners/v3/instapay/transfers/single" % withdraw_url,
                "withdraw_query_url": "%s" % withdraw_query_url + "/partners/v3/instapay/transfers/single/%s",
                "withdraw_balance_query_url": "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5e9807281718270057767a3e/portal/accounts/v1/transactions",
                # unionbank测试环境余额查询接口不通
                "description": "test",
                "partner_id": "4a8f2ae5-129d-45d7-88c5-a47e8236221e",
                "username": "copperstone_lending",
                "password": "c0PP3rston3L3nDi#LFFdDGRtdApsWhd",
                "grant_type": "password",
                "scope": "instapay",
                "sender_name": "Juan Cruz",
                "sender_address_line1": "GRACE",
                "sender_address_line2": "PARK CALOOCAN CITY",
                "sender_address_city": "Caloocan",
                "sender_address_province": 142,
                "sender_address_zip_code": 1900,
                "beneficiary_address_zip_code": 1900,
                "sender_address_country": 204,
                "next_query_time": 360
            }
        else:
            url = "https://api-uat.unionbankph.com/ubp/external"
            body = {
                "channel_name": channel_name,
                "type": "unionbank_withdraw",
                "client_id": "1a14e08d-72d1-43eb-8ab2-28ac145e8cd1",
                "client_secret": "pK1nT3xR7kQ2fB5aH4pA1fR7xJ4jE5iX0dJ7jU5uC0nW3mQ8aU",
                "authorize_url": "%s/partners/v1/oauth2/token" % url,
                "withdraw_url": "%s/partners/v3/instapay/transfers/single" % url,
                "withdraw_query_url": "%s" % url + "/partners/v3/instapay/transfers/single/%s",
                "withdraw_balance_query_url": "https://api-uat.unionbankph.com/ubp/external/portal/accounts/v1/transactions",
                "description": "test",
                "partner_id": "4a8f2ae5-129d-45d7-88c5-a47e8236221e",
                "username": "copperstone_lending",
                "password": "c0PP3rston3L3nDi#LFFdDGRtdApsWhd",
                "grant_type": "password",
                "scope": "instapay",
                "sender_name": "Juan Cruz",
                "sender_address_line1": "GRACE",
                "sender_address_line2": "PARK CALOOCAN CITY",
                "sender_address_city": "Caloocan",
                "sender_address_province": 142,
                "sender_address_zip_code": 1900,
                "beneficiary_address_zip_code": 1900,
                "sender_address_country": 204,
                "next_query_time": 360
            }
        self.update_configs("paysvr-test1", channel_name, body)
