import common.global_const as gc


def update_gbiz_capital_weipin_hanchen_jf():
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
                    "step_type": "PROTOCOL",
                    "interaction_type": "SMS",
                    "channel": "weipin_hanchen_jf",
                    "way": "jingfa",
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
                },
                {
                    "step_type": "PROTOCOL",
                    "interaction_type": "SMS",
                    "channel": "weipin_hanchen_jf",
                    "way": "weipin",
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
        #                             "资方二次校验失败：未命中\\[fail,updateCard\\]策略.*"
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
        #                     "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.98') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
        #                     "err_msg": "唯品汉辰京发[资产还款总额]不满足 【irr23.98，irr24】请关注！"
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
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "01-请求成功",
        #                             "01-请勿重复提交-请求成功"
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
        #                             "03-mock请求失败"
        #                         ]
        #                     },
        #                     {
        #                         "code": "9999",
        #                         "messages": [
        #                             "授信可用余额小于资产本金",
        #                             "授信额度已过期"
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
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "02-请求成功"
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
        #                             "01-请求成功"
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
        #                         "code": "9999",
        #                         "messages": [
        #                             "授信金额小于资产本金",
        #                             "授信额度已过期"
        #                         ]
        #                     },
        #                     {
        #                         "code": "1000000",
        #                         "messages": [
        #                             "03-mock请求失败"
        #                         ]
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
        #                         "code": "0",
        #                         "messages": [
        #                             "文件上传成功"
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
        #                             "遇到再配置"
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
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2000000",
        #                         "messages": [
        #                             "01-请求成功"
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
        #                         "code": "2000000",
        #                         "messages": [
        #                             "03-审批拒绝"
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
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2000000",
        #                         "messages": [
        #                             "02-请求成功"
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
        #                         "code": "2000000",
        #                         "messages": [
        #                             "01-请求成功"
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
        #                         "code": "2000000",
        #                         "messages": [
        #                             "03-请求成功",
        #                             "03-00007-资方审批不通过-请求成功",
        #                             "03-00006-用信审批不通过-请求成功"
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
        #             "need_refresh_due_at": True
        #         }
        #     },
        #     "ContractDown": {
        #         "init": {
        #             "delay_time": "delayMinutes(60)"
        #         }
        #     },
        #     "AssetAutoImport": {
        #         "init": {
        #             "delay_time": "delayMinutes(90)"
        #         }
        #     }
        # }
        "workflow": {
            "title": "唯品汉辰京发放款流程编排v3",
            "inclusions": [
                "gbiz_capital_workflow_asset"
            ],
            "props": {
                "CapitalRepayPlanProps": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "need_refresh_due_at": False,
                    "allowance_check_range": {
                        "min_value": -2,
                        "max_value": 2
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
                        "init": {},
                        "execute": {
                            "loan_validator": [
                                {
                                    "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.98') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                                    "err_msg": "唯品汉辰京发[资产还款总额]不满足【irr23.98，irr24】请关注！"
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
                        "init": {},
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
                        "init": {},
                        "execute": {},
                        "finish": []
                    }
                },
                {
                    "id": "LoanPreApply",
                    "type": "LoanPreApplyTaskHandler",
                    "events": [
                        "LoanPreApplySyncSucceededEvent",
                        "LoanPreApplySyncFailedEvent"
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
                                        "code": "0",
                                        "messages": []
                                    }
                                ]
                            }
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
                            "delayTime": "delaySeconds(5)"
                        },
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "1000000",
                                        "messages": [
                                            "01-请求成功",
                                            "01-请勿重复提交-请求成功"
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
                                            "03-mock请求失败"
                                        ]
                                    },
                                    {
                                        "code": "9999",
                                        "messages": [
                                            "授信可用余额小于资产本金",
                                            "授信额度已过期"
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
                            "delayTime": "delaySeconds(2)"
                        },
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "1000000",
                                        "messages": [
                                            "02-请求成功"
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
                                        "code": "9999",
                                        "messages": [
                                            "授信金额小于资产本金",
                                            "授信额度已过期"
                                        ]
                                    },
                                    {
                                        "code": "1000000",
                                        "messages": [
                                            "03-mock请求失败"
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
                                            "01-请求成功"
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
                    "events": [
                        "LoanPostApplySucceededEvent",
                        "LoanPostApplyFailedEvent"
                    ],
                    "activity": {
                        "init": {
                            "delayTime": "delaySeconds(120)"
                        },
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "0",
                                        "messages": [
                                            "文件上传成功"
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
                        "init": {},
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "2000000",
                                        "messages": [
                                            "01-请求成功"
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
                                        "code": "2000000",
                                        "messages": [
                                            "03-审批拒绝"
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
                    "events": [
                        "GrantSucceededEvent",
                        "GrantFailedEvent"
                    ],
                    "activity": {
                        "init": {
                            "delayTime": "delaySeconds(10)"
                        },
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "2000000",
                                        "messages": [
                                            "02-请求成功"
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
                                        "code": "2000000",
                                        "messages": [
                                            "03-请求成功",
                                            "03-00007-资方审批不通过-请求成功",
                                            "03-00006-用信审批不通过-请求成功"
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
                                        "code": "2000000",
                                        "messages": [
                                            "01-请求成功"
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
                            "delayTime": "delaySeconds(10)"
                        },
                        "execute": {
                            "props_key": "CapitalRepayPlanProps"
                        }
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
                            "delayTime": "delaySeconds(60)"
                        },
                        "execute": {
                            "props_key": "CapitalRepayPlanProps"
                        }
                    }
                },
                {
                    "id": "AssetVoid",
                    "type": "AssetVoidTaskHandler",
                    "events": [
                        "AssetVoidSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "manual"
                        }
                    }
                },
                {
                    "id": "AssetAutoImport",
                    "type": "AssetAutoImportTaskHandler",
                    "events": [],
                    "activity": {
                        "init": {
                            "delayTime": "delayMinutes(90)"
                        }
                    }
                },
                {
                    "id": "ChangeCapital",
                    "type": "ChangeCapitalTaskHandler",
                    "events": [
                        "CapitalChangeFailedEvent",
                        "CapitalChangeSucceededEvent",
                        "AssetVoidReadyEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "manual",
                            "cancelable": True,
                            "extraExecuteData": None
                        },
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
                },
                {
                    "id": "ContractDown",
                    "type": "ContractDownTaskHandler",
                    "events": [],
                    "activity": {
                        "execute": {
                            "interval_in_minutes": "240"
                        },
                        "init": {
                            "delayTime": "delaySeconds(10)"
                        }
                    }
                },
                {
                    "id": "AssetCancel",
                    "type": "AssetCancelSyncTaskHandler",
                    "events": [
                        "AssetVoidReadyEvent"
                    ],
                    "activity": {
                        "execute": {},
                        "init": {}
                    }
                },
                {
                    "id": "BlacklistCollect",
                    "type": "BlacklistCollectTaskHandler",
                    "activity": {
                        "init": {
                            "executeType": "manual"
                        }
                    }
                }
            ],
            "subscribers": [
                {
                    "memo": "资产导入就绪",
                    "listen": {
                        "event": "AssetImportReadyEvent"
                    },
                    "nodes": [
                        "AssetImport"
                    ]
                },
                {
                    "memo": "资产导入成功",
                    "listen": {
                        "event": "AssetImportSucceededEvent"
                    },
                    "nodes": [
                        "AssetImportVerify"
                    ]
                },
                {
                    "memo": "资产进件核心参数校验成功",
                    "listen": {
                        "event": "AssetImportVerifySucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "ApplyCanLoan"
                    ]
                },
                {
                    "memo": "资产就绪事件",
                    "listen": {
                        "event": "AssetReadyEvent"
                    },
                    "nodes": [
                        "LoanPreApply"
                    ]
                },
                {
                    "memo": "授信前影像资料上传成功",
                    "listen": {
                        "event": "LoanPreApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyNew"
                    ]
                },
                {
                    "memo": "授信申请成功",
                    "listen": {
                        "event": "LoanApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyQuery"
                    ]
                },
                {
                    "memo": "授信查询成功",
                    "listen": {
                        "event": "LoanApplyAsyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanPostApply"
                    ]
                },
                {
                    "memo": "支用前共享协议成功",
                    "listen": {
                        "event": "LoanPostApplySucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyConfirm"
                    ]
                },
                {
                    "memo": "支用申请成功",
                    "listen": {
                        "event": "ConfirmApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanConfirmQuery"
                    ]
                },
                {
                    "memo": "支用查询成功",
                    "listen": {
                        "event": "GrantSucceededEvent"
                    },
                    "nodes": [
                        "CapitalRepayPlanQuery",
                        "ContractDown"
                    ]
                },
                {
                    "memo": "还款计划查询成功",
                    "listen": {
                        "event": "RepayPlanHandleSucceededEvent"
                    },
                    "nodes": [
                        "OurRepayPlanRefine"
                    ]
                },
                {
                    "memo": "资方进件前校验失败",
                    "listen": {
                        "event": "AssetCanLoanFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "skipDoubleCheck": True,
                        "event": "AssetCanLoanFailedEvent"
                    }
                },
                {
                    "memo": "授信前上传影像失败",
                    "listen": {
                        "event": "LoanPreApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "skipDoubleCheck": False,
                        "event": "LoanPreApplySyncFailedEvent"
                    }
                },
                {
                    "memo": "同步进件申请失败",
                    "listen": {
                        "event": "LoanApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital",
                        "BlacklistCollect"
                    ],
                    "associateData": {
                        "skipDoubleCheck": True,
                        "event": "LoanApplySyncFailedEvent",
                        "sourceWorkflowNodeId": "LoanApplyQuery"
                    }
                },
                {
                    "memo": "异步进件申请失败",
                    "listen": {
                        "event": "LoanApplyAsyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital",
                        "BlacklistCollect"
                    ],
                    "associateData": {
                        "skipDoubleCheck": False,
                        "event": "LoanApplyAsyncFailedEvent",
                        "sourceWorkflowNodeId": "LoanApplyQuery"
                    }
                },
                {
                    "memo": "支用前共享协议失败",
                    "listen": {
                        "event": "LoanPostApplyFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "skipDoubleCheck": True,
                        "event": "LoanPostApplyFailedEvent"
                    }
                },
                {
                    "memo": "同步请款申请失败",
                    "listen": {
                        "event": "ConfirmApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "skipDoubleCheck": False,
                        "event": "ConfirmApplySyncFailedEvent",
                        "sourceWorkflowNodeId": "LoanConfirmQuery"
                    }
                },
                {
                    "memo": "资方放款失败",
                    "listen": {
                        "event": "GrantFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital",
                        "BlacklistCollect"
                    ],
                    "associateData": {
                        "skipDoubleCheck": False,
                        "event": "GrantFailedEvent",
                        "sourceWorkflowNodeId": "LoanConfirmQuery"
                    }
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_weipin_hanchen_jf", body)


def update_gbiz_capital_weipin_hanchen_jf_const():
    body = {
        "genderMap": {
            "m": "1",
            "f": "2"
        },
        "nationMap": {
            "汉": "01",
            "蒙古": "02",
            "回": "03",
            "藏": "04",
            "维吾尔": "05",
            "苗": "06",
            "彝": "07",
            "壮": "08",
            "布依": "09",
            "朝鲜": "10",
            "满": "11",
            "侗": "12",
            "瑶": "13",
            "白": "14",
            "土家": "15",
            "哈尼": "16",
            "哈萨克": "17",
            "傣": "18",
            "黎": "19",
            "傈僳": "20",
            "佤": "21",
            "畲": "22",
            "高山": "23",
            "拉祜": "24",
            "水": "25",
            "东乡": "26",
            "纳西": "27",
            "景颇": "28",
            "柯尔克孜": "29",
            "土": "30",
            "达斡尔": "31",
            "仫佬": "32",
            "羌": "33",
            "布朗": "34",
            "撒拉": "35",
            "毛南": "36",
            "仡佬": "37",
            "锡伯": "38",
            "阿昌": "39",
            "普米": "40",
            "塔吉克": "41",
            "怒": "42",
            "乌孜别克": "43",
            "俄罗斯": "44",
            "鄂温克": "45",
            "德昂": "46",
            "保安": "47",
            "裕固": "48",
            "京": "49",
            "塔塔尔": "50",
            "独龙": "51",
            "鄂伦春": "52",
            "赫哲": "53",
            "门巴": "54",
            "珞巴": "55",
            "基诺": "56",
            "其它": "57",
            "外国血统中国籍人士": "58",
            "未知": "00",
            "生家": "00",
            "穿青人": "00",
            "鑫": "07"
        },
        "educationMap": {
            "1": "1",
            "2": "1",
            "3": "2",
            "4": "3",
            "5": "4",
            "6": "4",
            "7": "4",
            "8": "5",
            "9": "5",
            "10": "5"
        },
        "marriageMap": {
            "1": "1",
            "2": "3",
            "3": "5",
            "4": "4"
        },
        "relationMap": {
            "0": "O",
            "1": "M",
            "2": "F",
            "3": "L",
            "4": "C",
            "5": "Y",
            "6": "T",
            "7": "O",
            "8": "D",
            "9": "H"
        },
        "creditPushAttachmentMap": {
            "1": "_cert_f.jpg",
            "2": "_cert_b.jpg",
            "29": "_face.jpg"
        },
        "creditPushContractMap": {
            "35400": "_financial_information_power_attorney.pdf"
        },
        "pushFilePath": "/upload/kuainiu/imgfiles/",
        "fileDateFormat": "yyyyMMdd",
        "capitalFtpChannelName": "weipin_hanchen_jf",
        "downFilePath": "/download/kuainiu/imgfiles/",
        "downContractMap": {
            "28": "_contract.pdf",
            "35403": "_policy_protocol.pdf",
            "35404": "_comprehensive_power_attorney.pdf",
            "35405": "_personal_info_auth.pdf",
            "35406": "_cut_payment_auth.pdf"
        },
        "beforeLoanPushContractMap": {
            "35402": "_policy_protocol.pdf",
            "35401": "_commissioned_deduction_agreement_2.pdf"
        },
        "attachmentInfoMap": {
            "credit": [
                {
                    "type": "cert_f",
                    "fileName": "_cert_f.jpg"
                },
                {
                    "type": "cert_b",
                    "fileName": "_cert_b.jpg"
                },
                {
                    "type": "face",
                    "fileName": "_face.jpg"
                },
                {
                    "type": "financial_information_power_attorney",
                    "fileName": "_financial_information_power_attorney.pdf"
                }
            ],
            "loan-confirm": [
                {
                    "type": "policy_protocol",
                    "fileName": "_policy_protocol.pdf"
                },
                {
                    "type": "commissioned_deduction_agreement_2",
                    "fileName": "_commissioned_deduction_agreement_2.pdf"
                }
            ]
        },
        "loanPurposeMap": {
            "0": "9",
            "1": "9",
            "2": "9",
            "3": "1",
            "4": "5",
            "5": "2",
            "6": "8",
            "7": "9",
            "8": "9",
            "9": "4",
            "10": "9",
            "11": "9",
            "12": "2",
            "13": "9",
            "14": "9",
            "15": "9"
        },
        "industryMap": {
            "0": "2",
            "1": "9",
            "2": "9",
            "3": "13",
            "4": "13",
            "5": "10",
            "6": "8",
            "7": "1",
            "8": "5",
            "9": "3",
            "10": "2",
            "11": "6",
            "12": "14",
            "13": "12",
            "14": "11",
            "15": "2"
        },
        "positionMap": {
            "0": "4",
            "1": "0",
            "2": "0",
            "3": "3",
            "4": "1",
            "5": "4",
            "6": "4",
            "7": "4",
            "8": "4",
            "9": "5"
        },
        "degreeMap": {
            "0": "5",
            "1": "2",
            "2": "3",
            "3": "4",
            "4": "5",
            "5": "5",
            "6": "5",
            "7": "5",
            "8": "5",
            "9": "5",
            "10": "5"
        },
        "employmentMap": {
            "1": "17",
            "2": "21",
            "3": "51",
            "4": "13",
            "5": "70",
            "6": "31"
        },
        "imageMaxAllowSize": 2097152,
        "customerType": "0",
        "sumRateFee": "0.24"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_weipin_hanchen_jf_const", body)
