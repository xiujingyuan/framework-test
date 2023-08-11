#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import datetime

import allure

from biztest.config.easymock.easymock_config import global_rbiz_mock
from biztest.config.global_rbiz.global_rbiz_kv_config import update_rbiz_config_withhold, \
    update_tha_rbiz_paysvr_config, update_rbiz_decrease_config, update_rbiz_refresh_fee_conf, update_rbiz_config, \
    update_account_statement_sync, update_rbiz_capital_withhold_rule
from biztest.function.global_rbiz.rbiz_global_db_function import update_asset_and_asset_tran_due_at_by_item_no, \
    get_withhold_by_item_no, get_asset_extend, \
    get_withhold_order_by_item_no, get_withhold_order_by_serial_no, get_withhold_by_serial_no, get_asset, \
    update_withhold, get_asset_delay, delete_asset_late_fee_refresh_log, get_asset_tran, update_asset_to_payoff_by_date
from biztest.interface.rbiz.rbiz_global_interface import combo_active_repay_with_no_loan, refresh_late_fee, \
    paysvr_callback, combo_active_repay, fox_withhold, paysvr_trade_callback, paysvr_smart_collect_callback, \
    run_withholdTimeout_by_api, transaction_confirm, run_accountStatementSync_by_api, \
    run_initStatusAccountStatementMatchWithholdRecord_by_api
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.payment_global import PaymentGlobalMock
from biztest.util.msgsender.msgsender import Msgsender
from biztest.util.task.task import TaskGlobalRepay
import common.global_const as gc
from biztest.util.tools.tools import get_date, get_tz, get_date_by_old_date


