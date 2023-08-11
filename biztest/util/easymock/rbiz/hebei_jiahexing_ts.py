# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *


class RepayHebeiJiahexingTsMock(Easymock):
    def hebei_jiahexing_repay_trial(self, respcode=9999, prinlamt=8000, intamt=43.33, penaltyamt=0):
        """
        试算接口
        校验了以下参数
        本金 prinlamt ：需要与我方一致，不一致则报错
        利息 intamt ：需要小于等于我方，大于我方报错
        罚息 penaltyamt ：若当日已经有罚息，则会将返回的罚息与我方存的罚息校验，不一致报错，若当日未刷罚息，则将试算返回的罚息存入
        """

        api = "/zhongke/hebei_jiahexing_ts/repaytrial"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "loanno": function({
                      _req
                    }) {
                      return _req.body.data.loanno
                    },
                    "applyno": function({
                      _req
                    }) {
                      return _req.body.data.applyno
                    },
                    "totalamt": %s,
                    "prinlamt": %s,
                    "intamt": %s,
                    "penaltyamt": %s,
                    "repaydate": "%s",
                    "transdate": "%s",
                    "transtime": "154726",
                    "respcode": "%s",
                    "respmesg": "交易处理成功",
                    "tradeserialno": "4661c7e31f274daaa06b5f05a6329a17"
                  }
                }''' % (float(prinlamt+intamt), prinlamt, intamt, penaltyamt, get_date(fmt="%Y-%m-%d"),
                        get_date(fmt="%Y-%m-%d"), respcode)
        self.update(api, mode)

    def hebei_jiahexing_push_apply(self):
        """
        推送申请
        """
        api = "/zhongke/hebei_jiahexing_ts/repayapply"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "transdate": get_date(fmt="%Y-%m-%d"),
                    "transtime": "152424",
                    "respcode": "0000",
                    "respmesg": "交易接收成功",
                    "tradeserialno": "b2f2940c145c4d389b0fd7861f4f1aac"
                }
            }
        self.update(api, mode)

    def hebei_jiahexing_push_repayquery(self):
        """
        推送查询
        paystatus	还款结果处理状态
            1-成功  #capital_notify状态变更为success
            0-失败  #capital_notify状态变是process
            2-处理中 #capital_notify状态变更为process
        """
        api = "/zhongke/hebei_jiahexing_ts/repayquery"
        mode = '''{
                  "code": 0,
                  "message": "success",
                  "data": {
                    "repayserialno": function({
                      _req
                    }) {
                      return _req.body.data.repayserialno
                    },
                    "loanno": "504511043301971401",  //似乎没有校验这个参数
                    "applyno": function({
                      _req
                    }) {
                      return _req.body.data.applyno
                    },
                    "paystatus": "1",   //只要这个状态对就可以了，其他参数似乎并未校验
                    "paydt": "20451208",
                    "paytotalamt": 691.07,
                    "payprinlamt": 647.04,
                    "payintamt": 43.33,
                    "paypenaltyamt": 0.7,
                    "transdate": "20230410",
                    "transtime": "152524",
                    "respcode": "9999", //这个code=0000/9999都可以成功
                    "respmesg": "交易处理成功",
                    "tradeserialno": "14e333336a674129b15ea7db01679f62"
                  }
                }'''
        self.update(api, mode)

    def hebei_jiahexing_repayplanquery(self):
        """
            还款计划查询，主要是用于刷罚息job调用，并从中获取到当期罚息
            prinlpenaltyamt 当期罚息金额
            actualprinlpenaltyamt 实际已经还了的罚息
            我方得到的罚息=prinlpenaltyamt-actualprinlpenaltyamt
            除了以上罚息参数，其他参数不会校验
        """
        api = "/zhongke/hebei_jiahexing_ts/repayplanquery"
        mode = '''{
                      "code": 0,
                      "message": "success",
                      "data": {
                        "loanno": function({
                          _req
                        }) {
                          return _req.body.data.loanno
                        },
                        "applyno":function({
                          _req
                        }) {
                          return _req.body.data.applyno
                        },
                        "totalnum": 12,
                        "curter": 1,
                        "payschedule": [{
                            "planno": "@id",
                            "term": 1,
                            "enddt": "20451204",
                            "prinlamt": 647.04,
                            "actualprinlamt": 0,
                            "intamt": 43.33,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 6.6, //校验这个金额，这个是当期罚息，其他的参数似乎不校验
                            "actualprinlpenaltyamt": 0, //这个是当期已还罚息，真正的罚息，是用prinlpenaltyamt-actualprinlpenaltyamt得到的
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 2,
                            "enddt": "20460104",
                            "prinlamt": 650.54,
                            "actualprinlamt": 0,
                            "intamt": 39.83,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 3,
                            "enddt": "20460204",
                            "prinlamt": 654.07,
                            "actualprinlamt": 0,
                            "intamt": 36.3,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 4,
                            "enddt": "20460304",
                            "prinlamt": 657.61,
                            "actualprinlamt": 0,
                            "intamt": 32.76,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 5,
                            "enddt": "20460404",
                            "prinlamt": 661.17,
                            "actualprinlamt": 0,
                            "intamt": 29.2,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 6,
                            "enddt": "20460504",
                            "prinlamt": 664.75,
                            "actualprinlamt": 0,
                            "intamt": 25.62,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 7,
                            "enddt": "20460604",
                            "prinlamt": 668.35,
                            "actualprinlamt": 0,
                            "intamt": 22.02,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 8,
                            "enddt": "20460704",
                            "prinlamt": 671.97,
                            "actualprinlamt": 0,
                            "intamt": 18.4,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 9,
                            "enddt": "20460804",
                            "prinlamt": 675.61,
                            "actualprinlamt": 0,
                            "intamt": 14.76,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 10,
                            "enddt": "20460904",
                            "prinlamt": 679.27,
                            "actualprinlamt": 0,
                            "intamt": 11.1,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 11,
                            "enddt": "20461004",
                            "prinlamt": 682.95,
                            "actualprinlamt": 0,
                            "intamt": 7.42,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          },
                          {
                            "planno": "@id",
                            "term": 12,
                            "enddt": "20461104",
                            "prinlamt": 686.67,
                            "actualprinlamt": 0,
                            "intamt": 3.72,
                            "actualintamt": 0,
                            "prinlpenaltyamt": 0,
                            "actualprinlpenaltyamt": 0,
                            "ispreps": "0",
                            "feetotal": 0,
                            "actualfeetotal": 0,
                            "shouldpayduepremium": 0,
                            "actualpayduepremium": 0
                          }
                        ],
                        "transdate": "20230410",
                        "transtime": "151234",
                        "respcode": "9999",
                        "respmesg": "交易处理成功",
                        "tradeserialno": "3c80f052a4e742f9aaa6d75936dee733"
                      }
                    }'''
        self.update(api, mode)
