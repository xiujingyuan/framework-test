
import common.global_const as gc


# def update_gbiz_capital_jinmeixin_hanchen_old():
#     body = {
#         "manual_reverse_allowed": False,
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
#                     "channel":"jinmeixin_hanchen",
#                     "interaction_type":"SMS",
#                     "way":"jinmeixin_hanchen",
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
#             "ChangeCapital": {
#                 "execute": {
#                     "event_handler_map": {
#                         "LoanApplySyncFailedEvent": "LoanApplyQuery",
#                         "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
#                         "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
#                         "GrantFailedEvent": "LoanConfirmQuery"
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
#             "AssetImport": {
#                 "execute": {
#                     "loan_validator": [
#                         {
#                             "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23') && #loan.totalAmount<=cmdb.irr(#loan,'24.5')",
#                             "err_msg": "金美信汉辰[资产还款总额]不满足 irr24，请关注！"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "成功"
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
#                                 "code": "1999999",
#                                 "messages": [
#                                     "mock_资料推送同步失败"
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
#                                 "code": "100067",
#                                 "messages": [
#                                     "流水号不存在",
#                                     "流水号不存在-SUC"
#                                 ]
#                             },
#                             {
#                                 "code": "1000000",
#                                 "messages": [
#                                     "成功-FAIL-mock_资料推送查询失败"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "成功-SUC"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "成功-IN_HANDLE"
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
#                                 "code": "2000000",
#                                 "messages": [
#                                     "成功"
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
#                                 "code": "2999999",
#                                 "messages": [
#                                     "mock_试算失败"
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
#                                 "code": "2900002",
#                                 "messages": [
#                                     "今日额度已抢完，请明日再试!"
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
#                                 "code": "3000000",
#                                 "messages": [
#                                     "成功"
#                                 ]
#                             },
#                             {
#                                 "code": "3999999",
#                                 "messages": [
#                                     "流水号重复.*"
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
#                                 "code": "3999999",
#                                 "messages": [
#                                     "mock_放款申请失败"
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
#                                 "code": "3000000",
#                                 "messages": [
#                                     "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：外部放款失败\\)",
#                                     "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：放款失败\\)",
#                                     "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：未查询到借款信息\\)",
#                                     "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：mock_放款失败\\)"
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
#                                 "code": "3000000",
#                                 "messages": [
#                                     "成功-LOAN_PASSED"
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
#                                 "code": "3000000",
#                                 "messages": [
#                                     "成功-LOANING"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "CapitalRepayPlanQuery": {
#                 "execute": {
#                     "adjust_fee_list": [
#                         "guarantee",
#                         "reserve"
#                     ],
#                     "allow_diff_effect_at": False,
#                     "allow_diff_due_at": False,
#                     "allowance_check_range": {
#                         "min_value": 0,
#                         "max_value": 0
#                     }
#                 }
#             },
#             "GuaranteeSign": {
#                 "init": {
#                     "delay_time": "delayMinutes(10)"
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
#                     "delay_time": "delayMinutes(5)"
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
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jinmeixin_hanchen", body)

