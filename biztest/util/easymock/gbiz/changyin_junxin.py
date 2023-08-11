# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_event_by_item_no_event_type
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy

from biztest.util.tools.tools import get_date


class ChangyinJunxinMock(Easymock):

    def update_card_query(self):
        """
        签约查询(新用户开户)
        """
        api = "/changyin/changyin_junxin/api/protocol/query"
        body = {
                "body": {
                    "agrSeq": "",
                    "resultCode": "0000",
                    "resultMsg": "此卡号尚未签约，请发起签约申请",
                    "result_code": "0000",
                    "result_msg": "此卡号尚未签约，请发起签约申请"
                },
                "head": {
                    "reqNo": "671b1feeb7f14111a3fefef5fd10e920",
                    "respCode": "0000",
                    "respMsg": "交易成功！",
                    "respNo": "CY12035020113553900032499"
                }
            }
        self.update(api, body)


    def update_card_query_old_user(self):
        """
        签约查询(老用户开户)
        """
        api = "/changyin/changyin_junxin/api/protocol/query"
        body = {

        }
        self.update(api, body)



    def update_protocol_apply(self):
        """
        签约申请
        """
        api = "/changyin/changyin_junxin/api/protocol/apply"
        body = {
                "body": {
                    "agrSeq": "",
                    "resultCode": "0000",
                    "resultMsg": "获取短信成功",
                    "result_code": "0000",
                    "result_msg": "获取短信成功"
                },
                "head": {
                    "reqNo": "b81a7d5392624486911110407e01dedc",
                    "respCode": "0000",
                    "respMsg": "交易成功！",
                    "respNo": "CY12035020113562400032565"
                }
            }
        self.update(api, body)

    def update_protocol_confirm(self):
        """
        签约确认
        """
        api = "/changyin/changyin_junxin/api/protocol/confirm"
        body = {
                "body": {
                    "agrSeq": "T@id",
                    "resultCode": "1002",
                    "resultMsg": "签约成功",
                    "result_code": "1002",
                    "result_msg": "签约成功"
                },
                "head": {
                    "reqNo": "ef8554bb5f0b44fa9c177af17babd883",
                    "respCode": "0000",
                    "respMsg": "交易成功！",
                    "respNo": "CY12035020114002700032756"
                }
            }
        self.update(api, body)

    def update_credit_apply(self, item_no, respCode='0000',respMsg='交易成功！'):
        """
        授信申请
        """
        api = "/changyin/changyin_junxin/api/credit/apply"
        body = {
                  "body": {
                    "applCde": "T@id",
                    "outApplSeq": item_no
                  },
                  "head": {
                    "reqNo": "de9848817c7f413c8f652b148a2eef49",
                    "respCode": respCode,
                    "respMsg": respMsg,
                    "respNo": "CY12035020114285900033962"
                  }
                }
        self.update(api, body)

    def update_credit_query(self, item_no, respCode='0000',respMsg='交易成功！',outSts='04', baselimit=200000):
        """
        授信查询
        outSts	外部状态
                01	授信中
                02	授信拒绝
                04	授信通过
        """
        api = '/changyin/changyin_junxin/api/credit/query'
        body = '''{
                "body": {
                "applCde": function({
                      _req
                    }) {
                      return _req.body.applCde
                    },
                "baseLimit": %s,
                "contractNo": "HT@id",
                "custId": "C@id",
                "isUnion": "N",
                "outApplSeq": "%s",
                "outSts": %s
            },
            "head": {
                "reqNo": "35e6cd2da61349ccb566f20046acffc6",
                "respCode": %s,
                "respMsg": "%s",
                "respNo": "CY12035022817001000151482"
            }
        }''' % (baselimit, item_no, outSts, respCode, respMsg)
        self.update(api, body)


    def update_confirm_apply(self, item_no, dnsts=100):
        """
        放款申请
        dnSts 放款状态
                100:放款中
                200:放款成功
                300:放款失败
        """
        api = '/changyin/changyin_junxin/api/loan/apply'
        body = '''{
                  "body": {
                    "applCde":function({
                      _req
                    }) {
                      return _req.body.applCde
                    },
                    "dnSts": %s,
                    "loanSeq": "L@id",
                    "outLoanSeq": "%s"
                  },
                  "head": {
                    "reqNo": "2c6aa198c0774ae09f2a07abc0aa9fb4",
                    "respCode": "0000",
                    "respMsg": "交易成功！",
                    "respNo": "CY@id"
                  }
                }''' % (dnsts, item_no)
        self.update(api, body)

    def update_loan_query(self, item_no, asset_info, dnsts='200', payMsg='清算成功'):
        """
        放款结果查询
        dnSts	放款状态
                100:放款中
                200:放款成功
                300:放款失败
        """
        api = '/changyin/changyin_junxin/api/loan/query'
        body = '''{
              "body": {
                "applCde": function({
                      _req
                    }) {
                      return _req.body.applCde
                    },
                "contractNo": "H@id",
                "dnAmt": "%s",
                "dnSts": "%s",
                "loanActvDt": "%s",
                "loanActvTime": "%s",
                "loanNo": "A@id",
                "loanSeq": function({
                      _req
                    }) {
                      return _req.body.loanSeq
                    },
                "outLoanSeq": "%s",
                "payMsg": "%s"
              },
              "head": {
                "reqNo": "dda1bd589aee465f87cbf36c7093b785",
                "respCode": "0000",
                "respMsg": "交易成功！",
                "respNo": "CY@id"
              }
            }''' % (asset_info['data']['asset']['amount'], dnsts, get_date(fmt="%Y-%m-%d"), get_date(fmt="%Y-%m-%d %H:%M:%S"),
                  item_no, payMsg)
        self.update(api, body)


    def update_repayplan_query(self, asset_info, item_no):
        """
        还款计划查询
        """
        alr = get_asset_loan_record_by_item_no(item_no)
        loanno = alr[0].get('asset_loan_record_due_bill_no')
        applCde = eval(alr[0].get('asset_loan_record_extend_info')).get('appl_cde')
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/changyin/changyin_junxin/api/repaymentPlan/query'
        body = {
                  "body": {
                    "applCde": applCde,
                    "loanNo": loanno,
                    "repaymentPlanList": [
                        {
                            "dueDt": "2035-03-02",
                            "intRate": "0.085",
                            "lastSetlDt": "",
                            "odIntRate": "0.1275",
                            "perdNo": "0",
                            "ppErInd": "N",
                            "prodCommIntAmt": "0.0",
                            "prodIntAmt": "0.0",
                            "prodPrcpAmt": "0.0",
                            "psCommOdInt": "0.0",
                            "psFeeAmt": "0.0",
                            "psInstmAmt": "0.0",
                            "psNormIntAmt": "0.0",
                            "psOdInd": "N",
                            "psOdIntAmt": "0.0",
                            "psPrcpAmt": "0.0",
                            "psRemPrcp": "10000.0",
                            "setlCommOdInt": "0.0",
                            "setlFeeAmt": "0.0",
                            "setlInd": "N",
                            "setlNormInt": "0.0",
                            "setlOdIntAmt": "0.0",
                            "setlPrcp": "0.0"
                        }
                    ],
                    "status": "M0"
                  },
                  "head": {
                    "reqNo": "c63cd35f36eb43c598e0afcd9ec3bea4",
                    "respCode": "0000",
                    "respMsg": "交易成功！",
                    "respNo": "CY@id"
                  }
                }
        repayplan = {
                    "dueDt": "2035-04-02",
                    "intRate": "0.085",
                    "lastSetlDt": "",
                    "odIntRate": "0.1275",
                    "perdNo": "0",
                    "ppErInd": "N",
                    "prodCommIntAmt": "0.0",
                    "prodIntAmt": "0.0",
                    "prodPrcpAmt": "0.0",
                    "psCommOdInt": "0.0",
                    "psFeeAmt": "0.0",
                    "psInstmAmt": "872.2",
                    "psNormIntAmt": "70.83",
                    "psOdInd": "N",
                    "psOdIntAmt": "0.0",
                    "psPrcpAmt": "801.37",
                    "psRemPrcp": "9198.63",
                    "setlCommOdInt": "0.0",
                    "setlFeeAmt": "0.0",
                    "setlInd": "N",
                    "setlNormInt": "0.0",
                    "setlOdIntAmt": "0.0",
                    "setlPrcp": "0.0"
                  }

        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplan)
            repayment_plan['perdNo'] = i + 1
            repayment_plan['psPrcpAmt'] = float(fee_info['principal'])/100
            repayment_plan['psNormIntAmt'] = float(fee_info['interest'])/100
            repayment_plan['psInstmAmt'] = float(fee_info['principal'] + fee_info['interest'])/100
            repayment_plan['dueDt'] = fee_info['date']
            body['body']['repaymentPlanList'].append(repayment_plan)
        self.update(api, body)



    def update_certificate_apply(self):
        """
        申请结清证明
        status	接收状态
            0-成功
            1-失败
        """
        api = '/changyin/changyin_junxin/api/signature/apply'
        body = {
              "body": {
                "status": "0",
                "statusDesc": "接收成功"
              },
              "head": {
                "reqNo": "fdbe9aa3187b47a7b260c82a032a5730",
                "respCode": "0000",
                "respMsg": "交易成功！",
                "respNo": "CY@id"
              }
            }
        self.update(api, body)

    def update_certificate_download(self):
        """
        下载结清证明
        status	状态
            0-成功
            1-失败
            2-开具中
        """
        api = '/changyin/changyin_junxin/api/signature/query'
        body = '''{
                "body": {
                    "imageId": "614420230412065549010747",
                    "imgUrl": "/upload/cyxf/30/2023/04/12/14436020813128811009/loan_clear_certificate.pdf",
                    "outSeq": function({
                              _req
                            }) {
                              return _req.body.outSeq
                            },
                    "status": "0" },
                "head": {
                    "reqNo": "54ab3bd0155541f1a49979900b6fb1c7",
                    "respCode": "0000",
                    "respMsg": "交易成功！",
                    "respNo": "CY@id"
                }
            }'''
        self.update(api, body)
