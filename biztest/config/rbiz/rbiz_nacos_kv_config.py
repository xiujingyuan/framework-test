# -*- coding: utf-8 -*-
import common.global_const as gc
from biztest.config.easymock.easymock_config import mock_project


def update_repay_paysvr_config(project=''):
    if project:
        base_url_tq = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/rbiz_auto_test" % project
    else:
        base_url_tq = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-payment-staging"
    content = {
        "api_config": {
            "payment_url": base_url_tq,
            "callback_url": gc.REPAY_URL,
            "withdraw_url": "/withdraw/autoWithdraw",
            "withdraw_query_url": "/withdraw/query",
            "url": base_url_tq
        },
        "channel_black_list": {
            "yixin_rongsheng": {
                "process_noloan": True,
                "repay_type": [],
                "provider_codes": "baofoo"
            },
            "beiyin_daqin": {
                "process_noloan": True,
                "repay_type": [],
                "provider_codes": "baofoo"
            },
            "lanzhou_haoyue_qinjia": {
                "process_noloan": True,
                "repay_type": [],
                "provider_codes": "baofoo"
            },
            "yilian_dingfeng": {
                "process_noloan": True,
                "repay_type": [],
                "provider_codes": "baofoo"
            },
            "weipin_zhongwei": {
                "process_noloan": True,
                "repay_type": [],
                "provider_codes": "baofoo"
            },
            "jinmeixin_daqin": {
                "process_noloan": True,
                "repay_type": [],
                "provider_codes": "baofoo"
            },
            "jinmeixin_hanchen": {
                "process_noloan": True,
                "repay_type": [],
                "provider_codes": "baofoo"
            },
            "jincheng_hanchen": {
                "process_noloan": True,
                "repay_type": [],
                "provider_codes": "baofoo"
            },
            "lanzhou_haoyue": {
                "process_noloan": True,
                "repay_type": [
                    "early_settlement"
                ],
                "channels": "baofoo_qjj_protocol,baofoo_tq_protocol,baofoo_qjj_withhold,baofoo_tq_withhold",
                "provider_codes": "baofoo"
            },
            "zhongke_hegang": {
                "process_noloan": True,
                "repay_type": [
                    "early_settlement"
                ],
                "channels": "baofoo_qjj_protocol,baofoo_tq_protocol,baofoo_qjj_withhold,baofoo_tq_withhold",
                "provider_codes": "baofoo"
            },
            "mozhi_jinmeixin": {
                "process_noloan": True,
                "repay_type": [
                    "early_settlement"
                ],
                "channels": "baofoo_qjj_protocol,baofoo_tq_protocol,baofoo_qjj_withhold,baofoo_tq_withhold",
                "provider_codes": "baofoo"
            },
            "mozhi_beiyin_zhongyi": {
                "process_noloan": True,
                "repay_type": [
                    "early_settlement"
                ],
                "channels": "yeepay_qjj_protocol,yeepay_tq1_protocol",
                "provider_codes": "baofoo,yeepay"
            },
            "weishenma_daxinganling": {
                "process_noloan": True,
                "repay_type": [
                    "early_settlement"
                ],
                "channels": "yeepay_qjj_protocol,yeepay_tq1_protocol",
                "provider_codes": "yeepay"
            },
            "beiyin_tianbang": {
                "process_noloan": True,
                "repay_type": [
                    "early_settlement"
                ],
                "channels": "yeepay_qjj_protocol,yeepay_tq1_protocol",
                "provider_codes": "baofoo,yeepay"
            },
            "zhongke_lanzhou": {
                "process_noloan": True,
                "repay_type": [
                    "early_settlement"
                ],
                "provider_codes": "baofoo"
            }
        },
        "merchant": {
            "withhold": {
                "biz": {
                    "merchant_id": 3,
                    "merchant_md5": "b21f3f04444c407f0008bf46649d2bbe",
                    "merchant_name": "biz"
                },
                "trade": {
                    "merchant_id": 30,
                    "merchant_md5": "6317c1b418e84c4932790bf390cd5ae7",
                    "merchant_name": "rbiz"
                },
                "paydayloan": {
                    "merchant_id": 30,
                    "merchant_md5": "6317c1b418e84c4932790bf390cd5ae7",
                    "merchant_name": "rbiz",
                    "single": {
                        "merchant_id": 30,
                        "merchant_md5": "6317c1b418e84c4932790bf390cd5ae7",
                        "merchant_name": "rbiz"
                    },
                    "multiple": {
                        "merchant_id": 30,
                        "merchant_md5": "6317c1b418e84c4932790bf390cd5ae7",
                        "merchant_name": "rbiz"
                    },
                    "dkhk": {
                        "merchant_id": 12,
                        "merchant_md5": "d078a9993c33511a1d7e5890ad7eca7e",
                        "merchant_name": "dkhk"
                    },
                    "kkj": {
                        "merchant_id": 14,
                        "merchant_md5": "0316b5a2d5f8ce656b25d3d2178f4e8d",
                        "merchant_name": "kkj"
                    },
                    "xjdd": {
                        "merchant_id": 13,
                        "merchant_md5": "221737fd260aeeb1c214eb6f33a91b76",
                        "merchant_name": "xjdd"
                    },
                    "xjmb": {
                        "merchant_id": 15,
                        "merchant_md5": "da1ccb751bbebb81ceb7fe7b895778be",
                        "merchant_name": "xjmb"
                    },
                    "jdjk": {
                        "merchant_id": 16,
                        "merchant_md5": "4080cd944f1cac9d4caf799bedb4131c",
                        "merchant_name": "jdjk"
                    },
                    "trade": {
                        "merchant_id": 30,
                        "merchant_md5": "6317c1b418e84c4932790bf390cd5ae7",
                        "merchant_name": "rbiz"
                    },
                    "other": {
                        "merchant_id": 30,
                        "merchant_md5": "6317c1b418e84c4932790bf390cd5ae7",
                        "merchant_name": "rbiz"
                    }
                },
                "hospital": {
                    "merchant_id": 5,
                    "merchant_md5": "d36d01bf71f63a6836a1785f0a483ac2",
                    "merchant_name": "kfq"
                },
                "guarantee": {
                    "merchant_id": 10,
                    "merchant_md5": "cf6d003a82b35237ff4c1a2ffe52e3ca",
                    "merchant_name": "DBD"
                },
                "eliteloan": {
                    "merchant_id": 11,
                    "merchant_md5": "6327c247a3621ab6d35cb7ed2c82a0e0",
                    "merchant_name": "JYD"
                }
            },
            "withdraw": {},
            "bind_card": {}
        },
        "rbiz": {
            "merchant_id": "30",
            "merchant_md5": "6317c1b418e84c4932790bf390cd5ae7"
        },
        "maintenance": {},
        "withdraw_config": {
            "merchant_name": "rbiz",
            "merchant_id": 30,
            "merchant_md5": "6317c1b418e84c4932790bf390cd5ae7",
            "withdraw_callback_url": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/repay1/paysvr/withdraw/callback"
        },
        "sign_company_config": {
            "sign_subject_domain_mapping": [
                {
                    "sign_company": [
                        "qjj"
                    ],
                    "config_priority": 1,
                    "payment_domain": "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5de5d515d1784d36471d6041/rbiz_auto_test",
                    "callback_domain": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/repay1"
                }
            ],
            "sign_subject": {
                "default": "tq",
                "dsq": "tq,tqa,tqb",
                "banana": "tq,tqa,tqb",
                "strawberry": "tq,tqa,tqb",
                "cash": "tq",
                "kfq": "tq",
                "dkhk": "tq",
                "kkj": "tq",
                "kn_dsq_duolaidianqjj_paydayloan": "tq",
                "kn_strawberry_duolaidianqjj_paydayloan": "tq",
                "kn_banana_duolaidianqjj_paydayloan": "tq",
                "kn_dsq_tongrongmiyang_paydayloan": "qjj",
                "kn_dsq_duolaidianmiyang_paydayloan": "qjj",
                "kn_dsq_duolaidianmiyangnew_paydayloan": "qjj",
                "kn_dsq_longshangmiyang_paydayloan": "qjj",
                "kn_banana_tongrongmiyang_paydayloan": "qjj",
                "kn_banana_duolaidianmiyang_paydayloan": "qjj",
                "kn_banana_duolaidianmiyangnew_paydayloan": "qjj",
                "kn_banana_longshangmiyang_paydayloan": "qjj",
                "kn_strawberry_tongrongmiyang_paydayloan": "qjj",
                "kn_strawberry_duolaidianmiyang_paydayloan": "qjj",
                "kn_strawberry_duolaidianmiyangnew_paydayloan": "qjj",
                "kn_strawberry_longshangmiyang_paydayloan": "qjj",
                "kn_banana_tongrongqianjingjing_paydayloan": "qjj",
                "kn_strawberry_tongrongqianjingjing_paydayloan": "qjj",
                "kn_strawberry_haohanqianjingjing_paydayloan": "qjj",
                "kn_banana_haohanqianjingjing_paydayloan": "qjj",
                "kn_pitaya_huabei_runqian_paydayloan": "tq",
                "kn_dsq_tongrongbiaonei_paydayloan": "tq",
                "kn_banana_tongrongbiaonei_paydayloan": "tq",
                "kn_strawberry_tongrongbiaonei_paydayloan": "tq",
                "kn_pitaya_tongrongbiaonei_paydayloan": "tq"
            },
            "sign_subject_mapping": [],
            "all_sign_company_list": [
                "tq",
                "tqa",
                "tqb",
                "qjj"
            ]
        },
        "user_ip": [
            "115.159.91.52"
        ],
        "channel_mapping": [],
        "channel_write_back_list": [
            "hami_tianshan",
            "shilong_siping",
            "hami_tianshan_tianbang",
            "longjiang_daqin",
            "hamitianbang_xinjiang",
            "lanzhou_haoyue",
            "zhongke_hegang",
            "yilian_dingfeng",
            "lanzhou_haoyue_qinjia"
        ],
        "batch_sign_bind_card_url": base_url_tq + "/batchBinding/uploadBindingCard"
    }
    gc.NACOS.update_configs("repay" + str(gc.ENV), "repay_paysvr_config", content, "KV")


