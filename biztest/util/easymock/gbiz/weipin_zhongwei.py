# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class WeipinZhongweiMock(Easymock):

    def update_account_open(self):
        '''
        用户注册
        :return:
        '''
        api = "/zhongzhirong/weipin_zhongwei/account.open"
        body = {
              "code": 0,
              "message": "成功",
              "data": {
                "respCode": "000000",
                "respMessage": "渠道处理成功",
                "userId": "16530278743892430040",
                "status": "S"
              }
            }
        self.update(api, body)

    def update_card_pre_binding(self):
        '''
        预绑卡
        :return:
        '''
        api = '/zhongzhirong/weipin_zhongwei/card.pre.binding'
        body = {
          "code": 0,
          "message": "成功",
          "data": {
            "respCode": "000000",
            "respMessage": "请求成功",
            "userId": "16530278743892430040",
            "status": "01"
          }
        }
        self.update(api, body)

    def update_card_binding(self):
        '''
        绑卡
        :return:
        '''
        api = '/zhongzhirong/weipin_zhongwei/card.binding'
        body = {
          "code": 0,
          "message": "成功",
          "data": {
            "respCode": "000000",
            "respMessage": "请求成功",
            "userId": "16530278743892430040",
            "status": "01"
          }
        }
        self.update(api, body)

    def update_image_upload(self, item_no, respCode='000000', respMessage='成功'):
        '''
        影像上传
        :return:
        '''
        api = '/zhongzhirong/weipin_zhongwei/image.upload'
        body = {
          "code": 0,
          "message": "成功",
          "data": {
            "respCode": respCode,
            "respMessage": respMessage,
            "creditApplyNo": item_no
          }
        }
        self.update(api, body)

    def update_credit_apl(self, item_no, respCode='000000', respMessage='渠道处理成功', status='S'):
        '''
        授信申请
        :return:
        '''
        api = '/zhongzhirong/weipin_zhongwei/credit.apl'
        body = {
          "code": 0,
          "message": "成功",
          "data": {
            "respCode": respCode,
            "respMessage": respMessage,
            "status": status,
            "creditAppNo": item_no,
            "userId": "16530278743892430040"
          }
        }
        self.update(api, body)

    def update_credit_apl_query(self, item_no, respCode='000000', respMessage='渠道处理成功', status='S'):
        '''
        授信申请查询
        :return:
        '''
        # 107000 --风控拒绝
        api = '/zhongzhirong/weipin_zhongwei/credit.apl.query'
        body = {
          "code": 0,
          "message": "成功",
          "data": {
            "respCode": respCode,
            "respMessage": respMessage,
            "creditAppNo": item_no,
            "userId": "16530278743892430040",
            "status": status,
            "creditLimit": 20000,
            "creditRate": 0.18,
            "failreason": None
          }
        }
        self.update(api, body)

    def update_loan_apl(self, item_no, respCode='000000', respMessage='成功', status='S'):
        '''
        借款申请
        :return:
        '''
        api = '/zhongzhirong/weipin_zhongwei/loan.apl'
        body = {
              "code": 0,
              "message": "成功",
              "data": {
                "respCode": respCode,
                "respMessage": respMessage,
                "status": status,
                "creditAppNo": item_no,
                "userId": "16530278743892430040"
              }
            }
        self.update(api,body)

    def update_loan_apl_query(self, item_no, respCode='000000', respMessage='成功', disbursementStatus='00' ,failreason=''):
        '''
        借款申请查询
        :return:
        '''
        api = '/zhongzhirong/weipin_zhongwei/loan.apl.query'
        body = {
              "code": 0,
              "message": "成功",
              "data": {
                "respCode": respCode,
                "respMessage": respMessage,
                "creditAppNo": item_no,
                "userId": "16530278743892430040",
                "disbursementStatus": disbursementStatus,
                "failreason": failreason,
                "completeTime": get_date(fmt="%Y%m%d%H%M%S"),
                "paymentPlanList": []  # 资方实际已返回，我们没用做逻辑判断，先不mock返回
              }
            }
        self.update(api, body)

    def update_repayplan_query(self, item_no, asset_info):
        '''
        还款计划查询
        :return:
        '''
        api = '/zhongzhirong/weipin_zhongwei/repayplan.query'
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        body = {
          "code": 0,
          "message": "成功",
          "data": {
            "respCode": "000000",
            "respMessage": "访问成功",
            "creditAppNo": item_no,
            "userId": "16530278743892430040",
            "planList": []
          }
        }
        planList = {
                "tenor": 1,
                "paymentDueDate": "20220428",
                "payablePrincipal": 383.4,
                "paymentPrincipal": 0,
                "payableInterest": 75,
                "paymentInterest": 0,
                "payablePenaltyInterest": 0,
                "paymentPenaltyInterest": 0,
                "payableCompoundInterest": 0,
                "paymentCompoundInterest": 0,
                "payableFee": 0,
                "paymentFee": 0,
                "paymentFlag": "1",
                "paymentDate": None,
                "totalAmount": 458.4,
                "principalAmount": 383.4,
                "interestAmount": 75,
                "penaltyIntAmount": 0,
                "compoundAmount": 0,
                "feeAmount": 0,
                "exemptAmount": 0,
                "waivedAmount": 0,
                "delqDays": 0
              }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(planList)
            repayment_plan['tenor'] = i + 1
            repayment_plan['payablePrincipal'] = float(fee_info['principal'])/100
            repayment_plan['payableInterest'] = float(fee_info['interest'])/100
            repayment_plan['totalAmount'] = repayment_plan['payablePrincipal'] + repayment_plan['payableInterest']
            repayment_plan['paymentDueDate'] = fee_info['date'].replace("-", "")
            body['data']['planList'].append(repayment_plan)
        self.update(api, body)

    def update_contract_download(self, item_no):
        '''
        协议下载
        :return:
        '''
        api = '/zhongzhirong/weipin_zhongwei/contract.download'
        body = {
          "code": 0,
          "message": "成功",
          "data": {
            "respCode": "000000",
            "respMessage": "成功",
            "creditAppNo": item_no,
            "userId": "16530278743892430040",
            "contractList": [{
                "contractType": "0007",
                # 文件base64编码
                "contractFile": "JVBER"
              },
              {
                "contractType": "0003",
                "contractFile": "JVBER"
              },
              {
                "contractType": "0002",
                "contractFile": "JVBER"
              },
              {
                "contractType": "0006",
                "contractFile": "JVBER"
              }
            ]
          }
        }
        self.update(api, body)


    def update_certificate_apply(self):
        '''
         结清证明申请
        :return:
        '''
        api = '/zhongzhirong/weipin_zhongwei/settlement.proof'
        body = {
              "code": 0,
              "message": "成功",
              "data": {
                "respCode": "000000",
                "respMessage": "访问成功",
                "content": None
              }
            }
        self.update(api, body)