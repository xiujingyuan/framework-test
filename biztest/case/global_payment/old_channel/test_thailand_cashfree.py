# -*- coding: utf-8 -*-
import pytest

from biztest.config.easymock.easymock_config import global_payment_easy_mock
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import check_binding, \
    check_binding_request, check_card, check_withdraw, check_withdraw_receipt, assert_withdrawandreceipt_process, \
    assert_withdrawandreceipt_success, assert_check_withdraw_withdrawreceipt_initinfo, assert_withdrawandreceipt_fail, \
    assert_withholdandreceipt_process, assert_withholdandreceipt_success, assert_withholdandreceipt_fail, \
    assert_check_withhold_withholdreceipt_initinfo
from biztest.function.global_payment.global_payment_db_function import update_provider_score, \
    update_task_by_task_order_no, \
    update_channel_error
from biztest.interface.payment_global.payment_global_interface import auto_bind, clear_cache, \
    auto_withdraw, run_task_by_order_no, auto_pay, global_withhold_autoRegister, \
    global_autoWithdraw_retry
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_cashfree_mock import CashfreMock
from biztest.util.tools.tools import get_sysconfig, get_item_no, global_encry_data

env = get_sysconfig("--env")
country = get_sysconfig("--country")
provider = "cashfree"
sign_company = "yomoyo"
channel_name_verify = "cashfree_yomoyo_verify"
channel_name_withdraw = "cashfree_yomoyo_withdraw"
channel_name_ebank = "cashfree_yomoyo_ebank"
# channel_name_ebank = "cashfree_yomoyo_sdk"
project_id = "5b9a3ddd3a0f7700206522eb"  # mock
nacos_domain = "nacos-test-ind.starklotus.com"  # nacos


