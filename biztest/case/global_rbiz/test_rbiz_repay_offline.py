from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.global_rbiz.global_rbiz_kv_config import update_rbiz_api_config, update_account_statement_sync
from biztest.function.global_gbiz.gbiz_global_db_function import insert_manual_asset, update_manual_asset
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.interface.rbiz.rbiz_global_interface import repay_offline_withhold_apply, repay_offline_withhold_deal, \
    repay_offline_withhold_confirm, run_initStatusAccountStatementMatchWithholdRecord_by_api, refresh_late_fee, \
    paysvr_callback, transaction_confirm, run_accountStatementSync_by_api
from biztest.util.db.db_util import DataBase


"""
1、正向匹配成功，通过withhold_payment_card_num匹配成功
2、正向匹配成功，通过withhold_card_num匹配成功
3、正向匹配成功，通过放款查询的卡号匹配成功
4、反向匹配成功
5、人工确认成功
6、罚息减免
7、多次还款后资产结清
"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.offline_repay
class TestRbizOfflineRepay(BaseGlobalRepayTest):
    interest_amount = 3500
    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizOfflineRepay, self).init()
        update_rbiz_api_config("5e46037fd53ef1165b98246e")
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element)

        insert_manual_asset(self.item_no, self.loan_channel, self.principal_amount,
                            self.four_element["data"]["card_num_encrypt"])
        update_account_statement_sync()

    def test_offline_repay_forward_match_01(self, setup):
        update_account_statement_sync(data_source="")
        statement = self.mock.update_flow_query_withhold(self.principal_amount)
        payment_card_num = statement["data"][0]["trade_no"]
        run_accountStatementSync_by_api()
        self.task.run_task("abc", "account_statement_sync", {"code": 0, "message": "同步成功"})
        update_account_statement_record(payment_card_num, account_statement_record_check_row=payment_card_num)

        resp, _ = repay_offline_withhold_apply(item_no=self.item_no)
        serial_no = resp["content"]["data"]["order_no"]
        request_no = resp["content"]["data"]["request_no"]
        repay_offline_withhold_confirm(item_no=self.item_no, request_no=request_no, transaction_no=payment_card_num)

        self.task.run_task(request_no, "execute_combine_withhold", {"code": 0, "message": "Transaction Successful"})
        self.task.run_task(serial_no, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "offlinerepay",
                    "payment_type": "",
                    "withhold_card_num": self.four_element["data"]["card_num_encrypt"],
                    "withhold_amount": self.principal_amount,
                    "sign_company": "amberstar1",
                    "repay_type": "advance",
                    "trade_type": "OFFLINE_WITHHOLD"}
        check_withhold_success_data(serial_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=self.principal_amount - self.interest_amount,
                         repaid_interest_amount=self.interest_amount, repaid_amount=self.principal_amount,
                         balance_amount=self.interest_amount)

    def test_offline_repay_forward_match_02(self, setup):
        update_account_statement_sync(data_source="")
        statement = self.mock.update_flow_query_withhold(self.principal_amount)
        payment_card_num = statement["data"][0]["trade_no"]
        run_accountStatementSync_by_api()
        self.task.run_task("abc", "account_statement_sync", {"code": 0, "message": "同步成功"})
        update_account_statement_record(payment_card_num, account_statement_record_check_row=payment_card_num)

        resp, _ = repay_offline_withhold_apply(item_no=self.item_no)
        serial_no = resp["content"]["data"]["order_no"]
        request_no = resp["content"]["data"]["request_no"]
        repay_offline_withhold_confirm(item_no=self.item_no, request_no=request_no, transaction_no=get_random_num())
        update_withhold(serial_no, withhold_card_num=global_encry_data("card_number", payment_card_num))
        self.task.run_task(request_no, "execute_combine_withhold", {"code": 0, "message": "Transaction Successful"})
        self.task.run_task(serial_no, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "offlinerepay",
                    "payment_type": "",
                    "withhold_card_num": global_encry_data("card_number", payment_card_num),
                    "withhold_amount": self.principal_amount,
                    "sign_company": "amberstar1",
                    "repay_type": "advance",
                    "trade_type": "OFFLINE_WITHHOLD"}
        check_withhold_success_data(serial_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=self.principal_amount - self.interest_amount,
                         repaid_interest_amount=self.interest_amount, repaid_amount=self.principal_amount,
                         balance_amount=self.interest_amount)

    def test_offline_repay_forward_match_03(self, setup):
        update_account_statement_sync(data_source="")
        statement = self.mock.update_flow_query_withhold(self.principal_amount)
        payment_card_num = statement["data"][0]["trade_no"]
        run_accountStatementSync_by_api()
        self.task.run_task("abc", "account_statement_sync", {"code": 0, "message": "同步成功"})
        update_account_statement_record(payment_card_num, account_statement_record_check_row=payment_card_num)

        resp, _ = repay_offline_withhold_apply(item_no=self.item_no)
        serial_no = resp["content"]["data"]["order_no"]
        request_no = resp["content"]["data"]["request_no"]
        repay_offline_withhold_confirm(item_no=self.item_no, request_no=request_no, transaction_no=get_random_num())
        update_manual_asset(self.item_no,
                            manual_asset_receiver_card_no=global_encry_data("card_number", payment_card_num))
        self.task.run_task(request_no, "execute_combine_withhold", {"code": 0, "message": "Transaction Successful"})
        self.task.run_task(serial_no, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "offlinerepay",
                    "payment_type": "",
                    "withhold_card_num": self.four_element["data"]["card_num_encrypt"],
                    "withhold_amount": self.principal_amount,
                    "sign_company": "amberstar1",
                    "repay_type": "advance",
                    "trade_type": "OFFLINE_WITHHOLD"}
        check_withhold_success_data(serial_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=self.principal_amount - self.interest_amount,
                         repaid_interest_amount=self.interest_amount, repaid_amount=self.principal_amount,
                         balance_amount=self.interest_amount)

    def test_offline_repay_reverse_match(self, setup):
        update_account_statement_sync(data_source="")
        statement = self.mock.update_flow_query_withhold(self.principal_amount)
        payment_card_num = statement["data"][0]["trade_no"]
        run_accountStatementSync_by_api()
        self.task.run_task("abc", "account_statement_sync", {"code": 0, "message": "同步成功"})
        update_account_statement_record(payment_card_num, account_statement_record_check_row=payment_card_num)

        resp, _ = repay_offline_withhold_apply(item_no=self.item_no)
        serial_no = resp["content"]["data"]["order_no"]
        request_no = resp["content"]["data"]["request_no"]
        repay_offline_withhold_confirm(item_no=self.item_no, request_no=request_no, transaction_no=payment_card_num)
        run_initStatusAccountStatementMatchWithholdRecord_by_api()
        self.task.run_task(payment_card_num, "account_statement_record_match", {"code": 0, "message": ".*匹配成功.*"})
        self.task.run_task(serial_no, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "offlinerepay",
                    "payment_type": "",
                    "withhold_card_num": self.four_element["data"]["card_num_encrypt"],
                    "withhold_amount": self.principal_amount,
                    "sign_company": "amberstar1",
                    "repay_type": "advance",
                    "trade_type": "OFFLINE_WITHHOLD"}
        check_withhold_success_data(serial_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=self.principal_amount - self.interest_amount,
                         repaid_interest_amount=self.interest_amount, repaid_amount=self.principal_amount,
                         balance_amount=self.interest_amount)

    def test_offline_repay_manual_deal_without_withhold(self, setup):
        update_account_statement_sync(data_source="")
        statement = self.mock.update_flow_query_withhold(self.principal_amount)
        payment_card_num = statement["data"][0]["trade_no"]
        run_accountStatementSync_by_api()
        self.task.run_task("abc", "account_statement_sync", {"code": 0, "message": "同步成功"})
        update_account_statement_record(payment_card_num, account_statement_record_check_row=payment_card_num)

        resp = repay_offline_withhold_deal(serial_no=get_random_str(), item_no=self.item_no,
                                           status="success", trade_id=payment_card_num)
        serial_no = resp["content"]["data"]["order_no"]

        self.task.run_task(serial_no, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "offlinerepay",
                    "payment_type": "",
                    "withhold_card_num": "enc_03_3573347754854320128_693",
                    "withhold_amount": self.principal_amount,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "OFFLINE_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(serial_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=self.principal_amount - self.interest_amount,
                         repaid_interest_amount=self.interest_amount, repaid_amount=self.principal_amount,
                         balance_amount=self.interest_amount)

    def test_offline_repay_manual_deal(self, setup):
        update_account_statement_sync(data_source="")
        statement = self.mock.update_flow_query_withhold(self.principal_amount)
        payment_card_num = statement["data"][0]["trade_no"]
        run_accountStatementSync_by_api()
        self.task.run_task("abc", "account_statement_sync", {"code": 0, "message": "同步成功"})
        update_account_statement_record(payment_card_num, account_statement_record_check_row=payment_card_num)

        resp, _ = repay_offline_withhold_apply(item_no=self.item_no)
        serial_no = resp["content"]["data"]["order_no"]
        request_no = resp["content"]["data"]["request_no"]
        repay_offline_withhold_confirm(item_no=self.item_no, request_no=request_no, transaction_no=get_random_num())
        repay_offline_withhold_deal(serial_no=serial_no, request_no=request_no, status="success",
                                    trade_id=payment_card_num)
        self.task.run_task(serial_no, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "offlinerepay",
                    "payment_type": "",
                    "withhold_card_num": "enc_03_3573347754854320128_693",
                    "withhold_amount": self.principal_amount,
                    "sign_company": "amberstar1",
                    "repay_type": "advance",
                    "trade_type": "OFFLINE_WITHHOLD"}
        check_withhold_success_data(serial_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=self.principal_amount - self.interest_amount,
                         repaid_interest_amount=self.interest_amount, repaid_amount=self.principal_amount,
                         balance_amount=self.interest_amount)

    def test_offline_repay_latefee_decrease(self, setup):
        # 先逾期
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i)
            refresh_late_fee(self.item_no)

        # 进行还款
        update_account_statement_sync(data_source="")
        statement = self.mock.update_flow_query_withhold(self.principal_amount,
                                                         trade_date=get_date(day=-2, timezone=get_tz(gc.COUNTRY)))
        payment_card_num = statement["data"][0]["trade_no"]
        run_accountStatementSync_by_api()
        self.task.run_task("abc", "account_statement_sync", {"code": 0, "message": "同步成功"})
        update_account_statement_record(payment_card_num, account_statement_record_check_row=payment_card_num)

        resp, _ = repay_offline_withhold_apply(item_no=self.item_no)
        serial_no = resp["content"]["data"]["order_no"]
        request_no = resp["content"]["data"]["request_no"]
        repay_offline_withhold_confirm(item_no=self.item_no, request_no=request_no, transaction_no=get_random_num())
        # 处理还款
        repay_offline_withhold_deal(serial_no=serial_no, request_no=request_no, status="success",
                                    trade_id=payment_card_num)
        self.run_all_task_after_repay_success()
        self.task.run_task(serial_no, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "offlinerepay",
                    "payment_type": "",
                    "withhold_card_num": "enc_03_3573347754854320128_693",
                    "withhold_amount": self.principal_amount,
                    "sign_company": "amberstar1",
                    "repay_type": "overdue",
                    "trade_type": "OFFLINE_WITHHOLD"}
        check_withhold_success_data(serial_no, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=495500, repaid_interest_amount=3500,
                         repaid_late_amount=1000, repaid_amount=500000, decrease_late_amount=1500, late_amount=1000,
                         balance_amount=4500)
        tran_log = get_asset_tran_log(asset_tran_log_asset_item_no=self.item_no,
                                      asset_tran_log_operate_type="decrease_fee")[0]
        Assert.assert_match_json({"asset_tran_log_amount": -1500, "asset_tran_log_operator_name": "系统"}, tran_log)

    @pytest.mark.skip
    def test_offline_repay_mutile_repay(self, setup):
        # 先逾期
        late_day = 5
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i)
            refresh_late_fee(self.item_no)

        # 进行三次还款
        resp, _ = repay_offline_withhold_apply(item_no=self.item_no)
        serial_no1 = resp["content"]["data"]["order_no"]
        request_no1 = resp["content"]["data"]["request_no"]
        repay_offline_withhold_confirm(item_no=self.item_no, request_no=request_no1, transaction_no=get_random_num())

        resp, _ = repay_offline_withhold_apply(item_no=self.item_no)
        serial_no2 = resp["content"]["data"]["order_no"]
        request_no2 = resp["content"]["data"]["request_no"]
        repay_offline_withhold_confirm(item_no=self.item_no, request_no=request_no2, transaction_no=get_random_num())

        resp, _ = repay_offline_withhold_apply(item_no=self.item_no)
        serial_no3 = resp["content"]["data"]["order_no"]
        request_no3 = resp["content"]["data"]["request_no"]
        repay_offline_withhold_confirm(item_no=self.item_no, request_no=request_no3, transaction_no=get_random_num())

        withhold = {"withhold_channel": "offlinerepay",
                    "payment_type": "",
                    "withhold_card_num": "enc_03_3573347754854320128_693",
                    "withhold_amount": 121212,
                    "sign_company": "amberstar1",
                    "repay_type": "overdue",
                    "trade_type": "OFFLINE_WITHHOLD"}
        # 还款并检查数据
        payment_card_num1 = insert_account_statement_record(amount=121212)
        repay_offline_withhold_deal(serial_no=serial_no1, request_no=request_no1, status="success",
                                    trade_id=payment_card_num1)
        self.run_all_task_after_repay_success()

        check_withhold_success_data(serial_no1, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=115712, repaid_interest_amount=3500,
                         repaid_late_amount=2000, repaid_amount=121212, decrease_late_amount=500, late_amount=2000,
                         balance_amount=384288)

        # 还款并检查数据
        payment_card_num2 = insert_account_statement_record(amount=121212)
        repay_offline_withhold_deal(serial_no=serial_no2, request_no=request_no2, status="success",
                                    trade_id=payment_card_num2)
        self.run_all_task_after_repay_success()

        # todo check_withhold_success_data(serial_no2, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=230924, repaid_interest_amount=3500,
                         repaid_late_amount=2000, repaid_amount=236424, decrease_late_amount=500, late_amount=2000,
                         balance_amount=269076)

        # 还款并检查数据
        payment_card_num3 = insert_account_statement_record(amount=500000)
        repay_offline_withhold_deal(serial_no=serial_no3, request_no=request_no3, status="success",
                                    trade_id=payment_card_num3)
        self.run_all_task_after_repay_success()

        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_late_amount=2000, repaid_amount=505500, decrease_late_amount=500, late_amount=2000,
                         asset_status="payoff")

    def test_offline_repay_apply(self, setup):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_url_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key = resp["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(merchant_key, project_num_loan_channel_amount, 3)
        Assert.assert_match_json({"code": 0, "message": "Transaction Processing",
                                  "data": {"type": "URL",
                                           "content": "https://rzp.io/i/nQR3ymulq"}},
                                 resp["content"])

        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_account_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key = resp["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(merchant_key, project_num_loan_channel_amount, 3)
        Assert.assert_match_json({"code": 0, "message": "Transaction Processing",
                                  "data": {"type": "ACCOUNT",
                                           "content": "{\n  \"bank_code\" : \"HDFC0000944\",\n  "
                                                      "\"bank_name\" : \"HDFC\",\n  "
                                                      "\"vpa_account\" : null,\n  "
                                                      "\"expire_time\" : \".*\",\n  "
                                                      "\"bank_account\" : \"50200068003498\",\n  "
                                                      "\"bank_user_name\" : \"SHAURYA RAJ VERMA\"\n}"}},
                                 resp["content"])

        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_upi_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key = resp["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(merchant_key, project_num_loan_channel_amount, 3)
        Assert.assert_match_json({"code": 0, "message": "Transaction Processing",
                                  "data": {"type": "ACCOUNT",
                                           "content": "{\n  \"bank_code\" : \"HDFC0000944\",\n  "
                                                      "\"bank_name\" : \"HDFC\",\n  "
                                                      "\"vpa_account\" : \"50200068003498\",\n  "
                                                      "\"expire_time\" : \".*\",\n  "
                                                      "\"bank_account\" : null,\n  "
                                                      "\"bank_user_name\" : \"SHAURYA RAJ VERMA\"\n}"}},
                                 resp["content"])

    def test_offline_repay_confirm(self, setup):
        # 代扣序列号不存在
        confirm_resp = transaction_confirm(get_random_str())
        Assert.assert_match_json({"code": 1, "message": "The withholding record does not exist,orderNo:%s" %
                                                        confirm_resp["req"]["data"]["order_no"]},
                                 confirm_resp["content"])
        # 申请代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_account_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key = resp["content"]["data"]["project_list"][0]["order_no"]
        # 代扣状态：处理中
        Assert.assert_equal("process", get_withhold(withhold_serial_no=merchant_key)[0]["withhold_status"])
        confirm_resp = transaction_confirm(merchant_key)
        transaction_no = confirm_resp["req"]["data"]["transaction_no"]
        Assert.assert_equal(transaction_no,
                            get_withhold(withhold_serial_no=merchant_key)[0]["withhold_third_serial_no"])
        Assert.assert_equal(confirm_resp["content"],
                            {"code": 0, "message": "The bank statement was confirmed successfully!", "data": None})

        # 代扣状态：失败
        paysvr_callback(merchant_key, project_num_loan_channel_amount, 3)
        Assert.assert_equal("fail", get_withhold(withhold_serial_no=merchant_key)[0]["withhold_status"])
        confirm_resp = transaction_confirm(merchant_key)
        transaction_no = confirm_resp["req"]["data"]["transaction_no"]
        Assert.assert_equal(transaction_no,
                            get_withhold(withhold_serial_no=merchant_key)[0]["withhold_third_serial_no"])
        Assert.assert_equal(confirm_resp["content"],
                            {"code": 0, "message": "The bank statement was confirmed successfully!", "data": None})

        # 代扣状态：成功
        update_withhold(merchant_key, withhold_third_serial_no="")
        paysvr_callback(merchant_key, project_num_loan_channel_amount, 2)
        Assert.assert_equal("success", get_withhold(withhold_serial_no=merchant_key)[0]["withhold_status"])
        confirm_resp = transaction_confirm(merchant_key)
        Assert.assert_equal(confirm_resp["content"],
                            {"code": 1, "message": "Withholding is already a success,orderNo:%s" % merchant_key,
                             "data": None})

    def test_offline_repay_match_by_query(self, setup):
        # 申请代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_account_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key = resp["content"]["data"]["project_list"][0]["order_no"]
        transaction_confirm(merchant_key, get_random_str())
        withhold = get_withhold(withhold_serial_no=merchant_key)[0]
        self.task.run_task(withhold["withhold_request_no"],
                           "execute_combine_withhold",
                           {"code": 0, "data": {"error_message": "The query interface did not return the "
                                                                 "corresponding bank flow information. Procedure.*"}})

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=121212)
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)

        run_accountStatementSync_by_api()
        self.task.run_task(get_date(day=-1, fmt="%Y-%m-%d"), "paysvr_pull_billing_data", {"code": 0, "message": "同步成功"})
        self.run_all_task_by_serial_no(merchant_key)
        check_asset_data(self.item_no, repaid_principal_amount=117712, repaid_interest_amount=3500,
                         repaid_amount=121212, balance_amount=382288)
        # 再次申请
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_account_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key = resp["content"]["data"]["project_list"][0]["order_no"]

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=121212)
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)

        self.run_all_task_by_serial_no(merchant_key)
        check_asset_data(self.item_no, repaid_principal_amount=238924, repaid_interest_amount=3500,
                         repaid_amount=242424, balance_amount=261076)

    def test_offline_repay_match_by_reverse_match(self, setup):
        # 申请代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_account_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key = resp["content"]["data"]["project_list"][0]["order_no"]
        mock_data = self.mock.update_query_channel_reconci_data(1, amount=self.principal_amount)
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)

        run_accountStatementSync_by_api()
        self.task.run_task(get_date(day=-1, fmt="%Y-%m-%d"), "paysvr_pull_billing_data", {"code": 0, "message": "同步成功"})
        run_initStatusAccountStatementMatchWithholdRecord_by_api()
        self.task.run_task(transaction_no, "account_statement_record_match", {"code": 0, "message": ".*匹配成功.*"})
        self.run_all_task_by_serial_no(merchant_key)
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})

        # 进行数据检查
        withhold = {"withhold_channel": "qpay_kn_ebank",
                    "payment_type": "ebank",
                    "withhold_card_num": self.four_element["data"]["card_num"],
                    "withhold_amount": self.principal_amount,
                    "sign_company": "amberstar1",
                    "repay_type": "advance",
                    "withhold_third_serial_no": str(transaction_no)}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=self.principal_amount - self.interest_amount,
                         repaid_interest_amount=self.interest_amount, repaid_amount=self.principal_amount,
                         balance_amount=self.interest_amount)

    def test_offline_repay_match_by_paysvr_callback(self, setup):
        # 申请代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_account_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key = resp["content"]["data"]["project_list"][0]["order_no"]

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=121212)
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)

        run_accountStatementSync_by_api()
        self.task.run_task(get_date(day=-1, fmt="%Y-%m-%d"), "paysvr_pull_billing_data", {"code": 0, "message": "同步成功"})

        paysvr_callback(merchant_key, int(project_num_loan_channel_amount), 2)
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        check_asset_data(self.item_no, repaid_principal_amount=117712, repaid_interest_amount=3500,
                         repaid_amount=121212, balance_amount=382288)
        # 再次申请
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_account_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key_new = resp["content"]["data"]["project_list"][0]["order_no"]

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=121212)
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key_new, transaction_no)

        paysvr_callback(merchant_key_new, int(project_num_loan_channel_amount), 2)
        self.task.run_task(merchant_key_new, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        check_asset_data(self.item_no, repaid_principal_amount=238924, repaid_interest_amount=3500,
                         repaid_amount=242424, balance_amount=261076)

    def test_offline_repay_latefee_decrease_new(self, setup):
        # 先逾期
        self.update_asset_due_at(-1, refresh=True)
        # 申请代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        self.mock.update_withhold_autopay_ebank_account_success(int(project_num_loan_channel_amount))
        resp = self.loan_active_repay_apply(project_num_loan_channel_amount, "ebank")
        merchant_key = resp["content"]["data"]["project_list"][0]["order_no"]
        # 再逾期
        late_day = 3
        for i in range(1, late_day + 1):
            self.update_asset_due_at(-i, refresh=True)

        mock_data = self.mock.update_query_channel_reconci_data(1, amount=int(project_num_loan_channel_amount),
                                                                finish_at=get_date(day=-2))
        transaction_no = mock_data["data"][0]["channel_order_no"]
        transaction_confirm(merchant_key, transaction_no)

        run_accountStatementSync_by_api()
        self.task.run_task(get_date(day=-1, fmt="%Y-%m-%d"), "paysvr_pull_billing_data",
                           {"code": 0, "message": "同步成功"})

        run_initStatusAccountStatementMatchWithholdRecord_by_api()
        self.task.run_task(transaction_no, "account_statement_record_match", {"code": 0, "message": ".*匹配成功.*"})
        self.run_all_task_by_serial_no(merchant_key)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500, late_amount=500,
                         repaid_late_amount=500, decrease_late_amount=1000, repaid_amount=504000, asset_status="payoff")
