import common.global_const as gc
import biztest.config.global_gbiz.global_gbiz_common_config as global_gbiz_common_config
from biztest.function.global_gbiz.gbiz_global_common_function import get_payment_account_config, get_channle_apr_rule


def update_gbiz_payment_config(mock_url=None, min_balance_amount=20000, skip_balance_query=False):
    city = gc.COUNTRY
    if mock_url:
        base_url = mock_url
    else:
        base_url = "http://biz-payment-test%s:8901" % gc.ENV
    paysvr_subject = get_payment_account_config(city, min_balance_amount, skip_balance_query)
    content = {
        "payment_env": "overseas",
        "paysvr_system": {
            "paysvr": {
                "system_type": "paysvr",
                "url": base_url,
                "callback_url": "http://biz-grant%s-svc/payment/callback" % gc.ENV,
                "sign": {
                    "name": "gbiz",
                    "merchant_md5": "cb4920d69092c4b536d243f4c3a5f174"
                }
            }
        },
        "paysvr_subject": paysvr_subject,
        "task_config": {
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
                                "code": "1",
                                "messages": [
                                    "风险交易: 疑似重复放款"
                                ]
                            }
                        ]
                    }
                ]
            },
            "PaymentWithdrawQuery": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0-E20000",
                                "messages": [
                                    "Success",
                                    "complete",
                                    "OK",
                                    "SUCCESS",
                                    "Details of transfer with transferId a927a2ecfdc64601bc76c1ede05f37a1",
                                    "Transfer completed successfully"
                                ]
                            },
                            {
                                "code": "0-SUCCESS",
                                "messages": [
                                    "Success",
                                    "OK",
                                    "Details of transfer with transferId a927a2ecfdc64601bc76c1ede05f37a1"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "syncPaymentWithdrawCode"
                        },
                        "matches": [
                            {
                                "code": "2-E1000",
                                "messages": [
                                    "测试线下支付放款中，当作成功处理"
                                ]
                            },
                            {
                                "code": "2-KN_GENERATE_OFFLINE_CODE",
                                "messages": [
                                    "KN_GENERATE_OFFLINE_CODE"
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
                                "code": "2-.*"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retryPayment",
                            "max_times": 2,
                            "max_elapsed_hours": 24,
                            "next_run_at": "delayMinutes(120)"
                        },
                        "matches": [
                            {
                                "code": "1-E20001",
                                "messages": [
                                    "Your account does not have enough balance to carry out the payout operation.",
                                    "BENEFICIARY_BANK_NODE_OFFLINE",
                                    "NPCI or Beneficiary bank systems are offline. Reinitiate transfer after 30 min.",
                                    "NPCI or Beneficiary bank systems are offline. Reinitiate transfer after 30 min",
                                    "Payout failed. Reinitiate transfer after 30 min.",
                                    "transferId is invalid or does not exist",
                                    "Beneficiary Account is Frozen. Please contact beneficiary bank.",
                                    "Beneficiary Account is Closed. Please contact beneficiary bank.",
                                    "Invalid beneficiary details.",
                                    "IMPS is not enabled on Beneficiary Account",
                                    "Payout failed. Contact support for help",
                                    "FAILED",
                                    "Transaction Amount greater than the limit supported by the beneficiary bank."
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retryPayment",
                            "max_times": 2,
                            "max_elapsed_hours": 24,
                            "next_run_at": "delayMinutes(60)"
                        },
                        "matches": [
                            {
                                "code": "1-rejected",
                                "messages": [
                                    "create contact failed",
                                    "ANY_OTHER_REASON",
                                    "Payout failed. Reinitiate transfer after 30 min.",
                                    "ACCOUNT_DOES_NOT_EXIST",
                                    "Please provide a valid Bank IFSC code."
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail",
                            "circuit_break_name": "Payment_WITHDRAW_FAILED_Circuit_Break"
                        },
                        "matches": [
                            {
                                "code": "1-KN_RISK_CONTROL",
                                "messages": [
                                    "Transaction not permitted to beneficiary account.",
                                    "风控拦截，超过交易次数",
                                    "冲正资产，人工处理成失败",
                                    "已超过最大允许失败次数",
                                    "Risk control intercepts, exceeding the number of trades",
                                    "Invalid beneficiary account number",
                                    "Risk control intercepts and exceeds trading limits",
                                    "处理成功"
                                ]
                            },
                            {
                                "code": "1-KN_INVALID_ACCOUNT",
                                "messages": [
                                    "Transaction not permitted to beneficiary account.",
                                    "风控拦截，超过交易次数",
                                    "冲正资产，人工处理成失败",
                                    "已超过最大允许失败次数",
                                    "Risk control intercepts, exceeding the number of trades",
                                    "Invalid beneficiary account number",
                                    "Risk control intercepts and exceeds trading limits",
                                    "处理成功",
                                    "Invalid account, please check it"
                                ]
                            },
                            {
                                "code": "1-KN_ACCOUNT_BALANCE_LIMIT_EXCEEDED",
                                "messages": [
                                    "Wallet balance limit exceeded"
                                ]
                            },
                            {
                                "code": "1-E20010",
                                "messages": [
                                    "Order closed"
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
                                "code": "3",
                                "messages": [
                                    "交易不存在"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_payment_config", content, group="KV")


def update_gbiz_capital_channel(channel, over_time_seconds=172800):
    city = gc.COUNTRY
    rule = get_channle_apr_rule(city, channel)
    content = {
        "channel_account_mapping": {
            "withdraw_account": channel + "_withdraw"
        },
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "LoanApplyQuery",
            "LoanApplyConfirm",
            "ChangeCapital"
        ],
        # "task_config_map": {
        #     "ChangeCapital": {
        #         "execute": {
        #             "event_handler_map": {
        #                 "GrantFailedEvent": "LoanConfirmQuery",
        #                 "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
        #                 "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
        #                 "LoanApplySyncFailedEvent": "LoanApplyQuery"
        #             },
        #             "can_change_capital": True
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0",
        #                         "messages": [
        #                             "成功"
        #                         ]
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "finalFail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "12",
        #                         "messages": []
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1",
        #                         "messages": [
        #                             "遇到再进行配置"
        #                         ]
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "retry"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "-10000",
        #                         "messages": []
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "AssetImport": {
        #         "execute": {
        #             "loan_validator": [
        #                 {
        #                     "rule": rule,
        #                     "err_msg": "资产还款总额不为apr36"
        #                 }
        #             ]
        #         }
        #     },
        #     "LoanApplyNew": {
        #         "init": {
        #             "delay_time": "delaySeconds(5)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyQuery": {
        #         "init": {
        #             "delay_time": "delaySeconds(5)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "retry"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyConfirm": {
        #         "init": {
        #             "delay_time": "delaySeconds(5)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanConfirmQuery": {
        #         "init": {
        #             "delay_time": "delaySeconds(5)"
        #         },
        #         "execute": {
        #             "allow_update_card": "false"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "updateCard"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1",
        #                         "messages": [
        #                             "\\[E20001\\]Wallet balance limit exceeded",
        #                             "\\[E20001\\]Target Account is not registered",
        #                             "\\[E20001\\]Target Wallet is not registered",
        #                             "\\[KN_INVALID_ACCOUNT\\]Invalid account, please check it",
        #                             "\\[KN_ACCOUNT_BALANCE_LIMIT_EXCEEDED\\]Wallet balance limit exceeded"
        #                         ]
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1",
        #                         "messages": [
        #                             "\\[G00022\\]超过最大失败次数.*",
        #                             "\\[G00023\\]超过最大代付时长.*",
        #                             "\\[E20001\\]InquirySuccess",
        #                             "\\[E20010\\]KN_TIMEOUT_CLOSE_ORDER",
        #                             "\\[E20010\\]KN_GENERATE_OFFLINE_CODE",
        #                             "\\[E20010\\]Success",
        #                             "\\[E20010\\]inquiry success",
        #                             "\\[E20010\\]Order closed",
        #                             "\\[KN_RISK_CONTROL\\]Risk control intercepts and exceeds trading limits",
        #                             "\\[rejected Payout\\]failed. Reinitiate transfer after 30 min.",
        #                             "\\[KN_INVALID_ACCOUNT\\]Risk control intercepts and exceeds trading limits",
        #                             "\\[rejected\\]Payout failed. Reinitiate transfer after 30 min."
        #                         ]
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "retry"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "CapitalRepayPlanGenerate": {}
        # },
        "workflow": {
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
                                    "rule": rule,
                                    "err_msg": "[资产还款总额]不满足apr36，请关注！"
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
                            "cancelable": True,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(5)"
                        },
                        "execute": {

                        },
                        "finish": [
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
                            },
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
                                "GrantFailedEvent": "LoanConfirmQuery",
                                "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                                "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                                "LoanApplySyncFailedEvent": "LoanApplyQuery"
                            }
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
                                            "海外不允许切资方，可以不用配",
                                            "成功"
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
                                            "海外没有该场景，可以不用配"
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
                            "delayTime": "delaySeconds(5)"
                        },
                        "execute": {

                        },
                        "finish": [
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
                            },
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
                                    "policy": "retry",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "2",
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
                    "events": [

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
                    "id": "LoanApplyConfirm",
                    "type": "LoanApplyConfirmTaskHandler",
                    "events": [
                        "ConfirmApplySyncSucceededEvent",
                        "ConfirmApplySyncFailedEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(5)"
                        },
                        "execute": {

                        },
                        "finish": [
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
                            },
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
                            "delayTime": "delaySeconds(5)"
                        },
                        "execute": {
                        },
                        "finish": [
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
                                            "\\[E20001\\]InquirySuccess",
                                            "\\[E20010\\]KN_TIMEOUT_CLOSE_ORDER",
                                            "\\[E20010\\]KN_GENERATE_OFFLINE_CODE",
                                            "\\[E20010\\]Success",
                                            "\\[E20010\\]inquiry success",
                                            "\\[E20010\\]Order closed",
                                            "\\[KN_RISK_CONTROL\\]Risk control intercepts and exceeds trading limits",
                                            "\\[rejected Payout\\]failed. Reinitiate transfer after 30 min.",
                                            "\\[KN_INVALID_ACCOUNT\\]Risk control intercepts and exceeds trading limits",
                                            "\\[rejected\\]Payout failed. Reinitiate transfer after 30 min."
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
                                            "\\[E20001\\]Wallet balance limit exceeded",
                                            "\\[E20001\\]Target Account is not registered",
                                            "\\[E20001\\]Target Wallet is not registered",
                                            "\\[KN_INVALID_ACCOUNT\\]Invalid account, please check it",
                                            "\\[KN_ACCOUNT_BALANCE_LIMIT_EXCEEDED\\]Wallet balance limit exceeded"
                                        ]
                                    }
                                ]
                            },
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
                                    "policy": "retry",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "2",
                                        "messages": None
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
                    "id": "UpdateCardMsgSender",
                    "type": "UpdateCardMsgSender",
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
                            "update_card_over_time_seconds": over_time_seconds
                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "CapitalAssetReverse",
                    "type": "CapitalAssetReverseTaskHandler",
                    "events": [
                        "AssetReverseSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "manual",
                            "cancelable": False
                        },
                        "execute": {}
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
                        "event": "UpdateCardNotifyEvent"
                    },
                    "nodes": [
                        "AssetConfirmOverTimeCheck"
                    ],
                    "associateData": {
                        "canRetry": True,
                        "assetConfirmType": "WITHDRAW_FINAL_FAIL_UPDATE_CARD",
                        "overTimeInterval": over_time_seconds
                    }
                },
                {
                    "listen": {
                        "event": "UpdateCardNotifyEvent"
                    },
                    "nodes": [
                        "UpdateCardMsgSender"
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
                        "event": "GrantSucceededEvent",
                        "matches": [

                        ]
                    },
                    "nodes": [
                        "CapitalRepayPlanGenerate"
                    ]
                }
            ]
        }

    }
    gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_" + channel, content, group="KV")


def update_gbiz_capital_channel_user_cancel(channel):
    city = gc.COUNTRY
    rule = get_channle_apr_rule(city, channel)
    content = {
        "channel_account_mapping": {
            "withdraw_account": channel + "_withdraw"
        },
        "cancelable_task_list": [
            "ApplyCanLoan",
            "ChangeCapital"
        ],
        # "task_config_map": {
        #     "ChangeCapital": {
        #         "execute": {
        #             "event_handler_map": {
        #                 "GrantFailedEvent": "LoanConfirmQuery",
        #                 "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
        #                 "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
        #                 "LoanApplySyncFailedEvent": "LoanApplyQuery"
        #             },
        #             "can_change_capital": True
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0",
        #                         "messages": [
        #                             "成功"
        #                         ]
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "finalFail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "12",
        #                         "messages": []
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1",
        #                         "messages": [
        #                             "遇到再进行配置"
        #                         ]
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "retry"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "-10000",
        #                         "messages": []
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "AssetImport": {
        #         "execute": {
        #             "loan_validator": [
        #                 {
        #                     "rule": rule,
        #                     "err_msg": "资产还款总额不为apr36"
        #                 }
        #             ]
        #         }
        #     },
        #     "LoanApplyNew": {
        #         "init": {
        #             "delay_time": "delaySeconds(5)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyQuery": {
        #         "init": {
        #             "delay_time": "delaySeconds(5)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "retry"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2"
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # },
        "workflow": {
            "inclusions": [
                "gbiz_capital_workflow_asset"
            ],
            "nodes": [
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
                                    "rule": rule,
                                    "err_msg": "[资产还款总额]不满足apr36，请关注！"
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
                            "cancelable": True,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(5)"
                        },
                        "execute": {

                        },
                        "finish": [
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
                            },
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
                                "GrantFailedEvent": "LoanConfirmQuery",
                                "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                                "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                                "LoanApplySyncFailedEvent": "LoanApplyQuery"
                            }
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
                                            "海外不允许切资方，可以不用配"
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
                                            "海外没有该场景，可以不用配"
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
                            "delayTime": "delaySeconds(5)"
                        },
                        "execute": {

                        },
                        "finish": [
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
                            },
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
                                    "policy": "retry",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "2",
                                        "messages": None
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
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(5)"
                        },
                        "execute": {

                        },
                        "finish": [
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
                            },
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
                            "delayTime": "delaySeconds(5)"
                        },
                        "execute": {
                        },
                        "finish": [
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
                                            "\\[E20001\\]InquirySuccess",
                                            "\\[E20010\\]KN_TIMEOUT_CLOSE_ORDER",
                                            "\\[E20010\\]KN_GENERATE_OFFLINE_CODE",
                                            "\\[E20010\\]Success",
                                            "\\[E20010\\]inquiry success",
                                            "\\[E20010\\]Order closed",
                                            "\\[KN_RISK_CONTROL\\]Risk control intercepts and exceeds trading limits",
                                            "\\[rejected Payout\\]failed. Reinitiate transfer after 30 min.",
                                            "\\[KN_INVALID_ACCOUNT\\]Risk control intercepts and exceeds trading limits",
                                            "\\[rejected\\]Payout failed. Reinitiate transfer after 30 min."
                                        ]
                                    }
                                ]
                            },
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
                                    "policy": "retry",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "2",
                                        "messages": None
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
                        "event": "GrantSucceededEvent",
                        "matches": [

                        ]
                    },
                    "nodes": [
                        "CapitalRepayPlanGenerate"
                    ]
                }
            ]
        }
    }
    gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_" + channel, content, group="KV")


