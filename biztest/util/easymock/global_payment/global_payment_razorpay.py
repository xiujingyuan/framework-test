# -*- coding: utf-8 -*-
import time
from datetime import datetime

from biztest.config.payment.url_config import global_razorpay_collect_inner_no, global_razorpay_collect_channel_key1, \
    global_razorpay_collect_paid_amount, global_razorpay_collect_payment_mode_other, \
    global_razorpay_collect_payment_mode_upi, global_razorpay_collect_cardnum, global_razorpay_collect_mobile, \
    global_razorpay_collect_ifsc, global_razorpay_collect_name, global_razorpay_collect_channel_key2, \
    global_razorpay_ebank_channel_key, global_razorpay_ebank_payment_mode, \
    global_razorpay_ebank_fail_message, global_razorpay_verifyid, global_withdraw_failed_message, \
    global_razorpay_withdraw_balance, global_razorpay_withdraw_fail_rejected, global_razorpay_withdraw_fail_cancelled, \
    global_razorpay_withdraw_fail_reversed, global_razorpay_withdraw_mode, global_razorpay_withdraw_inner_key, \
    global_razorpay_withdraw_success_processed, global_razorpay_withdraw_process_processing, \
    global_razorpay_withdraw_process_queued, global_razorpay_withdraw_process_pending, \
    global_razorpay_withdraw_contact_id, global_razorpay_withdraw_fund_account_id, \
    global_razorpay_ebank_service_tax, global_razorpay_ebank_service_fee, global_razorpay_transfer_id, \
    global_ebank_payurl, global_razorpay_ebank_payment_option, global_razorpay_ebank_channel_option, \
    global_razorpay_ebank_payment_mode_card, global_razorpay_ebank_channel_option_card, \
    global_razorpay_collect_payment_option, global_razorpay_collect_channel_mode_upi
from biztest.interface.payment.payment_interface import get_timestamp
from biztest.util.easymock.easymock import Easymock


