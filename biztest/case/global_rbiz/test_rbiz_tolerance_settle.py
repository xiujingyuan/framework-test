from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.global_rbiz.global_rbiz_kv_config import update_tha_rbiz_paysvr_config, update_rbiz_config
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.function.global_rbiz.rbiz_global_db_function import get_withhold_by_item_no
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, run_assetTolerancePayoffJob_by_api, \
    asset_tolerance_settle, paysvr_smart_collect_callback, withhold_cancel, paysvr_query_tolerance_result
from biztest.util.db.db_util import DataBase


'''
用例集：
1、容差接口：固定比例
2、容差接口：放款本金grant_principal
3、容差接口：剩余本金balance_principal
4、容差接口：最小期次本金min_period_principal
5、容差接口：还款期次本金repay_period_principal
6、容差接口：资产剩余金额balance_asset_amount
7、还款查询task，是否支持金额检查--开关false
8、还款查询task，是否支持金额检查--开关true
9、还款回调任务，是否支持金额检查--开关false
10、还款回调任务，是否支持金额检查--开关true
11、通过job，进行剩余金额拨备减免，检查开关
12、通过job，进行剩余金额拨备减免，存在多个费用进行减免
13、通过api，进行剩余金额拨备减免
14、通过自动触发，进行剩余金额拨备减免
15、容差按期结清
'''


