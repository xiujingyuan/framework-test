import common.global_const as gc


def update_gbiz_capital_daxinganling_zhongyi():
    daxinganling_zhongyi = {
        "manual_reverse_allowed": False,
        "recall_via_ivr_enabled": True,
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "raise_limit_allowed": False,
        "register_config": {
            "account_register_duration": 20,
            "is_strict_seq": False,
            "register_step_list": [
                {
                    "step_type": "PROTOCOL",
                    "channel": "daxinganling_zhongyi",
                    "way": "daxinganling_zhongyi",
                    "interaction_type": "SMS",
                    "status_scene": {
                        "register": {
                            "success_type": "once",
                            "register_status_effect_duration_day": 0,
                            "allow_fail": False,
                            "need_confirm_result": False
                        },
                        "route": {
                            "success_type": "once"
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
        #                 "GrantFailedEvent": "LoanApplyQuery",
        #                 "LoanApplySyncFailedEvent": "LoanApplyQuery",
        #                 "LoanApplyAsyncFailedEvent": "LoanApplyQuery"
        #             }
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
        #                         "messages": [
        #
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
        #                             "遇到再进行配置"
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
        #                         "code": "-10000",
        #                         "messages": [
        #                             "遇到再进行配置"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "AssetImport": {
        #         "execute": {
        #             "loan_validator": [
        #                 {
        #                     "rule": "loan.totalAmount>=cmdb.irr(#loan,'35.98') && #loan.totalAmount<=cmdb.irr(#loan,'36')",
        #                     "err_msg": "大兴安岭中[资产还款总额]不满足 irr36，请关注！"
        #                 }
        #             ]
        #         }
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
        #                         "code": "0",
        #                         "messages": [
        #                             "请求成功"
        #                         ]
        #                     },
        #                     {
        #                         "code": "1",
        #                         "messages": [
        #                             "大兴安岭-中裔\\],订单提交\\(进件\\),返回code=1001,msg=商户订单号重复校验未通过"
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
        #                             "大兴安岭-中裔,订单提交\\(进件\\),返回code=1000,msg=mock 请求失败"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "LoanApplyQuery": {
        #         "init": {
        #             "delay_time": "delaySeconds(30)"
        #         },
        #         "finish": [
        #             {
        #                 "action": {
        #                     "policy": "fail"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "4041",
        #                         "messages": [
        #                             "error_4041_交易失败"
        #                         ]
        #                     },
        #                     {
        #                         "code": "4040",
        #                         "messages": [
        #                             "error_4040_内层mock 失败测试_null"
        #                         ]
        #                     }
        #                 ]
        #             },
        #             {
        #                 "action": {
        #                     "policy": "grantSuccess"
        #                 },
        #                 "matches": [
        #                     {
        #                         "code": "0",
        #                         "messages": [
        #                             "放款成功"
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
        #                         "code": "4040",
        #                         "messages": [
        #                             "error_4040_null_null",
        #                             "error_4040_null_风控审核进行中"
        #                         ]
        #                     }
        #                 ]
        #             }
        #         ]
        #     },
        #     "CapitalRepayPlanQuery": {
        #         "execute": {
        #             "allowance_check_range": {
        #                 "min_value": 0,
        #                 "max_value": 0
        #             },
        #             "allow_diff_due_at": False,
        #             "allow_diff_effect_at": False
        #         }
        #     },
        #     "OurRepayPlanRefine": {
        #         "execute": {
        #             "need_refresh_due_at": False
        #         }
        #     },
        #     "ContractDown": {
        #         "init": {
        #             "delay_time": "delaySeconds(600)"
        #         }
        #     },
        #     "ContractPush": {
        #         "init": {
        #             "delay_time": "delayDays(1,\"08:00:00\")"
        #         }
        #     }
        # }
        "workflow": {
            "title": "大兴安岭中裔流程编排v3",
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
                                    "rule": "loan.totalAmount>=cmdb.irr(#loan,'35.98') && #loan.totalAmount<=cmdb.irr(#loan,'36')",
                                    "err_msg": "大兴安岭中[资产还款总额]不满足 irr36，请关注！"
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
                            "simpleLock": None,
                            "delayTime": "delaySeconds(5)"
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
                                            "请求成功"
                                        ]
                                    },
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
                                    "policy": "fail",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "1",
                                        "messages": [
                                            "大兴安岭-中裔,订单提交\\(进件\\),返回code=1403,msg=属地化经营校验不通过",
                                            "大兴安岭-中裔,订单提交\\(进件\\),返回code=1008,msg=正则校验未通过,校验字段:contactName1",
                                            "大兴安岭-中裔,订单提交\\(进件\\),返回code=1008,msg=正则校验未通过,校验字段:contactMobile1",
                                            "大兴安岭-中裔,订单提交\\(进件\\),返回code=1008,msg=正则校验未通过,校验字段:mobile",
                                            "大兴安岭-中裔,订单提交\\(进件\\),返回code=1000,msg=mock 请求失败"
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
                                "GrantFailedEvent": "LoanApplyQuery",
                                "LoanApplySyncFailedEvent": "LoanApplyQuery",
                                "LoanApplyAsyncFailedEvent": "LoanApplyQuery"
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
                                            "遇到再进行配置"
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
                    "id": "LoanApplyQuery",
                    "type": "LoanApplyQueryTaskHandler",
                    "events": [
                        "LoanApplyAsyncFailedEvent",
                        "GrantSucceededEvent"
                    ],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(30)"
                        },
                        "execute": {},
                        "finish": [
                            {
                                "action": {
                                    "policy": "fail",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "4007",
                                        "messages": [
                                            "error_4007_None_None"
                                        ]
                                    },
                                    {
                                        "code": "4017",
                                        "messages": [
                                            "error_4017_综合信用评分不足_None",
                                            "error_4017_资料内容未通过系统校验_None"
                                        ]
                                    },
                                    {
                                        "code": "4019",
                                        "messages": [
                                            "error_4019_运营计划流量金额不符合_None"
                                        ]
                                    },
                                    {
                                        "code": "4041",
                                        "messages": [
                                            "error_4041_II、III类账户限制_None",
                                            "error_4041_卡状态异常_None",
                                            "error_4041_交易失败_None",
                                            "error_4041_交易不被银行受理_None",
                                            "error_4041_、账户交易金额超限_None",
                                            "error_4041_账户状态异常_None",
                                            "error_4041_户名或卡号错误_None",
                                            "error_4041_交易失败"
                                        ]
                                    },
                                    {
                                        "code": "4040",
                                        "messages": [
                                            "error_4040_内层mock 失败测试_null"
                                        ]
                                    }
                                ]
                            },
                            {
                                "action": {
                                    "policy": "grantSuccess",
                                    "ignoreNotify": False
                                },
                                "matches": [
                                    {
                                        "code": "0",
                                        "messages": [
                                            "放款成功"
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
                                        "code": "4040",
                                        "messages": [
                                            "error_4040_None_风控审核进行中",
                                            "error_4040_None_签约进行中",
                                            "error_4040_None_支付进行中",
                                            "error_4040_None_订单分发进行中"
                                        ]
                                    },
                                    {
                                        "code": "9999",
                                        "messages": [
                                            "error_9999_None_None"
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
                            "allow_diff_effect_at": True,
                            "allowance_check_range": {
                                "min_value": -162,
                                "max_value": 162
                            },
                            "allow_diff_due_at": True
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
                            "need_refresh_due_at": True,
                            "allow_diff_effect_at": True,
                            "allowance_check_range": {
                                "min_value": -162,
                                "max_value": 162
                            },
                            "allow_diff_due_at": True
                        },
                        "finish": []
                    }
                },
                {
                    "id": "CapitalRepayPlanPush",
                    "type": "CapitalRepayPlanPushTaskHandler",
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
                    "id": "ContractDown",
                    "type": "ContractDownTaskHandler",
                    "events": [],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(600)"
                        },
                        "execute": {},
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
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(600)"
                        },
                        "execute": {},
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
                    "memo": "资产就绪成功事件订阅",
                    "listen": {
                        "event": "AssetReadyEvent"
                    },
                    "nodes": [
                        "LoanApplyNew"
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
                        "ChangeCapital"
                    ],
                    "associateData": {
                        "sourceWorkflowNodeId": "LoanApplyQuery",
                        "event": "LoanApplySyncFailedEvent",
                        "skipDoubleCheck": False
                    }
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
                    "memo": "支用查询成功事件订阅",
                    "listen": {
                        "event": "GrantSucceededEvent"
                    },
                    "nodes": [
                        "CapitalRepayPlanQuery"
                    ]
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
                    "memo": "我放还款计划刷新成功事件订阅",
                    "listen": {
                        "event": "OurRepayPlanRefreshHandleSucceededEvent"
                    },
                    "nodes": [
                        "CapitalRepayPlanPush",
                        "ContractDown",
                        "ContractPush"
                    ]
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_daxinganling_zhongyi", daxinganling_zhongyi)


def update_gbiz_capital_daxinganling_zhongyi_const():
    body = {
        "default_protocol_way": "baofoo",
        "product_code": "YMS_M",
        "default_merchant_number": "100025773",
        "traffic_channel_code": "63",
        "bh_grace_days": 3,
        "credit_expire_hour": 36,
        "loan_rate": 0.36,
        # 资方环境不一样，key会不一样，走资方时需要注意
        # key:0u31vlf8jrbdf646 ,token:57e227a1e220b123106c95bc1599c491 url：http://ltapi.wsmtec.com
        # key:2vc82v5ihoslgzjf ,token:85eea623bade4ecf20423a257ca2237e url：https://hwapi.wsmtec.com
        "aes_secret_key1": "0u31vlf8jrbdf646",
        "aes_secret_iv1": "0u31vlf8jrbdf646",
        "aes_secret_key": "2vc82v5ihoslgzjf",
        "aes_secret_iv": "2vc82v5ihoslgzjf",
        "cpm": 102,
        "marriage_map": {
            "0": "1",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4"
        },
        "education_map": {
            "0": "10",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "10": "10"
        },
        "relationship_map": {
            "0": "4",
            "1": "8",
            "2": "8",
            "3": "3",
            "4": "2",
            "5": "4",
            "6": "5",
            "7": "4",
            "8": "1",
            "9": "8"
        },
        "bank_code_map": {
            "ABC": "1002",
            "BOC": "1001",
            "BJBANK": "3002",
            "CCB": "1004",
            "CIB": "2006",
            "CMBC": "2004",
            "CMB": "2005",
            "COMM": "1005",
            "CITIC": "2001",
            "CEB": "2002",
            "GDB": "2007",
            "ICBC": "1003",
            "HXB": "2003",
            "LZYH": "3131",
            "PAB": "2008",
            "PSBC": "1006",
            "SHBANK": "3042",
            "SPDB": "2009",
            "CZBANK": "2011",
            "EGBANK": "2010",
            "BOHAIB": "2012"
        },
        "company_industry_map": {
            "0": 9,
            "1": 1,
            "2": 1,
            "3": 2,
            "4": 2,
            "5": 6,
            "6": 8,
            "7": 6,
            "8": 2,
            "9": 4,
            "10": 4,
            "11": 4,
            "12": 8,
            "13": 4,
            "14": 3,
            "15": 5
        },
        "gender_map": {
            "M": 1,
            "F": 2
        },
        "loan_apply_attachments": [
            1,
            2,
            29
        ],
        "ip_seg_pools": [
            "1.56.0.0-1.63.255.255",
            "123.164.0.0-123.167.255.255",
            "60.14.0.0-60.15.255.255",
            "58.194.0.0-58.195.255.255",
            "60.218.0.0-60.219.255.255",
            "218.10.0.0-218.10.255.255",
            "60.252.0.0-60.252.255.255",
            "61.180.128.0-61.180.255.255",
            "61.47.128.0-61.47.191.255",
            "203.90.192.0-203.90.223.255",
            "202.97.224.0-202.97.231.255",
            "113.0.0.0-113.7.255.255",
            "221.208.0.0-221.211.255.255",
            "175.46.0.0-175.47.255.255",
            "112.98.0.0-112.99.255.255",
            "42.184.0.0-42.185.255.255",
            "221.212.0.0-221.212.255.255",
            "61.167.0.0-61.167.255.255",
            "222.172.0.0-222.172.127.255",
            "61.138.0.0-61.138.63.255",
            "202.97.192.0-202.97.223.255",
            "103.29.128.0-103.29.131.255",
            "112.100.0.0-112.103.255.255",
            "42.100.0.0-42.103.255.255",
            "218.8.0.0-218.9.255.255",
            "114.196.0.0-114.197.255.255",
            "125.211.0.0-125.211.255.255",
            "221.206.0.0-221.206.255.255",
            "221.207.128.0-221.207.255.255",
            "202.118.128.0-202.118.255.255",
            "221.207.64.0-221.207.127.255",
            "203.90.160.0-203.90.191.255",
            "103.2.212.0-103.2.215.255",
            "122.156.0.0-122.159.255.255",
            "1.188.0.0-1.191.255.255",
            "113.8.0.0-113.9.255.255",
            "222.170.0.0-222.171.255.255",
            "218.7.0.0-218.7.255.255",
            "60.11.0.0-60.11.255.255",
            "61.158.0.0-61.158.127.255",
            "125.58.128.0-125.58.255.255",
            "203.90.128.0-203.90.159.255",
            "202.97.240.0-202.97.255.255",
            "103.3.100.0-103.3.103.255"
        ],
        "allow_Address": "黑龙江",
        "industry_category_map": {
            "1": "Z",
            "2": "I",
            "3": "H",
            "4": "K",
            "5": "C",
            "6": "F",
            "7": "N",
            "8": "G",
            "9": "M",
            "10": "R",
            "11": "J",
            "12": "S",
            "13": "R",
            "14": "S",
            "15": "A"
        },
        "push_fee_list": [
            "guarantee",
            "reserve",
            "consult"
        ],
        "ftp_channel_name": "daxinganling_zhongyi",
        "push_contract_list": [
            {
                "path": "/upload/FKSJ/63-YMS_M-contract",
                "date_path_format": "yyyyMMdd",
                "file_suffix": ".pdf",
                "contract_type": "34501"
            }
        ],
        "statement_config": {
            "ftpChannelName": "daxinganling_zhongyi",
            "basePath": "/upload/YWSJ",
            "targetFtpChannelName": "kuainiu",
            "targetFtpBasePath": "/daxinganling_zhongyi/statement",
            "fileConfigList": [
                {
                    "filePrefix": "chargeback_",
                    "subDir": "/FKDZWJ",
                    "businessDateIndex": 9
                },
                {
                    "filePrefix": "loanSuccessful_",
                    "subDir": "/FKDZWJ",
                    "businessDateIndex": 9
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_daxinganling_zhongyi_const", body)
