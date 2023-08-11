# -*- coding: utf-8 -*-
import time

import requests
from dateutil.relativedelta import relativedelta

from biztest.function.biz.biz_check_class import BizCheckBase
# from biztest.function.rbiz.CreateData import AssetImportFactory
from biztest.function.rbiz.rbiz_db_function import get_withhold_by_item_no, \
    get_asset_tran_balance_amount_by_item_no_and_period, update_before_asset_tran_finish_by_item_no_and_period
from biztest.interface.rbiz.biz_central_interface_class import BizInterfaceBase
from biztest.interface.rbiz.rbiz_interface import simple_active_repay
from biztest.util.tools.tools import get_calc_date, get_date
from biztest.util.xxl_job.xxl_job_new import XxlJobNew
import datetime
import math
import allure
import common.global_const as gc


class BizCentralPushBase(BizInterfaceBase, BizCheckBase):
    xxl_job = XxlJobNew('xxl_job_k8s')
    country = 'china'
    # central_job = JOB_GROUP_CENTRAL_DICT[gc.ENV]
    # repay_job = JOB_GROUP_REPAY_DICT[gc.ENV]
    # asset_import = AssetImportFactory.get_import_obj(gc.ENV, 'china', db_env=gc.ENVIRONMENT)
    # nacos = gc.NACOS
    # check_settlement_except_cols = ['capital_transaction_expect_operate_at',
    #                                 'capital_transaction_actual_operate_at',
    #                                 'capital_transaction_status',
    #                                 'capital_transaction_operation_type',
    #                                 'capital_transaction_type',
    #                                 'capital_transaction_period',
    #                                 'capital_transaction_repaid_amount']
    # check_user_repay_except_cols = ['capital_transaction_user_repay_at',
    #                                 'capital_transaction_withhold_result_channel']
    # check_settlement_fee_type = ['principal', 'interest']
    # item_no, item_num_no_loan, count, period = None, None, 12, 1
    # # item_no 大单资产编号
    # # item_num_no_loan 小单资产编号
    # # count 期数
    # # period 当期期次
    # pd_recharge_list = []
    # # 当期执行的还款的list
    # tenant = "biz-central{0}".format(gc.ENV)
    # begin_time = get_date()

    def wait_central_task_appear(self, task_order_no, task_type, is_one=False, timeout=60):
        return self.db.wait_central_task_appear(task_order_no, task_type, self.begin_time, is_one=is_one,
                                                timeout=timeout)

    @staticmethod
    def get_calc_date(base_time, year=0, month=0, day=0, fmt="%Y-%m-%d %H:%M:%S", is_str=True):
        """
        :param base_time: 正数 往后推1年，负数往前推1年
        :param year: 正数 往后推1年，负数往前推1年
        :param month: 正数 往后推1月，负数往前推1月
        :param day: 正数 往后推1天，负数往前推1天
        :param fmt: 时间格式化
        :param is_str: 是否返回字符串
        :return:
        """
        ret = base_time + relativedelta(years=year, months=month, days=day)
        return ret.strftime(fmt) if is_str else ret

    @classmethod
    def add_work_days(cls, date, days):
        if isinstance(date, datetime.date):
            raise TypeError('need date type')
        if days == 0:
            return date
        direct = days / math.abs(days)
        days = math.abs(days)
        while days:
            date = get_calc_date(date, days=direct, fmt='%Y-%m-%d 00:00:00')
            if cls.is_work_day(date):
                days -= 1
        return date

    def is_work_day(self, date):
        holiday = self.get_holiday(date)
        if holiday:
            return holiday[0]
        return self.is_week_day(date)

    @staticmethod
    def is_week_day(date):
        if date.isoweekday() in (6, 7):
            return True
        return False

    def __set_date_holiday(self, date, is_holiday):
        holiday = self.db.get_holiday(date)
        if holiday:
            self.db.update_holiday(date, is_holiday)
        else:
            self.db.set_holiday(date, is_holiday)
        self.refresh_holiday_info()

    def set_holiday(self, date, holiday):
        self.__set_date_holiday(date, holiday)

    def set_date_holiday(self, date):
        self.__set_date_holiday(date, 1)

    def set_date_not_holiday(self, date):
        self.__set_date_holiday(date, 0)

    def refresh_holiday_info(self):
        url = self.central_base_url + '/job/refreshholiday'
        req = requests.get(url)
        if req.status_code == 200 and req.json()['code'] == 0:
            print('refresh holiday info success!')
        else:
            print('refresh holiday info failed!')

    def set_compensate_before(self, lanzhou_config):
        """
        设置代偿时间为当前时间之前
        default_time:默认代偿时间16：00：00
        :return: 返回资方推送的计划时间
        """
        # 配置代偿推送时间
        default_time = '16:00:00'
        default_plan_at = "{0} {1}".format(self.current_date, default_time)
        if datetime.datetime.now() < datetime.datetime.strptime(default_plan_at, "%Y-%m-%d %H:%M:%S"):
            new_compensate_time = "{0}:00:00".format(datetime.datetime.now().hour)
            lanzhou_config['push_time']['push_compensate_time'] = new_compensate_time
            capital_notify_plan_at = "{0} {1}".format(self.current_date, new_compensate_time)
            self.set_lanzhou_config(lanzhou_config)
        elif datetime.datetime.now() >= datetime.datetime.strptime(default_plan_at, "%Y-%m-%d %H:%M:%S"):
            lanzhou_config['push_time']['push_compensate_time'] = default_time
            capital_notify_plan_at = default_plan_at
            self.set_lanzhou_config(lanzhou_config)
        return capital_notify_plan_at

    @allure.step(f"执行捞取资方代偿的xxl_job..")
    def run_capital_compensate_xxl_job(self, loan_channel):
        """
        执行捞取资方代偿的xxl_job
        :return:
        """
        executor_param = {
            "loan_channels": [loan_channel]
        }
        self.xxl_job.trigger_job(self.central_job, 'StoreCompensateNotifyJob', executor_param=executor_param)

    @allure.step(f"执行捞取资方推送的xxl_job..")
    def run_capital_push_xxl_job(self):
        """
        执行捞取资方推送的xxl_job
        :return:
        """
        self.xxl_job.trigger_job(self.central_job, 'CapitalNotifyProcessJob')

    @allure.step(f"执行代偿-只推清结算的xxl_job..")
    def run_dcs_compensate_xxl_job(self, loan_channel, grace_day=0):
        """
        执行代偿-只推清结算的xxl_job
        涉及资方：中科-兰州, 哈密天山, 哈密天邦
        :return:
        """
        executor_param = {
            "loan_channel_config_list": [
                {
                    "loan_channel": loan_channel,
                    "grace_day": grace_day
                }
            ],
            "date": None
        }
        self.xxl_job.trigger_job(self.central_job, 'CompensateSettlementNotifyJob', executor_param=executor_param)

    @allure.step(f"执行中科-兰州的还款和代偿文件的xxl_job..")
    def run_lanzhou_file_xxl_job(self, is_compensate):
        """
        执行处理兰州正常、代偿的文件信息任务的xxl job
        代偿:"COMPFILE",
        正常还款:"REPAYMENTFILE"
        :return:
        """
        executor_param = {
            "remote_base_path": "/upload/11001",
            "date": None,
            "process_files": ["COMPFILE" if is_compensate else "REPAYMENTFILE"]
        }
        self.xxl_job.trigger_job(self.central_job, 'LanzhouCallbackFileProcessJob', executor_param=executor_param)

    def wait_all_user_at_receive(self, withhold, withhold_no_loan, timeout=60):
        withhold_count = len(withhold) + len(withhold_no_loan)
        user_count = 0
        timeout_begin = 0
        while withhold_count != user_count:
            user_count = self.db.get_user_at_count(self.item_no)
            time.sleep(1)
            if timeout_begin > timeout:
                raise ValueError("user repay not sync with asset is :'{0}', '{1}'!".format(self.item_no,
                                                                                           self.item_num_no_loan))
            timeout_begin += 1

    def repay_success(self, asset_tran_amount, asset_tran_amount_no_loan):
        params_combo_active = {
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        resp_combo_active, req_body = simple_active_repay(self.item_no, **params_combo_active)
        assert resp_combo_active['content'][
                   'code'] == 0, f"提前还款失败,req_body={req_body},resp_combo_active={resp_combo_active}"
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        return withhold, withhold_no_loan

    def wait_and_run_central_task(self, task_order_no, task_type, is_one=True, timeout=3, excepts={"code": 0}):
        task_list = self.wait_central_task_appear(task_order_no, task_type=task_type, is_one=is_one, timeout=timeout)
        if task_list:
            self.run_task_in_biz_central_by_task_id(task_list[0]['task_id'], excepts=excepts)
            return task_list[0]['task_id']

    def repay_advance_fixed_period(self, period):
        self.period = period
        self.db.update_before_capital_tran_finish_by_item_no_and_period(self.item_no, period)
        update_before_asset_tran_finish_by_item_no_and_period(self.item_no, period)
        update_before_asset_tran_finish_by_item_no_and_period(self.item_num_no_loan, period)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, period)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, period)
        return self.repay_success(asset_tran_amount, asset_tran_amount_no_loan)

    def get_suspend_task_config(self):
        return self.nacos.get_config(self.tenant, 'suspend_task_config')

    def update_suspend_task_config(self, values):
        self.nacos.update_configs(self.tenant, 'suspend_task_config', values)

    def get_account_import_config(self):
        return self.nacos.get_config(self.tenant, 'account_import_config')

    def update_account_import_config(self, values):
        self.nacos.update_configs(self.tenant, 'account_import_config', values)

    def get_biz_central_system_config(self):
        return self.nacos.get_config(self.tenant, 'biz-central-{0}.properties'.format(gc.ENV), group='SYSTEM')

    def update_biz_central_system_config(self, values):
        self.nacos.update_configs(self.tenant, 'biz-central-{0}.properties'.format(gc.ENV), values, group='SYSTEM')
        raise ValueError("need reload services")

    @allure.step(f"执行rbiz所有task..")
    def run_all_task_after_repay_success(self):
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
        return withhold, withhold_no_loan

    @allure.step(f"通过Api执行资方推送的job..")
    def run_capital_push_by_api(self):
        """
        通过api执行捞取资方推送的job
        :return:
        """
        job_type = "capitalNotifyPushJob"
        job_params = {
            "date_before_minutes": 1440
        }
        self.run_job_by_api(job_type, job_params)

    @allure.step(f"通过Api执行代偿的job..")
    def run_generate_compensate_by_api(self):
        """
        通过api执行捞取资方推送的job
        :return:
        """
        job_type = "generateCompensateJob"
        job_params = {
            "channel": "",
            "startDate": "",
            "endDate": ""
        }
        self.run_job_by_api(job_type, job_params)