@pytest.mark.global_rbiz_thailand
@pytest.mark.tolerance_settle
class TestRbizToleranceSettle(BaseGlobalRepayTest):
    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizToleranceSettle, self).init()
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
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e")
        update_rbiz_config()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element, 4)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def make_smart_repay_party(self, item_no, amount):
        resp, req = paysvr_smart_collect_callback(item_no, amount)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([item_no, merchant_key, channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})

    def make_asset_repay_party(self, amount):
        self.mock.update_withhold_autopay_ebank_url_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        self.mock.update_withhold_query_success(self.item_no, 1, "auto_thailand_channel")

        # 回调返回金额不一致
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        resp, _ = paysvr_callback(order_no, amount, 2, "auto_thailand_channel")
        Assert.assert_match_json({"code": 0, "message": "Receive the success"}, resp["content"])
        self.run_all_task_after_repay_success()

    def test_query_tolerance_by_fixed(self, setup_4):
        update_rbiz_config(tolerance_type="fixed")
        resp_combo_active = self.combo_active_repay_apply(0, 0, period_list=[1, ])
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(merchant_key)[0]["withhold_request_req_key"]
        self.mock.mock_close_order_success()
        withhold_cancel(request_key, "")
        # 未还款检查
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 140000,
                                           "allow_max_repayment_amount": 142000,
                                           "overdue_days": -7,
                                           "tolerance_amount": 1000,
                                           "allow_repayment": False}},
                                 resp["content"])

        # 部分还款检查
        self.make_smart_repay_party(self.item_no, 12121)
        self.make_smart_repay_party(self.item_no_x, 1212)
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 126667,
                                           "allow_max_repayment_amount": 128667,
                                           "overdue_days": -7,
                                           "tolerance_amount": 1000,
                                           "allow_repayment": False}},
                                 resp["content"])
        # 剩余金额太小检查
        self.make_smart_repay_party(self.item_no, 116300)
        self.make_smart_repay_party(self.item_no_x, 11288)
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 1,
                                           "allow_max_repayment_amount": 1079,
                                           "overdue_days": -7,
                                           "tolerance_amount": 1000,
                                           "allow_repayment": False}},
                                 resp["content"])
        # 资产结清
        self.make_smart_repay_party(self.item_no, 100)
        self.make_smart_repay_party(self.item_no_x, 100)
        resp = paysvr_query_tolerance_result(merchant_key)

        Assert.assert_match_json({"code": 1,
                                  "message": "该期次已经结清",
                                  "data": None},
                                 resp["content"])

    def test_query_tolerance_by_grant_principal(self, setup_4):
        update_rbiz_config(tolerance_type="grant_principal")
        resp_combo_active = self.combo_active_repay_apply(0, 0, period_list=[1, 2])
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(merchant_key)[0]["withhold_request_req_key"]
        withhold_cancel(request_key, "")
        # 未还款检查
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 55000,  # (5000+500)*0.1
                                           "allow_max_repayment_amount": 283000,  # 2820+10
                                           "overdue_days": -7,
                                           "tolerance_amount": 227000,  # 2820-(5000+500)*0.1
                                           "allow_repayment": True}},
                                 resp["content"])
        # 部分还款
        self.make_smart_repay_party(self.item_no, 12121)
        self.make_smart_repay_party(self.item_no_x, 1212)
        resp = paysvr_query_tolerance_result(merchant_key)

        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 55000,  # (5000+500)*0.1
                                           "allow_max_repayment_amount": 269667,  # 2820-121.21-12.12+10
                                           "overdue_days": -7,
                                           "tolerance_amount": 213667,  # 2820-121.21-12.12-(5000+500)*0.1
                                           "allow_repayment": True}},
                                 resp["content"])

    def test_query_tolerance_by_balance_principal(self, setup_4):
        update_rbiz_config(tolerance_type="balance_principal")
        resp_combo_active = self.combo_active_repay_apply(0, 0, period_list=[1, 2])
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(merchant_key)[0]["withhold_request_req_key"]
        withhold_cancel(request_key, "")
        # 未还款检查
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 55000,  # (5000+500)*0.1
                                           "allow_max_repayment_amount": 283000,  # 2820+10
                                           "overdue_days": -7,
                                           "tolerance_amount": 227000,  # 2820-(5000+500)*0.1
                                           "allow_repayment": True}},
                                 resp["content"])
        # 部分还款检查
        self.make_smart_repay_party(self.item_no, 12121)
        self.make_smart_repay_party(self.item_no_x, 1212)
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 54017,  # (5000+500-86.21-12.12)*0.1
                                           "allow_max_repayment_amount": 269667,  # 2820-121.21-12.12+10
                                           "overdue_days": -7,
                                           "tolerance_amount": 214650,  # (2820-121.21-12.12)-265.17
                                           "allow_repayment": True}},
                                 resp["content"])

    def test_query_tolerance_by_min_period_principal(self, setup_4):
        update_rbiz_config(tolerance_type="min_period_principal")
        resp_combo_active = self.combo_active_repay_apply(0, 0, period_list=[1, 2])
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(merchant_key)[0]["withhold_request_req_key"]
        withhold_cancel(request_key, "")
        # 未还款检查
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 13750,  # (1250+125)*0.1
                                           "allow_max_repayment_amount": 283000,
                                           "overdue_days": -7,
                                           "tolerance_amount": 268250,
                                           "allow_repayment": True}},
                                 resp["content"])
        # 部分还款检查
        self.make_smart_repay_party(self.item_no, 12121)
        self.make_smart_repay_party(self.item_no_x, 1212)
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 12767,  # (1163.79+112.88)*0.1
                                           "allow_max_repayment_amount": 269667,  # 2820-121.21-12.12+10
                                           "overdue_days": -7,
                                           "tolerance_amount": 255900,  # (2820-121.21-12.12)-127.67
                                           "allow_repayment": True}},
                                 resp["content"])

    def test_query_tolerance_by_repay_period_principal(self, setup_4):
        update_rbiz_config(tolerance_type="repay_period_principal")
        resp_combo_active = self.combo_active_repay_apply(0, 0, period_list=[1, 2])
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(merchant_key)[0]["withhold_request_req_key"]
        withhold_cancel(request_key, "")
        # 未还款检查
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 27500,  # (1250+1250+125+125)*0.1
                                           "allow_max_repayment_amount": 283000,
                                           "overdue_days": -7,
                                           "tolerance_amount": 254500,  # 282000-27500
                                           "allow_repayment": True}},
                                 resp["content"])
        # 部分还款检查
        self.make_smart_repay_party(self.item_no, 12121)
        self.make_smart_repay_party(self.item_no_x, 1212)
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 26517,  # (1163.79+1250+112.88+125)*0.1
                                           "allow_max_repayment_amount": 269667,  # 2820-121.21-12.12+10
                                           "overdue_days": -7,
                                           "tolerance_amount": 242150,  # (2820-121.21-12.12)-127.67
                                           "allow_repayment": True}},
                                 resp["content"])

    def test_query_tolerance_by_balance_asset_amount(self, setup_4):
        update_rbiz_config(tolerance_type="balance_asset_amount")
        resp_combo_active = self.combo_active_repay_apply(0, 0, period_list=[1, 2])
        merchant_key = resp_combo_active['content']["data"]["project_list"][0]["order_no"]
        request_key = get_withhold_request_by_serial_no(merchant_key)[0]["withhold_request_req_key"]
        withhold_cancel(request_key, "")
        # 未还款检查
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 56400,  # (5140+500)*0.1
                                           "allow_max_repayment_amount": 283000,
                                           "overdue_days": -7,
                                           "tolerance_amount": 225600,  # 282000-56400
                                           "allow_repayment": True}},
                                 resp["content"])
        # 部分还款检查
        self.make_smart_repay_party(self.item_no, 12121)
        self.make_smart_repay_party(self.item_no_x, 1212)
        resp = paysvr_query_tolerance_result(merchant_key)
        Assert.assert_match_json({"code": 0,
                                  "data": {"allow_min_repayment_amount": 55067,  # (5140+500-121.21-12.12)*0.1
                                           "allow_max_repayment_amount": 269667,  # 2820-121.21-12.12+10
                                           "overdue_days": -7,
                                           "tolerance_amount": 213600,  # (2820-121.21-12.12)-127.67
                                           "allow_repayment": True}},
                                 resp["content"])

    def test_query_task_check_amount_false(self, setup):
        """
        还款查询task，是否支持金额检查--开关false
        """
        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]

        # 金额检查开关false
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e", callback_amount_consistent_check=True)

        # 查询返回金额不一致
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel", amount=1234)
        self.task.run_task(request_no, "execute_combine_withhold",
                           {"code": 2, "message": "申请代扣的金额553500和实际扣款的金额不一致1234"})

        # 查询返回金额一致
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel")
        self.task.run_task(request_no, "execute_combine_withhold",
                           {"code": 0, "message": "Transaction Successful"})

        self.run_all_task_after_repay_success()

        # 验证数据 代扣相关
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_query_task_check_amount_true(self, setup):
        """
        还款查询task，是否支持金额检查--开关true
        """
        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]

        # 金额检查开关true
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e", callback_amount_consistent_check=False)

        # 查询返回金额不一致
        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel", amount=1234)
        self.task.run_task(request_no, "execute_combine_withhold",
                           {"code": 0, "message": "Transaction Successful"})
        self.run_all_task_after_repay_success()
        asset_info = get_asset_info_by_item_no(self.item_no_x)[0]
        Assert.assert_match_json({"asset_repaid_amount": "1234"}, asset_info)

        # 再次发起代扣，结清资产
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]

        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel")
        self.task.run_task(request_no, "execute_combine_withhold",
                           {"code": 0, "message": "Transaction Successful"})

        self.run_all_task_after_repay_success()

        # 验证数据 代扣相关
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_callback_check_amount_false(self, setup):
        """
        还款回调任务，是否支持金额检查--开关false
        """
        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        self.mock.update_withhold_query_success(self.item_no, 1, "auto_thailand_channel")

        # 金额检查开关false
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e", callback_amount_consistent_check=True)

        # 回调返回金额不一致
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        resp, _ = paysvr_callback(order_no, 1234, 2, "auto_thailand_channel")
        Assert.assert_match_json({"code": 2, "message": r"Order [%s] callback amount error, repayment system "
                                                        r"[553500],paysvr callback amount [1234]" % order_no},
                                 resp["content"])

        # 回调返回金额一致
        resp, _ = paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2,
                                  "auto_thailand_channel")
        Assert.assert_match_json({"code": 0, "message": "Receive the success"},
                                 resp["content"])

        self.run_all_task_after_repay_success()

        # 验证数据 代扣相关
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_callback_check_amount_true(self, setup):
        """
        还款回调任务，是否支持金额检查--开关true
        """
        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        self.mock.update_withhold_query_success(self.item_no, 1, "auto_thailand_channel")

        # 金额检查开关true
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e", callback_amount_consistent_check=False)

        # 回调返回金额不一致
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        resp, _ = paysvr_callback(order_no, 1234, 2, "auto_thailand_channel")
        Assert.assert_match_json({"code": 0, "message": "Receive the success"}, resp["content"])
        self.run_all_task_after_repay_success()
        asset_info = get_asset_info_by_item_no(self.item_no_x)[0]
        Assert.assert_match_json({"asset_repaid_amount": "1234"}, asset_info)

        # 再次发起代扣，结清资产
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        resp, _ = paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2,
                                  "auto_thailand_channel")
        Assert.assert_match_json({"code": 0, "message": "Receive the success"}, resp["content"])

        self.run_all_task_after_repay_success()

        # 验证数据 代扣相关
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_asset_tolerance_switch(self, setup):
        self.make_asset_repay_party(amount=553000)
        # 开关false
        update_rbiz_config(auto_tolerance=False)
        run_assetTolerancePayoffJob_by_api(term=10000000)
        time.sleep(3)
        task1 = get_task_by_order_no_and_task_type(self.item_no, "toleranceSettle")
        task2 = get_task_by_order_no_and_task_type(self.item_no_x, "toleranceSettle")
        Assert.assert_equal((), task1, "大单生成了toleranceSettle的task")
        Assert.assert_equal((), task2, "小单生成了toleranceSettle的task")

        # 开关true，但是配置金额不满足
        update_rbiz_config(tolerance_amount=1, auto_tolerance=True)
        run_assetTolerancePayoffJob_by_api(term=10000000)
        time.sleep(3)
        task1 = get_task_by_order_no_and_task_type(self.item_no, "toleranceSettle")
        task2 = get_task_by_order_no_and_task_type(self.item_no_x, "toleranceSettle")
        Assert.assert_equal((), task1, "大单生成了toleranceSettle的task")
        Assert.assert_equal((), task2, "小单生成了toleranceSettle的task")

        # 开关true，但是job金额不满足
        update_rbiz_config(tolerance_amount=1000, auto_tolerance=True)
        run_assetTolerancePayoffJob_by_api(toleranceAmount=1, term=10000000)
        time.sleep(3)
        task1 = get_task_by_order_no_and_task_type(self.item_no, "toleranceSettle")
        task2 = get_task_by_order_no_and_task_type(self.item_no_x, "toleranceSettle")
        Assert.assert_equal((), task1, "大单生成了toleranceSettle的task")
        Assert.assert_equal((), task2, "小单生成了toleranceSettle的task")

        # 开关true，且金额满足
        update_rbiz_config(tolerance_amount=1000, auto_tolerance=True)
        run_assetTolerancePayoffJob_by_api(term=10000000)
        task1 = get_task_by_order_no_and_task_type(self.item_no, "toleranceSettle")
        task2 = get_task_by_order_no_and_task_type(self.item_no_x, "toleranceSettle")
        Assert.assert_not_equal((), task1, "大单生成了toleranceSettle的task")
        Assert.assert_equal((), task2, "小单生成了toleranceSettle的task")

        self.task.run_task(self.item_no, "toleranceSettle", {"code": 0})
        self.task.run_task(self.item_no, "provisionRecharge", {"code": 0})
        self.task.run_task(self.item_no, "provisionRepay", {"code": 0})
        check_provision(self.item_no, "tolerance_payoff", 500, "repayprincipal")

    def test_asset_tolerance_mutile_fee_tolerance(self, setup):
        self.make_asset_repay_party(amount=52000)
        params_due_at = {
            "advance_month": 0,
            "advance_day": -80,
            "period": 1,
            "item_no": self.item_no
        }
        update_asset_and_asset_tran_due_at_by_item_no(**params_due_at)
        update_rbiz_config(tolerance_amount=520000, auto_tolerance=True)
        run_assetTolerancePayoffJob_by_api(term=10000000)
        self.task.run_task(self.item_no, "toleranceSettle", {"code": 0})
        self.task.run_task(self.item_no, "provisionRecharge", {"code": 0})
        self.task.run_task(self.item_no, "provisionRepay", {"code": 0})
        check_provision(self.item_no, "tolerance_payoff", 500000, "repayprincipal")
        check_provision(self.item_no, "tolerance_payoff", 1500, "repayinterest")

    def test_asset_tolerance_by_api(self, setup):
        self.make_asset_repay_party(amount=553000)
        # 开关true，切金额满足
        update_rbiz_config(tolerance_amount=1000, auto_tolerance=True)
        asset_tolerance_settle(self.item_no)

        task1 = get_task_by_order_no_and_task_type(self.item_no, "provisionRecharge")
        task2 = get_task_by_order_no_and_task_type(self.item_no_x, "provisionRecharge")
        Assert.assert_not_equal((), task1, "大单生成了provisionRecharge的task_")
        Assert.assert_equal((), task2, "小单生成了provisionRecharge的task_")

        self.task.run_task(self.item_no, "provisionRecharge", {"code": 0})
        self.task.run_task(self.item_no, "provisionRepay", {"code": 0})
        check_provision(self.item_no, "tolerance_payoff", 500, "repayprincipal")

    def test_asset_tolerance_by_auto(self, setup_4):
        self.mock.update_withhold_autopay_ebank_url_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)

        # 回调返回金额不一致
        update_rbiz_config(1000, auto_tolerance=True)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        resp, _ = paysvr_callback(order_no, amount - 500, 2, "auto_thailand_channel")
        self.task.run_task(self.item_no, "withhold_callback_process", {"code": 0})
        self.task.run_task(order_no, "assetWithholdOrderRecharge", {"code": 0})
        self.task.run_task(self.item_no, "toleranceSettle", {"code": 0})
        self.task.run_task(self.item_no, "provisionRecharge", {"code": 0})
        self.task.run_task(self.item_no, "provisionRepay", {"code": 0})
        check_provision(self.item_no, "tolerance_payoff", 500, "repayprincipal")

    def test_asset_tolerance_period(self, setup_4):
        self.mock.update_withhold_autopay_ebank_url_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)

        # 回调返回金额不一致
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        resp, _ = paysvr_callback(order_no, amount - 1000, 2, "auto_thailand_channel")
        self.run_all_task_after_repay_success()
        self.update_asset_due_at(-9, refresh=True)

        # 发起单期减免
        update_rbiz_config(tolerance_amount=1100, auto_tolerance=True)
        run_assetTolerancePayoffJob_by_api(byPeriod=True, term=10000000)
        self.task.run_task(self.item_no, "toleranceSettle", {"code": 0})
        self.task.run_task(self.item_no, "provisionRecharge", {"code": 0})
        self.task.run_task(self.item_no, "provisionRepay", {"code": 0})
        check_provision(self.item_no, "tolerance_payoff", 1000, "repayprincipal")

        # 验证数据
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_amount=128500, decrease_late_amount=9, late_amount=250,
                         balance_amount=385750, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_amount=12500, late_amount=25, balance_amount=37525, asset_status="repay")

        resp, req = paysvr_smart_collect_callback(self.item_no, 124500)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
