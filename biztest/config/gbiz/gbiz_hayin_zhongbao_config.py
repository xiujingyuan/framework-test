import common.global_const as gc

# def update_gbiz_capital_hayin_zhongbao_old():
#     body = {
#               "cancelable_task_list": [
#                 "ApplyCanLoan",
#                 "LoanApplyNew",
#                 "ChangeCapital"
#               ],
#               "manual_reverse_allowed": False,
#               "raise_limit_allowed": False,
#               "register_config": {
#                 "ref_accounts": None,
#                 "register_step_list": [
#                   {
#                     "channel": "hayin_zhongbao",
#                     "step_type": "PROTOCOL",
#                     "way": "hayin_zhongbao",
#                     "interaction_type": "SMS",
#                     "status_scene": {
#                       "register": {
#                         "success_type": "once",
#                         "register_status_effect_duration_day": 1,
#                         "allow_fail": False,
#                         "need_confirm_result": False
#                       },
#                       "route": {
#                         "success_type": "once",
#                         "allow_fail": False
#                       },
#                       "validate": {
#                         "success_type": "once"
#                       }
#                     },
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
#                         "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
#                         "err_msg": "哈银中保[资产还款总额]不满足 irr24，请关注！"
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
#                             "授信环节影像文件资料上传成功"
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
#                           "code": "1",
#                           "messages": [
#                             "0_成功"
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
#                             "F1000_mock授信申请拒绝"
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
#                           "code": "1",
#                           "messages": [
#                             "0_成功_10000_null_null_授信金额与申请金额不同",
#                             "0_成功_10000_null_null"
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
#                             "0_mock授信查询失败_90000_null_null",
#                             "0_mock授信查询失败_10000_null_null_当前日期不在授信有效期内"
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
#                           "code": "1",
#                           "messages": [
#                             "0_成功_20000_null_null"
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
#                             "用信环节影像文件资料上传成功"
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
#                 "LoanApplyConfirm": {
#                   "init": {
#                     "simple_lock": {
#                       "key": "LoanApplyConfirm-hayin",
#                       "ttlSeconds": 600  # 600秒，10分钟，意味着10分钟内只能有一个资产执行这个任务成功
#                     }
#                   },
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "2",
#                           "messages": [
#                             "0_成功"
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
#                           "code": "2",
#                           "messages": [
#                             "F1099_mock用信申请失败"
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
#                           "code": "2",
#                           "messages": [
#                             "0_成功_10000_null_null_200"
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
#                           "code": "2",
#                           "messages": [
#                             "0_成功_10000_null_null_900",
#                             "0_成功_90000_null_null_400"
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
#                           "code": "2",
#                           "messages": [
#                             "0_成功_10000_null_null_100",
#                             "0_成功_10000_null_null_450"
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
#                     "delay_time": "delayDays(1, \"09:30:00\")",
#                     "simple_lock": {
#                       "key": "contractdown-hayin",
#                       "ttlSeconds": 10
#                     }
#                   }
#                 },
#                 "AssetAutoImport": {
#                   "init": {
#                     "delay_time": "delayMinutes(90)"
#                   }
#                 },
#                 "CertificateApply": {
#                   "finish": [
#                     {
#                       "action": {
#                         "policy": "success"
#                       },
#                       "matches": [
#                         {
#                           "code": "0",
#                           "messages": [
#                             "0_成功_PROC_null_null",
#                             "0_成功_SUCC_null_null"
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
#                           "code": "0",
#                           "messages": [
#                             "遇到在配置"
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
#                           "code": "0",
#                           "messages": [
#                             "遇到在配置"
#                           ]
#                         }
#                       ]
#                     }
#                   ]
#                 },
#                 "CertificateDownload": {
#                   "execute": {
#                     "interval_in_minutes": "240"
#                   }
#                 }
#               }
#             }
#
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hayin_zhongbao", body)


