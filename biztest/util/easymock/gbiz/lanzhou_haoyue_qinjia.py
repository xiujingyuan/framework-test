# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class LanzhouHaoyueQinjiaMock(Easymock):

    def update_loanbaseinfo_push(self):
        api = "/qingjia/lanzhou_haoyue_qinjia/loanBaseInfoPush"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "channel": "KN10001",
                    "sendflag": "01",
                    "sendmsg": "成功",
                    "sendcode": "0000",
                    "reqSuccess": true,
                    "bizSuccess": true,
                    "trancode": "QLZS000000001",
                    "transerno": "KN@id",
                    "respdate": "%s",
                    "resptime": "%s",
                    "transtate": "S",
                    "errocode": "000000",
                    "errormsg": "成功"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)


    def update_upload_file(self):
        api = "/qingjia/lanzhou_haoyue_qinjia/fileNotice"
        mode = '''{
            "code": 0,
            "message": "",
            "data": {
                "channel": "KN10001",
                "sendflag": "01",
                "sendmsg": null,
                "sendcode": "0000",
                "fileno": "983429940683812864",
                "reqSuccess": true,
                "bizSuccess": true,
                "trancode": "QLZS000000011",
                "transerno": "KN100012022060617592807331d742f8",
                "respdate": "20220606",
                "resptime": "175930",
                "transtate": "S",
                "errocode": "000000",
                "errormsg": "成功"
            }
        }'''
        self.update(api, mode)


    def update_creditapply_success(self):
        api = "/qingjia/lanzhou_haoyue_qinjia/route"
        mode = '''{
                      "code": 0,
                      "message": "",
                      "data": {
                        "channel": "KN10001",
                        "sendflag": "00",
                        "sendmsg": "路由处理中 ",
                        "sendcode": "0000",
                        "routerno": "@id",
                        "fundno": null,
                        "warrantno": null,
                        "warrantname": null,
                        "enddate": null,
                        "lendercardlist": null,
                        "repaycardlist": null,
                        "contractflag": null,
                        "reqSuccess": true,
                        "bizSuccess": false,
                        "trancode": "QLZS000000302",
                        "transerno": "KN@id",
                        "respdate": "%s",
                        "resptime": "%s",
                        "transtate": "S",
                        "errocode": "000000",
                        "errormsg": "成功"
                      }
                    }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_creditapplyquery_success(self, asset_info):
        api = "/qingjia/lanzhou_haoyue_qinjia/routeQuery"
        mode = '''{
                      "code": 0,
                      "message": "",
                      "data": {
                        "channel": "KN10001",
                        "sendflag": "01",
                        "sendmsg": "请求成功",
                        "sendcode": "0001",
                        "errocode": "000000",
                        "errormsg": "成功",
                        "routerno": function({
                      _req
                    }) {
                      return _req.body.routerno
                    },
                        "rate": "7.20",
                        "creditamt": "%s",
                        "fundno": "F011",
                        "warrantno": "R005",
                        "warrantname": "昊悦",
                        "enddate": "2024-06-15",
                        "contractflag": "02",
                        "lendercardlist": [{
                            "bankid": "102100099996",
                            "bankname": "中国工商银行"
                          }, {
                            "bankid": "103100000026",
                            "bankname": "中国农业银行"
                          }]
                        }
                      }''' % (asset_info['data']['asset']['amount'])
        self.update(api, mode)

    def update_loanapplytrial_success(self):
        api = "/qingjia/lanzhou_haoyue_qinjia/loanApplyTrial"
        mode = '''{
                    "code": 0,
                    "message": "",
                    "data": {
                        "channel": "KN10001",
                        "sendflag": null,
                        "sendmsg": null,
                        "sendcode": null,
                        "businessrate": "7.20",
                        "lprRate": "3.7",
                        "lprDate": "2022-04-20",
                        "reqSuccess": true,
                        "bizSuccess": false,
                        "trancode": "QLZS000000018",
                        "transerno": "KN@id",
                        "respdate": "%s",
                        "resptime": "%s",
                        "transtate": "S",
                        "errocode": "000000",
                        "errormsg": "成功"
                    }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_loanapplyconfirm_success(self):
        api = "/qingjia/lanzhou_haoyue_qinjia/loanApply"
        mode = '''{
                    "code": 0,
                    "message": "",
                    "data": {
                        "channel": "KN10001",
                        "sendflag": "00",
                        "sendmsg": null,
                        "sendcode": "0000",
                        "merserno": function({
                      _req
                    }) {
                      return _req.body.merserno
                    },
                        "reqSuccess": true,
                        "bizSuccess": false,
                        "trancode": "QLZS000000004",
                        "transerno": "KN@id",
                        "respdate": "%s",
                        "resptime": "%s",
                        "transtate": "S",
                        "errocode": "000000",
                        "errormsg": "成功"
                    }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_loanapplyconfirmquery_success(self, asset_info):
        api = "/qingjia/lanzhou_haoyue_qinjia/loanQuery"
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
                    "contractno": "C@id",
                    "loanno": "L@id", //存入due_bill_no
                    "loanamt": %s,
                    "loanblance": %s,
                    "loanpayway": "2",
                    "loanyrate": 7.2,
                    "loanstartdate": "%s",
                    "loanenddate": "%s",
                    "reqSuccess": true,
                    "bizSuccess": true,
                    "trancode": "QLZS000000013",
                    "transerno": "KN@id",
                    "respdate": "%s",
                    "resptime": "%s",
                    "transtate": "S",
                    "errocode": "000000",
                    "errormsg": "成功"
                  }
                }''' % (asset_info['data']['asset']['amount'], asset_info['data']['asset']['amount'],
                        get_date(fmt="%Y-%m-%d"), get_date(month=12, fmt="%Y-%m-%d"), get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_queryrepayplan_success(self, asset_info):
        api = "/qingjia/lanzhou_haoyue_qinjia/repayPlanQuery"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        respdate = get_date(fmt="%Y%m%d")
        resptime = get_date(fmt="%H%M%S")
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
                    "loanno": None,
                    "merserno": "KN10001202206028afac47c42",
                    "loanamt": asset_info['data']['asset']['amount'],
                    "paymentschedule": {
                      "payment_schedule": [],
                      "feeplanlist": []
                    },
                    "reqSuccess": True,
                    "bizSuccess": True,
                    "trancode": "QLZS000000010",
                    "transerno": "KN@id",
                    "respdate": respdate,
                    "resptime": resptime,
                    "transtate": "S",
                    "errocode": "000000",
                    "errormsg": "errormsg"
                  }
                }
        repayment_plan_tmp = {
                  "tpnum": 1,
                  "loanenddate": "2022-07-02",
                  "settledate": "2022-07-02",
                  "payprinciaalamt": 806.19,
                  "actualpayprincipalamt": 0,
                  "payinterestamt": 60,
                  "actualpayinterestamt": 0,
                  "payprincipalpenaltyamt": 0,
                  "actualpayprincipalpenaltyamt": None,
                  "ispreps": "0",
                  "payfeetotal": "0",
                  "actualfeetotal": "0"
                }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['tpnum'] = i + 1
            repayment_plan['loanenddate'] = fee_info['date'].replace("-", "")
            repayment_plan['settledate'] = fee_info['date'].replace("-", "")
            repayment_plan['payprinciaalamt'] = float(fee_info['principal']) / 100
            repayment_plan['payinterestamt'] = float(fee_info['interest']) / 100
            mode['data']['paymentschedule']['payment_schedule'].append(repayment_plan)
        self.update(api, mode)

    def update_repayplanpush_success(self):
        api = "/qingjia/lanzhou_haoyue_qinjia/repayPlanSync"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "channel": "KN10001",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "sendcode": "0000",
                    "reqSuccess": true,
                    "bizSuccess": true,
                    "trancode": "QLZS000000100",
                    "transerno": "KN@id",
                    "respdate": "%s",
                    "resptime": "%s",
                    "transtate": "S",
                    "errocode": "000000",
                    "errormsg": "请求成功"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_loancreditquery_fail(self):
        api = "/qingjia/lanzhou_haoyue_qinjia/routeQuery"
        mode = '''{
                "code": 0,
                "message": "",
                "data": {
                    "channel": "KN10001",
                    "sendflag": "02",
                    "sendmsg": "测试mock",
                    "sendcode": "9999",
                    "routerno": null,
                    "rate": null,
                    "creditamt": null,
                    "fundno": null,
                    "warrantno": null,
                    "warrantname": null,
                    "enddate": null,
                    "contractflag": null,
                    "lendercardlist": null,
                    "repaycardlist": null,
                    "reqSuccess": true,
                    "bizSuccess": false,
                    "trancode": "QLZS000000303",
                    "transerno": "KN@id",
                    "respdate": "%s",
                    "resptime": "%s",
                    "transtate": "S",
                    "errocode": "000000",
                    "errormsg": "成功"
                }
            }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)


    def update_loanapplyconfirmquery_fail(self):
        api = "/qingjia/lanzhou_haoyue_qinjia/loanQuery"
        mode = '''{
            "code": 0,
            "message": "",
            "data": {
                "channel": "KN10001",
                "sendflag": "02",
                "sendmsg": "此产品暂不支持当前利率",
                "sendcode": "0007",
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
                "reqSuccess": true,
                "bizSuccess": false,
                "trancode": "QLZS000000013",
                "transerno": "KN@id",
                "respdate": "%s",
                "resptime": "%s",
                "transtate": "S",
                "errocode": "000000",
                "errormsg": "成功"
            }}''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)


    def update_loanapplytrial_other_rate_success(self, rate):
        api = "/qingjia/lanzhou_haoyue_qinjia/loanApplyTrial"
        mode = '''{
                    "code": 0,
                    "message": "",
                    "data": {
                        "channel": "KN10001",
                        "sendflag": null,
                        "sendmsg": null,
                        "sendcode": null,
                        "businessrate": "%s",
                        "lprRate": "3.7",
                        "lprDate": "2022-04-20",
                        "reqSuccess": true,
                        "bizSuccess": false,
                        "trancode": "QLZS000000018",
                        "transerno": "KN@id",
                        "respdate": "%s",
                        "resptime": "%s",
                        "transtate": "S",
                        "errocode": "000000",
                        "errormsg": "成功"
                    }
                }''' % (rate, get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)

    def update_loanapplyconfirmquery_other_rate_success(self, asset_info, rate):
        api = "/qingjia/lanzhou_haoyue_qinjia/loanQuery"
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
                    "contractno": "C@id",
                    "loanno": "L@id", //存入due_bill_no
                    "loanamt": %s,
                    "loanblance": %s,
                    "loanpayway": "2",
                    "loanyrate": %s,
                    "loanstartdate": "%s",
                    "loanenddate": "%s",
                    "reqSuccess": true,
                    "bizSuccess": true,
                    "trancode": "QLZS000000013",
                    "transerno": "KN@id",
                    "respdate": "%s",
                    "resptime": "%s",
                    "transtate": "S",
                    "errocode": "000000",
                    "errormsg": "成功"
                  }
                }''' % (asset_info['data']['asset']['amount'], asset_info['data']['asset']['amount'], rate,
                        get_date(fmt="%Y-%m-%d"), get_date(month=12, fmt="%Y-%m-%d"), get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)



    def update_certificateapply_success(self):
        '''
        申请结清证明
        '''
        api = "/qingjia/lanzhou_haoyue_qinjia/certificateApply"
        mode = '''{
                  "code": 0,
                  "message": "",
                  "data": {
                    "channel": "KN10001",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "sendcode": "00",
                    "reqSuccess": true,
                    "bizSuccess": true,
                    "trancode": "QLZS000000110",
                    "transerno": "KN@id",
                    "respdate": "%s",
                    "resptime": "%s",
                    "transtate": "S",
                    "errocode": "000000",
                    "errormsg": "成功"
                  }
                }''' % (get_date(fmt="%Y%m%d"), get_date(fmt="%H%M%S"))
        self.update(api, mode)


    def update_certificatedownload_success(self):
        api = "/qingjia/lanzhou_haoyue_qinjia/certificateDownload"
        mode = {
                  "code": 0,
                  "message": "",
                  "data": {
                    "channel": "KN10001",
                    "sendflag": "01",
                    "sendmsg": "处理成功",
                    "sendcode": "00",
                    "fileurl": "http://paydayloandevv4-1251122539.cossh.myqcloud.com/20190422/e43d5bb369463bdbb36c4bdda2c086ef.pdf",
                    "reqSuccess": True,
                    "bizSuccess": True,
                    "trancode": "QLZS000000111",
                    "transerno": "KN@id",
                    "respdate": get_date(fmt="%Y%m%d"),
                    "resptime": get_date(fmt="%H%M%S"),
                    "transtate": "S",
                    "errocode": "000000",
                    "errormsg": "成功"
                  }
                }
        self.update(api, mode)

if __name__ == "__main__":
    pass
