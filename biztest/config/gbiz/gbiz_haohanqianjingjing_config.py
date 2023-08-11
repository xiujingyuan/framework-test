
import common.global_const as gc

def update_gbiz_capital_haohanqianjingjing(update_card_over_time_seconds=86400):
    paydayloan = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "register_config": {
            "register_step_list":[
                {
                    "channel":"haohanqianjingjing",
                    "step_type":"PAYSVR_PROTOCOL",
                    "way":"qianjingjing",
                    "interaction_type":"SMS",
                    "group":"kuainiu",
                    "status_scene":{
                        "register":{
                            "success_type":"executed",
                            "allow_fail":True,
                            "need_confirm_result":True
                        },
                        "route":{
                            "success_type":"executed",
                            "allow_fail":True
                        },
                        "validate":{
                            "success_type":"executed"
                        }
                    },
                    "actions":[
                        {
                            "type":"GetSmsVerifyCode"
                        },
                        {
                            "type":"CheckSmsVerifyCode"
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
                            "err_msg": "浩瀚钱京京[资产还款总额]不满足 irr36，请关注！"
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
                                "code": "0",
                                "messages": [
                                    "处理成功"
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
                                "code": "1"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(420)"
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
                    "delay_time": "delaySeconds(2)"
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
            "CapitalRepayPlanGenerate": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "BondTransferQuery": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                }
            },
            "PaymentTransferQuery": {
                "init": {
                    "delay_time": "delaySeconds(3)"
                }
            },
            "AssetConfirmOverTimeCheck": {
                "execute": {
                    "update_card_over_time_seconds": update_card_over_time_seconds
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
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_haohanqianjingjing", paydayloan)


def update_gbiz_capital_haohanqianjingjing_const():
    body = {
        "transferName": "enc_04_2755506557550069760_659",
        "transferAccount": "enc_03_3370357756397094912_403",
        "transferIdentity": "enc_02_2580379904328075267_458",
        "transferBankCode": "ICBC",
        "withdrawSubjectKey": "hhqjj_withdraw",
        "transferSubjectKey": "hhqjj_transfer"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_haohanqianjingjing_const", body)