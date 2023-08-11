import pytest, time
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import compensate_handle_tasks, repay_tasks, noloan_compensate_handle_tasks, \
    auto_settlement_handle_tasks
from biztest.function.biz.biz_db_function import set_withhold_history
from biztest.function.dcs.biz_database import get_repay_amount_rbiz, get_capital_biz, get_one_repay_plan, \
    update_asset_extend_ref_and_sub_order_type, set_up_the_asset_trans_for_compensate
from biztest.function.dcs.capital_database import update_expect_settlement_at_before_one_day
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.check_precharge import check_compensate_clean_precharge_clearing_tran, \
    check_repay_after_compensate_precharge_clearing_tran, check_clean_accrual_tran
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz, get_four_params_rbiz_db
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_db_function import get_asset_tran_balance_amount_by_item_no_and_period
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count
from biztest.interface.rbiz.biz_central_interface import run_type_task_biz_central
from biztest.interface.rbiz.rbiz_interface import asset_bill_decrease, paysvr_callback, monitor_check
from biztest.util.tools.tools import get_four_element, get_item_no
import common.global_const as gc


class TestDcsTongrongbiaonei(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "tongrongbiaonei"
    period_count = 12

    def setup_method(self):
        monitor_check()
        set_up_the_asset_trans_for_compensate()
        self.init(self.env_test)
        self.item_no = 'trbn_' + get_item_no()
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, count=self.period_count,
                                                                               script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_tongrongbiaonei
    def test_tongrongbiaonei(self):
        # 检查小单放款是否成功，否则还款和清分会失败
        check_asset_grant(self.item_no)
        print("=================第一期代偿=================")
        compensate_period = (1,)
        # 到期日往前推一个月，再往前推一天
        self.change_asset_due_at(-1, -1)
        # 开始大单代偿清分
        # time.sleep(2.5)
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, compensate_period)
        # 检查代偿清分的数据
        capital = get_capital_biz(self.item_no, compensate_period[0])
        check_final = CheckDcsFinal(self.item_no, compensate_period[0], 'compensate', 'qsq')
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, compensate_period[0], 'compensate', 'qsq')
        check_trans.check_trans_all()
        check_trans.check_trans_amount()

        print("=================第一期逾期还款+第二期提前还款=================")
        repay_period = (1, 2)
        # step 2 刷罚息，第一期到期日上面已经修改过了

        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        # step 2 刷完罚息需要执行biz的task，不然还款计划不完整
        run_type_task_biz_central("AssetChange", self.item_no)
        # step 3 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, repay_period)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, repay_period)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 4 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        # step 5 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, repay_period)
        # 检查清分的数据
        for capital_i in range(repay_period[0], repay_period[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq")
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq")
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
