# -*- coding: utf-8 -*-
# import gc

import pytest

from biztest.config.easymock.easymock_config import global_payment_easy_mock
from biztest.config.payment.url_config import global_amount
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import check_withhold, \
    check_withhold_receipt, check_autopay_response, check_autopay_response_fail, check_account, check_binding, \
    check_binding_request, check_card, assert_check_withdraw_withdrawreceipt_initinfo, \
    assert_withdrawandreceipt_process, assert_withdrawandreceipt_success, assert_withdrawandreceipt_fail
from biztest.function.global_payment.global_payment_db_function import get_carduuid_bycardnum, \
    update_withhold_receipt_expired_at, update_task_by_task_order_no, update_channel_error, \
    get_withdraw_receipt_by_channel_key
from biztest.function.global_payment.global_payment_db_operation import get_withdraw_receipt_info_by_merchant_key
from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, auto_withdraw, \
    auto_pay, gbpay_qrcode_charge_callback, global_withhold_close_order, auto_bind_tha, clear_cache, \
    global_autoWithdraw_retry
from biztest.util.asserts.assert_util import Assert
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_gbpay_mock import GbpayMock
from biztest.util.tools.tools import get_sysconfig, get_date, get_four_element_global

env = get_sysconfig("--env")
country = get_sysconfig("--country")
provider = "gbpay"
sign_company = "amberstar1"
channel_name_withdraw = "gbpay_amberstar1_withdraw"
channel_name_qrcode = "gbpay_amberstar1_qrcode"
channel_name_verify = "gbpay_cymo1_verify"
# card_uuid = "6622092000001290502"  # 对应的卡号为 enc_03_3513454134508920832_259 --》6213948554081919，必须和用户中心返回的一致
user_uuid = "197222248434630658"
switch_card_uuid = "6622092000001290603"  # 对应的卡号为 1113939657--》新 enc_04_4122683620882653184_714，必须和用户中心返回的一致
switch_user_uuid = "1972222000001290603"
project_id = "5b9a3ddd3a0f7700206522eb"  # mock
nacos_domain = "nacos-test-tha.starklotus.com"  # nacos


