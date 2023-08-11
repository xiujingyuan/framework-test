# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *
from biztest.function.gbiz.gbiz_check_function import get_asset_event


class MengShangZhongYiMock(Easymock):
    def update_loan_apply_get_route(self, code=0, message='success', respcd='0000', resptx='[0001]交易成功'):
        """
        进件-获取资金路由接口
        """
        api = "/mengshang/mengshang_zhongyi/fundRoute"
        body = {
                  "code": code,
                  "message": message,
                  "data": {
                    "investorList": [{
                      "fdpFullName": "内蒙古蒙商消费金融股份有限公司",
                      "fdpName": "蒙商消费金融",
                      "fdpScale": 1
                    }],
                    "rateList": [{
                      "installCnt": 1,
                      "interestDayRate": 0.000239,
                      "interestYearRate": 0.086
                    }],
                    "respcd": respcd,
                    "resptx": resptx
                  }
                }
        self.update(api, body)

    def update_loan_apply_new(self, code=0, message='success', respcd='0500', resptx='[0501]交易已受理，请稍后查询交易结果',
                              bus_number='b@id'):
        """
        进件-借款审核
        """
        api = "/mengshang/mengshang_zhongyi/loanExamines"
        body = {
                  "code": code,
                  "message": message,
                  "data": {
                    "busNumber": bus_number,  # 存入asset_loan_record_extend_info字段中，成功时校验是否为空
                    "respcd": respcd,
                    "resptx": resptx
                  }
                }
        self.update(api, body)


    def update_loan_apply_query(self, code=0, message='success', respcd='0000', resptx='[0001]交易成功'):
        """
        LoanApplyQuery&LoanConfirmQuery共同调用的交易结果查询接口
        """
        api = "/mengshang/mengshang_zhongyi/tradeRestQuerys"
        body = '''{
                  "code": %s,
                  "message": "%s",
                  "data": {
                    "busNumber": function({
                                            _req
                                          }) {
                                            return _req.body.data.busNumber
                                          },   //会校验这个参数需要与请求保持一致
                    "busType": "01",  //busType	交易类型：01借款审核、02借款发放
                    "ordrNo": function({
                                            _req
                                          }) {
                                            return _req.body.comm.ordrno
                                          },
                    "respcd": "%s",
                    "resptx": "%s",
                    "tradeStatus": "01",  //资金方说这个参数不管
                    "tradeStatusDesc": "交易成功" //资金方说这个参数不管
                  }
                }''' % (code, message, respcd, resptx)
        self.update(api, body)


    def update_loanconfirm_apply(self, code=0, message='success', respcd='0500', resptx='[0501]交易已受理，请稍后查询交易结果'):
        """
        LoanApplyConfirm 借款申请
        """
        api = "/mengshang/mengshang_zhongyi/loanPayments"
        body = {
                "code": code,
                "message": message,
                "data": {
                    "respcd": respcd,
                    "resptx": resptx
                }
            }
        self.update(api, body)

    def update_loan_query(self, code=0, message='success', respcd='0000', resptx='[0001]交易成功'):
        """
        LoanApplyQuery&LoanConfirmQuery共同调用的交易结果查询接口
        """
        api = "/mengshang/mengshang_zhongyi/tradeRestQuerys"
        body = '''{
                "code": %s,
                "message": "%s",
                "data": {
                    "busType": "02",
                    "loanApplicanDate": "%s",  //放款成功时间，没时分秒，使用当前时间补充
                    "orderNo": "T@id",  // 存入alr_due_bill_no中
                    "ordrNo": function({
                                            _req
                                          }) {
                                            return _req.body.comm.ordrno
                                          },
                    "payPlanList": [   //这个还款计划不管，没用到，也没有校验
                        {
                            "period": 1,
                            "scheduleDate": 20220810,
                            "scheduleInterest": 57.33,
                            "schedulePrincipal": 640.8,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 2,
                            "scheduleDate": 20220910,
                            "scheduleInterest": 52.74,
                            "schedulePrincipal": 645.39,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 3,
                            "scheduleDate": 20221010,
                            "scheduleInterest": 48.12,
                            "schedulePrincipal": 650.01,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 4,
                            "scheduleDate": 20221110,
                            "scheduleInterest": 43.46,
                            "schedulePrincipal": 654.67,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 5,
                            "scheduleDate": 20221210,
                            "scheduleInterest": 38.77,
                            "schedulePrincipal": 659.36,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 6,
                            "scheduleDate": 20230110,
                            "scheduleInterest": 34.04,
                            "schedulePrincipal": 664.09,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 7,
                            "scheduleDate": 20230210,
                            "scheduleInterest": 29.28,
                            "schedulePrincipal": 668.85,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 8,
                            "scheduleDate": 20230310,
                            "scheduleInterest": 24.49,
                            "schedulePrincipal": 673.64,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 9,
                            "scheduleDate": 20230410,
                            "scheduleInterest": 19.66,
                            "schedulePrincipal": 678.47,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 10,
                            "scheduleDate": 20230510,
                            "scheduleInterest": 14.8,
                            "schedulePrincipal": 683.33,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 11,
                            "scheduleDate": 20230610,
                            "scheduleInterest": 9.9,
                            "schedulePrincipal": 688.23,
                            "scheduleServiceFee": 0
                        },
                        {
                            "period": 12,
                            "scheduleDate": 20230710,
                            "scheduleInterest": 4.97,
                            "schedulePrincipal": 693.16,
                            "scheduleServiceFee": 0
                        }
                    ],
                    "respcd": "%s",
                    "resptx": "%s",
                    "tradeStatus": "01",
                    "tradeStatusDesc": "交易成功"
                }
            }''' % (code, message, get_date(fmt="%Y-%m-%d"), respcd, resptx)
        self.update(api, body)


    def update_repayplan_query(self,  item_no, asset_info):
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        alr = get_asset_loan_record_by_item_no(item_no)
        order_no = alr[0].get('asset_loan_record_due_bill_no')
        api = '/mengshang/mengshang_zhongyi/queryRepayPlan'
        body = {
              "code": 0,
              "message": "success",
              "data": {
                "businessDate": get_date(fmt="%Y-%m-%d"),
                "orderNo": order_no,
                "period": 12,
                "repayPlanList": [],
                "respcd": "0000",
                "resptx": "[0001]交易成功"
              }
            }
        repayplan_tmp = {
                        "currency": "156",
                        "exemptionFine": 0,
                        "instalInterest": 57.33,  # 应还利息
                        "installCnt": 1,  # 期次
                        "lateRepayDate": 20220810,  # 最迟还款日
                        "overDays": 0,
                        "overdueInterest": 0,
                        "payOffFlag": "N",
                        "reduceInterest": 0,
                        "repayBaseAmt": 0,
                        "repayInterest": 0,
                        "repayOverdueInterest": 0,
                        "repayStatus": "0",
                        "repayTotalAmt": 0,
                        "shouldTotalAmt": 698.13,
                        "transAmt": 640.8  # 应还本金
                      }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplan_tmp)
            repayment_plan['installCnt'] = i + 1
            repayment_plan['transAmt'] = float(fee_info['principal']) / 100
            repayment_plan['instalInterest'] = float(fee_info['interest']) / 100
            repayment_plan['lateRepayDate'] = fee_info['date'].replace("-", "")
            body['data']['repayPlanList'].append(repayment_plan)
        self.update(api, body)

