import json
import pytest

from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.global_rbiz.global_rbiz_kv_config import update_tha_rbiz_paysvr_config, \
    update_rbiz_undo_decrease_config, update_rbiz_refresh_fee_conf, update_rbiz_decrease_config
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import check_late_fee, check_msg_content_late_fee, \
    check_asset_data
from biztest.function.global_rbiz.rbiz_global_db_function import get_asset_tran, \
    get_asset_tran_balance_amount_by_item_no, get_asset_tran_log, get_asset_extend, update_withhold, \
    delete_asset_late_fee_refresh_log
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, run_refreshLateFeeV1_by_api, \
    run_assetDecreaseDueAtOnDay_by_api, run_decreasedLateInterestUndoJob_by_api, refresh_late_fee, \
    project_repay_query, trade_withhold
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import get_four_element_global, get_date, get_tz, get_random_str

"""
罚息用例集：
1、只刷新一天的罚息，通过api
2、罚息刷到上限，本金的36%， 通过api
3、首逾罚息减免
4、罚息减免撤销
5、超过120天，刷罚息job不再捞起
6、刷罚息时间，job触发
7、刷罚息时间，api触发
8、刷罚息时间，用户主动还款前(未超过120天&超过120天)
9、刷罚息时间，收到代扣完成通知(包括刷新罚息&减免罚息)
10、刷罚息时间，收到collect代扣通知
11、刷罚息时间，前端刷新还款计划


  以下用例均测试多期，申请第二期

还款金额小于未还本息和，有N天罚息，逾期前申请的还款，逾期前还款，先还本息，不减免罚息
还款金额小于未还本息和，有N天罚息，逾期前申请的还款，逾期后还款，先还本息，不减免罚息
还款金额小于未还本息和，有N天罚息，逾期后申请的还款，先还罚息，再还本金，不减免罚息

还款日等于逾期日，只够还本息，减免所有罚息
还款日等于逾期日，不够还所有罚息，减免剩余罚息
还款日小于逾期日，只够还本息，减免所有罚息
还款日小于逾期日，不够还所有罚息，减免剩余罚息

还款日大于逾期日，只够还本息，减免可减免的所有罚息
还款日大于逾期日，够还部分罚息，减免后罚息仍然剩余
还款日大于逾期日，够还部分罚息，减免后罚息刚好结清
还款日大于逾期日，够还部分罚息，减免的罚息少于可减免罚息罚息，减免后期次结清
还款日大于逾期日，够还所有罚息，不减免，当期结清
还款日大于逾期日，够还所有罚息，仍然有多余，存在账户中
多期一起还款，每期都满足罚息减免规则，那么每期均减免
用户申请第一期还款，回调时第一期部分已还，第二期有罚息，且符合上述规则，不减免


"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.late_fee
class TestRbizLateFee(BaseGlobalRepayTest):

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizLateFee, self).init()
        update_rbiz_decrease_config(can_decrease_day=3)
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    @pytest.fixture(scope="function")
    def setup_4(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass

        request.addfinalizer(teardown)
        update_rbiz_refresh_fee_conf()
        update_rbiz_decrease_config(can_decrease_day=3)
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e")
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element, 4)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def test_refresh_late_overdue_one_day(self, setup):
        self.update_asset_due_at(-1, refresh=True)
        # 验证金融服务费罚息和罚息，1天是本金的1%
        check_late_fee(self.item_no, self.principal_amount * 0.001)
        check_late_fee(self.item_no_x, self.principal_no_loan_amount * 0.001)

        check_msg_content_late_fee(self.item_no, "assetFoxSync", exp_late_interest=self.principal_amount * 0.001)
        check_msg_content_late_fee(self.item_no_x, "assetFoxSync",
                                   exp_late_interest=self.principal_no_loan_amount * 0.001)

    def test_refresh_late_overdue_to_max(self, setup):
        self.update_asset_due_at(-1000, refresh=True)
        # 验证罚息最大值
        check_late_fee(self.item_no, self.principal_amount * 0.36)
        check_late_fee(self.item_no_x, self.principal_no_loan_amount * 0.36)

        check_msg_content_late_fee(self.item_no, "assetFoxSync", exp_late_interest=self.principal_amount * 0.36)
        check_msg_content_late_fee(self.item_no_x, "assetFoxSync",
                                   exp_late_interest=self.principal_no_loan_amount * 0.36)

    def test_asset_decrease_due_at_one_day(self, setup):
        # 发起还款，但是还款失败
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)
        # 刷新罚息
        self.update_asset_due_at(-1, refresh=True)
        # 进行罚息减免
        run_assetDecreaseDueAtOnDay_by_api()
        self.task.run_task(self.item_no, "AssetDecrease", {"code": 0, "message": "减免成功！"})
        self.task.run_task(self.item_no_x, "AssetDecrease", {"code": 0, "message": "减免成功！"})
        # 结果校验
        tran_loan = get_asset_tran(asset_tran_asset_item_no=self.item_no, asset_tran_type="lateinterest")[0]
        Assert.assert_match_json({"asset_tran_amount": 0, "asset_tran_decrease_amount": 500,
                                  "asset_tran_repaid_amount": 0, "asset_tran_balance_amount": 0,
                                  "asset_tran_total_amount": 500}, tran_loan)
        tran_no_loan = get_asset_tran(asset_tran_asset_item_no=self.item_no_x, asset_tran_type="lateinterest")[0]
        Assert.assert_match_json({"asset_tran_amount": 0, "asset_tran_decrease_amount": 50,
                                  "asset_tran_repaid_amount": 0, "asset_tran_balance_amount": 0,
                                  "asset_tran_total_amount": 50}, tran_no_loan)
        extend_loan = get_asset_extend(asset_extend_asset_item_no=self.item_no, asset_extend_type="dueat_onday")[0]
        Assert.assert_equal({"1": {"lateinterest": 500}}, json.loads(extend_loan["asset_extend_val"]))
        extend_no_loan = get_asset_extend(asset_extend_asset_item_no=self.item_no_x, asset_extend_type="dueat_onday")[0]
        Assert.assert_equal({"1": {"lateinterest": 50}}, json.loads(extend_no_loan["asset_extend_val"]))

    def test_asset_decreased_late_interest_undo(self, setup):
        # 发起还款，但是还款失败
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)
        # 刷新罚息
        self.update_asset_due_at(-1, refresh=True)
        # 进行罚息减免
        run_assetDecreaseDueAtOnDay_by_api()
        self.task.run_task(self.item_no, "AssetDecrease", {"code": 0, "message": "减免成功！"})
        self.task.run_task(self.item_no_x, "AssetDecrease", {"code": 0, "message": "减免成功！"})
        # 进行减免撤销
        update_rbiz_undo_decrease_config()
        run_decreasedLateInterestUndoJob_by_api()
        self.task.run_task(self.item_no, "DeceasedLateInterestUndo", )
        self.task.run_task(self.item_no_x, "DeceasedLateInterestUndo", )

        # 结果校验
        tran_loan = get_asset_tran(asset_tran_asset_item_no=self.item_no, asset_tran_type="lateinterest")[0]
        Assert.assert_match_json({"asset_tran_amount": 500, "asset_tran_decrease_amount": 0,
                                  "asset_tran_repaid_amount": 0, "asset_tran_balance_amount": 0,
                                  "asset_tran_total_amount": 500}, tran_loan)
        tran_no_loan = get_asset_tran(asset_tran_asset_item_no=self.item_no_x, asset_tran_type="lateinterest")[0]
        Assert.assert_match_json({"asset_tran_amount": 50, "asset_tran_decrease_amount": 0,
                                  "asset_tran_repaid_amount": 0, "asset_tran_balance_amount": 0,
                                  "asset_tran_total_amount": 50}, tran_no_loan)
        extend_loan = get_asset_extend(asset_extend_asset_item_no=self.item_no, asset_extend_type="dueat_onday")[0]
        Assert.assert_equal({"1": {"lateinterest": 500}}, json.loads(extend_loan["asset_extend_val"]))
        extend_no_loan = get_asset_extend(asset_extend_asset_item_no=self.item_no_x, asset_extend_type="dueat_onday")[0]
        Assert.assert_equal({"1": {"lateinterest": 50}}, json.loads(extend_no_loan["asset_extend_val"]))

    def test_asset_overdue_more_than_120_no_refresh(self, setup):
        update_rbiz_refresh_fee_conf(max_overdue_days=120)
        for i in [119, 120, 121, 122, 123]:
            self.update_asset_due_at(-i)
            run_refreshLateFeeV1_by_api(self.item_no)
            self.task.run_task(self.item_no, "RefreshLateInterest")
            self.task.run_task(self.item_no_x, "RefreshLateInterest")
            self.task.run_task(self.item_no, "AssetAccountChangeNotify")
            self.task.run_task(self.item_no_x, "AssetAccountChangeNotify")
            delete_asset_late_fee_refresh_log(asset_late_fee_refresh_log_asset_item_no=self.item_no)
            delete_asset_late_fee_refresh_log(asset_late_fee_refresh_log_asset_item_no=self.item_no_x)

            # 验证罚息最大值
            days = i if i <= 121 else 121
            check_late_fee(self.item_no, self.principal_amount * 0.001 * days)
            check_late_fee(self.item_no_x, self.principal_no_loan_amount * 0.001 * days)

            check_msg_content_late_fee(self.item_no, "assetFoxSync",
                                       exp_late_interest=self.principal_amount * 0.001 * days)
            check_msg_content_late_fee(self.item_no_x, "assetFoxSync",
                                       exp_late_interest=self.principal_no_loan_amount * 0.001 * days)

    def test_refresh_late_trigger_by_job(self, setup):
        # 发起还款，但是还款失败
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        trade_withhold(self.item_no, "asset_delay", 1500, "collect", period_list=[1], delay_days=3,
                       four_element=self.four_element)

        # 修改资产到期日
        self.update_asset_due_at(-1)
        # 刷新罚息
        run_refreshLateFeeV1_by_api(self.item_no)
        self.task.run_task(self.item_no, "RefreshLateInterest")
        self.task.run_task(self.item_no_x, "RefreshLateInterest")
        self.task.run_task(self.item_no, "AssetAccountChangeNotify")
        self.task.run_task(self.item_no_x, "AssetAccountChangeNotify")
        # 验证金融服务费罚息和罚息，1天是本金的1%
        check_late_fee(self.item_no, self.principal_amount * 0.001)
        check_late_fee(self.item_no_x, self.principal_no_loan_amount * 0.001)

        check_msg_content_late_fee(self.item_no, "assetFoxSync", exp_late_interest=self.principal_amount * 0.001)
        check_msg_content_late_fee(self.item_no_x, "assetFoxSync",
                                   exp_late_interest=self.principal_no_loan_amount * 0.001)

    def test_refresh_late_trigger_by_api(self, setup):
        # 修改资产到期日
        self.update_asset_due_at(-1)
        # 刷新罚息
        refresh_late_fee(self.item_no)
        self.task.run_task(self.item_no, "AssetAccountChangeNotify")
        refresh_late_fee(self.item_no_x)
        self.task.run_task(self.item_no_x, "AssetAccountChangeNotify")
        # 验证金融服务费罚息和罚息，1天是本金的1%
        check_late_fee(self.item_no, self.principal_amount * 0.001)
        check_late_fee(self.item_no_x, self.principal_no_loan_amount * 0.001)

        check_msg_content_late_fee(self.item_no, "assetFoxSync", exp_late_interest=self.principal_amount * 0.001)
        check_msg_content_late_fee(self.item_no_x, "assetFoxSync",
                                   exp_late_interest=self.principal_no_loan_amount * 0.001)

    def test_refresh_late_trigger_by_user_active_repay(self, setup):
        # 修改资产到期日
        self.update_asset_due_at(-100)
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        assert resp_combo_active['content']['code'] == 1, f"主动合并代扣失败,resp_combo_active={resp_combo_active}"
        assert resp_combo_active['content'][
                   'message'] == f"资产编号[{self.item_no}],第[1]期不支持部分还款,还款输入金额[503500]小于应还金额[553500]", \
            f"主动合并代扣失败,resp_combo_active={resp_combo_active}"

        # 验证金融服务费罚息和罚息，1天是本金的1%
        self.task.run_task(self.item_no, "AssetAccountChangeNotify")
        self.task.run_task(self.item_no_x, "AssetAccountChangeNotify")
        check_late_fee(self.item_no, self.principal_amount * 0.001 * 100)
        check_late_fee(self.item_no_x, self.principal_no_loan_amount * 0.001 * 100)
        check_msg_content_late_fee(self.item_no, "assetFoxSync", exp_late_interest=self.principal_amount * 0.001 * 100)
        check_msg_content_late_fee(self.item_no_x, "assetFoxSync",
                                   exp_late_interest=self.principal_no_loan_amount * 0.001 * 100)

        # 罚息刷到最大天数
        self.update_asset_due_at(-121)
        run_refreshLateFeeV1_by_api(self.item_no)
        self.task.run_task(self.item_no, "RefreshLateInterest")
        self.task.run_task(self.item_no_x, "RefreshLateInterest")
        self.task.run_task(self.item_no, "AssetAccountChangeNotify")
        self.task.run_task(self.item_no_x, "AssetAccountChangeNotify")
        # 验证罚息最大值
        check_late_fee(self.item_no, self.principal_amount * 0.001 * 121)
        check_late_fee(self.item_no_x, self.principal_no_loan_amount * 0.001 * 121)
        check_msg_content_late_fee(self.item_no, "assetFoxSync", exp_late_interest=self.principal_amount * 0.001 * 121)
        check_msg_content_late_fee(self.item_no_x, "assetFoxSync",
                                   exp_late_interest=self.principal_no_loan_amount * 0.001 * 121)

        # 再次还款，看罚息是否刷新
        self.update_asset_due_at(-130)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        assert resp_combo_active['content']['code'] == 1, f"主动合并代扣失败,resp_combo_active={resp_combo_active}"
        assert resp_combo_active['content'][
                   'message'] == f"资产编号[{self.item_no}],第[1]期不支持部分还款,还款输入金额[503500]小于应还金额[568500]", \
            f"主动合并代扣失败,resp_combo_active={resp_combo_active}"

        # 验证金融服务费罚息和罚息，1天是本金的1%
        self.task.run_task(self.item_no, "AssetAccountChangeNotify")
        self.task.run_task(self.item_no_x, "AssetAccountChangeNotify")
        check_late_fee(self.item_no, self.principal_amount * 0.001 * 130)
        check_late_fee(self.item_no_x, self.principal_no_loan_amount * 0.001 * 130)
        check_msg_content_late_fee(self.item_no, "assetFoxSync", exp_late_interest=self.principal_amount * 0.001 * 130)
        check_msg_content_late_fee(self.item_no_x, "assetFoxSync",
                                   exp_late_interest=self.principal_no_loan_amount * 0.001 * 130)

    def test_refresh_late_trigger_by_withhold_callback_success(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        # 回调失败
        paysvr_callback(merchant_key, withhold_amount, 3)
        # 修改资产到期日
        self.update_asset_due_at(-5)

        # 回调成功
        paysvr_callback(merchant_key, withhold_amount, 2, finished_at=get_date(day=-1, timezone=get_tz()))
        self.run_all_task_after_repay_success()

        # 检查数据
        tran_log = get_asset_tran_log(asset_tran_log_asset_item_no=self.item_no,
                                      asset_tran_log_operate_type="decrease_fee")[0]
        Assert.assert_match_json({"asset_tran_log_amount": -2500, "asset_tran_log_operator_name": "回调系统"}, tran_log)
        tran_log = get_asset_tran_log(asset_tran_log_asset_item_no=self.item_no_x,
                                      asset_tran_log_operate_type="decrease_fee")[0]
        Assert.assert_match_json({"asset_tran_log_amount": -250, "asset_tran_log_operator_name": "回调系统"}, tran_log)

        tran_loan = get_asset_tran(asset_tran_asset_item_no=self.item_no, asset_tran_type="lateinterest")[0]
        Assert.assert_match_json({"asset_tran_amount": 0, "asset_tran_decrease_amount": 2500,
                                  "asset_tran_repaid_amount": 0, "asset_tran_balance_amount": 0,
                                  "asset_tran_total_amount": 2500, "asset_tran_status": "finish"}, tran_loan)
        tran_no_loan = get_asset_tran(asset_tran_asset_item_no=self.item_no_x, asset_tran_type="lateinterest")[0]
        Assert.assert_match_json({"asset_tran_amount": 0, "asset_tran_decrease_amount": 250,
                                  "asset_tran_repaid_amount": 0, "asset_tran_balance_amount": 0,
                                  "asset_tran_total_amount": 250, "asset_tran_status": "finish"}, tran_no_loan)

    def test_refresh_late_trigger_by_collect_callback_success(self, setup):
        self.update_asset_due_at(-1)
        self.repay_collect({"item_no": self.item_no, "amount": 1500, "repay_type": "asset"})

        # 检查数据
        tran_log = get_asset_tran_log(asset_tran_log_asset_item_no=self.item_no,
                                      asset_tran_log_operate_type="refresh_fee")[0]
        Assert.assert_match_json({"asset_tran_log_amount": 500, "asset_tran_log_operator_name": "系统"}, tran_log)
        tran_log = get_asset_tran_log(asset_tran_log_asset_item_no=self.item_no_x,
                                      asset_tran_log_operate_type="refresh_fee")[0]
        Assert.assert_match_json({"asset_tran_log_amount": 50, "asset_tran_log_operator_name": "系统"}, tran_log)

        tran_loan = get_asset_tran(asset_tran_asset_item_no=self.item_no, asset_tran_type="lateinterest")[0]
        Assert.assert_match_json({"asset_tran_amount": 500, "asset_tran_decrease_amount": 0,
                                  "asset_tran_repaid_amount": 500, "asset_tran_balance_amount": 0,
                                  "asset_tran_total_amount": 500, "asset_tran_status": "finish"}, tran_loan)
        tran_no_loan = get_asset_tran(asset_tran_asset_item_no=self.item_no_x, asset_tran_type="lateinterest")[0]
        Assert.assert_match_json({"asset_tran_amount": 50, "asset_tran_decrease_amount": 0,
                                  "asset_tran_repaid_amount": 0, "asset_tran_balance_amount": 0,
                                  "asset_tran_total_amount": 50, "asset_tran_status": "nofinish"}, tran_no_loan)

    def test_refresh_late_trigger_by_project_repay(self, setup):
        # 修改资产到期日
        self.update_asset_due_at(-1)
        # 刷新罚息
        project_repay_query(self.item_no)
        self.task.run_task(self.item_no, "AssetAccountChangeNotify")
        project_repay_query(self.item_no_x)
        self.task.run_task(self.item_no_x, "AssetAccountChangeNotify")
        # 验证金融服务费罚息和罚息，1天是本金的1%
        check_late_fee(self.item_no, self.principal_amount * 0.001)
        check_late_fee(self.item_no_x, self.principal_no_loan_amount * 0.001)

        check_msg_content_late_fee(self.item_no, "assetFoxSync", exp_late_interest=self.principal_amount * 0.001)
        check_msg_content_late_fee(self.item_no_x, "assetFoxSync",
                                   exp_late_interest=self.principal_no_loan_amount * 0.001)

    def test_repay_amount_less_than_principal_and_interest_1(self, setup_4):
        # 发起还款，但是还款失败
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 3
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        update_withhold(order_no, withhold_create_at=get_date(day=-5, timezone=get_tz()))
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) - 100, 2,
                        finished_at=get_date(day=-4, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=124900, repaid_interest_amount=3500,
                         repaid_amount=128400, late_amount=375, balance_amount=385975, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_amount=12500, late_amount=36, balance_amount=37536, asset_status="repay")

    def test_repay_amount_less_than_principal_and_interest_2(self, setup_4):
        # 发起还款，但是还款失败
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 3
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        update_withhold(order_no, withhold_create_at=get_date(day=-5, timezone=get_tz()))
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) - 100, 2,
                        finished_at=get_date(day=-2, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=124900, repaid_interest_amount=3500,
                         repaid_amount=128400, late_amount=375, balance_amount=385975, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_amount=12500, late_amount=36, balance_amount=37536, asset_status="repay")

    def test_repay_amount_less_than_principal_and_interest_3(self, setup_4):
        self.update_asset_due_at(-1, refresh=True)
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 3
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        update_withhold(order_no, withhold_create_at=get_date(day=-2, timezone=get_tz()))
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) - 137 - 138, 2,
                        finished_at=get_date(day=-2, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=124451, repaid_interest_amount=3500,
                         repaid_late_amount=375,
                         repaid_amount=128326, late_amount=375, balance_amount=386049, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500, repaid_late_amount=36,
                         repaid_amount=12536, late_amount=36, balance_amount=37500, asset_status="repay")

    def test_repay_amount_less_than_principal_and_interest_4(self, setup_4):
        self.update_asset_due_at(-1, refresh=True)
        coupon_num = "coupon_" + get_random_str(10)
        project_num_loan_channel_amount = project_num_no_loan_amount = 0
        for period in [1, 2, 3, 4]:
            project_num_loan_channel_amount += int(get_asset_tran_balance_amount_by_item_no(self.item_no, period))
            project_num_no_loan_amount += int(get_asset_tran_balance_amount_by_item_no(self.item_no_x, period))
        resp_combo_active = self.combo_active_repay_apply(0, 0, period_list=[1, 2, 3, 4],
                                                          coupon_num=coupon_num, coupon_amount=2000)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 3
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功 金额为
        paysvr_callback(order_no,
                        int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) - 137 - 138 - 2000, 2,
                        finished_at=get_date(day=-2, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=497451, repaid_interest_amount=14000,
                         repaid_late_amount=375,
                         repaid_amount=511826, late_amount=375, balance_amount=2549, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_late_amount=36,
                         repaid_amount=50036, late_amount=36, balance_amount=0, asset_status="payoff")

    def test_repay_date_equal_due_at_repay_0_late_decrease_all(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 3
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2,
                        finished_at=get_date(day=-3, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_amount=128500, decrease_late_amount=375, balance_amount=385500, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_amount=12500, decrease_late_amount=36, balance_amount=37500, asset_status="repay")

    def test_repay_date_equal_due_at_repay_little_late_decrease_part(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 3
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) + 100, 2,
                        finished_at=get_date(day=-3, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_late_amount=88, late_amount=88, decrease_late_amount=287,
                         repaid_amount=128588, balance_amount=385500, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_late_amount=12, late_amount=12, decrease_late_amount=24,
                         repaid_amount=12512, balance_amount=37500, asset_status="repay")

    def test_repay_date_less_due_at_repay_0_late_decrease_all(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 3
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2,
                        finished_at=get_date(day=-4, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_amount=128500, decrease_late_amount=375, balance_amount=385500, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_amount=12500, decrease_late_amount=36, balance_amount=37500, asset_status="repay")

    def test_repay_date_less_due_at_repay_little_late_decrease_part(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 3
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) + 100, 2,
                        finished_at=get_date(day=-4, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_late_amount=88, late_amount=88, decrease_late_amount=287,
                         repaid_amount=128588, balance_amount=385500, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_late_amount=12, late_amount=12, decrease_late_amount=24,
                         repaid_amount=12512, balance_amount=37500, asset_status="repay")

    def test_repay_date_large_due_at_repay_0_late_decrease_all(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期5天
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2,
                        finished_at=get_date(day=-1, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500, late_amount=125,
                         repaid_amount=128500, decrease_late_amount=500, balance_amount=385625, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500, late_amount=12,
                         repaid_amount=12500, decrease_late_amount=48, balance_amount=37512, asset_status="repay")

    def test_repay_date_large_due_at_repay_little_late_decrease_part(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no,
                        int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) + 100, 2,
                        finished_at=get_date(day=-1, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500, late_amount=125,
                         repaid_late_amount=100,
                         repaid_amount=128600, decrease_late_amount=500, balance_amount=385525, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500, late_amount=12,
                         repaid_amount=12500, decrease_late_amount=48, balance_amount=37512, asset_status="repay")

    def test_repay_date_large_due_at_repay_all_late_decrease_all(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no,
                        int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) + 137 * 2 + 100, 2,
                        finished_at=get_date(day=-1, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_late_amount=338, late_amount=338,
                         repaid_amount=128838, decrease_late_amount=287, balance_amount=385500, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_late_amount=36, late_amount=36,
                         repaid_amount=12536, decrease_late_amount=24, balance_amount=37500, asset_status="repay")

    def test_repay_date_large_due_at_repay_more_late_decrease_all(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no,
                        int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) + 125 * 5 + 20, 2,
                        finished_at=get_date(day=-1, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_late_amount=585, late_amount=585, decrease_late_amount=40,
                         repaid_amount=129085, balance_amount=385500, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500, repaid_late_amount=60, late_amount=60,
                         repaid_amount=12560, balance_amount=37500, asset_status="repay")

    def test_repay_date_large_due_at_repay_more_late_decrease_0(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no,
                        int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) + 137 * 5, 2,
                        finished_at=get_date(day=-1, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_late_amount=625, late_amount=625,
                         repaid_amount=129125, balance_amount=385500, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_late_amount=60, late_amount=60,
                         repaid_amount=12560, balance_amount=37500, asset_status="repay")

    def test_repay_date_large_due_at_repay_all_late_still_remain(self, setup_4):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        # 逾期3天
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功
        paysvr_callback(order_no,
                        int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) + 137 * 5 + 100, 2,
                        finished_at=get_date(day=-1, timezone=get_tz()))
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3600,
                         repaid_late_amount=625, late_amount=625,
                         repaid_amount=129225, balance_amount=385400, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_late_amount=60, late_amount=60,
                         repaid_amount=12560, balance_amount=37500, asset_status="repay")
