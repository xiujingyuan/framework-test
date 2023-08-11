import common.global_const as gc


def update_gbiz_capital_lanhai_zhongbao_rl():
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
                    "channel": "lanhai_zhongbao_rl",
                    "step_type": "PROTOCOL",
                    "way": "lanhai_zhongbao_rl",
                    "interaction_type": "SMS",
                    "status_scene": {
                        "register": {
                            "success_type": "once",
                            "register_status_effect_duration_day": 180,
                            "allow_fail": False,
                            "need_confirm_result": False,
                            "post_register": True
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
            "title": "蓝海中保润楼流程编排v3",
            "inclusions": [
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
            "nodes": [{
                "id": "AssetImport",
                "type": "AssetImportTaskHandler",
                "events": [
                    "AssetImportSucceededEvent"
                ],
                "activity": {
                    "init": {},
                    "execute": {
                        "loan_validator": [{
                            "rule": "loan.totalAmount==cmdb.irrv2(#loan,'35.99')",
                            "err_msg": "蓝海中保润楼[资产还款总额]不满足 irr35.99，请关注！"
                        }]
                    }
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
                        "execute": {}
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
                            "returnMsg": "执行进件前校验",
                            "cancelable": True,
                            "delayTime": "delaySeconds(60)"
                        },
                        "execute": {}
                    }
                },
                {
                    "id": "ChangeCapital",
                    "type": "ChangeCapitalTaskHandler",
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
                        "finish": [{
                            "action": {
                                "policy": "success"
                            },
                            "matches": [{
                                "code": "0",
                                "messages": [
                                    "切资方路由\\(二次\\)成功"
                                ]
                            }]
                        },
                            {
                                "action": {
                                    "policy": "finalFail"
                                },
                                "matches": [{
                                    "code": "12",
                                    "messages": []
                                }]
                            },
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [{
                                    "code": "1",
                                    "messages": [
                                        "遇到在配置"
                                    ]
                                }]
                            },
                            {
                                "action": {
                                    "policy": "retry"
                                },
                                "matches": [{
                                    "code": "100998"
                                }]
                            }
                        ]
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
                        "execute": {},
                        "finish": [{
                            "action": {
                                "policy": "success"
                            },
                            "matches": [{
                                "code": "0",
                                "messages": [
                                    "授信环节影像文件资料上传成功"
                                ]
                            }]
                        },
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [{
                                    "code": "19999",
                                    "messages": [
                                        "遇到再配置"
                                    ]
                                }]
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
                        "finish": [{
                            "action": {
                                "policy": "success"
                            },
                            "matches": [{
                                "code": "1",
                                "messages": [
                                    "0_Success_P",
                                    "E1000003_相同业务申请已存在"
                                ]
                            }]
                        },
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [{
                                    "code": "1",
                                    "messages": [
                                        "0_Success_F"
                                    ]
                                }]
                            }
                        ]
                    }
                },
                {
                    "id": "LoanApplyQuery",
                    "type": "LoanApplyQueryTaskHandler",
                    "events": [
                        "LoanApplyAsyncFailedEvent",
                        "LoanApplyAsyncSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "delayTime": "delaySeconds(60)"
                        },
                        "execute": {},
                        "finish": [{
                            "action": {
                                "policy": "success"
                            },
                            "matches": [{
                                "code": "1",
                                "messages": [
                                    "0_Success_S_null",
                                    "0_Success_R_重复授信"
                                ]
                            }]
                        },
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [{
                                    "code": "1",
                                    "messages": [
                                        "E2000001_授信申请不存在",
                                        "0_Success_F_null",
                                        "0_Success_S_null_当前日期不在授信有效期内",
                                        "0_Success_S_null_剩余授信额度小于借款本金"
                                    ]
                                }]
                            },
                            {
                                "action": {
                                    "policy": "retry"
                                },
                                "matches": [{
                                    "code": "1",
                                    "messages": [
                                        "0_Success_P_null"
                                    ]
                                }]
                            }
                        ]
                    }
                },
                {
                    "id": "PostRegisterNotify",
                    "type": "PostRegisterNotifyBizPerformer",
                    "events": [
                        "PostRegisterNotifySuccessEvent"
                    ],
                    "activity": {
                        "init": {},
                        "execute": {}
                    }
                },
                {
                    "id": "CheckAccountStatus",
                    "type": "CheckAccountStatusTaskHandler",
                    "events": [
                        "CapitalAccountCheckSuccessEvent",
                        "CapitalAccountCheckFailEvent"
                    ],
                    "activity": {
                        "init": {},
                        "execute": {}
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
                        "init": {},
                        "execute": {},
                        "finish": [{
                            "action": {
                                "policy": "success"
                            },
                            "matches": [{
                                "code": "0",
                                "messages": [
                                    "用信环节影像文件资料上传成功"
                                ]
                            }]
                        },
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [{
                                    "code": "19999",
                                    "messages": [
                                        "遇到再配置"
                                    ]
                                }]
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
                        "finish": [{
                            "action": {
                                "policy": "success"
                            },
                            "matches": [{
                                "code": "2",
                                "messages": [
                                    "E1000003_相同业务申请已存在",
                                    "0_Success_P"
                                ]
                            }]
                        },
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [{
                                    "code": "2",
                                    "messages": [
                                        "0_Success_F"
                                    ]
                                }]
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
                            "delayTime": "delaySeconds(120)"
                        },
                        "execute": {},
                        "finish": [{
                            "action": {
                                "policy": "success"
                            },
                            "matches": [{
                                "code": "2",
                                "messages": [
                                    "0_成功_10000_null_null_200",
                                    "0_Success_S_S",
                                    "0_Success_S_null"
                                ]
                            }]
                        },
                            {
                                "action": {
                                    "policy": "fail"
                                },
                                "matches": [{
                                    "code": "2",
                                    "messages": [
                                        "0_Success_F_null"
                                    ]
                                }]
                            },
                            {
                                "action": {
                                    "policy": "retry"
                                },
                                "matches": [{
                                    "code": "2",
                                    "messages": [
                                        "0_Success_P_null"
                                    ]
                                }]
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
                        "init": {},
                        "execute": {
                            "props_key": "CapitalRepayPlanProps"
                        }
                    }
                },
                {
                    "id": "ContractDown",
                    "type": "ContractDownTaskHandler",
                    "events": [
                        "ContractDownSucceededEvent"
                    ],
                    "activity": {
                        "execute": {
                            "interval_in_minutes": "240"
                        },
                        "init": {
                            "delayTime": "delayMinutes(10)",
                            "simpleLock": {
                                "key": "contractdown-changyin",
                                "ttlSeconds": 10
                            }
                        }
                    }
                },
                {
                    "id": "GuaranteeUpload",
                    "type": "GuaranteeUploadTaskHandler",
                    "events": [],
                    "activity": {
                        "init": {},
                        "execute": {}
                    }
                },
                {
                    "id": "GuaranteeApply",
                    "type": "GuaranteeApplyTaskHandler",
                    "events": [],
                    "activity": {
                        "init": {},
                        "execute": {}
                    }
                },
                {
                    "id": "OurRepayPlanRefine",
                    "type": "OurRepayPlanRefineTaskHandler",
                    "events": [
                        "OurRepayPlanRefreshHandleSucceededEvent"
                    ],
                    "activity": {
                        "init": {},
                        "execute": {
                            "props_key": "CapitalRepayPlanProps"
                        }
                    }
                },
                {
                    "id": "AssetAutoImport",
                    "type": "AssetAutoImportTaskHandler",
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(90)"
                        },
                        "execute": {

                        },
                        "finish": [

                        ]
                    }
                }
            ],
            "subscribers": [{
                "memo": "资产导入就绪事件订阅",
                "listen": {
                    "event": "AssetImportReadyEvent",
                    "matches": []
                },
                "nodes": [
                    "AssetImport"
                ]
            },
                {
                    "memo": "资产导入成功事件订阅",
                    "listen": {
                        "event": "AssetImportSucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "AssetImportVerify"
                    ]
                },
                {
                    "memo": "资产进件核心参数校验成功事件订阅",
                    "listen": {
                        "event": "AssetImportVerifySucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "ApplyCanLoan"
                    ]
                },
                {
                    "memo": "资产就绪失败事件订阅",
                    "listen": {
                        "event": "AssetCanLoanFailedEvent",
                        "matches": []
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
                    "memo": "资产就绪成功事件订阅",
                    "listen": {
                        "event": "AssetReadyEvent",
                        "matches": []
                    },
                    "nodes": [
                        "LoanPreApply"
                    ]
                },
                {
                    "memo": "资产进件前任务失败事件订阅",
                    "listen": {
                        "event": "LoanPreApplySyncFailedEvent",
                        "matches": []
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
                    "memo": "资产进件前任务成功事件订阅",
                    "listen": {
                        "event": "LoanPreApplySyncSucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "LoanApplyNew"
                    ]
                },
                {
                    "memo": "资产进件失败事件订阅",
                    "listen": {
                        "event": "LoanApplySyncFailedEvent",
                        "matches": []
                    },
                    "nodes": [
                        "ChangeCapital",
                        "BlacklistCollect"
                    ],
                    "associateData": {
                        "skipDoubleCheck": False,
                        "event": "LoanApplySyncFailedEvent",
                        "sourceWorkflowNodeId": "LoanApplyQuery"
                    }
                },
                {
                    "memo": "资产进件成功事件订阅",
                    "listen": {
                        "event": "LoanApplySyncSucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "LoanApplyQuery"
                    ]
                },
                {
                    "memo": "资产进件查询失败事件订阅",
                    "listen": {
                        "event": "LoanApplyAsyncFailedEvent",
                        "matches": []
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
                    "memo": "资产进件查询成功事件订阅",
                    "listen": {
                        "event": "LoanApplyAsyncSucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "PostRegisterNotify"
                    ]
                },
                {
                    "memo": "通知后置开户成功事件订阅",
                    "listen": {
                        "event": "PostRegisterNotifySuccessEvent",
                        "matches": []
                    },
                    "nodes": [
                        "CheckAccountStatus"
                    ]
                },
                {
                    "memo": "用户开户失败事件订阅",
                    "listen": {
                        "event": "CapitalAccountCheckFailEvent",
                        "matches": []
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "skipDoubleCheck": True,
                        "event": "CapitalAccountCheckFailEvent"
                    }
                },
                {
                    "memo": "用户开户成功事件订阅",
                    "listen": {
                        "event": "CapitalAccountCheckSuccessEvent",
                        "matches": []
                    },
                    "nodes": [
                        "LoanPostApply"
                    ]
                },
                {
                    "memo": "资产进件后任务失败事件订阅",
                    "listen": {
                        "event": "LoanPostApplyFailedEvent",
                        "matches": []
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
                    "memo": "资产进件后任务成功事件订阅",
                    "listen": {
                        "event": "LoanPostApplySucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "LoanApplyConfirm"
                    ]
                },
                {
                    "memo": "支用申请失败事件订阅",
                    "listen": {
                        "event": "ConfirmApplySyncFailedEvent",
                        "matches": []
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
                    "memo": "支用申请成功事件订阅",
                    "listen": {
                        "event": "ConfirmApplySyncSucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "LoanConfirmQuery"
                    ]
                },
                {
                    "memo": "支用查询失败事件订阅",
                    "listen": {
                        "event": "GrantFailedEvent",
                        "matches": []
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "skipDoubleCheck": False,
                        "event": "GrantFailedEvent",
                        "sourceWorkflowNodeId": "LoanConfirmQuery"
                    }
                },
                {
                    "memo": "支用查询成功事件订阅",
                    "listen": {
                        "event": "GrantSucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "CapitalRepayPlanQuery",
                        "ContractDown"
                    ]
                },
                {
                    "memo": "合同下载成功事件订阅",
                    "listen": {
                        "event": "ContractDownSucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "GuaranteeUpload",
                        "GuaranteeApply"
                    ]
                },
                {
                    "memo": "还款计划查询成功事件订阅",
                    "listen": {
                        "event": "RepayPlanHandleSucceededEvent",
                        "matches": []
                    },
                    "nodes": [
                        "OurRepayPlanRefine"
                    ]
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanhai_zhongbao_rl", body)


def update_gbiz_capital_lanhai_zhongbao_rl_const():
    body = {
        "assetPackageNo": "APB5ALF23PL",
        "objectKeyPrefix": "kuainiu-test",
        "ftpChannel": "lanhai_zhongbao_rl",
        "guarRate": "15.08",
        "creditRate": "24",
        "rate": "8.9",
        "dueDayMethod": "1",
        "businessRiskPrice": "24",
        "fileChannel": "85bb80c91e71730f932727cc843ce3cc",
        "country": "01",
        "userAccessSuccessStatus": [
            "01"
        ],
        "ipPool": [
            "58.14.0.0-58.15.255.255",
            "60.217.192.0-60.217.255.255",
            "60.232.128.0-60.233.255.255",
            "112.36.128.0-112.36.255.255",
            "113.125.0.0-113.129.27.255",
            "39.87.224.0-39.89.255.255",
            "60.209.0.0-60.209.255.255",
            "112.225.0.0-112.226.255.255",
            "123.234.0.0-123.235.255.255",
            "116.154.0.0-116.154.127.255",
            "222.134.64.0-222.134.159.255",
            "182.46.64.0-182.46.127.255",
            "182.34.128.0-182.34.255.255",
            "60.214.96.0-60.214.159.255",
            "112.239.0.0-112.239.127.255",
            "112.248.0.0-112.248.255.255",
            "112.253.64.0-112.253.95.255",
            "58.194.192.0-58.194.215.255",
            "60.212.0.0-60.212.127.255",
            "60.215.160.0-60.215.223.255",
            "60.217.0.0-60.217.0.255",
            "60.217.2.0-60.217.3.255",
            "112.237.0.0-112.238.255.255",
            "112.249.0.0-112.249.255.255",
            "113.121.0.0-113.121.63.255"
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
            },
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/credit-pbc-protocol.pdf",
                "contractNoExpr": "#{#record.assetItemNo}",
                "code": "5",
                "type": "35601"
            },
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/credit-person-protocol.pdf",
                "contractNoExpr": "#{#record.assetItemNo}",
                "code": "6",
                "type": "35602"
            },
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/credit-contract.pdf",
                "contractNoExpr": "#{#record.identifier}ST",
                "code": "8",
                "type": "35607"
            },
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/borrower-statement.pdf",
                "contractNoExpr": "#{#record.assetItemNo}",
                "code": "29",
                "type": "35603"
            }
        ],
        "preLoanImageConfig": [
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/loan-contract.pdf",
                "contractNoExpr": "#{#record.assetItemNo}",
                "code": "7",
                "type": "35604"
            },
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/credit-guarantee-authorization.pdf",
                "contractNoExpr": "#{#record.assetItemNo}WT",
                "code": "9",
                "type": "35608"
            },
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/withdrawProtocal.pdf",
                "contractNoExpr": "#{#record.assetItemNo}",
                "code": "10",
                "type": "35606"
            },
            {
                "fileNameDirExpr": "#{#record.assetItemNo}/guarantee-letter.pdf",
                "contractNoExpr": "#{#record.assetItemNo}",
                "code": "13",
                "type": "35605"
            }
        ],
        "contractDownConfig": [
            {
                "contractType": "35609",
                "ftpPathExpr": "/writable/aggregation/cash/in/#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_8_#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}_#{#record.tradeNo}.pdf"
            },
            {
                "contractType": "28",
                "ftpPathExpr": "/writable/aggregation/cash/in/#{T(DateUtil).format(#record.finishAt, 'yyyyMMdd')}",
                "fileNameExpr": "10000202212985_7_#{T(DateUtil).format(#record.finishAt, 'yyyyMMdd')}_#{#record.dueBillNo}.pdf"
            }
        ],
        "guarAmountTranTypes": [
            "technical_service"
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
            "08",
            "403",
            "40100"
        ],
        "incomeMap": {
            "0-2000": "1",
            "2001-3000": "1",
            "3001-5000": "1",
            "5001-8000": "1",
            "8001-12000": "1",
            "12000-0": "1"
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
            "3": "001",
            "4": "099",
            "5": "099",
            "6": "099",
            "7": "099",
            "8": "099",
            "9": "099"
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
            "3": "001",
            "4": "099",
            "5": "099",
            "6": "099",
            "7": "099",
            "8": "099",
            "9": "099"
        },
        "gpsCode": "370000",
        "gpsIpsMap": {
            "370000": ["111.17.133.231", "218.56.37.66", "112.237.192.65", "221.0.112.108", "222.173.97.97",
                       "39.134.144.62", "61.156.54.227", "210.12.171.198", "223.99.214.160", "210.82.240.199"
                       ]
        },
        "guaranteeConfig": {
            "channelDir": "/upload/dfkn/zb/lhbk/dljt",
            "partnerNo": "ZB-KN",
            "productName": "快牛-蓝海-大连",
            "applyStatus": "S",
            "cfundChannelNo": "ZB-KN-LHBK-DLJT",
            "cfundChannelName": "中保-快牛-蓝海银行-大连金投",
            "payWay": "02",
            "repayWay": "01",
            "yearRate": "0.36",
            "actYearRate": "0.089",
            "periodGuaranteeRate": "0.271",
            "ointRate": "0",
            "validPass": "Y",
            "lendStatus": "S",
            "idCardType": "01",
            "dateFormat": "yyyyMMdd",
            "normalLoanStatus": "NOR",
            "productNo": "KNLHDL",
            "annualIncome": "B20205",
            "industry": "B1003",
            "relation": "90",
            "loanUse": "07",
            "serviceFeeTypes": [],
            "guaranteeFeeTypes": [
                "technical_service"
            ],
            "contractUploadConfig": {
                "fileName": "contract",
                "remoteDir": "/contract",
                "subFilesConfigMap": {
                    "28": {
                        "name": "loan",
                        "extension": "pdf"
                    },
                    "35606": {
                        "name": "draw",
                        "extension": "pdf"
                    },
                    "35608": {
                        "name": "commission_guarantee",
                        "extension": "pdf"
                    },
                    "35601": {
                        "name": "credit",
                        "extension": "pdf"
                    },
                    "35602": {
                        "name": "person",
                        "extension": "pdf"
                    }
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanhai_zhongbao_rl_const", body)
