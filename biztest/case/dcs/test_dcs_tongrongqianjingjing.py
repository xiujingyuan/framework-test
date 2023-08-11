import pytest, time
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import compensate_handle_tasks, repay_tasks
from biztest.function.dcs.biz_database import get_repay_amount_rbiz, get_capital_biz
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.interface.rbiz.biz_central_interface import run_type_task_biz_central
from biztest.interface.rbiz.rbiz_interface import paysvr_callback, monitor_check
from biztest.util.tools.tools import get_four_element, get_item_no
import common.global_const as gc


class TestDcsTongRongQianJingJing(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT

    @pytest.mark.DCS_test_0629
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_tongrong
    def test_tongrongqianjingjing(self):
        monitor_check()
        self.init(self.env_test)
        channel = "tongrongqianjingjing"
        item_no = 'ck_trqjj_' + get_item_no()[:16]
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(channel, self.four_element, item_no,
                                                                               count=6, script_system='dcs')

        # 检查小单放款是否成功，否则还款和清分会失败
        check_asset_grant(self.item_no)
        print("=================第一期代偿=================")
        compensate_period = (1,)
        # 到期日往前推一个月，再往前推一天
        self.change_asset_due_at(-1, -1)
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, compensate_period)
        # 检查代偿清分的数据
        capital = get_capital_biz(self.item_no, compensate_period[0])
        cleck_final = CheckDcsFinal(self.item_no, compensate_period[0], 'compensate', 'qsq')
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, compensate_period[0], 'compensate', 'qsq')
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()

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
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, channel, "repay")
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
