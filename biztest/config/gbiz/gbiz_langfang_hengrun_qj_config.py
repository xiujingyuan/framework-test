import common.global_const as gc


def update_gbiz_capital_langfang_hengrun_qj():
    body = {
        "cancelable_task_list": [
            "ApplyCanLoan",
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
                    "channel": "langfang_hengrun_qj",
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
        "workflow": {
            "title": "廊坊恒润资金方流程编排v3",
            "inclusions": [
                "gbiz_capital_workflow_asset"
            ],
            "props": {
                "CapitalRepayPlanProps": {
                    "allow_diff_due_at": False,
                    "allow_diff_effect_at": False,
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
                                    "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.80') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                                    "err_msg": "廊坊恒润亲家[资产还款总额]不满足 irr24，请关注！"
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
                                            "01_0000_成功_成功"
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
                                        "code": "1999999",
                                        "messages": [
                                            "02_0001_失败测试_mock失败"
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
                                            "进件合同生成成功"
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
                                            "影像资料上传&通知成功"
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
                                        "code": "2000000",
                                        "messages": [
                                            "00_0000_成功_路由处理中",
                                            "00_0000_成功_路由处理中 "
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
                                        "code": "2000007",
                                        "messages": [
                                            "02_9999_mock失败测试_路由失败"
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
                                        "code": "2000000",
                                        "messages": [
                                            "01_0001_成功_路由成功"
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
                                            "00_0000_成功_null"
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
                                        "code": "2000005",
                                        "messages": [
                                            "02_0004_mock失败_路由查询失败test"
                                        ]
                                    },
                                    {
                                        "code": "9999",
                                        "messages": [
                                            "当前资产待放金额.*大于查询返回授信成功金额.*"
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "ContractSignature",
                    "type": "ContractSignatureTaskHandler",
                    "events": [
                        "ContractSignatureSucceededEvent"
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
                    "id": "GuaranteeApply",
                    "type": "GuaranteeApplyTaskHandler",
                    "events": [
                        "GuaranteeApplySucceededEvent"
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
                    "id": "GuaranteeDown",
                    "type": "GuaranteeDownTaskHandler",
                    "events": [
                        "GuaranteeDownloadSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False
                        },
                        "execute": {
                            "interval_in_minutes": "2"
                        },
                        "finish": []
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
                                            "请款前文件上传&通知成功"
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
                                        "code": "3000000",
                                        "messages": [
                                            "00_0000_成功_null",
                                            "00_0000_内层成功_null"
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
                                        "code": "3000007",
                                        "messages": [
                                            "02_0007_内层失败msg_null"
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
                                        "code": "3000000",
                                        "messages": [
                                            "01_0001_成功_null",
                                            "01_0001_内层成功_null"
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
                                        "code": "3000077",
                                        "messages": [
                                            "01_0011_内层失败测试_null"
                                        ]
                                    },
                                    {
                                        "code": "3000009",
                                        "messages": [
                                            "02_0002_内层失败测试_null"
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
                                        "code": "3000000",
                                        "messages": [
                                            "00_0000_成功_null"
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
                    "id": "ContractDown",
                    "type": "ContractDownTaskHandler",
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
                    "id": "ElectronicReceiptDown",
                    "type": "ElectronicReceiptDownTaskHandler",
                    "events": [],
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
                                "GrantFailedEvent": "LoanConfirmQuery",
                                "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
                                "LoanCreditFailedEvent": "LoanCreditQuery"
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
                        "skipDoubleCheck": True
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
                        "LoanCreditApply"
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
                        "event": "LoanCreditApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanCreditQuery"
                    ]
                },
                {
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
                    "listen": {
                        "event": "LoanCreditSucceededEvent"
                    },
                    "nodes": [
                        "ContractSignature"
                    ]
                },
                {
                    "listen": {
                        "event": "LoanCreditFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": "LoanCreditQuery",
                        "event": "LoanCreditFailedEvent",
                        "skipDoubleCheck": False
                    }
                },
                {
                    "listen": {
                        "event": "LoanCreditFailedEvent"
                    },
                    "nodes": [
                        "BlacklistCollect"
                    ]
                },
                {
                    "listen": {
                        "event": "ContractSignatureSucceededEvent"
                    },
                    "nodes": [
                        "GuaranteeApply"
                    ]
                },
                {
                    "listen": {
                        "event": "GuaranteeApplySucceededEvent"
                    },
                    "nodes": [
                        "GuaranteeDown"
                    ]
                },
                {
                    "listen": {
                        "event": "GuaranteeDownloadSucceededEvent"
                    },
                    "nodes": [
                        "LoanPostCredit"
                    ]
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
                        "CapitalRepayPlanQuery",
                        "ContractDown",
                        "ElectronicReceiptDown"
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
                        "event": "LoanVoucherApplySuccessEvent"
                    },
                    "nodes": [
                        "ElectronicReceiptDown"
                    ]
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_langfang_hengrun_qj", body)


def update_gbiz_capital_langfang_hengrun_qj_const():
    body = {
        "env": "mock",
        "channel": "KN10001",
        "ftpChannelName": "langfang_hengrun_qj",
        "warrantNo": "R999",
        "projectNo": "hr-knqj-lfyh",
        "bankIdMap":
            {
                "ICBC": "1021",
                "CCB": "1051",
                "BOC": "1041",
                "ABC": "1031",
                "CMB": "3081",
                "SPDB": "3101",
                "CITIC": "3021",
                "HXB": "3041",
                "HXBANK": "3041",
                "CMBC": "30510",
                "GDB": "3061",
                "CIB": "3091",
                "SPABANK": "7832",
                "EGBANK": "31545",
                "BOHAIB": "31811",
                "SHBANK": "3131",
                "BJBANK": "30310",
                "CZBANK": "31633",
                "CZB": "31633"
            },
        "pickupBankIdMap":
            {
                "ICBC": "102100099996",
                "CCB": "105100000017",
                "BOC": "104100000004",
                "ABC": "103100000026",
                "CMB": "308584000013",
                "SPDB": "310290000013",
                "CITIC": "302100011000",
                "HXB": "304100040000",
                "HXBANK": "304100040000",
                "CMBC": "305100000013",
                "GDB": "306581000003",
                "CIB": "309391000011",
                "SPABANK": "307584007998",
                "BOHAIB": "318110000014",
                "SHBANK": "325290000012",
                "BJBANK": "313100000013",
                "EGBANK": "315456000105",
                "CZB": "316331000018",
                "CZBANK": "316331000018"
            },
        "preApplyContractCreateMap":
            {
                "35200":
                    {
                        "filetype": "qjcredit",
                        "postYEscalation": 842,
                        "postXEscalation": 0
                    },
                "35201":
                    {
                        "filetype": "lfcredit",
                        "postYEscalation": 842,
                        "postXEscalation": 0
                    },
                "35202":
                    {
                        "filetype": "lfquery",
                        "postYEscalation": 842,
                        "postXEscalation": 0
                    },
                "35203":
                    {
                        "filetype": "lflimit",
                        "postYEscalation": 842,
                        "postXEscalation": 0
                    }
            },
        "postApplyPushAttachments":
            [
                {
                    "attachmentType": 1,
                    "fileType": "idcardfront",
                    "suffix": "jpg",
                    "remoteDir": "/cpu/KN10001/need"
                },
                {
                    "attachmentType": 2,
                    "fileType": "idcardback",
                    "suffix": "jpg",
                    "remoteDir": "/cpu/KN10001/need"
                },
                {
                    "attachmentType": 29,
                    "fileType": "face",
                    "suffix": "jpg",
                    "remoteDir": "/cpu/KN10001/need"
                },
                {
                    "attachmentType": 35200,
                    "fileType": "qjcredit",
                    "suffix": "pdf",
                    "remoteDir": "/cpu/KN10001/need"
                },
                {
                    "attachmentType": 35201,
                    "fileType": "lfcredit",
                    "suffix": "pdf",
                    "remoteDir": "/cpu/KN10001/need"
                },
                {
                    "attachmentType": 35202,
                    "fileType": "lfquery",
                    "suffix": "pdf",
                    "remoteDir": "/cpu/KN10001/need"
                },
                {
                    "attachmentType": 35203,
                    "fileType": "lflimit",
                    "suffix": "pdf",
                    "remoteDir": "/cpu/KN10001/need"
                }
            ],
        "preLoanConfirmContractCreateMap":
            {
                "35207":
                    {
                        "filetype": "loancount",
                        "postYEscalation": 842,
                        "postXEscalation": 0,
                        "isSigns": "true",
                        "post2YEscalation": 842,
                        "post2XEscalation": 0
                    },
                "35204":
                    {
                        "filetype": "danbaocount",
                        "postYEscalation": 842,
                        "postXEscalation": 0
                    },
                "35205":
                    {
                        "filetype": "deduction",
                        "postYEscalation": 842,
                        "postXEscalation": 0
                    },
                "35206":
                    {
                        "filetype": "danbaoletter",
                        "isSign": False
                    }
            },
        "preLoanConfirmPushAttachments":
            [
                {
                    "attachmentType": 35207,
                    "fileType": "loancount",
                    "suffix": "pdf",
                    "remoteDir": "/cpu/KN10001/need"
                },
                {
                    "attachmentType": 35208,
                    "fileType": "danbaocount",
                    "suffix": "pdf",
                    "remoteDir": "/cpu/KN10001/need"
                },
                {
                    "attachmentType": 35205,
                    "fileType": "deduction",
                    "suffix": "pdf",
                    "remoteDir": "/cpu/KN10001/need"
                },
                {
                    "attachmentType": 35206,
                    "fileType": "danbaoletter",
                    "suffix": "pdf",
                    "remoteDir": "/cpu/KN10001/need"
                }
            ],
        "guaranteeSignatureMap":
            {
                "35204":
                    {
                        "fileType": "DBHT",
                        "signType": "10",
                        "fileFormat": "PDF",
                        "companySignKeyList":
                            [
                                "乙方（盖章）"
                            ],
                        "isContractStorage": True,
                        "fileName": "廊坊恒润亲家-个人贷款委托担保合同-担保方未签章"
                    },
                "35206":
                    {
                        "fileType": "DBH",
                        "signType": "10",
                        "fileFormat": "PDF",
                        "companySignKeyList":
                            [
                                "恒润融资担保有限公司"
                            ],
                        "isContractStorage": False,
                        "fileName": "廊坊恒润亲家-担保函"
                    }
            },
        "guaranteeSignatureDownMap":
            {
                "35208":
                    {
                        "fileType": "DBHT",
                        "signType": "10",
                        "fileFormat": "PDF",
                        "companySignKeyList":
                            [
                                "乙方（盖章）"
                            ],
                        "isContractStorage": True,
                        "fileName": "廊坊恒润亲家-个人贷款委托担保合同.pdf"
                    },
                "35206":
                    {
                        "fileType": "DBH",
                        "signType": "10",
                        "fileFormat": "PDF",
                        "companySignKeyList":
                            [
                                "广西恒润融资担保有限公司"
                            ],
                        "isContractStorage": False,
                        "fileName": "廊坊恒润亲家-担保函.pdf"
                    }
            },
        "guaranteeTypeMap":
            {
                "35208": "35204"
            },
        "loanUseMap":
            {
                "1": "1",
                "2": "2",
                "3": "9",
                "4": "1",
                "5": "4",
                "6": "2",
                "7": "2",
                "8": "2",
                "9": "1"
            },
        "liveStatusMap":
            {
                "0": "9",
                "1": "1",
                "2": "2",
                "3": "3",
                "4": "4",
                "5": "5",
                "6": "6",
                "7": "7"
            },
        "educationMap":
            {
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
        "marriageMap":
            {
                "1": "10",
                "2": "99",
                "3": "40",
                "4": "30"
            },
        "jobMap":
            {
                "0": "Y",
                "1": "2",
                "2": "2",
                "3": "1",
                "4": "3",
                "5": "3",
                "6": "3",
                "7": "7",
                "8": "1",
                "9": "1",
                "10": "4",
                "11": "5",
                "12": "4",
                "13": "5",
                "14": "1",
                "15": "Y"
            },
        "dutyMap":
            {
                "0": "9",
                "1": "1",
                "2": "2",
                "3": "3",
                "4": "3",
                "5": "3",
                "6": "3",
                "7": "3",
                "8": "3",
                "9": "4"
            },
        "degreeMap":
            {
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
        "industryMap":
            {
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
        "jobDetailMap":
            {
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
        "relationMap":
            {
                "0": "O",
                "1": "D",
                "2": "B",
                "3": "H",
                "4": "W",
                "5": "T",
                "6": "Y",
                "7": "O"
            },
        "nationMap": {
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
            "基": "255"
        },
        "cityIps":
            [
                "110000#110.96.0.0-110.127.255.255",
                "120000#219.226.0.0-219.226.255.255",
                "130100#27.128.0.0-27.128.79.255",
                "130200#27.190.0.0-27.191.255.255",
                "130300#106.8.0.0-106.8.63.255",
                "130400#27.188.0.0-27.188.255.255",
                "130500#27.129.192.0-27.129.255.255",
                "130600#27.128.192.0-27.128.207.255",
                "130700#27.129.52.0-27.129.55.255",
                "130800#27.129.60.0-27.129.63.255",
                "130900#106.8.192.0-106.8.255.255",
                "131000#27.128.208.0-27.128.223.255",
                "131100#27.128.115.0-27.128.119.255"
            ],
        "productIdMap":
            {
                "new": "212M1HRLFS1",
                "old": "212M2HRLFS1"
            },
        "contractDownloadMap":
            {
                "28": "01"
            },
        "includeFeesMap":
            {
                "technical_service":
                    [
                        "Q001",
                        "Q002"
                    ]
            },
        "uploadFileInfo": {
            "ftpChannelName": "kuainiu",  # 线上这里要改成线上的
            "path": "/langfang_hengrun_qj/%s/guarantee",
            "fileName": "%s.pdf"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_langfang_hengrun_qj_const", body)
