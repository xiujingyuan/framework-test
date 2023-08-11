import common.global_const as gc

# def update_gbiz_capital_xiaomi_zhongji_old():
#     body = {
#           "cancelable_task_list": [
#             "ApplyCanLoan",
#             "LoanPreApply",
#             "LoanApplyNew",
#             "ChangeCapital"
#           ],
#           "manual_reverse_allowed": False,
#           "raise_limit_allowed": False,
#           "register_config": {
#             "account_register_duration": 20,
#             "is_multi_account_card_allowed": True,
#             "is_strict_seq": True,
#             "post_register": False,
#             "ref_accounts": None,
#             "register_step_list": [
#               {
#                 "channel": "xiaomi_zhongji",
#                 "step_type": "PAYSVR_PROTOCOL",
#                 "way": "tq",
#                 "sub_way": "baofoo_tq_protocol",
#                 "interaction_type": "SMS",
#                 "group": "kuainiu",
#                 "allow_fail": False,
#                 "need_confirm_result": True,
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
#                       "messages": []
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
#                     "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.90') && #loan.totalAmount<=cmdb.irr(#loan,'24.6')",
#                     "err_msg": "小米中际[资产还款总额]不满足 irr24，请关注！"
#                   }
#                 ]
#               }
#             },
#             "LoanPreApply": {
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "100000",
#                       "messages": [
#                         "存在可用授信额度,不需要再次授信!",
#                         "授信文件上传成功"
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
#                       "code": "9999",
#                       "messages": [
#                         "额度不可用,切资方!"
#                       ]
#                     },
#                     {
#                           "code": "100000",
#                           "messages": [
#                               "241081_mock额度查询失败"
#                           ]
#                       }
#                   ]
#                 }
#               ]
#             },
#             "LoanApplyNew": {
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "100000",
#                       "messages": [
#                         "存在可用授信额度,不需要再次授信!",
#                         "000000_成功_S",
#                         "000000_成功_W"
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
#                       "code": "100000",
#                       "messages": [
#                         "000000_mock授信申请失败_F"
#                       ]
#                     }
#                   ]
#                 }
#               ]
#             },
#             "LoanApplyQuery": {
#               "init": {
#                 "delayTime": "delaySeconds(60)"
#               },
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "100000",
#                       "messages": [
#                         "存在可用授信额度,不需要再次授信!",
#                         "000000_成功_S_null_null"
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
#                       "code": "100000",
#                       "messages": [
#                         "000000_mock授信查询失败_F_null_null",
#                         "000000_S_mock授信额度不足_null_null"
#                       ]
#                     },
#                     {
#                         "code": "9999",
#                         "messages": [
#                             "资方授信金额\\[.*\\]小于我方进件金额\\[.*\\]"
#                     ]
#                     }
#                   ]
#                 },
#                 {
#                   "action": {
#                     "policy": "retry"
#                   },
#                   "matches": [
#                         {
#                             "code": "100000",
#                             "messages": [
#                                 "000000_成功_W_null_null"
#                             ]
#                         }
#                   ]
#                 }
#               ]
#             },
#             "LoanPostApply": {
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "0",
#                       "messages": [
#                         "协议签约查询成功",
#                         "未查询到需要签约的合同"
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
#                       "code": "9999",
#                       "messages": [
#                         "遇到再配置"
#                       ]
#                     }
#                   ]
#                 },
#                   {
#                       "action": {
#                           "policy": "retry"
#                       },
#                       "matches": [
#                           {
#                               "code": "9999",
#                               "messages": [
#                                   "遇到配置"
#                               ]
#                           }
#                       ]
#                   }
#               ]
#             },
#             "LoanPostCredit": {
#               "init": {
#                 "delayTime": "delayMinutes(5)"
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
#                         "支用合同上传成功"
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
#                       "code": "9999",
#                       "messages": [
#                         "遇到再配置"
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
#                       "code": "200000",
#                       "messages": [
#                         "000000_成功_S",
#                         "000000_成功_W"
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
#                       "code": "200000",
#                       "messages": [
#                         "000000_放款申请失败_F"
#                       ]
#                     }
#                   ]
#                 }
#               ]
#             },
#             "LoanConfirmQuery": {
#               "init": {
#                 "delayTime": "delaySeconds(120)"
#               },
#               "finish": [
#                 {
#                   "action": {
#                     "policy": "success"
#                   },
#                   "matches": [
#                     {
#                       "code": "200000",
#                       "messages": [
#                         "000000_成功_S_null"
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
#                       "code": "200000",
#                       "messages": [
#                         "000000_mock放款查询失败_F_null",
#                         "000001_mock放款查询外层失败_S_null"
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
#                       "code": "200000",
#                       "messages": [
#                         "000000_成功_W_null"
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
#                 "delayTime": "delayMinutes(30)"
#               }
#             },
#             "AssetAutoImport": {
#               "init": {
#                 "delayTime": "delayMinutes(90)"
#               }
#             }
#           }
#         }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_xiaomi_zhongji", body)

