#!/usr/bin/python
# -*- coding: UTF-8 -*-
request_log_check_point = {
    "tongrongqianjingjing": {
        "LoanApplyNew": [
            {
                "api": "/tongrong/tongrongqianjingjing/loanApply",
                "check_points": [
                    {
                        "$.orderId": "asset_info['data']['asset']['item_no']",
                        "$.userBasicInfo.idNo": "asset_info['data']['borrower']['idnum_encrypt']",
                        "$.loanOrder.account": "'{:.2f}'.format(asset_info['data']['asset']['amount'])",
                        "$.loanOrder.termNo": "str(asset_info['data']['asset']['period_count'])",
                    }
                ]
            }
        ],
        "LoanApplyQuery": [
            {
                "api": "/tongrong/tongrongqianjingjing/loanApplyQuery",
                "check_points": [
                    {
                        "$.orderId": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "PaymentWithdraw": [
            {
                "api": "/withdraw/balance",
                "check_points": [
                    {
                        "$.account": "qsq_cpcn_tra_quick",
                    }
                ]
            },
            {
                "api": "/withdraw/autoWithdraw",
                "check_points": [
                    {
                        "$.merchant_key": "asset_info['data']['asset']['item_no']+'w'",
                        "$.amount": "asset_info['data']['asset']['amount']*100",
                        "$.receiver_type": 1,
                        "$.account": "qsq_cpcn_tra_quick",
                        "$.sign_company": "tra",
                        "$.receiver_name_encrypt": "asset_info['data']['receive_card']['account_name_encrypt']",
                        "$.receiver_account_encrypt": "asset_info['data']['receive_card']['num_encrypt']",
                        "$.receiver_identity_encrypt": "asset_info['data']['receive_card']['owner_id_encrypt']",
                    }
                ]
            }
        ],
        "PaymentWithdrawQuery": [
            {
                "api": "/withdraw/query",
                "check_points": [
                    {
                        "$.merchant_key": "asset_info['data']['asset']['item_no']+'w'",
                    }
                ]
            }
        ],
        "ContractDown": [
            {
                "api": "/tongrong/tongrongqianjingjing/loanApplyQuery",
                "check_points": [
                    {
                        "$.orderId": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "PaymentTransfer": [
            {
                "api": "/withdraw/balance",
                "check_points": [
                    {
                        "$.account": "qsq_cpcn_qjja_quick",
                    }
                ]
            },
            {
                "api": "/withdraw/autoWithdraw",
                "check_points": [
                    {
                        "$.merchant_key": "asset_info['data']['asset']['item_no']+'t'",
                        "$.amount": "asset_info['data']['asset']['amount']*100",
                        "$.receiver_type": 3,
                        "$.account": "qsq_cpcn_qjja_quick",
                        "$.sign_company": "qjja",
                        "$.receiver_name_encrypt": "enc_04_2755506557550069760_659",
                        "$.receiver_account_encrypt": "enc_03_3261214282402498560_335",
                        "$.receiver_identity_encrypt": "enc_02_3261216200759707648_479",
                        "$.receiver_bank_code": "CMBC"
                    }
                ]
            }
        ],
        "PaymentTransferQuery": [
            {
                "api": "/withdraw/query",
                "check_points": [
                    {
                        "$.merchant_key": "asset_info['data']['asset']['item_no']+'t'",
                    }
                ]
            }
        ],
        "BondContractSign": [
            {
                "api": "/tongrong/tongrongqianjingjing/bondTransfer",
                "check_points": [
                    {
                        "$.orderId": "asset_info['data']['asset']['item_no']",
                        "$.contractInfo.contractId": "'bondId_'+asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "BondContractDown": [
            {
                "api": "/tongrong/tongrongqianjingjing/loanApplyQuery",
                "check_points": [
                    {
                        "$.orderId": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
    },
    "haohanqianjingjing": {
        "LoanApplyNew": [],
        "LoanApplyQuery": [],
        "PaymentWithdraw": [
            {
                "api": "/withdraw/balance",
                "check_points": [
                    {
                        "$.account": "qsq_sumpay_tq_protocol",
                    }
                ]
            },
            {
                "api": "/withdraw/autoWithdraw",
                "check_points": [
                    {
                        "$.merchant_key": "asset_info['data']['asset']['item_no']+'w'",
                        "$.amount": "asset_info['data']['asset']['amount']*100",
                        "$.receiver_type": 1,
                        "$.account": "qsq_sumpay_tq_protocol",
                        "$.sign_company": "tq",
                        "$.receiver_name_encrypt": "asset_info['data']['receive_card']['account_name_encrypt']",
                        "$.receiver_account_encrypt": "asset_info['data']['receive_card']['num_encrypt']",
                        "$.receiver_identity_encrypt": "asset_info['data']['receive_card']['owner_id_encrypt']",
                    }
                ]
            }
        ],
        "PaymentWithdrawQuery": [
            {
                "api": "/withdraw/query",
                "check_points": [
                    {
                        "$.merchant_key": "asset_info['data']['asset']['item_no']+'w'",
                    }
                ]
            }
        ],
        "PaymentTransfer": [
            {
                "api": "/withdraw/balance",
                "check_points": [
                    {
                        "$.account": "qsq_sumpay_qjj_protocol",
                    }
                ]
            },
            {
                "api": "/withdraw/autoWithdraw",
                "check_points": [
                    {
                        "$.merchant_key": "asset_info['data']['asset']['item_no']+'t'",
                        "$.amount": "asset_info['data']['asset']['amount']*100",
                        "$.receiver_type": 3,
                        "$.account": "qsq_sumpay_qjj_protocol",
                        "$.sign_company": "qjj",
                        "$.receiver_name_encrypt": "enc_04_2755506557550069760_659",
                        "$.receiver_account_encrypt": "enc_03_3370357756397094912_403",
                        "$.receiver_identity_encrypt": "enc_02_2580379904328075267_458",
                        "$.receiver_bank_code": "ICBC"
                    }
                ]
            }
        ],
        "PaymentTransferQuery": [
            {
                "api": "/withdraw/query",
                "check_points": [
                    {
                        "$.merchant_key": "asset_info['data']['asset']['item_no']+'t'",
                    }
                ]
            }
        ],
    },
    "qinnong": {
        "LoanPreApply": [
            {
                "api": "/capital/ftp/upload/qinnong",
                "check_points": []
            }
        ],
        "LoanApplyNew": [
            {
                "api": "/qinnong/std/loan/apply",
                "check_points": [
                    {
                        "$.asset.loan_amount": "asset_info['data']['asset']['amount']*100",
                        "$.asset.loan_order_no": "asset_info['data']['asset']['item_no']",
                        "$.asset.period_count": "int(asset_info['data']['asset']['period_count'])",
                        "$.asset.guarantee_company": "kn_tianbang",
                    }
                ]
            }
        ],
        "LoanApplyQuery": [
            {
                "api": "/qinnong/std/loan/query",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "LoanApplyTrial": [],
        "GuaranteeApply": [
            {
                "api": "/tianbang/sign/request",
                "check_points": [
                    {
                        "$.loanInfo.orderNo": "asset_info['data']['asset']['item_no']",
                        "$.loanInfo.loanAmt": "asset_info['data']['asset']['amount']",
                        "$.loanInfo.loanContractNo": "'KN'+asset_info['data']['asset']['item_no']",
                        "$.contractItems[0].contractType": "57",
                    }
                ]
            }
        ],
        "GuaranteeDown": [
            {
                "api": "/tianbang/sign/get",
                "check_points": [
                    {
                        "$.orderNo": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "LoanPostApply": [
            {
                "api": "/capital/ftp/upload/qinnong",
                "check_points": []
            }
        ],
        "LoanApplyConfirm": [
            {
                "api": "/qinnong/std/loan/grant",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                        "$.loan_amount": "asset_info['data']['asset']['amount']*100",
                        "$.action": "withdraw",
                    }
                ]
            }
        ],
        "LoanConfirmQuery": [
            {
                "api": "/qinnong/std/loan/query",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "CapitalRepayPlanQuery": [
            {
                "api": "/qinnong/std/repayment/repay-plan",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "GuaranteeStatusSync": [
            {
                "api": "/tianbang/loan/status",
                "check_points": [
                    {
                        "$.orderNo": "asset_info['data']['asset']['item_no']",
                        "$.loanStatus": 0,
                    }
                ]
            }
        ],
    },
    "qinnong_jieyi": {
        "LoanPreApply": [
            {
                "api": "/capital/ftp/upload/qinnong",
                "check_points": []
            }
        ],
        "LoanApplyNew": [
            {
                "api": "/qinnong/std/loan/apply",
                "check_points": [
                    {
                        "$.asset.loan_amount": "asset_info['data']['asset']['amount']*100",
                        "$.asset.loan_order_no": "asset_info['data']['asset']['item_no']",
                        "$.asset.period_count": "int(asset_info['data']['asset']['period_count'])",
                        "$.asset.guarantee_company": "kn_jieyi",
                    }
                ]
            }
        ],
        "LoanApplyQuery": [
            {
                "api": "/qinnong/std/loan/query",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "LoanApplyTrial": [],
        "LoanPostApply": [
            {
                "api": "/capital/ftp/upload/qinnong",
                "check_points": []
            }
        ],
        "LoanApplyConfirm": [
            {
                "api": "/qinnong/std/loan/grant",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                        "$.loan_amount": "asset_info['data']['asset']['amount']*100",
                        "$.action": "withdraw",
                    }
                ]
            }
        ],
        "LoanConfirmQuery": [
            {
                "api": "/qinnong/std/loan/query",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "CapitalRepayPlanQuery": [
            {
                "api": "/qinnong/std/repayment/repay-plan",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ]
    },
    "qinnong_dingfeng": {
        "LoanPreApply": [
            {
                "api": "/capital/ftp/upload/qinnong",
                "check_points": []
            }
        ],
        "LoanApplyNew": [
            {
                "api": "/qinnong/std/loan/apply",
                "check_points": [
                    {
                        "$.asset.loan_amount": "asset_info['data']['asset']['amount']*100",
                        "$.asset.loan_order_no": "asset_info['data']['asset']['item_no']",
                        "$.asset.period_count": "int(asset_info['data']['asset']['period_count'])",
                        "$.asset.guarantee_company": "kn_dingfeng",
                    }
                ]
            }
        ],
        "LoanApplyQuery": [
            {
                "api": "/qinnong/std/loan/query",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "LoanApplyTrial": [],
        "LoanPostApply": [
            {
                "api": "/capital/ftp/upload/qinnong",
                "check_points": []
            }
        ],
        "LoanApplyConfirm": [
            {
                "api": "/qinnong/std/loan/grant",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                        "$.loan_amount": "asset_info['data']['asset']['amount']*100",
                        "$.action": "withdraw",
                    }
                ]
            }
        ],
        "LoanConfirmQuery": [
            {
                "api": "/qinnong/std/loan/query",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "CapitalRepayPlanQuery": [
            {
                "api": "/qinnong/std/repayment/repay-plan",
                "check_points": [
                    {
                        "$.loan_order_no": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ]
    },
    "zhongke_lanzhou": {
        "LoanApplyTrial": [
            # 这一步有问题，jaeger日志缺少root-span查不到日志（开发在看原因），先不设置检查点
            {
                "api": "/lanzhou/loanRateQuery",
                "check_points": [
                    # {
                    #     "$.productid": "KN-DEBX-ZKBC"
                    # }
                ]
            }
        ],
        "LoanPreApply": [
            {
                "api": "/capital/ftp/upload/lanzhou",
                "check_points": []
            },
            {
                "api": "/lanzhou/fileNotice",
                "check_points": []
            }
        ],
        "LoanApplyNew": [
            {
                "api": "/lanzhou/customerInfoPush",
                "check_points": [
                    {
                        "$.channelserialno": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "LoanApplyQuery": [
            {
                "api": "/lanzhou/cusFaceQuery",
                "check_points": [
                    {
                        "$.channelserialno": "asset_info['data']['asset']['item_no']",
                        "$.type": "C",
                    }
                ]
            }
        ],
        "LoanCreditApply": [
            {
                "api": "/lanzhou/faceRecognition",
                "check_points": [
                    {
                        "$.channelserialno": "asset_info['data']['asset']['item_no']",
                        "$.cusInfoSerialNo": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "LoanCreditQuery": [
            {
                "api": "/lanzhou/cusFaceQuery",
                "check_points": [
                    {
                        "$.channelserialno": "asset_info['data']['asset']['item_no']",
                        "$.type": "F",
                    }
                ]
            }
        ],
        "ContractPush": [
            {
                "api": "/capital/ftp/upload/lanzhou",
                "check_points": []
            },
            {
                "api": "/lanzhou/fileNotice",
                "check_points": []
            },
        ],
        "LoanApplyConfirm": [
            {
                "api": "/lanzhou/loanApply",
                "check_points": [
                    {
                        "$.channelserialno": "asset_info['data']['asset']['item_no']",
                        "$.merserno": "asset_info['data']['asset']['item_no']",
                        "$.appamt": "asset_info['data']['asset']['amount']",
                        "$.appterm": "str(asset_info['data']['asset']['period_count'])",
                    }
                ]
            }
        ],
        "LoanConfirmQuery": [
            {
                "api": "/lanzhou/loanQuery",
                "check_points": [
                    {
                        "$.merserno": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "CapitalRepayPlanQuery": [
            {
                "api": "/lanzhou/repaymentPlanQuery",
                "check_points": [
                    {
                        "$.merserno": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
    },
    "weishenma_daxinganling": {
        "LoanApplyNew": [
            {
                "api": "/weishenma_daxinganling/v2/pre-loan/loanApply",
                "check_points": [
                    {
                        "$.shddh": "asset_info['data']['asset']['item_no']",
                        "$.sqje": "asset_info['data']['asset']['amount']*100",
                        "$.qx": "asset_info['data']['asset']['period_count']",
                    }
                ]
            }
        ],
        "LoanApplyQuery": [
            {
                "api": "/weishenma_daxinganling/v2/pre-loan/loanApplyQuery",
                "check_points": [
                    {
                        "$.data[0]": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        # 用的LoanApplyQuery缓存，不会再调用资方
        "CapitalRepayPlanQuery": [],
        "CapitalRepayPlanPush": [
            {
                "api": "/weishenma_daxinganling/v2/pre-loan/repayPlanUpdate",
                "check_points": [
                    # {
                        # "$.shddh": "asset_info['data']['asset']['item_no']",
                    # }
                ]
            },
            {
                "api": "/weishenma_daxinganling/v2/post-loan/plan",
                "check_points": [
                    {
                        "$[0].orderId": "asset_info['data']['asset']['item_no']",
                        "$[0].dataId": "asset_info['data']['asset']['item_no']",
                        "$[0].totalTerm": "asset_info['data']['asset']['period_count']",
                        "$[0].orderDate": "asset_info['data']['asset']['grant_at'][:10]",
                        "$[0].annualInterestRate": 36,
                    }
                ]
            }
        ],
        "ContractDown": [],
    },
    "hami_tianshan_tianbang": {
        "LoanApplyNew": [
            {
                "api": "/hamitianshan/A002",
                "check_points": [
                    {
                        "$.outTraceNo": "asset_info['data']['asset']['item_no']",
                        "$.name": "asset_info['data']['borrower']['name_encrypt']",
                    }
                ]
            }
        ],
        "LoanApplyQuery": [
            {
                "api": "/hamitianshan/A003",
                "check_points": [
                    {
                        "$.outTraceNo": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "LoanPostApply": [
            {
                "api": "/hamitianshan/A014",
                "check_points": [
                    {
                        "$.outTraceNo": "asset_info['data']['asset']['item_no']",
                        "$.type": 1,
                    }
                ]
            }
        ],
        "ContractDown": [
            {
                "api": "/contract/upload-zip",
                "check_points": []
            }
        ],
        "LoanApplyConfirm": [
            {
                "api": "/hamitianshan/A004",
                "check_points": [
                    {
                        "$.outTraceNo": "asset_info['data']['asset']['item_no']",
                        "$.policyType": 3,
                    }
                ]
            }
        ],
        "LoanConfirmQuery": [
            {
                "api": "/hamitianshan/A005",
                "check_points": [
                    {
                        "$.outTraceNo": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
        "CapitalRepayPlanQuery": [
            {
                "api": "/hamitianshan/A005",
                "check_points": [
                    {
                        "$.outTraceNo": "asset_info['data']['asset']['item_no']",
                    }
                ]
            }
        ],
    },
    "zhongke_hegang": {
        "LoanPreApply": [
            {
                "api": "/capital/ftp/upload/hegang",
                "check_points": []
            }
        ],
        "LoanApplyNew": [
            {
                "api": "/hegang/creditApply",
                "check_points": [
                    {
                        "$.productCode": "KN0-CL-DEBX-S",
                        "$.hzfSerialNo": "('KN0-CL'+asset_info['data']['asset']['item_no']).ljust(39, '0')+'A'",
                        "$.applyAmt": "asset_info['data']['asset']['amount']",
                        "$.applyTerm": "asset_info['data']['asset']['period_count']",
                    }
                ]
            }
        ],
        "LoanApplyQuery": [
            {
                "api": "/hegang/creditQuery",
                "check_points": [
                    {
                        "$.hzfSerialNo": "('KN0-CL'+asset_info['data']['asset']['item_no']).ljust(39, '0')+'A'",
                    }
                ]
            }
        ],
        "LoanPostApply": [
            {
                "api": "/capital/ftp/upload/hegang",
                "check_points": []
            }
        ],
        "LoanApplyConfirm": [
            {
                "api": "/hegang/useApply",
                "check_points": [
                    {
                        "$.loanSerialNo": "('KN0-CL'+asset_info['data']['asset']['item_no']).ljust(39, '0')+'B'",
                        "$.hzfSerialNo": "('KN0-CL'+asset_info['data']['asset']['item_no']).ljust(39, '0')+'A'",
                        "$.amount": "asset_info['data']['asset']['amount']",
                        "$.applyTerm": "asset_info['data']['asset']['period_count']",
                    }
                ]
            }
        ],
        "LoanConfirmQuery": [
            {
                "api": "/hegang/loanQuery",
                "check_points": [
                    {
                        "$.loanSerialNo": "('KN0-CL'+asset_info['data']['asset']['item_no']).ljust(39, '0')+'B'",
                    }
                ]
            }
        ],
        "CapitalRepayPlanQuery": [
            {
                "api": "/hegang/repayPlanQuery",
                "check_points": [
                    {
                        "$.loanSerialNo": "('KN0-CL'+asset_info['data']['asset']['item_no']).ljust(39, '0')+'B'",
                    }
                ]
            }
        ],
        "ContractDown": [
            # 拼接gate-url给合同
            {
                "api": "/contract/upload-zip",
                "check_points": []
            }
        ],
        "ContractPush": [
            {
                "api": "/capital/ftp/upload/hegang",
                "check_points": []
            },
            {
                "api": "/hegang/channelSyncNotice",
                "check_points": [
                    {
                        "$.serialNo": "('KN0-CL'+asset_info['data']['asset']['item_no']).ljust(39, '0')+'B'",
                    },
                    {
                        "$.serialNo": "('KN0-CL'+asset_info['data']['asset']['item_no']).ljust(39, '0')+'B'",
                    }
                ]
            }
        ],
    },
    "yilian_dingfeng": {
        "LoanApplyNew": [
            {
                "api": "/qingjia/yilian_dingfeng/loanBaseInfoPush",
                "check_points": [
                    {
                        "$.idno": "asset_info['data']['borrower']['idnum_encrypt']",
                    }
                ]
            }
        ],
        "LoanCreditApply": [
            {
                "api": "/qingjia/yilian_dingfeng/route",
                "check_points": [
                    {
                        "$.contractno": "asset_info['data']['asset']['item_no']+'ED'",
                        "$.applyamt": "'{:.2f}'.format(asset_info['data']['asset']['amount'])",
                        "$.applyterm": "str(asset_info['data']['asset']['period_count'])",
                    }
                ]
            }
        ],
        "LoanApplyConfirm": [
            {
                "api": "/qingjia/yilian_dingfeng/loanApply",
                "check_points": [
                    {
                        "$.contractno": "asset_info['data']['asset']['item_no']",
                        "$.appamt": "asset_info['data']['asset']['amount']",
                        "$.appterm": "str(asset_info['data']['asset']['period_count'])",
                    }
                ]
            }
        ],
    },
}
