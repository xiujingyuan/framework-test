from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.interface.rbiz.rbiz_global_interface import withhold_refund_offline, \
    available_refund_query, withhold_refund_online, refund_callback, refund_withdraw_callback, asset_settle_debt, \
    paysvr_smart_collect_callback
from biztest.util.db.db_util import DataBase

"""
退款用例集：
1、线下退款成功
2、线上退款成功，通过查询
3、线上退款成功，通过回调
4、线上退款失败，通过代付成功，通过查询
5、线上退款失败，通过代付成功，通过回调
6、线上退款(online)失败后，不在再次发起线上退款(online)，不能发起线下退款，可以发起代付退款(withdraw)
7、线上退款(withdraw)失败后，不能发起线上退款(online)，不能发起线下退款，可以发起代付退款(withdraw)
8、线上退款(online)进行中时，不能重复发起线上退款(online)
9、线上退款(online)进行中时，不能重复发起线上退款(withdraw)
10、线上退款(withdraw)进行中时，不能重复发起线上退款(online)
11、线上退款(withdraw)进行中时，不能重复发起线上退款(withdraw)
12、线上退款代扣订单部分退款(online不能部分退，withdraw可以部分退)
13、线上退款(withdraw)可以多次退款-每次金额小于余额，多余余额后报错
14、线上退款(withdraw)，退完部分后，剩余金额充值到其他资产
15、线上退款(online)，退款过程中，不能发起充值到其他资产
16、线上退款(withdraw)，退款过程中，不能发起充值到其他资产
17、collect还款退款
"""


