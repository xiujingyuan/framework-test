import common.global_const as gc


# def update_gbiz_capital_haier_changtai_old():
#     body = {
#               "cancelable_task_list": [
#                 "ApplyCanLoan",
#                 "LoanPreApply",
#                 "LoanApplyNew",
#                 "ChangeCapital"
#               ],
#               "manual_reverse_allowed": False,
#               "raise_limit_allowed": False,
#               "register_config": {
#                 "account_register_duration": 20,
#                 "is_multi_account_card_allowed": True,
#                 "is_strict_seq": True,
#                 "post_register": False,
#                 "ref_accounts": None,
#                 "register_step_list": [
#                   {
#                     "channel": "haier_changtai",
#                     "step_type": "PAYSVR_PROTOCOL",
#                     "way": "tq",
#                     "sub_way": "baofoo_tq_protocol",
#                     "interaction_type": "SMS",
#                     "group": "kuainiu",
#                     "allow_fail": False,
#                     "need_confirm_result": True,
#                     "actions": [
#                       {
#                         "allow_fail": False,
#                         "type": "GetSmsVerifyCode"
#                       },
#                       {
#                         "allow_fail": False,
#                         "type": "CheckSmsVerifyCode"
#                       }
#                     ]
#                   }
#                 ]
#               },
#               "task_config_map": {
#                 "ChangeCapital": {
#                   "execute": {
#                     "event_handler_map": {
#                       "LoanApplySyncFailedEvent": "LoanApplyQuery",
#                       "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
#                       "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
#                       "GrantFailedEvent": "LoanConfirmQuery"
#                     },
#                     "can_change_capital": True
#                   },
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "0",
#                           "messages": [
#                             "切资方路由\\(二次\\)成功"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "finalFail"
#                       },
#                       "matches": [
#                         {
#                           "code": "12",
#                           "messages": []
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "1",
#                           "messages": [
#                             "遇到在配置"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "retry"
#                       },
#                       "matches": [
#                         {
#                           "code": "100998"
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "AssetImport": {
#                   "execute": {
#                     "loan_validator": [
#                       {
#                         "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.99') && #loan.totalAmount<=cmdb.irr(#loan,'24.6')",
#                         "err_msg": "海尔昌泰[资产还款总额]不满足 irr24，请关注！"
#                       }
#                     ]
#                   }
#                 },
#                 "LoanPreApply": {
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "10000",
#                           "messages": [
#                             "00000_处理成功_00000_成功_null_null"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "10000",
#                           "messages": [
#                             "00000_处理成功_00001_mock内层失败_null_null"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "LoanApplyNew": {
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "0",
#                           "messages": [
#                             "进件申请成功"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "LoanApplyQuery": {
#                   "init": {
#                     "delay_time": "delaySeconds(60)"
#                   },
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "0",
#                           "messages": [
#                             "进件查询成功"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "9999",
#                           "messages": [
#                             "遇到配置"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "retry"
#                       },
#                       "matches": [
#                         {
#                           "code": "9999",
#                           "messages": [
#                             "遇到在配置"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "LoanPostApply": {
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "0",
#                           "messages": [
#                             "支用前文件上传成功"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "9999",
#                           "messages": [
#                             "遇到再配置"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "retry"
#                       },
#                       "matches": [
#                         {
#                           "code": "9999",
#                           "messages": [
#                             "遇到配置"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "LoanApplyConfirm": {
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "20000",
#                           "messages": [
#                             "00000_处理成功_0_null_处理中"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "20000",
#                           "messages": [
#                             "00000_处理成功_-1_LA333_mock支用申请失败"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "LoanConfirmQuery": {
#                   "init": {
#                     "delay_time": "delaySeconds(120)"
#                   },
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "20000",
#                           "messages": [
#                             "00000_处理成功_1_null_已放款"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "20000",
#                           "messages": [
#                             "00000_处理成功_-1_LA666_mock支用查询失败",
#                             "00001_mock外层失败_1_null_已放款"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "retry"
#                       },
#                       "matches": [
#                         {
#                           "code": "20000",
#                           "messages": [
#                             "00000_处理成功_0_null_处理中"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "CapitalRepayPlanQuery": {
#                   "execute": {
#                     "allow_diff_effect_at": False,
#                     "allow_diff_due_at": False,
#                     "allowance_check_range": {
#                       "min_value": 0,
#                       "max_value": 0
#                     }
#                   }
#                 },
#                 "OurRepayPlanRefine": {
#                   "execute": {
#                     "need_refresh_due_at": False
#                   }
#                 },
#                 "ContractDown": {
#                   "execute": {
#                     "interval_in_minutes": "240"
#                   },
#                   "init": {
#                     "delay_time": "delayMinutes(30)"
#                   }
#                 },
#                 "AssetAutoImport": {
#                   "init": {
#                     "delay_time": "delayMinutes(90)"
#                   }
#                 }
#               }
#             }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_haier_changtai", body)

def update_gbiz_capital_haier_changtai():
    body = {
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
                    "channel": "haier_changtai",
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
            "title": "海尔昌泰流程编排v3",
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
                                    "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.99') && #loan.totalAmount<=cmdb.irr(#loan,'24.6')",
                                    "err_msg": "海尔昌泰[资产还款总额]不满足 irr24，请关注！"
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
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "10000",
                                        "messages": [
                                            "00000_处理成功_00000_成功_null_null"
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
                                        "code": "10000",
                                        "messages": [
                                            "00000_处理成功_00001_mock内层失败_null_null"
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
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "0",
                                        "messages": [
                                            "进件申请成功"
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
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "0",
                                        "messages": [
                                            "进件查询成功"
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
                                        "code": "9999",
                                        "messages": [
                                            "遇到配置"
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
                                            "遇到在配置"
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
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "0",
                                        "messages": [
                                            "支用前文件上传成功"
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
                                        "code": "9999",
                                        "messages": [
                                            "遇到再配置"
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
                                            "遇到配置"
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
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "20000",
                                        "messages": [
                                            "00000_处理成功_0_null_处理中"
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
                                        "code": "20000",
                                        "messages": [
                                            "00000_处理成功_-1_LA333_mock支用申请失败"
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
                                    "policy": "success"
                                },
                                "matches": [
                                    {
                                        "code": "20000",
                                        "messages": [
                                            "00000_处理成功_1_null_已放款"
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
                                        "code": "20000",
                                        "messages": [
                                            "00000_处理成功_-1_LA666_mock支用查询失败",
                                            "00001_mock外层失败_1_null_已放款"
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
                                            "00000_处理成功_0_null_处理中"
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
                        "execute": {
                            "interval_in_minutes": "240"
                        },
                        "init": {
                            "executeType": "auto",
                            "cancelable": False,
                            "simpleLock": None,
                            "delayTime": "delayMinutes(30)"
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
                }
            ]
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_haier_changtai", body)


def update_gbiz_capital_haier_changtai_const():
    body = {
        "productCode": "20239664",
        "sexMap":
            {
                "f": "20",
                "m": "10"
            },
        "individualEduMap": {
            "1": "40",
            "2": "40",
            "3": "30",
            "4": "30",
            "5": "30",
            "6": "20",
            "7": "10",
            "8": "00",
            "9": "00"
        },
        "individualMaritalMap": {
            "1": "10",
            "2": "20",
            "3": "40",
            "4": "50"
        },
        "individualEmpTypeMap": {
            "1": "O",
            "2": "N",
            "3": "M",
            "4": "L",
            "5": "K",
            "6": "P",
            "7": "K",
            "8": "R",
            "9": "I",
            "10": "O",
            "11": "J",
            "12": "Q",
            "13": "O",
            "14": "A",
            "15": "Z"
        },
        "purposeMap": {
            "1": "FLI",
            "2": "EDU",
            "3": "HOU",
            "4": "FMY",
            "5": "TRA",
            "6": "HEA",
            "7": "COS",
            "8": "FMY",
            "9": "FMY"
        },
        "relRelationMap": {
            "0": "06",
            "1": "01",
            "2": "02",
            "3": "02",
            "4": "99",
            "5": "99",
            "6": "99",
            "7": "99"
        },
        "bankCodeMap": {
            "ICBC": "102",
            "CCB": "105",
            "BOC": "104",
            "ABC": "103",
            "CMB": "308",
            "SPDB": "310",
            "CITIC": "",
            "CMBC": "",
            "HXBANK": "304",
            "GDB": "306",
            "CIB": "309",
            "SPABANK": "307",
            "BOHAI": "",
            "SHBANK": "04012900",
            "BJBANK": "04031000"
        },
        "uploadAttachmentMap": {
            "1": {
                "fileType": "DOC53",
                "path": "/lp_kuainiu/upload/idCard/%s",
                "fileName": "%s_01%s"
            },
            "2": {
                "fileType": "DOC54",
                "path": "/lp_kuainiu/upload/idCard/%s",
                "fileName": "%s_02%s"
            },
            "29": {
                "fileType": "DOC065",
                "path": "/lp_kuainiu/upload/face/%s",
                "fileName": "%s%s"
            }
        },
        "uploadContractMap": {
            "35700": {
                "fileType": "DOC004",
                "path": "/lp_kuainiu/upload/credit/%s",
                "fileName": "%s%s"
            },
            "35701": {
                "fileType": "DOC001",
                "path": "/lp_kuainiu/upload/consume/%s",
                "fileName": "%s%s"
            },
            "35702": {
                "fileType": "DOC600",
                "path": "/lp_kuainiu/upload/promise/%s",
                "fileName": "%s%s"
            },
            "35703": {
                "fileType": "DOC006",
                "path": "/lp_kuainiu/upload/contract/%s",
                "fileName": "%s%s"
            },
            "35704": {
                "fileType": "DOC101",
                "path": "/lp_kuainiu/upload/wtguarantee/%s",
                "fileName": "%s%s"
            },
            "35705": {
                "fileType": "DOC087",
                "path": "/lp_kuainiu/upload/person_information/%s",
                "fileName": "%s%s"
            }
        },
        "contractDownloadMap": {
            "35706": {
                "path": "/lp_kuainiu/down/consume/%s",
                "fileName": "%s.pdf"
            },
            "28": {
                "path": "/lp_kuainiu/down/contract/%s",
                "fileName": "%s.pdf"
            }
        },
        "provinceCodeMap": {},
        "cityCodeMap": {"310000": "310100",
                        "110000": "110100",
                        "120000": "120100",
                        "500000": "500100"
                        },
        "areaCodeMap": {},
        "districtCityCodeMap": {
            "310200": "310100"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_haier_changtai_const", body)
