import common.global_const as gc


def update_gbiz_capital_zhongyuan_zhongbao():
    body = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "register_config": {
            "ref_accounts": None,
            "register_step_list": [
                {
                    "channel": "zhongyuan_zhongbao",
                    "step_type": "PROTOCOL",
                    "way": "zhongyuan_zhongbao",
                    "interaction_type": "SMS",
                    "status_scene": {
                        "register": {
                            "success_type": "once",
                            "register_status_effect_duration_day": 1,
                            "allow_fail": False,
                            "need_confirm_result": False
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
        #                     "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.2') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
        #                     "err_msg": "中原中保[资产还款总额]不满足 irr24，请关注！"
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
        #                         "code": "0",
        #                         "messages": [
        #                             "客户信息维护成功"
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
        #                         "code": "19999",
        #                         "messages": [
        #                             "遇到再配置"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyNew": {
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0",
        #                         "messages": [
        #                             "授信申请成功"
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
        #                         "code": "0",
        #                         "messages": [
        #                             "授信查询成功"
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
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0",
        #                         "messages": [
        #                             "影像上传成功"
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
        #                         "code": "2",
        #                         "messages": [
        #                             "0000000_操作成功_Y_null_null_null"
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
        #                         "code": "2",
        #                         "messages": [
        #                             "0000000_操作成功_N_null_null_null"
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
        #                         "code": "2",
        #                         "messages": [
        #                             "0000000_操作成功_99_01_null_null"
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
        #                         "code": "2",
        #                         "messages": [
        #                             "7000000_mock 外层失败_99_01_null_null",
        #                             "0000000_操作成功_99_02_null_null"
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
        #                         "code": "2",
        #                         "messages": [
        #                             "0000000_操作成功_20__null_null",
        #                             "0000000_操作成功_88__null_null"
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
        #             },
        #             "adjust_fee_list": [
        #                 "technical_service"
        #             ]
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
        #             "delay_time": "delayMinutes(10)",
        #             "simple_lock": {
        #                 "key": "contractdown-zhongyuan",
        #                 "ttlSeconds": 10
        #             }
        #         }
        #     },
        #     "AssetAutoImport": {
        #         "init": {
        #             "delay_time": "delayMinutes(90)"
        #         }
        #     }
        # },
        "workflow": {
            "title": "中原中保流程编排v3",
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
                    },
                    "adjust_fee_list": [
                        "technical_service"
                    ]
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
                                    "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.2') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                                    "err_msg": "中原中保[资产还款总额]不满足 irr24，请关注！"
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
                    "id": "LoanPreApply",
                    "type": "LoanPreApplyTaskHandler",
                    "events": [
                        "LoanPreApplySyncSucceededEvent",
                        "LoanPreApplySyncFailedEvent"
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
                                        "messages": [
                                            "客户信息维护成功"
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
                                        "messages": [
                                            "授信申请成功"
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
                                        "code": "0",
                                        "messages": [
                                            "授信查询成功"
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
                                        "messages": [
                                            "影像上传成功"
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
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "success",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "2",
                                        "messages": [
                                            "0000000_操作成功_Y_null_null_null",
                                            "0000000_操作成功_N_RC07_虚拟运营商_Y"
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
                                        "code": "2",
                                        "messages": [
                                            "0000000_操作成功_N_RC12_02_设备黑名单拒绝_Y",
                                            "0000000_操作成功_N_1805035,RC06_客户额度异常;额度冻结_Y",
                                            "0000000_操作成功_N_null_null_null"
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
                                        "code": "2",
                                        "messages": [
                                            "0000000_操作成功_99_01_null_null"
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
                                        "code": "2",
                                        "messages": [
                                            "0000000_操作成功_99_02_9999_不符合授信标准！",
                                            "0000000_操作成功_99_03_9999_不符合授信标准！",
                                            "0000000_操作成功_99_02_ZYQZ,9999_您的综合评分不足，未能通过本次额度审批，感谢您的关注。;不符合授信标准！",
                                            "0000000_操作成功_99_02_9999,ZYXY_不符合授信标准！;您的综合评分不足，未能通过本次额度审批，感谢您的关注。",
                                            "0000000_操作成功_99_03_TKQX50_银行卡状态异常，请联系开户银行确认或换卡后重试！",
                                            "0000000_操作成功_99_02_ZYXY_您的综合评分不足，未能通过本次额度审批，感谢您的关注。",
                                            "0000000_操作成功_99_03_None_None",
                                            "0000000_操作成功_99_02_ZYXY,9999_您的综合评分不足，未能通过本次额度审批，感谢您的关注。;不符合授信标准！",
                                            "0000000_操作成功_99_02_9999,ZYQZ_不符合授信标准！;您的综合评分不足，未能通过本次额度审批，感谢您的关注。",
                                            "0000000_操作成功_99_03_RC07_虚拟运营商",
                                            "0000000_操作成功_99_03_1805035,RC06_客户额度异常;额度冻结",
                                            "7000000_mock 外层失败_99_01_null_null",
                                            "0000000_操作成功_99_02_null_null"
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
                                            "0000000_操作成功_20__None_None",
                                            "0000000_操作成功_88__None_None"
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
                            "simpleLock": {
                                "limitCount": 0,
                                "ttlSeconds": 10,
                                "key": "contractdown-zhongyuan"
                            },
                            "delayTime": "delayMinutes(10)"
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
                    "listen": {
                        "event": "AssetReadyEvent"
                    },
                    "nodes": [
                        "LoanPreApply"
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
                    "memo": "资产就绪成功事件订阅",
                    "listen": {
                        "event": "LoanPreApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyNew"
                    ]
                },
                {
                    "memo": "资产进件前任务失败事件订阅",
                    "listen": {
                        "event": "LoanPreApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": None,
                        "event": "LoanPreApplySyncFailedEvent",
                        "skipDoubleCheck": False
                    }
                },
                {
                    "memo": "资产进件前任务成功事件订阅",
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
                        "skipDoubleCheck": False
                    }
                },
                {
                    "memo": "资产进件成功事件订阅",
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
                    "memo": "资产进件查询成功事件订阅",
                    "listen": {
                        "event": "LoanPostApplySucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyConfirm"
                    ],
                    "associateData": {
                        "lockRecordStatus": 3
                    }
                },
                {
                    "memo": "资产进件后任务失败事件订阅",
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
                    "memo": "支用申请成功事件订阅",
                    "listen": {
                        "event": "ConfirmApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanConfirmQuery"
                    ]
                },
                {
                    "memo": "支用申请失败事件订阅",
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
                }
            ]
        }

    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongyuan_zhongbao", body)


def update_gbiz_capital_zhongyuan_zhongbao_const():
    body = {
        "channelNo": "83",
        "lprFloatRate": "0.0850",
        "priceIntRat": "0.0850",
        "mtdCde": "SYS002",
        "dueDayOpt": "1",
        "largeField": "",
        "bizSrc": "ZBGX_YMS",
        "dkPriceIntRat": "0.2380",
        "maritalMap": {
            "1": "10",
            "2": "20",
            "3": "40",
            "4": "50"
        },
        "cooprLoginType": [
            "01",
            "02"
        ],
        "indtryMap": {
            "1": "O",
            "2": "I",
            "3": "H",
            "4": "K",
            "5": "M",
            "6": "F",
            "7": "C",
            "8": "G",
            "9": "Q",
            "10": "P",
            "11": "J",
            "12": "S",
            "13": "R",
            "14": "S",
            "15": "A"
        },
        "position": "3",
        "empTypMap": {
            "1": "3",
            "2": "4",
            "3": "4",
            "4": "3",
            "5": "1",
            "6": "3",
            "7": "1",
            "8": "1",
            "9": "1",
            "10": "1",
            "11": "3",
            "12": "3",
            "13": "3",
            "14": "0",
            "15": "5"
        },
        "loanPurposeMap": {
            "1": "TRA",
            "2": "EDU",
            "3": "ZF",
            "4": "3C",
            "5": "TRA",
            "6": "JKYL",
            "7": "JKYL",
            "8": "NXP",
            "9": "TRA"
        },
        "relRelationMap": {
            "0": "06",
            "1": "01",
            "2": "08",
            "3": "02",
            "4": "03",
            "5": "04",
            "6": "05",
            "7": "99"
        },
        "fileUploadMap": {
            "1": "01",
            "2": "02",
            "29": "04"
        },
        "downLoadContractList": [
            {
                "contractType": 28,
                "fileType": "13",
                "contractZipMatchExpr": "#dat.cooppfApplCde==#record.assetItemNo&&#dat.submitLink=='01'"
            },
            {
                "contractType": 35901,
                "fileType": "11",
                "contractZipMatchExpr": "#dat.cooppfApplCde==#record.assetItemNo&&#dat.submitLink=='01'"
            },
            {
                "contractType": 35902,
                "fileType": "09",
                "contractZipMatchExpr": "#dat.cooppfApplCde==#record.assetItemNo&&#dat.submitLink=='01'"
            },
            {
                "contractType": 35903,
                "fileType": "10",
                "contractZipMatchExpr": "#dat.cooppfApplCde==#record.assetItemNo&&#dat.submitLink=='01'"
            },
            {
                "contractType": 35904,
                "fileType": "08",
                "contractZipMatchExpr": "#dat.cooppfApplCde==#record.assetItemNo&&#dat.submitLink=='02'"
            },
            {
                "contractType": 35905,
                "fileType": "94",
                "contractZipMatchExpr": "#dat.cooppfApplCde==#record.assetItemNo&&#dat.submitLink=='01'"
            },
            {
                "contractType": 35906,
                "fileType": "24",
                "contractZipMatchExpr": "#dat.cooppfApplCde==#record.assetItemNo&&#dat.submitLink=='01'"
            },
            {
                "contractType": 35907,
                "fileType": "25",
                "contractZipMatchExpr": "#dat.cooppfApplCde==#record.assetItemNo&&#dat.submitLink=='01'"
            }
        ],
        "zipFtpBasePathExpr": "/data/images/#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}",
        "contractDatPathExpr": "/data/out/#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}",
        "contractDatNameExpr": "zyxfA108_#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}.dat",
        "capitalFtpChannelName": "zhongyuan_zhongbao",
        "reconciliationConfig": {
            "loanTyp": "PDI0231",
            "baseDir": "/data/in",
            "suffix": ".dat",
            "prefix": "zyxfB91",
            "dataFormat": "yyyyMMdd"
        },
        "repayPlanAdjustFeeList": ["technical_service"]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongyuan_zhongbao_const", body)
