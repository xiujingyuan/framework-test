import common.global_const as gc


def update_gbiz_capital_jinmeixin_hanchen_jf():
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
                    "channel": "jinmeixin_hanchen_jf",
                    "interaction_type": "SMS",
                    "post_register": False,
                    "way": "jinmeixin_hanchen_jf",
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
        #   "ChangeCapital": {
        #     "execute": {
        #       "event_handler_map": {
        #         "LoanApplySyncFailedEvent": "LoanApplyQuery",
        #         "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
        #         "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
        #         "GrantFailedEvent": "LoanConfirmQuery"
        #       },
        #       "can_change_capital": True
        #     },
        #     "finish": [
        #       {
        #         "action": {
        #           "policy": "success"
        #         },
        #         "matches": [
        #           {
        #             "code": "0",
        #             "messages": [
        #               "切资方路由\\(二次\\)成功"
        #             ]
        #           }
        #         ]
        #       },
        #       {
        #         "action": {
        #           "policy": "finalFail"
        #         },
        #         "matches": [
        #           {
        #             "code": "12"
        #           }
        #         ]
        #       },
        #       {
        #         "action": {
        #           "policy": "fail"
        #         },
        #         "matches": [
        #           {
        #             "code": "1",
        #             "messages": [
        #               "资方二次校验失败：未命中\\[fail,updateCard\\]策略.*"
        #             ]
        #           }
        #         ]
        #       },
        #       {
        #         "action": {
        #           "policy": "retry"
        #         },
        #         "matches": [
        #           {
        #             "code": ""
        #           }
        #         ]
        #       }
        #     ]
        #   },
        #   "AssetImport": {
        #     "execute": {
        #       "loan_validator": [
        #         {
        #           "rule": "#loan.totalAmount > cmdb.irrv2(#loan,'23.99') && #loan.totalAmount <= cmdb.irrv2(#loan,'24')",
        #           "err_msg": "金美信汉辰京发[资产还款总额]不满足 【irr23.99，irr24】请关注！"
        #         }
        #       ]
        #     }
        #   },
        #   "LoanPreApply": {
        #     "finish": [
        #       {
        #         "action": {
        #           "policy": "success"
        #         },
        #         "matches": [
        #           {
        #             "code": "0"
        #           }
        #         ]
        #       }
        #     ]
        #   },
        #   "LoanApplyNew": {
        #     "init": {
        #       "delay_time": "delaySeconds(5)"
        #     },
        #     "finish": [
        #       {
        #         "action": {
        #           "policy": "fail"
        #         },
        #         "matches": [
        #             {
        #                 "code": "1000000",
        #                 "messages": [
        #                     "03-mock请求失败"
        #                 ]
        #             },
        #             {
        #                 "code": "9999",
        #                 "messages": [
        #                     "授信可用余额小于资产本金",
        #                     "授信额度已过期"
        #                 ]
        #             }
        #         ]
        #       },
        #       {
        #         "action": {
        #           "policy": "success"
        #         },
        #         "matches": [
        #           {
        #             "code": "1000000",
        #              "messages": [
        #               "01-请求成功",
        #               "01-请勿重复提交-请求成功"
        #             ]
        #           }
        #         ]
        #       }
        #     ]
        #   },
        #   "LoanApplyQuery": {
        #     "init": {
        #       "delay_time": "delaySeconds(2)"
        #     },
        #     "finish": [
        #       {
        #         "action": {
        #           "policy": "fail"
        #         },
        #         "matches": [
        #           {
        #             "code": "9999",
        #               "messages": [
        #                   "授信金额小于资产本金",
        #                   "授信额度已过期"
        #               ]
        #           },
        #           {
        #               "code": "1000000",
        #               "messages": [
        #                     "03-mock请求失败"
        #                 ]
        #             }
        #         ]
        #       },
        #       {
        #         "action": {
        #           "policy": "retry"
        #         },
        #         "matches": [
        #          {
        #             "code": "1000000",
        #             "messages": [
        #               "01-请求成功"
        #             ]
        #           }
        #         ]
        #       },
        #       {
        #         "action": {
        #           "policy": "success"
        #         },
        #         "matches": [
        #           {
        #             "code": "1000000",
        #             "messages": [
        #                   "02-请求成功"
        #               ]
        #           }
        #         ]
        #       }
        #     ]
        #   },
        #    "LoanPostApply": {
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
        #   "LoanApplyConfirm": {
        #     "finish": [
        #       {
        #         "action": {
        #           "policy": "fail"
        #         },
        #         "matches": [
        #           {
        #             "code": "2000000",
        #               "messages": [
        #                   "03-审批拒绝"
        #               ]
        #           }
        #         ]
        #       },
        #       {
        #         "action": {
        #           "policy": "success"
        #         },
        #         "matches": [
        #           {
        #             "code": "2000000",
        #           "messages": [
        #               "01-请求成功"
        #               ]
        #           }
        #         ]
        #       }
        #     ]
        #   },
        #   "LoanConfirmQuery": {
        #     "init": {
        #       "delay_time": "delaySeconds(10)"
        #     },
        #     "finish": [
        #       {
        #         "action": {
        #           "policy": "retry"
        #         },
        #         "matches": [
        #             {
        #               "code": "2000000",
        #               "messages": [
        #                     "01-请求成功"
        #                 ]
        #             }
        #         ]
        #       },
        #       {
        #         "action": {
        #           "policy": "fail"
        #         },
        #         "matches": [
        #           {
        #             "code": "2000000",
        #               "messages": [
        #                   "03-请求成功",
        #                   "03-00007-资方审批不通过-请求成功",
        #                   "03-00006-用信审批不通过-请求成功"
        #               ]
        #           }
        #         ]
        #       },
        #       {
        #         "action": {
        #           "policy": "success"
        #         },
        #         "matches": [
        #           {
        #             "code": "2000000",
        #             "messages": [
        #               "02-请求成功"
        #             ]
        #           }
        #         ]
        #       }
        #     ]
        #   },
        #   "ContractPush": {
        #     "init": {
        #       "delay_time": "delaySeconds(60)"
        #     }
        #   },
        #   "CapitalRepayPlanQuery": {
        #     "execute": {
        #       "diff_effect_at": False,
        #       "diff_due_at": False,
        #       "allowance_check_range": {
        #             "min_value": 0,
        #             "max_value": 0
        #         }
        #     }
        #   },
        #   "OurRepayPlanRefine": {
        #     "execute": {
        #       "need_refresh_due_at": False
        #     }
        #   },
        #   "ContractDown": {
        #     "init": {
        #       "delay_time": "delaySeconds(60)"
        #     }
        #   },
        #     "AssetAutoImport": {
        #         "init": {
        #             "delay_time": "delayMinutes(90)"
        #         }
        #     }
        # }
        "workflow": {
            "title": "金美信汉辰京发放  款流程编排v3",

            "inclusions": [
                "gbiz_capital_workflow_asset"
            ],
            "props": {
                "CapitalRepayPlanProps": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": True,
                    "need_refresh_due_at": True,
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
                        "init": {
                            "executeType": "auto",
                            "cancelable": False
                        },
                        "execute": {
                            "loan_validator": [
                                {
                                    "rule": "#loan.totalAmount > cmdb.irrv2(#loan,'23.99') && #loan.totalAmount <= cmdb.irrv2(#loan,'24')",
                                    "err_msg": "金美信汉辰京发[资产还款总额]不满足 【irr23.99，irr24】请关注！"
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
                                        "messages": []
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
                                            "资方二次校验失败：未命中\\[fail,updateCard\\]策略.*"
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
                                        "code": "",
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
                                        "code": "1000000",
                                        "messages": [
                                            "01-请求成功",
                                            "03-请勿重复提交-请求成功",
                                            "03-用户已存在有效授信记录-请求成功",
                                            "00-请勿重复提交-请求成功",
                                            "02-请勿重复提交-请求成功",
                                            "成功查询到有效额度",
                                            "01-请勿重复提交-请求成功"
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
                                            "03-该用户30天内有授信申请被拒绝，不能再次申请-请求成功",
                                            "03-其他拒绝-请求成功",
                                            "03-mock请求失败"
                                        ]
                                    },
                                    {
                                        "code": "1106",
                                        "messages": [
                                            "nation 民族不能为空: None"
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
                            "delayTime": "delaySeconds(2)"
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
                                            "02-请求成功"
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
                                            "01-请求成功",
                                            "00-请求成功"
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
                                        "code": "9999",
                                        "messages": [
                                            "授信金额小于资产本金",
                                            "授信额度已过期"
                                        ]
                                    },
                                    {
                                        "code": "1000000",
                                        "messages": [
                                            "03-00001-不符合准入条件-请求成功",
                                            "03-00001,00004-信用记录不足,不符合准入条件-请求成功",
                                            "03-00003-涉嫌欺诈规则-请求成功",
                                            "03-99999-其他拒绝-请求成功",
                                            "03-00004-信用记录不足-请求成功",
                                            "03-请求成功",
                                            "03-00002-身份验证不通过-请求成功",
                                            "03-其他拒绝-请求成功",
                                            "03-00014-用户已存在有效授信记录-请求成功",
                                            "03-00002,00003-身份验证不通过,涉嫌欺诈规则-请求成功",
                                            "None-00012-查不到申请记录-请求成功",
                                            "03-mock请求失败"
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
                                        "code": "0",
                                        "messages": [
                                            "文件上传成功"
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
                                        "code": "2000000",
                                        "messages": [
                                            "01-请求成功"
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
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(10)"
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
                                            "02-请求成功"
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
                                            "01-请求成功"
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
                                            "03-00006-申请审批不通过-请求成功",
                                            "03-00004-信用记录不足-请求成功",
                                            "03-00003-涉嫌欺诈规则-请求成功",
                                            "03-00007-资方审批不通过-请求成功",
                                            "03-00003,00006-申请审批不通过,涉嫌欺诈规则-请求成功",
                                            "03-99999-其他拒绝-请求成功",
                                            "03-请求成功"
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
                    "id": "ContractPush",
                    "type": "ContractPushTaskHandler",
                    "events": [],
                    "activity": {
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delaySeconds(60)"
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
                            "delayTime": "delayMinutes(60)"
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
                        "sourceWorkflowNodeId": None,
                        "event": "AssetCanLoanFailedEvent",
                        "skipDoubleCheck": False
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
                        "sourceWorkflowNodeId": None,
                        "event": "LoanPreApplySyncFailedEvent",
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
                        "sourceWorkflowNodeId": "LoanConfirmQuery",
                        "event": "GrantFailedEvent",
                        "skipDoubleCheck": False
                    }
                },
                {
                    "listen": {
                        "event": "GrantFailedEvent"
                    },
                    "nodes": [
                        "BlacklistCollect"
                    ]
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
                        "ContractDown"
                    ]
                }
            ]

        }}

    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jinmeixin_hanchen_jf", body)


def update_gbiz_capital_jinmeixin_hanchen_jf_const():
    body = {
        "acctType": "DEBIT",
        "repayMethod": "2",
        "sumRateFee": 0.24,
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
            "未知": "00"
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
        "loanOKFilesMap": [
            "_contract.pdf.ok",
            "_policy_protocol.pdf.ok"
        ],
        "pushFilePath": "/upload/kuainiu/imgfiles/",
        "fileDateFormat": "yyyyMMdd",
        "capitalFtpChannelName": "jingfa",
        "downFilePath": "/download/kuainiu/imgfiles/",
        "downContractMap": {
            "28": "_contract.pdf",
            "33806": "_policy_protocol.pdf",
            "33807": "_policy.pdf"
        },
        "loanPushContractMap": {
            "33800": "_contract.pdf",
            "33805": "_policy_protocol.pdf"
        },
        "beforeLoanPushContractMap": {
            "33801": "_comprehensive_power_attorney.pdf",
            "33802": "_commissioned_deduction_agreement_1.pdf",
            "33803": "_commissioned_deduction_agreement_2.pdf"
        },
        "creditPushContractMap": {
            "33804": "_financial_information_power_attorney.pdf"
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
                    "type": "comprehensive_power_attorney",
                    "fileName": "_comprehensive_power_attorney.pdf"
                },
                {
                    "type": "commissioned_deduction_agreement_2",
                    "fileName": "_commissioned_deduction_agreement_2.pdf"
                },
                {
                    "type": "commissioned_deduction_agreement_1",
                    "fileName": "_commissioned_deduction_agreement_1.pdf"
                },
                {
                    "type": "contract",
                    "fileName": "_contract.pdf"
                },
                {
                    "type": "policy_protocol",
                    "fileName": "_policy_protocol.pdf"
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
        "imageMaxAllowSize": 1572864,
        "contractTypeCode": 33800,
        "repayDateFormat": "yyyyMMdd",
        "defaultLoanPurpose": "9",
        "defaultMarriage": "1",
        "defaultEducation": "4",
        "defaultIndustry": "12",
        "defaultPosition": "4",
        "customerType": "0",
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
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jinmeixin_hanchen_jf_const", body)
