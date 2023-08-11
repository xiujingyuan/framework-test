# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayMengShangZhongYiMock(Easymock):
    def mengshang_zhongyi_repay_trial(self, respcd='0000', resptx='[0001]交易成功', principal=866.46, interest=10.00):
        """
        试算接口
        校验了以下参数
        本金 principal ：需要与我方一致，不一致则报错
        利息 interest ：需要小于等于我方，大于我方报错
        respcd	返回码
            0000	交易成功
            0100-0900	因蒙商消费系统原因产生的应答码
            1000-2900	有关各渠道送报文格式检查产生的应答码
            3000-5900	有关各渠道相关业务检查产生的应答码
            #具体code对应错误信息，查看code文档
        """

        api = "/mengshang/mengshang_zhongyi/repayTrial"
        mode = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "damage": 0,
                    "penalty": 0,
                    "principal": principal,
                    "interest": interest,
                    "respcd": respcd,
                    "resptx": resptx,
                    "total": 9199.01  # 没有校验,不用管
                  }
                }
        self.update(api, mode)

    def mengshang_zhongyi_repay_apply(self):
        """
        还款申请
        respcd	返回码
            0000	交易成功
            其他都可能是失败/重试--------具体是否失败code，需要看配置 还款系统KV: repay_mengshang_zhongyi_config.applyFailCodes
            非配置内的code,应该都是重试
        """
        api = "/mengshang/mengshang_zhongyi/deductionRepay"
        mode = {
              "code": 0,
              "message": "success",
              "data": {
                "respcd": "0500",
                "resptx": "[0501]交易已受理，请稍后查询交易结果"
              }
            }
        self.update(api, mode)

    def mengshang_zhongyi_repay_query(self, respcd='0000', resptx='[0001]交易成功',repayPrincipal=800.99,
                                      repayInterest=71.67, repayGuaranteeFee=72.84, repayTerm=1):
        """
        还款查询
        respcd	返回码
            0000	交易成功
            其他都可能是失败/重试--------具体是否失败code，需要看配置 还款系统KV: repay_mengshang_zhongyi_config.queryFailCodes
            非配置内的code,应该都是重试
        """
        api = "/mengshang/mengshang_zhongyi/queryDeduction"
        mode = '''{
                  "code": "0",
                  "message": "success",
                  "data": {
                    "totalAmt": 7470.21,  //没有用没有校验
                    "orderNo": "C022306140029740012",  //alr_due_bill_no, 没有校验
                    "respcd": "%s",
                    "resptx": "%s",
                    "ordrno": function({
                      _req
                    }) {
                      return _req.body.data.ordrno     //这个参数校验了，必须和请求保持一致
                    },
                    "payChannel": "BM-KN",
                    "paySerialNo": "@guid", //资金方实际没有返回，没有校验
                    "repaySucTime": "%s",  // 还款成功时间，校验必须有值，格式正确
                    "repayInfos": [{
                      "repayBreakFee": 0,
                      "repayOtherFee": 0,
                      "repayPenalty": 0,
                      "repayServiceFee": 0,
                      "repayPrincipal": %s, // 当期代扣的本金，要校验，不一致报错
                      "repayInterest": %s,  //如果是提前结清，则是资金方试算返回的金额，如果是正常还款，则是当期的利息；要校验，不一致报错
                      "repayGuaranteeFee": %s,   // 当期代扣的我方用户还款计划中的reserve+consult类型的费用和；要校验，不一致报错
                      "repayTerm": %s,  // 还款的期次，似乎也没有校验
                      "repayType": "04"  //04提前结清、05正常还款； 但没有校验这个参数是否正确
                    }]
                  }
                }''' % (respcd, resptx, get_date(fmt="%Y%m%d%H%M%S"), repayPrincipal, repayInterest, repayGuaranteeFee,
                        repayTerm)
        self.update(api, mode)
