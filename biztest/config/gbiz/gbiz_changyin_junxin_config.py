import common.global_const as gc

# def update_gbiz_capital_changyin_junxin_old():
#     body ={
#           "cancelable_task_list": [
#             "ApplyCanLoan",
#             "LoanApplyNew",
#             "ChangeCapital"
#           ],
#           "manual_reverse_allowed": False,
#           "raise_limit_allowed": False,
#           "register_config": {
#             "ref_accounts": None,
#             "register_step_list": [
#               {
#                 "channel": "changyin_junxin",
#                 "step_type": "PROTOCOL",
#                 "way": "changyin_junxin",
#                 "interaction_type": "SMS",
#                 "status_scene": {
#                   "register": {
#                     "success_type": "once",
#                     "register_status_effect_duration_day": 0,
#                     "allow_fail": False,
#                     "need_confirm_result": False
#                   },
#                   "route": {
#                     "success_type": "once",
#                     "allow_fail": False
#                   },
#                   "validate": {
#                     "success_type": "once"
#                   }
#                 },
#                 "actions": [
#                   {
#                     "allow_fail": False,
#                     "type": "GetSmsVerifyCode"
#                   },
#                   {
#                     "allow_fail": False,
#                     "type": "CheckSmsVerifyCode"
#                   }
#                 ]
#               }
#             ]
#           },
#           "task_config_map": {
#             "ChangeCapital": {
#               "execute": {
#                 "event_handler_map": {
#                   "LoanApplySyncFailedEvent": "LoanApplyQuery",
#                   "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
#                   "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
#                   "GrantFailedEvent": "LoanConfirmQuery"
#                 },
#                 "can_change_capital": True
#               },
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "0",
#                       "messages": [
#                         "切资方路由\\(二次\\)成功"
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "finalFail"
#                   },
#                   "matches": [
#                     {
#                       "code": "12",
#                       "messages": [
#
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "fail"
#                   },
#                   "matches": [
#                     {
#                       "code": "1",
#                       "messages": [
#                         "遇到在配置"
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "retry"
#                   },
#                   "matches": [
#                     {
#                       "code": "100998"
#                     }
#                   ]
#                 }
#               ]
#             },
#             "AssetImport": {
#               "execute": {
#                 "loan_validator": [
#                   {
#                     "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.98') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
#                     "err_msg": "长银钧信[资产还款总额]不满足 irr24，请关注！"
#                   }
#                 ]
#               }
#             },
#             "LoanApplyNew": {
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "2",
#                       "messages": [
#                         "0000_交易成功！"
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "fail"
#                   },
#                   "matches": [
#                     {
#                       "code": "2",
#                       "messages": [
#                         "0001_mock测试授信申请失败"
#                       ]
#                     }
#                   ]
#                 }
#               ]
#             },
#             "LoanApplyQuery": {
#               "init": {
#                 "delay_time": "delaySeconds(60)"
#               },
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "2",
#                       "messages": [
#                         "0_Success_S_.*",
#                          "0000_交易成功！_04_null_null",
#                         "0_交易成功！_4_null_null"
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "fail"
#                   },
#                   "matches": [
#                     {
#                       "code": "2",
#                       "messages": [
#                         "0_交易成功！_2_null_null",
#                         "0_交易成功！_授信金额小于资产本金_4_null_null"
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "retry"
#                   },
#                   "matches": [
#                     {
#                       "code": "2",
#                       "messages": [
#                         "0000_交易成功！_返回长银客户号为空_授信金额小于资产本金_01_null_null"
#                       ]
#                     }
#                   ]
#                 }
#               ]
#             },
#             "LoanApplyConfirm": {
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "3",
#                       "messages": [
#                         "0000_交易成功！_100"
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "fail"
#                   },
#                   "matches": [
#                     {
#                       "code": "3",
#                       "messages": [
#                         "0000_交易成功！_300"
#                       ]
#                     }
#                   ]
#                 }
#               ]
#             },
#             "LoanConfirmQuery": {
#               "init": {
#                 "delay_time": "delaySeconds(120)"
#               },
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "3",
#                       "messages": [
#                         "0000_交易成功！_200_清算成功"
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "fail"
#                   },
#                   "matches": [
#                     {
#                       "code": "3",
#                       "messages": [
#                         "0000_交易成功！_300_放款失败"
#                       ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "retry"
#                   },
#                   "matches": [
#                     {
#                       "code": "3",
#                       "messages": [
#                         "0000_交易成功！_100_",
#                         "0000_交易成功！_请求返回放款金额 不等于 资产本金,请确认_100_"
#                       ]
#                     }
#                   ]
#                 }
#               ]
#             },
#             "CapitalRepayPlanQuery": {
#               "execute": {
#                 "allow_diff_effect_at": False,
#                 "allow_diff_due_at": False,
#                 "allowance_check_range": {
#                   "min_value": 0,
#                   "max_value": 0
#                 }
#               }
#             },
#             "OurRepayPlanRefine": {
#               "execute": {
#                 "need_refresh_due_at": False
#               }
#             },
#             "ContractDown": {
#               "execute": {
#                 "interval_in_minutes": "240"
#               },
#               "init": {
#                 "delay_time": "delayMinutes(10)",
#                 "simple_lock": {
#                   "key": "contractdown-changyin",
#                   "ttlSeconds": 10
#                 }
#               }
#             },
#             "AssetAutoImport": {
#               "init": {
#                 "delay_time": "delayMinutes(90)"
#               }
#             },
#             "CertificateApply": {
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "4",
#                       "messages": [
#                         "0_接收成功"
#                       ]
#                     }
#                   ]
#                 }
#               ]
#             },
#             "CertificateDownload": {
#               "execute": {
#                 "interval_in_minutes": "30"
#               },
#               "init": {
#                 "delay_time": "delayMinutes(10)"
#               }
#             }
#           }
#         }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_changyin_junxin", body)

