# -*- coding: utf-8 -*-
import datetime

import pytest
import datetime

from biztest.case.rbiz.base_repay_test import BaseRepayTest

from biztest.util.easymock.rbiz.paysvr import *
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.biz.biz_check_function import check_capital_push_request_log, check_data, check_capital_notify
from biztest.function.biz.biz_db_function import get_capital_notify_req_data_param_by_item_no, \
    get_capital_notify_req_data_by_item_no
from biztest.function.rbiz.rbiz_check_function import check_withhold_request_log, check_withhold_result_without_split, \
    check_account_recharge_and_repay, check_asset_tran_repay_one_period, check_withhold_split_count_by_request_no, \
    check_withhold_split_count_by_item_no_and_request_no, check_asset_tran_payoff, check_withhold_by_serial_no, \
    check_settle_payoff_capital_withhold_detail_vs_asset_tran, check_capital_withhold_detail_vs_asset_tran, \
    check_withhold_data_by_sn, check_withhold_sign_company, check_card_bind_info, check_card_by_item_no, \
    check_withhold_card_by_card_num, check_individual_by_item_no
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period, \
    get_withhold_by_item_no, get_withhold_by_serial_no, update_card_bind_update_at_by_card_number, \
    get_asset_tran_by_item_no_and_type_and_period, get_capital_part_fee_amount
from biztest.interface.rbiz.rbiz_interface import monitor_check, bind_sms, simple_active_repay, paysvr_callback, \
    asset_buyback
from biztest.util.easymock.rbiz.hebei_jiahexing_ts import RepayHebeiJiahexingTsMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element, get_date_before_today, get_item_no
import common.global_const as gc


