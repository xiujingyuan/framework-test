
import common.global_const as gc

def update_gbiz_capital_changyin_mingdonghua_rl():
    body ={
            "cancelable_task_list":[
                "ApplyCanLoan",
                "LoanApplyNew",
                "ChangeCapital"
            ],
            "manual_reverse_allowed":False,
            "raise_limit_allowed":False,
            "register_config":{
                "register_step_list":[
                    {
                        "step_type":"PROTOCOL",
                        "channel":"changyin_mingdonghua_rl",
                        "way": "changyin_mingdonghua_rl",
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
                                "allow_fail":False,
                                "type":"GetSmsVerifyCode"
                            },
                            {
                                "allow_fail":False,
                                "type":"CheckSmsVerifyCode"
                            }
                        ]
                    }
                ]
            },
            "task_config_map":{
                "ChangeCapital":{
                    "execute":{
                        "event_handler_map":{
                            "LoanApplySyncFailedEvent":"LoanApplyQuery",
                            "LoanApplyAsyncFailedEvent":"LoanApplyQuery",
                            "ConfirmApplySyncFailedEvent":"LoanConfirmQuery",
                            "GrantFailedEvent":"LoanConfirmQuery"
                        },
                        "can_change_capital":True
                    },
                    "finish":[
                        {
                            "action":{
                                "policy":"success"
                            },
                            "matches":[
                                {
                                    "code":"0",
                                    "messages":[
                                        "切资方路由\\(二次\\)成功"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"finalFail"
                            },
                            "matches":[
                                {
                                    "code":"12",
                                    "messages":[

                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"fail"
                            },
                            "matches":[
                                {
                                    "code":"1",
                                    "messages":[
                                        "遇到在配置"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"retry"
                            },
                            "matches":[
                                {
                                    "code":"100998"
                                }
                            ]
                        }
                    ]
                },
                "AssetImport":{
                    "execute":{
                        "loan_validator":[
                            {
                                "rule":"#loan.totalAmount>=cmdb.irr(#loan,'23.98') && #loan.totalAmount<=cmdb.irr(#loan,'24')",
                                "err_msg":"长银明东华润楼[资产还款总额]不满足 irr24，请关注！"
                            }
                        ]
                    }
                },
                "LoanPreApply":{
                    "finish":[
                        {
                            "action":{
                                "policy":"success"
                            },
                            "matches":[
                                {
                                    "code":"0",
                                    "messages":[
                                        "影像资料上传成功"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"fail"
                            },
                            "matches":[
                                {
                                    "code":"19999",
                                    "messages":[
                                        "遇到再配置"
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "LoanApplyNew":{
                    "finish":[
                        {
                            "action":{
                                "policy":"success"
                            },
                            "matches":[
                                {
                                    "code":"10000",
                                    "messages":[
                                        "0_Success_P"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"fail"
                            },
                            "matches":[
                                {
                                    "code":"10000",
                                    "messages":[
                                        "0_Success_F"
                                    ]
                                }

                            ]
                        }
                    ]
                },
                "LoanApplyQuery":{
                    "init":{
                        "delay_time":"delaySeconds(60)"
                    },
                    "finish":[
                        {
                            "action":{
                                "policy":"success"
                            },
                            "matches":[
                                {
                                    "code":"10000",
                                    "messages":[
                                        "0_Success_S_null",
                                        "0_Success_S"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"fail"
                            },
                            "matches":[
                                {
                                    "code": "19999",
                                    "messages": [
                                        "E2000001_授信申请不存在_"
                                    ]
                                },
                                {
                                    "code": "10000",
                                    "messages": [
                                        "0_Success_F_授信失败",
                                        "授信金额小于资产本金"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"retry"
                            },
                            "matches":[
                                {
                                    "code":"10000",
                                    "messages":[
                                        "0_Success_P_null"
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "LoanPostApply":{
                    "finish":[
                        {
                            "action":{
                                "policy":"success"
                            },
                            "matches":[
                                {
                                    "code":"0",
                                    "messages":[
                                        "影像资料上传成功"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"fail"
                            },
                            "matches":[
                                {
                                    "code":"19999",
                                    "messages":[
                                        "遇到再配置"
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "LoanApplyConfirm":{
                    "finish":[
                        {
                            "action":{
                                "policy":"success"
                            },
                            "matches":[
                                {
                                    "code":"20000",
                                    "messages":[
                                        "0_Success_P"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"fail"
                            },
                            "matches":[
                                {
                                    "code":"20000",
                                    "messages":[
                                        "0_Success_F"
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "LoanConfirmQuery":{
                    "init":{
                        "delay_time":"delaySeconds(120)"
                    },
                    "finish":[
                        {
                            "action":{
                                "policy":"success"
                            },
                            "matches":[
                                {
                                    "code":"20000",
                                    "messages":[
                                        "0_Success_S_放款成功",
                                        "0_Success_S_清算成功"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"fail"
                            },
                            "matches":[
                                {
                                    "code":"20000",
                                    "messages":[
                                        "0_Success_F_放款失败"
                                    ]
                                },
                                {
                                    "code": "29999",
                                    "messages": [
                                        "E2000001_借款申请不存在_"
                                    ]
                                }
                            ]
                        },
                        {
                            "action":{
                                "policy":"retry"
                            },
                            "matches":[
                                {
                                    "code":"20000",
                                    "messages":[
                                        "0_Success_P_"
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "CapitalRepayPlanQuery":{
                    "execute":{
                        "allow_diff_effect_at":False,
                        "allow_diff_due_at":False,
                        "allowance_check_range":{
                            "min_value":0,
                            "max_value":0
                        }
                    }
                },
                "OurRepayPlanRefine":{
                    "execute":{
                        "need_refresh_due_at":False
                    }
                },
                "GuaranteeApply":{
                    "init":{
                        "delay_time":"delayHours(60)"
                    }
                },
                "ContractDown":{
                    "init":{
                        "delay_time":"delayMinutes(10)"
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
                                    "code": "30000",
                                    "messages": [
                                        "0_Success_S_接收成功"
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
                                        "遇到在配置"
                                    ]
                                }
                            ]
                        }
                    ]
                },
                "CertificateDownload": {
                    "execute": {
                        "interval_in_minutes": "30"
                    },
                    "init": {
                        "delay_time": "delayMinutes(30)"
                    }
              },
                "AssetAutoImport":{
                    "init":{
                        "delay_time":"delayMinutes(90)"
                    }
                }
            }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_changyin_mingdonghua_rl", body)

def update_gbiz_capital_changyin_mingdonghua_rl_const():
    body ={
            "assetPackageNo": "AP0LB62VHV1",
            "objectKeyPrefix": "kuainiu-test",
            "loanTyp": "DJT100",
            "capitalFtpChannelName": "changyin_runlou",
            "periodicFilePath": "/writable/assistance/upload/%s",
            "includeFeesMap": {
                "technical_service": "psFeeAmt"
            },
            "serialNos": {
                "apply_no": "#creditApplyEventDto.applyNo",
                "out_cust_id": "#creditApplyEventDto.outCustId",
                "loan_apply_business_no": "#loanApplyEventDto.businessNo",
                "loan_seq": "#loanApplyEventDto.loanSeq",
                "contract_no": "#contractNo"
            },
            "bankCodeMap": {
                "icbc": "0102",
                "boc": "0104",
                "ccb": "0105",
                "spdb": "0310",
                "cgb": "0306",
                "pab": "04105840",
                "cib": "0309",
                "abc": "0103",
                "comm": "0301",
                "citic": "0302",
                "cmb": "0308",
                "hxb": "0304",
                "psbc": "0403",
                "ceb": "0303",
                "cmbc": "0305",
                "cabank": "03137950"
            },
            "genderMap": {
                "m": "10",
                "f": "20"
            },
            "marriageMap": {
                "0": "90",
                "1": "10",
                "2": "20",
                "3": "90",
                "4": "50"
            },
            "educationMap": {
                "1": "40",
                "2": "40",
                "3": "30",
                "4": "99",
                "5": "30",
                "6": "20",
                "7": "10",
                "8": "00",
                "9": "00"
            },
            "degreeMap": {
                "1": "5",
                "2": "5",
                "3": "5",
                "4": "5",
                "5": "5",
                "6": "5",
                "7": "4",
                "8": "3",
                "9": "2"
            },
            "acctTypMap": {
                "individual": "01",
                "enterprise": "02"
            },
            "professionMap": {
                "1": "40000",
                "2": "40000",
                "3": "40000",
                "4": "40000",
                "5": "60000",
                "6": "40000",
                "7": "40000",
                "8": "40000",
                "9": "20000",
                "10": "10000",
                "11": "40000",
                "12": "30000",
                "13": "40000",
                "14": "10000",
                "15": "50000"
            },
            "belongsIndusMap": {
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
            "relRelationMap": {
                "1": "09",
                "2": "01",
                "3": "02",
                "4": "03",
                "5": "08",
                "6": "05",
                "9": "99"
            },
            "purposeMap": {
                "1": "FLI",
                "2": "EDU",
                "3": "RENT",
                "4": "SJSM",
                "5": "TRA",
                "6": "JKYL",
                "7": "OTH",
                "8": "OTH",
                "9": "OTH"
            },
            "creditApplyUploadMap": {
                "1": {
                    "type": "ATTACHMENT",
                    "imageName": "idCardFront",
                    "imageCode": "1"
                },
                "2": {
                    "type": "ATTACHMENT",
                    "imageName": "idCardBack",
                    "imageCode": "2"
                },
                "29": {
                    "type": "ATTACHMENT",
                    "imageName": "faceRecognition",
                    "imageCode": "3"
                },
                "34200": {
                    "type": "CONTRACT",
                    "imageName": "credit-mix-protocol",
                    "imageCode": "21"
                },
                "34202": {
                    "type": "CONTRACT",
                    "imageName": "non-students-declaration",
                    "imageCode": "74"
                },
                "34201": {
                    "type": "CONTRACT",
                    "imageName": "debet-purpose-declaration",
                    "imageCode": "75"
                }
            },
            "loanApplyUploadMap": {
                "34203": {
                    "type": "CONTRACT",
                    "imageName": "digitalCertifacen",
                    "imageCode": "29"
                },
                "34204": {
                    "type": "CONTRACT",
                    "imageName": "withdrawProtocal",
                    "imageCode": "11"
                }
            },
            "contractDownloadMap": {
                "28": {
                    "type": "CONTRACT",
                    "imageName": "changyinContract",
                    "imageCode": "7"
                },
                "34205": {
                    "type": "CONTRACT",
                    "imageName": "guaranteeContract",
                    "imageCode": "10"
                }
            }
        }
    return gc.NACOS.update_configs("grant%s" % gc.ENV, "gbiz_capital_changyin_mingdonghua_rl_const", body)