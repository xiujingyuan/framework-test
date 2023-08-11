
import common.global_const as gc

def update_gbiz_capital_jincheng_hanchen():
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
                    "channel":"jincheng_hanchen",
                    "interaction_type":"SMS",
                    "way":"jincheng_hanchen",
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
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount>=cmdb.irr(#loan,'23') && "
                                    "#loan.totalAmount<=cmdb.irr(#loan,'24.2')",
                            "err_msg": "锦程汉辰[资产还款总额]不满足 irr24，请关注！"
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
                                    "mock_资料推送同步失败"
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
                                "code": "100067",
                                "messages": [
                                    "流水号不存在"
                                ]
                            },
                            {
                                "code": "1000000",
                                "messages": [
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
                                "code": "2999999",
                                "messages": [
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
                                    "流水号重复.*"
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
                                "code": "3999999",
                                "messages": [
                                    "mock_放款申请失败"
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
                                    "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：放款失败\\)",
                                    "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：未查询到借款信息\\)",
                                    "成功-LOAN_FAILURE-\\(拒绝代码：null， 拒绝原因：mock_放款失败\\)"
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
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "CapitalAccountCheckFailEvent": "AccountRegisterQuery"
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
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": False,
                    "allowance_check_range": {
                        "min_value": -1500,
                        "max_value": 1500
                    }
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayMinutes(120)",
                    "simple_lock": {
                        "key": "contractdown-ftp",
                        "ttlSeconds": 60
                    }
                }
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delaySeconds(300)"
                }
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            },
            "RongDanIrrTrial": {
                "execute": {
                    "trail_irr_limit": 35.99
                }}
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jincheng_hanchen", body)


def update_gbiz_capital_jincheng_hanchen_const():
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
            "HXBANK": "HXB",
            "SHBANK": "SHB",
            "SPDB": "SPDB",
            "PSBC": "PSBC"
        },
        "contractMap": {
            "28": "LOAN",
            "31900": "PERSONAL_INFO_QUERY",
            "31901": "PERSONAL_CREDIT_QUERY",
            "31902": "BIZ_LOAN_REQUIREMENTS",
            "31903": "BIZ_CREDIT_AUTH",
            "31904": "GUARANTEE"
        },
        "contractPushMap": {
            "31905": {
                "subDirExpr": "",
                "nameExpr": "#{#asset.itemNo}_#{#contract.code}.pdf",
                "downloadType": 31905
            },
            "31908": {
                "subDirExpr": "",
                "nameExpr": "#{#asset.itemNo}_#{#contract.code}.pdf",
                "downloadType": 31906
            }
        },
        "ftpChannelName": "kuainiu",
        "baseFtpPath": "/tempfiles/dev/jincheng_hanchen",
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
        "fundCode": "JCCFC",
        "pushOrOrderNoSubfix": "JC",
        "guaranteeName": "hanchen_jincheng"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_jincheng_hanchen_const", body)


def update_gbiz_guarantee_hanchen_jincheng_const():
    body = {"bankAnnualRate": "10.3",
            "totalRate": "23.99",
            "ftpChannelName": "hanchen_jincheng",
            "baseDir": "/file",
            "marriageMap": {
                "1": "10",
                "2": "20",
                "3": "30",
                "4": "40",
                "0": "99"
            },
            "educationMap": {
                "1": "10",
                "2": "10",
                "3": "20",
                "4": "30",
                "5": "40",
                "6": "40",
                "7": "60",
                "8": "70",
                "9": "80",
                "10": "90"
            },
            "residenceStatus": {
                "0": "9",
                "1": "1",
                "2": "2",
                "3": "3",
                "4": "4",
                "5": "5",
                "6": "6",
                "7": "7"
            },
            "corpTradeMap": {
                "0": "9",
                "1": "S",
                "2": "S",
                "3": "P",
                "4": "Q",
                "5": "G",
                "6": "E",
                "7": "C",
                "8": "I",
                "9": "J",
                "10": "L",
                "11": "R",
                "12": "R"
            },
            "dutyMap": {
                "0": "9",
                "1": "1",
                "2": "2"
            },
            "signContractTypes": {
                "31908": {
                    "type": "rdzx_bank_letter",
                    "interfaceName": "tasynstreamsave"
                },
                "31905": {
                    "type": "jnsq_bank_letter",
                    "interfaceName": "personstreamsave",
                    "noSeal": True
                }
            },
            "filePrefixMap": {
                "loan_detail": "loan_",
                "repay_plan": "paymentPlan_",
                "borrower": "customer_",
                "borrower_family": "customer_family_",
                "borrower_marriage": "customer_marriage_",
                "borrower_work": "customer_work_"
            }
            }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_guarantee_hanchen_jincheng_const", body)
