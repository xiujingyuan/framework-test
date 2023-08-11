
import common.global_const as gc

def update_gbiz_capital_beiyin_daqin(account_effect_duration_day=180):
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
                    "channel":"beiyin_daqin",
                    "interaction_type":"SMS",
                    "way":"beiyin_daqin",
                    "status_scene":{
                        "register":{
                            "success_type":"once",
                            "register_status_effect_duration_day":account_effect_duration_day,
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
                            "rule": "#loan.totalAmount==cmdb.irrByDay(#loan,'23.9994')",
                            "err_msg": "北银大秦[资产还款总额]不满足 irr23.9994（按日360天），请关注！"
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
            "CapitalRepayPlanQuery": {
                "execute": {
                    "allow_diff_effect_at": False,
                    "allow_diff_due_at": True,
                    "allowance_check_range": {
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": True
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
            "RongDanIrrTrial": {
                "execute": {
                    "trail_irr_limit": 35.99
                }}
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_beiyin_daqin", body)


def update_gbiz_capital_beiyin_daqin_const():
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
            "33100": "PERSONAL_COMPOSITE_AUTH",
            "33102": "GUARANTEE",
            "33103": "PERSONAL_CREDIT_QUERY",
            "33104": "PERSONAL_INFO_QUERY",
            "33105": "BIZ_LOAN_REQUIREMENTS",
            "33106": "BIZ_CREDIT_AUTH"
        },
        "contractPushMap": {
            "33107": {
                "subDirExpr": "",
                "nameExpr": "#{#asset.itemNo}_#{#contract.code}.pdf"
            }
        },
        "ftpChannelName": "chongtian_jinmeixin",
        "baseFtpPath": "/home/jmx_pro/beiyin",
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
        "guaranteeName": "daqin_beiyin",
        "fundCode": "BOBCFC",
        "pushOrOrderNoSubfix": "BY",
        "needFullHMS": True
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_beiyin_daqin_const", body)