def update_gbiz_capital_changyin_junxin():
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
                  "channel": "changyin_junxin",
                  "step_type": "PROTOCOL",
                  "way": "changyin_junxin",
                  "interaction_type": "SMS",
                  "status_scene": {
                    "register": {
                      "success_type": "once",
                      "register_status_effect_duration_day": 0,
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
            "workflow": {
              "title": "长银钧信流程编排v3",
              "inclusions": [
                "gbiz_capital_workflow_asset"
              ],
              "props": {
                "CapitalRepayPlanProps": {
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
                          "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.98') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                          "err_msg": "长银钧信[资产还款总额]不满足 irr24，请关注！"
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
                          "policy": "success",
                          "ignoreNotify": False
                        },
                        "matches": [
                          {
                            "code": "2",
                            "messages": [
                              "0000_交易成功！"
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
                              "0001_mock测试授信申请失败"
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
                            "code": "2",
                            "messages": [
                              "0_Success_S_.*",
                              "0000_交易成功！_04_null_null",
                              "0_交易成功！_4_null_null"
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
                            "code": "2",
                            "messages": [
                              "0_交易成功！_2_null_null",
                              "0_交易成功！_授信金额小于资产本金_4_null_null"
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
                            "code": "2",
                            "messages": [
                              "0000_交易成功！_返回长银客户号为空_授信金额小于资产本金_01_null_null"
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
                          "policy": "success"
                        },
                        "matches": [
                          {
                            "code": "3",
                            "messages": [
                              "0000_交易成功！_100"
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
                            "code": "3",
                            "messages": [
                              "0000_交易成功！_300"
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
                            "code": "3",
                            "messages": [
                              "0000_交易成功！_200_清算成功"
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
                            "code": "3",
                            "messages": [
                              "0000_交易成功！_300_放款失败"
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
                            "code": "3",
                            "messages": [
                              "0000_交易成功！_100_",
                              "0000_交易成功！_请求返回放款金额 不等于 资产本金,请确认_100_"
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
                      "delayTime": "delayMinutes(10)",
                      "executeType": "auto",
                      "cancelable": False,
                      "simpleLock": {
                        "ttlSeconds": 10,
                        "key": "contractdown-changyin"
                      }
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
                  "id": "CertificateApplyVerifySync",
                  "type": "CertificateApplyVerifySyncTaskHandler",
                  "events":
                    [
                      "CertificateApplyReadyEvent"
                    ],
                  "activity":
                    {
                      "init":
                        {},
                      "finish":
                        []
                    }
                },
                {
                  "id": "CertificateApply",
                  "type": "CertificateApplyTaskHandler",
                  "events":
                    [
                      "CertificateApplySuccessEvent"
                    ],
                  "activity":
                    {
                      "init":
                        {},
                      "finish": [
                        {
                          "action": {
                            "policy": "success"
                          },
                          "matches": [
                            {
                              "code": "4",
                              "messages": [
                                "0_接收成功"
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
                  "events":
                    [],
                  "activity":
                    {
                      "init":
                        {
                          "delayTime": "delayMinutes(10)"
                        },
                      "execute":
                        {
                          "interval_in_minutes": "30"
                        }
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
                    "event": "RepayPlanHandleSucceededEvent"
                  },
                  "nodes": [
                    "OurRepayPlanRefine"
                  ]
                },
                {
                "listen": {
                      "event": "CertificateApplySuccessEvent"
                    },
                  "nodes":
                    [
                      "CertificateDownload"
                    ]
                },
                {
                  "listen":
                    {
                     "event": "CertificateApplyReadyEvent"
                    },
                  "nodes":
                    [
                      "CertificateApply"
                    ]
                }
              ]
            }
          }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_changyin_junxin", body)
def update_gbiz_capital_changyin_junxin_const():
    body = {
          "loanTyp": "KUN100",
          "priceIntRat": 0.085,
          "custDayRate": 0.24,
          "guaranteeType": "technical_service",
          "capitalFtpChannelName": "changyin_junxin",
          "periodicFilePath": "/download/cyxf/KUN100/out/files/%s",
          "bankCodeMap": {
            "icbc": "0102",
            "boc": "0104",
            "ccb": "0105",
            "spdb": "0310",
            "cgb": "0306",
            "pab": "04105840",
            "cib": "0309",
            "abc": "0103",
            "comm": "0301",
            "citic": "0302",
            "cmb": "0308",
            "hxb": "0304",
            "psbc": "0403",
            "ceb": "0303",
            "cmbc": "0305",
            "cabank": "03137950"
          },
          "genderMap": {
            "m": "10",
            "f": "20"
          },
          "marriageMap": {
            "0": "90",
            "1": "10",
            "2": "20",
            "3": "90",
            "4": "50"
          },
          "educationMap": {
            "1": "40",
            "2": "40",
            "3": "30",
            "4": "99",
            "5": "30",
            "6": "20",
            "7": "10",
            "8": "00",
            "9": "00"
          },
          "degreeMap": {
            "1": "5",
            "2": "5",
            "3": "5",
            "4": "5",
            "5": "5",
            "6": "5",
            "7": "4",
            "8": "3",
            "9": "2"
          },
          "acctTypMap": {
            "individual": "01",
            "enterprise": "02"
          },
          "professionMap": {
            "1": "40000",
            "2": "40000",
            "3": "40000",
            "4": "40000",
            "5": "60000",
            "6": "40000",
            "7": "40000",
            "8": "40000",
            "9": "20000",
            "10": "10000",
            "11": "40000",
            "12": "30000",
            "13": "40000",
            "14": "10000",
            "15": "50000"
          },
          "belongsIndusMap": {
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
          "relRelationMap": {
            "1": "09",
            "2": "01",
            "3": "02",
            "4": "03",
            "5": "08",
            "6": "05",
            "9": "99"
          },
          "purposeMap": {
            "1": "FLI",
            "2": "EDU",
            "3": "RENT",
            "4": "SJSM",
            "5": "TRA",
            "6": "JKYL",
            "7": "OTH",
            "8": "OTH",
            "9": "OTH"
          },
          "loanApplyUploadAttachmentList": [
            {
              "type": "1",
              "name": "idCardFront",
              "code": "1"
            },
            {
              "type": "2",
              "name": "idCardBack",
              "code": "2"
            },
            {
              "type": "29",
              "name": "faceRecognition",
              "code": "3"
            },
            {
              "type": "34800",
              "name": "credit-mix-protocol",
              "code": "21"
            },
            {
              "type": "34802",
              "name": "non-students-declaration",
              "code": "74"
            },
            {
              "type": "34801",
              "name": "debet-purpose-declaration",
              "code": "75"
            }
          ],
          "loanConfirmUploadAttachmentList": [
            {
              "type": "34803",
              "name": "digitalCertifacen",
              "code": "29"
            },
            {
              "type": "34807",
              "name": "withdrawProtocal",
              "code": "11"
            }
          ],
          "contractDownAttachmentList": [
            {
              "type": "28",
              "name": "changyinContract",
              "code": "7"
            },
            {
              "type": "34805",
              "name": "guaranteeContract",
              "code": "10"
            }
          ],
        "defaultGuarContAddr": "西安"
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_changyin_junxin_const", body)