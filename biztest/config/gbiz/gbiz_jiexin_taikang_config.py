
import common.global_const as gc

def update_gbiz_capital_jiexin_taikang(account_register_duration_min=90):
    body = {
              "cancelable_task_list": [
                "ApplyCanLoan",
                "LoanApplyNew",
                "ChangeCapital"
              ],
              "manual_reverse_allowed": False,
              "raise_limit_allowed": False,
              "register_config": {
                 "register_step_list": [
                          {
                            "channel": "jiexin_taikang",
                            "step_type": "PROTOCOL",
                            "way": "jiexin_taikang",
                            "interaction_type": "SMS",
                            "status_scene": {
                              "register": {
                                "success_type": "once",
                                "allow_fail": False,
                                "post_register": True,
                                "register_status_effect_duration_day": 1,
                                "need_confirm_result": False
                              },
                              "route": {
                                "success_type": "once",
                                "allow_fail": False,
                                "is_multi_account_card_allowed": True,
                              },
                              "validate": {
                                "success_type": "once",
                                "account_register_duration_min": account_register_duration_min,
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
                          },
                          {
                            "channel": "jiexin_taikang",
                            "step_type": "URL",
                            "way": "jiexin_taikang",
                            "interaction_type": "URL",
                            "status_scene": {
                              "register": {
                                "success_type": "current",
                                "register_status_effect_duration_day": -1,
                                "allow_fail": False,
                                "post_register": True,
                                "need_confirm_result": False
                              },
                              "route": {
                                "success_type": "current",
                                "allow_fail": False
                              },
                              "validate": {
                                "success_type": "current",
                                "account_register_duration_min":account_register_duration_min
                              }},
                              "actions": [
                                {
                                  "interaction_type": "SILENCE",
                                  "type": "PreGetUrl"
                                },
                                {
                                  "type": "GetUrl"
                                },
                                {
                                  "interaction_type": "SILENCE",
                                  "type": "PostGetUrl"
                                }
                              ]
                            }

                        ]
                      },
              "task_config_map": {
                "ChangeCapital": {
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
                },
                "AssetImport": {
                  "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount > cmdb.irrv2(#loan,'35.99') && #loan.totalAmount <= cmdb.irrv2(#loan,'36')",
                            "err_msg": "捷信泰康[资产还款总额]不满足【irr35.99，irr36】请关注！"
                        }
                    ]
                  }
                },
                "LoanPreApply": {
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
                          "code": "0",
                          "messages": [
                            "success-null-null"
                          ]
                        }
                      ]
                    }
                  ]
                },
                "LoanApplyNew": {
                  "finish": [
                    {
                      "action": {
                        "policy": "success"
                      },
                      "matches": [
                        {
                          "code": "0",
                          "messages": [
                            "success-null-null-null"
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
                            "mock失败-null-null-null",
                            "地区code为空 或者 查询不到对应省市",
                          ]
                        }
                      ]
                    }

                  ]
                },
                "LoanApplyQuery": {
                  "init": {
                    "delay_time": "delaySeconds(60)"
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
                            "success-SUCCESS-null-null"
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
                            "success-FAIL-null-null"
                          ]
                        },
                        {
                          "code": "9999",
                          "messages": [
                            "授信金额小于资产本金",
                            "授信额度已过期"
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
                            "success-IN_PROGRESS-null-null"
                          ]
                        }
                      ]
                    }
                  ]
                },
                "LoanApplyConfirm": {
                  "finish": [
                    {
                      "action": {
                        "policy": "success"
                      },
                      "matches": [
                        {
                          "code": "0",
                          "messages": [
                            "成功-SUCCESS-null-null",
                            "success-SUCCESS-null-null"
                          ]
                        },
                        {
                          "code": "19999",
                          "messages": [
                            "遇到再配置"
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
                            "success-FAIL-null-null"
                          ]
                        }
                      ]
                    }
                  ]
                },
                "LoanConfirmQuery": {
                  "init": {
                    "delay_time": "delaySeconds(120)"
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
                            "成功-SUCCESS-null-null-null",
                            "success-SUCCESS-null-null-null"
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
                            "success-FAIL-mock放款失败-null-null"
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
                            "0000-null-01-null"
                          ]
                        },
                          {
                              "code": "0",
                              "messages": [
                                  "success-IN_PROGRESS-null-null-null"
                              ]
                          }
                      ]
                    }
                  ]
                },
                "CapitalRepayPlanQuery": {
                  "execute": {
                    "adjust_fee_list": [
                      "technical_service"
                    ],
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                      "min_value": 0,
                      "max_value": 0
                    }
                  }
                },
                "ContractDown": {
                  "init": {
                    "delay_time": "delayMinutes(120)"
                  }
                },
                "ContractPush": {
                  "init": {
                    "delay_time": "delayMinutes(60)"
                  }
                },
                "AssetAutoImport": {
                  "init": {
                    "delay_time": "delayMinutes(90)"
                  }
                }
              }
            }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jiexin_taikang", body)