def update_repay_refund_config(project=''):
    if project:
        base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/rbiz_auto_test" % project
    else:
        base_url = "http://repay%s.k8s-ingress-nginx.kuainiujinke.com/" % gc.ENV
    refund = {
        "usefulChannels": [],
        "offline_refund_channels": {},
        "force_refund_url": "%s/page/force-withhold-refund" % base_url,
        "withdraw_conf": {
            "delay_days": 1,
            "withdraw_time": "16:00",
            "sign_company_withdraw_channel_mapping": [
                {
                    "sign_company": [
                        "my,my1"
                    ],
                    "withdraw_channel": "qsq_cpcn_tq_quick"
                },
                {
                    "sign_company": [
                        "tq,tqa,tqb"
                    ],
                    "withdraw_channel": "qsq_cpcn_tq_quick"
                }
            ]
        },
        "repeated_refund_url": "%s/repeatedWithhold/refund" % base_url
    }
    gc.NACOS.update_configs("repay" + str(gc.ENV), "repay_refund_config", refund, "KV")


def update_repay_hami_tianshan_tianbang_config(project=''):
    if project:
        base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/rbiz_auto_test/hamitianshan/" % project
    else:
        base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/gate%s/hamitianshan/" % gc.ENV
    hami = {
        "open": True,
        "withhold_auto_retry": {
            "from_rbiz": {
                "fail_switch_paysvr": {
                    "open": True,
                    "comment_black_list": [],
                    "interval_minutes": 2
                }
            }
        },
        "extendOverdueDays": 3,
        "notifyOpen": True,
        "skipCheckTranFinish": True,
        "signCompany": "hm",
        "first_withhold_channel": "hami_tianshan_tianbang",
        "repay_time": "05:00:00,20:30:00",
        "settle_intertemporal_limit": True,
        "api_config": {
            "gate_url": base_url,
            "withholdNotify": "A010",
            "RepayNotify": "B002"
        },
        "open_channel": True,
        "split_order_type": "capital_rule",
        "route_rules": [
            {
                "route_type": "settle_day_at_due_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "settle_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "last_period_settle",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "repay_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "multi_repay",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "single_repay_intertemporal",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "check_only_current_period",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "settle",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "capital_special_change",
                "route_value": {
                    "auto": {
                        "times": 1,
                        "calByDay": False
                    },
                    "active": {
                        "times": 1,
                        "calByDay": False
                    },
                    "manual": {
                        "times": 1,
                        "calByDay": False
                    }
                },
                "change_paysvr": True
            },
            {
                "route_type": "asset_white_list",
                "route_value": "S2021062379499568367,B2021082279601398550,B2021082562431361682,B2021082656803194938,S2021032556013564129,B2021041466671506855",
                "change_paysvr": True
            }
        ]
    }
    gc.NACOS.update_configs("repay" + str(gc.ENV), "repay_hami_tianshan_tianbang_config", hami, "KV")


