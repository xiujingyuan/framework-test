import time, pytest
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import rbiz_mock
from biztest.function.biz.biz_db_function import set_withhold_history
from biztest.function.dcs.capital_database import update_expect_settlement_at_before_one_day
from biztest.function.dcs.check_precharge import check_compensate_clean_precharge_clearing_tran, \
    check_clean_precharge_clearing_tran, check_clean_accrual_tran, check_clean_scenes_receive, \
    check_repay_after_compensate_precharge_clearing_tran
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz, get_four_params_rbiz_db, \
    wait_dcs_record_appear, run_dcs_task_until_disappear
from biztest.config.dcs.xxljob_config import capital_settlement_tasks, compensate_handle_tasks, repay_tasks, \
    noloan_compensate_handle_tasks, auto_settlement_handle_tasks, not_received_handle_tasks
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan, get_repay_amount_rbiz, \
    update_asset_extend_ref_and_sub_order_type, set_up_the_asset_trans_for_compensate
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count, scenes_receive, run_task_in_biz_dcs, \
    run_dcs_task_by_order_no, update_deposit_orderandtrade_and_run_task
from biztest.interface.rbiz.rbiz_interface import asset_provision_settle, asset_bill_decrease, \
    combo_active_repay_without_no_loan, paysvr_callback, monitor_check
from biztest.util.easymock.rbiz.qinnong import RepayQinnongMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after
import common.global_const as gc


class TestDcsNoloanClearingAndSettlement(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "qinnong_jieyi"
    period_count = 6
    source_type = 'irr36_quanyi'  # irr36_quanyi(这个关联到小单合并还款会有问题) , apr36 , irr36
    principal = 800000
    interest = 5200
    period_one_amount = 16495

    @classmethod
    def setup_class(cls):
        cls.qn_mock = RepayQinnongMock(rbiz_mock)
        # set_up_the_asset_trans_for_compensate()

    def setup_method(self):
        monitor_check()
        self.init(self.env_test)
        self.item_no = 'qn_' + get_item_no()
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, count=self.period_count, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong_noloan
    def test_noloan_clearing_and_settlement(self):
        print("====================（先领取权益 再还款的场景 分润给场景方）====================")
        check_asset_grant(self.item_no)
        update_asset_extend_ref_and_sub_order_type("lieyin", "", self.item_num_no_loan)  # 放款成功后根据需要更新ref_and_sub_order_type

        # 权责分配
        wait_dcs_record_appear(
            "select * from clean_task where task_order_no='%s' and task_type='accrualAllocated'" % self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)

        scenes_receive(self.item_num_no_loan)
        # 领取权益
        wait_dcs_record_appear(
            "select * from clean_task where task_order_no='%s' and task_type='scenesReceiveSave'" % self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)

        # 开始小单清分
        run_dcs_task_by_count(self.item_num_no_loan, 1)
        period_advance = (1,)
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_advance)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_advance)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        set_withhold_history(self.item_num_no_loan)

        wait_dcs_record_appear(
            "select * from clean_task where task_order_no='%s' and task_type='accountChangeNotifySync'" % self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)
        check_clean_accrual_tran(self.item_num_no_loan)
        # 结算
        update_expect_settlement_at_before_one_day(self.item_num_no_loan)
        settlement_run = RunDcsJobPost(self.item_num_no_loan, "noloan", "repay")
        settlement_run.run_clearing_jobs_post_settlement(auto_settlement_handle_tasks)
