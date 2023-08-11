# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class WeipinHanchenJfMock(Easymock):

    def update_bindcard_query_new_user(self):
        """
        开户查询(新用户开户)
        status	绑卡状态
            00-处理中
            01-成功
            02-失败
            03-等待短信验证码验证
        :return:
        """
        api = "/jingfa/weipin_hanchen_jf/kuainiu/query/bindCardResultQuery"
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "transMsg": "未查询到绑卡记录",
                    "isAccountOpening": 0,    # 0-未绑卡 ，1-已绑卡
                    "status": "02"
                },
                "message": "请求成功"
            }
        }
        self.update(api, body)

    def update_bindcard_query_success(self):
        """
        开户查询（开户成功）
        status	绑卡状态
            00-处理中
            01-成功
            02-失败
            03-等待短信验证码验证
        :return:
        """
        api = "/jingfa/weipin_hanchen_jf/kuainiu/query/bindCardResultQuery"
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "transMsg": "",
                    "isAccountOpening": 1,
                    "status": "03"
                },
                "message": "请求成功"
            }
        }
        self.update(api, body)

    def update_bindcard_query_old_user_success(self):
        """
        开户查询（开户成功）,老用户查询
        status	绑卡状态
            00-处理中
            01-成功
            02-失败
            03-等待短信验证码验证
        :return:
        """
        api = "/jingfa/weipin_hanchen_jf/kuainiu/query/bindCardResultQuery"
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "transMsg": "交易成功",
                    "isAccountOpening": 1,
                    "status": "01"
                },
                "message": "请求成功"
            }
        }
        self.update(api, body)

    def update_bindcard_get_sms_verify(self):
        """
        获取短信验证码
        status	签约请求结果
                00-处理中；
                01-成功；
                02-失败；
                03-等待短信验证码验证
                99-已绑卡
        :return:
        """
        api = "/jingfa/weipin_hanchen_jf/kuainiu/apply/preBindingCardApply"
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "uniqueNo": "u@id",
                    "status": "03"
                },
                "message": "请求成功"
            }
        }
        self.update(api, body)

    def update_bindcard_confirm(self):
        """
        协议支付签约(绑卡确认接口)
        status	绑卡状态
                00-处理中；
                01-成功；
                02-失败；
        :return:
        """
        api = "/jingfa/weipin_hanchen_jf/kuainiu/apply/bindCardConfirm"
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "protocolNo": "mk@id",
                    "status": "01"
                },
                "message": "请求成功"
            }
        }
        self.update(api, body)

    def update_creditapply_status(self, creditStatus='01', message='请求成功'):
        """
        授信申请接口
        creditStatus 授信状态
            00 已接收
            01 审批中
            02 审批通过
            03 审批拒绝
        :return:
        """
        api = '/jingfa/weipin_hanchen_jf/kuainiu/apply/creditApply'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "creditStatus": creditStatus
                },
                "message": message
            }
        }
        self.update(api, body)

    def update_creditresult_query(self, startDate='20221021', endDate='20291231', quota=2000000, creditStatus='02',
                                  message='请求成功'):
        """
        授信结果查询接口
        creditStatus	授信状态
            01 审批中
            02 审批通过
            03 审批拒绝
        :return:
        """
        api = '/jingfa/weipin_hanchen_jf/kuainiu/query/creditResultQuery'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "endDate": endDate,
                    "quota": quota,
                    "creditStatus": creditStatus,
                    "startDate": startDate
                },
                "message": message
            }
        }
        self.update(api, body)

    def update_quota_query(self):
        api = '/jingfa/weipin_hanchen_jf/kuainiu/v2/query/quotaQuery'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "quotaFlag": "01"
                },
                "message": "请求成功"
            }
        }
        # 这是已授信返回的json结构
        # {
        #     "code": 0,
        #     "message": "success",
        #     "data": {
        #         "code": "000000",
        #         "data": {
        #             "availableQuota": 1000000, #会判断
        #             "endDate": "20240522", #会判断
        #             "quotaFlag": "02",
        #             "totalQuota": 1000000,
        #             "creditNo": "WPHCW2023041684747795", #落到alr_tN字段
        #             "startDate": "20230522",
        #             "usedQuota": 0
        #         },
        #         "message": "请求成功"
        #     }
        # }
        self.update(api, body)

    def update_quota_query_old_user(self,availableQuota=1000000, endDate='20500522'):
        api = '/jingfa/weipin_hanchen_jf/kuainiu/v2/query/quotaQuery'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "availableQuota": availableQuota, #会判断
                    "endDate": endDate, #会判断
                    "quotaFlag": "02",
                    "totalQuota": 1000000,
                    "creditNo": "WPHC@id", #落到alr_tN字段
                    "startDate": "20230522",
                    "usedQuota": 0
                },
                "message": "请求成功"
            }
        }
        self.update(api, body)

    def update_loanapplyconfirm_success(self):
        """
        用信申请接口
        loanStatus	贷款状态
            01 审批中
            02 审批通过
            03 审批拒绝
            :return:
        """
        api = '/jingfa/weipin_hanchen_jf/kuainiu/apply/loanApply'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "loanStatus": "01"
                },
                "message": "请求成功"
            }
        }
        self.update(api, body)

    def update_loanapplyconfirm_fail(self):
        """
        用信申请接口
        loanStatus	贷款状态
            01 审批中
            02 审批通过
            03 审批拒绝
            :return:
        """
        api = '/jingfa/weipin_hanchen_jf/kuainiu/apply/loanApply'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "loanStatus": "03"
                },
                "message": "审批拒绝"
            }
        }
        self.update(api, body)

    def update_loanresult_query(self, asset_info, loanstatus='02', rejectcode='', remark=''):
        """
        用信查询接口
       loanStatus	用信状态
            01 审批中
            02 审批通过
            03 审批拒绝
            :return:
        """
        api = '/jingfa/weipin_hanchen_jf/kuainiu/query/loanResultQuery'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "rejectCode": rejectcode,
                    "loanStatus": loanstatus,
                    "loanDate": get_date(fmt="%Y-%m-%d %H:%M:%S"),
                    "loanAmt": asset_info['data']['asset']['amount'] * 100,
                    "remark": remark
                },
                "message": "请求成功"
            }
        }
        self.update(api, body)

    def upate_repayplan_query(self, asset_info):
        """
        还款计划查询
        :return:
        """
        api = '/jingfa/weipin_hanchen_jf/kuainiu/query/repayPlanQuery'
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        period = asset_info['data']['asset']['period_count']
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "code": "000000",
                "data": {
                    "loanDate": get_date(fmt="%Y%m%d"),
                    "periods": period,
                    "repayPlans": []
                },
                "message": "请求成功"
            }
        }
        repayplanlist = {
            "preRepayPrinciple": 74560,
            "preTotalAmt": 94560,
            "preRepayDate": "20221124",
            "preRepayInterest": 20000,
            "preDefaultInterest": 0,
            "currentPeriod": 1
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplanlist)
            repayment_plan['currentPeriod'] = i + 1
            repayment_plan['preRepayPrinciple'] = float(fee_info['principal'])
            repayment_plan['preRepayInterest'] = float(fee_info['interest'])
            repayment_plan['preTotalAmt'] = float(fee_info['principal']) + float(fee_info['interest'])
            repayment_plan['preRepayDate'] = fee_info['date'].replace("-", "")
            body['data']['data']['repayPlans'].append(repayment_plan)
        self.update(api, body)
