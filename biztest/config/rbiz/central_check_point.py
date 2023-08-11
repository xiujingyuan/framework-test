#!/usr/bin/python
# -*- coding: UTF-8 -*-
central_request_log_check_point = {
    "zhongke_hegang": {
        "ZhongkeHegangCapitalPush": [
            {
                "api": "/hegang/repayQuery/KN1-CL-HLJ",
                "check_points": [
                    {
                        "$.tradeNo": "capital_notify_info['heGangRepayApplyReqDto']['tradeNo']",
                        "$.loanSerialNo": "capital_notify_info['heGangRepayApplyReqDto']['loanSerialNo']",
                    }
                ]
            },
            {
                "api": "/hegang/repayApply/KN1-CL-HLJ",
                "check_points": [
                    {
                        "$.tradeNo": "capital_notify_info['heGangRepayApplyReqDto']['tradeNo']",
                        "$.loanSerialNo": "capital_notify_info['heGangRepayApplyReqDto']['loanSerialNo']",
                        "$.payWay": "capital_notify_info['heGangRepayApplyReqDto']['payWay']",
                        "$.payType": "capital_notify_info['heGangRepayApplyReqDto']['payType']",
                        "$.loanNo": "capital_notify_info['heGangRepayApplyReqDto']['loanNo']",
                        "$.tradeAmt": "capital_notify_info['heGangRepayApplyReqDto']['tradeAmt']",
                        "$.tradeCapital": "capital_notify_info['heGangRepayApplyReqDto']['tradeCapital']",
                        "$.tradeInt": "capital_notify_info['heGangRepayApplyReqDto']['tradeInt']",
                        "$.tradeTermNo": "capital_notify_info['heGangRepayApplyReqDto']['tradeTermNo']",
                    }
                ]
            }
        ],
    },
    "zhongke_hegang_advance_payoff": {
        "ZhongkeHegangCapitalPush": [
            {
                "api": "/hegang/repayQuery/KN1-CL-HLJ",
                "check_points": [
                    {
                        "$.tradeNo": "capital_notify_info['heGangRepayApplyReqDto']['tradeNo']",
                        "$.loanSerialNo": "capital_notify_info['heGangRepayApplyReqDto']['loanSerialNo']",
                    }
                ]
            },
            {
                "api": "/hegang/repayApply/KN1-CL-HLJ",
                "check_points": [
                    {
                        "$.tradeNo": "capital_notify_info['heGangRepayApplyReqDto']['tradeNo']",
                        "$.loanSerialNo": "capital_notify_info['heGangRepayApplyReqDto']['loanSerialNo']",
                        "$.payWay": "capital_notify_info['heGangRepayApplyReqDto']['payWay']",
                        "$.payType": "capital_notify_info['heGangRepayApplyReqDto']['payType']",
                        "$.loanNo": "capital_notify_info['heGangRepayApplyReqDto']['loanNo']",
                        "$.tradeAmt": "capital_notify_info['heGangRepayApplyReqDto']['tradeAmt']",
                        "$.tradeCapital": "capital_notify_info['heGangRepayApplyReqDto']['tradeCapital']",
                        "$.tradeInt": "capital_notify_info['heGangRepayApplyReqDto']['tradeInt']",
                        "$.tradeTermNo": "capital_notify_info['heGangRepayApplyReqDto']['tradeTermNo']",
                    }
                ]
            }
        ],
    },
    "yilian_dingfeng": {
        "YilianDingfengCapitalPush": [
            {
                "api": "/qingjia/yilian_dingfeng/normalRepayNotice",
                "check_points": [
                    {
                        "$.bizid": "capital_notify_info['bizid']",
                        "$.repaytype": "capital_notify_info['repaytype']",
                        "$.deducttype": "capital_notify_info['deducttype']",
                        "$.loanno": "capital_notify_info['loanno']",
                        "$.detaillist[0].period": "capital_notify_info['detaillist'][0]['period']",
                        "$.detaillist[0].repaytime": "capital_notify_info['detaillist'][0]['repaytime']",
                        "$.detaillist[0].indeedtotal": "capital_notify_info['detaillist'][0]['indeedtotal']",
                        "$.detaillist[0].indeedcapital": "capital_notify_info['detaillist'][0]['indeedcapital']",
                        "$.detaillist[0].indeedinterest": "capital_notify_info['detaillist'][0]['indeedinterest']",
                        "$.detaillist[0].indeedservicefee": "capital_notify_info['detaillist'][0]['indeedservicefee']",
                    }
                ]
            }
        ],
    },
    "yilian_dingfeng_advance_payoff": {
        "YilianDingfengCapitalPush": [
            {
                "api": "/qingjia/yilian_dingfeng/repayTrial",
                "check_points": [
                    {
                        "$.loanno": "capital_notify_info['loanno']",
                        "$.beginnum": "1",
                        "$.calctype": "3",
                    }
                ]
            },
            {
                "api": "/qingjia/yilian_dingfeng/settleRepayNotice",
                "check_points": [
                    {
                        "$.bizid": "capital_notify_info['bizid']",
                        "$.deducttype": "capital_notify_info['deducttype']",
                        "$.loanno": "capital_notify_info['loanno']",
                        "$.detaillist[0].period": "capital_notify_info['detaillist'][0]['period']",
                        "$.detaillist[0].repaytime": "capital_notify_info['detaillist'][0]['repaytime']",
                        "$.detaillist[0].indeedtotal": "capital_notify_info['detaillist'][0]['indeedtotal']",
                        "$.detaillist[0].indeedcapital": "capital_notify_info['detaillist'][0]['indeedcapital']",
                        "$.detaillist[0].indeedinterest": "capital_notify_info['detaillist'][0]['indeedinterest']",
                        "$.detaillist[0].indeedservicefee": "capital_notify_info['detaillist'][0]['indeedservicefee']",
                    }
                ]
            }
        ],
    },
    # 金美信大秦不通知资方
    "jinmeixin_daqin": {
        "JinmeixinDaqinCapitalPush": [
            {
                "api": "/chongtian/jinmeixin_daqin/repay/resultNotify",
                # check_points为空代表调用次数为0
                "check_points": []
            }
        ],
    },
    #  金美信大秦通知资方
    "jinmeixin_daqin_notify_capital": {
        "JinmeixinDaqinCapitalPush": [
            {
                "api": "/chongtian/jinmeixin_daqin/repay/resultNotify",
                "check_points": [
                    {
                        "$.orderId": "capital_notify_info['orderId']",
                        "$.repaySource": "capital_notify_info['repaySource']",
                        "$.repayStatus": "capital_notify_info['repayStatus']",
                        "$.loanOrderNo": "capital_notify_info['loanOrderNo']",
                        "$.repayTime": "capital_notify_info['repayTime']",
                        "$.repayTerm": "capital_notify_info['repayTerm']",
                        "$.repayAmt": "capital_notify_info['repayAmt']",
                        "$.mobile": "capital_notify_info['mobile']",
                        "$.bankCardNo": "capital_notify_info['bankCardNo']",
                        "$.bankName": "capital_notify_info['bankName']",
                        "$.bankCode": "capital_notify_info['bankCode']",
                        "$.repayPlanList[0].loanOrderNo": "capital_notify_info['repayPlanList'][0]['loanOrderNo']",
                        "$.repayPlanList[0].termNo": "capital_notify_info['repayPlanList'][0]['termNo']",
                        "$.repayPlanList[0].payOrderId": "capital_notify_info['repayPlanList'][0]['payOrderId']",
                        "$.repayPlanList[0].repayStatus": "capital_notify_info['repayPlanList'][0]['repayStatus']",
                        "$.repayPlanList[0].repayAmt": "capital_notify_info['repayPlanList'][0]['repayAmt']",
                        "$.repayPlanList[0].repayPrin": "capital_notify_info['repayPlanList'][0]['repayPrin']",
                        "$.repayPlanList[0].repayInt": "capital_notify_info['repayPlanList'][0]['repayInt']",
                        "$.repayPlanList[0].repayFee": "capital_notify_info['repayPlanList'][0]['repayFee']",
                        "$.repayPlanList[0].repayTime": "capital_notify_info['repayPlanList'][0]['repayTime']",
                    }
                ]
            }
        ],
    },

    # 金美信汉辰不通知资方
    "jinmeixin_hanchen": {
        "JinmeixinHanchenCapitalPush": [
            {
                "api": "/chongtian/jinmeixin_hanchen/repay/resultNotify",
                # check_points为空代表调用次数为0
                "check_points": []
            }
        ],
    },
    #  金美信汉辰通知资方
    "jinmeixin_hanchen_notify_capital": {
        "JinmeixinHanchenCapitalPush": [
            {
                "api": "/chongtian/jinmeixin_hanchen/repay/resultNotify",
                "check_points": [
                    {
                        "$.orderId": "capital_notify_info['orderId']",
                        "$.repaySource": "capital_notify_info['repaySource']",
                        "$.repayStatus": "capital_notify_info['repayStatus']",
                        "$.loanOrderNo": "capital_notify_info['loanOrderNo']",
                        "$.repayTime": "capital_notify_info['repayTime']",
                        "$.repayTerm": "capital_notify_info['repayTerm']",
                        "$.repayAmt": "capital_notify_info['repayAmt']",
                        "$.mobile": "capital_notify_info['mobile']",
                        "$.bankCardNo": "capital_notify_info['bankCardNo']",
                        "$.bankName": "capital_notify_info['bankName']",
                        "$.bankCode": "capital_notify_info['bankCode']",
                        "$.repayPlanList[0].loanOrderNo": "capital_notify_info['repayPlanList'][0]['loanOrderNo']",
                        "$.repayPlanList[0].termNo": "capital_notify_info['repayPlanList'][0]['termNo']",
                        "$.repayPlanList[0].payOrderId": "capital_notify_info['repayPlanList'][0]['payOrderId']",
                        "$.repayPlanList[0].repayStatus": "capital_notify_info['repayPlanList'][0]['repayStatus']",
                        "$.repayPlanList[0].repayAmt": "capital_notify_info['repayPlanList'][0]['repayAmt']",
                        "$.repayPlanList[0].repayPrin": "capital_notify_info['repayPlanList'][0]['repayPrin']",
                        "$.repayPlanList[0].repayInt": "capital_notify_info['repayPlanList'][0]['repayInt']",
                        "$.repayPlanList[0].repayFee": "capital_notify_info['repayPlanList'][0]['repayFee']",
                        "$.repayPlanList[0].repayTime": "capital_notify_info['repayPlanList'][0]['repayTime']",
                    }
                ]
            }
        ],
    },
    "lanzhou_haoyue_qinjia": {
        "LanzhouHaoyueQinjiaCapitalPush": [
            {
                "api": "/qingjia/lanzhou_haoyue_qinjia/normalRepayNotice",
                "check_points": [
                    {
                        "$.bizid": "capital_notify_info['bizid']",
                        "$.repaytype": "capital_notify_info['repaytype']",
                        "$.deducttype": "capital_notify_info['deducttype']",
                        "$.loanno": "capital_notify_info['loanno']",
                        "$.detaillist[0].period": "capital_notify_info['detaillist'][0]['period']",
                        "$.detaillist[0].repaytime": "capital_notify_info['detaillist'][0]['repaytime']",
                        "$.detaillist[0].indeedtotal": "capital_notify_info['detaillist'][0]['indeedtotal']",
                        "$.detaillist[0].indeedcapital": "capital_notify_info['detaillist'][0]['indeedcapital']",
                        "$.detaillist[0].indeedinterest": "capital_notify_info['detaillist'][0]['indeedinterest']",
                        "$.detaillist[0].indeedservicefee": "capital_notify_info['detaillist'][0]['indeedservicefee']",
                    }
                ]
            }
        ],
    },
    "lanzhou_haoyue_qinjia_advance_payoff": {
        "LanzhouHaoyueQinjiaCapitalPush": [
            {
                "api": "/qingjia/lanzhou_haoyue_qinjia/repayTrial",
                "check_points": [
                    {
                        "$.loanno": "capital_notify_info['loanno']",
                        "$.beginnum": "1",
                        "$.calctype": "3",
                    }
                ]
            },
            {
                "api": "/qingjia/lanzhou_haoyue_qinjia/settleRepayNotice",
                "check_points": [
                    {
                        "$.bizid": "capital_notify_info['bizid']",
                        "$.deducttype": "capital_notify_info['deducttype']",
                        "$.loanno": "capital_notify_info['loanno']",
                        "$.detaillist[0].period": "capital_notify_info['detaillist'][0]['period']",
                        "$.detaillist[0].repaytime": "capital_notify_info['detaillist'][0]['repaytime']",
                        "$.detaillist[0].indeedtotal": "capital_notify_info['detaillist'][0]['indeedtotal']",
                        "$.detaillist[0].indeedcapital": "capital_notify_info['detaillist'][0]['indeedcapital']",
                        "$.detaillist[0].indeedinterest": "capital_notify_info['detaillist'][0]['indeedinterest']",
                        "$.detaillist[0].indeedservicefee": "capital_notify_info['detaillist'][0]['indeedservicefee']",
                    }
                ]
            }
        ],
    },

}
