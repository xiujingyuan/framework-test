from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.function.global_rbiz.rbiz_global_db_function import update_asset
from biztest.interface.rbiz.rbiz_global_interface import fox_overdue_view, fox_query_asset_repay, \
    fox_query_new_overdue, fox_deadline_asset_query, fox_query_asset_repay_detail, fox_withhold, fox_withhold_query, \
    fox_cancel_and_decrease
from biztest.util.db.db_util import DataBase

"""

关单减免：



"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.rbiz_fox
class TestRbizFox(BaseGlobalRepayTest):

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizFox, self).init()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type,
                                                     self.four_element)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def test_fox_deadline_asset_query(self, setup):
        self.update_asset_due_at(0)
        update_asset(self.item_no, asset_due_at=get_date(fmt="%Y-%m-%d"))
        update_asset(self.item_no_x, asset_due_at=get_date(fmt="%Y-%m-%d"))

        # 查询到期的资产信息
        resp, _ = fox_deadline_asset_query()
        result = False
        for item in resp["content"]["data"]:
            if item["asset_item_no"] in (self.item_no, self.item_no_x):
                Assert.assert_match_json({"status": "nofinish",
                                          "type": "paydayloan",
                                          "owner": "TAILAND",
                                          "asset_item_no": self.item_no + "|" + self.item_no_x,
                                          "asset_extend_ref_order_no": self.item_no + "|" + self.item_no_x,
                                          "asset_extend_ref_order_type": self.source_type + ".*"
                                          },
                                         item)
                result = True
        Assert.assert_equal(result, True, "无数据")

    def test_fox_query_new_overdue(self, setup):
        # 刷新罚息
        self.update_asset_due_at(-1, refresh=True)
        # 查询新入催资产
        resp, _ = fox_query_new_overdue()
        Assert.assert_in(self.item_no, resp["content"]["data"])
        Assert.assert_in(self.item_no_x, resp["content"]["data"])

        # 查询单笔资产逾期情况
        resp, _ = fox_overdue_view(self.item_no)
        Assert.assert_match_json({"data": {"asset": {"asset_item_number": self.item_no},
                                           "asset_transactions": [{'asset_transaction_type': 'lateinterest'},
                                                                  {'asset_transaction_type': 'repayinterest'},
                                                                  {'asset_transaction_type': 'repayprincipal'},
                                                                  ]}},
                                 resp["content"])

    def test_fox_withhold(self, setup):
        # 刷新罚息
        self.update_asset_due_at(-1, refresh=True)
        # 发起fox代扣
        self.mock.update_withhold_autopay_ebank_url_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        resp, req = fox_withhold(item_no=self.item_no, payment_type="ebank",
                                 amount=project_num_loan_channel_amount, four_element=self.four_element)
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel")
        order_no = resp["content"]["data"]["order_no"]
        self.run_all_task_after_repay_success()

        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element['data']['card_num'],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 504000,
            "repay_type": "overdue",
            "order_operate_type": "manual",
            "trade_type": "FOX_MANUAL_WITHHOLD"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_late_amount=500, repaid_amount=504000, late_amount=500, asset_status="payoff")

        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp, req = fox_withhold(item_no=self.item_no_x, payment_type="ebank",
                                 amount=project_num_no_loan_amount, four_element=self.four_element)
        self.mock.update_withhold_query_success(self.item_no_x, 2, "auto_thailand_channel")
        order_no_x = resp["content"]["data"]["order_no"]
        self.run_all_task_after_repay_success()

        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element['data']['card_num'],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 50050,
            "repay_type": "overdue",
            "order_operate_type": "manual",
            "trade_type": "FOX_MANUAL_WITHHOLD"
        }
        check_withhold_success_data(order_no_x, **withhold)
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_late_amount=50, repaid_amount=50050,
                         late_amount=50, asset_status="payoff")

        # fox代扣查询
        resp, req = fox_withhold_query("fox" + self.item_no)
        Assert.assert_match_json({
            "code": 0,
            "message": "成功",
            "data": {
                "status": 0,
                "order_no": order_no,
                "amount": 504000,
                "req_key": "fox" + self.item_no,
                "error_code": "E20000"
            }
        }, resp["content"])

        # fox查询资产还款信息
        time.sleep(3)
        resp, _ = fox_query_asset_repay()
        result = False
        for item in resp["content"]["data"]["data_list"]:
            if item["item_no"] == self.item_no:
                Assert.assert_match_json({"item_no": self.item_no,
                                          "repay_date": get_date(fmt="%Y-%m-%d"),
                                          "repay_amount": -504000,
                                          "repay_period": 1},
                                         item)
                result = True
                break
        Assert.assert_equal(True, result, "大单结果正确")
        for item in resp["content"]["data"]["data_list"]:
            if item["item_no"] == self.item_no_x:
                Assert.assert_match_json({"item_no": self.item_no_x,
                                          "repay_date": get_date(fmt="%Y-%m-%d"),
                                          "repay_amount": -50050,
                                          "repay_period": 1},
                                         item)
                result = True
                break
        Assert.assert_equal(True, result, "小单结果正确")
        # fox查询还款详情
        resp, _ = fox_query_asset_repay_detail(self.item_no)
        Assert.assert_match_json({
            "code": 0,
            "message": "查询成功",
            "data": {
                "data": {
                    "asset": {
                        "asset_item_no": self.item_no}}}},
            resp["content"])

    def test_fox_overdue_repay(self, setup):
        # 刷新罚息
        self.update_asset_due_at(-1)
        self.refresh_late_fee(self.item_no)
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        resp_fox = self.loan_fox_repay_apply(int(project_num_loan_channel_amount), self.four_element)
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_fox_phl_channel")
        check_json_rs_data(resp_fox['content'], code=0)
        order_no = resp_fox["content"]["data"]["order_no"]
        self.run_all_task_after_repay_success()

        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element['data']['card_num'],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_fox_phl_channel",
            "withhold_amount": 504000,
            "repay_type": "overdue",
            "order_operate_type": "manual",
            "trade_type": "FOX_MANUAL_WITHHOLD"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_late_amount=500, repaid_amount=504000, late_amount=500, asset_status="payoff")

    def test_fox_advance_repay(self, setup):
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        resp_fox = self.loan_fox_repay_apply(int(project_num_loan_channel_amount), self.four_element)
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_fox_phl_channel")
        order_no = resp_fox["content"]["data"]["order_no"]
        check_json_rs_data(resp_fox['content'], code=0)

        self.run_all_task_after_repay_success()

        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element['data']['card_num'],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_fox_phl_channel",
            "withhold_amount": 503500,
            "repay_type": "advance",
            "order_operate_type": "manual",
            "trade_type": "FOX_MANUAL_WITHHOLD"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")

    def test_fox_withhold_cancel_and_decrease_no_withhold(self, setup):
        self.mock.mock_close_order_success()
        # 资产逾期
        self.update_asset_due_at(-1, refresh=True)
        # 进行减免
        resp = fox_cancel_and_decrease(self.item_no)
        Assert.assert_match_json({"code": 0, "message": "罚息减免成功！", "data": None},
                                 resp["content"], "减免成功")
        # 数据检查
        lock_data_is_not_here(self.item_no)
        check_asset_data(self.item_no, decrease_late_amount=100, late_amount=400, balance_amount=503900)

    def test_fox_withhold_cancel_and_decrease_success(self, setup):
        self.mock.mock_close_order_success()
        # 资产逾期
        self.update_asset_due_at(-1, refresh=True)
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        lock_data_is_here(self.item_no)
        # 进行减免
        resp = fox_cancel_and_decrease(self.item_no)
        Assert.assert_match_json({"code": 0, "message": "罚息减免成功！", "data": None},
                                 resp["content"], "减免成功")
        # 数据检查
        lock_data_is_not_here(self.item_no)
        check_asset_data(self.item_no, decrease_late_amount=100, late_amount=400, balance_amount=503900)

    def test_fox_withhold_cancel_and_decrease_fail(self, setup):
        self.mock.mock_close_order_fail()
        # 资产逾期
        self.update_asset_due_at(-1, refresh=True)
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        lock_data_is_here(self.item_no)
        # 进行减免
        resp = fox_cancel_and_decrease(self.item_no)
        Assert.assert_match_json({"code": 1, "message": r"\[serial_no=.*\]取消支付失败！返回数据：{\"code\":1,\"mes"
                                                        r"sage\":\"订单已经成为终态，关闭订单失败\",\"data\":null}！",
                                  "data": {"error_code": "E3000", "error_message": "Business error"}},
                                 resp["content"], "减免成功")
        # 数据检查
        lock_data_is_here(self.item_no)
        check_asset_data(self.item_no, late_amount=500, balance_amount=504000)
