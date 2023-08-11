import common.global_const as gc


def update_gbiz_capital_zhongbang_haoyue_rl():
    body = {
        "manual_reverse_allowed": False,
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
                    "channel": "zhongbang_haoyue_rl",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
                    "sub_way": "baofoo_hy_protocol",
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "status_scene": {
                        "register": {
                            "success_type": "once",
                            "allow_fail": False,
                            "need_confirm_result": False,
                            "register_status_effect_duration_day": 1
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
                            "allow_fail": False,
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "allow_fail": False,
                            "type": "CheckSmsVerifyCode"
                        }
                    ]
                }
            ],
            "ref_accounts": []
        },
        # "task_config_map": {
        #     "ChangeCapital": {
        #         "execute": {
        #             "event_handler_map": {
        #                 "LoanApplySyncFailedEvent": "LoanApplyQuery",
        #                 "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
        #                 "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
        #                 "GrantFailedEvent": "LoanConfirmQuery"
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
        #                             "遇到再配置"
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
        #     },
        #     "AssetImport": {
        #         "execute": {
        #             "loan_validator": [
        #                 {
        #                     "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.70') && #loan.totalAmount<=cmdb.irr(#loan,'24.2')",
        #                     "err_msg": "众邦昊悦润楼[资产还款总额]不满足 irr24，请关注！"
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
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "10000",
        #                         "messages": [
        #                             "F-Success"
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
        #                         "code": "10000",
        #                         "messages": [
        #                             "P-Success"
        #                         ]
        #                     },
        #                     {
        #                         "code": "19999",
        #                         "messages": [
        #                             "\\[众邦昊悦润楼\\]授信申请返回异常， code: E1000003, message: 相同业务申请已存在",
        #                             "E1000003_相同业务申请已存在"
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
        #                         "code": "100001",
        #                         "messages": [
        #                             "F-性别信息与证件性别代码不一致，请检查后重试！-Success",
        #                             "F-证件有效期已经到期或即将30日内到期，请检查后重试！-Success",
        #                             "F-Success",
        #                             "\\[众邦昊悦润楼\\]资产\\[.*\\],资产本金\\[.*\\]授信可用余额不足\\[.*\\]-Success",
        #                             "\\[众邦昊悦润楼\\]资产\\[.*\\],授信额度已过期，授信时间\\[.*\\], 当前时间\\[.*\\]-Success"
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
        #                         "code": "10000",
        #                         "messages": [
        #                             "S-Success",
        #                             "R-CM9099 统一额度校验失败\\[该客户额度信息已存在\\]！-Success"
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
        #                         "code": "10000",
        #                         "messages": [
        #                             "P-Success"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanPostApply": {
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2000000",
        #                         "messages": [
        #                             "遇到再配置"
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
        #                         "code": "20000",
        #                         "messages": [
        #                             "S-Success"
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
        #                         "code": "30000",
        #                         "messages": [
        #                             "F-Success"
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
        #                         "code": "30000",
        #                         "messages": [
        #                             "P-Success-111"
        #                         ]
        #                     },
        #                     {
        #                         "code": "39999",
        #                         "messages": [
        #                             "\\[众邦昊悦润楼\\]放款申请返回异常， code: E1000003, message: 相同业务申请已存在"
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
        #                         "code": "30000",
        #                         "messages": [
        #                             "F-Success"
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
        #                         "code": "30000",
        #                         "messages": [
        #                             "S-Success"
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
        #                         "code": "30000",
        #                         "messages": [
        #                             "P-Success"
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
        #             "delay_time": "delaySeconds(10)"
        #         }
        #     },
        #     "AssetAutoImport": {
        #         "init": {
        #             "delay_time": "delayMinutes(90)"
        #         }
        #     },
        #     "CertificateDownload": {
        #         "init": {
        #             "simple_lock": {
        #                 "key": "certificatedownload-zbhyrl",
        #                 "ttlSeconds": 5
        #             }
        #         }
        #     }
        # },
        "workflow":
            {
                "title": "众邦昊悦润楼放款流程编排v3",
                "inclusions":
                    [
                        "gbiz_capital_workflow_asset"
                    ],
                "props": {
                    "CapitalRepayPlanProps": {
                        "allow_diff_effect_at": False,
                        "allow_diff_due_at": True,
                        "need_refresh_due_at": True,
                        "allowance_check_range": {
                            "min_value": 0,
                            "max_value": 0
                        },
                        "adjust_fee_list": [
                            "technical_service"
                        ]
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
                                                        "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.70') && #loan.totalAmount<=cmdb.irr(#loan,'24.2')",
                                                        "err_msg": "众邦昊悦润楼[资产还款总额]不满足 irr24，请关注！"
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
                                                            "code": "10000",
                                                            "messages":
                                                                [
                                                                    "P-Success"
                                                                ]
                                                        },
                                                        {
                                                            "code": "19999",
                                                            "messages":
                                                                [
                                                                    "\\[众邦昊悦润楼\\]授信申请返回异常， code: E1000003, message: 相同业务申请已存在",
                                                                    "E1000003_相同业务申请已存在"
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
                                                            "code": "10000",
                                                            "messages":
                                                                [
                                                                    "F-Success"
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
                                                            "code": "10000",
                                                            "messages":
                                                                [
                                                                    "S-Success",
                                                                    "R-CM9099 统一额度校验失败\\[该客户额度信息已存在\\]！-Success"
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
                                                            "code": "10000",
                                                            "messages":
                                                                [
                                                                    "F-性别信息与证件性别代码不一致，请检查后重试！-Success",
                                                                    "F-证件有效期已经到期或即将30日内到期，请检查后重试！-Success",
                                                                    "F-Success",
                                                                    "\\[众邦昊悦润楼\\]资产\\[.*\\],资产本金\\[.*\\]授信可用余额不足\\[.*\\]-Success",
                                                                    "\\[众邦昊悦润楼\\]资产\\[.*\\],授信额度已过期，授信时间\\[.*\\], 当前时间\\[.*\\]-Success"
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
                                                            "code": "10000",
                                                            "messages":
                                                                [
                                                                    "P-Success"
                                                                ]
                                                        }
                                                    ]
                                            }
                                        ]
                                }
                        },
                        {
                            "id": "LoanPostApply",
                            "type": "LoanPostApplyTaskHandler",
                            "events":
                                [
                                    "LoanPostApplySucceededEvent",
                                    "LoanPostApplyFailedEvent"
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
                                                            "code": "20000",
                                                            "messages":
                                                                [
                                                                    "S-Success"
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
                                                            "code": "30000",
                                                            "messages":
                                                                [
                                                                    "P-Success"
                                                                ]
                                                        },
                                                        {
                                                            "code": "39999",
                                                            "messages":
                                                                [
                                                                    "\\[众邦昊悦润楼\\]放款申请返回异常， code: E1000003, message: 相同业务申请已存在"
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
                                                            "code": "30000",
                                                            "messages":
                                                                [
                                                                    "F-Success"
                                                                ]
                                                        }
                                                    ]
                                            }
                                        ]
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
                                            "delayTime": "delayMinutes(2)"
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
                                                            "code": "30000",
                                                            "messages":
                                                                [
                                                                    "S-Success"
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
                                                            "code": "30000",
                                                            "messages":
                                                                [
                                                                    "F-Success"
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
                                                            "code": "30000",
                                                            "messages":
                                                                [
                                                                    "P-Success"
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
                                            "props_key": "CapitalRepayPlanProps",
                                            "need_refresh_due_at": False
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
                                        {
                                            "interval_in_minutes": "240"
                                        },
                                    "init":
                                        {
                                            "delayTime": "delaySeconds(10)"
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
                            "id": "CertificateApply",
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
                            "id": "CertificateDownload",
                            "type": "CertificateDownloadTaskHandler",
                            "events":
                                [],
                            "activity":
                                {
                                    "execute":
                                        {},
                                    "init":
                                        {
                                            "simpleLock":
                                                {
                                                    "key": "certificatedownload-zbhyrl",
                                                    "ttlSeconds": 5
                                                }
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
                                    "LoanPostApply"
                                ]
                        },
                        {
                            "memo": "支用前共享协议成功",
                            "listen":
                                {
                                    "event": "LoanPostApplySucceededEvent"
                                },
                            "nodes":
                                [
                                    "LoanApplyConfirm"
                                ]
                        },
                        {
                            "memo": "支用申请成功",
                            "listen":
                                {
                                    "event": "ConfirmApplySyncSucceededEvent"
                                },
                            "nodes":
                                [
                                    "LoanConfirmQuery"
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
                            "memo": "支用前共享协议失败",
                            "listen":
                                {
                                    "event": "LoanPostApplyFailedEvent"
                                },
                            "nodes":
                                [
                                    "ChangeCapital"
                                ],
                            "associateData":
                                {
                                    "skipDoubleCheck": True,
                                    "event": "LoanPostApplyFailedEvent"
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
                            "memo": "结清证明申请成功",
                            "listen":
                                {
                                    "event": "CertificateApplyReadyEvent"
                                },
                            "nodes":
                                [
                                    "CertificateDownload"
                                ]
                        }
                    ]
            }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongbang_haoyue_rl", body)


def update_gbiz_capital_zhongbang_haoyue_rl_const():
    body = {
        "assetPackageNo": "AP0LB62VHV2",
        "imageMaxAllowSize": 1572864,
        "imageMinAllowSize": 3072,
        "userType": "0310",
        "idType": "Ind01",
        "nationality": "CHN",
        "bucketKey": "rl-obs",
        "nationMap": {
            "汉": "01"
        },
        "nationOther": "02",
        "sexMap": {
            "m": "1",
            "f": "2"
        },
        "familyStatus": "7",
        "marriageMap": {
            "1": "10",
            "2": "21",
            "3": "30",
            "4": "40"
        },
        "defaultMarriage": "10",
        "educationMap": {
            "1": "10",
            "2": "10",
            "3": "20",
            "4": "30",
            "5": "40",
            "6": "50",
            "7": "60",
            "8": "70",
            "9": "80",
            "10": "90"
        },
        "defaultEducation": "20",
        "occupationMap": {
            "1": "1",
            "2": "X",
            "3": "4",
            "4": "4",
            "5": "4",
            "6": "6",
            "7": "6",
            "8": "1",
            "9": "4",
            "10": "4",
            "11": "4",
            "12": "4",
            "13": "4",
            "14": "1",
            "15": "5"
        },
        "defaultOccupation": 4,
        "headShipMap": {
            "0": "4",
            "1": "1",
            "2": "1",
            "3": "3",
            "4": "3",
            "5": "3",
            "6": "3",
            "7": "3",
            "8": "3",
            "9": "3",
            "10": "3",
            "11": "3",
            "12": "3",
            "13": "3",
            "14": "3",
            "15": "3"
        },
        "defaultHeadShip": 4,
        "defaultPosition": 0,
        "industryMap": {
            "1": "S",
            "2": "S",
            "3": "P",
            "4": "Q",
            "5": "S",
            "6": "E",
            "7": "C",
            "8": "I",
            "9": "J",
            "10": "O",
            "11": "H",
            "12": "R",
            "13": "O",
            "14": "L",
            "15": "A"
        },
        "defaultIndustry": "O",
        "repayType": "ECI",
        "loanPurposeMap": {
            "1": "08",
            "2": "05",
            "3": "04",
            "4": "03",
            "5": "03",
            "6": "07",
            "7": "07",
            "8": "08"
        },
        "defaultLoanPurpose": "08",
        "eduDegreeMap": {
            "1": "2",
            "2": "3",
            "3": "4",
            "4": "0",
            "5": "0",
            "6": "0",
            "7": "0",
            "8": "0",
            "9": "0",
            "10": "0"
        },
        "defaultEduDegree": "0",
        "relationMap": {
            "0": "99",
            "1": "0302",
            "2": "0302",
            "3": "0304",
            "4": "0301",
            "5": "0310",
            "6": "0311",
            "7": "99",
            "8": "0302",
            "9": "0303"
        },
        "attachmentMap": {
            "101": {
                "typeId": 1,
                "eventType": "ZBHYRL_FILE_ID_101"
            },
            "102": {
                "typeId": 2,
                "eventType": "ZBHYRL_FILE_ID_102"
            },
            "103": {
                "typeId": 29,
                "eventType": "ZBHYRL_FILE_ID_103"
            },
            "106": {
                "typeId": 29,
                "eventType": "ZBHYRL_FILE_ID_106"
            }
        },
        "contractMap": {
            "11": {
                "typeId": 28,
                "fileName": "借款合同.pdf"
            },
            "06": {
                "typeId": 35100,
                "fileName": "额度合同.pdf"
            }
        },
        "successCode": "0000",
        "failedCode": "9999",
        "bankNoMap": {
            "ICBC": "102100099996",
            "ABC": "103100000026",
            "BOC": "104100000004",
            "COMM": "301290000007",
            "CITIC": "302100011000",
            "CEB": "303100000006",
            "HXB": "304100040000",
            "CMBC": "305100000013",
            "GDB": "306581000003",
            "PAB": "307584007998",
            "CMB": "308584000013",
            "CIB": "309391000011",
            "SPDB": "310290000013",
            "BJBANK": "313100000013",
            "SHBANK": "325290000012",
            "PSBC": "403100000004",
            "CCB": "105100000017"
        },
        "outBusinessNoMap": {
            "68f06fc97994c1ec1e60280881c3cc17": "867c5cf19da2e3a13a3becd379e528b6"
        },
        "yearRate": "24",
        "flowFlag": "99",
        "threeElementsAuthResult": "Y",
        "fourElementsAuthResult": "Y",
        "newScoreMap": {
            "0": "D",
            "350": "D",
            "351": "C",
            "613": "C",
            "614": "B",
            "637": "B",
            "638": "A",
            "950": "A"
        },
        "oldScoreMap": {
            "0": "D",
            "350": "D",
            "351": "C",
            "590": "C",
            "591": "B",
            "621": "B",
            "622": "A",
            "950": "A"
        },
        "statementConfig": {
            "ftpChannelName": "zhongbang_haoyue_rl",
            "pathFormat1": "/writable/assistance/reconciliation/%s",
            "pathFormat": "/writable/reconciliation/%s",
            "targetFtpChannelName": "kuainiu",
            "targetFtpBasePath": "/zhongbang_haoyue_rl/statement",
            "fileConfigList": [
                {
                    "fileFormat": "%s_%s_Loan%s",
                    "fileSuffix": ".txt",
                    "dateFormat": "yyyyMMdd",
                    "businessDateIndex": 4,
                    "separator": "\\|"
                }
            ]
        },
        "scoreMap": {
            "A": "850",
            "B": "615",
            "C": "500",
            "D": "350"
        },
        "businessNoPrefix": {
            "memo": "以下配置不建议变更，会影响后续流程数据",
            "loanApplyPrefix": "",
            "loanApplyConfirmPrefix": ""
        },
        "kosKey": "zhongbang_haoyue_rl_obs",
        "bucketKey": "rl-obs",
        "kosUrlPrefix": "kuainiu-test",
        "imageQuantity": 0.8,
        "gpsLongitude": "620000",
        "gpsLatitude": "620000",
        "gpsAdd": "620000",
        "ipNet": "103.22.57.154",
        "ipNetAdd": "620000",
        "ipPool": {
            "620000": [
                "115.85.227.211",
                "125.76.76.223",
                "202.100.67.84",
                "180.95.152.27",
                "180.95.218.239",
                "202.100.70.211",
                "221.7.33.48",
                "180.95.144.66",
                "125.76.9.16",
                "180.95.141.243",
                "125.74.138.125",
                "124.152.130.214",
                "180.95.210.22",
                "27.226.41.210",
                "221.7.37.155",
                "124.152.165.202",
                "124.152.65.106",
                "103.22.56.171",
                "221.7.33.80",
                "60.164.188.8",
                "125.74.213.23",
                "202.100.78.214",
                "124.152.148.248",
                "180.95.152.223",
                "222.23.16.9",
                "124.152.94.137",
                "60.164.70.150",
                "221.7.32.169",
                "118.182.212.16",
                "202.100.67.148",
                "222.23.71.220",
                "210.26.41.27",
                "125.74.85.21",
                "118.181.170.144",
                "59.76.94.198",
                "180.95.139.54",
                "125.76.14.82",
                "42.93.88.93"
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongbang_haoyue_rl_const", body)
