# -*- coding: utf-8 -*-
import pytest

from biztest.config.payment_global.global_payment_kv_config import update_cashfree_verify
from biztest.function.global_payment.global_payment_check_function import check_card, check_binding_request, \
    check_binding, check_account
from biztest.function.global_payment.global_payment_db_operation import update_provider, update_channel
from biztest.interface.payment_global.payment_global_interface import auto_bind_tha
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_cashfree import CashfreeMock
from biztest.util.tools.tools import get_four_element_global


class TestIndiaCashfreeBind:
    def setup_class(self):
        self.sign_company = "yomoyo"
        self.channel = "cashfree_%s_verify" % self.sign_company
        update_channel(self.channel, channel_status="1", channel_sign_company_code=self.sign_company)
        update_provider("razorpay", "close")
        update_cashfree_verify(self.sign_company, "5e9807281718270057767a3e")
        self.cashfree_mock = CashfreeMock("18355257123", "123456", "5e9807281718270057767a3e")

    def teardown_class(self):
        update_provider("razorpay", "open")
        update_cashfree_verify(self.sign_company)
        DataBase.close_connects()

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_verify
    def test_account_bind_success_switch_close(self):
        self.cashfree_mock.update_cashfree_account_bind_success("wo shi shui")
        update_cashfree_verify(self.sign_company, "5e9807281718270057767a3e", name_match_switch=False)
        four_element = get_four_element_global()
        self.bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        req, resp = auto_bind_tha(self.sign_company, four_element, "test1",
                                  bank_account_encrypt=self.bank_account_encrypt)
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]
        Assert.assert_match_json({"code": 0,
                                  "data": {"channel_code": "KN_ACCOUNT_NAME_NOT_MATCH",
                                           "channel_message": "the similarity is less than 0.8",
                                           "channel_name": self.channel,
                                           "platform_code": "E20019",
                                           "platform_message": "the similarity is less than 0.8",
                                           "register_name": "wo shi shui"},
                                  "message": "绑卡成功"},
                                 resp,
                                 "绑卡返回结果正确")
        check_account(card_uuid, "account")
        check_binding(card_uuid, "account", 1, self.channel)
        check_binding_request(merchant_key, four_element, 0, req, resp)
        check_card(card_uuid, "account", four_element, 1, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_verify
    def test_account_bind_success_switch_open_name_match(self):
        self.cashfree_mock.update_cashfree_account_bind_success("carltonliu")
        update_cashfree_verify(self.sign_company, "5e9807281718270057767a3e", name_match_switch=True)
        four_element = get_four_element_global()
        self.bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        req, resp = auto_bind_tha(self.sign_company, four_element, "test1",
                                  bank_account_encrypt=self.bank_account_encrypt)
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]
        Assert.assert_match_json({"code": 0,
                                  "data": {"channel_code": "200",
                                           "channel_message": "Bank Account details verified successfully.",
                                           "channel_name": self.channel,
                                           "platform_code": "E20000",
                                           "platform_message": "Bank Account details verified successfully.",
                                           "register_name": "carltonliu"},
                                  "message": "绑卡成功"},
                                 resp,
                                 "绑卡返回结果正确")
        check_account(card_uuid, "account")
        check_binding(card_uuid, "account", 1, self.channel)
        check_binding_request(merchant_key, four_element, 0, req, resp)
        check_card(card_uuid, "account", four_element, 1, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_verify
    def test_account_bind_success_switch_open_name_in_incloude(self):
        self.cashfree_mock.update_cashfree_account_bind_success("Unregistered")
        update_cashfree_verify(self.sign_company, "5e9807281718270057767a3e", name_match_switch=True)
        four_element = get_four_element_global()
        self.bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        req, resp = auto_bind_tha(self.sign_company, four_element, "test1",
                                  bank_account_encrypt=self.bank_account_encrypt)
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]
        Assert.assert_match_json({"code": 0,
                                  "data": {"channel_code": "KN_ACCOUNT_NAME_NOT_CHECK",
                                           "channel_message": "special characters, no checksum required",
                                           "channel_name": self.channel,
                                           "platform_code": "E20000",
                                           "platform_message": "special characters, no checksum required",
                                           "register_name": "Unregistered"},
                                  "message": "绑卡成功"},
                                 resp,
                                 "绑卡返回结果正确")
        check_account(card_uuid, "account")
        check_binding(card_uuid, "account", 1, self.channel)
        check_binding_request(merchant_key, four_element, 0, req, resp)
        check_card(card_uuid, "account", four_element, 1, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_verify
    def test_account_bind_success_switch_open_name_not_match_but_in_rate(self):
        self.cashfree_mock.update_cashfree_account_bind_success("carltonwu")
        update_cashfree_verify(self.sign_company, "5e9807281718270057767a3e", name_match_switch=True)
        four_element = get_four_element_global()
        self.bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        req, resp = auto_bind_tha(self.sign_company, four_element, "test1",
                                  bank_account_encrypt=self.bank_account_encrypt)
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]
        Assert.assert_match_json({"code": 1,
                                  "data": {"channel_code": "KN_ACCOUNT_NAME_NOT_MATCH",
                                           "channel_message": "the similarity is less than 0.8",
                                           "channel_name": self.channel,
                                           "platform_code": "E20019",
                                           "platform_message": "the similarity is less than 0.8",
                                           "register_name": "carltonwu"},
                                  "message": "绑卡失败"},
                                 resp,
                                 "绑卡返回结果正确")
        check_account(card_uuid, "account")
        check_binding(card_uuid, "account", 2, self.channel)
        check_binding_request(merchant_key, four_element, 1, req, resp)
        check_card(card_uuid, "account", four_element, 0, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_verify
    def test_account_bind_fail_switch_open_name_not_match_not_in_rate(self):
        self.cashfree_mock.update_cashfree_account_bind_success("carltonwu")
        update_cashfree_verify(self.sign_company, "5e9807281718270057767a3e", name_match_switch=True)
        four_element = get_four_element_global()
        self.bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        req, resp = auto_bind_tha(self.sign_company, four_element, "test1",
                                  bank_account_encrypt=self.bank_account_encrypt)
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]
        Assert.assert_match_json({"code": 1,
                                  "data": {"channel_code": "KN_ACCOUNT_NAME_NOT_MATCH",
                                           "channel_message": "the similarity is less than 0.8",
                                           "channel_name": self.channel,
                                           "platform_code": "E20019",
                                           "platform_message": "the similarity is less than 0.8",
                                           "register_name": "carltonwu"},
                                  "message": "绑卡失败"},
                                 resp,
                                 "绑卡返回结果正确")
        check_account(card_uuid, "account")
        check_binding(card_uuid, "account", 2, self.channel)
        check_binding_request(merchant_key, four_element, 1, req, resp)
        check_card(card_uuid, "account", four_element, 0, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_verify
    def test_account_bind_fail_not_exist(self):
        self.cashfree_mock.update_cashfree_account_bind_not_exist()
        four_element = get_four_element_global()
        self.bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        req, resp = auto_bind_tha(self.sign_company, four_element, "test1",
                                  bank_account_encrypt=self.bank_account_encrypt)
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]
        Assert.assert_match_json({"code": 1,
                                  "data": {"channel_code": "200",
                                           "channel_message": "Invalid account number or ifsc provided",
                                           "channel_name": "cashfree_yomoyo_verify",
                                           "platform_code": "KN_INVALID_ACCOUNT",
                                           "platform_message": "Invalid account number or ifsc provided"},
                                  "message": "绑卡失败"},
                                 resp,
                                 "绑卡返回结果正确")
        check_account(card_uuid, "account")
        check_binding(card_uuid, "account", 2, self.channel)
        check_binding_request(merchant_key, four_element, 1, req, resp)
        check_card(card_uuid, "account", four_element, 0, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree
    @pytest.mark.global_cashfree_verify
    def test_account_bind_fail_error(self):
        self.cashfree_mock.update_cashfree_account_bind_error()
        four_element = get_four_element_global()
        self.bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        req, resp = auto_bind_tha(self.sign_company, four_element, "test1",
                                  bank_account_encrypt=self.bank_account_encrypt)
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]
        Assert.assert_match_json({"code": 1,
                                  "data": {"channel_code": "422",
                                           "channel_message": "Please provide a valid IFSC code",
                                           "channel_name": self.channel,
                                           "platform_code": "E20018",
                                           "platform_message": "Please provide a valid IFSC code"},
                                  "message": "绑卡失败"},
                                 resp,
                                 "绑卡返回结果正确")
        check_account(card_uuid, "account")
        check_binding(card_uuid, "account", 2, self.channel)
        check_binding_request(merchant_key, four_element, 1, req, resp)
        check_card(card_uuid, "account", four_element, 0, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_verify
    @pytest.mark.global_cashfree
    def test_upi_bind_success(self):
        # cashfree_upi鉴权是同步返回结果的
        update_cashfree_verify(self.sign_company, "5e9807281718270057767a3e", upi_unbind_account_switch=True)
        self.cashfree_mock.update_cashfree_upi_bind_success("carltonliu")
        four_element = get_four_element_global()
        self.mobile_encrypt = four_element["data"]["upi_encrypt"]
        self.upi_encrypt = four_element["data"]["upi_encrypt"]
        self.user_name_encrypt = four_element["data"]["upi_encrypt"]

        # 发起绑卡
        req, resp = auto_bind_tha(self.sign_company, four_element, "test1", upi_encrypt=self.upi_encrypt)
        Assert.assert_match_json({"code": 0,
                                  "data": {"channel_code": "200",
                                           "channel_message": "VPA verification successful",
                                           "channel_name": self.channel,
                                           "platform_code": "E20000",
                                           "platform_message": "VPA verification successful",
                                           "register_name": "carltonliu"},
                                  "message": "绑卡成功"},
                                 resp,
                                 "绑卡返回结果正确")
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]

        check_account(card_uuid, "upi")
        check_binding(card_uuid, "upi", 1, self.channel)
        check_binding_request(merchant_key, four_element, 0, req, resp)
        check_card(card_uuid, "upi", four_element, 1, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_verify
    @pytest.mark.global_cashfree
    def test_upi_bind_success_not_exist_account_switch_open(self):
        # cashfree_upi鉴权是同步返回结果的
        update_cashfree_verify(self.sign_company, "5e9807281718270057767a3e", upi_unbind_account_switch=True)
        self.cashfree_mock.update_cashfree_upi_bind_not_exist()
        four_element = get_four_element_global()
        self.mobile_encrypt = four_element["data"]["upi_encrypt"]
        self.upi_encrypt = four_element["data"]["upi_encrypt"]
        self.user_name_encrypt = four_element["data"]["upi_encrypt"]

        # 发起绑卡
        req, resp = auto_bind_tha(self.sign_company, four_element, "test1", upi_encrypt=self.upi_encrypt)
        Assert.assert_match_json({"code": 0,
                                  "data": {"channel_code": "KN_UPI_UNBIND_ACCOUNT",
                                           "channel_message": "unbind account, no checksum required",
                                           "channel_name": self.channel,
                                           "platform_code": "E20000",
                                           "platform_message": "unbind account, no checksum required"},
                                  "message": "绑卡成功"},
                                 resp,
                                 "绑卡返回结果正确")
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]

        check_account(card_uuid, "upi")
        check_binding(card_uuid, "upi", 1, self.channel)
        check_binding_request(merchant_key, four_element, 0, req, resp)
        check_card(card_uuid, "upi", four_element, 1, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_verify
    @pytest.mark.global_cashfree
    def test_upi_bind_fail_not_exist_account_switch_open(self):
        # cashfree_upi鉴权是同步返回结果的
        update_cashfree_verify(self.sign_company, "5e9807281718270057767a3e", upi_unbind_account_switch=False)
        self.cashfree_mock.update_cashfree_upi_bind_not_exist()
        four_element = get_four_element_global()
        self.mobile_encrypt = four_element["data"]["upi_encrypt"]
        self.upi_encrypt = four_element["data"]["upi_encrypt"]
        self.user_name_encrypt = four_element["data"]["upi_encrypt"]

        # 发起绑卡
        req, resp = auto_bind_tha(self.sign_company, four_element, "test1", upi_encrypt=self.upi_encrypt)
        Assert.assert_match_json({"code": 1,
                                  "data": {"channel_code": "200",
                                           "channel_message": "VPA verification successful",
                                           "channel_name": self.channel,
                                           "platform_code": "E20000",
                                           "platform_message": "VPA verification successful"},
                                  "message": "绑卡失败"},
                                 resp,
                                 "绑卡返回结果正确")
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]

        check_account(card_uuid, "upi")
        check_binding(card_uuid, "upi", 2, self.channel)
        check_binding_request(merchant_key, four_element, 1, req, resp)
        check_card(card_uuid, "upi", four_element, 0, req, resp)

    @pytest.mark.global_payment_india
    @pytest.mark.global_cashfree_verify
    @pytest.mark.global_cashfree
    def test_upi_bind_fail_error(self):
        # cashfree_upi鉴权是同步返回结果的
        self.cashfree_mock.update_cashfree_upi_bind_error()
        four_element = get_four_element_global()
        self.mobile_encrypt = four_element["data"]["upi_encrypt"]
        self.upi_encrypt = four_element["data"]["upi_encrypt"]
        self.user_name_encrypt = four_element["data"]["upi_encrypt"]

        # 发起绑卡
        req, resp = auto_bind_tha(self.sign_company, four_element, "test1", upi_encrypt=self.upi_encrypt)
        Assert.assert_match_json({"code": 1,
                                  "data": {"channel_code": "520",
                                           "channel_message": "Validation attempt failed",
                                           "channel_name": self.channel,
                                           "platform_code": "E20001",
                                           "platform_message": "Validation attempt failed"},
                                  "message": "绑卡失败"},
                                 resp,
                                 "绑卡返回结果正确")
        merchant_key = req["merchant_key"]
        card_uuid = resp["data"]["card_uuid"]

        check_account(card_uuid, "upi")
        check_binding(card_uuid, "upi", 2, self.channel)
        check_binding_request(merchant_key, four_element, 1, req, resp)
        check_card(card_uuid, "upi", four_element, 0, req, resp)
