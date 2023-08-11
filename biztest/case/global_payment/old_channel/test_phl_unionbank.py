# -*- coding: utf-8 -*-

import pytest

from biztest.config.easymock.easymock_config import global_payment_easy_mock_phl
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import \
    assert_check_withdraw_withdrawreceipt_initinfo, assert_withdrawandreceipt_process, \
    assert_withdrawandreceipt_success, assert_withdrawandreceipt_fail
from biztest.function.global_payment.global_payment_db_function import get_carduuid_bycardnum, update_channel_error
from biztest.function.global_payment.global_payment_db_operation import get_withdraw_receipt_info_by_merchant_key
from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, auto_withdraw, \
    clear_cache
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_phl_unionbank import UnionbankMock
from biztest.util.tools.tools import get_four_element_global, get_guid

provider = "unionbank"
sign_company = "copperstone"
channel_name_withdraw = "unionbank_copperstone_withdraw"
user_uuid = "58042740327317418"
card_uuid = "6621102700001270802"
nacos_domain = "nacos-test-phl.starklotus.com"  # nacos
project_id = "5e9807281718270057767a3e"  # mock


# update 2022.6.9
# unionbank放款没有回调
# unionbank现在测试环境的余额查询跑不通，必须mock的
# unionbank接口异常如订单不存在时的返回和其他通道不一样，现在前置查询只能走通道查
# 用例1：银行账号放款- 发起放款请求成功，查询放款结果成功
# 用例2：银行账号放款- 发起放款请求失败  各种异常场景返回的code和message都不一样
# 用例3：银行账号放款- 发起放款请求成功，查询放款结果返回订单不存在(channel_error配置为失败，且配置为消息忽略)
# 用例4：银行账号放款- 发起放款请求失败，查询放款结果失败（channel_error配置为失败）
# 用例5：银行账号放款- 发起放款请求成功，查询放款结果处理中（channel_error不配置/处理中）、后又channel_error配置为失败
# 用例6：银行账号放款- 发起放款请求成功，查询放款结果异常
# 用例7：电子钱包-Gcash放款
# 用例8：电子钱包-Paymaya放款
# 发起放款请求前置查询返回的不是交易不存在 1. 放款成功  2.其他非交易不存在 ，还未写
# PS：没有走路由，线上有些场景没有覆盖

