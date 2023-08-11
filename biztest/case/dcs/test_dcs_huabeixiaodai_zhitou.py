import time, pytest
# capital7环境就用 xxljob_config ，capital6环境就用 xxljob_config2 。
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.dcs.xxljob_config import hbxd_advance_clearing_job, buyback_clearing_job, buyback_handle_tasks, \
    capital_settlement_tasks, compensate_handle_tasks, repay_tasks
from biztest.function.dcs.biz_database import get_capital_biz, get_one_repay_plan, insert_buyback, get_repay_amount_rbiz
from biztest.function.dcs.capital_database import get_final_all
from biztest.function.dcs.check_dcs_final import CheckDcsFinal
from biztest.function.dcs.check_dcs_trans import CheckDcsTrans
from biztest.function.dcs.dcs_common import check_asset_grant, check_repay_biz, get_four_params_rbiz_db
from biztest.function.dcs.dcs_grant_asset import AssetImportGrant
from biztest.function.dcs.run_dcs_job_post import RunDcsJobPost
from biztest.interface.rbiz.biz_central_interface import run_type_task_biz_central
from biztest.interface.rbiz.rbiz_interface import refresh_late_fee, combo_active_repay_without_no_loan
from biztest.util.tools.tools import get_item_no
import common.global_const as gc


