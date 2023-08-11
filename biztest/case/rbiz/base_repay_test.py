#!/usr/bin/python
# -*- coding: UTF-8 -*-
import json

import allure

from biztest.function.rbiz.rbiz_check_function import check_card_by_item_no, check_individual_by_item_no, \
    check_json_rs_data, time
from biztest.function.rbiz.rbiz_db_function import get_task_by_order_no_and_task_type, string_split, string_truncation, \
    get_withhold_by_item_no
from biztest.interface.rbiz.biz_central_interface import run_task_in_biz_central
from biztest.interface.rbiz.rbiz_interface import sync_withhold_card, refresh_late_fee, simple_active_repay, \
    combo_active_repay_without_no_loan, asset_recharge_success_account_to_biz_by_api, \
    asset_repay_success_account_to_biz_by_api, asset_repay_success_asset_change_to_biz_by_api, \
    asset_withhold_success_to_biz_by_api, change_asset_due_at_by_test_platform
from biztest.util.http.http_util import Http
from biztest.util.task.task import Task
from biztest.util.msg.msg import Msg
from biztest.util.log.log_util import LogUtil
from biztest.util.tools.tools import get_four_element, get_guid
import common.global_const as gc


class BaseRepayTest(object):

    def init(self, env):
        self.task = Task("rbiz%s" % env)
        self.msg = Msg("rbiz%s" % env)
        self.item_no = self.item_num_no_loan = ""
        LogUtil.log_info("BaseRepayTest.init()...env=%s" % env)

    def change_asset_due_at(self, advance_month, advance_day):
        change_asset_due_at_by_test_platform(self.item_no, advance_month, advance_day)
        asset_repay_success_asset_change_to_biz_by_api(self.item_no, "asset_change_refresh_fee")
        asset_repay_success_asset_change_to_biz_by_api(self.item_num_no_loan, "asset_change_refresh_fee")
        # environment = gc.ENVIRONMENT
        # asset_import = AssetImportFactory.get_import_obj(gc.ENV, "china", environment)
        # asset_import.change_asset(
        #     advance_month,
        #     self.item_no,
        #     self.item_num_no_loan,
        #     advance_day=advance_day,
        #     compensate_time=compensate_time
        # )

    def repay_apply_success(self, asset_tran_amount, asset_tran_amount_no_loan, code=0):
        params_combo_active = {
            "project_num_loan_channel_amount": int(asset_tran_amount["asset_tran_balance_amount"]),
            "project_num_no_loan_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        check_json_rs_data(resp_combo_active['content'], code=code)
        return resp_combo_active['content']

    def rbiz_autorepay_success(self, country="china", env="3", item_no="", status=2):
        url = "http://k8s-framework-test.k8s-ingress-nginx.kuainiujinke.com/rbiz-auto-repay"
        request_body = {
            "country": country,
            "env": env,
            "item_no": item_no,
            "status": status
        }
        return request_body, Http.http_post(url, request_body)

    def add_a_card(self):
        # 卡号和电话号码都更新
        new_four_element = get_four_element()
        id_num = self.four_element['data']["id_number_encrypt"]
        user_name = self.four_element['data']["user_name_encrypt"]
        card_num = new_four_element['data']['bank_code_encrypt']
        tel = new_four_element['data']["phone_number_encrypt"]
        sync_withhold_card(id_num, user_name, card_num, tel, "banana")
        # 卡号不一样，则新增卡
        check_card_by_item_no(self.item_no, card_acc_num_encrypt=self.four_element['data']["bank_code_encrypt"],
                              card_acc_id_num_encrypt=self.four_element['data']["id_number_encrypt"],
                              card_acc_tel_encrypt=self.four_element['data']["phone_number_encrypt"])
        check_individual_by_item_no(self.item_no,
                                    individual_name_encrypt=self.four_element['data']["user_name_encrypt"],
                                    individual_id_num_encrypt=self.four_element['data']["id_number_encrypt"],
                                    individual_tel_encrypt=self.four_element['data']["phone_number_encrypt"])
        return card_num, tel

    def get_auto_withhold_execute_task_run(self, item_no, run_withhold_count=1):
        task_auto_v1_message = json.loads(
            get_task_by_order_no_and_task_type(item_no, 'auto_withhold_execute')[0]['task_response_data'])['message']
        request_no_list = string_split(string_truncation(task_auto_v1_message)[0], ',')
        request_no_list.sort(reverse=True)
        print('request_no_list', request_no_list)
        for request_no in request_no_list:
            for i in range(0, run_withhold_count):
                print("i:", i)
                self.task.run_task(request_no, 'execute_combine_withhold')
        return request_no_list

    def refresh_late_fee(self, item_no):
        refresh_late_fee(item_no)
        self.task.run_task_by_order_no(item_no)
        self.msg.run_msg_by_id_and_search_by_order_no(item_no)
        asset_repay_success_asset_change_to_biz_by_api(item_no, "asset_change_refresh_fee")

    # 大小单都代扣成功之后的task执行
    @allure.step("step  执行rbiz的task")
    def run_all_task_after_repay_success(self, withhold=None):
        if withhold is None:
            withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        # 先执行一次execute_combine_withhold task
        self.task.run_task_by_order_no(withhold[0]['withhold_request_no'])
        order_no_list = [withhold_item["withhold_request_no"] for withhold_item in withhold] + \
                        [withhold_item["withhold_serial_no"] for withhold_item in withhold] + \
                        [withhold_item["withhold_request_no"] for withhold_item in withhold_no_loan] + \
                        [withhold_item["withhold_serial_no"] for withhold_item in withhold_no_loan]
        order_no_list = list(dict.fromkeys(order_no_list)) + [self.item_no, self.item_num_no_loan,
                                                              self.four_element['data']["id_number_encrypt"]]
        print(order_no_list)
        for i in range(5):
            for order_no in order_no_list:
                self.task.run_task_by_order_no(order_no)
                self.task.run_task_by_order_no(self.item_no)
                self.task.run_task_by_order_no(self.item_num_no_loan)
                self.task.wait_task_stable(task_order_no=order_no)
                self.msg.run_msg_by_id_and_search_by_order_no(order_no)
        self.task.check_task_stable(order_no_list)
        self.run_all_msg_after_repay_success()
        return withhold, withhold_no_loan

    # 大小单都代扣成功之后的消息发送
    @allure.step("step  执行rbiz的msg")
    def run_all_msg_after_repay_success(self):
        asset_recharge_success_account_to_biz_by_api(self.four_element['data']["id_number_encrypt"])
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        if withhold:
            for withhold_item in withhold:
                asset_withhold_success_to_biz_by_api(withhold_item["withhold_serial_no"])
                run_task_in_biz_central(withhold_item["withhold_serial_no"])
        if withhold_no_loan:
            for withhold_item in withhold_no_loan:
                asset_withhold_success_to_biz_by_api(withhold_item["withhold_serial_no"])
                run_task_in_biz_central(withhold_item["withhold_serial_no"])
        asset_repay_success_account_to_biz_by_api(self.four_element['data']["id_number_encrypt"])
        asset_repay_success_asset_change_to_biz_by_api(self.item_no)
        asset_repay_success_asset_change_to_biz_by_api(self.item_num_no_loan)


    def check_response_after_apply_success(self, repay_resp, withhold, withhold_no_loan):
        check_json_rs_data(repay_resp, code=0, message='交易处理中')
        check_json_rs_data(repay_resp['data'], type="BIND_SMS")
        check_json_rs_data(repay_resp['data']['project_list'][0], status=2, memo='处理中',
                           project_num=self.item_num_no_loan, order_no=withhold_no_loan[0]['withhold_serial_no'])
        check_json_rs_data(repay_resp['data']['project_list'][1], status=2, memo='处理中',
                           project_num=self.item_no, order_no=withhold[0]['withhold_serial_no'])

    # 发起仅还1单
    def repay_only_one_project_success(self, repay_amount, item_no, code=0):
        params_repay = {
            "project_num_loan_channel_amount": repay_amount,
            "project_num_loan_channel": item_no,
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"]
        }
        resp_repay_loan, req_body = combo_active_repay_without_no_loan(**params_repay)
        check_json_rs_data(resp_repay_loan['content'], code=code)
        return resp_repay_loan['content']

    def run_task_after_loan_repay(self, item_no):
        self.task.run_task_by_order_no_count(item_no, count=3)
        withhold = get_withhold_by_item_no(item_no)
        order_no_list = [withhold_item["withhold_request_no"] for withhold_item in withhold] + \
                        [withhold_item["withhold_serial_no"] for withhold_item in withhold]
        order_no_list = list(dict.fromkeys(order_no_list)) + [self.item_no]
        print(order_no_list)
        for i in range(5):
            for order_no in order_no_list:
                self.task.run_task_by_order_no_count(order_no, count=3)
                self.task.wait_task_stable(task_order_no=order_no)
                self.task.run_task_by_order_no(item_no)
        asset_recharge_success_account_to_biz_by_api(self.four_element['data']["id_number_encrypt"])
        asset_repay_success_account_to_biz_by_api(self.four_element['data']["id_number_encrypt"])
        asset_repay_success_asset_change_to_biz_by_api(item_no)
        for withhold_item in withhold:
            asset_withhold_success_to_biz_by_api(withhold_item["withhold_serial_no"])
        self.task.check_task_stable(order_no_list)

    def run_account_msg_after_repaid(self):
        asset_recharge_success_account_to_biz_by_api(self.four_element['data']["id_number_encrypt"])
        asset_repay_success_account_to_biz_by_api(self.four_element['data']["id_number_encrypt"])
        asset_repay_success_asset_change_to_biz_by_api(self.item_no)
        asset_repay_success_asset_change_to_biz_by_api(self.item_num_no_loan)
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)
        for withhold_item in withhold:
            asset_withhold_success_to_biz_by_api(withhold_item["withhold_serial_no"])
        for withhold_item in withhold_no_loan:
            asset_withhold_success_to_biz_by_api(withhold_item["withhold_serial_no"])

    def run_task_after_withhold_callback(self, order_no_list=[]):
        self.task.run_task_by_order_no_count(self.item_no, count=3)
        self.task.run_task_by_order_no(self.item_num_no_loan)
        # 除了资产编号，还想运行什么task
        if order_no_list:
            for order_no in order_no_list:
                self.task.run_task_by_order_no(order_no)
                self.task.run_task_by_order_no(self.item_no)
                self.task.run_task_by_order_no(self.item_num_no_loan)
                self.msg.run_msg_by_id_and_search_by_order_no(order_no)
