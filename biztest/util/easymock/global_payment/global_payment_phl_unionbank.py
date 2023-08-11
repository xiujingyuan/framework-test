from biztest.config.payment.url_config import global_rapyd_payment_id, global_rapyd_paid_at, global_amount, \
    xendit_redirect_url, xendit_resp_payment_mode, xendit_ebank_resp_payment_mode
from biztest.util.easymock.easymock import Easymock


class UnionbankMock(Easymock):

    # 用户中心mock
    def update_fk_userinfo(self, account_no, bank_code="LBP", withdraw_type="bank"):
        api = "/phl/v1/biz/getUserInfo"
        if withdraw_type == "bank":
            mode = {
                "code": 0,
                "data": {
                    "accountNoEncrypt": account_no,  # 线上放款返回的数据
                    "bankCardCode": bank_code,
                    "bankCardMethod": 1,  # 1.Bank Account银行账户 2.E-Wallet电子钱包 3.Cash pickup（线下取款这个暂时没有用）
                    "birthday": "08/19/1978",
                    "civilStatusId": 0,
                    "fullnameEncrypt": "enc_04_3676045626170679296_741",
                    "gender": "female",
                    "idType": "UMID (unified multi-purpose ID)",
                    "idcardPicUrl": "https://dxcloud-sg-ph-prod.oss-ap-southeast-1.aliyuncs.com/20210927/Z3RNVnVWcFhTOXNU",
                    "identificationIdEncrypt": "enc_04_3676045921617453056_080",
                    "identificationTypeId": 1,
                    "locationEncrypt": "enc_04_3676046388007280640_167",
                    "motherMaidenNameEncrypt": "enc_04_3676046601648349184_239",
                    "phoneEncrypt": "enc_04_3676046762994835456_519"
                },
                "msg": "success"
            }
        elif withdraw_type == "Gcash":
            mode = {
                "code": 0,
                "data": {
                    "accountNoEncrypt": account_no,
                    "bankCardCode": "GCash",
                    "bankCardMethod": 2,  # 1.Bank Account银行账户 2.E-Wallet电子钱包 3.Cash pickup（线下取款这个暂时没有用）
                    "birthday": "03/20/1984",
                    "civilStatusId": 0,
                    "fullnameEncrypt": "enc_04_3676045626170679296_741",
                    "gender": "male",
                    "idType": "UMID (unified multi-purpose ID)",
                    "idcardPicUrl": "https://dxcloud-sg-ph-prod.oss-ap-southeast-1.aliyuncs.com/cWtlcXcxQ3FJeGQ120220527",
                    "identificationIdEncrypt": "enc_04_3676045921617453056_080",
                    "identificationTypeId": 1,
                    "locationEncrypt": "enc_04_3676046388007280640_167",
                    "motherMaidenNameEncrypt": "enc_04_3676046601648349184_239",
                    "phoneEncrypt": "enc_04_3676046762994835456_519"
                },
                "msg": "success"
            }
        elif withdraw_type == "Paymaya":
            mode = {
                "code": 0,
                "data": {
                    "accountNoEncrypt": account_no,
                    "bankCardCode": "Paymaya",
                    "bankCardMethod": 2,  # 1.Bank Account银行账户 2.E-Wallet电子钱包 3.Cash pickup（线下取款这个暂时没有用）
                    "birthday": "03/20/1984",
                    "civilStatusId": 0,
                    "fullnameEncrypt": "enc_04_3676045626170679296_741",
                    "gender": "male",
                    "idType": "UMID (unified multi-purpose ID)",
                    "idcardPicUrl": "https://dxcloud-sg-ph-prod.oss-ap-southeast-1.aliyuncs.com/cWtlcXcxQ3FJeGQ120220527",
                    "identificationIdEncrypt": "enc_04_3676045921617453056_080",
                    "identificationTypeId": 1,
                    "locationEncrypt": "enc_04_3676046388007280640_167",
                    "motherMaidenNameEncrypt": "enc_04_3676046601648349184_239",
                    "phoneEncrypt": "enc_04_3676046762994835456_519"
                },
                "msg": "success"
            }
        else:
            return
        self.update(api, mode)

    def update_unionbank_withdraw(self, status, channel_key, uuid):
        api = "/partners/v3/instapay/transfers/single"
        if status == "success":
            mode = {  # 取code+description
                "code": "TS",
                "senderRefId": channel_key,
                "state": "Credited Beneficiary Account",
                "uuid": "03b87469-5d5d-4038-8251-f2a1b970420c",
                "description": "Successful transaction",
                "type": "INSTAPAY",
                "amount": "11.42",
                "ubpTranId": "UB361",
                "reversalUbpTranId": None,
                "coreRefId": "2302114500376687994",
                "traceNo": "854083",
                "tranRequestDate": "2022-07-15T10:11:32.000"
            }
        # unionbank发起放款请求的时候失败会有很多种，不同的返回我们解析code和message保存的字段也都不一样
        elif status == "fail_test1":
            mode = {  # 取httpCode+httpMessage
                "httpCode": "500",
                "httpMessage": "Internal Server Error",
                "moreInformation": "Cannot read property 'toString' of null"
            }
        elif status == "fail_test2":
            mode = {  # 取error.code+details.message（details没返回则取error.message）
                "error": [
                    {
                        "code": -1,
                        "message": "Missing/Invalid Parameters.",
                        "details": [
                            {
                                "field": "beneficiary.name",
                                "message": "beneficiary.name you entered has invalid characters."
                            }
                        ]
                    }
                ]
            }
        elif status == "fail_test2_1":
            mode = {  # 取error.code+details.message（details没返回则取error.message）
                "error": [
                    {
                        "code": -1,
                        "message": "Missing/Invalid Parameters.",
                        "details": [
                            {
                                "field": "beneficiary.name",
                                "message": None
                            }
                        ]
                    }
                ]
            }
        elif status == "fail_test3":
            mode = {  # 优先取details.coreCode+detailssmessage；details没返回就取errors.code+errors.description
                "errors": [
                    {
                        "code": "TF",
                        "description": "Failed to credit Beneficiary Account",
                        "details": {
                            "senderRefId": channel_key,
                            "tranRequestDate": "2022-06-08T14:46:03.000",
                            "uuid": "a7397420-ac0f-4e0d-bc3c-80fe5e926120",
                            "coreCode": "F",
                            "message": "UNABLE TO PROCESS",
                            "coreRefId": "CONVB190808000001",
                            "traceNo": "210939",
                            "ubpTranId": "UB136",
                            "reversalUbpTranId": "UB137"
                        }
                    }
                ]
            }
        elif status == "fail_test3_1":
            mode = {  # 优先取details.coreCode+detailssmessage；details没返回就取errors.code+errors.description
                "errors": [
                    {
                        "code": "TF",
                        "description": "Failed to credit Beneficiary Account",
                        "details": {
                            "senderRefId": channel_key,
                            "tranRequestDate": "2022-06-08T14:46:03.000",
                            "uuid": "a7397420-ac0f-4e0d-bc3c-80fe5e926120",
                            "coreCode": None,
                            "message": None,
                            "coreRefId": "CONVB190808000001",
                            "traceNo": "210939",
                            "ubpTranId": "UB136",
                            "reversalUbpTranId": "UB137"
                        }
                    }
                ]
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode)

    def update_unionbank_withdraw_query(self, status, channel_key, uuid=None):
        api = "/partners/v3/instapay/transfers/single/" + channel_key
        if status == "success":
            mode = {
                "record": {
                    "senderRefId": channel_key,
                    "code": "TS",
                    "uuid": uuid,
                    "state": "Credited Beneficiary Account",
                    "description": "Successful transaction",
                    "type": "INSTAPAY",
                    "amount": global_amount / 100,
                    "ubpTranId": "UB361",
                    "reversalUbpTranId": None,
                    "coreRefId": "2302114500376687994",
                    "traceNo": "854083",
                    "tranRequestDate": "2022-07-15T10:11:32.000Z",
                    "tranFinacleDate": "2022-03-10",
                    "createdAt": "2022-07-15T10:11:45.000Z",
                    "updatedAt": "2022-07-15T10:11:48.000Z"
                }
            }
        elif status == "fail":
            mode = {
                "record": {
                    "senderRefId": channel_key,
                    "code": "TF",
                    "uuid": uuid,
                    "state": "Credited Beneficiary Account",
                    "description": "Failed to credit Beneficiary Account",
                    "type": "INSTAPAY",
                    "amount": global_amount / 100,
                    "ubpTranId": "UB361",
                    "reversalUbpTranId": None,
                    "coreRefId": "2302114500376687994",
                    "traceNo": "854083",
                    "tranRequestDate": "2022-07-15T10:11:32.000Z",
                    "tranFinacleDate": "2022-03-10",
                    "createdAt": "2022-07-15T10:11:45.000Z",
                    "updatedAt": "2022-07-15T10:11:48.000Z"
                }
            }
        elif status == "process":
            mode = {
                "record": {
                    "senderRefId": channel_key,
                    "code": "SP",
                    "uuid": uuid,
                    "state": "Credited Beneficiary Account",
                    "description": "Successful transaction",
                    "type": "INSTAPAY",
                    "amount": global_amount / 100,
                    "ubpTranId": "UB361",
                    "reversalUbpTranId": None,
                    "coreRefId": "2302114500376687994",
                    "traceNo": "854083",
                    "tranRequestDate": "2022-07-15T10:11:32.000Z",
                    "tranFinacleDate": "2022-03-10",
                    "createdAt": "2022-07-15T10:11:45.000Z",
                    "updatedAt": "2022-07-15T10:11:48.000Z"
                }
            }
        elif status == "notexsit":
            mode = {
                "errors": [
                    {
                        "code": -2,
                        "message": "Transaction Not Found."
                    }
                ]
            }
        elif status == "none":
            mode = [

            ]
        elif status == "error":
            mode = {"_res": {"status": 500}}
        else:
            pass
        # self.update(api, mode)
        self.update_by_api_id("62a084a7b22a72002044d0da", api, mode, "get")

    def update_unionbank_balance(self, status):
        api = "/portal/accounts/v1/transactions"
        if status == "success":
            mode = {
                "records": [{
                    "recordNumber": "1",
                    "tranId": "S869993",
                    "tranType": "D",
                    "amount": "36.81",
                    "currency": "PHP",
                    "tranDate": "2017-03-25T00:00:00.000",
                    "remarks2": "",
                    "remarks": "Interest run",
                    "balance": "99741.14",
                    "balanceCurrency": "PHP",
                    "postedDate": "2017-07-28T22:31:13.000",
                    "tranDescription": "100018122478:Int.Pd:01-01-2017 to 03-31-2017"
                }],
                "totalRecords": "1",
                "lastRunningBalance": "100048.070000"  # unionbank的可用余额
            }
        elif status == "fail":
            mode = {
                "records": []
            }
        elif status == "500":
            mode = {"_res": {"status": 500}}
        else:
            pass
        self.update(api, mode, method='get')
