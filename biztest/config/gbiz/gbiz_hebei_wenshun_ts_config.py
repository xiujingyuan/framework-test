
import common.global_const as gc

def update_gbiz_capital_hebei_wenshun_ts():
    body = {
            "cancelable_task_list": [
                "ApplyCanLoan",
                "LoanApplyNew",
                "ChangeCapital"
            ],
            "manual_reverse_allowed": False,
            "raise_limit_allowed": False,
            "register_config": {
                "account_register_duration": 20,
                "is_multi_account_card_allowed": True,
                "is_strict_seq": True,
                "post_register": False,
                "ref_accounts": None,
                "register_step_list": [
                    {
                        "channel": "hebei_wenshun_ts",
                        "step_type": "PAYSVR_PROTOCOL",
                        "way": "tq",  # 支付主体未确认
                        "interaction_type": "SMS",
                        "group": "kuainiu",
                        "allow_fail": False,
                        "need_confirm_result": True,
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
                                "rule": "loan.totalAmount>=cmdb.irr(#loan,'23.98') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                                "err_msg": "河北稳顺[资产还款总额]不满足 irr24，请关注！"
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
                                        "影像资料上传成功"
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
                                        "遇到再配置"
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
                                    "code": "10000",
                                    "messages": [
                                        "0000_交易接收成功"
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
                                        "9000_交易处理失败"
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
                                        "9999_交易处理成功_1_null_null"
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
                                        "9999_交易处理成功_0_年龄不在授信范围内_R009"
                                    ]
                                },
                                {
                                    "code": "10000",
                                    "messages": [
                                        "9999_交易处理成功_0_null_null"
                                    ]
                                },
                                {
                                    "code": "19999",
                                    "messages": [
                                        "1000_查无此交易_null_null_null"
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
                                        "9999_交易处理成功_2_null_null"
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "LoanPostApply": {
                    "init": {
                        "delay_time": "delayMinutes(8)"
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
                                        "影像资料上传成功"
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
                                        "遇到再配置"
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
                                    "code": "20000",
                                    "messages": [
                                        "成功-SUCCESS-null-null",
                                        "0000_交易接收成功"
                                    ]
                                },
                                {
                                    "code": "29999",
                                    "messages": [
                                        "1101_重复放款"
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
                                    "code": "20000",
                                    "messages": [
                                        "9999_交易接收失败"
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
                                    "code": "20000",
                                    "messages": [
                                        "9999_交易处理成功_1_null_null"
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
                                    "code": "20000",
                                    "messages": [
                                        "9999_交易处理成功_0_null_null"
                                    ]
                                },
                                {
                                    "code": "29999",
                                    "messages": [
                                        "1000_查无此交易_null_null_null"
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
                                    "code": "20000",
                                    "messages": [
                                        "9999_交易处理成功_2_null_null"
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
                            "min_value": 0,
                            "max_value":0
                        }
                    }
                },
                "ContractDown": {
                    "init": {
                        "delay_time": "delayHours(48)"
                    }
                },
                "AssetAutoImport": {
                    "init": {
                        "delay_time": "delayMinutes(90)"
                    }
                }
            }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hebei_wenshun_ts", body)

def update_gbiz_capital_hebei_wenshun_ts_const():
    body = {
            "ftpName": "hebei_wenshun_ts",
            "ftpBasePath": "/sftp",
            "creditApplyFtpPath": "/10010/SX/",
            "guaranteeFtpPath": "/10010/RD/",
            "loanApplyFtpPath": "/10010/FK/",
            "uploadAttachmentMap": {
                "1": "certFileB_%s.jpg",
                "2": "certFileA_%s.jpg",
                "29": "facephoto_%s.jpg"
            },
            "uploadContractMap": {
                "34400": "investigationAuthorization_%s.pdf",
                "34401": "infoUseAuthorization_%s.pdf",
                "34402": "infoQueryAuthorization_%s.pdf",
                "34403": "loanusePromise_%s.pdf"
            },
            "guaranteeFileUploadMap": {
                "34404": "investigationAuthorizationRD_%s.pdf",
                "34405": "guacont_%s.pdf"
            },
            "loanApplyUploadMap": {
                "34406": "contract_%s.pdf"
            },
            "guaranteeFileSyncType": "USEAPPLY_FILE",
            "contractDownloadMap": {
                "28": {
                    "basePath": "/sftp/11003",
                    "fileNameFormat": "signedcontract_%s.pdf"
                }
            },
            "termTypeMap": {
                "month": "M",
                "day": "D"
            },
            "loanUseMap": {
                "1": "10",
                "2": "16",
                "3": "18",
                "4": "20",
                "5": "13",
                "6": "17",
                "7": "17",
                "8": "11",
                "9": "20"
            },
            "loanUseDetailMap": {
                "1": "1000",
                "2": "1600",
                "3": "1800",
                "4": "2004",
                "5": "1300",
                "6": "1700",
                "7": "1701",
                "8": "1100",
                "9": "2000"
            },
            "genderMap": {
                "m": "M",
                "f": "F"
            },
            "essdegrMap": {
                "1": "80",
                "2": "70",
                "3": "60",
                "4": "50",
                "5": "40",
                "6": "30",
                "7": "20",
                "8": "14",
                "9": "11"
            },
            "degreeMap": {},
            "marriagMap": {
                "1": "10",
                "2": "20",
                "3": "30",
                "4": "40"
            },
            "workstMap": {
                "1": "24",
                "2": "16",
                "3": "51",
                "4": "70",
                "5": "90",
                "6": "90"
            },
            "industryMap": {
                "1": "O",
                "2": "H",
                "3": "F",
                "4": "K",
                "5": "C",
                "6": "G",
                "7": "D",
                "8": "I",
                "9": "Q",
                "10": "P",
                "11": "J",
                "12": "L",
                "13": "R",
                "14": "S",
                "15": "A"
            },
            "jobNatureMap": {},
            "jobMap": {},
            "dutyMap": {},
            "jobTitleMap": {},
            "relRelationMap": {
                "0": "C",
                "1": "F",
                "2": "E",
                "3": "H",
                "4": "W",
                "5": "T",
                "6": "Y",
                "7": "O"
            },
            "cityIp": [
                "130100-39.134.187.0#9.134.193.255",
                "130200-27.129.8.0#27.129.15.255",
                "130300-27.129.40.0#27.129.43.255",
                "130400-27.129.24.0#27.129.31.255",
                "130500-27.129.48.0#27.129.51.25",
                "130600-27.128.192.0#27.128.207.255",
                "130700-27.129.52.0#27.129.55.255",
                "130800-27.129.60.0#27.129.63.255",
                "130900-27.129.44.0#27.129.47.255",
                "131000-27.128.208.0#27.128.223.255",
                "131100-27.128.80.0#27.128.81.255",
                "370100-1.51.144.0#1.51.159.255",
                "370200-27.221.80.0#27.221.95.255",
                "370300-58.58.96.0#58.58.109.255",
                "370400-58.57.224.0#58.57.255.255",
                "370500-58.57.128.0#58.57.159.255",
                "370600-58.58.80.0#58.58.95.255",
                "370700-39.90.64.0#39.90.127.255",
                "370800-58.58.48.0#58.58.63.255",
                "370900-27.221.160.0#27.221.191.255",
                "371000-58.58.208.0#58.58.223.255",
                "371100-58.58.176.0#58.58.191.255",
                "371600-58.58.0.0#58.58.15.255",
                "371400-1.51.168.0#1.51.191.255",
                "371500-27.222.96.0#27.222.127.255",
                "371300-58.57.32.0#58.57.63.255",
                "371700-39.87.192.0#39.87.223.255",
                "120000-27.0.128.0#27.0.135.255"
            ],
            "bankLineNoMap": {
                "ICBC": "102100004951",
                "CCB": "105100000017",
                "BOC": "104100000004",
                "ABC": "103100000018",
                "SPDB": "310290000013",
                "CITIC": "302100011000",
                "HXB": "304100040000",
                "CMBC": "305100000013",
                "GDB": "306581000003",
                "CIB": "309391000011",
                "PAB": "307584008005",
                "CZBANK": "316331000018",
                "EGBANK": "315456000105",
                "BH": "318110000014",
                "SHBANK": "325290000012",
                "BJBANK": "313100000013",
                "SHB": "325290000012"
            }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_hebei_wenshun_ts_const", body)