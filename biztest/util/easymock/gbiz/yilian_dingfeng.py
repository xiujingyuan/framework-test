# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from copy import deepcopy
from biztest.util.tools.tools import get_guid, get_date


class YilianDingfengMock(Easymock):

    def update_ftp_upload_success(self):
        api = "/capital/ftp/upload/:channel"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "dir": "/10002/20210531/S2021053130647355554/",
            "name": "01_kn_qyd_S2021053130647355554_guarantee.pdf",
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
        self.update(api, mode)

    def update_file_notice(self):
        api = "/qingjia/yilian_dingfeng/fileNotice"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "channel": "KN10001",
            "sendflag": "01",
            "sendmsg": null,
            "sendcode": "0000",
            "fileno": "3290321377324",
            "errocode": "000000",
            "errormsg": "成功"
          }
        }'''
        self.update(api, mode)

    def update_customer_info_push(self):
        api = "/qingjia/yilian_dingfeng/loanBaseInfoPush"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "channel": "KN10001",
            "sendflag": "01",
            "sendmsg": "成功",
            "sendcode": "0000",
            "errocode": "000000",
            "errormsg": "成功"
          }
        }'''
        self.update(api, mode)

    def update_creditapply_success(self):
        api = "/qingjia/yilian_dingfeng/route"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "channel": "KN10001",
            "sendflag": "00",
            "sendmsg": "路由处理中 ",
            "sendcode": "0000",
            "routerno": "route_%s",
            "fundno": null,
            "warrantno": null,
            "warrantname": null,
            "enddate": null,
            "lendercardlist": null,
            "repaycardlist": null,
            "contractflag": null,
            "errocode": "000000",
            "errormsg": "成功"
          }
        }''' % get_guid()
        self.update(api, mode)

    def update_creditapply_fail(self):
        api = "/qingjia/yilian_dingfeng/route"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "channel": "KN10001",
            "sendflag": "02",
            "sendmsg": "银行风控拒绝 ",
            "sendcode": "0005",
            "routerno": null,
            "fundno": null,
            "warrantno": null,
            "warrantname": null,
            "enddate": null,
            "lendercardlist": null,
            "repaycardlist": null,
            "contractflag": null,
            "errocode": "000000",
            "errormsg": "成功"
          }
        }'''
        self.update(api, mode)

    def update_credit_query_success(self):
        api = "/qingjia/yilian_dingfeng/routeQuery"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "channel": "KN10001",
            "sendflag": "01",
            "sendmsg": "路由成功",
            "sendcode": "0001",
            "routerno": function({
                      _req
                    }) {
                      return _req.body.routerno
                    },
            "rate": null,
            "creditamt": "20000.00",
            "fundno": "F003",
            "warrantno": "R002",
            "warrantname": "云南鼎丰",
            "enddate": "2022-10-16",
            "contractflag": "01",
            "lendercardlist": [],
            "errocode": "000000",
            "errormsg": "成功"
          }
        }'''
        self.update(api, mode)

    def update_credit_query_fail(self):
        api = "/qingjia/yilian_dingfeng/routeQuery"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "channel": "KN10001",
                    "sendflag": "02",
                    "sendmsg": "银行风控拒绝",
                    "sendcode": "0005",
                    "routerno": function({
                              _req
                            }) {
                              return _req.body.routerno
                            },
                    "errocode": "000000",
                    "errormsg": "成功"
                  }
                }'''
        self.update(api, mode)

    def update_loan_apply(self):
        api = "/qingjia/yilian_dingfeng/loanApply"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "channel": "KN10001",
            "sendflag": "00",
            "sendmsg": "处理中 ",
            "sendcode": "0000",
            "merserno": function({
                      _req
                    }) {
                      return _req.body.merserno
                    },
            "trancode": "QLZS000000302",
            "transerno": "KN10001202204183e9940",
            "respdate": "20220418",
            "resptime": "161843",
            "transtate": "S",
            "errocode": "000000",
            "errormsg": "成功"
          }
        }'''
        self.update(api, mode)

    def update_loan_query_success(self, asset_info):
        api = "/qingjia/yilian_dingfeng/loanQuery"
        mode = '''{
          "code": 0,
          "message": "",
          "data": {
            "channel": "KN10001",
            "sendflag": "01",
            "sendmsg": "",
            "sendcode": "0001",
            "merserno": function({
                      _req
                    }) {
                      return _req.body.merserno
                    },
            "contractno": "contract_01",
            "loanno": "loanno_%s",
            "loanamt": %s,
            "loanblance": 2000,
            "loanpayway": "",
            "loanyrate": 8.5,
            "loanstartdate": "%s",
            "loanenddate": "2023-04-18",
            "errocode": "000000",
            "errormsg": "成功"
          }
        }'''% (get_guid(),
                asset_info['data']['asset']['amount'],
                get_date(fmt="%Y-%m-%d"))
        self.update(api, mode)

    def update_loan_query_fail(self):
        api = "/qingjia/yilian_dingfeng/loanQuery"
        mode = '''{
            "code": 0,
            "message": "",
            "data": {
                "channel": "KN10001",
                "sendflag": "02",
                "sendmsg": "交易处理失败",
                "sendcode": "0006",
                "merserno": function({
                      _req
                    }) {
                      return _req.body.merserno
                    },
                "contractno": null,
                "loanno": null,
                "loanamt": null,
                "loanblance": null,
                "loanpayway": null,
                "loanyrate": null,
                "loanstartdate": null,
                "loanenddate": null,
                "errocode": "000000",
                "errormsg": "成功"
            }
        }'''
        self.update(api, mode)

    def update_repay_plan(self, asset_info):
        api = "/qingjia/yilian_dingfeng/repayPlanQuery"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
            "code": 0,
            "message": "",
            "data": {
                "channel": "KN10001",
                "sendflag": "01",
                "sendmsg": "处理成功",
                "sendcode": "0000",
                "totalnum": asset_info['data']['asset']['period_count'],
                "retnum": asset_info['data']['asset']['period_count'],
                "loanno": "YLQINJQB20220425175900361053",
                "loanamt": asset_info['data']['asset']['amount'],
                "paymentschedule": {
                    "payment_schedule": [],
                    "feeplanlist": []
                },
                "errocode": "000000",
                "errormsg": "成功"
            }
        }
        repayment_plan_tmp = {
            "tpnum": 12,
            "loanenddate": "2023-04-25",
            "settledate": "",
            "payprinciaalamt": 259.81,
            "actualpayprincipalamt": 0,
            "payinterestamt": 1.85,
            "actualpayinterestamt": 0,
            "payprincipalpenaltyamt": 0,
            "actualpayprincipalpenaltyamt": 0,
            "ispreps": "0",
            "payfeetotal": "0.0",
            "actualfeetotal": "0.0"
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['tpnum'] = i + 1
            repayment_plan['payprinciaalamt'] = float(fee_info['principal']) / 100
            repayment_plan['payinterestamt'] = float(fee_info['interest']) / 100
            repayment_plan['loanenddate'] = fee_info['date'].replace("-", "")
            mode['data']['paymentschedule']['payment_schedule'].append(repayment_plan)
        self.update(api, mode)

    def update_certificate_apply(self):
        api = '/qingjia/yilian_dingfeng/certificateApply'
        body ={
            "code": 0,
            "message": "",
            "data": {
                "channel": "KN10001",
                "sendflag": "01",
                "sendmsg": "处理成功",
                "sendcode": "true",
                "bizSuccess": True,
                "reqSuccess": True,
                "trancode": "QLZS000000110",
                "transerno": "KN100012022072617211040592e8b9aa",
                "respdate": "20220726",
                "resptime": "172110",
                "transtate": "S",
                "errocode": "000000",
                "errormsg": "成功"
            }
        }
        self.update(api, body)

    def update_certificate_download(self):
        api = '/qingjia/yilian_dingfeng/certificateDownload'
        body ={
          "code": 0,
          "message": "",
          "data": {
            "channel": "KN10001",
            "sendflag": "01",
            "sendmsg": "处理成功",
            "sendcode": "00",
              # 这个地址是随便放的一个，资方测试环境提供的有时效
            "fileurl": "http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ229035220721181651.pdf",
            "bizSuccess": True,
            "reqSuccess": True,
            "trancode": "QLZS000000111",
            "transerno": "KN10001202207261755293034943e904",
            "respdate": "20220726",
            "resptime": "175529",
            "transtate": "S",
            "errocode": "000000",
            "errormsg": "成功"
          }
        }
        self.update(api, body)