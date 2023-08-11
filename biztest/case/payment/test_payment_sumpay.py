# -*- coding: utf-8 -*-
import pytest
from biztest.config.payment.url_config import get_env_dict
from biztest.util.tools.tools import get_four_element_in_payment
from biztest.function.payment.payment_db_operation import get_binding_info_by_card_num, \
    get_binding_request_info_by_card_num, get_binding_sms_request_info_by_card_num, \
    get_withhold_receipt_info_by_card_num, get_withhold_info_by_card_num
from biztest.interface.payment.payment_interface import withhold_bindsms, withhold_bind, \
    auto_withhold, auto_private_withdraw
from biztest.util.asserts.assert_util import Assert
import common.global_const as gc


@pytest.mark.payment
@pytest.mark.payment_sumpay
class TestPaymentSumpay:
    env = gc.ENV
    env_test = get_env_dict(env)
    db_test_payment = gc.PAYMENT_DB

    @pytest.mark.skip
    def test_sumpay_protocol(self):  # 统统付绑卡和协议支付测试环境没有证书，跑不通
        """
        通联协议支付测试
        :return:
        """
        self.four_element = get_four_element_in_payment()
        channel_name = "sumpay_tra_protocol"
        # 组装获取验证码参数
        resp_bindsms = withhold_bindsms(self.four_element, channel_name)
        assert resp_bindsms["code"] == 0, '获取验证码成功'

        # 传入通道进行绑卡
        resp_withhold_bind = withhold_bind(self.four_element, channel_name, 111111, resp_bindsms["data"]["verify_seq"])
        assert resp_withhold_bind["code"] == 0, "绑卡成功"

        # 绑卡成功后检查binding_sms_request、binding_request和binding表
        params_card_num = self.four_element["bank_code_encrypt"]
        binding_sms_request = get_binding_sms_request_info_by_card_num(params_card_num)
        assert binding_sms_request[0]["binding_sms_request_channel"] == channel_name, "获取短信通道"
        assert binding_sms_request[0]["binding_sms_request_status"] == "success", "短信验证码获取成功"

        binding_request_info = get_binding_request_info_by_card_num(params_card_num)
        assert binding_request_info[0]["binding_request_channel"] == channel_name, "绑卡通道"
        assert binding_request_info[0]["binding_request_status"] == 0, "绑卡请求成功"

        binding_info = get_binding_info_by_card_num(params_card_num)
        assert binding_info[0]["binding_channel_name"] == channel_name, "绑卡通道"
        assert binding_info[0]["binding_status"] == 1, "绑卡成功"

        # 发起代扣
        resp_withhold_autopay = auto_withhold(self.four_element, channel_name)

        withhold_info = get_withhold_info_by_card_num(params_card_num)
        withhold_receipt_info = get_withhold_receipt_info_by_card_num(params_card_num)
        # 检查卡号和通道存储
        withhold_info[0]['withhold_card_num'] = self.four_element["bank_code_encrypt"]
        withhold_receipt_info[0]['withhold_receipt_card_num'] = self.four_element["bank_code_encrypt"]
        withhold_receipt_info[0]['withhold_receipt_channel_name'] = channel_name

        if withhold_info[0]["withhold_status"] == 2:
            # 代扣成功返回给rbiz的参数断言
            assert resp_withhold_autopay['code'] == 0, "交易成功"
            assert resp_withhold_autopay['message'] == "交易成功", "交易成功"
            assert resp_withhold_autopay['data']['channel_message'] == "交易成功", "交易成功"
            assert resp_withhold_autopay['data']['error_code'] == "E20000", "代扣成功错误码"
            # 检查代扣成功后withhold和withhold_receipt表的数据
            # 对数据库中查询出来的SQL，进行断言  # 或者这样断言  assert withhold_info[0]['withhold_status'] == 2

            Assert.assert_equal(withhold_info[0]["withhold_status"], 2, "代扣成功")
            Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_status"], 2,
                                '代扣成功')
        elif withhold_info[0]["withhold_status"] == 3:
            # 代扣成功返回给rbiz的参数断言
            assert resp_withhold_autopay['code'] == 1, "交易失败"
            # 检查代扣失败后withhold和withhold_receipt表的数据
            Assert.assert_equal(withhold_info[0]["withhold_status"], 3, '代扣失败')
            Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_status"], 3, '代扣失败')
        else:
            print("代扣结果不明确")

    def test_sumpay_withhold(self):
        """
        通联协议支付测试
        :return:
        """
        self.four_element = get_four_element_in_payment()
        channel_name = ""
        params_card_num = self.four_element["bank_code_encrypt"]

        # 发起代扣
        resp_withhold_autopay = auto_withhold(self.four_element, channel_name)

        withhold_info = get_withhold_info_by_card_num(params_card_num)
        withhold_receipt_info = get_withhold_receipt_info_by_card_num(params_card_num)
        # 检查卡号和通道存储
        withhold_info[0]['withhold_card_num'] = self.four_element["bank_code_encrypt"]
        withhold_receipt_info[0]['withhold_receipt_card_num'] = self.four_element["bank_code_encrypt"]
        withhold_receipt_info[0]['withhold_receipt_channel_name'] = channel_name

        if withhold_info[0]["withhold_status"] == 2:
            # 代扣成功返回给rbiz的参数断言
            assert resp_withhold_autopay['code'] == 0, "交易成功"
            assert resp_withhold_autopay['message'] == "交易成功", "交易成功"
            assert resp_withhold_autopay['data']['channel_message'] == "交易成功", "交易成功"
            assert resp_withhold_autopay['data']['error_code'] == "E20000", "代扣成功错误码"
            # 检查代扣成功后withhold和withhold_receipt表的数据
            # 对数据库中查询出来的SQL，进行断言  # 或者这样断言  assert withhold_info[0]['withhold_status'] == 2

            Assert.assert_equal(withhold_info[0]["withhold_status"], 2, "代扣成功")
            Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_status"], 2, '代扣成功')
        elif withhold_info[0]["withhold_status"] == 3:
            # 代扣成功返回给rbiz的参数断言
            assert resp_withhold_autopay['code'] == 1, "交易失败"
            # 检查代扣失败后withhold和withhold_receipt表的数据
            Assert.assert_equal(withhold_info[0]["withhold_status"], 3, '代扣失败')
            Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_status"], 3, '代扣失败')
        else:
            print("代扣结果不明确")

    def test_sumpay_withdraw(self):
        """
        通联代付测试
        :return:
        """
        self.four_element = get_four_element_in_payment()
        channel_name = "qsq_sumpay_tq_protocol"

        # 发起代付
        resp_private_autowithdraw = auto_private_withdraw(channel_name, self.four_element)
        # payment返回给外部：代付是异步处理的，所以code=2
        assert resp_private_autowithdraw['code'] == 2, "代付处理中"
