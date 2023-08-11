# -*- coding: utf-8 -*-
import biztest.config.gbiz.gbiz_common_config as gbiz_common_config
import common.global_const as gc


def update_gbiz_capital_huabei_runqian():
    huabei_runqian = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "ChangeCapital"
        ],
        "register_config": {
            "is_multi_account_card_allowed": True,
            "account_register_duration": 60,
            "account_recall_register_duration": 240,
            "must_bind_one_groups": [
                "kuainiu"
            ],
            "ref_accounts": [
                "wsm_dxal_account"
            ],
            "is_strict_seq": False,
            "register_step_list": [
                {
                    "channel": "huabei_runqian",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "allow_fail": True,
                    "register_status_effect_duration": 0,
                    "need_confirm_result": True,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": True,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36')",
                            "err_msg": "华北润乾[资产还款总额]不满足 irr36，请关注！"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "-1",
                                "messages": [
                                    "订单编号已存在"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "-1",
                                "messages": [
                                    "进件失败"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(30)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "3"
                            },
                            {
                                "code": "10003"
                            },
                            {
                                "code": "99999",
                                "messages": [
                                    "贷款申请信息不存在"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "-1"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(30)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "3"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "99999",
                                "messages": [
                                    "放款审批中"
                                ]
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -1,
                        "max_value": 1
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_huabei_runqian", huabei_runqian)


def update_gbiz_capital_siping_jiliang():
    siping_jiliang = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "manual_reverse_allowed": True,
        "register_config": {
            "is_multi_account_card_allowed": True,
            "account_register_duration": 60,
            "account_recall_register_duration": 10,
            "register_step_list": [
                {
                    "channel": "siping_jiliang",
                    "step_type": "PROTOCOL",
                    "way": "siping_jiliang",
                    "interaction_type": "SMS",
                    "group": "siping_jiliang",
                    "allow_fail": False,
                    "need_confirm_result": False,  # 反查，mock情况需要设置成false
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irrByDay(#loan,'36','365per_year','D$24','D$24')",
                            "err_msg": "四平吉良[资产还款总额]不满足 irr36（按日365天，月结日D$24，结清日D$24），请关注！"
                        }
                    ]
                }
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            },
            "LoanPreApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "21"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "20"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "3"
                            },
                            {
                                "code": "5"
                            },
                            {
                                "code": "2001030",
                                "messages": [
                                    "授信流水号不存在"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "2",
                                "messages": [
                                    "AUDIT_SUCCESS",
                                    "成功"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "40"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1111111",
                                "messages": [
                                    "这是mockcode返回失败"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1008"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1007"
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "RongDanIrrTrial": {
                "execute": {
                    "trail_irr_limit": 33
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_siping_jiliang", siping_jiliang)


def update_gbiz_capital_shilong_siping():
    shilong_siping = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "rate_limit_groups": {
            "shilong_siping_ftp_limit": [
                "LoanPreApply",
                "LoanPostApply"
            ],
            "shilong_siping_api_limit": [
                "LoanApplyNew",
                "LoanApplyQuery",
                "LoanApplyConfirm",
                "LoanConfirmQuery",
                "CapitalRepayPlanQuery",
                "ChangeCapital"
            ]
        },
        "register_config": {
            "is_multi_account_card_allowed": True,
            "account_register_duration": 60,
            "account_recall_register_duration": 10,
            "ref_accounts": [
                "wsm_dxal_account"
            ],
            "register_step_list": [
                {
                    "channel": "shilong_siping",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "allow_fail": True,
                    "need_confirm_result": True,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "raise_limit_allowed": True,
        "raise_limit_standard_amount": 1000000,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "UserConfirmTimeOutEvent": "LoanConfirmQuery",
                        "LoanPostApplyFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,36)",
                            "err_msg": "大单还款总额不满足irr36！"
                        }
                    ]
                }
            },
            "LoanPreApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyNew": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "20"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
                            },
                            {
                                "code": "21"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "30"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "3"
                            },
                            {
                                "code": "5"
                            },
                            {
                                "code": "2001030"
                            }
                        ]
                    }
                ]
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "40"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [

                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(180)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1007"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1008"
                            }
                        ]
                    }
                ]
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_shilong_siping", shilong_siping)


def update_gbiz_capital_hami_tianshan_tianbang():
    content = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "ChangeCapital"
        ],
        "register_config": {
            "is_multi_account_card_allowed": True,
            "ref_accounts": [

            ],
            "register_step_list": [
                {
                    "channel": "hami_tianshan_tianbang",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
                    "interaction_type": "SMS",
                    "group": "hami",
                    "allow_fail": True,
                    "need_confirm_result": True,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": True,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanPostApplyFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36')",
                            "err_msg": "哈密天邦（全国）[资产还款总额]不满足 irr36，请关注！"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2"
                            },
                            {
                                "code": "1100069"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delayMinutes(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10001"
                            }

                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "10002"
                            },
                            {
                                "code": "1100011"
                            },
                            {
                                "code": "22",
                                "messages": [
                                    " "
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayMinutes(60)"
                }
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": ""
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2"
                            },
                            {
                                "code": "22",
                                "messages": [
                                    " "
                                ]
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "CertificateDownload": {}
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hami_tianshan_tianbang", content)


def update_gbiz_capital_hamitianbang_xinjiang():
    content = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "ChangeCapital"
        ],
        "register_config": {
            "register_step_list": [
                {
                    "channel": "hamitianbang_xinjiang",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq  ",
                    "interaction_type": "SMS",
                    "group": "hami",
                    "status_scene": {
                        "register": {
                            "success_type": "executed",
                            "allow_fail": True,
                            "need_confirm_result": True
                        },
                        "route": {
                            "success_type": "executed",
                            "allow_fail": True
                        },
                        "validate": {
                            "success_type": "executed"
                        }
                    },
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": True,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanPostApplyFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    " "
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36')",
                            "err_msg": "哈密天邦（新疆）[资产还款总额]不满足 irr36，请关注！"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2"
                            },
                            {
                                "code": "1100069"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delayMinutes(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10001"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "10002"
                            },
                            {
                                "code": "1100011"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "10000"
                            }
                        ]
                    }
                ]
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayMinutes(60)"
                }
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": ""
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "CertificateDownload": {

            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hamitianbang_xinjiang", content)


def update_gbiz_capital_jingque_haikou():
    jingque_haikou = {
        "register_config": {
            "ref_accounts": [
                "wsm_dxal_account"
            ],
            "is_multi_account_card_allowed": True,
            "account_register_duration": 60,
            "account_recall_register_duration": 240,
            "must_bind_one_groups": [
                "jingque_haikou"
            ],
            "register_step_list": [
                {
                    "channel": "jingque_haikou",
                    "step_type": "PROTOCOL",
                    "way": "jingque_haikou",
                    "interaction_type": "SMS",
                    "register_status_effect_duration": 365,
                    "need_confirm_result": True,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,36)",
                            "err_msg": "大单还款总额不为irr36"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": ""
                            }
                        ]
                    }
                ]
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                }
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(30)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "grantSuccess"
                        },
                        "matches": [
                            {
                                "code": "30"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "40"
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jingque_haikou", jingque_haikou)


def update_gbiz_capital_qinnong():
    body = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "register_config": {
            "multiAccountCardAllowed": True,
            "strictSeq": True,
            "account_register_duration": 60,
            "account_recall_register_duration": 240,
            "must_bind_one_groups": [
                "kuainiu"
            ],
            "ref_accounts": [],
            "is_multi_account_card_allowed": True,
            "is_strict_seq": True,
            "register_step_list": [
                {
                    "channel": "qinnong",
                    "group": "kuainiu",
                    "way": "tq",
                    "strictSeq": True,
                    "step_type": "PAYSVR_PROTOCOL",
                    "interaction_type": "SMS",
                    "allow_fail": True,
                    "register_status_effect_duration": 0,
                    "allow_retry": True,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "UserConfirmTimeOutEvent": "LoanConfirmQuery",
                        "LoanPostApplyFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "二次核验未命中\\[fail\\]或\\[updateCard\\]策略.*"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "-10000",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36','360per_year','D$25','D+0')",
                            "err_msg": "秦农[资产还款总额]不满足 irr36（月结日D$25，结清日D+0），请关注！"
                        }
                    ]
                }
            },
            "LoanPreApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(30)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10000002"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "10000007"
                            },
                            {
                                "code": "10000"
                            },
                            {
                                "code": "601002",
                                "messages": [
                                    "借款申请不存在"
                                ]
                            },
                            {
                                "code": "10000",
                                "messages": [
                                    "借款申请不存在"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": []
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(180)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10000004"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "10000008"
                            },
                            {
                                "code": "10000006",
                                "messages": []
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -1,
                        "max_value": 1
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "AssetConfirmOverTimeCheck": {
                "execute": {
                    "raise_limit_over_time_seconds": 600
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delaySeconds(240)"
                }
            },
            "CertificateDownload": {
                "init": {
                    "delay_time": "delaySeconds(3)"
                }
            },
            "CertificateApply": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "1",
                                "messages": [
                                    "结清证明申请处理失败：结清证明申请已存在"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "结清证明申请处理失败：资产未结清或未结算完成"
                                ]
                            },
                            {
                                "code": "100010",
                                "messages": [
                                    "系统正在维护中，请稍后再试"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_qinnong", body)


def update_gbiz_capital_qinnong_const(raise_limit_allowed=False):
    body = {
        "merchantId": "kn_qyd",
        "ftpChannelName": "qinnong",
        "raiseLimitStandardAmount": 1000000,
        "raiseLimitAllowed": raise_limit_allowed,
        "productCodeMap": {
            "6": "QN_KN_PDT_6",
            "12": "QN_KN_PDT_12"
        },
        "guaranteeConfig": {
            "ftpChannelName": "tianbang_qinnong",
            "ftpUploadPath": "/upload/KNQN01/receive/",
            "projectCode": "KNQN01",
            "interestRate": "0.078"
        },
        "ftpPath": "/10002",
        "knftpPath": "/10002",
        "guaranteeCompany": "kn_tianbang",
        "loanUsageMap": {
            "1": 9,
            "2": 2,
            "3": 5,
            "4": 11,
            "5": 3,
            "6": 0,
            "7": 0,
            "8": 11,
            "9": 9,
        },
        "orderStatusMap": {
            "commit": "10000001",
            "pass": "10000002",
            "grant": "10000003",
            "repay": "10000004",
            "payoff": "10000005",
            "invalid": "10000006",
            "refuse": "10000007",
            "failed": "10000008"
        },
        "marriageMap": {
            "1": 1,
            "2": 2,
            "3": 1,
            "4": 1
        },
        "relationMap": {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 1,
            "4": 3,
            "5": 3,
            "6": 3,
            "7": 3,
        },
        "bankCodeMap": {
            "hxb": "03040000",
            "bjbank": "04031000",
            "boc": "01040000",
            "cmb": "03080010",
            "icbc": "01020000",
            "ccb": "01050000",
            "cib": "03090000",
            "ceb": "03030000",
            "abc": "01040000",
            "psbc": "01000000",
            "cmbc": "03050000",
            "spdb": "03100000",
            "comm": "03010000",
            "pab": "03070010",
            "shbank": "04010000",
            "gdb": "03060000",
            "citic": "03020000"
        },
        "jobMap": {
            "1": "30704",
            "2": "30400",
            "3": "30400",
            "4": "10221",
            "5": "50600",
            "6": "30500",
            "7": "50600",
            "8": "10213",
            "9": "30600",
            "10": "52499",
            "11": "10799",
            "12": "20100",
            "13": "52499",
            "14": "20102",
            "15": "40000"
        },
        "qinnongAuthContractConfigDtos": [
            {
                "knType": "1",
                "qinongType": "bank_idcard_face",
                "qinongText": "身份证正面",
                "qinnongFileTemplateKey": "01_%s_%s_certFileA.jpg"
            },
            {
                "knType": "2",
                "qinongType": "bank_idcard_back",
                "qinongText": "身份证反面",
                "qinnongFileTemplateKey": "01_%s_%s_certFileB.jpg"
            },
            {
                "knType": "29",
                "qinongType": "bank_living_photo",
                "qinongText": "活体照片",
                "qinnongFileTemplateKey": "01_%s_%s_livingRecognition.jpg"
            }
        ],
        "qinnongGuaranteeContractConfigDtos": [
            {
                "knType": "30402",
                "qinongType": "bank_guarantee_protocol",
                "qinongText": "担保函",
                "qinnongFileTemplateKey": "01_%s_%s_guarantee_letter.pdf"
            },
            {
                "knType": "30403",
                "qinongType": "bank_entrust_guarantee_protocol",
                "qinongText": "委托担保协议",
                "qinnongFileTemplateKey": "01_%s_%s_guarantee.pdf"
            }
        ],
        "qinnongDownLoadContractConfigDtos": [
            {
                "qinongType": "loanContract",
                "qinongText": "借款协议",
                "knType": "28"
            },
            {
                "qinongType": "creditAuthorize",
                "qinongText": "个人征信授权协议",
                "knType": "30404"
            },
            {
                "qinongType": "personalInfoAuthorize",
                "qinongText": "个人信息使用授权协议",
                "knType": "30405"
            },
            {
                "qinongType": "bank_electronic_loan_IOU",
                "qinongText": "借款借据",
                "knType": "30406"
            }
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_qinnong_const", body)


def update_gbiz_capital_qinnong_jieyi_const(raise_limit_allowed=False):
    body = {
        "merchantId": "kn_qyd",
        "ftpChannelName": "qinnong",
        "raiseLimitStandardAmount": 1000000,
        "raiseLimitAllowed": raise_limit_allowed,
        "productCodeMap": {
            "6": "QN_KN_PDT_6",
            "12": "QN_KN_PDT_12"
        },
        "guaranteeConfig": {

            "ftpChannelName": "jieyi_qinnong",

            "ftpUploadPath": "/upload/test/",
            "projectCode": "KNQNJY01",
            "interestRate": "0.078"
        },
        "ftpPath": "/10002",
        "knftpPath": "/10002",
        "guaranteeCompany": "kn_jieyi",
        "loanUsageMap": {
            "1": 9,
            "2": 2,
            "3": 5,
            "4": 11,
            "5": 3,
            "6": 0,
            "7": 0,
            "8": 11,
            "9": 9,
        },
        "orderStatusMap": {
            "commit": "10000001",
            "pass": "10000002",
            "grant": "10000003",
            "repay": "10000004",
            "payoff": "10000005",
            "invalid": "10000006",
            "refuse": "10000007",
            "failed": "10000008"
        },
        "marriageMap": {
            "1": 1,
            "2": 2,
            "3": 1,
            "4": 1
        },
        "relationMap": {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 1,
            "4": 3,
            "5": 3,
            "6": 3,
            "7": 3,
        },
        "bankCodeMap": {
            "hxb": "03040000",
            "bjbank": "04031000",
            "boc": "01040000",
            "cmb": "03080010",
            "icbc": "01020000",
            "ccb": "01050000",
            "cib": "03090000",
            "ceb": "03030000",
            "abc": "01040000",
            "psbc": "01000000",
            "cmbc": "03050000",
            "spdb": "03100000",
            "comm": "03010000",
            "pab": "03070010",
            "shbank": "04010000",
            "gdb": "03060000",
            "citic": "03020000"
        },
        "jobMap": {
            "1": "30704",
            "2": "30400",
            "3": "30400",
            "4": "10221",
            "5": "50600",
            "6": "30500",
            "7": "50600",
            "8": "10213",
            "9": "30600",
            "10": "52499",
            "11": "10799",
            "12": "20100",
            "13": "52499",
            "14": "20102",
            "15": "40000"
        },
        "qinnongAuthContractConfigDtos": [
            {
                "knType": "1",
                "qinongType": "bank_idcard_face",
                "qinongText": "身份证正面",
                "qinnongFileTemplateKey": "01_%s_%s_certFileA.jpg"
            },
            {
                "knType": "2",
                "qinongType": "bank_idcard_back",
                "qinongText": "身份证反面",
                "qinnongFileTemplateKey": "01_%s_%s_certFileB.jpg"
            },
            {
                "knType": "29",
                "qinongType": "bank_living_photo",
                "qinongText": "活体照片",
                "qinnongFileTemplateKey": "01_%s_%s_livingRecognition.jpg"
            }
        ],
        "qinnongGuaranteeContractConfigDtos": [
            {
                "knType": "30702",
                "qinongType": "bank_guarantee_protocol",
                "qinongText": "担保函",
                "qinnongFileTemplateKey": "01_%s_%s_guarantee_letter.pdf"
            },
            {
                "knType": "30703",
                "qinongType": "bank_entrust_guarantee_protocol",
                "qinongText": "委托担保协议",
                "qinnongFileTemplateKey": "01_%s_%s_guarantee.pdf"
            }
        ],
        "qinnongDownLoadContractConfigDtos": [
            {
                "qinongType": "loanContract",
                "qinongText": "借款协议",
                "knType": "28"
            },
            {
                "qinongType": "creditAuthorize",
                "qinongText": "个人征信授权协议",
                "knType": "30404"
            },
            {
                "qinongType": "personalInfoAuthorize",
                "qinongText": "个人信息使用授权协议",
                "knType": "30405"
            },
            {
                "qinongType": "bank_electronic_loan_IOU",
                "qinongText": "借款借据",
                "knType": "30406"
            }
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_qinnong_jieyi_const", body)


def update_gbiz_capital_qinnong_dingfeng_const(raise_limit_allowed=False):
    body = {
        "merchantId": "K02040880612870088K",
        "ftpChannelName": "qinnong",
        "raiseLimitStandardAmount": 1000000,
        "raiseLimitAllowed": raise_limit_allowed,
        "productCodeMap": {
            "6": "QN_KN_PDT_6",
            "12": "QN_KN_PDT_12"
        },
        "ftpPath": "/10002",
        "knftpPath": "",
        "marriageMap": {
            "1": 1,
            "2": 2,
            "3": 1,
            "4": 1
        },
        "relationMap": {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 1,
            "4": 3,
            "5": 3,
            "6": 3,
            "7": 3,
        },
        "bankCodeMap": {
            "hxb": "03040000",
            "bjbank": "04031000",
            "boc": "01040000",
            "cmb": "03080010",
            "icbc": "01020000",
            "ccb": "01050000",
            "cib": "03090000",
            "ceb": "03030000",
            "abc": "01040000",
            "psbc": "01000000",
            "cmbc": "03050000",
            "spdb": "03100000",
            "comm": "03010000",
            "pab": "03070010",
            "shbank": "04010000",
            "gdb": "03060000",
            "citic": "03020000"
        },
        "loanUsageMap": {
            "1": 9,
            "2": 2,
            "3": 5,
            "4": 11,
            "5": 3,
            "6": 0,
            "7": 0,
            "8": 11,
            "9": 9,
        },
        "orderStatusMap": {
            "commit": 10000001,
            "pass": 10000002,
            "grant": 10000003,
            "repay": 10000004,
            "payoff": 10000005,
            "invalid": 10000006,
            "refuse": 10000007,
            "failed": 10000008
        },
        "qinnongAuthContractConfigDtos": [
            {
                "knType": 1,
                "qinongType": "bank_idcard_face",
                "qinongText": "身份证正面",
                "qinnongFileTemplateKey": "01_%s_%s_certFileA.jpg"
            },
            {
                "knType": 2,
                "qinongType": "bank_idcard_back",
                "qinongText": "身份证反面",
                "qinnongFileTemplateKey": "01_%s_%s_certFileB.jpg"
            },
            {
                "knType": 29,
                "qinongType": "bank_living_photo",
                "qinongText": "活体照片",
                "qinnongFileTemplateKey": "01_%s_%s_livingRecognition.jpg"
            }
        ],
        "qinnongGuaranteeContractConfigDtos": [
            {
                "knType": 30780,
                "qinongType": "bank_guarantee_protocol",
                "qinongText": "担保函",
                "qinnongFileTemplateKey": "01_%s_%s_guarantee_letter.pdf"
            },
            {
                "knType": 30781,
                "qinongType": "bank_entrust_guarantee_protocol",
                "qinongText": "委托担保协议",
                "qinnongFileTemplateKey": "01_%s_%s_guarantee.pdf"
            }
        ],
        "qinnongDownLoadContractConfigDtos": [
            {
                "qinongType": "loanContract",
                "qinongText": "借款协议",
                "knType": 28
            },
            {
                "qinongType": "creditAuthorize",
                "qinongText": "个人征信授权协议",
                "knType": 30783
            },
            {
                "qinongType": "personalInfoAuthorize",
                "qinongText": "个人信息使用授权协议",
                "knType": 30784
            },
            {
                "qinongType": "bank_electronic_loan_IOU",
                "qinongText": "借款借据",
                "knType": 30785
            }
        ],
        "jobMap": {
            "1": "30704",
            "2": "30400",
            "3": "30400",
            "4": "10221",
            "5": "50600",
            "6": "30500",
            "7": "50600",
            "8": "10213",
            "9": "30600",
            "10": "52499",
            "11": "10799",
            "12": "20100",
            "13": "52499",
            "14": "20102",
            "15": "40000"
        },
        "certifySuccessCodeMapping": {
            "1": [
                "重复申请"
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_qinnong_dingfeng_const", body)


def update_tianbang_paydayloan(mock_url=''):
    if mock_url:
        base_url = mock_url
    else:
        base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/gate%s/tianbang/" % gc.ENV
    tianbang = {
        "base_url": base_url
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "tianbang_paydayloan", tianbang)


def update_gbiz_capital_qinnong_jieyi():
    body = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "register_config": {
            "is_multi_account_card_allowed": True,
            "account_register_duration": 60,
            "account_recall_register_duration": 240,
            "must_bind_one_groups": [
                "kuainiu"
            ],
            "ref_accounts": [],
            "register_step_list": [
                {
                    "channel": "qinnong_jieyi",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "allow_fail": True,
                    "register_status_effect_duration": 0,
                    "need_confirm_result": True,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "UserConfirmTimeOutEvent": "LoanConfirmQuery",
                        "LoanPostApplyFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36','360per_year','D$25','D+0')",
                            "err_msg": "秦农杰益[资产还款总额]不满足 irr36（月结日D$25，结清日D+0），请关注！"
                        }
                    ]
                }
            },
            "LoanPreApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(30)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10000002"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "10000007"
                            },
                            {
                                "code": "10000"
                            },
                            {
                                "code": "601002",
                                "messages": [
                                    "借款申请不存在"
                                ]
                            },
                            {
                                "code": "10000",
                                "messages": [
                                    "借款申请不存在"
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetConfirmOverTimeCheck": {
                "execute": {
                    "raise_limit_over_time_seconds": 600
                }
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": []
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10000004"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "10000008"
                            },
                            {
                                "code": "10000006"
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -896,
                        "max_value": 896
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                }
            },
            "CertificateDownload": {
                "init": {
                    "delay_time": "delaySeconds(3)"
                }
            },
            "CertificateApply": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "1",
                                "messages": [
                                    "结清证明申请处理失败：结清证明申请已存在"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }

    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_qinnong_jieyi", body)


def update_gbiz_capital_qinnong_dingfeng():
    body = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "register_config": {
            "is_multi_account_card_allowed": True,
            "account_register_duration": 60,
            "account_recall_register_duration": 240,
            "must_bind_one_groups": [
                "kuainiu"
            ],
            "ref_accounts": [],
            "register_step_list": [
                {
                    "channel": "qinnong_dingfeng",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "allow_fail": True,
                    "register_status_effect_duration": 0,
                    "need_confirm_result": True,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "UserConfirmTimeOutEvent": "LoanConfirmQuery",
                        "LoanPostApplyFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36','360per_year','D$25','D+0')",
                            "err_msg": "秦农鼎丰[资产还款总额]不满足 irr36（月结日D$25，结清日D+0），请关注！"
                        }
                    ]
                }
            },
            "LoanPreApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(30)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10000002"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "10000007"
                            },
                            {
                                "code": "10000"
                            },
                            {
                                "code": "601002",
                                "messages": [
                                    "借款申请不存在"
                                ]
                            },
                            {
                                "code": "10000",
                                "messages": [
                                    "借款申请不存在"
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetConfirmOverTimeCheck": {
                "execute": {
                    "raise_limit_over_time_seconds": 600
                }
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": []
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10000004"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "10000008"
                            },
                            {
                                "code": "10000006"
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -896,
                        "max_value": 896
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                }
            },
            "CertificateDownload": {
                "init": {
                    "delay_time": "delaySeconds(3)"
                }
            },
            "CertificateApply": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "1",
                                "messages": [
                                    "结清证明申请处理失败：结清证明申请已存在"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_qinnong_dingfeng", body)


def update_gbiz_capital_zhongke_lanzhou():
    zhongke_lanzhou = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "register_config": {
            "is_multi_account_card_allowed": True,
            "ref_accounts": [

            ],
            "register_step_list": [
                {
                    "channel": "zhongke_lanzhou",
                    "step_type": "PROTOCOL",
                    "way": "zhongke_lanzhou",
                    "interaction_type": "SMS",
                    "allow_fail": False,
                    "need_confirm_result": False,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode",
                            "extra_data": {
                                "sms_verify_seconds": 300
                            }
                        },
                        {
                            "type": "CheckSmsVerifyCode",
                            "async_result_query_retry_delay_time": 1000,
                            "async_result_query_max_retry_times": 10
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanCreditFailedEvent": "LoanCreditQuery",
                        "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'27')",
                            "err_msg": "中科兰州[资产还款总额]不满足 irr27，请关注！"
                        }
                    ]
                }
            },
            "LoanPreApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "2"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyNew": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {}
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(180)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1999901"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1900002",
                                "messages": []
                            }
                        ]
                    }
                ]
            },
            "LoanCreditApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanCreditQuery": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "2999901"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2900002"
                            }
                        ]
                    }
                ]
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delaySeconds(120)"
                }
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "3999904"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "3999903"
                            },
                            {
                                "code": "3999905"
                            },
                            {
                                "code": "3999909"
                            },
                            {
                                "code": "3999990"
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": True,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "CertificateApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "40000"
                            },
                            {
                                "code": "41200",
                                "messages": [
                                    "已存在该借据号的申请结清记录"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "结清证明申请处理失败：资产未结清或未结算完成"
                                ]
                            },
                            {
                                "code": "100010",
                                "messages": [
                                    "系统正在维护中，请稍后再试"
                                ]
                            }
                        ]
                    }
                ]
            },
            "CertificateDownload": {
                "init": {
                    "delay_time": "delayDays(1, \"08:00:00\")"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongke_lanzhou", zhongke_lanzhou)


def update_gbiz_capital_lanzhou_dingsheng_zkbc2():
    zhongke_lanzhou = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "register_config": {
            "is_multi_account_card_allowed": True,
            "ref_accounts": [

            ],
            "register_step_list": [
                {
                    "channel": "lanzhou_dingsheng_zkbc2",
                    "step_type": "PROTOCOL",
                    "way": "lanzhou_dingsheng_zkbc2",
                    "interaction_type": "SMS",
                    "allow_fail": False,
                    "need_confirm_result": False,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode",
                            "extra_data": {
                                "sms_verify_seconds": 300
                            }
                        },
                        {
                            "type": "CheckSmsVerifyCode",
                            "async_result_query_retry_delay_time": 1000,
                            "async_result_query_max_retry_times": 10
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanCreditFailedEvent": "LoanCreditQuery",
                        "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'27')",
                            "err_msg": "兰州鼎晟[资产还款总额]不满足 irr27，请关注！"
                        }
                    ]
                }
            },
            "LoanPreApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "2"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyNew": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {}
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(180)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1999901"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1900002",
                                "messages": []
                            }
                        ]
                    }
                ]
            },
            "LoanCreditApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanCreditQuery": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "2999901"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2900002"
                            }
                        ]
                    }
                ]
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delaySeconds(120)"
                }
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "3999904"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "3999903"
                            },
                            {
                                "code": "3999905"
                            },
                            {
                                "code": "3999909"
                            },
                            {
                                "code": "3999990"
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": True,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "CertificateApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "40000"
                            },
                            {
                                "code": "41200",
                                "messages": [
                                    "已存在该借据号的申请结清记录"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "结清证明申请处理失败：资产未结清或未结算完成"
                                ]
                            },
                            {
                                "code": "100010",
                                "messages": [
                                    "系统正在维护中，请稍后再试"
                                ]
                            }
                        ]
                    }
                ]
            },
            "CertificateDownload": {
                "init": {
                    "delay_time": "delayDays(1, \"08:00:00\")"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_dingsheng_zkbc2", zhongke_lanzhou)




def update_gbiz_capital_mozhi_beiyin_zhongyi():
    mozhi_beiyin = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "register_config": {
            "ref_accounts": [

            ],
            "is_multi_account_card_allowed": True,
            "account_register_duration": 60,
            "is_strict_seq": False,
            "register_step_list": [
                {
                    "channel": "mozhi_beiyin_zhongyi",
                    "step_type": "PROTOCOL",
                    "way": "BAOFU_KUAINIU",
                    "interaction_type": "SMS",
                    "allow_fail": False,
                    "register_status_effect_duration": 1,
                    "allow_retry": True,
                    "need_confirm_result": False,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode",
                            "allow_fail": False
                        },
                        {
                            "type": "CheckSmsVerifyCode",
                            "allow_fail": False
                        }
                    ]
                },
                {
                    "channel": "mozhi_beiyin_zhongyi",
                    "step_type": "PROTOCOL",
                    "way": "BEIYIN",
                    "interaction_type": "SMS",
                    "allow_fail": False,
                    "register_status_effect_duration": 1,
                    "allow_retry": True,
                    "need_confirm_result": False,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode",
                            "allow_fail": False
                        },
                        {
                            "type": "CheckSmsVerifyCode",
                            "allow_fail": False
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irrByDay(#loan,'35.64')",
                            "err_msg": "墨智北银[资产还款总额]不满足 irr35.64（按日360天），请关注！"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delayTime('5s')"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "1000000"
                            },
                            {
                                "code": "1300000",
                                "messages": [
                                    "额度查询:额度状态\\[AUDITING\\]"
                                ]
                            },
                            {
                                "code": "999999",
                                "messages": [
                                    "借款订单已存在.*"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1010003",
                                "messages": [
                                    "额度查询:额度状态\\[ACTIVE\\],额度使用状态\\[LIMIT_ERR\\],额度使用描述\\[可用额度不足不可借款\\]"
                                ]
                            },
                            {
                                "code": "1300000",
                                "messages": [
                                    "额度查询:额度状态\\[AUDITING\\]\\]"
                                ]
                            },
                            {
                                "code": "1100000"
                            },
                            {
                                "code": "1010005",
                                "messages": [
                                    "额度查询:额度状态\\[ACTIVE\\],额度使用状态\\[OTHER_ERR\\],额度使用描述\\[很抱歉，暂时无法提供借款服务。\\]"
                                ]
                            },
                            {
                                "code": "1500000"
                            },
                            {
                                "code": "998",
                                "messages": [
                                    "可用授信额度不足"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delayDays(1,\"04:00:00\")"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "100100"
                            },
                            {
                                "code": "999"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "100101"
                            },
                            {
                                "code": "998"
                            },
                            {
                                "code": "11002",
                                "messages": [
                                    "没有查询到记录"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "11005"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "90000"
                            },
                            {
                                "code": "998"
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delayTime('3s')"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "101000"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "101001"
                            },
                            {
                                "code": "101002",
                                "messages": []
                            },
                            {
                                "code": "90000",
                                "messages": [
                                    "交易流水不存在",
                                    "没有查询到记录",
                                    "用户可用授信信息异常",
                                    "用户获取授信信息异常2"
                                ]
                            },
                            {
                                "code": "11002",
                                "messages": [
                                    "交易流水不存在",
                                    "没有查询到记录",
                                    "用户可用授信信息异常",
                                    "用户获取授信信息异常2"
                                ]
                            }
                        ]
                    }
                ]
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayTime('3m')"
                }
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -1,
                        "max_value": 1
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delayTime('2m')"
                }
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_mozhi_beiyin_zhongyi", mozhi_beiyin)


def update_gbiz_capital_beiyin_tianbang():
    content = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "register_config": {
            "ref_accounts": [

            ],
            "is_multi_account_card_allowed": True,
            "account_register_duration": 60,
            "is_strict_seq": False,
            "register_step_list": [
                {
                    "channel": "beiyin_tianbang",
                    "step_type": "PROTOCOL",
                    "way": "BAOFU_KUAINIU2",
                    "interaction_type": "SMS",
                    "allow_fail": False,
                    "register_status_effect_duration": 1,
                    "allow_retry": True,
                    "need_confirm_result": False,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode",
                            "allow_fail": False
                        },
                        {
                            "type": "CheckSmsVerifyCode",
                            "allow_fail": False
                        }
                    ]
                },
                {
                    "channel": "beiyin_tianbang",
                    "step_type": "PROTOCOL",
                    "way": "BEIYIN",
                    "interaction_type": "SMS",
                    "allow_fail": False,
                    "register_status_effect_duration": 1,
                    "allow_retry": True,
                    "need_confirm_result": False,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode",
                            "allow_fail": False
                        },
                        {
                            "type": "CheckSmsVerifyCode",
                            "allow_fail": False
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irrByDay(#loan,'23.9994')",
                            "err_msg": "北银天邦[资产还款总额]不满足 irr23.9994（按日360天），请关注！"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delayTime('5s')"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "1000000"
                            },
                            {
                                "code": "1300000",
                                "messages": [
                                    "额度查询:额度状态\\[AUDITING\\]"
                                ]
                            },
                            {
                                "code": "999999",
                                "messages": [
                                    "借款订单已存在.*"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1010003",
                                "messages": [
                                    "额度查询:额度状态\\[ACTIVE\\],额度使用状态\\[LIMIT_ERR\\],额度使用描述\\[可用额度不足不可借款\\]"
                                ]
                            },
                            {
                                "code": "1300000",
                                "messages": [
                                    "额度查询:额度状态\\[AUDITING\\]\\]"
                                ]
                            },
                            {
                                "code": "1100000"
                            },
                            {
                                "code": "1010005",
                                "messages": [
                                    "额度查询:额度状态\\[ACTIVE\\],额度使用状态\\[OTHER_ERR\\],额度使用描述\\[很抱歉，暂时无法提供借款服务。\\]"
                                ]
                            },
                            {
                                "code": "1500000"
                            },
                            {
                                "code": "998",
                                "messages": [
                                    "可用授信额度不足"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delayTime('5s')"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "100100"
                            },
                            {
                                "code": "999"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "100101"
                            },
                            {
                                "code": "998"
                            },
                            {
                                "code": "11002",
                                "messages": [
                                    "没有查询到记录"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "11005"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "90000"
                            },
                            {
                                "code": "998"
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delayTime('3s')"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "101000"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "101001"
                            },
                            {
                                "code": "101002",
                                "messages": []
                            },
                            {
                                "code": "90000",
                                "messages": [
                                    "交易流水不存在",
                                    "没有查询到记录",
                                    "用户可用授信信息异常",
                                    "用户获取授信信息异常2"
                                ]
                            },
                            {
                                "code": "11002",
                                "messages": [
                                    "交易流水不存在",
                                    "没有查询到记录",
                                    "用户可用授信信息异常",
                                    "用户获取授信信息异常2"
                                ]
                            }
                        ]
                    }
                ]
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayTime('3m')"
                }
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -1,
                        "max_value": 1
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delayTime('2m')"
                }
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_beiyin_tianbang", content)


def update_gbiz_capital_mozhi_jinmeixin():
    mozhi_jinmeixin = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "register_config": {
            "is_multi_account_card_allowed": True,
            "account_register_duration": 40,
            "is_strict_seq": False,
            "register_step_list": [
                {
                    "channel": "mozhi_jinmeixin",
                    "step_type": "PROTOCOL",
                    "way": "BAOFU_KUAINIU",
                    "interaction_type": "SMS",
                    "allow_fail": False,
                    "register_status_effect_duration": 1,
                    "allow_retry": True,
                    "need_confirm_result": False,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode",
                            "allow_fail": False
                        },
                        {
                            "type": "CheckSmsVerifyCode",
                            "allow_fail": False
                        }
                    ]
                }
            ]
        },
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36')",
                            "err_msg": "墨智金美信[资产还款总额]不满足 irr36，请关注！"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "授信申请成功"
                                ]
                            },
                            {
                                "code": "1000000",
                                "messages": [
                                    "额度查询:额度状态\\[ACTIVE\\]"
                                ]
                            },
                            {
                                "code": "1300000",
                                "messages": [
                                    "额度查询:额度状态\\[AUDITING\\]"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "998",
                                "messages": [
                                    "可用授信额度不足"
                                ]
                            },
                            {
                                "code": "1010003",
                                "messages": [
                                    "额度查询:额度状态\\[ACTIVE\\],额度使用状态\\[LIMIT_ERR\\],额度使用描述\\[可用额度不足不可借款\\]"
                                ]
                            },
                            {
                                "code": "1010005",
                                "messages": [
                                    "额度查询:额度状态\\[ACTIVE\\],额度使用状态\\[OTHER_ERR\\],额度使用描述\\[很抱歉，暂时无法提供借款服务。\\]"
                                ]
                            },
                            {
                                "code": "11001",
                                "messages": [
                                    "账户不存在"
                                ]
                            },
                            {
                                "code": "1500000"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(120)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "100100"
                            },
                            {
                                "code": "999"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "100101"
                            },
                            {
                                "code": "998"
                            },
                            {
                                "code": "11002",
                                "messages": [
                                    "没有查询到记录"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "100103",
                                "messages": [
                                    "审核中"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
                            },
                            {
                                "code": "998"
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(120)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "101000"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "101002"
                            },
                            {
                                "code": "11002",
                                "messages": [
                                    "没有查询到记录",
                                    "借款订单不存在"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "101004",
                                "messages": [
                                    "APPLYING"
                                ]
                            },
                            {
                                "code": "99999",
                                "messages": [
                                    "系统繁忙，请10分钟后再试"
                                ]
                            }
                        ]
                    }
                ]
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayMinutes(240)"
                }
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -2,
                        "max_value": 2
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delayMinutes(2)"
                }
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_mozhi_jinmeixin", mozhi_jinmeixin)


