from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.global_rbiz.global_rbiz_kv_config import update_tha_rbiz_paysvr_config
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, paysvr_smart_collect_callback
from biztest.util.db.db_util import DataBase

"""
共债资产寻找原则，先找account_no对应资产，再找本资产的ref，再找最早放款成功的小单，再还对应的大单，以此类推
最后仍然有多余的，放到account中
罚息用例集：
1、开户成功（印度+墨西哥）
2、开户失败后，重新开户
3、收到还款回调，未能匹配到任何资产
4、收到还款回调，找到原资产，资产已经结清，同时无其他共债待还资产（有withhold，order_monunt为0，detail无，充值到account）
5、收到还款回调，找到原资产，资产已经结清，有其他共债待还资产，共债未结清
6、收到还款回调，找到原资产，资产已经结清，有其他共债待还资产，共债刚好结清
7、收到还款回调，找到原资产，资产已经结清，有其他共债待还资产，仍有多余，放到account
8、收到还款回调，找到原资产，无代扣中的订单
9、收到还款回调，找到原资产，有非collect代扣中的订单--可以充值并还款
10、收到还款回调，找到原资产，有非collect代扣失败的订单--新建withhold记录
11、收到还款回调，同资产有多个回调一起回来，顺序处理
12、收到还款回调，不同资产多个回调一起回来，并发处理
13、收到还款回调，找到原资产，回调金额小于资产待还金额-资产未结清
14、收到还款回调，找到原资产，回调金额等于资产待还金额--资产结清
15、收到还款回调，找到原资产，回调金额大于资产待还金额，同时无其他共债待还资产--剩余金额在account内
16、收到还款回调，找到原资产，回调金额大于资产待还金额，有其他共债待还资产--剩余金额还到共债资产
"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.collect_repay
class TestRbizCollectRepay(BaseGlobalRepayTest):

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizCollectRepay, self).init()
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e")
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type,
                                                     self.four_element)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def test_collect_register_success(self, setup):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        # 印度开户成功
        self.mock.update_withold_auto_register_success()
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          payment_type="collect")
        Assert.assert_match_json({"code": 0,
                                  "message": "Transaction Processing",
                                  "data": {"type": "collect",
                                           "content": '{\n  "receiver_account" : "",\n  "receiver_vpa_qrcode" : "da'
                                                      'ta.*",\n  "receiver_vpa" : "enc_03_3810939474465529856_444",\n  '
                                                      '"bank_account" : null,\n  "withhold_channel" : ".*",\n  '
                                                      '"expire_time" : null\n}',
                                           'project_list': None}},
                                 resp_combo_active["content"])
        # 墨西哥开户成功
        self.mock.update_withold_auto_register_success_for_mex()
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          payment_type="collect")
        Assert.assert_match_json({"code": 0,
                                  "message": "Transaction Processing",
                                  "data": {"type": "collect",
                                           "content": '{\n  "receiver_account" : ".*",\n  "receiver_vpa_qrcode" : '
                                                      'null,\n  "receiver_vpa" : "",\n  "bank_account" : null,\n  '
                                                      '"withhold_channel" : ".*",\n  "expire_time" : "2023.*"\n}',
                                           'project_list': None}},
                                 resp_combo_active["content"])

    def test_collect_register_retry_success(self, setup):
        self.mock.update_withold_auto_register_success(1)
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          payment_type="collect")
        Assert.assert_match_json({"code": 1,
                                  "message": "Transaction Fail",
                                  "data": {"error_code": "E20013",
                                           "project_list": None}},
                                 resp_combo_active["content"])
        self.mock.update_withold_auto_register_success(0)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          payment_type="collect")
        Assert.assert_match_json({"code": 0,
                                  "message": "Transaction Processing",
                                  "data": {"type": "collect",
                                           "content": '{\n  "receiver_account" : "",\n  "receiver_vpa_qrcode" : "da'
                                                      'ta.*",\n  "receiver_vpa" : "enc_03_3810939474465529856_444",\n  '
                                                      '"bank_account" : null,\n  "withhold_channel" : ".*",\n  '
                                                      '"expire_time" : null\n}',
                                           'project_list': None}},
                                 resp_combo_active["content"])

    def test_collect_callback_find_no_asset(self):
        resp, req = paysvr_smart_collect_callback("item_no_12121212121212", 1212)
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process",
                           {"code": 1, "message": "item_no_12121212121212资产不存在"})

    def test_collect_callback_asset_already_payoff_no_debt_asset(self, setup):
        # 进行正常还款，结清资产
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2)
        self.run_all_task_after_repay_success()
        # 线下还款进行回调
        resp, req = paysvr_smart_collect_callback(self.item_no, 1212)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([merchant_key, channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay",
                           {"code": 0, "message": "资产%s代扣.*没有对应的withhold_detail" % self.item_no})

    def test_collect_callback_asset_already_payoff_find_debt_asset_amount_less(self, setup):
        # 进行正常还款，结清资产
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2)
        self.run_all_task_after_repay_success()
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type,
                                                         self.four_element)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 线下还款进行回调
        resp, req = paysvr_smart_collect_callback(self.item_no, 1212)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([merchant_key, channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no_new, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 1212,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no_new, repaid_interest_amount=1212, repaid_amount=1212, balance_amount=502288)

    def test_collect_callback_asset_already_payoff_find_debt_asset_amount_equal(self, setup):
        # 进行正常还款，结清资产
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2)
        self.run_all_task_after_repay_success()
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type,
                                                         self.four_element)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 线下还款进行回调
        resp, req = paysvr_smart_collect_callback(self.item_no, int(project_num_loan_channel_amount) +
                                                  int(project_num_no_loan_amount))
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([merchant_key, channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no_new, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": int(project_num_loan_channel_amount) + int(project_num_no_loan_amount),
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no_new, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x_new, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_collect_callback_asset_already_payoff_find_debt_asset_amount_more(self, setup):
        # 进行正常还款，结清资产
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2)
        self.run_all_task_after_repay_success()
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type,
                                                         self.four_element)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 线下还款进行回调
        resp, req = paysvr_smart_collect_callback(self.item_no, int(project_num_loan_channel_amount) +
                                                  int(project_num_no_loan_amount) + 100)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([merchant_key, channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no_new, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": int(project_num_loan_channel_amount) + int(project_num_no_loan_amount) + 100,
                    "order_amount": int(project_num_loan_channel_amount) + int(project_num_no_loan_amount),
                    "balance_amount": 100,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no_new, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x_new, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_collect_callback_find_no_withhold(self, setup):
        resp, req = paysvr_smart_collect_callback(self.item_no, 1212)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([merchant_key, channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 1212,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_interest_amount=1212, repaid_amount=1212, balance_amount=502288)

    def test_collect_callback_find_normal_process_receipt(self, setup):
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)

        resp, req = paysvr_smart_collect_callback(self.item_no, 1212)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "processWithholdEnd", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 1212,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_interest_amount=1212, repaid_amount=1212, balance_amount=502288)

    def test_collect_callback_find_normal_failed_receipt(self, setup):
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 3)

        resp, req = paysvr_smart_collect_callback(self.item_no, 1212)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([merchant_key, channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 1212,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_interest_amount=1212, repaid_amount=1212, balance_amount=502288)

    def test_collect_callback_mutile_callback_same_asset(self, setup):
        # 线下还款进行回调
        resp, req = paysvr_smart_collect_callback(self.item_no, 1212)
        merchant_key_1 = req["data"]["merchant_key"]
        channel_key_1 = req["data"]["channel_key"]
        resp, req = paysvr_smart_collect_callback(self.item_no, 1212)
        channel_key_2 = req["data"]["channel_key"]

        self.task.run_task(channel_key_1, "offline_withhold_process",
                           {"code": 0, "message": "处理回调成功！"})
        self.task.run_task(channel_key_2, "offline_withhold_process",
                           {"code": 2, "message": ".*存在还款中的collect代扣记录"})

        self.task.run_task(merchant_key_1, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key_1, "processWithholdEnd", {"code": 0, "message": "Receive the success"})
        self.task.run_task(channel_key_2, "offline_withhold_process",
                           {"code": 2, "message": ".*存在collect还未还款成功的代扣记录"})

        self.task.run_task(merchant_key_1, "assetWithholdOrderRecharge", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(channel_key_2, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})

    def test_collect_callback_mutile_callback_diff_asset(self, setup):
        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type,
                                                         self.four_element)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        # 线下还款进行回调
        resp, req = paysvr_smart_collect_callback(self.item_no, 1212)
        merchant_key_1 = req["data"]["merchant_key"]
        channel_key_1 = req["data"]["channel_key"]
        resp, req = paysvr_smart_collect_callback(self.item_no_new, 1212)
        merchant_key_2 = req["data"]["merchant_key"]
        channel_key_2 = req["data"]["channel_key"]

        self.task.run_task(channel_key_1, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.task.run_task(channel_key_2, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})

        self.task.run_task(merchant_key_1, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key_2, "withhold_callback_process", {"code": 0, "message": "Receive the success"})

        self.task.run_task(merchant_key_1, "processWithholdEnd", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key_2, "processWithholdEnd", {"code": 0, "message": "Receive the success"})

        self.task.run_task(merchant_key_1, "assetWithholdOrderRecharge", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(merchant_key_2, "assetWithholdOrderRecharge", {"code": 0, "message": "资产还款成功"})

        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(self.item_no_new, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})

    def test_collect_callback_amount_less(self, setup):
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                      payment_type="collect")

        resp, req = paysvr_smart_collect_callback(self.item_no, 1212)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 1212,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_interest_amount=1212, repaid_amount=1212, balance_amount=502288)

    def test_collect_callback_amount_equal(self, setup):
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                      payment_type="collect")

        resp, req = paysvr_smart_collect_callback(self.item_no, int(project_num_loan_channel_amount) +
                                                  int(project_num_no_loan_amount))
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(self.item_no_x, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 553500,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_collect_callback_amount_more_no_debt_asset(self, setup):
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                      payment_type="collect")

        resp, req = paysvr_smart_collect_callback(self.item_no, int(project_num_loan_channel_amount) +
                                                  int(project_num_no_loan_amount) + 100)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([channel_key])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(self.item_no_x, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 553600,
                    "order_amount": 553500,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual",
                    "balance_amount": 100}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")

    def test_collect_callback_amount_more_find_debt_asset(self, setup):
        self.item_no_1, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                       self.source_type,
                                                       self.four_element)
        self.item_no_x_1 = asset_import_auto_no_loan(asset_info)

        self.item_no_2, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                       self.source_type,
                                                       self.four_element)
        self.item_no_x_2 = asset_import_auto_no_loan(asset_info)

        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_1)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x_1)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                      payment_type="collect")

        resp, req = paysvr_smart_collect_callback(self.item_no_1, int(project_num_loan_channel_amount) +
                                                  int(project_num_no_loan_amount) + 100)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([channel_key, self.item_no_1])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no_1, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})

        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 553600,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no_1, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x_1, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        check_asset_data(self.item_no, repaid_interest_amount=100, repaid_amount=100,
                         balance_amount=503400, asset_status="repay")

        resp, req = paysvr_smart_collect_callback(self.item_no_2, int(project_num_loan_channel_amount) - 100)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success([merchant_key, channel_key, self.item_no_2])
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no_2, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        check_asset_data(self.item_no_2, repaid_principal_amount=499900, repaid_interest_amount=3500,
                         repaid_amount=503400, balance_amount=100, asset_status="repay")

    @pytest.mark.skip("还不支持减免")
    def test_collect_callback_decrease(self, setup):
        self.mock.update_withold_auto_register_success()
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                      payment_type="collect")

        for i in range(1, 6):
            self.update_asset_due_at(-i, refresh=True)

        resp, req = paysvr_smart_collect_callback(self.item_no, int(project_num_loan_channel_amount) +
                                                  int(project_num_no_loan_amount) + 3000, finished_at=get_date(day=-2))
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success()
        self.task.run_task(merchant_key, "withhold_callback_process", {"code": 0, "message": "Receive the success"})
        self.task.run_task(merchant_key, "assetWithholdOrderRecharge", {"code": 0, "message": "代扣充值成功"})
        self.task.run_task(self.item_no, "assetWithholdOrderRepay", {"code": 0, "message": "资产还款成功"})
        # 进行数据检查
        withhold = {"withhold_channel": "pandapay_test_collect",
                    "payment_type": "collect",
                    "withhold_card_num": self.four_element['data']['card_num'],
                    "withhold_amount": 554500,
                    "sign_company": None,
                    "repay_type": "advance",
                    "trade_type": "MANUAL_WITHHOLD",
                    "order_operate_type": "manual"}
        check_withhold_success_data(merchant_key, **withhold)
        check_asset_data(self.item_no, repaid_interest_amount=1212, repaid_amount=1212, balance_amount=502288)
