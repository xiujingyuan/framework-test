import common.global_const as gc


def update_gbiz_capital_tcl_zhongji():
    data = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "register_config": {
            "account_register_duration": 20,
            "is_multi_account_card_allowed": True,
            "is_strict_seq": True,
            "post_register": False,
            "ref_accounts": None,
            "register_step_list": [
                {
                    "channel": "tcl_zhongji",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
                    "sub_way": "baofoo_tq_protocol",
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "allow_fail": False,
                    "need_confirm_result": True,
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
        #                             "遇到在配置"
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
        #                         "code": "100998"
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "AssetImport": {
        #         "execute": {
        #             "loan_validator": [
        #                 {
        #                     "rule": "#loan.totalAmount>=cmdb.irr(#loan,'35.90') && #loan.totalAmount<=cmdb.irr(#loan,'35.95')",
        #                     "err_msg": "TCL中际[资产还款总额]不满足 irr24，请关注！"
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
        #                             "000000-成功-01"
        #                         ]
        #                     },
        #                     {
        #                         "code": "1100002",
        #                         "messages": [
        #                             "100002-存在正在审核中的授信单,无法发起新的授信审核-null"
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
        #                             "000000-成功-02"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyQuery": {
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
        #                             "000000-01-null-成功"
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
        #                             "000000-02-系统自动审批拒绝\\|-成功",
        #                             "000000-02-null-成功"
        #                         ]
        #                     },
        #                     {
        #                         "code": "1100002",
        #                         "messages": [
        #                             "100002-null-null-未查询到相关授信数据"
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
        #                             "000000-04-null-成功"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyConfirm": {
        #         "init": {
        #             "simple_lock": {
        #                 "key": "tcl-loanapplyconfirm",
        #                 "ttlSeconds": 120
        #             }
        #             },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "2000000",
        #                         "messages": [
        #                             "00000_处理成功_0_null_处理中",
        #                             "000000-3-null-成功"
        #                         ]
        #                     },
        #                     {
        #                         "code": "2120009",
        #                         "messages": [
        #                             "120009-null-null-贷款申请已存在!"
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
        #                             "000000-4-null-成功"
        #                         ]
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
        #                         "code": "2000000",
        #                         "messages": [
        #                             "成功-1-null"
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
        #                             "成功-2-订单正在处理;null",
        #                             "成功-4-null"
        #                         ]
        #                     },
        #                     {
        #                         "code": "2100002",
        #                         "messages": [
        #                             "进件号.*不存在放款信息-null-null"
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
        #                             "成功-3-null"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "CapitalRepayPlanQuery": {
        #         "execute": {
        #             "allow_diff_effect_at": False,
        #             "allow_diff_due_at": True,
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
        #         "execute": {
        #             "interval_in_minutes": "240"
        #         },
        #         "init": {
        #             "delay_time": "delayMinutes(30)"
        #         }
        #     },
        #     "AssetAutoImport": {
        #         "init": {
        #             "delay_time": "delayMinutes(90)"
        #         }
        #     }
        # }

        "workflow": {
            "title": "TCL中际放款流程编排v3",
            "inclusions": [
                "gbiz_capital_workflow_asset"
            ],
            "props": {
                "CapitalRepayPlanProps": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "need_refresh_due_at": False,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
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
                                    "rule": "#loan.totalAmount>=cmdb.irr(#loan,'35.90') && #loan.totalAmount<=cmdb.irr(#loan,'36')",
                                    "err_msg": "TCL中际[资产还款总额]不满足 irr36，请关注！"
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
                            "cancelable": True,
                            "simpleLock": {
                                "limitCount": 0,
                                "ttlSeconds": 60,
                                "key": "tcl-loanapplynew"
                            },
                            "delayTime": None
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
                                            "000000-成功-01"
                                        ]
                                    },
                                    {
                                        "code": "1100002",
                                        "messages": [
                                            "100002-存在正在审核中的授信单,无法发起新的授信审核-null"
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
                                            "000000-成功-02"
                                        ]
                                    },
                                    {
                                        "code": "1999996",
                                        "messages": [
                                            "999996-不支持该文件名后缀上传-null"
                                        ]
                                    },
                                    {
                                        "code": "1100002",
                                        "messages": [
                                            "100002-客户手机号不一致,请联系后台管理人员,手机号:\\d+-null",
                                            "100002-创建客户失败，请检查创建信息或联系开发人员-null"
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
                                            "遇到在配置"
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
                                        "code": "100998",
                                        "messages": None
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
                                            "000000-01-null-成功"
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
                                            "000000-02-系统自动审批拒绝\\|-成功",
                                            "000000-02-null-成功"
                                        ]
                                    },
                                    {
                                        "code": "1100002",
                                        "messages": [
                                            "100002-null-null-未查询到相关授信数据"
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
                                            "000000-04-null-成功"
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
                            "delayTime": "delayMinutes(90)"
                        },
                        "execute": {},
                        "finish": []
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
                            "cancelable": False,
                            "simpleLock": {
                                "limitCount": 0,
                                "ttlSeconds": 120,
                                "key": "tcl-loanapplyconfirm"
                            },
                            "delayTime": None
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
                                        "code": "2000000",
                                        "messages": [
                                            "00000_处理成功_0_null_处理中",
                                            "000000-3-null-成功"
                                        ]
                                    },
                                    {
                                        "code": "2120009",
                                        "messages": [
                                            "120009-null-null-贷款申请已存在!"
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
                                        "code": "2000000",
                                        "messages": [
                                            "000000-4-null-成功"
                                        ]
                                    }
                                ]
                            }
                        ]
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
                                        "code": "2000000",
                                        "messages": [
                                            "成功-1-null"
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
                                        "code": "2000000",
                                        "messages": [
                                            "成功-2-查询记录不存在;null",
                                            "成功-2-null\\|超过Ⅱ、Ⅲ类卡限额;null",
                                            "成功-2-查询记录不存在;处理完成",
                                            "成功-2-null\\|收款卡状态异常;null",
                                            "成功-2-null\\|超过收款卡限额;null",
                                            "成功-2-null\\|银行交易失败;处理完成",
                                            "成功-2-null\\|银行交易失败;null",
                                            "成功-2-null\\|交易失败，请联系发卡行;null",
                                            "成功-2-null\\|收款卡状态异常;处理完成",
                                            "成功-2-null\\|风控拦截;null",
                                            "成功-2-null\\|收款卡已冻结;null",
                                            "成功-2-null\\|收款卡已冻结;处理完成",
                                            "成功-2-null\\|商户10025642128的托管账户余额不足;null",
                                            "成功-2-null\\|超过收款卡限额;处理完成",
                                            "成功-2-null\\|银行无此账户信息;null",
                                            "成功-4-null"
                                        ]
                                    },
                                    {
                                        "code": "2100002",
                                        "messages": [
                                            "进件号.*不存在放款信息-null-null"
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
                                        "code": "2000000",
                                        "messages": [
                                            "成功-3-null"
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
                    "events": [],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(30)"
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
                            "props_key":"CapitalRepayPlanProps"
                        },
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
                            "cancelable": False
                        },
                        "execute": {},
                        "finish": []
                    }
                }
            ],
            "subscribers": [
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
                        "event": "CapitalChangeSucceededEvent"
                    },
                    "nodes": [
                        "AssetAutoImport"
                    ]
                },
                {
                    "listen": {
                        "event": "AssetVoidReadyEvent"
                    },
                    "nodes": [
                        "AssetVoid"
                    ]
                },
                {
                    "listen": {
                        "event": "CapitalChangeFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ]
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
                        "event": "LoanApplyAsyncFailedEvent"
                    },
                    "nodes": [
                        "BlacklistCollect"
                    ]
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
                        "CapitalRepayPlanQuery",
                        "ContractDown"
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
                        "event": "RepayPlanHandleSucceededEvent"
                    },
                    "nodes": [
                        "OurRepayPlanRefine"
                    ]
                },
                {
                    "listen": {
                        "event": "OurRepayPlanRefreshHandleSucceededEvent"
                    },
                    "nodes": [
                        "ContractPush"
                    ]
                }
            ]
        }

    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_tcl_zhongji", data)


