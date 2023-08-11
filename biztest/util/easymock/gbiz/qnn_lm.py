# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock
from biztest.interface.cmdb.cmdb_interface import *
from biztest.function.cmdb.cmdb_common_function import *


class QnnMock(Easymock):
    def update_account_query_false(self):
        api = "/checkAccount"
        mode = {"message": "", "code": 200, "data": {"account": False, "card": False, "protocol_sign": False}}
        self.update(api, mode)

    def update_account_query_true(self):
        api = "/checkAccount"
        mode = {"message": "", "code": 200, "data": {"account": True, "card": True, "protocol_sign": True}}
        self.update(api, mode)

    def update_account_create_true(self):
        api = "/accountCreate"
        mode = {"message": "", "code": 200, "data": {"status": False,
                                                     "redirect_url": "https:\\/\\/hubk.lanmaoly.com\\/bha-neo-app\\/gat"
                                                                     "eway\\/mobile\\/personalRegisterExpand\\/index.ht"
                                                                     "l?requestKey=7479eba0-6291-40c7-bcf5-"
                                                                     "6b961e161213"}}
        self.update(api, mode)

    def update_loan_apply_success(self):
        api = "/loan"
        mode = {"message": "", "code": 200, "data": ""}
        self.update(api, mode)
        pass

    def update_project_status_true(self):
        api = "/assetProjectStatus"
        mode = {"message": "", "code": 200, "data": {"status": True}}
        self.update(api, mode)
        pass

    def update_auth_query_no_authed(self):
        api = "/assetGrantToCardAuthorizationQuery"
        mode = {"message": "", "code": 200, "data": {"grant_to_card_auth": "not_authed"}}
        self.update(api, mode)

    def update_auth_query_success(self):
        api = "/assetGrantToCardAuthorizationQuery"
        mode = {"message": "", "code": 200, "data": {"grant_to_card_auth": "success"}}
        self.update(api, mode)

    def update_auth_request(self):
        api = "/assetGrantToCardAuthorization"
        mode = {"message": "", "code": 200, "data": {"status": False,
                                                     "redirect_url": "https:\\/\\/p2pcg.hfbank.com.cn\\/bha-neo-app\\/g"
                                                                     "ateway\\/mobile\\/loanCheck\\/index.html?request"
                                                                     "Key=059084ad-0492-4895-9188-7a848dbc9bbc"}}
        self.update(api, mode)

    def update_loan_query_success(self):
        api = "/loanQuery"
        mode = {"message": "", "code": 200, "data": {"status": 1, "finish_at": "@now", "message": ""}}
        self.update(api, mode)

    def update_withdraw_query_success(self):
        api = "/queryWithdraw"
        mode = {"message": "", "code": 200, "data": {"status": "success", "fail_reason": "", "finish_at": "@now"}}
        self.update(api, mode)

    def update_contract_down(self):
        api = "/contracts"
        mode = '''{
            "message": "",
            "code": 200,
            "data": [
                {
                    "item_no": function({_req}){return _req.query.item_no},
                    "from_system": "dsq",
                    "name": "钱牛牛借款合同",
                    "type": 28,
                    "download_url": "http://paydayloandevv4-1251122539.cos.ap-shanghai.myqcloud.com/20190311/SaveToCos/QNN11312570190311192924.pdf",
                    "view_url": "https://testapi.fadada.com:8443/api//viewdocs.action?app_id=400925×tamp=20190311192927&v=2.0&msg_digest=QjUzMTk2NjkxNkQ1M0RDQ0E4MjhEMzk1MjIwRDBGQTcwNTIyQkJERg==&send_app_id=null&transaction_id=1903111929261126789825"
                },
                {
                    "item_no": function({_req}){return _req.query.item_no},
                    "from_system": "dsq",
                    "name": "钱牛牛借款人居间协议",
                    "type": 8100,
                    "download_url": "http://paydayloandevv4-1251122539.cos.ap-shanghai.myqcloud.com/20190311/SaveToCos/QNN11312567190311192924.pdf",
                    "view_url": "https://testapi.fadada.com:8443/api//viewdocs.action?app_id=400925×tamp=20190311192928&v=2.0&msg_digest=QjdEMjRCNDZEMzU0NDBERUU5MkNDNEFDQzRBNDI2QUQyRDA2QTI5RA==&send_app_id=null&transaction_id=1903111929271126789822"
                },
                {
                    "item_no": function({_req}){return _req.query.item_no},
                    "from_system": "dsq",
                    "name": "钱牛牛借款人信用承诺书",
                    "type": 8012,
                    "download_url": "http://paydayloandevv4-1251122539.cos.ap-shanghai.myqcloud.com/20190311/SaveToCos/QNN11312569190311192924.pdf",
                    "view_url": "https://testapi.fadada.com:8443/api//viewdocs.action?app_id=400925×tamp=20190311192925&v=2.0&msg_digest=NzM5MEE0NzcxRjgwQkU0RDgwMkZCNDBEREJBMEFFRUMyMTQ3M0ZEMQ==&send_app_id=null&transaction_id=1903111929251126789821"
                }
            ]
        }'''
        self.update(api, mode)

    def update_replay_plan(self, asset_info):
        api = "/repaymentPlan"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
            "message": "",
            "code": 200,
            "data": {
                "interest_rate": 10,
                "service_fee_rate": 6,
                "penalty_interest_rate": 0,
                "subsidy_interest_rate": 10,
                "repayment_plans": []
            }
        }
        repayment_plan_tmp = {
            "principal": 250000,
            "repaid_principal": 0,
            "interest": 6250,
            "repaid_interest": 0,
            "service_fee": 3750,
            "repaid_service_fee": 0,
            "penalty_interest": 0,
            "subsidy_interest": 0,
            "type": 1,
            "status": 0,
            "expect_finish_at": get_date(day=90),
            "period": 1,
            "late_status": 0,
            "repay_channel": "",
            "create_at": "@now",
            "finish_at": "1000-01-01 00:00:00",
            "repay_at": "1000-01-01 00:00:00",
            "update_at": "@now",
            "management_fee": 0,
            "repaid_management_fee": 0,
            "referral_fee": 0,
            "repaid_referral_fee": 0,
            "start_at": "@now"
        }
        for i in range(asset_info['data']['asset']['period_count']):
            if asset_info['data']['asset']['period_count'] == 1:
                fee_info = get_fee_info_by_period(rate_info, i + 1)
                repayment_plan = deepcopy(repayment_plan_tmp)
                repayment_plan['period'] = i + 1
                repayment_plan['principal'] = fee_info['principal'] * 3
                repayment_plan['interest'] = fee_info['interest'] * 3
                repayment_plan['service_fee'] = fee_info['service'] * 3
                if asset_info['data']['asset']['from_system_name'] != '草莓':
                    repayment_plan['management_fee'] = fee_info['after_loan_manage'] * 3
                    repayment_plan['referral_fee'] = fee_info['technical_service'] * 3
                repayment_plan['expect_finish_at'] = get_date(day=90)
                mode['data']['repayment_plans'].append(repayment_plan)
            else:
                fee_info = get_fee_info_by_period(rate_info, i + 1)
                repayment_plan = deepcopy(repayment_plan_tmp)
                repayment_plan['period'] = i + 1
                repayment_plan['principal'] = fee_info['principal']
                repayment_plan['interest'] = fee_info['interest']
                repayment_plan['service_fee'] = fee_info['service']
                if asset_info['data']['asset']['from_system_name'] != '草莓':
                    repayment_plan['management_fee'] = fee_info['after_loan_manage']
                    repayment_plan['referral_fee'] = fee_info['technical_service']
                repayment_plan['expect_finish_at'] = fee_info['date']
                mode['data']['repayment_plans'].append(repayment_plan)

        self.update(api, mode)


if __name__ == "__main__":
    qnn = QnnMock('carltonliu', 'lx19891115', "5d19e7f91ce48c002028bec0")
    # qnn.update_loan_apply_success()
    qnn.update_project_status_true()
