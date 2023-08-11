# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class ZhongkeHegangMock(Easymock):

    def update_creditapply_success(self):
        api = "/hegang/creditApply/:productCode"
        mode = '''{
                  "respCode": "0000",
                  //成功：respCode=0000/9999/1100
                  //失败：respCode=9000；其他都重试
                  "respMesg": "zhizhi mock 测试",
                  "transDate": "%s",
                  "transTime": "%s"
                }
                ''' % (get_date(fmt="%Y-%m-%d"), get_date(fmt="%H:%M:%S"))
        self.update(api, mode)

    def update_creditapply_fail(self):
        api = "/hegang/creditApply/:productCode"
        mode = ''' {
                        "respCode": "9000",
                          //成功：respCode=0000/9999/1100
                         //失败：respCode=9000；其他都重试
                        "respMesg": "授信申请失败",
                        "transDate": "%s",
                        "transTime": "%s"
                    }
                   ''' % (get_date(fmt="%Y-%m-%d"), get_date(fmt="%H:%M:%S"))
        self.update(api, mode)


    def update_creditquery_success(self, asset_info):
        api = "/hegang/creditQuery/:productCode"
        transdate = get_date(fmt="%Y-%m-%d")
        transtime = get_date(fmt="%H:%M:%S")
        time = get_date(fmt="%Y-%m-%d %H:%M:%S")
        amount = asset_info['data']['asset']['amount']
        mode = '''{
                  "transDate": "%s",
                  "transTime": "%s",
                  "respCode": "9999",
                    //成功：respCode=9999 +result= 1 
                    //失败：respCode=9000/9999 +result= 0；其他组合重试
                  "respMesg": "交易处理成功",
                  "hzfSerialNo": function({
                    _req
                  }) {
                    return _req.body.hzfSerialNo
                  },
                  "result": "1", //1 通过 0 拒绝
                  "time": "%s",
                  "remark": null,
                  "rejectCode": "",
                  "amount": %s,
                  "creditQueryStatus": "01",
                  "creditScoreData": "",
                  "creditLoseDate": null,
                  "riskModelData": null,
                  "validHzfSerialNo": null,
                  "certNo": "%s",
                  "custName": "%s",
                  "certType": "SF",
                  "agreementNo": null,
                  "certEndDate": "2037-12-04",
                  "mobilePhone": "%s"
                }''' % (transdate, transtime, time, amount, asset_info['data']['borrower']['idnum_encrypt'],
                        asset_info['data']['borrower']['name_encrypt'], asset_info['data']['borrower']['tel_encrypt'])
        self.update(api, mode)

    def update_creditquery_fail(self, asset_info):
        api = "/hegang/creditQuery/:productCode"
        transdate = get_date(fmt="%Y-%m-%d")
        transtime = get_date(fmt="%H:%M:%S")
        time = get_date(fmt="%Y-%m-%d %H:%M:%S")
        amount = asset_info['data']['asset']['amount']
        mode = '''{
                  "transDate": "%s",
                  "transTime": "%s",
                  "respCode": "9000",
                  "respMesg": "交易处理失败",
                    //成功：respCode=9999 +result= 1 
                    //失败：respCode=9000/9999 +result= 0；其他组合重试
                  "hzfSerialNo": function({
                    _req
                  }) {
                    return _req.body.hzfSerialNo
                  },
                  "result": "0", //1 通过 0 拒绝
                  "time": "%s",
                  "remark": null,
                  "rejectCode": "",
                  "amount": %s,
                  "creditQueryStatus": "01",
                  "creditScoreData": "",
                  "creditLoseDate": null,
                  "riskModelData": null,
                  "validHzfSerialNo": null,
                  "certNo": "%s",
                  "custName": "%s",
                  "certType": "SF",
                  "agreementNo": null,
                  "certEndDate": "2037-12-04",
                  "mobilePhone": "%s"
                }''' % (transdate, transtime, time, amount, asset_info['data']['borrower']['idnum_encrypt'],
                        asset_info['data']['borrower']['name_encrypt'], asset_info['data']['borrower']['tel_encrypt'])
        self.update(api, mode)

    def update_useapply_success(self):
        api = "/hegang/useApply/:productCode"
        mode = '''{
                  "respCode": "0000", //成功0000、9999，其他都重试
                  "respMesg": "zhizhi 用款申请 mock 测试",
                  "transDate": "%s",
                  "transTime": "%s"
                } ''' % (get_date(fmt="%Y-%m-%d"), get_date(fmt="%H:%M:%S"))
        self.update(api, mode)



    def update_loanquery_success(self, asset_info):
        api = "/hegang/loanQuery/:productCode"
        transDate = get_date(fmt="%Y-%m-%d")
        transTime = get_date(fmt="%H:%M:%S")
        loanTime = get_date(fmt="%Y-%m-%d %H:%M:%S")
        amount = asset_info['data']['asset']['amount']
        mode = '''{
                  "amount": %s,
                  //成功：respCode=9999 + status=1 + transStatus=1
                  //失败：
                 // respCode=9999 + status=0+transStatus=0-----资金方返回的失败组合
                  "caseStatus": "0",
                  "folatPoint": 3,
                  "loanNo": "Test@id", //我方的alr_no
                  "loanSerialNo": function({
                    _req
                  }) {
                    return _req.body.loanSerialNo
                  }, //对应我方的trade_no
                  "loanTime": "%s",
                  "lprRate": 4,
                  "ovRate": 7,
                  "rate": 7,
                  "repayPlan": [],//不校验该字段，可以为空也可以不为空
                  "respCode": "9999",
                  "respMesg": "交易处理成功", 
                  "status": "1",//1 成功 0 失败
                  "transAmount": %s,
                  "transDate": "%s",
                  "transStatus": "1",//1 成功 0 失败
                  "transTime": "%s"
                }''' % (amount, loanTime, amount, transDate, transTime)
        self.update(api, mode)

    def update_loanquery_fail(self, asset_info):
        api = "/hegang/loanQuery/:productCode"
        transDate = get_date(fmt="%Y-%m-%d")
        transTime = get_date(fmt="%H:%M:%S")
        loanTime = get_date(fmt="%Y-%m-%d %H:%M:%S")
        mode = '''{
            "amount": 0,
            "caseStatus": "0",
            "exceptionCode": "E012",
            "exceptionMsg": "暂不支持该卡号",
            "loanSerialNo": function({_req}) {return _req.body.loanSerialNo}, //对应我方的trade_no
            "loanTime": "%s",
            "remark": "未查询到卡bin信息",
            "repayPlan": [ ],
            "respCode": "9000",
            "respMesg": "交易处理失败",
            "status": "0",
            "transDate": "%s",
            "transStatus": "0",
            "transTime": "%s"
        }''' % (loanTime, transDate, transTime)
        self.update(api, mode)

    def update_repay_plan_query_success(self, asset_info):
        api = "/hegang/repayPlanQuery/:productCode"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        loanserialno = alr_info[0]['asset_loan_record_trade_no']
        transDate = get_date(fmt="%Y-%m-%d")
        transTime = get_date(fmt="%H:%M:%S")
        mode = {
                  "installmentNo": 1,
                  "loanSerialNo": loanserialno,
                  "respCode": "9999",
                  "respMesg": "交易处理成功",
                  "totalInstallmentNo": 12,
                  "transDate": transDate,
                  "transTime": transTime,
                  "repayPlan": []
                }
        repayment_plan_tmp = {
                  "agreedFee": 0,
                  "agreedInterest": 46.67,
                  "agreedOInterest": 0,
                  "agreedPenaltyFee": 0,
                  "agreedPrincipal": 645.54,
                  "agreedRepaymentDate": "2021-04-04",
                  "paidFee": 0,
                  "paidInterest": 0,
                  "paidOInterest": 0,
                  "paidPenaltyFee": 0,
                  "paidPrincipal": 0,
                  "remark": "",
                  "termNo": 1
                }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['termNo'] = i + 1
            repayment_plan['agreedPrincipal'] = float(fee_info['principal']) / 100
            repayment_plan['agreedInterest'] = float(fee_info['interest']) / 100
            repayment_plan['agreedRepaymentDate'] = fee_info['date']
            mode['repayPlan'].append(repayment_plan)
        self.update(api, mode)

    def update_upload_success(self):
        api = "/hegang/uploadFiles/:productCode"
        mode = '''{
                  "code": 0,
                  "message": "附件上传成功",
                  "data": null
                }'''
        self.update(api, mode)

    def update_file_sync_notify_success(self):
        api = "/hegang/channelSyncNotice/:productCode"
        mode = '''{
          "transDate": "2021-04-30",
          "transTime": "15:41:57",
          "respCode": "9999",
          "respMesg": "交易处理成功"
        }'''
        self.update(api, mode)

    def update_certificate_apply(self):
        api = "/hegang/loanFinishApply/:productCode"
        mode = {
              "respCode": "0000",
              "respMesg": "交易接收成功",
              "transDate": "2022-07-27",
              "transTime": "18:55:09"
            }
        self.update(api, mode)

    def update_certificate_download(self, item_no):
        alr_info=get_asset_loan_record_by_item_no(item_no)
        loanserialno = alr_info[0]['asset_loan_record_due_bill_no']
        api = "/hegang/loanFinishQuery/:productCode"
        mode = {
              "loanFinishName": "宿金凤_结清凭证_HT332704000000065.pdf",
              "loanFinishPath": "/download/20220727/11003/loanFinish",
              "loanNo": loanserialno,
              "respCode": "9999",
              "respMesg": "交易处理成功",
              "status": "1",
              "transDate": "2022-07-27",
              "transTime": "18:58:28"
            }
        self.update(api, mode)


if __name__ == "__main__":
    pass
