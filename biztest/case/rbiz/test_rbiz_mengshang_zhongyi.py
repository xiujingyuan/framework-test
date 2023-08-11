# -*- coding: utf-8 -*-
import datetime

import pytest
import datetime

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.case.rbiz.rbiz_push_base import BizCentralPushBase

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
    get_asset_tran_by_item_no_and_type_and_period, get_zhongbang_zhongji_capital_fee_amount
from biztest.interface.rbiz.rbiz_interface import monitor_check, bind_sms, simple_active_repay, paysvr_callback, \
    asset_buyback
from biztest.util.easymock.rbiz.mengshang_zhongyi import RepayMengShangZhongYiMock
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.util.tools.tools import get_four_element, get_date_before_today, get_item_no
import common.global_const as gc


@pytest.mark.rbiz_auto_test
@pytest.mark.rbiz_mengshang_zhongyi
class TestRbizMengshangZhongyi(BaseRepayTest):
    """
    mengshang_zhongyi 还款

    """
    loan_channel = "mengshang_zhongyi"
    our_sign_company = "tq,tqa,tqb"
    grant_principal = 1000000

    @classmethod
    def setup_class(cls):
        monitor_check()
        cls.mszy_mock = RepayMengShangZhongYiMock(rbiz_mock)
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.task = Task("rbiz%s" % gc.ENV)
        cls.msg = Msg("rbiz%s" % gc.ENV)

    def setup_method(self):
        # 大小单进件
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element,
                                                                               item_no="ms" + get_item_no(),
                                                                               asset_amount=10000)

    def test_mengshang_zhongyi_active_advance_repay(self):
        """
        提前还1期 不允许
        """
        # step 1 主动还款 提前还款
        self.change_asset_due_at(0, -10)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan, code=1)

    def test_mengshang_zhongyi_active_normal_repay(self):
        """
        正常还1期，(该资金方无宽限期)
        资方扣1单（资金方扣所有），小单1单
        """
        # step 1 主动还款 到期日
        self.change_asset_due_at(-1, 0)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.mszy_mock.mengshang_zhongyi_repay_apply()
        self.paysvr_mock.update_query_protocol_channels_not_bind_sms(channel_name='baofoo_tq_protocol')
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # 获取代扣流水号
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        # 资方代扣金额 = 第1期全额
        capital_withhold_amount = int(asset_tran_amount["asset_tran_amount"])
        self.mszy_mock.mengshang_zhongyi_repay_query(repayPrincipal=800.99, repayInterest=71.67,
                                                     repayGuaranteeFee=72.84, repayTerm=1)
        self.run_all_task_after_repay_success()

        # step 2 DB数据检查，大单1单 小单1单
        withhold = get_withhold_by_item_no(self.item_no)
        withhold_no_loan = get_withhold_by_item_no(self.item_num_no_loan)

        # 代扣顺序： 资方先扣
        check_withhold_data_by_sn(order_no_capital, withhold_channel=self.loan_channel)
        # 代扣拆单：拆成2单
        check_withhold_split_count_by_item_no_and_request_no(self.item_no, withhold[0]["withhold_request_no"], 1)
        capital_withhold = {
            "withhold_sign_company": "tq",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_withhold_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        capital_withhold_type = ['repayprincipal', 'repayinterest', 'consult', 'reserve']
        check_capital_withhold_detail_vs_asset_tran(order_no_capital, capital_withhold_type)
        # 小单代扣数据检查
        param_no_loan = {
            "withhold_amount": int(asset_tran_amount_no_loan["asset_tran_balance_amount"])
        }
        check_withhold_result_without_split(self.item_num_no_loan, **param_no_loan)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_repay_one_period(self.item_no)

        # # step 3 数据检查，检查推给资金方的日志
        # check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel, "execute_combine_withhold",
        #                            withhold[0]['withhold_serial_no'], 1)

        # 处理推送部分,该资金方是假推送
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "MengshangZhongyiCapitalPush", excepts={"code": 0})
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        # # 检查推送请求的参数
        check_capital_notify(self.item_no, withhold[0]["withhold_serial_no"], capital_notify_type="normal",
                             capital_notify_status='success')

    def test_mengshang_zhongyi_active_advance_settle_payoff(self):
        """
        在第一期内提前结清，此处写死资金方占用1天
        资方通道扣：大单当期本+当期部分费（算法：实际占用天数/当期总天数 x 当期费用总金额(四舍五入保留2位小数) ）+当期部分的息（必须小于等于当期利息,试算接口返回的金额）+剩余期次的所有本金
        我方扣：当期剩余的息+当期剩余的费+剩余期次的息和费
        """
        self.change_asset_due_at(-1, 1)  # 如果非大月份，该case可能跑不过，因为公式中的天数不一样了
        self.mszy_mock.mengshang_zhongyi_repay_trial(principal=10000.00, interest=10.00)
        self.mszy_mock.mengshang_zhongyi_repay_apply()
        self.paysvr_mock.update_query_protocol_channels_not_bind_sms(channel_name='baofoo_tq_protocol')
        # step 1 主动还款
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)

        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]

        # 代扣金额
        # 资方代扣金额 = 大单当期本+当期费+当期部分的息（必须小于等于当期利息,试算返回的）+剩余期次的所有本金
        # 我方代扣金额 = 当期剩余的息+剩余期次的息和费

        one_interest = get_asset_tran_by_item_no_and_type_and_period(self.item_no, "repayinterest", 1)[0][
            'asset_tran_amount']
        one_fee01 = get_asset_tran_by_item_no_and_type_and_period(self.item_no, "consult", 1)[0][
            'asset_tran_amount']   # 我方原始费用值
        capital_fee = get_zhongbang_zhongji_capital_fee_amount(self.item_no, end_period=1)
        one_fee02 = get_asset_tran_by_item_no_and_type_and_period(self.item_no, "reserve", 1)[0][
            'asset_tran_amount']
        capital_withhold_amount = self.grant_principal + capital_fee + 1000  # 资金方扣的金额, mock第一期的代扣利息为10元，写死
        capital_tran_amount = self.grant_principal + one_interest + capital_fee
        our_withhold_amount = int(asset_tran_amount["asset_tran_amount"]) - capital_withhold_amount
        our_tran_amount = int(asset_tran_amount["asset_tran_amount"]) - self.grant_principal - capital_fee - 1000

        self.mszy_mock.mengshang_zhongyi_repay_query(repayPrincipal=10000.00, repayInterest=10.00,
                                                     repayGuaranteeFee=70.48, repayTerm=1)
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()

        # # # step 2 数据检查，检查推给资金方的日志
        # check_withhold_request_log(withhold[0]['withhold_request_no'], self.loan_channel + "_advance_payoff",
        #                            "execute_combine_withhold",
        #                            withhold[0]['withhold_serial_no'], 5)

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
            "withhold_sign_company": "tq",
            "withhold_channel": self.loan_channel,
            "withhold_status": "success",
            "withhold_amount": capital_withhold_amount,
            "asset_tran_amount": capital_tran_amount
        }
        check_withhold_by_serial_no(order_no_capital, **capital_withhold)
        our_withhold = {
            "withhold_sign_company": "tq,tqa,tqb",
            "withhold_channel": "baidu_tq3_quick",
            "withhold_status": "success",
            "withhold_amount": our_withhold_amount,
            "asset_tran_amount": our_tran_amount
        }
        check_withhold_by_serial_no(order_no_our, **our_withhold)
        # 检查充值还款
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[0]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold[1]['withhold_channel_key'])
        check_account_recharge_and_repay(self.four_element['data']["id_number_encrypt"],
                                         withhold_no_loan[0]['withhold_channel_key'])
        # 检查 asset_tran
        check_asset_tran_payoff(self.item_no)

        # 处理推送部分，假推
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        self.run_capital_push_by_api()
        self.wait_and_run_central_task(self.item_no, "MengshangZhongyiCapitalPush", excepts={"code": 0})
        self.wait_and_run_central_task(self.item_no, "GenerateCapitalNotify")
        # # 检查capital notify
        check_capital_notify(self.item_no, withhold[0]["withhold_serial_no"], capital_notify_type="early_settlement",
                             capital_notify_status='success')

    def test_mengshang_zhongyi_active_overdue_repay(self):
        """
        逾期还款(逾期后走我方代扣，不需要推送，但是需要走代偿)
        推送消息给dcs
        """
        # step 1 主动还款 逾期1天
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()

        # 推送部分， 逾期按照代偿处理，不推送

    def test_mengshang_zhongyi_protocol_sign_success(self):
        """
        到期日提前结清（该资金方支持到期日提前结清，在第一期到期日提前结清），检查绑卡信息
        蒙商中裔要协议共享，此处走提前结清场景（到期日提前结清），需要在paysvr接口返回baofoo通道并且状态=1时，会在paysvr重新走绑卡
        """
        self.change_asset_due_at(-1, 0)  # 如果非大月份，该case可能跑不过，因为公式中的天数不一样了
        # 提前修改需要使用到的接口mock返回
        self.mszy_mock.mengshang_zhongyi_repay_trial(principal=10000.00, interest=71.67)
        self.paysvr_mock.update_query_protocol_channels_not_bind_sms(channel_name='baofoo_tq_protocol')

        # 主动还款
        # 获取大单还款总金额
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no)
        #获取小单总金额
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan)
        # 发起还款
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        # 获取发起还款之后同步生成的代扣流水号（资金方与我方各1）
        order_no_capital = repay_resp["data"]["project_list"][0]["order_no"]
        order_no_our = repay_resp["data"]["project_list"][1]["order_no"]

        # 获取短信验证码
        verify_seq = bind_sms(order_no_capital)
        # 再次调用还款接口，进行协议支付验证
        params_combo_active = {
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"],
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"],
            "project_num_no_loan_amount": asset_tran_amount_no_loan["asset_tran_balance_amount"]
        }
        params_combo_active.update(order_no=order_no_capital, verify_seq=verify_seq, verify_code='123456')
        simple_active_repay(self.item_no, **params_combo_active)

        # 检查card_bind的数据
        card_bind = {
            "card_bind_serial_no": order_no_capital,
            "card_bind_channel": "mengshang_zhongyi_sign",
            "card_bind_status": "success"
        }
        check_card_bind_info(self.four_element['data']["bank_code_encrypt"], **card_bind)

