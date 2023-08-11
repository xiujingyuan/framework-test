from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_date


class TongrongmiyangMock(Easymock):

    def update_apply_success(self, asset_info):
        api = "/tongrongmiyang/tongrongqianjingjing/loanApply"
        code = 200
        check_point = {
            "path": self.path_prefix + api,
            "body": {
                "loanOrder.termNo": "{}".format(asset_info["data"]["asset"]["period_count"]),
                "loanOrder.account": "{:.2f}".format(asset_info["data"]["asset"]["amount"])
            }
        }
        mode = '''{
          "code": %s,
          "message": "成功",
          "data": null,
          "success": true
        }''' % self.get_mock_result_with_check(code, check_point)
        self.update(api, mode)

    def update_apply_fail(self):
        api = "/tongrongmiyang/tongrongqianjingjing/apply"
        mode = ""
        self.update(api, mode)

    def update_apply_query_success(self):
        api = "/tongrongmiyang/tongrongqianjingjing/loanApplyQuery"
        mode = '''{
          "code": 200,
          "message": "成功！",
          "data": {
            "status": 1,
            "pdfUrl": "http://paydayloandevv4-1251122539.cossh.myqcloud.com/20190422/e43d5bb369463bdbb36c4bdda2c086ef.pdf",
            "contractId": "bondTransferContractId_ph_trmy_5001141986",
            "workflowCode": "200",
            "workflowMessage": "成功！"
          },
          "success": true
        }'''
        print(self.update(api, mode))

    def update_apply_query_fail(self):
        api = "/tongrongmiyang/tongrongqianjingjing/loanApplyQuery"
        mode = '''{
          "code": 200,
          "message": "失败",
          "data": {
            "status": -1,
            "pdfUrl": "",
            "contractId": "",
            "workflowCode": "200",
            "workflowMessage": "订单失败"
          },
          "success": true
        }'''
        self.update(api, mode)

    def update_balance_enough(self):
        api = "/tongrongmiyang/tongrongqianjingjing/balanceQuery"
        mode = '''	{
          "code": 200,
          "message": "成功",
          "data": {
            "bal_sign": 5000000,
            "mer_id": "53079"
          },
          "success": true
        }'''
        self.update(api, mode)

    def update_loan_apply_success(self):
        api = "/tongrongmiyang/tongrongqianjingjing/applyConfirm"
        mode = '''{
          "code": 200,
          "message": "成功",
          "data": null,
          "success": true
        }'''
        self.update(api, mode)

    def update_loan_apply_query_success(self):
        api = "/tongrongmiyang/tongrongqianjingjing/confirmQuery"
        mode = '''{
          "code": 200,
          "message": "成功！",
          "data": {
            "status": "1",
            "orderId": function({_req}){return _req.body.orderId},
            "issueRequestNo": function({_req}){return _req.body.queryRequestNo},
            "retCode": null,
            "errMsg": null,
            "transferDate": "%s",
            "sign": null
          },
          "success": true
        }''' % get_date(fmt="%Y%m%d")
        self.update(api, mode)

    def update_loan_apply_query_fail(self):
        api = "/tongrongmiyang/tongrongqianjingjing/confirmQuery"
        mode = '''{
          "code": 200,
          "message": "成功！",
          "data": {
            "status": "-1",
            "orderId": function({_req}){return _req.body.orderId},
            "issueRequestNo": function({_req}){return _req.body.QueryRequestNo},
            "retCode": "1001",
            "errMsg": "放款失败",
            "transferDate": "",
            "sign": null
          },
          "success": true
        }'''
        self.update(api, mode)
