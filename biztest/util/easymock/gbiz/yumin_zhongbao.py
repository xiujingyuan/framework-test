# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import *


class YuMinZhongBaoMock(Easymock):

    def update_amount_query_timeout(self):
        api = "/zhongzhirong/yumin_zhongbao/ym.amount.query"
        mode = {
            "code": "0",
            "message": "mock系统返回timeout",
            "data": None
        }
        self.update(api, mode)

    def update_card_pre_bind(self):
        api = "/zhongzhirong/yumin_zhongbao/ym.card.pre.bind"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "msgCodeId": "@id"
            }
        }
        self.update(api, mode)

    def update_card_bind(self):
        api = "/zhongzhirong/yumin_zhongbao/ym.card.bind"
        mode = '''{
              "code": "0",
              "message": "成功",
              "data": {
                "success": "true"
              }
            }'''
        self.update(api, mode)

    def update_image_upload(self):
        api = "/zhongzhirong/yumin_zhongbao/ym.image.upload"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "success": "true"
            }
        }
        self.update(api, mode)

    def update_image_live_upload(self):
        api = "/zhongzhirong/yumin_zhongbao/ym.image.live.upload"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "success": "true"
            }
        }
        self.update(api, mode)

    def update_credit_apply(self, status='Processing'):
        '''
        授信申请
        applyStatus
            Reject 拒绝
            Processing 处理中 --我方可当成功处理
        :return:
        '''
        api = "/zhongzhirong/yumin_zhongbao/ym.credit.apply"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "applyStatus": status
            }
        }
        self.update(api, mode)

    def update_credit_status(self, item, creditApprovalStatus='003', creditStatus='103'):
        '''
        授信状态查询
        creditApprovalStatus 处理状态
                001 审批中
                002 审批失败
                003 审批通过

        creditStatus 额度状态
                103 额度生效
                104 额度失效
                105 额度暂停
                106 额度冻结
        '''
        alr_data = get_asset_loan_record_by_item_no(item)
        creat_date = str(alr_data[0]['asset_loan_record_create_at'][0:13]).replace("-", "").replace(" ", "")
        api = "/zhongzhirong/yumin_zhongbao/ym.credit.status"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "result": [{
                    "applyDate": get_date(fmt="%Y-%m-%d"),
                    "approvedAmt": "83443930",
                    "approvedPsTm": get_date(fmt="%Y-%m-%d"),
                    "approvedRate": "8.95",
                    "availableAmt": "83443930",
                    "creditApplyNo": "30010001" + creat_date + str(item[-11:]) + "_1",
                    "creditApprovalStatus": creditApprovalStatus,
                    "creditBeginDate": get_date(fmt="%Y-%m-%d"),
                    "creditEndDate": get_date(month=12, fmt="%Y-%m-%d"),
                    "creditStatus": creditStatus,
                    "repaymentMethod": "01,03"
                },
                    # 下面是授信失败的流水号
                    {
                        "applyDate": "2054-04-21",
                        "creditApplyNo": "30010001202208241629969113913_1",
                        "creditApprovalStatus": "002"
                    },
                    {
                        "applyDate": "2054-04-21",
                        "creditApplyNo": "30010001202208241628206682844_1",
                        "creditApprovalStatus": "002"
                    }
                ]
            }
        }
        self.update(api, mode)

    def update_loan_apply(self, replyCode='Processing', replyMsg=None):
        '''
        放款申请
        replyCode:
            Succes，Fail，Processing
        '''
        api = "/zhongzhirong/yumin_zhongbao/ym.loan.apply"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "replyCode": replyCode,
                "replyMsg": replyMsg
            }
        }
        self.update(api, mode)

    def update_loan_status(self, item, loanResult='Success', resultMsg=None):
        '''
        放款状态查询
        '''
        alr_data = get_asset_loan_record_by_item_no(item)
        creat_date = str(alr_data[0]['asset_loan_record_create_at'][0:13]).replace("-", "").replace(" ", "")
        api = "/zhongzhirong/yumin_zhongbao/ym.loan.status"
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "result": [{
                    "contractCode": "裕民银行PH借字第"+get_date(fmt="%Y%m%d%H%M%S")+"号",
                    "firstTermRepayDay": "2054-06-25",
                    "loanAmt": "1000000",
                    "loanApplyNo": "30010001" + creat_date + str(item[9:]) + "_2",
                    "loanDate": get_date(fmt="%Y%m%d%H%M%S"),
                    "loanEndDate": get_date(month=12, fmt="%Y-%m-%d"),
                    "loanNo": "BN" + item,  # 资方返回的格式为：BN5764966139433717760，为了好写自动化，固定格式为：RN+资产编号
                    "loanResult": loanResult,
                    "loanStartDate": get_date(fmt="%Y-%m-%d"),
                    "repayDay": "25",
                    "resultMsg": resultMsg
                }]
            }
        }
        self.update(api, mode)

    def update_repay_plan(self, item, asset_info):
        '''
        还款计划查询
        :return:
        '''
        api = "/zhongzhirong/yumin_zhongbao/ym.repay.plan"
        # 未调试
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
            "code": "0",
            "message": "成功",
            "data": {
                "planList": []
            }
        }
        planList= {
                    "currentArrears": 0,
                    "interestAmount": 25556,  # 应还利息
                    "invalidCouponAmount": 0,
                    "loanNo": "BN" + item,
                    "otsndCmpdIntBal": 0,
                    "otsndIntAmt": 0,
                    "otsndPnpAmt": 0,
                    "otsndPnyIntAmt": 0,
                    "overdueDay": "0",
                    "paymentFlag": "PR",
                    "penaltyIntAmount": 0,
                    "planNo": "",
                    "principalAmount": 97114,  # 应还本金
                    "repayDate": "20540625",
                    "rpyblCmpdInt": 0,
                    "termNo": "1",
                    "totalAmount": 122670,  # 应还总额
                    "totalTerm": "12",
                    "unusedCouponAmount": 0,
                    "usedCouponAmount": 0
                }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(planList)
            repayment_plan['termNo'] = i + 1
            repayment_plan['principalAmount'] = float(fee_info['principal'])
            repayment_plan['interestAmount'] = float(fee_info['interest'])
            repayment_plan['totalAmount'] = float(fee_info['principal'] + fee_info['interest'])
            repayment_plan['repayDate'] = fee_info['date'].replace("-", "")
            mode['data']['planList'].append(repayment_plan)
        self.update(api, mode)

    def update_limit_cacel(self):
        '''
        额度注销接口，请求成功
        '''
        api = "/zhongzhirong/yumin_zhongbao/ym.limit.cancel"
        mode = {
                  "code": "0",
                  "message": "成功",
                  "data": {
                    "success": "true"
                  }
                }
        self.update(api, mode)

    def update_limit_cacel_repet(self):
        '''
        重复请求额度注销接口
        '''
        api = "/zhongzhirong/yumin_zhongbao/ym.loan.status"
        mode = {
                "code": "90001",
                "message": "异常情况 999003:网贷-授信-授信合同不存在！【详情】授信合同编号不存在或额度已经失效。",
                "data": None
            }
        self.update(api, mode)




if __name__ == "__main__":
    pass
