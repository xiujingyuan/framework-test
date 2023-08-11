
import common.global_const as gc


# def update_gbiz_capital_zhongbang_zhongji_old():
#     body = {
#               "manual_reverse_allowed": False,
#               "cancelable_task_list": [
#                 "ApplyCanLoan",
#                 "LoanPreApply",
#                 "LoanApplyNew",
#                 "ChangeCapital"
#               ],
#               "raise_limit_allowed": False,
#               "register_config": {
#                 "account_register_duration": 20,
#                 "is_strict_seq": False,
#                 "register_step_list": [
#                   {
#                     "channel": "zhongbang_zhongji",
#                     "step_type": "PAYSVR_PROTOCOL",
#                     "is_strict_seq": True,
#                     "way": "tq",
#                     "sub_way": "baofoo_tq_protocol",
#                     "interaction_type": "SMS",
#                     "group": "kuainiu",
#                     "allow_retry": True,
#                     "allow_fail": False,
#                     "register_status_effect_duration": 1,
#                     "need_confirm_result": True,
#                     "is_multi_account_card_allowed": True,
#                     "status_scene": {
#                           "register": {
#                               "success_type": "once",
#                               "allow_fail": False,
#                               "need_confirm_result": True
#                           },
#                           "route": {
#                               "success_type": "once",
#                               "allow_fail": False
#                           },
#                           "validate": {
#                               "success_type": "once"
#                           }
#                       },
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
#                 ],
#                 "ref_accounts": [
#
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
#                           "messages": [
#
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
#                           "code": "1",
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
#                           "code": ""
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "AssetImport": {
#                   "execute": {
#                     "loan_validator": [
#                       {
#                         "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.70') && #loan.totalAmount<=cmdb.irr(#loan,'24.2')",
#                         "err_msg": "众邦中际[资产还款总额]不满足 irr24，请关注！"
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
#                           "code": "0"
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "LoanApplyNew": {
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "10000",
#                           "messages": [
#                             "2-mock 失败"
#                           ]
#                         }
#                       ]
#                     },
#                       {
#                           "action": {
#                               "policy": "success"
#                           },
#                           "matches": [
#                               {
#                                   "code": "10000",
#                                   "messages": [
#                                       "0-SUCCESS",
#                                       "2-授信申请流水号重复！-授信申请流水号重复！"
#                                   ]
#                               }
#                           ]
#                       },
#                       {
#                           "action": {
#                               "policy": "retry"
#                           },
#                           "matches": [
#                               {
#                                   "code": "1000",
#                                   "messages": [
#                                       ""
#                                   ]
#                               }
#                           ]
#                       }]
#                 },
#                 "LoanApplyQuery": {
#                   "init": {
#                     "delay_time": "delaySeconds(2)"
#                   },
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "10000",
#                           "messages": [
#                             "2-CM9196 同步核心客户信息失败，错误信息\\[888666 开立客户时证件到期日必须大于系统日期\\]-SUCCESS",
#                             "2-mock授信查询失败",
#                             "\\[众邦中际\\]资产\\[.*\\],授信金额\\[.*\\]小于资产本金\\[.*\\]-SUCCESS",
#                             "\\[众邦中际\\]资产\\[.*\\],资产本金\\[.*\\]授信可用余额不足\\[.*\\]-SUCCESS",
#                             "\\[众邦中际\\]资产\\[.*\\],授信额度已过期，授信时间\\[.*\\], 当前时间\\[.*\\]-SUCCESS"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                           {
#                               "code": "10000",
#                               "messages": [
#                                   "1-SUCCESS"
#                               ]
#                           }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "retry"
#                       },
#                       "matches": [
#                         {
#                           "code": "10000",
#                           "messages": [
#                             "0-SUCCESS"
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
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "2000000",
#                           "messages": [
#                             ""
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "20000",
#                           "messages": [
#                             "000000-交易成功-SUCCESS"
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
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "30000",
#                           "messages": [
#                             "2-mock 用信失败"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "30000",
#                           "messages": [
#                             "0-SUCCESS"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "LoanConfirmQuery": {
#                   "init": {
#                     "delay_time": "delaySeconds(10)"
#                   },
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "fail"
#                       },
#                       "matches": [
#                         {
#                           "code": "30000",
#                           "messages": [
#                             "2-内层失败mock的-mock 放款失败"
#                           ]
#                         }
#                       ]
#                     },
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "30000",
#                           "messages": [
#                             "1-SUCCESS"
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
#                           "code": "30000",
#                           "messages": [
#                             "0-SUCCESS"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "CapitalRepayPlanQuery": {
#                   "execute": {
#                     "diff_effect_at": False,
#                     "diff_due_at": False,
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
#                     "delay_time": "delaySeconds(10)"
#                   }
#                 },
#                 "AssetAutoImport": {
#                       "init": {
#                           "delay_time": "delayMinutes(90)"
#                       }
#                   },
#                 "CertificateDownload": {
#                   "init": {
#                     "simple_lock": {
#                       "key": "certificatedownload-zbzj",
#                       "ttlSeconds": 5
#                     }
#                   }
#                 }
#               }
#             }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongbang_zhongji", body)

def update_gbiz_capital_zhongbang_zhongji():
  body = {
          "manual_reverse_allowed": True,
          "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanPreApply",
            "LoanApplyNew",
            "ChangeCapital"
          ],
          "raise_limit_allowed": False,
          "register_config": {
            "account_register_duration": 20,
            "is_strict_seq": False,
            "register_step_list": [
              {
                "channel": "zhongbang_zhongji",
                "step_type": "PAYSVR_PROTOCOL",
                "is_strict_seq": True,
                "way": "tq",
                "sub_way": "baofoo_tq_protocol",
                "interaction_type": "SMS",
                "group": "kuainiu",
                "allow_retry": True,
                "allow_fail": False,
                "register_status_effect_duration": 1,
                "need_confirm_result": True,
                "is_multi_account_card_allowed": True,
                "status_scene": {
                  "register": {
                    "success_type": "once",
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
                    "allow_fail": False,
                    "type": "GetSmsVerifyCode"
                  },
                  {
                    "allow_fail": False,
                    "type": "CheckSmsVerifyCode"
                  }
                ]
              }
            ],
            "ref_accounts": []
          },
          "workflow": {
            "title": "众邦中际放款流程编排v3",
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
                        "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.70') && #loan.totalAmount<=cmdb.irr(#loan,'24.2')",
                        "err_msg": "众邦中际[资产还款总额]不满足 irr24，请关注！"
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
                          "code": "0"
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
                          "code": "10000",
                          "messages": [
                            "0-SUCCESS",
                            "2-授信申请流水号重复！-授信申请流水号重复！"
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
                            "2-mock 失败"
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
                          "code": "1000",
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
                "id": "LoanApplyQuery",
                "type": "LoanApplyQueryTaskHandler",
                "events": [
                  "LoanApplyAsyncSucceededEvent",
                  "LoanApplyAsyncFailedEvent"
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
                          "code": "10000",
                          "messages": [
                            "1-SUCCESS"
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
                            "2-CM9196 同步核心客户信息失败，错误信息\\[888666 开立客户时证件到期日必须大于系统日期\\]-SUCCESS",
                            "2-mock授信查询失败",
                            "\\[众邦中际\\]资产\\[.*\\],授信金额\\[.*\\]小于资产本金\\[.*\\]-SUCCESS",
                            "\\[众邦中际\\]资产\\[.*\\],资产本金\\[.*\\]授信可用余额不足\\[.*\\]-SUCCESS",
                            "\\[众邦中际\\]资产\\[.*\\],授信额度已过期，授信时间\\[.*\\], 当前时间\\[.*\\]-SUCCESS"
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
                          "code": "10000",
                          "messages": [
                            "0-SUCCESS"
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
                          "code": "20000",
                          "messages": [
                            "000000-交易成功-SUCCESS"
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
                          "code": "2000000",
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
                          "code": "30000",
                          "messages": [
                            "0-SUCCESS"
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
                          "code": "30000",
                          "messages": [
                            "2-mock 用信失败"
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
                    "delayTime": "delayMinutes(10)"
                  },
                  "execute": {},
                  "finish": [
                    {
                      "action": {
                        "policy": "success"
                      },
                      "matches": [
                        {
                          "code": "30000",
                          "messages": [
                            "1-SUCCESS"
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
                          "code": "30000",
                          "messages": [
                            "2-内层失败mock的-mock 放款失败"
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
                          "code": "30000",
                          "messages": [
                            "0-SUCCESS"
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
                    "delayTime": "delayMinutes(60)"
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
                "id": "ContractDown",
                "type": "ContractDownTaskHandler",
                "events": [],
                "activity": {
                  "execute": {},
                  "init": {
                    "delayTime": "delaySeconds(10)"
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
                "id": "CertificateApply",
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
                "id": "CertificateDownload",
                "type": "CertificateDownloadTaskHandler",
                "events": [],
                "activity": {
                  "execute": {},
                  "init": {
                    "simpleLock": {
                      "key": "certificatedownload-zbzj",
                      "ttlSeconds": 5
                    }
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
                "memo": "支用前共享协议成功",
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
                "memo": "支用前共享协议失败",
                "listen": {
                  "event": "LoanPostApplyFailedEvent"
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
                  "ChangeCapital"
                ],
                "associateData": {
                  "skipDoubleCheck": False,
                  "event": "GrantFailedEvent",
                  "sourceWorkflowNodeId": "LoanConfirmQuery"
                }
              },
              {
                "memo": "结清证明申请成功",
                "listen": {
                  "event": "CertificateApplyReadyEvent"
                },
                "nodes": [
                  "CertificateDownload"
                ]
              }
            ]
          }
        }
  return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongbang_zhongji", body)
def update_gbiz_capital_zhongbang_zhongji_const():
    body = {
              "partnerCode": "10106ZYDKNZN",
              "imageMaxAllowSize": 1572864,
              "imageMinAllowSize": 3072,
              "userType": "0310",
              "idType": "Ind01",
              "nationality": "CHN",
              "nationMap": {
                "汉": "01"
              },
              "nationOther": "02",
              "sexMap": {
                "m": "1",
                "f": "2"
              },
              "familyStatus": "7",
              "marriageMap": {
                "1": "10",
                "2": "21",
                "3": "30",
                "4": "40"
              },
              "defaultMarriage": "10",
              "educationMap": {
                "1": "10",
                "2": "10",
                "3": "20",
                "4": "30",
                "5": "40",
                "6": "50",
                "7": "60",
                "8": "70",
                "9": "80",
                "10": "90"
              },
              "defaultEducation": "20",
              "occupationMap": {
                "1": "1",
                "2": "X",
                "3": "4",
                "4": "4",
                "5": "4",
                "6": "6",
                "7": "6",
                "8": "1",
                "9": "4",
                "10": "4",
                "11": "4",
                "12": "4",
                "13": "4",
                "14": "1",
                "15": "5"
              },
              "defaultOccupation": 4,
              "headShipMap": {
                "0": "4",
                "1": "1",
                "2": "1",
                "3": "3",
                "4": "3",
                "5": "3",
                "6": "3",
                "7": "3",
                "8": "3",
                "9": "3",
                "10": "3",
                "11": "3",
                "12": "3",
                "13": "3",
                "14": "3",
                "15": "3"
              },
              "defaultHeadShip": 4,
              "defaultPosition": 0,
              "industryMap": {
                "1": "S",
                "2": "S",
                "3": "P",
                "4": "Q",
                "5": "S",
                "6": "E",
                "7": "C",
                "8": "I",
                "9": "J",
                "10": "O",
                "11": "H",
                "12": "R",
                "13": "O",
                "14": "L",
                "15": "A"
              },
              "defaultIndustry": "O",
              "moduleId": "NCMS01",
              "repayType": "ECI",
              "loanPurposeMap": {
                "1": "08",
                "2": "05",
                "3": "04",
                "4": "03",
                "5": "03",
                "6": "07",
                "7": "07",
                "8": "08"
              },
              "defaultLoanPurpose": "08",
              "eduDegreeMap": {
                "1": "2",
                "2": "3",
                "3": "4",
                "4": "0",
                "5": "0",
                "6": "0",
                "7": "0",
                "8": "0",
                "9": "0",
                "10": "0"
              },
              "defaultEduDegree": "0",
              "relationMap": {
                "0": "99",
                "1": "0302",
                "2": "0302",
                "3": "0304",
                "4": "0301",
                "5": "0310",
                "6": "0311",
                "7": "99",
                "8": "0302",
                "9": "0303"
              },
              "attachmentMap": {
                "101": {
                  "typeId": 1,
                  "eventType": "ZBZJ_FILE_ID_101"
                },
                "102": {
                  "typeId": 2,
                  "eventType": "ZBZJ_FILE_ID_102"
                },
                "103": {
                  "typeId": 29,
                  "eventType": "ZBZJ_FILE_ID_103"
                },
                "106": {
                  "typeId": 29,
                  "eventType": "ZBZJ_FILE_ID_106"
                }
              },
              "contractMap": {
                "11": {
                  "typeId": 28,
                  "fileName": "借款合同.pdf"
                },
                "06": {
                  "typeId": 34300,
                  "fileName": "额度合同.pdf"
                }
              },
              "successCode": "0000",
              "failedCode": "9999",
              "bankNoMap": {
                "ICBC": "102100099996",
                "ABC": "103100000026",
                "BOC": "104100000004",
                "COMM": "301290000007",
                "CITIC": "302100011000",
                "CEB": "303100000006",
                "HXB": "304100040000",
                "CMBC": "305100000013",
                "GDB": "306581000003",
                "PAB": "307584007998",
                "CMB": "308584000013",
                "CIB": "309391000011",
                "SPDB": "310290000013",
                "BJBANK": "313100000013",
                "SHBANK": "325290000012",
                "PSBC": "403100000004",
                "CCB": "105100000017"
              },
              "requestNoPrefix":{
                   "memo":"以下配置不建议变更，会影响后续流程数据",
                   "loanApplyPrefix": "A",
                   "loanPostPrefix": "B",
                   "loanApplyConfirmPrefix": "C"
                },
                "outRequestNoMap":{},
              "yearRate": "24",
              "flowFlag": "1",
              "threeElementsAuthResult": "Y",
              "newScoreMap": {
                "0": "D",
                "350": "D",
                "351": "C",
                "613": "C",
                "614": "B",
                "637": "B",
                "638": "A",
                "950": "A"
              },
              "oldScoreMap": {
                "0": "D",
                "350": "D",
                "351": "C",
                "590": "C",
                "591": "B",
                "621": "B",
                "622": "A",
                "950": "A"
              },
              "loanDate": "20230216",
              "doctype": "03",
              "certificateFilePrefix": "settle_",
              "certificateFileSuffix": ".pdf",
              "ipSegPool": [
                "110000#110.96.0.0-110.127.255.255",
                "130100#27.128.0.0-27.128.79.255",
                "130200#27.190.0.0-27.191.255.255",
                "130300#106.8.0.0-106.8.63.255",
                "130400#27.188.0.0-27.188.255.255",
                "130500#27.129.192.0-27.129.255.255",
                "130600#27.128.192.0-27.128.207.255",
                "130700#27.129.52.0-27.129.55.255",
                "130800#27.129.60.0-27.129.63.255",
                "130900#106.8.192.0-106.8.255.255",
                "131000#27.128.208.0-27.128.223.255",
                "131100#27.128.115.0-27.128.119.255"
              ]
      }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongbang_zhongji_const", body)
