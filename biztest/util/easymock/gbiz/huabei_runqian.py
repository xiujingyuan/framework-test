# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy


class HhabeirunqianMock(Easymock):
    def update_apply_success(self):
        api = "/huabei/loan-apply"
        mode = '''{
          "errcode": "0",
          "errmsg": "进件成功"
        }'''
        self.update(api, mode)

    def update_apply_fail(self):
        api = "/huabei/loan-apply"
        mode = '''{
          "errcode": "-1",
          "errmsg": "进件失败"
        }'''
        self.update(api, mode)

    def update_apply_exist(self):
        api = "/huabei/loan-apply"
        mode = '''{
          "errcode": "-1",
          "errmsg": "订单编号已存在"
        }'''
        self.update(api, mode)

    def update_audit_success(self, asset_info):
        api = "/huabei/loan-audit-result-query"
        mode = '''{
                  "errcode": "0",
                  "errmsg": "成功",
                  "traceId": "124.119.15880430322617381",
                  "data": {
                    "orderNum": "%s",
                    "businessNum": "cs_@id",//存入asset_loan_record_trade_no
                    "cusNum": function({
                      _req
                    }) {
                      return _req.query.cusNum
                    },
                    "customerNum": "A01P20032702927",
                    "customerName": null,
                    "approvalOpinion": "",
                    "approvalCode": "01"
                  }
                }''' % (asset_info['data']['asset']['item_no'])
        self.update(api, mode)

    def update_audit_fail(self, asset_info):
        api = "/huabei/loan-audit-result-query"
        mode = '''{
          "errcode": "0",
          "errmsg": "成功",
          "traceId": "124.119.15880430322617381",
          "data": {
            "orderNum": "%s",
            "businessNum": "",
            "cusNum": function({
              _req
            }) {
              return _req.query.cusNum
            },
            "customerNum": "A01P20032702927",
            "customerName": null,
            "approvalOpinion": "审核失败",
            "approvalCode": "03"
          }
        }''' % (asset_info['data']['asset']['item_no'])
        self.update(api, mode)


    def update_audit_wait(self):
        api = "/huabei/loan-audit-result-query"
        mode = '''{
          "errcode": "-1",
          "errmsg": "查询失败"
        }'''
        self.update(api, mode)

    def update_loan_success(self, asset_info):
        api = "/huabei/loan-result-query"
        mode = '''{
          "errcode": "0",
          "errmsg": "成功",
          "traceId": "124.132.15880430326047347",
          "data": {
            "orderNum": "%s",//与我方资产编号校验
            "businessNum": "cs_@id", //存入due_bill_no
            "cusNum": "noenc_02_2846677820099790848_734",
            "customerNum": "A01P20032702927",
            "customerName": "%s",
            "certificateNum": "%s",
            "certificateType": "1",
            "productName": "快牛",
            "contractTotalAmt": 5000.0,//不校验这个参数
            "padUpAmt": %s,
            "contractSignDate": "@now",
            "channelCode": null,
            "applyDate": "",
            "dueNum": "YWNA0120032809550",
            "startDate": "2020-03-28", //不校验这个参数
            "expirationDate": "2020-09-28",//不校验这个参数
            "rateYear": 14.0,
            "pnlItr": 0.1,
            "repayDate": "",
            "loanDate": "@now",
            "approvalCode": "01"
          }
        }
        ''' % (asset_info['data']['asset']['item_no'], asset_info['data']['borrower']['name_encrypt'], asset_info['data']['borrower']['idnum_encrypt'],
               asset_info['data']['asset']['amount'])
        self.update(api, mode)

    def update_loan_fail(self, asset_info):
        api = "/huabei/loan-result-query"
        mode = '''{
          "errcode": "0",
          "errmsg": "成功",
          "traceId": "124.132.15880430326047347",
          "data": {
            "orderNum": "%s",//与我方资产编号校验
            "businessNum": "", 
            "cusNum": "noenc_02_2846677820099790848_734",
            "customerNum": "A01P20032702927",
            "customerName": "%s",
            "certificateNum": "%s",
            "certificateType": "1",
            "productName": "快牛",
            "contractTotalAmt": 5000.0,//不校验这个参数
            "padUpAmt": 8000.0,
            "contractSignDate": "2020-03-28",
            "channelCode": null,
            "applyDate": "",
            "dueNum": "YWNA0120032809550",
            "startDate": "2020-03-28",//不校验这个参数
            "expirationDate": "2020-09-28",//不校验这个参数
            "rateYear": 14.0,
            "pnlItr": 0.1,
            "repayDate": "",
            "loanDate": "",
            "approvalCode": "03"
          }
        }
        ''' % (asset_info['data']['asset']['item_no'],asset_info['data']['borrower']['name_encrypt'], asset_info['data']['borrower']['idnum_encrypt'])
        self.update(api, mode)

    def update_loan_wait(self):
        api = "/huabei/loan-result-query"
        mode = '''{
          "errcode": "-1",
          "errmsg": "查询失败"
        }
        '''
        self.update(api, mode)

    # def update_repayplan_success(self):
    #     api = "/huabeixiaodai_zhitou/loan-repaymentplans"
    #     mode = '''{
    #       "errcode": "0",
    #       "traceId": "124.121.15881271333568843",
    #       "data": [{
    #         "shouldRepaymentDate": "2020-04-28",
    #         "shouldRepaymentPrincipal": 1297.67,
    #         "periods": 1,
    #         "shouldRepaymentTotal": 1384.34,
    #         "repaymentStatus": "1",
    #         "shouldRepaymentInterest": 86.67
    #       }, {
    #         "shouldRepaymentDate": "2020-05-28",
    #         "shouldRepaymentPrincipal": 1311.73,
    #         "periods": 2,
    #         "shouldRepaymentTotal": 1384.34,
    #         "repaymentStatus": "1",
    #         "shouldRepaymentInterest": 72.61
    #       }, {
    #         "shouldRepaymentDate": "2020-06-28",
    #         "shouldRepaymentPrincipal": 1325.94,
    #         "periods": 3,
    #         "shouldRepaymentTotal": 1384.34,
    #         "repaymentStatus": "1",
    #         "shouldRepaymentInterest": 58.40
    #       }, {
    #         "shouldRepaymentDate": "2020-07-28",
    #         "shouldRepaymentPrincipal": 1340.31,
    #         "periods": 4,
    #         "shouldRepaymentTotal": 1384.34,
    #         "repaymentStatus": "1",
    #         "shouldRepaymentInterest": 44.03
    #       }, {
    #         "shouldRepaymentDate": "2020-08-28",
    #         "shouldRepaymentPrincipal": 1354.83,
    #         "periods": 5,
    #         "shouldRepaymentTotal": 1384.34,
    #         "repaymentStatus": "1",
    #         "shouldRepaymentInterest": 29.51
    #       }, {
    #         "shouldRepaymentDate": "2020-09-28",
    #         "shouldRepaymentPrincipal": 1369.52,
    #         "periods": 6,
    #         "shouldRepaymentTotal": 1384.34,
    #         "repaymentStatus": "1",
    #         "shouldRepaymentInterest": 14.82
    #       }]
    #     }
    #     '''
    #     self.update(api, mode)

    def update_repay_plan(self, asset_info):
        api = "/huabei/loan-repaymentplans"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
          "errcode": "0",
          "traceId": "124.121.15881271333568843",
          "data": []
        }
        repayment_plan_tmp = {
            "shouldRepaymentDate": "2020-09-28",
            "shouldRepaymentPrincipal": 1369.52,
            "periods": 6,
            "shouldRepaymentTotal": 1384.34,
            "repaymentStatus": "1",
            "shouldRepaymentInterest": 14.82
          }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['periods'] = i + 1
            repayment_plan['shouldRepaymentPrincipal'] = float(fee_info['principal']) / 100
            repayment_plan['shouldRepaymentInterest'] = float(fee_info['interest']) / 100
            repayment_plan['shouldRepaymentTotal'] = float('%.2f' % (repayment_plan['shouldRepaymentPrincipal'] + repayment_plan['shouldRepaymentInterest']))
            repayment_plan['shouldRepaymentDate'] = fee_info['date']
            mode['data'].append(repayment_plan)
        self.update(api, mode)

    def update_contract_success(self):
        api = "/huabei/loan-doc-path"
        mode = '''{
                  "errcode": "0",
                  "traceId": "1475.112.16232276839880889",
                  "data": [{
                    "businessNum": "2021HYXJ3672",
                    "fileInfos": [{
                        "docType": "9",
                        "path": "https://shuweicloud-stage.oss-cn-beijing.aliyuncs.com/jaWv/2021/06/09/335740239517598721.pdf?Expires=1623234884&OSSAccessKeyId=LTAIiONtvpEJZSea&Signature=htFZoQRdi8XcQ2lQ5CuxD34NzhU%3D"
                      },
                      {
                        "docType": "1",
                        "path": "https://shuweicloud-stage.oss-cn-beijing.aliyuncs.com/jaWv/2021/06/09/335740238120895492.pdf?Expires=1623234884&OSSAccessKeyId=LTAIiONtvpEJZSea&Signature=ALaJIKbgzMQ7rCP8ic4l0ogDBUE%3D"
                      },
                      {
                        "docType": "2",
                        "path": "https://shuweicloud-stage.oss-cn-beijing.aliyuncs.com/jaWv/2021/06/09/335740112476324873.pdf?Expires=1623234884&OSSAccessKeyId=LTAIiONtvpEJZSea&Signature=%2BL%2Btivk3eY%2F3rrCN3ySytAjGJ30%3D"
                      }
                    ]
                  }]
                }'''
        self.update(api, mode)


if __name__ == "__main__":
    pass
