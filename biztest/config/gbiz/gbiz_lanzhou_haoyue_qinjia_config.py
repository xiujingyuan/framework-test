import common.global_const as gc


def update_gbiz_capital_lanzhou_haoyue_qinjia():
    lanzhou_haoyue_qinjia = {
        "manual_reverse_allowed": False,
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "LoanPostApply",
            "ChangeCapital"
        ],
        "raise_limit_allowed": False,
        "register_config": {
            "register_step_list": [
                {
                    "channel": "lanzhou_haoyue_qinjia",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "qjhy",
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "status_scene": {
                        "register": {
                            "success_type": "once",
                            "allow_fail": False,
                            "need_confirm_result": True
                        },
                        "route": {
                            "success_type": "once",
                            "allow_fail": False
                        },
                        "validate": {
                            "success_type": "once"
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
        # "task_config_map": {
        #     "ChangeCapital": {
        #         "execute": {
        #             "event_handler_map": {
        #                 "GrantFailedEvent": "LoanConfirmQuery",
        #                 "LoanApplySyncFailedEvent": "LoanApplyQuery",
        #                 "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
        #                 "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
        #                 "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
        #                 "LoanCreditFailedEvent": "LoanCreditQuery",
        #                 "LoanPostCreditFailedEvent": "LoanConfirmQuery"
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
        #                             "切资方路由\\(二次\\)成功"
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
        #                         "messages": [
        #
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
        #                         "messages": [
        #                             "遇到再进行配置"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "AssetImport": {
        #         "execute": {
        #             "loan_validator": [
        #                 {
        #                     "rule": "#loan.totalAmount>cmdb.irr(#loan,'23.70')&&loan.totalAmount<cmdb.irr(#loan,'24')",
        #                     "err_msg": "兰州昊悦亲家[资产还款总额]不满足【irr23.70，irr24】请关注！"
        #                 }
        #             ]
        #         }
        #     },
        #     "LoanApplyNew": {
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "01-0000-成功-成功"
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
        #                         "code": "1000000",
        #                         "messages": [
        #                             "遇到在配置"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyQuery": {
        #         "finish": [
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
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "待配置"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanPostApply": {
        #         "init": {
        #             "delay_time": "delaySeconds(120)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "01-0000-成功-"
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
        #                         "code": "待配置"
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
        #                             "遇到再配置"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanCreditApply": {
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "00-0000-成功-路由处理中"
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
        #                         "code": "1700013",
        #                         "messages": [
        #                             "--存在处理中申请-"
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
        #                         "code": "待配置"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanCreditQuery": {
        #         "init": {
        #             "delay_time": "delaySeconds(60)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "01-0001-成功-路由成功",
        #                             "01-0001-成功-请求成功"
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
        #                         "code": "1000000",
        #                         "messages": [
        #                             "00-0000-成功-"
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
        #                         "code": "1000000",
        #                         "messages": [
        #                             "02-9999-成功-测试mock"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanPostCredit": {
        #         "init": {
        #             "delay_time": "delaySeconds(60)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "message": "01-0000-成功-"
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "待配置"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyConfirm": {
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "00-0000-成功-"
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
        #                         "code": "待配置"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanConfirmQuery": {
        #         "init": {
        #             "delay_time": "delaySeconds(120)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "01-0001-成功-"
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
        #                         "code": "1000000",
        #                         "messages": [
        #                             "00-0000-成功-"
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
        #                         "code": "1000000",
        #                         "messages": [
        #                             "02-0006-成功-交易处理失败",
        #                             "02-0007-成功-此产品暂不支持当前利率"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "CapitalRepayPlanQuery": {
        #         "execute": {
        #             "allow_diff_effect_at": False,
        #             "allow_diff_due_at": False,
        #             "allowance_check_range": {
        #                 "min_value": -1,
        #                 "max_value": 1
        #             }
        #         }
        #     },
        #     "OurRepayPlanRefine": {
        #         "execute": {
        #             "need_refresh_due_at": False
        #         }
        #     },
        #     "ContractSignature": {
        #         "init": {
        #             "delay_time": "delayMinutes(2)"
        #         }
        #     },
        #     "ContractPush": {
        #         "init": {
        #             "delay_time": "delayMinutes(2)"
        #         }
        #     },
        #     "ContractDown": {
        #         "init": {
        #             "delay_time": "delayDays(2, \"08:00:00\")"
        #         }
        #     },
        #     "AssetAutoImport": {
        #         "init": {
        #             "delay_time": "delayMinutes(120)"
        #         }
        #     },
        #     "CertificateApply": {
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "01-00-成功-处理成功",
        #                             "02-02-成功-提交失败,已存在提交的数据"
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
        #                         "code": "1000000",
        #                         "messages": [
        #                             "02-02-成功-借款未结清"
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
        #                         "code": "1000000",
        #                         "messages": [
        #                             "遇到在配置"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "CertificateDownload": {
        #         "init": {
        #             "delay_time": "delayDays(1, \"09:30:00\")"
        #         }
        #     },
        #     "RongDanIrrTrial": {
        #         "execute": {
        #             "trail_irr_limit": 35.99
        #         }}
        # }
        "workflow": {
            "title": "兰州昊悦亲家流程编排v3",
            "inclusions": [
                "gbiz_capital_workflow_asset"
            ],
            "props": {
                "CapitalRepayPlanProps": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "need_refresh_due_at": False,
                    "allowance_check_range": {
                        "min_value": -49,
                        "max_value": 49
                    }
                }
            },
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
                                    "rule": "#loan.totalAmount>cmdb.irr(#loan,'23.70')&&loan.totalAmount<cmdb.irr(#loan,'24')",
                                    "err_msg": "兰州昊悦亲家[资产还款总额]不满足【irr23.70，irr24】请关注！"
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
                                        "code": "1000000",
                                        "messages": [
                                            "01-0000-成功-成功"
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
                                        "code": "1555555",
                                        "messages": [
                                            "--contactmobile联系人电话长度超限-",
                                            "--tel工作单位电话长度超限-"
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
                                "GrantFailedEvent": "LoanConfirmQuery",
                                "LoanApplySyncFailedEvent": "LoanApplyQuery",
                                "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                                "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                                "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
                                "LoanCreditFailedEvent": "LoanCreditQuery",
                                "LoanPostCreditFailedEvent": "LoanConfirmQuery"
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
                                        "messages": []
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
                                        "code": "1100002",
                                        "messages": [
                                            "客户信息推送-查无此交易"
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
                    "events": [],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(120)"
                        },
                        "execute": {},
                        "finish": []
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
                            "cancelable": True,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(120)"
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
                                        "code": "1000000",
                                        "messages": [
                                            "01-0000-成功-"
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
                                        "code": "待配置",
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
                                            "遇到再配置"
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "LoanCreditApply",
                    "type": "LoanCreditApplyTaskHandler",
                    "events": [
                        "LoanCreditApplySyncSucceededEvent",
                        "LoanCreditApplySyncFailedEvent"
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
                                        "code": "1000000",
                                        "messages": [
                                            "00-0000-成功-路由处理中"
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
                                        "code": "1700013",
                                        "messages": [
                                            "--存在处理中申请-"
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
                                        "code": "待配置",
                                        "messages": None
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "LoanCreditQuery",
                    "type": "LoanCreditQueryTaskHandler",
                    "events": [
                        "LoanCreditSucceededEvent",
                        "LoanCreditFailedEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(60)"
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
                                        "code": "1000000",
                                        "messages": [
                                            "01-0001-成功-路由成功",
                                            "01-0001-成功-请求成功"

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
                                        "code": "1000000",
                                        "messages": [
                                            "00-0000-成功-"
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
                                        "code": "1000000",
                                        "messages": [
                                            "02-9999-成功-测试mock",
                                            "02-9999-成功-路由失败",
                                            "02-9999-成功-RUTE-系统异常",
                                            "02-0005-成功-银行风控拒绝",
                                            "02-4000-成功-",
                                            "02-9999-成功-人脸识别失败",
                                            "02-9999-成功-甘肃客户信息处理失败",
                                            "02-4000-成功-银行风控拒绝",
                                            "02-0005-成功-该客户针对该业务品种存在有效的额度申请信息，不需要重新申请！"
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "LoanApplyTrial",
                    "type": "LoanApplyTrialTaskHandler",
                    "events": [
                        "LoanApplyTrailSucceededEvent"
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
                    "id": "BlacklistCollect",
                    "type": "BlacklistCollectTaskHandler",
                    "events": [],
                    "activity": {
                        "init": {
                            "executeType": "manual",
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
                                        "code": "1000000",
                                        "messages": [
                                            "00-0000-成功-"
                                        ]
                                    },
                                    {
                                        "code": "1800012",
                                        "messages": [
                                            "--支用流水号重复-"
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
                                        "code": "待配置",
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
                        "GrantFailedEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(120)"
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
                                        "code": "1000000",
                                        "messages": [
                                            "01-0001-成功-"
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
                                        "code": "1000000",
                                        "messages": [
                                            "00-0000-成功-",
                                            "00-0013-成功-"
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
                                        "code": "1000000",
                                        "messages": [
                                            "02-0006-成功-交易处理失败",
                                            "02-0007-成功-此产品暂不支持当前利率",
                                            "02-0006-成功-风控规则拒绝",
                                            "02-0002-成功-支付失败",
                                            "02-0012-成功-当日未推送成功，次日可重新支用",
                                            "02-0006-成功-",
                                            "02-0011-成功-支用申请额度不足"
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "CapitalRepayPlanQuery",
                    "type": "CapitalRepayPlanQueryTaskHandler",
                    "events": [
                        "RepayPlanHandleSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False
                        },
                        "execute": {
                            "props_key": "CapitalRepayPlanProps"
                        },
                        "finish": []
                    }
                },
                {
                    "id": "ContractDown",
                    "type": "ContractDownTaskHandler",
                    "events": [
                        "ContractDownSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(60)"
                        },
                        "execute": {
                            "interval_in_minutes": "240"
                        },
                        "finish": []
                    }
                },
                {
                    "id": "OurRepayPlanRefine",
                    "type": "OurRepayPlanRefineTaskHandler",
                    "events": [
                        "OurRepayPlanRefreshHandleSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False
                        },
                        "execute": {
                            "props_key": "CapitalRepayPlanProps"
                        },
                        "finish": []
                    }
                },
                {
                    "id": "GuaranteeUpload",
                    "type": "GuaranteeUploadTaskHandler",
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
                    "id": "CapitalRepayPlanPush",
                    "type": "CapitalRepayPlanPushTaskHandler",
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
                    "id": "ContractPush",
                    "type": "ContractPushTaskHandler",
                    "events": [],
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
                    "id": "ContractSignature",
                    "type": "ContractSignatureTaskHandler",
                    "events": [],
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
                    "id": "CertificateApplySync",
                    "type": "CertificateApplyVerifySyncTaskHandler",
                    "events": [
                        "CertificateApplyReadyEvent"
                    ],
                    "activity": {
                        "init": {
                        }
                    }
                },
                {
                    "id": "CertificateApply",
                    "type": "CertificateApplyTaskHandler",
                    "events": [
                        "CertificateApplySuccessEvent"
                    ],
                    "activity": {
                        "init": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "1000000",
                                        "messages": [
                                            "01-00-成功-处理成功",
                                            "02-02-成功-提交失败,已存在提交的数据"
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
                                        "code": "1000000",
                                        "messages": [
                                            "02-02-成功-借款未结清",
                                            "02-02-成功-批次号重复,请更换批次号再申请。"
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
                                        "code": "1000000",
                                        "messages": [
                                            "遇到在配置"
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "CertificateDownload",
                    "type": "CertificateDownloadTaskHandler",
                    "events": [],
                    "activity": {
                        "execute": {
                            "interval_in_minutes": "240"
                        },
                        "init": {
                            "delay_time": "delayDays(1, \"09:30:00\")"
                        }
                    }
                }
            ],
            "subscribers": [
                {
                    "memo": "资产导入就绪事件订阅",
                    "listen": {
                        "event": "AssetImportReadyEvent"
                    },
                    "nodes": [
                        "AssetImport"
                    ]
                },
                {
                    "memo": "资产导入成功事件订阅",
                    "listen": {
                        "event": "AssetImportSucceededEvent"
                    },
                    "nodes": [
                        "AssetImportVerify"
                    ]
                },
                {
                    "memo": "资产进件核心参数校验成功事件订阅",
                    "listen": {
                        "event": "AssetImportVerifySucceededEvent"
                    },
                    "nodes": [
                        "ApplyCanLoan"
                    ]
                },
                {
                    "memo": "资产就绪成功事件订阅",
                    "listen": {
                        "event": "AssetReadyEvent"
                    },
                    "nodes": [
                        "LoanApplyNew"
                    ]
                },
                {
                    "memo": "资产就绪失败事件订阅",
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
                    "memo": "资产进件成功事件订阅",
                    "listen": {
                        "event": "LoanApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyQuery"
                    ]
                },
                {
                    "memo": "资产进件失败事件订阅",
                    "listen": {
                        "event": "LoanApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": "LoanApplyQuery",
                        "event": "LoanApplySyncFailedEvent",
                        "skipDoubleCheck": True
                    }
                },
                {
                    "memo": "资产进件查询成功事件订阅",
                    "listen": {
                        "event": "LoanApplyAsyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanPostApply"
                    ]
                },
                {
                    "memo": "资产进件查询失败事件订阅",
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
                    "memo": "资产进件后任务成功事件订阅",
                    "listen": {
                        "event": "LoanPostApplySucceededEvent"
                    },
                    "nodes": [
                        "LoanCreditApply"
                    ],
                    "associateData": {
                        "lockRecordStatus": 3
                    }
                },
                {
                    "memo": "支用申请失败事件订阅",
                    "listen": {
                        "event": "LoanPostApplyFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": None,
                        "event": "LoanPostApplyFailedEvent",
                        "skipDoubleCheck": True
                    }
                },
                {
                    "memo": "授信申请成功事件订阅",
                    "listen": {
                        "event": "LoanCreditApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanCreditQuery"
                    ]
                },
                {
                    "memo": "授信申请失败成功事件订阅",
                    "listen": {
                        "event": "LoanCreditApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": "LoanCreditQuery",
                        "event": "LoanCreditApplySyncFailedEvent",
                        "skipDoubleCheck": False
                    }
                },
                {
                    "memo": "授信查询成功事件订阅",
                    "listen": {
                        "event": "LoanCreditSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyTrial"
                    ],
                    "associateData": {
                        "lockRecordStatus": 3
                    }
                },
                {
                    "memo": "授信查失败事件订阅",
                    "listen": {
                        "event": "LoanCreditFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital",
                        "BlacklistCollect"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": "LoanCreditQuery",
                        "event": "LoanCreditFailedEvent",
                        "skipDoubleCheck": False
                    }
                },
                {
                    "memo": "放款试算成功事件订阅",
                    "listen": {
                        "event": "LoanApplyTrailSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyConfirm"
                    ]
                },
                {
                    "memo": "支用申请成功事件订阅",
                    "listen": {
                        "event": "ConfirmApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanConfirmQuery"
                    ]
                },
                {
                    "memo": "支用查询失败事件订阅",
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
                    "memo": "支用查询成功事件订阅",
                    "listen": {
                        "event": "GrantSucceededEvent"
                    },
                    "nodes": [
                        "CapitalRepayPlanQuery",
                        "ContractDown"
                    ]
                },
                {
                    "memo": "支用查询失败事件订阅",
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
                    "memo": "还款计划查询成功事件订阅",
                    "listen": {
                        "event": "RepayPlanHandleSucceededEvent"
                    },
                    "nodes": [
                        "OurRepayPlanRefine"
                    ]
                },
                {
                    "memo": "合同下载成功事件订阅",
                    "listen": {
                        "event": "ContractDownSucceededEvent"
                    },
                    "nodes": [
                        "GuaranteeUpload"
                    ]
                },
                {
                    "memo": "还款计划刷新成功事件订阅",
                    "listen": {
                        "event": "OurRepayPlanRefreshHandleSucceededEvent"
                    },
                    "nodes": [
                        "CapitalRepayPlanPush",
                        "ContractPush",
                        "ContractSignature"
                    ]
                },
                {
                    "memo": "结清证明准备",
                    "listen": {
                        "event": "CertificateApplyReadyEvent",
                        "matches": []
                    },
                    "nodes": [
                        "CertificateApply"
                    ]
                },
                {
                    "memo": "结清证明申请成功",
                    "listen": {
                        "event": "CertificateApplySuccessEvent",
                        "matches": []
                    },
                    "nodes": [
                        "CertificateDownload"
                    ]
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_haoyue_qinjia", lanzhou_haoyue_qinjia)


def update_gbiz_capital_lanzhou_haoyue_qinjia_const():
    body = {
        "channel": "KN10001",
        "defaultLoanBalance": "0",
        "defaultAmountUseRate": "0",
        "defaultLoanOverdue": "0",
        "defaultMaxOverdueDay": "0",
        "defaultMaxOverdueAmount": "0",
        "defaultOverdueDays": "0",
        "defaultOverdueCount": "0",
        "defaultFistoverdueday": "0",
        "ftpFileMaxSize": 3145728,
        "imageCompressScale": 0.5,
        "imageCompressQuantity": 0.8,
        "responseValidateErrorCode": 9000,
        "idType": "Ind01",
        "customerType": "1",
        "liveStatus": "9",
        "livePostCode": "000000",
        "job": "Y",
        "duty": "9",
        "jobNature": "90",
        "longTermIdValidDate": "2100-12-31",
        "monthIncome": "15000",
        "country": "CHN",
        "jobTitle": "0",
        "faceRecognizeResult": "1",
        "defaultFaceRecognizeScore": "75",
        "notFarmerFlag": "N",
        "realNameVerifyResult": "1",
        "notLoanOverdue": "0",
        "cardElementPass": "Y",
        "customChannel": "02",
        "workStatus": "91",
        "defaultFrmsLongitude": "-9999",
        "defaultFrmsLatitude": "-9999",
        "defaultLoanPayway": "2",
        "defaultMaxRate": "24",
        "defaultIsTrustee": "0",
        "defaultFrmsSecurityAuthMethod": "8",
        "defaultBcardLevelScore": "666",
        "defaultMac": "xx-xx-xx-xx-xx-xx",
        "defaultLoanUse": "3",
        "dateFormat": "yyyyMMdd",
        "zeroAmount": "0.00",
        "serialNoMaxLength": 32,
        "corpPostCode": "000000",
        "ftpChannelName": "yilian_dingfeng",
        "productIdMap": {
            "new_backup": "200275",
            "new": "200274",
            "old": "200274"
        },
        "feeMappingMap": {
            "Q003": [
                "reserve",
                "guarantee",
                "consult"
            ]
        },
        "pickupBankIdMap": {
            "ICBC": "102100099996",
            "ABC": "103100000026",
            "BOC": "104100000004",
            "CCB": "105100000017",
            "COMM": "301290000007",
            "CITIC": "302100011000",
            "CEB": "303100000006",
            "HXBANK": "304100040000",
            "CMBC": "305100000013",
            "GDB": "306581000003",
            "PAB": "307584007998",
            "CMB": "308584000013",
            "CIB": "309391000011",
            "SPDB": "310290000013",
            "BJBANK": "313100000013",
            "SHBANK": "325290000012"
        },
        "loanUseMap": {
            "1": "1",
            "2": "2",
            "3": "9",
            "4": "1",
            "5": "4",
            "6": "8",
            "7": "8",
            "8": "2",
            "9": "1"
        },
        "educationMap": {
            "1": "90",
            "2": "60",
            "3": "40",
            "4": "40",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "14",
            "9": "11"
        },
        "marriageMap": {
            "1": "10",
            "2": "99",
            "3": "40",
            "4": "30"
        },
        "degreeMap": {
            "1": "05",
            "2": "05",
            "3": "05",
            "4": "05",
            "5": "05",
            "6": "05",
            "7": "04",
            "8": "03",
            "9": "02"
        },
        "industryMap": {
            "1": "O",
            "2": "I",
            "3": "H",
            "4": "K",
            "5": "C",
            "6": "F",
            "7": "M",
            "8": "G",
            "9": "Q",
            "10": "P",
            "11": "J",
            "12": "Q",
            "13": "R",
            "14": "S",
            "15": "A"
        },
        "relationMap": {
            "0": "C",
            "1": "D",
            "2": "B",
            "3": "H",
            "4": "W",
            "5": "T",
            "6": "Y",
            "7": "O"
        },
        "productTypeMap": {
            "old": "212P1HY",
            "new": "212P2HY",
            "new_backup": "21201DF"
        },
        "jobDetailMap": {
            "1": "4J",
            "2": "4C",
            "3": "4A",
            "4": "6C",
            "5": "6R",
            "6": "3C",
            "7": "6J",
            "8": "4D",
            "9": "6L",
            "10": "2H",
            "11": "2F",
            "12": "2G",
            "13": "4M",
            "14": "3A",
            "15": "5Z"
        },
        "postApplyPushAttachments": [
            {
                "attachmentType": "32007",
                "fileType": "qjcredit",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "32011",
                "fileType": "lzcredit",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "32012",
                "fileType": "lzquery",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "1",
                "fileType": "idcardfront",
                "suffix": "jpg",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "2",
                "fileType": "idcardback",
                "suffix": "jpg",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "29",
                "fileType": "face",
                "suffix": "jpg",
                "remoteDir": "/cpu/KN10001/need/"
            }
        ],
        "grantPushAttachments": [
            {
                "attachmentType": "32008",
                "fileType": "danbaocount",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "32005",
                "fileType": "loancount",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            }
        ],
        "ipSegPool": [
            "27.224.128.0-27.224.191.255",
            "125.75.0.0-125.75.63.255",
            "202.201.0.0-202.201.105.255",
            "210.26.68.0-210.26.127.255",
            "222.23.32.0-222.23.191.255",
            "222.57.64.0-222.57.79.255",
            "42.89.72.0-42.89.111.255",
            "27.226.40.0-27.226.47.255",
            "60.164.0.0-60.164.15.255",
            "124.152.160.0-124.152.175.255",
            "210.26.24.0-210.26.31.255",
            "61.159.64.0-61.159.127.255",
            "222.57.16.0-222.57.31.255",
            "118.181.144.0-118.181.159.255",
            "42.90.16.0-42.90.47.255",
            "125.76.17.0-125.76.31.255",
            "42.88.208.0-42.88.231.255",
            "125.75.80.0-125.75.95.255",
            "27.225.176.0-27.225.199.255",
            "27.226.64.0-27.226.127.255",
            "124.152.65.0-124.152.75.255",
            "118.181.192.0-118.181.223.255"
        ],
        "nation": {
            "汉": "01",
            "蒙古": "201",
            "回": "202",
            "藏": "203",
            "维吾尔": "204",
            "苗": "205",
            "彝": "206",
            "壮": "207",
            "布依": "208",
            "朝鲜": "209",
            "满": "210",
            "侗": "211",
            "瑶": "212",
            "白": "213",
            "土家": "214",
            "哈尼": "215",
            "哈萨克": "216",
            "傣": "217",
            "黎": "218",
            "傈僳": "219",
            "佤": "220",
            "畲": "221",
            "高山": "222",
            "拉祜": "223",
            "水": "224",
            "东乡": "225",
            "纳西": "226",
            "景颇": "227",
            "柯尔克孜": "228",
            "土": "229",
            "达斡尔": "230",
            "仫佬": "231",
            "羌": "232",
            "布朗": "233",
            "撒拉": "234",
            "毛南": "235",
            "仡佬": "236",
            "锡伯": "237",
            "阿昌": "238",
            "普米": "239",
            "塔吉克": "240",
            "怒": "241",
            "乌孜别克": "242",
            "俄罗斯": "243",
            "鄂温克": "244",
            "德昂": "245",
            "保安": "246",
            "裕固": "247",
            "京": "248",
            "塔塔尔": "249",
            "独龙": "250",
            "鄂伦春": "251",
            "赫哲": "252",
            "门巴": "253",
            "珞巴": "254",
            "基诺": "255"
        },
        "contractSignatures": [
            {
                "attachmentType": "32008",
                "dealType": "rd",
                "contractparams": "{}"
            }
        ],
        "signedContractQueryList": [
            {
                "28": "01"
            }
        ],
        "selfYearIncomeRange": "18000-200000",
        "familyYearIncomeRange": "36000-400000",
        "familyIncomeMultiplier": "3"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_haoyue_qinjia_const", body)
