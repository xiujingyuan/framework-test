# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *
from biztest.function.gbiz.gbiz_check_function import get_asset_event


class ZhongYuanZunHaoMock(Easymock):
    def update_query_bind_card_new_user(self):
        '''
        用户从未开过户
        :return:
        '''
        api = "/zhongzhirong/zhongyuan_zunhao/query.bind.card"
        mode = {
                "code": 10002,
                "message": "参数错误 当前 用户编号 没有预绑卡 error",
                "data": None
            }

        self.update(api, mode)

    def update_query_bind_card_timeout(self):
        api = "/zhongzhirong/zhongyuan_zunhao/query.bind.card"
        mode = {
                "code": 1,
                "message": "mock资方接口返回timeout",
                "data": None
            }
        self.update(api, mode)

    def update_query_bind_card(self, four_element):
        '''
        用户尚未开户成功时
        :return:
        '''
        api = "/zhongzhirong/zhongyuan_zunhao/query.bind.card"
        mode = {
                "code": 0,
                "message": "成功",
                "data": {
                    "listAgreement": [
                        {
                            "custName": four_element['data']['user_name'],
                            "idNo": four_element['data']['id_number'],
                            "cardNo": four_element['data']['bank_code'],
                            "mobileNo": four_element['data']['phone_number'],
                            "status": "01",
                            "cardName": None,
                            "deductNoFlag": None,
                            "modifiedTime": None,
                            "channelRepayId": None,
                            "bankChannel": None
                        }
                    ]
                }
            }
        self.update(api, mode)


    def update_query_bind_card_after_openaccount(self, four_element):
        '''
        开户之后查询
        :return:
        '''
        api = "/zhongzhirong/zhongyuan_zunhao/query.bind.card"
        mode = {
                "code": 0,
                "message": "成功",
                "data": {
                    "listAgreement": [
                        {
                            "custName": four_element['data']['user_name'],
                            "idNo": four_element['data']['id_number'],
                            "cardNo": four_element['data']['bank_code'],
                            "mobileNo": four_element['data']['phone_number'],
                            "status": "02",
                            "cardName": None,
                            "deductNoFlag": None,
                            "modifiedTime": None,
                            "channelRepayId": None,
                            "bankChannel": None
                        }
                    ]
                }
            }
        self.update(api, mode)


    def update_pre_bind_card(self):
        '''
        获取验证码
        :return:
        '''
        api = "/zhongzhirong/zhongyuan_zunhao/pre.bind.card"
        mode = '''{
          "code": 0,
          "message": "成功",
          "data": {
            "checkFlag": "Y",
            "refuseNo": null,
            "refuseCause": null,
            "uniqueCode": "@id"
          }
        }'''
        self.update(api, mode)

    def update_bind_card(self):
        '''
        协议支付签约
        :return:
        '''
        api = "/zhongzhirong/zhongyuan_zunhao/bind.card"
        mode = {
          "code": 0,
          "message": "成功",
          "data": {
            "checkFlag": "Y",
            "refuseNo": None,
            "refuseCause": None,
            "bankChannel": "TLZFXPAY"
          }
        }
        self.update(api, mode)

    def update_upload_file_success(self):
        api = "/zhongzhirong/zhongyuan_zunhao/file.upload"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "retSinal": "Y",
                    "retCode": null,
                    "retDesc": null
                  }
                }'''
        self.update(api, mode)


    def update_loanapplynew_success(self):
        api = "/zhongzhirong/zhongyuan_zunhao/credit"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "custId": "@id",
                    "applCde": function({
                      _req
                    }) {
                      return _req.body.applCde
                    },
                    "cooppfApplCde": function({
                      _req
                    }) {
                      return _req.body.cooppfApplCde
                    },
                    "applSeq": "LC@id",
                    "checkFlag": "Y",
                    "checkMsgNo": null,
                    "checkMsg": null
                  }
                }'''
        self.update(api, mode)

    def update_loanapplynew_fail(self):
        api = "/zhongzhirong/zhongyuan_zunhao/credit"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "custId": "@id",
                    "applCde": function({
                      _req
                    }) {
                      return _req.body.applCde
                    },
                    "cooppfApplCde": function({
                      _req
                    }) {
                      return _req.body.cooppfApplCde
                    },
                    "applSeq": "LC@id",
                    "checkFlag": "N",
                    "checkMsgNo": "ZYZR,9999",
                    "checkMsg": "暂不符合授信政策，感谢您的关注。;不符合授信标准！"
                  }
                }'''
        self.update(api, mode)

    def update_loanapplyquery_success(self, asset_info):
        api = "/zhongzhirong/zhongyuan_zunhao/trans.query"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "listApproveInfo": [{
                      "applCde": function({
                        _req
                      }) {
                        return _req.body.applCde
                      },
                      "cooppfApplCde": function({
                        _req
                      }) {
                        return _req.body.cooppfApplCde
                      },
                      "applSeq": "LC@id",
                      "applPk": "sp@id",
                      "contTyp": "02",
                      "autoDnInd": null,
                      "applType": "XFDK", //放款查询：FKSQ，审批查询：XFDK
                      "outSts": "99", //20 审批中 30 待补件 88 待银行处理 99 结束 
                      "endMark": "01", //01 通过 02 否决 03 取消 
                      "applyAmt": %s,
                      "apprvAmt": %s,
                      "applyDt": "%s",
                      "refuseNo": null,
                      "refuseCause": null,
                      "contNo": "Cs@id",
                      "loanNo": "",
                      "dayIntRat": 0.000233,
                      "intRat": 0.085,
                      "apprvTnr": "%s",
                      "loanActvDt": null,
                      "apprvDt": "%s",
                      "contSts": "200",
                      "loanActvTime": null,
                      "signDt": "%s",
                      "signEndDt": "%s",
                      "adjType": null,
                      "lprRateType": "01",
                      "lprMapriceIssueDt": "2021-08-20",
                      "lprIssueMaprice": "0.03850000",
                      "lprFloatRate": "0.0465"
                    }]
                  }
                }''' % ((asset_info['data']['asset']['amount'])*100, (asset_info['data']['asset']['amount'])*100,
                       get_date(fmt="%Y-%m-%d %H:%M:%S"), asset_info['data']['asset']['period_count'],
                       get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d"), get_date(month=12, fmt="%Y-%m-%d"))
        self.update(api, mode)


    def update_loanapplyquery_fail(self, asset_info):
        api = "/zhongzhirong/zhongyuan_zunhao/trans.query"
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "listApproveInfo": [{
                      "applCde": function({
                        _req
                      }) {
                        return _req.body.applCde
                      },
                      "cooppfApplCde": function({
                        _req
                      }) {
                        return _req.body.cooppfApplCde
                      },
                      "applSeq": "LC@id",
                      "applPk": "sp@id",
                      "contTyp": "02",
                      "autoDnInd": null,
                      "applType": "XFDK", //放款查询：FKSQ，审批查询：XFDK
                      "outSts": "99", //20 审批中 30 待补件 88 待银行处理 99 结束 
                      "endMark": "02", //01 通过 02 否决 03 取消 
                      "applyAmt": %s,
                      "apprvAmt": %s,
                      "applyDt": "%s",
                      "refuseNo": "mock拒绝码",
                      "refuseCause": "mock拒绝原因",
                      "contNo": "Cs@id",
                      "loanNo": "",
                      "dayIntRat": 0.000233,
                      "intRat": 0.085,
                      "apprvTnr": "%s",
                      "loanActvDt": null,
                      "apprvDt": "%s",
                      "contSts": "200",
                      "loanActvTime": null,
                      "signDt": "%s",
                      "signEndDt": "%s",
                      "adjType": null,
                      "lprRateType": "01",
                      "lprMapriceIssueDt": "2021-08-20",
                      "lprIssueMaprice": "0.03850000",
                      "lprFloatRate": "0.0465"
                    }]
                  }
                }''' % ((asset_info['data']['asset']['amount'])*100, (asset_info['data']['asset']['amount'])*100,
                       get_date(fmt="%Y-%m-%d %H:%M:%S"), asset_info['data']['asset']['period_count'],
                       get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d"), get_date(month=12, fmt="%Y-%m-%d"))
        self.update(api, mode)

    def update_loanapplyquery_fail_02(self):
        '''
        线上一种异常情况，进件失败（比如因为姓名等）时切换资金方，此时切换资金方调用查询接口就会返回这种
        相当于是属于没有授信的那种
        :return:
        '''
        api = "/zhongzhirong/zhongyuan_zunhao/trans.query"
        mode = '''{
              "code": 0,
              "message": "成功",
              "data": null
            }'''
        self.update(api, mode)


    def update_querylpr_success(self):
        api = "/zhongzhirong/zhongyuan_zunhao/query.lpr"
        mode = '''{
              "code": 0,
              "message": "成功",
              "data": [{
                "listLPR": [{
                  "lpr_rate_type": "01",
                  "lpr_maprice_issue_dt": "2021-10-20",
                  "lpr_issue_maprice": "0.03850000"
                }],
                "sum_date": "2022-06-12",
                "sum_bs": "1"
              }]
            }'''
        self.update(api, mode)


    def update_loanapplyconfirm_success(self):
        api = "/zhongzhirong/zhongyuan_zunhao/loan"
        mode = '''{
              "code": 0,
              "message": "成功",
              "data": {
                "dnSeq": "LPB@id",
                "loanNo": "JJ@id",
                "cooppfApplCde": null
              }
            }'''
        self.update(api, mode)


    def update_loanapplyconfirm_fail(self):
        api = "/zhongzhirong/zhongyuan_zunhao/loan"
        mode = '''{
              "code": 1,
              "message": "mock失败",
              "data": {
                "dnSeq": "LPB@id",
                "loanNo": "JJ@id",
                "cooppfApplCde": null
              }
            }'''
        self.update(api, mode)

    def update_loanapplyconfirmquery_success(self, asset_info, item_no):
        api = "/zhongzhirong/zhongyuan_zunhao/trans.query"
        alr = get_asset_loan_record_by_item_no(item_no)
        loanno = alr[0].get('asset_loan_record_due_bill_no')
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "listApproveInfo": [{
                      "applCde": function({
                        _req
                      }) {
                        return _req.body.applCde
                      },
                      "cooppfApplCde": function({
                        _req
                      }) {
                        return _req.body.cooppfApplCde
                      },
                      "applSeq": "LC@id",
                      "applPk": "fk@id",
                      "contTyp": "02",
                      "autoDnInd": null,
                      "applType": "FKSQ", //放款查询：FKSQ，审批查询：XFDK
                      "outSts": "99", //20 审批中 30 待补件 88 待银行处理 99 结束 
                      "endMark": "01", //01 通过 02 否决 03 取消 
                      "applyAmt": %s,
                      "apprvAmt": %s,
                      "applyDt": "%s",
                      "refuseNo": null,
                      "refuseCause": null,
                      "contNo": "Cs@id",
                      "loanNo": "%s",
                      "dayIntRat": 0.000233,
                      "intRat": 0.085,
                      "apprvTnr": "%s",
                      "loanActvDt": null,
                      "apprvDt": "%s",
                      "contSts": "200",
                      "loanActvTime": "%s",
                      "signDt": "%s",
                      "signEndDt": "%s",
                      "adjType": null,
                      "lprRateType": "01",
                      "lprMapriceIssueDt": "2021-08-20",
                      "lprIssueMaprice": "0.03850000",
                      "lprFloatRate": "0.0465"
                    }]
                  }
                }''' % ((asset_info['data']['asset']['amount'])*100, (asset_info['data']['asset']['amount'])*100,
                       get_date(fmt="%Y-%m-%d %H:%M:%S"), loanno, asset_info['data']['asset']['period_count'],
                       get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d"),
                        get_date(month=12, fmt="%Y-%m-%d"))
        self.update(api, mode)

    def update_loanapplyconfirmquery_fail(self, asset_info, item_no):
        api = "/zhongzhirong/zhongyuan_zunhao/trans.query"
        alr = get_asset_loan_record_by_item_no(item_no)
        loanno = alr[0].get('asset_loan_record_due_bill_no')
        mode = '''{
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "listApproveInfo": [{
                      "applCde": function({
                        _req
                      }) {
                        return _req.body.applCde
                      },
                      "cooppfApplCde": function({
                        _req
                      }) {
                        return _req.body.cooppfApplCde
                      },
                      "applSeq": "LC@id",
                      "applPk": "fk@id",
                      "contTyp": "02",
                      "autoDnInd": null,
                      "applType": "FKSQ", //放款查询：FKSQ，审批查询：XFDK
                      "outSts": "99", //20 审批中 30 待补件 88 待银行处理 99 结束 
                      "endMark": "02", //01 通过 02 否决 03 取消 
                      "applyAmt": %s,
                      "apprvAmt": %s,
                      "applyDt": "%s",
                      "refuseNo": "mock拒绝码",
                      "refuseCause": "mock拒绝原因",
                      "contNo": "Cs@id",
                      "loanNo": "%s",
                      "dayIntRat": 0.000233,
                      "intRat": 0.085,
                      "apprvTnr": "%s",
                      "loanActvDt": null,
                      "apprvDt": "%s",
                      "contSts": "200",
                      "loanActvTime": "%s",
                      "signDt": "%s",
                      "signEndDt": "%s",
                      "adjType": null,
                      "lprRateType": "01",
                      "lprMapriceIssueDt": "2021-08-20",
                      "lprIssueMaprice": "0.03850000",
                      "lprFloatRate": "0.0465"
                    }]
                  }
                }''' % ((asset_info['data']['asset']['amount'])*100, (asset_info['data']['asset']['amount'])*100,
                       get_date(fmt="%Y-%m-%d %H:%M:%S"), loanno, asset_info['data']['asset']['period_count'],
                       get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d %H:%M:%S"), get_date(fmt="%Y-%m-%d"),
                        get_date(month=12, fmt="%Y-%m-%d"))
        self.update(api, mode)


    def update_queryrepayplan_success(self, item_no, asset_info):
        api = "/zhongzhirong/zhongyuan_zunhao/query.repayplan"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        loantnr = asset_info['data']['asset']['period_count']
        loanactvdt =get_date(fmt="%Y%m%d")
        alr = get_asset_loan_record_by_item_no(item_no)
        loanno = alr[0].get('asset_loan_record_due_bill_no')
        dnseq = alr[0].get('asset_loan_record_identifier')
        mode = {
                  "code": 0,
                  "message": "成功",
                  "data": {
                    "listLmLoan": [
                      {
                        "loanNo": loanno,
                        "dnSeq": dnseq,
                        "tkCooppfApplCde": "691001"+item_no,
                        "loanDebtSts": "NORM",
                        "curSetlserviceFeeAmt": 0,
                        "loanTnr": loantnr,
                        "loanActvDt": loanactvdt,
                        "listLmShd": []
                      }
                    ],
                    "psOdInd": None,
                    "graceDays": None,
                    "lastSetlDt": None
                  }
                }
        repayment_plan_tmp = {
                      "psPerdNo": 1,
                      "psDueDt": "2025-08-23",
                      "payDt": None,
                      "psInstmAmt": 87220,
                      "psPerdAmt": 87220,
                      "psPrcpAmt": 80580,
                      "psNormInt": 6640,
                      "feeSumAmt": 0,
                      "penalFeeAmt": 0,
                      "psOdIntAmt": 0,
                      "psRemPrcp": 839186,
                      "setlInstmAmt": 0,
                      "setlPrcp": 0,
                      "setlNormInt": 0,
                      "setlOdIntAmt": 0,
                      "setlFeeAmtS": 0,
                      "setlPenalFeeAmt": 0,
                      "amortPrimeAmt": 0,
                      "psSts": "1",
                      "hkTyp": "N"
                    }
        for i in range(asset_info['data']['asset']['period_count']):
                fee_info = get_fee_info_by_period(rate_info, i + 1)
                repayment_plan = deepcopy(repayment_plan_tmp)
                repayment_plan['psPerdNo'] = i + 1
                repayment_plan['psDueDt'] = fee_info['date'].replace("-", "")
                # psInstmAmt、psPerdAmt在代码中实际上不会校验
                repayment_plan['psInstmAmt'] = float(fee_info['principal']) + float(fee_info['interest'])#在代码中实际上不校验
                repayment_plan['psPerdAmt'] = float(fee_info['principal']) + float(fee_info['interest'])
                repayment_plan['psPrcpAmt'] = float(fee_info['principal'])
                repayment_plan['psNormInt'] = float(fee_info['interest'])
                mode['data']['listLmLoan'][0]['listLmShd'].append(repayment_plan)
        self.update(api, mode)

    def update_contractpush_success(self):
        api = "/capital/ftp/upload/zhongyuan_zunhao"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "dir": "/kn/knFile/upfile/zyzk6910/downfile/20250905/",
                    "name": "620521198603310501_S2022061584394385442.zip",
                    "type": null,
                    "fileSize": 56056,
                    "result": {
                      "code": 0,
                      "message": "成功"
                    }
                  }
                }'''
        self.update(api, mode)



if __name__ == "__main__":
    pass
