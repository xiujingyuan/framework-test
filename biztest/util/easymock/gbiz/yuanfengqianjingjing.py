from biztest.util.easymock.easymock import Easymock
from biztest.util.tools.tools import get_date, get_guid


class YuanfengqianjingjingMock(Easymock):
    def update_loan_grant_status_push(self):
        """
        批量新增贷款接口（仅用于数据同步,同步贷款信息）
        """
        api = "/yuanfeng/yuanfengqianjingjing/api/assets/v1"
        mode = {
                "code": 0,
                "message": "success",
                "data": {
                    "errcode": "0",
                    "errmsg": "新增成功！"
                }
            }
        self.update(api, mode)


    def update_loan_grant_status_repeat_push(self):
        """
        批量新增贷款接口（仅用于数据同步,同步贷款信息）
        推送成功之后，重复推送
        """
        api = "/yuanfeng/yuanfengqianjingjing/api/assets/v1"
        mode = {
                "code": "A0440",
                "message": "test:部分贷款信息已存在，A20230728084555227176",
                "data": None
            }
        self.update(api, mode)

    def update_contract_push(self, code=0, errcode="0"):
        api = "/yuanfeng/yuanfengqianjingjing/api/v2/doc/upload"
        mode = {
                  "code": code,
                  "message": "success",
                  "data": {
                    "errcode": errcode,
                    "errmsg": "ok",
                    "data": "@id"
                  }
                }
        self.update(api, mode)