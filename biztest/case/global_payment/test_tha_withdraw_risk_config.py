# -*- coding: utf-8 -*-
import pytest

from biztest.config.easymock.easymock_config import global_payment_easy_mock
from biztest.config.payment_global.global_payment_nacos import PaymentNacos
from biztest.function.global_payment.global_payment_check_function import \
    assert_check_withdraw_withdrawreceipt_initinfo, \
    assert_withdrawandreceipt_process, assert_withdrawandreceipt_success, assert_withdrawandreceipt_fail
from biztest.function.global_payment.global_payment_db_function import get_carduuid_bycardnum
from biztest.function.global_payment.global_payment_db_operation import update_withdraw_receipt_create_at
from biztest.interface.payment_global.payment_global_interface import run_task_by_order_no, auto_withdraw, \
    clear_cache
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_gbpay_mock import GbpayMock
from biztest.util.tools.tools import get_sysconfig

env = get_sysconfig("--env")
country = get_sysconfig("--country")
provider = "gbpay"
sign_company = "amberstar1"
channel_name_withdraw = "gbpay_amberstar1_withdraw"
channel_name_qrcode = "gbpay_amberstar1_qrcode"
channel_name_verify = "gbpay_cymo1_verify"
card_uuid = "6621102700001270802"  # 对应的卡号为enc_03_3513454134508920832_259，必须和用户中心返回的一致
user_uuid = "197222248434630658"
switch_card_uuid = "6621091000001268402"  # 对应的卡号为 enc_04_3251058110374617088_714，必须和用户中心返回的一致
switch_user_uuid = "6323231091032322682"
project_id = "5b9a3ddd3a0f7700206522eb"  # mock
nacos_domain = "nacos-test-tha.starklotus.com"  # nacos

"""
    1.如果配置不存在，默认针对同一用户进行12小时内4笔交易的限制
    2.如果enable=false，表示校验规则不启用，即全部放开
    3.当没有特殊white_config白名单时，使用默认的校验规则
    4.当有指定white_config白名单时，区分不同业务系统的 重复放款校验配置（包括笔数、时间）
    5.当all_white=true或指定card_uuid在white_config白名单中的card_uuid时，需要放开校验，允许所有交易。
    6.优先判断 card_uuid或者user_uuid其一 是否重复代付（适用于放款业务），仅user_uuid为空时判断card_uuid 是否重复代付（适用于提现业务）
    7.注意菲律宾线下放款业务的card_uuid都是一个，需要特殊处理（菲律宾线下取款时，不会传入card_uuid，因此系统中card_uuid为内部卡invalid_card_uuid，需排除在校验规则之外）

    author: fangchangfang
    date: 2020-04-22
"""