def update_gbiz_capital_xiaomi_zhongji():
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
              "channel": "xiaomi_zhongji",
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
          "title": "小米中际资金方流程编排v3",
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
              "activity": {
                "init": {},
                "execute": {
                  "loan_validator": [
                    {
                      "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.90') && #loan.totalAmount<=cmdb.irr(#loan,'24.6')",
                      "err_msg": "小米中际[资产还款总额]不满足 irr24，请关注！"
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
              "id": "LoanPreApply",
              "type": "LoanPreApplyTaskHandler",
              "activity": {
                "init": {},
                "finish": [
                  {
                    "action": {
                      "policy": "success"
                    },
                    "matches": [
                      {
                        "code": "100000",
                        "messages": [
                          "存在可用授信额度,不需要再次授信!",
                          "授信文件上传成功"
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
                          "额度不可用,切资方!"
                        ]
                      },
                      {
                        "code": "100000",
                        "messages": [
                          "241081_mock额度查询失败"
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
              "activity": {
                "init": {},
                "finish": [
                  {
                    "action": {
                      "policy": "success"
                    },
                    "matches": [
                      {
                        "code": "100000",
                        "messages": [
                          "存在可用授信额度,不需要再次授信!",
                          "000000_成功_S",
                          "000000_成功_W"
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
                        "code": "100000",
                        "messages": [
                          "240054_活体检测机构超长_",
                          "000000_mock授信申请失败_F"
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
                "LoanApplyAsyncSucceededEvent"
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
                        "code": "100000",
                        "messages": [
                          "存在可用授信额度,不需要再次授信!",
                          "000000_成功_S_null_null"
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
                        "code": "100000",
                        "messages": [
                          "000000_mock授信查询失败_F_null_null",
                          "000000_S_mock授信额度不足_null_null"
                        ]
                      },
                      {
                        "code": "9999",
                        "messages": [
                          "资方授信金额\\[.*\\]小于我方进件金额\\[.*\\]"
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
                        "code": "100000",
                        "messages": [
                          "000000_成功_W_null_null"
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
                          "协议签约查询成功",
                          "未查询到需要签约的合同"
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
              "id": "LoanPostCredit",
              "type": "LoanPostCreditTaskHandler",
              "activity": {
                "init": {
                  "delayTime": "delayMinutes(5)"
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
                          "支用合同上传成功"
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
                  }
                ]
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
                        "code": "200000",
                        "messages": [
                          "000000_成功_S",
                          "000000_成功_W"
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
                        "code": "200000",
                        "messages": [
                          "000000_放款申请失败_F"
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
                        "code": "200000",
                        "messages": [
                          "000000_成功_S_null"
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
                        "code": "200000",
                        "messages": [
                          "000000_mock放款查询失败_F_null",
                          "000001_mock放款查询外层失败_S_null"
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
                        "code": "200000",
                        "messages": [
                          "000000_成功_W_null"
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
              "id": "ContractPush",
              "type": "ContractPushTaskHandler",
              "events": [],
              "activity": {
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
                  "delayTime": "delayMinutes(30)"
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
              "id": "CertificateApplyVerify",
              "type": "CertificateApplyVerifySyncTaskHandler",
              "events":[
                  "CertificateApplyReadyEvent"
                ],
              "activity":{
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
                              "code": "300000",
                              "messages": [
                                  "000000_成功_0",
                                  "000000_成功_1"
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
              "activity":{
                  "execute": {
                      "interval_in_minutes": "240"
                    },
                  "init": {
                      "delayTime": "delayDays(1, \"09:00:00\")"
                    }
                }
            },
            {
              "id": "ChangeCapital",
              "type": "ChangeCapitalTaskHandler",
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
                          "遇到在配置"
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
                        "code": "100998"
                      }
                    ]
                  }
                ]
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
                "event": "AssetImportSucceededEvent",
                "matches": []
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
                "event": "AssetReadyEvent",
                "matches": []
              },
              "nodes": [
                "LoanPreApply"
              ]
            },
            {
              "memo": "授信前影像资料上传成功",
              "listen": {
                "event": "LoanPreApplySyncSucceededEvent",
                "matches": []
              },
              "nodes": [
                "LoanApplyNew"
              ]
            },
            {
              "memo": "授信申请成功",
              "listen": {
                "event": "LoanApplySyncSucceededEvent",
                "matches": []
              },
              "nodes": [
                "LoanApplyQuery"
              ]
            },
            {
              "memo": "授信查询成功",
              "listen": {
                "event": "LoanApplyAsyncSucceededEvent",
                "matches": []
              },
              "nodes": [
                "LoanPostApply"
              ]
            },
            {
              "memo": "支用前协议签约查询",
              "listen": {
                "event": "LoanPostApplySucceededEvent",
                "matches": []
              },
              "nodes": [
                "LoanPostCredit"
              ]
            },
            {
              "memo": "支用前合同上传成功",
              "listen": {
                "event": "LoanPostCreditSucceededEvent",
                "matches": []
              },
              "nodes": [
                "LoanApplyConfirm"
              ]
            },
            {
              "memo": "支用申请成功",
              "listen": {
                "event": "ConfirmApplySyncSucceededEvent",
                "matches": []
              },
              "nodes": [
                "LoanConfirmQuery"
              ]
            },
            {
              "memo": "支用查询成功",
              "listen": {
                "event": "GrantSucceededEvent",
                "matches": []
              },
              "nodes": [
                "CapitalRepayPlanQuery",
                "ContractDown",
                "ContractPush"
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
              "memo": "授信前影像资料上传失败",
              "listen": {
                "event": "LoanPreApplySyncFailedEvent",
                "matches": []
              },
              "nodes": [
                "ChangeCapital"
              ],
              "associateData": {
                "skipDoubleCheck": True,
                "event": "LoanPreApplySyncFailedEvent"
              }
            },
            {
              "memo": "支用前协议签约查询失败",
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
              "memo": "支用前合同上传失败",
              "listen": {
                "event": "LoanPostCreditFailedEvent",
                "matches": []
              },
              "nodes": [
                "ChangeCapital"
              ],
              "associateData": {
                "skipDoubleCheck": True,
                "event": "LoanPostCreditFailedEvent"
              }
            },
            {
              "memo": "资方放款失败",
              "listen": {
                "event": "GrantFailedEvent",
                "matches": []
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
                "skipDoubleCheck": False,
                "event": "LoanApplySyncFailedEvent",
                "sourceWorkflowNodeId": "LoanApplyQuery"
              }
            },
            {
              "memo": "异步进件申请失败",
              "listen": {
                "event": "LoanApplyAsyncFailedEvent",
                "matches": []
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
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_xiaomi_zhongji", body)

def update_gbiz_capital_xiaomi_zhongji_const():
    body = {
            "ftpName": "xiaomi_zhongji",
            "productNo": "XMKND",
            "uploadAttachmentMap":
            {
                "1": "01",
                "2": "02",
                "29": "03"
            },
            "creditUploadContractMap":
            {
                  "35500": "000044442222_06",
                  "35501": "000044442222_07",
                  "35502": "000044442222_05",
                  "35509": "313882000012_16"

            },
            "genderMap":
            {
                "f": "F",
                "m": "M"
            },
            "corpTypeMap":
            {
                "1": "M",
                "2": "M",
                "3": "M",
                "4": "I",
                "5": "K",
                "6": "L",
                "7": "C",
                "8": "J",
                "9": "G",
                "10": "H",
                "11": "F",
                "12": "M",
                "13": "B",
                "14": "A",
                "15": "D"
            },
            "occupationMap":
            {},
            "defaultOccupation": "C04",
            "raceMap":
            {
                "汉": "1",
                "蒙古": "2",
                "回": "3",
                "藏": "4",
                "维吾尔": "5",
                "苗": "6",
                "彝": "7",
                "壮": "8",
                "布依": "9",
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
                "毛难": "36",
                "仡佬": "37",
                "锡伯": "38",
                "阿昌": "39",
                "普米": "40",
                "塔吉克": "41",
                "怒": "42",
                "乌孜别克": "43",
                "俄罗斯": "44",
                "鄂温克": "45",
                "崩龙": "46",
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
                "外国血统": "98",
                "其他": "99"
            },
            "maritalStatusMap":
            {
                "0": "H",
                "1": "A",
                "2": "C",
                "3": "G",
                "4": "B"
            },
            "educationMap":
            {
                "1": "6",
                "2": "6",
                "3": "5",
                "4": "5",
                "5": "5",
                "6": "4",
                "7": "3",
                "8": "2",
                "9": "1"
            },
            "relationMap":
            {
                "0": "1",
                "1": "2",
                "2": "3",
                "3": "4",
                "4": "21",
                "5": "22",
                "6": "23",
                "7": "99"
            },
            "loanUseMap":
            {
                "1": "A",
                "2": "C",
                "3": "T",
                "4": "B",
                "5": "B",
                "6": "S",
                "7": "S",
                "8": "N",
                "9": "F"
            },
            "capitalProtocolNoMap":
                {},
            "loanSuccessContractPushMap":
                {
                    "35503": "10"
                },
            "downloadContractMap":
                {
                  "28": "10",
                  "35504": "000044442222_06"
                },
            "limitLoopDownloadContractMap":
                {
                    "28": "10"
                },
            "address": "C",
            "certificateDownPathMap":
            {
                "A20230718113239162942": "20230720"
               },  # 下载结清证明按照申请结清证明的时间来下载，若下载不到用这个配置修改
            "cityIps":
            [
              "北京市#110.96.0.0-110.127.255.255",
              "北京市#112.124.0.0-112.127.255.255",
              "北京市#115.120.0.0-115.123.255.255",
              "北京市#101.144.0.0-101.159.255.255",
              "北京市#211.160.0.0-211.163.255.255",
              "内蒙古自治区#1.24.0.0-1.31.255.255",
              "内蒙古自治区#121.193.0.0-121.193.255.255",
              "内蒙古自治区#221.199.192.0-221.199.207.255",
              "内蒙古自治区#221.199.128.0-221.199.191.255",
              "内蒙古自治区#116.95.0.0-116.95.255.255"
            ]
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_xiaomi_zhongji_const", body)