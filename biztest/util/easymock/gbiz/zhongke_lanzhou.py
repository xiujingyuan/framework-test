# -*- coding: utf-8 -*-
from biztest.function.cmdb.cmdb_common_function import get_fee_info_by_period
from biztest.interface.cmdb.cmdb_interface import cmdb_rate_loan_calculate_v6
from biztest.util.easymock.easymock import Easymock
from biztest.function.gbiz.gbiz_db_function import get_asset_loan_record_by_item_no
from copy import deepcopy
from biztest.util.tools.tools import *


class ZhongkeLanzhouMock(Easymock):
    def update_pre_tied_card(self):
        api = "/lanzhou/preTiedCard"
        mode = '''{
          "transDate": "2020-10-12",
          "transTime": "12:02:22",
          "respCode": "0000",
          "respMsg": "交易接收成功"
        }'''
        self.update(api, mode)

    def update_pre_tied_card_fail(self):
        api = "/lanzhou/preTiedCard"
        mode = '''{
          "transDate": "2020-10-12",
          "transTime": "12:02:22",
          "respCode": "9000",
          "respMsg": "交易接收失败"
        }'''
        self.update(api, mode)

    def update_tied_card(self):
        api = "/lanzhou/tiedCard"
        mode = '''{
          "transDate": "2020-10-12",
          "transTime": "12:02:22",
          "respCode": "0000",
          "respMsg": "交易接收成功"
        }'''
        self.update(api, mode)

    def update_tied_card_fail(self):
        api = "/lanzhou/tiedCard"
        mode = '''{
          "transDate": "2020-10-12",
          "transTime": "12:02:22",
          "respCode": "9000",
          "respMsg": "交易接收失败"
        }'''
        self.update(api, mode)

    def update_tied_card_query_success(self):
        api = "/lanzhou/tiedCardQuery"
        mode = '''{
          "msgId": "103462334671122432",
          "reCode": "S",
          "bizRespCode": "0000",
          "bizRespMsg": "交易成功",
          "transDate": "2020-10-12",
          "transTime": "12:10:51",
          "respCode": "9999",
          "respMsg": "交易处理成功"
        }'''
        self.update(api, mode)

    def update_tied_card_query_process(self):
        api = "/lanzhou/tiedCardQuery"
        mode = '''{
          "msgId": "103462334671122432",
          "reCode": "I",
          "bizRespCode": "0000",
          "bizRespMsg": "绑卡中",
          "transDate": "2020-10-12",
          "transTime": "12:10:51",
          "respCode": "0000",
          "respMsg": "交易接收成功"
        }'''
        self.update(api, mode)

    def update_tied_card_query_nodata(self):
        api = "/lanzhou/tiedCardQuery"
        mode = '''{
          "transDate": "2020-10-12",
          "transTime": "12:03:52",
          "respCode": "9000",
          "respMsg": "无绑卡记录"
        }'''
        self.update(api, mode)

    def update_tied_card_query_fail(self):
        api = "/lanzhou/tiedCardQuery"
        mode = '''{
          "msgId": "104181436000276480",
          "reCode": "F",
          "bizRespCode": "BF00105",
          "bizRespMsg": "短信验证码校验失败",
          "transDate": "2020-10-14",
          "transTime": "14:50:49",
          "respCode": "9000",
          "respMsg": "交易处理失败"
        }'''
        self.update(api, mode)

    def update_pretiedcardquey_success(self):
        api = "/lanzhou/preTiedCardQuery"
        mode = '''{
              "msgId": "@id",
              "respCode": "9999", //9999是成功、9000-失败
              "respMsg": "交易处理成功",
              "reCode": "S", //F是失败
              "bizRespCode": "0000", //BF00436	交易类型不存在
              "bizRespMsg": "111123测试",
              "transDate": "2021-04-07",
              "transTime": "12:12:12"
            }'''
        self.update(api, mode)

    def update_pretiedcardquey_fail(self):
        api = "/lanzhou/preTiedCardQuery"
        mode = '''{
              "msgId": "@id",
              "respCode": "9000", //9999是成功、9000-失败
              "respMsg": "交易处理失败",
              "reCode": "F", //F是失败
              "bizRespCode": "BF21030", //BF00436	交易类型不存在
              "bizRespMsg": "短信码错误",
              "transDate": "2021-04-07",
              "transTime": "12:12:12"
            }'''
        self.update(api, mode)

    def update_pretiedcardquey_process(self):
        api = "/lanzhou/preTiedCardQuery"
        mode = '''{
            "msgId": "@id",
            "transDate": "2021-04-16",
            "transTime": "17:53:13",
            "respCode": "0000",
            "respMsg": "交易接收成功"
        }'''
        self.update(api, mode)

    def update_loan_rate_query(self):
        api = "/lanzhou/loanRateQuery"
        mode = '''{
          "businessrate": "7.5",
          "transDate": "2020-10-12",
          "transTime": "12:35:48",
          "respCode": "9999",
          "respMsg": "交易处理成功"
        }'''
        self.update(api, mode)

    def update_ftp_upload_success(self):
        api = "/capital/ftp/upload/lanzhou"
        mode = {
            "code": 0,
            "message": "",
            "data": {
                "dir": "/mock_dir/",
                "name": "mock_agreement.pdf",
                "type": "mock协议",
                "result": {
                    "code": 0,
                    "message": "成功"
                }
            }
        }
        self.update(api, mode)

    def update_file_notice(self):
        api = "/lanzhou/fileNotice"
        mode = '''{
          "transDate": "2020-10-12",
          "transTime": "12:37:44",
          "respCode": "0000",
          "respMsg": "交易接收成功"
        }'''
        self.update(api, mode)

    def update_customer_info_push(self):
        api = "/lanzhou/customerInfoPush"
        mode = '''{
          "transDate": "2020-10-12",
          "transTime": "12:37:47",
          "respCode": "0000",
          "respMsg": "交易接收成功"
        }'''
        self.update(api, mode)

    def update_face_recognition(self):
        api = "/lanzhou/faceRecognition"
        mode = '''{
          "transDate": "2020-10-12",
          "transTime": "12:37:47",
          "respCode": "0000",
          "respMsg": "交易接收成功"
        }'''
        self.update(api, mode)

    def update_customer_face_query_success(self):
        api = "/lanzhou/cusFaceQuery"
        mode = '''{
          "result": "01",
          "resultMsg": "成功",
          "transDate": "2020-10-12",
          "transTime": "12:37:50",
          "respCode": "9999",
          "respMsg": "交易接收成功"
        }'''
        self.update(api, mode)

    def update_customer_face_query_fail(self):
        api = "/lanzhou/cusFaceQuery"
        mode = '''{
            "result": "02",
            "resultMsg": "处理失败",
            "transDate": "2020-10-14",
            "transTime": "10:50:14",
            "respCode": "9000",
            "respMsg": "交易处理失败"
        }'''
        self.update(api, mode)

    def update_loan_apply(self):
        api = "/lanzhou/loanApply"
        mode = '''{
          "transDate": "2020-10-12",
          "transTime": "12:37:47",
          "respCode": "0000",
          "respMsg": "交易接收成功"
        }'''
        self.update(api, mode)

    def update_loan_query_success(self, asset_info):
        api = "/lanzhou/loanQuery"
        mode = '''{
            "merserno": function({
              _req
            }) {
              return _req.body.merserno
            },
            "contractNo": "66506",
            "loanid": "id_%s",
            "loanamt": %s,
            "loanyrate": 7.5,
            "loanstartdate": "%s",
            "loanenddate": "20211012",
            "loanstate": "04",
            "loanmess": "交易成功",
            "fee": 0,
            "transDate": "%s",
            "transTime": "12:33:20",
            "respCode": "9999",
            "respMsg": "交易处理成功"
        }''' % (get_guid(),
                asset_info['data']['asset']['amount'],
                get_date(fmt="%Y%m%d"),
                get_date(fmt="%Y-%m-%d"))
        self.update(api, mode)

    def update_loan_query_fail(self):
        api = "/lanzhou/loanQuery"
        mode = '''{
          "merserno": function({
              _req
            }) {
              return _req.body.merserno
            },
          "contractNo": "127684201014105247",
          "loanstate": "09",
          "fee": 0,
          "transDate": "2020-10-14",
          "transTime": "16:01:23",
          "respCode": "9999",
          "respMsg": "交易处理成功"
        }'''
        self.update(api, mode)

    def update_repay_plan(self, asset_info):
        api = "/lanzhou/repaymentPlanQuery"
        rate_info = cmdb_rate_loan_calculate_v6(asset_info)
        mode = {
            "merserno": asset_info['data']['asset']['item_no'],
            "paymentPlan": [],
            "transDate": "2020-10-12",
            "transTime": "12:44:33",
            "respCode": "9999",
            "respMsg": "交易处理成功"
        }
        repayment_plan_tmp = {
            "tpnum": 1,
            "loanenddate": "20201112",
            "payprincipalamt": 801.37,
            "actualpayprincipalamt": 0,
            "payinterestamt": 70.83,
            "actualpayinterestamt": 0,
            "payprincipalpenaltyamt": 0,
            "actualpayprincipalpenaltyamt": 0,
            "ispreps": "0"
        }
        for i in range(asset_info['data']['asset']['period_count']):
            fee_info = get_fee_info_by_period(rate_info, i + 1)
            repayment_plan = deepcopy(repayment_plan_tmp)
            repayment_plan['tpnum'] = i + 1
            repayment_plan['payprincipalamt'] = float(fee_info['principal']) / 100
            repayment_plan['payinterestamt'] = float(fee_info['interest']) / 100
            repayment_plan['loanenddate'] = fee_info['date'].replace("-", "")
            mode['paymentPlan'].append(repayment_plan)
        self.update(api, mode)


if __name__ == "__main__":
    pass
