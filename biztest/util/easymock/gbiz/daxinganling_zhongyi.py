# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.function.gbiz.gbiz_db_function import *

"""
MOCK资方接口响应数据
"""


class DaxinganlingZhongyiMock(Easymock):
    def update_protocol_sms_success(self):
        '''
        获取短信验证码成功
        uniqueCode存入 capital_account_action_seq
        :return:
        '''
        api = "/daxinganling_zhongyi/v2/repay/bindCard/preBindCardEncrypted"
        mode = {
                "code": "2000",
                "msg": "请求成功",
                "data": {
                    "uniqueCode": "T@id"
                },
                "success": True
            }
        self.update(api, mode)

    def update_protocol_confirm_success(self):
        '''
        agreeNo存入开户表中capital_account_step_user_key、capital_account_user_key
        :return:
        '''
        api = "/daxinganling_zhongyi/v2/repay/bindCard/confirmBindCard"
        mode = {
                "code": "2000",
                "msg": "请求成功",
                "data": {
                    "agreeNo": "A@id"
                },
                "success": True
            }
        self.update(api, mode)


    # 订单提交接口-返回成功
    def update_loan_apply_success(self):
        api = "/daxinganling_zhongyi/v2/order"
        mode = {
                    "code": "2000",
                    "msg": "请求成功",
                    "data": None,
                    "success": True
                }
        self.update(api, mode)


    def update_loan_apply_fail(self):
        api = "/daxinganling_zhongyi/v2/order"
        mode = {
                    "code": "1000",
                    "msg": "mock 请求失败",
                    "data": None,
                    "success": True
                }
        self.update(api, mode)

    def update_repay_plan_push_success(self):
        api = "/daxinganling_zhongyi/v2/repay/repayMent/initOrUpdateRepayPlan"
        mode = {
                "code": "2000",
                "msg": "请求成功",
                "data": None,
                "success": True
            }
        self.update(api, mode)

    def update_loan_apply_query_success(self, item_no, asset_info):
        """
        放款成功，查询接口,还款计划起息时间（billingDate）是T+1（工作日+1，遇到节假日顺延，所以自动化在临近节假日时运行，可能时不正确的，回调也是一样的）
        :return:
        """
        api = '/daxinganling_zhongyi/v2/query/assetQueryLoanState'
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        body = {
              "code": "2000",
              "msg": "请求成功",
              "data": [
                {
                  "state": "success",
                  "merchantOrderNo": item_no,
                  "errorCode": None,
                  "loanDate": get_date(fmt="%Y-%m-%d"),
                  "billingDate": get_date(day=1, fmt="%Y-%m-%d"),
                  "contractPreviewUrl": "https://testsignapi.wsmtec.com/platform/api/home/fileinfo/get?code=2020230111054579-3e8ff9be5e96a676720e7ead803126ec&contractNo=2020230111054579&handle=redirect",
                  "contractDownloadUrl": "https://testsignapi.wsmtec.com/platform/api/home/fileinfo/get?code=2020230111054579-3e8ff9be5e96a676720e7ead803126ec&contractNo=2020230111054579",
                  "loanRate": "0.0650",
                  "totalInterest": "3555",
                  "sign": "41fa9b1d35e8e446f584eba5e05e1f00",
                  "loanBankWholeName": "大兴安岭农村商业银行股份有限公司",  # 这个字段值会存入asset_loan_record_extend_info中
                  "contractNo": item_no,
                  "accountingDate": get_date(fmt="%Y-%m-%d"),
                  "repayPlan": [

                  ],
                  "contractSignedDate": get_date(fmt="%Y-%m-%d"),
                  "loanDateFull": get_date(fmt="%Y-%m-%d %H:%M:%S"),
                  "errorMsg": None
                }
              ],
              "success": True
            }
        repayplanlist = {
                  "period": 1,
                  "repayDate": "2023-02-12",
                  "principal": 8088,
                  "interest": 542,
                  "amount": 8630
                }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayplanlist)
            repayment_plan['period'] = i + 1
            repayment_plan['principal'] = float(fee_info['principal'])
            repayment_plan['interest'] = float(fee_info['interest'])
            repayment_plan['amount'] = float(fee_info['principal']) + float(fee_info['interest'])
            repayment_plan['repayDate'] = fee_info['date']
            body['data'][0]['repayPlan'].append(repayment_plan)
        self.update(api, body)


    def update_loan_apply_query_fail(self, item_no):
        """
        放款查询接口
        :return:
        """
        api = '/daxinganling_zhongyi/v2/query/assetQueryLoanState'
        body={
                "code": "2000",
                "msg": "外层mock失败",
                "data": [
                    {
                        "state": "error",
                        "merchantOrderNo": item_no,
                        "errorCode": 4040,
                        "errorMsg": "内层mock 失败测试",
                        "loanDate": None,
                        "billingDate": None,
                        "contractPreviewUrl": None,
                        "contractDownloadUrl": None,
                        "loanRate": None,
                        "totalInterest": None,
                        "sign": "a5ff68aaf3ffd249dcc8437ca57644e7",
                        "loanBankWholeName": None,
                        "contractNo": None,
                        "accountingDate": None,
                        "repayPlan": None,
                        "contractSignedDate": None,
                        "loanDateFull": None
                    }
                ],
                "success": True
            }
        self.update(api, body)

    def update_contractpush_success(self, item_no):
        api = '/capital/ftp/upload/daxinganling_zhongyi'
        body = {
                "code": 0,
                "message": "",
                "data": {
                    "dir": "/upload/FKSJ/63-YMS_M-contract/20230112/",
                    "name": item_no+".pdf",
                    "type": None,
                    "fileSize": 183577,
                    "fileDigest": "375b1ef16bc3d18a86de23a0f9aeb99c",
                    "result": {
                        "code": 0,
                        "message": "成功"
                    }
                }
            }
        self.update(api, body)
