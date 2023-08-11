# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import *
import calendar


class QinNong(Easymock):
    def update_upload_success(self):
        api = "/qinnong/upload"
        mode = {"code": 0, "message": "附件sftp上传成功", "data": None}
        self.update(api, mode)

    def update_ftp_upload_success(self):
        api = "/capital/ftp/upload/qinnong"
        mode = {
                  "code": 0,
                  "message": "",
                  "data": {
                    "dir": "/10002/20210531/S2021053130647355554/",
                    "name": "01_kn_qyd_S2021053130647355554_guarantee.pdf",
                    "type": None,
                    "result": {
                      "code": 0,
                      "message": "成功"
                    }
                  }
                }
        self.update(api, mode)

    def update_apply_success(self):
        api = "/qinnong/std/loan/apply"
        mode = {"code": 0, "message": "成功", "data": {"__v": "@id", "loan_order_no": "qn_whl_1599460614897"}}
        self.update(api, mode)


    def update_apply_fail(self):
        api = "/qinnong/std/loan/apply"
        mode = {"code": 1, "message": "mock测试", "data": {"__v": "@id", "loan_order_no": "qn_whl_1599460614897"}}
        self.update(api, mode)

    def update_apply_query_success(self, asset_info):
        api = "/qinnong/std/loan/query"
        mode = {"code": 0, "message": "成功",
                "data": {"grant_amount": asset_info['data']['asset']['amount'] * 100,
                         "credit_amount": 1000000,
                         "__v": "@id",
                         "asset_status": "pass",
                         "loan_order_no": asset_info['data']['asset']['item_no']}}
        self.update(api, mode)

    def update_apply_query_not_order(self):
        api = "/qinnong/std/loan/query"
        mode = {
                "code": 10000,
                "message": "借款申请不存在",
                "data": None
            }
        self.update(api, mode)


    def update_apply_query_failed(self,  asset_info):
        api = "/qinnong/std/loan/query"
        mode = {"code": 0, "message": "成功",
                "data": {"grant_amount": asset_info['data']['asset']['amount'] * 100,
                         "loan_result_desc": "风控订单审核拒绝",
                         "__v": "@id",
                         "asset_status": "refuse",
                         "loan_order_no": asset_info['data']['asset']['item_no']}}
        self.update(api, mode)

    def update_post_apply_success(self):
        api = "/qinnong/upload"
        mode = {"code": 0, "message": "附件sftp上传成功", "data": None}
        self.update(api, mode)

    def update_confirm_apply_success(self, asset_info):
        api = "/qinnong/std/loan/grant"
        mode = {"code": 0, "message": "成功",
                "data": {"__v": "@id", "loan_order_no": asset_info['data']['asset']['item_no']}}
        self.update(api, mode)

    def update_confirm_query_success(self, asset_info):
        api = "/qinnong/std/loan/query"
        count = int(asset_info["data"]["asset"]["period_count"])
        mode = {"code": 0,
                "message": "success",
                "data": {"loan_result_desc": "",
                         "asset_item_no": asset_info['data']['asset']['item_no'],
                         "grant_amount": asset_info['data']['asset']['amount'] * 100,
                         "__v": "@id",
                         "due_at": get_date(month=count, fmt="%Y-%m-%d"),
                         # get_date(month=count, fmt="%Y-%m-%d")
                         # if datetime.now().day <= 25
                         # else get_date(month=count, fmt="%Y-%m-") + str(calendar.monthrange(datetime.now().year,
                         #                                                                    int(get_date(
                         #                                                                        month=count,
                         #                                                                        fmt="%m")))[1]),
                         "loan_order_no": asset_info['data']['asset']['item_no'],
                         "asset_status": "repay",
                         "debt_no": "@id",
                         "grant_at": get_date(fmt="%Y-%m-%d")}}
        self.update(api, mode)

    def update_confirm_query_fail(self, asset_info):
        api = "/qinnong/std/loan/query"
        count = int(asset_info["data"]["asset"]["period_count"])
        mode = {"code": 0,
                "message": "success",
                "data": {"loan_result_desc": "放款失败",
                         "asset_item_no": asset_info['data']['asset']['item_no'],
                         "grant_amount": asset_info['data']['asset']['amount'] * 100,
                         "__v": "@id",
                         "due_at": get_date(month=count, fmt="%Y-%m-%d"),
                         # get_date(month=count, fmt="%Y-%m-%d")
                         # if datetime.now().day <= 25
                         # else get_date(month=count, fmt="%Y-%m-") + str(calendar.monthrange(datetime.now().year,
                         #                                                                    int(get_date(
                         #                                                                        month=count,
                         #                                                                        fmt="%m")))[1]),
                         "loan_order_no": asset_info['data']['asset']['item_no'],
                         "asset_status": "invalid",
                         "grant_at": get_date(fmt="%Y-%m-%d")}}
        self.update(api, mode)

    def update_confirm_query_fail_02(self, asset_info):
        api = "/qinnong/std/loan/query"
        count = int(asset_info["data"]["asset"]["period_count"])
        mode = {"code": 0,
                "message": "success",
                "data": {"loan_result_desc": "放款失败",
                         "asset_item_no": asset_info['data']['asset']['item_no'],
                         "grant_amount": asset_info['data']['asset']['amount'] * 100,
                         "__v": "@id",
                         "due_at": get_date(month=count, fmt="%Y-%m-%d"),
                         "loan_order_no": asset_info['data']['asset']['item_no'],
                         "asset_status": "failed",
                         "grant_at": get_date(fmt="%Y-%m-%d")}}
        self.update(api, mode)

    def update_certificate_apply_success(self):
        api = "/qinnong/std/certify/apply"
        mode = {
          "code": 0,
          "message": "success",
          "data": {
            "__v": 1618198762.021277
          }
        }
        self.update(api, mode)

    def update_certificate_apply_fail(self):
        api = "/qinnong/std/certify/apply"
        mode = {
          "code": 1,
          "message": "结清证明申请处理失败：资产未结清或未结算完成",
          "data": None
        }
        self.update(api, mode)

    def update_certificate_apply_fail_exist(self):
        api = "/qinnong/std/certify/apply"
        mode = {
          "code": 1,
          "message": "结清证明申请处理失败：结清证明申请已存在",
          "data": None
        }
        self.update(api, mode)

    def update_repay_plan_success(self, asset_info):
        api = "/qinnong/std/repayment/repay-plan"
        mode_temp = {
            "due_day": "2020-10-08",
            "interest": 2610,
            "period": 0,
            "principal": 65582,
            "repay_plan_status": "nofinish"
        }
        mode = {
            "code": 0,
            "message": "success",
            "data": {
                "__v": "@id",
                "repay_plans": []
            }
        }
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        count = asset_info["data"]["asset"]["period_count"]
        for i in range(0, asset_info["data"]["asset"]["period_count"]):
            data_temp = deepcopy(mode_temp)
            if i == (asset_info["data"]["asset"]["period_count"] - 1):
                data_temp["due_day"] = get_date(month=i + 1, fmt="%Y-%m-%d")
            else:
                if datetime.now().day <= 25:
                    data_temp["due_day"] = get_date(month=i + 1, fmt="%Y-%m-%d")
                else:
                    data_temp["due_day"] = get_date(month=i + 1, fmt="%Y-%m-25")
                    # data_temp["due_day"] = get_date(month=i + 1, fmt="%Y-%m-") + \
                    #                        str(calendar.monthrange(datetime.now().year,
                    #                                                int(get_date(
                    #                                                    month=count,
                    #                                                    fmt="%m")))[1])
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            data_temp["interest"] = fee_info['interest']
            data_temp["period"] = i
            data_temp["principal"] = fee_info['principal']
            data_temp["repay_plan_status"] = "nofinish"
            mode["data"]["repay_plans"].append(data_temp)
        self.update(api, mode)

    def update_repay_plan_with_diff(self, asset_info, diff_type, diff_loc=0, due_at='2020-01-01 00:00:00'):
        """
        diff_type='diff_principal'，本金不一致
        diff_type='diff_period'，期次不一致
        diff_type='diff_due_at'，还款日期不一致
        diff_type='diff_interest_tolerable'，利息不一致，容差范围内
        diff_type='diff_interest_intolerable'，利息不一致，超过容差范围
        mock数据都将差别放在第1期
        :param asset_info:
        :param type:
        :return:
        """
        api = "/qinnong/std/repayment/repay-plan"
        mode_temp = {
            "due_day": "2020-10-08",
            "interest": 2610,
            "period": 0,
            "principal": 65582,
            "repay_plan_status": "nofinish"
        }
        mode = {
            "code": 0,
            "message": "success",
            "data": {
                "__v": "@id",
                "repay_plans": []
            }
        }
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        count = asset_info["data"]["asset"]["period_count"]
        for i in range(0, asset_info["data"]["asset"]["period_count"]):
            data_temp = deepcopy(mode_temp)
            if i == (asset_info["data"]["asset"]["period_count"] - 1):
                data_temp["due_day"] = get_date(month=i + 1, fmt="%Y-%m-%d")
            else:
                if datetime.now().day <= 25:
                    data_temp["due_day"] = get_date(month=i + 1, fmt="%Y-%m-%d")
                else:
                    data_temp["due_day"] = get_date(month=i + 1, fmt="%Y-%m-25")
                    # data_temp["due_day"] = get_date(month=i + 1, fmt="%Y-%m-") + \
                    #                        str(calendar.monthrange(datetime.now().year,
                    #                                                int(get_date(
                    #                                                    month=count,
                    #                                                    fmt="%m")))[1])
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            data_temp["interest"] = fee_info['interest']
            data_temp["period"] = i
            data_temp["principal"] = fee_info['principal']
            data_temp["repay_plan_status"] = "nofinish"
            mode["data"]["repay_plans"].append(data_temp)
        # 根据type修改还款数据
        if diff_type == 'diff_principal':
            mode["data"]['repay_plans'][diff_loc]['principal'] += 1
        elif diff_type == 'diff_due_at':
            mode["data"]['repay_plans'][diff_loc]['due_day'] = due_at
        elif diff_type == 'diff_interest_tolerable':
            mode["data"]['repay_plans'][diff_loc]['interest'] += 1
        elif diff_type == 'diff_interest_intolerable':
            mode["data"]['repay_plans'][diff_loc]['interest'] -= 1000
        elif diff_type == 'diff_period':
            mode["data"]['repay_plans'].pop(0)
        self.update(api, mode)


if __name__ == "__main__":
    pass
