import common.global_const as gc


def update_gbiz_capital_zhongyuan_haoyue_rl():
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
                    "channel": "zhongyuan_haoyue_rl",
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
            ]
        },
        "workflow": {
            "title": "中原昊悦润楼流程编排v3",
            "inclusions": [
                "gbiz_capital_workflow_asset"
            ],
            "props": {
                "CapitalRepayPlanProps": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -1,
                        "max_value": 1
                    },
                    "adjust_fee_list": [
                        "consult", "reserve"
                    ]
                }
            },
            "nodes": [
                {
                    "id": "AssetImport",
                    "type": "AssetImportTaskHandler",
                    "activity": {
                        "init": {},
                        "execute": {
                            "loan_validator": [
                                {
                                    "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.3') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                                    "err_msg": "中原昊悦润楼[资产还款总额]不满足 irr24，请关注！"
                                }
                            ]
                        }
                    }
                },
                {
                    "id": "AssetAutoImport",
                    "type": "AssetAutoImportTaskHandler",
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
                                            "授信环节影像文件资料上传成功"
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
                                        "code": "1",
                                        "messages": [
                                            "0_Success_P",
                                            "E1000003_相同业务申请已存在"
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
                                            "0_Success_F"
                                        ]
                                    }
                                ]
                            }
                        ]
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
                                        "code": "1",
                                        "messages": [
                                            "0_Success_S_null"
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
                                            "0_Success_F_null"
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
                                        "code": "1",
                                        "messages": [
                                            "0_Success_P_null"
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
                                            "0_Success_S"
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
                                        "code": "0",
                                        "messages": [
                                            "0_Success_F"
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
                                            "0_Success_P"
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
                                            "0_Success_F"
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
                                            "0_Success_S_null"
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
                                            "E2000001_借款申请不存在",
                                            "0_Success_F_null"
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
                                            "0_Success_P_null"
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
                                "key": "contractdown-changyin"
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
                        "LoanPreApply"
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
                        "event": "AssetCanLoanFailedEvent",
                        "skipDoubleCheck": True
                    }
                },
                {
                    "listen": {
                        "event": "LoanPreApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyNew"
                    ]
                },
                {
                    "listen": {
                        "event": "LoanPreApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "event": "LoanPreApplySyncFailedEvent",
                        "skipDoubleCheck": True
                    }
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
                        "event": "LoanApplySyncFailedEvent",
                        "skipDoubleCheck": False,
                        "sourceWorkflowNodeId": "LoanApplyQuery"
                    }
                },
                {
                    "listen": {
                        "event": "LoanApplySyncFailedEvent"
                    },
                    "nodes": [
                        "BlacklistCollect"
                    ]
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
                        "event": "LoanApplyAsyncFailedEvent",
                        "skipDoubleCheck": False,
                        "sourceWorkflowNodeId": "LoanApplyQuery"
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
                    "listen": {
                        "event": "LoanPostApplyFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "event": "LoanPostApplyFailedEvent",
                        "skipDoubleCheck": True,
                        "sourceWorkflowNodeId": "LoanApplyQuery"
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
                        "event": "ConfirmApplySyncFailedEvent",
                        "skipDoubleCheck": False,
                        "sourceWorkflowNodeId": "LoanConfirmQuery"
                    }
                },
                {
                    "listen": {
                        "event": "GrantSucceededEvent"
                    },
                    "nodes": [
                        "CapitalRepayPlanQuery",
                        "ContractDown",
                        "ContractPush"
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
                        "event": "GrantFailedEvent",
                        "skipDoubleCheck": False,
                        "sourceWorkflowNodeId": "LoanConfirmQuery"
                    }
                },
                {
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
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongyuan_haoyue_rl", body)


def update_gbiz_capital_zhongyuan_haoyue_rl_const():
    body = {
        "assetPackageNo": "AD0LIXWWO9C",
        "objectKeyPrefix": "kuainiu-test",
        "ftpChannel": "zhongyuan_haoyue_rl",
        "guarRate": "0.16",
        "creditRate": "0.24",
        "rate": "0.08",
        "dueDayMethod": "1",
        "businessRiskPrice": "0.24",
        "fileBaseDir": "/writable/aggregation/cash/out",
        "repayPlanFilePrefix": "repayPlan_10000202212985",
        "loanDetailFilePrefix": "loan_10000202212985",
        "fileChannel": "1a8367992210622dbdea6be43803e2aa",
        "adjustLastPeriodRateNumber": "zyhyrl_12m_20230704",
        "bucketKey": "rl-obs",
        "bucket": "zhongyuan_haoyue_rl_obs",
        "userAccessSuccessStatus": [
            "01",
            "02",
            "03"
        ],
        "preCreditImageConfig": [
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/idCardFront.jpg",
                "code": "1",
                "type": "1"
            },
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/idCardBack.jpg",
                "code": "2",
                "type": "2"
            },
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/faceRecognition.jpg",
                "code": "3",
                "type": "29"
            }
        ],
        "rdContractType": 35608,
        "loanSuccessContractUploadConfig": [
            {
                "contractType": 35608,
                "ftpPathExpr": "/writable/aggregation/cash/out/#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_9_#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}_#{#record.tradeNo}.pdf"
            }
        ],
        "guarAmountTranTypes": [
            "consult", "reserve"
        ],
        "deviceMap": {
            "PC": 1,
            "ANDROID": 2,
            "IOS": 3,
            "H5": 4,
            "API": 5
        },
        "nationMap": {
            "汉": "00",
            "蒙古": "01",
            "回": "02",
            "藏": "03",
            "维吾尔": "04",
            "苗": "05",
            "彝": "06",
            "壮": "07",
            "布依": "08",
            "朝鲜": "09",
            "满": "10",
            "侗": "11",
            "瑶": "12",
            "白": "13",
            "土家": "14",
            "哈尼": "15",
            "哈萨克": "16",
            "傣": "17",
            "黎": "18",
            "傈僳": "19",
            "佤": "20",
            "畲": "21",
            "高山": "22",
            "拉祜": "23",
            "水": "24",
            "东乡": "25",
            "纳西": "26",
            "景颇": "27",
            "柯尔克孜": "28",
            "土": "29",
            "达斡尔": "30",
            "仫佬": "31",
            "羌": "32",
            "布朗": "33",
            "撒拉": "34",
            "毛南": "35",
            "仡佬": "36",
            "锡伯": "37",
            "阿昌": "38",
            "普米": "39",
            "塔吉克": "40",
            "怒": "41",
            "乌孜别克": "42",
            "俄罗斯": "43",
            "鄂温克": "44",
            "德昂": "45",
            "保安": "46",
            "裕固": "47",
            "京": "48",
            "塔塔尔": "49",
            "独龙": "50",
            "鄂伦春": "51",
            "赫哲": "52",
            "门巴": "53",
            "珞巴": "54",
            "基诺": "55",
            "其它": "56",
            "外国血统中国籍人士": "57"
        },
        "scoreMap": {
            "A": "850",
            "B": "615",
            "C": "500",
            "D": "350"
        },
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
        "genderMap": {
            "m": "1",
            "f": "2"
        },
        "marriageMap": {
            "1": "10",
            "2": "20",
            "3": "40",
            "4": "30"
        },
        "eduLevelMap": {
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8"
        },
        "occupationList": [
            "0800",
            "403",
            "40100"
        ],
        "incomeMap": {
            "0-2000": "1",
            "2001-3000": "1",
            "3001-5000": "1",
            "5001-8000": "2",
            "8001-12000": "4",
            "12000-0": "4"
        },
        "contactTypeMap": {
            "0": "02",
            "1": "01",
            "2": "03",
            "3": "04",
            "4": "08",
            "5": "07",
            "6": "05",
            "7": "99"
        },
        "productUseMap": {
            "1": "099",
            "2": "099",
            "4": "099",
            "7": "099",
            "3": "001",
            "5": "005",
            "6": "099",
            "8": "099"
        },
        "industryMap": {
            "1": "O",
            "2": "L",
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
        "purposeNatureMap": {
            "1": "099",
            "2": "099",
            "4": "099",
            "7": "099",
            "3": "001",
            "5": "005",
            "6": "099",
            "8": "099"
        },
        "adjustFeeList": ["consult","reserve"],
        "contractDownConfig": [
            {
                "contractType": "28",
                "ftpPathExpr": "/writable/aggregation/cash/in/#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_7_#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}_#{#record.dueBillNo}.pdf"
            },
            {
                "contractType": "37200",
                "ftpPathExpr": "/writable/aggregation/cash/in/#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_5_#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}_#{#record.tradeNo}.pdf"
            },
            {
                "contractType": "37201",
                "ftpPathExpr": "/writable/aggregation/cash/in/#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_8_#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}_#{#record.tradeNo}.pdf"
            },
            {
                "contractType": "37202",
                "ftpPathExpr": "/writable/aggregation/cash/in/#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_6_#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}_#{#record.tradeNo}.pdf"
            },
            {
                "contractType": "37203",
                "ftpPathExpr": "/writable/aggregation/cash/in/#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_10_#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}_#{#record.tradeNo}.pdf"
            },
            {
                "contractType": "37204",
                "ftpPathExpr": "/writable/aggregation/cash/in/#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_26_#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}_#{#record.tradeNo}.pdf"
            },
            {
                "contractType": "37207",
                "ftpPathExpr": "/writable/aggregation/cash/in/#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_13_#{T(DateUtil).format(#record.grantAt, 'yyyyMMdd')}_#{#record.tradeNo}.pdf"
            }
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongyuan_haoyue_rl_const", body)
