
import common.global_const as gc


# def update_gbiz_capital_yixin_rongsheng_old(raise_limit_over_time_seconds=7200):
#     yixin_rongsheng = {
#         "manual_reverse_allowed": False,
#         "recall_via_ivr_enabled": True,
#         "cancelable_task_list": [
#             "ApplyCanLoan",
#             "LoanApplyNew",
#             "ChangeCapital"
#         ],
#         "raise_limit_allowed": False,
#         "register_config": {
#             "register_step_list":[
#                 {
#                     "step_type":"PROTOCOL",
#                     "channel":"yixin_rongsheng",
#                     "interaction_type":"SMS",
#                     "way":"yixin_rongsheng",
#                     "status_scene":{
#                         "register":{
#                             "success_type":"once",
#                             "register_status_effect_duration_day":1,
#                             "allow_fail":False,
#                             "need_confirm_result":False
#                         },
#                         "route":{
#                             "success_type":"once",
#                             "allow_fail":False
#                         },
#                         "validate":{
#                             "success_type":"once"
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
#         "task_config_map": {
#             "AssetImport": {
#                 "execute": {
#                     "loan_validator": [
#                         {
#                             "rule": "#loan.totalAmount==cmdb.irr(#loan,'35.99')",
#                             "err_msg": "宜信荣晟[资产还款总额]不满足 irr35.99，请关注！"
#                         }
#                     ]
#                 }
#             },
#             "LoanApplyNew": {
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "成功-1-null",
#                                     "成功--1-当前进件已经申请过，请勿重复申请"
#                                 ]
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "成功--1-null",
#                                     "成功--1-联系人姓名或手机号码填写有误",
#                                     "mock失败--1-mock的"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanApplyQuery": {
#                 "init": {
#                     "delay_time": "delaySeconds(60)"
#                 },
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "成功--1-null",
#                                     "mock失败-REFUSE-null"
#                                 ]
#                             },
#                             {
#                                 "code": "90000",
#                                 "messages": [
#                                     "进件不存在"
#                                 ]
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "成功-SIGN_SUCCESS-null"
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
#                                 "code": "0",
#                                 "messages": [
#                                     "成功-APPLYING-null"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanApplyConfirm": {
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "成功-0-发送放款通知成功",
#                                     "成功-0-已放款,不能发送放款通知"
#                                 ]
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "mock 失败-1-mock 失败"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanConfirmQuery": {
#                 "init": {
#                     "delay_time": "delaySeconds(120)"
#                 },
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "fail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "mock失败-LEND_FAILED-放款失败"
#                                 ]
#                             }
#                         ]
#                     },
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "成功-LENT-null"
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
#                                 "code": "0",
#                                 "messages": [
#                                     "成功-LENDING-null"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "ChangeCapital": {
#                 "execute": {
#                     "event_handler_map": {
#                         "LoanApplySyncFailedEvent": "LoanApplyQuery",
#                         "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
#                         "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
#                         "GrantFailedEvent": "LoanConfirmQuery"
#                     }
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
#                                 "code": "12"
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
#                                     "资方二次校验失败：未命中\\[fail,updateCard\\]策略.*"
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
#                                 "code": "100998"
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "CapitalRepayPlanQuery": {
#                 "execute": {
#                     "allow_diff_effect_at": False,
#                     "allow_diff_due_at": False,
#                     "allowance_check_range": {
#                         "min_value": -1,
#                         "max_value": 1
#                     }
#                 }
#             },
#             "ContractDown": {
#                 "init": {
#                     "delay_time": "delayMinutes(120)",
#                     "simple_lock": {
#                         "key": "contractdown-ftp",
#                         "ttlSeconds": 60
#                     }
#                 }
#             },
#             "ContractPush": {
#                 "init": {
#                     "delay_time": "delayMinutes(60)"
#                 }
#             },
#             "AssetAutoImport": {
#                 "init": {
#                     "delay_time": "delayMinutes(90)"
#                 }
#             },
#             "AssetConfirmOverTimeCheck": {
#                 "execute": {
#                     "raise_limit_over_time_seconds": raise_limit_over_time_seconds
#                 },
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "timeoutAndFail"
#                         },
#                         "matches": [
#                             {
#                                 "code": "10005",
#                                 "messages": [
#                                     "确认类型\\[LOAN_PRODUCT_CHANGE\\]已超时"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "RongDanIrrTrial": {
#                 "execute": {
#                     "trail_irr_limit": 35.99
#                 }
#             }
#         }
#     }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yixin_rongsheng", yixin_rongsheng)

def update_gbiz_capital_yixin_rongsheng():
    yixin_rongsheng = {
                      "manual_reverse_allowed": False,
                      "recall_via_ivr_enabled": True,
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
                            "channel": "yixin_rongsheng",
                            "interaction_type": "SMS",
                            "way": "yixin_rongsheng",
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
                                "type": "GetSmsVerifyCode"
                              },
                              {
                                "type": "CheckSmsVerifyCode"
                              }
                            ]
                          }
                        ]
                      },
                      "workflow": {
                        "title": "宜信荣晟流程编排v3",
                        "inclusions": [
                          "gbiz_capital_workflow_asset"
                        ],
                        "props": {
                          "CapitalRepayPlanProps": {
                            "need_refresh_due_at": False,
                            "allow_diff_effect_at": False,
                            "allow_diff_due_at": False,
                            "allowance_check_range": {
                              "min_value": -1,
                              "max_value": 1
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
                                    "rule": "#loan.totalAmount==cmdb.irr(#loan,'35.99')",
                                    "err_msg": "宜信荣晟[资产还款总额]不满足 irr35.99，请关注！"
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
                                    "policy": "success"
                                  },
                                  "matches": [
                                    {
                                      "code": "0",
                                      "messages": [
                                        "成功-1-null",
                                        "成功--1-当前进件已经申请过，请勿重复申请"
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
                                      "code": "0",
                                      "messages": [
                                        "成功--1-null",
                                        "成功--1-联系人姓名或手机号码填写有误",
                                        "mock失败--1-mock的"
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
                                      "messages": None
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
                                      "code": "100998",
                                      "messages": None
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
                                    "policy": "fail"
                                  },
                                  "matches": [
                                    {
                                      "code": "0",
                                      "messages": [
                                        "成功--1-null",
                                        "mock失败-REFUSE-null"
                                      ]
                                    },
                                    {
                                      "code": "90000",
                                      "messages": [
                                        "进件不存在"
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
                                      "code": "0",
                                      "messages": [
                                        "成功-SIGN_SUCCESS-null"
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
                                      "code": "0",
                                      "messages": [
                                        "成功-APPLYING-null"
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
                              "finish": []
                            }
                          },
                          {
                            "id": "ContractPush",
                            "type": "ContractPushTaskHandler",
                            "events": [
                              "ContractPushSucceededEvent"
                            ],
                            "activity": {
                              "init": {
                                "executeType": "auto",
                                "cancelable": False,
                                "simpleLock": None,
                                "delayTime": "delayMinutes(5)"
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
                                    "policy": "success"
                                  },
                                  "matches": [
                                    {
                                      "code": "0",
                                      "messages": [
                                        "成功-0-发送放款通知成功",
                                        "成功-0-已放款,不能发送放款通知"
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
                                      "code": "0",
                                      "messages": [
                                        "mock 失败-1-mock 失败"
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
                                    "policy": "fail"
                                  },
                                  "matches": [
                                    {
                                      "code": "0",
                                      "messages": [
                                        "mock失败-LEND_FAILED-放款失败"
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
                                      "code": "0",
                                      "messages": [
                                        "成功-LENT-null"
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
                                      "code": "0",
                                      "messages": [
                                        "成功-LENDING-null"
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
                              "execute": {
                                "interval_in_minutes": "120"
                              },
                              "init": {
                                "executeType": "auto",
                                "cancelable": False,
                                "simpleLock": {
                                  "ttlSeconds": 60,
                                  "key": "contractdown-ftp"
                                },
                                "delayTime": "delayMinutes(120)"
                              },
                              "finish": []
                            }
                          },
                          {
                            "id": "RongDanIrrTrial",
                            "type": "RongDanIrrTrialTaskHandler",
                            "activity": {
                              "execute": {
                                "trail_irr_limit": 35.99
                              },
                              "init": {
                                "executeType": "auto"
                              }
                            }
                          },
                          {
                            "id": "CapitalCallback",
                            "type": "CapitalCallbackTaskHandler",
                            "events":
                              [
                                "AssetCallBackReverseSucceededEvent"
                              ],
                            "activity":
                              {
                                "init":
                                  {},
                                "execute":
                                  {},
                                "finish":
                                  []
                              }
                          },
                          {
                            "id": "GrantCallBackReverse",
                            "type": "GrantCallBackReverseBizPerformer",
                            "events":
                              [
                                "AssetReverseReadyEvent"
                              ],
                            "activity":
                              {
                                "init":
                                  {},
                                "execute":
                                  {},
                                "finish":
                                  []
                              }
                          },
                          {
                            "id": "CapitalAssetReverse",
                            "type": "CapitalAssetReverseTaskHandler",
                            "events":
                              [
                                "AssetReverseSucceededEvent"
                              ],
                            "activity":
                              {
                                "init":
                                  {},
                                "execute":
                                  {},
                                "finish":
                                  []
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
                              "skipDoubleCheck": False
                            }
                          },
                          {
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
                              "event": "LoanApplyTrailSucceededEvent"
                            },
                            "nodes": [
                              "ContractPush"
                            ]
                          },
                          {
                            "listen": {
                              "event": "ContractPushSucceededEvent"
                            },
                            "nodes": [
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
                              "CapitalRepayPlanQuery"
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
                              "OurRepayPlanRefine",
                              "ContractDown"
                            ]
                          },
                          {
                            "listen":
                              {
                                "event": "AssetCallBackReverseSucceededEvent"
                              },
                            "nodes":
                              [
                                "GrantCallBackReverse"
                              ]
                          },
                          {
                            "listen":
                              {
                                "event": "AssetReverseReadyEvent"
                              },
                            "nodes":
                              [
                                "CapitalAssetReverse"
                              ]
                          },
                          {
                            "listen":
                              {
                                "event": "AssetReverseSucceededEvent"
                              },
                            "nodes":
                              [
                                "AssetVoid"
                              ]
                          }

    ]
                      }
                    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yixin_rongsheng", yixin_rongsheng)


def update_gbiz_capital_yixin_rongsheng_const():
    body = {
          "loanUseMap": {
            "0": "60",
            "1": "20",
            "2": "60",
            "3": "10",
            "4": "20",
            "5": "40",
            "6": "60",
            "7": "30",
            "8": "50",
            "9": "60"
          },
          "defaultSimilarity": 75,
          "similarityThreshold": 70,
          "fetchPhotoMethod": "ALBUM",
          "idCardExpired": "20991231",
          "defaultLoanUse": "60",
          "defaultEducation": "80",
          "aliveTimes": "1",
          "faceAuthTimes": "1",
          "contractPushMap": {
            "33405": "2",
            "33406": "1"
          },
          "genderMap": {
            "m": "男",
            "f": "女"
          },
          "fileTyeMap": {
            "1": "CARD_FRONT_PHOTO",
            "2": "CARD_BACK_PHOTO",
            "29": "FRONT_PHOTO"
          },
          "contactRelationMap": {
            "0": "3",
            "1": "1",
            "2": "7",
            "3": "4",
            "4": "6",
            "5": "8",
            "6": "5",
            "7": "5"
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
            "9": "10"
          },
          "defaultFirstRelationship": "7",
          "defaultSecondRelationship": "5",
          "maxAllowSize": 409600,
          "repayPlanDateFormat": "yyyy-MM-dd",
          "contractDownMap": {
            "28": "2",
            "33400": "6",
            "33401": "1006",
            "33402": "1012",
            "33403": "16",
            "33404": "17"
          },
          "ftpChannelName": "kuainiu",
          "baseDir": "/tempfiles/dev/yixin_rongsheng",
          "statementFtpChannelName": "kuainiu",
          "statementBaseDir": "/tempfiles/dev/yixin_rongsheng",
            "cancelRefundStatusList": [
            "0"],
        "reverseStatusList": ["LEND_FAILED"],
        "useSubAssetMap": {
            "yxrs_6m": True,
            "yxrs_12m": False
        },
        "outOrderNoMap": {
            "test": "1231231"
            }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yixin_rongsheng_const", body)