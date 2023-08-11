from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, withhold_cancel
from biztest.util.db.db_util import DataBase

"""
用例集：
支付返回关单成功，关闭代扣记录，释放锁
支付返回关单失败，透传失败，不作处理
关单接口500
关单接口异常，timeout
关单后，支付回调代扣失败
关单后，支付回调代扣成功
关单后，再次发起代扣
"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.withhold_cancel
class TestRbizWithholdCancel(BaseGlobalRepayTest):

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizWithholdCancel, self).init()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type,
                                                     self.four_element)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def test_cancel_withhold_success(self, setup):
        self.mock.mock_close_order_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request = get_withhold_request_by_serial_no(merchant_key)
        # 取消代扣
        request_key = request[0]["withhold_request_req_key"]
        resp_cancel = withhold_cancel(request_key, "")
        assert resp_cancel['content']['code'] == 0, f"代扣取消成功,resp_combo_active={resp_cancel}"
        lock_data_is_not_here(self.item_no)

        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2,
                        "auto_thailand_channel")
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request = get_withhold_request_by_serial_no(merchant_key)
        # 取消代扣
        request_key = request[0]["withhold_request_req_key"]
        resp_cancel = withhold_cancel(request_key, "")
        Assert.assert_match_json({"code": 0, "message": "cancel succes"}, resp_cancel['content'])

    def test_cancel_withhold_fail(self, setup):
        self.mock.mock_close_order_fail()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          "ebank")
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request = get_withhold_request_by_serial_no(merchant_key)
        # 取消代扣
        request_key = request[0]["withhold_request_req_key"]
        resp_cancel = withhold_cancel(request_key, "")
        assert resp_cancel['content']['code'] == 1, f"代扣取消成功,resp_combo_active={resp_cancel}"
        assert resp_cancel['content']['message'] == f'[serial_no={merchant_key}]取消支付失败！返回数据：' \
                                                    '{"code":1,"message":"订单已经成为终态，关闭订单失败","data":null}！', \
            f"代扣取消失败,resp_combo_active={resp_cancel}"
        lock_data_is_here(self.item_no)

    def test_cancel_withhold_500(self, setup):
        self.mock.mock_close_order_500()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          "ebank")
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request = get_withhold_request_by_serial_no(merchant_key)
        # 取消代扣
        request_key = request[0]["withhold_request_req_key"]
        resp_cancel = withhold_cancel(request_key, "")
        Assert.assert_equal(2, resp_cancel['content']['code'], "code正确")
        Assert.assert_match(resp_cancel['content']['message'], ".*500.*", "message正确")
        lock_data_is_here(self.item_no)

    def test_cancel_withhold_and_callback_fail(self, setup):
        self.mock.mock_close_order_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          "ebank")
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request = get_withhold_request_by_serial_no(merchant_key)
        # 取消代扣
        request_key = request[0]["withhold_request_req_key"]
        resp_cancel = withhold_cancel(request_key, "")
        assert resp_cancel['content']['code'] == 0, f"代扣取消成功,resp_combo_active={resp_cancel}"
        lock_data_is_not_here(self.item_no)
        # 回调失败
        paysvr_callback(merchant_key, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3,
                        "auto_thailand_channel")
        withhold = get_withhold_by_serial_no(merchant_key)[0]
        Assert.assert_equal(withhold["withhold_status"], "fail")
        check_asset_data(self.item_no, repaid_principal_amount=0, repaid_interest_amount=0, balance_amount=503500)

    def test_cancel_withhold_and_callback_success(self, setup):
        self.mock.mock_close_order_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          "ebank")
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request = get_withhold_request_by_serial_no(merchant_key)
        # 取消代扣
        request_key = request[0]["withhold_request_req_key"]
        resp_cancel = withhold_cancel(request_key, "")
        assert resp_cancel['content']['code'] == 0, f"代扣取消成功,resp_combo_active={resp_cancel}"
        lock_data_is_not_here(self.item_no)
        # 回调失败
        paysvr_callback(merchant_key, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2,
                        "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element['data']['card_num'],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 553500,
            "repay_type": "advance",
            "withhold_sub_status": "user_cancel"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_cancel_withhold_and_retry_withhold(self, setup):
        self.mock.mock_close_order_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          "ebank")
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request = get_withhold_request_by_serial_no(merchant_key)
        # 取消代扣
        request_key = request[0]["withhold_request_req_key"]
        resp_cancel = withhold_cancel(request_key, "")
        assert resp_cancel['content']['code'] == 0, f"代扣取消成功,resp_combo_active={resp_cancel}"
        lock_data_is_not_here(self.item_no)
        # 再次发起代扣
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          "ebank")
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2,
                        "auto_thailand_channel")
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element['data']['card_num'],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 553500,
            "repay_type": "advance",
            "withhold_sub_status": "normal"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
