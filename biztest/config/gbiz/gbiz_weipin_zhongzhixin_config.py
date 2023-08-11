import common.global_const as gc


def update_gbiz_capital_weipin_zhongzhixin():
    body = {
        "manual_reverse_allowed": False,
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
                    "interaction_type": "SMS",
                    "channel": "weipin_zhongzhixin",
                    "way": "weipin_zhongzhixin",
                    "status_scene": {
                        "register": {
                            "success_type": "once",
                            "register_status_effect_duration_day": 0,
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
                            "type": "GetSmsVerifyCode"
                        },
                        {
                            "type": "CheckSmsVerifyCode"
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
                            "rule": "loan.totalAmount>=cmdb.irr(#loan,'23.98') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                            "err_msg": "唯品中智信[资产还款总额]不满足 irr24，请关注！"
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
                                "code": "0",
                                "messages": [
                                    "90001_mock上传异常情况_success"
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
                                "code": "1000000",
                                "messages": [
                                    "S_000000_渠道处理成功_success_000000_访问成功"
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
                                "code": "1000000",
                                "messages": [
                                    "F_000000_渠道处理成功_success_000000_访问成功"
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
                                "code": "1000000",
                                "messages": [
                                    "S_null_000000_渠道处理成功_success_000000_访问成功"
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
                                "code": "1000000",
                                "messages": [
                                    "F_null_107000_风控拒绝_success_000000_访问成功"
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
                                    "P_null_100003_渠道处理中_success_000000_访问成功"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanApplyConfirm": {
                "init": {
                    "delay_time": "delaySeconds(15)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "2000000",
                                "messages": [
                                    "S_000000_成功_success_000000_访问成功"
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
                                    "F_000000_成功_success_000000_访问成功"
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
                                "code": "2000000",
                                "messages": [
                                    "00_null_000000_成功_success_000000_访问成功",
                                    "00__000000_成功_success_000000_访问成功"
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
                                    "02_mock放款同步失败_000000_成功_success_000000_访问成功",
                                    "02_mock放款异步查询失败_000000_成功_success_000000_访问成功"
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
                                "code": "2000000",
                                "messages": [
                                    "03_null_000000_成功_success_000000_访问成功",
                                    "03__000000_成功_success_000000_访问成功"
                                ]
                            }
                        ]
                    }
                ]
            },
            "GuaranteeApply": {
                "init": {
                    "delay_time": "delayHours(24)"
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
                                    ""
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
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "GuaranteeDownload": {
                "init": {
                    "delay_time": "delaySeconds(600)"
                }
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
                        "min_value": -1,
                        "max_value": 1
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractDown": {
                "execute": {
                    "upload_mode": "single",
                    "interval_in_minutes": "240"
                },
                "init": {
                    "delay_time": "delayMinutes(30)",
                    "simple_lock": {
                        "key": "contractdown-ftp",
                        "ttlSeconds": 60
                    }
                }
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_weipin_zhongzhixin", body)


def update_gbiz_capital_weipin_zhongzhixin_const():
    body = {
        "channel": "10010000028",
        "productId": "1201001030020",
        "tenantId": "888",
        "timeStampFormat": "yyyyMMddHHmmssSSS",
        "payChannel": "02",
        "idType": "01",
        "idCardExpired": "2099-12-31",
        "dateFormat": "yyyy-MM-dd",
        "paymentDateFormat": "yyyyMMdd",
        "nationality": "CHN",
        "race": {
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
            "基诺": "56"
        },
        "defaultRace": "97",
        "marital": {
            "0": "99",
            "1": "10",
            "2": "20",
            "3": "30",
            "4": "40"
        },
        "defaultMarital": "99",
        "sex": {
            "m": "1",
            "f": "2"
        },
        "defaultSex": "0",
        "education": {
            "0": "99",
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
        "defaultEducation": "99",
        "degree": {
            "0": "5",
            "1": "2",
            "2": "3",
            "3": "4",
            "4": "5",
            "5": "5",
            "6": "5",
            "7": "5",
            "8": "5",
            "9": "5",
            "10": "5"
        },
        "defaultDegree": "5",
        "occupationType": {
            "1": "17",
            "2": "21",
            "3": "51",
            "4": "13",
            "5": "70",
            "6": "31"
        },
        "defaultOccupationType": "99",
        "defaultCompanyAttribute": "40",
        "companyIndustry": {
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
            "10": "F",
            "11": "H",
            "12": "R",
            "13": "O",
            "14": "O",
            "15": "A"
        },
        "defaultCompanyIndustry": "9",
        "defaultOccupation": "3",
        "defaultPost": "9",
        "defaultTitle": "9",
        "income": {
            "0": "BELOW_2K",
            "2001": "2K_TO_5K",
            "3001": "2K_TO_5K",
            "5001": "5K_TO_8K",
            "8001": "8K_TO_10K",
            "12000": "15K_MORE"
        },
        "addressType": "0",
        "pushAttributes": {
            "1": "1",
            "2": "2",
            "29": "3"
        },
        "imageMaxAllowSize": 819200,
        "imageMinAllowSize": 3072,
        "housingConditions": "9",
        "loanUse": {
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
        "defaultLoanUse": "09",
        "amortMethod": "02",
        "contractDownload": {
            "28": "0007",
            "34902": "0003",
            "34901": "0002",
            "34903": "0006"
        },
        "adviceRate": "0.12",
        "relationship": {
            "0": "01",
            "1": "00",
            "2": "03",
            "3": "02",
            "4": "08",
            "5": "05",
            "6": "07",
            "7": "09"
        },
        "guaranteeContractStatus": "300",
        "guaranteeCurrency": "CNY",
        "guaranteeRate": "0.12",
        "platformCombinedRate": "0.24",
        "grantDateFormat": "yyyyMMddHHmmss",
        "projectNo": "zzx-kn-wph",
        "companyCertNo": "91440300793859199A",
        "guaranteeContractNo": "WT",
        "signContractNo": "34900",
        "downLoadContractNo":"34904",
        "signType": "10",
        "fileType": "DBHT",
        "fileFormat": "PDF",
        "companySignKeyList": ["甲方签章：深圳市中智信融资担保有限公司"],
        "fileChannel": "kuainiu",
        "fileName": "repayplan.txt",
        "okFileName": "repayplan.ok",
        "ftpChannelFormat": "/home/%s/upload/%s/%s",
        "ftpChannelFormat111": "/home/sftp/%sFTP/upload/%s/%s",
        "loanApplyPrefix": 1,
        "loanApplyConfirmPrefix": 2,
        "guaranteePrefix": 3
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_weipin_zhongzhixin_const", body)
