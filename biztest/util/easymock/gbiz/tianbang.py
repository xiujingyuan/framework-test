# -*- coding: utf-8 -*-
from biztest.util.easymock.easymock import Easymock


class TianBang(Easymock):
    def update_guarantee_apply_success(self):
        api = "/tianbang/sign/request"
        mode = {"resultCode": "000000", "resultMsg": "成功", "data": None, "extra": None}
        self.update(api, mode)

    def update_guarantee_down_success(self):
        api = "/tianbang/sign/get"
        mode = {"resultCode": "000000",
                "resultMsg": "获取下载连接成功",
                "data": {
                    "57": "https://120.25.135.98/win/contract/sign/download/KNQN01/20200907/57/"
                          "KNQN01_qn_whl_1599460614897_57.pdf",
                    "52": "https://120.25.135.98/win/contract/sign/download/KNQN01/20200907/52/"
                          "KNQN01_qn_whl_1599460614897_52.pdf"},
                "extra": None}
        self.update(api, mode)

    def update_guarantee_sync_success(self):
        api = "/tianbang/loan/status"
        mode = {"resultCode": "000000", "resultMsg": "成功", "data": None, "extra": None}
        self.update(api, mode)


if __name__ == "__main__":
    pass
