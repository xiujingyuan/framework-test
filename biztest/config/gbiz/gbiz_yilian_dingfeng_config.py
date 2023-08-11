
import common.global_const as gc


def update_gbiz_capital_yilian_dingfeng():
    body = {
        "cancelable_task_list": [
            "ApplyCanLoan",
            "LoanApplyNew",
            "ChangeCapital"
        ],
        "manual_reverse_allowed": False,
        "raise_limit_allowed": False,
        "register_config": {
            "register_step_list":[
                {
                    "channel":"yilian_dingfeng",
                    "step_type":"PAYSVR_PROTOCOL",
                    "way":"tq",
                    "interaction_type":"SMS",
                    "group":"yilian_dingfeng",
                    "status_scene":{
                        "register":{
                            "success_type":"executed",
                            "allow_fail":False,
                            "need_confirm_result":True
                        },
                        "route":{
                            "success_type":"executed",
                            "allow_fail":False
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
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "GrantFailedEvent": "LoanConfirmQuery",
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "ConfirmApplySyncFailedEvent": "LoanConfirmQuery",
                        "LoanCreditApplySyncFailedEvent": "LoanCreditQuery",
                        "LoanCreditFailedEvent": "LoanCreditQuery",
                        "LoanPostCreditFailedEvent": "LoanConfirmQuery"
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
                                    "遇到再进行配置"
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
                                "code": "-10000",
                                "messages": [
                                    "遇到再进行配置"
                                ]
                            }
                        ]
                    }
                ]
            },
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "#loan.totalAmount==cmdb.irr(#loan,'36')",
                            "err_msg": "亿联鼎丰[资产还款总额]不满足 irr36，请关注！"
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
                                    "01-0000-成功-成功"
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
                                "code": "1555555",
                                "messages": [
                                    "--facerecodegree人脸识别相似度\\(身份证照片与活体照片比对分数\\) 长度超限-"
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
                                "code": "1555555"
                            }
                        ]
                    }
                ]
            },
            "LoanPostApply": {
                "init": {
                    "delay_time": "delaySeconds(300)"
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
                                    "01-0000-成功-"
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
                                "code": "待配置"
                            }
                        ]
                    }
                ]
            },
            "LoanCreditApply": {
                "init": {
                    "delay_time": "delaySeconds(300)"
                },
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1010000"
                            },
                            {
                                "code": "1000000",
                                "messages": [
                                    "00-0000-成功-路由处理中"
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
                                "code": "待配置"
                            }
                        ]
                    }
                ]
            },
            "LoanCreditQuery": {
                "init": {
                    "delay_time": "delaySeconds(300)"
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
                                    "01-0001-成功-路由成功"
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
                                    "02-0005-成功-银行风控拒绝"
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
                                    "00-0000-成功-"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanPostCredit": {
                "init": {
                    "delay_time": "delaySeconds(300)"
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
                                    "01-0000-成功-"
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
                                "code": "待配置"
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
                                "code": "1000000",
                                "messages": [
                                    "00-0000-成功-处理中"
                                ]
                            },
                            {
                                "code": "1800015",
                                "messages": [
                                    "--该路由编号存在在途支用-"
                                ]
                            },
                            {
                                "code": "1800012",
                                "messages": [
                                    "--支用流水号重复-"
                                ]
                            }
                        ]
                    }
                ]
            },
            "LoanConfirmQuery": {
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
                                    "01-0001-成功-"
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
                                    "02-0006-成功-交易处理失败"
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
                                    "00-0000-成功-"
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
                        "min_value": -0,
                        "max_value": 0
                    }
                }
            },
            "OurRepayPlanRefine": {
                "execute": {
                    "need_refresh_due_at": False
                }
            },
            "ContractPush": {
                "init": {
                    "delay_time": "delayMinutes(2)"
                }
            },
            "ContractDown": {
                "init": {
                    "delay_time": "delayDays(2, \"08:00:00\")",
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
            },
            "CertificateApply": {
                "finish": [
                    {
                        "action": {
                            "policy": "success"
                        },
                        "matches": [
                            {
                                "code": "1000000",
                                "messages": [
                                    "01-true-成功-处理成功"
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
                                    "02-false-成功-借款未结清"
                                ]
                            }
                        ]
                    }
                ]

            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yilian_dingfeng", body)


def update_gbiz_capital_yilian_dingfeng_const():
    body = {
          "channel": "KN10001",
          "ftpChannelName": "yilian_dingfeng",
         # "ftpFileMaxSize": 3145728,
          "ftpFileMaxSize": 1024,
          "imageCompressScale": 0.5,
          "imageCompressQuantity": 0.8,
          "productIdMap": {
            "new_backup": "200275",
            "new": "200274",
            "old": "200274"
          },
          "pickupBankIdMap": {
            "ICBC": "102100099996",
            "ABC": "103100000026",
            "BOC": "104100000004",
            "CCB": "105100000017",
            "COMM": "301290000007",
            "CITIC": "302100011000",
            "CEB": "303100000006",
            "HXBANK": "304100040000",
            "CMBC": "305100000013",
            "GDB": "306581000003",
            "PAB": "307584007998",
            "CMB": "308584000013",
            "CIB": "309391000011",
            "SPDB": "310290000013",
            "BJBANK": "313100000013",
            "SHBANK": "325290000012"
          },
          "loanUseMap": {
            "1": "1",
            "2": "2",
            "3": "9",
            "4": "1",
            "5": "4",
            "6": "2",
            "7": "2",
            "8": "2",
            "9": "1"
          },
          "educationMap": {
            "1": "90",
            "2": "60",
            "3": "40",
            "4": "40",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "14",
            "9": "11"
          },
          "marriageMap": {
            "1": "10",
            "2": "99",
            "3": "40",
            "4": "30"
          },
          "degreeMap": {
            "1": "05",
            "2": "05",
            "3": "05",
            "4": "05",
            "5": "05",
            "6": "05",
            "7": "04",
            "8": "03",
            "9": "02"
          },
          "industryMap": {
            "1": "O",
            "2": "I",
            "3": "H",
            "4": "K",
            "5": "C",
            "6": "F",
            "7": "M",
            "8": "G",
            "9": "Q",
            "10": "P",
            "11": "J",
            "12": "Q",
            "13": "R",
            "14": "S",
            "15": "A"
          },
          "relationMap": {
            "0": "C",
            "1": "D",
            "2": "B",
            "3": "H",
            "4": "W",
            "5": "T",
            "6": "Y",
            "7": "O"
          },
          "productTypeMap": {
            "old": "21202DF",
            "new": "21202DF",
            "new_backup": "21201DF"
          },
          "multiProdTypeMap": {
            "df": {
              "old": "21202DF",
              "new": "21202DF"
            },
            "df2": {
              "old": "21202DF2",
              "new": "21202DF2"
            }
          },
          "jobDetailMap": {
            "1": "4J",
            "2": "4C",
            "3": "4A",
            "4": "6C",
            "5": "6R",
            "6": "3C",
            "7": "6J",
            "8": "4D",
            "9": "6L",
            "10": "2H",
            "11": "2F",
            "12": "2G",
            "13": "4M",
            "14": "3A",
            "15": "5Z"
          },
          "feeMappingMap": {
            "Q003": [
              "technical_service"
            ]
          },
          "postApplyPushAttachments": [
            {
              "attachmentType": "31700",
              "fileType": "ylamountcontract",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "31715",
              "fileType": "ylquery",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "31716",
              "fileType": "yluse",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "31703",
              "fileType": "ylcredit",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "31704",
              "fileType": "qjcredit",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "1",
              "fileType": "idcardfront",
              "suffix": "jpg",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "2",
              "fileType": "idcardback",
              "suffix": "jpg",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "29",
              "fileType": "face",
              "suffix": "jpg",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "31717",
              "fileType": "ylpromise",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            }
          ],
          "postCreditPushAttachments": [
            {
              "attachmentType": "31714",
              "fileType": "loancount",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "31706",
              "fileType": "deduction",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            }
          ],
          "grantPushAttachments": [
            {
              "attachmentType": "31708",
              "fileType": "danbaocount",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            },
            {
              "attachmentType": "31709",
              "fileType": "danbaoletter",
              "suffix": "pdf",
              "remoteDir": "/cpu/KN10001/need/"
            }
          ],
          "contractFtpMappingMap": {
            "28": {
              "base_path": "/cpu/KN10001/contract/",
              "suffix": "_loan.pdf"
            },
            "31707": {
              "base_path": "/cpu/KN10001/contract/",
              "suffix": "_limit.pdf",
              "path_date": "push_at"
            }
          },
          "guaranteeConfig": {
            "channelDir": "/upload/dfkn",
            "partnerNo": "DFKN",
            "productName": "快牛",
            "applyStatus": "S",
            "cfundChannelNo": "YLYH-DFKN",
            "cfundChannelName": "亿联银行",
            "payWay": "02",
            "repayWay": "01",
            "yearRate": "0.24",
            "actYearRate": "0.24",
            "periodServiceRate": "0.155",
            "ointRate": "0.03541667",
            "validPass": "Y",
            "lendStatus": "S",
            "idCardType": "01",
            "dateFormat": "yyyyMMdd",
            "normalLoanStatus": "NOR",
            "productNo": "YLDF",
            "annualIncome": "B20205",
            "industry": "B1003",
            "relation": "90",
            "loanUse": "07",
            "serviceFeeTypes": ["technical_service"],
            "guaranteeFeeTypes": [],
            "contractUploadConfig": {
              "fileName": "contract",
              "remoteDir": "/contract",
              "subFilesConfigMap": {
                "28": {
                  "name": "loan",
                  "extension": "pdf"
                },
                "31706": {
                  "name": "draw",
                  "extension": "pdf"
                },
                "31708": {
                  "name": "commission_guarantee",
                  "extension": "pdf"
                },
                "31709": {
                  "name": "guarantee",
                  "extension": "pdf"
                }
              }
            }
          }
        }
    gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_yilian_dingfeng_const", body)


def update_gbiz_guarantee_dingfeng_const():
    body = {
        "ftpChannelName": "dingfeng",
        "fileConfigMap": {
            "apply_info": {
                "fileName": "apply_info.txt",
                "remoteDir": "/daily"
            },
            "loan_detail": {
                "fileName": "loan_detail.txt",
                "remoteDir": "/daily"
            },
            "repay_plan": {
                "fileName": "repay_plan.txt",
                "remoteDir": "/daily"
            },
            "IMAGE": {
                "fileName": "apply",
                "remoteDir": "/apply",
                "subFilesConfigMap": {
                    "1": {
                        "name": "idFtImg",
                        "extension": "jpg"
                    },
                    "2": {
                        "name": "idBkImg",
                        "extension": "jpg"
                    },
                    "29": {
                        "name": "face1",
                        "extension": "jpg"
                    }
                }
            }
        },
        "sexMap": {
            "m": "01",
            "f": "02"
        },
        "partnerNoMap": {
            "yilian_dingfeng": "DFKN"
        },
        "educationMap": {
            "1": "90",
            "2": "70",
            "3": "60",
            "4": "50",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "10",
            "9": "10"
        },
        "marriageMap": {
            "1": "10",
            "2": "20",
            "3": "40",
            "4": "30"
        }
    }
    gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_guarantee_dingfeng_const", body)
