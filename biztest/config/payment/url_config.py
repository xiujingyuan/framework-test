# -*- coding: utf-8 -*-
# 国内和海外公用
import pytest
import common.global_const as gc


env_test = gc.ENV
env_environment = gc.ENVIRONMENT
global_payment_base_url = gc.PAYMENT_URL


env_dict = {
    "1": "test",
    "2": "staging",
    "3": "test",
    "4": "staging",
    "5": "test",
    "6": "staging",
    "7": "test",
    "8": "staging",
    "9": "test"
}


def get_env_dict(env):
    env_d = env_dict
    env_test = env_d[str(env)]
    return env_test


# channel_name = ["cpcn_tq_withhold", "baidu_tq2", "baidu_tq4_fc", "yeepay_tq1_withhold"]  先只跑一个通道
sign_company = "auto_test"  # auto_test主体下baidu_auto_test_quick通道有问题，暂时关闭

payment_staging_base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-payment-staging"
payment_test_base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-payment-test"


# global_payment参数化
global_sign_company_yomoyo = "yomoyo"
global_sign_company_yomoyo3 = "yomoyo3"
global_sign_company_cymo1 = "cymo1"
indonesia_sign_company_cymo1 = 'ksp_cymo1'  # 无卡支付
indonesia_sign_company_cymo2 = 'ksp_cymo2'  # 鉴权&放还款
india_bind_channel_name = "cashfree_yomoyo1_verify"  # cashfree绑卡通道
indonesia_bind_channel_name = "flinpay_ksp_cymo1_verify"
thailand_bind_channel_name = "kuainiu_cymo1_verify"
india_cashfree_ebank_channel_name = "cashfree_yomoyo2_ebank"
india_cashfree_reconic_channel_name = "cashfree_yomoyo2_ebank_reconci"
india_razorpay_ebank_channel_name = "razorpay_yomoyo_ebank"
india_razorpay_reconic_channel_name = "razorpay_ECGW0RlTS1NOb3_ebank_reconci"
cashfree_ebank_settlement_id = 262907
tha_bind_channel_name = "gbpay_cymo1_verify"  # gbpay绑卡通道
user_operator = "USER"  # 主动还款
system_operator = "SYSTEM"  # 自动代扣
global_amount = 10000
gbpay_resp_transfer_mode = "022"
xendit_resp_payment_mode = "7ELEVEN"
payloro_resp_payment_mode = "PLWN"
xendit_ebank_resp_payment_mode = "PH_GCASH"
global_rbiz_merchant_name = "rbiz"
global_gbiz_merchant_name = "gbiz"
global_dsq_merchant_name = "dsq"
global_cashfree_available_amount_lubi = 199794.78
global_cashfree_total_amount_lubi = 1234.78
global_withhold_failed_msg = "Payment has been declined by the user"
global_withhold_successed_msg = "Transaction Successful"
global_withhold_failed_link_expired = "this link has expired"
global_withhold_no_exist_msg = "Order Id does not exist"
global_withdraw_failed_reason = "BENEFICIARY_BANK_NODE_OFFLINE"
global_withdraw_failed_message = "Transfer amount is less than minimum amount of Rs.1"
global_withdraw_query_fail_001 = "Details of transfer with transferId a927a2ecfdc64601bc76c1ede05f37a1"
global_withdraw_no_exist_msg = "transferId is invalid or doesnot exist"
global_cashfree_withdraw_fail_001 = "REVERSED"
global_cashfree_withdraw_fail_002 = "FAILED"
global_cashfree_withdraw_fail_003 = "cont_EiyBkARIKlNDnz"
global_cashfree_withdraw_bene_id = "enc_03_2825130832279635968_656"
global_rapyd_payment_id = "payment_60b3d45e3831f7c20392bc692eda2b53"
global_rapyd_paid_at = 1620785993

channel_notify_base_url = "https://biz-gateway-proxy.starklotus.com/tha_payment1/cashfree/callback/"
global_rbiz_callback = "https://biz-gateway-proxy.starklotus.com/tha_repay1/paysvr/callback"
global_rbiz_redirect = "http://www.baidu.com"
global_gbiz_callback = "https://biz-gateway-proxy.starklotus.com/tha_grant1/paysvr/callback"
global_NAME_NOT_MATCH = 'KN_ACCOUNT_NAME_NOT_MATCH'
global_NAME_NOT_CHECK = 'KN_ACCOUNT_NAME_NOT_CHECK'
global_manual_close_order = "KN_MANUAL_CLOSE_ORDER"
global_timeout_close_order = "KN_TIMEOUT_CLOSE_ORDER"
SPECIAL_NAME = "MD"
user_ip_withhold_remark = "{\"user_ip\":\"27.55.70.41\"}"
xendit_redirect_url = "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=b0d96038-9521-4b4a-a30a-a7a00e0a53d8"
# global_ebank_payurl = "https:\/\/payments-test.cashfree.com\/order\/#7bwlccyo9i0w80810uw0z"
global_ebank_payurl = "https://payments-test.cashfree.com/order/#7bwlccyo9i0w80810uw0z"
global_cashfree_sdk_token = "sdk_token"
global_cashfree_sdk_appid = "13261e0a7b38f955c0b25bfb016231"
global_cashfree_sdk_channel_name = "cashfree_yomoyo2_sdk"
global_cashfree_ebank_channel_key = "254371"
global_cashfree_subscribe_id = "8615"
global_cashfree_subscribe_paymentId = "8134"
global_cashfree_subscribe_url = "https://bit.ly/2vJZikl"
global_autoSubscribe_withhold_failcode = "FAILED"
global_autoSubscribe_withhold_successcode = "SUCCESS"
global_autoSubscribe_withhold_message = "SUCCESSFUL or FAILED"

