# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy


class ShoujinMock(Easymock):
    def update_account_query_no_account(self):
        api = "/regOpenAccResult"
        mode = '''{
          "processType": "2",
          "idCardNo": "110200********7074",
          "channelCode": "0030",
          "status": "1",
          "realName": "*鹏",
          "msg": "待开户",
          "bankCardNo": "622846*********7025",
          "mobile": "132****6411"
        }
        // status：1-可提单，2-不可提单
        // msg：有感开户成功-开户成功，其他-未开户
        '''
        self.update(api, mode)

    def update_account_query_success(self):
        api = "/regOpenAccResult"
        mode = '''{
          "processType": "2",
          "idCardNo": "110200********7074",
          "channelCode": "0030",
          "status": "1",
          "realName": "*鹏",
          "msg": "有感开户成功",
          "bankCardNo": "622846*********7025",
          "mobile": "132****6411"
        }
        // status：1-可提单，2-不可提单
        // msg：有感开户成功-开户成功，其他-未开户
        '''
        self.update(api, mode)

    def update_account_query_fail(self):
        api = "/regOpenAccResult"
        mode = '''{
          "processType": "2",
          "idCardNo": "110200********7074",
          "channelCode": "0030",
          "status": "2",
          "realName": "*鹏",
          "msg": "四要素不一致",
          "bankCardNo": "622846*********7025",
          "mobile": "132****6411"
        }
        // status：1-可提单，2-不可提单
        // msg：有感开户成功-开户成功，其他-未开户
        '''
        self.update(api, mode)

    def update_upload_file_success(self):
        api = "/uploadFile/upload"
        data = '''function({_req}) {
            var data = {
              "id": "8a0bb89b705ce0190171776abbe500e8",
              "fileSize": 172,
              "downloadURL": "http://121.43.72.3:6060:6060/CnpayFileServer/commonAttach/download/8a0bb89b705ce0190171776abbe500e8.pdf",
              "fileName": "BIZ110771200414143901.pdf",
              "uuidName": "8a0bb89b705ce0190171776abbe500e8.pdf",
              "fileExt": "pdf",
              "success": true,
              "msg": "上传成功！",
              "accessURL": "http://121.43.72.3:6060:6060/CnpayFileServer/commonAttach/display/8a0bb89b705ce0190171776abbe500e8.pdf"
            };
            return JSON.stringify(data)
        }'''
        mode = '''{
            "code": 0,
            "message": "上传成功",
            "data": %s
        }// success：true-成功，false-失败
        ''' % data
        self.update(api, mode)

    def update_upload_file_fail(self):
        api = "/uploadFile/upload"
        data = '''function({_req}) {
            var data = {
              "id": "8a0bb89b705ce0190171776abbe500e8",
              "fileSize": 172,
              "downloadURL": "http://121.43.72.3:6060:6060/CnpayFileServer/commonAttach/download/8a0bb89b705ce0190171776abbe500e8.pdf",
              "fileName": "BIZ110771200414143901.pdf",
              "uuidName": "8a0bb89b705ce0190171776abbe500e8.pdf",
              "fileExt": "pdf",
              "success": false,
              "msg": "上传失败！",
              "accessURL": "http://121.43.72.3:6060:6060/CnpayFileServer/commonAttach/display/8a0bb89b705ce0190171776abbe500e8.pdf"
            };
            return JSON.stringify(data)
        }'''
        mode = '''{
            "code": 0,
            "message": "上传成功",
            "data": %s
        }// success：true-成功，false-失败
        ''' % data
        self.update(api, mode)

    def update_commit_file_success(self):
        api = "/commitFile"
        mode = '''{
          "orderNo": function({_req}) {
            return _req.body.orderNo
          },
          "status": "1",
          "msg": "成功"
        }'''
        self.update(api, mode)

    def update_loan_apply_success(self):
        api = "/commitOrder"
        mode = '''{
          "orderNo": function({_req}) {
            return _req.body.orderNo
          },
          "status": "1",
          "msg": "提单成功"
        }'''
        self.update(api, mode)

    def update_loan_apply_fail(self):
        api = "/commitOrder"
        mode = '''{
          "orderNo": function({_req}) {
            return _req.body.orderNo
          },
          "status": "2",
          "msg": "提单失败"
        }'''
        self.update(api, mode)

    def update_audit_success(self):
        api = "/auditResult"
        mode = '''{
          "orderNo": function({_req}) {
            return _req.body.orderNo
          },
          "status": "3",
          "msg": "审核成功"
        }
        //status：3-审核成功，4-审核失败，6-待开户，7-待提现预约，9-提现预约成功'''
        self.update(api, mode)

    def update_audit_fail(self):
        api = "/auditResult"
        mode = '''{
          "orderNo": function({_req}) {
            return _req.body.orderNo
          },
          "status": "4",
          "msg": "审核失败"
        }
        //status：3-审核成功，4-审核失败，6-待开户，7-待提现预约，9-提现预约成功'''
        self.update(api, mode)

    def update_audit_wait_confirm(self):
        api = "/auditResult"
        mode = '''{
          "orderNo": function({_req}) {
            return _req.body.orderNo
          },
          "status": "7",
          "msg": "待提现预约"
        }
        //status：3-审核成功，4-审核失败，6-待开户，7-待提现预约，9-提现预约成功'''
        self.update(api, mode)

    def update_audit_confirm_success(self):
        api = "/auditResult"
        mode = '''{
          "orderNo": function({_req}) {
            return _req.body.orderNo
          },
          "status": "9",
          "msg": "提现预约成功"
        }
        //status：3-审核成功，4-审核失败，6-待开户，7-待提现预约，9-提现预约成功'''
        self.update(api, mode)

    # def update_replay_plan(self):
    #     api = "/repaymentPlan"
    #     mode = '''{
    #       "loanMoney": "8000.00",
    #       "orderNo": function({_req}) {
    #         return _req.body.orderNo
    #       },
    #       "status": "3",
    #       "msg": "已放款",
    #       "startInterestDate": "2048-01-20",
    #       "loanTime": "2048-01-20 05:40:03",
    #       "repayPlan": [{
    #         "repanCn": "1",
    #         "mustBen": "1309.91",
    #         "mustIni": "56.67",
    #         "expirtDate": "2048-02-20",
    #         "mustFeeList": [],
    #         "mustMoney": 1366.57
    #       }, {
    #         "repanCn": "2",
    #         "mustBen": "1319.19",
    #         "mustIni": "47.39",
    #         "expirtDate": "2048-03-20",
    #         "mustFeeList": [],
    #         "mustMoney": 1366.58
    #       }, {
    #         "repanCn": "3",
    #         "mustBen": "1328.54",
    #         "mustIni": "38.04",
    #         "expirtDate": "2048-04-20",
    #         "mustFeeList": [],
    #         "mustMoney": 1366.58
    #       }, {
    #         "repanCn": "4",
    #         "mustBen": "1337.95",
    #         "mustIni": "28.63",
    #         "expirtDate": "2048-05-20",
    #         "mustFeeList": [],
    #         "mustMoney": 1366.58
    #       }, {
    #         "repanCn": "5",
    #         "mustBen": "1347.42",
    #         "mustIni": "19.16",
    #         "expirtDate": "2048-06-20",
    #         "mustFeeList": [],
    #         "mustMoney": 1366.58
    #       }, {
    #         "repanCn": "6",
    #         "mustBen": "1356.99",
    #         "mustIni": "9.61",
    #         "expirtDate": "2048-07-20",
    #         "mustFeeList": [],
    #         "mustMoney": 1366.6
    #       }]
    #     }
    #     // 1无此订单
    #     // 2未放款
    #     // 3已放款（结果,提现成功/参与人互转成功）
    #     // 4放款失败（非结果）
    #     // 5提现失败（非结果）
    #     // 6已流标（结果）
    #     // 7 待提现（非结果）
    #     // 8 提现中（非结果）
    #     // 9 提现超时（结果）
    #     // 10人工处理后需结清（结果）
    #     '''
    #     self.update(api, mode)

    def update_repay_plan(self, asset_info):
        api = "/repaymentPlan"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
          "loanMoney": asset_info['data']['asset']['amount'],
          "orderNo": get_asset_loan_record_by_item_no(asset_info["data"]["asset"]["item_no"])[0]["asset_loan_record_due_bill_no"],
          "status": "3",
          "msg": "已放款",
          "startInterestDate": "@now",
          "loanTime": "@now",
          "repayPlan": []
        }
        repayment_plan_tmp = {
            "repanCn": "6",
            "mustBen": "1356.99",
            "mustIni": "9.61",
            "expirtDate": "2048-07-20",
            "mustFeeList": [],
            "mustMoney": 1366.6
          }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['repanCn'] = i + 1
            repayment_plan['mustBen'] = float(fee_info['principal']) / 100
            repayment_plan['mustIni'] = float(fee_info['interest']) / 100
            repayment_plan['mustMoney'] = float('%.2f' % (repayment_plan['mustBen'] + repayment_plan['mustIni']))
            repayment_plan['expirtDate'] = fee_info['date']
            mode['repayPlan'].append(repayment_plan)
        self.update(api, mode)


if __name__ == "__main__":
    pass
