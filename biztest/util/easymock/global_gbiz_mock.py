from biztest.util.easymock.easymock import Easymock
from biztest.util.http.http_util import Http
from biztest.util.tools.tools import get_date, get_random_str, get_tz
import common.global_const as gc


class GlobalGbizMock(Easymock):
    def update_indiviudal_bank_info(self):
        api = "/tha/individual/getBankInfoByCardUUID"
        mode = '''{
          "data": {
            "bank_card_no_encrypt": "enc_03_2845502923004715008_044",
            "bank_card_bank_name": "Bangkok Bank"
          }
        }'''
        self.update(api, mode)

    def manual_asset_loan_success(self, item_no):
        url = gc.GRANT_URL + "/tha_bankcard/changeStatus"
        header = {"Content-Type": "application/json"}
        body = {
            "key": "manual_asset_change_%s" % get_random_str(10),
            "type": "ThaBankcardNotify",
            "from_system": "BIZ",
            "data": {
                "item_no": item_no,
                "status": "repay",
                "finish_at": get_date(),
                "err_msg": ""
            }
        }
        Http.http_post(url, body, header)


    def manual_asset_loan_fail(self, item_no):
        url = gc.GRANT_URL + "/tha_bankcard/changeStatus"
        header = {"Content-Type": "application/json"}
        body = {
            "key": "manual_asset_change_%s" % get_random_str(10),
            "type": "ThaBankcardNotify",
            "from_system": "BIZ",
            "data": {
                "item_no": item_no,
                "status": "void",
                "finish_at": "",
                "err_msg": "放款失败"
            }
        }
        Http.http_post(url, body, header)

    def manual_asset_update_card(self, item_no):
        url = gc.GRANT_URL+ "/tha_bankcard/changeStatus"
        header = {"Content-Type": "application/json"}
        body = {
            "key": "manual_asset_change_%s" % get_random_str(10),
            "type": "ThaBankcardNotify",
            "from_system": "BIZ",
            "data": {
                "item_no": item_no,
                "status": "update_card",
                "finish_at": "",
                "err_msg": "银行卡异常"
            }
        }
        Http.http_post(url, body, header)

    def update_card(self, asset_info, card_uuid="1234567890"):
        url = gc.GRANT_URL + "/paydayloan/update-receive-card"
        header = {"Content-Type": "application/json"}
        body = {
            "key": "update_card_%s" % get_random_str(10),
            "type": "UpdateCard",
            "from_system": "DSQ",
            "data": {
                "card_uuid": card_uuid,
                "id_num": asset_info['data']['borrower']['id_num'],
                "item_no": asset_info['data']['asset']['item_no']
            }
        }
        Http.http_post(url, body, header)

    def nbmfc_loan_success(self, item_no):
        url = gc.GRANT_URL + "/nbmfc/changeStatus"
        header = {"Content-Type": "application/json"}
        body = {
            "key": "manual_asset_change_%s" % get_random_str(10),
            "type": "NbmfcNotify",
            "from_system": "BIZ",
            "data": {
                "item_no": item_no,
                "order_no": "DBN"+item_no,
                "account_type": "Easypaisa",
                "account_no": "enc_03_3554539588658143232_639",
                "status": "repay",
                "err_msg": "放款成功",
                "finish_at": get_date(timezone=get_tz(gc.COUNTRY))
            }
        }
        Http.http_post(url, body, header)

    def nbmfc_loan_fail(self, item_no):
        url = gc.GRANT_URL + "/nbmfc/changeStatus"
        header = {"Content-Type": "application/json"}
        body = {
            "key": "manual_asset_change_%s" % get_random_str(10),
            "type": "NbmfcNotify",
            "from_system": "BIZ",
            "data": {
                "item_no": item_no,
                "status": "void",
                "err_msg": "卡号有误",
                "finish_at": get_date(timezone=get_tz())
            }
        }
        Http.http_post(url, body, header)

    def update_user_info(self):
        api = "/v1/biz/getUserInfo"
        mode = '''{
          "code": 0,
          "msg": "success",
          "data": {
            "email_encrypt": "enc_05_3552579410329083904_922",
            "name_encrypt": "enc_04_3552625523933323264_485",
            "father_name_encrypt": "enc_04_3552625523882991616_093",
            "gender": "female",
            "phone_encrypt": "enc_01_3552563306634420224_953",
            "id_number_encrypt": "enc_02_3552625523966877696_554",
            "bank_card_type": 1,
            "bank_card_bank_name": "KSN IMMWENNNN BANK.",
            "bank_card_account_encrypt": "enc_03_3573347754854320128_693"
          }
        }'''
        self.update(api, mode)