class RazorpayMock(Easymock):
    def update_razorpay_standard_payment_link_success(self):
        api = "/v1/payment_links"
        mode = {
                "accept_partial": "false",
                "amount":100,
                "amount_paid":0,
                "callback_method":"get",
                "callback_url":"http://cn.bing.com",
                "cancelled_at":0,
                "created_at":1605152877,
                "currency":"INR",
                "customer":{
                    "contact":"15177988787",
                    "email":"wangxiaoming@google.com",
                    "name":"郭坤"
                },
                "description":"test",
                "expire_by":1605154856,
                "expired_at":0,
                "first_min_partial_amount":0,
                "id":"plink_G077m2za7mhiVF",
                "notes":"",
                "notify":{
                    "email":"false",
                    "sms":"false"
                },
                "payments":"",
                "reference_id":"RBIZ411126250664487742",
                "reminder_enable":"false",
                "reminders":[

                ],
                "short_url":"https://rzp.io/i/OMK8puJgvS",
                "status":"created",
                "updated_at":1605152877,
                "upi_link":"false",
                "user_id":""
            }
        self.update(api, mode)

    def update_razorpay_standard_payment_link_failed(self):
        api = "/v1/payment_links"
        mode = {"status": "failed"}
        self.update(api, mode)

    def update_razorpay_standard_payment_link_query_success(self):
        api = "/v1/orders"
        mode = {
                  "entity": "collection",
                  "count": 1,
                  "items": [{
                    "id": "order_FaQiThS3r3Ivm1",
                    "entity": "order",
                    "amount": 505600,
                    "amount_paid": 0,
                    "amount_due": 505600,
                    "currency": "INR",
                    "receipt": "RBIZ409081690114380214",
                    "payments": {
                      "entity": "collection",
                      "count": 1,
                      "items": [{
                        "id": "pay_FaQkqq5jnanARy",
                        "entity": "payment",
                        "amount": 505600,
                        "currency": "INR",
                        "status": "captured", #authorized 认证中、captured已经捕获（成功）
                        "order_id": "order_FaQiThS3r3Ivm1",
                        "invoice_id": "inv_FaQiTgg7xpNTVx",
                        "international": "false",
                        "method": "card",
                        "amount_refunded": 0,
                        "refund_status": "",
                        "captured": "true", #成功的这个是true,需要捕获的是false
                        "description": "#inv_FaQiTgg7xpNTVx",
                        "card_id": "card_FaQkr0Ybue9f7s",
                        "card": {
                          "id": "card_FaQkr0Ybue9f7s",
                          "entity": "card",
                          "name": "Lalit Sahare",
                          "last4": "7556",
                          "network": "Visa",
                          "type": "debit",
                          "issuer": "UTIB",
                          "international": "false",
                          "emi": "false",
                          "sub_type": "consumer"
                        },
                        "bank": "",
                        "wallet": "",
                        "vpa": "",
                        "email": "lalit_sahare@yahoo.com",
                        "contact": "+919322634435",
                        "customer_id": "cust_FUsC4gGZ76VBd4",
                        "notes": [],
                        "fee": "944",
                        "tax": "144",
                        "error_code": "",
                        "error_description": "",
                        "error_source": "",
                        "error_step": "",
                        "error_reason": "",
                        "acquirer_data": {
                          "auth_code": "017794"
                        },
                        "created_at": 1599545165
                      }]
                    },
                    "offer_id": "",
                    "status": "paid", #paid（成功的），attempted（需要捕获时的）
                    "attempts": 1,
                    "notes": [],
                    "created_at": 1599545030
                  }]
                }
        self.update(api, mode)

    def update_razorpay_standard_payment_link_query_not_attempted(self):
        api = "/v1/orders"
        mode = {"entity": "collection", "count": 0, "items": []}
        self.update(api, mode)

    def update_razorpay_standard_payment_link_query_attempted(self, expired=False):
        time_stamp = 1603146756 if expired else int(time.time())
        api = "/v1/orders"
        mode = {
                "entity": "collection",
                "count": 1,
                "items": [
                    {
                        "id": "order_GIPDyvBIGRi2yZ",
                        "entity": "order",
                        "amount": 70000,
                        "amount_paid": 0,
                        "amount_due": 70000,
                        "currency": "INR",
                        "receipt": "RBIZ412286791807851113",
                        "payments": {
                            "entity": "collection",
                            "count": 1,
                            "items": [
                                {
                                    "id": "pay_GIPEErSyUlsL1b",
                                    "entity": "payment",
                                    "amount": 70000,
                                    "currency": "INR",
                                    "status": "failed",
                                    "order_id": "order_GIPDyvBIGRi2yZ",
                                    "invoice_id": None,
                                    "international": "false",
                                    "method": "netbanking",
                                    "amount_refunded": 0,
                                    "refund_status": None,
                                    "captured": "false",
                                    "description": "#GIPD3WAi5YB7bA",
                                    "card_id": None,
                                    "card": None,
                                    "bank": "FDRL",
                                    "wallet": None,
                                    "vpa": None,
                                    "email": "sdaf@fsa.com",
                                    "contact": "+919123456789",
                                    "notes": [

                                    ],
                                    "fee": None,
                                    "tax": None,
                                    "error_code": "BAD_REQUEST_ERROR",
                                    "error_description": "Payment failed",
                                    "error_source": "bank",
                                    "error_step": "payment_authorization",
                                    "error_reason": "payment_failed",
                                    "acquirer_data": {
                                        "bank_transaction_id": None
                                    },
                                    "created_at": time_stamp
                                }
                            ]
                        },
                        "offer_id": None,
                        "status": "attempted",
                        "attempts": 1,
                        "notes": [

                        ],
                        "created_at": time_stamp
                    }
                ]
            }
        self.update(api, mode)

    def update_razorpay_standard_payment_link_query_failed(self):
        api = "/v1/orders"
        mode = {"status": "failed"}
        self.update(api, mode)


    def update_razorpay_create_contacts_fail(self):
        api = "/v1/contacts"  # razorpay创建联系人失败，即绑卡失败
        mode = {
            "id": "cont_@word(15)",
            "entity": "contact",
            "name": "@first @middle @last",
            "contact": "",
            "email": "wangxiaoming@google.com",
            "type": "customer",
            "reference_id": "",
            "batch_id": None,
            "active": "false",  # true 创建成功，false 创建失败
            "notes": {
                "product": "contact"
            },
            "created_at": "1583303041"
        }
        self.update(api, mode)

    def update_razorpay_create_contacts_success(self):
        api = "/v1/contacts"  # razorpay创建联系人
        mode = {
            "id": "cont_@word(15)",
            "entity": "contact",
            "name": "@first @middle @last",
            "contact": "",
            "email": "wangxiaoming@google.com",
            "type": "customer",
            "reference_id": "",
            "batch_id": None,
            "active": "true",  # true 创建成功，false 创建失败
            "notes": {
                "product": "contact"
            },
            "created_at": "1583303041"
        }
        self.update(api, mode)

    def update_razorpay_ebank_fail(self):
        api = "/v1/invoices"  # 网关支付发起代扣请求失败
        mode = {
            "error": {
                "code": "SERVER_ERROR",
                "description": "The server encountered an error. The incident has been reported to admins.",
                "metadata": None
            }
        }
        self.update(api, mode)

    def update_razorpay_ebank_success(self):
        api = "/v1/invoices"  # 网关支付发起代扣请求成功，会返回支付链接
        mode = {
            "id": "inv_ETbjFTYwBtN1xM",
            "entity": "invoice",
            "receipt": "DSQ12345678904",
            "invoice_number": "DSQ12345678904",
            "customer_id": "cust_ELHZpCNsx1Xrs2",
            "customer_details": {
                "id": "cust_ELHZpCNsx1Xrs2",
                "name": "Jacky",
                "email": "xxx@qq.com",
                "contact": "123456789",
                "gstin": None,
                "billing_address": None,
                "shipping_address": None,
                "customer_name": "Jacky",
                "customer_email": "xxx@qq.com",
                "customer_contact": "123456789"
            },
            "order_id": global_razorpay_ebank_channel_key,  # 查询明细需要用到的流水号
            "line_items": [],
            "payment_id": None,
            "status": "issued",
            "expire_by": 1793630556,
            "issued_at": 1584518344,
            "paid_at": None,
            "cancelled_at": None,
            "expired_at": None,
            "sms_status": None,
            "email_status": None,
            "date": 1584518344,
            "terms": None,
            "partial_payment": "false",
            "gross_amount": 670042,
            "tax_amount": 0,
            "taxable_amount": 0,
            "amount": 670042,
            "amount_paid": 0,
            "amount_due": 670042,
            "currency": "INR",
            "currency_symbol": "₹",
            "description": "Payment Link for this purpose - cvb.",
            "notes": [],
            "comment": None,
            "short_url": global_ebank_payurl,  # 网关支付链接
            "view_less": "true",
            "billing_start": None,
            "billing_end": None,
            "type": "link",
            "group_taxes_discounts": "false",
            "created_at": 1584518344
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_success(self):
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [{
                "id": global_razorpay_ebank_channel_key,  # 查询明细需要用到的流水号
                "entity": "order",
                "amount": 25000,
                "amount_paid": 0,
                "amount_due": 25000,
                "currency": "INR",
                "receipt": "RBIZ403182561824119706",
                "offer_id": None,
                "status": "paid",  # status=paid表示代扣成功
                "attempts": 1,
                "notes": [],
                "created_at": 1584520891
            }]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_authorized(self):
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,
                    "entity": "order",
                    "amount": 505600,
                    "amount_paid": 0,
                    "amount_due": 505600,
                    "currency": "INR",
                    "receipt": "RBIZ409067701132683938",
                    "payments": {
                        "entity": "collection",
                        "count": 1,
                        "items": [
                            {
                                "id": global_razorpay_ebank_channel_key,
                                "entity": "payment",
                                "amount": 505600,
                                "currency": "INR",
                                "status": "authorized",  # 这个状态表示需要进行订单捕获
                                "order_id": "order_FZnz7nHHojUtbY",
                                "invoice_id": "inv_FZnz7lFHVh0wOa",
                                "international": False,
                                "method": "card",
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": False,
                                "description": "#inv_FZnz7lFHVh0wOa",
                                "card_id": "card_FZnzzDdhS2GCGH",
                                "card": {
                                    "id": "card_FZnzzDdhS2GCGH",
                                    "entity": "card",
                                    "name": "ashwin nagaraj",
                                    "last4": "6399",
                                    "network": "Visa",
                                    "type": "debit",
                                    "issuer": "SBIN",
                                    "international": False,
                                    "emi": False,
                                    "sub_type": "consumer"
                                },
                                "bank": None,
                                "wallet": None,
                                "vpa": None,
                                "email": "ashwingn1988@gmail.com",
                                "contact": "+919066776888",
                                "customer_id": "cust_FZnz7lXzneIuqk",
                                "token_id": "token_FZnzzHp4e8gAqT",
                                "notes": [

                                ],
                                "fee": None,
                                "tax": None,
                                "error_code": None,
                                "error_description": None,
                                "error_source": None,
                                "error_step": None,
                                "error_reason": None,
                                "acquirer_data": {
                                    "auth_code": "177434"
                                },
                                "created_at": 1599408682
                            }
                        ]
                    },
                    "offer_id": None,
                    "status": "attempted",
                    "attempts": 1,
                    "notes": [

                    ],
                    "created_at": 1901094228  # 时间设置到2030年，一直不会失效
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_two_authorized(self):
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,
                    "entity": "order",
                    "amount": 505600,
                    "amount_paid": 0,
                    "amount_due": 505600,
                    "currency": "INR",
                    "receipt": "RBIZ409067701132683938",
                    "payments": {
                        "entity": "collection",
                        "count": 2,
                        "items": [
                            {
                                "id": global_razorpay_ebank_channel_key,
                                "entity": "payment",
                                "amount": 505600,
                                "currency": "INR",
                                "status": "authorized",  # 这个状态表示需要进行订单捕获
                                "order_id": "order_FZnz7nHHojUtbY",
                                "invoice_id": "inv_FZnz7lFHVh0wOa",
                                "international": False,
                                "method": "card",
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": False,
                                "description": "#inv_FZnz7lFHVh0wOa",
                                "card_id": "card_FZnzzDdhS2GCGH",
                                "card": {
                                    "id": "card_FZnzzDdhS2GCGH",
                                    "entity": "card",
                                    "name": "ashwin nagaraj",
                                    "last4": "6399",
                                    "network": "Visa",
                                    "type": "debit",
                                    "issuer": "SBIN",
                                    "international": False,
                                    "emi": False,
                                    "sub_type": "consumer"
                                },
                                "bank": None,
                                "wallet": None,
                                "vpa": None,
                                "email": "ashwingn1988@gmail.com",
                                "contact": "+919066776888",
                                "customer_id": "cust_FZnz7lXzneIuqk",
                                "token_id": "token_FZnzzHp4e8gAqT",
                                "notes": [

                                ],
                                "fee": None,
                                "tax": None,
                                "error_code": None,
                                "error_description": None,
                                "error_source": None,
                                "error_step": None,
                                "error_reason": None,
                                "acquirer_data": {
                                    "auth_code": "177434"
                                },
                                "created_at": 1599408682
                            },
                            {
                                "id": global_razorpay_collect_channel_key1,
                                "entity": "payment",
                                "amount": 505600,
                                "currency": "INR",
                                "status": "authorized",  # 这个状态表示需要进行订单捕获
                                "order_id": "order_FZnz7nHHojUtbY",
                                "invoice_id": "inv_FZnz7lFHVh0wOa",
                                "international": False,
                                "method": "card",
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": False,
                                "description": "#inv_FZnz7lFHVh0wOa",
                                "card_id": "card_FZnzzDdhS2GCGH",
                                "card": {
                                    "id": "card_FZnzzDdhS2GCGH",
                                    "entity": "card",
                                    "name": "ashwin nagaraj",
                                    "last4": "6399",
                                    "network": "Visa",
                                    "type": "debit",
                                    "issuer": "SBIN",
                                    "international": False,
                                    "emi": False,
                                    "sub_type": "consumer"
                                },
                                "bank": None,
                                "wallet": None,
                                "vpa": None,
                                "email": "ashwingn1988@gmail.com",
                                "contact": "+919066776888",
                                "customer_id": "cust_FZnz7lXzneIuqk",
                                "token_id": "token_FZnzzHp4e8gAqT",
                                "notes": [

                                ],
                                "fee": None,
                                "tax": None,
                                "error_code": None,
                                "error_description": None,
                                "error_source": None,
                                "error_step": None,
                                "error_reason": None,
                                "acquirer_data": {
                                    "auth_code": "177434"
                                },
                                "created_at": 1599408682
                            }
                        ]
                    },
                    "offer_id": None,
                    "status": "attempted",
                    "attempts": 1,
                    "notes": [

                    ],
                    "created_at": 1901094228  # 时间设置到2030年，一直不会失效
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_authorized_timeout(self):
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,
                    "entity": "order",
                    "amount": 505600,
                    "amount_paid": 0,
                    "amount_due": 505600,
                    "currency": "INR",
                    "receipt": "RBIZ409067701132683938",
                    "payments": {
                        "entity": "collection",
                        "count": 1,
                        "items": [
                            {
                                "id": global_razorpay_ebank_channel_key,
                                "entity": "payment",
                                "amount": 505600,
                                "currency": "INR",
                                "status": "authorized",  # 这个状态表示需要进行订单捕获
                                "order_id": "order_FZnz7nHHojUtbY",
                                "invoice_id": "inv_FZnz7lFHVh0wOa",
                                "international": False,
                                "method": "card",
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": False,
                                "description": "#inv_FZnz7lFHVh0wOa",
                                "card_id": "card_FZnzzDdhS2GCGH",
                                "card": {
                                    "id": "card_FZnzzDdhS2GCGH",
                                    "entity": "card",
                                    "name": "ashwin nagaraj",
                                    "last4": "6399",
                                    "network": "Visa",
                                    "type": "debit",
                                    "issuer": "SBIN",
                                    "international": False,
                                    "emi": False,
                                    "sub_type": "consumer"
                                },
                                "bank": None,
                                "wallet": None,
                                "vpa": None,
                                "email": "ashwingn1988@gmail.com",
                                "contact": "+919066776888",
                                "customer_id": "cust_FZnz7lXzneIuqk",
                                "token_id": "token_FZnzzHp4e8gAqT",
                                "notes": [

                                ],
                                "fee": None,
                                "tax": None,
                                "error_code": None,
                                "error_description": None,
                                "error_source": None,
                                "error_step": None,
                                "error_reason": None,
                                "acquirer_data": {
                                    "auth_code": "177434"
                                },
                                "created_at": 1599408682
                            }
                        ]
                    },
                    "offer_id": None,
                    "status": "attempted",
                    "attempts": 1,
                    "notes": [

                    ],
                    "created_at": 1585561428,  # 关单时间为created_at+代码写死的20min+KV配置的5min
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_capture_success(self):
        api = "/v1/payments/" + global_razorpay_ebank_channel_key + "/capture"
        mode = {
            "id": "pay_29QQoUBi66xm2f",
            "entity": "payment",
            "amount": 5000,
            "currency": "INR",
            "status": "captured",  # captured表示订单捕获成功？
            "order_id": None,
            "invoice_id": None,
            "international": False,
            "method": "wallet",
            "amount_refunded": 0,
            "refund_status": None,
            "captured": True,
            "description": "Purchase Description",
            "card_id": None,
            "bank": None,
            "wallet": "freecharge",
            "vpa": None,
            "email": "a@b.com",
            "contact": "91xxxxxxxx",
            "notes": {
                "merchant_order_id": "order id"
            },
            "fee": 1438,
            "tax": 188,
            "error_code": None,
            "error_description": None,
            "created_at": 1400826750
        }
        self.update(api, mode)

    def update_razorpay_ebank_capture_fail(self):
        # 模拟确认异常
        api = "/v1/payments/" + global_razorpay_ebank_channel_key + "/capture"
        mode = {
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_success_new(self):
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,
                    "entity": "order",
                    "amount": 502512,
                    "amount_paid": 502512,
                    "amount_due": 0,
                    "currency": "INR",
                    "receipt": "RBIZ407028422106154656",
                    "payments": {
                        "entity": "collection",
                        "count": 1,
                        "items": [
                            {
                                "id": "pay_F9alICLckX8lU2",
                                "entity": "payment",
                                "amount": 502512,
                                "currency": "INR",
                                "status": "captured",
                                "order_id": "order_F9ahj8uPts5okK",
                                "invoice_id": "inv_F9ahj802sDIkZQ",
                                "international": False,
                                "method": global_razorpay_ebank_channel_option,
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": True,
                                "description": "#inv_F9ahj802sDIkZQ",
                                "card_id": None,
                                "card": None,
                                "bank": global_razorpay_ebank_payment_mode,
                                "wallet": None,
                                "vpa": None,
                                "email": "wangxiaoming@google.com",
                                "contact": "+919150336243",
                                "customer_id": "cust_F9X5A2O4Pc3l3g",
                                "notes": [

                                ],
                                "fee": global_razorpay_ebank_service_fee,
                                "tax": global_razorpay_ebank_service_tax,
                                "error_code": None,
                                "error_description": None,
                                "error_source": None,
                                "error_step": None,
                                "error_reason": None,
                                "created_at": 1593685223
                            }
                        ]
                    },
                    "offer_id": None,
                    "status": "paid",  # status=paid表示代扣成功
                    "attempts": 1,
                    "notes": [

                    ],
                    "created_at": 1593685021
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_success_002(self):
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,
                    "entity": "order",
                    "amount": 502512,
                    "amount_paid": 502512,
                    "amount_due": 0,
                    "currency": "INR",
                    "receipt": "RBIZ407028422106154656",
                    "payments": {
                        "entity": "collection",
                        "count": 1,
                        "items": [
                            {
                                "id": "pay_F9vrlyqo31W0Hf",
                                "entity": "payment",
                                "amount": 304200,
                                "currency": "INR",
                                "status": "captured",
                                "order_id": "order_F9vrLZevxBbZHK",
                                "invoice_id": "inv_F9vrLZ58ZGLRsl",
                                "international": False,
                                "method": global_razorpay_ebank_channel_option_card,
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": True,
                                "description": "#inv_F9vrLZ58ZGLRsl",
                                "card_id": "card_F9vrm4kwiaQbmD",
                                "card": {
                                    "id": "card_F9vrm4kwiaQbmD",
                                    "entity": "card",
                                    "name": "Animanand Kindo",
                                    "last4": "1796",
                                    "network": global_razorpay_ebank_payment_mode_card,
                                    "type": "debit",
                                    "issuer": "BKID",
                                    "international": False,
                                    "emi": False
                                },
                                "bank": None,
                                "wallet": None,
                                "vpa": None,
                                "email": "animanandkindo1234567890@gmail.com",
                                "contact": "+918235293673",
                                "customer_id": "cust_F3yTRgJj0Wx9Db",
                                "token_id": "token_F9vrm8Kn8NP4tW",
                                "notes": [],
                                "fee": global_razorpay_ebank_service_fee,
                                "tax": global_razorpay_ebank_service_tax,
                                "error_code": None,
                                "error_description": None,
                                "error_source": None,
                                "error_step": None,
                                "error_reason": None,
                                "created_at": 1593759546
                            }
                        ]
                    },
                    "offer_id": None,
                    "status": "paid",  # status=paid表示代扣成功
                    "attempts": 1,  # 不要改
                    "notes": [

                    ],
                    "created_at": 1593685021
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_success_003(self):
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,
                    "entity": "order",
                    "amount": 502512,
                    "amount_paid": 502512,
                    "amount_due": 0,
                    "currency": "INR",
                    "receipt": "RBIZ407028422106154656",
                    "payments": {
                        "entity": "collection",
                        "count": 2,
                        "items": [
                            {
                                "id": "pay_F9qiS8v2wTIW0U",
                                "entity": "payment",
                                "amount": 304200,
                                "currency": "INR",
                                "status": "failed",
                                "order_id": "order_F9qhuBHaC4R6cG",
                                "invoice_id": "inv_F9qhuAfDXx58FO",
                                "international": False,
                                "method": "upi",
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": False,
                                "description": "#inv_F9qhuAfDXx58FO",
                                "card_id": None,
                                "card": None,
                                "bank": None,
                                "wallet": None,
                                "vpa": "9700044435@ybl",
                                "email": "divakar3535@gmail.com",
                                "contact": "+919700044435",
                                "customer_id": "cust_F1f5RSGJvJOgZu",
                                "notes": [],
                                "fee": None,
                                "tax": None,
                                "error_code": "GATEWAY_ERROR",
                                "error_description": "Transaction failed due to insufficient funds.",
                                "error_source": "customer",
                                "error_step": "payment_debit_request",
                                "error_reason": "insufficient_funds",
                                "created_at": 1593741408
                            },
                            {
                                "id": "pay_F9qnBMe7ZsO698",
                                "entity": "payment",
                                "amount": 304200,
                                "currency": "INR",
                                "status": "captured",
                                "order_id": "order_F9qhuBHaC4R6cG",
                                "invoice_id": "inv_F9qhuAfDXx58FO",
                                "international": False,
                                "method": global_razorpay_collect_channel_mode_upi,
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": True,
                                "description": "#inv_F9qhuAfDXx58FO",
                                "card_id": None,
                                "card": None,
                                "bank": None,
                                "wallet": None,
                                "vpa": "9700044435@ybl",
                                "email": "divakar3535@gmail.com",
                                "contact": "+919700044435",
                                "customer_id": "cust_F1f5RSGJvJOgZu",
                                "notes": [],
                                "fee": global_razorpay_ebank_service_fee,
                                "tax": global_razorpay_ebank_service_tax,
                                "error_code": None,
                                "error_description": None,
                                "error_source": None,
                                "error_step": None,
                                "error_reason": None,
                                "created_at": 1593741677
                            }
                        ]
                    },
                    "offer_id": None,
                    "status": "paid",  # status=paid表示代扣成功
                    "attempts": 1,  # 不要改
                    "notes": [

                    ],
                    "created_at": 1593685021
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_fail_001(self):
        # 超时过期关单，关单时间为created_at+代码写死的20min+KV配置的5min
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,  # 查询明细需要用到的流水号
                    "entity": "order",
                    "amount": 502512,
                    "amount_paid": 0,
                    "amount_due": 502512,
                    "currency": "INR",
                    "receipt": "RBIZ403305012085873967",
                    "payments": {
                        "entity": "collection",
                        "count": 0,
                        "items": [

                        ]
                    },
                    "offer_id": None,
                    "status": "created",  # 非paid都是处理中
                    "attempts": 0,
                    "notes": [

                    ],
                    "created_at": 1585561428,  # 关单时间为created_at+代码写死的20min+KV配置的5min
                    "checkout_config_id": None
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_fail_002(self):
        # 超时过期关单，关单时间为created_at+代码写死的20min+KV配置的5min
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,  # 查询明细需要用到的流水号
                    "entity": "order",
                    "amount": 502512,
                    "amount_paid": 0,
                    "amount_due": 502512,
                    "currency": "INR",
                    "receipt": "RBIZ403305012085873967",
                    "payments": {
                        "entity": "collection",
                        "count": 1,
                        "items": [
                            {
                                "id": "pay_F0pJ4ih1wuMwOe",
                                "entity": "payment",
                                "amount": 223400,
                                "currency": "INR",
                                "status": "failed",
                                "order_id": "order_F0pGrhSdea7qbm",
                                "invoice_id": "inv_F0pGrgmRlcwn0t",
                                "international": False,
                                "method": global_razorpay_ebank_channel_option_card,
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": False,
                                "description": "#inv_F0pGrgmRlcwn0t",
                                "card_id": "card_F0pJ4pWYw52KBq",
                                "card": {
                                    "id": "card_F0pJ4pWYw52KBq",
                                    "entity": "card",
                                    "name": "SWAIN SAGAR",
                                    "last4": "1168",
                                    "network": global_razorpay_ebank_payment_mode_card,
                                    "type": "debit",
                                    "issuer": "SBIN",
                                    "international": False,
                                    "emi": False
                                },
                                "bank": None,
                                "wallet": None,
                                "vpa": None,
                                "email": "swainsagar060@gmail.com",
                                "contact": "+917655070225",
                                "customer_id": "cust_EwRAmi5zwi8CeP",
                                "notes": [],
                                "fee": None,
                                "tax": None,
                                "error_code": "BAD_REQUEST_ERROR",
                                "error_description": global_razorpay_ebank_fail_message,
                                "error_source": "customer",
                                "error_step": "payment_authentication",
                                "error_reason": "payment_timed_out",
                                "created_at": 1591771384
                            }
                        ]
                    },
                    "offer_id": None,
                    "status": "attempted",  # 非paid都是处理中
                    "attempts": 1,
                    "notes": [

                    ],
                    "created_at": 1585561428,  # 关单时间为created_at+代码写死的20min+KV配置的5min
                    "checkout_config_id": None
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_fail_003(self):
        # 超时过期关单，关单时间为created_at+代码写死的20min+KV配置的5min
        # option、mode为netbanking且用户支付过多次均失败，失败原因取created_at大的的那个
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,  # 查询明细需要用到的流水号
                    "entity": "order",
                    "amount": 502512,
                    "amount_paid": 0,
                    "amount_due": 502512,
                    "currency": "INR",
                    "receipt": "RBIZ403305012085873967",
                    "payments": {
                        "entity": "collection",
                        "count": 2,
                        "items": [
                            {
                                "id": "pay_F9tEtrxKzdbHf3",
                                "entity": "payment",
                                "amount": 307200,
                                "currency": "INR",
                                "status": "failed",
                                "order_id": "order_F9t8oSAKChmUoS",
                                "invoice_id": "inv_F9t8oRMgrkzQlb",
                                "international": False,
                                "method": "netbanking",
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": False,
                                "description": "#inv_F9t8oRMgrkzQlb",
                                "card_id": None,
                                "card": None,
                                "bank": "FDRL",
                                "wallet": None,
                                "vpa": None,
                                "email": "khubchand.m35@gamil.com",
                                "contact": "+919821961203",
                                "customer_id": "cust_EsALgv00964wcV",
                                "notes": [],
                                "fee": None,
                                "tax": None,
                                "error_code": "BAD_REQUEST_ERROR",
                                "error_description": "Payment was not completed on time.",
                                "error_source": "customer",
                                "error_step": "payment_authentication",
                                "error_reason": "payment_timed_out",
                                "created_at": 1593750111
                            },
                            {
                                "id": "pay_F9tBfRf9NmZ7AA",
                                "entity": "payment",
                                "amount": 307200,
                                "currency": "INR",
                                "status": "failed",
                                "order_id": "order_F9t8oSAKChmUoS",
                                "invoice_id": "inv_F9t8oRMgrkzQlb",
                                "international": False,
                                "method": global_razorpay_ebank_channel_option,
                                "amount_refunded": 0,
                                "refund_status": None,
                                "captured": False,
                                "description": "#inv_F9t8oRMgrkzQlb",
                                "card_id": None,
                                "card": None,
                                "bank": global_razorpay_ebank_payment_mode,
                                "wallet": None,
                                "vpa": None,
                                "email": "khubchand.m35@gamil.com",
                                "contact": "+919821961203",
                                "customer_id": "cust_EsALgv00964wcV",
                                "notes": [],
                                "fee": None,
                                "tax": None,
                                "error_code": "BAD_REQUEST_ERROR",
                                "error_description": global_razorpay_ebank_fail_message,
                                "error_source": "customer",
                                "error_step": "payment_authentication",
                                "error_reason": "payment_timed_out",
                                "created_at": 1593750294
                            }
                        ]
                    },
                    "offer_id": None,
                    "status": "attempted",  # 非paid都是处理中
                    "attempts": 2,
                    "notes": [

                    ],
                    "created_at": 1585561428,  # 关单时间为created_at+代码写死的20min+KV配置的5min
                    "checkout_config_id": None
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_fail_not_exist(self):
        # 交易不存在
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 0,
            "items": [

            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_process(self):
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,  # 查询明细需要用到的流水号
                    "entity": "order",
                    "amount": 25000,
                    "amount_paid": 0,
                    "amount_due": 25000,
                    "currency": "INR",
                    "receipt": "RBIZ403182561824119706",
                    "payments": {
                        "entity": "collection",
                        "count": 0,
                        "items": [

                        ]
                    },
                    "offer_id": None,
                    "status": "Issued",  # 非paid都是处理中
                    "attempts": 0,
                    "notes": [

                    ],
                    "created_at": 1901094228  # 时间设置到2030年，一直不会失效
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_cancloseorder(self):
        # razorpay_ebank用户拿到链接从未操作过："attempts": 0
        api = "/v1/orders"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_ebank_channel_key,
                    "entity": "order",
                    "amount": 502512,
                    "amount_paid": 0,
                    "amount_due": 502512,
                    "currency": "INR",
                    "receipt": "RBIZ404299380477309388",
                    "offer_id": None,
                    "status": "created",
                    "attempts": 0,  # 用户未还过款的标志，重要
                    "notes": [

                    ],
                    "created_at": 1903661340
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_fail_detail_001(self):
        # razorpay代扣失败明细查询返回为空：用户没有操作过支付链接
        api = "/v1/orders/" + global_razorpay_ebank_channel_key + "/payments"
        mode = {
            "entity": "collection",
            "count": 0,
            "items": []
        }
        self.update(api, mode)

    def update_razorpay_ebank_query_fail_detail_002(self):
        # razorpay代扣失败明细查询：用户支付了多次都失败
        api = "/v1/orders/" + global_razorpay_ebank_channel_key + "/payments"  # global_razorpay_ebank_channel_key依赖于easymock的配置，如果easy mock被改了会导致失败
        mode = {
            "entity": "collection",
            "count": 2,
            "items": [
                {
                    "id": "pay_EeDnD6A0Y7NocZ",
                    "entity": "payment",
                    "amount": 558500,
                    "currency": "INR",
                    "status": "failed",
                    "order_id": global_razorpay_ebank_channel_key,
                    "invoice_id": "inv_EeDkxVLvqcvInj",
                    "international": "false",
                    "amount_refunded": 0,
                    "refund_status": None,
                    "captured": "false",
                    "description": "#inv_EeDkxVLvqcvInj",
                    "card_id": None,
                    "bank": "BARB_R",
                    "wallet": None,
                    "vpa": None,
                    "email": "tajmohammad78335@gmail.com",
                    "contact": "+919855559453",
                    "customer_id": "cust_EeDkxVt2wpmljZ",
                    "notes": [],
                    "fee": None,
                    "tax": None,
                    "error_code": "BAD_REQUEST_ERROR",
                    "method": global_razorpay_ebank_payment_mode,
                    "error_description": global_razorpay_ebank_fail_message,
                    "created_at": 1586835792  # 取时间大的最后一次原因来更新,1586835792 > 1586835693
                },
                {
                    "id": "pay_EeDlTCxxX53wB5",
                    "entity": "payment",
                    "amount": 558500,
                    "currency": "INR",
                    "status": "failed",
                    "order_id": global_razorpay_ebank_channel_key,
                    "invoice_id": "inv_EeDkxVLvqcvInj",
                    "international": "false",
                    "method": "netbanking",
                    "amount_refunded": 0,
                    "refund_status": None,
                    "captured": "false",
                    "description": "#inv_EeDkxVLvqcvInj",
                    "card_id": None,
                    "bank": "BARB_R",
                    "wallet": None,
                    "vpa": None,
                    "email": "tajmohammad78335@gmail.com",
                    "contact": "+919855559453",
                    "customer_id": "cust_EeDkxVt2wpmljZ",
                    "notes": [],
                    "fee": None,
                    "tax": None,
                    "error_code": "BAD_REQUEST_ERROR",
                    "error_description": "Payment was not completed on time.",
                    "created_at": 1586835693
                }
            ]
        }
        self.update(api, mode)

    # def update_razorpay_ebank_query_success_detail(self):
    #     # razorpay代扣成功明细查询：用户支付了多次，其中有一次成功的，代扣成功需要通过该接口查询到支付方式：已取消调用该接口
    #     api = "/v1/orders/" + global_razorpay_ebank_channel_key + "/payments"
    #     mode = {
    #         "entity": "collection",
    #         "count": 2,
    #         "items": [
    #             {
    #                 "id": "pay_EeekNAcGakF5s1",
    #                 "entity": "payment",
    #                 "amount": 50700,
    #                 "currency": "INR",
    #                 "status": "captured",
    #                 "captured": "true",  # "status": "captured"且"captured": "true" 表示代扣成功
    #                 "order_id": global_razorpay_ebank_channel_key,
    #                 "invoice_id": "inv_EeeZHvCyazEH6j",
    #                 "international": "false",
    #                 "method": global_razorpay_ebank_payment_mode,
    #                 "amount_refunded": 0,
    #                 "refund_status": None,
    #                 "description": "#inv_EeeZHvCyazEH6j",
    #                 "card_id": None,
    #                 "bank": None,
    #                 "wallet": None,
    #                 "vpa": "7731009729@ybl",
    #                 "email": "prash.fresh1994@gmail.com",
    #                 "contact": "+917731009729",
    #                 "customer_id": "cust_EeeYy4lkRQfVjG",
    #                 "notes": [],
    #                 "fee": global_razorpay_ebank_service_fee,  # 总费用=服务费+税费，fee-tax保存到withhold_receipt_service_charge
    #                 "tax": global_razorpay_ebank_service_tax,  # 税费，保存到withhold_receipt_service_tax
    #                 "error_code": None,
    #                 "error_description": None,  # 代扣成功不会返回失败原因
    #                 "created_at": 1586930714
    #             },
    #             {
    #                 "id": "pay_EeefuupN7AuExw",
    #                 "entity": "payment",
    #                 "amount": 50700,
    #                 "currency": "INR",
    #                 "status": "failed",
    #                 "order_id": global_razorpay_ebank_channel_key,
    #                 "invoice_id": "inv_EeeZHvCyazEH6j",
    #                 "international": "false",
    #                 "method": "upi",
    #                 "amount_refunded": 0,
    #                 "refund_status": None,
    #                 "captured": "false",
    #                 "description": "#inv_EeeZHvCyazEH6j",
    #                 "card_id": None,
    #                 "bank": None,
    #                 "wallet": None,
    #                 "vpa": "prash.fresh1994-1@okhdfcbank",
    #                 "email": "prash.fresh1994@gmail.com",
    #                 "contact": "+917731009729",
    #                 "customer_id": "cust_EeeYy4lkRQfVjG",
    #                 "notes": [],
    #                 "fee": None,
    #                 "tax": None,
    #                 "error_code": "GATEWAY_ERROR",
    #                 "error_description": "Payment processing failed due to error at bank or wallet gateway",
    #                 "created_at": 1586930461
    #             }
    #         ]
    #     }
    #     self.update(api, mode)

    def update_bind_success_razorpay_steps1(self):
        # razorpay绑卡创建联系人
        api = "/v1/contacts"
        mode = {
            "id": global_razorpay_withdraw_contact_id,
            "entity": "contact",
            "name": "first middle last",
            "contact": "",
            "email": "wangxiaoming@google.com",
            "type": "customer",
            "reference_id": "",
            "batch_id": None,
            "active": "true",  # true成功，false失败
            "notes": {
                "product": "contact"
            },
            "created_at": "1583303041"
        }
        self.update(api, mode)

    def update_bind_fail_razorpay_steps1(self):
        # razorpay绑卡创建联系人
        api = "/v1/contacts"
        mode = {
            "id": global_razorpay_withdraw_contact_id,
            "entity": "contact",
            "name": "first middle last",
            "contact": "",
            "email": "wangxiaoming@google.com",
            "type": "customer",
            "reference_id": "",
            "batch_id": None,
            "active": "false",  # true成功，false失败
            "notes": {
                "product": "contact"
            },
            "created_at": "1583303041"
        }
        self.update(api, mode)

    def update_bind_success_razorpay_steps2(self):
        # razorpay创建资金账户
        api = "/v1/fund_accounts"
        mode = {
            "id": global_razorpay_withdraw_fund_account_id,
            "entity": "fund_account",
            "contact_id": global_razorpay_withdraw_contact_id,
            "account_type": "bank_account",
            "bank_account": {
                "ifsc": "YESB0000262",
                "bank_name": "Yes Bank",
                "name": "JOHN DOE",
                "notes": [

                ],
                "account_number": "026291800001191"
            },
            "batch_id": None,
            "active": "true",  # true成功，false失败
            "created_at": 1583303041
        }
        self.update(api, mode)

    def update_razorpay_withdraw_balance_success(self):
        # razorpay代付余额查询
        api = "/v1/transactions"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [{
                "id": "txn_EiApcnOGFzMMmq",
                "entity": "transaction",
                "account_number": "2323230035394297",
                "amount": 10472,
                "currency": "INR",
                "credit": 0,
                "debit": 10472,
                "balance": global_razorpay_withdraw_balance,  # razorpay余额
                "source": {
                    "id": global_razorpay_withdraw_inner_key,
                    "entity": "payout",
                    "fund_account_id": "fa_EiAeBLTwZNgHCH",
                    "amount": 10000,
                    "notes": {
                        "product": "withdraw"
                    },
                    "fees": 472,
                    "tax": 72,
                    "status": "processing",
                    "utr": None,
                    "mode": "IMPS",
                    "created_at": 1587698724
                },
                "created_at": 1587698724
            }]
        }
        self.update(api, mode)

    # def update_razorpay_withdraw_balance_fail(self):
    #     # razorpay代付余额查询
    #     api = "/v1/transactions"
    #     mode = {
    #         "entity": "collection",
    #         "count": 0,
    #         "items": [{
    #
    #         }]
    #     }
    #     self.update(api, mode)

    def update_razorpay_withdraw_balance_fail(self):
        # razorpay代付余额查询
        api = "/v1/transactions"
        mode = {
            "error": {
                "code": "BAD_REQUEST_ERROR",
                "description": global_withdraw_failed_message,
                "metadata": {

                },
                "field": "amount"
            }
        }
        self.update(api, mode)

    def update_razorpay_withdraw_success(self):
        # razorpay代付请求，razorpay代付请求不管status状态都是代付处理中
        api = "/v1/payouts"
        method = "post"
        mode = {
            "id": global_razorpay_withdraw_inner_key,
            "entity": "payout",
            "fund_account_id": "fa_EiAeBLTwZNgHCH",
            "amount": 10000,
            "currency": "INR",
            "notes": {
                "product": "withdraw"
            },
            "fees": 472,
            "tax": 72,
            "status": "processing",  # 代付请求返回的所有状态都是处理中必须通过查询接口，即使返回processed
            "purpose": "payout",
            "utr": None,
            "mode": "IMPS",
            "reference_id": "bf1623ba1fc244d8816cce21908ded5c",
            "narration": "KN Fund Transfer",
            "batch_id": None,
            "failure_reason": None,
            "created_at": 1587698724
        }
        self.update(api, mode, method)

    def update_razorpay_withdraw_error(self):
        # razorpay代付请求异常，razorpay代付请求不管status状态都是代付处理中
        api = "/v1/payouts"
        method = "post"
        mode = {
            "error": {
                "code": "BAD_REQUEST_ERROR",
                "description": global_withdraw_failed_message,
                "metadata": {

                },
                "field": "amount"
            }
        }
        self.update(api, mode, method)

    def update_razorpay_withdraw_query_not_exists(self):
        # razorpay代付结果查询请求返回交易不存在
        api = "/v1/payouts"
        method = "get"
        mode = {
            "entity": "collection",
            "count": 0,
            "items": [

            ]
        }
        self.update(api, mode, method)

    def update_razorpay_withdraw_query_success(self):
        # razorpay代付结果查询请求
        api = "/v1/payouts"
        method = "get"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [{
                "id": global_razorpay_withdraw_inner_key,
                "entity": "payout",
                "fund_account_id": "fa_EiAeBLTwZNgHCH",
                "amount": 10000,
                "currency": "INR",
                "notes": {
                    "product": "withdraw"
                },
                "fees": 472,
                "tax": 72,
                "status": global_razorpay_withdraw_success_processed,
                # processing处理中、queued代付中、pending代付中、rejected代付失败、processed代付成功、cancelled代付失败、reversed代付失败
                "purpose": "payout",
                "utr": None,
                "mode": global_razorpay_withdraw_mode,
                "reference_id": "bf1623ba1fc244d8816cce21908ded5c",
                "narration": "KN Fund Transfer",
                "batch_id": None,
                "failure_reason": None,
                "created_at": 1587698724
            }]
        }
        self.update(api, mode, method)

    def update_razorpay_withdraw_query_fail_001(self):
        # razorpay代付结果查询请求
        api = "/v1/payouts"
        method = "get"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [{
                "id": global_razorpay_withdraw_inner_key,
                "entity": "payout",
                "fund_account_id": "fa_EiAeBLTwZNgHCH",
                "amount": 10000,
                "currency": "INR",
                "notes": {
                    "product": "withdraw"
                },
                "fees": 472,
                "tax": 72,
                "status": global_razorpay_withdraw_fail_rejected,
                # processing处理中、queued代付中、pending代付中、rejected代付失败、processed代付成功、cancelled代付失败、reversed代付失败
                "purpose": "payout",
                "utr": None,
                "mode": global_razorpay_withdraw_mode,
                "reference_id": "bf1623ba1fc244d8816cce21908ded5c",
                "narration": "KN Fund Transfer",
                "batch_id": None,
                "failure_reason": global_withdraw_failed_message,
                "created_at": 1587698724
            }]
        }
        self.update(api, mode, method)

    def update_razorpay_withdraw_query_fail_002(self):
        # razorpay代付结果查询请求
        api = "/v1/payouts"
        method = "get"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [{
                "id": global_razorpay_withdraw_inner_key,
                "entity": "payout",
                "fund_account_id": "fa_EiAeBLTwZNgHCH",
                "amount": 10000,
                "currency": "INR",
                "notes": {
                    "product": "withdraw"
                },
                "fees": 472,
                "tax": 72,
                "status": global_razorpay_withdraw_fail_cancelled,
                # processing处理中、queued代付中、pending代付中、rejected代付失败、processed代付成功、cancelled代付失败、reversed代付失败
                "purpose": "payout",
                "utr": None,
                "mode": global_razorpay_withdraw_mode,
                "reference_id": "bf1623ba1fc244d8816cce21908ded5c",
                "narration": "KN Fund Transfer",
                "batch_id": None,
                "failure_reason": global_withdraw_failed_message,
                "created_at": 1587698724
            }]
        }
        self.update(api, mode, method)

    def update_razorpay_withdraw_query_fail_003(self):
        # razorpay代付结果查询请求
        api = "/v1/payouts"
        method = "get"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [{
                "id": global_razorpay_withdraw_inner_key,
                "entity": "payout",
                "fund_account_id": "fa_EiAeBLTwZNgHCH",
                "amount": 10000,
                "currency": "INR",
                "notes": {
                    "product": "withdraw"
                },
                "fees": 472,
                "tax": 72,
                "status": global_razorpay_withdraw_fail_reversed,
                # processing处理中、queued代付中、pending代付中、processed代付成功、rejected代付失败、cancelled代付失败、reversed代付失败
                "purpose": "payout",
                "utr": None,
                "mode": global_razorpay_withdraw_mode,
                "reference_id": "bf1623ba1fc244d8816cce21908ded5c",
                "narration": "KN Fund Transfer",
                "batch_id": None,
                "failure_reason": global_withdraw_failed_message,
                "created_at": 1587698724
            }]
        }
        self.update(api, mode, method)

    def update_razorpay_withdraw_query_process_001(self):
        # razorpay代付结果查询请求
        api = "/v1/payouts"
        method = "get"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [{
                "id": global_razorpay_withdraw_inner_key,
                "entity": "payout",
                "fund_account_id": "fa_EiAeBLTwZNgHCH",
                "amount": 10000,
                "currency": "INR",
                "notes": {
                    "product": "withdraw"
                },
                "fees": 472,
                "tax": 72,
                "status": global_razorpay_withdraw_process_processing,
                # processing处理中、queued代付中、pending代付中、rejected代付失败、processed代付成功、cancelled代付失败、reversed代付失败
                "purpose": "payout",
                "utr": None,
                "mode": global_razorpay_withdraw_mode,
                "reference_id": "bf1623ba1fc244d8816cce21908ded5c",
                "narration": "KN Fund Transfer",
                "batch_id": None,
                "failure_reason": global_withdraw_failed_message,
                "created_at": 1587698724
            }]
        }
        self.update(api, mode, method)

    def update_razorpay_withdraw_query_process_002(self):
        # razorpay代付结果查询请求
        api = "/v1/payouts"
        method = "get"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [{
                "id": global_razorpay_withdraw_inner_key,
                "entity": "payout",
                "fund_account_id": "fa_EiAeBLTwZNgHCH",
                "amount": 10000,
                "currency": "INR",
                "notes": {
                    "product": "withdraw"
                },
                "fees": 472,
                "tax": 72,
                "status": global_razorpay_withdraw_process_queued,
                # processing处理中、queued代付中、pending代付中、rejected代付失败、processed代付成功、cancelled代付失败、reversed代付失败
                "purpose": "payout",
                "utr": None,
                "mode": global_razorpay_withdraw_mode,
                "reference_id": "bf1623ba1fc244d8816cce21908ded5c",
                "narration": "KN Fund Transfer",
                "batch_id": None,
                "failure_reason": global_withdraw_failed_message,
                "created_at": 1587698724
            }]
        }
        self.update(api, mode, method)

    def update_razorpay_withdraw_query_process_003(self):
        # razorpay代付结果查询请求
        api = "/v1/payouts"
        method = "get"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [{
                "id": global_razorpay_withdraw_inner_key,
                "entity": "payout",
                "fund_account_id": "fa_EiAeBLTwZNgHCH",
                "amount": 10000,
                "currency": "INR",
                "notes": {
                    "product": "withdraw"
                },
                "fees": 472,
                "tax": 72,
                "status": global_razorpay_withdraw_process_pending,
                # processing处理中、queued代付中、pending代付中、rejected代付失败、processed代付成功、cancelled代付失败、reversed代付失败
                "purpose": "payout",
                "utr": None,
                "mode": global_razorpay_withdraw_mode,
                "reference_id": "bf1623ba1fc244d8816cce21908ded5c",
                "narration": "KN Fund Transfer",
                "batch_id": None,
                "failure_reason": global_withdraw_failed_message,
                "created_at": 1587698724
            }]
        }
        self.update(api, mode, method)

    def update_bind_fail_razorpay_steps2(self):
        # razorpay创建资金账户
        api = "/v1/fund_accounts"
        mode = {
            "id": global_razorpay_withdraw_fund_account_id,
            "entity": "fund_account",
            "contact_id": "cont_@word(15)",
            "account_type": "bank_account",
            "bank_account": {
                "ifsc": "YESB0000262",
                "bank_name": "Yes Bank",
                "name": "JOHN DOE",
                "notes": [

                ],
                "account_number": "026291800001191"
            },
            "batch_id": None,
            "active": "false",  # true成功，false失败
            "created_at": 1583303041
        }
        self.update(api, mode)

    def update_bind_process_razorpay_steps3(self):
        # razorpay绑卡打款验证处理中
        api = "/v1/fund_accounts/validations"
        mode = {
            "id": global_razorpay_verifyid,  # 这个值global_razorpay_verifyid必须要和查询接口一样
            "entity": "fund_account.validation",
            "fund_account": {
                "id": "fa_@word(15)",
                "entity": "fund_account",
                "contact_id": "cont_@word(15)",
                "account_type": "bank_account",
                "bank_account": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "JOHN DOE",
                    "notes": [

                    ],
                    "account_number": "026291800001191"
                },
                "batch_id": None,
                "active": "true",
                "created_at": 1583303041,
                "details": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "JOHN DOE",
                    "notes": [

                    ],
                    "account_number": "026291800001191"
                }
            },
            "status": "created",  # created请求处理中、completed请求成功，其他都是失败
            "amount": 100,
            "currency": "INR",
            "notes": {
                "product": "validation"
            },
            "results": {
                "account_status": None,
                "registered_name": None
            },
            "created_at": 1583303042,
            "utr": None
        }
        self.update(api, mode)

    def update_bind_success_razorpay_steps3(self, name):
        # razorpay绑卡打款验证处理中
        api = "/v1/fund_accounts/validations"
        mode = {
            "id": global_razorpay_verifyid,
            "entity": "fund_account.validation",
            "fund_account": {
                "id": "fa_EO2dA8mKs6kk8o",
                "entity": "fund_account",
                "contact_id": "cont_EO2d9LzFPDiZWk",
                "account_type": "bank_account",
                "bank_account": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "@name",
                    "notes": [],
                    "account_number": "026291800001191"
                },
                "batch_id": None,
                "active": "true",
                "created_at": 1583303041,
                "details": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "JOHN DOE",
                    "notes": [],
                    "account_number": "026291800001191"
                }
            },
            "status": "completed",  # status=completed 表示成功，created 表示处理中
            "amount": 100,
            "currency": "INR",
            "notes": {
                "product": "validation"
            },
            "results": {
                "account_status": "active",  # status=active 表示成功，invalid 失败
                "registered_name": name
            },
            "created_at": 1583303042,
            "utr": None
        }
        self.update(api, mode)

    def update_bind_success_razorpay_steps4(self, name):
        # razorpay绑卡打款验证查询
        api = "/v1/fund_accounts/validations/" + global_razorpay_verifyid  # global_razorpay_verifyid 要和打款验证的值接口一样，如果mock里面在测试时被改了，这里会跑不通
        mode = {
            "id": global_razorpay_verifyid,
            "entity": "fund_account.validation",
            "fund_account": {
                "id": "fa_EO2dA8mKs6kk8o",
                "entity": "fund_account",
                "contact_id": "cont_EO2d9LzFPDiZWk",
                "account_type": "bank_account",
                "bank_account": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "@name",
                    "notes": [],
                    "account_number": "026291800001191"
                },
                "batch_id": None,
                "active": "true",
                "created_at": 1583303041,
                "details": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "JOHN DOE",
                    "notes": [],
                    "account_number": "026291800001191"
                }
            },
            "status": "completed",  # status=completed 表示成功，created 表示处理中
            "amount": 100,
            "currency": "INR",
            "notes": {
                "product": "validation"
            },
            "results": {
                "account_status": "active",  # status=active 表示成功，invalid 失败
                "registered_name": name
            },
            "created_at": 1583303042,
            "utr": None
        }
        self.update(api, mode)

    def update_bind_fail_razorpay_steps4(self):
        # razorpay绑卡打款验证查询
        api = "/v1/fund_accounts/validations/" + global_razorpay_verifyid  # global_razorpay_verifyid 要和打款验证的值接口一样，如果mock里面在测试时被改了，这里会跑不通
        mode = {
            "id": "fav_EO2dAwLLGDFuzO",
            "entity": "fund_account.validation",
            "fund_account": {
                "id": "fa_EO2dA8mKs6kk8o",
                "entity": "fund_account",
                "contact_id": "cont_EO2d9LzFPDiZWk",
                "account_type": "bank_account",
                "bank_account": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "@name",
                    "notes": [],
                    "account_number": "026291800001191"
                },
                "batch_id": None,
                "active": "true",
                "created_at": 1583303041,
                "details": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "JOHN DOE",
                    "notes": [],
                    "account_number": "026291800001191"
                }
            },
            "status": "completed",  # status=completed 表示成功，created 表示处理中
            "amount": 100,
            "currency": "INR",
            "notes": {
                "product": "validation"
            },
            "results": {
                "account_status": "active",  # status=active 表示成功，invalid 失败
                "registered_name": "Unregistered"  # 写死的名字，会导致名字校验不过而绑卡失败
            },
            "created_at": 1583303042,
            "utr": None
        }
        self.update(api, mode)

    def update_bind_query_fail001_razorpay_steps4(self):
        # razorpay绑卡打款验证查询失败   第一种status=completed且results.account_status= invalid，置为绑卡失败；
        api = "/v1/fund_accounts/validations/" + global_razorpay_verifyid  # global_razorpay_verifyid 要和打款验证的值接口一样，如果mock里面在测试时被改了，这里会跑不通
        mode = {
            "id": "fav_EO2dAwLLGDFuzO",
            "entity": "fund_account.validation",
            "fund_account": {
                "id": "fa_EO2dA8mKs6kk8o",
                "entity": "fund_account",
                "contact_id": "cont_EO2d9LzFPDiZWk",
                "account_type": "bank_account",
                "bank_account": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "@name",
                    "notes": [],
                    "account_number": "026291800001191"
                },
                "batch_id": None,
                "active": "true",
                "created_at": 1583303041,
                "details": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "JOHN DOE",
                    "notes": [],
                    "account_number": "026291800001191"
                }
            },
            "status": "completed",  # status=completed 表示成功，created 表示处理中
            "amount": 100,
            "currency": "INR",
            "notes": {
                "product": "validation"
            },
            "results": {
                "account_status": "invalid",  # status=active 表示成功，invalid 失败
                "registered_name": None
            },
            "created_at": 1583303042,
            "utr": None
        }
        self.update(api, mode)

    def update_bind_fail001_razorpay_steps3(self):
        # razorpay绑卡打款验证直接失败   第一种status=completed 且results.account_status= invalid，置为绑卡失败
        api = "/v1/fund_accounts/validations"
        mode = {
            "id": "fav_EO2dAwLLGDFuzO",
            "entity": "fund_account.validation",
            "fund_account": {
                "id": "fa_EO2dA8mKs6kk8o",
                "entity": "fund_account",
                "contact_id": "cont_EO2d9LzFPDiZWk",
                "account_type": "bank_account",
                "bank_account": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "@name",
                    "notes": [],
                    "account_number": "026291800001191"
                },
                "batch_id": None,
                "active": "true",
                "created_at": 1583303041,
                "details": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "JOHN DOE",
                    "notes": [],
                    "account_number": "026291800001191"
                }
            },
            "status": "completed",  # status=completed 表示成功，created 表示处理中
            "amount": 100,
            "currency": "INR",
            "notes": {
                "product": "validation"
            },
            "results": {
                "account_status": "invalid",  # status=active 表示成功，invalid 失败
                "registered_name": None
            },
            "created_at": 1583303042,
            "utr": None
        }
        self.update(api, mode)

    def update_bind_fail002_razorpay_steps3(self):
        # razorpay绑卡打款验证直接失败   第二种status<>completed/active，不管results.account_status的状态，就置为绑卡失败
        api = "/v1/fund_accounts/validations/" + global_razorpay_verifyid  # global_razorpay_verifyid 要和打款验证的值接口一样，如果mock里面在测试时被改了，这里会跑不通
        mode = {
            "id": "fav_EO2dAwLLGDFuzO",
            "entity": "fund_account.validation",
            "fund_account": {
                "id": "fa_EO2dA8mKs6kk8o",
                "entity": "fund_account",
                "contact_id": "cont_EO2d9LzFPDiZWk",
                "account_type": "bank_account",
                "bank_account": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "@name",
                    "notes": [],
                    "account_number": "026291800001191"
                },
                "batch_id": None,
                "active": "true",
                "created_at": 1583303041,
                "details": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "JOHN DOE",
                    "notes": [],
                    "account_number": "026291800001191"
                }
            },
            "status": "unknown",  # status=completed 表示成功，created 表示处理中
            "amount": 100,
            "currency": "INR",
            "notes": {
                "product": "validation"
            },
            "results": {
                "account_status": None,
                "registered_name": None
            },
            "created_at": 1583303042,
            "utr": None
        }
        self.update(api, mode)

    def update_bind_query_process_razorpay_steps4(self):
        # razorpay绑卡打款验证查询处理中，status=created
        api = "/v1/fund_accounts/validations/" + global_razorpay_verifyid  # global_razorpay_verifyid 要和打款验证的值接口一样，如果mock里面在测试时被改了，这里会跑不通
        mode = {
            "id": "fav_EO2dAwLLGDFuzO",
            "entity": "fund_account.validation",
            "fund_account": {
                "id": "fa_EO2dA8mKs6kk8o",
                "entity": "fund_account",
                "contact_id": "cont_EO2d9LzFPDiZWk",
                "account_type": "bank_account",
                "bank_account": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "@name",
                    "notes": [],
                    "account_number": "026291800001191"
                },
                "batch_id": None,
                "active": "true",
                "created_at": 1583303041,
                "details": {
                    "ifsc": "YESB0000262",
                    "bank_name": "Yes Bank",
                    "name": "JOHN DOE",
                    "notes": [],
                    "account_number": "026291800001191"
                }
            },
            "status": "created",  # status=completed 表示成功，created 表示处理中
            "amount": 100,
            "currency": "INR",
            "notes": {
                "product": "validation"
            },
            "results": {
                "account_status": None,
                "registered_name": None
            },
            "created_at": 1583303042,
            "utr": None
        }
        self.update(api, mode)

    def update_razorpay_collect_customer_register_fail(self):
        # 开虚户第一步：创建联系人失败
        api = "/v1/customers"
        mode = {
            # "id": "cust_ETet05iEX6zshX",  # 有id就就是创建联系人成功
            "entity": "customer",
            "name": "JANE DOE",
            "email": "wangxiaoming@google.com",
            "contact": "15201959337",
            "gstin": None,
            "notes": [

            ],
            "created_at": 1584529463
        }
        self.update(api, mode)

    def update_razorpay_collect_customer_register_success(self):
        # 开虚户第一步：创建联系人成功
        api = "/v1/customers"
        mode = {
            "id": "cust_ETet05iEX6zshX",  # 有id就就是创建联系人成功
            "entity": "customer",
            "name": "JANE DOE",
            "email": "wangxiaoming@google.com",
            "contact": "15201959337",
            "gstin": None,
            "notes": [

            ],
            "created_at": 1584529463
        }
        self.update(api, mode)

    def update_razorpay_collect_account_register_fail(self):
        # 开虚户第二步：开户失败
        api = "/v1/virtual_accounts"
        mode = {
            "id": global_razorpay_collect_inner_no,
            "name": "KN",
            "entity": "virtual_account",
            "status": "closed",  # active 表示开户成功，非 active 开户失败
            "description": None,
            "amount_expected": None,
            "notes": [

            ],
            "amount_paid": 0,
            "customer_id": "cust_ETet05iEX6zshX",
            "receivers": [
                {
                    "id": "ba_EcitDc36PkwTfk",
                    "entity": "bank_account",
                    "ifsc": "RAZR0000001",
                    "bank_name": "RBL Bank",
                    "name": "KN",
                    "notes": [

                    ],
                    "account_number": "1112220091286919"
                }
            ],
            "close_by": 1586509822,
            "closed_at": None,
            "created_at": 1586508623
        }
        self.update(api, mode)

    def update_razorpay_collect_account_register_success(self):
        # 开虚户第二步：开户成功
        account_number = "auto_test" + get_timestamp()
        api = "/v1/virtual_accounts"
        mode = {
            "id": global_razorpay_collect_inner_no,  # 该id影响线下还款记录的查询，需和mock保持一致
            "name": "KN",
            "entity": "virtual_account",
            "status": "active",  # active 表示开户成功
            "description": None,
            "amount_expected": None,
            "notes": [

            ],
            "amount_paid": 0,
            "customer_id": "cust_ETet05iEX6zshX",
            "receivers": [
                {
                    "id": "ba_EcitDc36PkwTfk",
                    "entity": "bank_account",
                    "ifsc": "RAZR0000001",
                    "bank_name": "RBL Bank",
                    "name": "KN",
                    "notes": [

                    ],
                    "account_number": account_number
                }
            ],
            "close_by": 1586509822,
            "closed_at": None,
            "created_at": 1586508623
        }
        self.update(api, mode)

    def update_razorpay_collect_closeaccount_fail(self):
        # 注销虚户失败
        api = "/v1/virtual_accounts/" + global_razorpay_collect_inner_no + "/close"
        mode = {
            "id": "va_Di5gbNptcWV8fQ",
            "name": "Acme Corp",
            "entity": "virtual_account",
            "status": "active",  # closed 表示注销成功
            "description": "Virtual Account created for M/S ABC Exports",
            "amount_expected": 230000,
            "notes": {
                "material": "teakwood"
            },
            "amount_paid": 239000,
            "customer_id": "cust_DOMUFFiGdCaCUJ",
            "receivers": [{
                "id": "ba_Di5gbQsGn0QSz3",
                "entity": "bank_account",
                "ifsc": "RATN0VAAPIS",
                "bank_name": "RBL Bank",
                "name": "Acme Corp",
                "notes": [],
                "account_number": "1112220061746877"
            }],
            "close_by": 1574427237,
            "closed_at": 1574164078,
            "created_at": 1574143517
        }
        self.update(api, mode)

    def update_razorpay_collect_closeaccount_success(self):
        # 注销虚户成功
        api = "/v1/virtual_accounts/" + global_razorpay_collect_inner_no + "/close"
        mode = {
            "id": "va_Di5gbNptcWV8fQ",
            "name": "Acme Corp",
            "entity": "virtual_account",
            "status": "closed",  # closed 表示注销成功
            "description": "Virtual Account created for M/S ABC Exports",
            "amount_expected": 230000,
            "notes": {
                "material": "teakwood"
            },
            "amount_paid": 239000,
            "customer_id": "cust_DOMUFFiGdCaCUJ",
            "receivers": [{
                "id": "ba_Di5gbQsGn0QSz3",
                "entity": "bank_account",
                "ifsc": "RATN0VAAPIS",
                "bank_name": "RBL Bank",
                "name": "Acme Corp",
                "notes": [],
                "account_number": "1112220061746877"
            }],
            "close_by": 1574427237,
            "closed_at": 1574164078,
            "created_at": 1574143517
        }
        self.update(api, mode)

    def update_razorpay_collect_repaylist_onesuccess(self):
        # razorpay线下还款：第一步查询账户还款列表（打款成功一次）
        api = "/v1/virtual_accounts/" + global_razorpay_collect_inner_no + "/payments"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": global_razorpay_collect_channel_key1,
                    "entity": "payment",
                    "amount": global_razorpay_collect_paid_amount,
                    "currency": "INR",
                    "status": "captured",  # "status":"captured"且"captured": true表示打款成功
                    "captured": True,
                    "order_id": None,
                    "invoice_id": None,
                    "international": False,
                    "method": global_razorpay_collect_payment_option,
                    "amount_refunded": 0,
                    "refund_status": None,
                    "description": "Test~2223330014242391",
                    "card_id": None,
                    "bank": None,
                    "wallet": None,
                    "vpa": None,
                    "email": "mudita.savai@gmail.com",
                    "contact": global_razorpay_collect_mobile,  # card.card_mobile
                    "customer_id": "cust_EbUnrATKfuBeE1",
                    "notes": [

                    ],
                    "fee": global_razorpay_ebank_service_fee,  # 总费用=服务费+税费，fee-tax保存到withhold_receipt_service_charge
                    "tax": global_razorpay_ebank_service_tax,  # 税费，保存到withhold_receipt_service_tax
                    "error_code": None,
                    "error_description": None,
                    "error_source": None,
                    "error_step": None,
                    "error_reason": None,
                    "created_at": 1593776535
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_collect_repaylist_twosuccess(self):
        # razorpay线下还款：第一步查询账户还款列表（打款成功2次）
        api = "/v1/virtual_accounts/" + global_razorpay_collect_inner_no + "/payments"
        mode = {
            "entity": "collection",
            "count": 2,
            "items": [
                {
                    "id": global_razorpay_collect_channel_key1,
                    "entity": "payment",
                    "amount": global_razorpay_collect_paid_amount,
                    "currency": "INR",
                    "status": "captured",  # "status":"captured"且"captured": true表示打款成功
                    "captured": "true",
                    "order_id": None,
                    "invoice_id": None,
                    "international": "false",
                    "method": "bank_transfer",  # 当查询账户还款明细没有返回mode时，用该字段更新到withhold_receipt_payment_mode
                    "amount_refunded": 0,
                    "refund_status": None,
                    "description": "Test~2223330014242391",
                    "card_id": None,
                    "bank": None,
                    "wallet": None,
                    "vpa": None,
                    "email": "mudita.savai@gmail.com",
                    "contact": global_razorpay_collect_mobile,  # card.card_mobile
                    "customer_id": "cust_EbUnrATKfuBeE1",
                    "notes": [

                    ],
                    "fee": global_razorpay_ebank_service_fee,
                    "tax": global_razorpay_ebank_service_tax,
                    "error_code": None,
                    "error_description": None,
                    "created_at": 1586763010
                },
                {
                    "id": global_razorpay_collect_channel_key2,
                    "entity": "payment",
                    "amount": global_razorpay_collect_paid_amount,
                    "currency": "INR",
                    "status": "captured",  # "status":"captured"且"captured": true表示打款成功
                    "captured": "true",
                    "order_id": None,
                    "invoice_id": None,
                    "international": "false",
                    "method": "bank_transfer",  # 当查询账户还款明细没有返回mode时，用该字段更新到withhold_receipt_payment_mode
                    "amount_refunded": 0,
                    "refund_status": None,
                    "description": "Test~2223330014242391",
                    "card_id": None,
                    "bank": None,
                    "wallet": None,
                    "vpa": None,
                    "email": "mudita.savai@gmail.com",
                    "contact": global_razorpay_collect_mobile,  # card.card_mobile
                    "customer_id": "cust_EbUnrATKfuBeE1",
                    "notes": [

                    ],
                    "fee": global_razorpay_ebank_service_fee,
                    "tax": global_razorpay_ebank_service_tax,
                    "error_code": None,
                    "error_description": None,
                    "created_at": 1586763010
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_collect_repaylist_norepay(self):
        # razorpay线下还款：未打款
        api = "/v1/virtual_accounts/" + global_razorpay_collect_inner_no + "/payments"
        mode = {
            "entity": "collection",
            "count": 0,
            "items": [

            ]
        }
        self.update(api, mode)

    def update_razorpay_collect_repaydetail_success_channelkey1_havecard(self):
        # razorpay线下还款：第二步查询账户还款明细（有打款卡号）
        api = "/v1/payments/" + global_razorpay_collect_channel_key1 + "/bank_transfer"
        mode = {
            "id": "bt_EeOoeAeAbAMP29",
            "entity": global_razorpay_collect_payment_option,
            "payment_id": "pay_EeOoeBKHDpJZwf",
            "mode": global_razorpay_collect_payment_mode_upi,  # 更新到withhold_receipt_payment_mode
            "bank_reference": "010576117254",
            "amount": 500000,
            "payer_bank_account": {  # 这个节点可能是None，即"payer_bank_account":None,
                "id": "ba_EbaLlAw7i4CgRF",
                "entity": "bank_account",
                "ifsc": global_razorpay_collect_ifsc,  # card.card_bank_code
                "bank_name": "HDFC Bank",
                "name": global_razorpay_collect_name,  # card.card_username
                "notes": [],
                "account_number": global_razorpay_collect_cardnum
                # 更新到withhold_receipt_card_num，同时保存数据到card.card_account表
            },
            "virtual_account_id": "va_EeOOamTfCvVUu9",
            "virtual_account": {
                "id": "va_EeOOamTfCvVUu9",
                "name": "KN",
                "entity": "virtual_account",
                "status": "active12",
                "description": None,
                "amount_expected": None,
                "notes": [

                ],
                "amount_paid": 500000,
                "customer_id": "cust_EdwBzHjkt6jhpC",
                "receivers": [{
                    "id": "ba_EeOOatzbpCLCot",
                    "entity": "bank_account",
                    "ifsc": "RATN0VAAPIS",
                    "bank_name": "RBL Bank",
                    "name": "KN",
                    "notes": [

                    ],
                    "account_number": "2223330018756810"
                }],
                "close_by": 1592057131,
                "closed_at": None,
                "created_at": 1586873131
            }
        }
        self.update(api, mode)

    def update_razorpay_collect_repaydetail_success_channelkey1_nocard(self):
        # razorpay线下还款：第二步查询账户还款明细（没有打款卡号）
        api = "/v1/payments/" + global_razorpay_collect_channel_key1 + "/bank_transfer"
        mode = {
            "id": "bt_EeOoeAeAbAMP29",
            "entity": "bank_transfer",
            "payment_id": "pay_EeOoeBKHDpJZwf",
            "mode": global_razorpay_collect_payment_mode_other,  # 更新到withhold_receipt_payment_mode
            "bank_reference": "010576117254",
            "amount": 500000,
            "payer_bank_account": None,  # upi打款的没有转账卡号
            "virtual_account_id": "va_EeOOamTfCvVUu9",
            "virtual_account": {
                "id": "va_EeOOamTfCvVUu9",
                "name": "KN",
                "entity": "virtual_account",
                "status": "active12",
                "description": None,
                "amount_expected": None,
                "notes": [

                ],
                "amount_paid": 500000,
                "customer_id": "cust_EdwBzHjkt6jhpC",
                "receivers": [{
                    "id": "ba_EeOOatzbpCLCot",
                    "entity": "bank_account",
                    "ifsc": "RATN0VAAPIS",
                    "bank_name": "RBL Bank",
                    "name": "KN",
                    "notes": [

                    ],
                    "account_number": "2223330018756810"
                }],
                "close_by": 1592057131,
                "closed_at": None,
                "created_at": 1586873131
            }
        }
        self.update(api, mode)

    def update_razorpay_collect_repaydetail_success_channelkey2(self):
        # razorpay线下还款：第二步查询账户还款明细（有打款卡号）
        api = "/v1/payments/" + global_razorpay_collect_channel_key2 + "/bank_transfer"
        mode = {
            "id": "bt_EeOoeAeAbAMP29",
            "entity": global_razorpay_collect_payment_option,
            "payment_id": "pay_EeOoeBKHDpJZwf",
            "mode": global_razorpay_collect_payment_mode_other,  # 更新到withhold_receipt_payment_mode
            "bank_reference": "010576117254",
            "amount": 500000,
            "payer_bank_account": {  # 这个节点可能是None，即"payer_bank_account":None,
                "id": "ba_EbaLlAw7i4CgRF",
                "entity": "bank_account",
                "ifsc": global_razorpay_collect_ifsc,  # card.card_bank_code
                "bank_name": "HDFC Bank",
                "name": global_razorpay_collect_name,  # card.card_username
                "notes": [],
                "account_number": global_razorpay_collect_cardnum
                # 更新到withhold_receipt_card_num，同时保存数据到card.card_account表
            },
            "virtual_account_id": "va_EeOOamTfCvVUu9",
            "virtual_account": {
                "id": "va_EeOOamTfCvVUu9",
                "name": "KN",
                "entity": "virtual_account",
                "status": "active12",
                "description": None,
                "amount_expected": None,
                "notes": [

                ],
                "amount_paid": 500000,
                "customer_id": "cust_EdwBzHjkt6jhpC",
                "receivers": [{
                    "id": "ba_EeOOatzbpCLCot",
                    "entity": "bank_account",
                    "ifsc": "RATN0VAAPIS",
                    "bank_name": "RBL Bank",
                    "name": "KN",
                    "notes": [

                    ],
                    "account_number": "2223330018756810"
                }],
                "close_by": 1592057131,
                "closed_at": None,
                "created_at": 1586873131
            }
        }
        self.update(api, mode)

    def update_razorpay_collect_accountstatus_active(self):
        # razorpay虚户状态查询：可用status=active
        api = "/v1/virtual_accounts/" + global_razorpay_collect_inner_no
        mode = {
            "id": "va_D6Vw6zyJ0OmRZg",
            "name": "Acme Corp",
            "entity": "virtual_account",
            "status": "active",  # active 激活，closed 已过期
            "description": "Virtual Account for Raftar Soft",
            "amount_expected": 5000,
            "notes": [],
            "amount_paid": None,
            "customer_id": "cust_9xnHzNGIEY4TAV",
            "receivers": [{
                "id": "ba_D6Vw76RrHA3DC9",
                "entity": "bank_account",
                "ifsc": "RATN0VAAPIS",
                "bank_name": "RBL Bank",
                "name": "Acme Corp",
                "notes": [],
                "account_number": "2223330025991681"
            }],
            "close_by": None,
            "closed_at": 1568109789,
            "created_at": 1565939036
        }
        self.update(api, mode)

    def update_razorpay_collect_accountstatus_closed(self):
        # razorpay虚户状态查询：不可用status=closed
        api = "/v1/virtual_accounts/" + global_razorpay_collect_inner_no
        mode = {
            "id": "va_D6Vw6zyJ0OmRZg",
            "name": "Acme Corp",
            "entity": "virtual_account",
            "status": "closed",  # active 激活，closed 已过期
            "description": "Virtual Account for Raftar Soft",
            "amount_expected": 5000,
            "notes": [],
            "amount_paid": None,
            "customer_id": "cust_9xnHzNGIEY4TAV",
            "receivers": [{
                "id": "ba_D6Vw76RrHA3DC9",
                "entity": "bank_account",
                "ifsc": "RATN0VAAPIS",
                "bank_name": "RBL Bank",
                "name": "Acme Corp",
                "notes": [],
                "account_number": "2223330025991681"
            }],
            "close_by": None,
            "closed_at": 1568109789,
            "created_at": 1565939036
        }
        self.update(api, mode)

    def update_razorpay_transfer_fail(self):
        api = "/v1/transfers"
        mode = {
            "error": {
                "code": "BAD_REQUEST_ERROR",
                "description": global_withdraw_failed_message,
                "metadata": {

                },
                "field": "amount"
            }
        }
        self.update(api, mode)

    def update_razorpay_transfer_transfersuccess(self):
        api = "/v1/transfers"
        mode = {
            "id": global_razorpay_transfer_id,
            "entity": "transfer",
            "source": "acc_EKur39TDr0vNCN",
            "recipient": "acc_ExbVyNbpdbqoZx",
            "amount": 100,
            "currency": "INR",
            "amount_reversed": 0,
            "notes": {
                "product": "transfer"
            },
            "fees": 1,
            "tax": 0,
            "on_hold": False,
            "on_hold_until": None,
            "recipient_settlement_id": None,
            "created_at": 1591866119,
            "linked_account_notes": [

            ],
            "processed_at": 1591866119
        }
        self.update(api, mode)

    def update_razorpay_transfer_querysuccess(self):
        api = "/v1/settlements/recon/combined"
        mode = {
            "entity": "collection",
            "count": 84,
            "items": [{
                "entity_id": global_razorpay_transfer_id,
                "type": "transfer",
                "debit": global_razorpay_collect_paid_amount + global_razorpay_ebank_service_fee + global_razorpay_ebank_service_tax,
                "credit": 0,
                "amount": global_razorpay_collect_paid_amount,
                "currency": "INR",
                "fee": global_razorpay_ebank_service_fee,
                "tax": global_razorpay_ebank_service_tax,
                "on_hold": False,
                "settled": True,
                "created_at": 1591689543,
                "settled_at": 1591698736,
                "settlement_id": "setl_F0Ug4PFV3G2tNy",
                "posted_at": None,
                "description": None,
                "notes": None,
                "payment_id": None,
                "settlement_utr": "AXISCN0052167020",
                "order_id": None,
                "order_receipt": None,
                "method": None,
                "card_network": None,
                "card_issuer": None,
                "card_type": None,
                "dispute_id": None
            }]
        }
        self.update(api, mode)

    def update_razorpay_transfer_transferquery(self):
        api = "/v1/transfers/" + global_razorpay_transfer_id
        mode = {
            "id": "trf_F1dcqkN8mt3RnM",
            "entity": "transfer",
            "source": "acc_EKur39TDr0vNCN",
            "recipient": "acc_ExbVyNbpdbqoZx",
            "amount": 100,
            "currency": "INR",
            "amount_reversed": 0,
            "notes": {
                "product": "transfer"
            },
            "fees": 1,
            "tax": 0,
            "on_hold": False,
            "on_hold_until": None,
            "recipient_settlement_id": None,
            "created_at": 1591948588,
            "linked_account_notes": [],
            "processed_at": 1591948588
        }
        self.update(api, mode)

    def update_razorpay_transfer_query_nodata(self):
        api = "/v1/settlements/recon/combined"
        mode = {
            "entity": "collection",
            "count": 0,
            "items": []
        }
        self.update(api, mode)

    def update_razorpay_reconic_total_havadata(self):
        # 总账单：注意settlements节点下的值不要改，改了会导致脚本失败
        api = "/v1/settlements"
        mode = {
            "entity": "collection",
            "count": 1,
            "items": [
                {
                    "id": "setl_EVd17tCHzrE3NE",
                    "entity": "settlement",
                    "amount": 355270,  # 结算金额
                    "status": "processed",
                    "fees": 1180,
                    "tax": 180,
                    "utr": "AXISCN0049486968",
                    "created_at": 1584959561
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_reconic_total_nodata(self):
        # 总账单
        api = "/v1/settlements"
        mode = {
            "entity": "collection",
            "count": 0,
            "items": []
        }
        self.update(api, mode)

    def update_razorpay_reconic_detail_havedata(self):
        # 单笔账单明细：注意transactions节点下的值不要改，改了会导致脚本失败
        api = "/v1/settlements/recon/combined"
        mode = {
            "entity": "collection",
            "count": 2,
            "items": [
                {
                    "entity_id": "pay_EVJWxPV5DrHy93",
                    "type": "payment",
                    "debit": 0,
                    "credit": 204810,
                    "amount": 205400,
                    "currency": "INR",
                    "fee": 590,
                    "tax": 90,
                    "on_hold": False,
                    "settled": True,
                    "created_at": 1584890964,
                    "settled_at": 1584959561,
                    "settlement_id": "setl_EVd17tCHzrE3NE",
                    "posted_at": None,
                    "description": "#inv_EVJWEvXc6JHt4B",
                    "notes": "{}",
                    "payment_id": None,
                    "settlement_utr": "AXISCN0049486968",
                    "order_id": "order_EVJWEySIeDB55V",
                    "order_receipt": "RBIZ403226980514596029",
                    "method": "card",
                    "card_network": "RuPay",
                    "card_issuer": "UBIN",
                    "card_type": "debit",
                    "dispute_id": None
                },
                {
                    "entity_id": "pay_EVEDCXN9XDcMVw",
                    "type": "payment",
                    "debit": 0,
                    "credit": 150460,
                    "amount": 151050,
                    "currency": "INR",
                    "fee": 590,
                    "tax": 90,
                    "on_hold": False,
                    "settled": True,
                    "created_at": 1584872230,
                    "settled_at": 1584959561,
                    "settlement_id": "setl_EVd17tCHzrE3NE",
                    "posted_at": None,
                    "description": "#inv_EVEBLWAfeTqIgA",
                    "notes": "{}",
                    "payment_id": None,
                    "settlement_utr": "AXISCN0049486968",
                    "order_id": "order_EVEBLYSnj2Fdld",
                    "order_receipt": "RBIZ403228392065164683",
                    "method": "card",
                    "card_network": "Visa",
                    "card_issuer": "KKBK",
                    "card_type": "debit",
                    "dispute_id": None
                }
            ]
        }
        self.update(api, mode)

    def update_razorpay_reconic_detail_nodata(self):
        # 单笔账单明细
        api = "/v1/settlements/recon/combined"
        mode = {
            "entity": "collection",
            "count": 0,
            "items": []
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
