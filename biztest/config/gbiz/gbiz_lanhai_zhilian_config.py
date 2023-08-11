
import common.global_const as gc



def update_gbiz_capital_lanhai_zhilian(account_register_duration_min=30):
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
                    "channel": "lanhai_zhilian",
                    "way": "lanhai_zhilian",
                    "status_scene":{
                        "register":{
                            "success_type":"once",
                            "post_register":True,
                            "register_status_effect_duration_day": 30,
                            "allow_fail":False,
                            "need_confirm_result":False
                        },
                        "route":{
                            "success_type":"once",
                            "allow_fail":False
                        },
                        "validate":{
                            "success_type":"once",
                            "account_register_duration_min": account_register_duration_min
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
            ],
            "ref_accounts": None
        },
        "task_config_map": {
            "ChangeCapital": {
                "execute": {
                    "event_handler_map": {
                        "LoanApplySyncFailedEvent": "LoanApplyQuery",
                        "LoanApplyAsyncFailedEvent": "LoanApplyQuery",
                        "LoanCreditApplySyncFailedEvent": "LoanConfirmQuery",
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
            "AssetImport": {
                "execute": {
                    "loan_validator": [
                        {
                            "rule": "1==1",
                            "err_msg": "蓝海直连[资产还款总额]不满足 irr23.8（按日365天），请关注！"
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
                                "code": "10000",
                                "messages": [
                                    "true_响应成功_1"
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
                                "code": "20000",
                                "messages": [
                                    "true_响应成功_true"
                                ]
                            },
                            {
                                "code": "20030",
                                "message": [
                                    "true_授信在有效期内，不能重复授信_false"
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
                                "code": "20074",
                                "messages": [
                                    "true_身份验证失败,该手机号可能已经被使用_false"
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
                                "code": "20000",
                                "messages": [
                                    "true_响应成功_2_1_null"
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
                                    "true_响应成功_3_0_null_授信总金额为空或授信金额小于借款金额",
                                    "true_响应成功_2_1_null_授信可用金额为空或授信金额小于借款金额"
                                ]
                            },
                            {
                                "code": "20004",
                                "message": [
                                    "true_未找到证件类型及证件号码一致的用户_授信查询返回结果为空"
                                ]
                            }
                        ]
                    }
                ]
            },
             "LoanCreditApply": {
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
                                "code": "20000",
                                "messages": [
                                    "true_响应成功_0_null"
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
                                "code": "20054",
                                "messages": [
                                    "true_根据身份证号查询，用户不存在，不能进行换绑卡操作_null_null"
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
                                "code": "30000",
                                "messages": [
                                    "true_响应成功"
                                ]
                            },
                            {
                                "code": "30041",
                                "message": [
                                    "true_进件数据保存失败。可能是重复发送了请求或者系统网络不稳定_支用申请单号为空"
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
                                "code": "30005",
                                "messages": [
                                    "true_支用失败_支用申请单号为空"
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
                                "code": "30000",
                                "messages": [
                                    "true_响应成功_17_null"
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
                                "code": "30000",
                                "messages": [
                                    "true_响应成功_21_对方行应答RJ01应答信息账号不存在"
                                ]
                            },
                            {
                                "code": "30021",
                                "messages": [
                                    "true_未查询到数据_借款查询结果列表为空"
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
                                "code": "30000",
                                "messages": [
                                    "true_响应成功_06_null"
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
                "execute": {
                    "upload_mode": "single",
                    "interval_in_minutes": "240"
                },
                "init": {
                    "delay_time": "delayDays(1,\"21:30:00\")",
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
            },
            "RongDanIrrTrial": {
                "execute": {
                    "trail_irr_limit": 35.99
                }
            }
        }
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanhai_zhilian", body)

def update_gbiz_capital_lanhai_zhilian_const():
    body = {
        "signAcctType": "01",
        "userCertType": 0,
        "perBindCardSendType": 0,
        "bindCardSendType": 1,
        "perBindCardSuccessStatus": 1,
        "bindCardSuccessStatus": 0,
        "bindCardFailStatus": 2,
        "existFlag": 1,
        "cooperateId": "000UC010000101718",
        "creditFileMap": {
            "1": "idcard-01.jpg",
            "2": "idcard-02.jpg",
            "29": "face-01.jpg"
        },
        "areaType": "3",
        "zipFilePrefix": "CREDITBOB",
        "zipFileSuffix": ".tar",
        "loanPreApplyCodePreFix": 1,
        "loanApplyCodePreFix": 2,
        "loanConfirmCodePreFix": 3,
        "defaultFiledMap": {
            "productCode": "NA",
            "channelCode": "NA",
            "gonganFaceTime": "1900-01-01",
            "gonganFaceResult": "NA",
            "fourElementsResult": "NA",
            "faceResult": "NA",
            "faceScore": "-999",
            "faceConfidence": "-999",
            "isMask": "NA",
            "isRescreens": "NA",
            "hasOcr": "NA",
            "scoreA": "-999",
            "scoreB": "-999",
            "scoreC": "-999",
            "scoreF": "-999",
            "score": "-999",
            "totalAmount": "-999.0",
            "firstCreditTime": "1900-01-01",
            "firstCreditLine": "-999",
            "lastAdjustmentLimitTime": "1900-01-01",
            "lastSecondLimit": "-999",
            "totalCreditUpdateFreq": "-999",
            "avgCreditUpdateAmt": "-999",
            "isFirstLoan": "NA",
            "firstLoanTime": "1900-01-01",
            "firstLoanAmount": "-999",
            "lastLoadTime": "1900-01-01",
            "lastLoadAmount": "-999",
            "cumulativeLoanAmount": "-999",
            "currentBalance": "-999",
            "maxHistoryOverdueCapital": "-999",
            "totalHistoryOverdueCount": "-999",
            "totalHistoryOverdueCapital": "-999",
            "maxHistoryOverdueNum": "-999",
            "maxHistoryOverdueDay": "-999",
            "totalHistoryOverdueDay": "-999",
            "lastOverdueDayNum": "-999",
            "lastOverdueCapital": "-999",
            "isOverdueByFirstRepayment": "NA",
            "last3mApplyNumPlatform": "-999",
            "last6mApplyNumPlatform": "-999",
            "last6mLoanNumPlatform": "-999",
            "socialUnityCreditCode": "-999",
            "loanPrice": "-999",
            "creditAmount": "-999",
            "deviceIp": "NA",
            "deviceNumOfPhone": "-999",
            "deviceNumOfIdNo": "-999"
        },
        "gpsPool": [
            "117,36.65,10",
            "120.33,36.07,10",
            "118.05,36.78,10",
            "117.57,34.86,10",
            "118.49,37.46,10",
            "121.39,37.52,10",
            "119.1,36.62,10",
            "116.59,35.38,10",
            "117.13,36.18,10",
            "122.1,37.5,10",
            "119.46,35.42,10",
            "118.03,37.36,10",
            "116.29,37.45,10",
            "115.97,36.45,10",
            "118.35,35.05,10",
            "115.43,35.24,10",
            "117.67,36.19,10"
        ],
        "gpsAddr": "山东",
        "applyPurposeMap": {
            "1": "66",
            "2": "5",
            "3": "2",
            "4": "3",
            "5": "6",
            "6": "4",
            "7": "9",
            "8": "62",
            "9": "9"
        },
        "grarMode": 1,
        "registerChannel": "XKD_YuanMengShu",
        "custCodeMap": {
            "new": "0",
            "old": "1"
        },
        "telephoneClassCode": 200,
        "defaultStationFlag": 1,
        "validateFlag": 1,
        "residential": 22,
        "household": 23,
        "vocationMap": {
            "1": "7",
            "2": "7",
            "3": "4",
            "4": "6",
            "5": "1",
            "6": "4",
            "7": "1",
            "8": "4",
            "9": "1",
            "10": "8",
            "11": "4",
            "12": "7",
            "13": "10",
            "14": "0",
            "15": "5"
        },
        "relationTypeMap": {
            "0": "1",
            "1": "5",
            "2": "7",
            "3": "2",
            "4": "8",
            "5": "8",
            "6": "8",
            "7": "8"
        },
        "sexMap": {
            "f": 2,
            "m": 1
        },
        "marriageStatusMap": {
            "1": "10",
            "2": "20",
            "3": "40",
            "4": "30"
        },
        "eduLevelMap": {
            "1": "80",
            "2": "70",
            "3": "60",
            "4": "50",
            "5": "40",
            "6": "30",
            "7": "20",
            "8": "10",
            "9": "10"
        },
        "productId": "F9557D5E4A62400BBF7DC9A98627D281",
        "productNo": "PN00000026",
        "repaymentMethod": 1,
        "loanUnit": 2,
        "gpsAddrCode": "370000",
        "itemNoZipFileSeq":{},
        "ftpChannelName": "lanhai_zhilian",
        "contractDownConfigList": [
            {
                "contractType": 28,
                "ftpPathExpr": "/writable/BobToyuanmengshu/#{T(DateUtil).format(#record.finishAt, 'yyyyMMdd')}/loan",
                "fileNameExpr": "001_loan_#{#record.dueBillNo}_10.pdf"
            },
            {
                "contractType": 34703,
                "ftpPathExpr": "/writable/BobToyuanmengshu/#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}/withholding",
                "fileNameExpr": "001_withholding_#{#userId}_10.pdf"
            },
            {
                "contractType": 34702,
                "ftpPathExpr": "/writable/BobToyuanmengshu/#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}/credit",
                "fileNameExpr": "001_credit_#{T(StringUtil).split(#record.tradeNo,'_')[1]}_10.pdf"
            },
            {
                "contractType": 34701,
                "ftpPathExpr": "/writable/BobToyuanmengshu/#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}/thirdauth",
                "fileNameExpr": "001_thirdauth_#{T(StringUtil).split(#record.tradeNo,'_')[1]}_10.pdf"
            },
            {
                "contractType": 34700,
                "ftpPathExpr": "/writable/BobToyuanmengshu/#{T(DateUtil).format(#record.pushAt, 'yyyyMMdd')}/creditauth",
                "fileNameExpr": "001_creditauth_#{T(StringUtil).split(#record.tradeNo,'_')[1]}_10.pdf"
            }
        ]
    }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_lanhai_zhilian_const", body)