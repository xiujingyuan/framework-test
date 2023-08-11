import common.global_const as gc


def update_gbiz_capital_lanzhou_haoyue_chongtian():
    body = {
            "manual_reverse_allowed": False,
            "cancelable_task_list": [
                "ApplyCanLoan",
                "LoanApplyNew",
                "ChangeCapital"
            ],
            "raise_limit_allowed": False,
            "register_config": {
                "register_step_list":[
                    {
                        "step_type":"PROTOCOL",
                        "channel":"lanzhou_haoyue_chongtian",
                        "way": "lanzhou_haoyue_chongtian",
                        "interaction_type":"SMS",
                        "status_scene":{
                            "register":{
                                "success_type":"once",
                                "register_status_effect_duration_day":1,
                                "allow_fail":False,
                                "need_confirm_result":False
                            },
                            "route":{
                                "success_type":"once",
                                "allow_fail":False
                            },
                            "validate":{
                                "success_type":"once"
                            }
                        },
                        "actions":[
                            {
                                "type":"GetSmsVerifyCode"
                            },
                            {
                                "type":"CheckSmsVerifyCode"
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
                                    "code": "12"
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
                                "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23.7') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                                "err_msg": "兰州昊悦崇天[资产还款总额]不满足 [irr23.7, irr24]，请关注！"
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
                                    "code": "1000000",
                                    "messages": [
                                        "成功"
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
                                    "code": "1999999",
                                    "messages": [
                                        "该用户已注册!",
                                        "mock_资料推送同步失败"
                                    ]
                                },
                                {
                                    "code": "1000001",
                                    "messages": [
                                        "联系人姓名不可为空（遇到再配置）",
                                        "身份证号已存在",
                                        "\\[居住市\\]不能为空",
                                        "\\[居住省\\]不能为空",
                                        "手机号已存在，不可修改（遇到再配置）",
                                        "公司名或者居住地长度不足"
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
                                "policy": "fail"
                            },
                            "matches": [
                                {
                                    "code": "1000067",
                                    "messages": [
                                        "流水号不存在"
                                    ]
                                },
                                {
                                    "code": "1000000",
                                    "messages": [
                                        "成功-FAIL-拉取身份证正面图片失败",
                                        "成功-FAIL-拉取活体图片失败",
                                        "成功-FAIL-mock_资料推送查询失败"
                                    ]
                                }
                            ]
                        },
                        {
                            "action": {
                                "policy": "success"
                            },
                            "matches": [
                                {
                                    "code": "1000000",
                                    "messages": [
                                        "成功-SUC"
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
                                        "成功-IN_HANDLE"
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
                                    "code": "2000000",
                                    "messages": [
                                        "成功"
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
                                    "code": "2900002",
                                    "messages": [
                                        "遇到再配置"
                                    ]
                                },
                                {
                                    "code": "2999999",
                                    "messages": [
                                        "用户资料不完整",
                                        "mock_试算失败"
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
                                    "code": "2900002",
                                    "messages": [
                                        "今日额度已抢完，请明日再试!"
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
                                    "code": "3000000",
                                    "messages": [
                                        "成功"
                                    ]
                                },
                                {
                                    "code": "3999999",
                                    "messages": [
                                        "流水号重复\\[.*\\]"
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
                                    "code": "3000044",
                                    "messages": [
                                        "签章失败",
                                        "遇到再配置"
                                    ]
                                },
                                {
                                    "code": "3999999",
                                    "messages": [
                                        "mock_放款申请失败"
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
                                "policy": "fail"
                            },
                            "matches": [
                                {
                                    "code": "3000000",
                                    "messages": [
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：外部放款失败\\)",
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：签章失败\\)",
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：null\\)",
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：放款失败\\)",
                                        "成功-WITHDRAWALS_REJECTED-\\(拒绝代码：null， 拒绝原因：风控拒绝\\)",
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：手动置为失效\\)",
                                        "成功-LOAN_FAILURE-.*"
                                    ]
                                }
                            ]
                        },
                        {
                            "action": {
                                "policy": "success"
                            },
                            "matches": [
                                {
                                    "code": "3000000",
                                    "messages": [
                                        "成功-LOAN_PASSED",
                                        "成功-LOAN_PASSED-.*"
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
                                    "code": "3000000",
                                    "messages": [
                                        "成功-LOANING",
                                        "成功-LOANING-.*"
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
                                "policy": "fail"
                            },
                            "matches": [
                                {
                                    "code": "3000000",
                                    "messages": [
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：外部放款失败\\)",
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：签章失败\\)",
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：null\\)",
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：放款失败\\)",
                                        "成功-WITHDRAWALS_REJECTED-\\(拒绝代码：null， 拒绝原因：风控拒绝\\)",
                                        "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：手动置为失效\\)",
                                        "成功-LOAN_FAILURE-.*"
                                    ]
                                }
                            ]
                        },
                        {
                            "action": {
                                "policy": "success"
                            },
                            "matches": [
                                {
                                    "code": "3000000",
                                    "messages": [
                                        "成功-LOAN_PASSED"
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
                                    "code": "3000000",
                                    "messages": [
                                        "成功-LOANING"
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "CapitalRepayPlanQuery": {
                    "execute": {
                        "adjust_fee_list": [
                            "consult"
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
                    "execute": {
                        "interval_in_minutes": "240"
                    },
                    "init": {
                        "delay_time": "delayDays(1, '04:20:00')",
                        "simple_lock": {
                            "key": "contractdown-ftp",
                            "ttlSeconds": 60
                        }
                    }
                },
                "AssetAutoImport": {
                    "init": {
                        "delay_time": "delayMinutes(90)"
                    }
                }
            }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_haoyue_chongtian", body)

def update_gbiz_capital_lanzhou_haoyue_chongtian_const():
    body = {
          "productCode": "FCDP",
          "contactRelationMap": {
            "0": "C",
            "1": "F",
            "2": "B",
            "3": "H",
            "4": "W",
            "5": "T",
            "6": "Y",
            "7": "Y"
          },
          "fileTyeMap": {
            "1": "CARD_FRONT_PHOTO",
            "2": "CARD_BACK_PHOTO",
            "29": "LIVE_PHOTO"
          },
          "educationMap": {
            "1": "F",
            "2": "F",
            "3": "E",
            "4": "E",
            "5": "E",
            "6": "D",
            "7": "C",
            "8": "B",
            "9": "A"
          },
          "maritalStatusMap": {
            "1": "S",
            "2": "C",
            "3": "D",
            "4": "W"
          },
          "professionMap": {
            "1": "J",
            "2": "J",
            "3": "J",
            "4": "J",
            "5": "P",
            "6": "P",
            "7": "P",
            "8": "P",
            "9": "P",
            "10": "B",
            "11": "K",
            "12": "P",
            "13": "P",
            "14": "B",
            "15": "L"
          },
          "incomeMap": {
            "0": "B",
            "2001": "B",
            "3001": "C",
            "5001": "D",
            "8001": "E",
            "12000": "F"
          },
          "loanUsageMap": {
            "1": "PL19",
            "2": "PL03",
            "3": "PL19",
            "4": "PL19",
            "5": "PL07",
            "6": "PL18",
            "7": "PL15",
            "8": "PL19",
            "9": "PL19"
          },
          "bankCodeMap": {
            "ICBC": "ICBC",
            "SPABANK": "PAB",
            "BOC": "BOC",
            "CCB": "CCB",
            "CIB": "CIB",
            "CMB": "CMB",
            "ABC": "ABC",
            "BJBANK": "BOB",
            "CEB": "CEB",
            "CITIC": "CITIC",
            "CMBC": "CMBC",
            "GDB": "GDB",
            "HXB": "HXB",
            "HXBANK": "HXB",
            "SHBANK": "SHB",
            "SPDB": "SPDB",
            "PSBC": "PSBC",
            "PAB": "PAB"
          },
          "contractMap": {
            "28": "LOAN",
            "34100": "PERSONAL_INFO_QUERY",
            "34101": "WITHHOLD",
            "34102": "BIZ_LOAN_REQUIREMENTS",
            "34103": "BIZ_CREDIT_AUTH",
            "34104": "ENTRUST_GUARANTEE",
            "34105": "PERSONAL_CREDIT_QUERY"
          },
          "priceTag": "IRR24",
          "defaultSimilarity": "75",
          "similarityThreshold": "74",
          "userCheckPushType": "105",
          "userInfoPushType": "2",
          "bindCardType": "1",
          "idCardLongTimeExpireDay": "20991231",
          "loanScene": "LOAN",
          "bindCardCertType": "I",
          "userPushIdType": "1",
          "fundCode": "XH",
          "pushOrOrderNoSubfix": "XH",
          "includeFeesMap": {
            "consult": "schdFee"
          },
          "needIp": True,
          "ipSegPool": [
            "27.224.128.0-27.224.191.255",
            "125.75.0.0-125.75.63.255",
            "202.201.0.0-202.201.105.255",
            "210.26.68.0-210.26.127.255",
            "222.23.32.0-222.23.191.255",
            "222.57.64.0-222.57.79.255",
            "42.89.72.0-42.89.111.255",
            "27.226.40.0-27.226.47.255",
            "60.164.0.0-60.164.15.255",
            "124.152.160.0-124.152.175.255",
            "210.26.24.0-210.26.31.255",
            "61.159.64.0-61.159.127.255",
            "222.57.16.0-222.57.31.255",
            "118.181.144.0-118.181.159.255",
            "42.90.16.0-42.90.47.255",
            "125.76.17.0-125.76.31.255",
            "42.88.208.0-42.88.231.255",
            "125.75.80.0-125.75.95.255",
            "27.225.176.0-27.225.199.255",
            "27.226.64.0-27.226.127.255",
            "124.152.65.0-124.152.75.255",
            "118.181.192.0-118.181.223.255"
          ]
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanzhou_haoyue_chongtian_const", body)