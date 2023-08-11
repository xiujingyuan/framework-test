import common.global_const as gc


def update_grouter_capital_rule_zhongyuan_zunhao(endtime='23:59'):
    body = {
            "fixedValues": {
                "importBeginTime": {
                    "name": "允许进件开始时间",
                    "value": "00:00"
                },
                "importEndTime": {
                    "name": "允许进件结束时间",
                    "value": endtime
                },
                "channel": {
                    "name": "资金方编码",
                    "value": "zhongyuan_zunhao"
                },
                "assetType": {
                    "name": "资产类型_消费分期",
                    "value": "paydayloan"
                },
                "minLoanAmount": {
                    "name": "最小借款金额（分）",
                    "value": 100000
                },
                "maxLoanAmount": {
                    "name": "最大借款金额（分）",
                    "value": 4000000
                },
                "minAge": {
                    "name": "借款人年龄下限",
                    "value": 22
                },
                "maxAge": {
                    "name": "借款人年龄上限",
                    "value": 55
                },
                "accountFailStatus": {
                    "name": "开户失败状态",
                    "value": 1
                },
                "bankCodeList": {
                    "name": "支持的银行编码列表",
                    "value": ["ICBC","ABC","BOC","CCB","BJBANK","COMM","CITIC","CEB","HXBANK","CMBC","GDB","SPABANK","CMB","CIB","SPDB","CZBANK","BOHAIB","SHBANK","PSBC","HZCB","NJCB","PAB","HXB"]
                },
                "blockDays": {
                    "name": "黑名单超时时间",
                    "value": 7
                },
                "blockTypes": {
                    "name": "黑名单类型列表",
                    "value": ["id_card"]
                }
            },
            "rules": {
                "global": {
                    "name": "全局规则组",
                    "compositeRuleType": "EnhancedActivationRuleGroup",
                    "composingRules": [
                        {
                            "name": "校验借款人年龄",
                            "condition": "#facts.borrower.age < #const.minAge.value or #facts.borrower.age > #const.maxAge.value"
                        },
                        {
                            "name": "校验借贷金额是否资方允许范围内",
                            "condition": "#facts.asset.amount < #const.minLoanAmount.value or #facts.asset.amount > #const.maxLoanAmount.value"
                        },
                        {
                            "name": "校验资产类型是否为消费分期",
                            "condition": "#facts.asset.type != #const.assetType.value"
                        },
                        {
                            "name": "校验资方支持的银行",
                            "condition": "!#const.bankCodeList.value.contains(#facts.receiveCard.bankCode)",
                            "actions": [
                                "#resultCollector.collect(#facts.channelName, #ruleName + '[' + #facts.receiveCard.bankCode +']')"
                            ]
                        },
                        {
                            "name": "校验第一联系人姓名至少有一个合法字符",
                            "condition": "T(StringUtil).isEmpty(#facts.borrower.relativeName) or !#facts.borrower.relativeName.matches('.*[\\u4e00-\\u9fa5a-zA-Z0-9·]{1}.*')"
                        },
                        {
                            "name": "校验是否在黑名单中",
                            "condition": "#facts.channelFactors.isInBlackList == true"
                        },
                        {
                            "name": "校验用户账户状态不能为失败",
                            "condition": "#facts.channelFactors.accountInfo.accountStatus == #const.accountFailStatus.value",
                            "actions": [
                                "#resultCollector.collect(#facts.channelName, #ruleName + ':' + #facts.channelFactors.accountInfo.message)"
                            ]
                        },
                        {
                            "name": "校验资方所需附件类型",
                            "condition": "#facts.attachmentTypeList == null or !#facts.attachmentTypeList.contains('1') or  !#facts.attachmentTypeList.contains('2') or !#facts.attachmentTypeList.contains('29')"
                        },
                        {
                            "name": "校验资方所需附件URL扩展名",
                            "condition": "#facts.attachmentUrlExtList == null or (!#facts.attachmentUrlExtList.contains('1_JPG') and !#facts.attachmentUrlExtList.contains('1_PNG') and !#facts.attachmentUrlExtList.contains('1_JPEG') ) or (!#facts.attachmentUrlExtList.contains('2_JPG') and !#facts.attachmentUrlExtList.contains('2_PNG') and !#facts.attachmentUrlExtList.contains('2_JPEG') ) or (!#facts.attachmentUrlExtList.contains('29_JPG') and !#facts.attachmentUrlExtList.contains('29_PNG') and !#facts.attachmentUrlExtList.contains('29_JPEG') )"
                        }
                    ]
                },
                "import": {
                    "name": "进件路由规则",
                    "compositeRuleType": "EnhancedActivationRuleGroup",
                    "composingRules": [
                        {
                            "name": "校验第二联系人姓名至少有一个合法字符",
                            "condition": "T(StringUtil).isEmpty(#facts.borrower.secondRelativeName) or !#facts.borrower.secondRelativeName.matches('.*[\\u4e00-\\u9fa5a-zA-Z0-9·]{1}.*')"
                        },
                        {
                            "name": "校验工作地址",
                            "condition": "T(StringUtil).isEmpty(#facts.borrower.workplace)"
                        }
                    ]
                },
                "change": {},
                "route": {}
            }
        }
    return gc.NACOS.update_configs("grouter%s" % gc.ENV, "grouter_capital_rule_zhongyuan_zunhao", body)