class TestThailandGbpay:

    # 所有用例前执行
    def setup_class(cls):
        # 使用固定的 card_uuid+user_uuid
        cls.account = get_carduuid_bycardnum("account", "enc_03_3513454134508920832_259")[0]
        # 修改kv，使走到mock
        cls.global_payment_nacos = PaymentNacos(nacos_domain)
        # 默认nacos配置usercenter.properties中用户中心一直是mock地址，修改地址需要重启
        # cls.global_payment_nacos.update_user_center_config(project_id=project_id)
        cls.global_payment_nacos.update_gbpay_withdraw(project_id=project_id)
        cls.global_payment_nacos.update_gbpay_qrcode(project_id=project_id)
        cls.global_payment_nacos.update_gbpay_verify(project_id=project_id)

    # 每个用例前执行
    def setup(cls):
        # 由于用同一个user_uuid会导致控制拦截
        update_withdraw_receipt_create_at()
        # mock使fk返回用户信息和卡信息与本地库数据一致
        cls.global_payment_mock = GbpayMock(global_payment_easy_mock)
        # 修改mock
        cls.global_payment_mock.update_fk_userinfo(
            cls.account["card_id_num"], cls.account["card_username"], cls.account["card_account"])
        clear_cache()  # 有时候直接修改数据库配置，会有缓存的问题

    # 每个类的最后需要还原之前的修改，并关闭数据库链接
    @classmethod
    def teardown_class(cls):
        # cls.global_payment_nacos.update_user_center_config()  # 不管是日常测试还是自动化测试，用户中心都暂时先一直使用mock
        cls.global_payment_nacos.update_gbpay_verify()  # 不管是日常测试还是自动化测试，绑卡都暂时先一直使用mock
        cls.global_payment_nacos.update_gbpay_withdraw()
        cls.global_payment_nacos.update_gbpay_qrcode()
        cls.global_payment_nacos.update_auto_withdraw_risk_white(enable="true")
        DataBase.close_connects()

    @pytest.mark.global_payment_auto_withdraw_risk_white
    def test_withdraw_risk_white_no_limit(self):
        # 如果enable=false，表示校验规则不启用，即全部放开
        self.global_payment_nacos.update_auto_withdraw_risk_white(enable="false")
        for c in range(2):
            # 1、修改mock，使代付能够成功
            # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
            self.global_payment_mock.update_withdraw_balance("enough")
            self.global_payment_mock.update_withdraw_query("not_exit")
            self.global_payment_mock.update_withdraw("success")
            # 2、使用固定的 card_uuid 发起代付
            req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
            # 3、执行代付task#withdraw
            run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
            # 检查withdraw／withdraw_receipt基础信息
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                           channel_name_withdraw)
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"],  code="WD_00", message="Success")
            # 3、需要修改一下查询的mock
            self.global_payment_mock.update_withdraw_query("success")
            # 4、执行代付task#withdrawQuery
            run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
            # 检查withdraw／withdraw_receipt的终态信息
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="WD_00_00", message="Success")

    @pytest.mark.global_payment_auto_withdraw_risk_white
    def test_withdraw_risk_white_limit_12_2(self):
        # 如果enable=true，表示校验规则启用，根据card_uuid或者user_uuid其一满足 --》12小时内2笔交易的限制
        self.global_payment_nacos.update_auto_withdraw_risk_white(enable="true")
        for c in range(2):
            # 1、修改mock，使代付能够成功
            # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
            self.global_payment_mock.update_withdraw_balance("enough")
            self.global_payment_mock.update_withdraw_query("not_exit")
            self.global_payment_mock.update_withdraw("success")
            # 2、使用固定的 card_uuid 发起代付
            req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
            # 3、执行代付task#withdraw
            run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
            # 检查withdraw／withdraw_receipt基础信息
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                           channel_name_withdraw)
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"],  code="WD_00", message="Success")
            # 3、需要修改一下查询的mock
            self.global_payment_mock.update_withdraw_query("success")
            # 4、执行代付task#withdrawQuery
            run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
            # 检查withdraw／withdraw_receipt的终态信息
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="WD_00_00", message="Success")
        # 第三笔会因为风控拦截而放款失败（和前两笔是一样的card_uuid+card_uuid）
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付订单更新成功！"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw)
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "KN_RISK_CONTROL", "风控拦截:疑似重复放款")

        # 第4笔会因为风控拦截而放款失败（和前两笔card_uuid是一样的，user_uuid和card_uuid有一个触发上限都会触发拦截）
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, switch_user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付订单更新成功！"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], switch_user_uuid, card_uuid,
                                                       channel_name_withdraw)
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "KN_RISK_CONTROL", "风控拦截:疑似重复放款")

        # 第5笔会因为风控拦截而放款失败（和最前两笔user_uuid是一样的，user_uuid和card_uuid有一个触发上限都会触发拦截）
        # mock使fk返回用户信息和卡信息与本地库数据一致，换卡必须修改用户中心的返回卡
        global_payment_mock = GbpayMock(global_payment_easy_mock)
        global_payment_mock.update_fk_userinfo('enc_02_2773064776828854272_908', 'enc_04_2873140847753830400_459',
                                               'enc_04_3251058110374617088_714', bank_code="T00008")
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、换卡  重新发起代付
        req_retry, resp_retry = auto_withdraw(sign_company, switch_card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdrawUpdate
        run_task_by_order_no(req_retry["merchant_key"], except_json={"code": 0, "message": "代付订单更新成功！"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req_retry["trade_no"], req_retry["merchant_key"], user_uuid, switch_card_uuid,  channel_name_withdraw)
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_fail(req_retry["trade_no"], req_retry["merchant_key"], "KN_RISK_CONTROL", "风控拦截:疑似重复放款")

    @pytest.mark.global_payment_auto_withdraw_risk_white
    def test_withdraw_risk_white_merchant_name_no_limit(self):
        # 当all_white=true时，需要根据merhcnat_name放开校验，允许所有交易
        self.global_payment_nacos.update_auto_withdraw_risk_white(all_white="true")
        for c in range(4):
            # 1、修改mock，使代付能够成功
            # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
            self.global_payment_mock.update_withdraw_balance("enough")
            self.global_payment_mock.update_withdraw_query("not_exit")
            self.global_payment_mock.update_withdraw("success")
            # 2、使用固定的 card_uuid 发起代付
            req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
            # 3、执行代付task#withdraw
            run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
            # 检查withdraw／withdraw_receipt基础信息
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                           channel_name_withdraw)
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"],  code="WD_00", message="Success")
            # 3、需要修改一下查询的mock
            self.global_payment_mock.update_withdraw_query("success")
            # 4、执行代付task#withdrawQuery
            run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
            # 检查withdraw／withdraw_receipt的终态信息
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="WD_00_00", message="Success")

    @pytest.mark.global_payment_auto_withdraw_risk_white
    def test_withdraw_risk_white_card_uuid_no_limit(self):
        # 当all_white=false但card_uuid在white_config白名单中的时，那么该card_uuid允许所有交易
        self.global_payment_nacos.update_auto_withdraw_risk_white(all_white="false", card_uuid=card_uuid)
        for c in range(2):
            # 1、修改mock，使代付能够成功
            # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
            self.global_payment_mock.update_withdraw_balance("enough")
            self.global_payment_mock.update_withdraw_query("not_exit")
            self.global_payment_mock.update_withdraw("success")
            # 2、使用固定的 card_uuid 发起代付
            req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
            # 3、执行代付task#withdraw
            run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
            # 检查withdraw／withdraw_receipt基础信息
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                           channel_name_withdraw)
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"],  code="WD_00", message="Success")
            # 3、需要修改一下查询的mock
            self.global_payment_mock.update_withdraw_query("success")
            # 4、执行代付task#withdrawQuery
            run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
            # 检查withdraw／withdraw_receipt的终态信息
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="WD_00_00", message="Success")

    @pytest.mark.global_payment_auto_withdraw_risk_white
    def test_withdraw_risk_white_card_uuid_no_limit_nouseruuuid(self):
        # 当all_white=false但card_uuid在white_config白名单中的时，那么该card_uuid允许所有交易
        self.global_payment_nacos.update_auto_withdraw_risk_white(all_white="false", card_uuid=card_uuid)
        for c in range(2):
            # 1、修改mock，使代付能够成功
            # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
            self.global_payment_mock.update_withdraw_balance("enough")
            self.global_payment_mock.update_withdraw_query("not_exit")
            self.global_payment_mock.update_withdraw("success")
            # 2、使用固定的 card_uuid 发起代付
            req, resp = auto_withdraw(sign_company, card_uuid, user_uuid="", channel_name=channel_name_withdraw)
            # 3、执行代付task#withdraw
            run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
            # 检查withdraw／withdraw_receipt基础信息
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], "", card_uuid, channel_name_withdraw)
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"],  code="WD_00", message="Success")
            # 3、需要修改一下查询的mock
            self.global_payment_mock.update_withdraw_query("success")
            # 4、执行代付task#withdrawQuery
            run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
            # 检查withdraw／withdraw_receipt的终态信息
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="WD_00_00", message="Success")

    @pytest.mark.global_payment_auto_withdraw_risk_white
    def test_withdraw_risk_white_limit_carduuuid(self):
        # 当all_white=false且card_uuid为空时，表示校验规则启用。根据card_uuuidj校验12小时内2笔交易的限制；
        self.global_payment_nacos.update_auto_withdraw_risk_white(all_white="false", card_uuid="")
        for c in range(2):
            # 1、修改mock，使代付能够成功
            # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
            self.global_payment_mock.update_withdraw_balance("enough")
            self.global_payment_mock.update_withdraw_query("not_exit")
            self.global_payment_mock.update_withdraw("success")
            # 2、使用固定的 card_uuid 发起代付
            req, resp = auto_withdraw(sign_company, card_uuid, user_uuid="", channel_name=channel_name_withdraw)
            # 3、执行代付task#withdraw
            run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
            # 检查withdraw／withdraw_receipt基础信息
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], "", card_uuid, channel_name_withdraw)
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"],  code="WD_00", message="Success")
            # 3、需要修改一下查询的mock
            self.global_payment_mock.update_withdraw_query("success")
            # 4、执行代付task#withdrawQuery
            run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
            # 检查withdraw／withdraw_receipt的终态信息
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="WD_00_00", message="Success")
        # 第三笔会因为风控拦截而放款失败
        # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
        self.global_payment_mock.update_withdraw_balance("enough")
        self.global_payment_mock.update_withdraw_query("not_exit")
        self.global_payment_mock.update_withdraw("success")
        # 2、使用固定的 card_uuid 发起代付
        req, resp = auto_withdraw(sign_company, card_uuid, user_uuid, channel_name=channel_name_withdraw)
        # 3、执行代付task#withdrawUpdate
        run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付订单更新成功！"})
        # 检查withdraw／withdraw_receipt基础信息
        assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], user_uuid, card_uuid,
                                                       channel_name_withdraw)
        # 检查withdraw／withdraw_receipt的终态信息
        assert_withdrawandreceipt_fail(req["trade_no"], req["merchant_key"], "KN_RISK_CONTROL", "风控拦截:疑似重复放款")

    @pytest.mark.global_payment_auto_withdraw_risk_white
    def test_withdraw_risk_invalid_card_uuid(self):
        #菲律宾线下取款时，不会传入card_uuid，因此系统中card_uuid为内部卡，需排除在校验规则之外，不受交易次数限制；
        self.global_payment_nacos.update_auto_withdraw_risk_white(all_white="invalid_card_uuid", card_uuid=card_uuid)
        for c in range(5):
            # 1、修改mock，使代付能够成功
            # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
            self.global_payment_mock.update_withdraw_balance("enough")
            self.global_payment_mock.update_withdraw_query("not_exit")
            self.global_payment_mock.update_withdraw("success")
            # 2、使用固定的 card_uuid 发起代付
            req, resp = auto_withdraw(sign_company, card_uuid, user_uuid="", channel_name=channel_name_withdraw)
            # 3、执行代付task#withdraw
            run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
            # 检查withdraw／withdraw_receipt基础信息
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], "", card_uuid, channel_name_withdraw)
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"],  code="WD_00", message="Success")
            # 3、需要修改一下查询的mock
            self.global_payment_mock.update_withdraw_query("success")
            # 4、执行代付task#withdrawQuery
            run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
            # 检查withdraw／withdraw_receipt的终态信息
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="WD_00_00", message="Success")

    @pytest.mark.global_payment_auto_withdraw_risk_white
    def test_withdraw_risk_test_gbiz(self):
        #菲律宾线下取款时，不会传入card_uuid，因此系统中card_uuid为内部卡，需排除在校验规则之外，不受交易次数限制；
        self.global_payment_nacos.update_auto_withdraw_risk_white(all_white="test", card_uuid=" ")
        for c in range(2):
            # 1、修改mock，使代付能够成功
            # gbiz代付时：先查询余额，余额充足才会路由到该通道。该通道下单之前需要查询一下订单是否存在
            self.global_payment_mock.update_withdraw_balance("enough")
            self.global_payment_mock.update_withdraw_query("not_exit")
            self.global_payment_mock.update_withdraw("success")
            # 2、使用固定的 card_uuid 发起代付
            req, resp = auto_withdraw(sign_company, card_uuid, user_uuid="", channel_name=channel_name_withdraw)
            # 3、执行代付task#withdraw
            run_task_by_order_no(req["merchant_key"], except_json={"code": 2, "message": "代付提现处理中"})
            # 检查withdraw／withdraw_receipt基础信息
            assert_check_withdraw_withdrawreceipt_initinfo(req["trade_no"], req["merchant_key"], "", card_uuid, channel_name_withdraw)
            assert_withdrawandreceipt_process(req["trade_no"], req["merchant_key"],  code="WD_00", message="Success")
            # 3、需要修改一下查询的mock
            self.global_payment_mock.update_withdraw_query("success")
            # 4、执行代付task#withdrawQuery
            run_task_by_order_no(req["merchant_key"], except_json={"code": 0, "message": "代付提现查询成功"})
            # 检查withdraw／withdraw_receipt的终态信息
            assert_withdrawandreceipt_success(req["trade_no"], req["merchant_key"], code="WD_00_00", message="Success")

