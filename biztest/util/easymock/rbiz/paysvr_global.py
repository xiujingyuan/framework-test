# -*- coding: utf-8 -*-
from biztest.config.global_rbiz.paysvr_global_mock_config import global_mock_auto_pay_mode, \
    global_mock_withhold_query_mode
from biztest.util.easymock.easymock import *
from biztest.config.rbiz.url_config import *


class PaysvrMockGlobal(Easymock):
    auto_pay_path = mock_global_paysvr_auto_pay_path
    withhold_query_path = mock_global_paysvr_withhold_query_path
    auto_pay_mode = global_mock_auto_pay_mode
    withhold_query_mode = global_mock_withhold_query_mode

    def __init__(self, user, password, project):
        super(PaysvrMockGlobal, self).__init__(user, password, project)

    def update_auto_pay_withhold_success(self, item_no):
        self.auto_pay_mode['code'] = 0
        self.auto_pay_mode['data']['status'] = 2
        self.auto_pay_mode['data']['channel_key'] = item_no
        self.update(self.auto_pay_path, self.auto_pay_mode)

    def update_auto_pay_withhold_fail(self):
        self.auto_pay_mode['code'] = 1
        self.auto_pay_mode['data']['status'] = 3
        self.update(self.auto_pay_path, self.auto_pay_mode)

    def update_auto_pay_withhold_proccess(self, item_no):
        self.auto_pay_mode['code'] = 2
        self.auto_pay_mode['data']['status'] = 1
        self.auto_pay_mode['data']['channel_key'] = item_no
        self.update(self.auto_pay_path, self.auto_pay_mode)

    def update_withhold_query_success(self, item_no):
        self.withhold_query_mode['code'] = 0
        self.withhold_query_mode['data']['status'] = 2
        self.auto_pay_mode['data']['channel_key'] = item_no
        self.update(self.withhold_query_path, self.withhold_query_mode)

    def update_withhold_query_fail(self, item_no):
        self.withhold_query_mode['code'] = 1
        self.withhold_query_mode['data']['status'] = 3
        self.auto_pay_mode['data']['channel_key'] = item_no
        self.update(self.withhold_query_path, self.withhold_query_mode)

    def update_withhold_query_process(self, item_no):
        self.withhold_query_mode['code'] = 2
        self.withhold_query_mode['data']['status'] = 1
        self.auto_pay_mode['data']['channel_key'] = item_no
        self.update(self.withhold_query_path, self.withhold_query_mode)

