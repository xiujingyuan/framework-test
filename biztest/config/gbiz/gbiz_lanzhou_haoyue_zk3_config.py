import common.global_const as gc

def update_gbiz_capital_lanzhou_haoyue_zk3():
    body = {
                "cancelable_task_list":
                [
                    "ApplyCanLoan",
                    "LoanApplyTrial",
                    "LoanPreApply",
                    "LoanApplyNew",
                    "ChangeCapital"
                ],
                "register_config":
                {
                    "register_step_list":
                    [
                        {
                            "step_type": "PAYSVR_PROTOCOL",
                            "interaction_type": "SMS",
                            "channel": "lanzhou_haoyue_zk3",
                            "way": "tq",  # ⚠️测试环境用tq,线上用hy
                            "group": "kuainiu",
                            "status_scene":
                            {
                                "register":
                                {
                                    "success_type": "executed",
                                    "allow_fail": True,
                                    "need_confirm_result": True
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

                "workflow":
                {
                    "title": "兰州昊悦中科3流程编排v3",
                    "inclusions":
                    [
                        "gbiz_capital_workflow_asset"
                    ],
                    "props":
                    {
                        "CapitalRepayPlanProps":
                        {
                            "need_refresh_due_at": False,
                            "allow_diff_due_at": True,
                            "allow_diff_effect_at": False,
                            "allowance_check_range":
                            {
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
                                {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute":
                                {
                                    "loan_validator":
                                    [
                                        {
                                            "rule": "#loan.totalAmount>cmdb.irr(#loan,'23.70')&&loan.totalAmount<cmdb.irr(#loan,'24')",
                                            "err_msg": "兰州昊悦zk3[资产还款总额]不满足【irr23.70，irr24】，请关注！"
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
                                {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
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
                                {
                                    "executeType": "auto",
                                    "cancelable": True
                                },
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
                                {
                                    "executeType": "auto",
                                    "cancelable": True
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
                                                "code": "0"
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
                                                "code": "2"
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
                                {
                                    "executeType": "auto",
                                    "cancelable": True
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
                                                "code": "0"
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
                                                "code": "9000"
                                            },
                                            {
                                                "code": "1200",
                                                "messages":
                                                [
                                                    "民族不能为空"
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
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "simpleLock": None,
                                    "delayTime": "delaySeconds(120)"
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
                                                "code": "1999901"
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
                                                "code": "1900002",
                                                "messages":
                                                []
                                            },
                                            {
                                                "code": "1100002",
                                                "messages":
                                                [
                                                    "客户信息推送-查无此交易"
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
                                                    "客户信息推送-处理中"
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
                                {
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "simpleLock": None,
                                    "delayTime": "delaySeconds(60)"
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
                                                "code": "0"
                                            }
                                        ]
                                    }
                                ]
                            }
                        },
                        {
                            "id": "LoanCreditApply",
                            "type": "LoanCreditApplyTaskHandler",
                            "events":
                            [
                                "LoanCreditApplySyncSucceededEvent",
                                "LoanCreditApplySyncFailedEvent"
                            ],
                            "activity":
                            {
                                "init":
                                {
                                    "executeType": "auto",
                                    "cancelable": False
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
                                                "code": "0"
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
                                                "code": "9000",
                                                "messages":
                                                [
                                                    "有未使用授信，不可重复授信",
                                                    "该客户针对该业务品种在其他渠道存在在途的额度申请信息，不能重复申请",
                                                    "已存在授信申请记录和放款申请记录，请勿重复申请。"
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
                                {
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "simpleLock": None,
                                    "delayTime": "delaySeconds(180)"
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
                                                "code": "2999901"
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
                                                "code": "2999903"
                                            },
                                            {
                                                "code": "2900003"
                                            },
                                            {
                                                "code": "2100002",
                                                "messages":
                                                [
                                                    "授信申请-查无此交易"
                                                ]
                                            },
                                            {
                                                "code": "2777701",
                                                "messages":
                                                [
                                                    "授信申请-授信额度已过期"
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
                                                    "授信申请-处理中"
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
                            "events":
                            [
                                "LoanApplyTrailSucceededEvent"
                            ],
                            "activity":
                            {
                                "init":
                                {
                                    "executeType": "auto",
                                    "cancelable": True
                                },
                                "execute":
                                {},
                                "finish":
                                []
                            }
                        },
                        {
                            "id": "LoanPostCredit",
                            "type": "LoanPostCreditTaskHandler",
                            "events":
                            [
                                "LoanPostCreditSucceededEvent"
                            ],
                            "activity":
                            {
                                "init":
                                {
                                    "executeType": "auto",
                                    "cancelable": False
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
                                                "code": "0",
                                                "messages":
                                                [
                                                    "放款支用前推送合同成功"
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
                                {
                                    "executeType": "auto",
                                    "cancelable": False
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
                                                "code": "0"
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
                                                "code": "9000",
                                                "messages":
                                                [
                                                    "人脸识别失败",
                                                    "该笔授信已过有效期，请重新授信",
                                                    "拒绝受理提示：未在受理时间段内"
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
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "simpleLock": None,
                                    "delayTime": "delaySeconds(300)"
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
                                                "code": "3999904"
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
                                                "code": "3999909",
                                                "messages":
                                                [
                                                    "贷款支用查询-交易处理成功"
                                                ]
                                            },
                                            {
                                                "code": "3100099",
                                                "messages":
                                                [
                                                    "贷款支用查询-查无此交易"
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
                                                    "贷款支用查询-交易接收成功"
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
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute":
                                {
                                    "props_key": "CapitalRepayPlanProps"
                                },
                                "finish":
                                []
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
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute":
                                {
                                    "props_key": "CapitalRepayPlanProps"
                                },
                                "finish":
                                []
                            }
                        },
                        {
                            "id": "ContractSignature",
                            "type": "ContractSignatureTaskHandler",
                            "events":
                            [
                                "ContractSignatureSucceededEvent"
                            ],
                            "activity":
                            {
                                "init":
                                {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute":
                                {},
                                "finish":
                                []
                            }
                        },
                        {
                            "id": "ContractDown",
                            "type": "ContractDownTaskHandler",
                            "events":
                            [],
                            "activity":
                            {
                                "init":
                                {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute":
                                {},
                                "finish":
                                []
                            }
                        },
                        {
                            "id": "RongDanIrrTrial",
                            "type": "RongDanIrrTrialTaskHandler",
                            "events":
                            [
                                "RongDanIrrTrialSucceededEvent"
                            ],
                            "activity":
                            {
                                "init":
                                {
                                    "executeType": "auto",
                                    "cancelable": False
                                },
                                "execute":
                                {
                                    "trail_irr_limit": 35.99
                                },
                                "finish":
                                []
                            }
                        },
                        {
                            "id": "BlacklistCollect",
                            "type": "BlacklistCollectTaskHandler",
                            "events":
                            [],
                            "activity":
                            {
                                "init":
                                {
                                    "executeType": "manual",
                                    "cancelable": False
                                },
                                "execute":
                                {},
                                "finish":
                                []
                            }
                        },
                        {
                            "id": "CertificateApplyVerifySync",
                            "type": "CertificateApplyVerifySyncTaskHandler",
                            "events":
                            [
                                "CertificateApplyReadyEvent"
                            ],
                            "activity":
                            {
                                "init":
                                {},
                                "finish":
                                []
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
                                                "code": "0"
                                            },
                                            {
                                                "code": "40000"
                                            },
                                            {
                                                "code": "41200",
                                                "messages":
                                                [
                                                    "已存在该借据号的申请结清记录"
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
                                                "code": "41200",
                                                "messages":
                                                [
                                                    "该借据未结清"
                                                ]
                                            },
                                            {
                                                "code": "49000",
                                                "messages":
                                                [
                                                    "拒绝受理提示：未在受理时间段内"
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
                                "init":
                                {
                                    "delayTime": "delayDays(1, \"10:00:00\")"
                                },
                                "execute":
                                {
                                    "interval_in_minutes": "30"
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
                                    "executeType": "auto",
                                    "cancelable": False,
                                    "simpleLock": None,
                                    "delayTime": "delayMinutes(120)"
                                },
                                "execute":
                                {},
                                "finish":
                                []
                            }
                        },
                        {
                            "id": "ChangeCapital",
                            "type": "ChangeCapitalTaskHandler",
                            "events":
                            [
                                "CapitalChangeSucceededEvent",
                                "AssetVoidReadyEvent",
                                "CapitalChangeFailedEvent"
                            ],
                            "activity":
                            {
                                "init":
                                {
                                    "executeType": "manual",
                                    "cancelable": True
                                },
                                "execute":
                                {
                                    "event_handler_map":
                                    {
                                        "LoanCreditFailedEvent": "LoanCreditQuery",
                                        "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
                                        "GrantFailedEvent": "LoanConfirmQuery",
                                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
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
                        }
                    ],
                    "subscribers":
                    [
                        {
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
                            "listen":
                            {
                                "event": "AssetImportVerifySucceededEvent"
                            },
                            "nodes":
                            [
                                "ApplyCanLoan"
                            ]
                        },
                        {
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
                                "sourceWorkflowNodeId": None,
                                "event": "AssetCanLoanFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
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
                                "sourceWorkflowNodeId": None,
                                "event": "LoanPreApplySyncFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
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
                            "listen":
                            {
                                "event": "LoanApplySyncFailedEvent"
                            },
                            "nodes":
                            [
                                "ChangeCapital"
                            ],
                            "associateData":
                            {
                                "sourceWorkflowNodeId": "LoanApplyQuery",
                                "event": "LoanApplySyncFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
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
                            "listen":
                            {
                                "event": "LoanApplyAsyncFailedEvent"
                            },
                            "nodes":
                            [
                                "ChangeCapital"
                            ],
                            "associateData":
                            {
                                "sourceWorkflowNodeId": "LoanApplyQuery",
                                "event": "LoanApplyAsyncFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen":
                            {
                                "event": "LoanPostApplySucceededEvent"
                            },
                            "nodes":
                            [
                                "LoanCreditApply"
                            ],
                            "associateData":
                            {
                                "lockRecordStatus": 3
                            }
                        },
                        {
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
                                "sourceWorkflowNodeId": None,
                                "event": "LoanPostApplyFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen":
                            {
                                "event": "LoanCreditApplySyncSucceededEvent"
                            },
                            "nodes":
                            [
                                "LoanCreditQuery"
                            ]
                        },
                        {
                            "listen":
                            {
                                "event": "LoanCreditApplySyncFailedEvent"
                            },
                            "nodes":
                            [
                                "ChangeCapital"
                            ],
                            "associateData":
                            {
                                "sourceWorkflowNodeId": "LoanCreditQuery",
                                "event": "LoanCreditApplySyncFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen":
                            {
                                "event": "LoanCreditSucceededEvent"
                            },
                            "nodes":
                            [
                                "LoanApplyTrial"
                            ],
                            "associateData":
                            {
                                "lockRecordStatus": 3
                            }
                        },
                        {
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
                                "sourceWorkflowNodeId": "LoanCreditQuery",
                                "event": "LoanCreditFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen":
                            {
                                "event": "LoanCreditFailedEvent"
                            },
                            "nodes":
                            [
                                "BlacklistCollect"
                            ]
                        },
                        {
                            "listen":
                            {
                                "event": "LoanApplyTrailSucceededEvent"
                            },
                            "nodes":
                            [
                                "LoanPostCredit"
                            ]
                        },
                        {
                            "listen":
                            {
                                "event": "LoanPostCreditSucceededEvent"
                            },
                            "nodes":
                            [
                                "LoanApplyConfirm"
                            ]
                        },
                        {
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
                                "sourceWorkflowNodeId": "LoanConfirmQuery",
                                "event": "ConfirmApplySyncFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
                            "listen":
                            {
                                "event": "GrantSucceededEvent"
                            },
                            "nodes":
                            [
                                "CapitalRepayPlanQuery",
                                "ContractSignature"
                            ]
                        },
                        {
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
                                "sourceWorkflowNodeId": "LoanConfirmQuery",
                                "event": "GrantFailedEvent",
                                "skipDoubleCheck": False
                            }
                        },
                        {
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
                            "listen":
                            {
                                "event": "ContractSignatureSucceededEvent"
                            },
                            "nodes":
                            [
                                "ContractDown"
                            ]
                        },
                        {
                            "listen":
                            {
                                "event": "CertificateApplySuccessEvent"
                            },
                            "nodes":
                            [
                                "CertificateDownload"
                            ]
                        },
                        {
                            "listen":
                            {
                                "event": "CertificateApplyReadyEvent"
                            },
                            "nodes":
                            [
                                "CertificateApply"
                            ]
                        }
                    ]
                }
            }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_haoyue_zk3", body)
def update_gbiz_capital_lanzhou_haoyue_zk3_const():
    body = {
            "ftpBaseDir": "/upload/zyd",
            "ftpChannelName": "lanzhou_haoyue_zk3",
            "maxRate": 24,
            "capitalChannelCode": "Z-KN-ZKBC",
            "productCode": "Z-KN-DEBX-ZKBC",
            "nonBusinessTimeMsgs":
            [
                "非业务时间段"
            ],
            "authorization": 30603,
            "attachmentConfig":
            {
                "BEFORE_CUSTOMER_INFO_PUSH":
                {
                    "1": "certFileA",
                    "2": "certFileB",
                    "30604": "cusinfo"
                },
                "BEFORE_CREDIT_APPLY":
                {
                    "29": "facephoto",
                    "30603": "authorization"
                },
                "BEFORE_LOAN_APPLY":
                {
                    "30601": "contract",
                    "31101": "guaconletter",
                    "37300": "guacon"

                }
            },
            "loanUseMap":
            {
                "1": "1",
                "2": "6",
                "3": "9",
                "4": "1",
                "5": "4",
                "6": "8",
                "7": "8",
                "8": "2",
                "9": "10"
            },
            "educationMap":
            {
                "1": "90",
                "2": "90",
                "3": "60",
                "4": "40",
                "5": "40",
                "6": "30",
                "7": "20",
                "8": "14",
                "9": "11"
            },
            "jobMap":
            {
                "1": "5",
                "2": "5",
                "3": "5",
                "4": "4",
                "5": "4",
                "6": "4",
                "7": "4",
                "8": "4",
                "9": "4",
                "10": "1",
                "11": "4",
                "12": "1",
                "13": "4",
                "14": "2",
                "15": "6"
            },
            "dutyMap":
            {
                "1": "3",
                "2": "1",
                "3": "4",
                "4": "9",
                "5": "4",
                "6": "4"
            },
            "dupCustomerInfoPushConfigList":
            [
                {
                    "code": "1999901"
                }
            ],
            "dupCreditApplyConfigList":
            [
                {
                    "code": "2999901"
                }
            ],
            "testIp": [
                "125.75.255.255",
                "118.183.255.255",
                "103.22.56.0",
                "27.224.0.0"
            ],  # 只是测试环境使用这个(因为资金方要求了测试环境这几个ip才是白名单)，线上不能配置这个，若配置了则会使用这个里面的ip值
            "ipSegments":
            [
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
            "certificateFileConfig":
            {
                "attachmentType": 24,
                "prefix": "zyzk_",
                "suffix": "_finish",
                "fileType": "pdf"
            },
            "certificateZipFileConfig":
            {
                "baseDir": "/upload/zyd/11001",
                "suffix": "_loanFinish",
                "fileType": "zip"
            },
            "industryTypeMap":
            {
                "1": "O794",
                "2": "H62",
                "3": "F5211",
                "4": "K70",
                "5": "C3670",
                "6": "F518",
                "7": "C3521",
                "8": "F5292",
                "9": "Q8411",
                "10": "P83",
                "11": "J69",
                "12": "L726",
                "13": "R88",
                "14": "S94",
                "15": "A01"
            },
            "nationCodeMap":
            {
                "汉": "100",
                "少数民族": "200",
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
                "基诺": "255",
                "其他": "998",
                "未知": "999",
                "穿青人": "998",
                "摩梭人": "998"
            },
            "bankMap":
            {
                "BOC":
                {
                    "bankId": "104100000004",
                    "fullName": "中国银行总行"
                },
                "HXB":
                {
                    "bankId": "304100040000",
                    "fullName": "华夏银行股份有限公司总行"
                },
                "CMB":
                {
                    "bankId": "308584000013",
                    "fullName": "招商银行股份有限公司"
                },
                "ICBC":
                {
                    "bankId": "102100099996",
                    "fullName": "中国工商银行"
                },
                "CCB":
                {
                    "bankId": "105100000017",
                    "fullName": "中国建设银行股份有限公司总行"
                },
                "CIB":
                {
                    "bankId": "309391000011",
                    "fullName": "兴业银行总行"
                },
                "CEB":
                {
                    "bankId": "303100000006",
                    "fullName": "中国光大银行"
                },
                "ABC":
                {
                    "bankId": "103100000026",
                    "fullName": "中国农业银行股份有限公司"
                },
                "PSBC":
                {
                    "bankId": "403100000004",
                    "fullName": "中国邮政储蓄银行有限责任公司"
                },
                "CMBC":
                {
                    "bankId": "305100000013",
                    "fullName": "中国民生银行"
                },
                "SPDB":
                {
                    "bankId": "310290000013",
                    "fullName": "上海浦东发展银行"
                },
                "COMM":
                {
                    "bankId": "301290000007",
                    "fullName": "交通银行"
                },
                "PAB":
                {
                    "bankId": "307584007998",
                    "fullName": "平安银行（原深圳发展银行）"
                },
                "SPABANK":
                {
                    "bankId": "307584007998",
                    "fullName": "平安银行（原深圳发展银行）"
                },
                "SHBANK":
                {
                    "bankId": "325290000012",
                    "fullName": "上海银行股份有限公司"
                },
                "GDB":
                {
                    "bankId": "306581000003",
                    "fullName": "广发银行股份有限公司"
                },
                "CITIC":
                {
                    "bankId": "302100011000",
                    "fullName": "中信银行股份有限公司"
                },
                "BJBANK":
                {
                    "bankId": "313100000013",
                    "fullName": "北京银行"
                }
            },
            "cutp": "1",
            "livest": "9",
            "marriage": "10",
            "jobnature": "90"
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_haoyue_zk3_const", body)