class TestThailandGbpay:

    # 每个类的前置条件
    def setup_class(cls):
        # 使用固定的卡enc_02_3019550690894153728_426--》7007248474  、固定的card_uuid+user_uuid
        cls.account = get_carduuid_bycardnum("account", "enc_02_3019550690894153728_426")[0]
        # 修改kv，使走到mock
        cls.global_payment_nacos = PaymentNacos(nacos_domain)
        # 默认nacos配置usercenter.properties中用户中心一直是mock地址，修改地址需要重启
        # cls.global_payment_nacos.update_user_center_config(project_id=project_id)
        cls.global_payment_nacos.update_gbpay_withdraw(project_id=project_id)
        cls.global_payment_nacos.update_gbpay_qrcode(project_id=project_id)
        cls.global_payment_nacos.update_gbpay_verify(project_id=project_id)
        # mock使fk返回用户信息和卡信息与本地库数据一致
        cls.global_payment_mock = GbpayMock(global_payment_easy_mock)
        # 修改mock
        cls.global_payment_mock.update_fk_userinfo(
            cls.account["card_id_num"], cls.account["card_username"], cls.account["card_account"],
            cls.account["card_bank_code"], cls.account["card_uuid"])
        # 修改渠道的评分为最高，使一定路由到该通道
        # update_provider_score(1000, provider, sign_company)
        clear_cache()  # 有时候直接修改数据库配置，会有缓存的问题

    # 每个类的最后需要还原之前的修改，并关闭数据库链接
    @classmethod
    def teardown_class(cls):
        # cls.global_payment_nacos.update_user_center_config()  # 不管是日常测试还是自动化测试，用户中心都暂时先一直使用mock
        cls.global_payment_nacos.update_gbpay_verify()  # 不管是日常测试还是自动化测试，绑卡都暂时先一直使用mock
        cls.global_payment_nacos.update_gbpay_withdraw()
        cls.global_payment_nacos.update_gbpay_qrcode()
        # update_provider_score(100, provider, sign_company)
        DataBase.close_connects()

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_fail_process(self):
        # 1、修改mock，使代付能够成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("fail")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_01", "Balance is not enough")
        # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否有延迟
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_500(self):
        # 1、修改mock，使代付能够成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("500")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_NO_CHANNEL_CODE",
                                          "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5b9a3ddd3a0f7700206522eb/withdraw/v2/transfers返回错误HttpStatus500,{}")
        # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否有延迟
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_repead(self):
        # 1、修改mock，使代付能够成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("process")  # 此时订单返回非不存在，则标示疑似重复下单，流程会停止
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "exception order，pls query"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00", "Success")
        # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否有延迟
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_query_success(self):
        # 1、修改mock，使代付能够成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], code="WD_00", message="Success")
        # 3、需要修改一下查询的mock
        withdraw_receipt_info = get_withdraw_receipt_info_by_merchant_key(req["merchant_key"])
        self.global_payment_mock.update_withdraw_query("success", resp["data"]["channel_key"],
                                                       withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"])
        # 4、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="WD_00_00", message="Success")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_query_fail_errorcode(self):
        # 1、修改mock，使代付能够成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00", "Success")
        # 4、需要修改一下查询的mock
        self.global_payment_mock.update_withdraw_query("fail")
        # 配置错误码（gbpay线上WD_00_90配置的是代付失败，此时我们修改一下错误码配置，使其先为处理中）
        update_channel_error("gbpay", "WD_00_90", 2, "WITHDRAW_QUERY")

        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 检查withdraw／withdraw_receipt（9.16的分支要记录此时的中间状态）
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00_90", "Error")

        # 6、还原我们刚刚修改的错误码
        update_channel_error("gbpay", "WD_00_90", 1, "WITHDRAW_QUERY")  # 测试的时候发现，gbpay的错误码检查了返回的msg，这一点需要注意
        # 执行代付task  # withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询失败"})
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "WD_00_90", "Error")
        # 测试的时候发现，gbpay的错误码检查了返回的msg，这一点需要注意

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_query_process(self):
        # 1、修改mock，使代付能够成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00", "Success")
        # 4、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 5、此时不修改查询mock，此时查询到的订单还会是订单不存在，但是gbpay的订单不存在并没有配置响应的错误码，故此时订单会一直是处理中
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 检查withdraw／withdraw_receipt（9.16的分支要记录此时的中间状态）
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_ORDER_NOT_EXISTS", "Success")
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否被挂起
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_query_500(self):
        # 1、修改mock，使代付能够成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})

        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00", "Success")

        # 4、需要修改一下查询的mock
        self.global_payment_mock.update_withdraw_query("500")
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 检查withdraw／withdraw_receipt
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00", "Success")

        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否被挂起
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_success(self):
        # 1、修改mock，使代付能够成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})

        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00", "Success")
        # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否被挂起
        update_task_by_task_order_no(req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_fail_retry_success(self):
        # 第一次代付失败，后只换trade_no重新发起代付，代付成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})

        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00", "Success")

        # 4、需要修改一下查询的mock
        self.global_payment_mock.update_withdraw_query("fail")
        # 配置错误码（gbpay线上WD_00_90配置的是代付失败，此时我们修改一下错误码配置，使其先为处理中）
        update_channel_error("gbpay", "WD_00_90", 2, "WITHDRAW_QUERY")

        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 检查withdraw／withdraw_receipt（9.16的分支要记录此时的中间状态）
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00_90", "Error")

        # 6、还原我们刚刚修改的错误码
        update_channel_error("gbpay", "WD_00_90", 1, "WITHDRAW_QUERY")  # 测试的时候发现，gbpay的错误码检查了返回的msg，这一点需要注意
        # 执行代付task  # withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询失败"})
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "WD_00_90", "Error")
        # 测试的时候发现，gbpay的错误码检查了返回的msg，这一点需要注意

        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、只换 trade_no 重新发起代付
        req_retry, resp_retry = global_autoWithdraw_retry(sign_company, self.account["card_uuid"], user_uuid,
                                                          channel_name=channel_name_withdraw,
                                                          merchant_key=req["merchant_key"])
        # 3、执行代付task#withdraw
        run_task_by_order_no(req_retry["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req_retry["trade_no"], req_retry["merchant_key"], "WD_00", "Success")

        # 4、需要修改一下查询的mock
        withdraw_receipt_info = get_withdraw_receipt_info_by_merchant_key(req_retry["merchant_key"])
        self.global_payment_mock.update_withdraw_query("success", resp["data"]["channel_key"],
                                                       withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"])
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req_retry["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_success(req_retry["trade_no"], req_retry["merchant_key"], "WD_00_00", "Success")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_withdraw
    def test_gbpay_withdraw_fail_updatecard_success(self):
        # 第一次代付失败，后不换mrchant_key，更换card_uuid重新发起代付，代付成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid,
                                  channel_name=channel_name_withdraw)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00", "Success")

        # 4、需要修改一下查询的mock
        self.global_payment_mock.update_withdraw_query("fail", resp["data"]["channel_key"])
        # 配置错误码（gbpay线上WD_00_90配置的是代付失败，此时我们修改一下错误码配置，使其先为处理中）
        update_channel_error("gbpay", "WD_00_90", 2, "WITHDRAW_QUERY")

        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付订单正在处理中！需要重试！"})
        # 检查withdraw／withdraw_receipt（9.16的分支要记录此时的中间状态）
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00_90", "Error")

        # 6、还原我们刚刚修改的错误码
        update_channel_error("gbpay", "WD_00_90", 1, "WITHDRAW_QUERY")  # 测试的时候发现，gbpay的错误码检查了返回的msg，这一点需要注意
        # 执行代付task  # withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json={"code": 1, "message": "代付提现查询失败"})
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "WD_00_90", "Error")

        # mock使fk返回用户信息和卡信息与本地库数据一致，换卡必须修改用户中心的返回卡
        global_payment_mock = GbpayMock(global_payment_easy_mock)
        global_payment_mock.update_fk_userinfo('enc_01_2580379923923863552_908', 'enc_04_2868629754750699520_459',
                                               'enc_04_4122683620882653184_714', bank_code="T00008",
                                               card_uuid=switch_card_uuid)
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、换 trade_no且换卡  重新发起代付
        req_retry, resp_retry = global_autoWithdraw_retry(sign_company, switch_card_uuid, user_uuid,
                                                          channel_name=channel_name_withdraw,
                                                          merchant_key=req["merchant_key"])
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
        # 检查withdraw_receipt，由于withdraw不会更新掉，所以还是之前的信息
        assert_withdrawandreceipt_process(req_retry["trade_no"], req_retry["merchant_key"], "WD_00", "Success")

        # 4、需要修改一下查询的mock
        withdraw_receipt_info = get_withdraw_receipt_info_by_merchant_key(req_retry["merchant_key"])
        self.global_payment_mock.update_withdraw_query("success", resp["data"]["channel_key"],
                                                       withdraw_receipt_info[0]["withdraw_receipt_channel_inner_key"])
        # 5、执行代付task#withdrawQuery
        run_task_by_order_no(req_retry["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_success(req_retry["trade_no"], req_retry["merchant_key"], "WD_00_00", "Success")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_charge_success(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")
        # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否被挂起
        update_task_by_task_order_no(autopay_req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_charge_fail(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("fail")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response_fail(autopay_resp, channel_name_qrcode, global_amount, "WH_99", "The OTP must be 'Y'")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 3)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode, "WH_99", "")
        # 此时不会生成代扣查询task#withoholdQuery

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_charge_500(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("500")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response--》2022.10.25印度版本上线后改了这个逻辑，导致返回给rbiz的结构data下参数没有了，以前代扣直接fail现在置为process
        # check_autopay_response_fail(autopay_resp, channel_name_qrcode, global_amount, "KN_NO_CHANNEL_CODE", "KN_NO_CHANNEL_CODE", "KN_UNKNOWN_ERROR")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 3)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode, "KN_NO_CHANNEL_CODE",
                               "")
        # 此时不会生成代扣查询task#withoholdQuery

    # @pytest.mark.global_payment_thailand_auto
    # @pytest.mark.global_payment_gbpay
    # @pytest.mark.global_payment_gbpay_qrcode
    # def test_gbpay_qrcode_charge_repead_order(self):
    #     # 1、修改mock，是能够成功======》代扣前的前置查询已于2022.10.12取消，所以不存在这个场景了
    #     self.global_payment_mock.update_qrcode_query("success")
    #     # 2、使用固定的 card_uuid 发起代扣
    #     autopay_req, autopay_resp = global_withhold_autopay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
    #                                                         amount=global_amount,
    #                                                         channel_name=channel_name_qrcode)
    #     # 检查autopay的response
    #     check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REPEAT_ORDER", "KN_REPEAT_ORDER",
    #                            "KN_UNKNOWN_ERROR", payment_type="qrcode")
    #     # 检查数据库中的数据
    #     check_withhold(autopay_req["merchant_key"], self.account, 1)
    #     check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode, "KN_REPEAT_ORDER",
    #                            "KN_REPEAT_ORDER")
    #     # 需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否被挂起
    #     update_task_by_task_order_no(autopay_req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_query_success(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改mock，使代扣查询到成功
        self.global_payment_mock.update_qrcode_query("success", global_amount)

        # 4、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 0, "message": "支付订单查询成功"})
        run_task_by_order_no(autopay_req["merchant_key"],
                             except_json={"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 2)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode, "WH_00_S_00",
                               "")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_query_fail_errorcode(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改mock，使代扣查询到失败
        self.global_payment_mock.update_qrcode_query("fail")
        # 配置错误码（gbpay线上WH_00_D配置的是代扣失败，此时我们修改一下错误码配置，使其先为处理中）
        update_channel_error("gbpay", "WH_00_D", 2, "CHARGE_QUERY")

        # 4、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 5、还原我们刚刚修改的错误码
        update_channel_error("gbpay", "WH_00_D", 1, "CHARGE_QUERY")

        # 6、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 1, "message": "支付订单查询失败"})
        run_task_by_order_no(autopay_req["merchant_key"],
                             except_json={"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 3)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode, "WH_00_D",
                               "")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_query_process(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改mock，使代扣查询到处理中
        self.global_payment_mock.update_qrcode_query("process")
        # 此时不修改错误码，保持现有的错误码

        # 4、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")
        # 需要把查询task关闭，方便后续观察数据
        update_task_by_task_order_no(autopay_req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_query_not_exist(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改mock，使代扣查询到订单不存在
        self.global_payment_mock.update_qrcode_query("not_exit")
        # 把错误码改为处理中
        update_channel_error("gbpay", "WH_02", 2, "CHARGE_QUERY")

        # 4、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 5、把 订单不存在的错误码改为 失败
        update_channel_error("gbpay", "WH_02", 1, "CHARGE_QUERY")

        # 6、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 1, "message": "支付订单查询失败"})
        run_task_by_order_no(autopay_req["merchant_key"],
                             except_json={"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 3)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode, "WH_02",
                               "Invalid referenceNo.")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_query_500(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改mock，使代扣查询到订单不存在
        self.global_payment_mock.update_qrcode_query("500")

        # 4、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 需要把查询task关闭，方便后续观察数据
        update_task_by_task_order_no(autopay_req["merchant_key"], "close")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_query_timeout_order_success(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改订单时间，并修改mock为成功，使订单超时关单是正好查询到代扣成功
        update_withhold_receipt_expired_at(autopay_req["merchant_key"], get_date(minute=-1))
        self.global_payment_mock.update_qrcode_query("success", global_amount)

        # 4、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 0, "message": "支付订单查询成功"})
        run_task_by_order_no(autopay_req["merchant_key"],
                             except_json={"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 2)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode, "WH_00_S_00",
                               "")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_query_timeout_order_fail(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")
        # 3、修改订单时间，并修改mock为失败，使订单超时关单是正好查询到代扣失败，WH_99已经配置为失败
        update_withhold_receipt_expired_at(autopay_req["merchant_key"], get_date(minute=-1))
        self.global_payment_mock.update_qrcode_query("fail")

        # 4、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 1, "message": "支付订单查询失败"})
        run_task_by_order_no(autopay_req["merchant_key"],
                             except_json={"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 3)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode, "WH_00_D",
                               "")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_query_timeout_order_process(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改订单时间，并修改mock为处理中，使订单超时关单是正好查询到代扣处理中，WH_00_G已经配置为处理中
        update_withhold_receipt_expired_at(autopay_req["merchant_key"], get_date(minute=-1))
        self.global_payment_mock.update_qrcode_query("process")

        # 4、执行查询task#withholdChargeQuery
        run_task_by_order_no(autopay_req["merchant_key"], except_json={"code": 1, "message": "支付订单查询订单超时"})
        run_task_by_order_no(autopay_req["merchant_key"],
                             except_json={"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 3)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode,
                               "KN_TIMEOUT_CLOSE_ORDER", "")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_payment_callback(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、回调不存在的订单
        req, resp = gbpay_qrcode_charge_callback(channel_name_qrcode, global_amount / 100,
                                                 autopay_resp["data"]["channel_key"][1:])
        Assert.assert_equal("00", resp["resultCode"], "给通道的code正确")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")
        # 执行查询task#withholdCallback
        run_task_by_order_no(autopay_resp["data"]["channel_key"][1:],
                             except_json={"code": 1, "message": "代扣订单不存在", "data": None})

        # 3、回调错误的金额
        req, resp = gbpay_qrcode_charge_callback(channel_name_qrcode, global_amount / 10,
                                                 autopay_resp["data"]["channel_key"])
        Assert.assert_equal("00", resp["resultCode"], "给通道的code正确")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")
        channel_key = autopay_resp["data"]["channel_key"]
        # 执行查询task#withholdCallback
        run_task_by_order_no(autopay_resp["data"]["channel_key"],
                             except_json={"code": 2,
                                          "message": "任务[withholdCallback]发生异常！收据[" + channel_key + "]金额[" + str(
                                              global_amount)
                                                     + "]与回调金额[" + str(global_amount * 10) + "]不一致或不在容差范围内，回调任务无法继续执行",
                                          "data": None})
        # 需要把查询task关闭，方便后续观察数据
        update_task_by_task_order_no(autopay_resp["data"]["channel_key"], "close")

        # 3、回调正确
        req, resp = gbpay_qrcode_charge_callback(channel_name_qrcode, global_amount / 100,
                                                 autopay_resp["data"]["channel_key"])
        Assert.assert_equal("00", resp["resultCode"], "给通道的code正确")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")
        # 执行查询task#withholdCallback
        run_task_by_order_no(autopay_resp["data"]["channel_key"],
                             except_json={"code": 0, "message": "处理成功", "data": None})
        run_task_by_order_no(autopay_req["merchant_key"])  # 此时有两个task，暂时不检查task执行情况
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 2)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode, "WH_00_S_00",
                               "callback WH_00")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_charge_callback(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、回调失败的订单
        req, resp = gbpay_qrcode_charge_callback(channel_name_qrcode, global_amount / 100,
                                                 autopay_resp["data"]["channel_key"],
                                                 "90")
        Assert.assert_equal("FAIL", resp["resultCode"], "给通道的code正确")

        # 3、回调正确
        req, resp = gbpay_qrcode_charge_callback(channel_name_qrcode, global_amount / 100,
                                                 autopay_resp["data"]["channel_key"])
        Assert.assert_equal("00", resp["resultCode"], "给通道的code正确")
        # 3、回调正确
        req, resp = gbpay_qrcode_charge_callback(channel_name_qrcode, global_amount / 100,
                                                 autopay_resp["data"]["channel_key"])
        Assert.assert_equal("00", resp["resultCode"], "给通道的code正确")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")
        # 执行查询task#withholdCallback
        run_task_by_order_no(autopay_resp["data"]["channel_key"],
                             except_json={"code": 0, "message": "处理成功", "data": None})
        run_task_by_order_no(autopay_req["merchant_key"])  # 此时有两个task，暂时不检查task执行情况
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 2)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode, "WH_00_S_00",
                               "callback WH_00")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_close_order_status_success(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改mock，使代扣查询到成功，此时再来关单
        self.global_payment_mock.update_qrcode_query("success", global_amount)
        close_req, close_resp = global_withhold_close_order(autopay_req["merchant_key"])
        Assert.assert_equal(1, close_resp["code"], "给前端的code正确")
        Assert.assert_equal("订单已经成为终态，关闭订单失败", close_resp["message"], "给前端说关单失败")

        # 4、此时不用执行查询task#withholdChargeQuery，前端关单时会同步查询代扣状态，此时只有withholdUpdate需要执行
        run_task_by_order_no(autopay_req["merchant_key"])
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 2)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 2, channel_name_qrcode, "WH_00_S_00",
                               "")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_close_order_status_fail(self):
        # 1、修改mock，是能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改mock，使代扣查询到失败，此时再来关单
        self.global_payment_mock.update_qrcode_query("fail")
        update_channel_error("gbpay", "WH_00_D", 1, "CHARGE_QUERY")
        close_req, close_resp = global_withhold_close_order(autopay_req["merchant_key"])
        Assert.assert_equal(1, close_resp["code"], "给前端的code正确")
        Assert.assert_equal("订单已经成为终态，关闭订单失败", close_resp["message"], "给前端说不用关单了")

        # 4、此时不用执行查询task#withholdChargeQuery，前端关单时会同步查询代扣状态，此时只有withholdUpdate需要执行
        run_task_by_order_no(autopay_req["merchant_key"])
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 3)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode, "WH_00_D",
                               "")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_qrcode
    def test_gbpay_qrcode_close_order_status_process(self):
        # 1、修改mock，使能够成功
        self.global_payment_mock.update_qrcode_query("not_exit")
        self.global_payment_mock.update_qrcode("success")
        # 2、使用固定的 card_uuid 发起代扣
        autopay_req, autopay_resp = auto_pay(sign_company, "qrcode", card_uuid=self.account["card_uuid"],
                                             amount=global_amount,
                                             channel_name=channel_name_qrcode)
        # 检查autopay的response
        check_autopay_response(autopay_resp, channel_name_qrcode, global_amount, "KN_REQUEST_SUCCESS", codes="success",
                               payment_type="qrcode")
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 1)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 1, channel_name_qrcode,
                               "KN_REQUEST_SUCCESS", "")

        # 3、修改mock，使代扣查询到失败，并允许失败的时候关单，此时再来关单（此时不允许关单）
        self.global_payment_mock.update_qrcode_query("process")
        update_channel_error("gbpay", "WH_00_G", 2, "CHARGE_QUERY,MANUAL_CLOSE")
        close_req, close_resp = global_withhold_close_order(autopay_req["merchant_key"])
        Assert.assert_equal(0, close_resp["code"], "给前端的code正确")
        Assert.assert_equal("关闭订单成功", close_resp["message"], "给前端说关闭订单成功")

        # 4、此时不用执行查询task#withholdChargeQuery，前端关单时会同步查询代扣状态，此时只有withholdUpdate需要执行
        run_task_by_order_no(autopay_req["merchant_key"])
        # 检查数据库中的数据
        check_withhold(autopay_req["merchant_key"], self.account, 3)
        check_withhold_receipt(autopay_req["merchant_key"], self.account, 3, channel_name_qrcode,
                               "KN_MANUAL_CLOSE_ORDER", "")

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_verify
    def test_gbpay_verify_success(self):
        four_element = get_four_element_global()
        self.global_payment_mock.update_gbpay_bindcard("success")
        bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        # 发起绑卡
        autobind_req, autobind_resp = auto_bind_tha("cymo1", four_element, "T00007",
                                                    bank_account_encrypt=bank_account_encrypt)
        Assert.assert_equal(0, autobind_resp["code"], "绑卡成功")
        Assert.assert_equal("V_00", autobind_resp["data"]["channel_code"], "绑卡成功V_00")
        Assert.assert_equal(channel_name_verify, autobind_resp["data"]["channel_name"], "绑卡成功channel_name")

        # # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
        check_account(autobind_resp["data"]["card_uuid"], "account")
        check_binding(autobind_resp["data"]["card_uuid"], "account", 1, channel_name_verify)
        check_binding_request(autobind_req["merchant_key"], four_element, 0, autobind_req, autobind_resp)
        check_card(autobind_resp["data"]["card_uuid"], "account", four_element, 1, autobind_req, autobind_resp)

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_verify
    def test_gbpay_verify_fail(self):
        four_element = get_four_element_global()
        self.global_payment_mock.update_gbpay_bindcard("fail")
        bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        # 发起绑卡
        autobind_req, autobind_resp = auto_bind_tha("cymo1", four_element, "T00007",
                                                    bank_account_encrypt=bank_account_encrypt)
        Assert.assert_equal(1, autobind_resp["code"], "绑卡失败")
        Assert.assert_equal("V_01", autobind_resp["data"]["channel_code"], "绑卡失败V_01")
        Assert.assert_equal(channel_name_verify, autobind_resp["data"]["channel_name"], "绑卡成功channel_name")

        # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
        check_account(autobind_resp["data"]["card_uuid"], "account")
        check_binding(autobind_resp["data"]["card_uuid"], "account", 2, channel_name_verify)
        check_binding_request(autobind_req["merchant_key"], four_element, 1, autobind_req, autobind_resp)
        check_card(autobind_resp["data"]["card_uuid"], "account", four_element, 0, autobind_req, autobind_resp)

    @pytest.mark.global_payment_thailand_auto
    @pytest.mark.global_payment_gbpay
    @pytest.mark.global_payment_gbpay_verify
    def test_gbpay_verify_500(self):
        four_element = get_four_element_global()
        self.global_payment_mock.update_gbpay_bindcard("500")
        bank_account_encrypt = four_element["data"]["bank_account_encrypt"]

        # 发起绑卡
        autobind_req, autobind_resp = auto_bind_tha(sign_company, four_element, "T00007",
                                                    bank_account_encrypt=bank_account_encrypt)
        print(autobind_resp)
        Assert.assert_equal(1, autobind_resp["code"], "绑卡失败")
        Assert.assert_equal("KN_NO_CHANNEL_CODE", autobind_resp["data"]["channel_code"], "绑卡失败channel_code")
        Assert.assert_equal("KN_UNKNOWN_ERROR", autobind_resp["data"]["platform_code"], "绑卡失败platform_code")
        Assert.assert_equal(channel_name_verify, autobind_resp["data"]["channel_name"], "绑卡成功channel_name")

        # dsq绑卡结果查询接口，这一步可能会更新card和binding表的状态，需要放在其他检查前面
        check_account(autobind_resp["data"]["card_uuid"], "account")
        check_binding(autobind_resp["data"]["card_uuid"], "account", 2, channel_name_verify)
        # check_binding_request(autobind_req["merchant_key"], four_element, 1, autobind_req, autobind_resp)
        check_card(autobind_resp["data"]["card_uuid"], "account", four_element, 0, autobind_req, autobind_resp)

    # 这段用例测试用，自动化的时候不跑，但是也不要删除，就留在这里
    @pytest.mark.parametrize("query_status,withdraw_status,case_code,case_msg,task_demo",
                             [("500", "", "KN_NO_CHANNEL_CODE", "", {"code": 2, "message": "代付提现处理中"}),
                              ("success", "", "KN_REPEAT_ORDER", "KN_REPEAT_ORDER",
                               {"code": 2, "message": "exception order，pls query"}),
                              ("fail", "", "WD_00_90", "Error", {"code": 2, "message": "exception order，pls query"}),
                              ("not_exit", "success", "WD_00", "Success", {"code": 2, "message": "代付提现处理中"}),
                              ("not_exit", "fail", "WD_01", "Balance is not enough", {"code": 2, "message": "代付提现处理中"}),
                              ("not_exit", "repead", "WD_03", "Duplicate Transaction",
                               {"code": 2, "message": "代付提现处理中"}),
                              ("not_exit", "500", "KN_NO_CHANNEL_CODE",
                               "https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5b9a3ddd3a0f7700206522eb/withdraw/v2/transfers返回错误HttpStatus500,{}",
                               {"code": 2, "message": "代付提现处理中"})
                              ],
                             ids=["pre_500", "exit_success", "exit_fail", "success", "fail", "repead", "500"])
    # 参数说明：前置查询接口code，下单接口code，数据库存储code，数据库存储msg，task_memo
    # 场景说明：前置查询接口500，已失败的订单重复下单，已成功的订单重复下单，下单成功，下单失败，下单重复，下单接口500
    def test_gbpay_withdraw(self, query_status, withdraw_status, case_code, case_msg, task_demo):
        # 1、修改mock，使代付能够成功
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query(query_status)
        self.global_payment_mock.update_withdraw(withdraw_status)
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid)
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json=task_demo)
        # 4、检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], case_code, case_msg)
        # 5、需要把查询task关闭，方便后续观察数据，可以观察task#withdrawQuery是否有延迟
        update_task_by_task_order_no(req["merchant_key"], "close")

    # 这段用例测试用，自动化的时候不跑，但是也不要删除，就留在这里
    def test_notrun_gbpay_withdraw_Query(self):
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("fail")
        req, resp = auto_withdraw(sign_company, self.account["card_uuid"], user_uuid)
        # 执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_01", "Balance is not enough")

        # 1、修改mock，使代付订单不存在
        self.global_payment_mock.update_withdraw_query("not_exit")
        # 2、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        # 3、检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_ORDER_NOT_EXISTS",
                                          "Balance is not enough")
        # 4、将订单不存在配置为失败
        update_channel_error("gbpay", "KN_ORDER_NOT_EXISTS", 1, "WITHDRAW_QUERY,CHARGE_QUERY,IGNORE_MESSAGE")
        # 5、再次执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        # 6、检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "KN_ORDER_NOT_EXISTS",
                                          "Balance is not enough")

        # 1、修改mock，使代付能够失败
        self.global_payment_mock.update_withdraw_query("fail")
        # 2、配置错误码（此时我们修改一下错误码配置，确保其为处理中）
        update_channel_error("gbpay", "WD_00_90", 2, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 3、执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        # 4、检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"], "WD_00_90", "Balance is not enough")
        # 5、将刚刚修改的错误码，配置为失败
        update_channel_error("gbpay", "WD_00_90", 1, "WITHDRAW_QUERY,IGNORE_MESSAGE")
        # 6、再次执行代付task#withdrawQuery
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 1, "message": "代付提现查询失败"}')
        # 7、检查withdraw／withdraw_receipt
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "WD_00_90", "Balance is not enough")
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid,
                                                       self.account["card_uuid"],
                                                       channel_name_withdraw)

        # 1、修改mock，使重新下单成功
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、只换 trade_no 重新发起代付
        req2, resp2 = global_autoWithdraw_retry(sign_company, self.account["card_uuid"], user_uuid,
                                                merchant_key=req["merchant_key"])
        # 3、执行代付task#withdraw
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 2, "message": "代付提现处理中"}')
        assert_withdrawandreceipt_process(req2["trade_no"], req["merchant_key"], "WD_00", "Success")
        # 4、执行代付task#withdrawQuery，接口500
        self.global_payment_mock.update_withdraw_query("500")
        run_task_by_order_no(req["merchant_key"])
        run_task_by_order_no(req["merchant_key"])
        # 4、执行代付task#withdrawQuery，订单号不一致
        withdraw1 = get_withdraw_receipt_by_channel_key(resp["data"]["channel_key"])
        self.global_payment_mock.update_withdraw_query("success", withdraw1[0]["withdraw_receipt_channel_inner_key"])
        run_task_by_order_no(req["merchant_key"])
        run_task_by_order_no(req["merchant_key"])
        assert_withdrawandreceipt_process(req2["trade_no"], req["merchant_key"], "WD_00", "Success")
        # 4、执行代付task#withdrawQuery，金额不一致
        withdraw2 = get_withdraw_receipt_by_channel_key(resp2["data"]["channel_key"])
        self.global_payment_mock.update_withdraw_query("success", withdraw2[0]["withdraw_receipt_channel_inner_key"],
                                                       "1.18")
        run_task_by_order_no(req["merchant_key"])
        run_task_by_order_no(req["merchant_key"])
        assert_withdrawandreceipt_process(req2["trade_no"], req["merchant_key"], "WD_00", "Success")
        # 4、执行代付task#withdrawQuery
        self.global_payment_mock.update_withdraw_query("success", withdraw2[0]["withdraw_receipt_channel_inner_key"])
        run_task_by_order_no(req["merchant_key"], except_json='{"code": 0, "message": "代付提现查询成功"}')
        assert_withdrawandreceipt_success(req2["trade_no"], req["merchant_key"], "WD_00_00", "Success")

    print("下面的通道没有使用了，这个代码是之前的代码，暂时只做屏蔽，不做删除")

    # from biztest.function.global_payment.global_payment_db_operation import get_available_uuid, get_withhold_receipt_by_merchant_key, \
    #     update_withhold_receipt_create_at, update_channel_error, get_carduuid_bycardnum
    # from biztest.interface.payment_global.payment_global_interface import gbpay_checkout_charge_callback
    # from pprint import pprint

    def test_gbpay_checkout_token_fail(self):
        four_element = get_four_element_global()
        # channel = "gbpay_%s_checkout" % self.sign_company
        # account = get_available_uuid("account", 1)[0]
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_fail()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # Assert.assert_match_json({"code": 1,
        #                           "data": {"amount": 1111,
        #                                    "balance_not_enough": 0,
        #                                    "channel_code": "KN_NO_CHANNEL_CODE",
        #                                    "channel_message": "failed to obtain token, code[54]",
        #                                    "channel_name": channel,
        #                                    "payment_data": {},
        #                                    "platform_code": "KN_UNKNOWN_ERROR",
        #                                    "platform_message": "unknown error, please retry again",
        #                                    "status": 3},
        #                           "message": "交易失败"}, resp, "代扣失败")
        # merchant_key = req["merchant_key"]
        # check_withhold(merchant_key, account, 3)
        # check_withhold_receipt(merchant_key, account, 3, channel, "KN_NO_CHANNEL_CODE",
        #                        "failed to obtain token, code[54]")

    def test_gbpay_checkout_charge_fail(self):
        four_element = get_four_element_global()
        # channel = "gbpay_%s_checkout" % self.sign_company
        # account = get_available_uuid("account", 1)[0]
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_fail()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # Assert.assert_match_json({"code": 1,
        #                           "data": {"amount": 1111,
        #                                    "balance_not_enough": 0,
        #                                    "channel_code": "KN_NO_CHANNEL_CODE",
        #                                    "channel_message": "msg[null],code[WH_54]",
        #                                    "channel_name": channel,
        #                                    "payment_data": {},
        #                                    "platform_code": "KN_UNKNOWN_ERROR",
        #                                    "platform_message": "unknown error, please retry again",
        #                                    "status": 3},
        #                           "message": "交易失败"}, resp, "代扣失败")
        # merchant_key = req["merchant_key"]
        # check_withhold(merchant_key, account, 3)
        # check_withhold_receipt(merchant_key, account, 3, channel, "KN_NO_CHANNEL_CODE", "msg[null],code[WH_54]")

    def test_gbpay_checkout_3d_secured_fail(self):
        four_element = get_four_element_global()
        # channel = "gbpay_%s_checkout" % self.sign_company
        # account = get_available_uuid("account", 1)[0]
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_fail()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # Assert.assert_match_json({"code": 1,
        #                           "data": {"amount": 1111,
        #                                    "balance_not_enough": 0,
        #                                    "channel_code": "KN_NO_CHANNEL_CODE",
        #                                    "channel_message": "failed to obtain html",
        #                                    "channel_name": channel,
        #                                    "payment_data": {},
        #                                    "platform_code": "KN_UNKNOWN_ERROR",
        #                                    "platform_message": "unknown error, please retry again",
        #                                    "status": 3},
        #                           "message": "交易失败"}, resp, "代扣失败")
        # merchant_key = req["merchant_key"]
        # check_withhold(merchant_key, account, 3)
        # check_withhold_receipt(merchant_key, account, 3, channel, "KN_NO_CHANNEL_CODE", "failed to obtain html")

    def test_gbpay_checkout_3d_secured_success(self):
        four_element = get_four_element_global()
        # channel = "gbpay_%s_checkout" % self.sign_company
        # account = get_available_uuid("account", 1)[0]
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # Assert.assert_match_json({"code": 2,
        #                           "data": {"amount": 1111,
        #                                    "balance_not_enough": 0,
        #                                    "channel_code": "KN_REQUEST_SUCCESS",
        #                                    "channel_message": "KN_REQUEST_SUCCESS",
        #                                    "channel_name": channel,
        #                                    "payment_data": {"html": r"<!DOCTYPE html>"},
        #                                    "platform_code": "E20002",
        #                                    "platform_message": "PROCESSING",
        #                                    "status": 1},
        #                           "message": "交易进行中"}, resp, "代扣失败")
        # merchant_key = req["merchant_key"]
        # check_withhold(merchant_key, account, 1)
        # check_withhold_receipt(merchant_key, account, 1, channel, "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")

    def test_gbpay_checkout_charge_repead_order(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_qrcode_query_exist()
        # self.global_payment_mock.update_qrcode_withohold_500()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # Assert.assert_match_json({"code": 2,
        #                           "data": {"amount": 1111,
        #                                    "balance_not_enough": 0,
        #                                    "channel_code": "KN_REPEAT_ORDER",
        #                                    "channel_message": "KN_REPEAT_ORDER",
        #                                    "channel_name": channel,
        #                                    "payment_data": {},
        #                                    "payment_option": "",
        #                                    "payment_type": "checkout",
        #                                    "platform_code": "KN_UNKNOWN_ERROR",
        #                                    "platform_message": "unknown error, please retry again",
        #                                    "status": 1},
        #                           "message": "交易进行中"},
        #                          resp,
        #                          "代扣请求成功")
        # merchant_key = req["merchant_key"]
        # check_withhold(merchant_key, account, 1)
        # check_withhold_receipt(merchant_key, account, 1, channel, "KN_REPEAT_ORDER", "KN_REPEAT_ORDER")

    def test_gbpay_checkout_query_success(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # self.global_payment_mock.update_checkout_query_success(withhold_receipt)
        # run_task_by_order_no(merchant_key, {"code": 0, "message": "支付订单查询成功"})
        # run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # check_withhold(merchant_key, account, 2)
        # check_withhold_receipt(merchant_key, account, 2, channel, "WH_00_A_00", "SUCCESS")

    def test_gbpay_checkout_query_fail(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # self.global_payment_mock.update_checkout_query_fail(withhold_receipt)
        # update_channel_error("gbpay", "WH_00_D_55", "", 1, "CHARGE_QUERY")
        # run_task_by_order_no(merchant_key, {"code": 1, "message": "支付订单查询失败"})
        # run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # check_withhold(merchant_key, account, 3)
        # check_withhold_receipt(merchant_key, account, 3, channel, "WH_00_D_55", "WH_00_D_55")

    def test_gbpay_checkout_query_process(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # self.global_payment_mock.update_checkout_query_process(withhold_receipt)
        # update_channel_error("gbpay", "G", "", 2, "CHARGE_QUERY")
        # run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        # check_withhold(merchant_key, account, 1)
        # check_withhold_receipt(merchant_key, account, 1, channel, "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")

    def test_gbpay_checkout_query_not_exist(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # self.global_payment_mock.update_checkout_query_not_exit()
        # update_channel_error("gbpay", "WH_02", "", 1, "CHARGE_QUERY")
        # run_task_by_order_no(merchant_key, {"code": 1, "message": "支付订单查询失败"})
        # run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # check_withhold(merchant_key, account, 3)
        # check_withhold_receipt(merchant_key, account, 3, channel, "WH_02", "Invalid referenceNo.")

    def test_gbpay_checkout_query_500(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # self.global_payment_mock.update_checkout_query_500()
        # run_task_by_order_no(merchant_key, {"code": 2, "message": "代扣订单正在处理中！需要重试！"})
        # check_withhold(merchant_key, account, 1)
        # check_withhold_receipt(merchant_key, account, 1, channel, "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")

    def test_gbpay_checkout_query_timeout_order_success(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # update_withhold_receipt_create_at(merchant_key, month=-1)
        # self.global_payment_mock.update_checkout_query_success(withhold_receipt)
        #
        # run_task_by_order_no(merchant_key, {"code": 0, "message": "支付订单查询成功"})
        # run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # check_withhold(merchant_key, account, 2)
        # check_withhold_receipt(merchant_key, account, 2, channel, "WH_00_A_00", "SUCCESS")

    def test_gbpay_checkout_query_timeout_order_fail(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # update_withhold_receipt_create_at(merchant_key, month=-1)
        # self.global_payment_mock.update_checkout_query_fail(withhold_receipt)
        # update_channel_error("gbpay", "WH_00_D_55", "", 1, "CHARGE_QUERY")
        #
        # run_task_by_order_no(merchant_key, {"code": 1, "message": "支付订单查询失败"})
        # run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # check_withhold(merchant_key, account, 3)
        # check_withhold_receipt(merchant_key, account, 3, channel, "WH_00_D_55", "WH_00_D_55")

    def test_gbpay_checkout_query_timeout_order_process(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # update_withhold_receipt_create_at(merchant_key, month=-1)
        # self.global_payment_mock.update_checkout_query_process(withhold_receipt)
        # update_channel_error("gbpay", "WH_00_G", "", 2, "CHARGE_QUERY")
        #
        # run_task_by_order_no(merchant_key, {"code": 1, "message": "支付订单查询订单超时"})
        # run_task_by_order_no(merchant_key, {"code": 0, "message": r"代扣订单\[.*\]状态更新成功！", "data": None})
        # check_withhold(merchant_key, account, 3)
        # check_withhold_receipt(merchant_key, account, 3, channel, "KN_TIMEOUT_CLOSE_ORDER", "KN_TIMEOUT_CLOSE_ORDER")

    def test_gbpay_checkout_close_order_status_success(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # self.global_payment_mock.update_checkout_query_success(withhold_receipt)
        # close_req, close_resp = global_withhold_close_order(merchant_key)
        # Assert.assert_match_json({"code": 1,
        #                           "data": None,
        #                           "message": "订单已经成为终态，关闭订单失败"},
        #                          close_resp,
        #                          "关单失败")
        # run_task_by_order_no(merchant_key, {"code": 0})
        # check_withhold(merchant_key, account, 2)
        # check_withhold_receipt(merchant_key, account, 2, channel, "WH_00_A_00", "SUCCESS")

    def test_gbpay_checkout_close_order_status_fail(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # self.global_payment_mock.update_checkout_query_fail(withhold_receipt)
        # close_req, close_resp = global_withhold_close_order(merchant_key)
        # Assert.assert_match_json({"code": 1,
        #                           "data": None,
        #                           "message": "订单已经成为终态，关闭订单失败"},
        #                          close_resp,
        #                          "关单失败")
        # run_task_by_order_no(merchant_key, {"code": 0})
        # check_withhold(merchant_key, account, 3)
        # check_withhold_receipt(merchant_key, account, 3, channel, "WH_00_D_55", "WH_00_D_55")

    def test_gbpay_checkout_close_order_status_process(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # self.global_payment_mock.update_checkout_query_process(withhold_receipt)
        # close_req, close_resp = global_withhold_close_order(merchant_key)
        # Assert.assert_match_json({"code": 0,
        #                           "message": "关闭订单成功",
        #                           "data": {
        #                               "platform_code": "E20000",
        #                               "platform_message": "WH_00_G",
        #                               "channel_name": channel,
        #                               "channel_code": "KN_MANUAL_CLOSE_ORDER",
        #                               "channel_message": "SUCCESS"}},
        #                          close_resp,
        #                          "关单失败")
        # run_task_by_order_no(merchant_key)
        # check_withhold(merchant_key, account, 3)
        # check_withhold_receipt(merchant_key, account, 3, channel, "KN_MANUAL_CLOSE_ORDER", "WH_00_G")

    def test_gbpay_checkout_charge_callback(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_checkout" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # self.global_payment_mock.update_checkout_3d_secured_success()
        # req, resp = global_withhold_autopay("cymo1", "checkout",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # merchant_key = req["merchant_key"]
        # withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
        # req, resp = gbpay_checkout_charge_callback(channel,
        #                                            withhold_receipt[0]["withhold_receipt_amount"] / 100,
        #                                            withhold_receipt[0]["withhold_receipt_channel_key"])
        # Assert.assert_match_json({"resultCode": "00"}, resp, "回调成功")
        #
        # run_task_by_order_no(withhold_receipt[0]["withhold_receipt_channel_key"],
        #                      {"code": 0, "data": None, "message": "处理成功"})
        # run_task_by_order_no(merchant_key)
        # check_withhold(merchant_key, account, 2)
        # check_withhold_receipt(merchant_key, account, 2, channel, "WH_00_S_00", "callback WH_00")

    def test_gbpay_withhold_token_fail(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_withhold" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_fail()
        # req, resp = global_withhold_autopay(self.sign_company, "withhold",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # Assert.assert_match_json({"code": 2,
        #                           "data": {"amount": 1111,
        #                                    "balance_not_enough": 0,
        #                                    "channel_code": "KN_NO_CHANNEL_CODE",
        #                                    "channel_message": "failed to obtain token, code[54]",
        #                                    "channel_name": channel,
        #                                    "payment_type": "withhold",
        #                                    "payment_data": {},
        #                                    "platform_code": "KN_UNKNOWN_ERROR",
        #                                    "platform_message": "unknown error, please retry again",
        #                                    "status": 1},
        #                           "message": "交易进行中"}, resp, "代扣失败")
        # pprint(resp)
        # merchant_key = req["merchant_key"]
        # check_withhold(merchant_key, account, 1)
        # check_withhold_receipt(merchant_key, account, 1, channel, "KN_NO_CHANNEL_CODE",
        #                        "failed to obtain token, code[54]")

    def test_gbpay_withhold_charge_fail(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_withhold" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_fail()
        # req, resp = global_withhold_autopay("cymo1", "withhold",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # pprint(resp)
        # Assert.assert_match_json({"code": 2,
        #                           "data": {"amount": 1111,
        #                                    "balance_not_enough": 0,
        #                                    "channel_code": "WH_54",
        #                                    "channel_name": channel,
        #                                    "payment_data": {},
        #                                    "payment_type": "withhold",
        #                                    "platform_code": "E20002",
        #                                    "platform_message": "PROCESSING",
        #                                    "status": 1},
        #                           "message": "交易进行中"}, resp, "代扣失败")
        # merchant_key = req["merchant_key"]
        # check_withhold(merchant_key, account, 1)
        # check_withhold_receipt(merchant_key, account, 1, channel, "WH_54", "")

    def test_gbpay_withhold_charge_success(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_withhold" % self.sign_company
        # self.global_payment_mock.update_checkout_query_not_exit()
        # self.global_payment_mock.update_checkout_token_success()
        # self.global_payment_mock.update_checkout_charge_success()
        # req, resp = global_withhold_autopay("cymo1", "withhold",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # pprint(resp)
        # Assert.assert_match_json({"code": 2,
        #                           "data": {"amount": 1111,
        #                                    "balance_not_enough": 0,
        #                                    "channel_code": "KN_REQUEST_SUCCESS",
        #                                    "channel_message": "KN_REQUEST_SUCCESS",
        #                                    "channel_name": channel,
        #                                    "payment_type": "withhold",
        #                                    "platform_code": "E20002",
        #                                    "platform_message": "PROCESSING",
        #                                    "status": 1},
        #                           "message": "交易进行中"}, resp, "代扣失败")
        # merchant_key = req["merchant_key"]
        # check_withhold(merchant_key, account, 1)
        # check_withhold_receipt(merchant_key, account, 1, channel, "KN_REQUEST_SUCCESS", "KN_REQUEST_SUCCESS")

    def test_gbpay_withhold_charge_repead_order(self):
        four_element = get_four_element_global()
        # account = get_available_uuid("account", 1)[0]
        # channel = "gbpay_%s_withhold" % self.sign_company
        # self.global_payment_mock.update_qrcode_query_exist()
        # self.global_payment_mock.update_qrcode_withohold_500()
        # req, resp = global_withhold_autopay("cymo1", "withhold",
        #                                     card_uuid=account["account_card_uuid"],
        #                                     card_num=four_element["data"]["card_num_encrypt"])
        # pprint(resp)
        # Assert.assert_match_json({"code": 2,
        #                           "data": {"amount": 1111,
        #                                    "balance_not_enough": 0,
        #                                    "channel_code": "KN_REPEAT_ORDER",
        #                                    "channel_message": "KN_REPEAT_ORDER",
        #                                    "channel_name": channel,
        #                                    "payment_data": {},
        #                                    "payment_option": "",
        #                                    "payment_type": "withhold",
        #                                    "platform_code": "KN_UNKNOWN_ERROR"
        #                                                     "",
        #                                    "platform_message": "unknown error, please retry again",
        #                                    "status": 1},
        #                           "message": "交易进行中"},
        #                          resp,
        #                          "代扣请求成功")
        # merchant_key = req["merchant_key"]
        # check_withhold(merchant_key, account, 1)
        # check_withhold_receipt(merchant_key, account, 1, channel, "KN_REPEAT_ORDER", "KN_REPEAT_ORDER")
