from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.easymock.easymock_config import global_rbiz_mock
from biztest.config.global_rbiz.global_rbiz_kv_config import update_tha_rbiz_paysvr_config, update_rbiz_config
from biztest.function.global_dcs.dcs_global_check import check_dcs_asset_data, check_dcs_asset_and_tran, \
    check_dcs_account_log, check_dcs_refund_result, check_dcs_clearing_tran, check_dcs_settlement
from biztest.function.global_dcs.dcs_global_common_function import asset_import_and_auto_loan, \
    asset_import_and_auto_noloan
from biztest.function.global_dcs.dcs_global_db import dcs_run_task_by_order_no, get_task_capital_asset_sync, \
    get_account_balance_available, update_dcs_global_task_next_run_at, update_clearing_tran_create_at, \
    get_dcs_final_tran_info_by_item_no
from biztest.function.global_dcs.dcs_run_xxl_job import DcsRunXxlJob
from biztest.function.global_rbiz.rbiz_global_check_function import check_refund_request
from biztest.function.global_rbiz.rbiz_global_db_function import get_asset_tran_balance_amount_by_item_no, \
    get_withhold_by_item_no, get_withhold_by_serial_no, time, get_withhold_request_by_serial_no
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
import pytest
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, withhold_cancel, paysvr_query_tolerance_result
from biztest.util.asserts.assert_util import Assert
from biztest.util.easymock.payment_global import PaymentGlobalMock
from biztest.util.task.task import TaskGlobalRepay
from biztest.util.tools.tools import get_four_element_global
from biztest.function.global_dcs.dcs_global_common_function import refund_result_success_to_dcs
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, withhold_refund_online, available_refund_query

