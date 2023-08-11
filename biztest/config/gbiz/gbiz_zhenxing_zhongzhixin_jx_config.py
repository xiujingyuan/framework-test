
import common.global_const as gc


def update_gbiz_capital_zhenxing_zhongzhixin_jx(raise_limit_over_time_seconds=7200):
    body ={
          "manual_reverse_allowed": False,
          "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
          ],
          "raise_limit_allowed": False,
          "register_config": {
            "is_strict_seq": False,
            "register_step_list": [
              {
                "is_strict_seq": True,
                "allow_fail": False,
                "step_type": "PROTOCOL",
                "channel": "zhenxing_zhongzhixin_jx",
                "way": "zhenxing_zhongzhixin_jx",
                "interaction_type": "SMS",
                "status_scene": {
                  "register": {
                    "success_type": "once",
                    "allow_fail": False,
                    "need_confirm_result": False,
                    "allow_retry": True
                  },
                  "route": {
                    "success_type": "once",
                    "allow_fail": False,
                    "is_multi_account_card_allowed": True
                  },
                  "validate": {
                    "success_type": "once",
                    "account_register_duration_min": 90
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
          "task_config_map": {
            "ChangeCapital": {
              "execute": {
                "event_handler_map": {
                  "LoanApplySyncFailedEvent": "LoanApplyQuery",
                  "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                  "LoanCreditFailedEvent": "LoanCreditQuery",
                  "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
                  "LoanPostCreditFailedEvent": "LoanPostCredit",
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
                      "messages": [

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
                    "rule": "#loan.totalAmount > cmdb.irrv2(#loan,'23.6') && #loan.totalAmount <= cmdb.irrv2(#loan,'24')",
                    "err_msg": "振兴中智信捷信[资产还款总额]不满足【irr23.6，irr24】请关注！"
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
                        "地区code为空 或者 查询不到对应省市",
                        "遇到再配置"
                      ]
                    },
                    {
                        "code": "1",
                        "messages": [
                            "mock 进件失败-null-null-null" ]
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
                        "mock失败测试-FAIL-null-null"
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
            "LoanCreditApply": {
              "finish": [
                {
                  "action": {
                    "policy": "success"
                  },
                  "matches": [
                    {
                      "code": 0
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
                                  "mock失败测试-null-null-null"
                              ]
                          }

                      ]
                  }
              ]
            },
            "LoanPostCredit": {
              "finish": [
                {
                  "action": {
                    "policy": "success"
                  },
                  "matches": [
                    {
                      "code": "0",
                      "messages": [
                        "success-SUCCESS"
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
                                  "success-IN_PROGRESS"
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
                                  "mock失败测试-FAIL"
                              ]
                          }
                      ]
                  }
              ]
            },
            "LoanCreditQuery": {
              "finish": [
                {
                  "action": {
                    "policy": "success"
                  },
                  "matches": [
                    {
                      "code": "0",
                      "messages": [
                        "success-null-null-SUCCESS"
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
                                  "success-null-null-IN_PROGRESS"
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
                                  "success-null-null-FAIL"
                              ]
                          },
                            {
                                "code": "1",
                                "messages": [
                                    "mock预审查询失败-null-null-FAIL"
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
                        "mock 用信失败-FAIL-null-null"
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
                        "mock 放款失败-FAIL-null-null-null"
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
            "AssetAutoImport": {
              "init": {
                "delay_time": "delayMinutes(90)"
              }
            },
            "AssetConfirmOverTimeCheck": {
              "execute": {
                "raise_limit_over_time_seconds": raise_limit_over_time_seconds
              },
              "finish": [
                {
                  "action": {
                    "policy": "timeoutAndFail"
                  },
                  "matches": [
                    {
                      "code": "10005",
                      "messages": [
                        "确认类型\\[CONTRACT_VIA_URL\\]已超时"
                      ]
                    }
                  ]
                }
              ]
            }
          }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhenxing_zhongzhixin_jx", body)
def update_gbiz_capital_zhenxing_zhongzhixin_jx_const():
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
            "maxIncome": 10010,
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
                "3": "O"
            },
            "failedRespCode": "9999",
            "channelCode": "BAOFU",
            "merchantId": "F_AL_ZX_NU",
            "repayPlanDateFormat": "yyyy-MM-dd",
            "creditPushAttachmentMap": {
                "1": "-idcardfront.jpg",
                "2": "-idcardback.jpg",
                "29": "-fr.jpg"
            },
            "creditPushContractMap": {
                "34601": "-aul.pdf",
                "34602": "-flc.pdf"
            },
            "pushFilePath": "/KUAINIU_TEST/APP0",
            "capitalFtpChannelName": "jiexin_zhenxing",
            "downFilePath": "/KUAINIU_TEST/CONTRACT",
            "downContractMap": {
                 "28": "-ptc.pdf",
                "34603": "-lfg.pdf",
                "34604": "-guc.pdf"
            },
            "defaultDuty": "83",
            "defaultEmployerPhone": "13000000000",
            "defaultDeviceBrand": "Xiaomi",
            "networkType": "4G",
            "defaultCodeTable": "13",
            "defaultSimilarity": 75,
            "similarityThreshold": 70,
            "defaultInterestRate": "8.3%",
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
            "defaultCodeTableInformation": "辽宁省",
            "districtVersion": 1001,
            "imageMaxAllowSize": 1572864,
            "creditType": "101",
            "creditProduct": "F_AL_ZX_NU",
             "bankCodeMap": {
                "PSBC": "PSBC",
                "ICBC": "ICBC",
                "BOC": "BOC",
                "SPDB": "SPDB",
                "PAB": "PAB",
                "BJBANK": "BJCB",
                "COMM": "BOCM",
                "GDB": "CGB",
                "CEB": "EVRB",
                "CCB": "CCB",
                "CIB": "CIB",
                "HXB": "HUA",
                "ABC": "ABC"
            },
        "h5PageUrlTimeout": 2,
        "periodFileUploadMap": {
            "auls": "-aul.pdf",
            "flcs": "-flc.pdf"
        },
        "periodFileRootPath": "/KUAINIU_TEST/SUMMARY"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhenxing_zhongzhixin_jx_const", body)
