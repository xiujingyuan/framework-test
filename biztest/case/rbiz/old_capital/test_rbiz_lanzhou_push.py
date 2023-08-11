# -*- coding: utf-8 -*-
import json

import pandas as pd
import allure

from biztest.case.rbiz.rbiz_push_base import BizCentralPushBase
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config, update_repay_lanzhou_config

from biztest.function.biz.biz_db_function import pytest
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_withhold_by_item_no, \
    get_withhold_by_channel_key, get_asset_info_by_item_no
from biztest.util.easymock.rbiz.paysvr import PaysvrMock
from biztest.util.easymock.rbiz.lanzhou_haoyue import RepayLanzhouMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_calc_date, get_four_element
from datetime import datetime, time
import common.global_const as gc


class TestRbizLanzhouPush(BizCentralPushBase):
    """
    zhongke_lanzhou 还款推送

    """

    @classmethod
    def setup_class(cls):
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        update_repay_lanzhou_config()
        cls.loan_channel = "zhongke_lanzhou"
        cls.current_date = datetime.now().date()
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.lanzhou_mock = RepayLanzhouMock(rbiz_mock)
        cls.check_settlement_fee_type = ['principal', 'interest', 'guarantee']
        cls.grace_day = 0
        # mock代扣成功
        cls.lanzhou_mock.update_repay_apply()
        cls.lanzhou_mock.update_repay_query()
        cls.paysvr_mock.update_query_protocol_channels_bind_sms()
        cls.paysvr_mock.update_auto_pay_withhold_success()
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))
        # 在脚本执行之前，初始化限制配置
        normal_time_limit = {"startTime": "00:00:00", "endTime": "22:30:00"}
        fail_times = {"auto": {"times": 1, "calByDay": False}, "active": {"times": 1, "calByDay": False},
                      "manual": {"times": 1, "calByDay": False}}
        update_repay_lanzhou_config()
        pass

    @classmethod
    def teardown_class(cls):
        update_repay_paysvr_config()
        update_repay_lanzhou_config()

    def setup_method(self):
        self.four_element = get_four_element()

        # # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element,
                                                                               count=self.count)

    def __set_lanzhou_statement(self, is_compensate):
        loan_id = self.db.get_loan_id_by_item_no(self.item_no)['asset_loan_record_due_bill_no']
        compensate_amount = float(
            self.db.get_sum_amount(self.item_no, self.period, 'principal,interest')['total_amount']) / 100
        self.lanzhou_mock.update_lanzhou_statement(is_compensate, loan_id, compensate_amount, self.period)
        return loan_id

    def set_lanzhou_compensate_statement(self):
        return self.__set_lanzhou_statement(True)

    def set_lanzhou_compensate_repay(self):
        return self.__set_lanzhou_statement(False)

    def get_lanzhou_config(self):
        return json.loads(self.nacos.get_config(self.tenant, 'KV', 'lanzhou_config')['content'])

    def set_lanzhou_config(self, values):
        self.nacos.update_configs(self.tenant, 'lanzhou_config', values)

    def get_settlement_expect_list(self, start_period, end_period, asset, fee_dict, repay_list):
        """
        fee_dict = {'repayprincipal':{'fee_type':'DUE_AT', 'days':1, 'calc_way':'T'},
                    'repayinterest':{'fee_type':'USER_REPAY', 'days':0, 'calc_way':'D'},
                    'guarantee':{'fee_type':'PUSH', 'days':1, 'calc_way':'D'}}
        :param start_period:
        :param end_period:
        :param asset:
        :param fee_dict:
        :param repay_list:
        :return:
        """
        for fee, fee_type, calc_way, days in fee_dict.items():
            for period in range(start_period, end_period + 1):
                if fee_type == '':
                    pass
                else:
                    self.get_settlement_time(days, period, asset, fee, fee_type=fee_type, calc_way=calc_way)

    def get_settlement_time(self, days, period, asset, fee, fee_type='PUSH', calc_way='T'):
        push_time_sql = "select asset_tran_due_at from asset_tran where " \
                        "asset_tran_asset_item_no = '{0}' and asset_tran_period={1} and " \
                        "asset_tran_type = '{2}'".format(asset, period, fee)
        capital_transaction = self.db.query(push_time_sql)[0]
        if fee_type == 'DUE_AT':
            push_time = capital_transaction['asset_tran_due_at']
        elif fee_type == 'PUSH':
            push_time = datetime.date().today()
        return self.add_work_days(push_time, days) if calc_way == 'T' else self.get_calc_date(push_time, days)

        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element)

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

    @pytest.mark.lanzhou_push
    @pytest.mark.lanzhou_push_active_advance_repay_push
    @pytest.mark.parametrize("period, is_holiday", [(1, True), (2, False)])
    def test_active_advance_repay_push(self, period, is_holiday):
        """
        兰州提前还1期推送 -- 不推送，D+2是工作日推线下还款(或者D+2推送线下还款失败)/否则D+3当代偿
        最后一期不在该场景中，算提前结清
        :param period: 提前还款的期次，不能是最后一期
        :param is_holiday: D+2是否是工作日，True:节假日，False:工作日
        """
        # step 1 提前还第1期成功
        self.begin_time = get_calc_date(datetime.now(), fmt='%Y-%m-%d %H:%M:00')
        print('begin_time is {0}'.format(self.begin_time))
        withhold, withhold_no_loan = self.repay_advance_fixed_period(period)

        # self.wait_all_user_at_receive(withhold, withhold_no_loan)

        # 第二步 执行小单的 CapitalAssetUserRepay任务
        # self.execute_no_loan_capital_asset_user_repay_and_check()

        # 第三步 获取所有的CapitalAssetUserRepay任务并循环便利，按照代扣顺序/乱序/倒序-根据用例场景
        capital_asset_user_repay_task_list = self.wait_central_task_appear(self.item_no, "CapitalAssetUserRepay")
        for capital_asset_user_repay_task in capital_asset_user_repay_task_list:
            # 第四步 执行大单的CapitalAssetUserRepay任务并检查user_repay_at和withhold_result_channel
            fee_type = self.execute_capital_asset_user_repay_and_check(capital_asset_user_repay_task)
            if 'principal' in fee_type:
                # 第五步 执行CapitalNotifyStore任务
                self.execute_capital_notify_store_and_check(is_exist=False)
                # 如果是工作日，走线下 否则 走代偿
                # 设置当天是否为工作日
                self.set_holiday(self.current_date, is_holiday)
                # 检查线下还款是否会生成capital_notify，无论走线下还是代偿都会生成
                self.execute_offline_and_check()
                # 执行线下还款的task
                self.execute_capital_push_task_and_check(is_holiday)
                if not is_holiday:
                    # 第八步 执行更新资方还款计划的task并检查
                    self.execute_refresh_capital_transaction_task_and_check(self.pd_recharge_list,
                                                                            period,
                                                                            period,
                                                                            capital_type='advance')
                    # 第九步 执行生成capital_notify的task并检查
                    self.execute_capital_notify_store_and_check()

                # 第十步 执行代偿看会不会生成新的capital_notify
                self.execute_compensate_and_check(is_holiday, self.period)
            else:
                # 本次代扣没有本金的不会生成capital_notify记录
                self.execute_capital_notify_store_and_check(is_exist=False)

    @allure.step(f"执行代偿的任务并检查")
    def execute_compensate_and_check(self, is_holiday, period):
        # 修改到期日为D+grace_day+2
        self.asset_import.change_asset(-self.period,
                                       self.item_no,
                                       self.item_num_no_loan,
                                       -(self.grace_day + 2))
        # 执行代偿只推送清结算的xxljob
        current_compensate_task_order = ''
        self.run_dcs_compensate_xxl_job(self.loan_channel, self.grace_day + 1)
        if not is_holiday:
            self.check_compensate_not_exist(self.item_no,
                                            'LanzhouSettlementCompensate',
                                            datetime.now().strftime("%Y-%m-%d %H:%M:00"))
        else:
            self.wait_and_run_central_task(self.item_no, 'LanzhouSettlementCompensate')
            except_data = self.get_except_capital_transaction('advance',
                                                              self.period,
                                                              self.period,
                                                              self.pd_recharge_list,
                                                              is_holiday=is_holiday)
            self.check_capital_transaction_for_fee_type(self.item_no,
                                                        except_data,
                                                        self.check_settlement_except_cols,
                                                        self.period,
                                                        self.period)
            # 执行处理代偿文件的任务
            self.run_lanzhou_file_xxl_job(True)
            loan_id = self.set_lanzhou_compensate_statement()
            order_no = 'COMPFILE_{0}'.format(get_calc_date(self.current_date, day=-1, fmt='%Y-%m-%d'))
            self.wait_and_run_central_task(order_no, 'LanzhouCallback')
            self.wait_and_run_central_task(loan_id, 'LanzhouCallbackProcess')

    @allure.step(f"执行更新资方还款计划的任务")
    def execute_refresh_capital_transaction_task_and_check(self, withhold_info, period_start, period_end, capital_type):
        # 等待LanzhouRepaySettlement出现并执行
        self.wait_and_run_central_task(self.item_no, 'LanzhouRepaySettlement')
        except_data = self.get_except_capital_transaction(capital_type, period_start, period_end, withhold_info)
        # 提前还款，预计结算时间为到期日，实际结算时间为到期日D+grace_day+1（类型线下还款）
        # 如果到期日D+grace_day+1为休息日，则实际结算时间为到期日D+grace_day+2（类型代偿)
        self.check_capital_transaction_for_fee_type(self.item_no,
                                                    except_data,
                                                    self.check_settlement_except_cols,
                                                    period_start,
                                                    period_end)

    def get_except_capital_transaction(self, capital_type, period_start, period_end, withhold_info, is_holiday=False):
        """
        构造不同场景下capital_transaction的期望值
        :param capital_type:
        :param period_start:
        :param period_end:
        :param withhold_info:
        :param is_holiday:
        :return:
        """
        except_data = []
        now = datetime.now()
        current_date = '{0} 00:00:00'.format(self.get_calc_date(now, fmt='%Y-%m-%d', is_str=True))
        current_date_before = '{0} 00:00:00'.format(self.get_calc_date(now,
                                                                       day=-(self.grace_day + 1),
                                                                       fmt='%Y-%m-%d',
                                                                       is_str=True))
        current_date_compensate = '{0} 00:00:00'.format(self.get_calc_date(now,
                                                                           day=-(self.grace_day + 2),
                                                                           fmt='%Y-%m-%d',
                                                                           is_str=True))
        capital_transaction_status = 'finished'
        if capital_type == 'advance':
            # 如果提前还款，D+2是节假日，则走代偿，类型为compensate，状态为unfinished，
            # actual_operate_at为默认时间1000-01-01 00:00:00
            # 如果D+2是工作日，则走线下还款，类型为offline，状态为finished，actual_operate_at为到期日D+2
            operation_type = 'compensate' if is_holiday else 'offline'
            capital_transaction_status = 'unfinished' if is_holiday else capital_transaction_status
        elif capital_type == 'early_settlement':
            operation_type = 'early_settlement'
        elif capital_type == 'normal':
            operation_type = 'normal'

        if isinstance(withhold_info, list) and capital_type in ('advance', 'compensate'):
            # 如果是没有还款的代偿
            capital_tran = self.db.get_biz_capital_transaction_by_item_no_period(self.item_no, self.period)
            withhold_info = pd.DataFrame.from_records(data=capital_tran)
            withhold_info.rename(columns={'capital_transaction_origin_amount': 'capital_transaction_repaid_amount'})

        for fee in self.check_settlement_fee_type:
            for period in range(period_start, period_end + 1):
                withhold_info_index = withhold_info.set_index(['capital_transaction_period',
                                                               'capital_transaction_type'])
                repaid_amount = withhold_info_index.loc[period, fee]['capital_transaction_repaid_amount']
                actual_operate_at = current_date_before if fee == 'guarantee' else current_date
                current_date_before = current_date_compensate if operation_type == 'compensate' else current_date_before
                actual_operate_at = '1000-01-01 00:00:00' if is_holiday and capital_type == 'advance' else \
                    actual_operate_at
                except_data.append({'capital_transaction_expect_operate_at': current_date_before,
                                    'capital_transaction_actual_operate_at': actual_operate_at,
                                    'capital_transaction_status': capital_transaction_status,
                                    'capital_transaction_operation_type': operation_type,
                                    'capital_transaction_type': fee,
                                    'capital_transaction_repaid_amount': repaid_amount,
                                    'capital_transaction_period': period})
        return except_data

    @allure.step(f"执行D+2的线下还款推送到资方的任务并检查task是否生成")
    def execute_capital_push_task_and_check(self, is_holiday, is_early_settlement=False):
        # 执行捞取资方推送的xxl-job
        self.run_capital_push_xxl_job()
        # 等待LanzhouPush出现并执行
        offline_task_order_no = 'OFFLINE_{0}_{1}'.format(self.item_no, self.period)
        excepts = {'code': 1} if is_holiday else {'code': 0}
        task_id = self.wait_and_run_central_task(offline_task_order_no, 'LanzhouPush', excepts=excepts)
        # 获取兰州的推送配置文件
        self.get_lanzhou_config()
        if is_holiday:
            self.check_task_memo(task_id, '延迟推送')
            self.check_capital_notify_not_exist(self.item_no,
                                                notify_type='offline',
                                                start_period=self.period,
                                                end_period=self.period)
        else:
            if is_early_settlement:
                # 等待LanzhouRepayTrial出现并执行
                self.wait_and_run_central_task(self.item_no, 'LanzhouRepayTrial')
                # 等待LanzhouRepayTrialQuery出现并执行
                self.wait_and_run_central_task(self.item_no, 'LanzhouRepayTrialQuery')
            # 等待LanzhouRepayApply出现并执行
            self.wait_and_run_central_task(self.item_no, 'LanzhouRepayApply')
            # 出现前先修改mock为成功
            self.set_repay_query_success()
            # 等待LanzhouRepayQuery出现并执行
            self.wait_and_run_central_task(self.item_no, 'LanzhouRepayQuery')
            # 检查请求和返回

    @allure.step(f"执行D+2的线下还款生成任务和检查capital_notify是否生成")
    def execute_offline_and_check(self, timeout=60):
        # 执行D+2的线下还款生成任务和检查capital_notify是否生成，无论是否是工作日都会生成capital_notify
        # 获取配置
        lanzhou_config = self.get_lanzhou_config()
        # 设置代偿时间为当前时间之前, 这样的话生成的capital_notify不用修改时间可以直接运行
        capital_notify_plan_at = self.set_compensate_before(lanzhou_config)
        # 配置的线下还款的宽限时间，为数值为1：表示的是到期日的D+2执行
        self.grace_day = lanzhou_config['grace_day']

        # 修改到期日为逾期grace_day+1天
        _, _, biz_capital_tran_due_at_real = self.asset_import.change_asset(-self.period,
                                                                            self.item_no,
                                                                            self.item_num_no_loan,
                                                                            -(self.grace_day + 1))

        # 执行CapitalNotifyCompensateStore任务
        current_compensate_task_order = '{0}_{1}'.format(self.loan_channel, get_calc_date(self.current_date,
                                                                                          day=-1,
                                                                                          fmt='%Y-%m-%d'))
        while True:
            self.run_capital_compensate_xxl_job(self.loan_channel)
            self.wait_and_run_central_task(current_compensate_task_order, 'CapitalNotifyCompensateStore')
            is_exist = self.db.get_capital_notify_exist(self.item_no,
                                                        self.period,
                                                        'compensate,advance,early_settlement,overdue,normal,offline')
            if is_exist:
                break
            if not timeout:
                raise ValueError('not found the capital_notify with 1 min')
            timeout -= 1
            # 执行xxljob-线下还款
            time.sleep(1)
        # 检查生成的capital_notify是否正确
        self.check_capital_notify(self.item_no,
                                  capital_notify_type='offline',
                                  capital_notify_plan_at=capital_notify_plan_at,
                                  capital_notify_status='open',
                                  capital_notify_period_start=self.period,
                                  capital_notify_period_end=self.period,
                                  capital_notify_to_system=self.loan_channel)
        # 执行之前修改计划推送时间为: 当前时间
        # self.db.update_capital_notify_plan_at_by_id(capital_notify_id, '{0} 00:00:00'.format(self.current_date))

    @allure.step(f"执行大单的CapitalAssetUserRepay和检查capital_transaction的user_repay_at和withhold_result_channel")
    def execute_capital_asset_user_repay_and_check(self, task):
        # 执行大单的CapitalAssetUserRepay和检查capital_transaction的user_repay_at和withhold_result_channel
        self.run_task_in_biz_central_by_task_id(task['task_id'], excepts={"code": 0})
        task = self.db.get_central_task_request_data_by_id(task['task_id'])
        self.pd_recharge_list = self.get_withhold_info(self.item_no, task['rechargeList'], task['repayList'])
        return self.check_capital_transaction_for_fee_type(self.item_no,
                                                           self.pd_recharge_list,
                                                           self.check_user_repay_except_cols,
                                                           self.period,
                                                           self.period)

    @allure.step(f"执行小单的CapitalAssetUserRepay和检查capital_transaction的user_repay_at和withhold_result_channel")
    def execute_no_loan_capital_asset_user_repay_and_check(self):
        # 执行小单的CapitalAssetUserRepay任务后不会生成CapitalNotifyStore任务
        task_list = self.wait_central_task_appear(self.item_num_no_loan, "CapitalAssetUserRepay")
        for task in task_list:
            self.run_task_in_biz_central_by_task_id(task['task_id'])
            self.db.wait_central_task_close_by_id(task['task_id'])
            self.db.check_central_task_not_appear(self.item_no, "CapitalNotifyStore")
            self.db.check_central_task_not_appear(self.item_num_no_loan, "CapitalNotifyStore")

    @allure.step(f"执行CapitalNotifyStore和检查capital_notify和类型，计划时间")
    def execute_capital_notify_store_and_check(self, is_exist=False, **kwargs):
        # 执行小单的CapitalAssetUserRepay任务后不会生成CapitalNotifyStore任务
        capital_notify_store_task_list = self.wait_central_task_appear(self.item_no, 'CapitalNotifyStore')
        if len(capital_notify_store_task_list) > 1:
            raise ValueError("found CapitalNotifyStore more than one!")
        capital_notify_store_task = capital_notify_store_task_list[0]
        self.run_task_in_biz_central_by_task_id(capital_notify_store_task['task_id'])
        if not is_exist:
            self.check_capital_notify_not_exist(self.item_no)
        else:
            self.check_capital_notify(self.item_no, **kwargs)

    def set_repay_query_success(self):
        """
        设置还款查询接口为成功
        :return:
        """
        guarantee, principal_interest = self.db.get_signal_amount_bond_by_item_no_period(self.item_no, self.period)
        self.lanzhou_mock.update_repay_query(state=4, rpyBondComAmt=guarantee, rpyBankAmt=principal_interest)

    @staticmethod
    def get_withhold_info(item_no, recharge_list, repay_list):
        channel_name = get_withhold_by_channel_key(recharge_list)[0]['withhold_channel']
        loan_channel = get_asset_info_by_item_no(item_no)[0]['asset_loan_channel']
        channel_name = channel_name if channel_name == loan_channel else 'qsq'
        pd_recharge_list = pd.DataFrame.from_records(data=repay_list)
        pd_recharge_list.columns = ['capital_transaction_user_repay_at',
                                    'capital_transaction_period',
                                    'capital_transaction_type',
                                    'capital_transaction_repaid_amount']
        pd_recharge_list['capital_transaction_withhold_result_channel'] = channel_name
        pd_recharge_list['capital_transaction_user_repay_at'] = list(pd_recharge_list[
                                                                         'capital_transaction_user_repay_at'])[0]
        # .replace('repayprincipal', 'principal')
        pd_recharge_list['capital_transaction_type'] = pd_recharge_list.capital_transaction_type.apply(
            lambda x: x.replace('repay', ''))
        return pd_recharge_list