class TestThaPicocapitalPlus(BaseTestCapital, BaseGlobalRepayTest):
    """
    1、大小单如果是优惠券 / 容差还款，出入户置为空，等结算时再选择，结算与大单的代偿流程一致；
    不写出入户的原因是之前如果v_service余额不足会导致结算在转账这一步卡住；
    大单代偿 / 优惠券 / 容差还款的结算不会记录settlement、account_transfer
    表，这个原因是没有出入户无法批量转账，就不会记录结算表了，直接转账记账account_log。
    2、总结来说：大单的代偿以及大小单的优惠券/容差还款是没有出入户的
    """

    def init(self):
        super(TestThaPicocapitalPlus, self).init()
        self.channel = "pico_bangkok"
        self.four_element = get_four_element_global()
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e")
        self.task = TaskGlobalRepay()
        self.mock = PaymentGlobalMock(global_rbiz_mock)

    @pytest.fixture()
    def case(self):
        self.init()

    # 每个用例前执行
    def setup(self):
        # 清理历史task，避免job执行时间过长
        update_dcs_global_task_next_run_at(task_priority=1, status='close')

    @pytest.mark.global_dcs_thailand
    def test_loan_and_noloan_tolerance_payoff(self, case):
        # withhold_channel = "tolerance_payoff" 容差结清 - 20221028 test通过
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        check_dcs_asset_data(self.item_no, self.item_no_x)
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        # KV:dcs_channel_config中写死配置account_channel对应的放款出户为 v_pico_principal_gbpay
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        # 正常还款清分
        # 1.发起主动代扣
        # 手动修改rbiz还款状态为success
        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_list = [project["order_no"] for project in resp_combo_active["content"]["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order,  project_num_loan_channel_amount+project_num_no_loan_amount, 2,  channel_name="tolerance_payoff")
        self.mock.update_withhold_query_success(self.item_no, 2, "tolerance_payoff")
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        for i in range(3):
            self.msg.run_msg_by_id_and_search_by_order_no(order_no)
            self.task.run_task_by_order_no_count(self.item_no)
            self.task.run_task_by_order_no_count(self.item_no_x)
        for i in range(4):
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
            self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])

        print("=================大小单接收到WithholdFinishNotify消息后需要执行withholdFinishNotify==================")
        dcs_run_task_by_order_no(order_no, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行accountRepayLand落地account_repay表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行assetRepayDetailSave落地asset_repay_detail表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})

        # 2023-04-14海外清分流程停止：final_master、final_tran不再写入数据、clearing_tran只落地展期的数据
        # print("===============开始大单还款清分、结算  ===已取消，线上不再清分=================")
        # repay_run = DcsRunXxlJob(self.item_no, self.channel)
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no)
        # repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")
        # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        # check_dcs_clearing_tran(self.item_no, self.channel, biz_type="repay", status="success")
        # print("===============开始小单还款清分、结算 ===已取消，线上不再清分=================")
        # repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no_x)
        # repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")
        # # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        # check_dcs_clearing_tran(self.item_no_x, "noloan", biz_type="repay", status="success")

    @pytest.mark.global_dcs_thailand
    def test_loan_and_noloan_coupon_repay(self, case):
        # withhold_channel = "coupon" 优惠券 - 20221028 test通过
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        check_dcs_asset_data(self.item_no, self.item_no_x)
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        # KV:dcs_channel_config中写死配置account_channel对应的放款出户为 v_pico_principal_gbpay
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        # 正常还款清分
        # 1.发起主动代扣
        # 手动修改rbiz还款状态为success
        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount,
                                                          project_num_no_loan_amount)
        order_list = [project["order_no"] for project in resp_combo_active["content"]["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order,  project_num_loan_channel_amount+project_num_no_loan_amount, 2,  channel_name="tolerance_payoff")
        self.mock.update_withhold_query_success(self.item_no, 2, "coupon")
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        for i in range(3):
            self.msg.run_msg_by_id_and_search_by_order_no(order_no)
            self.task.run_task_by_order_no_count(self.item_no)
            self.task.run_task_by_order_no_count(self.item_no_x)
        for i in range(4):
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
            self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])

        print("=================大小单接收到WithholdFinishNotify消息后需要执行withholdFinishNotify==================")
        dcs_run_task_by_order_no(order_no, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行accountRepayLand落地account_repay表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行assetRepayDetailSave落地asset_repay_detail表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})

        # 2023-04-14海外清分流程停止：final_master、final_tran不再写入数据、clearing_tran只落地展期的数据
        # print("===============开始大单还款清分、结算=================")
        # repay_run = DcsRunXxlJob(self.item_no, self.channel)
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no)
        # repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")
        # # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        # check_dcs_clearing_tran(self.item_no, self.channel, biz_type="repay", status="success")
        # print("===============开始小单还款清分、结算=================")
        # repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no_x)
        # repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")
        # # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        # check_dcs_clearing_tran(self.item_no_x, "noloan", biz_type="repay", status="success")

    @pytest.mark.global_dcs_thailand
    def test_loan_and_noloan_compensate_then_tolerance_payoff(self, case):
        """
        先代偿再还款  -  tolerance_payoff - 20221028 test通过
        """
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        check_dcs_asset_data(self.item_no, self.item_no_x)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        # 手动修改rbiz还款时间
        self.update_asset_due_at(-8)
        # 刷新罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_no_x)

        # 开始大单代偿清分（小单不需要代偿）、大单代偿结算
        compensate_run = DcsRunXxlJob(self.item_no, self.channel)
        compensate_run.run_clearing_jobs_post("biz_dcs_CompensateCleanFinalJob")

        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount,
                                                          project_num_no_loan_amount)
        order_list = [project["order_no"] for project in resp_combo_active["content"]["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order,  project_num_loan_channel_amount+project_num_no_loan_amount, 2,  channel_name="tolerance_payoff")
        self.mock.update_withhold_query_success(self.item_no, 2, "tolerance_payoff")
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        for i in range(3):
            self.msg.run_msg_by_id_and_search_by_order_no(order_no)
            self.task.run_task_by_order_no_count(self.item_no)
            self.task.run_task_by_order_no_count(self.item_no_x)
        for i in range(4):
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
            self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])

        print("=================大小单接收到WithholdFinishNotify消息后需要执行withholdFinishNotify==================")
        dcs_run_task_by_order_no(order_no, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行accountRepayLand落地account_repay表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行assetRepayDetailSave落地asset_repay_detail表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})

        #
        # print("===============开始大单还款清分、结算=================")
        # repay_run = DcsRunXxlJob(self.item_no, self.channel)
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no)
        # repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")
        # print("===============开始小单还款清分、结算=================")
        # repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no_x)
        # repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")
        #
        # # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        # check_dcs_clearing_tran(self.item_no, self.channel, biz_type="repay", status="success")
        # check_dcs_clearing_tran(self.item_no_x, "noloan", biz_type="repay", status="success")
        #
        # print("===============开始大单代偿-结算=================")
        # repay_run = DcsRunXxlJob(self.item_no, self.channel)
        # update_clearing_tran_create_at(self.item_no)
        # repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")

    @pytest.mark.global_dcs_thailand
    def test_loan_and_noloan_compensate_then_coupon_repay(self, case):
        """
        先代偿再还款  - coupon - 20221028 test通过
        """
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        check_dcs_asset_data(self.item_no, self.item_no_x)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        # 手动修改rbiz还款时间
        self.update_asset_due_at(-8)
        # 刷新罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_no_x)

        # 开始大单代偿清分（小单不需要代偿）、大单代偿结算
        compensate_run = DcsRunXxlJob(self.item_no, self.channel)
        compensate_run.run_clearing_jobs_post("biz_dcs_CompensateCleanFinalJob")

        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount,
                                                          project_num_no_loan_amount)
        self.mock.update_withhold_query_success(self.item_no, 2, "coupon")
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        for i in range(3):
            self.msg.run_msg_by_id_and_search_by_order_no(order_no)
            self.task.run_task_by_order_no_count(self.item_no)
            self.task.run_task_by_order_no_count(self.item_no_x)
        for i in range(4):
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
            self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])

        print("=================大小单接收到AccountChangeNotify消息后需要执行accountRepayLand落地account_repay表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})

        print("===============开始大单还款清分、结算=================")
        repay_run = DcsRunXxlJob(self.item_no, self.channel)
        repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        update_clearing_tran_create_at(self.item_no)
        repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")
        print("===============开始小单还款清分、结算=================")
        repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        update_clearing_tran_create_at(self.item_no_x)
        repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")

        # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        check_dcs_clearing_tran(self.item_no, self.channel, biz_type="repay", status="success")
        check_dcs_clearing_tran(self.item_no_x, "noloan", biz_type="repay", status="success")

        print("===============开始大单代偿-结算=================")
        repay_run = DcsRunXxlJob(self.item_no, self.channel)
        update_clearing_tran_create_at(self.item_no)
        repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")

    @pytest.mark.global_dcs_thailand
    def test_picocapital_plus_advance_repay(self, case):
        # 大小单放款、提前还款后清分、结算  -  20220927test通过
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        check_dcs_asset_data(self.item_no, self.item_no_x)
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        # KV:dcs_channel_config中写死配置account_channel对应的放款出户为 v_pico_principal_gbpay
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        # 正常还款清分
        # 1.发起主动代扣
        # 手动修改rbiz还款状态为success
        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount,
                                                          project_num_no_loan_amount)
        order_list = [project["order_no"] for project in resp_combo_active["content"]["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order,  project_num_loan_channel_amount+project_num_no_loan_amount, 2,  channel_name="tolerance_payoff")
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel")
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        for i in range(3):
            self.msg.run_msg_by_id_and_search_by_order_no(order_no)
            self.task.run_task_by_order_no_count(self.item_no)
            self.task.run_task_by_order_no_count(self.item_no_x)
        for i in range(4):
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
            self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])

        print("=================大小单接收到WithholdFinishNotify消息后需要执行withholdFinishNotify==================")
        dcs_run_task_by_order_no(order_no, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行accountRepayLand落地account_repay表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行assetRepayDetailSave落地asset_repay_detail表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})

        # print("===============开始大单还款清分、结算=================")
        # repay_run = DcsRunXxlJob(self.item_no, self.channel)
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no)
        # repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob")
        # # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        # check_dcs_clearing_tran(self.item_no, self.channel, biz_type="repay", status="success")
        # check_dcs_settlement(self.item_no, self.channel, st_status=2, tf_status='success')
        # print("===============开始小单还款清分、结算=================")
        # repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no_x)
        # repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob")
        # # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        # check_dcs_clearing_tran(self.item_no_x, "noloan", biz_type="repay", status="success")
        # check_dcs_settlement(self.item_no_x, "noloan", st_status=2, tf_status='success')

    @pytest.mark.global_dcs_thailand
    def test_picocapital_plus_compensate_then_repay(self, case):
        """
        先代偿再还款  -  20220927test通过
        """
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        check_dcs_asset_data(self.item_no, self.item_no_x)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        # 手动修改rbiz还款时间
        self.update_asset_due_at(-8)
        # 刷新罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_no_x)

        # 开始大单代偿清分（小单不需要代偿）、大单代偿结算
        compensate_run = DcsRunXxlJob(self.item_no, self.channel)
        compensate_run.run_clearing_jobs_post("biz_dcs_CompensateCleanFinalJob")

        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount,
                                                          project_num_no_loan_amount)
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel")
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        for i in range(3):
            self.msg.run_msg_by_id_and_search_by_order_no(order_no)
            self.task.run_task_by_order_no_count(self.item_no)
            self.task.run_task_by_order_no_count(self.item_no_x)
        for i in range(4):
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
            self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
            self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])

        print("=================大小单接收到AccountChangeNotify消息后需要执行accountRepayLand落地account_repay表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})


        print("===============开始大单还款清分、结算=================")
        repay_run = DcsRunXxlJob(self.item_no, self.channel)
        repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        update_clearing_tran_create_at(self.item_no)
        repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob")
        print("===============开始小单还款清分、结算=================")
        repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        update_clearing_tran_create_at(self.item_no_x)
        repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob")

        # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        check_dcs_clearing_tran(self.item_no, self.channel, biz_type="repay", status="success")
        check_dcs_settlement(self.item_no, self.channel, st_status=2, tf_status='success')
        check_dcs_clearing_tran(self.item_no_x, "noloan", biz_type="repay", status="success")
        check_dcs_settlement(self.item_no_x, "noloan", st_status=2, tf_status='success')

        print("===============开始大单代偿-结算=================")
        repay_run = DcsRunXxlJob(self.item_no, self.channel)
        update_clearing_tran_create_at(self.item_no)
        repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")
        # 代偿结算结果检查--》代偿不会记录结算表，因为大单不能批量转账，是在结算时才决定出入户的
        check_dcs_clearing_tran(self.item_no, self.channel, biz_type="compensate", status="success")


    @pytest.mark.global_dcs_thailand
    def test_picocapital_plus_part_repay(self, case):
        """
         部分还款清分，大单会触发自动代偿，小单不会触发自动代偿 -  20220927test通过
        """
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        check_dcs_asset_data(self.item_no, self.item_no_x)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        # 正常还款清分
        # 1.发起主动代扣
        # 手动修改rbiz还款状态为success
        self.mock.update_withhold_autopay_ebank_url_success()
        self.update_asset_due_at(-8)
        # 刷新罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_no_x)

        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调返回金额为部分还款金额-》小单全额+大单的部分金额
        # resp, _ = paysvr_callback(order_no, int(project_num_no_loan_amount)+10000, 2, "auto_thailand_channel")

        order_list = [project["order_no"] for project in resp_combo_active["content"]["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order,  int(project_num_no_loan_amount)+10000, 2,  channel_name="auto_thailand_channel")
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel")

        self.run_all_task_after_repay_success()
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])

        print("=================大小单接收到WithholdFinishNotify消息后需要执行withholdFinishNotify==================")
        dcs_run_task_by_order_no(order_no, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行accountRepayLand落地account_repay表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})
        print("=================大小单接收到AccountChangeNotify消息后需要执行assetRepayDetailSave落地asset_repay_detail表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})

        # print("===============开始大单还款清分、结算=================")
        # repay_run = DcsRunXxlJob(self.item_no, self.channel)
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no)
        # repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob")
        # print("===============开始小单还款清分、结算=================")
        # repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        # repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        # update_clearing_tran_create_at(self.item_no_x)
        # repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob")
        #
        # #开始大单代偿-结算
        # repay_run = DcsRunXxlJob(self.item_no, self.channel)
        # update_clearing_tran_create_at(self.item_no)
        # repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")
        #
        # # 检查account_repay、final_master、final_tran、clearing_tran、settlement、account_transfer  表
        # check_dcs_clearing_tran(self.item_no, self.channel, biz_type="repay", status="success")
        # check_dcs_settlement(self.item_no, self.channel, st_status=2, tf_status='success')
        # check_dcs_clearing_tran(self.item_no_x, "noloan", biz_type="repay", status="success")
        # check_dcs_settlement(self.item_no_x, "noloan", st_status=2, tf_status='success')

    @pytest.mark.global_dcs_thailand
    def test_picocapital_plus_refund(self, case):
        """
         重复代扣退款发消息给dcs，归集时需要减去对应的钱
        """
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        check_dcs_asset_data(self.item_no, self.item_no_x)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        """
        准备重复代扣的数据，2笔金额一样的
        """
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(asset_tran_amount) + int(asset_tran_amount_no_loan)
        # 发起第一次主动还款
        resp_combo_active = self.combo_active_repay_apply(asset_tran_amount, asset_tran_amount_no_loan)
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        # 回调失败
        paysvr_callback(merchant_key, withhold_amount, 3)
        self.task.run_task_by_order_no_count(self.item_no)
        self.task.run_task_by_order_no_count(merchant_key, 3)
        # 发起第二次主动还款
        resp_combo_active_new = self.combo_active_repay_apply(asset_tran_amount, asset_tran_amount_no_loan)
        merchant_key_new = resp_combo_active_new['content']["data"]["project_list"][0]["order_no"]
        # 回调失败
        paysvr_callback(merchant_key_new, withhold_amount, 3)

        # 两笔金额一样且代扣失败的数据已准备好，  然后 回调成功 第2笔
        paysvr_callback(merchant_key_new, withhold_amount, 2)
        self.task.run_task_by_order_no_count(self.item_no)
        self.task.run_task_by_order_no_count(merchant_key_new, 3)
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        # dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        # dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})
        # 开始大小单还款清分
        repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        repay_run = DcsRunXxlJob(self.item_no, self.channel)
        repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")

        # 再回调成功 第1笔
        paysvr_callback(merchant_key, withhold_amount, 2, "auto_thailand_channel")
        request_no_new = get_withhold_by_serial_no(merchant_key)[0]["withhold_request_no"]
        # 执行所有task
        self.task.run_task_by_order_no_count(request_no_new)
        self.task.run_task_by_order_no_count(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        # 注意第二次还款不会通知给dcs了，所以不用执行task
        print(f"###---准备重复代扣数据结束----资产编号：{self.item_no}，扣款流水1；{merchant_key_new}，扣款流水2：{merchant_key}---#####")

        # 通知dcs第1笔已退款成功（type= rollback-原路退款），直接mock消息
        #test_channel_withhold在clearing_config中配置的归集户是v_pico_hk_gbpay
        refund_result_success_to_dcs(withhold_amount, "refund1_" + merchant_key, merchant_key, 'rollback', "test_channel_withhold")
        time.sleep(2)
        repay_run.run_clearing_jobs_post("dbTaskJob")
        check_dcs_refund_result("refund1_" + merchant_key, merchant_key, withhold_amount, 'v_pico_hk_gbpay', 'success')
        # repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        # repay_run.run_clearing_jobs_post("dbTaskJob")

        # 通知dcs第2笔已退款成功（type=withdraw-代付退款），直接mock消息
        #test_channel_withdraw在grant_config中配置的归集户是v_pico_qr_hk_gbpay
        refund_result_success_to_dcs(withhold_amount, "refund2_" + merchant_key_new, merchant_key_new, 'withdraw', "test_channel_withdraw")
        check_dcs_refund_result("refund2_" + merchant_key_new, merchant_key_new, withhold_amount, 'v_pico_planet_hk_gbpay', 'new')

        # 开始归集
        repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        repay_run.run_clearing_jobs_post("biz_dcs_SplitWithholdJob")
        time.sleep(2)
        repay_run.run_clearing_jobs_post("dbTaskJob")
        time.sleep(2)
        repay_run.run_clearing_jobs_post("dbTaskJob")
        time.sleep(2)
        repay_run.run_clearing_jobs_post("biz_dcs_CollectingJob")
        time.sleep(2)
        repay_run.run_clearing_jobs_post("dbTaskJob")

    @pytest.mark.global_dcs_thailand
    def test_picocapital_plus_collect(self, case):
        """
         正常还款后归集
        """
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        check_dcs_asset_data(self.item_no, self.item_no_x)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        # 正常还款清分
        # 1.发起主动代扣
        # 手动修改rbiz还款状态为success
        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount,
                                                          project_num_no_loan_amount)
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel")
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)

        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])

        # 开始归集
        repay_run = DcsRunXxlJob(self.item_no, "loan")
        repay_run.run_clearing_jobs_post("biz_dcs_SplitWithholdJob")
        time.sleep(2)
        repay_run.run_clearing_jobs_post("biz_dcs_CollectingJob")
        time.sleep(2)
        # 开始扣除成本
        repay_run.run_clearing_jobs_post("biz_dcs_WithholdCostJob", serial_no=order_no)
        # TODO 归集&成本数据检查  withhold、pre_collect、collect、withhold_cost



    @pytest.mark.global_dcs_thailand
    def test_picocapital_plus_rbiz_refund(self, case):
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        check_dcs_asset_data(self.item_no, self.item_no_x)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay") # KV:dcs_channel_config中写死配置account_channel对应的放款出户为 v_pico_principal_gbpay
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")


        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        refund_sn = resp["content"]["data"]["refund_no"]
        check_refund_request(refund_sn, refund_request_status="ready", refund_request_channel="skypay_test_withdraw")
        # check_dcs_refund_result(refund_sn, merchant_key=,withhold_amount=,status="ready", channel="auto_thailand_channel")

        # 退款请求paysvr
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 2)
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refunding", fang="skypay_test_withdraw")
        check_dcs_refund_result(refund_sn, refund_result_status="process", refund_result_channel="refund_apply_channel",
                            refund_result_finish_at="1000-01-01")
        # 查询退款结果
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refund_success", refund_request_channel="skypay_test_withdraw")
        check_dcs_refund_result(refund_sn, refund_result_status="success", refund_result_channel="refund_query_channel")


    @pytest.mark.global_dcs_thailand
    def test_pico_part_repay_then_compensate(self, case):
        """
         部分还款清分，大单会触发自动代偿，小单不会触发自动代偿
        """
        self.item_no, asset_info = asset_import_and_auto_loan(self.channel, 7, "tha", "mango", "game_bill",
                                                              self.four_element)
        self.item_no_x = asset_import_and_auto_noloan(asset_info)
        check_dcs_asset_data(self.item_no, self.item_no_x)
        print("=================放款成功检查dcs.asset_withdraw、asset、asste_tran表数据==================")
        # 大单放款成功进行记账
        account_info = get_account_balance_available("v_pico_principal_gbpay")
        balance_available = account_info[0]["balance_available"]  # 初始余额
        # 执行grantAccountBalanceManagement
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        check_dcs_account_log(self.item_no, balance_available)
        print("=================放款成功检查记账信息(需要自循环的资方)==================")
        task_capital_asset_sync = get_task_capital_asset_sync(self.item_no)
        dcs_run_task_by_order_no(task_capital_asset_sync[0]["task_order_no"],
                                 except_json={"code": 0, "message": "处理成功"})
        check_dcs_asset_and_tran(self.item_no)
        print("=================接收资方还款计划（目前只是保存数据没有用）==================")

        # 正常还款清分
        # 1.发起主动代扣
        # 手动修改rbiz还款状态为success
        self.mock.update_withhold_autopay_ebank_url_success()
        self.update_asset_due_at(0)
        # 刷新罚息
        # self.refresh_late_fee(self.item_no)
        # self.refresh_late_fee(self.item_no_x)

        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调返回金额为部分还款金额-》小单全额+大单利息(让大单只还罚息500+利息3500)
        resp, _=paysvr_callback(order_no, int(project_num_no_loan_amount)+3500, is_success=2, channel_name="auto_thailand_channel",
                    finished_at="2022-09-19 00:00:00")
        self.run_all_task_after_repay_success()
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no_x)
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])

        print("=================大小单接收到AccountChangeNotify消息后需要执行accountRepayLand落地account_repay表==================")
        dcs_run_task_by_order_no(self.item_no, except_json={"code": 0, "message": "处理成功"})
        dcs_run_task_by_order_no(self.item_no_x, except_json={"code": 0, "message": "处理成功"})

        print("===============开始大单还款清分、结算=================")
        repay_run = DcsRunXxlJob(self.item_no, self.channel)
        repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        update_clearing_tran_create_at(self.item_no)
        repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob")
        print("===============开始小单还款清分、结算=================")
        repay_run = DcsRunXxlJob(self.item_no_x, "noloan")
        repay_run.run_clearing_jobs_post("biz_dcs_RepayToFinalJob")
        update_clearing_tran_create_at(self.item_no_x)
        repay_run.run_clearing_jobs_post("biz_dcs_AutoSettlementJob")
        print("===============开始大单代偿-结算=================")
        repay_run = DcsRunXxlJob(self.item_no, self.channel)
        update_clearing_tran_create_at(self.item_no)
        repay_run.run_clearing_jobs_post("biz_dcs_CompensateSettlementJob")

    def test_query_tolerance_by_repay_period_principal(self, setup_4):
        update_rbiz_config(tolerance_type="repay_period_principal")
        resp_combo_active = self.combo_active_repay_apply(0, 0, period_list=[1, 2])
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(merchant_key)[0]["withhold_request_req_key"]
        withhold_cancel(request_key, "")
        # 未还款检查
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 27500,  # (1250+1250+125+125)*0.1
                                           "allow_max_repayment_amount": 283000,
                                           "overdue_days": -7,
                                           "tolerance_amount": 254500,  # 282000-27500
                                           "allow_repayment": True}},
                                 resp["content"])
        # 部分还款检查
        self.make_smart_repay_party(self.item_no, 12121)
        self.make_smart_repay_party(self.item_no_x, 1212)
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 26517,  # (1163.79+1250+112.88+125)*0.1
                                           "allow_max_repayment_amount": 269667,  # 2820-121.21-12.12+10
                                           "overdue_days": -7,
                                           "tolerance_amount": 242150,  # (2820-121.21-12.12)-127.67
                                           "allow_repayment": True}},
                                 resp["content"])

# TODO 增加展期用例