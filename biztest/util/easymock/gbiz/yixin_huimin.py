# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
import json

class YixinHuiminMock(Easymock):
    # 惠民的开户步骤总共4步，此处仅mock了开户4步的查询接口，没有必要调用开户接口
    def update_account_open_success(self, four_element):
        api = "/p2p/openAcc/query.htm"
        mode = '''{
                  "userId": "Test@integer(100000000, 900000000000)",
                  "state": null,
                  "opType": "0",
                  "respCode": "0000",
                  "respDescription": "交易成功",
                  "remark": null,
                  "bankId": null,
                  "identType": "111",
                  "accountNo": null,
                  "accountNoEncrypt": null,
                  "mobileNum": null,
                  "mobileNumEncrypt": null,
                  "identNo": null,
                  "identNoEncrypt": "%s",
                  "customerName": null,
                  "customerNameEncrypt": "%s",
                  "identityRole": "1",
                  "accStatus": "02",
                  "accBalance": "0",
                  "frozenBalance": "0",
                  "unSettleBalance": "0"
                }''' % (four_element['data']['id_number_encrypt'], four_element['data']['user_name_encrypt'])
        self.update(api, mode)

    def update_bindcard_success(self, four_element):
        api = "/p2p/cgb/queryBindBankCardList.htm"
        mode = '''{
                    "userID": function({
                      _req
                    }) {
                      return _req.body.userID
                    },
                    "respCode": "0000",
                    "respDescription": "交易成功",
                    "cardList": [{
                      "bindCardId": "@integer(1000000000000000, 9000000000000000000)",
                      "accountNo": null,
                      "accountNoEncrypt": "%s",
                      "cardTp": "01",
                      "mobileNum": null,
                      "mobileNumEncrypt": "%s",
                      "bankId": "0105",
                      "completeTime": "20200310000000"
                    }]
                  }''' % (four_element['data']['bank_code_encrypt'], four_element['data']['phone_number_encrypt'])
        self.update(api, mode)

    def update_account_auth_success(self):
        api = "/p2p/cgb/queryBizAuth.htm"
        mode = '''{
                  "bizAuthList": [{
                    "bizAuthCode": "1001",
                    "endDate": "20300224",
                    "maxAmount": "100000.00",
                    "minAmount": "1.00",
                    "startDate": "20200224"
                  }, {
                    "bizAuthCode": "1003",
                    "endDate": "20300224",
                    "maxAmount": "100000.00",
                    "minAmount": "1.00",
                    "startDate": "20200224"
                  }],
                  "respCode": "0000",
                  "respDescription": "交易成功",
                  "userId": function({
                    _req
                  }) {
                    return _req.body.userID
                  }
                }'''
        self.update(api, mode)

    def update_protocol_success(self, four_element):
        api = "/p2p/cgb/contract/queryCustomer.htm"
        name_encrypt = four_element['data']['user_name_encrypt']
        bank_code_encrypt = four_element['data']['bank_code_encrypt']
        idnum_encrypt = four_element['data']['id_number_encrypt']
        phone_encrypt = four_element['data']['phone_number_encrypt']
        mode = {
                    "respCode":"0000",
                    "respDescription":"【平台响应消息】交易成功",
                    "contracts":[
                        {
                            "cdtMop":"TLTN",
                            "exMerchId":"200604000004490",
                            "exMerchName":"通联新代扣--test",
                            "protState":"1",
                            "bankId":"0105",
                            "identType":"111",
                            "accountName":None,
                            "accountNameEncrypt": name_encrypt,
                            "accountNo":None,
                            "accountNoEncrypt": bank_code_encrypt,
                            "identNo":None,
                            "identNoEncrypt": idnum_encrypt,
                            "mobileNum":None,
                            "mobileNumEncrypt": phone_encrypt,
                            "completeTime":"20200310000000"
                        }
                    ]
                }
        str_mode = json.dumps(mode)
        self.update(api, str(str_mode))


    def update_loanriskquery_success_1(self):
        api = "/prism/query"
        mode = '''{
                  "status": 10000, //10000成功，其他失败重试
                  "msg": "success",
                  "data": {
                    "list": [{
                      "prismEntity": {
                        "YQ074": ""
                      },
                      "score": "765"
                    }]
                  }
                }'''
        self.update(api, mode)

    def update_loanriskquery_success_2(self):
        api = "/card/portrayal"
        mode = '''{
                  "status": 10000, //10000成功，其他失败
                  "msg": "success",
                  "data": {
                    "list": [],
                    "evaluate": {}
                  }
                }'''
        self.update(api, mode)


    def update_loanapplynew_success(self):
        api = "/receiveContract"
        mode = '''{
                  "biz_response": {
                    "resCode": "1",
                    "resMessage": "成功",
                    "uuid": function({
                      _req
                    }) {
                      return _req.body.uuid
                    },
                    "intoPiecesId": ""
                  },
                  "code": "10000",
                  "msg": "Success",
                  "sign": "nTxXjorE4toYjdGkkBySfnXY5k3LKwuYm0PuVhPjwujqNQjBi7gd0KmnrTIcvklRhxKqrn+8VPhD1e9uiendRriytsvEC+2smrTZhJ7MMeRbzyuxnG3z6FAyTb4jqb2WLG/J1VLN5GROt1yatY8KTDeDEp48bgvX95o2CJ8iHj0="
                  }'''
        self.update(api, mode)

    def update_verifyPasswd_success(self):
        api = "/p2p/subjectRegister/page/html.htm"
        mode = '''{
                  "data": {
                    a: "提现密验mock url"
                  }
                }'''
        self.update(api, mode)

    def update_verifyquery_success(self):
        api = "/p2p/subjectRegister/query.htm"
        mode = '''{
                    "crAmount": "8000.00",
                    "crDate": "20200401",
                    "crExpirtDate": "20211001",
                    "crInterest": "234.94",
                    "crRate": "10",
                    "fullScale": "1",
                    "regType": "1",
                    "repayDate": "01",
                    "repayDateType": "0",
                    "repayPeriods": "6",
                    "respCode": "0000",
                    "respDescription": "交易成功",
                    "state": "02",
                    "subjectAmount": "8000.00",
                    "subjectNo":  function({
                      _req
                    }) {
                      return _req.body.subjectNo
                    },
                    "surplusAmt": "8000.00",
                    "userId": "CE0000000015911181"
                  }'''
        self.update(api, mode)

    def update_loanwait_success(self, asset_info):
        api = "/queryIntoPiecesStatus"
        mode = '''{
                  "code": "10000",
                  "msg": "Success",
                  "biz_response": {
                    "resCode": "1",
                    "uuid":  function({
                      _req
                    }) {
                      return _req.body.uuid
                    },
                    "resMessage": "",
                    "loan": %s,
                    "completeTime": "@now",
                    "mortgagorName": null,
                    "mortgagorNameEncrypt": "%s",
                    "mobile": null,
                    "mobileEncrypt": "%s",
                    "loanReturnAccount": null,
                    "loanReturnAccountEncrypt": "%s",
                    "status": "1",
                    "intoPiecesId": "@integer(100000000000, 800000000000)"
                  }
                }''' % (asset_info['data']['asset']['amount'], asset_info['data']['borrower']['name_encrypt'],
                        asset_info['data']['borrower']['tel_encrypt'], asset_info['data']['receive_card']['num_encrypt'])
        self.update(api, mode)

    def update_loanconfirmquery_success(self, asset_info):
        api = "/queryIntoPiecesStatus"
        mode = '''{
                  "code": "10000",
                  "msg": "Success",
                  "biz_response": {
                    "resCode": "1",
                    "uuid":  function({
                      _req
                    }) {
                      return _req.body.uuid
                    },
                    "resMessage": "",
                    "loan": %s,
                    "completeTime": "@now",
                    "mortgagorName": null,
                    "mortgagorNameEncrypt": "%s",
                    "mobile": null,
                    "mobileEncrypt": "%s",
                    "loanReturnAccount": null,
                    "loanReturnAccountEncrypt": "%s",
                    "status": "6",
                    "intoPiecesId": "@integer(100000000000, 800000000000)"
                  }
                }''' % (asset_info['data']['asset']['amount'], asset_info['data']['borrower']['name_encrypt'],
                        asset_info['data']['borrower']['tel_encrypt'], asset_info['data']['receive_card']['num_encrypt'])
        self.update(api, mode)

    def update_loanApplyconfirm_success(self):
        api = "/receiveVerifyOrderId"
        mode = '''{
                  "_res": {
                    status: 200
                  },
                  "biz_response": {
                    "resCode": "1", 
                    "resMessage": "mock返回",
                    "uuid": function({
                      _req
                    }) {
                      return _req.body.uuid
                    },
                    "intoPiecesId": "" //"@integer(10000000,80000000)"
                  },
                  "code": "10000",
                  "msg": "Success",
                  "sign": "ehwi4ZQvSQ0GzxYA+I9WEckBp2QI1cOJZwHL6uLUq2vXM3pq7PUiEkaV8ze6/8j2S0g7WT0Dfec4mNpnD3tOFM/0U1YVNYvzTpk6eYIdSaPN42k0c1Mx397xAJQBfqY3z3Edh5d31U5yW1iVjaBcqaIkVui1wkVtBYLLOJdyJPQ="
                }'''
        self.update(api, mode)

    # 注意：宜信惠民还款计划涉及过多字段，故返回的参数时间金额为固定的，并未参数化
    # def update_repayplan_success(self,asset_info):
    #     api = "/repay/querySyRepaymentPlan"
    #     alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
    #     alr_no = alr_info[0]['asset_loan_record_due_bill_no']
    #     mode = {
    #                 "biz_response": {
    #                   "acctNo": "6217003260001430884",
    #                   "bankId": "0105",
    #                   "calDefIntEndDate": "",
    #                   "clearFlag": "",
    #                   "conDpsFlag": "0",
    #                   "conStatus": "1",
    #                   "contBeginDate": "2020-05-01",
    #                   "contEndDate": "2020-10-01",
    #                   "contSystemFlag": "",
    #                   "contractAmt": "8000.00",
    #                   "contractNo": alr_no,
    #                   "extDelayBeginDate": "",
    #                   "extDelayDays": "0",
    #                   "extDelayTerm": "0",
    #                   "feePrestoreAmt": "0.00",
    #                   "loanBalance": "8000.00",
    #                   "loanTerm": "6",
    #                   "maxDelayDays": "0",
    #                   "passBackFlag": "0",
    #                   "preFeeInfoList": [],
    #                   "prestoreAmt": "0.00",
    #                   "recCount": "6",
    #                   "recycleFlag": "0",
    #                   "repayDay": "2020-05-01",
    #                   "repayPlans": [
    #                     {
    #                       "acctFlag": "0",
    #                       "delayFlag": "1",
    #                       "lnsCurAmt": "1305.82",
    #                       "lnsCurFee": "7.90",
    #                       "lnsCurInt": "66.67",
    #                       "lnsDearteDefInt": "0.00",
    #                       "lnsDearteFee": "0.00",
    #                       "lnsDearteFeeAmt": "0.00",
    #                       "lnsDearteInt": "0.00",
    #                       "lnsDearteLatAmt": "0.00",
    #                       "lnsDearteOthAmt": "0.00",
    #                       "lnsDeartePrin": "0.00",
    #                       "lnsDefInt": "0.00",
    #                       "lnsFeeAmt": "0.00",
    #                       "lnsFeeInfoList": [
    #                         {
    #                           "curFeeAmt": "7.90",
    #                           "dearteFeeAmt": "0.00",
    #                           "feeCode": "1201",
    #                           "feeName": "平台分期服务费",
    #                           "recFeeAmt": "0.00",
    #                           "unPaidFeeAmt": "7.90"
    #                         }
    #                       ],
    #                       "lnsLatAmt": "0.00",
    #                       "lnsOthAmt": "0.00",
    #                       "lnsRecDefInt": "0.00",
    #                       "lnsRecFee": "0.00",
    #                       "lnsRecFeeAmt": "0.00",
    #                       "lnsRecInt": "0.00",
    #                       "lnsRecLatAmt": "0.00",
    #                       "lnsRecOthAmt": "0.00",
    #                       "lnsRecPrin": "0.00",
    #                       "overdueDays": "0",
    #                       "overduePeriods": "0",
    #                       "prePayAmt": "8114.07",
    #                       "repayBeginDate": "2020-05-01",
    #                       "repayDate": "",
    #                       "repayEndDate": "2020-05-01",
    #                       "repayTerm": "1",
    #                       "subSection": "1",
    #                       "totalUnPaidAmt": "1380.39",
    #                       "unPaidAmt": "1305.82",
    #                       "unPaidDefInt": "0.00",
    #                       "unPaidFee": "7.90",
    #                       "unPaidFeeAmt": "0.00",
    #                       "unPaidInt": "66.67",
    #                       "unPaidLatAmt": "0.00",
    #                       "unPaidLatOthAmt": "0.00"
    #                     },
    #                     {
    #                       "acctFlag": "0",
    #                       "delayFlag": "1",
    #                       "lnsCurAmt": "1316.71",
    #                       "lnsCurFee": "7.90",
    #                       "lnsCurInt": "55.78",
    #                       "lnsDearteDefInt": "0.00",
    #                       "lnsDearteFee": "0.00",
    #                       "lnsDearteFeeAmt": "0.00",
    #                       "lnsDearteInt": "0.00",
    #                       "lnsDearteLatAmt": "0.00",
    #                       "lnsDearteOthAmt": "0.00",
    #                       "lnsDeartePrin": "0.00",
    #                       "lnsDefInt": "0.00",
    #                       "lnsFeeAmt": "0.00",
    #                       "lnsFeeInfoList": [
    #                         {
    #                           "curFeeAmt": "7.90",
    #                           "dearteFeeAmt": "0.00",
    #                           "feeCode": "1201",
    #                           "feeName": "平台分期服务费",
    #                           "recFeeAmt": "0.00",
    #                           "unPaidFeeAmt": "7.90"
    #                         }
    #                       ],
    #                       "lnsLatAmt": "0.00",
    #                       "lnsOthAmt": "0.00",
    #                       "lnsRecDefInt": "0.00",
    #                       "lnsRecFee": "0.00",
    #                       "lnsRecFeeAmt": "0.00",
    #                       "lnsRecInt": "0.00",
    #                       "lnsRecLatAmt": "0.00",
    #                       "lnsRecOthAmt": "0.00",
    #                       "lnsRecPrin": "0.00",
    #                       "overdueDays": "0",
    #                       "overduePeriods": "0",
    #                       "prePayAmt": "6789.46",
    #                       "repayBeginDate": "2020-06-01",
    #                       "repayDate": "",
    #                       "repayEndDate": "2020-06-01",
    #                       "repayTerm": "2",
    #                       "subSection": "1",
    #                       "totalUnPaidAmt": "1380.39",
    #                       "unPaidAmt": "1316.71",
    #                       "unPaidDefInt": "0.00",
    #                       "unPaidFee": "7.90",
    #                       "unPaidFeeAmt": "0.00",
    #                       "unPaidInt": "55.78",
    #                       "unPaidLatAmt": "0.00",
    #                       "unPaidLatOthAmt": "0.00"
    #                     },
    #                     {
    #                       "acctFlag": "0",
    #                       "delayFlag": "1",
    #                       "lnsCurAmt": "1327.68",
    #                       "lnsCurFee": "7.90",
    #                       "lnsCurInt": "44.81",
    #                       "lnsDearteDefInt": "0.00",
    #                       "lnsDearteFee": "0.00",
    #                       "lnsDearteFeeAmt": "0.00",
    #                       "lnsDearteInt": "0.00",
    #                       "lnsDearteLatAmt": "0.00",
    #                       "lnsDearteOthAmt": "0.00",
    #                       "lnsDeartePrin": "0.00",
    #                       "lnsDefInt": "0.00",
    #                       "lnsFeeAmt": "0.00",
    #                       "lnsFeeInfoList": [
    #                         {
    #                           "curFeeAmt": "7.90",
    #                           "dearteFeeAmt": "0.00",
    #                           "feeCode": "1201",
    #                           "feeName": "平台分期服务费",
    #                           "recFeeAmt": "0.00",
    #                           "unPaidFeeAmt": "7.90"
    #                         }
    #                       ],
    #                       "lnsLatAmt": "0.00",
    #                       "lnsOthAmt": "0.00",
    #                       "lnsRecDefInt": "0.00",
    #                       "lnsRecFee": "0.00",
    #                       "lnsRecFeeAmt": "0.00",
    #                       "lnsRecInt": "0.00",
    #                       "lnsRecLatAmt": "0.00",
    #                       "lnsRecOthAmt": "0.00",
    #                       "lnsRecPrin": "0.00",
    #                       "overdueDays": "0",
    #                       "overduePeriods": "0",
    #                       "prePayAmt": "5453.88",
    #                       "repayBeginDate": "2020-07-01",
    #                       "repayDate": "",
    #                       "repayEndDate": "2020-07-01",
    #                       "repayTerm": "3",
    #                       "subSection": "1",
    #                       "totalUnPaidAmt": "1380.39",
    #                       "unPaidAmt": "1327.68",
    #                       "unPaidDefInt": "0.00",
    #                       "unPaidFee": "7.90",
    #                       "unPaidFeeAmt": "0.00",
    #                       "unPaidInt": "44.81",
    #                       "unPaidLatAmt": "0.00",
    #                       "unPaidLatOthAmt": "0.00"
    #                     },
    #                     {
    #                       "acctFlag": "0",
    #                       "delayFlag": "1",
    #                       "lnsCurAmt": "1338.74",
    #                       "lnsCurFee": "7.90",
    #                       "lnsCurInt": "33.75",
    #                       "lnsDearteDefInt": "0.00",
    #                       "lnsDearteFee": "0.00",
    #                       "lnsDearteFeeAmt": "0.00",
    #                       "lnsDearteInt": "0.00",
    #                       "lnsDearteLatAmt": "0.00",
    #                       "lnsDearteOthAmt": "0.00",
    #                       "lnsDeartePrin": "0.00",
    #                       "lnsDefInt": "0.00",
    #                       "lnsFeeAmt": "0.00",
    #                       "lnsFeeInfoList": [
    #                         {
    #                           "curFeeAmt": "7.90",
    #                           "dearteFeeAmt": "0.00",
    #                           "feeCode": "1201",
    #                           "feeName": "平台分期服务费",
    #                           "recFeeAmt": "0.00",
    #                           "unPaidFeeAmt": "7.90"
    #                         }
    #                       ],
    #                       "lnsLatAmt": "0.00",
    #                       "lnsOthAmt": "0.00",
    #                       "lnsRecDefInt": "0.00",
    #                       "lnsRecFee": "0.00",
    #                       "lnsRecFeeAmt": "0.00",
    #                       "lnsRecInt": "0.00",
    #                       "lnsRecLatAmt": "0.00",
    #                       "lnsRecOthAmt": "0.00",
    #                       "lnsRecPrin": "0.00",
    #                       "overdueDays": "0",
    #                       "overduePeriods": "0",
    #                       "prePayAmt": "4107.24",
    #                       "repayBeginDate": "2020-08-01",
    #                       "repayDate": "",
    #                       "repayEndDate": "2020-08-01",
    #                       "repayTerm": "4",
    #                       "subSection": "1",
    #                       "totalUnPaidAmt": "1380.39",
    #                       "unPaidAmt": "1338.74",
    #                       "unPaidDefInt": "0.00",
    #                       "unPaidFee": "7.90",
    #                       "unPaidFeeAmt": "0.00",
    #                       "unPaidInt": "33.75",
    #                       "unPaidLatAmt": "0.00",
    #                       "unPaidLatOthAmt": "0.00"
    #                     },
    #                     {
    #                       "acctFlag": "0",
    #                       "delayFlag": "1",
    #                       "lnsCurAmt": "1349.90",
    #                       "lnsCurFee": "7.90",
    #                       "lnsCurInt": "22.59",
    #                       "lnsDearteDefInt": "0.00",
    #                       "lnsDearteFee": "0.00",
    #                       "lnsDearteFeeAmt": "0.00",
    #                       "lnsDearteInt": "0.00",
    #                       "lnsDearteLatAmt": "0.00",
    #                       "lnsDearteOthAmt": "0.00",
    #                       "lnsDeartePrin": "0.00",
    #                       "lnsDefInt": "0.00",
    #                       "lnsFeeAmt": "0.00",
    #                       "lnsFeeInfoList": [
    #                         {
    #                           "curFeeAmt": "7.90",
    #                           "dearteFeeAmt": "0.00",
    #                           "feeCode": "1201",
    #                           "feeName": "平台分期服务费",
    #                           "recFeeAmt": "0.00",
    #                           "unPaidFeeAmt": "7.90"
    #                         }
    #                       ],
    #                       "lnsLatAmt": "0.00",
    #                       "lnsOthAmt": "0.00",
    #                       "lnsRecDefInt": "0.00",
    #                       "lnsRecFee": "0.00",
    #                       "lnsRecFeeAmt": "0.00",
    #                       "lnsRecInt": "0.00",
    #                       "lnsRecLatAmt": "0.00",
    #                       "lnsRecOthAmt": "0.00",
    #                       "lnsRecPrin": "0.00",
    #                       "overdueDays": "0",
    #                       "overduePeriods": "0",
    #                       "prePayAmt": "2749.44",
    #                       "repayBeginDate": "2020-09-01",
    #                       "repayDate": "",
    #                       "repayEndDate": "2020-09-01",
    #                       "repayTerm": "5",
    #                       "subSection": "1",
    #                       "totalUnPaidAmt": "1380.39",
    #                       "unPaidAmt": "1349.90",
    #                       "unPaidDefInt": "0.00",
    #                       "unPaidFee": "7.90",
    #                       "unPaidFeeAmt": "0.00",
    #                       "unPaidInt": "22.59",
    #                       "unPaidLatAmt": "0.00",
    #                       "unPaidLatOthAmt": "0.00"
    #                     },
    #                     {
    #                       "acctFlag": "0",
    #                       "delayFlag": "1",
    #                       "lnsCurAmt": "1361.15",
    #                       "lnsCurFee": "7.90",
    #                       "lnsCurInt": "11.34",
    #                       "lnsDearteDefInt": "0.00",
    #                       "lnsDearteFee": "0.00",
    #                       "lnsDearteFeeAmt": "0.00",
    #                       "lnsDearteInt": "0.00",
    #                       "lnsDearteLatAmt": "0.00",
    #                       "lnsDearteOthAmt": "0.00",
    #                       "lnsDeartePrin": "0.00",
    #                       "lnsDefInt": "0.00",
    #                       "lnsFeeAmt": "0.00",
    #                       "lnsFeeInfoList": [
    #                         {
    #                           "curFeeAmt": "7.90",
    #                           "dearteFeeAmt": "0.00",
    #                           "feeCode": "1201",
    #                           "feeName": "平台分期服务费",
    #                           "recFeeAmt": "0.00",
    #                           "unPaidFeeAmt": "7.90"
    #                         }
    #                       ],
    #                       "lnsLatAmt": "0.00",
    #                       "lnsOthAmt": "0.00",
    #                       "lnsRecDefInt": "0.00",
    #                       "lnsRecFee": "0.00",
    #                       "lnsRecFeeAmt": "0.00",
    #                       "lnsRecInt": "0.00",
    #                       "lnsRecLatAmt": "0.00",
    #                       "lnsRecOthAmt": "0.00",
    #                       "lnsRecPrin": "0.00",
    #                       "overdueDays": "0",
    #                       "overduePeriods": "0",
    #                       "prePayAmt": "1380.39",
    #                       "repayBeginDate": "2020-10-01",
    #                       "repayDate": "",
    #                       "repayEndDate": "2020-10-01",
    #                       "repayTerm": "6",
    #                       "subSection": "1",
    #                       "totalUnPaidAmt": "1380.39",
    #                       "unPaidAmt": "1361.15",
    #                       "unPaidDefInt": "0.00",
    #                       "unPaidFee": "7.90",
    #                       "unPaidFeeAmt": "0.00",
    #                       "unPaidInt": "11.34",
    #                       "unPaidLatAmt": "0.00",
    #                       "unPaidLatOthAmt": "0.00"
    #                     }
    #                   ],
    #                   "repayTerm": "0",
    #                   "rpyPlanChgFlag": "00000000",
    #                   "rspCode": "000000",
    #                   "rspMsg": "查询成功",
    #                   "startRec": "1",
    #                   "sumDelayDays": "0",
    #                   "totalDelayCnt": "0",
    #                   "totalRec": "6",
    #                   "totalUnPaidAmt": "8000.00",
    #                   "totalUnPaidDefInt": "0.00",
    #                   "totalUnPaidFee": "47.40",
    #                   "totalUnPaidFeeList": [
    #                     {
    #                       "curFeeAmt": "0.00",
    #                       "dearteFeeAmt": "0.00",
    #                       "feeCode": "1201",
    #                       "feeName": "平台分期服务费",
    #                       "recFeeAmt": "0.00",
    #                       "unPaidFeeAmt": "47.40"
    #                     }
    #                   ],
    #                   "totalUnPaidInt": "234.94",
    #                   "totalUnPaidLatAmt": "0.00",
    #                   "totalUnpaidFeeAmt": "0.00",
    #                   "unPaidPenalty": "0.00",
    #                   "unPaidPreFee": "0.00"
    #                 },
    #                 "code": "10000",
    #                 "msg": "Success",
    #                 "sign": "BAsrukJxSWiw144sQXMaUZB9W3dOeQTkQffce04reJXVC7YYfMY/lNnD/rAtwSvSo1eZLrXiXeMLWVNyUeXaxjgXh79KMWQmeEXL92JEJNQlg5KNMZiCBpSBquF1nAYKgStFNT84xQgz3mEs5EotqoGyZGcsTOz5acGE77eMHWI="
    #               }
    #     str_mode2 = json.dumps(mode)
    #     self.update(api, str(str_mode2))

    def update_repay_plan(self, asset_info):
        api = "/repay/querySyRepaymentPlan"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        alr_info = get_asset_loan_record_by_item_no(asset_info['data']['asset']['item_no'])
        alr_no = alr_info[0]['asset_loan_record_due_bill_no']
        mode = {
            "biz_response": {
              "acctNo": "6217003260001430884",
              "bankId": "0105",
              "calDefIntEndDate": "",
              "clearFlag": "",
              "conDpsFlag": "0",
              "conStatus": "1",
              "contBeginDate": "2020-05-01",
              "contEndDate": "2020-10-01",
              "contSystemFlag": "",
              "contractAmt": asset_info['data']['asset']['amount'],
              "contractNo": alr_no,
              "extDelayBeginDate": "",
              "extDelayDays": "0",
              "extDelayTerm": "0",
              "feePrestoreAmt": "0.00",
              "loanBalance": "8000.00",
              "loanTerm": "6",
              "maxDelayDays": "0",
              "passBackFlag": "0",
              "preFeeInfoList": [],
              "prestoreAmt": "0.00",
              "recCount": "6",
              "recycleFlag": "0",
              "repayDay": "2020-05-01",
              "repayPlans": [],
              "repayTerm": "0",
              "rpyPlanChgFlag": "00000000",
              "rspCode": "000000",
              "rspMsg": "查询成功",
              "startRec": "1",
              "sumDelayDays": "0",
              "totalDelayCnt": "0",
              "totalRec": "6",
              "totalUnPaidAmt": "8000.00",
              "totalUnPaidDefInt": "0.00",
              "totalUnPaidFee": "47.40",
              "totalUnPaidFeeList": [
                {
                  "curFeeAmt": "0.00",
                  "dearteFeeAmt": "0.00",
                  "feeCode": "1201",
                  "feeName": "平台分期服务费",
                  "recFeeAmt": "0.00",
                  "unPaidFeeAmt": "47.40"
                }
              ],
              "totalUnPaidInt": "234.94",
              "totalUnPaidLatAmt": "0.00",
              "totalUnpaidFeeAmt": "0.00",
              "unPaidPenalty": "0.00",
              "unPaidPreFee": "0.00"
            },
            "code": "10000",
            "msg": "Success",
            "sign": "BAsrukJxSWiw144sQXMaUZB9W3dOeQTkQffce04reJXVC7YYfMY/lNnD/rAtwSvSo1eZLrXiXeMLWVNyUeXaxjgXh79KMWQmeEXL92JEJNQlg5KNMZiCBpSBquF1nAYKgStFNT84xQgz3mEs5EotqoGyZGcsTOz5acGE77eMHWI="
          }
        repayment_plan_tmp = {
              "acctFlag": "0",
              "delayFlag": "1",
              "lnsCurAmt": "1338.74",
              "lnsCurFee": "7.90",
              "lnsCurInt": "33.75",
              "lnsDearteDefInt": "0.00",
              "lnsDearteFee": "0.00",
              "lnsDearteFeeAmt": "0.00",
              "lnsDearteInt": "0.00",
              "lnsDearteLatAmt": "0.00",
              "lnsDearteOthAmt": "0.00",
              "lnsDeartePrin": "0.00",
              "lnsDefInt": "0.00",
              "lnsFeeAmt": "0.00",
              "lnsFeeInfoList": [
                {
                  "curFeeAmt": "7.90",
                  "dearteFeeAmt": "0.00",
                  "feeCode": "1201",
                  "feeName": "平台分期服务费",
                  "recFeeAmt": "0.00",
                  "unPaidFeeAmt": "7.90"
                }
              ],
              "lnsLatAmt": "0.00",
              "lnsOthAmt": "0.00",
              "lnsRecDefInt": "0.00",
              "lnsRecFee": "0.00",
              "lnsRecFeeAmt": "0.00",
              "lnsRecInt": "0.00",
              "lnsRecLatAmt": "0.00",
              "lnsRecOthAmt": "0.00",
              "lnsRecPrin": "0.00",
              "overdueDays": "0",
              "overduePeriods": "0",
              "prePayAmt": "4107.24",
              "repayBeginDate": "2020-08-01",
              "repayDate": "",
              "repayEndDate": "2020-08-01",
              "repayTerm": "4",
              "subSection": "1",
              "totalUnPaidAmt": "1380.39",
              "unPaidAmt": "1338.74",
              "unPaidDefInt": "0.00",
              "unPaidFee": "7.90",
              "unPaidFeeAmt": "0.00",
              "unPaidInt": "33.75",
              "unPaidLatAmt": "0.00",
              "unPaidLatOthAmt": "0.00"
            }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['repayTerm'] = i + 1
            repayment_plan['lnsCurAmt'] = float(fee_info['principal']) / 100
            repayment_plan['lnsCurInt'] = float(fee_info['interest']) / 100
            repayment_plan['lnsCurFee'] = float(fee_info['service']) / 100
            repayment_plan['lnsFeeInfoList'][0]['curFeeAmt'] = float(fee_info['service']) / 100
            repayment_plan['repayBeginDate'] = fee_info['date']
            repayment_plan['repayEndDate'] = fee_info['date']
            mode['biz_response']['repayPlans'].append(repayment_plan)
        self.update(api, mode)

    def update_loanconfirmquery_fail(self, asset_info):
      api = "/queryIntoPiecesStatus"
      mode = '''{
                "code": "10000",
                "msg": "Success",
                "biz_response": {
                  "resCode": "1",
                  "uuid":  function({
                    _req
                  }) {
                    return _req.body.uuid
                  },
                  "resMessage": "",
                  "loan": %s,
                  "completeTime": "@now",
                  "mortgagorName": null,
                  "mortgagorNameEncrypt": "%s",
                  "mobile": null,
                  "mobileEncrypt": "%s",
                  "loanReturnAccount": null,
                  "loanReturnAccountEncrypt": "%s",
                  "status": "4",
                  "intoPiecesId": "@integer(100000000000, 800000000000)"
                }
              }''' % (asset_info['data']['asset']['amount'], asset_info['data']['borrower']['name_encrypt'],
                      asset_info['data']['borrower']['tel_encrypt'], asset_info['data']['receive_card']['num_encrypt'])
      self.update(api, mode)

    def update_loanapplynew_fail(self):
          api = "/receiveContract"
          mode = '''{
                      "biz_response": {
                        "resCode": "2001",
                        "resMessage": "进件失败",
                        "uuid": function({
                          _req
                        }) {
                          return _req.body.uuid
                        },
                        "intoPiecesId": ""
                      },
                      "code": "10000",
                      "msg": "Success",
                      "sign": "nTxXjorE4toYjdGkkBySfnXY5k3LKwuYm0PuVhPjwujqNQjBi7gd0KmnrTIcvklRhxKqrn+8VPhD1e9uiendRriytsvEC+2smrTZhJ7MMeRbzyuxnG3z6FAyTb4jqb2WLG/J1VLN5GROt1yatY8KTDeDEp48bgvX95o2CJ8iHj0="
                      }'''
          self.update(api, mode)

    def update_loanwait_fail(self, four_element):
        api = "/queryIntoPiecesStatus"
        mode = '''{
                  "code": "10000",
                  "msg": "Success",
                  "biz_response": {
                    "resCode": "1",
                    "uuid":  function({
                      _req
                    }) {
                      return _req.body.uuid
                    },
                    "resMessage": "失败",
                    "loan": 0,
                    "completeTime": "@now",
                    "mortgagorName": null,
                    "mortgagorNameEncrypt": "%s",
                    "mobile": null,
                    "mobileEncrypt": "%s",
                    "loanReturnAccount": null,
                    "loanReturnAccountEncrypt": "%s",
                    "status": "2",
                    "intoPiecesId": ""
                  }
                }''' % (four_element['data']['user_name_encrypt'], four_element['data']['phone_number_encrypt'],
                        four_element['data']['bank_code_encrypt'])
        self.update(api, mode)

if __name__ == "__main__":
    pass
