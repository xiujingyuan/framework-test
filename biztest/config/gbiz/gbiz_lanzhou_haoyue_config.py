
import common.global_const as gc

# def update_gbiz_capital_lanzhou_haoyue_old():
#     lanzhou_haoyue = {
#         "cancelable_task_list": [
#             "ApplyCanLoan",
#             "LoanApplyTrial",
#             "LoanPreApply",
#             "LoanApplyNew",
#             "ChangeCapital"
#         ],
#         "register_config": {
#             "register_step_list":[
#                 {
#                     "channel":"lanzhou_haoyue",
#                     "step_type":"PAYSVR_PROTOCOL",
#                     "way" : "tq",
#                     "interaction_type":"SMS",
#                     "group":"kuainiu",
#                     "status_scene":{
#                         "register":{
#                             "success_type":"executed",
#                             "allow_fail":True,
#                             "need_confirm_result":True
#                         },
#                         "route":{
#                             "success_type":"executed",
#                             "allow_fail":True
#                         },
#                         "validate":{
#                             "success_type":"executed"
#                         }
#                     },
#                     "actions":[
#                         {
#                             "type":"GetSmsVerifyCode"
#                         },
#                         {
#                             "type":"CheckSmsVerifyCode"
#                         }
#                     ]
#                 }
#             ]
#         },
#         "manual_reverse_allowed": False,
#         "raise_limit_allowed": False,
#         "task_config_map": {
#             "ChangeCapital": {
#                 "execute": {
#                     "event_handler_map": {
#                         "LoanCreditFailedEvent": "LoanCreditQuery",
#                         "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
#                         "GrantFailedEvent": "LoanConfirmQuery",
#                         "LoanApplySyncFailedEvent": "LoanApplyQuery",
#                         "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
#                         "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
#                     },
#                     "can_change_capital": True
#                 },
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "切资方路由\\(二次\\)成功"
#                                 ]
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "finalFail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "12",
#                                 "messages": []
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "1",
#                                 "messages": [
#                                 ]
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "retry"
#                         },
#                         "matches": [
#                             {
#                                 "code": "1",
#                                 "messages": [
#                                     ""
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "AssetImport": {
#                 "execute": {
#                     "loan_validator": [
#                         {
#                             "rule": "#loan.totalAmount==cmdb.irr(#loan,'23.99')",
#                             "err_msg": "兰州昊悦[资产还款总额]不满足 irr23.99，请关注！"
#                         }
#                     ]
#                 }
#             },
#             "LoanPreApply": {
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0"
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "retry"
#                         },
#                         "matches": [
#                             {
#                                 "code": "2"
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanApplyNew": {
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0"
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "9000"
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanApplyQuery": {
#                 "init": {
#                     "delay_time": "delaySeconds(120)"
#                 },
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "1999901"
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "1900002",
#                                 "messages": []
#                             },
#                             {
#                                 "code": "1999901"
#                             }
#
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "retry"
#                         },
#                         "matches": [
#                             {
#                                 "code": "1000000",
#                                 "messages": [
#                                     "客户信息推送-处理中"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanCreditApply": {
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "9999"
#                             },
#                             {
#                                 "code": "0"
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "9000",
#                                 "messages": [
#                                     "有未使用授信，不可重复授信"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanCreditQuery": {
#                 "init": {
#                     "delay_time": "delaySeconds(180)"
#                 },
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "2999901"
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "2999903"
#                             },
#                             {
#                                 "code": "2100002",
#                                 "messages": [
#                                     "授信申请-查无此交易"
#                                 ]
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "retry"
#                         },
#                         "matches": [
#                             {
#                                 "code": "2000000",
#                                 "messages": [
#                                     "授信申请-处理中"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanPostApply": {
#                 "init": {
#                     "delay_time": "delaySeconds(60)"
#                 },
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0"
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "ContractPush": {
#                 "init": {
#                     "delay_time": "delaySeconds(60)"
#                 }
#             },
#             "LoanApplyConfirm": {
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0"
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanConfirmQuery": {
#                 "init": {
#                     "delay_time": "delaySeconds(300)"
#                 },
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "3999904"
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "3999903"
#                             },
#                             {
#                                 "code": "3999905"
#                             },
#                             {
#                                 "code": "3999909"
#                             },
#                             {
#                                 "code": "3999990"
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "retry"
#                         },
#                         "matches": [
#                             {
#                                 "code": "3000000",
#                                 "messages": [
#                                     "贷款支用查询-处理中",
#                                     "贷款支用查询-交易接收成功"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "CapitalRepayPlanQuery": {
#                 "execute": {
#                     "allow_diff_effect_at": True,
#                     "allow_diff_due_at": False,
#                     "allowance_check_range": {
#                         "min_value": 0,
#                         "max_value": 0
#                     }
#                 }
#             },
#             "OurRepayPlanRefine": {
#                 "execute": {
#                     "need_refresh_due_at": False
#                 }
#             },
#             "CertificateApply": {
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0"
#                             },
#                             {
#                                 "code": "40000"
#                             },
#                             {
#                                 "code": "41200",
#                                 "messages": [
#                                     "已存在该借据号的申请结清记录"
#                                 ]
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "retry"
#                         },
#                         "matches": [
#                             {
#                                 "code": "1",
#                                 "messages": [
#                                     "结清证明申请处理失败：资产未结清或未结算完成"
#                                 ]
#                             },
#                             {
#                                 "code": "100010",
#                                 "messages": [
#                                     "系统正在维护中，请稍后再试"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "CertificateDownload": {
#                 "init": {
#                     "delay_time": "delayDays(1, \"08:00:00\")"
#                 }
#             },
#             "AssetAutoImport": {
#                 "init": {
#                     "delay_time": "delayMinutes(120)"
#                 }
#             },
#             "RongDanIrrTrial": {
#                 "execute": {
#                     "trail_irr_limit": 35.99
#                 }}
#         }
#     }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_haoyue", lanzhou_haoyue)

def update_gbiz_capital_lanzhou_haoyue():
    lanzhou_haoyue = {
                      "cancelable_task_list": [
                        "ApplyCanLoan",
                        "LoanApplyTrial",
                        "LoanPreApply",
                        "LoanApplyNew",
                        "ChangeCapital"
                      ],
                      "register_config": {
                        "register_step_list": [
                          {
                            "channel": "lanzhou_haoyue",
                            "step_type": "PAYSVR_PROTOCOL",
                            "way": "tq",
                            "interaction_type": "SMS",
                            "group": "kuainiu",
                            "status_scene": {
                              "register": {
                                "success_type": "executed",
                                "allow_fail": True,
                                "need_confirm_result": True
                              },
                              "route": {
                                "success_type": "executed",
                                "allow_fail": True
                              },
                              "validate": {
                                "success_type": "executed"
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
                      "manual_reverse_allowed": False,
                      "raise_limit_allowed": False,
                      "workflow": {
                        "inclusions": [
                          "gbiz_capital_workflow_asset"
                        ],
                        "props": {
                          "CapitalRepayPlanProps": {
                            "need_refresh_due_at": False,
                            "allow_diff_due_at": True,
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
                                    "rule": "#loan.totalAmount==cmdb.irr(#loan,'23.99')",
                                    "err_msg": "兰州昊悦[资产还款总额]不满足 irr23.99，请关注！"
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
                                      "code": "0"
                                    }
                                  ]
                                },
                                {
                                  "action": {
                                    "policy": "retry"
                                  },
                                  "matches": [
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
                                      "code": "0"
                                    }
                                  ]
                                },
                                {
                                  "action": {
                                    "policy": "fail"
                                  },
                                  "matches": [
                                    {
                                      "code": "9000"
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
                                      "code": "1999901"
                                    }
                                  ]
                                },
                                {
                                  "action": {
                                    "policy": "fail"
                                  },
                                  "matches": [
                                    {
                                      "code": "1900002",
                                      "messages": []
                                    },
                                    {
                                      "code": "1999901"
                                    }
                                  ]
                                },
                                {
                                  "action": {
                                    "policy": "retry"
                                  },
                                  "matches": [
                                    {
                                      "code": "1000000",
                                      "messages": [
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
                            "events": [
                              "LoanPostApplySucceededEvent",
                              "LoanPostApplyFailedEvent"
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
                                    "policy": "success"
                                  },
                                  "matches": [
                                    {
                                      "code": "9999"
                                    },
                                    {
                                      "code": "0"
                                    }
                                  ]
                                },
                                {
                                  "action": {
                                    "policy": "fail"
                                  },
                                  "matches": [
                                    {
                                      "code": "9000",
                                      "messages": [
                                        "有未使用授信，不可重复授信"
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
                                "delayTime": "delaySeconds(180)"
                              },
                              "execute": {},
                              "finish": [
                                {
                                  "action": {
                                    "policy": "success"
                                  },
                                  "matches": [
                                    {
                                      "code": "2999901"
                                    }
                                  ]
                                },
                                {
                                  "action": {
                                    "policy": "fail"
                                  },
                                  "matches": [
                                    {
                                      "code": "2999903"
                                    },
                                    {
                                      "code": "2100002",
                                      "messages": [
                                        "授信申请-查无此交易"
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
                                      "code": "2000000",
                                      "messages": [
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
                            "events": [
                              "LoanApplyTrailSucceededEvent"
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
                                      "code": "0"
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
                                "delayTime": "delaySeconds(300)"
                              },
                              "execute": {},
                              "finish": [
                                {
                                  "action": {
                                    "policy": "success"
                                  },
                                  "matches": [
                                    {
                                      "code": "3999904"
                                    }
                                  ]
                                },
                                {
                                  "action": {
                                    "policy": "fail"
                                  },
                                  "matches": [
                                    {
                                      "code": "3999903"
                                    },
                                    {
                                      "code": "3999905"
                                    },
                                    {
                                      "code": "3999909"
                                    },
                                    {
                                      "code": "3999990"
                                    }
                                  ]
                                },
                                {
                                  "action": {
                                    "policy": "retry"
                                  },
                                  "matches": [
                                    {
                                      "code": "3000000",
                                      "messages": [
                                        "贷款支用查询-处理中",
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
                            "id": "ContractDown",
                            "type": "ContractDownTaskHandler",
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
                            "id": "RongDanIrrTrial",
                            "type": "RongDanIrrTrialTaskHandler",
                            "events": [
                              "RongDanIrrTrialSucceededEvent"
                            ],
                            "activity": {
                              "init": {
                                "executeType": "auto",
                                "cancelable": False
                              },
                              "execute": {
                                "trail_irr_limit": 35.99
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
                            "id": "CertificateApplyVerifySync",
                            "type": "CertificateApplyVerifySyncTaskHandler",
                            "events": [
                              "CertificateApplyReadyEvent"
                            ],
                            "activity": {
                              "init": {},
                              "finish": []
                            }
                          },
                          {
                            "id": "CertificateApply",
                            "type": "CertificateApplyTaskHandler",
                            "events": [
                              "CertificateApplySuccessEvent"
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
                                                "code": "0"
                                            },
                                            {
                                                "code": "40000"
                                            },
                                            {
                                                "code": "41200",
                                                "messages": [
                                                    "已存在该借据号的申请结清记录"
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
                                                "code": "1",
                                                "messages": [
                                                    "结清证明申请处理失败：资产未结清或未结算完成"
                                                ]
                                            },
                                            {
                                                "code": "100010",
                                                "messages": [
                                                    "系统正在维护中，请稍后再试"
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
                            "events": [],
                            "activity": {
                              "init": {
                                "delayTime": "delayDays(1, \"08:00:00\")"
                              },
                              "execute": {
                                "interval_in_minutes": "30"
                              }
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
                                "delayTime": "delayMinutes(120)"
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
                                  "LoanCreditFailedEvent": "LoanCreditQuery",
                                  "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
                                  "GrantFailedEvent": "LoanConfirmQuery",
                                  "LoanApplySyncFailedEvent": "LoanApplyQuery",
                                  "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                                  "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
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
                              "LoanCreditApply"
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
                              "LoanApplyTrial"
                            ],
                            "associateData": {
                              "lockRecordStatus": 3
                            }
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
                              "event": "LoanApplyTrailSucceededEvent"
                            },
                            "nodes": [
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
                              "ContractSignature"
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
                              "event": "ContractSignatureSucceededEvent"
                            },
                            "nodes": [
                              "ContractDown"
                            ]
                          },
                          {
                            "listen": {
                              "event": "CertificateApplySuccessEvent"
                            },
                            "nodes": [
                              "CertificateDownload"
                            ]
                          },
                          {
                            "listen": {
                              "event": "CertificateApplyReadyEvent"
                            },
                            "nodes": [
                              "CertificateApply"
                            ]
                          }
                        ]
                      }
                    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_haoyue", lanzhou_haoyue)
def update_gbiz_capital_lanzhou_haoyue_const():
    body = {
        "ftpBaseDir": "/upload/zyd",
        "ftpChannelName": "lanzhou",
        "maxRate": 24,
        "capitalChannelCode": "Z-KN-ZKBC",
        "productCode": "Z-KN-DEBX-ZKBC",
        "nonBusinessTimeMsgs": [
            "非业务时间段"
        ],
        "authorization": 30603,
        "attachmentConfig": {
            "BEFORE_CUSTOMER_INFO_PUSH": {
                "1": "certFileA",
                "2": "certFileB",
                "30604": "cusinfo"
            },
            "BEFORE_CREDIT_APPLY": {
                "30603": "authorization",
                "29": "facephoto"
            },
            "BEFORE_LOAN_APPLY": {
                "31100": "guacon",
                "30601": "contract",
                "31101": "guaconletter"
            }
        },
        "loanUseMap": {
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
        "educationMap": {
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
        "jobMap": {
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
        "dutyMap": {
            "1": "3",
            "2": "1",
            "3": "4",
            "4": "9",
            "5": "4",
            "6": "4"
        },
        "dupCustomerInfoPushConfigList": [
            {
                "code": "1999901"
            }
        ],
        "dupCreditApplyConfigList": [
            {
                "code": "2999901"
            }
        ],
        "ipSegments": [
            "61.159.109.104-61.159.109.105"
        ],
        "certificateFileConfig": {
            "attachmentType": 24,
            "prefix": "zyzk_",
            "suffix": "_finish",
            "fileType": "pdf"
        },
        "certificateZipFileConfig": {
            "baseDir": "/upload/zyd/11001",
            "suffix": "_loanFinish",
            "fileType": "zip"
        },
        "industryTypeMap": {
            "1": "O824",
            "2": "I67",
            "3": "H6511",
            "4": "K721",
            "5": "C372",
            "6": "H638",
            "7": "M7811",
            "8": "G602",
            "9": "Q851",
            "10": "P84",
            "11": "J68",
            "12": "L7421",
            "13": "R88",
            "14": "S9426",
            "15": "A01"
        },
        "nationCodeMap": {
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
            "未知": "999"
        },
        "bankMap": {
            "BOC": {
                "bankId": "104100000004",
                "fullName": "中国银行总行"
            },
            "HXB": {
                "bankId": "304100040000",
                "fullName": "华夏银行股份有限公司总行"
            },
            "CMB": {
                "bankId": "308584000013",
                "fullName": "招商银行股份有限公司"
            },
            "ICBC": {
                "bankId": "102100099996",
                "fullName": "中国工商银行"
            },
            "CCB": {
                "bankId": "105100000017",
                "fullName": "中国建设银行股份有限公司总行"
            },
            "CIB": {
                "bankId": "309391000011",
                "fullName": "兴业银行总行"
            },
            "CEB": {
                "bankId": "303100000006",
                "fullName": "中国光大银行"
            },
            "ABC": {
                "bankId": "103100000026",
                "fullName": "中国农业银行股份有限公司"
            },
            "PSBC": {
                "bankId": "403100000004",
                "fullName": "中国邮政储蓄银行有限责任公司"
            },
            "CMBC": {
                "bankId": "305100000013",
                "fullName": "中国民生银行"
            },
            "SPDB": {
                "bankId": "310290000013",
                "fullName": "上海浦东发展银行"
            },
            "COMM": {
                "bankId": "301290000007",
                "fullName": "交通银行"
            },
            "PAB": {
                "bankId": "307584007998",
                "fullName": "平安银行（原深圳发展银行）"
            },
            "SHBANK": {
                "bankId": "325290000012",
                "fullName": "上海银行股份有限公司"
            },
            "GDB": {
                "bankId": "306581000003",
                "fullName": "广发银行股份有限公司"
            },
            "CITIC": {
                "bankId": "302100011000",
                "fullName": "中信银行股份有限公司"
            },
            "BJBANK": {
                "bankId": "313100000013",
                "fullName": "北京银行"
            }
        },
        "cutp": "1",
        "livest": "9",
        "marriage": "10",
        "jobnature": "90"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_haoyue_const", body)
