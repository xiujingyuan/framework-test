# -*- coding: utf-8 -*-
from copy import deepcopy

from sqlalchemy import JSON

from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.function.rbiz.rbiz_db_function import get_asset_info_by_item_no
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import *
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no


class ZhenJinFuMock(Easymock):
    def update_account_open_success(self):
        api = "/partner/dt/person_info.html"
        mode = '''{
                "retCode": 200,
                "retMsg": "操作成功",
                "data": "{\\"url\\":\\"http://www.baidu.com\\"}",
                "sign": "12121212",
                "timestamp": "1578637216"
            }
            // retCode
            // 200	操作成功
            // 40003	已开户成功
            // 40004	异常数据无法开户'''
        self.update(api, mode)

    def update_account_query_no_account(self):
        api = "/partner/dt/account_status_query.html"
        data = '''function({_req}) {
            var data = {
                "bankCardNo": null,
                "bankCardNoEncrypt": null,
                "idName": null,
                "idNameEncrypt": null,
                "idNo": null,
                "idNoEncrypt": null,
                "partnerUserId": _req.body.partnerUserId,
                "phone": null,
                "phoneEncrypt": null,
                "status": "0",
                "userType": "3"
                };
            return JSON.stringify(data)
        }'''
        mode = '''{
            "retCode": 200,
            "retMsg": "未开户",
            "data": %s,
            "sign": "1212",
            "timestamp": "1578638451"
        }''' % data
        self.update(api, mode)

    def update_account_query_success(self, four_element):
        api = "/partner/dt/account_status_query.html"
        data = '''
        function({_req}) {
            var data = {
                "bankCardNo": null,
                "bankCardNoEncrypt": "%s",
                "idName": null,
                "idNameEncrypt": "%s",
                "idNo": null,
                "idNoEncrypt": "%s",
                "partnerUserId": _req.body.partnerUserId,
                "phone": null,
                "phoneEncrypt": "%s",
                "status": "1",
                "userType": "3"
                };
            return JSON.stringify(data)
        }''' % (four_element['data']['bank_code_encrypt'], four_element['data']['user_name_encrypt'],
                four_element['data']['id_number_encrypt'], four_element['data']['phone_number_encrypt'])
        mode = '''{
            "retCode": 200,
            "retMsg": "操作成功",
            "data": %s,
            "sign": "1212",
            "timestamp": "1578638451"
        }''' % data
        self.update(api, mode)

    def update_upload_file_success(self):
        api = "/partner/dt/attachment.html"
        mode = {
            "retCode": 200,
            "retMsg": "操作成功",
            "data": None,
            "sign": "121212",
            "timestamp": "1578639250"
        }
        self.update(api, mode)

    def update_loan_apply_success(self):
        api = "/partner/dt/loan_person.html"
        mode = '''{
            "retCode": 200,
            "retMsg": "操作成功",
            "data": null,
            "sign": "121212",
            "timestamp": "1578639250"
            }
            //retCode：
            // 200	操作成功
            // 401	参数错误
            // 402	Md5验签没通过
            // 403	业务数据非法或（具体会返回错误的原因）
            // 404	数据解密异常
            // 408	证书路径没有配置
            // 500	系统异常
            // 100001	重复推送，标的已放款成功
            // 100002	重复推送，标的已处于审核中
            // 100003	重复推送，标的已审核失败
            // 100004	重复推送，标的已审核成功状态
            // 100005	重复推送，标的已处于放款中
            // 100006	重复推送，标的已放款失败
            // 100008	今日累计放款成功金额已超过当日用款额度
            // 200001	无效进件，未开户
            // 200002	无效进件，进件四要素和开户四要素不一致'''
        self.update(api, mode)

    def update_loan_query_success(self, item_no):
        credit_id = get_asset_loan_record_by_item_no(item_no)[0]["asset_loan_record_due_bill_no"]
        api = "/partner/dt/loan_query.html"
        data = '''
        function({_req}) {
            var data = {
                "creditId": "%s",
                "loanTime": %s,
                "loanRemark": "放款成功",
                "loanStatus": "27",
                "auditRemark": null,
                "subStatus": 27,
                "status": 0
                };
            return JSON.stringify(data)
        }''' % (credit_id, int(str(time.time()).split('.')[0]))
        mode = '''{
            "retCode": 200,
            "retMsg": "操作成功",
            "data": %s,
            "sign": "121212",
            "timestamp": "1578640248"
            }
            //loanStatus：00-审核中，01-审核成功，02-审核失败，26-放款中，27-放款成功，
            //28-放款失败，-1-1-缺少标的基本信息，-1-2-缺少标的借款人，-1-3-缺少电子合同''' % data
        self.update(api, mode)

    def update_get_contract_success(self):
        api = "/partner/dt/contact_query.html"
        mode = {
            "retCode": 200,
            "retMsg": "操作成功",
            "data": json.dumps({
                "tarUrl": "youjin_test/kuainiu/contract/LOAN_CONSULTATION_CS20181009783769.pdf",
                "status": "1"
            }),
            "sign": "giTLWo2Kh/++MgLM/hrwamascjM4DB+++lxm8C8o/L/Boc4UrPM6Jc+DRXgYyTJlBPDUP1SIKXV1gg12jZ3cd/WA==",
            "timestamp": "1578641088"
        }
        self.update(api, mode)

    def update_repayplan_success(self, asset_info):
        api = "/partner/dt/payback_plan_query.html"
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        creditId = alr_info[0]['asset_loan_record_due_bill_no']
        repayment_plan_temp = {
            "amount": 1030.14,
            "realPaybackTime": 1586448000,
            "compensationFee": 5.00,
            "realTermEndTime": 1586361600,
            "payStyle": "等额本息",
            "principal": 1014.92,
            "totalTerms": 3,
            "creditId": "BIZ84727200119113526",
            "curTerm": 3,
            "interest": 15.22,
            "dailyProfit": 0.654838709677419400,
            "curTermLife": 31,
            "paybackTime": 1586793600,
            "termStartTime": 1583769600,
            "termEndTime": 1586361600,
            "partnerFee": 25.34
        }
        mode = {
            "retCode": 200,
            "retMsg": "操作成功",
            "data": "",
            "sign": "MIadm+M/tMSyOzFGraTLgbUvFEJF7uxOer/UUbVh2v68djEgWFxexJSjljcz//+//==",
            "timestamp": "1578640666"
        }
        data_temp = []
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_temp)
            repayment_plan['principal'] = round((fee_info['principal'] / 100), 2)
            repayment_plan['interest'] = round((fee_info['interest'] / 100), 2)
            repayment_plan['amount'] = round(((fee_info['principal'] / 100) + (fee_info['interest'] / 100)), 2)
            repayment_plan['partnerFee'] = round((fee_info['after_loan_manage'] / 100), 2)
            repayment_plan['compensationFee'] = round((fee_info['technical_service'] / 100), 2)

            repayment_plan['realPaybackTime'] = repayment_plan['paybackTime'] = get_date_timestamp(month=i + 1)
            repayment_plan['realTermEndTime'] = repayment_plan['termEndTime'] = get_date_timestamp(month=i + 1, day=-1)
            repayment_plan['termStartTime'] = get_date_timestamp()
            repayment_plan['totalTerms'] = asset_info['data']['asset']['period_count']
            repayment_plan['curTerm'] = i + 1
            repayment_plan['creditId'] = creditId
            data_temp.append(repayment_plan)
        mode["data"] = json.dumps(data_temp)
        self.update(api, mode)

    def update_zhenjinfu_withhold_result(self, item_no, serial_no, fee_info, pay_status="1", payback_type="1",
                                         prepay_term="1", pay_remark="自动化测试"):
        # 这里有个坑，各种费用不能是int类型
        # "paybackType": "2", // 0：正常回款、1：提前还款、2：提前还清、
        # "status": "2" // 0. 处理中、1.回款成功、2.回款失败
        api = "/zhenjinfu/partner/dt/pre_pay_query.html"
        total_amount = fee_info["principal"] + fee_info["interest"]
        data_temp = {
            "amount": "%s" % total_amount,
            "compensationFee": "%s" % fee_info["technical_service"],
            "penalty": "0.00",
            "paybackType": payback_type,
            "payRemark": pay_remark,
            "partnerManagerFee": "%s" % fee_info["after_loan_manage"],
            "principal": "%s" % fee_info["principal"],
            "creditId": item_no,
            "prepayTerm": prepay_term,
            "serialId": serial_no,
            "interest": "%s" % fee_info["interest"],
            "payChannel": "1",
            "withdrawTime": get_date(),
            "status": pay_status
        }
        mode = {
            "retCode": 200,
            "retMsg": "操作成功",
            "data": json.dumps(data_temp),
            "sign": "MIadm",
            "timestamp": "1578640666"
        }
        self.update(api, mode)

    def update_zhenjinfu_trail_success(self, item_no, **fee_info):
        # 试算接口
        api = "/zhenjinfu/partner/dt/prepay_trial.html"
        total_amount = fee_info["principal"] + fee_info["c_interest"] + fee_info["technical_service"] + fee_info[
            "after_loan_manage"]
        data_temp = {
            "compensationFee": "0",
            "creditId": item_no,
            "defaultInterest": "0",
            "interest": "%s" % fee_info["c_interest"],
            "partner": "kuainiu_b",
            "partnerFee": "%s" % fee_info["after_loan_manage"],
            "compensationFee": "%s" % fee_info["technical_service"],
            "principal": "%s" % fee_info["principal"],
            "term": "1",
            "totalAmount": "%s" % total_amount,
        }
        mode = {
            "retCode": 200,
            "retMsg": "操作成功",
            "data": json.dumps(data_temp),
            "sign": "MIadm",
            "timestamp": "1578640666"
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
