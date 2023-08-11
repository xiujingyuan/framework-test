import common.global_const as gc



def update_gbiz_capital_zhongke_hegang():
    zhongke_hegang = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "ChangeCapital"
        ],
        "register_config": {
            "register_step_list":[
                {
                    "channel":"zhongke_hegang",
                    "step_type":"PAYSVR_PROTOCOL",
                    "way":"tq",
                    "interaction_type":"SMS",
                    "group":"zhongke_hegang",
                    "status_scene":{
                        "register":{
                            "success_type":"executed",
                            "allow_fail":True,
                            "need_confirm_result":True
                        },
                        "route":{
                            "success_type":"executed",
                            "allow_fail":True
                        },
                        "validate":{
                            "success_type":"executed"
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
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanPostApplyFailedEvent": "LoanConfirmQuery",
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery"
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
                                    ""
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetAutoImport": {
                "init": {
                    "delay_time": "delayMinutes(120)"
                }
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36')",
                            "err_msg": "中科鹤岗[资产还款总额]不满足 irr36，请关注！"
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
                                "code": "2"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyNew": {
                "init": {
                    "delay_time": "delaySeconds(5)"
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
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
                            },
                            {
                                "code": "9000"
                            }
                        ]
                    }
                ]
            },
            "LoanApplyQuery": {
                "init": {
                    "delay_time": "delaySeconds(1)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "199991"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "190000"
                            },
                            {
                                "code": "199990"
                            }
                        ]
                    }
                ]
            },
            "LoanPostApply": {
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
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "1"
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
                                "code": "0"
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
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
                                "code": "2999911"
                            }
                        ]
                    },
                    {
                        "action": {
                            "policy": "fail"
                        },
                        "matches": [
                            {
                                "code": "2999910"
                            },
                            {
                                "code": "2999900"
                            },
                            {
                                "code": "2900000",
                                "messages": [
                                    "交易处理失败-E012-暂不支持该卡号-未查询到卡bin信息"
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
                        "min_value": -12,
                        "max_value": 12
                    }
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delaySeconds(60)"
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delaySeconds(3)"
                }
            },
            "CertificateApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "0",
                                "messages": [
                                    "交易接收成功"
                                ]
                            },
                            {
                                "code": "1200",
                                "messages": [
                                    "已存在该借据号的申请结清记录--遇到再配置"
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
                                "code": "1200",
                                "messages": [
                                    "该借据未结清"
                                ]
                            }
                        ]
                    }
                ]
            },
            "CertificateDownload": {
                "init": {
                    "delay_time": "delayMinutes(10)"
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_zhongke_hegang", zhongke_hegang)

def update_gbiz_capital_hegang_const():
    content = {
        "productCodeConfigMap": {
            "KN0-CL": {
                "ftpChannelName": "hegang",
                "channelCode": "KN0-CL",
                "productCode": "KN0-CL-DEBX-S",
                "ftpDownloadBaseDir": "/download",
                "ftpUploadBaseDir": "/upload"
            },
            "KN1-CL-HLJ": {
                "ftpChannelName": "hegang1",
                "channelCode": "KN1-CL",
                "productCode": "KN1-CL-DEBX-S",
                "ftpDownloadBaseDir": "/download",
                "ftpUploadBaseDir": "/upload"
            },
            "KN1-CL-NOT-HLJ": {
                "ftpChannelName": "hegang1",
                "channelCode": "KN1-CL",
                "productCode": "KN1-CL-DEBX-S",
                "ftpDownloadBaseDir": "/download",
                "ftpUploadBaseDir": "/upload"
            }
        },
        "gpsPool": [
            "126.63219451904298,45.751474682220234,10",
            "123.97024154663086,47.345452992392715,10",
            "129.61343765258792,44.57970841241188,3",
            "131.1607933044434,46.64778639598821,3",
            "130.28120040893558,47.33382034035365,3",
            "126.98521614074708,46.63971359454575,3",
            "130.3342437744141,46.809224459253954,3"
        ],
        "hljProductCodes": [
            "KN1-CL-HLJ"
        ],
        "hljAddrRatio": 7,
        "gaoDeConfig": {
            "baseUrl": "https://restapi.amap.com/v3/geocode",
            "extensions": "all",
            "key": "68109c1ef3101720d60f3ca2887c5f6f",
            "output": "json",
            "poitype": "120300|120302",
            "homeorcorp": "1"
        },
        "loanUseMap": {
            "1": "GRRCXFD",
            "2": "GRRCXFD",
            "3": "XXJX",
            "4": "LY ",
            "5": "ZX",
            "6": "ZXMR",
            "7": "GRRCXFD",
            "8": "LDXJJZJ",
            "9": "JYSB",
            "10": "CD",
            "11": "ZF",
            "12": "ZX",
            "13": "LDXJJZJ",
            "14": "LDXJJZJ",
            "15": "GRRCXFD"
        },
        "educationMap": {
            "0": "WZ",
            "1": "SS",
            "2": "YJ",
            "3": "BK",
            "4": "DZ",
            "5": "ZZ",
            "6": "JX",
            "7": "GZ",
            "8": "CZ",
            "9": "CZ",
            "10": "WM"
        },
        "marriageMap": {
            "0": "WH",
            "1": "WH",
            "2": "YH",
            "3": "SO",
            "4": "LT"
        },
        "residenceMap": {
            "0": "WZ",
            "1": "ZY",
            "2": "AJ",
            "3": "QS",
            "4": "SS",
            "5": "ZF",
            "6": "GY",
            "7": "QT"
        },
        "jobMap": {
            "1": "FW",
            "2": "ZG",
            "3": "XS",
            "4": "DC",
            "5": "ZZ",
            "6": "SM",
            "7": "SC",
            "8": "JS",
            "9": "ZFZY",
            "10": "JK",
            "11": "JR",
            "12": "SM",
            "13": "JK",
            "14": "ZF",
            "15": "NL"
        },
        "employmentTypeMap": {
            "上班族": "FW",
            "企业主": "GL",
            "自由职业": "FW",
            "无业待业": "FW",
            "其它": "FW"
        },
        "dutyMap": {
            "0": "WZ",
            "1": "GJ",
            "2": "ZJ",
            "3": "WU",
            "4": "WU",
            "5": "WU",
            "6": "WU",
            "7": "WU",
            "8": "WU",
            "9": "QT"
        },
        "industryMap": {
            "0": "WZ",
            "1": "BZ",
            "2": "GL",
            "3": "JY",
            "4": "BZ",
            "5": "YC",
            "6": "DC",
            "7": "ZZ",
            "8": "XJ",
            "9": "JRY",
            "10": "YC",
            "11": "ZS",
            "12": "WY",
            "13": "FW",
            "14": "WZ",
            "15": "NL"
        },
        "contractConfig": {
            "CREDIT_APPLY": [
                {
                    "attachmentType": 1,
                    "fileCode": "certFileA",
                    "filePath": "10005A",
                    "fileExt": "jpg"
                },
                {
                    "attachmentType": 2,
                    "fileCode": "certFileB",
                    "filePath": "10005B",
                    "fileExt": "jpg"
                },
                {
                    "attachmentType": 29,
                    "fileCode": "facephoto",
                    "filePath": "10005",
                    "fileExt": "jpg"
                },
                {
                    "attachmentType": 30740,
                    "fileCode": "infoUseAuthorization",
                    "filePath": "10012"
                },
                {
                    "attachmentType": 30742,
                    "fileCode": "investigationAuthorization",
                    "filePath": "10006"
                }
            ],
            "USE_APPLY": [
                {
                    "attachmentType": 30741,
                    "fileCode": "contract",
                    "filePath": "10003"
                },
                {
                    "attachmentType": 30745,
                    "fileCode": "commissionPay",
                    "filePath": "10019"
                },
                {
                    "attachmentType": 30744,
                    "fileCode": "guacont",
                    "filePath": "10008"
                },
                {
                    "attachmentType": 30743,
                    "fileCode": "guatee",
                    "filePath": "10008B"
                }
            ],
            "LOAN_SUCCESS": [
                {
                    "attachmentType": 30747,
                    "fileCode": "guaask",
                    "filePath": "10009",
                    "fileType": "GUAASK"
                },
                {
                    "attachmentType": 30746,
                    "fileCode": "loanproof",
                    "filePath": "11009",
                    "fileType": "LOANPROOF"
                }
            ]
        },
        "downloadContractTypeList": [
            28
        ],
        "ipSegPool": {
            "黑龙江哈尔滨市": [
                "39.134.62.0-39.134.62.255",
                "1.58.0.0-1.58.255.255",
                "1.62.0.0-1.62.255.255",
                "1.189.0.0-1.189.255.255",
                "111.40.159.0-111.40.206.255",
                "111.40.208.0-111.40.224.255",
                "111.40.226.0-111.40.255.255",
                "219.147.128.0-219.147.191.255",
                "112.100.32.0-112.100.103.255",
                "222.171.0.0-222.171.255.255"
            ],
            "黑龙江省齐齐哈尔市": [
                "1.57.64.0-1.57.127.255",
                "113.2.0.0-113.2.63.255",
                "117.179.108.0-117.179.123.255",
                "110.112.0.0-110.112.159.255",
                "111.41.208.0-111.41.223.255",
                "112.98.0.0-112.98.31.255",
                "222.170.0.0-222.170.31.255"
            ],
            "黑龙江省鹤岗市": [
                "1.56.0.0-1.56.127.255",
                "112.98.176.0-112.98.191.255",
                "39.134.63.0-39.134.63.255"
            ],
            "黑龙江省大庆市": [
                "1.59.0.0-1.59.127.255",
                "42.100.96.0-42.100.127.255",
                "111.41.224.0-111.41.239.255"
            ]
        },
        "incomeMap": {
            "0": 15000,
            "2000": 5000,
            "3000": 3000,
            "5000": 5000,
            "8000": 8000,
            "12000": 12000
        },
        "annIncomeMap": {
            "2000": "02",
            "3000": "02",
            "5000": "03",
            "8000": "03",
            "12000": "04",
            "15000": "05"
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hegang_const", content)
