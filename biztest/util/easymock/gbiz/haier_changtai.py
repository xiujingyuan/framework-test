# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import get_date
from biztest.util.tools.tools import get_date_timestamp


class HaierChangtaiMock(Easymock):
    def update_loan_preapply(self, code='00000', message='处理成功', rtnCode='00000', rtnMsg='成功'):
        """
        协议共享接口
        """
        api = "/haier/haier_changtai/common/LP40023"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "rtnMsg": rtnMsg,
                    "requestNo": "L@id",
                    "rtnCode": rtnCode
                }
            }
        self.update(api, body)


    def update_loanconfirm_apply(self, code='00000', message='处理成功',status='0',msg2='处理中', code2=None):
        """
        支用申请
        status 支用申请状态:
                1:支用成功
                -1:支用失败
                0：支用处理中
        """
        api = "/haier/haier_changtai/api/loan/loanApply"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "status": status,
                    "code": code2,
                    "message": msg2
                }
            }
        self.update(api, body)

    def update_loanconfirm_query(self, code='00000', message='处理成功', status='1', msg2='已放款',  code2=None):
        """
        支用结果查询
        支用申请状态 status
            1:支用成功
            -1:支用失败
            0：支用处理中
        """
        api = "/haier/haier_changtai/api/loan/loanResultQuery"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "status": status,
                    "code":  code2,
                    "message": msg2,
                    "applSeq": "a@id",  # 存入asset_loan_record_trade_no
                    "contNo": "C-@id",  # 存入asset_loan_record_identifier
                    "loanMode": "N",
                    "loanNo": "L-@id"  # 存入asset_loan_record_due_bill_no
                }
            }
        self.update(api, body)

    def update_repayplan_query_tmp(self, asset_info):
        """
        还款计划查询接口，查询放款成功的时间
        """
        api = "/haier/haier_changtai/repay/LP30006"
        body = {
                  "code": "00000",
                  "message": "处理成功",
                  "data": {
                    "serno": "b0009b1bcbe84604bb35fdabd352885f",
                    "resultList": [{
                      "loanOdInd": "Y",
                      "superCoopr": "C0202300002192",
                      "applSeq": 30044682,
                      "apprvAmt": asset_info['data']['asset']['amount'],
                      "channelNo": "Y5",
                      "loanNo": "L-test001",
                      "cooprName": "上海腾桥信息技术有限公司",
                      "idNo": "360827199510269306",
                      "irrCuster": 24,
                      "mtdDesc": "等额本息-按还款周期（一致）",
                      "typGrp": "02",
                      "mtdCde": "DEBX02",
                      "loanActvDt": get_date(fmt="%Y-%m-%d"),  # 放款日期，就是放款成功的时间，存入alr表的起息时间
                      "nextDueDt": get_date(month=1, fmt="%Y-%m-%d"),  # 下一次还款日
                      "applyTnrTyp": "11",
                      "applyDt": get_date(fmt="%Y-%m-%d"),
                      "lastDueDt": get_date(month=12, fmt="%Y-%m-%d"),  # 最后还款日
                      "lmPmShdList": [],
                      "contNo": "C-test002",
                      "cooprCde": "D602023100000012722",
                      "loanTyp": "20239664",
                      "loanOsPrcp": 13000,
                      "odGrace": 4,
                      "loanMode": "N",
                      "apprvTnr": "12"  # 总期数
                    }]
                  }
                }
        self.update(api, body)
    def update_repayplan_query(self,  item_no, asset_info):
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        alr = get_asset_loan_record_by_item_no(item_no)
        loanno = alr[0].get('asset_loan_record_due_bill_no')
        contNo = alr[0].get('asset_loan_record_identifier')
        api = '/haier/haier_changtai/repay/LP30006'
        body = {
              "code": "00000",
              "message": "处理成功",
              "data": {
                "serno": "b0009b1bcbe84604bb35fdabd352885f",
                "resultList": [{
                  "loanOdInd": "Y",
                  "superCoopr": "C0202300002192",
                  "applSeq": 30044682,  # 不校验这个参数
                  "apprvAmt": asset_info['data']['asset']['amount'],
                  "channelNo": "Y5",
                  "loanNo": loanno,
                  "cooprName": "上海腾桥信息技术有限公司",
                  "idNo": "360827199510269306",  # 不校验这个身份证
                  "irrCuster": 24,
                  "mtdDesc": "等额本息-按还款周期（一致）",
                  "typGrp": "02",
                  "mtdCde": "DEBX02",
                  "loanActvDt": get_date(fmt="%Y-%m-%d"),  # 放款日期，就是放款成功的时间，存入alr表的起息时间
                  "nextDueDt": get_date(month=1, fmt="%Y-%m-%d"),  # 下一次还款日
                  "applyTnrTyp": "12",
                  "applyDt": get_date(fmt="%Y-%m-%d"),
                  "lastDueDt": get_date(month=12, fmt="%Y-%m-%d"),  # 最后还款日
                  "lmPmShdList": [{
                              "psWvOdInt": 0,
                              "setlPenalFeeAmt": 0,
                              "setlLateFeeAmt": 0,
                              "ppErInd": "N",
                              "psCommOdInt": 0,
                              "psDueDt": "2053-06-28",
                              "advanceFeeAmt": 0,
                              "lateFeeAmt": 0,
                              "psInstmAmt": 0,
                              "psIntRate": 0.24,
                              "psOdIntAmt": 0,
                              "psOdIntRate": 0.36,
                              "psPerdNo": 0,
                              "setlFeeAmt": 0,
                              "penalFeeAmt": 0,
                              "psWvCommInt": 0,
                              "setlOdIntAmt": 0,
                              "setlAdvanceFeeAmt": 0,
                              "setlPrcp": 0,
                              "psWvNmInt": 0,
                              "psCutAmt": 0,
                              "cpsSts": "01",
                              "psFeeAmt": 0,
                              "setlNormInt": 0,
                              "setlCommOdInt": 0,
                              "wvList": [],
                              "psPrcpAmt": 0,
                              "setlInd": "N",
                              "psNormInt": 0,
                              "psRemPrcp": 13000,
                              "acctFeeAmt": 0,
                              "psOdInd": "N",
                              "lastSetlDt": "",
                              "setlAcctFeeAmt": 0
                            }],
                  "contNo": contNo,
                  "cooprCde": "D602023100000012722",
                  "loanTyp": "20239664",  # 贷款产品
                  "loanOsPrcp": 13000,
                  "odGrace": 4,
                  "loanMode": "N",
                  "apprvTnr": "12"  # 总期数
                }]
              }
            }
        repayplan_tmp = {
                  "psWvOdInt": 0,
                  "setlPenalFeeAmt": 0,
                  "setlLateFeeAmt": 0,
                  "ppErInd": "N",
                  "psCommOdInt": 0,
                  "psDueDt": "2053-07-28",  # 当期到期时间
                  "advanceFeeAmt": 0,
                  "lateFeeAmt": 0,
                  "psInstmAmt": 1267.38,  # 没有校验这个值
                  "psIntRate": 0.24,
                  "psOdIntAmt": 38.11,
                  "psOdIntRate": 0.36,
                  "psPerdNo": 1,  # 期次
                  "setlFeeAmt": 0,
                  "penalFeeAmt": 0,
                  "psWvCommInt": 0,
                  "setlOdIntAmt": 0,
                  "setlAdvanceFeeAmt": 0,
                  "setlPrcp": 0,
                  "psWvNmInt": 0,
                  "psCutAmt": 0,
                  "cpsSts": "01",
                  "psFeeAmt": 0,
                  "setlNormInt": 0,
                  "setlCommOdInt": 0,
                  "wvList": [],
                  "psPrcpAmt": 969.27,  # 当期应还本金
                  "setlInd": "N",
                  "psNormInt": 260,  # 利息
                  "psRemPrcp": 12030.73,
                  "acctFeeAmt": 0,
                  "psOdInd": "Y",
                  "lastSetlDt": "",
                  "setlAcctFeeAmt": 0
                }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplan_tmp)
            repayment_plan['psPerdNo'] = i + 1
            repayment_plan['psPrcpAmt'] = float(fee_info['principal']) / 100
            repayment_plan['psNormInt'] = float(fee_info['interest']) / 100
            repayment_plan['psDueDt'] = fee_info['date']
            body['data']['resultList'][0]['lmPmShdList'].append(repayment_plan)
        self.update(api, body)
