import common.global_const as gc


def update_gbiz_capital_lanhai_zhongbao_puan():
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
                    "channel": "lanhai_zhongbao_puan",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
                    "sub_way": "baofoo_tq_protocol",
                    "interaction_type": "SMS",
                    "group": "kuainiu",
                    "status_scene": {
                        "register": {
                            "success_type": "once",
                            "allow_fail": False,
                            "need_confirm_result": True,
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
        "workflow": {
            "title": "蓝海中保普安放款流程编排v3",
            "inclusions": [
                "gbiz_capital_workflow_asset"
            ],
            "props": {
                "CapitalRepayPlanProps": {
                    "need_refresh_due_at": False,
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -554,
                        "max_value": 554
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
                                    "rule": "#loan.totalAmount>=cmdb.irr(#loan,'35.99') && #loan.totalAmount<=cmdb.irr(#loan,'36')",
                                    "err_msg": "蓝海中保普安[资产还款总额]不满足 irr36，请关注！"
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
                                        "code": "9999",
                                        "messages": [
                                            "存在授信额度,授信可用额度不足，授信可用金额\\[0.0\\]小于我方进件金额\\[4000.00\\]"
                                        ]
                                    },
                                    {
                                        "code": "0",
                                        "messages": [
                                            "存在授信额度,不需要再次授信",
                                            "不存在授信额度,需要授信申请"
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
                    "events": [
                        "LoanApplySyncSucceededEvent",
                        "LoanApplySyncFailedEvent"
                    ],
                    "activity": {
                        "init": {},
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [
                                    {
                                        "code": "10000",
                                        "messages": [
                                            "遇到再配置"
                                        ]
                                    },
                                    {
                                        "code": "9999",
                                        "messages": [
                                            "1_成功"
                                        ]
                                    }
                                ]
                            },
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "10000",
                                        "messages": [
                                            "0_成功"
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
                            "delayTime": "delayMinutes(10)"
                        },
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [
                                    {
                                        "code": "10000",
                                        "messages": [
                                            ""
                                        ]
                                    },
                                    {
                                        "code": "9999",
                                        "messages": [
                                            "0_成功_04_120000003_授信信息不存在",
                                            "0_成功_02_null_null"
                                        ]
                                    }
                                ]
                            },
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "10000",
                                        "messages": [
                                            "0_成功_03_null_null"
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
                                        "code": "9999",
                                        "messages": [
                                            "0_成功_01_None_None"
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
                            "cancelable": False,
                            "extraExecuteData": {
                                "lockRecordStatus": 3
                            }
                        },
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "20000",
                                        "messages": [
                                            ""
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
                                        "code": "20000",
                                        "messages": [
                                            ""
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
                                    "policy": "fail"
                                },
                                "matches": [
                                    {
                                        "code": "30000",
                                        "messages": [
                                            "0_成功_3_null_null"
                                        ]
                                    }
                                ]
                            },
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "30000",
                                        "messages": [
                                            "0_成功_1_null_null"
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
                            "delayTime": "delaySeconds(200)"
                        },
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [
                                    {
                                        "code": "30000",
                                        "messages": [
                                            ""
                                        ]
                                    },
                                    {
                                        "code": "9999",
                                        "messages": [
                                            "0_成功_4_null_null",
                                            "0_成功_3_null_null"
                                        ]
                                    }
                                ]
                            },
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "30000",
                                        "messages": [
                                            "0_成功_2_null_null"
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
                                        "code": "9999",
                                        "messages": [
                                            "0_成功_1_null_null"
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
                            "delayTime": "delaySeconds(10)"
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
                        "execute": {},
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
                    "memo": "授信额度查询成功",
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
                        "LoanApplyTrial"
                    ],
                    "associateData": {
                        "lockRecordStatus": 3
                    }
                },
                {
                    "memo": "支用前试算成功",
                    "listen": {
                        "event": "LoanApplyTrailSucceededEvent"
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
                    "memo": "授信额度查询失败",
                    "listen": {
                        "event": "LoanPreApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "skipDoubleCheck": True,
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
                    "memo": "同步请款申请失败",
                    "listen": {
                        "event": "ConfirmApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital",
                        "BlacklistCollect"
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
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanhai_zhongbao_puan", body)


def update_gbiz_capital_lanhai_zhongbao_puan_const():
    body = {
        "productId": "XKDPAZB",
        "repayPlanDateFormat": "yyyy-MM-dd",
        "contactRelationMap": {
            "0": "99",
            "1": "1",
            "2": "1",
            "3": "7",
            "4": "3",
            "5": "6",
            "6": "5",
            "7": "99",
            "8": "1",
            "9": "2"
        },
        "genderMap": {
            "m": "1",
            "f": "2"
        },
        "marriageStatusMap": {
            "0": "9",
            "1": "1",
            "2": "2",
            "3": "4",
            "4": "3"
        },
        "creditUploadAttachmentsMap": {
            "1": "1",
            "2": "2",
            "29": "3"
        },
        "creditUploadContractsMap": {
            "37100": "9",
            "37103": "16",
            "37102": "8",
            "37104": "5"
        },
        "loanUploadContractMap": {
            "37105": "6",
            "37106": "11",
            "37107": "12",
            "37108": "15",
            "37101": "7"
        },
        "contractDownLoadMap": {
            "37110": "9",
            "37112": "16",
            "37111": "8",
            "37113": "5",
            "37114": "6",
            "37115": "11",
            "37116": "12",
            "37117": "15",
            "28": "7"
        },
        "educationMap": {
            "0": "99",
            "1": "00",
            "2": "00",
            "3": "10",
            "4": "20",
            "5": "30",
            "6": "30",
            "7": "30",
            "8": "40",
            "9": "40",
            "10": "40"
        },
        "degreeMap": {
            "0": "05",
            "1": "02",
            "2": "03",
            "3": "04",
            "4": "00",
            "5": "00",
            "6": "00",
            "7": "00",
            "8": "00",
            "9": "00",
            "10": "00"
        },
        "industryMap": {
            "0": "U",
            "1": "S",
            "2": "U",
            "3": "P",
            "4": "Q",
            "5": "S",
            "6": "E",
            "7": "C",
            "8": "G",
            "9": "J",
            "10": "O",
            "11": "I",
            "12": "R",
            "13": "O",
            "14": "L",
            "15": "A"
        },
        "positionMap": {
            "0": "999",
            "1": "10",
            "2": "03",
            "3": "03",
            "4": "02",
            "5": "04",
            "6": "04",
            "7": "04",
            "8": "04",
            "9": "999"
        },
        "loanUseMap": {
            "1": "10",
            "3": "03",
            "5": "07",
            "6": "05",
            "8": "10"
        },
        "bankCodeMap": {
            "ICBC": "102",
            "PSBC": "403",
            "ABC": "103",
            "BOC": "104",
            "CCB": "105",
            "COMM": "301",
            "CITIC": "302",
            "CEB": "303",
            "HXBANK": "304",
            "CMBC": "305",
            "GDB": "306",
            "CMB": "308",
            "CIB": "309",
            "SHBANK": "313",
            "SPDB": "310",
            "SPABANK": "307",
            "BJBANK": "3137910"
        },
        "feeTypeList": [
            "technical_service"
        ],
        "ipSegPool": [
            "1.51.144.0-1.51.159.255",
            "1.51.192.0-1.51.255.255",
            "27.209.0.0-27.209.255.25",
            "27.221.96.0-27.221.127.255",
            "36.192.206.0-36.192.207.255",
            "39.64.0.0-39.64.255.255",
            "42.120.220.0-42.120.233.255",
            "42.245.231.0-42.245.231.255",
            "43.238.40.0-43.238.43.255",
            "45.115.156.0-45.115.159.255",
            "49.223.0.0-49.223.191.255",
            "58.58.128.0-58.58.143.255",
            "59.153.68.0-59.153.71.255",
            "60.212.128.0-60.212.255.255",
            "60.235.224.0-60.235.239.255",
            "61.133.103.0-61.133.103.255",
            "61.179.143.0-61.179.143.255",
            "103.53.144.0-103.53.147.255",
            "106.74.245.0-106.74.245.255",
            "110.196.236.0-110.196.251.255",
            "203.93.188.0-203.93.188.31",
            "218.59.240.0-218.59.251.255"
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanhai_zhongbao_puan_const", body)
