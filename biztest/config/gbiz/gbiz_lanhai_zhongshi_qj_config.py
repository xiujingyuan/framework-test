
import common.global_const as gc


# def update_gbiz_capital_lanhai_zhongshi_qj_old():
#     body = {
#         "manual_reverse_allowed": False,
#         "cancelable_task_list": [
#             "ApplyCanLoan",
#             "LoanApplyNew",
#             "ChangeCapital"
#         ],
#         "raise_limit_allowed": False,
#         "register_config": {
#             "register_step_list": [
#                 {
#                     "step_type": "PROTOCOL",
#                     "channel": "lanhai_zhongshi_qj",
#                     "interaction_type": "SMS",
#                     "status_scene": {
#                         "register": {
#                             "success_type": "once",
#                             "register_status_effect_duration_day": 0,
#                             "allow_fail": False,
#                             "need_confirm_result": False
#                         },
#                         "route": {
#                             "success_type": "once",
#                             "allow_fail": False
#                         },
#                         "validate": {
#                             "success_type": "once"
#                         }
#                     },
#                     "actions": [
#                         {
#                             "allow_fail": False,
#                             "type": "GetSmsVerifyCode"
#                         },
#                         {
#                             "allow_fail": False,
#                             "type": "CheckSmsVerifyCode"
#                         }
#                     ],
#                     "way": "lanhai_zhongshi_qj"
#                 }
#             ]
#         },
#         "task_config_map": {
#             "ChangeCapital": {
#                 "execute": {
#                     "event_handler_map": {
#                         "GrantFailedEvent": "LoanConfirmQuery",
#                         "LoanApplySyncFailedEvent": "LoanApplyQuery",
#                         "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
#                         "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
#                         "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
#                         "LoanCreditFailedEvent": "LoanCreditQuery"
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
#                                 "messages": [
#
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
#                                 "code": "1",
#                                 "messages": [
#                                     "遇到再进行配置"
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
#                                 "code": "-10000",
#                                 "messages": [
#                                     "遇到再进行配置"
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
#                             "rule": "#loan.totalAmount>=cmdb.irr(#loan,'35.90') && #loan.totalAmount<=cmdb.irr(#loan,'35.95')",
#                             "err_msg": "蓝海中世亲家[资产还款总额]不满足 [35.90,35.95]，请关注！"
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
#                                     "01-0000-成功-成功"
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
#                                 "code": "1555555",
#                                 "messages": [
#                                     "--contactmobile联系人电话长度超限-",
#                                     "--idsigndate证件签发日期 YYYY-MM-DD格式错误-"
#                                 ]
#                             },
#                             {
#                                 "code": "1000000",
#                                 "messages": [
#                                     "02-0000-mock失败-sendmsg失败"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanApplyQuery": {
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
#                                 "code": "待配置"
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanPostApply": {
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "01-0000-成功-"
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
#                                 "code": "1999999",
#                                 "messages": [
#                                     "--RUTE-系统异常-"
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
#                                 "code": "1",
#                                 "messages": [
#                                     "遇到再配置"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "00-0000-成功-路由处理中"
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
#                                 "code": "1700013",
#                                 "messages": [
#                                     "--存在处理中申请-"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "02-9999-mock失败-路由mock失败"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "LoanCreditQuery": {
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "01-0001-成功-路由成功"
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
#                                     "00-0000-成功-"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "02-0005-成功-银行风控拒绝",
#                                     "02-9999-成功-路由失败",
#                                     "02-0004-成功-亲家风控拒绝",
#                                     "02-0005-成功-个人可用额度等于零",
#                                     "02-0004-mock授信失败-"
#                                 ]
#                             },
#                             {
#                                 "code": "9000",
#                                 "messages": [
#                                     "当前资产待放金额.*大于查询返回授信成功金额.*"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "00-0000-成功-"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "02-1002-mock失败-"
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
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "1000000",
#                                 "messages": [
#                                     "01-0001-成功-"
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
#                                     "00-0000-成功-"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "02-1001-mock失败-"
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
#                         "technical_service"
#                     ],
#                     "allow_diff_effect_at": False,
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
#             "ContractDown": {
#                 "init": {
#                     "delay_time": "delayDays(1, \"08:00:00\")",
#                     "simple_lock": {
#                         "key": "contractdown-ftp",
#                         "ttlSeconds": 60
#                     }
#                 }
#             },
#             "AssetAutoImport": {
#                 "init": {
#                     "delay_time": "delayMinutes(90)"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "01-true-成功-处理成功",
#                                     "02-false-成功-提交失败,已存在提交的数据"
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
#                                     "遇到在配置"
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
#                                 "code": "1000000",
#                                 "messages": [
#                                     "遇到在配置"
#                                 ]
#                             }
#                         ]
#                     }
#                 ]
#             },
#             "CertificateDownload": {
#                 "execute": {
#                     "interval_in_minutes": "120"
#                 },
#                 "init": {
#                     "delay_time": "delayDays(1, \"07:00:00\")"
#                 }
#             }
#         }
#
#     }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanhai_zhongshi_qj", body)

