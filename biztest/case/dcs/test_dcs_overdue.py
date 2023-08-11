# 白金／联连 都已经清盘，以后也不怎么可能有d-1的资金方了
import time, pytest
# capital7环境就用 xxljob_config ，capital6环境就用 xxljob_config2 。
from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.easymock.easymock_config import mock_project, rbiz_mock
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.dcs.dcs_grant_asset import AssetImportGrant
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count
from biztest.interface.rbiz.biz_central_interface import run_type_task_biz_central
from biztest.interface.rbiz.rbiz_interface import refresh_late_fee, combo_active_repay_without_no_loan
from biztest.util.easymock.rbiz.paysvr import PaysvrMock
from biztest.util.tools.tools import get_item_no
from biztest.function.dcs.dcs_common import check_asset_grant, get_four_params_rbiz_db, check_repay_biz
from biztest.function.dcs.biz_database import get_repay_amount_rbiz

import common.global_const as gc


class TestDcsOverdue(BaseRepayTest):
    env_test = gc.ENV
    environment = gc.ENVIRONMENT

    # 老资产因为没有 data.cardsInfoDto 暂时无法放款成功到rbiz
    @pytest.mark.DCS_overdue_repay
    def test_overdue_repay(self):
        self.init(self.env_test)
        channel = "shoujin"  # baijin  zhenjinfu  lianlian  shoujin
        self.item_no = 'ha_sj_' + get_item_no()[:16]
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
        grant_asset = AssetImportGrant(channel, "youxi_bill", **kwargs)
        grant_asset.asset_import_biz()
        grant_asset.asset_grant_biz()
        grant_asset.asset_capital_plan_biz()
        grant_asset.asset_grant_noloan()

        # 检查小单放款是否成功，否则还款会失败
        check_asset_grant(self.item_no)
        print("=================没有代偿=================")
        print("=================第一期逾期还款=================")
        period_repay = (1,)

        # step 1 到期日往前推2月零3天
        self.change_asset_due_at(-2, -3)
        # step 2 刷罚息并执行rbiz的msg，到期日上面已经修改过了
        refresh_late_fee(self.item_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
        # step 2 刷完罚息需要执行biz的task，不然还款计划不完整
        run_type_task_biz_central("AssetChange", self.item_no)
        # step 3 发起主动代扣
        asset_tran_amount = get_repay_amount_rbiz(self.item_no, period_repay)
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
        run_dcs_task_by_count(self.item_no, 5)
        # repay_run = RunDcsJobPost(self.item_no, channel, "repay")
        # repay_run.run_clearing_jobs_post(repay_tasks, period_repay)
        # # 检查清分的数据
        # capital = get_capital_biz(self.item_no, period_repay[0])
        # cleck_final = CheckDcsFinal(self.item_no, period_repay[0], 'repay', "qsq")
        # cleck_final.check_final_all()
        # cleck_final.check_final_amount(capital)
        # cleck_trans = CheckDcsTrans(self.item_no, period_repay[0], 'repay', "qsq")
        # cleck_trans.check_trans_all()
        # cleck_trans.check_trans_amount()

        # time.sleep(5.5)
        print("=================第二期逾期部分还=================")
        period_repay2 = (2,)
        # step 3 发起主动代扣
        self.four_element = get_four_params_rbiz_db(self.item_no)
        params_combo_active = {
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"],
            "project_num_loan_channel": self.item_no,
            "project_num_loan_channel_priority": 1,
            "project_num_loan_channel_amount": 90000
        }
        combo_active_repay_without_no_loan(**params_combo_active)
        # step 4 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        run_dcs_task_by_count(self.item_no, 5)
        # repay_run = RunDcsJobPost(self.item_no, channel, "repay")
        # repay_run.run_clearing_jobs_post(repay_tasks, period_repay2)
        # 检查清分的数据
        # get_capital_biz(self.item_no, period_repay2[0])
        # cleck_final = CheckDcsFinal(self.item_no, period_repay2[0], 'repay', "qsq", 'N')
        # cleck_final.check_final_all()
        # # 部分还款不检查 check_final_amount
        # cleck_trans = CheckDcsTrans(self.item_no, period_repay2[0], 'repay', "qsq", 'N')
        # cleck_trans.check_trans_all()
        # cleck_trans.check_trans_amount()

        # time.sleep(5.5)
        print("=================剩余所有期次结清=================")
        period_repay2 = (2,)
        # step 3 发起主动代扣
        self.four_element = get_four_params_rbiz_db(self.item_no)
        params_combo_active = {
            "card_num_encrypt": self.four_element['data']["bank_code_encrypt"],
            "card_user_id_encrypt": self.four_element['data']["id_number_encrypt"],
            "card_user_name_encrypt": self.four_element['data']["user_name_encrypt"],
            "card_user_phone_encrypt": self.four_element['data']["phone_number_encrypt"],
            "project_num_loan_channel": self.item_no,
            "project_num_loan_channel_priority": 1,
            "project_num_loan_channel_amount": 648566
        }
        combo_active_repay_without_no_loan(**params_combo_active)
        # step 4 执行task和msg
        self.run_all_task_after_repay_success()
        self.run_all_msg_after_repay_success()
        # step 4 检查biz的帐信息
        check_repay_biz(self.item_no)
        # 开始大单还款清分
        run_dcs_task_by_count(self.item_no, 5)