def update_grouter_channel_change_config():
    content = {
        "allowed_channel_list": [
            "tha_picocapital",
            "tha_bankcard",
            "tha_amberstar",
            "pico_qr",
            "picocp_ams1",
            "pico_bangkok",
            "picocp_ams1",
            "picoqr_ams1",
            "picocp_ams2",
            "picoqr_ams2"
        ],
        "against_channel_map": {
            "picocp_ams1": [
                "tha_bankcard",
                "tha_picocapital",
                "tha_amberstar",
                "pico_qr",
                "pico_bang",
                "pico_nonth",
                "pico_sp",
                "pico_path",
                "pico_gem",
                "pico_planet",
                "pico_moon",
                "pico_bangkok",
                "picocp_ams1",
                # "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ],
            "pico_qr": [
                "tha_bankcard",
                "tha_picocapital",
                "picocp_ams1",
                "tha_amberstar",
                "pico_bang",
                "pico_nonth",
                "pico_sp",
                "pico_path",
                "pico_gem",
                "pico_planet",
                "pico_moon",
                "pico_bangkok",
                "picocp_ams1",
                "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ],
            "pico_bang": [
                "picocp_ams1",
                "pico_qr",
                "pico_nonth",
                "pico_sp",
                "pico_path",
                "pico_gem",
                "pico_planet",
                "pico_moon",
                "pico_bangkok",
                "picocp_ams1",
                "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ],
            "pico_nonth": [
                "picocp_ams1",
                "pico_qr",
                "pico_bang",
                "pico_sp",
                "pico_path",
                "pico_gem",
                "pico_planet",
                "pico_moon",
                "pico_bangkok",
                "picocp_ams1",
                "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ],
            "pico_sp": [
                "picocp_ams1",
                "pico_qr",
                "pico_bang",
                "pico_nonth",
                "pico_path",
                "pico_gem",
                "pico_planet",
                "pico_moon",
                "pico_bangkok",
                "picocp_ams1",
                "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ],
            "pico_path": [
                "picocp_ams1",
                "pico_qr",
                "pico_bang",
                "pico_nonth",
                "pico_sp",
                "pico_gem",
                "pico_planet",
                "pico_moon",
                "pico_bangkok",
                "picocp_ams1",
                "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ],
            "pico_gem": [
                "picocp_ams1",
                "pico_qr",
                "pico_bang",
                "pico_nonth",
                "pico_path",
                "pico_sp",
                "pico_planet",
                "pico_moon",
                "pico_bangkok",
                "picocp_ams1",
                "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ],
            "pico_planet": [
                "picocp_ams1",
                "pico_qr",
                "pico_bang",
                "pico_nonth",
                "pico_path",
                "pico_sp",
                "pico_gem",
                "pico_moon",
                "pico_bangkok",
                "picocp_ams1",
                "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ],
            "pico_moon": [
                "picocp_ams1",
                "pico_qr",
                "pico_bang",
                "pico_nonth",
                "pico_path",
                "pico_sp",
                "pico_gem",
                "pico_planet",
                "pico_bangkok",
                "picocp_ams1",
                "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ],
            "pico_bangkok": [
                "picocp_ams1",
                "pico_qr",
                "pico_bang",
                "pico_nonth",
                "pico_path",
                "pico_sp",
                "pico_gem",
                "pico_planet",
                "pico_moon",
                "picocp_ams1",
                "picoqr_ams1",
                "picocp_ams2",
                "picoqr_ams2"
            ]
        },
        "forbid_channel_config": {
            "max_elapsed_hours": "24",
            "channels": [
                ""
            ]
        }
    }

    gc.NACOS.update_configs("grouter%s" % gc.ENV, "grouter_channel_change_config", content, group="KV")


def incremental_update_config(tenant, data_id, **kwargs):
    tenant = tenant + gc.ENV
    group = "KV"
    gc.NACOS.incremental_update_config(tenant, data_id, group, **kwargs)


def update_grouter_channel_route_config(**kwargs):
    content = {
        "allowed_channel_list": []
    }
    for channel in {x.get('channel') for x in global_gbiz_common_config.capital_plan[gc.COUNTRY]}:
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


def update_gbiz_circuit_break_config(count=100):
    body = [
        {
            "name": "Payment_FINAL_FAILED_Circuit_Break",
            "data": {
                "errCount": {
                    "type": "spel",
                    "script": "#cache.getFromCache(#breakName)"
                }
            },
            "trigger": {
                "type": "realtime",
                "rule": "#errCount >= " + str(count)
            },
            "actions": [
                {
                    "type": "alert",
                    "interval": 60,
                    "receiver": [
                        "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                    ],
                    "content": "【海外test-代付最终失败熔断】Payment_FINAL_FAILED，错误数：#{#errCount}，自动挂起ApplyCanLoan、PaymentWithdraw、PaymentWithdrawQuery、ChangeCapital，请关注并处理！"
                },
                {
                    "type": "suspendTask",
                    "rule": "contains(task.type, {'ApplyCanLoan', 'PaymentWithdraw', 'PaymentWithdrawQuery', 'ChangeCapital'})"
                }
            ],
            "recovery": {
                "type": "manual"
            }
        },
        {
            "name": "Payment_Service_Exception_Circuit_Break",
            "data": {
                "errCount": {
                    "type": "sql",
                    "script": "select count(1) as cnt from task where task_status = 'open' and task_type = 'PaymentWithdraw' and task_memo like '%可用金额[10]小于本次代付金额%'"
                }
            },
            "trigger": {
                "type": "realtime",
                "rule": "#errCount.cnt >= " + str(count)
            },
            "actions": [
                {
                    "type": "alert",
                    "interval": 60,
                    "receiver": [
                        "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                    ],
                    "content": "【海外test-代付熔断】Payment_Service_Exception，错误数：#{#errCount.cnt}，自动挂起ApplyCanLoan、PaymentWithdraw，请关注并处理！"
                },
                {
                    "type": "suspendTask",
                    "rule": "contains(task.type, {'ApplyCanLoan', 'PaymentWithdraw'})"
                }
            ],
            "recovery": {
                "type": "manual"
            }
        },
        {
            "name": "Manual_Job_Autorun_Circuit_Break",
            "data": {
                "errCount": {
                    "type": "spel",
                    "script": "#cache.getFromCache(#breakName)"
                }
            },
            "trigger": {
                "type": "realtime",
                "rule": "#errCount >= " + str(count)
            },
            "actions": [
                {
                    "type": "alert",
                    "interval": 60,
                    "receiver": [
                        "https://tv-service-alert.kuainiu.io/alert?botId=0cd5bf44-90b7-4a78-8f54-a903fdae0111"
                    ],
                    "content": "【海外test-手动任务熔断触发】Manual_Job_Autorun_Circuit_Break,错误数：#{#errCount}，自动挂起AssetVoid。请关注并处理！"
                },
                {
                    "type": "suspendTask",
                    "rule": "contains(task.type, {'AssetVoid'})"
                }
            ],
            "recovery": {
                "type": "manual"
            }
        }
    ]
    gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_circuit_break_config", body, group="KV")


def update_gbiz_circuit_break_config_v2(succrate=0, errCount=50):
    body = [
        {
            "name": "Payment_WITHDRAW_FAILED_Circuit_Break",
            "data": [
                {
                    "name": "errCount",
                    "type": "spel",
                    "script": "#DataContext.cacheReader.get()"
                },
                {
                    "name": "beginTime",
                    "type": "spel",
                    "script": "T(DateUtil).format(T(DateUtil).addMinutes(-30))"
                },
                {
                    "name": "endTime",
                    "type": "spel",
                    "script": "T(DateUtil).format(T(DateUtil).now())"
                },
                {
                    "name": "succRate",
                    "type": "sql",
                    "script": "select IFNULL(count(IF(withdraw_record_status='success', 1, null))*100/count(1), 0) val, count(1) totalCount from withdraw_record where withdraw_record_apply_at between '#{#DataContext.data.beginTime}' and '#{#DataContext.data.endTime}' and withdraw_record_status in ('success','fail')"
                }
            ],
            "trigger": {
                "type": "realtime",
                "rule": "#DataContext.data.succRate.totalCount >= 1 and #DataContext.data.succRate.val < " + str(
                    succrate)
            },
            "actions": [
                {
                    "type": "AlertAction",
                    "execMode": "ByBreakerFired",
                    "execParams": {
                        "interval": 300,
                        "receiver": [
                            "https://tv-service-alert.kuainiu.chat/alert?botId=78ca6a7b-c1ed-450f-8a8d-2505f6e77e331"
                        ],
                        "template": "【泰国-代付熔断】Payment_WITHDRAW_FAILED_Circuit_Break，当日总失败数：#{#DataContext.data.errCount}，代付成功率(#{#DataContext.data.beginTime}至#{#DataContext.data.endTime})：#{#DataContext.data.succRate.val}%低于90%，该时段内相关代付失败资产会被刷入熔断事件表，且PaymentWithdrawNew、PaymentWithdraw、ChangeCapital、AssetVoid会被挂起直至手动解除熔断，其他资产的PaymentWithdraw在熔断发生后1小时内将被限流(10s/个)，请重点关注处理！"
                    }
                },
                {
                    "type": "FlushBreakEventsAction",
                    "execMode": "ByBreakerFired",
                    "memo": "以下data中圈定的数据将计入熔断事件表，熔断重复触发时，不重复记录",
                    "execParams": {
                        "data": {
                            "type": "sql",
                            "script": "select DISTINCT SUBSTRING(withdraw_order_asset_item_no, 1, CHAR_LENGTH(withdraw_order_asset_item_no)-1) orderNo from withdraw_record left join withdraw_order on withdraw_order_no=withdraw_record_order_no where withdraw_record_apply_at between '#{#DataContext.data.beginTime}' and '#{#DataContext.data.endTime}' and withdraw_record_status in ('fail')"
                        }
                    }
                },
                {
                    "type": "SuspendTaskAction",
                    "execMode": "ByAsyncTask",
                    "memo": "命中熔断事件表的任务将被阻断(挂起)，可以手动关闭某条熔断事件，或关闭熔断记录",
                    "execParams": {
                        "rule": "{'PaymentWithdrawNew', 'PaymentWithdrawQuery','PaymentWithdraw','ChangeCapital', 'AssetVoid'}.contains(#DataContext.task.type) and #DataContext.breakEvents.contains(#DataContext.requestData.assetItemNo)"
                    }
                },
                {
                    "type": "RateLimitTaskAction",
                    "execMode": "ByAsyncTask",
                    "memo": "熔断1个小时内的task会被限流",
                    "execParams": {
                        "ttlSeconds": 10,
                        "rule": "{'PaymentWithdraw'}.contains(#DataContext.task.type) and T(DateUtil).addMinutes(-60).before(T(DateUtil).parseDate(#DataContext.data.endTime))"
                    }
                }
            ],
            "recovery": {
                "type": "manual"
            }
        },
        {
            "name": "ASSET_VOID_Circuit_Break",
            "data": [
                {
                    "name": "errCount",
                    "type": "spel",
                    "script": "#DataContext.cacheReader.get()"
                },
                {
                    "name": "succRate",
                    "type": "sql",
                    "script": "select IFNULL(count(IF(asset_status = 'repay', 1, null)) * 100 / count(1), 0) val, count(1) totalCount from asset where asset_create_at between date_sub(now(), interval 24 hour) and now() and asset_status in ('repay', 'void') and asset_loan_channel !='noloan'"
                }
            ],
            "trigger": {
                "type": "realtime",
                "rule": "#DataContext.data.succRate.totalCount >= 0 and #DataContext.data.succRate.val < " + str(
                    succrate)
            },
            "actions": [
                {
                    "type": "AlertAction",
                    "execMode": "ByBreakerFired",
                    "execParams": {
                        "interval": 60,
                        "receiver": [
                            "https://tv-service-alert.kuainiu.chat/alert?botId=78ca6a7b-c1ed-450f-8a8d-2505f6e77e331"
                        ],
                        "template": "【泰国-资产作废熔断】ASET_VOID_Circuit_Break，放款成功率：#{#DataContext.data.succRate.val}%低于90%，自动挂起所有资产的ChangeCapital、AssetVoid任务，请重点关注处理！成功率回升后，该熔断会自动解除！"
                    }
                },
                {
                    "type": "SuspendTaskAction",
                    "execMode": "ByAsyncTask",
                    "execParams": {
                        "rule": "{'ChangeCapital', 'AssetVoid'}.contains(#DataContext.task.type)"
                    }
                }
            ],
            "recovery": {
                "type": "AutoClose"
            }
        },
        {
            "name": "Payment_Service_Exception_Circuit_Break",
            "data": [
                {
                    "name": "errCount",
                    "type": "sql",
                    "script": "select count(1) as cnt from task where task_status = 'open' and task_type in ('PaymentWithdraw','PaymentWithdrawQuery') and task_memo like '%Read timed out executing POST%'"
                }
            ],
            "trigger": {
                "type": "realtime",
                "rule": "#DataContext.data.errCount.cnt >= " + str(errCount)
            },
            "actions": [
                {
                    "type": "AlertAction",
                    "execMode": "ByBreakerFired",
                    "execParams": {
                        "interval": 60,
                        "receiver": [
                            "https://tv-service-alert.kuainiu.chat/alert?botId=78ca6a7b-c1ed-450f-8a8d-2505f6e77e331"
                        ],
                        "template": "【代付熔断】Payment_Service_Exception，错误数：#{#DataContext.data.errCount.cnt}，自动挂起ApplyCanLoan、PaymentWithdraw，请关注并处理！"
                    }
                },
                {
                    "type": "SuspendTaskAction",
                    "execMode": "ByAsyncTask",
                    "execParams": {
                        "rule": "{'ApplyCanLoan','PaymentWithdraw','PaymentWithdrawQuery'}.contains(#DataContext.task.type)"
                    }
                }
            ],
            "recovery": {
                "type": "manual"
            }
        }
    ]
    gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_circuit_break_config_v2", body, group="KV")


def update_gbiz_manual_task_auto_process_config(channel):
    content = {
        "ChangeCapital": {
            channel: [
                {
                    "action": {
                        "policy": "autoCancel",
                        "next_run_at": "delayDays(1,\"04:00:00\")"
                    },
                    "matches": [
                        {
                            "code": "1",
                            "messages": [
                                "\\[G00022\\]超过最大失败次数.*",
                                "\\[KN_INVALID_ACCOUNT\\]Risk control intercepts and exceeds trading limits"
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
                            "code": "4",
                            "messages": [
                                channel + "->校验资金量失败;"
                            ]
                        }
                    ]
                }
            ]
        },
        "AssetVoid": {
            channel: [
                {
                    "action": {
                        "policy": "autoRollBackToChangeCapital",
                        "next_run_at": "delayMinutes(240)",
                        "circuit_break_name": "ASSET_VOID_Circuit_Break"
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
        "CapitalAssetReverse": {
        },
        "BlacklistCollect": {
        }
    }
    gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_manual_task_auto_process_config", content, group="KV")


def update_pak_gbiz_payment_config(mock_url=None, min_balance_amount=20000, skip_balance_query=False):
    if mock_url:
        base_url = mock_url
    else:
        base_url = "http://biz-payment-test%s:8901" % gc.ENV
    body = {
        "payment_env": "overseas",
        "paysvr_system": {
            "paysvr": {
                "system_type": "paysvr",
                "url": base_url,
                "callback_url": "http://biz-grant%s-svc/payment/callback" % gc.ENV,
                "sign": {
                    "name": "gbiz",
                    "merchant_md5": "cb4920d69092c4b536d243f4c3a5f174"
                }
            }
        },
        "paysvr_subject": {
            "qiss_withdraw": {
                "name": "qiss",
                "paysvr_system": "paysvr",
                "account": "test",
                "warn_amount": min_balance_amount,
                "skip_balance_query": skip_balance_query
            },
            "goldlion_withdraw": {
                "name": "goldlion",
                "paysvr_system": "paysvr",
                "account": "test",
                "warn_amount": min_balance_amount,
                "skip_balance_query": skip_balance_query
            }
        },
        "task_config": {
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
                                "code": "2"
                            },
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
                                "code": "1000",
                                "messages": [
                                    ".*可用余额.*已小于预警值.*",
                                    ".*可用金额.*小于本次代付金额.*"
                                ]
                            }
                        ]
                    }
                ]
            },
            "PaymentWithdrawQuery": {
                # 支付返回线上/线下的code/msg 一样，我们根据withdraw_type来判断是否为线下，线下则生成取款码通知msg
                "finish": [
                    {
                        "action": {
                            "policy": "successAndSyncWithdrawCode"
                        },
                        "matches": [
                            {
                                "code": "0-E20000",
                                "messages": [
                                    "Success",
                                    "complete",
                                    "OK",
                                    "SUCCESS",
                                    "Details of transfer with transferId a927a2ecfdc64601bc76c1ede05f37a1",
                                    "Transfer completed successfully"
                                ]
                            },
                            {
                                "code": "0-SUCCESS",
                                "messages": [
                                    "Success",
                                    "OK",
                                    "Details of transfer with transferId a927a2ecfdc64601bc76c1ede05f37a1"
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
                                "code": "2-.*"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retryPayment",
                            "max_times": 2,
                            "max_elapsed_hours": 24,
                            "next_run_at": "delayMinutes(120)"
                        },
                        "matches": [
                            {
                                "code": "1-E20001",
                                "messages": [
                                    "遇到再配置"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "retryPayment",
                            "max_times": 2,
                            "max_elapsed_hours": 24,
                            "next_run_at": "delayMinutes(60)"
                        },
                        "matches": [
                            {
                                "code": "1-rejected",
                                "messages": [
                                    "遇到再配置"
                                ]
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail",
                            "circuit_break_name": "Payment_FINAL_FAILED_Circuit_Break"
                        },
                        "matches": [
                            {
                                "code": "1-KN_RISK_CONTROL",
                                "messages": [
                                    "遇到再配置"
                                ]
                            },
                            {
                                "code": "1-KN_INVALID_ACCOUNT",
                                "messages": [
                                    "Risk control intercepts and exceeds trading limits",
                                    "Invalid account, please check it"
                                ]
                            },
                            {
                                "code": "1-KN_ACCOUNT_BALANCE_LIMIT_EXCEEDED",
                                "messages": [
                                    "遇到再配置"
                                ]
                            },
                            {
                                "code": "1-rejected",
                                "messages": [
                                    "Payout failed. Reinitiate transfer after 30 min."
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
                                "code": "3",
                                "messages": [
                                    "交易不存在"
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    }
    gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_payment_config", body, group="KV")


if __name__ == "__main__":
    # 环境更新
    gc.init_env(1, "india", "dev")
    update_gbiz_payment_config()
    # update_gbiz_capital_nbfc_f6_new()
    # #
    # # gc.init_env(1, "philippines", "dev")
    # # update_gbiz_payment_config()
    # # update_gbiz_capital_copper_stone()
    # # update_gbiz_capital_u_peso()
    # #
    # # gc.init_env(1, "mexico", "dev")
    # # update_gbiz_payment_config()
    # # update_gbiz_capital_mangguo()
    # #
    # # gc.init_env(1, "thailand", "dev")
    # # update_gbiz_payment_config()
    # # # update_gbiz_capital_picocp_ams1()
    # # update_gbiz_capital_pico_qr()
    # #
    # # gc.init_env(1, "pakistan", "dev")
    # # update_gbiz_payment_config()
    # # update_gbiz_capital_nbmfc()