def update_repay_hami_tianshan_config(project=''):
    if project:
        base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/rbiz_auto_test/hami_tianshan/" % project
    else:
        base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/gate%s/hamitianshan/" % gc.ENV
    hami = {
        "open": True,
        "withhold_auto_retry": {
            "from_rbiz": {
                "fail_switch_paysvr": {
                    "open": False,
                    "comment_black_list": [],
                    "interval_minutes": 2
                }
            }
        },
        "extendOverdueDays": 3,
        "notifyOpen": True,
        "skipCheckTranFinish": True,
        "signCompany": "hm",
        "first_withhold_channel": "hami_tianshan",
        "repay_time": "05:00:00,20:30:00",
        "settle_intertemporal_limit": True,
        "api_config": {
            "gate_url": base_url,
            "withholdNotify": "A010",
            "RepayNotify": "B002"
        },
        "open_channel": True,
        "split_order_type": "capital_rule",
        "route_rules": [
            {
                "route_type": "settle_day_at_due_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "settle_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "repay_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "multi_repay",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "check_only_current_period",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "settle",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "capital_special_change",
                "route_value": {
                    "auto": {
                        "times": 1,
                        "calByDay": False
                    },
                    "active": {
                        "times": 1,
                        "calByDay": False
                    },
                    "manual": {
                        "times": 1,
                        "calByDay": False
                    }
                },
                "change_paysvr": True
            },
            {
                "route_type": "asset_white_list",
                "route_value": "S202008219823717884925101,B202101135045344059079894",
                "change_paysvr": True
            }
        ]
    }
    gc.NACOS.update_configs("repay" + str(gc.ENV), "repay_hami_tianshan_config", hami, "KV")


