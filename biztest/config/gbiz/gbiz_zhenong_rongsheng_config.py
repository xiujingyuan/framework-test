import common.global_const as gc


def update_gbiz_capital_zhenong_rongsheng():
    body = {
        "manual_reverse_allowed": False,
        "recall_via_ivr_enabled": True,
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "raise_limit_allowed": False,
        "register_config": {
            "register_step_list": [
                {
                    "step_type": "PROTOCOL",
                    "channel": "zhenong_rongsheng",
                    "interaction_type": "SMS",
                    "way": "zhenong_rongsheng",
                    "status_scene": {
                        "register": {
                            "success_type": "once",
                            "register_status_effect_duration_day": 1,
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
        #     "AssetAutoImport": {
        #         "init": {
        #             "delay_time": "delayMinutes(120)"
        #         }
        #     },
        #     "AssetImport": {
        #         "execute": {
        #             "loan_validator": [
        #                 {
        #                     "rule": "#loan.totalAmount>=cmdb.irr(#loan,'35.99') && #loan.totalAmount<=cmdb.irr(#loan,'36')",
        #                     "err_msg": "浙农荣晟[资产还款总额]不满足 irr36，请关注！"
        #                 }
        #             ]
        #         }
        #     },
        #     "LoanPreApply": {
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
        #             }
        #         ]
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
        #                         "code": "1601044",
        #                         "messages": [
        #                             "mock请求失败"
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
        #                         "code": "1000000",
        #                         "messages": [
        #                             "申请已受理"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyQuery": {
        #         "init": {
        #             "delay_time": "delaySeconds(2)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1601301",
        #                         "messages": [
        #                             "查询信息不存在",
        #                             "F-查询信息不存在"
        #                         ]
        #                     },
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "F-"
        #                         ]
        #                     },
        #                     {
        #                         "code": "9999",
        #                         "messages": [
        #                             "\\[浙农荣晟\\]资产\\[.*\\],授信额度已过期，授信时间\\[2022-11-24\\], 当前时间.*-"
        #                         ]
        #                     },
        #                     {
        #                         "code": "9999",
        #                         "messages": [
        #                             "\\[浙农荣晟\\]资产\\[.*\\],资产本金\\[.*\\]授信可用余额不足\\[.*\\]-"
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
        #                         "code": "1000000",
        #                         "messages": [
        #                             "S-"
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
        #                             "I-处理中-"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyConfirm": {
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2601044",
        #                         "messages":[
        #                             "授信到期"
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
        #                         "code": "2000000"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanCreditQuery": {
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "3000000",
        #                         "messages":[
        #                             "I-F-处理中-"
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
        #                         "code": "3000000",
        #                         "messages": [
        #                             "I-I-处理中-"
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
        #                         "code": "3000000",
        #                         "messages": [
        #                             "I-处理中-"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanConfirmQuery": {
        #         "init": {
        #             "delay_time": "delaySeconds(10)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2000000",
        #                         "messages":[
        #                             "F-放款失败-"
        #                         ]
        #                     },
        #                     {
        #                         "code": "2601044",
        #                         "messages": [
        #                             "F-授信到期"
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
        #                         "code": "2000000",
        #                         "messages":[
        #                             "S-放款成功-"
        #                             ]
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "retry"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2000000",
        #                         "messages":[
        #                             "I-处理中-"
        #                             ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "CapitalRepayPlanQuery": {
        #         "execute": {
        #             "diff_effect_at": False,
        #             "diff_due_at": False,
        #             "allowance_check_range": {
        #                 "min_value": 0,
        #                 "max_value": 0
        #             }
        #         }
        #     },
        #     "OurRepayPlanRefine": {
        #         "execute": {
        #             "need_refresh_due_at": False
        #         }
        #     },
        #     "ContractDown": {
        #         "init": {
        #             "delay_time": "delaySeconds(60)"
        #         }
        #     },
        #     "CertificateApply": {
        #       "finish": [
        #         {
        #           "action": {
        #             "policy": "success"
        #           },
        #           "matches": [
        #             {
        #               "code": "0",
        #               "messages": [
        #                 "申请结清证明成功"
        #               ]
        #             }
        #           ]
        #         }
        #       ]
        #     },
        #     "CertificateDownload": {
        #       "execute": {
        #         "interval_in_minutes": "240"
        #       },
        #       "init": {
        #         "delay_time": "delayDays(1, \"09:30:00\")"
        #       }
        #     },
        #     "ChangeCapital": {
        #         "execute": {
        #             "event_handler_map": {
        #                 "LoanApplySyncFailedEvent": "LoanApplyQuery",
        #                 "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
        #                 "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
        #                 "LoanCreditFailedEvent": "LoanCreditQuery",
        #                 "GrantFailedEvent": "LoanConfirmQuery"
        #             }
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
        #                             "切资方,路由系统返回空"
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
        #                             "资方二次校验失败：未命中\\[fail\\]策略.*"
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
        #                         "code": ""
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # }
        "workflow":
            {
                "title": "浙农荣晟放款流程编排v3",
                "inclusions":
                    [
                        "gbiz_capital_workflow_asset"
                    ],
                "props": {
                    "CapitalRepayPlanProps": {
                        "allow_diff_effect_at": False,
                        "allow_diff_due_at": False,
                        "allowance_check_range": {
                            "min_value": 0,
                            "max_value": 0
                        }
                    }
                },
                "nodes":
                    [
                        {
                            "id": "AssetImport",
                            "type": "AssetImportTaskHandler",
                            "events":
                                [
                                    "AssetImportSucceededEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {},
                                    "execute":
                                        {
                                            "loan_validator":
                                                [
                                                    {
                                                        "rule": "#loan.totalAmount>=cmdb.irr(#loan,'35.99') && #loan.totalAmount<=cmdb.irr(#loan,'36')",
                                                        "err_msg": "浙农荣晟[资产还款总额]不满足 irr36，请关注！"
                                                    }
                                                ]
                                        },
                                    "finish":
                                        []
                                }
                        },
                        {
                            "id": "AssetImportVerify",
                            "type": "AssetImportVerifyTaskHandler",
                            "events":
                                [
                                    "AssetImportVerifySucceededEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {},
                                    "execute":
                                        {},
                                    "finish":
                                        []
                                }
                        },
                        {
                            "id": "ApplyCanLoan",
                            "type": "ApplyCanLoanTaskHandler",
                            "events":
                                [
                                    "AssetReadyEvent",
                                    "AssetCanLoanFailedEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {},
                                    "execute":
                                        {},
                                    "finish":
                                        []
                                }
                        },
                        {
                            "id": "LoanPreApply",
                            "type": "LoanPreApplyTaskHandler",
                            "events":
                                [
                                    "LoanPreApplySyncSucceededEvent",
                                    "LoanPreApplySyncFailedEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {},
                                    "finish":
                                        [
                                            {
                                                "action":
                                                    {
                                                        "policy": "success"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "0",
                                                            "messages":
                                                                [
                                                                    "文件上传成功"
                                                                ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "fail"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "9999",
                                                            "messages":
                                                                [
                                                                    ""
                                                                ]
                                                        }
                                                    ]
                                            }
                                        ]
                                }
                        },
                        {
                            "id": "LoanApplyNew",
                            "type": "LoanApplyNewTaskHandler",
                            "events":
                                [
                                    "LoanApplySyncSucceededEvent",
                                    "LoanApplySyncFailedEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {},
                                    "execute":
                                        {},
                                    "finish":
                                        [
                                            {
                                                "action":
                                                    {
                                                        "policy": "success"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "1000000",
                                                            "messages":
                                                                [
                                                                    "申请已受理"
                                                                ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "fail"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "1601044",
                                                            "messages":
                                                                [
                                                                    "mock请求失败"
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
                            "events":
                                [
                                    "LoanApplyAsyncSucceededEvent",
                                    "LoanApplyAsyncFailedEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {
                                            "delayTime": "delayMinutes(1)"
                                        },
                                    "execute":
                                        {},
                                    "finish":
                                        [
                                            {
                                                "action":
                                                    {
                                                        "policy": "success"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "1000000",
                                                            "messages":
                                                                [
                                                                    "S-"
                                                                ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "fail"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "1601301",
                                                            "messages": [
                                                                "查询信息不存在",
                                                                "F-查询信息不存在"
                                                            ]
                                                        },
                                                        {
                                                            "code": "1000000",
                                                            "messages": [
                                                                "F-"
                                                            ]
                                                        },
                                                        {
                                                            "code": "9999",
                                                            "messages": [
                                                                "\\[浙农荣晟\\]资产\\[.*\\],授信额度已过期，授信时间\\[2022-11-24\\], 当前时间.*-"
                                                            ]
                                                        },
                                                        {
                                                            "code": "9999",
                                                            "messages": [
                                                                "\\[浙农荣晟\\]资产\\[.*\\],资产本金\\[.*\\]授信可用余额不足\\[.*\\]-"
                                                            ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "retry"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "1000000",
                                                            "messages":
                                                                [
                                                                    "I-处理中-"
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
                            "events":
                                [
                                    "ConfirmApplySyncSucceededEvent",
                                    "ConfirmApplySyncFailedEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {},
                                    "execute":
                                        {},
                                    "finish":
                                        [
                                            {
                                                "action":
                                                    {
                                                        "policy": "success"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "2000000"
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "fail"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "2601044",
                                                            "messages":
                                                                [
                                                                    "授信到期"
                                                                ]
                                                        }
                                                    ]
                                            }
                                        ]
                                }
                        },
                        {
                            "id": "LoanCreditQuery",
                            "type": "LoanCreditQueryTaskHandler",
                            "events":
                                [
                                    "LoanCreditSucceededEvent",
                                    "LoanCreditFailedEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {},
                                    "execute":
                                        {},
                                    "finish":
                                        [
                                            {
                                                "action":
                                                    {
                                                        "policy": "fail"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "3000000",
                                                            "messages":
                                                                [
                                                                    "I-F-处理中-"
                                                                ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "success"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "3000000",
                                                            "messages":
                                                                [
                                                                    "I-I-处理中-"
                                                                ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "retry"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "3000000",
                                                            "messages":
                                                                [
                                                                    "I-处理中-"
                                                                ]
                                                        }
                                                    ]
                                            }
                                        ]
                                }
                        },
                        {
                            "id": "UserLoanConfirmNotify",
                            "type": "UserLoanConfirmNotifyBizPerformer",
                            "events":
                                [],
                            "activity":
                                {
                                    "init":
                                        {
                                            "delayTime": "delayMinutes(120)",
                                            "extraExecuteData": "CONTRACT_VIA_URL"
                                        }
                                }
                        },
                        {
                            "id": "LoanConfirmQuery",
                            "type": "LoanConfirmQueryTaskHandler",
                            "events":
                                [
                                    "GrantSucceededEvent",
                                    "GrantFailedEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {
                                            "delayTime": "delayMinutes(10)"
                                        },
                                    "execute":
                                        {},
                                    "finish":
                                        [
                                            {
                                                "action":
                                                    {
                                                        "policy": "success"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "2000000",
                                                            "messages":
                                                                [
                                                                    "S-放款成功-"
                                                                ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "fail"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "2000000",
                                                            "messages":
                                                                [
                                                                    "F-放款失败-"
                                                                ]
                                                        },
                                                        {
                                                            "code": "2601044",
                                                            "messages":
                                                                [
                                                                    "F-授信到期"
                                                                ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "retry"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "2000000",
                                                            "messages":
                                                                [
                                                                    "I-处理中-"
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
                            "events":
                                [
                                    "RepayPlanHandleSucceededEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {
                                            "delayTime": "delaySeconds(10)"
                                        },
                                    "execute":
                                        {
                                            "props_key": "CapitalRepayPlanProps"
                                        }
                                }
                        },
                        {
                            "id": "OurRepayPlanRefine",
                            "type": "OurRepayPlanRefineTaskHandler",
                            "events":
                                [
                                    "OurRepayPlanRefreshHandleSucceededEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {
                                            "delayTime": "delaySeconds(10)"
                                        },
                                    "execute":
                                        {
                                            "props_key": "CapitalRepayPlanProps"
                                        }
                                }
                        },
                        {
                            "id": "AssetVoid",
                            "type": "AssetVoidTaskHandler",
                            "events":
                                [
                                    "AssetVoidSucceededEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {
                                            "executeType": "manual"
                                        }
                                }
                        },
                        {
                            "id": "AssetAutoImport",
                            "type": "AssetAutoImportTaskHandler",
                            "events":
                                [],
                            "activity":
                                {
                                    "init":
                                        {
                                            "delayTime": "delayMinutes(120)"
                                        }
                                }
                        },
                        {
                            "id": "ChangeCapital",
                            "type": "ChangeCapitalTaskHandler",
                            "events":
                                [
                                    "CapitalChangeFailedEvent",
                                    "CapitalChangeSucceededEvent",
                                    "AssetVoidReadyEvent"
                                ],
                            "activity":
                                {
                                    "init":
                                        {
                                            "executeType": "manual",
                                            "cancelable": True,
                                            "extraExecuteData": None
                                        },
                                    "execute":
                                        {
                                            "event_handler_map":
                                                {
                                                    "LoanApplySyncFailedEvent": "LoanApplyQuery",
                                                    "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                                                    "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                                                    "LoanCreditFailedEvent": "LoanCreditQuery",
                                                    "GrantFailedEvent": "LoanConfirmQuery"
                                                },
                                            "can_change_capital": True
                                        },
                                    "finish":
                                        [
                                            {
                                                "action":
                                                    {
                                                        "policy": "success"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "0",
                                                            "messages":
                                                                [
                                                                    "切资方路由\\(二次\\)成功"
                                                                ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "finalFail"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "12",
                                                            "messages":
                                                                []
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "fail"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "1",
                                                            "messages":
                                                                [
                                                                    "遇到再进行配置"
                                                                ]
                                                        }
                                                    ]
                                            },
                                            {
                                                "action":
                                                    {
                                                        "policy": "retry"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "-10000",
                                                            "messages":
                                                                [
                                                                    "遇到再进行配置"
                                                                ]
                                                        }
                                                    ]
                                            }
                                        ]
                                }
                        },
                        {
                            "id": "ContractDown",
                            "type": "ContractDownTaskHandler",
                            "events":
                                [],
                            "activity":
                                {
                                    "execute":
                                        {},
                                    "init":
                                        {
                                            "delayTime": "delaySeconds(60)"
                                        }
                                }
                        },
                        {
                            "id": "AssetCancel",
                            "type": "AssetCancelSyncTaskHandler",
                            "events":
                                [
                                    "AssetVoidReadyEvent"
                                ],
                            "activity":
                                {
                                    "execute":
                                        {},
                                    "init":
                                        {}
                                }
                        },
                        {
                            "id": "BlacklistCollect",
                            "type": "BlacklistCollectTaskHandler",
                            "activity":
                                {
                                    "init":
                                        {
                                            "executeType": "manual"
                                        }
                                }
                        },
                        {
                            "id": "CertificateApplyVerify",
                            "type": "CertificateApplyVerifySyncTaskHandler",
                            "events":
                                [
                                    "CertificateApplyReadyEvent"
                                ],
                            "activity":
                                {
                                    "execute":
                                        {},
                                    "init":
                                        {}
                                }
                        },
                        {
                            "id": "CertificateApply",
                            "type": "CertificateApplyTaskHandler",
                            "events":
                                [
                                    "CertificateApplySuccessEvent"
                                ],
                            "activity":
                                {
                                    "execute":
                                        {},
                                    "init":
                                        {},
                                    "finish":
                                        [
                                            {
                                                "action":
                                                    {
                                                        "policy": "success"
                                                    },
                                                "matches":
                                                    [
                                                        {
                                                            "code": "0",
                                                            "messages":
                                                                [
                                                                    "申请结清证明成功"
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
                            "events":
                                [],
                            "activity":
                                {
                                    "execute":
                                        {
                                            "interval_in_minutes": "240"
                                        },
                                    "init":
                                        {
                                            "delayTime": "delayDays(1, \"09:30:00\")"
                                        }
                                }
                        }
                    ],
                "subscribers":
                    [
                        {
                            "memo": "资产导入就绪",
                            "listen":
                                {
                                    "event": "AssetImportReadyEvent"
                                },
                            "nodes":
                                [
                                    "AssetImport"
                                ]
                        },
                        {
                            "memo": "资产导入成功",
                            "listen":
                                {
                                    "event": "AssetImportSucceededEvent"
                                },
                            "nodes":
                                [
                                    "AssetImportVerify"
                                ]
                        },
                        {
                            "memo": "资产进件核心参数校验成功",
                            "listen":
                                {
                                    "event": "AssetImportVerifySucceededEvent",
                                    "matches":
                                        []
                                },
                            "nodes":
                                [
                                    "ApplyCanLoan"
                                ]
                        },
                        {
                            "memo": "资产就绪事件",
                            "listen":
                                {
                                    "event": "AssetReadyEvent"
                                },
                            "nodes":
                                [
                                    "LoanPreApply"
                                ]
                        },
                        {
                            "memo": "授信前影像资料上传成功",
                            "listen":
                                {
                                    "event": "LoanPreApplySyncSucceededEvent"
                                },
                            "nodes":
                                [
                                    "LoanApplyNew"
                                ]
                        },
                        {
                            "memo": "授信申请成功",
                            "listen":
                                {
                                    "event": "LoanApplySyncSucceededEvent"
                                },
                            "nodes":
                                [
                                    "LoanApplyQuery"
                                ]
                        },
                        {
                            "memo": "授信查询成功",
                            "listen":
                                {
                                    "event": "LoanApplyAsyncSucceededEvent"
                                },
                            "nodes":
                                [
                                    "LoanApplyConfirm"
                                ]
                        },
                        {
                            "memo": "获取协议签约地址",
                            "listen":
                                {
                                    "event": "ConfirmApplySyncSucceededEvent"
                                },
                            "nodes":
                                [
                                    "LoanCreditQuery"
                                ]
                        },
                        {
                            "memo": "支用申请成功",
                            "listen":
                                {
                                    "event": "LoanCreditSucceededEvent"
                                },
                            "nodes":
                                [
                                    "LoanConfirmQuery",
                                    "UserLoanConfirmNotify"
                                ]
                        },
                        {
                            "memo": "支用查询成功",
                            "listen":
                                {
                                    "event": "GrantSucceededEvent"
                                },
                            "nodes":
                                [
                                    "CapitalRepayPlanQuery",
                                    "ContractDown"
                                ]
                        },
                        {
                            "memo": "还款计划查询成功",
                            "listen":
                                {
                                    "event": "RepayPlanHandleSucceededEvent"
                                },
                            "nodes":
                                [
                                    "OurRepayPlanRefine"
                                ]
                        },
                        {
                            "memo": "资方进件前校验失败",
                            "listen":
                                {
                                    "event": "AssetCanLoanFailedEvent"
                                },
                            "nodes":
                                [
                                    "ChangeCapital"
                                ],
                            "associateData":
                                {
                                    "skipDoubleCheck": True,
                                    "event": "AssetCanLoanFailedEvent"
                                }
                        },
                        {
                            "memo": "授信前上传影像失败",
                            "listen":
                                {
                                    "event": "LoanPreApplySyncFailedEvent"
                                },
                            "nodes":
                                [
                                    "ChangeCapital"
                                ],
                            "associateData":
                                {
                                    "skipDoubleCheck": False,
                                    "event": "LoanPreApplySyncFailedEvent"
                                }
                        },
                        {
                            "memo": "同步进件申请失败",
                            "listen":
                                {
                                    "event": "LoanApplySyncFailedEvent"
                                },
                            "nodes":
                                [
                                    "ChangeCapital",
                                    "BlacklistCollect"
                                ],
                            "associateData":
                                {
                                    "skipDoubleCheck": True,
                                    "event": "LoanApplySyncFailedEvent",
                                    "sourceWorkflowNodeId": "LoanApplyQuery"
                                }
                        },
                        {
                            "memo": "异步进件申请失败",
                            "listen":
                                {
                                    "event": "LoanApplyAsyncFailedEvent"
                                },
                            "nodes":
                                [
                                    "ChangeCapital",
                                    "BlacklistCollect"
                                ],
                            "associateData":
                                {
                                    "skipDoubleCheck": False,
                                    "event": "LoanApplyAsyncFailedEvent",
                                    "sourceWorkflowNodeId": "LoanApplyQuery"
                                }
                        },
                        {
                            "memo": "获取协议签约地址失败",
                            "listen":
                                {
                                    "event": "LoanCreditFailedEvent"
                                },
                            "nodes":
                                [
                                    "ChangeCapital"
                                ],
                            "associateData":
                                {
                                    "skipDoubleCheck": True,
                                    "event": "LoanCreditFailedEvent"
                                }
                        },
                        {
                            "memo": "同步请款申请失败",
                            "listen":
                                {
                                    "event": "ConfirmApplySyncFailedEvent"
                                },
                            "nodes":
                                [
                                    "ChangeCapital"
                                ],
                            "associateData":
                                {
                                    "skipDoubleCheck": False,
                                    "event": "ConfirmApplySyncFailedEvent",
                                    "sourceWorkflowNodeId": "LoanConfirmQuery"
                                }
                        },
                        {
                            "memo": "资方放款失败",
                            "listen":
                                {
                                    "event": "GrantFailedEvent"
                                },
                            "nodes":
                                [
                                    "ChangeCapital"
                                ],
                            "associateData":
                                {
                                    "skipDoubleCheck": False,
                                    "event": "GrantFailedEvent",
                                    "sourceWorkflowNodeId": "LoanConfirmQuery"
                                }
                        },
                        {
                            "memo": "结清证明申请",
                            "listen":
                                {
                                    "event": "CertificateApplyReadyEvent"
                                },
                            "nodes":
                                [
                                    "CertificateApply"
                                ]
                        },
                        {
                            "memo": "结清证明申请成功",
                            "listen":
                                {
                                    "event": "CertificateApplySuccessEvent"
                                },
                            "nodes":
                                [
                                    "CertificateDownload"
                                ]
                        }
                    ]
            }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhenong_rongsheng", body)


def update_gbiz_capital_zhenong_rongsheng_const():
    body = {
        "creditType": 1,
        "idNoType": "01",
        "censusType": 1,
        "specialConcernUser": 0,
        "marriageMap": {
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 4
        },
        "defaultMarriage": 1,
        "educationMap": {
            "1": 1,
            "2": 1,
            "3": 2,
            "4": 3,
            "5": 5,
            "6": 5,
            "7": 4,
            "8": 6,
            "9": 6,
            "10": 0
        },
        "defaultEducation": 0,
        "positionMap": {
            "0": 5,
            "1": 2,
            "2": 1,
            "3": 1,
            "4": 1,
            "5": 1,
            "6": 1,
            "7": 1,
            "8": 1,
            "9": 5
        },
        "defaultPosition": 1,
        "industryMap": {
            "0": "O",
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
            "11": "H",
            "12": "R",
            "13": "O",
            "14": "O",
            "15": "A"
        },
        "defaultIndustry": "O",
        "relationMap": {
            "0": 7,
            "1": 1,
            "2": 1,
            "3": 2,
            "4": 0,
            "5": 6,
            "6": 4,
            "7": 7,
            "8": 1,
            "9": 3
        },
        "defaultRelation": 7,
        "loanPurposeMap": {
            "1": 1,
            "2": 2,
            "3": 3,
            "4": 9,
            "5": 5,
            "6": 6,
            "7": 7,
            "8": 8,
            "9": 9
        },
        "defaultLoanPurpose": 9,
        "repaymentSource": 1,
        "creditPushAttachmentMap": {
            "1": "idImageFront_",
            "2": "idImageBack_"
        },
        "creditPushContractMap": {
            "33900": "personalAuth_"
        },
        "downContractMap": {
            "28": "贷款合同.pdf"
        },
        "pushAttachmentPath": "/upload/video",
        "pushContractPath": "/upload/contract",
        "capitalFtpChannelName": "zhenong_rongsheng",
        "orderSource": 1,
        "personalAuthCode": 33900,
        "imageMaxAllowSize": 1572864,
        "amountMap": {
            "0": 0,
            "1": 1,
            "2": 2,
            "3": 2,
            "4": 2,
            "5": 3
        },
        "loanTotalMap": {
            "0": 0,
            "1000": 1,
            "5000": 1,
            "5001": 2,
            "10000": 2,
            "10001": 3,
            "20000": 3,
            "20001": 4,
            "40000": 4,
            "40001": 5
        },
        "m12MaxOverdueMap": {
            "0": 0,
            "1": 1,
            "3": 1,
            "4": 2,
            "7": 2,
            "8": 3,
            "14": 3,
            "15": 4
        },
        "availableAmtMap": {
            "0": 0,
            "1": 1,
            "1000": 1,
            "1001": 2,
            "4000": 2,
            "4001": 3,
            "8000": 3,
            "8001": 4,
            "15000": 4,
            "15001": 5,
            "30000": 5,
            "30001": 6
        },
        "signUrlTimeout": 2,
        "creditNoPrefix": "ZNSX",
        "bankMap": {
            "EGBANK": "恒丰银行",
            "CCB": "中国建设银行",
            "CEB": "光大银行",
            "PSBC": "中国邮政邮储银行",
            "ABC": "中国农业银行",
            "COMM": "交通银行",
            "SHBANK": "上海银行",
            "BOC": "中国银行",
            "CITIC": "中信银行",
            "HZCB": "杭州银行",
            "SPDB": "上海浦东发展银行",
            "ICBC": "中国工商银行",
            "BJBANK": "北京银行",
            "CIB": "兴业银行",
            "PAB": "平安银行",
            "CMB": "招商银行",
            "CZ": "浙商银行",
            "CMBC": "中国民生银行",
            "GDB": "广东发展银行"
        },
        "certificateConfig": {
            "certificateDownloadPath": "/download/settle/",
            "certificateDownloadFilePrefix": "settle_",
            "certificateDownloadFileSuffix": ".pdf",
            "certificateApplyPath": "/upload/settle/",
            "certificateApplyFilePrefix": "settlelist_",
            "certificateApplyFileSuffix": ".txt",
            "certificateDateFormat": "yyyyMMdd",
            "certificateFieldSeparator": "|"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhenong_rongsheng_const", body)