class TestDcsHuaBeiXiaoDaiZhiTou(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT
    channel = "huabeixiaodai_zhitou"
    period_count = 6

    def setup_method(self):
        self.init(self.env_test)
        self.item_no = 'ha_hbxd_' + get_item_no()[:16]
        self.item_num_no_loan = "noloan_" + self.item_no
        kwargs = {
            "system_type": None,
            "env_test": self.env_test,
            "item_no": self.item_no,
            "item_no_noloan": self.item_num_no_loan,
            "amount": 8000,
            "period_count": 6,
            "old": "Y"
        }
        grant_asset = AssetImportGrant(self.channel, "xiaobaixiong_bill", **kwargs)
        grant_asset.asset_import_biz()
        grant_asset.asset_grant_biz()
        grant_asset.asset_capital_plan_biz()
        grant_asset.asset_grant_noloan()

    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hbxd
    @pytest.mark.DCS_test_buyback
    def test_huabeixiaodai_buyback(self):
        print("====================回购====================")
        buyback_period = (3, 4, 5, 6)
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        # step 1 到期日往前推3月零1天
        self.change_asset_due_at(-3, -1)
        # 查询本金，然后直接往 buyback 表插入数据 （固定设置从第3期开始回购）
        principal_plan = get_one_repay_plan(self.item_no, 'repayprincipal', 1, buyback_period[-1])
        principal_amount = 0
        for ii in range(0, len(principal_plan)):
            if principal_plan[ii]["asset_tran_period"] in buyback_period:
                principal_amount = principal_amount + principal_plan[ii]["asset_tran_amount"]
        insert_buyback(self.item_no, self.period_count, principal_amount, buyback_period[0], self.channel)
        # 执行 回购脚本
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(buyback_handle_tasks, buyback_period)
        # 检查数据
        for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'compensate', 'qsq')
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'compensate', 'qsq')
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()
        print("=================清分完成后，处理回购的担保费和利息==================")
        compensate_run.run_clearing_job_post(buyback_clearing_job)
        compensate_run.run_capital_settlement_task(capital_settlement_tasks)
        for capital_i in range(buyback_period[0], buyback_period[-1] + 1):
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq")
            cleck_trans.check_wsm_advance_clearing(buyback_period[0], capital_i, "compensate", "interest")
            cleck_trans.check_wsm_advance_clearing(buyback_period[0], capital_i, "compensate", "guarantee")

    # @pytest.mark.dcs_auto_test
    @pytest.mark.DCS_test_hbxd
    def test_huabeixiaodai_compensate_payoff(self):
        print("=================第一期逾期次日开始提前结清=================")
        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)

        period_compensate = (1,)
        period_payoff = (1, 2, 3, 4, 5, 6)
        # step 1 到期日往前推1月零1天
        self.change_asset_due_at(-1, -1)

        print("================（制造先还款再代偿的场景）================")
        # time.sleep(2.5)
        # step 2 刷罚息并执行rbiz的msg，到期日上面已经修改过了
        refresh_late_fee(self.item_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
        # step 2 刷完罚息需要执行biz的task，不然还款计划不完整
        run_type_task_biz_central("AssetChange", self.item_no)
        # step 3 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_payoff)
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
        repay_run.run_clearing_jobs_post(repay_tasks, period_payoff)
        # 检查清分的数据
        for capital_i in range(period_payoff[0], period_payoff[-1] + 1):
            capital = get_capital_biz(self.item_no, capital_i)
            cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq")
            cleck_final.check_final_all()
            cleck_final.check_final_amount(capital)
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq")
            cleck_trans.check_trans_all()
            cleck_trans.check_trans_amount()

        print("================开始大单代偿清分（制造先还款再代偿的场景）================")
        # 开始大单代偿清分
        compensate_run = RunDcsJobPost(self.item_no, self.channel, "compensate")
        compensate_run.run_clearing_jobs_post_compensate(compensate_handle_tasks, period_compensate)
        # 检查代偿数据
        capital = get_capital_biz(self.item_no, period_compensate[0])
        cleck_final = CheckDcsFinal(self.item_no, period_compensate[0], 'compensate', 'qsq')
        cleck_final.check_final_all()
        cleck_final.check_final_amount(capital)
        cleck_trans = CheckDcsTrans(self.item_no, period_compensate[0], 'compensate', 'qsq')
        cleck_trans.check_trans_all()
        cleck_trans.check_trans_amount()
        print("==================等待清分完成后，在进行华北小贷单独的逻辑==================")
        actual_final = get_final_all(self.item_no, period_payoff[1], 'repay')
        actual_finish_time = actual_final[0]["actual_finish_time"][:10]
        repay_run.run_clearing_job_post(hbxd_advance_clearing_job, actual_finish_time)
        for capital_i in range(period_payoff[1], period_payoff[-1] + 1):
            cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq")
            cleck_trans.check_advance_clearing(self.channel, period_payoff[1], actual_finish_time)

    # 一天还一期，时间都落在第一期，最终资产结清 ， check_only_current_period 只能在当期还当期或者提前结清
    # def test_huabeixiaodai_zhitou_one_payoff(self):
    #     print("===============一天还一期，时间都落在第一期，最终资产结清============")
    # # 检查小单放款是否成功，否则还款会失败
    # check_asset_grant(self.item_no, self.item_no_noloan)
    # period = (1, 2, 3, 4, 5, 6)
    # # 修改放款日，修改上一期的到期日，查询还款金额然后还款，
    # for repay_i in period:
    #     update_grant_at(get_date_before_today(month=1), self.item_no)
    #     update_due_at(get_date_before_today(day=len(period)-repay_i+1), self.item_no, repay_i-1)
    #     asset_repay = AssetRepay(self.item_no, 0, repay_i)
    #     asset_repay.repay_callback()
    #     asset_repay.delete_null()
    #     update_atransaction(get_date_before_today(day=len(period)-repay_i), self.item_no, repay_i)
    # # 开始清分
    # RunDcsJob(self.item_no, self.channel).job_repay(repay_handle_task, period, is_one_repay='Y')
    # RunDcsJob(self.item_no, self.channel).job_repay(repay_final_handle_task, period)
    # # 检查清分的数据
    # for capital_i in range(period[0], period[-1]+1):
    #     capital = get_capital_biz(self.item_no, capital_i)
    #     cleck_final = CheckDcsFinal(self.item_no, capital_i, 'repay', "qsq")
    #     cleck_final.check_final_all()
    #     cleck_final.check_final_amount(capital)
    #     cleck_trans = CheckDcsTrans(self.item_no, capital_i, 'repay', "qsq")
    #     cleck_trans.check_trans_all()
    #     cleck_trans.check_trans_amount()