def update_gbiz_capital_jiexin_taikang_const():
    body = {
              "genderMap": {
                "m": "男",
                "f": "女"
              },
              "nationMap": {},
              "idCardExpired": "9999-12-31",
              "educationMap": {
                "1": "1",
                "2": "2",
                "3": "3",
                "4": "4",
                "5": "4",
                "6": "5",
                "7": "6",
                "8": "7",
                "9": "7"
              },
              "minIncome": 4000,
              "maxIncome": 20000,
              "maritalMap": {
                "1": "1",
                "2": "2",
                "3": "3",
                "4": "3"
              },
              "defaultMarital": "3",
              "defaultWechatId": "11111111-1111111111111111111",
              "deviceIdPrefix": "ID_",
              "defaultIpAddress": "0.0.0.0",
              "defaultGpsLat": "0",
              "defaultGpsLon": "0",
              "defaultGpsCity": "0",
              "defaultDeviceProducer": "Redmi K20 Pro",
              "contactRelationMap": {
                "0": "R",
                "1": "F",
                "2": "B",
                "3": "O",
                "4": "其他",
                "5": "其他",
                "6": "其他",
                "7": "其他"
              },
              "failedRespCode": "9999",
              "channelCode": "BAOFU",
              "merchantId": "F_AL_TK_HB",
              "repayPlanDateFormat": "yyyy-MM-dd",
              "creditPushAttachmentMap": {
                "1": "-idcardfront.jpg",
                "2": "-idcardback.jpg",
                "29": "-fr.jpg"
              },
              "creditPushContractMap": {
                "33700": "-aul.pdf",
                "33701": "-flc.pdf"
              },
              "pushFilePath": "/KUAINIU_TEST/APP0",
              "capitalFtpChannelName": "jiexin_taikang",
              "downFilePath": "/KUAINIU_TEST/CONTRACT",
              "downContractMap": {
                "28": "-ptc.pdf",
                "33703": "-ins.pdf"
              },
              "defaultDuty": "83",
              "defaultEmployerPhone": "13000000000",
              "defaultDeviceBrand": "Xiaomi",
              "networkType": "4G",
              "defaultCodeTable": "13",
              "defaultSimilarity": 75,
              "similarityThreshold": 70,
              "defaultInterestRate": "6.5%",
              "loanUsageMap": {
                "1": "dc",
                "2": "t",
                "3": "ra",
                "4": "le",
                "5": "d",
                "6": "h",
                "7": "h",
                "8": "p4",
                "9": "dc"
              },
                "includeFeesMap": {
                    "technical_service": "agreedFee"
                },
              "defaultLoanUsage": "dc",
              "defaultCodeTableInformation": "河北/山东/天津",
              "districtVersion": 1001,
              "imageMaxAllowSize": 1572864
    }