def update_repay_hamitianbang_xinjiang_config(project=''):
    if project:
        base_url = "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/%s/rbiz_auto_test/hamitianshan/" % project
    else:
        base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/gate%s/hamitianshan/" % gc.ENV
    hami = {
        "open": True,
        "withhold_auto_retry": {
            "from_rbiz": {
                "fail_switch_paysvr": {
                    "open": False,
                    "comment_black_list": [],
                    "interval_minutes": 2
                }
            }
        },
        "extendOverdueDays": 3,
        "notifyOpen": True,
        "skipCheckTranFinish": True,
        "signCompany": "hm",
        "first_withhold_channel": "hamitianbang_xinjiang",
        "repay_time": "05:00:00,20:30:00",
        "settle_intertemporal_limit": True,
        "api_config": {
            "gate_url": base_url,
            "withholdNotify": "A010",
            "RepayNotify": "B002"
        },
        "open_channel": True,
        "split_order_type": "capital_rule",
        "route_rules": [
            {
                "route_type": "check_only_current_period",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "settle",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "advance_support",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "settle_day_at_due_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "settle_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "repay_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "multi_repay",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "capital_special_change",
                "route_value": {
                    "auto": {
                        "times": 1,
                        "calByDay": False
                    },
                    "active": {
                        "times": 1,
                        "calByDay": False
                    },
                    "manual": {
                        "times": 1,
                        "calByDay": False
                    }
                },
                "change_paysvr": True
            },
            {
                "route_type": "asset_white_list",
                "route_value": "B2021072461793605713",
                "change_paysvr": True
            }
        ]
    }
    gc.NACOS.update_configs("repay" + str(gc.ENV), "repay_hamitianbang_xinjiang_config", hami, "KV")


