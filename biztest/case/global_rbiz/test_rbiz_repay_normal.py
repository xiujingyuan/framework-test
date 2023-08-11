from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, combo_query_key, \
    combo_active_repay_with_no_loan, tran_decrease, fox_cancel_and_decrease, run_FoxAdvancePushJob_by_api
from biztest.util.db.db_util import DataBase

"""
代扣回来后的动作：
1、罚息更新
2、罚息减免（根据withhold_finish_at之后的罚息，需减免），减免需要结清期次的罚息，未结清不减免
3、detail调整（增删改），order调整
4、充值还款
5、消息同步检查
用例集：
1、主动还款，提前还款
2、主动还款，正常还款
3、主动还款，逾期还款
4、还款发起失败
5、还款查询成功
6、还款查询失败
7、还款回调成功
8、还款回调失败
9、还款回调，先失败，后成功
10、还款金额不正确
11、还款金额太小
12、还款成功，资产已经结清，且有共债资产，不还到共债上面
13、还款成功，用户还款金额大于发起金额，多余金额留在账户中
14、还款顺序，用户还款金额小于申请金额，申请时detail无罚息，还款成功时tran有罚息，还款金额先还利息，再还本金，本金有剩余
15、还款顺序，用户还款金额等于申请金额，申请时detail无罚息，还款成功时tran有罚息，还款金额先还利息，再还本金，本金无剩余
16、还款顺序，用户还款金额大于申请金额，申请时detail无罚息，还款成功时tran有罚息，还款金额先还利息，再还本金，再还罚息，多余的留在账户
17、还款成功，用户还款金额大于发起金额，多余金额需还款到其他费用中(新增罚息)
18、detail修改，detail金额比tran待还金额小，detail金额需增加
19、detail修改，tran部分已还，detail金额比tran待还金额大，detail金额需减少
20、detail修改，tran部分减免，detail金额比tran待还金额大，detail金额需减少
21、detail修改，还款金额不够，detail金额需减少
22、detail修改，还款金额不够，detail条目需删除
23、detail修改，tran项全部被减免，detail罚息删除
24、detail修改，tran项全部被结清，detail本金删除
25、代扣查询接口
26、代扣copy，paysvr新建订单，rbiz进行copy


还款类型：
1、二维码
2、ebank
3、sdk
4、bcode
"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.normal_repay
class TestRbizNormalRepay(BaseGlobalRepayTest):

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizNormalRepay, self).init()
        self.mock.update_withhold_autopay_ebank_url_success()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def test_active_advance_repay(self, setup):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        self.mock.update_withhold_query_success(self.item_no, pay_status=2)
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_india_channel",
            "withhold_amount": 553500,
            "repay_type": "advance"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_active_normal_repay(self, setup):
        self.update_asset_due_at(0)
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        self.mock.update_withhold_query_success(self.item_no, pay_status=2)
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_india_channel",
            "withhold_amount": 553500,
            "repay_type": "normal"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_active_overdue_repay(self, setup):
        self.update_asset_due_at(-1, refresh=True)
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        self.mock.update_withhold_query_success(self.item_no, pay_status=2)
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_india_channel",
            "withhold_amount": 554050,
            "repay_type": "overdue"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_late_amount=500, repaid_amount=504000, late_amount=500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50050,
                         repaid_late_amount=50, late_amount=50, asset_status="payoff")

    def test_active_repay_apply_failed(self, setup):
        self.mock.update_withhold_auto_withhold_success(code=1)
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        withhold = get_withhold_by_serial_no(order_no)
        Assert.assert_equal(withhold[0]["withhold_status"], "fail", "withhold_status is not correct")

    def test_active_repay_query_success(self, setup):
        self.mock.update_withhold_auto_withhold_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_serial_no(order_no)[0]["withhold_request_no"]
        self.mock.update_withhold_query_success(self.item_no, pay_status=2)
        self.task.run_task(request_no, "execute_combine_withhold", {"code": 0, "message": "Transaction Successful"})
        withhold = get_withhold_by_serial_no(order_no)
        Assert.assert_equal(withhold[0]["withhold_status"], "success", "withhold_status is not correct")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_india_channel",
            "withhold_amount": 553500,
            "repay_type": "advance",
            "payment_type": "withhold"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_active_repay_query_failed(self, setup):
        self.mock.update_withhold_auto_withhold_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_serial_no(order_no)[0]["withhold_request_no"]
        self.mock.update_withhold_query_success(self.item_no, pay_status=3)
        self.task.run_task(request_no, "execute_combine_withhold", )
        withhold = get_withhold_by_serial_no(order_no)
        Assert.assert_equal(withhold[0]["withhold_status"], "fail", "withhold_status is not correct")

    def test_active_repay_callback_success(self, setup):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        self.mock.update_withhold_query_success(self.item_no, pay_status=3)
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount))
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 553500,
            "repay_type": "advance"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_active_repay_callback_fail(self, setup):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        self.mock.update_withhold_query_success(self.item_no, pay_status=2)
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)
        request_no = get_withhold_by_serial_no(order_no)[0]["withhold_request_no"]
        self.task.run_task(request_no, "execute_combine_withhold", )
        withhold = get_withhold_by_serial_no(order_no)
        Assert.assert_equal(withhold[0]["withhold_status"], "fail", "withhold_status is not correct")

    def test_active_repay_callback_fail_reverse_success(self, setup):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        self.mock.update_withhold_query_success(self.item_no, pay_status=2)
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)
        request_no = get_withhold_by_serial_no(order_no)[0]["withhold_request_no"]
        self.task.run_task(request_no, "execute_combine_withhold", )
        withhold = get_withhold_by_serial_no(order_no)
        Assert.assert_equal(withhold[0]["withhold_status"], "fail", "withhold_status is not correct")

        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount))
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 553500,
            "repay_type": "advance"
        }
        check_withhold_success_data(order_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_active_repay_apply_money_incorrect(self, setup):
        params_combo_active = {
            "card_uuid": self.four_element["data"]["card_num"],
            "id_num": self.four_element["data"]["id_number_encrypt"],
            "user_id": self.four_element["data"]["id_number"],
            "mobile": self.four_element["data"]["mobile_encrypt"],
            "payment_type": "ebank",
            "project_num_loan_channel": self.item_no,
            "project_num_no_loan": self.item_no_x,
            "project_num_loan_channel_amount": self.principal_amount,
            "project_num_no_loan_amount": 10000
        }
        resp_combo_active, _ = combo_active_repay_with_no_loan(**params_combo_active)
        assert resp_combo_active["content"][
                   "code"] == 1, f"主动合并代扣失败,resp_combo_active={resp_combo_active}"
        assert resp_combo_active["content"][
                   "message"] == f"资产编号[{self.item_no}],第[1]期不支持部分还款,还款输入金额[500000]小于应还金额[503500]", \
            f"主动合并代扣失败,resp_combo_active={resp_combo_active}"

    def test_active_repay_apply_money_less_100(self, setup):
        params_combo_active = {
            "card_uuid": self.four_element["data"]["card_num"],
            "id_num": self.four_element["data"]["id_number_encrypt"],
            "user_id": self.four_element["data"]["id_number"],
            "mobile": self.four_element["data"]["mobile_encrypt"],
            "payment_type": "ebank",
            "project_num_loan_channel": self.item_no,
            "project_num_no_loan": self.item_no_x,
            "project_num_loan_channel_amount": 1,
            "project_num_no_loan_amount": 1
        }
        resp_combo_active, _ = combo_active_repay_with_no_loan(**params_combo_active)
        assert resp_combo_active["content"][
                   "code"] == 1, f"主动合并代扣失败,resp_combo_active={resp_combo_active}"
        assert resp_combo_active["content"][
                   "message"] == f"Withholding amount must be over 100", \
            f"主动合并代扣失败,resp_combo_active={resp_combo_active}"

    def test_active_repay_asset_already_payoff(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type,
                                                         self.four_element)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调失败 第1笔
        paysvr_callback(merchant_key, withhold_amount, 3)
        self.task.run_task(self.item_no, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        # 回调成功 第2笔
        resp_combo_active_new = self.combo_active_repay_apply(project_num_loan_channel_amount,
                                                              project_num_no_loan_amount)
        merchant_key_new = resp_combo_active_new["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(merchant_key_new, withhold_amount, 2)
        self.run_all_task_after_repay_success()
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(self.item_no_x, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 回调成功 第1笔
        paysvr_callback(merchant_key, withhold_amount, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        self.task.run_task(self.item_no, "assetWithholdOrderRepay",
                           {"code": 0, "message": "资产.*代扣.*没有对应的withhold_detail"})
        self.task.run_task(self.item_no_x, "assetWithholdOrderRepay",
                           {"code": 0, "message": "资产.*代扣.*没有对应的withhold_detail"})
        # 数据检查
        withhold = get_withhold_by_serial_no(merchant_key)[0]
        account = get_account_by_id_num(withhold["withhold_user_idnum"])[0]
        Assert.assert_equal(553500, account["account_balance_amount"], "account余额正确")
        check_asset_data(self.item_no_new, balance_amount=503500, asset_status="repay")
        check_asset_data(self.item_no_x_new, balance_amount=50000, asset_status="repay")

    def test_active_repay_amount_more_than_apply_amount_stay_account(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调成功，金额大于申请金额
        paysvr_callback(merchant_key, withhold_amount + 100, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": withhold_amount + 100,
            "order_amount": withhold_amount,
            "balance_amount": 100,
            "repay_type": "advance"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        withhold = get_withhold_by_serial_no(merchant_key)[0]
        account = get_account_by_id_num(withhold["withhold_user_idnum"])[0]
        Assert.assert_equal(100, account["account_balance_amount"], "account余额正确")

    def test_active_repay_amount_not_repay_late_principal_has_balance(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调成功，金额大于申请金额
        paysvr_callback(merchant_key, withhold_amount, 3)
        # 资产逾期
        self.update_asset_due_at(-1, refresh=True)
        paysvr_callback(merchant_key, withhold_amount-600, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": withhold_amount-600,
            "repay_type": "advance"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=499400, repaid_interest_amount=3500,
                         repaid_amount=502900, late_amount=500, balance_amount=1100, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, late_amount=50,
                         balance_amount=50, asset_status="repay")

    def test_active_repay_amount_not_repay_late_principal_has_no_balance(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调成功，金额大于申请金额
        paysvr_callback(merchant_key, withhold_amount, 3)
        # 资产逾期
        self.update_asset_due_at(-1, refresh=True)
        paysvr_callback(merchant_key, withhold_amount, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": withhold_amount,
            "repay_type": "advance"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, decrease_late_amount=500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000,
                         repaid_amount=50000, decrease_late_amount=50, asset_status="payoff")

    def test_active_repay_amount_repay_late_principal_has_no_balance(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调成功，金额大于申请金额
        paysvr_callback(merchant_key, withhold_amount, 3)
        # 资产逾期
        self.update_asset_due_at(-1, refresh=True)
        paysvr_callback(merchant_key, withhold_amount + 520, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": withhold_amount + 520,
            "repay_type": "advance"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_late_amount=470, late_amount=470, decrease_late_amount=30,
                         repaid_amount=503970, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000,
                         repaid_late_amount=50, late_amount=50,
                         repaid_amount=50050, asset_status="payoff")

    def test_active_repay_amount_more_than_apply_amount_repay_new_item(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调失败 第1笔
        paysvr_callback(merchant_key, withhold_amount, 3)
        self.task.run_task(self.item_no, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        # 资产逾期并刷新罚息
        self.update_asset_due_at(-1, refresh=True)
        # 回调成功，金额大于申请金额
        paysvr_callback(merchant_key, withhold_amount + 1000, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": withhold_amount + 1000,
            "order_amount": withhold_amount + 550,
            "balance_amount": 450,
            "repay_type": "advance"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_late_amount=500, repaid_amount=504000, late_amount=500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50050,
                         repaid_late_amount=50, late_amount=50, asset_status="payoff")
        withhold = get_withhold_by_serial_no(merchant_key)[0]
        account = get_account_by_id_num(withhold["withhold_user_idnum"])[0]
        Assert.assert_equal(450, account["account_balance_amount"], "account余额正确")

    def test_active_repay_detail_amount_increase(self, setup):
        # 资产逾期并刷新罚息
        self.update_asset_due_at(-1, refresh=True)
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调失败
        paysvr_callback(merchant_key, withhold_amount, 3)
        # 继续逾期，并刷新罚息
        for i in range(1, 6):
            self.update_asset_due_at(-i, refresh=True)

        # 回调成功，金额大于申请金额
        update_withhold(merchant_key, withhold_create_at=get_date(day=-4))
        paysvr_callback(merchant_key, withhold_amount + 3000, 2, "auto_thailand_channel", finished_at=get_date(day=-2))
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": withhold_amount + 3000,
            "order_amount": withhold_amount + 2200,
            "balance_amount": 800,
            "repay_type": "overdue"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_late_amount=2500, repaid_amount=506000, late_amount=2500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000,
                         repaid_late_amount=250, repaid_amount=50250, late_amount=250, asset_status="payoff")
        withhold = get_withhold_by_serial_no(merchant_key)[0]
        account = get_account_by_id_num(withhold["withhold_user_idnum"])[0]
        Assert.assert_equal(800, account["account_balance_amount"], "account余额正确")

    def test_active_repay_tran_part_repay_set_detail_amount_small(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调失败 第1笔
        paysvr_callback(merchant_key, withhold_amount, 3)
        self.task.run_task(self.item_no, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        # 回调成功 第2笔 但是资产不能还完
        resp_combo_active_new = self.combo_active_repay_apply(project_num_loan_channel_amount,
                                                              project_num_no_loan_amount)
        merchant_key_new = resp_combo_active_new["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(merchant_key_new, withhold_amount - 100, 2)
        self.run_all_task_after_repay_success()
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(self.item_no_x, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 检查资产还款情况
        check_asset_data(self.item_no, repaid_principal_amount=499900, repaid_interest_amount=3500,
                         repaid_amount=503400, balance_amount=100, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

        # 回调成功 第1笔
        paysvr_callback(merchant_key, withhold_amount - 100, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 检查资产还款情况
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        withhold = get_withhold_by_serial_no(merchant_key)[0]
        account = get_account_by_id_num(withhold["withhold_user_idnum"])[0]
        Assert.assert_equal(withhold_amount - 200, account["account_balance_amount"], "account余额正确")

    def test_active_repay_tran_decrease_set_detail_amount_small(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(merchant_key, withhold_amount, 3)
        # 进行减免
        tran_decrease(self.item_no, "repayinterest", 3000)
        # 回调成功
        paysvr_callback(merchant_key, withhold_amount, 2)
        self.run_all_task_after_repay_success()
        # 检查资产还款情况
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=500,
                         repaid_amount=500500, decrease_interest_amount=3000, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

        withhold = get_withhold_by_serial_no(merchant_key)[0]
        account = get_account_by_id_num(withhold["withhold_user_idnum"])[0]
        Assert.assert_equal(3000, account["account_balance_amount"], "account余额正确")

    def test_active_repay_amount_not_enough_detail_repay_part(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调成功，金额大于申请金额
        paysvr_callback(merchant_key, withhold_amount - 100, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": withhold_amount - 100,
            "repay_type": "advance"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=499900, repaid_interest_amount=3500,
                         repaid_amount=503400, balance_amount=100, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_active_repay_amount_not_enough_detail_delete(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调成功，金额大于申请金额
        paysvr_callback(merchant_key, 100, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": 100,
            "repay_type": "advance"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, balance_amount=503500, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=100, repaid_amount=100, balance_amount=49900,
                         asset_status="repay")

    def test_active_repay_tran_item_decreased_detail_delete(self, setup):
        # 逾期
        self.update_asset_due_at(-1, refresh=True)
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 进行减免
        self.mock.mock_close_order_success()
        fox_cancel_and_decrease(self.item_no, 500)
        fox_cancel_and_decrease(self.item_no_x, 50)
        # 回调成功，金额大于申请金额
        paysvr_callback(merchant_key, withhold_amount, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": withhold_amount,
            "balance_amount": 550,
            "order_amount": withhold_amount - 550,
            "repay_type": "overdue",
            "withhold_sub_status": "user_cancel"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, decrease_late_amount=500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, decrease_late_amount=50,
                         asset_status="payoff")

    def test_active_repay_tran_item_payoff_detail_delete(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调失败 第1笔
        paysvr_callback(merchant_key, withhold_amount, 3)
        self.task.run_task(self.item_no, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        # 回调成功 第2笔 但是资产不能还完
        resp_combo_active_new = self.combo_active_repay_apply(project_num_loan_channel_amount,
                                                              project_num_no_loan_amount)
        merchant_key_new = resp_combo_active_new["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(merchant_key_new, withhold_amount - 100, 2)
        self.run_all_task_after_repay_success()
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(self.item_no_x, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 检查资产还款情况
        check_asset_data(self.item_no, repaid_principal_amount=499900, repaid_interest_amount=3500,
                         repaid_amount=503400, balance_amount=100, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

        # 回调成功 第1笔
        paysvr_callback(merchant_key, withhold_amount - 100, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()

        # 验证数据 资产相关
        withhold = {
            "withhold_card_num": self.four_element["data"]["card_num"],
            "withhold_payment_mode": "AUTOTEST",
            "sign_company": "amberstar1",
            "withhold_channel": "auto_thailand_channel",
            "withhold_amount": withhold_amount - 100,
            "order_amount": 100,
            "balance_amount": withhold_amount - 200,
            "repay_type": "advance"
        }
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_active_comb_query(self, setup):
        self.mock.update_withhold_auto_withhold_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          "withhold")
        req_key = get_withhold_request_by_item_no(self.item_no)[0]["withhold_request_req_key"]
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]

        resp_combo_query_key, req_body_combo_query_key, url = combo_query_key(req_key)
        Assert.assert_match_json({"code": 0,
                                  "data": [{"error_code": "E20017",
                                            "memo": "auto test mock data platform msg",
                                            "order_no": order_no,
                                            "project_num": self.item_no,
                                            "status": 2},
                                           {"error_code": "E20017",
                                            "memo": "auto test mock data platform msg",
                                            "order_no": order_no,
                                            "project_num": self.item_no_x,
                                            "status": 2}],
                                  "message": "Request Success"},
                                 resp_combo_query_key["content"])

        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2,
                        "auto_thailand_channel")

        resp_combo_query_key, req_body_combo_query_key, url = combo_query_key(req_key)
        Assert.assert_match_json({"code": 0,
                                  "data": [{"error_code": "E20000",
                                            "memo": "Transaction Successful",
                                            "order_no": order_no,
                                            "project_num": self.item_no,
                                            "status": 0},
                                           {"error_code": "E20000",
                                            "memo": "Transaction Successful",
                                            "order_no": order_no,
                                            "project_num": self.item_no_x,
                                            "status": 0}],
                                  "message": "Request Success"},
                                 resp_combo_query_key["content"])

    def test_active_repay_copy_withhold(self, setup):
        # 发起还款
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        withhold_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        merchant_key = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        # 回调成功 第1笔
        paysvr_callback(merchant_key, 100, 2)
        self.run_all_task_after_repay_success()
        # 回调成功 第2笔
        merchant_key_new = get_random_str()
        paysvr_callback(merchant_key_new, withhold_amount-100, 2, original_merchant_key=merchant_key)
        self.run_all_task_by_serial_no(merchant_key_new)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
