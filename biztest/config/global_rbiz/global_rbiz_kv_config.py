import common.global_const as gc


def update_india_rbiz_paysvr_config(project=None):
    if project:
        base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/global_rbiz_auto_test" % project
    else:
        base_url = "http://biz-payment-test1.biz-ind.svc.cluster.local:8901"
    content = {
        "payment_url": base_url,
        "rbiz": {
            "merchant_id": "3",
            "merchant_md5": "b21f3f04444c407f0008bf46649d2bbe"
        },
        "sign_subject": {},
        "sign_subject_mapping": [],
        "is_open": True,
        "user_ip": [
            "115.159.91.52"
        ],
        "withdraw_conf": {},
        "api_conf": {
            "withdraw_url": "/withdraw/autoWithdraw",
            "withdraw_query_url": "/withdraw/query",
            "withhold_cancel_url": "/withhold/closeOrder"
        },
        "sign_company_mapping": {
            "nbfc_f6": "sixsixsix",
            "nbfc_f6_new": "sixsixsix",
            "nbfc_sunita": "sunita",
            "qp": "kn"
        },
        "trade_sign_company_mapping": [
            {
                "trade_type": [
                    "asset_delay"
                ],
                "sign_company": "kn"
            }
        ],
        "manual_withhold_redirect_url": "http://www.baidu.com"
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_paysvr_config", content, "KV")


def update_tha_rbiz_paysvr_config(project=None, callback_amount_consistent_check=False):
    if project:
        base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/global_rbiz_auto_test" % project
    else:
        base_url = "http://biz-payment-test1.biz-tha.svc.cluster.local:8901"
    content = {
        "payment_url": base_url,
        "rbiz": {
            "merchant_id": "3",
            "merchant_md5": "b21f3f04444c407f0008bf46649d2bbe"
        },
        "sign_subject": {},
        "sign_subject_mapping": [],
        "is_open": True,
        "user_ip": [
            "115.159.91.52"
        ],
        "withdraw_conf": {
            "merchant_name": "biz",
            "merchant_id": "3",
            "merchant_md5": "b21f3f04444c407f0008bf46649d2bbe",
            "withdraw_callback_url": gc.REPAY_URL + "/paysvr/withdraw/callback"
        },
        "api_conf": {
            "withdraw_url": "/withdraw/autoWithdraw",
            "withdraw_query_url": "/withdraw/query",
            "withhold_cancel_url": "/withhold/closeOrder"
        },
        "sign_company_mapping": {
            "pico_bangkok": "amberstar1",
            "tha_bankcard": "cymo1",
            "tha_amberstar": "cymo1",
            "noloan": "cymo1",
            "tha_picocapital": "amberstar1",
            "tha_picocapital_plus": "amberstar1",
            "pico_bang": "amberstar1",
            "pico_qr": "amberstar1",
            "pico_nonth": "amberstar1",
            "pico_sp": "amberstar1",
            "pico_path": "amberstar1",
            "pico_moon": "amberstar1",
            "pico_planet": "amberstar1",
            "pico_gem": "amberstar1",
            "u_peso": "upeso",
            "copper_stone": "upeso",
            "nbmfc": "nbmfc",
            "picocp_ams1": "amberstar1",
            "picoqr_ams1": "amberstar2",
            "picocp_ams2": "amberstar1",
            "picoqr_ams2": "amberstar1"
        },
        "delay_account_isolate": True,
        "trade_sign_company_mapping": [
            {
                "trade_type": [
                    "credit_report",
                    "asset_delay",
                    "pre_service_fee"
                ],
                "sign_company": "amberstar1"
            }
        ],
        "callback_amount_consistent_check": callback_amount_consistent_check
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_paysvr_config", content, "KV")


def update_phl_rbiz_paysvr_config(project=None):
    if project:
        base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/global_rbiz_auto_test" % project
    else:
        base_url = "http://biz-payment-test1.biz-phl.svc.cluster.local:8901"
    content = {
        "payment_url": base_url,
        "rbiz": {
            "merchant_id": "3",
            "merchant_md5": "b21f3f04444c407f0008bf46649d2bbe"
        },
        "sign_subject": {},
        "sign_subject_mapping": [],
        "is_open": True,
        "user_ip": [
            "115.159.91.52"
        ],
        "withdraw_conf": {},
        "api_conf": {
            "withdraw_url": "/withdraw/autoWithdraw",
            "withdraw_query_url": "/withdraw/query",
            "withhold_cancel_url": "/withhold/closeOrder"
        },
        "sign_company_mapping": {
            "u_peso": "upeso",
            "copper_stone": "copperstone"
        },
        "trade_sign_company_mapping": [
            {
                "trade_type": [
                    "asset_delay"
                ],
                "sign_company": "copperstone"
            }
        ],
        "callback_amount_adjust_switch": True
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_paysvr_config", content, "KV")


def update_rbiz_grant_api_config(project=None):
    if project:
        base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/global_rbiz_auto_test" % project
    else:
        base_url = "https://biz-gateway-proxy.starklotus.com/tha_grant1"
    content = {
        "base_url": base_url,
        "user_id_action": "user-id-query",
        "offline_repay_info_action": "/asset/offline-repay-info"
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_grant_api_config", content, "KV")


def update_rbiz_config(tolerance_amount=1000, auto_tolerance=False, tolerance_type="fixed", by_period=True,
                       special_service_name=None, need_decrease_late=False, auto_void_withhold_amount=0):
    content = {
        "repay_priority": {
            "common_priority": {
                "lateservice": 1,
                "lateinterest": 3,
                "manage": 50,
                "credit_fee": 60,
                "fin_service": 68,
                "service": 70,
                "repayinterest": 80,
                "repayprincipal": 90
            },
            "asset_void_priority": {
                "lateservice": 90,
                "lateinterest": 70,
                "manage": 50,
                "credit_fee": 40,
                "service": 30,
                "repayinterest": 20,
                "repayprincipal": 10
            }
        },
        "can_cmdb_system_refresh": False,
        "refresh_late_fee_tolerance_amount": 100,
        "owner_list": [
            "KN"
        ],
        "hengfengNotifyQnn": False,
        "offline_recharge": {
            "tolerance": 7246
        },
        "service_fee": [
            "service",
            "fin_service"
        ],
        "late_tran_type_list": [
            "lateinterest",
            "latefin_service"
        ],
        "capital_tran": {
            "our_service": []
        },
        "tran_type_mapping": {},
        "capital_agreement_payment": [],
        "dsq_send_sms_condition": {},
        "deposit_sign_company_config": {},
        "short_period_withhold": True,
        "skipCheckTranFinish": True,
        "system_tolerance_config": {
            "tolerance_amount": tolerance_amount,
            "byPeriod": by_period,
            "auto_tolerance": auto_tolerance
        },
        "repay_tolerance_config": {
            "manual": {
                "overdue_days": 8,
                "less_than_overdue_days": {
                    "method": "fixed",
                    "value": 1000
                },
                "equals_overdue_days": {
                    "method": "percent",
                    "value": 10,
                    "base_line": "repay_period_principal"
                },
                "greater_than_overdue_days": {
                    "method": "percent",
                    "value": 10,
                    "base_line": "repay_period_principal"
                }
            },
            "active": {
                "overdue_days": 8,
                "less_than_overdue_days": {
                    "method": "fixed",
                    "value": 1000
                },
                "equals_overdue_days": {
                    "method": "percent",
                    "value": 10,
                    "base_line": "repay_period_principal"
                },
                "greater_than_overdue_days": {
                    "method": "percent",
                    "value": 10,
                    "base_line": "repay_period_principal"
                }
            },
            "void": {
                "overdue_days": 8,
                "less_than_overdue_days": {
                    "method": "fixed",
                    "value": 0
                },
                "equals_overdue_days": {
                    "method": "fixed",
                    "value": 0,
                    "base_line": "repay_period_principal"
                },
                "greater_than_overdue_days": {
                    "method": "fixed",
                    "value": 0,
                    "base_line": "repay_period_principal"
                }
            }
        },
        "erase_oddment_config": {
            "erase_oddment_amount": 999,
            "calculate_unit": 1000
        },
        "asset_delay_config": {
            "noLoan_auto_delay": True,
            "need_push_fox": True,
            "need_decrease_late": need_decrease_late,
            "special_service_name": special_service_name,
            "calculate_base_line": "grant_principal",
            "allow_min_value": 0.1,
            "allow_max_value": 150
        },
        "auto_void_withhold_amount": auto_void_withhold_amount,
        "dynamic_service": {
            "asset_withdraw_success": "pakAssetReGrantService"
        }
    }
    if tolerance_type == "fixed":
        content["repay_tolerance_config"]["active"]["less_than_overdue_days"] = {"method": "fixed", "value": 1000}
    elif tolerance_type == "grant_principal":
        content["repay_tolerance_config"]["active"]["less_than_overdue_days"] = {"method": "percent", "value": 10,
                                                                                 "base_line": "grant_principal"}
    elif tolerance_type == "balance_principal":
        content["repay_tolerance_config"]["active"]["less_than_overdue_days"] = {"method": "percent", "value": 10,
                                                                                 "base_line": "balance_principal"}
    elif tolerance_type == "min_period_principal":
        content["repay_tolerance_config"]["active"]["less_than_overdue_days"] = {"method": "percent", "value": 10,
                                                                                 "base_line": "min_period_principal"}
    elif tolerance_type == "repay_period_principal":
        content["repay_tolerance_config"]["active"]["less_than_overdue_days"] = {"method": "percent", "value": 10,
                                                                                 "base_line": "repay_period_principal"}
    elif tolerance_type == "balance_asset_amount":
        content["repay_tolerance_config"]["active"]["less_than_overdue_days"] = {"method": "percent", "value": 10,
                                                                                 "base_line": "balance_asset_amount"}
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_config", content, "KV")


def update_rbiz_config_withhold(intervalHour=24, assetDelayIntervalHour=24, asset_void_hour=36):
    content = {
        "switch": True,
        "withhold_types": {
            "active": {
                "is_open": True,
                "withhold_limit": 0,
                "asset_types": [
                    "paydayloan"
                ],
                "except_capitals": [],
                "except_subtypes": [],
                "bind_channel": {
                    "is_open": False,
                    "send_sign_company": False
                },
                "bind_channel_black_list": []
            },
            "auto": {
                "is_open": True,
                "gray_publish": False,
                "qnn_loan_open": True,
                "withhold_limit": 1,
                "asset_types": [
                    "paydayloan",
                    "eliteloan",
                    "guarantee",
                    "hospital"
                ],
                "except_capitals": [],
                "except_subtypes": []
            },
            "manual": {
                "is_open": True,
                "withhold_limit": 0,
                "qnn_loan_open": True,
                "asset_types": [
                    "paydayloan"
                ],
                "except_capitals": [],
                "except_subtypes": []
            },
            "order": {
                "is_open": True,
                "withhold_limit": 60000,
                "order_types": [],
                "asset_void_hour_validate_interval": asset_void_hour
            },
            "without_card": {
                "is_open": True,
                "asset_types": [],
                "except_capitals": [],
                "except_subtypes": []
            }
        },
        "white_list": [],
        "postpone_task_list": [],
        "use_limit_loan_channels": [],
        "timeout": {
            "except_withhold_trade_types": [
                "OFFLINE_WITHHOLD"
            ],
            "intervalMinute": 0,
            "intervalHour": intervalHour,
            "timeSpanHour": 12,
            "assetDelayIntervalHour": assetDelayIntervalHour,
            "except_channels": None,
            "include_channels": None
        },
        "product_trade_types": [
            "store_coupon"
        ],
        "notify_channels": [],
        "sms_tpl_conf": {
            "from_app_mapping": []
        },
        "restructureSwitch": True,
        "manualSwitch": True,
        "autoSwitch": True,
        "common_split_order_channel_list": [],
        "suspend_by_channel_message": [
            {
                "withhold_channel": "paysvr",
                "channel_message": [
                    "交易成功"
                ],
                "delay_minutes": 90
            }
        ],
        "suspend_last_fail_comment": {
            "fail_channel_message": [
                "余额不足"
            ],
            "delay_minutes": 20
        },
        "asset_reverse_notify_email": []
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_config_withhold", content, "KV")


def update_rbiz_capital_withhold_rule():
    content = {
        "default": {
            "normal": {
                "single_partial": False,
                "multi_partial": False,
                "multiPeriod": True,
                "prepay": True
            },
            "overdue": {
                "single_partial": False,
                "multi_partial": False,
                "multiPeriod": True,
                "prepay": True
            }
        },
        "advance_repay_config": {
            "service_name": "pak",
            "grace_days": 1,
            "deadline": "12:00:00"
        },
        "repay_trial_rule": {
            "fee_calculate_map": {
                "fin_service": "#currentPeriodAmount * (#useDays+1) / #occupyDays"
            }
        }
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_capital_withhold_rule", content, "KV")


def update_rbiz_refresh_fee_conf(max_overdue_days=120):
    content = {
        "max_fee_filter": False,
        "cmdb_conf": {
            "calculate_late": True,
            "save_late": True,
            "late_tolerance": 1,
            "calculate_asset_type": [
                "paydayloan"
            ]
        },
        "offline_channels": [
            "tha_bankcard",
            "nbmfc"
        ],
        "check_max_fee_switch": True,
        "max_overdue_days": max_overdue_days
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_refresh_fee_conf", content, "KV")


def update_rbiz_undo_decrease_config():
    content = {
        "days": -1
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_undo_decrease_config", content, "KV")


def update_rbiz_api_config(project=None):
    if project:
        base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/global_rbiz_auto_test" % project
    else:
        base_url = "https://gateway-api.kuainiujinke.com/biz-caiwu"
    content = {
        "baseUrl": "http://biz-repay1-svc.biz-tha.svc.cluster.local:8093",
        "accountStatementUrl": base_url + "/flow-query/get-account-statement",
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_api_config", content, "KV")


def update_rbiz_decrease_config(can_decrease_day=3):
    content = {"stb": {"decreaseRepay": True},
               "canDoDecreaseOverdueDays": can_decrease_day}
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "rbiz_decrease_config", content, "KV")


def update_account_statement_sync(data_source="paysvr", need_match=True):
    content = {
        "data_source": data_source,
        "bill_match_rule_config": {
            "need_match": need_match,
            "payment_type_list": ["ebank"],
            "payment_mode_list": [],
            "payment_option_list": ["ACCOUNT"]
        },
        "our_account_list": ["abc", "def"],
        "channel_name_list": ["abc", "def"]
    }
    gc.NACOS.update_configs("global-repay%s" % gc.ENV, "account_statement_sync", content, "KV")
