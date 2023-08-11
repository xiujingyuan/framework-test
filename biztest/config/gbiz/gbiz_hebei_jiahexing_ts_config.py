import common.global_const as gc

# def update_gbiz_capital_hebei_jiahexing_ts_old():
#     body = {
#               "cancelable_task_list": [
#                 "ApplyCanLoan",
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
#                     "channel": "hebei_jiahexing_ts",
#                     "step_type": "PAYSVR_PROTOCOL",
#                     "way": "tq",
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
#                         "rule": "loan.totalAmount>=cmdb.irr(#loan,'23.98') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
#                         "err_msg": "河北嘉合兴[资产还款总额]不满足 irr24，请关注！"
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
#                           "code": "0",
#                           "messages": [
#                             "影像资料上传成功"
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
#                           "code": "19999",
#                           "messages": [
#                             "遇到再配置"
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
#                           "code": "10000",
#                           "messages": [
#                             "0000_交易接收成功"
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
#                           "code": "19999",
#                           "messages": [
#                             "9000_交易处理失败"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                   "LoanApplyQuery": {
#                     "init": {
#                         "delay_time": "delaySeconds(60)"
#                     },
#                     "finish": [
#                         {
#                             "action": {
#                                 "policy": "success"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "10000",
#                                     "messages": [
#                                         "9999_交易处理成功_1_null_null"
#                                     ]
#                                 }
#                             ]
#                         },
#                         {
#                             "action": {
#                                 "policy": "fail"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "10000",
#                                     "messages": [
#                                         "9999_交易处理成功_0_年龄不在授信范围内_R009"
#                                     ]
#                                 },
#                                 {
#                                     "code": "10000",
#                                     "messages": [
#                                         "9999_交易处理成功_0_null_null"
#                                     ]
#                                 },
#                                 {
#                                     "code": "19999",
#                                     "messages": [
#                                         "1000_查无此交易_null_null_null"
#                                     ]
#                                 }
#                             ]
#                         },
#                         {
#                             "action": {
#                                 "policy": "retry"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "10000",
#                                     "messages": [
#                                         "9999_交易处理成功_2_null_null"
#                                     ]
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 "LoanPostApply": {
#                     "init": {
#                         "delay_time": "delayMinutes(8)"
#                     },
#                     "finish": [
#                         {
#                             "action": {
#                                 "policy": "success"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "0",
#                                     "messages": [
#                                         "影像资料上传成功"
#                                     ]
#                                 }
#                             ]
#                         },
#                         {
#                             "action": {
#                                 "policy": "fail"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "19999",
#                                     "messages": [
#                                         "遇到再配置"
#                                     ]
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 "LoanApplyConfirm": {
#                     "finish": [
#                         {
#                             "action": {
#                                 "policy": "success"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "20000",
#                                     "messages": [
#                                         "成功-SUCCESS-null-null",
#                                         "0000_交易接收成功"
#                                     ]
#                                 },
#                                 {
#                                     "code": "29999",
#                                     "messages": [
#                                         "1101_重复放款"
#                                     ]
#                                 }
#                             ]
#                         },
#                         {
#                             "action": {
#                                 "policy": "fail"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "20000",
#                                     "messages": [
#                                         "9999_交易接收失败"
#                                     ]
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 "LoanConfirmQuery": {
#                     "init": {
#                         "delay_time": "delaySeconds(120)"
#                     },
#                     "finish": [
#                         {
#                             "action": {
#                                 "policy": "success"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "20000",
#                                     "messages": [
#                                         "9999_交易处理成功_1_null_null"
#                                     ]
#                                 }
#                             ]
#                         },
#                         {
#                             "action": {
#                                 "policy": "fail"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "20000",
#                                     "messages": [
#                                         "9999_交易处理成功_0_null_null"
#                                     ]
#                                 },
#                                 {
#                                     "code": "29999",
#                                     "messages": [
#                                         "1000_查无此交易_null_null_null"
#                                     ]
#                                 }
#                             ]
#                         },
#                         {
#                             "action": {
#                                 "policy": "retry"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "20000",
#                                     "messages": [
#                                         "9999_交易处理成功_2_null_null"
#                                     ]
#                                 }
#                             ]
#                         }
#                     ]
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
#                   "init": {
#                     "delay_time": "delayHours(48)"
#                   }
#                 },
#                 "ContractPush": {
#                       "init": {
#                           "delay_time": "delayMinutes(10)"
#                       }
#                   },
#                 "AssetAutoImport": {
#                   "init": {
#                     "delay_time": "delayMinutes(90)"
#                   }
#                 },
#                   "CertificateApply": {
#                       "finish": [
#                           {
#                               "action": {
#                                   "policy": "success"
#                               },
#                               "matches": [
#                                   {
#                                       "code": "10000",
#                                       "messages": [
#                                           "0000_交易接收成功"
#                                       ]
#                                   },
#                                   {
#                                       "code": "19999",
#                                       "messages": [
#                                           "1102_结清证明已申请"
#                                       ]
#                                   }
#                               ]
#                           },
#                           {
#                               "action": {
#                                   "policy": "retry"
#                               },
#                               "matches": [
#                                   {
#                                       "code": "1000000",
#                                       "messages": [
#                                           "遇到在配置"
#                                       ]
#                                   }
#                               ]
#                           },
#                           {
#                               "action": {
#                                   "policy": "fail"
#                               },
#                               "matches": [
#                                   {
#                                       "code": "1000000",
#                                       "messages": [
#                                           "遇到在配置"
#                                       ]
#                                   }
#                               ]
#                           }
#                       ]
#                   }
#               }
#             }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hebei_jiahexing_ts", body)

def update_gbiz_capital_hebei_jiahexing_ts():
    body = {
              "cancelable_task_list": [
                "ApplyCanLoan",
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
                    "channel": "hebei_jiahexing_ts",
                    "step_type": "PAYSVR_PROTOCOL",
                    "way": "tq",
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
                "title": "河北嘉合兴泰山放款流程编排V3",
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
                            "rule": "loan.totalAmount>=cmdb.irr(#loan,'23.98') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                            "err_msg": "河北嘉合兴[资产还款总额]不满足 irr24，请关注！"
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
                                "影像资料上传成功"
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
                              "code": "10000",
                              "messages": [
                                "0000_交易接收成功"
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
                                "9000_交易处理失败"
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
                            "policy": "success",
                            "ignoreNotify": False
                          },
                          "matches": [
                            {
                              "code": "10000",
                              "messages": [
                                "9999_交易处理成功_1_null_null"
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
                              "code": "10000",
                              "messages": [
                                "9999_交易处理成功_0_年龄不在授信范围内_R009"
                              ]
                            },
                            {
                              "code": "10000",
                              "messages": [
                                "9999_交易处理成功_0_null_null"
                              ]
                            },
                            {
                              "code": "19999",
                              "messages": [
                                "1000_查无此交易_null_null_null"
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
                              "code": "10000",
                              "messages": [
                                "9999_交易处理成功_2_null_null"
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
                        "delayTime": "delayMinutes(8)"
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
                                "影像资料上传成功"
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
                              "code": "20000",
                              "messages": [
                                "成功-SUCCESS-null-null",
                                "0000_交易接收成功"
                              ]
                            },
                            {
                              "code": "29999",
                              "messages": [
                                "1101_重复放款"
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
                              "code": "20000",
                              "messages": [
                                "9999_交易接收失败"
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
                              "code": "20000",
                              "messages": [
                                "9999_交易处理成功_1_null_null"
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
                              "code": "20000",
                              "messages": [
                                "9999_交易处理成功_0_null_null"
                              ]
                            },
                            {
                              "code": "29999",
                              "messages": [
                                "1000_查无此交易_null_null_null"
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
                              "code": "20000",
                              "messages": [
                                "9999_交易处理成功_2_null_null"
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
                        "need_refresh_due_at": False
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
                        "delayTime": "delayHours(48)"
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
                        "delayTime": "delayMinutes(10)"
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
                      "execute": {},
                      "finish": []
                    }
                  },
                  {
                    "id": "CertificateApplyVerify",
                    "type": "CertificateApplyVerifySyncTaskHandler",
                    "events": [
                      "CertificateApplyReadyEvent"
                    ],
                    "activity": {
                      "execute": {},
                      "init": {}
                    }
                  },
                  {
                    "id": "CertificateApply",
                    "type": "CertificateApplyTaskHandler",
                    "events": [
                      "CertificateApplySuccessEvent"
                    ],
                    "activity": {
                      "execute": {},
                      "init": {},
                      "finish": [
                        {
                          "action": {
                            "policy": "success"
                          },
                          "matches": [
                            {
                              "code": "10000",
                              "messages": [
                                "0000_交易接收成功"
                              ]
                            },
                            {
                              "code": "19999",
                              "messages": [
                                "1102_结清证明已申请"
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
                                "遇到在配置"
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
                              "code": "1000000",
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
                    "id": "CertificateDownload",
                    "type": "CertificateDownloadTaskHandler",
                    "events": [],
                    "activity": {
                      "execute": {
                        "interval_in_minutes": "240"
                      }
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
                      "event": "LoanApplyAsyncFailedEvent"
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
                      "LoanPostApply"
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
                    "memo": "结清证明申请",
                    "listen": {
                      "event": "CertificateApplyReadyEvent"
                    },
                    "nodes": [
                      "CertificateApply"
                    ]
                  },
                  {
                    "memo": "结清证明申请成功",
                    "listen": {
                      "event": "CertificateApplySuccessEvent"
                    },
                    "nodes": [
                      "CertificateDownload"
                    ]
                  }
                ]
              }
            }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hebei_jiahexing_ts", body)
def update_gbiz_capital_hebei_jiahexing_ts_const():
    body = {
              "ftpName": "hebei_jiahexing_ts",
              "ftpBasePath": "/sftp",
              "creditApplyFtpPath": "/10010/SX/",
              "guaranteeFtpPath": "/10010/RD/",
              "loanApplyFtpPath": "/10010/FK/",
              "uploadAttachmentMap": {
                "1": "certFileB_%s.jpg",
                "2": "certFileA_%s.jpg",
                "29": "facephoto_%s.jpg"
              },
              "uploadContractMap": {
                "35000": "investigationAuthorization_%s.pdf",
                "35001": "infoUseAuthorization_%s.pdf",
                "35002": "infoQueryAuthorization_%s.pdf",
                "35003": "loanusePromise_%s.pdf"
              },
              "guaranteeFileUploadMap": {
                "35004": "investigationAuthorizationRD_%s.pdf",
                "35005": "guacont_%s.pdf",
                "35007": "deductAuthorization_%s.pdf"
              },
              "loanApplyUploadMap": {
                "35006": "contract_%s.pdf"
              },
              "guaranteeFileSyncType": "FINGUARANT_FILE",
              "contractDownloadMap": {
                "28": {
                  "basePath": "/sftp/11003",
                  "fileNameFormat": "signedcontract_%s.pdf"
                }
              },
              "termTypeMap": {
                "month": "M",
                "day": "D"
              },
              "loanUseMap": {
                "1": "10",
                "2": "16",
                "3": "18",
                "4": "20",
                "5": "13",
                "6": "17",
                "7": "17",
                "8": "11",
                "9": "20"
              },
              "loanUseDetailMap": {
                "1": "1000",
                "2": "1600",
                "3": "1800",
                "4": "2004",
                "5": "1300",
                "6": "1700",
                "7": "1701",
                "8": "1100",
                "9": "2000"
              },
              "genderMap": {
                "m": "M",
                "f": "F"
              },
              "essdegrMap": {
                "1": "80",
                "2": "70",
                "3": "60",
                "4": "50",
                "5": "40",
                "6": "30",
                "7": "20",
                "8": "14",
                "9": "11"
              },
              "degreeMap": {},
              "marriagMap": {
                "1": "10",
                "2": "20",
                "3": "30",
                "4": "40"
              },
              "workstMap": {
                "1": "24",
                "2": "16",
                "3": "51",
                "4": "70",
                "5": "90",
                "6": "90"
              },
              "industryMap": {
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
              "jobNatureMap": {},
              "jobMap": {},
              "dutyMap": {},
              "jobTitleMap": {},
              "relRelationMap": {
                "0": "C",
                "1": "F",
                "2": "E",
                "3": "H",
                "4": "W",
                "5": "T",
                "6": "Y",
                "7": "O"
              },
              "cityIpGpsInfo": [
                "130100-39.134.187.0#39.134.193.255-114.30,38.02,5",
                "130200-27.129.8.0#27.129.15.255-118.10,39.36,5",
                "130300-27.129.40.0#27.129.43.255-119.50,39.55,5",
                "130400-27.129.24.0#27.129.31.255-114.20,36.30,5",
                "130500-27.129.48.0#27.129.51.25-114.48,37.07,5",
                "130600-27.128.192.0#27.128.207.255-115.45,38.30,5",
                "130700-27.129.52.0#27.129.55.255-114.52,40.50,5",
                "130800-27.129.60.0#27.129.63.255-118.20,40.80,5",
                "130900-27.129.44.0#27.129.47.255-116.83,38.30,5",
                "131000-27.128.208.0#27.128.223.255-116.70,39.52,5",
                "131100-27.128.80.0#27.128.81.255-115.68,37.73,5",
                "370100-1.51.144.0#1.51.159.255-117.10,36.40,5",
                "370200-27.221.80.0#27.221.95.255-120.38,36.07,5",
                "370300-58.58.96.0#58.58.109.255-118.05,36.82,5",
                "370400-58.57.224.0#58.57.255.255-117.33,34.52,5",
                "370500-58.57.128.0#58.57.159.255-118.49,37.46,5",
                "370600-58.58.80.0#58.58.95.255-121.39,37.52,5",
                "370700-39.90.64.0#39.90.127.255-119.10,36.62,5",
                "370800-58.58.48.0#58.58.63.255-116.59,35.38,5",
                "370900-27.221.160.0#27.221.191.255-117.13,36.18,5",
                "371000-58.58.208.0#58.58.223.255-122.10,37.50,5",
                "371100-58.58.176.0#58.58.191.255-119.46,35.42,5",
                "371600-58.58.0.0#58.58.15.255-118.03,37.36,5",
                "371400-1.51.168.0#1.51.191.255-116.29,37.45,5",
                "371500-27.222.96.0#27.222.127.255-115.97,36.45,5",
                "371300-58.57.32.0#58.57.63.255-118.35,35.05,5",
                "371700-39.87.192.0#39.87.223.255-115.43,35.24,5",
                "120000-27.0.128.0#27.0.135.255-117.20,39.13,5"
              ],
              "bankLineNoMap": {
                "ICBC": "102100004951",
                "CCB": "105100000017",
                "BOC": "104100000004",
                "ABC": "103100000018",
                "SPDB": "310290000013",
                "CITIC": "302100011000",
                "HXB": "304100040000",
                "CMBC": "305100000013",
                "GDB": "306581000003",
                "CIB": "309391000011",
                "PAB": "307584008005",
                "CZBANK": "316331000018",
                "EGBANK": "315456000105",
                "BH": "318110000014",
                "SHBANK": "325290000012",
                "BJBANK": "313100000013",
                "SHB": "325290000012"
              },
            "itemNoContractDownloadDate": {   # 这个配置是用来，当合同下载任务下载时间不对时，可以在这里将对应资产的事件映射为固定时间
                "B2023031375499000536": "20230315"
            },
        "certificateDownloadMap": {
            "24": {
                "basePath": "/sftp/11007",
                "fileNameFormat": "payoffproof_%s.pdf"
            }
        },
        "certificateDownloadInterval": 0  # 这个配置是用于结清证明下载的目录是否当日下载，0是当日下载，1是前一天，但是线上不配置，默认前一天下载
            }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hebei_jiahexing_ts_const", body)