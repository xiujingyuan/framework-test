#!/usr/bin/python
# -*- coding: UTF-8 -*-
rbiz_request_log_check_point = {
    "zhongke_hegang": {
        "execute_combine_withhold": [
            {
                "api": "/withhold/autoPay",
                "check_points": [
                    {
                        "$.merchant_key": "withhold_info[0]['withhold_serial_no']",
                        "$.amount": "withhold_info[0]['withhold_amount']",
                        "$.sign_company": "zhongrong",
                        "$.ledgers": "{\n  \"zhongrong-wd\" : 10625,\n  \"zhongrong-hg1\" : 69111,\n  \"zhongrong-zr\" : 634\n}",
                    }
                ]
            }
        ],
    },
    "zhongke_hegang_advance_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/hegang/repayTrialQuery/KN1-CL-HLJ",
                "check_points": [
                    {
                        "$.querySerialNo": "withhold_info[0]['withhold_third_serial_no']",
                    }
                ]
            },
            {
                "api": "/withhold/autoPay",
                "check_points": [
                    {
                        "$.merchant_key": "withhold_info[0]['withhold_serial_no']",
                        "$.amount": "withhold_info[0]['withhold_amount']",
                        "$.sign_company": "zhongrong",
                        "$.ledgers": "{\n  \"zhongrong-wd\" : 10625,\n  \"zhongrong-hg1\" : 801000,\n  \"zhongrong-zr\" : 634\n}",
                    }
                ]
            }
        ],
    },
    "yilian_dingfeng": {
        "execute_combine_withhold": [
            {
                "api": "/withhold/autoPay",
                "check_points": [
                    {
                        "$.merchant_key": "withhold_info[0]['withhold_serial_no']",
                        "$.amount": "withhold_info[0]['withhold_amount']",
                        "$.sign_company": "dingfeng",
                        "$.ledgers": "{\n  \"dingfeng-df\" : 2926,\n  \"dingfeng-yl\" : 34888\n}",
                    }
                ]
            }
        ],
    },
    "yilian_dingfeng_advance_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/withhold/autoPay",
                "check_points": [
                    {
                        "$.merchant_key": "withhold_info[0]['withhold_serial_no']",
                        "$.amount": "withhold_info[0]['withhold_amount']",
                        "$.sign_company": "dingfeng",
                        "$.ledgers": "{\n  \"dingfeng-df\" : 2926,\n  \"dingfeng-yl\" : 401000\n}",
                    }
                ]
            }
        ],
    },
    "jinmeixin_daqin": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_daqin/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "DO",
                        "$.repayTerm[0]": 1,
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_daqin_last_period": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_daqin/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "DO",
                        "$.repayTerm[0]": 12,
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_daqin_pre_last_period": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_daqin/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "PRE",
                        "$.repayTerm[0]": 12,
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_daqin_advance_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_daqin/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "PRE",
                        "$.repayTerm": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12
                        ],
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_daqin_part_normal": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_daqin/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "DO",
                        "$.repayTerm[0]": 1,
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100+27.2",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_daqin_advance_part_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_daqin/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "PRE",
                        "$.repayTerm": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12
                        ],
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100+27.2",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "weipin_zhongwei": {
        "execute_combine_withhold": [
            {
                "api": "/zhongzhirong/weipin_zhongwei/repay.apl",
                "check_points": [
                    {
                        "$.repaymentAppNo": "withhold_info[0]['withhold_serial_no']",
                        "$.productCode": "kn_wp_dd",
                        "$.repaymentAmount": "withhold_info[0]['withhold_amount']/100",
                        "$.customerGroup": "06",
                        "$.repaymentType": "01",
                        "$.repaymentCategory": "01",
                        "$.tenor": 1,
                        "$.bankNo": "withhold_info[0]['withhold_card_num']",
                        "$.openId": "'KN_'+withhold_info[0]['withhold_user_idnum']",
                    }
                ]
            }
        ],
    },
    "weipin_zhongwei_advance_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/zhongzhirong/weipin_zhongwei/repay.apl",
                "check_points": [
                    {
                        "$.repaymentAppNo": "withhold_info[0]['withhold_serial_no']",
                        "$.productCode": "kn_wp_dd",
                        "$.repaymentAmount": "withhold_info[0]['withhold_amount']/100",
                        "$.customerGroup": "06",
                        "$.repaymentType": "01",
                        "$.repaymentCategory": "03",
                        "$.tenor": 1,
                        "$.bankNo": "withhold_info[0]['withhold_card_num']",
                        "$.openId": "'KN_'+withhold_info[0]['withhold_user_idnum']",
                    }
                ]
            }
        ],
    },
    "lanzhou_haoyue_qinjia": {
        "execute_combine_withhold": [
            {
                "api": "/withhold/autoPay",
                "check_points": [
                    {
                        "$.merchant_key": "withhold_info[0]['withhold_serial_no']",
                        "$.amount": "withhold_info[0]['withhold_amount']",
                        "$.sign_company": "qjhy",
                        "$.ledgers": "{\n  \"qjhy-lz\" : 34648,\n  \"qjhy-hy\" : 3174\n}",
                    }
                ]
            }
        ],
    },
    "lanzhou_haoyue_qinjia_advance_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/withhold/autoPay",
                "check_points": [
                    {
                        "$.merchant_key": "withhold_info[0]['withhold_serial_no']",
                        "$.amount": "withhold_info[0]['withhold_amount']",
                        "$.sign_company": "qjhy",
                        "$.ledgers": "{\n  \"qjhy-lz\" : 401000,\n  \"qjhy-hy\" : 3174\n}",
                    }
                ]
            }
        ],
    },
    "yumin_zhongbao": {
        "execute_combine_withhold": [
            {
                "api": "/zhongzhirong/yumin_zhongbao/ym.repay.apply",
                "check_points": [
                    {
                        "$.openId": "'KN_'+withhold_info[0]['withhold_user_idnum']",
                        "$.paySeqNo": "withhold_info[0]['withhold_channel_key']",
                        "$.productCode": "kn_ym_dd",
                        "$.totalAmount": "withhold_info[0]['withhold_amount']",
                        "$.repaymentMethod": "CARD",
                        "$.repaymentMode": "RAM",
                        "$.principal": 24118,
                        "$.interest": 1952,
                        "$.guaranteeAmount": 2296,
                        "$.compoundInterest": 0,
                        "$.penaltyInterest": 0,
                    }
                ]
            }
        ],
    },
    "yumin_zhongbao_advance_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/zhongzhirong/yumin_zhongbao/ym.repay.apply",
                "check_points": [
                    {
                        "$.openId": "'KN_'+withhold_info[0]['withhold_user_idnum']",
                        "$.paySeqNo": "withhold_info[0]['withhold_channel_key']",
                        "$.productCode": "kn_ym_dd",
                        "$.totalAmount": "withhold_info[0]['withhold_amount']",
                        "$.repaymentMethod": "CARD",
                        "$.repaymentMode": "ES",
                        "$.principal": 300000,
                        "$.interest": 1000,
                        "$.compoundInterest": 0,
                        "$.penaltyInterest": 0,
                    }
                ]
            }
        ],
    },
    "yixin_rongsheng": {
        "execute_combine_withhold": [
            {
                "api": "/yixin/yixin_rongsheng/repay.do",
                "check_points": [
                    {
                        "$.userId": "'KN_'+withhold_info[0]['withhold_user_idnum']",
                        "$.transNo": "withhold_info[0]['withhold_serial_no']",
                        "$.repayAmount": "withhold_info[0]['withhold_amount']",
                        "$.repayType": "DO",
                        "$.cardNo": "withhold_info[0]['withhold_card_num']",
                        "$.periods": "1",
                    }
                ]
            }
        ],
    },
    "yixin_rongsheng_advance_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/yixin/yixin_rongsheng/repay.do",
                "check_points": [
                    {
                        "$.userId": "'KN_'+withhold_info[0]['withhold_user_idnum']",
                        "$.transNo": "withhold_info[0]['withhold_serial_no']",
                        "$.repayAmount": "withhold_info[0]['withhold_amount']",
                        "$.repayType": "PRE",
                        "$.cardNo": "withhold_info[0]['withhold_card_num']",
                        "$.periods": "1,2,3,4,5,6",

                    }
                ]
            }
        ],
    },
    "zhongyuan_zunhao": {
        "execute_combine_withhold": [
            {
                "api": "/zhongzhirong/zhongyuan_zunhao/repay",
                "check_points": [
                    {
                        "$.openId": "'KN_'+withhold_info[0]['withhold_user_idnum']",
                        "$.productCode": "kn_zy_dd",
                        "$.settlTyp": "05",
                        "$.cooppfApplCde": "'691001_'+withhold_info[0]['withhold_serial_no']",
                        # 这个金额不是代扣金额
                        "$.amt": 61054,
                        "$.repaymentSign": "N",
                        "$.hkCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.hkMobileNo": "withhold_info[0]['withhold_user_phone']",
                        "$.listLmLoan[0].psPerdNo": "1",
                        "$.listSubDetail[0].subType": "2",
                        "$.listSubDetail[0].subAmt": 5070,
                    }
                ]
            }
        ],
    },
    "zhongyuan_zunhao_advance_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/zhongzhirong/zhongyuan_zunhao/repay",
                "check_points": [
                    {
                        "$.openId": "'KN_'+withhold_info[0]['withhold_user_idnum']",
                        "$.productCode": "kn_zy_dd",
                        "$.settlTyp": "04",
                        "$.cooppfApplCde": "'691001_'+withhold_info[0]['withhold_serial_no']",
                        "$.repaymentSign": "N",
                        "$.hkCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.hkMobileNo": "withhold_info[0]['withhold_user_phone']",
                        "$.listLmLoan[0].psPerdNo": "1,2,3,4,5,6,7,8,9,10,11,12",
                        "$.listSubDetail[0].subType": "2",
                        "$.listSubDetail[0].subAmt": 1810,
                    }
                ]
            }
        ],
    },
    # 金美信汉辰
    "jinmeixin_hanchen": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_hanchen/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "DO",
                        "$.repayTerm[0]": 1,
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_hanchen_last_period": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_hanchen/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "DO",
                        "$.repayTerm[0]": 12,
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_hanchen_pre_last_period": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_hanchen/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "PRE",
                        "$.repayTerm[0]": 12,
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_hanchen_advance_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_hanchen/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "PRE",
                        "$.repayTerm": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12
                        ],
                        "$.repayAmt": "withhold_info[0]['withhold_amount']/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_hanchen_part_normal": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_hanchen/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "DO",
                        "$.repayTerm[0]": 1,
                        "$.repayAmt": "(withhold_info[0]['withhold_amount']+374)/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },
    "jinmeixin_hanchen_advance_part_payoff": {
        "execute_combine_withhold": [
            {
                "api": "/chongtian/jinmeixin_hanchen/repay/request",
                "check_points": [
                    {
                        "$.orderId": "withhold_info[0]['withhold_serial_no']",
                        "$.repayType": "PRE",
                        "$.repayTerm": [
                            1,
                            2,
                            3,
                            4,
                            5,
                            6,
                            7,
                            8,
                            9,
                            10,
                            11,
                            12
                        ],
                        "$.repayAmt": "(withhold_info[0]['withhold_amount']+374)/100",
                        "$.mobile": "withhold_info[0]['withhold_user_phone']",
                        "$.name": "withhold_info[0]['withhold_user_name']",
                        "$.idnum": "withhold_info[0]['withhold_user_idnum']",
                        "$.bankCardNo": "withhold_info[0]['withhold_card_num']",
                        "$.bankName": "建设银行",
                        "$.bankCode": "CCB",
                        "$.repayPen": 0,
                    }
                ]
            }
        ],
    },

}