class BaseGlobalRepayTest(object):
    from_app = "mango"
    from_system = "tha"
    loan_channel = "pico_bangkok"
    source_type = "test_bill"
    principal_amount = 500000
    principal_no_loan_amount = 50000

    def init(self):
        self.task = TaskGlobalRepay()
        self.msgsender = Msgsender("rbiz")
        self.item_no = self.item_no_x = ""
        self.mock = PaymentGlobalMock(global_rbiz_mock)

    def setup_class(self):
        self.task = TaskGlobalRepay()
        self.msgsender = Msgsender("rbiz")
        self.item_no = self.item_no_x = ""
        self.mock = PaymentGlobalMock(global_rbiz_mock)
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e")
        update_asset_to_payoff_by_date()
        update_rbiz_refresh_fee_conf()
        update_rbiz_decrease_config()
        update_rbiz_config()
        update_rbiz_capital_withhold_rule()
        update_account_statement_sync()
        self.mock.update_withhold_autopay_ebank_url_success()

    def teardown_class(self):
        update_tha_rbiz_paysvr_config()
        DataBase.close_connects()

    def update_asset_due_at(self, advance_day, advance_month=0, period=1, refresh=False):
        params_due_at = {
            "advance_month": advance_month,
            "advance_day": advance_day,
            "period": period,
            "item_no": self.item_no
        }
        update_asset_and_asset_tran_due_at_by_item_no(**params_due_at)
        if refresh:
            # self.close_all_withhold(self.item_no)
            self.refresh_late_fee(self.item_no)

    def close_all_withhold(self, item_no):
        update_rbiz_config_withhold()
        withhold_list = get_withhold_by_item_no(item_no)
        for withhold in withhold_list:
            if withhold["withhold_status"] not in ("success", "fail"):
                order_no = withhold["withhold_serial_no"]
                update_withhold(order_no, withhold_create_at=get_date(day=-1, hour=-2, timezone=get_tz(gc.COUNTRY)))
                run_withholdTimeout_by_api()
                self.task.wait_task_appear(order_no, "withhold_timeout")
                self.task.run_task(order_no, "withhold_timeout", {"code": 0, "message": "将订单设置为失败成功！"})

    def refresh_late_fee(self, item_no):
        delete_asset_late_fee_refresh_log(asset_late_fee_refresh_log_asset_item_no=item_no)
        refresh_late_fee(item_no)
        self.task.run_task(item_no, "AssetAccountChangeNotify")
        self.msgsender.run_msg_by_order_no_list([item_no, ])
        extend_list = get_asset_extend(asset_extend_asset_item_no=item_no, asset_extend_type="ref_order_no")
        if extend_list is not None and len(extend_list) > 0:
            item_no_x = extend_list[0]["asset_extend_val"]
            if get_asset(asset_item_no=item_no_x) is not None and len(get_asset(asset_item_no=item_no_x)) > 0:
                refresh_late_fee(item_no_x)
                self.task.run_task(item_no_x, "AssetAccountChangeNotify")
                self.msgsender.run_msg_by_order_no_list([item_no_x, ])
        sql = "update asset_tran_log " \
              "set asset_tran_log_create_at=DATE_FORMAT(asset_tran_log_create_at, '%Y-%m-%d 01:00:00') " \
              "where asset_tran_log_asset_item_no in ('{0}', '{0}_noloan') and " \
              "asset_tran_log_operate_type='refresh_fee'".format(item_no)
        gc.REPAY_DB.update(sql)

    def combo_active_repay_apply(self, asset_tran_amount, asset_tran_amount_no_loan, payment_type='qrcode',
                                 coupon_amount=0, coupon_num=None, period_list=None, repay_type=None):
        if asset_tran_amount == 0 or asset_tran_amount_no_loan == 0:
            asset_tran_amount = self.get_asset_trial_amount(self.item_no, period_list, repay_type)
            asset_tran_amount_no_loan = self.get_asset_trial_amount(self.item_no_x, period_list, repay_type)
        params_combo_active = {
            "card_uuid": self.four_element['data']['card_num'],
            "id_num": self.four_element['data']["id_number_encrypt"],
            "user_id": self.four_element['data']['id_number'],
            "mobile": self.four_element['data']['mobile_encrypt'],
            "payment_type": payment_type,
            "project_num_loan_channel": self.item_no,
            "project_num_no_loan": self.item_no_x,
            "project_num_loan_channel_amount": asset_tran_amount,
            "project_num_no_loan_amount": asset_tran_amount_no_loan,
            "coupon_amount": None if coupon_amount == 0 else coupon_amount,
            "coupon_num": None if coupon_amount == 0 else coupon_num,
            "repay_type": repay_type
        }
        resp_combo_active, req_body = combo_active_repay_with_no_loan(**params_combo_active)
        return resp_combo_active

    def loan_active_repay_apply(self, asset_tran_amount, payment_type='paycode', payment_option='store',
                                coupon_amount=0, coupon_num=None, period_list=None, repay_type=None):
        params_combo_active = {
            "card_uuid": self.four_element['data']['card_num'],
            "id_num": self.four_element['data']["id_number_encrypt"],
            "user_id": self.four_element['data']['id_number'],
            "mobile": self.four_element['data']['mobile_encrypt'],
            "payment_type": payment_type,
            "payment_option": payment_option,
            "project_num_loan_channel": self.item_no,
            "project_num_loan_channel_amount": asset_tran_amount if asset_tran_amount != 0 else
            self.get_asset_trial_amount(self.item_no, period_list, repay_type),
            "coupon_amount": None if coupon_amount == 0 else coupon_amount,
            "coupon_num": None if coupon_amount == 0 else coupon_num,
            "repay_type": repay_type
        }
        resp_combo_active, req_body = combo_active_repay(**params_combo_active)
        return resp_combo_active

    def get_asset_trial_amount(self, item_no, period_list, repay_type):
        asset_info = get_asset(asset_item_no=self.item_no)[0]
        asset_tran_list = get_asset_tran(asset_tran_asset_item_no=item_no)
        asset_tran_amount = 0
        for asset_tran in asset_tran_list:
            if int(asset_tran["asset_tran_period"]) in period_list:
                if asset_tran["asset_tran_type"] == "fin_service" and repay_type in ("advance", "advance_settle"):
                    asset_tran_amount += self.get_fin_service_trial_amount(asset_info, asset_tran, repay_type)
                else:
                    asset_tran_amount += asset_tran["asset_tran_balance_amount"]
        return asset_tran_amount

    def get_fin_service_trial_amount(self, asset_info, asset_tran, repay_type):
        product_category = int(asset_info["asset_product_category"])
        grant_day = get_date_by_old_date(asset_info["asset_actual_grant_at"], "%Y-%m-%d %H:%M:%S", fmt="%Y-%m-%d")
        up_period_due_at = get_date_by_old_date(asset_tran["asset_tran_due_at"], "%Y-%m-%d %H:%M:%S",
                                                day=-product_category, fmt="%Y-%m-%d")
        day_count = (datetime.now() - datetime.strptime(max(grant_day, up_period_due_at), "%Y-%m-%d")).days
        total_fee_amount = asset_tran["asset_tran_total_amount"]
        # 本期未开始
        trial_amount = 0
        if day_count < 0:
            if repay_type == "advance":
                temp_amount = total_fee_amount * (0 + 1) / product_category
                trial_amount = temp_amount \
                    if temp_amount < asset_tran["asset_tran_balance_amount"] else asset_tran["asset_tran_balance_amount"]
            if repay_type == "advance_settle":
                trial_amount = 0
        # 本期进行中
        elif 0 <= day_count <= product_category:
            temp_amount = total_fee_amount * (day_count + 1) / product_category
            trial_amount = temp_amount \
                if temp_amount < asset_tran["asset_tran_balance_amount"] else asset_tran["asset_tran_balance_amount"]
        # 逾期
        else:
            trial_amount = asset_tran["asset_tran_balance_amount"]
        return round(trial_amount)

    def loan_fox_repay_apply(self, asset_tran_amount, four_element, payment_type='paycode'):
        params_fox = {
            "payment_type": payment_type,
            "item_no": self.item_no,
            "amount": asset_tran_amount,
            "four_element": four_element
        }
        resp_fox, req_body = fox_withhold(**params_fox)
        assert resp_fox['content'][
                   'code'] == 0, f"fox代扣失败,resp_combo_active={resp_fox},req_body={req_body}"
        return resp_fox

    def prepare_repeated_withhold(self, asset_tran_amount, asset_tran_amount_no_loan):
        """
        准备重复代扣的数据，2笔金额一样
        """
        withhold_amount = int(asset_tran_amount) + int(asset_tran_amount_no_loan)

        resp_combo_active = self.combo_active_repay_apply(asset_tran_amount, asset_tran_amount_no_loan)
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        # 回调失败 第1笔
        paysvr_callback(merchant_key, withhold_amount, 3)
        # 回调成功 第2笔
        resp_combo_active_new = self.combo_active_repay_apply(asset_tran_amount, asset_tran_amount_no_loan)
        merchant_key_new = resp_combo_active_new['content']["data"]["project_list"][0]["order_no"]
        paysvr_callback(merchant_key_new, withhold_amount, 2)
        self.run_all_task_after_repay_success()
        # 回调成功 第1笔
        paysvr_callback(merchant_key, withhold_amount, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        print(
            f"#####---准备重复代扣数据结束----资产编号：{self.item_no}，扣款流水1；{merchant_key_new}，扣款流水2：{merchant_key}------#####")
        return merchant_key, merchant_key_new, withhold_amount

    # 大小单都代扣成功之后的task执行
    @allure.step("step  执行rbiz的task")
    def run_all_task_after_repay_success(self, key_list=None):
        if key_list is None:
            key_list = []
        order_no_list = []
        withhold_order_list = get_withhold_order_by_item_no(self.item_no)
        for withhold_order in withhold_order_list:
            withhold_order_list_new = get_withhold_order_by_serial_no(withhold_order["withhold_order_serial_no"])
            order_no_list += [order["withhold_order_request_no"] for order in withhold_order_list_new] + \
                             [order["withhold_order_serial_no"] for order in withhold_order_list_new] + \
                             [order["withhold_order_reference_no"] for order in withhold_order_list_new]
        extend_list = get_asset_extend(asset_extend_asset_item_no=self.item_no, asset_extend_type="ref_order_no")
        if extend_list is not None and len(extend_list) > 0 and "asset_extend_val" in extend_list[0].keys():
            item_no_x = extend_list[0]["asset_extend_val"]
            withhold_order_list = get_withhold_order_by_item_no(item_no_x)
            for withhold_order in withhold_order_list:
                withhold_order_list_new = get_withhold_order_by_serial_no(withhold_order["withhold_order_serial_no"])
                order_no_list += [order["withhold_order_request_no"] for order in withhold_order_list_new] + \
                                 [order["withhold_order_serial_no"] for order in withhold_order_list_new] + \
                                 [order["withhold_order_reference_no"] for order in withhold_order_list_new]
        order_no_list = list(dict.fromkeys(order_no_list + key_list))
        print(order_no_list)
        for i in range(7):
            task_list = self.task.get_task_by_order_no_list(order_no_list)
            if task_list is None or len(task_list) == 0:
                break
            for task in task_list:
                self.task.run_task_by_id(task["task_id"])
        self.task.check_task_stable(order_no_list)

    # 大小单都代扣成功之后的消息发送
    @allure.step("step  执行rbiz的msg")
    def run_all_msg_after_repay_success(self, key_list=None):
        if key_list is None:
            key_list = []
        withhold = get_withhold_by_item_no(self.item_no)
        order_no_list = [withhold_item["withhold_serial_no"] for withhold_item in withhold] + \
                        [withhold_item["withhold_user_idnum"] for withhold_item in withhold]
        item_no_x = None
        asset_delay_list = get_asset_delay(asset_delay_item_no=self.item_no, asset_delay_status="success")
        if asset_delay_list is not None and len(asset_delay_list) > 0:
            order_no_list += [asset_delay["asset_delay_trade_no"] for asset_delay in asset_delay_list]
        extend_list = get_asset_extend(asset_extend_asset_item_no=self.item_no, asset_extend_type="ref_order_no")
        if extend_list is not None and len(extend_list) > 0 and "asset_extend_val" in extend_list[0].keys():
            item_no_x = extend_list[0]["asset_extend_val"]
            withhold_no_loan = get_withhold_by_item_no(item_no_x)
            order_no_list += [withhold_item["withhold_serial_no"] for withhold_item in withhold_no_loan]
        order_no_list = \
            list(dict.fromkeys(order_no_list + key_list + [self.item_no, ])) + \
            ([item_no_x, ] if item_no_x is not None else [])
        print(order_no_list)
        self.msgsender.run_msg_by_order_no_list(order_no_list)

    @allure.step("step  执行rbiz的task")
    def run_all_task_by_serial_no(self, serial_no):
        order_no_list = []
        withhold_order_list = get_withhold_order_by_serial_no(serial_no)
        for withhold_order in withhold_order_list:
            withhold_order_list_new = get_withhold_order_by_serial_no(withhold_order["withhold_order_serial_no"])
            order_no_list += [order["withhold_order_request_no"] for order in withhold_order_list_new] + \
                             [order["withhold_order_serial_no"] for order in withhold_order_list_new] + \
                             [order["withhold_order_reference_no"] for order in withhold_order_list_new]
        order_no_list = list(dict.fromkeys(order_no_list))
        print(order_no_list)
        for i in range(7):
            task_list = self.task.get_task_by_order_no_list(order_no_list)
            if task_list is None or len(task_list) == 0:
                break
            for task in task_list:
                self.task.run_task_by_id(task["task_id"])
        self.task.check_task_stable(order_no_list)

    def repay_asset(self, repay_params):
        repay_type = repay_params.get("repay_type", "asset")
        payment_type = repay_params.get("payment_type", "normal")
        if payment_type == "card":
            self.repay_card(repay_params)
        elif repay_type == "void" and payment_type == "normal":
            self.repay_void(repay_params)
        elif repay_type == "asset" and payment_type == "normal":
            self.repay_normal(repay_params)
        elif repay_type == "delay" and payment_type == "normal":
            self.repay_trade(repay_params)
        elif repay_type in ["asset", "delay", "void"] and (payment_type == "collect" or payment_type == "spi"):
            self.repay_collect(repay_params)
        else:
            raise Exception("repay_type:%s, payment_type:%s 错误")

    def repay_normal(self, repay_params):
        item_no = repay_params.get("item_no", "")
        amount = repay_params.get("amount", 0)
        status = repay_params.get("status", 3)
        finish_at = repay_params.get("finish_at", get_date(timezone=get_tz(gc.COUNTRY)))
        order_list = gc.REPAY_DB.do_sql("select * from withhold_order "
                                        "inner join withhold on withhold_serial_no=withhold_order_serial_no "
                                        "inner join withhold_request on withhold_order_req_key=withhold_request_req_key "
                                        "where withhold_status != 'success' and "
                                        "withhold_request_trade_type='COMBINE_WITHHOLD' and "
                                        "withhold_order_reference_no='%s' and "
                                        "withhold_order_withhold_sub_status in ('normal','advance','advance_settle') and "
                                        "withhold_payment_type != 'collect' order by withhold_order_id" % item_no)
        if order_list is None or len(order_list) == 0:
            raise Exception("未找到正常还款请求")
        order = order_list[-1]
        withhold_list = get_withhold_by_serial_no(order["withhold_order_serial_no"])
        callback_amount = withhold_list[-1]["withhold_amount"] if amount == 0 else amount
        paysvr_callback(order["withhold_order_serial_no"], callback_amount, int(status), finished_at=finish_at)
        self.task.run_task(order["withhold_order_serial_no"], "processWithholdEnd", {"code": 0})
        self.run_all_task_by_serial_no(order["withhold_order_serial_no"])
        self.run_all_msg_after_repay_success()
        return order["withhold_order_serial_no"]

    def repay_void(self, repay_params):
        item_no = repay_params.get("item_no", "")
        amount = repay_params.get("amount", 0)
        status = repay_params.get("status", 3)
        finish_at = repay_params.get("finish_at", get_date(timezone=get_tz(gc.COUNTRY)))
        order_list = gc.REPAY_DB.do_sql("select * from withhold_order "
                                        "inner join withhold on withhold_serial_no=withhold_order_serial_no "
                                        "inner join withhold_request on withhold_order_req_key=withhold_request_req_key "
                                        "where withhold_status != 'success' and "
                                        "withhold_request_trade_type='ASSET_VOID_WITHHOLD' and "
                                        "withhold_order_reference_no='%s' and "
                                        "withhold_order_withhold_sub_status='normal' and "
                                        "withhold_payment_type != 'collect' order by withhold_order_id" % item_no)
        if order_list is None or len(order_list) == 0:
            raise Exception("未找到资产取消请求")
        order = order_list[-1]
        withhold_list = get_withhold_by_serial_no(order["withhold_order_serial_no"])
        callback_amount = withhold_list[-1]["withhold_amount"] if amount == 0 else amount
        paysvr_callback(order["withhold_order_serial_no"], callback_amount, int(status), finished_at=finish_at)
        self.task.run_task(order["withhold_order_serial_no"], "processWithholdEnd", {"code": 0})
        self.run_all_task_by_serial_no(order["withhold_order_serial_no"])
        self.run_all_msg_after_repay_success()
        extend_list = get_asset_extend(asset_extend_asset_item_no=self.item_no, asset_extend_type="ref_order_no")
        if extend_list is not None and len(extend_list) > 0 and "asset_extend_val" in extend_list[0].keys():
            item_no_x = extend_list[0]["asset_extend_val"]
            task = self.task.get_task(task_order_no=item_no_x, task_type="noLoanAssetVoid")
            if task is not None and len(task) > 0:
                self.task.run_task(item_no_x, "noLoanAssetVoid", {"code": 0, "message": "作废小单成功"})
                self.task.run_task(item_no_x, "AssetAccountChangeNotify")
        return order["withhold_order_serial_no"]

    def repay_trade(self, repay_params):
        item_no = repay_params.get("item_no", "")
        amount = repay_params.get("amount", 0)
        status = repay_params.get("status", 3)
        finish_at = repay_params.get("finish_at", get_date(timezone=get_tz(gc.COUNTRY)))
        order_list = gc.REPAY_DB.do_sql("select * from withhold_order "
                                        "inner join withhold on withhold_serial_no=withhold_order_serial_no "
                                        "where withhold_status != 'success' and "
                                        "withhold_order_reference_no='%s' and "
                                        "withhold_order_withhold_sub_status='asset_delay' and "
                                        "withhold_payment_type != 'collect' order by withhold_order_id" % item_no)
        if order_list is None or len(order_list) == 0:
            raise Exception("未找到展期订单")
        order = order_list[-1]
        withhold_list = get_withhold_by_serial_no(order["withhold_order_serial_no"])
        callback_amount = withhold_list[-1]["withhold_amount"] if amount == 0 else amount
        paysvr_trade_callback(order["withhold_order_serial_no"], callback_amount, int(status), finished_at=finish_at)
        self.task.run_task(order["withhold_order_serial_no"], "processWithholdEnd", {"code": 0})
        self.run_all_task_by_serial_no(order["withhold_order_serial_no"])
        self.run_all_msg_after_repay_success()
        return order["withhold_order_serial_no"]

    def repay_collect(self, repay_params):
        item_no = repay_params.get("item_no", "")
        amount = repay_params.get("amount", 0)
        repay_type = repay_params.get("repay_type", "asset")
        finish_at = repay_params.get("finish_at", get_date(timezone=get_tz(gc.COUNTRY)))
        if repay_type == "asset":
            account = item_no
        elif repay_type == "delay":
            account = "assetDelay" + item_no
        elif repay_type == "void":
            account = "assetVoid" + item_no
        else:
            account = None
        if repay_type == "delay":
            order_list = gc.REPAY_DB.do_sql("select * from withhold_order "
                                            "inner join withhold on withhold_serial_no=withhold_order_serial_no "
                                            "where withhold_order_reference_no='%s' and "
                                            "withhold_order_withhold_sub_status='asset_delay' and "
                                            "withhold_third_serial_no='%s' and "
                                            "withhold_payment_type='collect' order by withhold_order_id" %
                                            (item_no, account))
            if order_list is None or len(order_list) == 0:
                raise Exception("未找到展期线下还款订单")
        resp, req = paysvr_smart_collect_callback(account, amount, finished_at=finish_at)
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0})
        task = gc.REPAY_DB.do_sql("select * from task where task_create_at>DATE_ADD(now(), INTERVAL -30 MINUTE) "
                                  "and task_type='withhold_callback_process' and task_request_data like '%%%s%%'" %
                                  channel_key)[0]
        self.run_all_task_by_serial_no(task["task_order_no"])
        self.run_all_msg_after_repay_success()
        return task["task_order_no"]

    def repay_card(self, repay_params):
        item_no = repay_params.get("item_no", "")
        amount = repay_params.get("amount", 0)
        finish_at = repay_params.get("finish_at", get_date(timezone=get_tz(gc.COUNTRY)))

        order_list = gc.REPAY_DB.do_sql("select * from withhold_order "
                                        "inner join withhold on withhold_serial_no=withhold_order_serial_no "
                                        "where withhold_status != 'success' and "
                                        "withhold_order_reference_no='%s' and "
                                        "withhold_third_serial_no not like '%%%s%%' and "
                                        "withhold_third_serial_no != '' and "
                                        "withhold_payment_type != 'collect' order by withhold_order_id" %
                                        (item_no, item_no))
        if order_list is None or len(order_list) == 0:
            raise Exception("未找到卡对卡还款订单")
        order = order_list[-1]
        withhold_list = get_withhold_by_serial_no(order["withhold_order_serial_no"])
        callback_amount = withhold_list[-1]["withhold_amount"] if amount == 0 else amount
        mock_data = self.mock.update_query_channel_reconci_data(1, amount=callback_amount, finish_at=finish_at)
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(order["withhold_order_serial_no"], transaction_no)

        run_accountStatementSync_by_api()
        self.task.run_task(get_date(day=-1, fmt="%Y-%m-%d"), "paysvr_pull_billing_data", {"code": 0, "message": "同步成功"})
        run_initStatusAccountStatementMatchWithholdRecord_by_api()
        self.task.run_task(transaction_no, "account_statement_record_match", {"code": 0, "message": ".*匹配成功.*"})
        self.run_all_task_by_serial_no(order["withhold_order_serial_no"])