def update_repay_lanzhou_config():
    lanzhou = {
        "open": True,
        "withhold_auto_retry": {
            "from_rbiz": {
                "fail_switch_paysvr": {
                    "open": False,
                    "comment_black_list": [],
                    "interval_minutes": 2
                }
            }
        },
        "skipCheckTranFinish": True,
        "signCompany": "hy",
        "first_withhold_channel": "lanzhou_haoyue",
        "settle_intertemporal_limit": False,
        "ledger_account_config": {
            "hy-002": [
                "repayprincipal",
                "repayinterest"
            ]
        },
        "open_channel": True,
        "split_order_type": "capital_rule",
        "split_order_rules": [
            {
                "conditions": [
                    "normal"
                ],
                "withholdItems": [
                    "repayprincipal",
                    "repayinterest"
                ],
                "usePaysvrChannel": False,
                "sameSignCompanyCombine": True,
                "sameChannelCombine": True,
                "signCompany": None,
                "combineWithNoLoan": False
            },
            {
                "conditions": [
                    "normal"
                ],
                "withholdItems": [
                    "after_loan_manage",
                    "technical_service",
                    "guarantee",
                    "consult",
                    "reserve"
                ],
                "usePaysvrChannel": True,
                "sameSignCompanyCombine": True,
                "sameChannelCombine": True,
                "signCompany": None,
                "combineWithNoLoan": False
            },
            {
                "conditions": [
                    "overdue"
                ],
                "withholdItems": [
                    "repayprincipal",
                    "repayinterest",
                    "after_loan_manage",
                    "technical_service",
                    "lateinterest",
                    "consult",
                    "reserve",
                    "guarantee"
                ],
                "usePaysvrChannel": True,
                "sameSignCompanyCombine": False,
                "sameChannelCombine": False,
                "signCompany": None,
                "combineWithNoLoan": False
            }
        ],
        "route_rules": [
            {
                "route_type": "settle_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": True
            },
            {
                "route_type": "settle",
                "route_value": "N",
                "change_paysvr": True
            },
            {
                "route_type": "multi_repay",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "repay_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": True
            },
            {
                "route_type": "fail_times",
                "route_value": {
                    "auto": {
                        "times": 1,
                        "calByDay": True
                    },
                    "active": {
                        "times": 1,
                        "calByDay": True
                    },
                    "manual": {
                        "times": 1,
                        "calByDay": True
                    }
                },
                "change_paysvr": True
            },
            {
                "route_type": "partial_repay",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "after_grant_date_limit",
                "route_value": "29",
                "change_paysvr": True
            },
            {
                "route_type": "advance_support",
                "route_value": "N",
                "change_paysvr": True
            }
        ]
    }
    gc.NACOS.update_configs("repay" + str(gc.ENV), "repay_lanzhou_haoyue_config", lanzhou, "KV")