@pytest.mark.global_rbiz_thailand
@pytest.mark.global_rbiz_refund
class TestRbizRefund(BaseGlobalRepayTest):

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass
        request.addfinalizer(teardown)
        super(TestRbizRefund, self).init()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    def test_offline_refund_success(self, setup):
        loan__amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan__amount, no_loan_amount)

        refund_resp = withhold_refund_offline(self.item_no, sn1, refund_amount + 100, "6213945677921542",
                                              "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": "申请退款的金额大于代扣充值[%s]剩余金额，" % sn1, "data": None},
                                 refund_resp["content"])
        refund_resp = withhold_refund_offline(self.item_no, sn1, refund_amount, "6213945677921542",
                                              "skypay_test_withdraw")
        resp, req_url = available_refund_query(self.item_no)
        available_resp = {
            "item_no": self.item_no,
            "refund_no": refund_resp["content"]["data"]["refund_no"],
            "refund_withhold_serial_no": sn1,
            "refund_status": 2
        }
        check_available_refund_response(resp["content"], **available_resp)

    def test_online_refund_success_by_refund_by_query(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        refund_sn = resp["content"]["data"]["refund_no"]
        check_refund_request(refund_sn, refund_request_status="ready", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="ready", refund_result_channel="auto_thailand_channel",
                            refund_result_finish_at="1000-01-01")
        # 退款请求paysvr
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 2)
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refunding", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="process", refund_result_channel="refund_apply_channel",
                            refund_result_finish_at="1000-01-01")
        # 查询退款结果
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refund_success", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="success", refund_result_channel="refund_query_channel")

    def test_online_refund_success_by_refund_by_callback(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        refund_sn = resp["content"]["data"]["refund_no"]
        check_refund_request(refund_sn, refund_request_status="ready", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="ready", refund_result_channel="auto_thailand_channel",
                            refund_result_finish_at="1000-01-01")
        # 退款请求paysvr
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 3)
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refunding", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="process", refund_result_channel="refund_apply_channel",
                            refund_result_finish_at="1000-01-01")
        # 查询退款结果
        refund_callback(sn1, 2)
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refund_success", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="success", refund_result_channel="refund_callback_channel")

    def test_online_refund_success_by_withdraw_by_query(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        refund_sn = resp["content"]["data"]["refund_no"]
        check_refund_request(refund_sn, refund_request_status="ready", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="ready", refund_result_channel="auto_thailand_channel",
                            refund_result_finish_at="1000-01-01")
        # 退款请求paysvr
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 3)
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refunding", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="process", refund_result_channel="refund_apply_channel",
                            refund_result_finish_at="1000-01-01")
        # 查询退款结果
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refund_fail", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="fail", refund_result_channel="refund_query_channel")
        check_withdraw(refund_sn, withdraw_status="ready", withdraw_channel="skypay_test_withdraw",
                       withdraw_finish_at="1000-01-01")
        # 发起退款代付
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=2)
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn,
                             refund_request_status="withdrawing", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="fail", refund_result_channel="refund_query_channel")
        check_withdraw(refund_sn, withdraw_status="process", withdraw_channel="test_channel_withdraw",
                       withdraw_finish_at="1000-01-01")
        # 查询退款代付结果
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn,
                             refund_request_status="withdraw_success", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="fail", refund_result_channel="refund_query_channel")
        check_withdraw(refund_sn, withdraw_status="success", withdraw_channel="test_channel_withdraw")

    def test_online_refund_success_by_withdraw_by_callback(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        refund_sn = resp["content"]["data"]["refund_no"]
        check_refund_request(refund_sn, refund_request_status="ready", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="ready", refund_result_channel="auto_thailand_channel",
                            refund_result_finish_at="1000-01-01")
        # 退款请求paysvr
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 2)
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refunding", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="process", refund_result_channel="refund_apply_channel",
                            refund_result_finish_at="1000-01-01")
        # 查询退款结果
        refund_callback(sn1, 3)
        self.task.run_task(sn1, "refund_online")
        check_refund_request(refund_sn,
                             refund_request_status="refund_fail", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="fail", refund_result_channel="refund_callback_channel")
        check_withdraw(refund_sn, withdraw_status="ready", withdraw_channel="skypay_test_withdraw",
                       withdraw_finish_at="1000-01-01")
        # 发起退款代付
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=3)
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn,
                             refund_request_status="withdrawing", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="fail", refund_result_channel="refund_callback_channel")
        check_withdraw(refund_sn, withdraw_status="process", withdraw_channel="test_channel_withdraw",
                       withdraw_finish_at="1000-01-01")
        # 查询退款代付结果
        refund_withdraw_callback(sn1, 2)
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn,
                             refund_request_status="withdraw_success", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="fail", refund_result_channel="refund_callback_channel")
        check_withdraw(refund_sn, withdraw_status="success", withdraw_channel="test_channel_withdraw")

    def test_refund_online_fail_repead_fail(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)

        # 第一次退款失败
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        refund_sn = resp["content"]["data"]["refund_no"]
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 3)
        self.task.run_task(sn1, "refund_online")
        self.task.run_task(sn1, "refund_online")
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=3)
        self.task.run_task(sn1, "refund_withdraw")
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn,
                             refund_request_status="withdraw_fail", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="fail", refund_result_channel="refund_query_channel")
        check_withdraw(refund_sn, withdraw_status="fail", withdraw_channel="test_channel_withdraw")

        # 第二次重新退款，不能退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542",
                                      "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": "退款请求失败，请稍后重试！"}, resp["content"])

    def test_refund_online_fail_offline_success(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)

        # 线上退款失败
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        refund_sn = resp["content"]["data"]["refund_no"]
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 3)
        self.task.run_task(sn1, "refund_online")
        self.task.run_task(sn1, "refund_online")
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=3)
        self.task.run_task(sn1, "refund_withdraw")
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn,
                             refund_request_status="withdraw_fail", refund_request_channel="skypay_test_withdraw")
        check_refund_result(refund_sn, refund_result_status="fail", refund_result_channel="refund_query_channel")
        check_withdraw(refund_sn, withdraw_status="fail", withdraw_channel="test_channel_withdraw")

        # 线下退款提示不能退款
        resp = withhold_refund_offline(self.item_no, sn1, refund_amount, "6213945677921542",
                                       "skypay_test_withdraw")
        Assert.assert_match_json({"code": 0, "message": "退款信息流补录成功！"}, resp["content"])

    def test_refund_online_process_can_not_refund_online(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起退款
        withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 退款请求paysvr
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 3)
        self.task.run_task(sn1, "refund_online")
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 查询退款结果
        self.task.run_task(sn1, "refund_online")
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 发起退款代付
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=2)
        self.task.run_task(sn1, "refund_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 查询退款代付结果
        self.task.run_task(sn1, "refund_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": r"该笔代扣充值\[.*\]余额为零，无法退款"},
                                 resp["content"])

    def test_refund_online_process_can_not_refund_withdraw(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起退款
        withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 退款请求paysvr
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 3)
        self.task.run_task(sn1, "refund_online")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 查询退款结果
        self.task.run_task(sn1, "refund_online")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 发起退款代付
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=2)
        self.task.run_task(sn1, "refund_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 查询退款代付结果
        self.task.run_task(sn1, "refund_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 1, "message": r"该笔代扣充值\[.*\]余额为零，无法退款"},
                                 resp["content"])

    def test_refund_withdraw_process_can_not_refund_online(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起代付退款
        withhold_refund_online(self.item_no, sn1, refund_amount - 100, "6213945677921542",
                               "skypay_test_withdraw", "WITHDRAW")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 发起退款代付
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=3)
        self.task.run_task(sn1, "refund_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 查询退款代付结果
        refund_withdraw_callback(sn1, 2)
        self.task.run_task(sn1, "refund_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw")
        Assert.assert_match_json({"code": 1, "message": "退款请求失败，请稍后重试！"}, resp["content"])

    def test_refund_withdraw_process_can_not_refund_withdraw(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起代付退款
        withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 发起退款代付
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=3)
        self.task.run_task(sn1, "refund_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！"}, resp["content"])
        # 查询退款代付结果
        refund_withdraw_callback(sn1, 2)
        self.task.run_task(sn1, "refund_withdraw")
        resp = withhold_refund_online(self.item_no, sn1, 1, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 0, "message": "退款请求成功", "data": {"refund_no": ".*"}}, resp["content"])

    def test_online_refund_part(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起线上退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount - 100, "6213945677921542",
                                      "skypay_test_withdraw", "ONLINE")
        Assert.assert_match_json({"code": 1, "message": "退款请求失败，请稍后重试！", "data": None}, resp["content"])
        # 发起代付退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount - 100, "6213945677921542",
                                      "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 0, "message": "退款请求成功", "data": {"refund_no": ".*"}}, resp["content"])
        refund_sn = resp["content"]["data"]["refund_no"]
        check_refund_request(refund_sn, refund_request_status="ready", refund_request_amount=refund_amount - 100,
                             refund_request_channel="skypay_test_withdraw", refund_request_trade_type="withdraw")
        check_withdraw(refund_sn, withdraw_status="ready", withdraw_channel="skypay_test_withdraw",
                       withdraw_amount=refund_amount - 100, withdraw_finish_at="1000-01-01")
        # 发起退款代付
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=3)
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn, refund_request_status="withdrawing", refund_request_amount=refund_amount - 100,
                             refund_request_channel="skypay_test_withdraw", refund_request_trade_type="withdraw")
        check_withdraw(refund_sn, withdraw_status="process", withdraw_channel="test_channel_withdraw",
                       withdraw_amount=refund_amount - 100, withdraw_finish_at="1000-01-01")
        # 查询退款代付结果
        refund_withdraw_callback(sn1, 2)
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn, refund_request_status="withdraw_success",
                             refund_request_amount=refund_amount - 100,
                             refund_request_channel="skypay_test_withdraw", refund_request_trade_type="withdraw")
        check_withdraw(refund_sn, withdraw_status="success", withdraw_channel="test_channel_withdraw",
                       withdraw_amount=refund_amount - 100)

    def test_online_refund_withdraw_multiple(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 第一次发起部分退款
        resp = withhold_refund_online(self.item_no, sn1, 100, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        refund_sn1 = resp["content"]["data"]["refund_no"]
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=2)
        self.task.run_task(sn1, "refund_withdraw")
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn1, refund_request_status="withdraw_success", refund_request_amount=100,
                             refund_request_channel="skypay_test_withdraw", refund_request_trade_type="withdraw")
        check_withdraw(refund_sn1, withdraw_status="success", withdraw_channel="test_channel_withdraw",
                       withdraw_amount=100)

        # 第二次再次发起部分退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount - 100 - 100, "6213945677921542",
                                      "skypay_test_withdraw", "WITHDRAW")
        refund_sn2 = resp["content"]["data"]["refund_no"]
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=2)
        self.task.run_task(sn1, "refund_withdraw")
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn2, refund_request_status="withdraw_success",
                             refund_request_amount=refund_amount - 200, refund_request_channel="skypay_test_withdraw",
                             refund_request_trade_type="withdraw")
        check_withdraw(refund_sn2, withdraw_status="success", withdraw_channel="test_channel_withdraw",
                       withdraw_amount=refund_amount - 200)

        # 第三次退款金额大于剩余金额
        resp = withhold_refund_online(self.item_no, sn1, 101, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 1, "message": r"申请退款的金额大于代扣充值\[.*\]剩余金额，", "data": None},
                                 resp["content"])

    def test_online_refund_part_settle_to_debt_asset(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起部分退款
        resp = withhold_refund_online(self.item_no, sn1, 100, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        refund_sn = resp["content"]["data"]["refund_no"]
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=2)
        self.task.run_task(sn1, "refund_withdraw")
        self.task.run_task(sn1, "refund_withdraw")
        check_refund_request(refund_sn, refund_request_status="withdraw_success", refund_request_amount=100,
                             refund_request_channel="skypay_test_withdraw", refund_request_trade_type="withdraw")
        check_withdraw(refund_sn, withdraw_status="success", withdraw_channel="test_channel_withdraw",
                       withdraw_amount=100)

        # 共债资产
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type,
                                                         self.four_element)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        channel_key = get_withhold_by_serial_no(sn1)[0]["withhold_channel_key"]
        resp = asset_settle_debt(self.item_no, channel_key)
        Assert.assert_match_json({"code": 0, "data": ".*%s\" : 49900.*" % self.item_no_x_new, "message": "分配到其他资产成功"},
                                 resp["content"])
        Assert.assert_match_json({"code": 0, "data": ".*%s\" : 503500.*" % self.item_no_new, "message": "分配到其他资产成功"},
                                 resp["content"])
        # 发起代付退款
        resp = withhold_refund_online(self.item_no, sn1, refund_amount - 100 - 100, "6213945677921542",
                                      "skypay_test_withdraw", "WITHDRAW")
        Assert.assert_match_json({"code": 1, "message": r"该笔代扣充值\[.*\]余额为零，无法退款"},
                                 resp["content"])

    def test_refund_online_and_settle_not_process(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起退款
        withhold_refund_online(self.item_no, sn1, refund_amount, "6213945677921542", "skypay_test_withdraw")
        channel_key = get_withhold_by_serial_no(sn1)[0]["withhold_channel_key"]
        resp = asset_settle_debt(self.item_no, channel_key)
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！", "data": None}, resp["content"])
        # 退款请求paysvr
        self.mock.mock_global_withhold_refund(sn1)
        self.mock.mock_global_withhold_refund_query(sn1, 3)
        self.task.run_task(sn1, "refund_online")
        resp = asset_settle_debt(self.item_no, channel_key)
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！", "data": None}, resp["content"])
        # 查询退款结果
        self.task.run_task(sn1, "refund_online")
        resp = asset_settle_debt(self.item_no, channel_key)
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！", "data": None}, resp["content"])
        # 发起退款代付
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=2)
        self.task.run_task(sn1, "refund_withdraw")
        resp = asset_settle_debt(self.item_no, channel_key)
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！", "data": None}, resp["content"])
        # 查询退款代付结果
        self.task.run_task(sn1, "refund_withdraw")
        # 再次发起资产余额充值
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type,
                                                         self.four_element)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        resp = asset_settle_debt(self.item_no, channel_key)
        Assert.assert_match_json({"code": 1, "message": ".*余额为零，无法分配其他资产", "data": None}, resp["content"])

    def test_refund_withdraw_and_settle_not_process(self, setup):
        loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        sn1, sn2, refund_amount = self.prepare_repeated_withhold(loan_amount, no_loan_amount)
        # 发起部分代付退款
        resp = withhold_refund_online(self.item_no, sn1, 100, "6213945677921542", "skypay_test_withdraw", "WITHDRAW")
        refund_sn = resp["content"]["data"]["refund_no"]
        # 退款过程中不能发起资产结清操作
        channel_key = get_withhold_by_serial_no(sn1)[0]["withhold_channel_key"]
        resp = asset_settle_debt(self.item_no, channel_key)
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！", "data": None},
                                 resp["content"])
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(sn1, status=2)
        self.task.run_task(sn1, "refund_withdraw")
        resp = asset_settle_debt(self.item_no, channel_key)
        Assert.assert_match_json({"code": 1, "message": "有未完成的退款，请稍后重试！", "data": None},
                                 resp["content"])
        self.task.run_task(sn1, "refund_withdraw")
        # 退款结果校验
        check_refund_request(refund_sn, refund_request_status="withdraw_success", refund_request_amount=100,
                             refund_request_channel="skypay_test_withdraw", refund_request_trade_type="withdraw")
        check_withdraw(refund_sn, withdraw_status="success", withdraw_channel="test_channel_withdraw",
                       withdraw_amount=100)
        # 再次发起资产余额充值
        self.item_no_new, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                         self.source_type,
                                                         self.four_element)
        self.item_no_x_new = asset_import_auto_no_loan(asset_info)
        resp = asset_settle_debt(self.item_no, channel_key)
        Assert.assert_match_json({"code": 0, "data": ".*%s\" : 49900.*" % self.item_no_x_new, "message": "分配到其他资产成功"},
                                 resp["content"])
        Assert.assert_match_json({"code": 0, "data": ".*%s\" : 503500.*" % self.item_no_new, "message": "分配到其他资产成功"},
                                 resp["content"])

    def test_collect_repay_refund(self, setup):
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        total_amount = int(project_num_loan_channel_amount) + int(project_num_no_loan_amount)
        resp, req = paysvr_smart_collect_callback(self.item_no, total_amount + 3000)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success()
        # 发起代付退款
        resp = withhold_refund_online(self.item_no, merchant_key, 1000, "6213945677921542",
                                      "skypay_test_withdraw", "WITHDRAW")
        refund_sn1 = resp["content"]["data"]["refund_no"]
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(merchant_key, status=2)
        self.task.run_task(merchant_key, "refund_withdraw")
        self.task.run_task(merchant_key, "refund_withdraw")
        check_refund_request(refund_sn1, refund_request_status="withdraw_success", refund_request_amount=1000,
                             refund_request_channel="skypay_test_withdraw", refund_request_trade_type="withdraw")
        check_withdraw(refund_sn1, withdraw_status="success", withdraw_channel="test_channel_withdraw",
                       withdraw_amount=1000)

        resp, req = paysvr_smart_collect_callback(self.item_no, 3000)
        merchant_key = req["data"]["merchant_key"]
        channel_key = req["data"]["channel_key"]
        self.task.run_task(channel_key, "offline_withhold_process", {"code": 0, "message": "处理回调成功！"})
        self.run_all_task_after_repay_success()
        # 发起线上退款
        resp = withhold_refund_online(self.item_no, merchant_key, 3000, "6213945677921542",
                                      "skypay_test_withdraw", "ONLINE")
        refund_sn2 = resp["content"]["data"]["refund_no"]
        self.mock.mock_global_withhold_refund(merchant_key)
        self.mock.mock_global_withhold_refund_query(merchant_key, 3)
        self.task.run_task(merchant_key, "refund_online")
        self.task.run_task(merchant_key, "refund_online")
        self.mock.update_withdraw_apply_success()
        self.mock.mock_global_withdraw_query_for_rbiz(merchant_key, status=2)
        self.task.run_task(merchant_key, "refund_withdraw")
        self.task.run_task(merchant_key, "refund_withdraw")
        check_refund_request(refund_sn2, refund_request_status="withdraw_success",
                             refund_request_amount=3000, refund_request_channel="skypay_test_withdraw",
                             refund_request_trade_type="online")
        check_withdraw(refund_sn2, withdraw_status="success", withdraw_channel="test_channel_withdraw",
                       withdraw_amount=3000)