def update_gbiz_capital_hayin_zhongbao():
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
                "channel": "hayin_zhongbao",
                "step_type": "PROTOCOL",
                "way": "hayin_zhongbao",
                "interaction_type": "SMS",
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
            "title": "哈银中保流程编排v3",
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
                        "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                        "err_msg": "哈银中保[资产还款总额]不满足 irr24，请关注！"
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
                        "policy": "success"
                      },
                      "matches": [
                        {
                          "code": "0",
                          "messages": [
                            "授信环节影像文件资料上传成功"
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
                        "policy": "success"
                      },
                      "matches": [
                        {
                          "code": "1",
                          "messages": [
                            "0_成功"
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
                            "F1000_mock授信申请拒绝"
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
                          "code": "1",
                          "messages": [
                            "0_成功_10000_null_null_授信金额与申请金额不同",
                            "0_成功_10000_null_null"
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
                            "0_mock授信查询失败_90000_null_null",
                            "0_mock授信查询失败_10000_null_null_当前日期不在授信有效期内"
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
                            "0_成功_20000_null_null"
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
                            "用信环节影像文件资料上传成功"
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
                    "cancelable": False,
                    "simpleLock": {
                      "ttlSeconds": 600,
                      "key": "LoanApplyConfirm-hayin"
                    },
                    "delayTime": None
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
                            "0_成功"
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
                            "F1099_mock用信申请失败"
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
                          "code": "2",
                          "messages": [
                            "0_成功_10000_null_null_200"
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
                            "0_成功_10000_null_null_900",
                            "0_成功_90000_null_null_400"
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
                            "0_成功_10000_null_null_100",
                            "0_成功_10000_null_null_450"
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
                "events": [
                  "ContractDownSucceededEvent"
                ],
                "activity": {
                  "init": {
                    "executeType": "auto",
                    "cancelable": False,
                    "simpleLock": {
                      "ttlSeconds": 10,
                      "key": "contractdown-hayin"
                    },
                    "delayTime": "delayDays(1, \"09:30:00\")"
                  },
                  "execute": {
                    "interval_in_minutes": "240"
                  },
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
                    "cancelable": False
                  },
                  "execute": {},
                  "finish": []
                }
              },
              {
                "id": "GuaranteeUpload",
                "type": "GuaranteeUploadTaskHandler",
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
                "id": "GuaranteeApply",
                "type": "GuaranteeApplyTaskHandler",
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
                "id": "CertificateApplyVerify",
                "type": "CertificateApplyVerifySyncTaskHandler",
                "events": [
                  "CertificateApplyReadyEvent"
                ],
                "activity": {
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
                            "0_成功_PROC_null_null",
                            "0_成功_SUCC_null_null"
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
                          "code": "0",
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
                  },
                  "init": {}
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
                "memo": "资产导入就绪事件订阅",
                "listen": {
                  "event": "AssetImportReadyEvent"
                },
                "nodes": [
                  "AssetImport"
                ]
              },
              {
                "memo": "资产导入成功事件订阅",
                "listen": {
                  "event": "AssetImportSucceededEvent"
                },
                "nodes": [
                  "AssetImportVerify"
                ]
              },
              {
                "memo": "资产进件核心参数校验成功事件订阅",
                "listen": {
                  "event": "AssetImportVerifySucceededEvent"
                },
                "nodes": [
                  "ApplyCanLoan"
                ]
              },
              {
                "memo": "资产就绪失败事件订阅",
                "listen": {
                  "event": "AssetReadyEvent"
                },
                "nodes": [
                  "LoanPreApply"
                ]
              },
              {
                "memo": "资产进件前任务失败事件订阅",
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
                "memo": "资产进件前任务成功事件订阅",
                "listen": {
                  "event": "LoanPreApplySyncSucceededEvent"
                },
                "nodes": [
                  "LoanApplyNew"
                ]
              },
              {
                "memo": "资产进件失败事件订阅",
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
                "memo": "资产进件成功事件订阅",
                "listen": {
                  "event": "LoanApplySyncSucceededEvent"
                },
                "nodes": [
                  "LoanApplyQuery"
                ]
              },
              {
                "memo": "资产进件失败事件订阅",
                "listen": {
                  "event": "LoanApplySyncFailedEvent"
                },
                "nodes": [
                  "ChangeCapital",
                  "BlacklistCollect"
                ],
                "associateData": {
                  "sourceWorkflowNodeId": "LoanApplyQuery",
                  "event": "LoanApplySyncFailedEvent",
                  "skipDoubleCheck": False
                }
              },
              {
                "memo": "资产进件成功事件订阅",
                "listen": {
                  "event": "LoanApplyAsyncSucceededEvent"
                },
                "nodes": [
                  "LoanPostApply"
                ]
              },
              {
                "memo": "资产进件查询失败事件订阅",
                "listen": {
                  "event": "LoanApplyAsyncFailedEvent"
                },
                "nodes": [
                  "ChangeCapital",
                  "BlacklistCollect"
                ],
                "associateData": {
                  "sourceWorkflowNodeId": "LoanApplyQuery",
                  "event": "LoanApplyAsyncFailedEvent",
                  "skipDoubleCheck": False
                }
              },
              {
                "memo": "资产进件后任务成功事件订阅",
                "listen": {
                  "event": "LoanPostApplySucceededEvent"
                },
                "nodes": [
                  "LoanApplyConfirm"
                ],
                "associateData": {
                  "lockRecordStatus": 3
                }
              },
              {
                "memo": "资产进件后任务失败事件订阅",
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
                "memo": "支用申请成功事件订阅",
                "listen": {
                  "event": "ConfirmApplySyncSucceededEvent"
                },
                "nodes": [
                  "LoanConfirmQuery"
                ]
              },
              {
                "memo": "支用申请失败事件订阅",
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
                "memo": "支用查询成功事件订阅",
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
                "memo": "支用查询失败事件订阅",
                "listen": {
                  "event": "GrantFailedEvent"
                },
                "nodes": [
                  "ChangeCapital",
                  "BlacklistCollect"
                ],
                "associateData": {
                  "sourceWorkflowNodeId": "LoanConfirmQuery",
                  "event": "GrantFailedEvent",
                  "skipDoubleCheck": False
                }
              },
              {
                "memo": "还款计划查询成功事件订阅",
                "listen": {
                  "event": "RepayPlanHandleSucceededEvent"
                },
                "nodes": [
                  "OurRepayPlanRefine"
                ]
              },
              {
                "memo": "合同下载成功事件订阅",
                "listen": {
                  "event": "ContractDownSucceededEvent"
                },
                "nodes": [
                  "GuaranteeUpload",
                  "GuaranteeApply"
                ]
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
  return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hayin_zhongbao", body)
def update_gbiz_capital_hayin_zhongbao_const():
    body = {
            "genderMap": {
              "m": "1",
              "f": "2"
            },
            "marriageMap": {
              "1": "1",
              "2": "2",
              "3": "3",
              "4": "4"
            },
            "educationMap": {
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
            "occupationMap": {
              "1": "4",
              "2": "4",
              "3": "4",
              "4": "1",
              "5": "6",
              "6": "1",
              "7": "6",
              "8": "1",
              "9": "1",
              "10": "0",
              "11": "3",
              "12": "3",
              "13": "4",
              "14": "0",
              "15": "5"
            },
            "incomeMap": {
              "0-2000": "2000",
              "2001-3000": "3000",
              "3001-5000": "5000",
              "5001-8000": "8000",
              "8001-12000": "12000",
              "12000-0": "15000"
            },
            "relaMap": {
              "0": "03",
              "1": "01",
              "2": "08",
              "3": "02",
              "4": "06",
              "5": "07",
              "6": "04",
              "7": "05",
              "8": "09"
            },
            "loanPurposeMap": {
              "1": "CMP",
              "2": "EDU",
              "3": "REN",
              "4": "DIG",
              "5": "TRA",
              "6": "MED",
              "7": "MED",
              "8": "APP",
              "9": "OTH"
            },
            "fileTypeMap": {
              "1": "FRONT_ID_CARD",
              "2": "BACK_ID_CARD",
              "29": "FACE"
            },
            "fileSuffixMap": {
              "jpg": "JPG",
              "png": "PNG",
              "jpe": "JPE"
            },
            "loanApplyContractUploadConfig": [
              {
                "contractType": "35301",
                "ftpPathExpr": "/upload/custInfoQU_agreement/#{T(DateUtil).format(#record.createAt, 'yyyyMMdd')}",
                "fileNameExpr": "#{#record.assetItemNo}.pdf"
              },
              {
                "contractType": "35302",
                "ftpPathExpr": "/upload/applyCredit_agreement/#{T(DateUtil).format(#record.createAt, 'yyyyMMdd')}",
                "fileNameExpr": "#{#record.assetItemNo}.pdf"
              },
              {
                "contractType": "35303",
                "ftpPathExpr": "/upload/nostudent_commitment/#{T(DateUtil).format(#record.createAt, 'yyyyMMdd')}",
                "fileNameExpr": "#{#record.assetItemNo}.pdf"
              },
              {
                "contractType": "35304",
                "ftpPathExpr": "/upload/applyLimit_agreement/#{T(DateUtil).format(#record.createAt, 'yyyyMMdd')}",
                "fileNameExpr": "#{#record.assetItemNo}.pdf"
              }
            ],
            "loanConfirmContractUploadConfig": [
              {
                "contractType": "35305",
                "ftpPathExpr": "/upload/entrustDeductions_agreement/#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}",
                "fileNameExpr": "#{#record.assetItemNo}.pdf"
              },
              {
                "contractType": "35306",
                "ftpPathExpr": "/upload/loan_agreement/#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}",
                "fileNameExpr": "#{#record.assetItemNo}.pdf"
              }
            ],
            "contractDownConfig": [
              {
                "contractType": "28",
                "ftpPathExpr": "/download/img/zfpz/#{T(DateUtil).format(#record.finishAt, 'yyyyMMdd')}",
                "fileNameExpr": "#{#record.assetItemNo}.pdf"
              },
              {
                "contractType": "35309",
                "ftpPathExpr": "/download/applyLimit_agreement/#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}",
                "fileNameExpr": "#{#record.assetItemNo}_sign.pdf"
              }
            ],
            "loanSuccessContractUploadConfig": [
              {
                "contractType": "35307",
                "ftpPathExpr": "/upload/guarantee_agreement/#{T(DateUtil).format(#record.finishAt, 'yyyyMMdd')}",
                "fileNameExpr": "#{#record.assetItemNo}.pdf"
              }
            ],
            "bankCodeMap": {
              "ICBC": "中国工商银行",
              "CCB": "中国建设银行",
              "BOC": "中国银行",
              "ABC": "中国农业银行",
              "CMB": "招商银行",
              "SPDB": "上海浦东发展银行",
              "CITIC": "中信银行",
              "HXB": "华夏银行",
              "CMBC": "中国民生银行",
              "CEB": "中国光大银行",
              "CIB": "兴业银行",
              "PAB": "平安银行",
              "SPABANK": "平安银行",
              "CZBANK": "浙商银行",
              "EGBANK": "恒丰银行",
              "BOHAIB": "渤海银行",
              "SHBANK": "上海银行",
              "SHB": "上海银行",
              "BJBANK": "北京银行"
            },
            "ftpChannel": "hayin_zhongbao",
            "guaranteeConfig": {
              "channelDir": "/upload/dfkn/zb",
              "partnerNo": "ZB-KN",
              "productName": "快牛",
              "applyStatus": "S",
              "cfundChannelNo": "ZB-KN-HYXJ",
              "cfundChannelName": "中保-快牛-哈银消金",
              "payWay": "02",
              "repayWay": "01",
              "yearRate": "0.24",
              "actYearRate": "0.082",
              "ointRate": "0",
              "validPass": "Y",
              "lendStatus": "S",
              "idCardType": "01",
              "dateFormat": "yyyyMMdd",
              "normalLoanStatus": "NOR",
              "productNo": "HYZB",
              "annualIncome": "B20205",
              "industry": "B1003",
              "relation": "90",
              "loanUse": "07",
              "guaranteeFeeTypes": ["technical_service"],
              "periodGuaranteeRate": 0.158,
              "periodServiceRate": "",
              "contractUploadConfig": {
                "fileName": "contract",
                "remoteDir": "/contract",
                "subFilesConfigMap": {
                  "28": {
                    "name": "loan",
                    "extension": "pdf"
                  },
                  "35305": {
                    "name":"draw",
                    "extension":"pdf"
                 },
                "35307":{
                    "name":"commission_guarantee",
                    "extension":"pdf"
                  },
                  "35302": {
                    "name": "credit",
                    "extension": "pdf"
                  },
                  "35301": {
                    "name": "person",
                    "extension": "pdf"
                  }
                }
              }
            }
            }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hayin_zhongbao_const", body)