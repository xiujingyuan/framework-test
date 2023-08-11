from copy import deepcopy

from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_capital_account_card_by_idnum_encrypt, \
    get_asset_loan_record_by_item_no
from biztest.util.tools.tools import get_date


class LianlianMock(Easymock):

    def update_account_open_success(self):
        api = "/brokers/members/authorizedDelegations"
        method = "post"
        mode = {
            "data": {
                "memberId": "@integer(10000000, 800000000)",
                "url": "http://www.baidu.com",
                "data": ""},
            "statusCode": "0"}
        self.update(api, mode, method)

    def update_account_open_status_success(self, idnum_encrypt, channel):
        api = "/brokers/members/status"
        method = "get"
        user_key = get_capital_account_card_by_idnum_encrypt(idnum_encrypt, channel)[0]["capital_account_card_user_key"]
        mode = {
            "data": {
                "allowPass": True,
                "memberId": user_key,
                "hasOpenAccount": True,
                "bankCardHasBound": True,
                "bindingCardDifferent": False,
                "tradePasswordHasSet": True,
                "authorizedDeductionDelegationHasSigned": True,
                "repaymentDelegationHasSigned": True,
                "paymentDelegationHasSigned": True,
                "idCardIsUsed": False
            },
            "statusCode": "0"
        }
        self.update(api, mode, method)

    def update_account_open_status_fail(self):
        api = "/brokers/members/status"
        method = "get"
        mode = {
            "data": {
                "allowPass": True,
                "hasOpenAccount": False,
                "bankCardHasBound": False,
                "bindingCardDifferent": False,
                "tradePasswordHasSet": False,
                "authorizedDeductionDelegationHasSigned": True,
                "repaymentDelegationHasSigned": False,
                "paymentDelegationHasSigned": False,
                "idCardIsUsed": False
            },
            "statusCode": "0"
        }
        self.update(api, mode, method)

    def update_loan_apply_success(self, idnum_encrypt, channel):
        api = '/brokers/preloan/preloan'
        user_key = get_capital_account_card_by_idnum_encrypt(idnum_encrypt, channel)[0]["capital_account_card_user_key"]
        method = 'post'
        mode = {
            "data": {
                "memberId": user_key,
                "loanOrderId": "@integer(1000000000, 9000000000)"
            },
            "statusCode": "0"}
        self.update(api, mode, method)

    def update_loan_apply_fail(self):
        api = '/brokers/preloan/preloan'
        method = 'post'
        mode = {}
        self.update(api, mode, method)

    def update_loan_apply_query_success(self):
        api = '/brokers/preloan/preloan'
        method = 'get'
        mode = {
            "data": {
                "status": 3,
                "auditDescription": "mock测试"
            },
            "statusCode": "0"
        }
        self.update(api, mode, method)

    def update_loan_apply_query_fail(self):
        api = '/brokers/preloan/preloan'
        method = 'get'
        mode = {
            "data": {
                "status": 4,
                "auditDescription": "资质审核不通过"
            },
            "statusCode": "0"
        }
        self.update(api, mode, method)

    def update_confirm_apply_success(self):
        api = '/brokers/preloan/confirm'
        method = 'post'
        mode = {
            "data": {
                "loanId": "@integer(1000000000, 9000000000)"
            },
            "statusCode": "0"
        }
        self.update(api, mode, method)

    def update_confirm_query_success(self, item_no):
        api = '/brokers/loanReleases/loanReleases'
        method = 'get'
        loan_id = get_asset_loan_record_by_item_no(item_no)[0]["asset_loan_record_due_bill_no"]
        mode = {
            "statusCode": "0",
            "message": None,
            "data": {
                "loanId": loan_id,
                "status": 2,
                "soldOutAt": "2019-11-13 11:44:11",
                "createdAt": "@now",
                "borrowerContract": "",
                "investments": [{
                    "investorName": None,

                    "investorNameEncrypt": "enc_04_2568578206311910400_267",
                    "amount": "6000.00",
                    "contractCode": "KNDE06-01-GR20191113KN389190335-389190396",
                    "contractDownloadUrl": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/mXJy2XRxf4H0olS4.pdf",
                    "investorIdCardNumber": None,
                    "investorIdCardNumberEncrypt": "enc_02_2568576104512623616_602",
                    "guaranteeContractCode": "KNDE06-01-DB20191113KN389190335-389190396",
                    "guaranteeContractDownloadUrl": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/"
                                                    "MZJy2GgMMRRLE114.pdf"
                }],
                "counselingContract": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/GUJy2un_Z24KB8O4.pdf",
                "counselingContractCode": "KNDE06-1-ZX20191113KN389190335-389190335",
                "withdrawal": {
                    "amount": "3000.00",
                    "amountLeft": 0.00,
                    "startAt": "2019-11-13 12:11:07",
                    "completedAt": "@now",
                    "status": 2
                }
            }}
        self.update(api, mode, method)

    # 提现申请成功
    def update_withdraw_apply_success(self):
        api = '/brokers/withdrawals/withdrawals'
        method = 'post'
        mode = {
            "data": {
                "url": "http://www.qq.con",
                "data": "t=1578016298"
            },
            "statusCode": "0"
        }
        self.update(api, mode, method)

    # 提现接口申请失败,code不正确
    def update_withdraw_apply_fail(self):
        api = '/brokers/withdrawals/withdrawals'
        method = 'post'
        mode = {
            "data": {
                "url": "Test_URL02",
                "data": "自动化测试"
            },
            "statusCode": "10"
        }
        self.update(api, mode, method)

    # 提现接口申请失败，返回500
    def update_withdraw_apply_fail_with_500(self):
        api = '/brokers/withdrawals/withdrawals'
        method = 'post'
        mode = {
            "_res": {
                "status": 500,
            }
        }
        self.update(api, mode, method)

    def update_withdraw_query_fail_500(self):
        api = '/brokers/loanReleases/loanReleases'
        method = 'get'
        mode = {
            "_res": {
                "status": 500
            }}
        #     "statusCode": "0",
        #     "message": None,
        #     "data": {
        #         "loanId": "4569373314",
        #         "status": 2,
        #         "soldOutAt": "2019-11-13 11:44:11",
        #         "createdAt": "@now",
        #         "borrowerContract": "",
        #         "investments": [{
        #             "investorName": None,
        #             "investorNameEncrypt": "enc_04_2568578206311910400_267",
        #             "amount": "6000.00",
        #             "contractCode": "KNDE06-01-GR20191113KN389190335-389190396",
        #             "contractDownloadUrl": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/mXJy2XRxf4H0olS4.pdf",
        #             "investorIdCardNumber": None,
        #             "investorIdCardNumberEncrypt": "enc_02_2568576104512623616_602",
        #             "guaranteeContractCode": "KNDE06-01-DB20191113KN389190335-389190396",
        #             "guaranteeContractDownloadUrl": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/MZJy2GgMMRRLE114.pdf"
        #         }],
        #         "counselingContract": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/GUJy2un_Z24KB8O4.pdf",
        #         "counselingContractCode": "KNDE06-1-ZX20191113KN389190335-389190335",
        #         "withdrawal": {
        #             "amount": "3000.00",
        #             "amountLeft": 0.0,
        #             "startAt": "2019-11-13 12:11:07",
        #             "completedAt": "@now",
        #             "status": 2
        #         }
        #     }
        # }
        self.update(api, mode, method)

    def update_withdraw_query_process(self, asset_info):
        api = '/brokers/loanReleases/loanReleases'
        method = 'get'
        item_no = asset_info['data']['asset']['item_no']
        loan_id = get_asset_loan_record_by_item_no(item_no)[0]["asset_loan_record_due_bill_no"]
        mode = {
            "statusCode": "0",
            "message": None,
            "data": {
                "loanId": loan_id,
                "status": 2,
                "soldOutAt": "2019-11-13 11:44:11",
                "createdAt": "@now",
                "borrowerContract": "",
                "investments": [{
                    "investorName": None,
                    "investorNameEncrypt": "enc_04_2568578206311910400_267",
                    "amount": "6000.00",
                    "contractCode": "KNDE06-01-GR20191113KN389190335-389190396",
                    "contractDownloadUrl": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/mXJy2XRxf4H0olS4.pdf",
                    "investorIdCardNumber": None,
                    "investorIdCardNumberEncrypt": "enc_02_2568576104512623616_602",
                    "guaranteeContractCode": "KNDE06-01-DB20191113KN389190335-389190396",
                    "guaranteeContractDownloadUrl": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/"
                                                    "MZJy2GgMMRRLE114.pdf"
                }],
                "counselingContract": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/GUJy2un_Z24KB8O4.pdf",
                "counselingContractCode": "KNDE06-1-ZX20191113KN389190335-389190335",
                "withdrawal": {
                    "amount": "%s.00" % asset_info['data']['asset']['amount'],
                    "amountLeft": 0.0,
                    "startAt": "2019-11-13 12:11:07",
                    "completedAt": "@now",
                    "status": 1
                }
            }
        }
        self.update(api, mode, method)

    def update_withdraw_query_success(self, asset_info):
        api = '/brokers/loanReleases/loanReleases'
        method = 'get'
        item_no = asset_info['data']['asset']['item_no']
        loan_id = get_asset_loan_record_by_item_no(item_no)[0]["asset_loan_record_due_bill_no"]
        mode = {
            "statusCode": "0",
            "message": None,
            "data": {
                "loanId": loan_id,
                "status": 2,
                "soldOutAt": "2019-11-13 11:44:11",
                "createdAt": "@now",
                "borrowerContract": "",
                "investments": [{
                    "investorName": None,
                    "investorNameEncrypt": "enc_04_2568578206311910400_267",
                    "amount": "6000.00",
                    "contractCode": "KNDE06-01-GR20191113KN389190335-389190396",
                    "contractDownloadUrl": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/mXJy2XRxf4H0olS4.pdf",
                    "investorIdCardNumber": None,
                    "investorIdCardNumberEncrypt": "enc_02_2568576104512623616_602",
                    "guaranteeContractCode": "KNDE06-01-DB20191113KN389190335-389190396",
                    "guaranteeContractDownloadUrl": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/"
                                                    "MZJy2GgMMRRLE114.pdf"
                }],
                "counselingContract": "http://resources.lianlianmoney.com:80/DOCUM/2019/1113/GUJy2un_Z24KB8O4.pdf",
                "counselingContractCode": "KNDE06-1-ZX20191113KN389190335-389190335",
                "withdrawal": {
                    "amount": "%s.00" % asset_info['data']['asset']['amount'],
                    "amountLeft": 0.0,
                    "startAt": "2019-11-13 12:11:07",
                    "completedAt": "@now",
                    "status": 2
                }
            }
        }
        self.update(api, mode, method)

    def update_replay_plan(self, asset_info):
        api = "/brokers/loanPhases/loanPhases"
        item_no = asset_info['data']['asset']['item_no']
        loan_id = get_asset_loan_record_by_item_no(item_no)[0]["asset_loan_record_due_bill_no"]
        repayment_plan_tmp = {
            "id": 1000069839,
            "loanId": loan_id,
            "repaymentType": 3,
            "phaseCount": 180,
            "number": 1,
            "principal": "4000.00",
            "interest": "53.34",
            "amount": "4053.34",
            "dueAt": get_date(day=30, fmt="%Y-%m-%d 00:00:00"),
            "status": 0,
            "expectGuaranteedAt": "@now",
            "repayerId": -1,
            "fee": "0.00",
            "transferFee": "0.00",
            "prepaid": False,
            "contracts": [],
            "confirmContracts": [],
            "assignContracts": []
        }
        mode = {
            "data": {
                "items": [],
                "count": asset_info['data']['asset']['period_count']
            },
            "statusCode": "0"
        }

        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['number'] = i + 1
            repayment_plan['principal'] = str("%.02f" % (fee_info['principal'] / 100))
            repayment_plan['interest'] = str("%.02f" % (fee_info['interest'] / 100))
            repayment_plan['amount'] = str("%.02f" % ((fee_info['principal'] / 100) +
                                                      (fee_info['interest'] / 100)))
            if asset_info['data']['asset']['period_count'] == 1:
                repayment_plan['dueAt'] = get_date(day=30, fmt="%Y-%m-%d 00:00:00")
            else:
                repayment_plan['dueAt'] = get_date(month=i + 1, fmt="%Y-%m-%d")
            mode['data']['items'].append(repayment_plan)

        self.update(api, mode)