# def update_gbiz_capital_zhongyuan_zunhao_old(account_register_duration_min=120):
#     zhongyuan_zunhao = {
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
#                     "channel":"zhongyuan_zunhao",
#                     "interaction_type":"SMS",
#                     "way":"zhongyuan_zunhao",
#                     "status_scene":{
#                         "register":{
#                             "success_type":"once",
#                             "register_status_effect_duration_day":1,
#                             "allow_fail":False,
#                             "need_confirm_result":True,
#                             "post_register":True
#                         },
#                         "route":{
#                             "success_type":"once",
#                             "allow_fail":False
#                         },
#                         "validate":{
#                             "account_register_duration_min": account_register_duration_min,
#                             "success_type":"once"
#                         }
#                     },
#                     "actions":[
#                         {
#                             "allow_fail":False,
#                             "type":"GetSmsVerifyCode"
#                         },
#                         {
#                             "allow_fail":False,
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
#                                     "遇到再配置"
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
#                             "rule": "#loan.totalAmount==cmdb.irrByDay(#loan,'23.8','365per_year','D+0','D+0')",
#                             "err_msg": "中原樽昊[资产还款总额]不满足 irr23.8（按日365天），请关注！"
#                         }
#                     ]
#                 }},
#             "LoanPreApply": {
#                 "finish": [
#                     {
#                         "action": {
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "0",
#                                 "messages": [
#                                     "成功_Y"
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
#                                     "mock失败_N"
#                                 ]
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
#                                 "code": "10",
#                                 "messages": [
#                                     "成功_Y"
#                                 ]
#                             },
#                             {
#                                 "code": "110002",
#                                 "messages": [
#                                     "参数错误 已存在的授信申请"
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
#                                 "code": "10",
#                                 "messages": [
#                                     "成功_N_ZYZR,9999_暂不符合授信政策，感谢您的关注。;不符合授信标准！"
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
#                             "policy": "success"
#                         },
#                         "matches": [
#                             {
#                                 "code": "10",
#                                 "messages": [
#                                     "成功_99_01"
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
#                                 "code": "10",
#                                 "messages": [
#                                     "成功_20_"
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
#                                 "code": "10",
#                                 "messages": [
#                                     "mock失败_99_02",
#                                     "成功_99_02_mock拒绝码_mock拒绝原因"
#                                 ]
#                             },
#                             {
#                                 "code": "20",
#                                 "messages": [
#                                     "成功_返回业务data为空"
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
#                                 "code": "20",
#                                 "messages": [
#                                     "成功"
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
#                                 "code": "20",
#                                 "messages": [
#                                     "遇到在说"
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
#                                 "code": "21",
#                                 "messages": [
#                                     "mock失败"
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
#                                 "code": "20",
#                                 "messages": [
#                                     "成功_99_01"
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
#                                 "code": "20",
#                                 "messages": [
#                                     "成功_20_"
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
#                                 "code": "20",
#                                 "messages": [
#                                     "mock失败_99_02",
#                                     "成功_99_02_mock拒绝码_mock拒绝原因"
#                                 ]
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
#             "OurRepayPlanRefine": {
#                 "execute": {
#                     "need_refresh_due_at": False
#                 }
#             },
#             "ContractDown": {
#                 "init": {
#                     "delay_time": "delayDays(3,\"08:30:00\")"
#                 }
#             },
#             "ContractPush": {
#                 "init": {
#                     "delay_time": "delayMinutes(30)"
#                 }
#             },
#             "AssetAutoImport": {
#                 "init": {
#                     "delay_time": "delayMinutes(120)"
#                 }
#             },
#             "GuaranteeUpload": {
#                 "init": {
#                     "delay_time": "delayDays(4, \"08:00:00\")"
#                 }
#             },
#             "GuaranteeApply": {
#                 "init": {
#                     "delay_time": "delayDays(4, \"08:00:00\")"
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
#                                 "code": "30",
#                                 "messages": [
#                                     "成功_Y"
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
#                                 "code": "30",
#                                 "messages": [
#                                     "xxxxx"
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
#                                 "code": "30",
#                                 "messages": [
#                                     "遇到在配置"
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
#             "RongDanIrrTrial": {
#                 "execute": {
#                     "trail_irr_limit": 35.99
#                 }}
#         }
#     }
#     return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongyuan_zunhao", zhongyuan_zunhao)

