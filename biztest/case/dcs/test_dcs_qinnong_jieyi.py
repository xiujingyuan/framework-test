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
    run_dcs_task_by_order_no
from biztest.interface.rbiz.rbiz_interface import asset_provision_settle, asset_bill_decrease, \
    combo_active_repay_without_no_loan, paysvr_callback, monitor_check
from biztest.util.easymock.rbiz.qinnong import RepayQinnongMock
from biztest.util.tools.tools import get_item_no, get_four_element, get_date_after
import common.global_const as gc


class TestDcsQinNongJieyi(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "qinnong_jieyi"  # qinnong , qinnong_jieyi
    period_count = 6
    source_type = 'irr36_quanyi'  # irr36_quanyi(这个关联到小单合并还款会有问题) , apr36 , irr36
    principal = 800000
    interest = 5200
    period_one_amount = 16495

    @classmethod
    def setup_class(cls):
        cls.qn_mock = RepayQinnongMock(rbiz_mock)
        set_up_the_asset_trans_for_compensate()

    def setup_method(self):
        monitor_check()
        self.init(self.env_test)
        self.item_no = 'qn_' + get_item_no()
        self.four_element = get_four_element()
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.channel, self.four_element,
                                                                               self.item_no, count=self.period_count, script_system='dcs')

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong
    def test_qinnong_qsq_advance_repay(self):
        print("====================第一期提前还款====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_advance = (1,)
        # step 1 到期日往前推10天
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
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
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_advance)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_advance[0])
        check_final = CheckDcsFinal(self.item_no, period_advance[0], 'repay', "qsq")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_advance[0], 'repay', "qsq")
        check_trans.check_trans_all()
        check_trans.check_trans_amount()
        print("=================清分完成后，秦农提前还款，收取第一期利息，到期日结算==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_advance[0], period_advance[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_advance[0], period_advance[0], "advance", "qsq", "N", "",
                                                    expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_advance[0], period_advance[0], "repay", "")

    @pytest.mark.DCS_test_auto_test_demo
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong
    def test_qinnong_qsq_normal_repay(self):
        print("====================第一期正常还款====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_normal)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        check_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        check_trans.check_trans_all()
        check_trans.check_trans_amount()
        print("=================清分完成后，我方代扣正常还款算作代偿，收取第一期利息==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "compensate", "qsq", "N", "",
                                                    expect_operate_at)
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "")
        # 大单结算
        update_expect_settlement_at_before_one_day(self.item_no)
        settlement_run = RunDcsJobPost(self.item_no, self.channel, "repay", loan_type="BIG")
        settlement_run.run_clearing_jobs_post_settlement(auto_settlement_handle_tasks)



    @pytest.mark.DCS_test_auto_test_demo
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong
    def test_qinnong_qsq_payoff(self):
        print("====================第一期到期日 提前结清====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_payoff = (1, 2, 3, 4, 5, 6)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        self.qn_mock.update_repay_trail(self.principal, self.interest)
        asset_tran_amount["asset_tran_balance_amount"] = self.principal + self.period_one_amount
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_task_after_loan_repay(self.item_no)
        self.run_all_msg_after_repay_success()

        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # check_repay_biz(self.item_num_no_loan)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)
        # 检查清分的数据
        # for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
        #     capital = get_capital_biz(self.item_no, capital_i)
        #     check_final = CheckDcsFinal(self.item_no, capital_i, 'repay', 'qsq')
        #     check_final.check_final_all()
        #     check_final.check_final_amount(capital)
        #     check_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', 'qsq')
        #     check_trans.check_trans_all()
        #     check_trans.check_trans_amount()
        print("=================清分完成后，秦农提前结清，收取第一期利息，还款次日结算==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_payoff[0], period_payoff[0])
        expect_operate_at = repay_plan[0]["asset_tran_finish_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_payoff[0], period_payoff[-1], "early_settlement", "qsq", "N",
                                                    "", "2022-03-28")
        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        # step 4 检查数据
        # for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
        #     check_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq")
        #     check_trans.check_settlement_notify_clearing(period_payoff[0], capital_i, "repay", "")

    @pytest.mark.DCS_test_auto_test_demo
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong
    def test_qinnong_qsq_compensate_repay(self):
        print("================第一期代偿并代偿后还款================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_compensate = (1,)
        # step 1 到期日往前推一个月
        self.change_asset_due_at(-1, -1)

        print("================第一期代偿后还款（制造先还款再代偿的场景）================")
        # time.sleep(2.5)
        # step 2 刷罚息，到期日上面已经修改过了
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        # step 2 刷完罚息需要执行biz的task，不然还款计划不完整
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 3 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_compensate)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_compensate)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 4 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 执行biz的task（这一步也可以不要）
        # run_biz_tasks(self.env_test, "RbizAssetChangeReceive", self.item_no)
        # step 5 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_compensate)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_compensate[0])
        check_final = CheckDcsFinal(self.item_no, period_compensate[0], 'repay', "qsq")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_compensate[0], 'repay', "qsq")
        check_trans.check_trans_all()
        check_trans.check_trans_amount()

        print("================开始大单代偿清分（制造先还款再代偿的场景）================")
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_compensate)
        # 检查代偿清分的数据
        capital = get_capital_biz(self.item_no, period_compensate[0])
        check_final = CheckDcsFinal(self.item_no, period_compensate[0], 'compensate', 'qsq')
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_compensate[0], 'compensate', 'qsq')
        check_trans.check_trans_all()
        check_trans.check_trans_amount()
        print("=================清分完成后，秦农代偿，收取第一期利息==================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_compensate[0], period_compensate[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_compensate[0], period_compensate[0], "compensate", "qsq",
                                                    "N", "", expect_operate_at)
        # step 3 执行task
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        # step 4 检查数据
        check_trans.check_settlement_notify_clearing(period_compensate[0], period_compensate[0], "compensate", "")

    @pytest.mark.DCS_test_auto_test_demo
    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong
    def test_qinnong_provision_repay_normal(self):
        print("====================（第一期拨备结清推正常还款的场景）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)
        # step 2 拨备结清第1期
        asset_provision_settle(self.item_no, 1)
        # step 3 执行还款的task和msg
        self.run_task_after_loan_repay(self.item_no)
        self.run_account_msg_after_repaid()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)
        # 检查清分的数据
        capital = get_capital_biz(self.item_no, period_normal[0])
        check_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        check_final.check_final_all()
        check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        check_trans.check_trans_all()
        check_trans.check_trans_amount()

        print("================清分完成后，秦农补充流程，我方代扣正常还款需要推线下还款=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "normal", "qsq", "N", "",
                                                    expect_operate_at)

        # step 3 执行task
        run_dcs_task_by_count(self.item_no, 3)
        check_trans.check_settlement_notify_clearing(period_normal[0], period_normal[0], "repay", "guarantee")

    @pytest.mark.DCS_test_qinnong
    def test_qinnong_decrease_repay_normal(self):
        print("====================（第一期减免部分费用 本金未还完 用户第2次还完 推还款的场景）====================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_normal = (1,)
        # step 1 到期日往前推1月
        self.change_asset_due_at(-1, 0)

        # step 2 手动充值700元，还款
        asset_bill_decrease(self.item_no, 850332)
        # step 3 执行还款的msg
        self.run_task_after_loan_repay(self.item_no)
        self.run_account_msg_after_repaid()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)

        # 还款-还剩余部分
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_normal)
        self.four_element = get_four_params_rbiz_db(self.item_no)
        params_combo_active = {
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"],
            "project_num_loan_channel": self.item_no,
            "project_num_loan_channel_priority": 1,
            "project_num_loan_channel_amount": asset_tran_amount["asset_tran_balance_amount"]
        }
        combo_active_repay_without_no_loan(**params_combo_active)
        # step 4 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        repay_run = RunDcsJobPost(self.item_no, self.channel, "repay")
        repay_run.run_clearing_jobs_post(repay_tasks, period_normal)

        # 检查清分的数据
        check_final = CheckDcsFinal(self.item_no, period_normal[0], 'repay', "qsq")
        check_final.check_final_all()
        # check_final.check_final_amount(capital)
        check_trans = CheckDcsTrans(self.item_no, period_normal[0], 'repay', "qsq")
        check_trans.check_trans_all()
        # check_trans.check_trans_amount()
        print("================清分完成后，秦农补充流程，我方代扣正常还款需要推线下还款=================")
        # step 1 查找预计结算时间
        repay_plan = get_one_repay_plan(self.item_no, 'repayprincipal', period_normal[0], period_normal[0])
        expect_operate_at = repay_plan[0]["asset_tran_due_at"][:10]
        # step 2 模拟biz_central调用接口
        advanced_clearing = BizInterfaceDcs(self.item_no, self.channel, self.period_count, self.env_test)
        advanced_clearing.capital_settlement_notify(period_normal[0], period_normal[0], "advance", "qsq", "N", "",
                                                    expect_operate_at)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong
    def test_noloan_advance_repay(self):
        print("====================（先领取权益，再还款的场景，目前只有lieyin需要领取权益）====================")
        check_asset_grant(self.item_no)

        period_repay = (1,)
        self.change_asset_due_at(0, -10)
        update_asset_extend_ref_and_sub_order_type("lieyin", "",
                                                   self.item_num_no_loan)  # 放款成功后根据需要更新ref_and_sub_order_type
        wait_dcs_record_appear(
            "select * from clean_task where task_order_no='%s' and task_type='accrualAllocated'" % self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)
        scenes_receive(self.item_num_no_loan, "lieyin")
        run_dcs_task_until_disappear(self.item_num_no_loan)
        # 还款
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_repay)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_repay)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        set_withhold_history(self.item_num_no_loan)

        run_dcs_task_until_disappear(self.item_num_no_loan)
        check_clean_accrual_tran(self.item_num_no_loan)
        check_clean_precharge_clearing_tran(self.item_num_no_loan)

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong
    def test_noloan_compensate_without_scenes_receive(self):
        print("====================（先代偿 领取权益 再还款的场景 还款之后不会代偿场景方）====================")
        check_asset_grant(self.item_no)
        update_asset_extend_ref_and_sub_order_type("lieyin", "", self.item_num_no_loan)

        # 开始大单代偿清分
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)

        # 权责分配
        wait_dcs_record_appear(
            "select * from clean_task where task_order_no='%s' and task_type='accrualAllocated'" % self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)
        period_compensate = (1,)
        compensate_run = RunDcsJobPost(self.item_num_no_loan, "noloan", "compensate")
        # 代偿
        compensate_run.run_clearing_jobs_post_compensate(noloan_compensate_handle_tasks, period_compensate)
        # 逾期之后领取权益
        scenes_receive(self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)
        # 还款

        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_compensate)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_compensate)
        resp_repay = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        order_list = [project["order_no"] for project in resp_repay["data"]["project_list"]]
        for order in order_list:
            paysvr_callback(order, 2)
        self.run_task_after_withhold_callback(order_list)
        # step 3 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()

        set_withhold_history(self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)

        check_clean_accrual_tran(self.item_num_no_loan)
        # 检查clean_precharge_clearing_tran 不代偿给场景方
        check_compensate_clean_precharge_clearing_tran(self.item_num_no_loan, **{"is_compensate_scenes": "N"})
        # 权益领取逾期了
        check_clean_scenes_receive(self.item_num_no_loan, status='overdue', scenes='lieyin')
        # 作废权益
        compensate_run.run_clearing_jobs_post_compensate(not_received_handle_tasks, period_compensate)
        run_dcs_task_by_count(self.item_num_no_loan, 3)
        # 检查点：场景方的明细cancel，入拨备的这条没验证
        check_compensate_clean_precharge_clearing_tran(self.item_num_no_loan, **{"is_compensate_scenes": "cancel"})

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong
    def test_noloan_compensate_with_scenes_receive(self):
        print("====================（先领取权益 再代偿的场景 分润给场景方）====================")
        check_asset_grant(self.item_no)
        update_asset_extend_ref_and_sub_order_type("lieyin", "",
                                                   self.item_num_no_loan)  # 放款成功后根据需要更新ref_and_sub_order_type

        # 权责分配
        wait_dcs_record_appear(
            "select * from clean_task where task_order_no='%s' and task_type='accrualAllocated'" % self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)

        scenes_receive(self.item_num_no_loan)
        # 领取权益
        wait_dcs_record_appear(
            "select * from clean_task where task_order_no='%s' and task_type='scenesReceiveSave'" % self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)

        # 开始小单代偿清分
        self.change_asset_due_at(-1, -1)
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        run_dcs_task_by_count(self.item_num_no_loan, 1)
        period_compensate = (1,)
        compensate_run = RunDcsJobPost(self.item_num_no_loan, "noloan", "compensate")
        compensate_run.run_clearing_jobs_post_compensate(noloan_compensate_handle_tasks, period_compensate)
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
        check_compensate_clean_precharge_clearing_tran(self.item_num_no_loan)
        check_repay_after_compensate_precharge_clearing_tran(self.item_num_no_loan)
        # 结算
        update_expect_settlement_at_before_one_day(self.item_num_no_loan)
        compensate_run.run_clearing_jobs_post_settlement(auto_settlement_handle_tasks)
        # 只有代偿后还款的明细会自动结算
        check_repay_after_compensate_precharge_clearing_tran(self.item_num_no_loan, **{"exp_status": "finished"})

    @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_qinnong
    def test_noloan_partrepay(self):
        print("====================（先领取权益，再部分还款触发代偿的场景，目前只有lieyin需要领取权益）====================")
        check_asset_grant(self.item_no)

        self.change_asset_due_at(0, -1)
        period_payoff = (1, 2, 3, 4, 5, 6)
        update_asset_extend_ref_and_sub_order_type("lieyin", "",
                                                   self.item_num_no_loan)  # 放款成功后根据需要更新ref_and_sub_order_type
        run_dcs_task_until_disappear(self.item_num_no_loan)
        scenes_receive(self.item_num_no_loan, "lieyin")
        run_dcs_task_until_disappear(self.item_num_no_loan)
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
        asset_tran_amount_no_loan = get_repay_amount_rbiz(self.item_num_no_loan, period_payoff)
        # 拨备结清以实现部分还款
        asset_bill_decrease(self.item_num_no_loan, int(asset_tran_amount_no_loan["asset_tran_balance_amount"]) + int(
            asset_tran_amount["asset_tran_balance_amount"]) - 47932)  # 注意1000是需要拨备结清的钱，而且期次是还到最后一期的，不是第一期
        self.run_task_after_loan_repay(self.item_num_no_loan)
        self.run_account_msg_after_repaid()
        set_withhold_history(self.item_num_no_loan)
        run_dcs_task_until_disappear(self.item_num_no_loan)
        # 数据没有检查