def update_gbiz_capital_jinmeixin_hanchen():
    body = {
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
                    "channel": "jinmeixin_hanchen",
                    "interaction_type": "SMS",
                    "way": "jinmeixin_hanchen",
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
                "title": "金美信汉辰放款流程编排v3",
                "inclusions": [
                  "gbiz_capital_workflow_asset"
                ],
              "props": {
                "CapitalRepayPlanProps": {
                  "adjust_fee_list": [
                    "guarantee",
                    "reserve"
                  ],
                  "need_refresh_due_at": False,
                  "allow_diff_effect_at": False,
                  "allow_diff_due_at": False,
                  "allowance_check_range": {
                    "min_value": 0,
                    "max_value": 0
                  }
                }
              },
                "nodes": [
                  {
                    "id": "AssetAutoImport",
                    "type": "AssetAutoImportTaskHandler",
                    "events": [],
                    "activity": {
                      "init": {
                        "delayTime": "delayMinutes(120)"
                      },
                      "execute": {},
                      "finish": []
                    }
                  },
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
                            "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23') && #loan.totalAmount<=cmdb.irr(#loan,'24.5')",
                            "err_msg": "金美信汉辰[资产还款总额]不满足 irr24，请关注！"
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
                            "policy": "success"
                          },
                          "matches": [
                            {
                              "code": "1000000",
                              "messages": [
                                "成功"
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
                              "code": "1999999",
                              "messages": [
                                "mock_资料推送同步失败"
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
                        "delayTime": "delayMinutes(1)"
                      },
                      "execute": {},
                      "finish": [
                        {
                          "action": {
                            "policy": "fail"
                          },
                          "matches": [
                            {
                              "code": "100067",
                              "messages": [
                                "流水号不存在",
                                "流水号不存在-SUC"
                              ]
                            },
                            {
                              "code": "1000000",
                              "messages": [
                                "成功-FAIL-mock_资料推送查询失败"
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
                              "code": "1000000",
                              "messages": [
                                "成功-SUC"
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
                              "code": "1000000",
                              "messages": [
                                "成功-IN_HANDLE"
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
                      "init": {},
                      "execute": {},
                      "finish": [
                        {
                          "action": {
                            "policy": "success"
                          },
                          "matches": [
                            {
                              "code": "2000000",
                              "messages": [
                                "成功"
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
                              "code": "2999999",
                              "messages": [
                                "mock_试算失败"
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
                              "code": "2900002",
                              "messages": [
                                "今日额度已抢完，请明日再试!"
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
                            "policy": "success"
                          },
                          "matches": [
                            {
                              "code": "3000000",
                              "messages": [
                                "成功"
                              ]
                            },
                            {
                              "code": "3999999",
                              "messages": [
                                "流水号重复.*"
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
                              "code": "3999999",
                              "messages": [
                                "mock_放款申请失败"
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
                              "code": "3000000",
                              "messages": [
                                "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：外部放款失败\\)",
                                "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：放款失败\\)",
                                "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：未查询到借款信息\\)",
                                "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：mock_放款失败\\)"
                              ]
                            },
                            {
                              "code": "3000067",
                              "messages": [
                                "流水号不存在-LOAN_PASSED"
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
                              "code": "3000000",
                              "messages": [
                                "成功-LOAN_PASSED"
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
                              "code": "3000000",
                              "messages": [
                                "成功-LOANING"
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
                      "init": {},
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
                    "id": "GuaranteeSign",
                    "type": "GuaranteeSignTaskHandler",
                    "events": [
                      "GuaranteeSignSucceededEvent"
                    ],
                    "activity": {
                      "execute": {},
                      "init": {
                        "delayTime": "delayMinutes(10)"
                      }
                    }
                  },
                  {
                    "id": "GuaranteeDown",
                    "type": "GuaranteeDownTaskHandler",
                    "events": [
                      "GuaranteeDownloadSucceededEvent"
                    ],
                    "activity": {
                      "execute": {
                        "interval_in_minutes": "240"
                      },
                      "init": {}
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
                        "delayTime": "delayMinutes(120)",
                        "simpleLock": {
                          "key": "contractdown-ftp",
                          "ttlSeconds": 60
                        }
                      }
                    }
                  },
                  {
                    "id": "ContractPush",
                    "type": "ContractPushTaskHandler",
                    "events": [],
                    "activity": {
                      "execute": {},
                      "init": {
                        "delayTime": "delayMinutes(5)"
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
                  },
                  {
                    "id": "RongDanIrrTrial",
                    "type": "RongDanIrrTrialTaskHandler",
                    "activity": {
                      "init": {},
                      "execute": {
                        "trail_irr_limit": 35.99
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
                      "LoanCreditApply"
                    ]
                  },
                  {
                    "memo": "获取借款试算",
                    "listen": {
                      "event": "LoanCreditApplySyncSucceededEvent"
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
                      "ContractDown",
                      "GuaranteeSign"
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
                    "memo": "担保方签约成功",
                    "listen": {
                      "event": "GuaranteeSignSucceededEvent"
                    },
                    "nodes": [
                      "GuaranteeDown"
                    ]
                  },
                  {
                    "memo": "担保方合同下载成功",
                    "listen": {
                      "event": "GuaranteeDownloadSucceededEvent"
                    },
                    "nodes": [
                      "ContractPush"
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
                    "memo": "同步进件申请失败",
                    "listen": {
                      "event": "LoanApplySyncFailedEvent"
                    },
                    "nodes": [
                      "ChangeCapital"
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
                    "memo": "借款试算失败",
                    "listen": {
                      "event": "LoanCreditApplySyncFailedEvent"
                    },
                    "nodes": [
                      "ChangeCapital",
                      "BlacklistCollect"
                    ],
                    "associateData": {
                      "skipDoubleCheck": True,
                      "event": "LoanCreditApplySyncFailedEvent"
                    }
                  },
                  {
                    "memo": "同步请款申请失败",
                    "listen": {
                      "event": "ConfirmApplySyncFailedEvent"
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
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jinmeixin_hanchen", body)



def update_gbiz_capital_jinmeixin_hanchen_const():
    body = {
        "productCode": "FCDP",
        "contactRelationMap": {
            "0": "C",
            "1": "F",
            "2": "B",
            "3": "H",
            "4": "W",
            "5": "T",
            "6": "Y",
            "7": "Y"
        },
        "fileTyeMap": {
            "1": "CARD_FRONT_PHOTO",
            "2": "CARD_BACK_PHOTO",
            "29": "LIVE_PHOTO"
        },
        "educationMap": {
            "1": "F",
            "2": "F",
            "3": "E",
            "4": "E",
            "5": "E",
            "6": "D",
            "7": "C",
            "8": "B",
            "9": "A"
        },
        "maritalStatusMap": {
            "1": "S",
            "2": "C",
            "3": "D",
            "4": "W"
        },
        "professionMap": {
            "1": "J",
            "2": "J",
            "3": "J",
            "4": "J",
            "5": "P",
            "6": "P",
            "7": "P",
            "8": "P",
            "9": "P",
            "10": "B",
            "11": "K",
            "12": "P",
            "13": "P",
            "14": "B",
            "15": "L"
        },
        "incomeMap": {
            "0": "B",
            "2001": "B",
            "3001": "C",
            "5001": "D",
            "8001": "E",
            "12000": "F"
        },
        "loanUsageMap": {
            "1": "PL19",
            "2": "PL03",
            "3": "PL19",
            "4": "PL19",
            "5": "PL07",
            "6": "PL18",
            "7": "PL15",
            "8": "PL19",
            "9": "PL19"
        },
        "bankCodeMap": {
            "ICBC": "ICBC",
            "SPABANK": "PAB",
            "BOC": "BOC",
            "CCB": "CCB",
            "CIB": "CIB",
            "CMB": "CMB",
            "ABC": "ABC",
            "BJBANK": "BOB",
            "CEB": "CEB",
            "CITIC": "CITIC",
            "CMBC": "CMBC",
            "GDB": "GDB",
            "HXBANK": "HXB",
            "SHBANK": "SHB",
            "SPDB": "SPDB",
            "PSBC": "PSBC"
        },
        "contractMap": {
            "28": "LOAN",
            "33300": "BIZ_LOAN_REQUIREMENTS",
            "33301": "BIZ_CREDIT_AUTH",
            "33302": "WITHHOLD",
            "33303": "ENTRUST_GUARANTEE",
            "33304": "GUARANTEE",
            "33305": "PERSONAL_COMPOSITE_AUTH",
            "33309": "WITHHOLD_AUTH"
        },
        "contractPushMap": {
            "33311": {
                "subDirExpr": "",
                "nameExpr": "#{#asset.itemNo}_#{#contract.code}.pdf",
                "downloadType": 33306
            }
        },
        "ftpChannelName": "kuainiu",
        "baseFtpPath": "/tempfiles/test/jinmeixin_hanchen",
        "priceTag": "IRR24",
        "defaultSimilarity": "75",
        "similarityThreshold": "74",
        "userCheckPushType": "105",
        "userInfoPushType": "2",
        "bindCardType": "1",
        "idCardLongTimeExpireDay": "20991231",
        "loanScene": "LOAN",
        "bindCardCertType": "I",
        "userPushIdType": "1",
        "fundCode": "JMX",
        "pushOrOrderNoSubfix": "JMXH",
        "guaranteeName": "hanchen_jinmeixin",
        "includeFeesMap": {
            "reserve": "schdTermServFee",
            "guarantee": "schdLoanServFee"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jinmeixin_hanchen_const", body)