def update_gbiz_capital_zhongyuan_zunhao(account_register_duration_min=120):
    zhongyuan_zunhao = {
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
                            "channel": "zhongyuan_zunhao",
                            "interaction_type": "SMS",
                            "way": "zhongyuan_zunhao",
                            "status_scene": {
                              "register": {
                                "success_type": "once",
                                "register_status_effect_duration_day": 1,
                                "allow_fail": False,
                                "need_confirm_result": True,
                                "post_register": True
                              },
                              "route": {
                                "success_type": "once",
                                "allow_fail": False
                              },
                              "validate": {
                                "account_register_duration_min": account_register_duration_min,
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
                        "title": "中原樽昊流程编排v3",
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
                                    "rule": "#loan.totalAmount==cmdb.irrByDay(#loan,'23.8','365per_year','D+0','D+0')",
                                    "err_msg": "中原樽昊[资产还款总额]不满足 irr23.8（按日365天），请关注！"
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
                                        "成功_Y"
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
                                        "mock失败_N"
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
                                      "code": "10",
                                      "messages": [
                                        "成功_Y"
                                      ]
                                    },
                                    {
                                      "code": "110002",
                                      "messages": [
                                        "参数错误 已存在的授信申请"
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
                                      "code": "10",
                                      "messages": [
                                        "成功_N_ZYZR,9999_暂不符合授信政策，感谢您的关注。;不符合授信标准！"
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
                                      "code": "10",
                                      "messages": [
                                        "成功_99_01"
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
                                      "code": "10",
                                      "messages": [
                                        "成功_20_"
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
                                      "code": "10",
                                      "messages": [
                                        "mock失败_99_02",
                                        "成功_99_02_mock拒绝码_mock拒绝原因"
                                      ]
                                    },
                                    {
                                      "code": "20",
                                      "messages": [
                                        "成功_返回业务data为空"
                                      ]
                                    }
                                  ]
                                }
                              ]
                            }
                          },
                          {
                            "id": "PostRegisterNotify",
                            "type": "PostRegisterNotifyBizPerformer",
                            "events": [
                              "PostRegisterNotifySuccessEvent"
                            ],
                            "activity": {
                              "init": {},
                              "execute": {},
                              "finish": []
                            }
                          },
                          {
                            "id": "CheckAccountStatus",
                            "type": "CheckAccountStatusTaskHandler",
                            "events": [
                              "CapitalAccountCheckSuccessEvent",
                              "CapitalAccountCheckFailEvent"
                            ],
                            "activity": {
                              "init": {},
                              "execute": {}
                            }
                          },
                          {
                            "id": "LoanApplyConfirm",
                            "type": "LoanApplyConfirmTaskHandler",
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
                                      "code": "20",
                                      "messages": [
                                        "成功"
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
                                      "code": "20",
                                      "messages": [
                                        "遇到在说"
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
                                      "code": "21",
                                      "messages": [
                                        "mock失败"
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
                                      "code": "20",
                                      "messages": [
                                        "成功_99_01"
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
                                      "code": "20",
                                      "messages": [
                                        "成功_20_"
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
                                      "code": "20",
                                      "messages": [
                                        "mock失败_99_02",
                                        "成功_99_02_mock拒绝码_mock拒绝原因"
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
                              "execute": {
                                "upload_mode": "single",
                                "interval_in_minutes": "240"
                              },
                              "init": {
                                "delayTime": "delayDays(1,\"21:30:00\")",
                                "simple_lock": {
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
                              "init": {
                                "delayTime": "delayMinutes(30)"
                              }
                            }
                          },
                          {
                            "id": "GuaranteeUpload",
                            "type": "GuaranteeUploadTaskHandler",
                            "events": [],
                            "activity": {
                              "init": {
                                "delayTime": "delayDays(4, \"08:00:00\")"
                              }
                            }
                          },
                          {
                            "id": "GuaranteeApply",
                            "type": "GuaranteeApplyTaskHandler",
                            "events": [],
                            "activity": {
                              "init": {
                                "delayTime": "delayDays(4, \"08:00:00\")"
                              }
                            }
                          },
                          {
                            "id": "CertificateApplySync",
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
                                      "code": "30",
                                      "messages": [
                                        "成功_Y"
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
                                      "code": "30",
                                      "messages": [
                                        "xxxxx"
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
                                      "code": "30",
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
                              "init": {
                                "delayTime": "delayDays(1, \"08:00:00\")"
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
                                "delayTime": "delayMinutes(120)"
                              }
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
                                        "遇到再配置"
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
                            "memo": "资产就绪成功事件订阅",
                            "listen": {
                              "event": "AssetReadyEvent"
                            },
                            "nodes": [
                              "LoanPreApply"
                            ]
                          },
                          {
                            "memo": "资产就绪失败事件订阅",
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
                              "skipDoubleCheck": True
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
                              "skipDoubleCheck": True
                            }
                          },
                          {
                            "memo": "资产进件查询成功事件订阅",
                            "listen": {
                              "event": "LoanApplyAsyncSucceededEvent"
                            },
                            "nodes": [
                              "PostRegisterNotify"
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
                              "skipDoubleCheck": True
                            }
                          },
                          {
                            "memo": "通知后置开户成功事件订阅",
                            "listen": {
                              "event": "PostRegisterNotifySuccessEvent",
                              "matches": []
                            },
                            "nodes": [
                              "CheckAccountStatus"
                            ]
                          },
                          {
                            "memo": "用户开户失败事件订阅",
                            "listen": {
                              "event": "CapitalAccountCheckFailEvent",
                              "matches": []
                            },
                            "nodes": [
                              "ChangeCapital"
                            ],
                            "associateData": {
                              "skipDoubleCheck": True,
                              "event": "CapitalAccountCheckFailEvent"
                            }
                          },
                          {
                            "memo": "用户开户成功事件订阅",
                            "listen": {
                              "event": "CapitalAccountCheckSuccessEvent",
                              "matches": []
                            },
                            "nodes": [
                              "LoanApplyConfirm"
                            ]
                          },
                          {
                            "memo": "支用申请失败事件订阅",
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
                            "memo": "支用申请成功事件订阅",
                            "listen": {
                              "event": "ConfirmApplySyncSucceededEvent",
                              "matches": []
                            },
                            "nodes": [
                              "LoanConfirmQuery"
                            ]
                          },
                          {
                            "memo": "支用查询失败事件订阅",
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
                            "memo": "支用查询成功事件订阅",
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
                            "memo": "合同下载成功事件订阅",
                            "listen": {
                              "event": "ContractDownSucceededEvent",
                              "matches": []
                            },
                            "nodes": [
                              "GuaranteeUpload",
                              "GuaranteeApply"
                            ]
                          },
                          {
                            "memo": "还款计划查询成功事件订阅",
                            "listen": {
                              "event": "RepayPlanHandleSucceededEvent",
                              "matches": []
                            },
                            "nodes": [
                              "OurRepayPlanRefine"
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
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongyuan_zunhao", zhongyuan_zunhao)
def update_gbiz_capital_zhongyuan_zunhao_const():
    body = {
        "certificateCodePrefix": "3",
        "certificateType": "14",
        "productCode": "kn_zy_dd",
        "notBindCardCode": 10002,
        "systemFlag": "691001",
        "openIdPrefix": "KN_",
        "idType": "20",
        "applcdeDateFormat": "yyyyMMddHH",
        "repayMode": "SYS002",
        "dueDayOpt": "1",
        "loanAccount": "N",
        "loanHkAccount": "N",
        "lprRateType": "01",
        "largeField": "{\"dk_price_int_rat\":0.24}",
        "submitLink": "01",
        "uploadMode": "01",
        "loanApplyCodePrefix": "1",
        "loanConfirmCodePrefix": "2",
        "executeApr": "0.085",
        "imageMaxAllowSize": 819200,
        "responseErrorCode": 9999,
        "grantDateFormat": "yyyy-MM-dd HH:mm:ss",
        "capitalFtpChannelName": "zhongyuan_zunhao",
        "pushContractFtpBasePath": "/kn/knFile/downfile/images",
        "ftpDatePathFormat": "yyyyMMdd",
        "downLoadContractFtpName": "kuainiu",
        "downloadContractFtpBasePath": "/tempfiles/dev/zhongyuan_zunhao",
        "positionOptMap": {
            "1": "10",
            "2": "50",
            "3": "50",
            "4": "50",
            "5": "50",
            "6": "50"
        },
        "indivEmpTypMap": {
            "1": "3",
            "2": "4",
            "3": "4",
            "4": "3",
            "5": "1",
            "6": "3",
            "7": "1",
            "8": "1",
            "9": "1",
            "10": "1",
            "11": "3",
            "12": "3",
            "13": "3",
            "14": "0",
            "15": "5"
        },
        "relationMap": {
            "0": "06",
            "1": "01",
            "2": "08",
            "3": "02",
            "4": "03",
            "5": "04",
            "6": "05",
            "7": "99"
        },
        "purposeMap": {
            "1": "3C",
            "2": "EDU",
            "3": "ZF",
            "4": "3C",
            "5": "TRA",
            "6": "JKYL",
            "7": "JKYL",
            "8": "NXP",
            "9": "3C"
        },
        "fileTypeMap": {
            "1": "01",
            "2": "02",
            "29": "04"
        },
        "pushContractTypes": [
            33006
        ],
        "downLoadContractList": [
            {
                "contractType": 28,
                "fileType": "13",
                "suffix": ".pdf",
                "submitLink": "02"
            },
            {
                "contractType": 33001,
                "fileType": "11",
                "suffix": ".pdf",
                "submitLink": "01"
            },
            {
                "contractType": 33002,
                "fileType": "09",
                "suffix": ".pdf",
                "submitLink": "01"
            },
            {
                "contractType": 33003,
                "fileType": "10",
                "suffix": ".pdf",
                "submitLink": "01"
            },
            {
                "contractType": 33004,
                "fileType": "08",
                "suffix": ".pdf",
                "submitLink": "02"
            },
            {
                "contractType": 33009,
                "fileType": "94",
                "suffix": ".pdf",
                "submitLink": "02"
            }
        ],
        "zipFtpBasePath": "/kn/knFile/upfile/zyzk6910/upfile/images",
        "guaranteeConfig": {
            "channelDir": "/upload/dfkn/zh",
            "partnerNo": "ZHKN",
            "productName": "快牛",
            "applyStatus": "S",
            "cfundChannelNo": "ZHKN-ZYXJ",
            "cfundChannelName": "樽昊-快牛-中原消金",
            "payWay": "02",
            "repayWay": "01",
            "yearRate": "0.24",
            "actYearRate": "0.24",
            "periodServiceRate": "0.155",
            "ointRate": "0.00041111",
            "validPass": "Y",
            "lendStatus": "S",
            "idCardType": "01",
            "dateFormat": "yyyyMMdd",
            "normalLoanStatus": "NOR",
            "productNo": "ZYZH",
            "annualIncome": "B20205",
            "industry": "B1003",
            "relation": "90",
            "loanUse": "07",
            "serviceFeeTypes": ["technical_service"],
            "guaranteeFeeTypes": [],
            "contractUploadConfig": {
                "fileName": "contract",
                "remoteDir": "/contract",
                "subFilesConfigMap": {
                    "28": {
                        "name": "loan",
                        "extension": "pdf"
                    },
                    "33010": {
                        "name": "draw",
                        "extension": "pdf"
                    },
                    "33007": {
                        "name": "commission_guarantee",
                        "extension": "pdf"
                    }
                }
            }
        },
        "reconciliationConfig": {
            "loanTyp": "PDI0561",
            "baseDir": "/kn/knFile/upfile/zyzk6910/downfile",
            "suffix": ".dat",
            "prefix": "zyxfB91",
            "dataFormat": "yyyyMMdd"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongyuan_zunhao_const", body)