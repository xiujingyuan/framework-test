# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import get_date


class HebeiJiahexingTsMock(Easymock):

    def update_ftp_upload_success(self):
        api = "/capital/ftp/upload/:channel"
        body = '''{
          "code": 0,
          "message": "",
          "data": {
            "dir": "/sftp/10010/SX/20230131/",
            "name": "ccaW2022041675144779.zip",
            "type": null,
            "result": {
              "code": 0,
              "message": "成功"
            }
          },
          "_req.path": function({
            _req
          }) {
            return _req.path
          }
        }'''
        self.update(api, body)

    def update_file_notice(self):
      api = '/zhongke/hebei_jiahexing_ts/channelfilesyncnotice'
      body = {
          "code": 0,
          "message": "success",
          "data": {
            "transdate": "20230131",
            "transtime": "140927",
            "respcode": "0000",
            "respmesg": "交易接收成功",
            "tradeserialno": "@id"
          }
        }
      self.update(api, body)

    def update_credit_apply(self, itemno, respcode='0000', respmesg='交易接收成功'):
        api = '/zhongke/hebei_jiahexing_ts/creditapply'
        body = {
          "code": 0,
          "message": "success",
          "data": {
            "applyno": "1040123" + itemno, #资方返回格式为：10401232023013100000000100001902
            "transdate": "20230131",
            "transtime": "140618",
            "respcode": respcode,
            "respmesg": respmesg,
            "tradeserialno": "@id"   # 资方返回格式为：c73207c09762427cb6b4fe619fcbcb48
          }
        }
        self.update(api, body)


    def update_credit_query(self, itemno, respcode='9999', respmesg='交易处理成功', result='1'):
        api = '/zhongke/hebei_jiahexing_ts/creditquery'
        body = {
          "code": 0,
          "message": "success",
          "data": {
            "channelserialno": "ca" + itemno,
            "applyno": "1040123" + itemno,
            "result": result,
            "time": get_date(fmt="%Y%m%d%H%M%S"),
            "amt": 8000,
            "bankid": "HEBEI",
            "expiredate": get_date(month=12, fmt="%Y%m%d"),
            "bankorderno": "504404" + itemno, #签借款合同会用到这个参数
            "transdate": get_date(fmt="%Y%m%d"),
            "transtime": get_date(fmt="%H%M%S"),
            "respcode": respcode,
            "respmesg": respmesg,
            "tradeserialno": "、@id" #资方返回格式为：c475bd4a8bf54589a0f7662b09fc2653
          }
        }
        self.update(api, body)

    def update_credit_query_notorder(self):
      api = '/zhongke/hebei_jiahexing_ts/creditquery'
      body = {
        "code": 0,
        "message": "success",
        "data": {
          "transdate": get_date(fmt="%Y%m%d"),
          "transtime": get_date(fmt="%H%M%S"),
          "respcode": "1000",
          "respmesg": "查无此交易",
          "tradeserialno": "@id"
        }
      }
      self.update(api, body)

    def update_loan_apply(self, respcode='0000', respmesg='交易接收成功'):
        api = '/zhongke/hebei_jiahexing_ts/loanapply'
        body = {
          "code": 0,
          "message": "success",
          "data": {
            "transdate": get_date(fmt="%Y%m%d"),
            "transtime": get_date(fmt="%H%M%S"),
            "respcode": respcode,
            "respmesg": respmesg,
            "tradeserialno": "@id"
          }
        }
        self.update(api, body)

    def update_loan_query(self,itemno, respcode='9999', respmesg='交易处理成功', status='1'):
        api = '/zhongke/hebei_jiahexing_ts/loanquery'
        body = {
          "code": 0,
          "message": "success",
          "data": {
            "loanserialno": "la" + itemno,
            "applyno": "1040123" + itemno,
            "status": status,
            "loantime": get_date(fmt="%Y%m%d%H%M%S"),
            "amt": 8000,
            "loanno": "loanno" + itemno,  #资方返回格式为：504404153301955746
            "repayplan": [ #此处返回的还款计划暂时没有用到
            ],
            "transdate": get_date(fmt="%Y%m%d"),
            "transtime": get_date(fmt="%H%M%S"),
            "respcode": respcode,
            "respmesg": respmesg,
            "tradeserialno": "@id"
          }
        }
        self.update(api, body)

    def update_loan_query_notorder(self):
        api ='/zhongke/hebei_jiahexing_ts/loanquery'
        body = {
            "code": 0,
            "message": "success",
            "data": {
                "transdate": get_date(fmt="%Y%m%d"),
                "transtime": get_date(fmt="%H%M%S"),
                "respcode": "1000",
                "respmesg": "查无此交易",
                "tradeserialno": "@id"
            }
        }
        self.update(api, body)

    def update_repayplan_query(self, itemno, asset_info):
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        api = '/zhongke/hebei_jiahexing_ts/repayplanquery'
        body = {
          "code": 0,
          "message": "success",
          "data": {
            "loanno": "loanno" + itemno,
            "applyno": "1040123" + itemno,
            "totalnum": 12,
            "curter": 1,
            "payschedule": [],
            "transdate": get_date(fmt="%Y%m%d"),
            "transtime": get_date(fmt="%Y%m%d"),
            "respcode": "9999",
            "respmesg": "交易处理成功",
            "tradeserialno": "@id"
          }
        }

        payschedule = {
                "planno": "@id",
                "term": 1,
                "enddt": "20440515",
                "prinlamt": 647.04,
                "actualprinlamt": 0,
                "intamt": 43.33,
                "actualintamt": 0,
                "prinlpenaltyamt": 0,
                "actualprinlpenaltyamt": 0,
                "ispreps": "0",
                "feetotal": 0,
                "actualfeetotal": 0,
                "shouldpayduepremium": 0,
                "actualpayduepremium": 0
              }
        for i in range(asset_info['data']['asset']['period_count']):
          fee_info = get_fee_info_by_period(rate_info, i + 1)
          repayment_plan = deepcopy(payschedule)
          repayment_plan['term'] = i + 1
          repayment_plan['prinlamt'] = float(fee_info['principal'])/100
          repayment_plan['intamt'] = float(fee_info['interest'])/100
          repayment_plan['enddt'] = str(fee_info['date']).replace('-', '')
          body['data']['payschedule'].append(repayment_plan)
        self.update(api, body)

    def update_certificate_apply(self):
        api = '/zhongke/hebei_jiahexing_ts/settlecertifyapply'
        body = {
                  "code": 0,
                  "message": "success",
                  "data": {
                    "transdate": "20230508",
                    "transtime": "102625",
                    "respcode": "0000",
                    "respmesg": "交易接收成功",
                    "tradeserialno": "4daa1865cbfa4a579480f86ca1e316e6"
                  }
                }
        self.update(api, body)
