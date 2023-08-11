import common.global_const as gc

# def update_gbiz_capital_mengshang_zhongyi_old():
#     data = {
#             "manual_reverse_allowed": False,
#             "cancelable_task_list": [
#                 "ApplyCanLoan",
#                 "LoanPreApply",
#                 "LoanApplyNew",
#                 "ChangeCapital"
#             ],
#             "raise_limit_allowed": False,
#             "register_config": {
#                 "account_register_duration": 20,
#                 "is_multi_account_card_allowed": True,
#                 "is_strict_seq": True,
#                 "post_register": False,
#                 "ref_accounts": None,
#                 "register_step_list": [
#                         {
#                             "channel": "mengshang_zhongyi",
#                             "step_type": "PAYSVR_PROTOCOL",
#                             "way": "tq",
#                             "sub_way": "baofoo_tq_protocol",
#                             "interaction_type": "SMS",
#                             "group": "kuainiu",
#                             "allow_fail": False,
#                             "need_confirm_result": True,
#                             "actions": [
#                                 {
#                                     "allow_fail": False,
#                                     "type": "GetSmsVerifyCode"
#                                 },
#                                 {
#                                     "allow_fail": False,
#                                     "type": "CheckSmsVerifyCode"
#                                 }
#                             ]
#                         }
#                 ]
#             },
#             "task_config_map": {
#                 "ChangeCapital": {
#                     "execute": {
#                         "event_handler_map": {
#                             "LoanApplySyncFailedEvent": "LoanApplyQuery",
#                             "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
#                             "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
#                             "GrantFailedEvent": "LoanConfirmQuery"
#                         },
#                         "can_change_capital": True
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
#                                         "切资方路由\\(二次\\)成功"
#                                     ]
#                                 }
#                             ]
#                         },
#                         {
#                             "action": {
#                                 "policy": "finalFail"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "12",
#                                     "messages": []
#                                 }
#                             ]
#                         },
#                         {
#                             "action": {
#                                 "policy": "fail"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "1",
#                                     "messages": [
#                                         "资方二次校验失败：未命中\\[fail,updateCard\\]策略.*"
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
#                                     "code": ""
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 "AssetImport": {
#                     "execute": {
#                         "loan_validator": [
#                             {
#                                 "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.90') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
#                                 "err_msg": "蒙商中裔[资产还款总额]不满足 irr24，请关注！"
#                             }
#                         ]
#                     }
#                 },
#                 "LoanPreApply": {
#                     "finish": [
#                         {
#                             "action": {
#                                 "policy": "success"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "0"
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 "LoanApplyNew": {
#                     "init": {
#                         "delayTime": "delaySeconds(5)"
#                     },
#                     "finish": [
#                         {
#                             "action": {
#                                 "policy": "success"
#                             },
#                             "matches": [
#                                 {
#                                     "code": "10500",
#                                     "messages": [
#                                         "\\[0501\\]交易已受理，请稍后查询交易结果"
#                                     ]
#                                 },
#                                 {
#                                     "code": "13400",
#                                     "messages": [
#                                         "\\[3402\\]申请流水号已经重复错误_资方返回业务申请流水号为空"
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
#                                     "code": "10001",
#                                     "messages": [
#                                         "MOCK的申请借款审核失败_资方返回业务申请流水号为空"
#                                     ]
#                                 },
#                                 {
#                                     "code": "10003",
#                                     "messages": [
#                                         "mock进件路由失败"
#                                     ]
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 "LoanApplyQuery": {
#                     "init": {
#                         "delayTime": "delaySeconds(2)"
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
#                                         "0000-\\[0001\\]交易成功"
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
#                                     "code": "10500",
#                                     "messages": [
#                                         "0500-\\[0501\\]交易已受理，请稍后查询交易结果"
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
#                                         "9999-MOCK审核查询失败"
#                                     ]
#                                 },
#                                 {
#                                     "code": "10000",
#                                     "messages": [
#                                         "0000-MOCK外层失败"
#                                     ]
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 "LoanPostApply": {
#                     "init": {
#                         "delayTime": "delaySeconds(120)"
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
#                                         "文件上传成功"
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
#                                     "code": "1",
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
#                                     "code": "20500",
#                                     "messages": [
#                                         "0500-\\[0501\\]交易已受理，请稍后查询交易结果"
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
#                                     "code": "20700",
#                                     "messages": [
#                                         "0700-Mock失败测试"
#                                     ]
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 "LoanConfirmQuery": {
#                     "init": {
#                         "delayTime": "delaySeconds(10)"
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
#                                         "0000-\\[0001\\]交易成功"
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
#                                     "code": "20500",
#                                     "messages": [
#                                         "0500-\\[0501\\]交易已受理，请稍后查询交易结果"
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
#                                         "0000-Mock外层放款失败测试"
#                                     ]
#                                 },
#                                 {
#                                     "code": "20008",
#                                     "messages": [
#                                         "0008-Mock内层code放款失败测试"
#                                     ]
#                                 }
#                             ]
#                         }
#                     ]
#                 },
#                 "CapitalRepayPlanQuery": {
#                     "execute": {
#                         "allow_diff_effect_at": False,
#                         "allow_diff_due_at": False,
#                         "allowance_check_range": {
#                             "min_value": 0,
#                             "max_value": 0
#                         }
#                     }
#                 },
#                 "OurRepayPlanRefine": {
#                     "execute": {
#                         "need_refresh_due_at": False
#                     }
#                 },
#                 "ContractDown": {
#                     "init": {
#                         "delayTime": "delayMinutes(60)"
#                     }
#                 },
#                 "AssetAutoImport": {
#                     "init": {
#                         "delayTime": "delayMinutes(90)"
#                     }
#                 }
#             }
#         }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_mengshang_zhongyi", data)

def update_gbiz_capital_mengshang_zhongyi():
    data = {
              "manual_reverse_allowed": False,
              "cancelable_task_list": [
                "ApplyCanLoan",
                "LoanPreApply",
                "LoanApplyNew",
                "ChangeCapital"
              ],
              "raise_limit_allowed": False,
              "register_config": {
                "account_register_duration": 20,
                "is_multi_account_card_allowed": True,
                "is_strict_seq": True,
                "post_register": False,
                "ref_accounts": None,
                "register_step_list": [
                  {
                    "channel": "mengshang_zhongyi",
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
                "title": "蒙商中裔放款流程编排v3",
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
                      "init": {},
                      "execute": {
                        "loan_validator": [
                          {
                            "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.90') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                            "err_msg": "蒙商中裔[资产还款总额]不满足 irr24，请关注！"
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
                    "id": "LoanPreApply",
                    "type": "LoanPreApplyTaskHandler",
                    "events": [
                      "LoanPreApplySyncSucceededEvent",
                      "LoanPreApplySyncFailedEvent"
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
                              "code": "0",
                              "messages": [
                                "文件上传成功"
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
                                ""
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
                      "init": {},
                      "execute": {},
                      "finish": [
                        {
                          "action": {
                            "policy": "success"
                          },
                          "matches": [
                            {
                              "code": "10500",
                              "messages": [
                                "\\[0501\\]交易已受理，请稍后查询交易结果"
                              ]
                            },
                            {
                              "code": "13400",
                              "messages": [
                                "\\[3402\\]申请流水号已经重复错误_资方返回业务申请流水号为空"
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
                              "code": "10001",
                              "messages": [
                                "MOCK的申请借款审核失败_资方返回业务申请流水号为空"
                              ]
                            },
                            {
                              "code": "10003",
                              "messages": [
                                "mock进件路由失败"
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
                            "policy": "success"
                          },
                          "matches": [
                            {
                              "code": "10000",
                              "messages": [
                                "0000-\\[0001\\]交易成功"
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
                              "code": "19999",
                              "messages": [
                                "9999-MOCK审核查询失败"
                              ]
                            },
                            {
                              "code": "10000",
                              "messages": [
                                "0000-MOCK外层失败"
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
                              "code": "10500",
                              "messages": [
                                "0500-\\[0501\\]交易已受理，请稍后查询交易结果"
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
                      "init": {},
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
                                "文件上传成功"
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
                              "code": "20500",
                              "messages": [
                                "0500-\\[0501\\]交易已受理，请稍后查询交易结果"
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
                              "code": "20700",
                              "messages": [
                                "0700-Mock失败测试"
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
                        "delayTime": "delayMinutes(2)"
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
                                "0000-\\[0001\\]交易成功"
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
                                "0000-Mock外层放款失败测试"
                              ]
                            },
                            {
                              "code": "20008",
                              "messages": [
                                "0008-Mock内层code放款失败测试"
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
                              "code": "20500",
                              "messages": [
                                "0500-\\[0501\\]交易已受理，请稍后查询交易结果"
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
                        "delayTime": "delaySeconds(10)"
                      },
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
                    "id": "AssetAutoImport",
                    "type": "AssetAutoImportTaskHandler",
                    "events": [],
                    "activity": {
                      "init": {
                        "delayTime": "delayMinutes(120)"
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
                                "资方二次校验失败：未命中\\[fail,updateCard\\]策略.*"
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
                              "code": "",
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
                    "id": "ContractDown",
                    "type": "ContractDownTaskHandler",
                    "events": [],
                    "activity": {
                      "execute": {
                        "interval_in_minutes": "240"
                      },
                      "init": {
                        "delayTime": "delayMinutes(60)"
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
                  }
                ],
                "subscribers": [
                    {
                        "memo": "资产导入就绪",
                        "listen": {
                            "event": "AssetImportReadyEvent",
                            "matches": []
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
                      "LoanPreApply"
                    ]
                  },
                  {
                    "memo": "授信前影像资料上传成功",
                    "listen": {
                      "event": "LoanPreApplySyncSucceededEvent"
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
                      "LoanPostApply"
                    ]
                  },
                  {
                    "memo": "支用前上传影像文件",
                    "listen": {
                      "event": "LoanPostApplySucceededEvent"
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
                      "ContractDown"
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
                    "memo": "切资方资产自动导入(虚拟事件和订阅，用于流程编排可视化)",
                    "listen": {
                      "event": "msgbus-AssetAutoImportMsgSendSuccess"
                    },
                    "nodes": [
                      "AssetImport"
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
                    "memo": "授信前上传影像失败",
                    "listen": {
                      "event": "LoanPreApplySyncFailedEvent"
                    },
                    "nodes": [
                      "ChangeCapital"
                    ],
                    "associateData": {
                      "skipDoubleCheck": False,
                      "event": "LoanPreApplySyncFailedEvent"
                    }
                  },
                  {
                    "memo": "同步进件申请失败",
                    "listen": {
                      "event": "LoanApplySyncFailedEvent"
                    },
                    "nodes": [
                      "ChangeCapital",
                      "BlacklistCollect"
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
                    "memo": "支用前上传影像文件失败",
                    "listen": {
                      "event": "LoanPostApplyFailedEvent"
                    },
                    "nodes": [
                      "ChangeCapital"
                    ],
                    "associateData": {
                      "skipDoubleCheck": False,
                      "event": "LoanPostApplyFailedEvent"
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
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_mengshang_zhongyi", data)
def update_gbiz_capital_mengshang_zhongyi_const():
    body = {
              "imageMaxAllowSize": 1572864,
              "imageMinAllowSize": 3072,
              "chanlNo": "0101030044",
              "prodSubNo": "530001",
              "mercNo": "kuainiu",
              "guaranteedCompany": "0401010031",
              "downloadFilePath": "/download/contract/%s/%s",
              "uploadFilePath": "/upload/media/%s",
              "sftpChannel": "mengshang_zhongyi",
              "attachmentFileMap": {
                "17": 29,
                "01": 1,
                "02": 2
              },
              "creditContractFileMap": {
                "18": 37002,
                "36": 37003,
                "06": 37000,
                "08": 37001
              },
              "eduDegreeMap": {
                "1": "10",
                "2": "10",
                "3": "20",
                "4": "30",
                "5": "40",
                "6": "40",
                "7": "60",
                "8": "70",
                "9": "80",
                "10": "99"
              },
              "defaultEduDegree": "99",
              "marriageMap": {
                "0": "50",
                "1": "20",
                "2": "10",
                "3": "40",
                "4": "30"
              },
              "defaultMarriage": "50",
              "loanUseMap": {
                "1": "10",
                "3": "07",
                "5": "03",
                "6": "09",
                "8": "10"
              },
              "defaultLoanUse": "02",
              "yearRate": "24",
              "positionMap": {
                "0": "0",
                "1": "1",
                "2": "2",
                "3": "3",
                "4": "4",
                "5": "5",
                "6": "6",
                "X": "X"
              },
              "defaultPosition": "Y",
              "relationMap": {
                "0": "3",
                "1": "1",
                "2": "1",
                "3": "1",
                "4": "1",
                "5": "2",
                "6": "2",
                "7": "3",
                "8": "1",
                "9": "1"
              },
              "defaultRelRelation": "3",
              "industryMap": {
                "0": "07"
              },
              "defaultIndustry": "07",
              "businessNatureMap": {
                "0": "Z"
              },
              "defaultBusinessNature": "Z",
              "scoreMap": {
                "0": "C",
                "613": "C",
                "614": "B",
                "637": "B",
                "638": "A",
                "950": "A"
              },
              "contractMap": {
                "37000": {
                  "type": 37005,
                  "fileKey": "06"
                },
                "37001": {
                  "type": 37006,
                  "fileKey": "08"
                },
                "37002": {
                  "type": 37007,
                  "fileKey": "18"
                },
                "37003": {
                  "type": 37008,
                  "fileKey": "36"
                },
                "37004": {
                  "type": 37010,
                  "fileKey": "07"
                },
                "37009": {
                  "type": 28,
                  "fileKey": "04"
                }
              },
              "loanContractFileMap": {
                "04": 37009,
                "07": 37004
              },
              "bankNoMap": {
                "psbc": "01000000",
                "icbc": "01020000",
                "abc": "01030000",
                "boc": "01040000",
                "ccb": "01050000",
                "comm": "03010000",
                "citic": "03020000",
                "ceb": "03030000",
                "hxbank": "03040000",
                "cmbc": "03050000",
                "gdb": "03060000",
                "cmb": "03080000",
                "cib": "03090000",
                "pdb": "03100000",
                "czbank": "03160000",
                "shbank": "04010000",
                "bjbank": "04031000",
                "nbbank": "04080000",
                "spabank": "04100000",
                "gcb": "04130000",
                "bhb": "04220000",
                "zzbank": "04350000",
                "hsbank": "04400000",
                "cqbank": "04410000",
                "lzyh": "04470000",
                "bsb": "04791920",
                "bjrcb": "1418100"
              },
              "statementConfig": {
                "ftpChannelName": "mengshang_zhongyi",
                "pathFormat": "/load/%s/%s",
                "targetFtpChannelName": "kuainiu",
                "targetFtpBasePath": "/mengshang_zhongyi/statement",
                "fileConfigList": [
                  {
                    "fileFormat": "%s_ORDER_STANDARD_%s%s",
                    "startLine": 2,
                    "fileSuffix": ".txt",
                    "separator": "|"
                  }
                ]
              },
              "chanlRiskinfos": [
                  {
                      "key": "gonganFaceTime",
                      "defaultValue": "1900-01-01",
                      "script": ""
                  },
                  {
                      "key": "gonganFaceResult",
                      "defaultValue": "03",
                      "script": ""
                  },
                  {
                      "key": "fourElementsResult",
                      "defaultValue": "01",
                      "script": ""
                  },
                  {
                      "key": "faceTime",
                      "defaultValue": "",
                      "script": ""
                  },
                  {
                      "key": "faceResult",
                      "defaultValue": "01",
                      "script": ""
                  },
                  {
                      "key": "faceScore",
                      "defaultValue": "",
                      "script": "#borrowerExtend.faceRecognizeScore"
                  },
                  {
                      "key": "idCert",
                      "defaultValue": "",
                      "script": "#borrowerExtend.idnumExpireDay"
                  },
                  {
                      "key": "riskLevel",
                      "defaultValue": "",
                      "script": "#borrowerExtend.aCardLevelScore"
                  },
                  {
                      "key": "realRate",
                      "defaultValue": "",
                      "script": "#calculateResDto.rateInfoDto.maxYearInterestRate"
                  },
                  {
                      "key": "contactsMobile",
                      "defaultValue": "",
                      "script": "#individual.relativeTelEncrypt"
                  },
                  {
                      "key": "contactsMobile2",
                      "defaultValue": "",
                      "script": "#individual.secondRelativeTelEncrypt"
                  },
                  {
                      "key": "systemType",
                      "defaultValue": "",
                      "script": "#borrowerExtend.deviceSys"
                  },
                  {
                      "key": "networkType",
                      "defaultValue": "",
                      "script": "#borrowerExtend.deviceNetworkType"
                  },
                  {
                      "key": "deviceId",
                      "defaultValue": "",
                      "script": "#borrowerExtend.deviceId"
                  },
                  {
                      "key": "latitude",
                      "defaultValue": "",
                      "script": "#borrowerExtend.latitude"
                  },
                  {
                      "key": "longitude",
                      "defaultValue": "",
                      "script": "#borrowerExtend.longitude"
                  },
                  {
                      "key": "model",
                      "defaultValue": "",
                      "script": "#borrowerExtend.deviceType"
                  },
                  {
                      "key": "brand",
                      "defaultValue": "",
                      "script": "#borrowerExtend.deviceType"
                  },
                  {
                      "key": "companyPhone",
                      "defaultValue": "",
                      "script": "#individual.corpTel"
                  },
                  {
                      "key": "companyAddress",
                      "defaultValue": "",
                      "script": "#individual.workplace"
                  }
              ]
            }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_mengshang_zhongyi_const", body)