@pytest.mark.rbiz_auto_test
@pytest.mark.rbiz_hebei_jiahexing_ts
class TestRbizHebeiJiahexingTs(BaseRepayTest):
    """
    hebei_jiahexing_ts 还款
    注意：此资金方走的我方通道代扣
    所以以下case中都没有校验小单的通道，因为将通道改为了大单的通道"hebei_jiahexing_ts"，导致小单执行时也是这个代扣通道
    """
    loan_channel = "hebei_jiahexing_ts"
    our_sign_company = "tq,tqa,tqb"
    grant_principal = 800000

    @classmethod
    def setup_class(cls):
        monitor_check()
        cls.hebei_jiahexing_mock = RepayHebeiJiahexingTsMock(rbiz_mock)
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.task = Task("rbiz%s" % gc.ENV)
        cls.msg = Msg("rbiz%s" % gc.ENV)

    def setup_method(self):
        # 大小单进件
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element,
                                                                               item_no="jhx" + get_item_no(),
                                                                               asset_amount=8000)

    def test_hebei_jiahexing_ts_active_advance_repay(self):
        """
        提前还1期 不允许
        """
        # step 1 主动还款 提前还款
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan, code=1)

    def test_hebei_jiahexing_ts_active_normal_repay(self):
        """
        正常还1期，(该资金方宽限期3天，到期3天都可以走正常还款逻辑)
        资方扣1单，小单1单
        走的是资金方扣，但是不调用资金方任何接口，只是走我方接口代扣
        """
        # step 1 主动还款 到期日
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        # 因为需要走paysvr代扣，避免代扣通道变更，所以此处修改了代扣通道名称
        self.paysvr_mock.update_auto_pay_withhold_success(channel_name='hebei_jiahexing_ts')
        self.paysvr_mock.update_withhold_query(channel_name='hebei_jiahexing_ts')
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # 获取代扣流水号
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        # 资方代扣金额 = 第1期全额
        capital_withhold_amount = int(asset_tran_amount["asset_tran_amount"])
        self.run_all_task_after_repay_success()

        # step 2 DB数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 1)
        capital_withhold = {
            "withhold_sign_company": "jiahexing",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        capital_withhold_type = ['repayprincipal', 'repayinterest', 'consult', 'reserve', 'guarantee']
        check_capital_withhold_detail_vs_asset_tran(order_no_capital, capital_withhold_type)
        # 小单代扣数据检查
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        # 这个是小单的通道等校验，此处屏蔽，原因见顶部中文描述
        # check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_repay_one_period(self.item_no)
        # 恢复paysvr接口返回
        self.paysvr_mock.update_auto_pay_withhold_success()
        self.paysvr_mock.update_withhold_query()

        # 处理推送部分
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.hebei_jiahexing_mock.hebei_jiahexing_push_apply()
        self.wait_and_run_central_task(self.item_no, "HebeiJiahexingTsCapitalPush", excepts={"code": 2})
        # 因为这个资金方要在这个任务中调用两个甚至3个（有试算的时候）接口，所以需要执行两次
        self.hebei_jiahexing_mock.hebei_jiahexing_push_repayquery()
        self.wait_and_run_central_task(self.item_no, "HebeiJiahexingTsCapitalPush", excepts={"code": 0})
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        # # 检查推送请求的参数
        check_capital_notify(self.item_no, withhold[0]["withhold_serial_no"], capital_notify_type="normal",
                             capital_notify_status='success')

    def test_hebei_jiahexing_ts_active_advance_settle_payoff(self):
        """
        在第一期内提前结清，此处写死资金方占用1天
       涉及拆单：
        资金方扣：提前结清所有期次的本金+利息（试算接口返回）+费用（按日计息）+担保费（按日计息）
        我方扣：剩余部分
        按日计息公式：
            实际占用天数 = 日期相减（算头不算尾）
            应还资金方费用 = 当期还款金额（consult/reserve/guarentee）/当期天数 x 实际占用天数
        """
        self.change_asset_due_at(-1, 1)  # 如果非大月份，该case可能跑不过，因为公式中的天数不一样了
        self.hebei_jiahexing_mock.hebei_jiahexing_repay_trial(respcode=9999, prinlamt=8000, intamt=10, penaltyamt=0)
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)

        # 因为需要走paysvr代扣，避免代扣通道变更，所以此处修改了代扣通道名称

        self.paysvr_mock.update_auto_pay_withhold_success(channel_name='hebei_jiahexing_ts')
        self.paysvr_mock.update_withhold_query(channel_name='hebei_jiahexing_ts')

        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]

        # 代扣金额
        # 资方代扣金额 = 大单当期本 + 利息（试算接口返回）[必须小于等于当期利息] + 费用（按日计息) + 担保费（按日计息）+ 剩余期次的所有本金
        # 我方代扣金额 = 当期剩余的息（若有）+ 剩余期次的息和费

        one_interest = get_asset_tran_by_item_no_and_type_and_period(self.item_no, "repayinterest", 1)[0][
            'asset_tran_amount']
        one_fee01 = get_asset_tran_by_item_no_and_type_and_period(self.item_no, "consult", 1)[0][
            'asset_tran_amount']   # 我方原始费用值
        # 资金方的费用，按照占用天数计算
        reserve = get_capital_part_fee_amount(self.item_no, end_period=1, fee_type='reserve')
        consult = get_capital_part_fee_amount(self.item_no, end_period=1, fee_type='consult')
        guarantee = get_capital_part_fee_amount(self.item_no, end_period=1, fee_type='guarantee')
        capital_fee = reserve + consult + guarantee
        one_fee02 = get_asset_tran_by_item_no_and_type_and_period(self.item_no, "reserve", 1)[0][
            'asset_tran_amount']
        capital_withhold_amount = self.grant_principal + capital_fee + 1000  # 资金方扣的金额,mock第一期的代扣利息为10元，写死
        capital_tran_amount = self.grant_principal + one_interest + capital_fee
        our_withhold_amount = int(asset_tran_amount["asset_tran_amount"]) - capital_withhold_amount
        our_tran_amount = int(asset_tran_amount["asset_tran_amount"]) - self.grant_principal - capital_fee
        self.run_all_task_after_repay_success()

        # step 3 数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_request_no(withhold[0]["withhold_request_no"], 3)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 2)

        #  拆成2单扣
        capital_withhold = {
            "withhold_sign_company": "jiahexing",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_tran_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        # our_withhold = {
        #     "withhold_sign_company": "tq,tqa,tqb",
        #     "withhold_channel": "hebei_jiahexing_ts",
        #     "withhold_status": "success",
        #     "withhold_amount": our_withhold_amount,
        #     "asset_tran_amount": our_tran_amount
        # }
        #check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)
        # 恢复paysvr mock的通道变更
        self.paysvr_mock.update_auto_pay_withhold_success()
        self.paysvr_mock.update_withhold_query()

        # 处理推送部分
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        # 提前结清需要先试算再推送
        self.hebei_jiahexing_mock.hebei_jiahexing_repay_trial(respcode=9999, prinlamt=8000, intamt=10, penaltyamt=0)
        self.hebei_jiahexing_mock.hebei_jiahexing_push_apply()
        self.wait_and_run_central_task(self.item_no, "HebeiJiahexingTsCapitalPush", excepts={"code": 2})
        # 因为这个资金方要在这个任务中调用两个甚至3个（有试算的时候）接口，所以需要执行两次
        self.hebei_jiahexing_mock.hebei_jiahexing_push_repayquery()
        self.wait_and_run_central_task(self.item_no, "HebeiJiahexingTsCapitalPush", excepts={"code": 0})
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        # # 检查capital notify
        check_capital_notify(self.item_no, withhold[0]["withhold_serial_no"], capital_notify_type="early_settlement",
                             capital_notify_status='success')

    def test_hebei_jiahexing_ts_active_overdue_79day_repay(self):
        """
        只还第一期（第一期逾期4天，真正逾期1天）
        宽限期外还款，逾期4-79天内（逾期还款）
        资方扣1单（资方代扣所有（罚息需要调用接口获取）），小单1单
        走的是资金方扣，先调用资金方的试算接口，然后走我方接口代扣
        """
        # step 1 主动还款 逾期4天，真正逾期1天
        self.change_asset_due_at(-1, -4)
        self.hebei_jiahexing_mock.hebei_jiahexing_repayplanquery()  # 大单刷罚息此时应该是调用的资金方的接口
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        #发起代扣前会调用试算接口，因为之前刷罚息mock返回的第一期罚息为6.6元，所以试算mock也需要是这么多罚息，不然会报错：罚息不一致
        self.hebei_jiahexing_mock.hebei_jiahexing_repay_trial(respcode=9999, prinlamt=647.04, intamt=43.33, penaltyamt=6.6)
        # 因为需要走paysvr代扣，避免代扣通道变更，所以此处修改了代扣通道名称
        self.paysvr_mock.update_auto_pay_withhold_success(channel_name='hebei_jiahexing_ts')
        self.paysvr_mock.update_withhold_query(channel_name='hebei_jiahexing_ts')
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # 获取代扣流水号
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        # 资方代扣金额 = 第1期全额
        capital_withhold_amount = int(asset_tran_amount["asset_tran_amount"])
        self.run_all_task_after_repay_success()

        # step 2 DB数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 1)
        capital_withhold = {
            "withhold_sign_company": "jiahexing",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        capital_withhold_type = ['repayprincipal', 'repayinterest', 'consult', 'reserve', 'guarantee', 'lateinterest']
        check_capital_withhold_detail_vs_asset_tran(order_no_capital, capital_withhold_type)
        # 小单代扣数据检查
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        #check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_repay_one_period(self.item_no)
        # 恢复paysvr mock的通道变更
        self.paysvr_mock.update_auto_pay_withhold_success()
        self.paysvr_mock.update_withhold_query()

        # 处理推送部分
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        # 逾期4-79天内需要先试算再推送
        self.hebei_jiahexing_mock.hebei_jiahexing_repay_trial(respcode=9999, prinlamt=647.04, intamt=43.33,
                                                              penaltyamt=6.6)
        self.hebei_jiahexing_mock.hebei_jiahexing_push_apply()
        self.wait_and_run_central_task(self.item_no, "HebeiJiahexingTsCapitalPush", excepts={"code": 2})
        # 因为这个资金方要在这个任务中调用两个甚至3个（有试算的时候）接口，所以需要执行两次
        self.hebei_jiahexing_mock.hebei_jiahexing_push_repayquery()
        self.wait_and_run_central_task(self.item_no, "HebeiJiahexingTsCapitalPush", excepts={"code": 0})
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        # # 检查capital notify
        check_capital_notify(self.item_no, withhold[0]["withhold_serial_no"], capital_notify_type="overdue",
                             capital_notify_status='success')

    def test_hebei_jiahexing_ts_active_overdue_80day_repay(self):
        """
        逾期>=80天后还款,回购资产，全部走我方扣
        不推送
        """
        self.change_asset_due_at(-1, -80)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()