class TestPhilippinesUnionbank:
    unionbank_uuid = get_guid()

    # 每个类的前置条件
    def setup_class(self):
        # 菲律宾使用默认卡
        self.account = get_carduuid_bycardnum("card", "enc_04_4106612382062092288_439")[0]
        self.four_element = get_four_element_global()
        self.global_payment_nacos = PaymentNacos(nacos_domain)
        self.global_payment_mock = UnionbankMock(global_payment_easy_mock_phl)
        # 使unionbank余额足够
        self.global_payment_mock.update_unionbank_balance("success")
        # 有时候直接修改数据库配置，会有缓存的问题
        clear_cache()

    # 每个类的最后需要还原之前的修改，并关闭数据库链接
    @classmethod
    def teardown_class(self):
        # 恢复为非Mock
        self.global_payment_nacos = PaymentNacos(nacos_domain)
        self.global_payment_nacos.update_nacos_unionbank_withdraw()
        self.global_payment_mock = UnionbankMock(global_payment_easy_mock_phl)
        # self.global_payment_mock.update_fk_userinfo(account_no="enc_04_3383474380125773824_485", bank_code="LBP",
        #                                             withdraw_type="bank")
        self.global_payment_mock.update_fk_userinfo(account_no="enc_04_4022717234631155712_060", bank_code="LBP",
                                                    withdraw_type="BDO")  # unionbank放款成功数据
        self.global_payment_mock.update_unionbank_balance("success")
        DataBase.close_connects()

    # TODO 余额查询

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_query_success(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在  TODO 如何模拟unionbank的交易不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、保证发起代付可以成功
        self.global_payment_mock.update_unionbank_withdraw("success", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        # 修改withdraw_query_url走mock
        self.global_payment_nacos.update_nacos_unionbank_withdraw(query_project_id=project_id)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction")
        # 4、mock返回代付查询成功
        withdraw_receipt_info = get_withdraw_receipt_info_by_merchant_key(req["merchant_key"])
        self.global_payment_mock.update_unionbank_withdraw_query("success", resp["data"]["channel_key"],
                                                                 withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"])
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询 success"})
        # 6、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction", resp_transfer_mode=None)

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_fail_test1(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、修改mock使发起代付失败
        self.global_payment_mock.update_unionbank_withdraw("fail_test1", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="500",
                                          message="Internal Server Error")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_fail_test2(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、修改mock使发起代付失败
        self.global_payment_mock.update_unionbank_withdraw("fail_test2", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="-1",
                                          message="beneficiary.name you entered has invalid characters.")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_fail_test2_1(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、修改mock使发起代付失败
        self.global_payment_mock.update_unionbank_withdraw("fail_test2_1", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="-1",
                                          message="Missing/Invalid Parameters.")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_fail_test3(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、修改mock使发起代付失败
        self.global_payment_mock.update_unionbank_withdraw("fail_test3", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="F", message="UNABLE TO PROCESS")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_fail_test3_1(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、修改mock使发起代付失败
        self.global_payment_mock.update_unionbank_withdraw("fail_test3_1", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="TF",
                                          message="Failed to credit Beneficiary Account")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_query_notexsit(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在  TODO 如何模拟unionbank的交易不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、保证发起代付可以成功
        self.global_payment_mock.update_unionbank_withdraw("success", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        # 修改withdraw_query_url走mock
        self.global_payment_nacos.update_nacos_unionbank_withdraw(query_project_id=project_id)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction")
        # channel_error中将交易不存在配置为失败和忽略消息
        update_channel_error("unionbank", "-2", 1, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 4、mock返回代付查询返回交易不存在
        self.global_payment_mock.update_unionbank_withdraw_query("notexsit", resp["data"]["channel_key"],
                                                                 self.unionbank_uuid)
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询 fail"})
        # 6、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt的终态信息（注意message配置了消息忽略）
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "-2", "Successful transaction")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_query_fail(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在  TODO 如何模拟unionbank的交易不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、保证发起代付可以成功
        self.global_payment_mock.update_unionbank_withdraw("success", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        # 修改withdraw_query_url走mock
        self.global_payment_nacos.update_nacos_unionbank_withdraw(query_project_id=project_id)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction")
        # channel_error中配置为失败
        update_channel_error("unionbank", "TF", 1, "WITHDRAW_QUERY")
        # 4、mock返回代付查询返回失败
        withdraw_receipt_info = get_withdraw_receipt_info_by_merchant_key(req["merchant_key"])
        self.global_payment_mock.update_unionbank_withdraw_query("fail", resp["data"]["channel_key"],
                                                                 withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"])
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询 fail"})
        # 6、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "TF", "Failed to credit Beneficiary Account")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_query_process_to_fail(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在  TODO 如何模拟unionbank的交易不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、保证发起代付可以成功
        self.global_payment_mock.update_unionbank_withdraw("success", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        # 修改withdraw_query_url走mock
        self.global_payment_nacos.update_nacos_unionbank_withdraw(query_project_id=project_id)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction")
        # channel_error中配置为处理中
        update_channel_error("unionbank", "SP", 2, "WITHDRAW_QUERY")
        # 4、mock返回代付查询返回处理中
        self.global_payment_mock.update_unionbank_withdraw_query("process", resp["data"]["channel_key"],
                                                                 self.unionbank_uuid)
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 6、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt的终态信息（注意message配置了消息忽略）
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "SP", "Successful transaction")

        # 再将处理中的在channel_error中配置为失败
        update_channel_error("unionbank", "SP", 1, "WITHDRAW_QUERY")
        # 4、mock返回代付查询返回处理中
        self.global_payment_mock.update_unionbank_withdraw_query("process", resp["data"]["channel_key"],
                                                                 self.unionbank_uuid)
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询 fail"})
        # 6、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "SP", "Successful transaction")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_withdraw_query_error(self):
        # 1、mock用户中心的返回的是银行账户
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="LBP", withdraw_type="bank")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、保证发起代付可以成功
        self.global_payment_mock.update_unionbank_withdraw("success", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "account", "LBP")
        # 修改withdraw_query_url走mock
        self.global_payment_nacos.update_nacos_unionbank_withdraw(query_project_id=project_id)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction")
        # 4、mock返回代付查询返回处理中
        self.global_payment_mock.update_unionbank_withdraw_query("error", resp["data"]["channel_key"],
                                                                 self.unionbank_uuid)
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 6、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "TS", "Successful transaction")

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_gcash_withdraw_query_success(self):
        # 1、mock用户中心的返回的是电子钱包Gcash
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="GCash", withdraw_type="Gcash")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在  TODO 如何模拟unionbank的交易不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、保证发起代付可以成功
        self.global_payment_mock.update_unionbank_withdraw("success", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "wallet", "GCash")
        # 修改withdraw_query_url走mock
        self.global_payment_nacos.update_nacos_unionbank_withdraw(query_project_id=project_id)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction")
        # 4、mock返回代付查询成功
        withdraw_receipt_info = get_withdraw_receipt_info_by_merchant_key(req["merchant_key"])
        self.global_payment_mock.update_unionbank_withdraw_query("success", resp["data"]["channel_key"],
                                                                 withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"])
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询 success"})
        # 6、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction", resp_transfer_mode=None)

    @pytest.mark.global_payment_phl_auto
    @pytest.mark.global_payment_unionbank
    @pytest.mark.global_payment_unionbank_withdraw
    def test_unionbank_paymaya_withdraw_query_success(self):
        # 1、mock用户中心的返回的是电子钱包Paymaya
        self.global_payment_mock.update_fk_userinfo(account_no=self.four_element['data']['card_num_encrypt'],
                                                    bank_code="Paymaya", withdraw_type="Paymaya")
        # 2、只让withdraw走mock，获取token和withdraw_query_url地址为通道真实的，保证前置查询到订单不存在  TODO 如何模拟unionbank的交易不存在
        self.global_payment_nacos.update_nacos_unionbank_withdraw(withdraw_project_id=project_id)
        # 3、保证发起代付可以成功
        self.global_payment_mock.update_unionbank_withdraw("success", self.unionbank_uuid, self.unionbank_uuid)
        # 4、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现 process"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw, "wallet", "Paymaya")
        # 修改withdraw_query_url走mock
        self.global_payment_nacos.update_nacos_unionbank_withdraw(query_project_id=project_id)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction")
        # 4、mock返回代付查询成功
        withdraw_receipt_info = get_withdraw_receipt_info_by_merchant_key(req["merchant_key"])
        self.global_payment_mock.update_unionbank_withdraw_query("success", resp["data"]["channel_key"],
                                                                 withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"])
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询 success"})
        # 6、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"])
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="TS",
                                          message="Successful transaction", resp_transfer_mode=None)
