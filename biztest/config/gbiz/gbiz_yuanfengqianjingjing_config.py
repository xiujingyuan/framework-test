
import common.global_const as gc

def update_gbiz_capital_yuanfengqianjingjing(update_card_over_time_seconds=86400):
    paydayloan = {
                "cancelable_task_list": [
                    "ApplyCanLoan",
                    "LoanApplyNew",
                    "ChangeCapital"
                ],
                "register_config": {
                    "is_multi_account_card_allowed": True,
                    "register_step_list": [
                        {
                            "channel": "yuanfengqianjingjing",
                            "step_type": "PAYSVR_PROTOCOL",
                            "way": "qianjingjing",
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
                "workflow": {
                    "title": "元丰钱京京",
                    "inclusions": [
                        "gbiz_capital_workflow_asset"
                    ],
                    "nodes": [
                        {
                            "id": "UpdateCard-API",
                            "type": "UpdateCardSyncTaskHandler",
                            "events": [
                                "AccountBankCardUpdateSucceededEvent"
                            ],
                            "activity": {
                                "init": {},
                                "execute": {},
                                "finish": []
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
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute": {
                                    "loan_validator": [
                                        {
                                            "rule": "#loan.totalAmount>=cmdb.irr(#loan,'35.99') && #loan.totalAmount<=cmdb.irr(#loan,'36')",
                                            "err_msg": "元丰钱京京[资产还款总额]不满足 【irr35.99, irr36】，请关注！"
                                        }
                                    ]
                                },
                                "finish": []
                            }
                        },
                        {
                            "id": "AssetImportVerify",
                            "type": "AssetImportVerifyTaskHandler",
                            "events": [
                                "AssetImportVerifySucceededEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute": {},
                                "finish": []
                            }
                        },
                        {
                            "id": "ApplyCanLoan",
                            "type": "ApplyCanLoanTaskHandler",
                            "events": [
                                "AssetReadyEvent",
                                "AssetCanLoanFailedEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": True
                                },
                                "execute": {},
                                "finish": []
                            }
                        },
                        {
                            "id": "LoanApplyNew",
                            "type": "LoanApplyNewTaskHandler",
                            "events": [
                                "LoanApplySyncSucceededEvent",
                                "LoanApplySyncFailedEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": True
                                },
                                "execute": {},
                                "finish": [
                                    {
                                        "action": {
                                            "policy": "success",
                                            "ignoreNotify": False
                                        },
                                        "matches": [
                                            {
                                                "code": "0",
                                                "messages": None
                                            }
                                        ]
                                    },
                                    {
                                        "action": {
                                            "policy": "fail",
                                            "ignoreNotify": False
                                        },
                                        "matches": [
                                            {
                                                "code": "1",
                                                "messages": None
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "id": "ChangeCapital",
                            "type": "ChangeCapitalTaskHandler",
                            "events": [
                                "CapitalChangeSucceededEvent",
                                "AssetVoidReadyEvent",
                                "CapitalChangeFailedEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "manual",
                                    "cancelable": True
                                },
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
                                    "policy": "success",
                                    "ignoreNotify": False
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
                                    "policy": "finalFail",
                                    "ignoreNotify": False
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
                                    "policy": "fail",
                                    "ignoreNotify": False
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
                                        "policy": "retry",
                                        "ignoreNotify": False
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
                        },
                        {
                            "id": "LoanApplyQuery",
                            "type": "LoanApplyQueryTaskHandler",
                            "events": [
                                "LoanApplyAsyncSucceededEvent",
                                "LoanApplyAsyncFailedEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute": {},
                                "finish": [
                                    {
                                        "action": {
                                            "policy": "success",
                                            "ignoreNotify": False
                                        },
                                        "matches": [
                                            {
                                                "code": "0",
                                                "messages": None
                                            }
                                        ]
                                    },
                                    {
                                        "action": {
                                            "policy": "fail",
                                            "ignoreNotify": False
                                        },
                                        "matches": [
                                            {
                                                "code": "1",
                                                "messages": None
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "id": "AssetAutoImport",
                            "type": "AssetAutoImportTaskHandler",
                            "events": [],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute": {},
                                "finish": []
                            }
                        },
                        {
                            "id": "LoanApplyConfirm",
                            "type": "LoanApplyConfirmTaskHandler",
                            "events": [
                                "ConfirmApplySyncSucceededEvent",
                                "ConfirmApplySyncFailedEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute": {},
                                "finish": [
                                    {
                                        "action": {
                                            "policy": "success",
                                            "ignoreNotify": False
                                        },
                                        "matches": [
                                            {
                                                "code": "0",
                                                "messages": None
                                            }
                                        ]
                                    },
                                    {
                                        "action": {
                                            "policy": "fail",
                                            "ignoreNotify": False
                                        },
                                        "matches": []
                                    }
                                ]
                            }
                        },
                        {
                            "id": "LoanConfirmQuery",
                            "type": "LoanConfirmQueryTaskHandler",
                            "events": [
                                "GrantSucceededEvent",
                                "UpdateCardNotifyEvent",
                                "GrantFailedEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "simpleLock": None,
                                    "delayTime": "delayMinutes(2)"
                                },
                                "execute": {
                                    "allow_update_card": True
                                },
                                "finish": [
                                    {
                                        "action": {
                                            "policy": "success",
                                            "ignoreNotify": False
                                        },
                                        "matches": [
                                            {
                                                "code": "0",
                                                "messages": None
                                            }
                                        ]
                                    },
                                    {
                                        "action": {
                                            "policy": "fail",
                                            "ignoreNotify": False
                                        },
                                        "matches": [
                                            {
                                                "code": "1",
                                                "messages": [
                                                    "\\[G00022\\]超过最大失败次数.*",
                                                    "\\[G00023\\]超过最大代付时长.*",
                                                    "\\[E20155\\]您的银行卡暂不支持该业务，请向您的银行咨询",
                                                    "\\[1000\\]资产\\[.*\\],代付账户余额为0"
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "action": {
                                            "policy": "retry",
                                            "ignoreNotify": False
                                        },
                                        "matches": [
                                            {
                                                "code": "2",
                                                "messages": [
                                                    "元丰钱京京代付未成功",
                                                    "支付订单.*,代付中"
                                                ]
                                            }
                                        ]
                                    },
                                    {
                                        "action": {
                                            "policy": "updateCard",
                                            "ignoreNotify": False
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
                                                    "\\[E20205\\]账户为银行黑名单账户或因风控原因拒绝支付",
                                                    "\\[E20009\\]持卡人身份证已过期",
                                                    "\\[E20122\\]该卡连续交易失败次数超限，请明日再试",
                                                    "\\[E20151\\]您的卡已冻结，详询发卡行"
                                                ]
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "id": "CapitalRepayPlanGenerate",
                            "type": "CapitalRepayPlanGenerateTaskHandler",
                            "events": [
                                "CapitalRepayPlanGenerateSucceededEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute": {},
                                "finish": []
                            }
                        },
                        {
                            "id": "UpdateCardRequestMsgSender",
                            "type": "UpdateCardRequestMsgSender",
                            "events": [],
                            "activity": {
                                "init": {},
                                "execute": {},
                                "finish": []
                            }
                        },
                        {
                            "id": "AssetConfirmOverTimeCheck",
                            "type": "AssetConfirmOverTimeCheckTaskHandler",
                            "events": [
                                "UpdateCardTimeOutEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "delayTime": "delaySeconds(86400)"
                                },
                                "execute": {
                                },
                                "finish": [
                                        {
                                            "action": {
                                                "policy": "timeoutAndFail",
                                                "ignoreNotify": False
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
                        },
                        {
                            "id": "RongDanIrrTrial",
                            "type": "RongDanIrrTrialTaskHandler",
                            "events": [
                                "RongDanIrrTrialSucceededEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute": {},
                                "finish": []
                            }
                        },
                        {
                            "id": "BondTransfer",
                            "type": "BondTransferTaskHandler",
                            "events": [
                                "BondTransferApplySucceededEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute": {},
                                "finish": []
                            }
                        },
                        {
                            "id": "BondTransferQuery",
                            "type": "BondTransferQueryTaskHandler",
                            "events": [
                                "BondTransferSucceededEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "simpleLock": None,
                                    "delayTime": "delayMinutes(2)"
                                },
                                "execute": {},
                                "finish": []
                            }
                        },
                        {
                            "id": "ContractPush",
                            "type": "ContractPushTaskHandler",
                            "events": [],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "simpleLock": None,
                                    "delayTime": "delayFixTime('22:30:00')"
                                },
                                "execute": {},
                                "finish": []
                            }
                        },
                        {
                            "id": "LoanGrantStatusPush",
                            "type": "LoanGrantStatusPushTaskHandler",
                            "events": [
                                "GrantNoticeSucceededEvent"
                            ],
                            "activity": {
                                "init": {
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "simpleLock": None,
                                    "delayTime": "delayFixTime('22:30:00')"
                                },
                                "execute": {},
                                "finish": []
                            }
                        }
                    ],
                    "subscribers": [
                        {
                            "listen": {
                                "event": "AccountBankCardUpdateSucceededEvent"
                            },
                            "nodes": [
                                "LoanApplyConfirm"
                            ]
                        },
                        {
                            "listen": {
                                "event": "AssetImportReadyEvent"
                            },
                            "nodes": [
                                "AssetImport"
                            ]
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
                                "event": "AssetImportVerifySucceededEvent"
                            },
                            "nodes": [
                                "ApplyCanLoan"
                            ]
                        },
                        {
                            "listen": {
                                "event": "AssetReadyEvent"
                            },
                            "nodes": [
                                "LoanApplyNew"
                            ]
                        },
                        {
                            "listen": {
                                "event": "AssetCanLoanFailedEvent"
                            },
                            "nodes": [
                                "ChangeCapital"
                            ],
                            "associateData": {
                                "sourceWorkflowNodeId": None,
                                "event": "AssetCanLoanFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen": {
                                "event": "LoanApplySyncSucceededEvent"
                            },
                            "nodes": [
                                "LoanApplyQuery"
                            ]
                        },
                        {
                            "listen": {
                                "event": "LoanApplySyncFailedEvent"
                            },
                            "nodes": [
                                "ChangeCapital"
                            ],
                            "associateData": {
                                "sourceWorkflowNodeId": "LoanApplyQuery",
                                "event": "LoanApplySyncFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen": {
                                "event": "LoanApplyAsyncSucceededEvent"
                            },
                            "nodes": [
                                "LoanApplyConfirm"
                            ]
                        },
                        {
                            "listen": {
                                "event": "LoanApplyAsyncFailedEvent"
                            },
                            "nodes": [
                                "ChangeCapital"
                            ],
                            "associateData": {
                                "sourceWorkflowNodeId": "LoanApplyQuery",
                                "event": "LoanApplyAsyncFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen": {
                                "event": "ConfirmApplySyncSucceededEvent"
                            },
                            "nodes": [
                                "LoanConfirmQuery"
                            ]
                        },
                        {
                            "listen": {
                                "event": "ConfirmApplySyncFailedEvent"
                            },
                            "nodes": [
                                "ChangeCapital"
                            ],
                            "associateData": {
                                "sourceWorkflowNodeId": "LoanConfirmQuery",
                                "event": "ConfirmApplySyncFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen": {
                                "event": "GrantSucceededEvent"
                            },
                            "nodes": [
                                "CapitalRepayPlanGenerate"
                            ]
                        },
                        {
                            "listen": {
                                "event": "UpdateCardNotifyEvent"
                            },
                            "nodes": [
                                "AssetConfirmOverTimeCheck"
                            ],
                            "associateData": {
                                "canRetry": True,
                                "assetConfirmType": "WITHDRAW_FINAL_FAIL_UPDATE_CARD",
                                "overTimeInterval": update_card_over_time_seconds
                            }
                        },
                        {
                            "listen": {
                                "event": "UpdateCardNotifyEvent"
                            },
                            "nodes": [
                                "UpdateCardRequestMsgSender"
                            ]
                        },
                        {
                            "listen": {
                                "event": "GrantFailedEvent"
                            },
                            "nodes": [
                                "ChangeCapital"
                            ],
                            "associateData": {
                                "sourceWorkflowNodeId": "LoanConfirmQuery",
                                "event": "GrantFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen": {
                                "event": "UpdateCardTimeOutEvent"
                            },
                            "nodes": [
                                "AssetVoid"
                            ]
                        },
                        {
                            "listen": {
                                "event": "RongDanIrrTrialSucceededEvent"
                            },
                            "nodes": [
                                "BondTransfer"
                            ]
                        },
                        {
                            "listen": {
                                "event": "BondTransferApplySucceededEvent"
                            },
                            "nodes": [
                                "BondTransferQuery"
                            ]
                        },
                        {
                            "listen": {
                                "event": "BondTransferSucceededEvent"
                            },
                            "nodes": [
                                "LoanGrantStatusPush"
                            ]
                        },
                        {
                            "listen": {
                                "event": "GrantNoticeSucceededEvent"
                            },
                            "nodes": [
                                "ContractPush"
                            ]
                        }
                    ]
                }
            }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yuanfengqianjingjing", paydayloan)


def update_gbiz_capital_yuanfengqianjingjing_const():
    body = {
        "transferName": "enc_04_2755506557550069760_659",
        "transferAccount": "enc_03_4573340679996453888_590",
        "transferIdentity": "enc_02_2580379904328075267_458",
        "transferBankCode": "ICBC",
        "withdrawSubjectKey": "yfqjj_withdraw",
        "transferSubjectKey": "yfqjj_transfer",
        "successCodeList": [
            "0"
        ],
        "mode": "1",
        "attachmentConfigList": [
            {
                "docType": "4",
                "contractType": 1,
                "maxAllowedSize": 0,
                "minAllowedSize": 0
            },
            {
                "docType": "5",
                "contractType": 2,
                "maxAllowedSize": 0,
                "minAllowedSize": 0
            }
        ],
        "contractConfigList": [
        {
            "docType": "1",
            "contractType": 37500
        },
        {
            "docType": "44",
            "contractType": 37503
        },
        {
            "docType": "45",
            "contractType": 37504
        }
    ],
        "periodUnit": "1",
        "payChannel": "sumpay",
        "dateFormat": "yyyy-MM-dd HH:mm:ss",
        "loanUsageMap": {
            "1": "个人消费",
            "2": "各类培训",
            "3": "租房",
            "4": "娱乐",
            "5": "旅游",
            "6": "医疗",
            "7": "美容",
            "8": "购物",
            "9": "其他"
        },
        "bankCodeMap": {
            "ICBC": "ICBC",
            "CCB": "CCB",
            "ABC": "ABC",
            "CMB": "CMB",
            "BOC": "BOC",
            "COMM": "BCM",
            "HXBANK": "HXB",
            "CMBC": "CMBC",
            "CEB": "CEB",
            "CIB": "CIB",
            "SPDB": "SPDB",
            "CITIC": "CITIC",
            "PSBC": "PSBC",
            "SPABANK": "PAB",
            "GDB": "CGB",
            "SHBANK": "BOS",
            "BJBANK": "BOB",
            "EGBANK": "EGB"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yuanfengqianjingjing_const", body)