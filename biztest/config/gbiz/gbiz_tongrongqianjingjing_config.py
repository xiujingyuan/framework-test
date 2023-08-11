import common.global_const as gc


def update_gbiz_capital_tongrongqianjingjing():
    body = {
        "cancelable_task_list":
            [
                "ApplyCanLoan",
                "LoanApplyNew",
                "ChangeCapital"
            ],
        "register_config":
            {
                "register_step_list":
                    [
                        {
                            "channel": "tongrongqianjingjing",
                            "step_type": "PAYSVR_PROTOCOL",
                            "way": "qianjingjing",
                            "interaction_type": "SMS",
                            "group": "kuainiu",
                            "status_scene":
                                {
                                    "register":
                                        {
                                            "success_type": "executed",
                                            "allow_fail": True,
                                            "need_confirm_result": True,
                                            "register_status_effect_duration_day": 0
                                        },
                                    "route":
                                        {
                                            "success_type": "executed",
                                            "allow_fail": True
                                        },
                                    "validate":
                                        {
                                            "success_type": "executed"
                                        }
                                },
                            "actions":
                                [
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
        # "task_config_map":{
        #         "ChangeCapital":
        #             {
        #                 "execute":
        #                     {
        #                         "event_handler_map":
        #                             {
        #                                 "UpdateCardTimeOutEvent": "LoanConfirmQuery",
        #                                 "GrantFailedEvent": "LoanConfirmQuery",
        #                                 "LoanApplySyncFailedEvent": "LoanApplyQuery",
        #                                 "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
        #                                 "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
        #                             },
        #                         "can_change_capital": True
        #                     },
        #                 "finish":
        #                     [
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "success"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "0",
        #                                         "messages":
        #                                             [
        #                                                 "切资方路由\\(二次\\)成功"
        #                                             ]
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "finalFail"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "12",
        #                                         "messages":
        #                                             []
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "fail"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "1",
        #                                         "messages":
        #                                             [
        #                                                 "遇到再进行配置"
        #                                             ]
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "retry"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "-10000",
        #                                         "messages":
        #                                             [
        #                                                 "遇到再进行配置"
        #                                             ]
        #                                     }
        #                                 ]
        #                         }
        #                     ]
        #             },
        #         "AssetAutoImport":
        #             {
        #                 "init":
        #                     {
        #                         "delay_time": "delayMinutes(90)"
        #                     }
        #             },
        #         "AssetImport":
        #             {
        #                 "execute":
        #                     {
        #                         "loan_validator":
        #                             [
        #                                 {
        #                                     "rule": "#loan.totalAmount>=cmdb.irr(#loan,'35.99') && #loan.totalAmount<=cmdb.irr(#loan,'36')",
        #                                     "err_msg": "通融钱京京[资产还款总额]不满足 irr36，请关注！"
        #                                 }
        #                             ]
        #                     }
        #             },
        #         "LoanApplyNew":
        #             {
        #                 "finish":
        #                     [
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "success"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "10000",
        #                                         "messages":
        #                                             [
        #                                                 "00000_true_成功_2_B"
        #                                             ]
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "fail"
        #                                 },
        #                             "matches": [
        #                                 {
        #                                     "code": "10000",
        #                                     "messages":
        #                                         [
        #                                             "00000_true_成功_3_B"
        #                                         ]
        #                                 }
        #                             ]
        #
        #                         }
        #                     ]
        #             },
        #         "LoanApplyQuery":
        #             {
        #                 "init":
        #                     {
        #                         "delay_time": "delayMinutes(1)"
        #                     },
        #                 "finish":
        #                     [
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "success"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "10000",
        #                                         "messages":
        #                                             [
        #                                                 "00000_true_成功_2_A"
        #                                             ]
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "fail"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "10000",
        #                                         "messages":
        #                                             [
        #                                                 "500001_false_:查询订单失败_null_null"
        #                                             ]
        #                                     },
        #                                     {
        #                                         "code": "10000",
        #                                         "messages":
        #                                             [
        #                                                 "00000_true_成功_3_A"
        #                                             ]
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "retry"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "1101",
        #                                         "messages":
        #                                             [
        #                                                 "系统错误"
        #                                             ]
        #                                     }
        #                                 ]
        #                         }
        #                     ]
        #             },
        #         "LoanPostApply":
        #             {
        #                 "finish":
        #                     [
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "success"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "0",
        #                                         "messages":
        #                                             [
        #                                                 "合同预览成功"
        #                                             ]
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "fail"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "19999",
        #                                         "messages":
        #                                             [
        #                                                 "遇到再配置"
        #                                             ]
        #                                     }
        #                                 ]
        #                         }
        #                     ]
        #             },
        #         "LoanPostCredit":
        #             {
        #                 "finish":
        #                     [
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "success"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "10000",
        #                                         "messages":
        #                                             [
        #                                                 "00000_true_成功"
        #                                             ]
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "fail"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "19999",
        #                                         "messages":
        #                                             [
        #                                                 "遇到再配置"
        #                                             ]
        #                                     }
        #                                 ]
        #                         }
        #                     ]
        #             },
        #         "LoanApplyConfirm":
        #             {
        #                 "finish":
        #                     [
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "success"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "0"
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "fail"
        #                                 },
        #                             "matches":
        #                                 []
        #                         }
        #                     ]
        #             },
        #         "LoanConfirmQuery":
        #             {
        #                 "init":
        #                     {
        #                         "delay_time": "delayMinutes(2)"
        #                     },
        #                 "execute":
        #                     {
        #                         "allow_update_card": True
        #                     },
        #                 "finish":
        #                     [
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "success"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "0"
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "fail"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "1",
        #                                         "messages":
        #                                             [
        #                                                 "\\[G00022\\]超过最大失败次数.*",
        #                                                 "\\[G00023\\]超过最大代付时长.*",
        #                                                 "\\[E20155\\]您的银行卡暂不支持该业务，请向您的银行咨询",
        #                                                 "\\[1000\\]资产\\[.*\\],代付账户余额为0"
        #                                             ]
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "retry"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "2",
        #                                         "messages":
        #                                             [
        #                                                 "通融钱京京代付未成功"
        #                                             ]
        #                                     },
        #                                     {
        #                                         "code": "2"
        #                                     }
        #                                 ]
        #                         },
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "updateCard"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "1",
        #                                         "messages":
        #                                             [
        #                                                 "\\[E20107\\]无效卡号，请核对后重新输入",
        #                                                 "\\[E20129\\]您输入的卡号已注销，详询发卡行",
        #                                                 "\\[E20005\\]超出支付限额,请联系发卡行",
        #                                                 "\\[KN_INVALID_ACCOUNT\\]无效账户",
        #                                                 "\\[E20012\\]该卡暂无法支付，请换卡，或联系银行",
        #                                                 "\\[E20135\\]持卡人账户状态为已锁定，请联系签约行",
        #                                                 "\\[E20141\\]银行交易失败，请联系发卡行，或稍后重试",
        #                                                 "\\[E20144\\]银行卡状态异常，请换卡或联系发卡行",
        #                                                 "\\[E20195\\]持卡人身份证或手机号输入不正确",
        #                                                 "\\[E20106\\]银行预留手机号有误",
        #                                                 "\\[E20104\\]持卡人姓名有误",
        #                                                 "\\[E20008\\]持卡人信息有误，请检查后重新输入",
        #                                                 "\\[E20108\\]您输入的卡号已挂失，详询发卡行",
        #                                                 "\\[E20145\\]交易失败，单笔交易金额超限",
        #                                                 "\\[E20205\\]账户为银行黑名单账户或因风控原因拒绝支付",
        #                                                 "\\[E20009\\]持卡人身份证已过期",
        #                                                 "\\[E20122\\]该卡连续交易失败次数超限，请明日再试",
        #                                                 "\\[E20151\\]您的卡已冻结，详询发卡行"
        #                                             ]
        #                                     }
        #                                 ]
        #                         }
        #                     ]
        #             },
        #         "ContractDown":
        #             {
        #                 "execute":
        #                     {
        #                         "interval_in_minutes": "240"
        #                     },
        #                 "init":
        #                     {
        #                         "delay_time": "delayRandomSeconds(300,600)"
        #                     }
        #             },
        #         "BondContractDown":
        #             {
        #                 "execute":
        #                     {
        #                         "interval_in_minutes": "120"
        #                     },
        #                 "init":
        #                     {
        #                         "delay_time": "delayMinutes(5)"
        #                     }
        #             },
        #         "ElectronicReceiptDown": {
        #             "execute": {
        #                 "interval_in_minutes": "120"
        #             },
        #             "init": {
        #                 "delay_time": "delayHours(24)"
        #             }
        #         },
        #         "AssetConfirmOverTimeCheck":
        #             {
        #                 "execute":
        #                     {
        #                         "update_card_over_time_seconds": 20
        #                     },
        #                 "finish":
        #                     [
        #                         {
        #                             "action":
        #                                 {
        #                                     "policy": "timeoutAndFail"
        #                                 },
        #                             "matches":
        #                                 [
        #                                     {
        #                                         "code": "10005",
        #                                         "messages":
        #                                             [
        #                                                 "确认类型.*已超时"
        #                                             ]
        #                                     }
        #                                 ]
        #                         }
        #                     ]
        #             }
        #     }
        "workflow": {
            "title": "通融钱京京放款流程编排v3",
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
                        "init": {

                        },
                        "execute": {

                        },
                        "finish": [

                        ]
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
                                    "rule": "#loan.totalAmount==cmdb.irr(#loan,'35.99')",
                                    "err_msg": "通融钱京京[资产还款总额]不满足 irr36，请关注！"
                                }
                            ]
                        },
                        "finish": [

                        ]
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
                        "execute": {

                        },
                        "finish": [

                        ]
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
                        "execute": {

                        },
                        "finish": [

                        ]
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
                        "execute": {

                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "10000",
                                        "messages": [
                                            "00000_true_成功_2_B"
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
                                        "code": "10000",
                                        "messages": [
                                            "00000_true_成功_3_B"
                                        ]
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
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(1)"
                        },
                        "execute": {

                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "10000",
                                        "messages": [
                                            "00000_true_成功_2_A"
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
                                        "code": "10000",
                                        "messages": [
                                            "00000_true_成功_3_A",
                                            "500001_false_:查询订单失败_null_null"
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
                                        "code": "1101",
                                        "messages": [
                                            "系统错误"
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "AssetAutoImport",
                    "type": "AssetAutoImportTaskHandler",
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(90)"
                        },
                        "execute": {

                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "LoanPostApply",
                    "type": "LoanPostApplyTaskHandler",
                    "events": [
                        "LoanPostApplySucceededEvent",
                        "LoanPostApplyFailedEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False
                        },
                        "execute": {

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
                                            "合同预览成功"
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
                                        "code": "19999",
                                        "messages": [
                                            "遇到再配置"
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "LoanPostCredit",
                    "type": "LoanPostCreditTaskHandler",
                    "events": [
                        "LoanPostCreditSucceededEvent",
                        "LoanPostCreditFailedEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False
                        },
                        "execute": {

                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "10000",
                                        "messages": [
                                            "00000_true_成功"
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
                                        "code": "10000",
                                        "messages": [
                                            "遇到再配置"
                                        ]
                                    }
                                ]
                            }
                        ]
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
                        "execute": {

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

                                ]
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
                                            "通融钱京京代付未成功"
                                        ]
                                    },
                                    {
                                        "code": "2",
                                        "messages": None
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
                        "execute": {

                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "ContractDown",
                    "type": "ContractDownTaskHandler",
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayRandomSeconds(300,600)"
                        },
                        "execute": {
                            "interval_in_minutes": "240"
                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "UpdateCardRequestMsgSender",
                    "type": "UpdateCardRequestMsgSender",
                    "events": [

                    ],
                    "activity": {
                        "init": {

                        },
                        "execute": {

                        },
                        "finish": [

                        ]
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
                            "cancelable": False
                        },
                        "execute": {
                            "update_card_over_time_seconds": 30
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
                    "id": "LoanGrantStatusPush",
                    "type": "LoanGrantStatusPushTaskHandler",
                    "events": [
                        "GrantNoticeSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False
                        },
                        "execute": {

                        },
                        "finish": [

                        ]
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
                        "execute": {

                        },
                        "finish": [

                        ]
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
                            "cancelable": False
                        },
                        "execute": {

                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "BondContractDown",
                    "type": "BondContractDownTaskHandler",
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(5)"
                        },
                        "execute": {
                            "interval_in_minutes": "120"
                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "ElectronicReceiptDown",
                    "type": "ElectronicReceiptDownTaskHandler",
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayHours(24)"
                        },
                        "execute": {
                            "interval_in_minutes": "120"
                        },
                        "finish": [

                        ]
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
                        "LoanPostApply"
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
                        "event": "LoanPostApplySucceededEvent"
                    },
                    "nodes": [
                        "LoanPostCredit"
                    ]
                },
                {
                    "listen": {
                        "event": "LoanPostApplyFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": None,
                        "event": "LoanPostApplyFailedEvent",
                        "skipDoubleCheck": False
                    }
                },
                {
                    "listen": {
                        "event": "LoanPostCreditSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyConfirm"
                    ]
                },
                {
                    "listen": {
                        "event": "LoanPostCreditFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": "LoanPostCredit",
                        "event": "LoanPostCreditFailedEvent",
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
                        "CapitalRepayPlanGenerate",
                        "ContractDown"
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
                        "overTimeInterval": 20
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
                        "LoanGrantStatusPush"
                    ]
                },
                {
                    "listen": {
                        "event": "GrantNoticeSucceededEvent"
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
                        "BondContractDown",
                        "ElectronicReceiptDown"
                    ]
                }
            ]
        }

    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_tongrongqianjingjing", body)


def update_gbiz_capital_tongrongqianjingjing_const():
    body = {
        "merchantId": "2022010419061200028",
        "productId": "PD2023020115090824300006",
        "transferNoticeType": "30611",
        "transferAgreeType": "10501",
        "sexMap":
            {
                "m": "1",
                "f": "2"
            },
        "maritalStatusMap":
            {
                "1": "10",
                "2": "20",
                "3": "30",
                "4": "40"
            },
        "applyPeriodsTypeMap":
            {
                "month": "2",
                "day": "1"
            },
        "applyPurposeMap":
            {
                "1": "2",
                "2": "3",
                "3": "9",
                "4": "2",
                "5": "4",
                "6": "5",
                "7": "5",
                "8": "2",
                "9": "2"
            },
        "relationshipMap":
            {
                "0": "0",
                "1": "1",
                "2": "4",
                "3": "3",
                "4": "6",
                "5": "9",
                "6": "5",
                "7": "9"
            },
        "districtCodeMap":
            {
                "510112": "510112",
                "320602": "320613",
                "442001": "44200014",
                "441901": "4419002",
                "330104": "330102",
                "421023": "421088",
                "320684": "320614",
                "652101": "650402",
                "542301": "540202",
                "460401": "460400",
                "430521": "430582",
                "620201": "620200",
                "331021": "331083",
                "230702": "230700",
                "320611": "320613",
                "341822": "341882",
                "320829": "320813",
                "652201": "650500",
                "350402": "350421",
                "542121": "540300",
                "371202": "370116",
                "140402": "140723",
                "310230": "310151"
            },
        "cityCodeMap": {
            "659000": "659001",
            "652100": "650400",
            "542300": "540200",
            "419000": "419001",
            "652200": "650500",
            "469000": "469023",
            "429000": "429005",
            "371200": "370100",
            "542400": "540600"
        },
        "uploadAttachmentMap":
            {
                "1": "IDRXM",
                "2": "IDGHM",
                "29": "FACE_LIVE"
            },
        "previewContractTypes":
            [
                "JKHT"
            ],
        "signContractTypes":
            [
                "JKHT"
            ],
        "downloadContractMap":
            {
                "28": "JKHT"
            },
        "cityCodeMap": {
        },  # 可以不配
        "provinceCodeMap": {},  # 可以不配
        "districtCodeMap":
            {
                "110101": "110118",
                "123456": "659001"
            },
        "transferName": "enc_04_2693365926816388096_659",
        "transferAccount": "enc_03_3323854946851883008_894",
        "transferIdentity": "enc_01_2665895771173817344_479",
        "transferBankCode": "CMBC",
        "withdrawSubjectKey": "trqjj_withdraw",
        "transferSubjectKey": "trqjj_transfer"
    }

    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_tongrongqianjingjing_const", body)