class TestIndiaCashfree:

    # 每个类的前置条件
    def setup_class(cls):
        # 引入mock和nacos
        cls.global_payment_mock = CashfreMock(global_payment_easy_mock)
        cls.global_payment_nacos = PaymentNacos(nacos_domain)
        update_provider_score(1000, provider, sign_company)
        clear_cache()  # 有时候直接修改数据库配置，会有缓存的问题

    # 每个类的最后需要还原之前的修改，并关闭数据库链接
    @classmethod
    def teardown_class(cls):
        cls.global_payment_nacos.update_cashfree_verify()
        cls.global_payment_nacos.update_cashfree_withdraw()
        cls.global_payment_nacos.update_cashfree_ebank()
        cls.global_payment_nacos.update_cashfree_collect()
        update_provider_score(60, provider, sign_company)
        DataBase.close_connects()

    def cashfree_beneficiary(self, token_status, balance_status):
        # 改代付为mock地址
        self.global_payment_nacos.update_cashfree_withdraw(project_id=project_id)
        # 定义用户信息，使用库里已有的信息，不用 self.global_payment_mock.update_fk_userinfo()
        account = {
            "card_uuid": "267146737401987072",
            "user_uuid": "267145582290665472",
            "card_num": "enc_03_3679003761944567808_126",
            "ifsc": "HDFC0000001"
        }
        # account = {
        #     "card_uuid": "267528742916587520",
        #     "user_uuid": "267525883852488704",
        #     "card_num": "enc_03_3678833168796360704_478"
        # }
        # 使用库里已有的信息，已经开户成功的数据不会请求查询和添加受益人接口
        self.global_payment_mock.update_gettoken(token_status)
        self.global_payment_mock.update_balance(balance_status)
        # self.global_payment_mock.update_beneficiary(beneficiary_status, account["card_num"])
        # self.global_payment_mock.update_add_beneficiary(add_beneficiary_status)
        # 发起代付
        req, resp = auto_withdraw(sign_company, account["card_uuid"], account["user_uuid"], "")
        return req, resp, account

    @pytest.mark.global_payment_cashfree_withdraw
    @pytest.mark.parametrize("token, transfer_status,withdraw_status,case_code,case_msg,task_demo",
                             [("500", "", "", "KN_NO_CHANNEL_CODE", "", '{"code": 2, "message": "代付提现处理中"}'),
                              ("200", "500", "", "KN_NO_CHANNEL_CODE", "", '{"code": 2, "message": "代付提现处理中"}'),
                              ("200", "success", "", "KN_REPEAT_ORDER", "KN_REPEAT_ORDER", '{"code": 2, "message": "exception order，pls query"}'),
                              ("200", "fail", "", "FAILED", "test_BENEFICIARY_BANK_OFFLINE", '{"code": 2, "message": "exception order，pls query"}'),
                              ("200", "not_exit", "success", "200", "Transfer completed successfully", '{"code": 2, "message": "代付提现处理中"}'),
                              ("200", "not_exit", "fail", "422", "Transfer request to paytm wallet failed", '{"code": 2, "message": "代付提现处理中"}'),
                              ("200", "not_exit", "process", "201", "Transfer request pending at the bank.", '{"code": 2, "message": "代付提现处理中"}'),
                              ("200", "not_exit", "500", "KN_NO_CHANNEL_CODE", "response data is null", '{"code": 2, "message": "代付提现处理中"}'),
                              pytest.param("200", "fail", "", "KN_REPEAT_ORDER", "KN_REPEAT_ORDER", '{"code": 2, "message": "代付提现处理中"}', marks=pytest.mark.skip)
                              ],
                             ids=["token_500", "pre_500", "exit_success", "exit_fail", "success", "fail", "process", "500", "fail2"])
    # 参数说明：获取token接口code，前置查询接口code，下单接口code，数据库存储code，数据库存储msg，task_memo
    # 场景说明：前置token失败，前置接口500，订单已存在且成功，订单已存在且失败，下单成功，下单失败，下单处理中，下单500
    def test_cashfree_withdraw(self, token, transfer_status, withdraw_status, case_code, case_msg, task_demo):
        req, resp, account = self.cashfree_beneficiary("200", "success")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        # 修改mock，并执行代付task#withdraw
        self.global_payment_mock.update_gettoken(token)
        self.global_payment_mock.update_transfer_status(transfer_status)
        self.global_payment_mock.update_transfer(withdraw_status, resp["data"]["channel_key"])
        run_task_by_order_no(req["merchant_key"], except_json=task_demo)
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], case_code, case_msg)
        # 关闭未完成的task
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_cashfree_withdraw
    @pytest.mark.parametrize("token, transfer_status,case_code,case_msg,task_demo",
                             [("500", "", "200", "Transfer completed successfully", '{"code": 2, "message": "代付订单正在处理中！需要重试！'),
                              ("200", "500", "200", "Transfer completed successfully", '{"code": 2, "message": "代付订单正在处理中！需要重试！'),
                              ("200", "success", "SUCCESS", "Details of transfer with transferId test", '{"code": 0, "message": "代付提现查询成功"}'),
                              ("200", "process", "PENDING", "test_PENDING", '{"code": 2, "message": "代付订单正在处理中！需要重试！"}'),
                              ("200", "fail", "FAILED", "test_BENEFICIARY_BANK_OFFLINE", '{"code": 1, "message": "代付提现查询失败"}')
                              ],
                             ids=["token_500", "500", "success", "process", "fail"])
    # 参数说明：获取token接口code，查询接口code，数据库存储code，数据库存储msg，task_memo
    # 场景说明：前置token失败，查询接口500，查询到成功，查询到处理中，查询到失败
    def test_cashfree_withdraw_Query(self, token, transfer_status, case_code, case_msg, task_demo):
        req, resp, account = self.cashfree_beneficiary("200", "success")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        # 修改mock，并执行代付task#withdraw
        self.global_payment_mock.update_gettoken("200")
        self.global_payment_mock.update_transfer_status("not_exit")
        self.global_payment_mock.update_transfer("success", resp["data"]["channel_key"])
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "200", "Transfer completed successfully")
        # 修改mock，并执行代付task#withdrawQuery
        self.global_payment_mock.update_gettoken(token)
        self.global_payment_mock.update_transfer_status(transfer_status, resp["data"]["channel_key"])
        run_task_by_order_no(req["merchant_key"], except_json=task_demo)
        # 检查withdraw／withdraw_receipt
        if transfer_status == "process":
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], case_code, case_msg)
        else:
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], account["user_uuid"],
                                                           account["card_uuid"], channel_name_withdraw,
                                                           withdraw_type="online")
        if transfer_status == "success":
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], case_code, case_msg, account["ifsc"])
        if transfer_status == "fail":
            assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], case_code, case_msg)
        # 关闭未完成的task
        run_task_by_order_no(req["merchant_key"])
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_cashfree_withdraw
    def test_cashfree_withdraw_fail_retry_success(self):
        req, resp, account = self.cashfree_beneficiary("200", "success")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        # 修改mock，并执行代付task#withdraw
        self.global_payment_mock.update_gettoken("200")
        self.global_payment_mock.update_transfer_status("not_exit")
        self.global_payment_mock.update_transfer("fail", resp["data"]["channel_key"])
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "422", "Transfer request to paytm wallet failed")
        # 需要修改一下查询的mock
        self.global_payment_mock.update_transfer_status("not_exit")
        # 配置错误码（此时我们修改一下错误码配置，确保其为处理中）
        update_channel_error("cashfree", "404", 2, "VERIFY_BANK_CODE,VERIFY,WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "404", "Transfer request to paytm wallet failed")
        # 将刚刚修改的错误码，配置为失败
        update_channel_error("cashfree", "404", 1, "VERIFY_BANK_CODE,VERIFY,WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询失败"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "404", "Transfer request to paytm wallet failed")
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], account["user_uuid"],
                                                       account["card_uuid"], channel_name_withdraw,
                                                       withdraw_type="online")

        # 1、修改mock使下单成功
        self.global_payment_mock.update_gettoken("200")
        self.global_payment_mock.update_balance("success")
        # 2、只换 trade_no 重新发起代付
        req2, resp2 = global_autoWithdraw_retry(sign_company, account["card_uuid"], account["user_uuid"], merchant_key=req["merchant_key"])
        # 执行代付task#withdrawRegister
        run_task_by_order_no(req["merchant_key"])
        # 3、修改mock使下单成功
        self.global_payment_mock.update_gettoken("200")
        self.global_payment_mock.update_transfer_status("not_exit")
        self.global_payment_mock.update_transfer("success", resp2["data"]["channel_key"])
        # 执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw_receipt
        assert_withdrawandreceipt_process(req2["trade_no"], req["merchant_key"], "200", "Transfer completed successfully")
        # 执行代付task#withdrawQuery，订单号不一致
        self.global_payment_mock.update_transfer_status("success", resp["data"]["channel_key"])
        run_task_by_order_no(req["merchant_key"])
        run_task_by_order_no(req["merchant_key"])
        # 执行代付task#withdrawQuery，金额不一致
        self.global_payment_mock.update_transfer_status("success", resp2["data"]["channel_key"], 1000)
        run_task_by_order_no(req["merchant_key"])
        run_task_by_order_no(req["merchant_key"])
        # 执行代付task#withdrawQuery
        self.global_payment_mock.update_transfer_status("success", resp2["data"]["channel_key"])
        run_task_by_order_no(req["merchant_key"])
        assert_withdrawandreceipt_success(req2["trade_no"], req["merchant_key"], "SUCCESS", "Details of transfer with transferId test", account["ifsc"])
        assert_check_withdraw_withdrawreceipt_initinfo(req2["trade_no"], req["merchant_key"], account["user_uuid"],
                                                       account["card_uuid"], channel_name_withdraw,
                                                       withdraw_type="online")

    def test_cashfree_withdraw_unkonw(self):
        req, resp, account = self.cashfree_beneficiary("200", "success")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        # 修改mock，并执行代付task#withdraw
        self.global_payment_mock.update_gettoken("200")
        self.global_payment_mock.update_transfer_status("not_exit")
        self.global_payment_mock.update_transfer("success", resp["data"]["channel_key"])
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "200", "Transfer completed successfully")
        # 需要修改一下查询的mock
        self.global_payment_mock.update_transfer_status("unkonw", resp["data"]["channel_key"])
        run_task_by_order_no(req["merchant_key"])
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "SUCCESS", "Details of transfer with transferId test")
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], account["user_uuid"],
                                                       account["card_uuid"], channel_name_withdraw,
                                                       withdraw_type="online")
        update_task_by_task_order_no(req["merchant_key"], "close")

        req2, resp2, account2 = self.cashfree_beneficiary("200", "success")
        run_task_by_order_no(req2["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        # 修改mock，并执行代付task#withdraw
        self.global_payment_mock.update_gettoken("200")
        self.global_payment_mock.update_transfer_status("not_exit")
        self.global_payment_mock.update_transfer("success", resp["data"]["channel_key"])
        run_task_by_order_no(req2["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req2["trade_no"], req2["merchant_key"], "200", "Transfer completed successfully")
        # 需要修改一下查询的mock
        self.global_payment_mock.update_transfer_status("ERROR", resp2["data"]["channel_key"])
        run_task_by_order_no(req2["merchant_key"])
        assert_withdrawandreceipt_process(req2["trade_no"], req2["merchant_key"], "SUCCESS", "Details of transfer with transferId test")
        assert_check_withdraw_withdrawreceipt_initinfo(req2["trade_no"], req2["merchant_key"], account2["user_uuid"],
                                                       account2["card_uuid"], channel_name_withdraw,
                                                       withdraw_type="online")
        update_task_by_task_order_no(req2["merchant_key"], "close")


    @pytest.mark.global_payment_cashfree_test
    def cashfree_ebank(self, token_status, order_status):
        # 改代扣为mock地址
        self.global_payment_nacos.update_cashfree_ebank(project_id=project_id)
        # 定义用户信息，使用库里已有的信息，不用 self.global_payment_mock.update_fk_userinfo()
        # 发起代扣时，前端不传入card_uuid，程序会用默认的值
        account = {
            "card_uuid": "9100000000000000000",
            "user_uuid": "267122081823457280",
            "card_num": "enc_03_3679136422914695168_339"
        }
        # 修改mock，使下单申请能够成功
        self.global_payment_mock.update_gettoken(token_status)
        self.global_payment_mock.update_order(order_status)
        # 发起代付
        req, resp = auto_pay(sign_company, "ebank", user_uuid=account["user_uuid"])
        return req, resp, account

    @pytest.mark.global_payment_cashfree_ebank
    @pytest.mark.parametrize("order_status,case_code,case_msg",
                             [("success", "ACTIVE", "ACTIVE"),
                              ("fail", "ACTIVE", "ACTIVE"),
                              ("error", "ACTIVE", "ACTIVE"),
                              ("500", "KN_NO_CHANNEL_CODE", "")
                              ], ids=["success", "fail", "error", "500"])
    def test_cashfree_ebank(self, order_status, case_code, case_msg):
        autopay_req, autopay_resp, account = self.cashfree_ebank("success", order_status)
        # 检查数据库中的数据
        if order_status == "success":
            assert_withholdandreceipt_process(autopay_req["merchant_key"], case_code, case_msg)
        else:
            assert_withholdandreceipt_fail(autopay_req["merchant_key"], case_code, case_msg)
        # 需要把查询task关闭，方便后续观察数据，可以观察task#withholdQuery是否被挂起
        update_task_by_task_order_no(autopay_req["merchant_key"], "close")

    @pytest.mark.global_payment_cashfree_ebank
    @pytest.mark.parametrize("order_status,payments_status,case_code,case_msg,task_demo",
                             [("success", "success", "SUCCESS", "TESTMOCK SUCCESS", '{"code": 0, "message": "支付订单交易查询 success"}'),
                              ("process", "", "ACTIVE", "ACTIVE", '{"code": 2, "message": "代扣订单正在处理中！需要重试！"}'),
                              ("expired_status", "null_list", "EXPIRED", "0 attempts", '{"code": 1, "message": "支付订单查询过期"}'),
                              pytest.param("expired_at", "fail_list", "KN_TIMEOUT_CLOSE_ORDER", "2 attempts, TESTMOCK FAILED",
                                           '{"code": 1, "message": "支付订单查询 this link has expired"}',
                                           marks=pytest.mark.skip),
                              ("500", "", "ACTIVE", "ACTIVE", '{"code": 2, "message": "代扣订单正在处理中！需要重试！"}')
                              ], ids=["success", "process", "expired_status", "expired_at", "500"])
    def test_cashfree_ebank_Query(self, order_status, payments_status, case_code, case_msg, task_demo):
        autopay_req, autopay_resp, account = self.cashfree_ebank("success", "success")
        # 检查数据库中的数据
        assert_withholdandreceipt_process(autopay_req["merchant_key"], "ACTIVE", "ACTIVE")
        # 查询订单
        self.global_payment_mock.update_gettoken("success")
        self.global_payment_mock.update_order_status(order_status, autopay_resp["data"]["channel_key"])
        self.global_payment_mock.update_payments_status(payments_status, autopay_resp["data"]["channel_key"])
        run_task_by_order_no(autopay_req["merchant_key"], except_json=task_demo)
        run_task_by_order_no(autopay_req["merchant_key"])
        # 检查数据库中的数据
        if order_status == "process" or order_status == "500":
            assert_withholdandreceipt_process(autopay_req["merchant_key"], case_code, case_msg)
        else:
            assert_check_withhold_withholdreceipt_initinfo(autopay_req["merchant_key"], channel_name_ebank,
                                                           account["user_uuid"], account["card_uuid"],
                                                           account["card_num"],
                                                           autopay_resp["data"]["payment_data"]["redirect_url"])
        if order_status == "success":
            assert_withholdandreceipt_success(autopay_req["merchant_key"], case_code, case_msg, "card", "credit_card")
        if order_status == "expired_status" or order_status == "expired_at":
            assert_withholdandreceipt_fail(autopay_req["merchant_key"], case_code, case_msg)
        # 关闭未完成的task
        update_task_by_task_order_no(autopay_req["merchant_key"], "close")

    @pytest.mark.global_payment_cashfree_collect
    def test_cashfree_collect(self):
        # 改代扣为mock地址
        self.global_payment_nacos.update_cashfree_collect(project_id=project_id)
        # 修改mock，使下单申请能够成功
        self.global_payment_mock.update_gettoken_collect("success")
        self.global_payment_mock.update_register("success", "6600000103")
        self.global_payment_mock.update_register_qrcode("success")
        # 发起代付
        req, resp = global_withhold_autoRegister(sign_company, user_uuid="262042584153587712", amount=125700)
        # 检查数据库中的数据








    def cashfree_verify_bank(self, token_status, verify_status, name=None):
        self.global_payment_nacos.update_cashfree_verify(project_id=project_id)
        account = {
            "test_name": "TEST NAME JOY",  # 使用相同的姓名
            "ifsc": "TEST0001209",  # 使用相同的ifsc
            "card_uuid": get_item_no()[4:],
            "user_uuid": get_item_no()[3:]
        }
        test_name_encry = global_encry_data("name", account["test_name"])
        card_account_encry = global_encry_data("card_number", account["card_uuid"])

        # # 不走mock的时候用这个，需要先去把数据库里的数据删掉
        # account = {
        #     "test_name": "JANE DOE",
        #     "ifsc": "CITI0000001",
        #     "card_uuid": "267146737401987072",
        #     "user_uuid": "267145582290665472"
        # }
        # test_name_encry = "enc_04_2752900383591899136_178"  # 后面检查点会用
        # card_account_encry = ""  # 不mock就传空

        account.update({"test_name_encry": test_name_encry, "card_account_encry": card_account_encry})
        # mock用户中心的返回-bank验卡不需要传入upi
        self.global_payment_mock.update_fk_userinfo(test_name_encry, account["ifsc"], card_account_encry)
        # mock，通道返回的姓名完全匹配
        self.global_payment_mock.update_gettoken(token_status)
        if name is not None:  # 如果传了name，就用传入的，否则就用account里的姓名
            self.global_payment_mock.update_verify_bankDetails(verify_status, name)  # 通道的数据需要明文
        else:
            self.global_payment_mock.update_verify_bankDetails(verify_status, account["test_name"])  # 通道的数据需要明文
        # 发起绑卡
        autobind_req, autobind_resp = auto_bind(sign_company, account["card_uuid"], account["user_uuid"])
        return autobind_req, autobind_resp, account

    def cashfree_verify_vpi(self, token_status, vpi_status, name=None):
        self.global_payment_nacos.update_cashfree_verify(project_id=project_id)
        account = {
            "test_name": "TEST NAME VPA",  # 使用相同的姓名
            "ifsc": "0000000000",  # 使用相同的ifsc
            "card_uuid": get_item_no()[4:],
            "user_uuid": get_item_no()[3:]
        }
        test_name_encry = global_encry_data("name", account["test_name"])
        upi_encry = global_encry_data("card_number", account["card_uuid"] + "@upi")

        # 不走mock的时候用这个，需要先去把数据库里的数据删掉
        # account = {
        #     "test_name": "JANE DOE",
        #     "ifsc": "0000000000",
        #     "card_uuid": "267146737401987072",
        #     "user_uuid": "267145582290665472"
        # }
        # test_name_encry = "enc_04_2752900383591899136_178"  # 后面检查点会用
        # upi_encry = ""  # 不mock就传空

        account.update({"test_name_encry": test_name_encry, "upi_encry": upi_encry})
        # mock用户中心的返回-upi验卡不需要传入bank
        self.global_payment_mock.update_fk_userinfo(test_name_encry, upi=upi_encry)
        # mock，通道返回的姓名完全匹配
        self.global_payment_mock.update_gettoken(token_status)
        if name is not None:  # 如果传了name，就用传入的，否则就用account里的姓名
            self.global_payment_mock.update_verify_upiDetails(vpi_status, name)  # 通道的数据需要明文
        else:
            self.global_payment_mock.update_verify_upiDetails(vpi_status, account["test_name"])  # 通道的数据需要明文
        # 发起绑卡
        autobind_req, autobind_resp = auto_bind(sign_company, account["card_uuid"], account["user_uuid"])
        return autobind_req, autobind_resp, account

    @pytest.mark.global_payment_cashfree_verify
    def test_cashfree_verify_success_bank(self):
        autobind_req, autobind_resp, account = self.cashfree_verify_bank("success", "success")
        # 检查给bc的返回
        Assert.assert_match_json({"code": 0,
                                  "message": "绑卡成功",
                                  "data": {"platform_code": "E20000",
                                           "platform_message": "SUCCESS",
                                           "channel_name": channel_name_verify,
                                           "channel_code": "200",
                                           "channel_message": "Bank Account details verified successfully",
                                           "card_uuid": account["card_uuid"],
                                           "user_uuid": account["user_uuid"],
                                           "register_name_encrypt": account["test_name_encry"],
                                           "unknown_error": 0}},
                                 autobind_resp,
                                 "绑卡返回结果正确")
        # 检查我方数据库的卡信息存储
        check_binding(account["card_uuid"], "account", 1, channel_name_verify, "ind", account["test_name_encry"])
        check_binding_request(autobind_req["merchant_key"], "", 0, autobind_req, autobind_resp, "ind",
                              account["test_name_encry"])
        check_card(autobind_resp["data"]["card_uuid"], "account", "", 1, autobind_req, "ind")

    @pytest.mark.global_payment_cashfree_verify
    def test_cashfree_verify_success_upi(self):
        autobind_req, autobind_resp, account = self.cashfree_verify_vpi("success", "success")
        # 检查给bc的返回
        Assert.assert_match_json({"code": 0,
                                  "message": "绑卡成功",
                                  "data": {"platform_code": "E20000",
                                           "platform_message": "SUCCESS",
                                           "channel_name": channel_name_verify,
                                           "channel_code": "200",
                                           "channel_message": "VPA verification successful",
                                           "card_uuid": account["card_uuid"],
                                           "user_uuid": account["user_uuid"],
                                           "register_name_encrypt": account["test_name_encry"],
                                           "unknown_error": 0}},
                                 autobind_resp,
                                 "绑卡返回结果正确")
        # 检查我方数据库的卡信息存储
        check_binding(account["card_uuid"], "upi", 1, channel_name_verify, "ind", account["test_name_encry"])
        check_binding_request(autobind_req["merchant_key"], "", 0, autobind_req, autobind_resp, "ind",
                              account["test_name_encry"])
        check_card(autobind_resp["data"]["card_uuid"], "upi", "", 1, autobind_req, "ind")

    @pytest.mark.global_payment_cashfree_verify
    def test_cashfree_verify_500(self):
        # mock，一种是在获取token的时候就500，一种是在绑卡的时候响应500
        # autobind_req, autobind_resp, account = self.cashfree_verify_bank("success", "500")
        autobind_req, autobind_resp, account = self.cashfree_verify_bank("500", "success")
        # autobind_req, autobind_resp, account = self.cashfree_verify_vpi("success", "500")
        # 检查给bc的返回，此时channel_code为KN_NO_CHANNEL_CODE，没有register_name；
        # 若涉及到失败自动换通道的逻辑，会走到失败自动换通道逻辑，返回的是切换后的通道，且绑卡为处理中
        Assert.assert_match_json({"code": 1,
                                  "message": "绑卡失败",
                                  "data": {"platform_code": "E20001",
                                           "platform_message": "FAILED",
                                           "channel_name": channel_name_verify,
                                           "channel_code": "KN_NO_CHANNEL_CODE",
                                           "channel_message": "",
                                           "card_uuid": account["card_uuid"],
                                           "user_uuid": account["user_uuid"],
                                           "unknown_error": 0}},
                                 autobind_resp,
                                 "绑卡返回结果正确")
        # 检查我方数据库的卡信息存储，若涉及到失败自动换通道的逻辑，会走到失败自动换通道逻辑，check_binding_request会有两条记录
        check_binding(account["card_uuid"], "account", 2, channel_name_verify, "ind", "")
        check_binding_request(autobind_req["merchant_key"], "", 1, autobind_req, autobind_resp, "ind", "")
        check_card(autobind_resp["data"]["card_uuid"], "account", "", 0, autobind_req, "ind")

    @pytest.mark.global_payment_cashfree_verify
    def test_cashfree_verify_bank_invalid(self):
        autobind_req, autobind_resp, account = self.cashfree_verify_bank("success", "invalid")
        # 检查给bc的返回
        Assert.assert_match_json({"code": 1,
                                  "message": "绑卡失败",
                                  "data": {"platform_code": "E20001",
                                           "platform_message": "FAILED",
                                           "channel_name": channel_name_verify,
                                           "channel_code": "200",
                                           "channel_message": "IFSC code is invalid",
                                           "card_uuid": account["card_uuid"],
                                           "user_uuid": account["user_uuid"],
                                           "register_name_encrypt": account["test_name_encry"],
                                           "unknown_error": 0}},
                                 autobind_resp,
                                 "绑卡返回结果正确")
        # 检查我方数据库的卡信息存储，此时会涉及到换卡逻辑，本用例可能会无法通过
        check_binding(account["card_uuid"], "account", 2, channel_name_verify, "ind", "")
        check_binding_request(autobind_req["merchant_key"], "", 1, autobind_req, autobind_resp, "ind",
                              account["test_name_encry"])
        check_card(autobind_resp["data"]["card_uuid"], "account", "", 0, autobind_req, "ind")

    @pytest.mark.global_payment_cashfree_verify
    def test_cashfree_verify_fail(self):
        autobind_req, autobind_resp, account = self.cashfree_verify_bank("success", "fail")
        # 检查给bc的返回，此时channel_code为通道返回的（我mock了422和520两种，422会走到自动重试的逻辑里），没有register_name
        Assert.assert_match_json({"code": 1,
                                  "message": "绑卡失败",
                                  "data": {"platform_code": "E20001",
                                           "platform_message": "FAILED",
                                           "channel_name": channel_name_verify,
                                           "channel_code": "520",
                                           "channel_message": "Verification attempt failed",
                                           "card_uuid": account["card_uuid"],
                                           "user_uuid": account["user_uuid"],
                                           "unknown_error": 0}},
                                 autobind_resp,
                                 "绑卡返回结果正确")
        # 检查我方数据库的卡信息存储，此时会涉及到换卡逻辑，本用例可能会无法通过
        check_binding(account["card_uuid"], "account", 2, channel_name_verify, "ind", "")
        check_binding_request(autobind_req["merchant_key"], "", 1, autobind_req, autobind_resp, "ind", "")
        check_card(autobind_resp["data"]["card_uuid"], "account", "", 0, autobind_req, "ind")

    def test_cashfree_verify_failname(self):
        autobind_req, autobind_resp, account = self.cashfree_verify_bank("success", "success", "106CREDIT A")
        test_name_encry = global_encry_data("name", "106CREDIT A")
        # 检查给bc的返回，当通道没有返回名字时同名字匹配失败处理，还有一个配置是姓名白名单（不用匹配直接通过）
        Assert.assert_match_json({"code": 1,
                                  "message": "绑卡失败",
                                  "data": {"platform_code": "KN_ACCOUNT_NAME_NOT_MATCH",
                                           "platform_message": "KN_ACCOUNT_NAME_NOT_MATCH",
                                           "channel_name": channel_name_verify,
                                           "channel_code": "KN_ACCOUNT_NAME_NOT_MATCH",
                                           "channel_message": "the similarity is less than 0.88",
                                           "card_uuid": account["card_uuid"],
                                           "user_uuid": account["user_uuid"],
                                           "register_name_encrypt": test_name_encry,
                                           "unknown_error": 0}},
                                 autobind_resp,
                                 "绑卡返回结果正确")
        # 检查我方数据库的卡信息存储，此时会涉及到换卡逻辑，本用例可能会无法通过
        check_binding(account["card_uuid"], "account", 2, channel_name_verify, "ind", "")
        check_binding_request(autobind_req["merchant_key"], "", 1, autobind_req, autobind_resp, "ind", test_name_encry)
        check_card(autobind_resp["data"]["card_uuid"], "account", "", 0, autobind_req, "ind")

    def test_cashfree_verify_upi_no(self):
        autobind_req, autobind_resp, account = self.cashfree_verify_vpi("success", "invalid")
        # 检查给bc的返回
        # 检查我方数据库的卡信息存储，此时会涉及到换卡逻辑，本用例可能会无法通过

    def cashfree_register(self, token_status, balance_status, beneficiary_status, add_beneficiary_status):
        self.global_payment_nacos.update_cashfree_withdraw(project_id=project_id)

        autobind_req, autobind_resp, account = self.cashfree_verify_bank("success", "success")
        card_num_encry = global_encry_data("card_number",
                                           "91|account|{0}|{1}".format(account["card_uuid"], account["ifsc"]))
        # card_num_encry = ""

        # autobind_req, autobind_resp, account = self.cashfree_verify_vpi("success", "success")
        # card_num_encry = global_encry_data("card_number", "91|upi|{0}|{1}".format(account["card_uuid"] + "@upi", account["ifsc"]))

        account.update({"account_card_uuid": account["card_uuid"], "card_num": card_num_encry})
        # 修改mock，使开户能够成功
        self.global_payment_mock.update_gettoken(token_status)
        self.global_payment_mock.update_balance(balance_status)
        self.global_payment_mock.update_beneficiary(beneficiary_status, card_num_encry)
        self.global_payment_mock.update_add_beneficiary(add_beneficiary_status)
        # 发起代付
        req, resp = auto_withdraw(sign_company, account["card_uuid"], account["user_uuid"], amount=1106)
        return req, resp, account

    def test_cashfree_register_success(self):
        # 获取token成功，余额查询成功，受益人不存在，添加受益人成功
        req, resp, account = self.cashfree_register("success", "success", "fail", "success")
        # 执行代付task#withdrawRegister
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        # 检查我方数据库的卡信息存储，此时会将请求参数中的card_num存储为协议号
        # 此时不检查check_binding_request表，因为autobind_req不好获取；；此时不检查card表，因为此时不会写card表
        protocol_info = '{"bene_id":"%s"}' % account["card_num"]
        check_binding(account["card_uuid"], "", 1, channel_name_withdraw, "ind", "", protocol_info)
        # 检查withdraw／withdraw_receipt
        check_withdraw(req["merchant_key"], account, 1, channel_name_withdraw)
        check_withdraw_receipt(req["merchant_key"], account, 0, channel_name_withdraw, "", "")
        # 关闭未完成的task
        update_task_by_task_order_no(req["merchant_key"], "close")

    def test_cashfree_register_fail(self):
        # 获取token成功，余额查询成功，受益人不存在，添加受益人失败
        req, resp, account = self.cashfree_register("success", "success", "fail", "fail")
        # 执行代付task#withdrawRegister，明确为失败的code才会置为开户失败，否则task重试
        run_task_by_order_no(req["merchant_key"])
        # # 检查我方数据库的卡信息存储，此时不会存储到协议号
        # protocol_info = ''
        # check_binding(account["card_uuid"], "account", 2, channel_name_withdraw, "ind", "", protocol_info)
        # # 检查withdraw／withdraw_receipt
        # check_withdraw(req["merchant_key"], account, 3, channel_name_withdraw)
        # check_withdraw_receipt(req["merchant_key"], account, 3, channel_name_withdraw, "KN_BINDING_UNVALID",
        #                            "Post data is empty or not a valid JSON")

    def test_cashfree_register_beneficiary(self):
        # 获取token成功，余额查询成功，受益人存在，此时不会调用添加受益人接口
        req, resp, account = self.cashfree_beneficiary("success", "success", "success", "")
        # 执行代付task#withdrawRegister
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        # 检查我方数据库的卡信息存储，此时不会存储到协议号
        protocol_info = '{"bene_id":"%s"}' % account["card_num"]
        check_binding(account["card_uuid"], "account", 1, channel_name_withdraw, "ind", "", protocol_info)
        # 检查withdraw／withdraw_receipt
        check_withdraw(req["merchant_key"], account, 1, channel_name_withdraw)
        check_withdraw_receipt(req["merchant_key"], account, 0, channel_name_withdraw, "", "")
        # 关闭未完成的task
        update_task_by_task_order_no(req["merchant_key"], "close")

    def test_cashfree_register_500(self):
        # 获取token成功，余额查询成功，受益人不存在，添加受益人接口异常，task重试
        req, resp, account = self.cashfree_register("success", "success", "fail", "500")
        # 执行代付task#withdrawRegister
        run_task_by_order_no(req["merchant_key"],
                             except_json={"code": 2, "message": "%s订单放款开户绑卡失败,重试" % resp["data"]["channel_key"]})
        # 检查我方数据库的卡信息存储，此时不会存储到协议号
        protocol_info = ''
        check_binding(account["card_uuid"], "account", 2, channel_name_withdraw, "ind", "", protocol_info)
        # 检查withdraw／withdraw_receipt
        check_withdraw(req["merchant_key"], account, 1, channel_name_withdraw)
        check_withdraw_receipt(req["merchant_key"], account, 0, channel_name_withdraw, "", "")
        # 关闭未完成的task
        update_task_by_task_order_no(req["merchant_key"], "close")

    def test_cashfree_register_beneficiary500_exit(self):
        # 获取token成功，余额查询成功，受益人接口异常，同受益人不存在处理，继续调用添加受益人接口，接口返回受益人已经存在
        req, resp, account = self.cashfree_register("success", "success", "500", "exit")
        # 执行代付task#withdrawRegister
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "开户成功，已创建代付任务", "data": None})
        # 检查withdraw／withdraw_receipt
        check_withdraw(req["merchant_key"], account, 1, channel_name_withdraw)
        check_withdraw_receipt(req["merchant_key"], account, 0, channel_name_withdraw, "", "")
        # 关闭未完成的task
        update_task_by_task_order_no(req["merchant_key"], "close")

    def test_cashfree_register_balancefail(self):
        # 获取token成功，余额查询失败／余额不足／接口异常，不会收单，也不会去开户
        req, resp, account = self.cashfree_beneficiary("success", "no", "", "")
        # 执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付订单更新成功！"})
        # 检查withdraw／withdraw_receipt
        check_withdraw(req["merchant_key"], account, 3, "route_no_channel")
        check_withdraw_receipt(req["merchant_key"], account, 3, "route_no_channel", "KN_INVALID_CHANNEL",
                               "invalid channel")



