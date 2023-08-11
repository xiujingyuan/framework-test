
import common.global_const as gc

def update_gbiz_capital_jiexin_taikang_xinheyuan(account_register_duration_min=90):
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
                      "channel": "jiexin_taikang_xinheyuan",
                      "step_type": "PROTOCOL",
                      "way": "jiexin_taikang_xinheyuan",
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
                      "channel": "jiexin_taikang_xinheyuan",
                      "step_type": "URL",
                      "way": "jiexin_taikang_xinheyuan",
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
                              "success_type": "current"
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
                        "rule": "#loan.totalAmount > cmdb.irrv2(#loan,'23.99') && #loan.totalAmount <= cmdb.irrv2(#loan,'24')",
                        "err_msg": "捷信泰康信合元[资产还款总额]不满足【irr23.99，irr24】请关注！"
                    }
                ]
              }
            },
            "LoanApplyNew": {
              "finish": [
                {
                  "action": {
                    "policy": "success"
                  },
                  "matches": [
                    {
                      "code": "10000",
                      "messages": [
                        "0000-null"
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
                        "9999-null"
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
                      "code": "10000",
                      "messages": [
                        "0000-null-01-null"
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
                        "0000-null-02-null",
                        "0000-null-02-综合评分不足"
                      ]
                    },
                    {
                        "code": "19999",
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
                      "code": "10000",
                      "messages": [
                        "0000-null-03-null"
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
                      "code": "10000",
                      "messages": [
                        "0000-null"
                      ]
                    },
                    {
                      "code": "19999",
                      "messages": [
                        "E00001-订单已存在"
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
                        "9999-mock失败"
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
                      "code": "10000",
                      "messages": [
                        "0000-null-06-success"
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
                        "0000-null-04-重复进件关闭历史单,此前状态:\\[5\\]",
                        "0000-null-08-success"
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
                    }
                  ]
                }
              ]
            },
            "CapitalRepayPlanQuery": {
              "execute": {
                "allow_diff_effect_at": False,
                "allow_diff_due_at": False,
                "allowance_check_range": {
                  "min_value": -5,
                  "max_value": 5
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
            },
             "CheckAccountStatus": {
              "init": {
                "delay_time": "delayMinutes(5)"
              }
            }
          }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jiexin_taikang_xinheyuan", body)


def update_gbiz_capital_jiexin_taikang_xinheyuan_const():
    body = {
            "reqSysCode": "KNXJJX",
            "fundCode": "XJ_JX",
            "capitalChannel": "knxjjx",
            "respCodePrefix": "1",
            "bindBankProcessRespCode": "P00001",
            "failedRespCode": "9999",
            "termType": "02",
            "defaultLoanUse": "MOD",
            "idCardExpired": "2099-12-31",
            "defaultDegree": "9",
            "defaultMarriage": "05",
            "defaultChildrenStatus": "5",
            "defaultOccupation": "Z",
            "defaultSimilarity": 75,
            "similarityThreshold": 70,
            "defaultFirstRelationship": "2",
            "defaultSecondRelationship": "6",
            "defaultDuty": "3",
            "defaultTechnical": "9",
            "defaultCompanyTrade": "9",
            "defaultCompanyNature": "50",
            "defaultEmployment": "24",
            "residentialStatus": "9",
            "idType": "10",
            "repayPlanDateFormat": "yyyy-MM-dd",
            "loanUseMap":
            {
                "1": "SHO",
                "2": "EDU",
                "3": "REN",
                "4": "DEC",
                "5": "TRA",
                "6": "MED",
                "7": "MED",
                "8": "SHO",
                "0": "MOD"
            },
            "genderMap":
            {
                "m": "男",
                "f": "女"
            },
            "educationMap":
            {
                "1": "01",
                "2": "02",
                "3": "03",
                "4": "03",
                "5": "03",
                "6": "04",
                "7": "05",
                "8": "06",
                "9": "07"
            },
            "degreeMap":
            {
                "1": "5",
                "2": "5",
                "3": "5",
                "4": "5",
                "5": "5",
                "6": "05",
                "7": "4",
                "8": "3",
                "9": "2"
            },
            "marriageMap":
            {
                "1": "01",
                "2": "02",
                "3": "03",
                "4": "04"
            },
            "occupationMap":
            {
                "1": "4",
                "2": "4",
                "3": "4",
                "4": "3",
                "5": "3",
                "6": "3",
                "7": "6",
                "8": "1",
                "9": "1",
                "10": "1",
                "11": "4",
                "12": "3",
                "13": "4",
                "14": "0",
                "15": "5"
            },
            "pictureTypeMap":
            {
                "1": "0",
                "2": "1",
                "29": "2"
            },
            "companyTradeMap":
            {
                "1": "H",
                "2": "H",
                "3": "F",
                "4": "E",
                "5": "C",
                "6": "G",
                "7": "D",
                "8": "I",
                "9": "O",
                "10": "P",
                "11": "J",
                "12": "I",
                "13": "P",
                "14": "S",
                "15": "A"
            },
            "jobNatureMap":
            {
                "1": "10",
                "2": "50",
                "3": "50",
                "4": "50",
                "5": "10",
                "6": "50"
            },
            "contractDownMap":
            {
                 "33600": "GRXF.XDED.HT.1.14.pdf",
                "33601": "KH.GR.SQS.JX.1.27.pdf",
                "28": "JXXJ.HBYH.GR.KKHT.1.39.pdf",
                "33603": "JXXJ.GRDK.BZBX.DZBXD.1.39.pdf",
                "33604": "GRXX.CL.SQS.XHY.1.27.pdf"
            },
            "contactRelationMap":
            {
                "0": "01",
                "1": "02",
                "2": "04",
                "3": "03",
                "4": "07",
                "5": "05",
                "6": "06",
                "7": "05"
            },
            "cityCodeMap": {
                "110000": "110100",
                "120000": "120100",
                "310000": "310100",
                "500000": "500100"
            }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jiexin_taikang_xinheyuan_const", body)