global_order_not_exists = "KN_ORDER_NOT_EXISTS"
global_order_binding_fail = "KN_BINDING_UNVALID"
global_razorpay_ebank_channel_key = "order_Eeh4WcY72Fln1Z"
global_razorpay_ebank_merchant_key = "f2020052215284"
global_razorpay_ebank_amount = 400000  # 派士
global_razorpay_ebank_service_fee = 1298
global_razorpay_ebank_service_tax = 198
global_razorpay_ebank_fail_message = "Payment failed due to insufficient balance in wallet"
global_razorpay_ebank_success_message = "{\"attempts\":1}"
global_razorpay_ebank_payment_mode = "SBIN"
global_razorpay_ebank_channel_option = "netbanking"
global_razorpay_ebank_payment_option = "Net Banking"
global_razorpay_ebank_payment_mode_card = "RuPay"
global_razorpay_ebank_channel_option_card = "card"
global_razorpay_ebank_payment_option_card = "Debit Card"
global_razorpay_verifyid = "fav_EZ8ECbMFZkxqeA"
global_cashfree_verifyid = "4323"
global_razorpay_collect_inner_no = "va_EcitDZIWwDHn7n"  # 该id影响线下还款记录的查询，需和mock保持一致，这个是虚户号
global_razorpay_collect_channel_key1 = "pay_EbaLkolwKjG62n_023"
global_razorpay_collect_channel_key2 = "pay_EbaLkolwKjG62n_024"
global_razorpay_collect_paid_amount = 50350
global_razorpay_collect_channel_mode_upi = "upi"
global_razorpay_collect_channel_option_upi = "Upi"
global_razorpay_collect_payment_mode_upi = "UPI"
global_razorpay_collect_payment_mode_other = "RTGS"
global_razorpay_collect_payment_option = "bank_transfer"
global_razorpay_transfer_id = "trf_E9utgtfGTcpcmm"
global_razorpay_in_account_no = "v_account_razorpay"
india_razorpay_transfer_channel_name = "razorpay_yomoyo_transfer"
india_paytm_transfer_channel_name = "paytm_yomoyo_transfer"
global_paytm_in_account_no = "v_paytm_account_test1"

global_razorpay_collect_cardnum = "50100263837006"
global_razorpay_collect_cardnum_encrypt = "enc_03_2828155385343909888_988"  # 50100263837006加密
global_razorpay_collect_mobile = "+919004177636"
global_razorpay_collect_mobile_encrypt = "enc_01_2828154284204892160_056"  # +919004177636加密
global_razorpay_collect_ifsc = "HDFC0000001"
global_razorpay_collect_name = "MUDITA SAVAI"
global_razorpay_collect_name_encrypt = "enc_04_2828155385377464320_484"  # MUDITA SAVAI加密

global_razorpay_withdraw_contact_id = "cont_EiyBkARIKlNDnz"
global_razorpay_withdraw_fund_account_id = "fa_EiyBlGa2cVVS7y"
global_razorpay_withdraw_process_processing = "processing"
global_razorpay_withdraw_process_queued = "queued"
global_razorpay_withdraw_process_pending = "pending"
global_razorpay_withdraw_balance = 1976943155
global_razorpay_withdraw_fail_rejected = "rejected"
global_razorpay_withdraw_fail_cancelled = "cancelled"
global_razorpay_withdraw_fail_reversed = "reversed"
global_razorpay_withdraw_success_processed = "processed"
global_razorpay_withdraw_mode = "IMPS"
global_razorpay_withdraw_inner_key = "pout_EiApcm4LE7vZxG"

payment_type_subscribe = "subscribe"
payment_type_sdk = "sdk"
sdk_payment_option = "upi"
global_paymentMode = "UPI"
payment_type_ebank = "ebank"
payment_type_paycode = "paycode"
# 付款码-虚拟户
payment_option_va = "virtual account"
payment_mode_bca = "BCA"
# 付款码-便利店
payment_option_retail = "retail"
payment_mode_ft = "FT"
payment_mode_atm = "ATM"

# 泰国二维码支付
payment_type_qrcode = "qrcode"
payment_option_qrcode = "QR Code"
payment_mode_promptpay = "promptpay"

taiguo_sign_company_cymo1 = 'cymo1'  # 鉴权&放还款
taiguo_sign_company_cymo2 = 'cymo2'  # 无卡支付