def update_gbiz_repay_plan_config():
    body = {
        "default": {
            "min_value": 0,
            "max_value": 0
        },
        "tongrongmiyang": {
            "min_value": 0,
            "max_value": 0
        },
        "yunxin_quanhu": {
            "min_value": 0,
            "max_value": 0
        },
        "zhenjinfu": {
            "min_value": -1,
            "max_value": 1
        },
        "longshangmiyang": {
            "min_value": 0,
            "max_value": 0
        },
        "shoujin": {
            "min_value": 0,
            "max_value": 0
        },
        "huabeixiaodai_zhitou": {
            "min_value": 0,
            "max_value": 0
        },
        "hami_tianshan": {
            "min_value": 0,
            "max_value": 0
        },
        "weishenma_daxinganling": {
            "min_value": 0,
            "max_value": 0
        },
        "qinnong": {
            "min_value": -1,
            "max_value": 1
        }

    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_repay_plan_config", body)


def update_gbiz_msg_client_config():
    body = [
        {
            "name": "biz_host",
            "baseUrl": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/central%s/" % gc.ENV,
            "method": "POST",
            "contentType": "application/json",
            "successCode": 0,
            "sendType": "API"
        },
        {
            "name": "biz_central_host",
            "baseUrl": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/central%s/" % gc.ENV,
            "method": "POST",
            "contentType": "application/json",
            "successCode": 0,
            "sendType": "API"
        },
        {
            "name": "AssetReverseNotifyV2",
            "restUrl": "Gbiz-AssetReverseNotifyV1",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "AssetGrantCancelNotifyMQV2",
            "restUrl": "Gbiz-AssetGrantCancelRoutingV2",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "rbiz_host",
            "baseUrl": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/repay%s/" % gc.ENV,
            "method": "POST",
            "contentType": "application/json",
            "successCode": 0,
            "sendType": "API"
        },
        {
            "name": "AssetWithdrawSuccess",
            "restUrl": "sync/asset-withdraw-success",
            "toSystem": "rbiz",
            "parent": "rbiz_host"
        },
        {
            "name": "topic_host",
            "method": "POST",
            "contentType": "application/json",
            "sendType": "TOPIC"
        },
        {
            "name": "AssetSyncNotify",
            "restUrl": "Gbiz-AssetSyncNotify",
            "toSystem": "MQ",
            "parent": "topic_host"
        },
        {
            "name": "AttachmentSyncNotify",
            "parent": "biz_host",
            "toSystem": "BIZ",
            "restUrl": "attachment-sync"
        },
        {
            "name": "UpdateCardSyncNotify",
            "restUrl": "/card/updateAssetCard",
            "toSystem": "BIZ",
            "parent": "biz_central_host"
        },
        {
            "name": "GrantCapitalAsset",
            "restUrl": "Gbiz-GrantCapitalAsset",
            "parent": "topic_host"
        },
        {
            "name": "AssetWithdrawSuccess",
            "restUrl": "Gbiz-AssetWithdrawSuccess",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "AssetImportSync",
            "restUrl": "Gbiz%s-AssetImport" % gc.ENV,
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "AssetReverseNotify",
            "restUrl": "Gbiz-AssetReverseNotify",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "AssetGrantCancelNotifyMQ",
            "restUrl": "Gbiz-AssetGrantCancel",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "AssetChangeLoanChannelMQ",
            "restUrl": "Gbiz-AssetChangeLoanChannel",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "AssetLoanSuccessMQ",
            "restUrl": "Gbiz-AssetLoanSuccess",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "AssetApplyTrailSuccess",
            "restUrl": "Gbiz-AssetApplyTrailSuccess",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "PostLoanConfirmNotifyMQ",
            "restUrl": "Gbiz-PostLoanConfirmRouting",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "UpdateCardNotify",
            "restUrl": "Gbiz-UpdateCardRequest1",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "PaymentWithdrawSuccess",
            "restUrl": "Gbiz-PaymentWithdrawSuccess",
            "toSystem": "MQ",
            "parent": "topic_host"
        },
        {
            "name": "UserLoanConfirmNotifyMQ",
            "restUrl": "Gbiz-UserLoanConfirmRouting",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "CertificateSuccessNotify",
            "restUrl": "Gbiz-CertificateNotify",
            "toSystem": "MQ",
            "parent": "topic_host"
        },
        {
            "name": "CapitalFailedLoanRecordSync",
            "restUrl": "Gbiz-CapitalFailedLoanRecordSync",
            "parent": "topic_host",
            "toSystem": "MQ"
        },
        {
            "name": "AssetAutoImport",
            "restUrl": "Gbiz%s-AssetAutoImport" % gc.ENV,
            "parent": "topic_host",
            "toSystem": ""
        }
    ]
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz%s_msg_client_config" % gc.ENV, body)


def update_capital_order_period_loan_channel():
    body = {
        "pre_capital": [
            "1",
            "3"
        ],
        "xingrui": [
            "3",
            "6"
        ],
        "duolaidianmiyangnew": [
            "1",
            "3",
            "6"
        ],
        "suijinsuo": [
            "1"
        ],
        "manaowan": [
            "1",
            "3",
            "6"
        ],
        "lianzidai": [
            "1",
            "3",
            "6"
        ],
        "jiazhaoye": [
            "1",
            "3"
        ],
        "qnn": [
            "1",
            "3",
            "6",
            "12"
        ],
        "lianlian": [
            "1",
            "6"
        ],
        "baijin": [
            "1",
            "3",
            "6"
        ],
        "shengcai": [
            "1"
        ],
        "mindai": [
            "1",
            "3",
            "6"
        ],
        "yixin_xintuo": [
            "1",
            "3"
        ],
        "yixin_huimin": [
            "1"
        ],
        "yxxt_single": [
            "1",
            "3"
        ],
        "tongrongmiyang": [
            "1",
            "3",
            "6"
        ],
        "duolaidianmiyang": [
            "1",
            "3"
        ],
        "erongsuo": [
            "1",
            "3"
        ],
        "xingchenzx": [
            "3",
            "6"
        ],
        "maizi": [
            "3"
        ],
        "xingchen": [
            "3",
            "6"
        ],
        "xingruinew": [
            "6"
        ],
        "yunxin_quanhu": [
            "3",
            "6"
        ],
        "zhenjinfu": [
            "3"
        ],
        "longshangmiyang": [
            "6"
        ],
        "shoujin": [
            "6"
        ],
        "huabeixiaodai_zhitou": [
            "6"
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "capital_order_period_loan_channel", body)


def update_loan_condition_channels():
    body = [
        {
            "value": "xingchen",
            "text": "星辰(新系统)"
        },
        {
            "value": "xingrui",
            "text": "兴睿"
        },
        {
            "value": "xingruinew",
            "text": "兴睿新"
        },
        {
            "value": "duolaidianmiyangnew",
            "text": "多来点觅飏济宁"
        },
        {
            "value": "qnn",
            "text": "钱牛牛(懒猫)"
        },
        {
            "value": "lianlian",
            "text": "联连"
        },
        {
            "value": "baijin",
            "text": "白金钱包(存管)"
        },
        {
            "value": "mindai",
            "text": "民贷天下"
        },
        {
            "value": "tongrongmiyang",
            "text": "通融觅飏"
        },
        {
            "value": "xingchenzx",
            "text": "星辰征信(老系统)"
        },
        {
            "value": "yunxin_quanhu",
            "text": "云信全互"
        },
        {
            "value": "zhenjinfu",
            "text": "真金服"
        },
        {
            "value": "longshangmiyang",
            "text": "龙商觅飏"
        },
        {
            "value": "shoujin",
            "text": "首金"
        },
        {
            "value": "huabeixiaodai_zhitou",
            "text": "华北小贷直投"
        }
    ]
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "loan-condition-channels", body)


def update_loan_condition_channels_from_system():
    body = {
        "cash": [
            {
                "value": "kaola",
                "text": "考拉理财"
            }
        ],
        "dsq": [
            {
                "value": "qnn",
                "text": "钱牛牛(懒猫)"
            },
            {
                "value": "lianlian",
                "text": "联连"
            },
            {
                "value": "baijin",
                "text": "白金钱包(存管)"
            },
            {
                "value": "mindai",
                "text": "民贷天下"
            },
            {
                "value": "tongrongmiyang",
                "text": "通融觅飏"
            },
            {
                "value": "xingchenzx",
                "text": "星辰征信(老系统)"
            },
            {
                "value": "duolaidianmiyangnew",
                "text": "多来点觅飏济宁"
            },
            {
                "value": "xingrui",
                "text": "兴睿"
            },
            {
                "value": "xingruinew",
                "text": "兴睿新"
            },
            {
                "value": "xingchen",
                "text": "星辰(新系统)"
            },
            {
                "value": "yunxin_quanhu",
                "text": "云信全互"
            },
            {
                "value": "zhenjinfu",
                "text": "真金服"
            },
            {
                "value": "longshangmiyang",
                "text": "龙商觅飏"
            },
            {
                "value": "shoujin",
                "text": "首金"
            },
            {
                "value": "huabeixiaodai_zhitou",
                "text": "华北小贷直投"
            }
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "loan-condition-channels-from-system", body)


def update_gbiz_silence_channel_list(channel_list=None):
    if channel_list:
        body = channel_list
    else:
        body = ["tongrongmiyang", ]
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_silence_channel_list", body)


def update_grouter_channel_route_config(**kwargs):
    ''''
    specified_channel_list 这个里面的配置的资金方是可以命中这个资金方
    但是别的用户也能命中这个资金方
    手机号和身份证号只要二者中有一个与用户匹配就可以，也可以两个都配置
    '''
    content = {
        "allowed_channel_list": [],
        "can_not_retry_messages": [
            "资金路由系统校验失败.*"
        ],
        "specified_channel_list": [
            {
                "loan_channel": "xxxx",
                "mobiles": [
                    "手机号密文"
                ],
                "idnums": [
                    "身份证密文"
                ]
            }
        ]
    }
    for channel in gbiz_common_config.capital_plan.keys():
        if channel in kwargs.keys():
            item = {
                "loan_channel": channel,
                "mobiles": [kwargs[channel]]
            }
        else:
            item = {
                "loan_channel": channel
            }
        content["allowed_channel_list"].append(item)
    return gc.NACOS.update_configs("grouter%s" % gc.ENV, "grouter_channel_route_config", content)


def update_gbiz_base_config():
    body = {
        "max_debt_count": {
            "kn": 3,
            "paysvr": 3
        },
        "from_app_white_list": {
            "banana": [
                "香蕉"
            ],
            "strawberry": [
                "重庆草莓",
                "草莓",
                "杭州草莓"
            ],
            "pitaya": [
                "火龙果"
            ]
        },
        "source_type": {
            "apr_list": [
                "real24",
                "real27",
                "real36",
                "apr36",
                "rongdan",
                "apr36_huaya"
            ],
            "irr_map": {
                "loan": [
                    "irr36",
                    "irr36_quanyi",
                    "irr36_rongshu",
                    "irr36_lexin"
                ],
                "noloan_rongdan": [
                    "rongdan_irr"
                ],
                "noloan_quanyi": [
                    "lieyin"
                ]
            }
        },
        "BCAssetImport": {
            "noloan_validator": [
                {
                    "condition": "#noloan.periodType=='month' && string.startsWith(#loan.refOrderType,'irr36')",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.irr(#loan,'36')-500&&#loan.totalAmount+#noloan.totalAmount<=cmdb.irr(#loan,'36')",
                    "err_msg": "IRR36融担小单，综合成本超出【irr36-500分,irr36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan'&&(#loan.loanChannel!='siping_jiliang'&&#loan.loanChannel!='mozhi_jinmeixin'&&#loan.loanChannel!='yilian_dingfeng'&&#loan.loanChannel!='jinmeixin_daqin'&&#loan.loanChannel!='lanzhou_haoyue_qinjia'&&#loan.loanChannel!='zhongyuan_zunhao'&&#loan.loanChannel!='jinmeixin_hanchen')",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.apr(#loan,'35')&&#loan.totalAmount+#noloan.totalAmount<=cmdb.apr(#loan,'36')",
                    "err_msg": "APR融担小单，综合成本超出【apr35,apr36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan'&&#loan.loanChannel=='siping_jiliang'",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.aprByDay(#loan,'34','365per_year','D$24','D$24')&&#loan.totalAmount+#noloan.totalAmount<=cmdb.aprByDay(#loan,'36','365per_year','D$24','D$24')",
                    "err_msg": "四平吉良APR融担小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan'&&#loan.loanChannel=='mozhi_jinmeixin'",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.aprByDay(#loan,'34','365per_year','D-1','D-1')&&#loan.totalAmount+#noloan.totalAmount<=cmdb.aprByDay(#loan,'36','365per_year','D-1','D-1')",
                    "err_msg": "墨智金美信APR融担小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan'&&#loan.loanChannel=='yilian_dingfeng'",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.aprByDay(#loan,'34','365per_year','D$28','D$28')&&#loan.totalAmount+#noloan.totalAmount<=cmdb.aprByDay(#loan,'36','365per_year','D$28','D$28')",
                    "err_msg": "亿联鼎丰APR融担小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan'&&#loan.loanChannel=='jinmeixin_daqin'",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.aprByDay(#loan,'34','365per_year','D$29D>1','D$29D>1')&&#loan.totalAmount+#noloan.totalAmount<=cmdb.aprByDay(#loan,'36','365per_year','D$29D>1','D$29D>1')",
                    "err_msg": "金美信大秦APR融担小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan'&&#loan.loanChannel=='jincheng_hanchen'",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.aprByDay(#loan,'34','360per_year','D$28','D$28')&&#loan.totalAmount+#noloan.totalAmount<=cmdb.aprByDay(#loan,'36','360per_year','D$28','D$28')",
                    "err_msg": "金美信大秦APR融担小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan_irr'",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.irr(#loan,'36')-100&&#loan.totalAmount+#noloan.totalAmount<=cmdb.irr(#loan,'36')",
                    "err_msg": "IRR融担小单，综合成本超出【irr36-100分,irr36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='lieyin'&&(#loan.loanChannel!='siping_jiliang'&&#loan.loanChannel!='mozhi_jinmeixin')",
                    "rule": "(#noloan.totalAmount+cmdb.irr(#loan,'36'))>=cmdb.apr(#loan,'35')&&(#noloan.totalAmount+cmdb.irr(#loan,'36')<=cmdb.apr(#loan,'36'))",
                    "err_msg": "IRR权益小单，综合成本超出【apr35,apr36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='lieyin'&&#loan.loanChannel=='siping_jiliang'",
                    "rule": "(#noloan.totalAmount+#loan.totalAmount)>=cmdb.aprByDay(#loan,'34','365per_year','D$24','D$24')&&(#noloan.totalAmount+#loan.totalAmount)<=cmdb.aprByDay(#loan,'36','365per_year','D$24','D$24')",
                    "err_msg": "四平吉良IRR权益小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='lieyin'&&#loan.loanChannel=='mozhi_jinmeixin'",
                    "rule": "(#noloan.totalAmount+#loan.totalAmount)>=cmdb.aprByDay(#loan,'34','365per_year','D-1','D-1')&&(#noloan.totalAmount+#loan.totalAmount)<=cmdb.aprByDay(#loan,'36','365per_year','D-1','D-1')",
                    "err_msg": "墨智金美信IRR权益小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan'&&#loan.loanChannel=='lanzhou_haoyue_qinjia'",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.aprByDay(#loan,'34','360per_year','D$28','D$28')&&#loan.totalAmount+#noloan.totalAmount<=cmdb.aprByDay(#loan,'36','360per_year','D$28','D$28')",
                    "err_msg": "兰州昊悦（亲家）APR融担小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan'&&#loan.loanChannel=='zhongyuan_zunhao'",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.aprByDay(#loan,'34','365per_year','D+0','D+0')&&#loan.totalAmount+#noloan.totalAmount<=cmdb.aprByDay(#loan,'36','365per_year','D+0','D+0')",
                    "err_msg": "中原樽昊APR融担小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                },
                {
                    "condition": "#noloan.periodType=='month'&&#noloan.refOrderType=='rongdan'&&#loan.loanChannel=='jinmeixin_hanchen'",
                    "rule": "#loan.totalAmount+#noloan.totalAmount>=cmdb.aprByDay(#loan,'34','365per_year','D$29D>1','D$29D>1')&&#loan.totalAmount+#noloan.totalAmount<=cmdb.aprByDay(#loan,'36','365per_year','D$29D>1','D$29D>1')",
                    "err_msg": "金美信汉辰APR融担小单，综合成本超出【aprByDay34,aprByDay36】范围，请关注！"
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_base_config", body)


def update_capital_allow_period_loan_channel():
    body = {
        "qnn": [
            {
                "sub_type": "multiple",
                "period_count": "1",
                "period_type": "day",
                "period_days": "30"
            },
            {
                "sub_type": "multiple",
                "period_count": "3",
                "period_type": "month",
                "period_days": "0"
            },
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            },
            {
                "sub_type": "multiple",
                "period_count": "12",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "lianlian": [
            {
                "sub_type": "multiple",
                "period_count": "1",
                "period_type": "day",
                "period_days": "30"
            },
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "baijin": [
            {
                "sub_type": "multiple",
                "period_count": "1",
                "period_type": "day",
                "period_days": "30"
            },
            {
                "sub_type": "multiple",
                "period_count": "3",
                "period_type": "month",
                "period_days": "0"
            },
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "mindai": [
            {
                "sub_type": "multiple",
                "period_count": "1",
                "period_type": "day",
                "period_days": "30"
            },
            {
                "sub_type": "multiple",
                "period_count": "3",
                "period_type": "month",
                "period_days": "0"
            },
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "tongrongmiyang": [
            {
                "sub_type": "multiple",
                "period_count": "1",
                "period_type": "day",
                "period_days": "30"
            },
            {
                "sub_type": "multiple",
                "period_count": "3",
                "period_type": "month",
                "period_days": "0"
            },
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "xingchenzx": [
            {
                "sub_type": "multiple",
                "period_count": "3",
                "period_type": "month",
                "period_days": "0"
            },
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "xingruinew": [
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "xingrui": [
            {
                "sub_type": "multiple",
                "period_count": "3",
                "period_type": "month",
                "period_days": "0"
            },
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "xingchen": [
            {
                "sub_type": "multiple",
                "period_count": "3",
                "period_type": "month",
                "period_days": "0"
            },
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "yunxin_quanhu": [
            {
                "sub_type": "multiple",
                "period_count": "3",
                "period_type": "month",
                "period_days": "0"
            },
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "zhenjinfu": [
            {
                "sub_type": "multiple",
                "period_count": "3",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "longshangmiyang": [
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "shoujin": [
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ],
        "huabeixiaodai_zhitou": [
            {
                "sub_type": "multiple",
                "period_count": "6",
                "period_type": "month",
                "period_days": "0"
            }
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "capital_allow_period_loan_channel", body)


def update_gbiz_payment_config(mock_url=''):
    if mock_url:
        base_url = mock_url
    else:
        base_url = "http://biz-payment-staging.k8s-ingress-nginx.kuainiujinke.com"
    body = {
        "paysvr_system": {
            "my": {
                "system_type": "paySvr",
                "url": base_url,
                "callback_url": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/grant1/payment/callback",
                "sign": {
                    "name": "gbiz",
                    "merchant_id": 32,
                    "merchant_md5": "4ea12f8a107c6f540f065fbc21429b4a"
                }
            },
            "tq": {
                "system_type": "paySvr",
                "url": base_url,
                "callback_url": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/grant1/payment/callback",
                "sign": {
                    "name": "gbiz",
                    "merchant_id": 32,
                    "merchant_md5": "4ea12f8a107c6f540f065fbc21429b4a"
                }
            },
            "paysvr_qianjingjing": {
                "system_type": "paySvr",
                "url": base_url,
                "callback_url": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/grant1/payment/callback",
                "sign": {
                    "name": "gbiz",
                    "merchant_id": 32,
                    "merchant_md5": "4ea12f8a107c6f540f065fbc21429b4a"
                }
            },
            "deposit_qianjingjing": {
                "system_type": "depository",
                "url": base_url,
                "callback_url": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/grant1/payment/callback",
                "sign": {
                    "name": "gbiz",
                    "merchant_id": 32,
                    "merchant_md5": "4ea12f8a107c6f540f065fbc21429b4a"
                }
            }
        },
        "paysvr_subject": {
            "yfqjj_withdraw": {
                "name": "yf",
                "paysvr_system": "tq",
                "account": "qsq_sumpay_yf_protocol",
                "warn_amount": "5000000"
            },
            "yfqjj_transfer": {
                "name": "qjj",
                "paysvr_system": "tq",
                "account": "qsq_sumpay_qjj_protocol",
                "warn_amount": "10000000"
            },
            "tongrong_withdraw": {
                "name": "tr",
                "account": "qsq_cpcn_tr_quick",
                "paysvr_system": "my",
                "warn_amount": "5000000",
                "skip_balance_query": False
            },
            "tongrong_transfer": {
                "name": "my",
                "account": "qsq_allinpay_my_protocol",
                "paysvr_system": "my",
                "warn_amount": "5000000",
                "skip_balance_query": False
            },
            "longshang_withdraw": {
                "name": "ls",
                "account": "qsq_cpcn_ls_quick",
                "paysvr_system": "tq",
                "warn_amount": "5000000",
                "skip_balance_query": False
            },
            "longshang_transfer": {
                "name": "ls",
                "account": "qsq_cpcn_ls_quick",
                "paysvr_system": "tq",
                "warn_amount": "5000000",
                "skip_balance_query": False
            },
            "trqjj_withdraw": {
                "name": "tra",
                "account": "qsq_cpcn_tra_quick",
                "paysvr_system": "paysvr_qianjingjing",
                "warn_amount": "5000000",
                "skip_balance_query": False
            },
            "trqjj_transfer": {
                "name": "qjja",
                "account": "qsq_cpcn_qjja_quick",
                "paysvr_system": "paysvr_qianjingjing",
                "warn_amount": "5000000",
                "skip_balance_query": False
            },
            "hhqjj_withdraw": {
                "name": "tq",
                "paysvr_system": "tq",
                "account": "qsq_sumpay_tq_protocol",
                "warn_amount": "5000000"
            },
            "hhqjj_transfer": {
                "name": "qjj",
                "paysvr_system": "tq",
                "account": "qsq_sumpay_qjj_protocol",
                "warn_amount": "5000000"
            },
            "trbn_withdraw": {
                "name": "tq",
                "paysvr_system": "tq",
                "account": "qsq_sumpay_tq_protocol",
                "warn_amount": "5000000"
            },
            "tq": {
                "name": "tq",
                "paysvr_system": "tq"
            },
            "tqa": {
                "name": "tqa",
                "paysvr_system": "tq"
            },
            "tqb": {
                "name": "tqb",
                "paysvr_system": "tq"
            },
            "hq": {
                "name": "hq",
                "paysvr_system": "tq"
            },
            "hm": {
                "name": "hm",
                "paysvr_system": "tq"
            },
            "my": {
                "name": "my",
                "paysvr_system": "my"
            },
            "qianjingjing": {
                "name": "qjj",
                "paysvr_system": "paysvr_qianjingjing"
            },
            "ds": {
                "name": "ds",
                "paysvr_system": "tq"
            },
            "lj": {
                "name": "lj",
                "paysvr_system": "tq"
            },
            "dingfeng": {
                "name": "dingfeng",
                "paysvr_system": "tq"
            },
            "qjhy": {
                "name": "qjhy",
                "paysvr_system": "tq"
            },
            "hy": {
                "name": "hy",
                "paysvr_system": "tq"
            },
            "lhzb": {
                "name": "lhzb",
                "paysvr_system": "tq"
            }
        },
        "paysvr_bind_card": {
            "blacklist_code_msg": {
                "DK0000019": [
                    "超过同一用户绑定卡数"
                ]
            },
            "blacklist_expired_days": 90
        },
        "task_config": {
            "PaymentWithdrawQuery": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0-E20017",
                                "messages": [
                                    "交易处理中"
                                ]
                            },
                            {
                                "code": "0-E20000",
                                "messages": [
                                    "交易成功",
                                    "自动化测试成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "2-E99997",
                                "messages": [
                                    "操作处理中"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retryPayment",
                            "max_times": 2,
                            "max_elapsed_hours": 24,
                            "next_run_at": "delayMinutesWithExGrowth(30, #currentOptSeq, 100, 60*24)"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "操作失败xxxxxx"
                                ]
                            },
                            {
                                "code": "1-E20004",
                                "messages": [
                                    "余额不足"
                                ]
                            },
                            {
                                "code": "1-E20164",
                                "messages": [
                                    "订单号不存在"
                                ]
                            },
                            {
                                "code": "1-E20013",
                                "messages": [
                                    "交易失败, 请稍后重试"
                                ]
                            },
                            {
                                "code": "1-FAILED",
                                "messages": [
                                    "放款失败"
                                ]
                            },
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1-E20107",
                                "messages": [
                                    "无效卡号，请核对后重新输入"
                                ]
                            },
                            {
                                "code": "1-E20129",
                                "messages": [
                                    "您输入的卡号已注销，详询发卡行"
                                ]
                            },
                            {
                                "code": "1-E20005",
                                "messages": [
                                    "超出支付限额,请联系发卡行"
                                ]
                            },
                            {
                                "code": "1-KN_INVALID_ACCOUNT",
                                "messages": [
                                    "无效账户"
                                ]
                            },
                            {
                                "code": "1-E20012",
                                "messages": [
                                    "该卡暂无法支付，请换卡，或联系银行"
                                ]
                            },
                            {
                                "code": "1-E20135",
                                "messages": [
                                    "持卡人账户状态为已锁定，请联系签约行"
                                ]
                            },
                            {
                                "code": "1-E20141",
                                "messages": [
                                    "银行交易失败，请联系发卡行，或稍后重试"
                                ]
                            },
                            {
                                "code": "1-E20144",
                                "messages": [
                                    "银行卡状态异常，请换卡或联系发卡行"
                                ]
                            },
                            {
                                "code": "1-E20195",
                                "messages": [
                                    "持卡人身份证或手机号输入不正确"
                                ]
                            },
                            {
                                "code": "1-E20106",
                                "messages": [
                                    "银行预留手机号有误"
                                ]
                            },
                            {
                                "code": "1-E20104",
                                "messages": [
                                    "持卡人姓名有误"
                                ]
                            },
                            {
                                "code": "1-E20008",
                                "messages": [
                                    "持卡人信息有误，请检查后重新输入"
                                ]
                            },
                            {
                                "code": "1-E20108",
                                "messages": [
                                    "您输入的卡号已挂失，详询发卡行"
                                ]
                            },
                            {
                                "code": "1-E20145",
                                "messages": [
                                    "交易失败，单笔交易金额超限"
                                ]
                            },
                            {
                                "code": "1-E20009",
                                "messages": [
                                    "持卡人身份证已过期"
                                ]
                            },
                            {
                                "code": "1-KN_RISK_CONTROL",
                                "messages": [
                                    "处理成功",
                                    ""
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "terminated"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "风控拦截，疑似重复代付"
                                ]
                            },
                            {
                                "code": "1-E20167",
                                "messages": [
                                    "风控拦截，疑似重复代付"
                                ]
                            }
                        ]
                    }
                ]
            },
            "PaymentWithdraw": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "2",
                                "messages": [
                                    "订单交易正在处理中！",
                                    "订单.*交易正在处理中！"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1000",
                                "messages": [
                                    ".*可用余额.*已小于预警值.*",
                                    ".*可用金额.*小于本次代付金额.*"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1000",
                                "messages": [
                                    ".*代付账户余额为0.*"
                                ]
                            },
                            {
                                "code": "2",
                                "messages": [
                                    "脱敏服务异常"
                                ]
                            }
                        ]
                    }
                ]
            },
            "PaymentTransfer": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            },
                            {
                                "code": "2",
                                "messages": [
                                    "订单交易正在处理中！",
                                    "订单.*交易正在处理中！"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry",
                            "circuit_break_name": "#{#taskParams.loanChannel}_balance_not_enough"
                        },
                        "matches": [
                            {
                                "code": "1000",
                                "messages": [
                                    ".*可用余额.*已小于预警值.*"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1000",
                                "messages": [
                                    ".*可用金额.*小于本次代付金额.*",
                                    ".*代付账户余额为0"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2",
                                "messages": [
                                    "脱敏服务异常"
                                ]
                            }
                        ]
                    }
                ]
            },
            "PaymentTransferQuery": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0-E20000",
                                "messages": [
                                    "交易成功",
                                    "自动化测试成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "2-E99997",
                                "messages": [
                                    "操作处理中"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retryPayment",
                            "max_times": 2,
                            "max_elapsed_hours": 24,
                            "next_run_at": "delayMinutesWithExGrowth(30, #currentOptSeq, 100, 60*24)"
                        },
                        "matches": [
                            {
                                "code": "1-FAILED",
                                "messages": [
                                    "放款失败"
                                ]
                            },
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1-KN_RISK_CONTROL",
                                "messages": [
                                    "处理成功",
                                    ""
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "terminated"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "风控拦截，疑似重复代付"
                                ]
                            },
                            {
                                "code": "1-E20167",
                                "messages": [
                                    "风控拦截，疑似重复代付"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }

    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_payment_config", body)


def update_gbiz_capital_longjiang_daqin():
    paydayloan = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "ChangeCapital"
        ],
        "register_config": {
            "is_multi_account_card_allowed": True,
            "account_register_duration": 60,
            "account_recall_register_duration": 240,
            "must_bind_one_groups": [
                "kuainiu"
            ],
            "register_step_list": [
                {
                    "channel": "longjiang_daqin",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",  # 线上配置lj
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "allow_fail": True,
                    "register_status_effect_duration": 0,
                    "need_confirm_result": True,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "二次核验未命中\\[fail\\]或\\[updateCard\\]策略.*"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "-10000",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'24')",
                            "err_msg": "龙江大秦[资产还款总额]不满足 irr24，请关注！"
                        }
                    ]
                }
            },
            "LoanPreApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(20)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": ["mock测试失败"]
                            },
                            {
                                "code": "11"
                            },
                            {
                                "code": "601002"
                            },
                            {
                                "code": "190005"
                            }
                        ]
                    }
                ]
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
                            },
                            {
                                "code": "601002"
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
                            },
                            {
                                "code": "21"
                            },
                            {
                                "code": "601002"
                            },
                            {
                                "code": "190005"
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allowance_check_range": {
                        "min_value": -4,
                        "max_value": 4
                    }
                }

            },
            "OurRepayPlanRefine": {},
            "ContractDown": {
                "init": {
                    "delay_time": "delayTime('5m')"
                }
            },
            "CertificateApply": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    }
                ]
            },
            "CertificateDownload": {
                "init": {
                    "delay_time": "delaySeconds(300)"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_longjiang_daqin", paydayloan)


def incremental_update_config(tenant, data_id, **kwargs):
    tenant = tenant + gc.ENV
    group = "KV"
    gc.NACOS.incremental_update_config(tenant, data_id, group, **kwargs)


def update_grouter_channel_change_config():
    body = {
        "allowed_channel_list": [
            "shilong_siping",
            "weishenma_daxinganling",
            "qinnong",
            "qinnong_jieyi",
            "zhongke_lanzhou",
            "hami_tianshan_tianbang",
            "tongrongqianjingjing",
            "jingque_haikou",
            "haohanqianjingjing",
            "mozhi_beiyin_zhongyi",
            "qinnong_dingfeng",
            "hamitianbang_xinjiang",
            "lanzhou_haoyue",
            "lanzhou_dingsheng_zkbc2",
            "mozhi_jinmeixin",
            "beiyin_tianbang",
            "zhongke_hegang",
            "yilian_dingfeng",
            "jinmeixin_daqin",
            "weipin_zhongwei",
            "jincheng_hanchen",
            "lanzhou_haoyue_qinjia",
            "zhongyuan_zunhao",
            "beiyin_daqin",
            "yixin_hengrun",
            "jinmeixin_hanchen",
            "yixin_rongsheng",
            "jiexin_taikang_xinheyuan",
            "jiexin_taikang",
            "yumin_zhongbao",
            "jinmeixin_hanchen_jf",
            "lanhai_zhongshi_qj",
            "zhenong_rongsheng",
            "lanzhou_haoyue_chongtian",
            "changyin_mingdonghua_rl",
            "zhongbang_zhongji",
            "daxinganling_zhongyi",
            "lanhai_zhilian",
            "zhenxing_zhongzhixin_jx",
            "weipin_zhongzhixin",
            "zhongbang_haoyue_rl"
        ],
        "against_channel_map": {
            "qinnong": [
                "qinnong_jieyi",
                "qinnong_dingfeng"
            ],
            "qinnong_jieyi": [
                "qinnong",
                "qinnong_dingfeng"
            ],
            "qinnong_dingfeng": [
                "qinnong",
                "qinnong_jieyi"
            ],
            "hami_tianshan_tianbang": [
                "hamitianbang_xinjiang"
            ],
            "hamitianbang_xinjiang": [
                "hami_tianshan_tianbang"
            ],
            "tongrongqianjingjing": [
                "haohanqianjingjing"
            ],
            "haohanqianjingjing": [
                "tongrongqianjingjing"
            ],
            "zhongke_lanzhou": [
                "lanzhou_haoyue",
                "lanzhou_dingsheng_zkbc2"
            ],
            "lanzhou_haoyue": [
                "zhongke_lanzhou",
                "lanzhou_dingsheng_zkbc2",
                "lanzhou_haoyue_qinjia",
                "lanzhou_haoyue_chongtian"
            ],
            "lanzhou_haoyue_qinjia": [
                "lanzhou_haoyue",
                "lanzhou_haoyue_chongtian"
            ],
            "lanzhou_dingsheng_zkbc2": [
                "zhongke_lanzhou",
                "lanzhou_haoyue"
            ],
            "mozhi_beiyin_zhongyi": [
                "beiyin_tianbang"
            ],
            "beiyin_tianbang": [
                "mozhi_beiyin_zhongyi"
            ],

            "jiexin_taikang": [
                "jiexin_taikang_xinheyuan"
            ],
            "jiexin_taikang_xinheyuan": [
                "jiexin_taikang"
            ],
            "jinmeixin_hanchen": [
                "jinmeixin_hanchen_jf"
            ],
            "jinmeixin_hanchen_jf": [
                "jinmeixin_hanchen"
            ],
            "lanzhou_haoyue_chongtian": [
                "lanzhou_haoyue",
                "lanzhou_haoyue_qinjia"
            ]
        },
        "forbid_channel_config": {
            "max_elapsed_hours": "36",
            "channels": [
                "tongrongqianjingjing",
                "haohanqianjingjing",
                "qinnong",
                "qinnong_jieyi",
                "qinnong_dingfeng",
                "mozhi_beiyin_zhongyi",
                "zhongke_lanzhou",
                "hami_tianshan_tianbang",
                "hamitianbang_xinjiang",
                "longjiang_daqin",
                "zhongke_lanzhou",
                "lanzhou_dingsheng_zkbc2",
                "mozhi_jinmeixin",
                "beiyin_tianbang",
                "zhongke_hegang",
                "yilian_dingfeng",
                "jinmeixin_daqin",
                "weipin_zhongwei",
                "jincheng_hanchen",
                "lanzhou_haoyue_qinjia",
                "zhongyuan_zunhao",
                "beiyin_daqin",
                "yixin_hengrun",
                "jinmeixin_hanchen",
                "yixin_rongsheng",
                "jiexin_taikang_xinheyuan",
                "jiexin_taikang",
                "yumin_zhongbao",
                "jinmeixin_hanchen_jf",
                "lanhai_zhongshi_qj",
                "zhenong_rongsheng",
                "lanzhou_haoyue_chongtian",
                "changyin_mingdonghua_rl",
                "zhongbang_zhongji",
                "daxinganling_zhongyi",
                "lanhai_zhilian",
                "zhenxing_zhongzhixin_jx",
                "changyin_junxin",
                "weipin_zhongzhixin",
                "zhongbang_haoyue_rl"
            ]
        }
    }
    return gc.NACOS.update_configs("grouter%s" % gc.ENV, "grouter_channel_change_config", body)


def update_gbiz_circuit_break_config():
    body = [
        {
            "name": "AssetVoid_Circuit_Break",
            "data": {
                "errCount": {
                    "type": "spel",
                    "script": "#cache.getFromCache(#breakName)"
                }
            },
            "trigger": {
                "type": "realtime",
                "rule": "#errCount >= 10"
            },
            "actions": [
                {
                    "type": "alert",
                    "interval": 60,
                    "receiver": [
                        "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                    ],
                    "content": "【发生熔断TEST】'切资方,路由系统返回空'资产作废笔数：#{#errCount}，已超过阈值，自动挂起AssetVoid，请关注并处理！"
                },
                {
                    "type": "suspendTask",
                    "rule": "contains(task.type, {'AssetVoid'})"
                }
            ],
            "recovery": {
                "type": "auto"
            }
        },
        {
            "name": "tongrongqianjingjing_balance_not_enough",
            "data": {
                "errCount": {
                    "type": "spel",
                    "script": "#cache.getFromCache(#breakName)"
                }
            },
            "trigger": {
                "type": "realtime",
                "rule": "#errCount >= 20"
            },
            "actions": [
                {
                    "type": "alert",
                    "interval": 60,
                    "receiver": [
                        "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                    ],
                    "content": "【发生熔断TEST】通融余额不足, 错误数：#{#errCount}，已自动挂起代付PaymentWithdraw等任务，请关注并处理！"
                },
                {
                    "type": "suspendTask",
                    "rule": "taskParams.loanChannel == 'tongrongqianjingjing' and contains(task.type, {'PaymentWithdraw', 'PaymentTransfer'})"
                }
            ],
            "recovery": {
                "type": "manual"
            }
        },
        {
            "name": "haohanqianjingjing_balance_not_enough",
            "data": {
                "errCount": {
                    "type": "spel",
                    "script": "#cache.getFromCache(#breakName)"
                }
            },
            "trigger": {
                "type": "realtime",
                "rule": "#errCount >= 2"
            },
            "actions": [
                {
                    "type": "alert",
                    "interval": 60,
                    "receiver": [
                        "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                    ],
                    "content": "【发生熔断TEST】浩瀚余额不足, 错误数：#{#errCount}，已自动挂起代付PaymentWithdraw等任务，请关注并处理！"
                },
                {
                    "type": "suspendTask",
                    "rule": "taskParams.loanChannel == 'haohanqianjingjing' and contains(task.type, {'PaymentWithdraw', 'PaymentTransfer'})"
                }
            ],
            "recovery": {
                "type": "manual"
            }
        },
        {
            "name": "SQL_Circuit_Break_DEMO",
            "data": {
                "errCount": {
                    "type": "sql",
                    "script": "select count(1) as cnt from asset"
                }
            },
            "trigger": {
                "type": "realtime",
                "rule": "#errCount['cnt'] > 1"
            },
            "actions": [
                {
                    "type": "alert",
                    "interval": 60,
                    "receiver": [
                        "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                    ],
                    "content": "【发生熔断TEST】资产笔数：#{#errCount['cnt']}，已超过阈值，自动挂起AssetVoid，请关注并处理！"
                },
                {
                    "type": "suspendTask",
                    "rule": "contains(task.type, {'AssetVoid'})"
                }
            ],
            "recovery": {
                "type": "auto"
            }
        }
    ]
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_circuit_break_config", body)


def update_gbiz_circuit_break_config_v2(cnt=1000):
    body = [{
                "name":"AssetVoid_Circuit_Break",
                "data":[
                    {
                        "name":"errCount",
                        "type":"spel",
                        "script":"#DataContext.cacheReader.get()"
                    }
                ],
                "trigger":{
                    "type":"realtime",
                    "rule":"#DataContext.data.errCount >= 1"
                },
                "actions":[
                    {
                        "type":"AlertAction",
                        "execMode":"ByBreakerFired",
                        "execParams":{
                            "interval":60,
                            "receiver":[
                                "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                            ],
                            "template":"【发生熔断TEST】'切资方,路由系统返回空'资产作废笔数：#{#DataContext.data.errCount}，已超过阈值，自动挂起AssetVoid，请关注并处理！"
                        }
                    },
                    {
                        "type":"SuspendTaskAction",
                        "execMode":"ByAsyncTask",
                        "execParams":{
                            "rule":"{'AssetVoid'}.contains(#DataContext.task.type)"
                        }
                    }
                ],
                "recovery":{
                    "type":"AutoClose"
                }
            },
            {
                "name":"tongrongqianjingjing_balance_not_enough",
                "data":[
                    {
                        "name":"errCount",
                        "type":"spel",
                        "script":"#DataContext.cacheReader.get()"
                    }
                ],
                "trigger":{
                    "type":"realtime",
                    "rule":"#DataContext.data.errCount >= " + str(cnt)
                },
                "actions":[
                    {
                        "type":"AlertAction",
                        "execMode":"ByBreakerFired",
                        "execParams":{
                            "interval":60,
                            "receiver":[
                                "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                            ],
                            "template":"【发生熔断TEST】通融余额不足, 错误数：#{#DataContext.data.errCount}，已自动挂起代付PaymentWithdraw等任务，请关注并处理！"
                        }
                    },
                    {
                        "type":"SuspendTaskAction",
                        "execMode":"ByAsyncTask",
                        "execParams":{
                            "rule":"{'PaymentWithdraw', 'PaymentTransfer','LoanApplyConfirm','LoanApplyNew'}.contains(#DataContext.task.type) and #DataContext.requestData.loanChannel == 'tongrongqianjingjing'"
                        }
                    }
                ],
                "recovery":{
                    "type":"manual"
                }
            },
            {
                "name":"haohanqianjingjing_balance_not_enough",
                "data":[
                    {
                        "name":"errCount",
                        "type":"spel",
                        "script":"#DataContext.cacheReader.get()"
                    }
                ],
                "trigger":{
                    "type":"realtime",
                    "rule":"#DataContext.data.errCount >= "+ str(cnt)
                },
                "actions":[
                    {
                        "type":"AlertAction",
                        "execMode":"ByBreakerFired",
                        "execParams":{
                            "interval":60,
                            "receiver":[
                                "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                            ],
                            "template":"【发生熔断TEST】浩瀚余额不足, 错误数：#{#DataContext.data.errCount}，已自动挂起代付PaymentWithdraw等任务，请关注并处理！"
                        }
                    },
                    {
                        "type":"SuspendTaskAction",
                        "execMode":"ByAsyncTask",
                        "execParams":{
                            "rule":"{'PaymentWithdraw', 'PaymentTransfer','LoanApplyConfirm','LoanApplyNew'}.contains(#DataContext.task.type) and #DataContext.requestData.loanChannel == 'haohanqianjingjing'"
                        }
                    }
                ],
                "recovery":{
                    "type":"manual"
                }
            },
            {
                "name":"SQL_Circuit_Break_DEMO",
                "data":[
                    {
                        "name":"errCount",
                        "type":"sql",
                        "script":"select count(1) as cnt from asset"
                    }
                ],
                "trigger":{
                    "type":"realtime",
                    "rule":"#DataContext.data.errCount.cnt > 2"
                },
                "actions":[
                    {
                        "type":"AlertAction",
                        "execMode":"ByBreakerFired",
                        "execParams":{
                            "interval":60,
                            "receiver":[
                                "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                            ],
                            "template":"【发生熔断TEST】资产笔数：#{#DataContext.data.errCount.cnt}，已超过阈值，自动挂起AssetVoid，请关注并处理！"
                        }
                    },
                    {
                        "type":"SuspendTaskAction",
                        "execMode":"ByAsyncTask",
                        "execParams":{
                            "rule":"{'AssetVoid'}.contains(#DataContext.task.type)"
                        }
                    }
                ],
                "recovery":{
                    "type":"auto"
                }
            }
        ]
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_circuit_break_config_v2", body)


def update_gbiz_manual_task_auto_process_config():
    content = {
        "ChangeCapital": {
            "changyin_junxin": [
                {
                    "action": {
                        "policy": "autoCancel",
                        "ignoreNotify": "true"
                    },
                    "matches": [
                        {
                            "code": "2",
                            "messages": [
                                "0001_mock测试授信申请失败"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRun",
                        "ignoreNotify": True
                    },
                    "matches": [
                        {
                            "code": "2",
                            "messages": [
                                "0000_交易成功！_合同编号为空_02_null_您的综合评分未达到我司标准"
                            ]
                        }
                    ]
                },
                {
                    "code": "4",
                    "messages": [
                        ".*校验资金量失败.*"
                    ]
                },
                {
                    "code": "10000",
                    "messages": [
                        "AssetVoid回滚到ChangeCapital自动执行"
                    ]
                }
            ],
            "zhongke_lanzhou": [
                {
                    "action": {
                        "policy": "autoRun",
                        "circuit_break_name": "zhongke_lanzhou_circuit_break_01"
                    },
                    "matches": [
                        {
                            "code": "4",
                            "messages": [
                                ".*校验资金量失败.*",
                                "路由系统未返回具体不满足资方进件的原因，进件前切资方数据",
                                ".*资方校验失败: 校验资方允许进件时间.*",
                                ".*资方校验失败: 校验用户账户状态必须为成功:.*",
                                ".*资方校验失败: 校验资方不支持的银行;",
                                "进件,路由系统返回空"
                            ]
                        },
                        {
                            "code": "1",
                            "messages": [
                                "开户超时",
                                "用户开户失败"
                            ]
                        },
                        {
                            "code": "3999903",
                            "messages": [
                                "贷款支用查询-风控规则拒绝"
                            ]
                        },
                        {
                            "code": "3999905",
                            "messages": [
                                "贷款支用查询-放款失败-异常",
                                "贷款支用查询-放款失败-贷款起始日期不为.*",
                                "贷款支用查询-放款失败-贷款支用起始日期不为.*",
                                "贷款支用查询-放款失败-客户申请总额度超过单人限额",
                                "贷款支用查询-放款失败-网贷平台客户在贷余额已超过客户限额",
                                "贷款支用查询-放款失败-报文校验不通过.*",
                                "贷款支用查询-放款失败-当前时间不在区间\\(00:00 - 19:00\\)内，不允许放款！",
                                "贷款支用查询-放款失败-管理器执行SQL出错.*",
                                "贷款支用查询-放款失败-该客户申请总额度已超过单人限额"
                            ]
                        },
                        {
                            "code": "3999909",
                            "messages": [
                                "贷款支用查询-II、III类账户超过日限额",
                                "贷款支用查询-II,III类账户超过日限额",
                                "贷款支用查询-II、III类账户超过年度限额",
                                "贷款支用查询-超过业务限额",
                                "贷款支用查询-收款人账号异常",
                                "贷款支用查询-账户状态异常",
                                "贷款支用查询-收款方客户在我行预留身份证件已过期，需更新身份资料后办理业务",
                                "贷款支用查询-账户状态为挂失",
                                "贷款支用查询-账户处理异常",
                                "贷款支用查询-账户状态为已冻结",
                                "贷款支用查询-日间撤销",
                                "贷款支用查询-放款失败，手工处理",
                                "贷款支用查询-卡性质限制"
                            ]
                        },
                        {
                            "code": "2900002",
                            "messages": [
                                "人脸识别-处理失败",
                                "人脸识别-人脸识别失败",
                                "人脸识别-人脸信息有误！",
                                "人脸识别-用户认证不通过，相似度.*",
                                "人脸识别-身份证联网核查不通过！",
                                "人脸识别-交易高峰期，请稍后进行该交易"
                            ]
                        },
                        {
                            "code": "10000",
                            "messages": [
                                "AssetVoid回滚到ChangeCapital自动执行"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToCanLoan",
                        "next_run_at": "delayDays(1,\"04:00:00\")"
                    },
                    "matches": [
                        {
                            "code": "3999990",
                            "messages": [
                                "贷款支用查询-非业务时间段"
                            ]
                        }
                    ]
                }
            ],
            "qinnong": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "4",
                            "messages": [
                                ".*校验资金量失败.*",
                                ".*资方校验失败: 校验资方允许进件时间.*",
                                ".*资方校验失败: 校验资产共债;",
                                "进件,路由系统返回空"
                            ]
                        },
                        {
                            "code": "1",
                            "messages": [
                                "超过放款限额",
                                "该用户已申请其它类型借款.",
                                "存在未处理资产"
                            ]
                        },
                        {
                            "code": "10000006",
                            "messages": [
                                "放款失败",
                                "放款失败:人工冲正"
                            ]
                        },
                        {
                            "code": "10000007",
                            "messages": [
                                "风控订单审核拒绝",
                                "^联网核查拒单.*",
                                "风控拒单, 请求风控失败",
                                "人工核查拒单"
                            ]
                        },
                        {
                            "code": "10000",
                            "messages": [
                                "AssetVoid回滚到ChangeCapital自动执行",
                                "该用户已申请其它类型借款.*",
                                ".*借款人年龄必须在23-50之间.*",
                                "地区信息不完整:.*"
                            ]
                        },
                        {
                            "code": "100001",
                            "messages": [
                                "系统维护中，暂时停止借款"
                            ]
                        }
                    ]
                }
            ],
            "qinnong_jieyi": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "4",
                            "messages": [
                                ".*校验资金量失败.*",
                                ".*资方校验失败: 校验资方允许进件时间.*",
                                ".*资方校验失败: 校验资产共债;",
                                "进件,路由系统返回空"
                            ]
                        },
                        {
                            "code": "1",
                            "messages": [
                                "超过放款限额",
                                "该用户已申请其它类型借款.",
                                "存在未处理资产",
                                "状态异常"
                            ]
                        },
                        {
                            "code": "10000006",
                            "messages": [
                                "放款失败",
                                "放款失败:人工冲正"
                            ]
                        },
                        {
                            "code": "10000007",
                            "messages": [
                                "风控订单审核拒绝",
                                "^联网核查拒单.*",
                                "风控拒单, 请求风控失败",
                                "人工核查拒单",
                                "联网核查拒单: 公民身份号码与姓名一致，但不存在照片"
                            ]
                        },
                        {
                            "code": "10000",
                            "messages": [
                                "AssetVoid回滚到ChangeCapital自动执行",
                                ".*借款人年龄必须在23-50之间.*",
                                "该用户已申请其它类型借款.*",
                                ".*借款人年龄必须在23-50之间.*",
                                "地区信息不完整:.*"
                            ]
                        },
                        {
                            "code": "100001",
                            "messages": [
                                "系统维护中，暂时停止借款"
                            ]
                        }
                    ]
                }
            ],
            "weishenma_daxinganling": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "4",
                            "messages": [
                                ".*校验资金量失败.*",
                                "未查询到具体不满足资方进件的原因，进件前切资方数据",
                                "weishenma_daxinganling->资方校验失败: 校验用户账户状态必须为成功: .*",
                                "weishenma_daxinganling->资方校验失败- 校验用户账户状态必须为成功- .*",
                                "资方校验失败- 校验资方允许进件时间",
                                "weishenma_daxinganling->资方校验失败: 校验第一联系人手机号号段:.*",
                                "weishenma_daxinganling->资方校验失败: 校验居住地址市;"
                            ]
                        },
                        {
                            "code": "1043",
                            "messages": [
                                "风控审核未通过"
                            ]
                        },
                        {
                            "code": "1029",
                            "messages": [
                                "保证金金额校验未通过"
                            ]
                        },
                        {
                            "code": "1021",
                            "messages": [
                                "支付失败"
                            ]
                        },
                        {
                            "code": "1022",
                            "messages": [
                                "商户订单号不存在"
                            ]
                        },
                        {
                            "code": "1003",
                            "messages": [
                                "支付明细校验未通过（解析失败或字段缺失）"
                            ]
                        },
                        {
                            "code": "1008",
                            "messages": [
                                "字段规则校验未通过"
                            ]
                        },
                        {
                            "code": "1014",
                            "messages": [
                                "A类黑名单校验未通过"
                            ]
                        },
                        {
                            "code": "1018",
                            "messages": [
                                "资金方匹配失败"
                            ]
                        },
                        {
                            "code": "1030",
                            "messages": [
                                "当日金额上限校验未通过"
                            ]
                        },
                        {
                            "code": "10000",
                            "messages": [
                                "AssetVoid回滚到ChangeCapital自动执行"
                            ]
                        }
                    ]
                }
            ],
            "tongrongqianjingjing": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "1999",
                            "messages": [
                                "00131040收款方账户不支持此业务\\(N5T9705\\)",
                                "00131040账户状态不正常,请检查是否存在冻结或圈存（账户名不符）",
                                "00131040账户状态为未激活或网络支付功能为未激活",
                                "00131040_plat2-collate置失败请求",
                                "00131040_成功\\[00000000000\\]-此卡已挂失，请与发卡方联系\\[609X1000041\\]",
                                "00131040_成功\\[00000000000\\]-持卡人认证失败\\[669X1000005\\]",
                                "00131040_成功\\[00000000000\\]-身份证号或手机号或姓名中有1项或多项不符\\[669X1020305\\]",
                                "00131040贷方卡号状态非正常",
                                "00131040_成功\\[00000000000\\]-超转帐限额\\[789X1020461\\]",
                                "00131040_成功\\[00000000000\\]-输入的账号无效，请确认后输入\\[619X1020914\\]",
                                "00131040_成功\\[00000000000\\]-发卡方无此主账号\\[619X1020114\\]",
                                "00131040账户状态为已注销",
                                "00131040_成功\\[00000000000\\]-交易失败，详情请咨询您的发卡行\\[609X1000001\\]",
                                "00131040账户状态异常",
                                "00131040_成功\\[00000000000\\]-受限制的卡\\[609X1020062\\]",
                                "00131040收款账户被中止服务，交易失败.",
                                "00131093查询不到该卡号的对应银行,请核实或联系运营后重试",
                                "00131040_成功\\[00000000000\\]-发卡方状态不正常，请稍后重试\\[609X1000091\\]",
                                "00131040_成功\\[00000000000\\]-Ⅱ、Ⅲ类户年累计交易金额超限\\[789X1021261\\]",
                                "00131040_成功\\[00000000000\\]-帐户已作废或消户\\[619X1020414\\]",
                                "00131040_成功\\[00000000000\\]-交易金额超限\\[789X1000061\\]",
                                "00131040贷方卡号不存在",
                                "00131040_成功\\[00000000000\\]-无效卡号或无此账号\\[619X1000014\\]",
                                "00131040收款方账户状态为已注销\\(F3C1112\\)",
                                "00131040_成功\\[00000000000\\]-不允许此卡交易\\[639X1020057\\]",
                                ".*最终代付失败.*"
                            ]
                        },
                        {
                            "code": "7999",
                            "messages": [
                                ".*代付最终失败,且已经换卡成功一次，不能再换"
                            ]
                        },
                        {
                            "code": "99999",
                            "messages": [
                                ".*代付最终失败,且已经换卡成功一次，不能再换"
                            ]
                        },
                        {
                            "code": "1",
                            "messages": [
                                ".*超出支付限额,请联系发卡行",
                                ".*持卡人身份证或手机号输入不正确",
                                ".*该卡暂无法支付，请换卡，或联系银行",
                                ".*操作失败",
                                "\\[E20145\\]交易失败，单笔交易金额超限",
                                "\\[E20108\\]您输入的卡号已挂失，详询发卡行"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToCanLoan",
                        "next_run_at": "delayDays(1,\"05:00:00\")"
                    },
                    "matches": [
                        {
                            "code": "4",
                            "messages": [
                                ".*校验资金量失败.*"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToCanLoan",
                        "next_run_at": "delayRandomSeconds(0, 300)"
                    },
                    "matches": [
                        {
                            "code": "-1",
                            "messages": [
                                "2002:接口调用方\\(平台方\\)自身签署失败: errCode = 1,000,001,msg = 内部服务错误",
                                "^2002:PDF文档验签失败：errCode=1,000,002,errMsg=内部服务错误.*",
                                "2002:七牛云上传失败",
                                "1001:系统错误！",
                                "2002:创建账号失败：errCode = 1,000,001,msg = 内部服务错误",
                                "2002:ServiceClient为空，获取\\[5111589919\\]的客户端失败，请重新注册客户端"
                            ]
                        },
                        {
                            "code": "-1",
                            "messages": [
                                ".*账号重庆两江新区通融小额贷款有限公司签署次数不足，请联系重庆两江新区通融小额贷款有限公司充值后再签署.*"
                            ]
                        }
                    ]
                }
            ],
            "hami_tianshan_tianbang": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "4",
                            "messages": [
                                ".*校验资金量失败.*",
                                "资方校验失败: 校验资方允许进件时间"
                            ]
                        },
                        {
                            "code": "10002",
                            "messages": [
                                "运营商三要素不匹配！",
                                "风控拒绝：命中A12.*",
                                "\\[orc识别\\]姓名校验失败",
                                "\\[orc识别\\]身份证号校验失败",
                                "身份证已过有效期",
                                "命中 入网时长准入  规则",
                                "\\[运营商在网时长获取失败\\]",
                                "四要素校验失败",
                                "运营商在网状态非正常！",
                                "命中 法院执行名单准入 失信执行名单准入  规则",
                                "FailedOperation.ImageBlur-照片模糊",
                                "对不起，您没有通过反欺诈校验",
                                "FailedOperation.ImageDecodeFailed-图片解码失败",
                                "人脸核身校验不通过",
                                "FailedOperation.IdCardInfoIllegal-身份证信息不合法（身份证号、姓名字段校验非法等）"
                            ]
                        },
                        {
                            "code": "2",
                            "messages": [
                                "二、三类账户交易金额超限",
                                "账户状态异常，请联系发卡行",
                                "交易失败，请核实信息并联系发卡行确认！"
                            ]
                        }
                    ]
                }
            ],
            "haohanqianjingjing": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "1",
                            "messages": [
                                ".*超出支付限额,请联系发卡行",
                                ".*持卡人身份证或手机号输入不正确",
                                ".*该卡暂无法支付，请换卡，或联系银行",
                                "\\[E20107\\]无效卡号，请核对后重新输入",
                                ".*银行预留手机号有误",
                                "\\[E20108\\]您输入的卡号已挂失，详询发卡行"
                            ]
                        },
                        {
                            "code": "10000",
                            "messages": [
                                "AssetVoid回滚到ChangeCapital自动执行"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToCanLoan",
                        "next_run_at": "delayDays(1,\"05:00:00\")"
                    },
                    "matches": [
                        {
                            "code": "4",
                            "messages": [
                                ".*校验资金量失败.*"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToLoanConfirm"
                    },
                    "matches": [
                        {
                            "code": "1",
                            "messages": [
                                "\\[E99999\\]操作失败"
                            ]
                        }
                    ]
                }
            ],
            "beiyin_tianbang": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "1010005",
                            "messages": [
                                "额度查询:额度状态\\[ACTIVE\\],额度使用状态\\[OTHER_ERR\\],额度使用描述\\[很抱歉，暂时无法提供借款服务。\\]"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToCanLoan",
                    },
                    "matches": [
                        {
                            "code": "1",
                            "messages": [
                                "资方二次校验失败：未命中\\[fail,updateCard\\]策略.*"
                            ]
                        }
                    ]
                }
            ]
        },
        "AssetVoid": {
            "changyin_junxin": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "16",
                            "messages": [
                                "用户取消"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayMinutes(240)"
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                "切资方,路由系统返回空"
                            ]
                        }
                    ]
                }
            ],
            "tongrongqianjingjing": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "10",
                            "messages": [
                                "换卡超时,作废资产"
                            ]
                        },
                        {
                            "code": "10005",
                            "messages": [
                                "换卡超时,作废资产"
                            ]
                        },
                        {
                            "code": "16",
                            "messages": [
                                "用户取消"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayDays(1,\"05:00:00\")"
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                "资方校验失败: 校验资方允许进件时间",
                                ".*校验资金量失败.*"
                            ]
                        }
                    ]
                }
            ],
            "haohanqianjingjing": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "16",
                            "messages": [
                                "用户取消"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayDays(1,\"05:00:00\")"
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                "资方校验失败: 校验资方允许进件时间",
                                ".*校验资金量失败.*"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRun",
                        "circuit_break_name": "AssetVoid_Circuit_Break",
                        "ignoreNotify": False
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                "切资方,路由系统返回空"
                            ]
                        }
                    ]
                }
            ],
            "qinnong": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "16",
                            "messages": [
                                "用户取消"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayDays(1,\"01:00:00\")"
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                ".*校验资金量失败.*",
                                ".*资方校验失败: 校验资方允许进件时间.*"
                            ]
                        }
                    ]
                }
            ],
            "qinnong_jieyi": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "16",
                            "messages": [
                                "用户取消"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayDays(1,\"02:00:00\")"
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                ".*校验资金量失败.*",
                                ".*资方校验失败: 校验资方允许进件时间.*"
                            ]
                        }
                    ]
                }
            ],
            "hami_tianshan_tianbang": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "16",
                            "messages": [
                                "用户取消"
                            ]
                        }
                    ]
                },
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayMinutes(240)"
                    },
                    "matches": [
                        {
                            "code": "22",
                            "messages": [
                                ".*服务调用成功.*",
                                ".*服务调用失败.*"
                            ]
                        },
                        {
                            "code": "12",
                            "messages": [
                                ".*切资方,路由系统返回空.*"
                            ]
                        }
                    ]
                }
            ],
            "hamitianbang_xinjiang": [

                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayMinutes(240)"
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                ".*切资方,路由系统返回空.*"
                            ]
                        }
                    ]
                }
            ],
            "zhongke_lanzhou": [
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayMinutes(240)"
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                ".*切资方,路由系统返回空.*"
                            ]
                        }
                    ]
                }
            ],
            "lanzhou_haoyue": [
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayMinutes(240)"
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                ".*切资方,路由系统返回空.*"
                            ]
                        }
                    ]
                }
            ],
            "jinmeixin_hanchen": [
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayMinutes(240)"
                    },
                    "matches": [
                        {
                            "code": "12",
                            "messages": [
                                "切资方,路由系统返回空"
                            ]
                        }
                    ]
                }
            ]
        },
        "CapitalAssetReverse": {},
        "BlacklistCollect": {
            "hami_tianshan_tianbang": [
                {
                    "action": {
                        "policy": "autoRun"
                    },
                    "matches": [
                        {
                            "code": "10002",
                            "messages": [
                                ".*风控策略拒绝.*",
                                "相浮评审拒绝：命中A12.*"
                            ]
                        }
                    ]
                }
            ],
            "zhongke_hegang": [
                {
                    "action": {
                        "policy": "autoRun",
                        "igNoreNotify": True
                    },
                    "matches": [
                        {
                            "code": "190000",
                            "messages": [
                                "交易处理失败"
                            ]
                        }
                    ]
                }
            ]
        },
        "LoanConfirmQuery": {
            "default": [
                {
                    "action": {
                        "policy": "autoRunAndResetRetrytimes"
                    },
                    "matches": [
                        {
                            "code": "2",
                            "messages": []
                        }
                    ]
                }
            ]
        },
        "PaymentWithdrawQuery": {
            "default": [
                {
                    "action": {
                        "policy": "autoRunAndResetRetrytimes"
                    },
                    "matches": [
                        {
                            "code": "2",
                            "messages": [
                                ".*代付查询为处理中,继续重试查询.*"
                            ]
                        }
                    ]
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_manual_task_auto_process_config", content)


def update_gbiz_capital_noloan():
    content = {
        # "task_config_map": {
        #     "RongDanAllocate": {
        #         "execute": {
        #             "weishenma_daxinganling": [
        #                 {
        #                     "name": "tianbang",
        #                     "percent": 0.5
        #                 },
        #                 {
        #                     "name": "daqin",
        #                     "percent": 0.5
        #                 },
        #                 {
        #                     "name": "runqian",
        #                     "percent": 0
        #                 }
        #             ]
        #         }
        #     }
        # },
        "workflow": {
            "nodes": [
                {
                    "id": "BCAssetImportSync",
                    "type": "BCAssetImportSyncTaskHandler",
                    "events": ["AssetImportReadyEvent"],
                    "activity": {
                        "init": {},
                        "execute": {}
                    }
                },
                {
                    "id": "AssetImport",
                    "type": "AssetImportTaskHandler",
                    "events": [
                        "AssetImportSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto"
                        },
                        "execute": {},
                        "finish": []
                    }
                },
                {
                    "id": "AssetImportVerify",
                    "type": "AssetImportVerifyTaskHandler",
                    "events": [
                        "RongdanAllocateSucceededEvent",
                        "NoLoanAssetImportVerifySucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto"
                        },
                        "execute": {},
                        "finish": []
                    }
                },
                {
                    "id": "RefreshNoLoan",
                    "type": "RefreshNoLoanTaskHandler",
                    "events": [],
                    "activity": {
                        "init": {
                            "executeType": "auto"
                        },
                        "execute": {},
                        "finish": []
                    }
                },
                {
                    "id": "RongDanAllocate",
                    "type": "RongDanAllocateTaskHandler",
                    "events": [
                        "RongdanAllocateSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto"
                        },
                        "execute": {
                            "weishenma_daxinganling": [
                                {
                                    "name": "tianbang",
                                    "percent": 0.5
                                },
                                {
                                    "name": "daqin",
                                    "percent": 0.5
                                },
                                {
                                    "name": "runqian",
                                    "percent": 0
                                }
                            ],
                            "zhongke_hegang": [
                                {
                                    "name": "tianbang",
                                    "percent": 0.5
                                },
                                {
                                    "name": "daqin",
                                    "percent": 0.5
                                }
                            ]
                        },
                        "finish": []
                    }
                }
            ],
            "subscribers": [
                {
                    "listen": {
                        "event": "AssetImportReadyEvent",
                        "matches": []
                    },
                    "nodes": ["AssetImport"]
                },
                {
                    "listen": {
                        "event": "AssetImportSucceededEvent"
                    },
                    "nodes": [
                        "AssetImportVerify"
                    ]
                },
                {
                    "listen": {
                        "event": "RongdanAllocateSucceededEvent"
                    },
                    "nodes": [
                        "RefreshNoLoan"
                    ]
                },
                {
                    "listen": {
                        "event": "NoLoanAssetImportVerifySucceededEvent"
                    },
                    "nodes": [
                        "RongDanAllocate"
                    ]
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_noloan", content)


def update_gbiz_capital_yixin_hengrun(raise_limit_over_time_seconds=7200):
    yixin_hengrun = {
        "manual_reverse_allowed": False,
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "raise_limit_allowed": False,
        "register_config": {
            "account_register_duration": 90,
            "is_strict_seq": False,
            "strictSeq": False,
            "register_step_list": [
                {
                    "is_strict_seq": True,
                    "strictSeq": True,
                    "allow_fail": False,
                    "step_type": "PROTOCOL",
                    "register_status_effect_duration": 1,
                    "channel": "yixin_hengrun",
                    "interaction_type": "SMS",
                    "need_confirm_result": False,
                    "actions": [
                        {
                            "allow_fail": False,
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "allow_fail": False,
                            "type": "CheckSmsVerifyCode"
                        }
                    ],
                    "way": "yixin_hengrun",
                    "allow_retry": True
                }
            ],
            "is_multi_account_card_allowed": True,
            "ref_accounts": None
        },
        "task_config_map": {
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36')",
                            "err_msg": "宜信恒润[资产还款总额]不满足 irr36，请关注！"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "成功-1-null",
                                    "成功--1-当前进件已经申请过，请勿重复申请"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "成功--1-null",
                                    "成功--1-联系人姓名或手机号码填写有误",
                                    "mock失败--1-mock的"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "成功--1-null",
                                    "mock失败-REFUSE-null"
                                ]
                            },
                            {
                                "code": "90000",
                                "messages": [
                                    "进件不存在"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "loanProductChange"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "成功-SIGN_SUCCESS-null"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "成功-APPLYING-null"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "成功-0-发送放款通知成功",
                                    "成功-0-已放款,不能发送放款通知"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "mock 失败-1-mock 失败"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(120)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "mock失败-LEND_FAILED-放款失败"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "成功-LENT-null"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "成功-LENDING-null"
                                ]
                            }
                        ]
                    }
                ]
            },
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "资方二次校验失败：未命中\\[fail,updateCard\\]策略.*"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "100998"
                            }
                        ]
                    }
                ]
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -1,
                        "max_value": 1
                    }
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delayMinutes(60)"
                }
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(90)"
                }
            },
            "AssetConfirmOverTimeCheck": {
                "execute": {
                    "raise_limit_over_time_seconds": raise_limit_over_time_seconds
                },
                "finish": [
                    {
                        "action": {
                            "policy": "timeoutAndFail"
                        },
                        "matches": [
                            {
                                "code": "10005",
                                "messages": [
                                    "确认类型\\[LOAN_PRODUCT_CHANGE\\]已超时"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yixin_hengrun", yixin_hengrun)


def update_gbiz_capital_zhongke_lanzhou_const():
    body = {
        "ftpBaseDir": "/upload",
        "ftpChannelName": "lanzhou",
        "maxRate": 27,
        "capitalChannelCode": {
            "zhongke_lanzhou": "KN-ZKBC",
            "lanzhou_dingsheng_zkbc2": "KN2-ZKBC"
        },
        "productCode": {
            "zhongke_lanzhou": "KN-DEBX-ZKBC",
            "lanzhou_dingsheng_zkbc2": "KN2-DEBX-ZKBC"
        },
        "contractTypes": [
            1,
            2
        ],
        "nonBusinessTimeMsgs": [
            "非业务时间段"
        ],
        "authorization": 30603,
        "confirmApplyAttachmentMap": {
            "30601": "contract",
            "30602": "withhold",
            "30603": "authorization",
            "30604": "cusinfo",
            "30605": "guacon"
        },
        "loanUseMap": {
            "1": "1",
            "2": "6",
            "3": "9",
            "4": "1",
            "5": "4",
            "6": "8",
            "7": "8",
            "8": "2",
            "9": "10"
        },
        "educationMap": {
            "1": "90",
            "2": "90",
            "3": "60",
            "4": "40",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "14",
            "9": "11"
        },
        "jobMap": {
            "1": "5",
            "2": "5",
            "3": "5",
            "4": "4",
            "5": "4",
            "6": "4",
            "7": "4",
            "8": "4",
            "9": "4",
            "10": "1",
            "11": "4",
            "12": "1",
            "13": "4",
            "14": "2",
            "15": "6"
        },
        "dutyMap": {
            "1": "3",
            "2": "1",
            "3": "4",
            "4": "9",
            "5": "4",
            "6": "4"
        },
        "dupCustomerInfoPushConfigList": [
            {
                "code": "1999901"
            }
        ],
        "dupFaceRecognitionConfigList": [
            {
                "code": "2999901"
            }
        ],
        "certificateFileConfig": {
            "attachmentType": 24,
            "ftpChannelName": "kuainiu",
            "baseDir": "/tempfiles/test/upload/11001",
            "prefix": "zkbc_",
            "suffix": "_finish",
            "fileType": "pdf"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_const", body)


def update_gbiz_capital_yixin_hengrun_const():
    body = {
        "loanUseMap": {
            "0": "60",
            "1": "20",
            "2": "60",
            "3": "10",
            "4": "20",
            "5": "40",
            "6": "60",
            "7": "30",
            "8": "50",
            "9": "60"
        },
        "defaultSimilarity": 75,
        "similarityThreshold": 70,
        "fetchPhotoMethod": "ALBUM",
        "idCardExpired": "20991231",
        "defaultLoanUse": "60",
        "defaultEducation": "80",
        "aliveTimes": "1",
        "faceAuthTimes": "1",
        "contractPushMap": {
            "33205": "2",
            "33206": "1"
        },
        "genderMap": {
            "m": "男",
            "f": "女"
        },
        "fileTyeMap": {
            "1": "CARD_FRONT_PHOTO",
            "2": "CARD_BACK_PHOTO",
            "29": "FRONT_PHOTO"
        },
        "contactRelationMap": {
            "0": "3",
            "1": "1",
            "2": "7",
            "3": "4",
            "4": "6",
            "5": "8",
            "6": "5",
            "7": "5"
        },
        "educationMap": {
            "1": "80",
            "2": "70",
            "3": "60",
            "4": "50",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "10",
            "9": "10"
        },
        "defaultFirstRelationship": "7",
        "defaultSecondRelationship": "5",
        "maxAllowSize": 409600,
        "repayPlanDateFormat": "yyyy-MM-dd",
        "contractDownMap": {
            "28": "2",
            "33200": "6",
            "33201": "1006",
            "33202": "1012",
            "33203": "16",
            "33204": "17"
        },
        "ftpChannelName": "kuainiu",
        "baseDir": "/tempfiles/dev/yixin_hengrun",
        "statementFtpChannelName": "kuainiu",
        "statementBaseDir": "/tempfiles/dev/yixin_hengrun"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yixin_hengrun_const", body)


def update_gbiz_capital_hami_tianbang_const():
    body = {
        "ftpChannelName": "tianbang_hami",
        "ftpStatementChannelName": "hami_tianbang_statement",
        "ftpConfig": {
            "username": "ftpuser1",
            "uploadRemotePath": "/pylon/account",
            "uploadLocalPath": "/Users/fenlai/Desktop/upload/test",
            "downloadRemotePath": "/pylon/account",
            "downloadLocalPath": "/Users/fenlai/Desktop/upload/test"
        },
        "tianbangFtpConfig": {
            "username": "kuainiu",
            "uploadRemoteContractPath": "/contract/",
            "uploadRemoteLoanDataPath": "/loandata/"
        },
        "interestRate": "0.1",
        "checkType": "S0004",
        "brNo": "JG00001",
        "chnlNo": "HK00004",
        "loanContract": {
            "type": 1,
            "knType": 30181
        },
        "authContract": {
            "type": 7,
            "knType": 30182
        },
        "guaranteeContract": {
            "type": 6,
            "policyType": 3,
            "knType": 30710
        },
        "certificate": {
            "type": 2,
            "knType": 24
        },
        "bankMap": {
            "hxb": {
                "code": "304100040000",
                "name": "华夏银行股份有限公司总行"
            },
            "bjbank": {
                "code": "313100000013",
                "name": "北京银行"
            },
            "boc": {
                "code": "104100000004",
                "name": "中国银行总行"
            },
            "cmb": {
                "code": "308584000013",
                "name": "招商银行股份有限公司"
            },
            "icbc": {
                "code": "102100099996",
                "name": "中国工商银行"
            },
            "ccb": {
                "code": "105100000017",
                "name": "中国建设银行股份有限公司总行"
            },
            "cib": {
                "code": "309391000011",
                "name": "兴业银行总行"
            },
            "ceb": {
                "code": "303100000006",
                "name": "中国光大银行"
            },
            "abc": {
                "code": "103100000026",
                "name": "中国农业银行股份有限公司"
            },
            "psbc": {
                "code": "403100000004",
                "name": "中国邮政储蓄银行有限责任公司"
            },
            "cmbc": {
                "code": "305100000013",
                "name": "中国民生银行"
            },
            "spdb": {
                "code": "310290000013",
                "name": "上海浦东发展银行"
            },
            "comm": {
                "code": "301290000007",
                "name": "交通银行"
            },
            "pab": {
                "code": "307584007998",
                "name": "平安银行"
            },
            "shbank": {
                "code": "325290000012",
                "name": "上海银行股份有限公司"
            },
            "gdb": {
                "code": "306581000003",
                "name": "广发银行股份有限公司"
            },
            "citic": {
                "code": "302100011000",
                "name": "中信银行股份有限公司"
            }
        },
        "marriageMap": {
            "1": "S",
            "2": "M",
            "3": "D",
            "4": "W"
        },
        "empStatusMap": {
            "1": "Y",
            "2": "Y",
            "3": "Y",
            "4": "N",
            "5": "Y",
            "6": "N"
        },
        "degreeMap": {
            "1": "8",
            "2": "8",
            "3": "8",
            "4": "8",
            "5": "8",
            "6": "8",
            "7": "4",
            "8": "3",
            "9": "2"
        },
        "eduMap": {
            "1": "80",
            "2": "70",
            "3": "60",
            "4": "50",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "10",
            "9": "11"
        },
        "workTypeMap": {
            "1": "4",
            "2": "4",
            "3": "4",
            "4": "4",
            "5": "4",
            "6": "4",
            "7": "4",
            "8": "4",
            "9": "4",
            "10": "4",
            "11": "4",
            "12": "4",
            "13": "4",
            "14": "0",
            "15": "5"
        },
        "relationshipMap": {
            "0": "C",
            "1": "F",
            "2": "B",
            "3": "H",
            "4": "W",
            "5": "T",
            "6": "Y",
            "7": "O"
        },
        "loanUsageMap": {
            "1": "08",
            "2": "02",
            "3": "07",
            "4": "01",
            "5": "03",
            "6": "07",
            "7": "05",
            "8": "00",
            "9": "07"
        },
        "periodTypeMap": {
            "month": "M",
            "day": "D"
        },
        "statusMap": {
            "1": "同意",
            "2": "拒绝"
        },
        "errorCodeMap": {
            "E": "1"
        },
        "productL1": {
            "hami_tianshan_tianbang": "L100003",
            "hamitianbang_xinjiang": "L100003"
        },
        "productL2": {
            "hami_tianshan_tianbang": "1594602016447",
            "hamitianbang_xinjiang": "2594602017386"
        },
        "rtnCodeMap": {
            "SUCCESS": 21,
            "FAIL": 22,
            "test": 23
        },
        "needTransGpsMap": {
            "hmtlf": True
        },
        "gpsInfoMap": {
            "hamitianbang_xinjiang": [
                "89.18529510498048,42.94970410415907,5",
                "93.5130500793457,42.84280733922825,5"
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hami_tianbang_const", body)


def update_gbiz_capital_mozhi_beiyin_const():
    body = {
        "grantNotifyUrl": "",
        "ftpChannelName": {
            "beiyin_tianbang": "beiyin_tianbang",
            "mozhi_beiyin_zhongyi": "mozhi_beiyin"
        },
        "guarantee_contract_map": {
            "beiyin_tianbang": 31400,
            "mozhi_beiyin_zhongyi": 30770
        },
        "threshold": "80",
        "creditLimit": 2000000,
        "creditAmountStatusMap": {
            "ACTIVE": 10,
            "FREEZE": 11,
            "NOTACTIVE": 12,
            "AUDITING": 13,
            "EXPIRED": 14,
            "REFUSE": 15,
            "APPLYING": 16
        },
        "creditAmountErrStatusMap": {
            "APPLYING_ERR": 10000,
            "LENDING_ERR": 10001,
            "OVERDUE_ERR": 10002,
            "LIMIT_ERR": 10003,
            "PAYING_ERR": 10004,
            "OTHER_ERR": 10005
        },
        "noExistErrStatus": "00000",
        "applyResultMap": {
            "PASS": 100,
            "REFUSE": 101,
            "FAIL": 102,
            "AUDITING": 103
        },
        "applyStatusMap": {
            "SUCCESS": 1000,
            "FAIL": 1001,
            "REFUSE": 1002,
            "LENDING": 1003,
            "APPLYING": 1004
        },
        "professionMap": {
            "1": "4",
            "2": "4",
            "3": "4",
            "4": "4",
            "5": "4",
            "6": "4",
            "7": "4",
            "8": "4",
            "9": "4",
            "10": "4",
            "11": "4",
            "12": "4",
            "13": "4",
            "14": "4",
            "15": "4"
        },
        "delPhonePrefixs": [
            "+86",
            "86",
            "12593",
            "17951",
            "17950",
            "17910",
            "17911",
            "10193",
            "17969",
            "17908",
            "17909",
            "96688",
            "11808"
        ],
        "emojiRegex": "(?:[\\uD83C\\uDF00-\\uD83D\\uDDFF]|[\\uD83E\\uDD00-\\uD83E\\uDDFF]|[\\uD83D\\uDE00-\\uD83D\\uDE4F]|[\\uD83D\\uDE80-\\uD83D\\uDEFF]|[\\u2600-\\u26FF]\\uFE0F?|[\\u2700-\\u27BF]\\uFE0F?|\\u24C2\\uFE0F?|[\\uD83C\\uDDE6-\\uD83C\\uDDFF]{1,2}|[\\uD83C\\uDD70\\uD83C\\uDD71\\uD83C\\uDD7E\\uD83C\\uDD7F\\uD83C\\uDD8E\\uD83C\\uDD91-\\uD83C\\uDD9A]\\uFE0F?|[\\u0023\\u002A\\u0030-\\u0039]\\uFE0F?\\u20E3|[\\u2194-\\u2199\\u21A9-\\u21AA]\\uFE0F?|[\\u2B05-\\u2B07\\u2B1B\\u2B1C\\u2B50\\u2B55]\\uFE0F?|[\\u2934\\u2935]\\uFE0F?|[\\u3030\\u303D]\\uFE0F?|[\\u3297\\u3299]\\uFE0F?|[\\uD83C\\uDE01\\uD83C\\uDE02\\uD83C\\uDE1A\\uD83C\\uDE2F\\uD83C\\uDE32-\\uD83C\\uDE3A\\uD83C\\uDE50\\uD83C\\uDE51]\\uFE0F?|[\\u203C\\u2049]\\uFE0F?|[\\u25AA\\u25AB\\u25B6\\u25C0\\u25FB-\\u25FE]\\uFE0F?|[\\u00A9\\u00AE]\\uFE0F?|[\\u2122\\u2139]\\uFE0F?|\\uD83C\\uDC04\\uFE0F?|\\uD83C\\uDCCF\\uFE0F?|[\\u231A\\u231B\\u2328\\u23CF\\u23E9-\\u23F3\\u23F8-\\u23FA]\\uFE0F?)",
        "fileTyeMap": {
            "1": "CARD_FRONT_PHOTO",
            "2": "CARD_BACK_PHOTO",
            "29": "FRONT_PHOTO"
        },
        "loanUseMap": {
            "1": "日常消费",
            "2": "教育",
            "3": "日常消费",
            "4": "日常消费",
            "5": "旅游",
            "6": "日常消费",
            "7": "日常消费",
            "8": "日常消费",
            "9": "日常消费"
        },
        "contactRelationMap": {
            "0": "SPOUSE",
            "1": "PARENT",
            "2": "BROTHER",
            "3": "CHILDREN",
            "4": "WORKMATE",
            "5": "CLASSMATE",
            "6": "FRIEND",
            "7": "OTHER"
        },
        "educationMap": {
            "1": "1",
            "2": "1",
            "3": "1",
            "4": "1",
            "5": "1",
            "6": "2",
            "7": "3",
            "8": "4",
            "9": "4"
        },
        "maritalStatusMap": {
            "1": "SINGLE",
            "2": "MARRIED",
            "3": "DIVORCED",
            "4": "WIDOW"
        },
        "bankCodeMap": {
            "兴业银行": "CIB",
            "广发银行": "GDB",
            "民生银行": "CMBC",
            "浦发银行": "SPDB",
            "平安银行": "PAB",
            "北京银行": "BJBANK",
            "华夏银行": "HXB",
            "中信银行": "CITIC",
            "中国银行": "BOC",
            "建设银行": "CCB",
            "工商银行": "ICBC",
            "农业银行": "ABC",
            "光大银行": "CEB"
        },
        "genderMap": {
            "M": "男",
            "F": "女"
        },
        "contract_mapping_map": {
            "28": {
                "base_path": "/agreement/",
                "suffix": "_loan_agreement.pdf"
            },
            "30775": {
                "base_path": "/agreement/",
                "suffix": "_credit_auth_agreement.pdf"
            },
            "31403": {
                "base_path": "/agreement/",
                "suffix": "_person_info_auth_agreement.pdf"
            },
            "31404": {
                "base_path": "/agreement/",
                "suffix": "_out_person_info_auth_agreement.pdf"
            }
        },
        "applyNotExistInfoList": [
            {
                "code": "90000",
                "messages": [
                    "交易流水不存在",
                    "没有查询到记录",
                    "用户可用授信信息异常",
                    "用户获取授信信息异常2"
                ]
            },
            {
                "code": "11002",
                "messages": [
                    "交易流水不存在",
                    "没有查询到记录",
                    "用户可用授信信息异常",
                    "用户获取授信信息异常2"
                ]
            }
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_mozhi_beiyin_const", body)


def update_gbiz_capital_mozhi_jinmeixin_const():
    body = {
        "ftpChannelName": "mozhi_jinmeixin",
        "grantNotifyUrl": "",
        "threshold": "80",
        "creditLimit": 700000,
        "creditAmountStatusMap": {
            "ACTIVE": 10,
            "FREEZE": 11,
            "NOTACTIVE": 12,
            "AUDITING": 13,
            "EXPIRED": 14,
            "REFUSE": 15,
            "APPLYING": 16
        },
        "creditAmountErrStatusMap": {
            "APPLYING_ERR": 10000,
            "LENDING_ERR": 10001,
            "OVERDUE_ERR": 10002,
            "LIMIT_ERR": 10003,
            "PAYING_ERR": 10004,
            "OTHER_ERR": 10005
        },
        "noExistErrStatus": "00000",
        "applyResultMap": {
            "PASS": 100,
            "REFUSE": 101,
            "FAIL": 102,
            "AUDITING": 103
        },
        "applyStatusMap": {
            "SUCCESS": 1000,
            "FAIL": 1001,
            "REFUSE": 1002,
            "LENDING": 1003,
            "APPLYING": 1004
        },
        "professionMap": {
            "1": "4",
            "2": "4",
            "3": "4",
            "4": "4",
            "5": "4",
            "6": "4",
            "7": "4",
            "8": "4",
            "9": "4",
            "10": "4",
            "11": "4",
            "12": "4",
            "13": "4",
            "14": "4",
            "15": "4"
        },
        "delPhonePrefixs": [
            "+86",
            "86",
            "12593",
            "17951",
            "17950",
            "17910",
            "17911",
            "10193",
            "17969",
            "17908",
            "17909",
            "96688",
            "11808"
        ],
        "emojiRegex": "(?:[\\u0e01-\\u0e5b]|[\\u2022\\u0e31\\u0e47]|[\\u2022\\u0e47\\u0e31]|[\\uD83C\\uDF00-\\uD83D\\uDDFF]|[\\uD83E\\uDD00-\\uD83E\\uDDFF]|[\\uD83D\\uDE00-\\uD83D\\uDE4F]|[\\uD83D\\uDE80-\\uD83D\\uDEFF]|[\\u2600-\\u26FF]\\uFE0F?|[\\u2700-\\u27BF]\\uFE0F?|\\u24C2\\uFE0F?|[\\uD83C\\uDDE6-\\uD83C\\uDDFF]{1,2}|[\\uD83C\\uDD70\\uD83C\\uDD71\\uD83C\\uDD7E\\uD83C\\uDD7F\\uD83C\\uDD8E\\uD83C\\uDD91-\\uD83C\\uDD9A]\\uFE0F?|[\\u0023\\u002A\\u0030-\\u0039]\\uFE0F?\\u20E3|[\\u2194-\\u2199\\u21A9-\\u21AA]\\uFE0F?|[\\u2B05-\\u2B07\\u2B1B\\u2B1C\\u2B50\\u2B55]\\uFE0F?|[\\u2934\\u2935]\\uFE0F?|[\\u3030\\u303D]\\uFE0F?|[\\u3297\\u3299]\\uFE0F?|[\\uD83C\\uDE01\\uD83C\\uDE02\\uD83C\\uDE1A\\uD83C\\uDE2F\\uD83C\\uDE32-\\uD83C\\uDE3A\\uD83C\\uDE50\\uD83C\\uDE51]\\uFE0F?|[\\u203C\\u2049]\\uFE0F?|[\\u25AA\\u25AB\\u25B6\\u25C0\\u25FB-\\u25FE]\\uFE0F?|[\\u00A9\\u00AE]\\uFE0F?|[\\u2122\\u2139]\\uFE0F?|\\uD83C\\uDC04\\uFE0F?|\\uD83C\\uDCCF\\uFE0F?|[\\u231A\\u231B\\u2328\\u23CF\\u23E9-\\u23F3\\u23F8-\\u23FA]\\uFE0F?)",
        "fileTyeMap": {
            "1": "CARD_FRONT_PHOTO",
            "2": "CARD_BACK_PHOTO",
            "29": "FRONT_PHOTO"
        },
        "loanUseMap": {
            "1": "日常消费",
            "2": "教育",
            "3": "日常消费",
            "4": "日常消费",
            "5": "旅游",
            "6": "日常消费",
            "7": "日常消费",
            "8": "日常消费",
            "9": "日常消费"
        },
        "contactRelationMap": {
            "0": "SPOUSE",
            "1": "PARENT",
            "2": "BROTHER",
            "3": "CHILDREN",
            "4": "WORKMATE",
            "5": "CLASSMATE",
            "6": "FRIEND",
            "7": "OTHER"
        },
        "educationMap": {
            "1": "1",
            "2": "1",
            "3": "1",
            "4": "1",
            "5": "1",
            "6": "2",
            "7": "3",
            "8": "4",
            "9": "4"
        },
        "maritalStatusMap": {
            "1": "SINGLE",
            "2": "MARRIED",
            "3": "DIVORCED",
            "4": "WIDOW"
        },
        "bankCodeMap": {
            "兴业银行": "CIB",
            "广发银行": "GDB",
            "民生银行": "CMBC",
            "浦发银行": "SPDB",
            "平安银行": "PAB",
            "北京银行": "BJBANK",
            "华夏银行": "HXB",
            "中信银行": "CITIC",
            "中国银行": "BOC",
            "建设银行": "CCB",
            "工商银行": "ICBC",
            "农业银行": "ABC",
            "光大银行": "CEB"
        },
        "genderMap": {
            "M": "男",
            "F": "女"
        },
        "addressKeyWordMap": {
            "上海上海市": "上海市上海市",
            "北京北京市": "北京市北京市",
            "天津天津市": "天津市天津市",
            "重庆重庆市": "重庆市重庆市"
        },
        "provinceNameMap": {
            "上海": "上海市",
            "北京": "北京市",
            "天津": "天津市",
            "重庆": "重庆市"
        },
        "contract_mapping_map": {
            "28": {
                "base_path": "/agreement/",
                "suffix": "_loan_agreement.pdf"
            }
        },
        "applyNotExistInfoList": [
            {
                "code": "90000",
                "messages": [
                    "交易流水不存在",
                    "没有查询到记录",
                    "用户可用授信信息异常",
                    "用户获取授信信息异常2"
                ]
            },
            {
                "code": "11002",
                "messages": [
                    "交易流水不存在",
                    "没有查询到记录",
                    "用户可用授信信息异常",
                    "用户获取授信信息异常2"
                ]
            }
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_mozhi_jinmeixin_const", body)


def update_gbiz_capital_siping_jiliang_const():
    body = {
        "preApplyAttachmentMap": {
            "1": "1001",
            "2": "1002",
            "29": "1003",
            "31201": "1206"
        },
        "confirmApplyAttachmentMap": {
            "31200": "1101",
            "31202": "1104",
            "31203": "1108",
            "31201": "1107"
        },
        "downloadAttachmentMap": {
            "2": "28"
        },
        "guaranteeType": "31203",
        "genderMap": {
            "M": 10,
            "F": 20
        },
        "marriageMap": {
            "0": "99",
            "1": "10",
            "2": "20",
            "3": "99",
            "4": "40"
        },
        "educationMap": {
            "0": "99",
            "1": "00",
            "2": "10",
            "3": "20",
            "4": "30",
            "5": "40",
            "6": "50",
            "7": "60",
            "8": "70",
            "9": "80",
            "10": "80"
        },
        "careerMap": {
            "0": "3",
            "1": "1",
            "2": "7",
            "3": "2",
            "4": "2",
            "5": "6",
            "6": "6",
            "7": "6",
            "8": "2",
            "9": "2",
            "10": "2",
            "11": "2",
            "12": "2",
            "13": "2",
            "14": "3",
            "15": "5"
        },
        "bankMap": {
            "hxb": "304100040000",
            "bjbank": "313100001104",
            "boc": "104100000004",
            "cmb": "308584001024",
            "citic": "302100011000",
            "icbc": "102100004951",
            "ccb": "105100000017",
            "cib": "309391000011",
            "ceb": "303100000006",
            "abc": "103100000018",
            "psbc": "403100000004",
            "cmbc": "305100000013",
            "spdb": "310290000013",
            "njcb": "313301008887",
            "nbbank": "313332082914"
        },
        "loanUsageMap": {
            "0": "66",
            "1": "66",
            "2": "63",
            "3": "2",
            "4": "6",
            "5": "6",
            "6": "64",
            "7": "4",
            "8": "10"
        },
        "industryMap": {
            "13": "O",
            "11": "I",
            "10": "H",
            "6": "K",
            "5": "F",
            "7": "D",
            "8": "G",
            "4": "Q",
            "3": "P",
            "9": "J",
            "14": "L",
            "12": "R",
            "1": "S"
        },
        "nationCodeMap": {
            "汉": "001",
            "土家": "002",
            "阿昌": "003",
            "白": "004",
            "保安": "005",
            "布朗": "006",
            "布依": "007",
            "朝鲜": "008",
            "达斡尔": "009",
            "傣": "010",
            "德昂": "011",
            "东乡": "012",
            "侗": "013",
            "独龙": "014",
            "鄂伦春": "015",
            "俄罗斯": "016",
            "鄂温克": "017",
            "高山": "018",
            "仡佬": "019",
            "哈尼": "020",
            "哈萨克": "021",
            "赫哲": "022",
            "回": "023",
            "基诺": "024",
            "景颇": "025",
            "京": "026",
            "柯尔克孜": "027",
            "拉祜": "028",
            "珞巴": "029",
            "傈僳": "030",
            "黎": "031",
            "满": "032",
            "毛南": "033",
            "门巴": "034",
            "蒙古": "035",
            "苗": "036",
            "仫佬": "037",
            "纳西": "038",
            "怒": "039",
            "普米": "040",
            "羌": "041",
            "撒拉": "042",
            "畲": "043",
            "水": "044",
            "塔吉克": "045",
            "塔塔尔": "046",
            "土": "047",
            "佤": "048",
            "维吾尔": "049",
            "乌孜别克": "050",
            "锡伯": "051",
            "瑶": "052",
            "彝": "053",
            "裕固": "054",
            "藏": "055",
            "壮": "056"
        },
        "relationMap": {
            "3": "07",
            "4": "01",
            "5": "08",
            "6": "08",
            "7": "08",
            "8": "05",
            "9": "02",
            "0": "99"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_siping_jiliang_const", body)


def update_gbiz_capital_longjiang_daqin_const():
    body = {
        "merchantNo": "MFT202101004",
        "fileMerchantNo": "xkltb",
        "multipleRate": 24,
        "ftpUploadDir": "/",
        "ftpDownloadDir": "/",
        "ftpChannelName": "longjiang_daqin",
        "productCodeMap": {
            "6": "LJB_XKLTB_6",
            "12": "LJB_XKLTB_12"
        },
        "loanUsage": {
            "1": "23",
            "2": "7",
            "3": "2",
            "4": "22",
            "5": "1",
            "6": "25",
            "7": "6",
            "8": "23",
            "9": "27"
        },
        "maritalStatus": {
            "1": "1",
            "2": "2",
            "3": "7",
            "4": "6"
        },
        "relationMap": {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "1",
            "4": "3",
            "5": "3",
            "6": "3",
            "7": "3"
        },
        "contractConfig": {
            "BEFORE_LOAN_APPLY": [
                {
                    "attachmentType": 1,
                    "filePrex": "01",
                    "fileCode": "certFileA",
                    "ext": "jpg",
                    "filePath": "10002",
                    "fileTmpKey": "certFileA",
                    "fileTmpName": "用户身份影像文件 A（身份证照片面）"
                },
                {
                    "attachmentType": 2,
                    "filePrex": "01",
                    "fileCode": "certFileB",
                    "ext": "jpg",
                    "filePath": "10002",
                    "fileTmpKey": "certFileB",
                    "fileTmpName": "用户身份影像文件 B（身份证国徵面）"
                },
                {
                    "attachmentType": 29,
                    "filePrex": "01",
                    "fileCode": "livingRecognition",
                    "ext": "jpg",
                    "filePath": "10002",
                    "fileTmpKey": "livingRecognition",
                    "fileTmpName": "活体识别照片"
                }
            ],
            "BEFORE_GRANT_APPLY": [
                {
                    "attachmentType": 30807,
                    "filePrex": "01",
                    "fileCode": "commitment",
                    "filePath": "10002",
                    "fileTmpKey": "commitment",
                    "fileTmpName": "承诺函"
                },
                {
                    "attachmentType": 30802,
                    "filePrex": "01",
                    "fileCode": "guarantee_letter",
                    "filePath": "10002",
                    "fileTmpKey": "guaranteeLetter",
                    "fileTmpName": "担保函"
                },
                {
                    "attachmentType": 30809,
                    "filePrex": "01",
                    "fileCode": "withhold",
                    "filePath": "10002",
                    "fileTmpKey": "withhold",
                    "fileTmpName": "委托扣款服务三方协议"
                }
            ],
            "GRANT_SUCCESS_DOWNLOAD": [
                {
                    "attachmentType": 30803,
                    "filePrex": "10",
                    "fileCode": "creditAuthorize",
                    "filePath": "10002"
                },
                {
                    "attachmentType": 28,
                    "filePrex": "10",
                    "fileCode": "loanContract",
                    "filePath": "10002"
                },
                {
                    "attachmentType": 30804,
                    "filePrex": "10",
                    "fileCode": "payment_voucher",
                    "filePath": "10002"
                },
                {
                    "attachmentType": 30805,
                    "filePrex": "10",
                    "fileCode": "bank_electronic_loan_IOU",
                    "filePath": "10002"
                },
                {
                    "attachmentType": 30800,
                    "filePrex": "10",
                    "fileCode": "personalInfoAuthorize",
                    "filePath": "10002"
                }
            ],
            "GRANT_SUCCESS_UPLOAD": [
                {
                    "attachmentType": 30801,
                    "filePrex": "01",
                    "fileCode": "securityAgreement",
                    "filePath": "10002",
                    "fileTmpKey": "securityAgreement",
                    "fileTmpName": "委托担保协议文件"
                }
            ],
            "PUSH_REPAY_PLAN": [
                {
                    "filePrex": "01",
                    "fileCode": "assetRepayPlan",
                    "filePath": "10002",
                    "fileTmpKey": "assetRepayPlan",
                    "fileTmpName": "资产方还款计划",
                    "ext": "pdf"
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_longjiang_daqin_const", body)


def update_gbiz_capital_huabei_runqian_const():
    body = {
        "relationMap": {
            "0": "0",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "5",
            "5": "4",
            "6": "6",
            "7": "99"
        },
        "docTypeMap": {
            "1": "28",
            "2": "30793",
            "9": "30794"
        },
        "guaranteeAttachmentMap": {
            "entrusted_guarantee": "30792",
            "corporate_guarantee": "30791"
        },
        "attachmentMap": {
            "1": "4",
            "2": "5",
            "29": "14",
            "30791": "21",
            "30792": "21"
        },
        "loanUsageDescMap": {
            "1": "数码/电子产品",
            "2": "教育培训",
            "3": "租房屋",
            "4": "其他",
            "5": "旅游",
            "6": "其他",
            "7": "其他",
            "8": "其他",
            "9": "其他"
        },
        "productIdMap": {
            "6": "CPA0101252",
            "12": "CPA0101252"
        },
        "loanStatusMap": {
            "1": "放款成功",
            "3": "放款失败"
        },
        "limitDateUnitMap": {
            "month": "1",
            "day": "8"
        },
        "loanUsageMap": {
            "1": "1",
            "2": "4",
            "3": "7",
            "4": "11",
            "5": "3",
            "6": "11",
            "7": "11",
            "8": "11",
            "9": "11"
        },
        "genderMap": {
            "f": "1",
            "m": "2"
        },
        "auditStatusMap": {
            "1": "审批成功",
            "3": "审批拒绝"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_huabei_runqian_const", body)


def update_gbiz_capital_haishengtong_daqin():
    content = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "register_config": {
            "is_multi_account_card_allowed": True,
            "account_register_duration": 40,
            "is_strict_seq": False,
            "register_step_list": [
                {
                    "channel": "haishengtong_daqin",
                    "step_type": "PROTOCOL",
                    "way": "1",
                    "interaction_type": "SMS",
                    "allow_fail": False,
                    "register_status_effect_duration": 1,
                    "allow_retry": True,
                    "need_confirm_result": False,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode",
                            "allow_fail": False
                        },
                        {
                            "type": "CheckSmsVerifyCode",
                            "allow_fail": False
                        }
                    ]
                }
            ]
        },
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36')",
                            "err_msg": "海胜通大秦[资产还款总额]不满足 irr36，请关注！"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "100001",
                                "messages": [
                                    "资方返回code:0000,msg:成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "99",
                                "messages": [
                                    "余额查询返回的可放余额小于放款金额"
                                ]
                            },
                            {
                                "code": "100400",
                                "messages": [
                                    "资方返回code:0040,msg:mock操作失败，系统异常"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(120)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "2000018",
                                "messages": [
                                    "资方返回code:0000,msg:查询成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "风险控制不通过"
                                ]
                            },
                            {
                                "code": "2000015",
                                "messages": [
                                    "资方返回code:0000,msg:审核未通过"
                                ]
                            },
                            {
                                "code": "80001",
                                "messages": [
                                    "进件查询失败，资方返回订单号为空"
                                ]
                            },
                            {
                                "code": "200201",
                                "messages": [
                                    "资方返回code:0020,msg:mock操作失败,参数错误"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "3",
                                "messages": [
                                    "待审核"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "init": {
                    "delay_time": "delaySeconds(180)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "300001",
                                "messages": [
                                    "资方返回code:0000,msg:处理成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "300201",
                                "messages": [
                                    "资方返回code:0020,msg:mock操作失败,参数错误"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(120)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "4000016",
                                "messages": [
                                    "资方返回code:0000,msg:查询成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "4000017",
                                "messages": [
                                    "资方返回code:0000,msg:放款失败",
                                    "资方返回code:0000,msg:查询成功"
                                ]
                            },
                            {
                                "code": "400501",
                                "messages": [
                                    "资方返回code:0050,msg:mock返回非文档中错误码"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "4000019"
                            }
                        ]
                    }
                ]
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayMinutes(240)"
                }
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_haishengtong_daqin", content)


def update_gbiz_capital_haishengtong_daqin_const():
    body = {
        "protocolProductCode": "GTQH01",
        "yearRate": "0.24",
        "loanProIDMappingMap": {
            "6": "16",
            "12": "12"
        },
        "attachmentTypeMap": {
            "29": 24,
            "31300": 23,
            "31301": 25,
            "31302": 30,
            "31303": 5
        },
        "loanApplyAttachments": [
            1,
            2,
            29,
            31303,
            31301,
            31302,
            31300
        ],
        "bankCodeMap": {
            "PSBC": "C10403",
            "CEB": "C10303",
            "ABC": "C10103",
            "CCB": "C10105",
            "GDB": "C10306",
            "SHBANK": "C10912",
            "PAB": "C10828",
            "COMM": "C10301",
            "HXB": "C10304",
            "CMBC": "C10305",
            "BJBANK": "C10802",
            "BOC": "C10104",
            "ICBC": "C10102",
            "CMB": "C10308",
            "CITIC": "C10302",
            "CIB": "C10309",
            "SPDB": "C10310"
        },
        "genderMap": {
            "F": 2,
            "M": 1
        },
        "educationMap": {
            "1": 15,
            "2": 15,
            "3": 14,
            "4": 13,
            "5": 12,
            "6": 12,
            "7": 12,
            "8": 5,
            "9": 5
        },
        "marriageMap": {
            "1": 2,
            "2": 16,
            "3": 18,
            "4": 19
        },
        "jobIndustryMap": {
            "1": 25,
            "2": 30,
            "3": 28,
            "4": 27,
            "5": 23,
            "6": 1,
            "7": 31,
            "8": 20,
            "9": 24,
            "10": 29,
            "11": 36,
            "12": 34,
            "13": 30,
            "14": 37,
            "15": 22
        },
        "contactRelationshipMap": {
            "0": "2",
            "1": "1",
            "2": "6",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "4",
            "7": "6"
        },
        "auditStatusMap": {
            "1": "风险控制不通过",
            "2": "风险控制通过",
            "3": "待审核",
            "4": "审核通过",
            "5": "审核未通过",
            "6": "放款成功",
            "7": "放款失败",
            "8": "待放款",
            "9": "放款中"
        },
        "productCodeMap": {
            "GTQH01": {
                "accountNo": "572010100101129343",
                "validityDate": "2023-03-23"
            },
            "GTQH02": {
                "accountNo": "572010100101129343",
                "validityDate": "2023-03-23"
            },
            "GTQH03": {
                "accountNo": "572010100101129343",
                "validityDate": "2023-03-23"
            }
        }
    }

    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_haishengtong_daqin_const", body)


def update_gbiz_capital_shanxixintuo(timeout=7200):
    body = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "raise_limit_allowed": False,
        "register_config": {
            "account_register_duration": 30,
            "is_strict_seq": True,
            "register_step_list": [
                {
                    "is_strict_seq": True,
                    "step_type": "PROTOCOL",
                    "register_status_effect_duration": 0,
                    "channel": "shanxixintuo",
                    "interaction_type": "SMS",
                    "need_confirm_result": False,
                    "way": "shanxixintuo",
                    "allow_fail": False,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ],
            "is_multi_account_card_allowed": True,
            "account_recall_register_duration": 40
        },
        "task_config_map": {
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "true||#loan.totalAmount==method.irr(#loan,'36','360per_year','D$25','D+0')",
                            "err_msg": "山西信托[资产还款总额]不满足 irr36（月结日D$25，结清日D+0），请关注！"
                        }
                    ]
                }
            },
            "AssetConfirmOverTimeCheck": {
                "execute": {
                    "user_opt_interaction_over_time_seconds": timeout
                }
            },
            "LoanPreApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanCreditApply": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1000",
                                "messages": [
                                    "成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1001",
                                "messages": [
                                    "mock失败"
                                ]
                            }
                        ]
                    }

                ]
            },
            "LoanCreditQuery": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "10005",
                                "messages": [
                                    "成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "10015"
                            },
                            {
                                "code": "100522",
                                "message": "\\[00400\\]流水不存在"
                            }
                        ]
                    }

                ]
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delaySeconds(5)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "2000",
                                "messages": [
                                    "接收成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2001",
                                "messages": [
                                    "mock失败"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(30)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "2000",
                                "messages": [
                                    "预审成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2001",
                                "messages": [
                                    "mock失败"
                                ]
                            }
                        ]
                    }

                ]
            },
            "LoanPostApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "3000"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "3001",
                                "messages": [
                                    "mock放款申请失败"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "3000",
                                "messages": [
                                    "放款成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "3001",
                                "messages": [
                                    "放款失败"
                                ]
                            },
                            {
                                "code": "3005",
                                "messages": [
                                    "流水不存在"
                                ]
                            }
                        ]
                    }

                ]
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                }
            },
            "CapitalRepayPlanQuery": {
                "execute": {
                    "diff_effect_at": False,
                    "diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": True
                }
            },
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "UserConfirmTimeOutEvent": "LoanConfirmQuery",
                        "UserConfirmFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": [

                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "遇到再进行配置"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "-10000",
                                "messages": [
                                    "遇到再进行配置"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_shanxixintuo", body)


def update_gbiz_capital_shanxixintuo_const():
    body = {
        "ftpChannelName": "shanxixintuo",
        "ftpBaseDir": "/upload/information",
        "orgCode": "sxxt",
        "productConfigMap": {
            "SXXT01": {
                "trustCode": "111111"
            },
            "SXXT02": {
                "trustCode": "222222"
            },
            "SXXT03": {
                "trustCode": "333333"
            }
        },
        "eduMap": {
            "1": "80",
            "2": "70",
            "3": "60",
            "4": "50",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "10",
            "9": "10"
        },
        "marriageMap": {
            "1": "01",
            "2": "20",
            "3": "70",
            "4": "60"
        },
        "custTypeMap": {
            "1": "02",
            "2": "03",
            "3": "03",
            "4": "99",
            "5": "01",
            "6": "04"
        },
        "workWayMap": {
            "1": "I",
            "2": "I",
            "3": "H",
            "4": "E",
            "5": "C",
            "6": "F",
            "7": "B",
            "8": "G",
            "9": "O",
            "10": "M",
            "11": "J",
            "12": "R",
            "13": "O",
            "14": "D",
            "15": "A"
        },
        "uploadAttachmentNameMap": {
            "1": {
                "ftpBaseDir": "/upload/information",
                "fileName": "01_001.jpg"
            },
            "2": {
                "ftpBaseDir": "/upload/information",
                "fileName": "01_002.jpg"
            }
        },
        "downloadAttachmentNameMap": {
            "28": {
                "ftpBaseDir": "/download/information",
                "fileName": "02_001_final.pdf"
            },
            "31501": {
                "ftpBaseDir": "/download/information",
                "fileName": "02_001.pdf"
            }
        },
        "unsignedLoanContractName": "02_001.pdf"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_shanxixintuo_const", body)


def update_gbiz_capital_tongrongbiaonei():
    body = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "register_config": {
            "is_multi_account_card_allowed": True,
            "register_step_list": [
                {
                    "channel": "tongrongbiaonei",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "allow_fail": True,
                    "register_status_effect_duration": 0,
                    "need_confirm_result": True,
                    "actions": [
                        {
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ]
        },
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "UpdateCardTimeOutEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
                    },
                    "can_change_capital": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "finalFail"
                        },
                        "matches": [
                            {
                                "code": "12",
                                "messages": [

                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "遇到再进行配置"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "-10000",
                                "messages": [
                                    "遇到再进行配置"
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36')",
                            "err_msg": "通融表内[资产还款总额]不满足 irr36，请关注！"
                        }
                    ]
                }
            },
            "LoanApplyNew": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "200"
                            },
                            {
                                "code": "2004",
                                "messages": [
                                    "订单状态异常！待放款"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [

                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delayMinutes(1)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "-1"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "1101",
                                "messages": [
                                    "系统错误"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [

                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
                "init": {
                    "delay_time": "delayMinutes(2)"
                },
                "execute": {
                    "allow_update_card": True
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "\\[G00022\\]超过最大失败次数.*",
                                    "\\[G00023\\]超过最大代付时长.*",
                                    "\\[FAILED\\]放款失败"
                                ]
                            },
                            {
                                "code": "KN_RISK_CONTROL"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "updateCard"
                        },
                        "matches": [
                            {
                                "code": "1",
                                "messages": [
                                    "\\[E20107\\]无效卡号，请核对后重新输入",
                                    "\\[E20129\\]您输入的卡号已注销，详询发卡行",
                                    "\\[E20005\\]超出支付限额,请联系发卡行",
                                    "\\[KN_INVALID_ACCOUNT\\]无效账户",
                                    "\\[E20012\\]该卡暂无法支付，请换卡，或联系银行",
                                    "\\[E20135\\]持卡人账户状态为已锁定，请联系签约行",
                                    "\\[E20141\\]银行交易失败，请联系发卡行，或稍后重试",
                                    "\\[E20144\\]银行卡状态异常，请换卡或联系发卡行",
                                    "\\[E20195\\]持卡人身份证或手机号输入不正确",
                                    "\\[E20106\\]银行预留手机号有误",
                                    "\\[E20104\\]持卡人姓名有误",
                                    "\\[E20008\\]持卡人信息有误，请检查后重新输入",
                                    "\\[E20108\\]您输入的卡号已挂失，详询发卡行",
                                    "\\[E20145\\]交易失败，单笔交易金额超限",
                                    "\\[E20009\\]持卡人身份证已过期"
                                ]
                            }
                        ]
                    }
                ]
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayRandomSeconds(300,600)"
                }
            },
            "AssetConfirmOverTimeCheck": {
                "execute": {
                    "update_card_over_time_seconds": 600
                },
                "finish": [
                    {
                        "action": {
                            "policy": "timeoutAndFail"
                        },
                        "matches": [
                            {
                                "code": "10005",
                                "messages": [
                                    "确认类型.*已超时"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_tongrongbiaonei", body)


def update_gbiz_capital_tongrongbiaonei_const():
    body = {
        "isSelfProduct": 1,
        "interestRate": "0.120",
        "lateInterestRate": "0.050",
        "usageMap": {
            "1": "2-个人日常消费",
            "2": "3-教育",
            "3": "12-场地租赁",
            "4": "2-个人日常消费",
            "5": "5-旅游",
            "6": "8-医疗",
            "7": "8-医疗",
            "8": "2-个人日常消费",
            "9": "7-其他消费"
        },
        "loanNotifyUrl": "null",
        "confirmNotifyUrl": "null",
        "withdrawSubjectKey": "trbn_withdraw"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_tongrongbiaonei_const", body)


def update_gbiz_guarantee_hanchen_jinmeixin_const():
    body = {
        "bankAnnualRate": "9.8",
        "totalRate": "24",
        "ftpChannelName": "hanchen_jinmeixin",
        "baseDir": "/file",
        "marriageMap": {
            "0": "99",
            "1": "10",
            "2": "20",
            "3": "30",
            "4": "40"
        },
        "educationMap": {
            "1": "10",
            "2": "10",
            "3": "20",
            "4": "30",
            "5": "40",
            "6": "40",
            "7": "60",
            "8": "70",
            "9": "80",
            "10": "90"
        },
        "residenceStatus": {
            "0": "9",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7"
        },
        "corpTradeMap": {
            "0": "9",
            "1": "S",
            "2": "S",
            "3": "P",
            "4": "Q",
            "5": "G",
            "6": "E",
            "7": "C",
            "8": "I",
            "9": "J",
            "10": "L",
            "11": "R",
            "12": "R"
        },
        "dutyMap": {
            "0": "9",
            "1": "1",
            "2": "2"
        },
        "signContractTypes": {
            "33311": {
                "type": "wd_bank_letter",
                "interfaceName": "tasynstreamsave",
                "downloadType": 33306
            }
        },
        "filePrefixMap": {
            "loan_detail": "loan_",
            "repay_plan": "paymentPlan_",
            "borrower": "customer_",
            "borrower_family": "customer_family_",
            "borrower_marriage": "customer_marriage_",
            "borrower_work": "customer_work_"
        }

    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_guarantee_hanchen_jinmeixin_const", body)



def update_gbiz_account_config():
    body = {
            "blacklist_code_msg": {
                "DK0000019": [
                    "超过同一用户绑定卡数"
                ]
            },
            "max_sms_not_verify_times": 2,
            "max_request_fail_times": 2,
            "blacklist_expired_days": 90,
            "api_err_msg_mapping": {
                "default_global_error_msg": "开户服务请求异常，请稍后再试！",
                "api_err_msg_matches": [
                    {
                        "message": "新增自定义msg需要加在最前面",
                        "matches": [
                            {
                                "code": "2",
                                "messages": [
                                    ".*资方返回失败msg，遇到再配置.*"
                                ]
                            }
                        ]
                    },
                    {
                        "message": "成功",
                        "matches": [
                            {
                                "code": "0",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "message": "处理中",
                        "matches": [
                            {
                                "code": "2",
                                "messages": []
                            }
                        ]
                    },
                    {
                        "message": "未执行",
                        "matches": [
                            {
                                "code": "4",
                                "messages": []
                            }
                        ]
                    }
                ]
            }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_account_config", body)


if __name__ == "__main__":
    # 环境更新
    gc.init_env(9, "china", "dev")
    update_gbiz_payment_config()
    update_gbiz_base_config()
    update_gbiz_account_config()
    update_gbiz_capital_noloan()
    update_gbiz_capital_hamitianbang_xinjiang()
    update_gbiz_capital_lanhai_zhongshi_qj()