def update_gbiz_capital_tcl_zhongji_const():
    body = {
        "productId": "20015",
        "certType": "01",
        "eduLevelMap": {
            "1": "11",
            "2": "09",
            "3": "08",
            "4": "07",
            "5": "06",
            "6": "05",
            "7": "04",
            "8": "02",
            "9": "01"
        },
        "defaultEduLevel": "99",
        "marriageMap": {
            "1": "01",
            "2": "04",
            "3": "08",
            "4": "07"
        },
        "defaultMarriage": "99",
        "relationTypeMap": {
            "0": "02",
            "1": "03",
            "2": "05",
            "3": "04",
            "4": "12",
            "5": "15",
            "6": "99",
            "7": "99"
        },
        "defaultRelationType": "99",
        "purposeMap": {
            "1": "02",
            "2": "10",
            "3": "12",
            "4": "12",
            "5": "09",
            "6": "11",
            "7": "13",
            "8": "14",
            "9": "99"
        },
        "bankCodeMap": {
            "ICBC": "ICBC",
            "ABC": "ABC",
            "BOC": "BOC",
            "CCB": "CCB",
            "SPDB": "SPDB",
            "PSBC": "PSBC",
            "COMM": "BOCO",
            "SPABANK": "SDB",
            "CMBC": "CMBC",
            "CIB": "CIB",
            "CEB": "CEB",
            "SHBANK": "SHYH",
            "CITIC": "ECITIC",
            "BJBANK": "BCCB",
            "HXBANK": "HXB",
            "GDB": "CGB"
        },
        "defaultPurpose": "99",
        "actualRate": "36.00",
        "monthRate": "1.71",
        "paymethod": "03",
        "bankCardBindType": "02",
        "accountType": "01",
        "bindCardFlag": "01",
        "creditApplyFileConfigList": [
            {
                "fileType": "01",
                "fileName": "身份证正面",
                "attachmentType": "1"
            },
            {
                "fileType": "02",
                "fileName": "身份证反面",
                "attachmentType": "2"
            },
            {
                "fileType": "03",
                "fileName": "人脸照片",
                "attachmentType": "29"
            }
        ],
        "supportFileExts": [
            "jpg",
            "png",
            "pdf",
            "jpeg",
            ""
        ],
        "monthIncomeMap": {
            "2000": "01",
            "3000": "02",
            "5000": "03",
            "8000": "03",
            "12000": "04",
            "0": "06"
        },
        "deviceTypeMap": {
            "android": "BEST_ADD",
            "ios": "BEST_IOS"
        },
        "organization": "BAOFOO",
        "bankAcctType": "01",
        "acctUsage": "04",
        "customerChannelList": [
            "test"
        ],
        "payoutTimeFormat": "yyyy-MM-dd HH:mm:ss",
        "repayPlanDateFormat": "yyyy-MM-dd",
        "contractDownConfigList": [
            {
                "capitalContractType": "03",
                "ourContractType": 36000
            },
            {
                "capitalContractType": "12",
                "ourContractType": 36001
            },
            {
                "capitalContractType": "11",
                "ourContractType": 36002
            },
            {
                "capitalContractType": "01",
                "ourContractType": 28
            },
            {
                "capitalContractType": "14",
                "ourContractType": 36003
            },
            {
                "capitalContractType": "02",
                "ourContractType": 36004
            }
        ],
        "contractPushConfigs": [
            {
                "contractType": 36005,
                "fileNameExpr": "担保协议.pdf",
                "capitalContractType": "22"
            },
            {
                "contractType": 36006,
                "fileNameExpr": "担保函.pdf",
                "capitalContractType": "21"
            },
            {
                "contractType": 36007,
                "fileNameExpr": "账户委托扣款授权书.pdf",
                "capitalContractType": "65"
            }
        ],
        "contractPushSuccessCodes": [
            "000000"
        ],
        "longTermIdnumExpireDay": "2099-12-31"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_tcl_zhongji_const", body)
