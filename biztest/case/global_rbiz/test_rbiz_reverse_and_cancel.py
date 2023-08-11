from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.global_rbiz.global_rbiz_kv_config import update_rbiz_config
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.interface.rbiz.rbiz_global_interface import void_asset_from_mq, cancel_asset_from_mq, \
    run_withholdTimeout_by_api, paysvr_callback
from biztest.util.db.db_util import DataBase


@pytest.mark.global_rbiz_thailand
@pytest.mark.reverse_and_cancel
class TestRbizReverseAndCancel(BaseGlobalRepayTest):

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizReverseAndCancel, self).init()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type,
                                                     self.four_element)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def test_asset_reverse_with_no_withhold(self, setup):
        # 冲正前检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "小单状态不对")
        # 冲正
        void_asset_from_mq(self.item_no, self.loan_channel)
        void_asset_from_mq(self.item_no_x, "noloan")
        self.task.run_task_by_order_no(self.item_no, [{"code": 0, "message": "处理成功"},
                                                      {"code": 0, "message": "处理成功"}])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[0]["task_status"])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[1]["task_status"])
        # 冲正后检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("sale", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("sale", asset_info[0]['asset_status'], "小单状态不对")

    def test_asset_reverse_with_withhold_process(self, setup):
        # 发起代扣
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        # 冲正
        void_asset_from_mq(self.item_no, self.loan_channel)
        self.task.run_task_by_order_no(self.item_no, [{"code": 2, "message": "资产.*存在未完成的代扣数据，暂时不允许冲正！等待稍后重试"},
                                                      {"code": 2, "message": "资产.*存在未完成的代扣数据，暂时不允许冲正！等待稍后重试"}])
        Assert.assert_equal("open",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[0]["task_status"])
        Assert.assert_equal("open",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[1]["task_status"])
        # 冲正后检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "小单状态不对")

    def test_asset_reverse_with_withhold_fail(self, setup):
        # 发起代扣并代扣失败
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        update_withhold(order_no, withhold_create_at=get_date(day=-1, hour=-2, timezone=get_tz(gc.COUNTRY)))
        run_withholdTimeout_by_api()
        self.task.wait_task_appear(order_no, "withhold_timeout")
        self.task.run_task(order_no, "withhold_timeout", {"code": 0, "message": "将订单设置为失败成功！"})
        # 冲正
        void_asset_from_mq(self.item_no, self.loan_channel)
        self.task.run_task_by_order_no(self.item_no, [{"code": 0, "message": "处理成功"},
                                                      {"code": 0, "message": "处理成功"}])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[0]["task_status"])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[1]["task_status"])
        # 冲正后检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("sale", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("sale", asset_info[0]['asset_status'], "小单状态不对")

    def test_asset_reverse_with_withhold_success_and_amount_less(self, setup):
        # 发起代扣并代扣成功
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]['order_no']
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) - 100)
        self.run_all_task_after_repay_success()
        update_rbiz_config(
            auto_void_withhold_amount=int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) - 100 - 1)
        # 冲正
        void_asset_from_mq(self.item_no, self.loan_channel)
        self.task.run_task_by_order_no(self.item_no, [{"code": 1, "message": "资产.*状态已经payoff或者writeoff，不处理！"},
                                                      {"code": 1,
                                                       "message": "资产.*存在成功的代扣数据,且金额不允许自动逆操作处理，暂时不允许冲正！等待稍后重试"}])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[0]["task_status"])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[1]["task_status"])
        # 冲正后检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("payoff", asset_info[0]['asset_status'], "小单状态不对")

    def test_asset_reverse_with_withhold_success_and_amount_big(self, setup):
        # 发起代扣并代扣成功
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]['order_no']
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) - 100)
        self.run_all_task_after_repay_success()
        update_rbiz_config(
            auto_void_withhold_amount=int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) - 100)
        # 冲正
        void_asset_from_mq(self.item_no, self.loan_channel)
        self.task.run_task_by_order_no(self.item_no, [{"code": 1, "message": "资产.*状态已经payoff或者writeoff，不处理！"},
                                                      {"code": 0, "message": "处理成功"}])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[0]["task_status"])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")[1]["task_status"])
        # 冲正后检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("sale", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("payoff", asset_info[0]['asset_status'], "小单状态不对")

    def test_asset_cancel_with_no_withhold(self, setup):
        # 冲正前检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "小单状态不对")
        # 冲正
        cancel_asset_from_mq(self.item_no, self.loan_channel)
        self.task.run_task_by_order_no(self.item_no, [{"code": 0, "message": "取消成功"},
                                                      {"code": 0, "message": "取消成功"}])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")[0]["task_status"])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")[1]["task_status"])
        # 冲正后检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "小单状态不对")

    def test_asset_cancel_with_withhold_process(self, setup):
        # 发起代扣
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        # 冲正
        cancel_asset_from_mq(self.item_no, self.loan_channel)
        self.task.run_task_by_order_no(self.item_no, [{"code": 2, "message": "资产.*存在未完成的代扣数据，暂时不允许取消！等待稍后重试"},
                                                      {"code": 2, "message": "资产.*存在未完成的代扣数据，暂时不允许取消！等待稍后重试"}])
        Assert.assert_equal("open",
                            self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")[0]["task_status"])
        Assert.assert_equal("open",
                            self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")[1]["task_status"])
        # 冲正后检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "小单状态不对")

    def test_asset_cancel_with_withhold_fail(self, setup):
        # 发起代扣并代扣失败
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        update_withhold(order_no, withhold_create_at=get_date(day=-1, hour=-2, timezone=get_tz(gc.COUNTRY)))
        run_withholdTimeout_by_api()
        self.task.wait_task_appear(order_no, "withhold_timeout")
        self.task.run_task(order_no, "withhold_timeout", {"code": 0, "message": "将订单设置为失败成功！"})
        # 冲正
        cancel_asset_from_mq(self.item_no, self.loan_channel)
        self.task.run_task_by_order_no(self.item_no, [{"code": 0, "message": "取消成功"},
                                                      {"code": 0, "message": "取消成功"}])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")[0]["task_status"])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")[1]["task_status"])
        # 冲正后检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "小单状态不对")

    def test_asset_cancel_with_withhold_success(self, setup):
        # 发起代扣并代扣失败
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]['order_no']
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) - 100)
        self.run_all_task_after_repay_success()
        # 冲正
        cancel_asset_from_mq(self.item_no, self.loan_channel)
        self.task.run_task_by_order_no(self.item_no, [{"code": 1, "message": "资产.*存在已经发生过还款，暂时不允许取消"},
                                                      {"code": 1, "message": "资产.*存在已经发生过还款，暂时不允许取消"}])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")[0]["task_status"])
        Assert.assert_equal("close",
                            self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")[0]["task_status"])
        # 冲正后检查
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("repay", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("payoff", asset_info[0]['asset_status'], "小单状态不对")

    def test_first_reverse_second_cancel(self, setup):
        # 先冲正，后取消
        void_asset_from_mq(self.item_no, self.loan_channel)
        time.sleep(2)
        cancel_asset_from_mq(self.item_no, self.loan_channel)

        # 运行冲正task
        void_task_list = self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")
        self.task.run_task_by_id(void_task_list[0]["task_id"], {"code": 0, "message": "处理成功"})
        self.task.run_task_by_id(void_task_list[1]["task_id"], {"code": 0, "message": "处理成功"})
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("sale", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("sale", asset_info[0]['asset_status'], "小单状态不对")
        # 运行取消task
        cancel_task_list = self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")
        self.task.run_task_by_id(cancel_task_list[0]["task_id"], {"code": 0, "message": "取消成功"})
        self.task.run_task_by_id(cancel_task_list[1]["task_id"], {"code": 0, "message": "取消成功"})
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "小单状态不对")

    def test_first_cancel_second_reverse(self, setup):
        # 先取消，后冲正
        void_asset_from_mq(self.item_no, self.loan_channel)
        time.sleep(2)
        cancel_asset_from_mq(self.item_no, self.loan_channel)
        # 运行取消task
        cancel_task_list = self.task.get_task(task_order_no=self.item_no, task_type="cancelAsset")
        self.task.run_task_by_id(cancel_task_list[0]["task_id"], {"code": 0, "message": "取消成功"})
        self.task.run_task_by_id(cancel_task_list[1]["task_id"], {"code": 0, "message": "取消成功"})
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "小单状态不对")
        # 运行冲正task
        void_task_list = self.task.get_task(task_order_no=self.item_no, task_type="voidAsset")
        self.task.run_task_by_id(void_task_list[0]["task_id"], {"code": 0, "message": "资产.*旧版本数据，不处理！"})
        self.task.run_task_by_id(void_task_list[1]["task_id"], {"code": 0, "message": "资产.*旧版本数据，不处理！"})
        asset_info = get_asset_info_by_item_no(self.item_no)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "大单状态不对")
        asset_info = get_asset_info_by_item_no(self.item_no_x)
        Assert.assert_equal("void", asset_info[0]['asset_status'], "小单状态不对")