def update_gbiz_capital_lanhai_zhongshi_qj():
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
                  "channel": "lanhai_zhongshi_qj",
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
                  ],
                  "way": "lanhai_zhongshi_qj"
                }
              ]
            },
            "workflow": {
              "title": "蓝海中世亲家流程编排v3",
              "inclusions": [
                "gbiz_capital_workflow_asset"
              ],
              "props": {
                "CapitalRepayPlanProps": {
                   "need_refresh_due_at": False,
                  "allow_diff_effect_at": False,
                  "allow_diff_due_at": False,
                      "adjust_fee_list": [
                        "guarantee",
                        "technical_service"
                      ],
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
                  "activity": {
                    "init": {},
                    "execute": {
                      "loan_validator": [
                        {
                          "rule": "#loan.totalAmount>=cmdb.irr(#loan,'35.90') && #loan.totalAmount<=cmdb.irr(#loan,'35.95')",
                          "err_msg": "蓝海中世亲家[资产还款总额]不满足 [35.90,35.95]，请关注！"
                        }
                      ]
                    }
                  }
                },
                {
                  "id": "AssetImportVerify",
                  "type": "AssetImportVerifyTaskHandler",
                  "events": [
                    "AssetImportVerifySucceededEvent"
                  ],
                  "activity": {
                    "init": {}
                  }
                },
                {
                  "id": "ApplyCanLoan",
                  "type": "ApplyCanLoanTaskHandler",
                  "activity": {
                    "init": {
                      "executeType": "auto",
                      "returnMsg": "执行进件前校验",
                      "cancelable": True,
                      "delayTime": "delaySeconds(60)"
                    }
                  }
                },
                {
                  "id": "LoanApplyNew",
                  "type": "LoanApplyNewTaskHandler",
                  "activity": {
                    "init": {},
                    "finish": [
                      {
                        "action": {
                          "policy": "success"
                        },
                        "matches": [
                          {
                            "code": "1000000",
                            "messages": [
                              "01-0000-成功-成功"
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
                            "code": "1555555",
                            "messages": [
                              "--contactmobile联系人电话长度超限-",
                              "--idsigndate证件签发日期 YYYY-MM-DD格式错误-"
                            ]
                          },
                          {
                            "code": "1000000",
                            "messages": [
                              "02-0000-mock失败-sendmsg失败"
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
                    "init": {},
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
                            "code": "待配置"
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
                    "LoanPostApplySucceededEvent"
                  ],
                  "activity": {
                    "init": {
                      "delayTime": "delaySeconds(120)"
                    },
                    "finish": [
                      {
                        "action": {
                          "policy": "success"
                        },
                        "matches": [
                          {
                            "code": "1000000",
                            "messages": [
                              "01-0000-成功-"
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
                            "code": "1999999",
                            "messages": [
                              "--RUTE-系统异常-"
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
                  "id": "LoanCreditApply",
                  "type": "LoanCreditApplyTaskHandler",
                  "events": [
                    "LoanCreditApplySyncSucceededEvent",
                    "LoanCreditApplySyncFailedEvent"
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
                            "code": "1000000",
                            "messages": [
                              "00-0000-成功-路由处理中"
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
                            "code": "1700013",
                            "messages": [
                              "--存在处理中申请-"
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
                              "02-9999-mock失败-路由mock失败"
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
                      "delayTime": "delaySeconds(60)"
                    },
                    "finish": [
                      {
                        "action": {
                          "policy": "success"
                        },
                        "matches": [
                          {
                            "code": "1000000",
                            "messages": [
                              "01-0001-成功-路由成功"
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
                              "00-0000-成功-"
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
                              "02-0005-成功-银行风控拒绝",
                              "02-9999-成功-路由失败",
                              "02-0004-成功-亲家风控拒绝",
                              "02-0005-成功-个人可用额度等于零",
                              "02-0004-mock授信失败-"
                            ]
                          },
                          {
                            "code": "9000",
                            "messages": [
                              "当前资产待放金额.*大于查询返回授信成功金额.*"
                            ]
                          }
                        ]
                      }
                    ]
                  }
                },
                {
                  "id": "ContractSignature",
                  "type": "ContractSignatureTaskHandler",
                  "activity": {
                    "init": {}
                  }
                },
                {
                  "id": "ContractPush",
                  "type": "ContractPushTaskHandler",
                  "activity": {
                    "init": {}
                  }
                },
                {
                  "id": "LoanApplyConfirm",
                  "type": "LoanApplyConfirmTaskHandler",
                  "activity": {
                    "init": {},
                    "finish": [
                      {
                        "action": {
                          "policy": "success"
                        },
                        "matches": [
                          {
                            "code": "1000000",
                            "messages": [
                              "00-0000-成功-"
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
                              "02-1002-mock失败",
                              "02-1002-mock失败-"
                            ]
                          },
                          {
                            "code": "1800016",
                            "messages": [
                              "--放款文件不存在-"
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
                    "finish": [
                      {
                        "action": {
                          "policy": "success"
                        },
                        "matches": [
                          {
                            "code": "1000000",
                            "messages": [
                              "01-0001-成功-"
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
                              "00-0000-成功-"
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
                              "02-1001-mock失败-"
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
                  "activity": {
                    "init": {},
                    "execute": {
                      "props_key": "CapitalRepayPlanProps"
                    }
                  }
                },
                {
                  "id": "ContractDown",
                  "type": "ContractDownTaskHandler",
                  "events": [],
                  "activity": {
                    "init": {
                      "delayTime": "delayDays(1, \"08:00:00\")",
                      "simple_lock": {
                        "key": "contractdown-ftp",
                        "ttlSeconds": 60
                      }
                    }
                  }
                },
                {
                      "id": "CertificateApplySync",
                      "type": "CertificateApplyVerifySyncTaskHandler",
                      "events": ["CertificateApplyReadyEvent"],
                      "activity": {
                          "init": {
                              "delayTime": "delayMinutes(90)"
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
                    "init": {},
                    "finish": [
                      {
                        "action": {
                          "policy": "success"
                        },
                        "matches": [
                          {
                            "code": "1000000",
                            "messages": [
                              "01-true-成功-处理成功",
                              "02-false-成功-提交失败,已存在提交的数据"
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
                              "02-False-成功-借款未结清"
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
                      "interval_in_minutes": "120"
                    },
                    "init": {
                      "delayTime": "delayDays(1, \"07:00:00\")"
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
                  "activity": {
                    "init": {
                      "delayTime": "delayMinutes(90)"
                    }
                  }
                },
                {
                  "id": "ChangeCapital",
                  "type": "ChangeCapitalTaskHandler",
                  "activity": {
                    "init": {
                      "executeType": "manual"
                    },
                    "execute": {
                      "event_handler_map": {
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
                        "LoanCreditFailedEvent": "LoanCreditQuery"
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
                    "event": "AssetImportSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "AssetImportVerify"
                  ]
                },
                {
                  "memo": "资产就绪事件",
                  "listen": {
                    "event": "AssetReadyEvent",
                    "matches": []
                  },
                  "nodes": [
                    "LoanApplyNew"
                  ]
                },
                {
                  "memo": "同步进件成功",
                  "listen": {
                    "event": "LoanApplySyncSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "LoanApplyQuery"
                  ]
                },
                {
                  "memo": "异步进件成功",
                  "listen": {
                    "event": "LoanApplyAsyncSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "LoanPostApply"
                  ]
                },
                {
                  "memo": "进件后处理成功",
                  "listen": {
                    "event": "LoanPostApplySucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "LoanCreditApply"
                  ]
                },
                {
                  "memo": "授信同步成功",
                  "listen": {
                    "event": "LoanCreditApplySyncSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "LoanCreditQuery"
                  ]
                },
                {
                  "memo": "授信异步成功",
                  "listen": {
                    "event": "LoanCreditSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "ContractSignature"
                  ]
                },
                {
                  "memo": "合同签章成功",
                  "listen": {
                    "event": "ContractSignatureSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "ContractPush"
                  ]
                },
                {
                  "memo": "合同推送成功",
                  "listen": {
                    "event": "ContractPushSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "LoanApplyConfirm"
                  ]
                },
                {
                  "memo": "放款申请成功",
                  "listen": {
                    "event": "ConfirmApplySyncSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "LoanConfirmQuery"
                  ]
                },
                {
                  "memo": "放款成功",
                  "listen": {
                    "event": "GrantSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "CapitalRepayPlanQuery",
                    "ContractDown"
                  ]
                },
                {
                  "memo": "还款计划查询成功",
                  "listen": {
                    "event": "RepayPlanHandleSucceededEvent",
                    "matches": []
                  },
                  "nodes": [
                    "OurRepayPlanRefine"
                  ]
                },


                {
                  "memo": "资方进件前校验失败",
                  "listen": {
                    "event": "AssetCanLoanFailedEvent",
                    "matches": []
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
                  "memo": "资方放款失败",
                  "listen": {
                    "event": "GrantFailedEvent",
                    "matches": []
                  },
                  "nodes": [
                    "ChangeCapital"
                  ],
                  "associateData": {
                    "skipDoubleCheck": False,
                    "event": "GrantFailedEvent",
                    "sourceWorkflowNodeId": "LoanConfirmQuery"
                  }
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
                  "memo": "同步请款申请失败",
                  "listen": {
                    "event": "ConfirmApplySyncFailedEvent",
                    "matches": []
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
                  "memo": "同步进件申请失败",
                  "listen": {
                    "event": "LoanApplySyncFailedEvent",
                    "matches": []
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
                  "memo": "进件后处理失败",
                  "listen": {
                    "event": "LoanPostApplyFailedEvent",
                    "matches": []
                  },
                  "nodes": [
                    "ChangeCapital"
                  ],
                  "associateData": {
                    "skipDoubleCheck": True,
                    "event": "LoanPostApplyFailedEvent"
                  }
                },
                {
                  "memo": "异步进件申请失败",
                  "listen": {
                    "event": "LoanApplyAsyncFailedEvent",
                    "matches": []
                  },
                  "nodes": [
                    "ChangeCapital"
                  ],
                  "associateData": {
                    "skipDoubleCheck": False,
                    "event": "LoanApplyAsyncFailedEvent",
                    "sourceWorkflowNodeId": "LoanApplyQuery"
                  }
                },
                {
                  "memo": "授信同步失败",
                  "listen": {
                    "event": "LoanCreditApplySyncFailedEvent",
                    "matches": []
                  },
                  "nodes": [
                    "ChangeCapital",
                    "BlacklistCollect"
                  ],
                  "associateData": {
                    "skipDoubleCheck": False,
                    "event": "LoanCreditApplySyncFailedEvent",
                    "sourceWorkflowNodeId": "LoanCreditQuery"
                  }
                },
                {
                  "memo": "授信异步查询查询失败",
                  "listen": {
                    "event": "LoanCreditFailedEvent",
                    "matches": []
                  },
                  "nodes": [
                    "ChangeCapital",
                    "BlacklistCollect"
                  ],
                  "associateData": {
                    "skipDoubleCheck": False,
                    "event": "LoanCreditFailedEvent",
                    "sourceWorkflowNodeId": "LoanCreditQuery"
                  }
                },
                {
                      "memo": "结清证明准备",
                      "listen": {
                          "event": "CertificateApplyReadyEvent",
                          "matches": []
                      },
                      "nodes": [
                          "CertificateApply"
                      ]
                  },
                {
                  "memo": "结清证明申请成功",
                  "listen": {
                    "event": "CertificateApplySuccessEvent",
                    "matches": []
                  },
                  "nodes": [
                    "CertificateDownload"
                  ]
                }
              ]
            }
          }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanhai_zhongshi_qj", body)

def update_gbiz_capital_lanhai_zhongshi_qj_const():
    body = {
        "defaultACardLevelScore": "666",
        "channel": "KN10001",
        "ftpChannelName": "lanhai_zhongshi_qj",
        "ftpFileMaxSize": 3145728,
        "imageCompressScale": 0.5,
        "imageCompressQuantity": 0.8,
        "productIdMap": {
            "new_backup": "201P1ZSLHS",
            "new": "201P2ZSLHS",
            "old": "201P2ZSLHS"
        },
        "pickupBankIdMap": {
            "ICBC": "102100099996",
            "ABC": "103100000026",
            "BOC": "104100000004",
            "CCB": "105100000017",
            "COMM": "301290000007",
            "CITIC": "302100011000",
            "CEB": "303100000006",
            "HXBANK": "304100040000",
            "CMBC": "305100000013",
            "GDB": "306581000003",
            "PAB": "307584007998",
            "CMB": "308584000013",
            "CIB": "309391000011",
            "SPDB": "310290000013",
            "BJBANK": "313100000013",
            "SHBANK": "325290000012"
        },
        "loanUseMap": {
            "1": "1",
            "2": "2",
            "3": "9",
            "4": "1",
            "5": "4",
            "6": "2",
            "7": "2",
            "8": "2",
            "9": "1"
        },
        "educationMap": {
            "1": "90",
            "2": "60",
            "3": "40",
            "4": "40",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "14",
            "9": "11"
        },
        "marriageMap": {
            "1": "10",
            "2": "99",
            "3": "40",
            "4": "30"
        },
        "degreeMap": {
            "1": "05",
            "2": "05",
            "3": "05",
            "4": "05",
            "5": "05",
            "6": "05",
            "7": "04",
            "8": "03",
            "9": "02"
        },
        "industryMap": {
            "1": "O",
            "2": "I",
            "3": "H",
            "4": "K",
            "5": "C",
            "6": "F",
            "7": "M",
            "8": "G",
            "9": "Q",
            "10": "P",
            "11": "J",
            "12": "Q",
            "13": "R",
            "14": "S",
            "15": "A"
        },
        "relationMap": {
            "0": "C",
            "1": "D",
            "2": "B",
            "3": "H",
            "4": "W",
            "5": "T",
            "6": "Y",
            "7": "O"
        },
        "jobDetailMap": {
            "1": "4J",
            "2": "4C",
            "3": "4A",
            "4": "6C",
            "5": "6R",
            "6": "3C",
            "7": "6J",
            "8": "4D",
            "9": "6L",
            "10": "2H",
            "11": "2F",
            "12": "2G",
            "13": "4M",
            "14": "3A",
            "15": "5Z"
        },
        "postApplyPushAttachments": [
            {
                "attachmentType": "34011",
                "fileType": "lhregion",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "34000",
                "fileType": "lhcredit",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "34001",
                "fileType": "lhquery",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "34002",
                "fileType": "lhlimit",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "34003",
                "fileType": "qjcredit",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "34004",
                "fileType": "deduction",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "1",
                "fileType": "idcardfront",
                "suffix": "jpg",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "2",
                "fileType": "idcardback",
                "suffix": "jpg",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "29",
                "fileType": "face",
                "suffix": "jpg",
                "remoteDir": "/cpu/KN10001/need/"
            }
        ],
        "postCreditPushAttachments": [
            {
                "attachmentType": "34012",
                "fileType": "danbaoconsult",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "34006",
                "fileType": "loancount",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            },
            {
                "attachmentType": "34005",
                "fileType": "danbaocount",
                "suffix": "pdf",
                "remoteDir": "/cpu/KN10001/need/"
            }
        ],
        "contractFtpMappingMap": {
            "28": {
                "base_path": "/cpu/KN10001/contract/",
                "business_no_type": "due_bill_no",
                "suffix": "_loan.pdf"
            },
            "34010": {
                "base_path": "/cpu/KN10001/contract/",
                "business_no_type": "router_no",
                "suffix": "_limit.pdf"
            }
        },
        "contractQuerySigned": {
            "34007": "rd"
        },
        "bankIdMap": {
            "ICBC": "1021",
            "CCB": "1051",
            "BOC": "1041",
            "ABC": "1031",
            "CMB": "3081",
            "SPDB": "3101",
            "CITIC": "3021",
            "HXB": "3041",
            "CMBC": "30510",
            "GDB": "3061",
            "CIB": "3091",
            "PAB": "7832",
            "CZBANK": "31633",
            "EGBANK": "31545",
            "BOHAIB": "31811",
            "SHBANK": "3131",
            "BJBANK": "30310"
        },
        "warrantNo": "R004",
        "districtKeyword": "山东",
        "ipPool": [
            "58.14.0.0-58.15.255.255",
            "60.217.192.0-60.217.255.255",
            "60.232.128.0-60.233.255.255",
            "112.36.128.0-112.36.255.255",
            "113.125.0.0-113.129.27.255",
            "39.87.224.0-39.89.255.255",
            "60.209.0.0-60.209.255.255",
            "112.225.0.0-112.226.255.255",
            "123.234.0.0-123.235.255.255",
            "116.154.0.0-116.154.127.255",
            "222.134.64.0-222.134.159.255",
            "182.46.64.0-182.46.127.255",
            "182.34.128.0-182.34.255.255",
            "60.214.96.0-60.214.159.255",
            "112.239.0.0-112.239.127.255",
            "112.248.0.0-112.248.255.255",
            "112.253.64.0-112.253.95.255",
            "58.194.192.0-58.194.215.255",
            "60.212.0.0-60.212.127.255",
            "60.215.160.0-60.215.223.255",
            "60.217.0.0-60.217.0.255",
            "60.217.2.0-60.217.3.255",
            "112.237.0.0-112.238.255.255",
            "112.249.0.0-112.249.255.255",
            "113.121.0.0-113.121.63.255"
        ],
        "districtJudgmentMap": {
            "idAddr": "A",
            "residential": "B",
            "workplace": "C",
            "idNum": "G",
            "mobile": "E",
            "multiple": "1",
            "ip": "G"
        },
        "preCreditContractSignatures": {
            "01": [
                    {
                    "attachmentType": "34011",
                    "filetype": "lhregion",
                    "needPushSignature": False,
                    "postYEscalation": 842,
                    "postXEscalation": 0
                     }]},
        "contractSignatures": {
            "01": [],
            "02": [
                {
                    "attachmentType": "34012",
                    "dealType": "",  # 这里是空，不需要
                    "filetype": "danbaoconsult",
                    "needPushSignature": False,
                    "postYEscalation": 842,
                    "postXEscalation": 0  # 这里需要测试，看签章的位置再调整
                    },
                {
                    "attachmentType": "34005",
                    "dealType": "rd",
                    "filetype": "danbaocount",
                    "needPushSignature": True,
                    "postYEscalation": 842,
                    "postXEscalation": 0
                },
                {
                    "attachmentType": "34006",
                    "dealType": "fk",
                    "filetype": "loancount",
                    "needPushSignature": False,
                    "postYEscalation": 842,
                    "postXEscalation": 595
                }
            ]
        },
        "includeFeesMap": {
            "guarantee": "Q001",
            "technical_service": "Q002"
        },
        "dbzxfwContractType": "34013",
        "defaultMaxRate": "36.00"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanhai_zhongshi_qj_const", body)