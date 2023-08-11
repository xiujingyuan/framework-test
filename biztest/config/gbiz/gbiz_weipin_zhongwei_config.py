
import common.global_const as gc


def update_gbiz_capital_weipin_zhongwei():
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
                    "channel":"weipin_zhongwei",
                    "way": "weipin_zhongwei",
                    "interaction_type":"SMS",
                    "status_scene":{
                        "register":{
                            "success_type":"once",
                            "register_status_effect_duration_day":0,
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
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'23.99')",
                            "err_msg": "唯品中为[资产还款总额]不满足 irr23.99，请关注！"
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
                                    "资料上传成功"
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
                                    "成功_90001_mock上传异常情况"
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
                                "code": "10000000",
                                "messages": [
                                    "成功_000000_S_渠道处理成功"
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
                                "code": "10000000",
                                "messages": [
                                    "成功_000000_F_渠道处理成功"
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
                                "code": "10000000",
                                "messages": [
                                    "成功_000000_S_渠道处理成功"
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
                                "code": "10107000",
                                "messages": [
                                    "成功_107000_F_风控拒绝"
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
                                "code": "10100003",
                                "messages": [
                                    "成功_100003_P_渠道处理中"
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
                                "code": "20000000",
                                "messages": [
                                    "成功_000000_S_成功"
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
                                "code": "20000000",
                                "messages": [
                                    "成功_000000_F_成功"
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
                                "code": "20000000",
                                "messages": [
                                    "成功_000000_00_成功"
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
                                "code": "20000000",
                                "messages": [
                                    "成功_000000_02_成功_mock放款异步查询失败",
                                    "成功_000000_02_成功_mock放款同步失败"
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
                                "code": "20000000",
                                "messages": [
                                    "成功_000000_03_成功"
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
                        "min_value": 0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delaySeconds(60)",
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
            "CertificateApply": {
                "init": {
                    "delay_time": "delaySeconds(10)"
                },
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
                    },
                    {
                        "action": {
                            "policy": "retry"
                        },
                        "matches": [
                            {
                                "code": "2",
                                "messages": [
                                    "资产.*,结清证明下载失败: 000000-访问成功"
                                ]
                            }
                        ]
                    }
                ]
            },
            "RongDanIrrTrial": {
                "execute": {
                    "trail_irr_limit": 35.99
                }}
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_weipin_zhongwei", body)



def update_gbiz_capital_weipin_zhongwei_const():
    body = {
        "productCode": "kn_wp_dd",
        "fileTypeMap": {
            "1": "1",
            "2": "2",
            "29": "3"
        },
        "maritalStatusMap": {
            "1": "10",
            "2": "20",
            "3": "40",
            "4": "40"
        },
        "sexMap": {
            "f": "2",
            "m": "1"
        },
        "educationMap": {
            "1": "80",
            "2": "70",
            "3": "60",
            "4": "40",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "10",
            "9": "10"
        },
        "occupationTypeMap": {
            "1": "24",
            "2": "54",
            "3": "51",
            "4": "70",
            "5": "90",
            "6": "31"
        },
        "relationshipMap": {
            "0": "01",
            "1": "00",
            "2": "03",
            "3": "02",
            "4": "08",
            "5": "05",
            "6": "07",
            "7": "09"
        },
        "incomeMap": {
            "0": "BELOW_2K",
            "2001": "2K_TO_5K",
            "3001": "2K_TO_5K",
            "5001": "5K_TO_8K",
            "8001": "8K_TO_10K",
            "12000": "15K_MORE"
        },
        "loanUseMap": {
            "1": "09",
            "2": "10",
            "3": "06",
            "4": "00",
            "5": "01",
            "6": "07",
            "7": "07",
            "8": "11",
            "9": "12"
        },
        "contractTypeMap": {
            "28": "0007",
            "31801": "0003",
            "31802": "0002",
            "31803": "0006"
        },
        "raceMap": {
            "汉": "01",
            "蒙古": "02",
            "回": "03",
            "藏": "04",
            "维吾尔": "05",
            "苗": "06",
            "彝": "07",
            "壮": "08",
            "布依": "09",
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
            "毛南": "36",
            "仡佬": "37",
            "锡伯": "38",
            "阿昌": "39",
            "普米": "40",
            "塔吉克": "41",
            "怒": "42",
            "乌孜别克": "43",
            "俄罗斯": "44",
            "鄂温克": "45",
            "德昂": "46",
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
            "其它": "97"
        },
        "contractFtpChannel": "kuainiu",
        "contractFtpBaseDir": "zhongzhirong/weipin",
        "companyCertNo": "9150010508307777ZA",
        "customerGroup": "06",
        "imageMaxAllowSize": 819200,
        "successRespCode": "000000",
        "openIdPrefix": "KN_",
        "idType": "01",
        "grantDateFormat": "yyyyMMddHHmmss",
        "longTimeIdExpireDay": "长期",
        "longTimeIdExpireDayActual": "2099-12-31",
        "defaultNationality": "CHN",
        "defaultDegree": "9",
        "defaultCompanyAttribute": "99",
        "defaultOccupation": "3",
        "defaultTitle": "9",
        "defaultPost": "3",
        "addressType": "0",
        "amortMethod": "02",
        "guaranteeContractPrefix": "WT",
        "guaranteeContractStatus": "300",
        "guaranteeCurrency": "CNY",
        "dateFormat": "yyyyMMdd",
        "adviceRate": "0.18",
        "loanApplyCodePrefix": "1",
        "loanConfirmCodePrefix": "2",
        "messageMaxLength": "150"
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_weipin_zhongwei_const", body)