def update_repay_zhongke_hegang_config(item_no=""):
    zhongke_hegang = {
        "open": True,
        "withhold_auto_retry": {
            "from_rbiz": {
                "fail_switch_paysvr": {
                    "open": False,
                    "comment_black_list": [],
                    "interval_minutes": 2
                }
            }
        },
        "skipCheckTranFinish": True,
        "signCompany": "zhongrong",
        "api_config": {
            "channel_no_mapping": {
                "KN1-CL-HLJ": "KN1-CL",
                "KN1-CL-NOT-HLJ": "KN1-CL",
                "KN0-CL": "KN0-CL"
            },
            "ledger_account_config_list": [
                {
                    "product_codes": [
                        "KN0-CL"
                    ],
                    "ledger_account_config": {
                        "zhongrong-hg": [
                            "repayprincipal",
                            "repayinterest"
                        ],
                        "zhongrong-zr": [
                            "guarantee"
                        ],
                        "zhongrong-wd": [
                            "reserve",
                            "consult"
                        ]
                    }
                },
                {
                    "product_codes": [
                        "KN1-CL-HLJ",
                        "KN1-CL-NOT-HLJ"
                    ],
                    "ledger_account_config": {
                        "zhongrong-hg1": [
                            "repayprincipal",
                            "repayinterest"
                        ],
                        "zhongrong-zr": [
                            "guarantee"
                        ],
                        "zhongrong-wd": [
                            "reserve",
                            "consult"
                        ]
                    }
                }
            ],
            "trial_fail_code": [
                "9000"
            ]
        },
        "first_withhold_channel": "zhongke_hegang",
        "settle_intertemporal_limit": True,
        "open_channel": True,
        "split_order_type": "capital_rule",
        "route_rules": [
            {
                "route_type": "advance_support",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "last_period_settle",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "repay_time",
                "route_value": "00:00:00,23:00:00",
                "change_paysvr": True
            },
            {
                "route_type": "settle_day_at_due_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "settle_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "normal_time_limit",
                "route_value": {
                    "startTime": "00:00:00",
                    "endTime": "23:00:00"
                },
                "change_paysvr": True
            },
            {
                "route_type": "settle",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "multi_repay",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "repay_day_at_grant_at",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "fail_times",
                "route_value": {
                    "auto": {
                        "times": 1,
                        "calByDay": True
                    },
                    "active": {
                        "times": 1,
                        "calByDay": True
                    },
                    "manual": {
                        "times": 1,
                        "calByDay": True
                    }
                },
                "change_paysvr": True
            },
            {
                "route_type": "partial_repay",
                "route_value": "N",
                "change_paysvr": False
            },
            {
                "route_type": "check_only_current_period",
                "route_value": "Y",
                "change_paysvr": False
            },
            {
                "route_type": "asset_white_list",
                "route_value": item_no,
                "change_paysvr": True
            }
        ]
    }
    gc.NACOS.update_configs("repay" + str(gc.ENV), "repay_zhongke_hegang_config", zhongke_hegang, "KV")


if __name__ == "__main__":
    for env in (1, 2, 3, 4, 9):
        gc.ENV = env
        project_id = mock_project['rbiz_auto_test']['id']
        update_repay_paysvr_config(project_id)
        update_repay_refund_config(project_id)
        update_repay_hami_tianshan_config(project_id)
        update_repay_hami_tianshan_tianbang_config(project_id)
        update_repay_hamitianbang_xinjiang_config(project_id)
        update_repay_shilong_siping_config(project_id)
        update_repay_weishenma_config(project_id)
        update_repay_lanzhou_config()
        update_repay_mozhi_beiyin_zhongyi_config()
        update_repay_longjiang_daqin_config()
        update_repay_huabei_runqian_config()
        update_repay_qinnong_config(project_id)
        update_repay_qinnong_jieyi_config(project_id)
