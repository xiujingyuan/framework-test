import common.global_const as gc


def update_gbiz_capital_yumin_zhongbao():
    yumin_zhongbao = {
        "manual_reverse_allowed": False,
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "raise_limit_allowed": False,
        "register_config": {
            "register_step_list": [
                {
                    "step_type": "PROTOCOL",
                    "channel": "yumin_zhongbao",
                    "interaction_type": "SMS",
                    "way": "yumin_zhongbao",
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
        #     "AssetImport": {
        #         "execute": {
        #             "loan_validator": [
        #                 {
        #                     "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
        #                     "err_msg": "裕民中保[资产还款总额]不满足 irr24，请关注！"
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
        #                             "0_成功_true,0_成功_true"
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
        #                         "code": "0",
        #                         "messages": [
        #                             "遇到再配"
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
        #                         "code": "10",
        #                         "messages": [
        #                             "成功_Processing"
        #                         ]
        #                     },
        #                     {
        #                         "code": "190001",
        #                         "messages": [
        #                             "999003:网贷-系统-消息已经存在！",
        #                             "999003:网贷-授信-存在有效额度不允许重复申请授信额度！"
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
        #                         "code": "10",
        #                         "messages": [
        #                             "成功_Reject"
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
        #                         "code": "10",
        #                         "messages": [
        #                             "成功_103_003"
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
        #                         "code": "10",
        #                         "messages": [
        #                             "成功_null_001"
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
        #                         "code": "10",
        #                         "messages": [
        #                             "成功_null_002"
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
        #                         "code": "20",
        #                         "messages": [
        #                             "成功_Success_",
        #                             "成功_Processing_"
        #                         ]
        #                     },
        #                     {
        #                         "code": "290001",
        #                         "messages": [
        #                             "999003:网贷-系统-消息已经存在！"
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
        #                         "code": "20",
        #                         "messages": [
        #                             "成功_Fail_失败"
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
        #                         "code": "20",
        #                         "messages": [
        #                             "成功_Success_"
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
        #                         "code": "20",
        #                         "messages": [
        #                             "成功_Fail_失败",
        #                             "成功_Fail_网贷-用信-放款失败！.*"
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
        #                         "code": "20",
        #                         "messages": [
        #                             "成功_Processing_"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
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
        #                         "code": "100998"
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
        #             "delay_time": "delayMinutes(30)",
        #             "simple_lock": {
        #                 "key": "contractdown-ftp",
        #                 "ttlSeconds": 60
        #             }
        #         }
        #     },
        #     "GuaranteeUpload": {
        #         "init": {
        #             "delay_time": "delayMinutes(10)"
        #         }
        #     },
        #     "CertificateApply": {
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
        #     "CertificateDownload": {
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
        #     "AssetAutoImport": {
        #         "init": {
        #             "delay_time": "delayMinutes(120)"
        #         }
        #     },
        #     "LoanCreditCancel": {
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "success"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "30",
        #                         "messages": [
        #                             "成功_true"
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
        #                         "code": "30",
        #                         "messages": [
        #                             "遇到再配"
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
        #                         "code": "390001",
        #                         "messages": [
        #                             "遇到再配置"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     }
        # }
        "workflow": {
            "title": "裕民中保流程编排v3",
            "inclusions": [
                "gbiz_capital_workflow_asset"
            ],
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
                                    "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                                    "err_msg": "裕民中保[资产还款总额]不满足 irr24，请关注！"
                                }
                            ]
                        },
                        "finish": [

                        ]
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
                        "execute": {

                        },
                        "finish": [

                        ]
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
                        "execute": {

                        },
                        "finish": [

                        ]
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
                            "cancelable": True
                        },
                        "execute": {

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
                                            "0_成功_True,0_成功_True",
                                            "0_成功_true,0_成功_true"
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
                                            "遇到再配"
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
                                        "code": "0",
                                        "messages": [
                                            "0_成功_True,90000_未知错误 HV000116.*",
                                            "90000_未知错误 HV000116:The object to be validated must not be None.*",
                                            "90000_未知错误 HV000116: The object to be validated must not be None.*"
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
                                        "messages": [

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
                                            "遇到再配置"
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
                        "execute": {

                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "10",
                                        "messages": [
                                            "成功_Processing"
                                        ]
                                    },
                                    {
                                        "code": "190001",
                                        "messages": [
                                            "999003:您在我行有存量授信或授信正在审批中，请结清后或稍后再试!",
                                            "999003:网贷-系统-消息已经存在！",
                                            "999003:网贷-授信-存在有效额度不允许重复申请授信额度！",
                                            "异常情况 999003:网贷-系统-消息已经存在！.*",
                                            "异常情况 999003:您在我行有存量授信或授信正在审批中，请结清后或稍后再试!.*",
                                            "异常情况 999003:网贷-系统-消息已经存在！.*",
                                            "异常情况 999003:网贷-授信-存在有效额度不允许重复申请授信额度！.*"

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
                                        "code": "10",
                                        "messages": [
                                            "成功_Reject"
                                        ]
                                    },
                                    {
                                        "code": "190001",
                                        "messages": [
                                            "异常情况 999002:网贷-系统-参数不正确！【详情】身份证号号码有误!.*",
                                            "异常情况 999002:网贷-系统-参数不正确！【详情】身份证已过期!.*",
                                            "异常情况 100001:身份证证件正面照ocr识别失败.*",
                                            "异常情况 100001:身份证证件反面照ocr识别失败.*",
                                            "异常情况 100005:图像上传失败.*",
                                            "异常情况 100001:身份证正面ocr识别检测出告警信息,身份证PS告警.*",
                                            "异常情况 100001:身份证反面ocr识别检测出告警信息,身份证PS告警.*",
                                            "异常情况 100003:证件信息不正确，请修改后再试.*",
                                            "异常情况 100001:身份证反面ocr识别检测出告警信息,身份证复印件告警.*",
                                            "异常情况 100001:身份证正面ocr识别检测出告警信息,身份证复印件告警.*",
                                            "异常情况 999003:网贷-授信-存在有效额度不允许重复申请授信额度！.*",
                                            "异常情况 200001:联网核查人像失败，请重新提交审核或联系银行客服.*",
                                            "异常情况 100002:身份证已过期，不允许开通电子账户.*",
                                            "异常情况 100001:身份证影像审核未通过，请重新提交审核。",
                                            "异常情况 200001:联网核查人像失败，请重新提交审核。",
                                            "异常情况 100001:身份证日期信息验证失败。",
                                            "参数错误 \\[homeAddress max length 60\\]。",
                                            "异常情况 100001:图片上传失败，图片数据HTTP发送fastdfs异常。.*",
                                            "异常情况 999002:【contactInfo\\[0\\].mobileNo】联系人手机号格式有误!。"
                                        ]
                                    },
                                    {
                                        "code": "110002",
                                        "messages": [
                                            "参数错误 \\[contactAddress max length 60\\]",
                                            "参数错误 \\[homeAddress max length 60\\].*",
                                            "参数错误 \\[contactAddress max length 60\\]。",
                                            "参数错误 \\[nation is empty\\].*"
                                        ]
                                    },
                                    {
                                        "code": "190100",
                                        "messages": [
                                            "存在有效额度 不允许重复授信。"
                                        ]
                                    },
                                    {
                                        "code": "190000",
                                        "messages": [
                                            "数据问题导致资方无法落库"
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
                                        "code": "190001",
                                        "messages": [
                                            "异常情况 连接远程服务异常:Read timed out。",
                                            "异常情况 连接远程服务异常:Connection reset。",
                                            "异常情况 999003:抱歉，接口熔断了！。"
                                        ]
                                    },
                                    {
                                        "code": "190000",
                                        "messages": [
                                            "未知错误 HV000116.*"
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
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(120)"
                        },
                        "execute": {

                        },
                        "finish": [

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
                        "execute": {

                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "10",
                                        "messages": [
                                            "成功_103_003"
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
                                        "code": "10",
                                        "messages": [
                                            "成功_None_001"
                                        ]
                                    },
                                    {
                                        "code": "290001",
                                        "messages": [
                                            "W000002:timeout_返回业务data为空"
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
                                        "code": "10",
                                        "messages": [
                                            "成功_null_002",
                                            "成功_返回业务数据为空",
                                            "\\[裕民-中保\\]资产\\[.*\\]授信结果查询，返回的结果列表中不包含已成功的授信流水号且不包含本次申请流水号\\[.*\\]，返回第一条结果：成功_None_00.*"
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
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "manual",
                            "cancelable": False
                        },
                        "execute": {

                        },
                        "finish": [

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
                        "execute": {

                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "20",
                                        "messages": [
                                            "成功_Success_",
                                            "成功_Processing_"
                                        ]
                                    },
                                    {
                                        "code": "290001",
                                        "messages": [
                                            "999003:网贷-用信-借款金额不符合要求！",
                                            "异常情况 999003:网贷-用信-借款金额不符合要求！.*",
                                            "999003:网贷-系统-消息已经存在！",
                                            "异常情况 999003:网贷-系统-消息已经存在！.*"
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
                                        "code": "20",
                                        "messages": [
                                            "成功_Fail_失败"
                                        ]
                                    },
                                    {
                                        "code": "290001",
                                        "messages": [
                                            "异常情况 借款场景下:授信状态不合法->实际状态REJECT ==资方异常，先不配",
                                            "999003:他行还款卡不可为空",
                                            "异常情况 未找到用户的绑卡信息。"
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
                        "execute": {

                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "20",
                                        "messages": [
                                            "成功_Success_"
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
                                        "code": "20",
                                        "messages": [
                                            "成功_Fail_失败",
                                            "成功_Fail_网贷-用信-放款失败！.*"
                                            "成功_Fail_收款账户当年累计交易金额超过收款行限制",
                                            "成功_Fail_网贷-用信-放款失败！【详情】esb 调用【核心系统】贷款开户及放款失败或返回错误，错误信息RB4005 \\[999912",
                                            "成功_Fail_网贷-用信-放款失败！【详情】esb 调用【核心系统】贷款开户及放款失败或返回错误，错误信息协议发送数据失败",
                                            "\\[裕民-中保\\]资产\\[.*\\]放款结果查询，返回的结果列表中不包含当前资产，返回第一条结果成功_Fail_网贷-用信-借款金额不符合要求！",
                                            "成功_Fail_已超过单日最大交易总额",
                                            "成功_Fail_收款账户余额超限",
                                            "成功_Fail_银行拒绝交易，请联系发卡行",
                                            "\\[裕民-中保\\]资产\\[.*\\]放款结果查询，返回的结果列表中不包含当前资产，返回第一条结果成功_Fail_抱歉，接口熔断了！",
                                            "成功_Fail_交易失败",
                                            "成功_Fail_网贷-用信-放款失败！【详情】扣款失败",
                                            "成功_Fail_网贷-用信-放款失败！【详情】疑似重复提交订单",
                                            "成功_Fail_扣款失败",
                                            "成功_Fail_II/III类账户年累计存款限额超限",
                                            "成功_Fail_交易处理中",
                                            "成功_Fail_银行账户状态异常，请联系银行",
                                            "成功_Fail_个人日常消费_卡状态异常",
                                            "成功_Fail_个人日常消费_II、III类账户限制",
                                            "成功_Fail_个人日常消费II.III类账户限制",
                                            "成功_Fail_II.III类账户超限",
                                            "成功_Fail_SUCCESS!",
                                            "成功_Fail_无此交易关单",
                                            "成功_Fail_风险等级过高",
                                            "成功_Fail_个人日常消费_交易风险过高",
                                            "成功_Fail_交易信息不存在",
                                            "成功_Fail_网贷-用信-支用端风控拒绝！",
                                            ".*放款结果查询，返回的结果列表中不包含当前资产，返回第一条结果成功_Fail_【核心系统】还款计划试算返回：数据拆包失败",
                                            "成功_Fail_网贷-用信-电子合同-签章失败！",
                                            "成功_Fail_网贷-用信-借款金额不符合要求！",
                                            "成功_Fail_账户状态为挂失",
                                            "成功_Fail_【核心系统】还款计划试算返回：协议发送数据失败",
                                            "成功_Fail_本次交易超过最大金额限制，请联系您的发卡行",
                                            "成功_Fail_抱歉，接口熔断了！",
                                            "成功_Fail_MB3025 负债类余额\\[.*\\]不足\\[.*\\]，不允许进行借记记账处理！",
                                            "成功_Fail_网贷-用信-放款失败！【详情】esb 调用【核心系统】贷款开户及放款失败或返回错误，错误信息RC5012 账号/证件号："
                                        ]
                                    },
                                    {
                                        "code": "290001",
                                        "messages": [
                                            "异常情况 根据放款流水号找不到放款记录。_返回业务数据为空",
                                            "999003:网贷-用信-申请信息不存在！_返回业务数据为空"
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
                                        "code": "20",
                                        "messages": [
                                            "成功_Processing_"
                                        ]
                                    },
                                    {
                                        "code": "90000",
                                        "messages": [
                                            "Required request body is missing.*"
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
                            "allow_diff_effect_at": False,
                            "allowance_check_range": {
                                "min_value": -1106,
                                "max_value": 1106
                            },
                            "allow_diff_due_at": False
                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "ContractDown",
                    "type": "ContractDownTaskHandler",
                    "events": [
                        "ContractDownSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": {
                                "limitCount": 0,
                                "ttlSeconds": 60,
                                "key": "contractdown-ftp"
                            },
                            "delayTime": "delayMinutes(30)"
                        },
                        "execute": {
                            "interval_in_minutes": "240"
                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "ContractPush",
                    "type": "ContractPushTaskHandler",
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(10)"
                        },
                        "execute": {

                        },
                        "finish": [

                        ]
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
                            "need_refresh_due_at": False
                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "GuaranteeUpload",
                    "type": "GuaranteeUploadTaskHandler",
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(10)"
                        },
                        "execute": {

                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "GuaranteeApply",
                    "type": "GuaranteeApplyTaskHandler",
                    "events": [

                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False
                        },
                        "execute": {

                        },
                        "finish": [

                        ]
                    }
                },
                {
                    "id": "CertificateApplySync",
                    "type": "CertificateApplyVerifySyncTaskHandler",
                    "events": [
                        "CertificateApplyReadyEvent"
                    ],
                    "activity": {
                        "init": {

                        }
                    }
                },
                {
                    "id": "CertificateApply",
                    "type": "CertificateApplyTaskHandler",
                    "events": [
                        "CertificateApplySuccessEvent"
                    ],
                    "activity": {
                        "init": {

                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "0"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "CertificateDownload",
                    "type": "CertificateDownloadTaskHandler",
                    "events": [

                    ],
                    "activity": {
                        "execute": {
                            "interval_in_minutes": "240"
                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "0"
                                    }
                                ]
                            }
                        ]
                    }
                },
                {
                    "id": "AssetChangeNoticeTask",
                    "type": "AssetChangeNoticeTaskHandler",
                    "events": [
                        "AssetSettledEvent"
                    ],
                    "activity": {
                        "init": {

                        }
                    }
                },
                {
                    "id": "LoanCreditCancel",
                    "type": "LoanCreditCancelTaskHandler",
                    "events": [
                    ],
                    "activity": {
                        "init": {

                        },
                        "finish": [
                            {
                                "action": {
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "30",
                                        "messages": [
                                            "成功_true"
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
                                        "code": "30",
                                        "messages": [
                                            "遇到再配"
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
                                        "code": "390001",
                                        "messages": [
                                            "遇到再配置"
                                        ]
                                    }
                                ]
                            }
                        ]
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
                    "memo": "资产就绪成功事件订阅",
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
                    "memo": "资产进件前任务成功事件订阅",
                    "listen": {
                        "event": "LoanPreApplySyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyNew"
                    ]
                },
                {
                    "memo": "资产进件失败事件订阅",
                    "listen": {
                        "event": "LoanPreApplySyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": None,
                        "event": "LoanPreApplySyncFailedEvent",
                        "skipDoubleCheck": True
                    }
                },
                {
                    "memo": "资产进件成功事件订阅",
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
                        "ChangeCapital",
                        "BlacklistCollect"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": "LoanApplyQuery",
                        "event": "LoanApplySyncFailedEvent",
                        "skipDoubleCheck": True
                    }
                },
                {
                    "memo": "资产进件查询成功事件订阅",
                    "listen": {
                        "event": "LoanApplyAsyncSucceededEvent"
                    },
                    "nodes": [
                        "LoanApplyConfirm"
                    ]
                },
                {
                    "memo": "资产进件查询失败事件订阅",
                    "listen": {
                        "event": "LoanApplyAsyncFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital",
                        "BlacklistCollect"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": "LoanApplyQuery",
                        "event": "LoanApplyAsyncFailedEvent",
                        "skipDoubleCheck": True
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
                    "memo": "支用查询失败事件订阅",
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
                    "memo": "支用查询成功事件订阅",
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
                    "memo": "支用查询失败事件订阅",
                    "listen": {
                        "event": "GrantFailedEvent"
                    },
                    "nodes": [
                        "ChangeCapital",
                        "BlacklistCollect"
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
                },
                {
                    "memo": "合同下载成功事件订阅",
                    "listen": {
                        "event": "ContractDownSucceededEvent"
                    },
                    "nodes": [
                        "GuaranteeUpload",
                        "GuaranteeApply"
                    ]
                },
                {
                    "memo": "结清证明准备",
                    "listen": {
                        "event": "CertificateApplyReadyEvent",
                        "matches": [

                        ]
                    },
                    "nodes": [
                        "CertificateApply"
                    ]
                },
                {
                    "memo": "结清证明申请成功",
                    "listen": {
                        "event": "CertificateApplySuccessEvent",
                        "matches": [

                        ]
                    },
                    "nodes": [
                        "CertificateDownload"
                    ]
                },
                {
                    "memo": "结清后取消授信",
                    "listen": {
                        "event": "AssetSettledEvent",
                        "matches": [

                        ]
                    },
                    "nodes": [
                        "LoanCreditCancel"
                    ]
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yumin_zhongbao", yumin_zhongbao)


def update_gbiz_capital_yumin_zhongbao_const():
    body = {
        "openIdPrefix": "KN_",
        "productCode": "kn_ym_dd",
        "cardPreBindType": "OPEN_ACCOUNT",
        "loanApplyCodePrefix": "1",
        "loanConfirmCodePrefix": "2",
        "idType": 1,
        "houseSituation": 9,
        "imageMaxSize": 1048476,
        "grtAgrmFlg": "1",
        "loanFreq": "0",
        "unionBillFlag": "Y",
        "repaymentMethod": "01",
        "assetType": "CL",
        "payType": "AP",
        "isDcSign": "Y",
        "systemFlag": "30010001",
        "idCardLongTime": "2099-12-31",
        "applCdeDateFormat": "yyyyMMddHH",
        "loanDateFormat": "yyyyMMddHHmmss",
        "rateYear": 0.24,
        "capitalFtpChannelName": "yumin_zhongbao",
        "marriedValue": 2,
        "mateRelationValue": 0,
        "contractConfig": {
            "openAccount": {
                "00": "33503"
            },
            "applyCredit": {
                "04": "33502",
                "05": "33501"
            },
            "loan": {
                "19": "28"
            }
        },
        "occupationMap": {
            "1": "4",
            "2": "4",
            "3": "4",
            "4": "4 ",
            "5": "6",
            "6": "4",
            "7": "6",
            "8": "4",
            "9": "2",
            "10": "2",
            "11": "2",
            "12": "4",
            "13": "2",
            "14": "1",
            "15": "5"
        },
        "subOccupationMap": {
            "1": "04010",
            "2": "04003",
            "3": "04001",
            "4": "04006",
            "5": "06011",
            "6": "04002",
            "7": "06010",
            "8": "04004",
            "9": "02005",
            "10": "02008",
            "11": "02006",
            "12": "04007",
            "13": "02002",
            "14": "01002",
            "15": "05001"
        },
        "industryTypeMap": {
            "1": "O",
            "2": "H",
            "3": "F",
            "4": "K",
            "5": "C",
            "6": "G",
            "7": "D",
            "8": "I",
            "9": "Q",
            "10": "P",
            "11": "J",
            "12": "L",
            "13": "R",
            "14": "S",
            "15": "A"
        },
        "educationMap": {
            "1": "80",
            "2": "70",
            "3": "60",
            "4": "50",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "10",
            "9": "00"
        },
        "maritalStatusMap": {
            "1": "10",
            "2": "20",
            "3": "40",
            "4": "30"
        },
        "nationMap": {
            "汉": "01",
            "满": "02",
            "侗": "03",
            "瑶": "04",
            "白": "05",
            "土家": "06",
            "哈尼": "07",
            "哈萨克": "08",
            "傣": "09",
            "黎": "10",
            "傈僳": "11",
            "佤": "12",
            "畲": "13",
            "高山": "14",
            "拉祜": "15",
            "水": "16",
            "东乡": "17",
            "纳西": "18",
            "景颇": "19",
            "柯尔克孜": "20",
            "土": "21",
            "达斡尔": "22",
            "仫佬": "23",
            "羌": "24",
            "布朗": "25",
            "撒拉": "26",
            "毛难": "27",
            "仡佬": "28",
            "锡伯": "29",
            "阿昌": "30",
            "普米": "31",
            "塔吉克": "32",
            "怒": "33",
            "乌孜别克": "34",
            "俄罗斯": "35",
            "鄂温克": "36",
            "崩龙": "37",
            "保安": "38",
            "裕固": "39",
            "京": "40",
            "塔塔尔": "41",
            "独龙": "42",
            "鄂伦春": "43",
            "赫哲": "44",
            "门巴": "45",
            "珞巴": "46",
            "基诺": "47",
            "蒙古": "48",
            "回": "49",
            "藏": "50",
            "维吾尔": "51",
            "苗": "52",
            "彝": "53",
            "壮": "54",
            "布依": "55",
            "朝鲜": "56",
            "外国血统中国籍人士": "98",
            "其他": "99"
        },
        "techPostMap": {
            "1": "3",
            "2": "1",
            "3": "3",
            "4": "9",
            "5": "4",
            "6": "4"
        },
        "companyTypeMap": {
            "1": "900",
            "2": "900",
            "3": "900",
            "4": "900",
            "5": "900",
            "6": "900",
            "7": "900",
            "8": "900",
            "9": "200",
            "10": "200",
            "11": "900",
            "12": "900",
            "13": "900",
            "14": "100",
            "15": "900"
        },
        "relationshipMap": {
            "0": "1",
            "1": "2",
            "2": "5",
            "3": "3",
            "4": "4",
            "5": "9",
            "6": "6",
            "7": "9"
        },
        "loanPurposeMap": {
            "1": "9",
            "2": "9",
            "3": "9",
            "4": "9",
            "5": "11",
            "6": "9",
            "7": "9",
            "8": "9",
            "9": "9"
        },
        "gpsPool": [
            "115.89,28.68,10",
            "114.92,25.85,10",
            "115.97,29.71,10",
            "117.97,28.47,10",
            "114.97,27.12,10",
            "117.22,29.3,10",
            "114.38,27.81,10",
            "116.34,28,10",
            "113.85,27.6,10",
            "114.92,27.81,10",
            "117.02,28.23,10"
        ],
        "creditTermMap": {
            "6": "000600",
            "12": "010000"
        },
        "uploadContractConfig": [
            {
                "contractType": "33506",
                "baseDir": "/kn/knFile/upfile/yumin/downfile/images",
                "fileNamePrefix": "guarantee_letter",
                "fileNameSuffix": ".pdf"
            },
            {
                "contractType": "33505",
                "baseDir": "/kn/knFile/upfile/yumin/downfile/images",
                "fileNamePrefix": "guarantee_contract",
                "fileNameSuffix": ".pdf"
            },
            {
                "contractType": "33504",
                "baseDir": "/kn/knFile/upfile/yumin/downfile/zzr",
                "fileNamePrefix": "ZZR_KN",
                "fileNameSuffix": ".pdf"
            }
        ],
        "guaranteeConfig": {
            "channelDir": "/upload/zb",
            "partnerNo": "KN",
            "productName": "快牛",
            "applyStatus": "S",
            "cfundChannelNo": "KN-YMBK",
            "cfundChannelName": "中保-快牛-裕民银行",
            "payWay": "02",
            "repayWay": "01",
            "yearRate": "0.24",
            "actYearRate": "0.24",
            "periodServiceRate": "0.1619",
            "ointRate": None,
            "validPass": "Y",
            "lendStatus": "S",
            "idCardType": "01",
            "dateFormat": "yyyyMMdd",
            "normalLoanStatus": "NOR",
            "productNo": "YMZB",
            "annualIncome": "B20205",
            "industry": "B1003",
            "relation": "90",
            "loanUse": "07",
            "serviceFeeTypes": ["technical_service"],
            "guaranteeFeeTypes": [],
            "contractUploadConfig": {
                "fileName": "contract",
                "remoteDir": "/contract",
                "subFilesConfigMap": {
                    "28": {
                        "name": "loan",
                        "extension": "pdf"
                    },
                    "33500": {
                        "name": "draw",
                        "extension": "pdf"
                    },
                    "33505": {
                        "name": "commission_guarantee",
                        "extension": "pdf"
                    },
                    "33506": {
                        "name": "guarantee",
                        "extension": "pdf"
                    }
                }
            }
        },
        "guaranteeFeeFileConfig": {
            "baseDir": "/kn/knFile/upfile/yumin/downfile",
            "contractBaseDir": "/kn/knFile/upfile/yumin/downfile/images",
            "zzrBaseDir": "/kn/knFile/upfile/yumin/downfile/zzr",
            "fileNameDateFormat": "yyyyMMdd",
            "replenishItemNoList": [],
            "updateItemNoList": [],
            "prefix": "repayment_plan"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yumin_zhongbao_const", body)
