import json

import common.global_const as gc
from biztest.config.payment.url_config import global_gbiz_callback, global_amount, global_rbiz_callback, \
    user_ip_withhold_remark, global_rbiz_redirect, \
    gbpay_resp_transfer_mode
from biztest.function.global_payment.global_payment_db_function import get_withdraw_by_merchant_key, \
    get_withdraw_receipt_by_merchant_key, get_withhold_by_merchant_key, get_withhold_receipt_by_merchant_key, \
    get_binding_by_card_uuid, get_binding_request_by_merchant_key, get_binding_merchant_request_by_merchant_key, \
    get_fusing_latest, get_fusing_log_by_trace_no
from biztest.function.global_payment.global_payment_db_operation import get_task, get_channel_reconci, \
    get_channel_settlement
from biztest.interface.payment_global.payment_global_interface import global_withdraw_query, global_withhold_query
from biztest.util.asserts.assert_util import Assert
from biztest.util.tools.tools import get_sysconfig


def check_account(card_uuid, account_type):
    account = gc.PAYMENT_DB.do_sql("select account.* from account inner join card on account_card_num=card_num "
                                   "where account_card_uuid='%s' and account_auth_mode='%s'" %
                                   (card_uuid, account_type))
    Assert.assert_equal(len(account), 1, "卡个数正确")


def check_binding(card_uuid, account_type, bind_status, channel_name, cityy="tha", register_name="",
                  protocol_info=None):
    if cityy == "ind":
        binding = gc.PAYMENT_DB.do_sql(
            "select * from binding where binding_card_uuid='%s' and binding_channel_name='%s'" % (
                card_uuid, channel_name))
        if protocol_info is not None:  # 印度开户
            Assert.assert_equal(binding[0]["binding_protocol_info"], protocol_info, "协议支付号正确")
        else:  # 印度验卡
            Assert.assert_equal(binding[0]["binding_register_name"], register_name, "绑卡姓名正确")
    else:
        binding = gc.PAYMENT_DB.do_sql(
            "select binding.* from binding inner join account on binding_card_num=account_card_num "
            "where account_card_uuid='%s' and account_auth_mode='%s' and binding_channel_name='%s'" %
            (card_uuid, account_type, channel_name))
        Assert.assert_equal(len(binding), 1, "绑卡数据个数正确")
    Assert.assert_equal(binding[0]["binding_status"], bind_status, "绑卡状态正确")
    Assert.assert_equal(binding[0]["binding_channel_name"], channel_name, "绑卡通道正确")


def check_binding_request(binding_merchant_key, four_element, bind_status, bind_req, bind_resp, cityy="tha",
                          register_name=""):
    binding_request = gc.PAYMENT_DB.do_sql(
        "select * from binding_request where binding_request_merchant_key='%s'" % binding_merchant_key)
    if cityy == "tha":
        Assert.assert_equal(binding_request[0]["binding_request_idnum"], four_element["data"]["id_number_encrypt"],
                            "身份证正确")
        Assert.assert_equal(binding_request[0]["binding_request_name"], four_element["data"]["user_name_encrypt"],
                            "姓名正确")
        Assert.assert_equal(binding_request[0]["binding_request_mobile"], four_element["data"]["mobile_encrypt"],
                            "手机号正确")
    else:
        Assert.assert_equal(binding_request[0]["binding_request_register_name"], register_name, "用户姓名正确")
    Assert.assert_equal(binding_request[0]["binding_request_channel"], bind_resp["data"]["channel_name"], "通道名正确")
    Assert.assert_equal(binding_request[0]["binding_request_status"], bind_status, "绑卡状态正常")
    Assert.assert_equal(binding_request[0]["binding_request_type"], "BIND", "绑卡类型正确")
    Assert.assert_equal(binding_request[0]["binding_request_channel_code"], bind_resp["data"]["channel_code"],
                        "绑卡返回code正确")
    if "channel_message" in bind_resp["data"].keys():
        Assert.assert_equal(binding_request[0]["binding_request_channel_message"], bind_resp["data"]["channel_message"],
                            "绑卡msg正确")
    # Assert.assert_equal(binding_request[0]["binding_request_bank_code"], bind_req["ifsc"], "绑卡银行号正确")
    Assert.assert_equal(binding_request[0]["binding_request_card_uuid"], bind_resp["data"]["card_uuid"],
                        "绑卡card_uuid正确")


def check_card(card_uuid, account_type, four_element, card_status, bind_req, cityy="tha"):
    if cityy == "ind":
        card = gc.PAYMENT_DB.do_sql("select * from card where card_uuid='%s'" % card_uuid)
    else:
        card = gc.PAYMENT_DB.do_sql("select card.* from card inner join account on card_num=account_card_num where "
                                    "account_card_uuid='%s' and account_auth_mode='%s' and card_auth_mode='%s'" %
                                    (card_uuid, account_type, account_type))
        if account_type == "account":
            Assert.assert_equal(card[0]["card_account"], four_element["data"]["bank_account_encrypt"], "卡号正确")
        elif account_type == "card":
            Assert.assert_equal(card[0]["card_account"], four_element["data"]["card_num_encrypt"], "卡号正确")
        elif account_type == "upi":
            Assert.assert_equal(card[0]["card_account"], four_element["data"]["upi_encrypt"], "卡号正确")
        else:
            raise Exception("account_type错误")
        Assert.assert_equal(card[0]["card_id_num"], four_element["data"]["id_number_encrypt"], "身份证正确")
        Assert.assert_equal(card[0]["card_username"], four_element["data"]["user_name_encrypt"], "姓名正确")
        Assert.assert_equal(card[0]["card_mobile"], four_element["data"]["mobile_encrypt"], "手机号正确")
        Assert.assert_equal(card[0]["card_email"], four_element["data"]["email_encrypt"], "手机号正确")
        Assert.assert_equal(card[0]["card_address"], four_element["data"]["address_encrypt"], "手机号正确")
    # Assert.assert_equal(card[0]["card_bank_code"], bind_req["ifsc"], "银行code正确")
    Assert.assert_equal(card[0]["card_status"], card_status, "卡状态正常")
    Assert.assert_equal(card[0]["card_auth_mode"], account_type, "绑卡类型正确")


def check_autobind_response(autobind_resp, channel_name, card_uuid, user_uuid, register_name, codes="success",
                            channel_code=""):
    if codes == "success":
        Assert.assert_equal(0, autobind_resp["code"], "绑卡成功")
        Assert.assert_equal("E20000", autobind_resp["data"]["platform_code"], "绑卡成功E20000")
        Assert.assert_equal("200", autobind_resp["data"]["channel_code"], "绑卡成功200")
        Assert.assert_equal(register_name, autobind_resp["data"]["register_name_encrypt"], "绑卡成功register_name")
    elif codes == "fail":
        Assert.assert_equal(1, autobind_resp["code"], "绑卡失败")
        Assert.assert_equal("E20001", autobind_resp["data"]["platform_code"], "绑卡失败E20001")
        Assert.assert_equal(channel_code, autobind_resp["data"]["channel_code"], "绑卡失败channel_code")
    else:
        Assert.assert_equal(1, autobind_resp["code"], "绑卡姓名验证失败")
        Assert.assert_equal("E20001", autobind_resp["data"]["platform_code"], "绑卡姓名验证失败E20001")
        Assert.assert_equal("200", autobind_resp["data"]["channel_code"], "绑卡姓名验证失败200")
        Assert.assert_equal(register_name, autobind_resp["data"]["register_name_encrypt"], "绑卡姓名验证失败register_name")
    Assert.assert_equal(channel_name, autobind_resp["data"]["channel_name"], "绑卡channel_name")
    Assert.assert_equal(card_uuid, autobind_resp["data"]["card_uuid"], "绑卡card_uuid")
    Assert.assert_equal(user_uuid, autobind_resp["data"]["user_uuid"], "绑卡user_uuid")


def check_withhold(merchant_key, account, status, account_type="card_uuid"):
    withhold = gc.PAYMENT_DB.do_sql("select * from withhold where withhold_merchant_key='%s'" % merchant_key)[0]
    if account_type == "card_uuid":
        Assert.assert_equal(account["account_card_uuid"], withhold["withhold_card_uuid"], "card_uuid正确")
    else:
        Assert.assert_equal(account["account_user_uuid"], withhold["withhold_user_uuid"], "user_uuid正确")
    Assert.assert_equal(status, withhold["withhold_status"], "status正确")
    Assert.assert_equal(0, withhold["withhold_status_stage"], "status_stage正确")


def check_withhold_receipt(merchant_key, account, status, channel, resp_code, resp_message, expected_data=None,
                           description=None):
    """
    expected_data 用来检查数据库中其它的值，其中的key需要和数据库表中字段保持一致, 如下
    expected_data = {
        "withhold_receipt_channel_inner_key": "plink_G077m2za7mhiVF",
        "withhold_receipt_amount": req["amount"],
        "withhold_receipt_payment_option": "Debit Card",
        "withhold_receipt_payment_mode": "Visa",
        "withhold_receipt_service_charge": 800,
        "withhold_receipt_service_tax": 144
    }
    """
    if expected_data is None:
        expected_data = dict()
    withhold_receipt = gc.PAYMENT_DB.do_sql("select * from withhold_receipt where withhold_receipt_merchant_key='%s'"
                                            % merchant_key)[0]
    Assert.assert_equal(channel, withhold_receipt["withhold_receipt_channel_name"], "channel正确")
    Assert.assert_equal(status, withhold_receipt["withhold_receipt_status"], "status正确")
    Assert.assert_equal(0, withhold_receipt["withhold_receipt_status_stage"], "message正确")
    Assert.assert_equal(resp_code, withhold_receipt["withhold_receipt_channel_resp_code"], "code正确")
    Assert.assert_equal(resp_message, withhold_receipt["withhold_receipt_channel_resp_message"], "message正确")
    if len(expected_data) > 0:
        for key in expected_data:
            Assert.assert_equal(expected_data[key], withhold_receipt[key], "%s正确" % key)
    if withhold_receipt["withhold_receipt_channel_name"] == "xendit_copperstone_paycode":
        Assert.assert_equal(description, withhold_receipt["withhold_receipt_description"], "取款码正确")


def check_autopay_response(autopay_resp, channel_name, amount, channel_code="KN_GENERATE_QR_CODE",
                           codes="success", description="", payment_type=""):
    if codes == "success":
        Assert.assert_equal("E20002", autopay_resp["data"]["platform_code"], "platform_code正确")
        Assert.assert_equal("PROCESSING", autopay_resp["data"]["platform_message"], "platform_message正确")
        if autopay_resp["data"]["payment_type"] == "barcode":
            Assert.assert_equal("https://s3.amazonaws.com/cash_payment_barcodes/sandbox_reference.png",
                                autopay_resp["data"]["payment_data"]["barcode_url"],
                                "barcode_url正确")
            Assert.assert_equal("data:image/png;base64,", autopay_resp["data"]["payment_data"]["image_dat"][:22],
                                "barcode 的 image_dat正确")
        if autopay_resp["data"]["payment_type"] == "paycode":
            Assert.assert_equal(description, autopay_resp["data"]["payment_data"]["wh_number"], "wh_number正确")
        elif autopay_resp["data"]["payment_type"] == "ebank":
            if autopay_resp["data"]["payment_option"] == "wallet" and autopay_resp["data"]["payment_mode"] == "GCash":
                Assert.assert_equal(
                    "https://ewallet-mock-connector.xendit.co/v1/ewallet_connector/checkouts?token=b0d96038-9521-4b4a-a30a-a7a00e0a53d8",
                    autopay_resp["data"]["payment_data"]["redirect_url"][:114],
                    "ebank_url正确")
            elif autopay_resp["data"]["payment_option"] == "store" and autopay_resp["data"][
                "payment_mode"] == "Palawan Pawnshop":
                return
            else:
                Assert.assert_equal("https://payments-test.cashfree.com/order/#",
                                    autopay_resp["data"]["payment_data"]["redirect_url"][:42],
                                    "ebank_url正确")
        else:
            Assert.assert_equal("data:image/png;base64,", autopay_resp["data"]["payment_data"]["image_dat"][:22],
                                "image_dat正确")
    else:
        Assert.assert_equal("KN_UNKNOWN_ERROR", autopay_resp["data"]["platform_code"], "platform_code正确")
        Assert.assert_equal("unknown error, please retry again", autopay_resp["data"]["platform_message"],
                            "platform_message正确")
    Assert.assert_equal(2, autopay_resp["code"], "code正确")
    Assert.assert_equal(channel_name, autopay_resp["data"]["channel_name"], "channel_name正确")
    Assert.assert_equal(channel_code, autopay_resp["data"]["channel_code"], "channel_code正确")
    Assert.assert_equal(amount, autopay_resp["data"]["amount"], "amount正确")
    Assert.assert_equal(1, autopay_resp["data"]["status"], "status正确")
    Assert.assert_equal(payment_type, autopay_resp["data"]["payment_type"], "payment_type正确")


def check_autopay_response_fail(autopay_resp, channel_name, amount, channel_code, channel_message, codes="success"):
    if codes == "success":
        Assert.assert_equal("E20001", autopay_resp["data"]["platform_code"], "platform_code正确")
        Assert.assert_equal("FAILED", autopay_resp["data"]["platform_message"], "platform_message正确")

    else:
        Assert.assert_equal("KN_UNKNOWN_ERROR", autopay_resp["data"]["platform_code"], "platform_code正确")
        Assert.assert_equal("unknown error, please retry again", autopay_resp["data"]["platform_message"],
                            "platform_message正确")
    Assert.assert_equal(1, autopay_resp["code"], "code正确")
    Assert.assert_equal(channel_name, autopay_resp["data"]["channel_name"], "channel_name正确")
    Assert.assert_equal(channel_code, autopay_resp["data"]["channel_code"], "channel_code正确")
    # Assert.assert_equal(channel_message, autopay_resp["data"]["channel_message"], "channel_message正确")
    Assert.assert_equal(amount, autopay_resp["data"]["amount"], "amount正确")
    Assert.assert_equal(3, autopay_resp["data"]["status"], "status正确")


# 已重写检查点，废弃该检查
def check_withdraw(merchant_key, account, status, channel):
    withdraw = gc.PAYMENT_DB.do_sql("select * from withdraw where withdraw_merchant_key='%s' " % merchant_key)[0]
    Assert.assert_equal(status, withdraw["withdraw_status"], "status正确")


# 已重写检查点，废弃该检查
def check_withdraw_receipt(merchant_key, account, status, channel, resp_code, resp_message):
    withdraw_receipt = gc.PAYMENT_DB.do_sql(
        "select * from withdraw_receipt where withdraw_receipt_merchant_key='%s' order by withdraw_receipt_id desc  limit 1"
        % merchant_key)[0]
    Assert.assert_equal(account["account_card_num"], withdraw_receipt["withdraw_receipt_card_num"], "card_num正确")
    Assert.assert_equal(status, withdraw_receipt["withdraw_receipt_status"], "status正确")
    Assert.assert_equal(channel, withdraw_receipt["withdraw_receipt_channel_name"], "channel正确")
    Assert.assert_equal(resp_code, withdraw_receipt["withdraw_receipt_channel_resp_code"], "code正确")
    Assert.assert_equal(resp_message, withdraw_receipt["withdraw_receipt_channel_resp_message"], "message正确")


def check_resp_data(actual_resp, expected_code, expected_message, expected_data=None):
    if expected_data is None:
        expected_data = dict()
    Assert.assert_equal(expected_code, actual_resp['code'], "code正确")
    Assert.assert_equal(expected_message, actual_resp['message'], "message正确")
    if len(expected_data) > 0:
        for key in expected_data:
            if expected_data[key].__class__ == dict:
                expected_sub_dict = expected_data[key]
                actual_resp_sub_dict = actual_resp["data"][key]
                for key in expected_sub_dict:
                    Assert.assert_equal(expected_sub_dict[key], actual_resp_sub_dict[key], "%s正确" % key)
            else:
                Assert.assert_equal(expected_data[key], actual_resp["data"][key], "%s正确" % key)


def check_withhold_channel_request(merchant_key, request_api, request_type):
    withhold_receipt = \
        gc.PAYMENT_DB.do_sql("select * from withhold_receipt where withhold_receipt_merchant_key='%s'" % merchant_key)[
            0]
    channel_request_log = \
        gc.PAYMENT_DB.do_sql("SELECT * FROM channel_request_log WHERE channel_request_log_channel_key='%s' "
                             "order by channel_request_log_id desc limit 1" % withhold_receipt[
                                 "withhold_receipt_channel_key"])[0]
    Assert.assert_equal(request_type, channel_request_log["channel_request_log_type"], "请求类型正确")
    Assert.assert_equal(request_api, channel_request_log["channel_request_log_url"].split("/")[-1], "请求接口正确")


def check_withhold_sendmsg(merchant_key, expected_data):
    """
    expected_data = {
    "platform_code": "E20000",
    "platform_message": "{\"attempts\":1}",
    "channel_name": "razorpay_yomoyo_ebank",
    "channel_code": "paid",
    "channel_message": "{\"attempts\":1}"
   }
    """
    sendmsg = gc.PAYMENT_DB.do_sql("select * from sendmsg where sendmsg_order_no = '%s'" % merchant_key)[0]
    Assert.assert_equal("withholdNotify", sendmsg["sendmsg_type"], "同步消息类型正确")
    sendmsg_content = (json.loads(sendmsg["sendmsg_content"]))["body"]["data"]
    for key in expected_data:
        Assert.assert_equal(sendmsg_content[key], expected_data[key], "%s正确" % key)


def check_reconci_task(task_order_no_list):
    for task_order_no in task_order_no_list:
        task_list = get_task(task_order_no=task_order_no)
        for task in task_list:
            Assert.assert_equal("close", task["task_status"], "task状态不正确，task信息%s" % str(task))


def check_cashfree_reconci():
    reconci_list = get_channel_reconci(channel_reconci_settlement_id=262907)
    except_reconci = [{'channel_reconci_account': '',
                       'channel_reconci_amount': 151050,
                       'channel_reconci_bank_code': '',
                       'channel_reconci_bank_name': 'android_intent',
                       'channel_reconci_channel_key': 'RBIZ41214881041000001',
                       'channel_reconci_channel_name': 'cashfree_yomoyo3_ebank',
                       'channel_reconci_channel_order_no': 'RBIZ41214881041000001',
                       'channel_reconci_fees': 590,
                       'channel_reconci_merchant_no': 'yomoyo3',
                       'channel_reconci_order_created_at': '1000-01-01 00:00:00',
                       'channel_reconci_order_finished_at': '2020-06-11 00:33:07',
                       'channel_reconci_payment_mode': 'UPI',
                       'channel_reconci_product_type': '',
                       'channel_reconci_provider_code': 'cashfree',
                       'channel_reconci_remark': '',
                       'channel_reconci_service_charge': 500,
                       'channel_reconci_service_tax': 90,
                       'channel_reconci_settlement_amount': 150460,
                       'channel_reconci_settlement_id': '262907',
                       'channel_reconci_status': 2,
                       'channel_reconci_type': 'WITHHOLD',
                       'channel_reconci_user_name': ''},
                      {'channel_reconci_account': '',
                       'channel_reconci_amount': 205400,
                       'channel_reconci_bank_code': '',
                       'channel_reconci_bank_name': 'android_intent',
                       'channel_reconci_channel_key': 'RBIZ41214881041000002',
                       'channel_reconci_channel_name': 'cashfree_yomoyo3_ebank',
                       'channel_reconci_channel_order_no': 'RBIZ41214881041000002',
                       'channel_reconci_fees': 590,
                       'channel_reconci_merchant_no': 'yomoyo3',
                       'channel_reconci_order_created_at': '1000-01-01 00:00:00',
                       'channel_reconci_order_finished_at': '2020-06-11 00:36:44',
                       'channel_reconci_payment_mode': 'UPI',
                       'channel_reconci_product_type': '',
                       'channel_reconci_provider_code': 'cashfree',
                       'channel_reconci_remark': '',
                       'channel_reconci_service_charge': 500,
                       'channel_reconci_service_tax': 90,
                       'channel_reconci_settlement_amount': 204810,
                       'channel_reconci_settlement_id': '262907',
                       'channel_reconci_status': 2,
                       'channel_reconci_type': 'WITHHOLD',
                       'channel_reconci_user_name': ''},
                      {'channel_reconci_account': '',
                       'channel_reconci_amount': 151050,
                       'channel_reconci_bank_code': '',
                       'channel_reconci_bank_name': 'android_intent',
                       'channel_reconci_channel_key': 'RBIZ41214881042000001',
                       'channel_reconci_channel_name': 'cashfree_yomoyo3_ebank',
                       'channel_reconci_channel_order_no': 'RBIZ41214881042000001',
                       'channel_reconci_fees': 590,
                       'channel_reconci_merchant_no': 'yomoyo3',
                       'channel_reconci_order_created_at': '1000-01-01 00:00:00',
                       'channel_reconci_order_finished_at': '2020-06-11 00:33:07',
                       'channel_reconci_payment_mode': 'UPI',
                       'channel_reconci_product_type': '',
                       'channel_reconci_provider_code': 'cashfree',
                       'channel_reconci_remark': '',
                       'channel_reconci_service_charge': 500,
                       'channel_reconci_service_tax': 90,
                       'channel_reconci_settlement_amount': 150460,
                       'channel_reconci_settlement_id': '262907',
                       'channel_reconci_status': 2,
                       'channel_reconci_type': 'WITHHOLD',
                       'channel_reconci_user_name': ''},
                      {'channel_reconci_account': '',
                       'channel_reconci_amount': 205400,
                       'channel_reconci_bank_code': '',
                       'channel_reconci_bank_name': 'android_intent',
                       'channel_reconci_channel_key': 'RBIZ41214881042000002',
                       'channel_reconci_channel_name': 'cashfree_yomoyo3_ebank',
                       'channel_reconci_channel_order_no': 'RBIZ41214881042000002',
                       'channel_reconci_fees': 590,
                       'channel_reconci_merchant_no': 'yomoyo3',
                       'channel_reconci_order_created_at': '1000-01-01 00:00:00',
                       'channel_reconci_order_finished_at': '2020-06-11 00:36:44',
                       'channel_reconci_payment_mode': 'UPI',
                       'channel_reconci_product_type': '',
                       'channel_reconci_provider_code': 'cashfree',
                       'channel_reconci_remark': '',
                       'channel_reconci_service_charge': 500,
                       'channel_reconci_service_tax': 90,
                       'channel_reconci_settlement_amount': 204810,
                       'channel_reconci_settlement_id': '262907',
                       'channel_reconci_status': 2,
                       'channel_reconci_type': 'WITHHOLD',
                       'channel_reconci_user_name': ''}]
    Assert.assert_match_json(except_reconci, reconci_list, "test")
    settlement_list = get_channel_settlement(channel_settlement_settlement_id=262907)
    except_settlement = [{'channel_settlement_adjustment_amount': 0,
                          'channel_settlement_amount': 712900,
                          'channel_settlement_fees': 2360,
                          'channel_settlement_merchant_no': 'yomoyo3',
                          'channel_settlement_provider_code': 'cashfree',
                          'channel_settlement_service_charge': 2000,
                          'channel_settlement_service_tax': 360,
                          'channel_settlement_settled_amount': 710540,
                          'channel_settlement_settled_at': '2020-06-12 10:32:04',
                          'channel_settlement_settlement_amount': 710540,
                          'channel_settlement_settlement_id': '262907'}]
    Assert.assert_match_json(except_settlement, settlement_list, "test")


def assert_check_withdraw_withdrawreceipt_initinfo(trade_no, merchant_key, user_uuid, card_uuid, channel_name,
                                                   transfer_option=None, transfer_mode=None, withdraw_type="online"):
    # 断言：检查代扣成功后withdraw和withdraw_receipt表数据统一检查

    withdraw_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM withdraw LEFT JOIN withdraw_receipt ON withdraw_receipt_merchant_key=withdraw_merchant_key  " \
        "WHERE withdraw_receipt_trade_no='%s'  order by withdraw_created_at desc limit 1" % trade_no)[0]
    withdraw_receipt_info = \
        gc.PAYMENT_DB.do_sql("SELECT * FROM withdraw_receipt  WHERE withdraw_receipt_trade_no='%s'order by "
                             "withdraw_receipt_created_at desc limit 1" % trade_no)[0]
    assert withdraw_info["withdraw_merchant_name"] == "gbiz", '和传入一致,固定为gbiz'
    assert withdraw_info["withdraw_merchant_key"] == merchant_key, '和传入一致'
    assert withdraw_info["withdraw_amount"] == global_amount, '代付金额和传入一致'
    assert withdraw_info["withdraw_reason"] == "f-放款", '和传入一致,固定为:f-放款'
    assert withdraw_info["withdraw_callback"] == global_gbiz_callback, '和传入一致'
    assert withdraw_info["withdraw_user_uuid"] == user_uuid, '和传入一致'
    assert withdraw_receipt_info["withdraw_receipt_merchant_name"] == "gbiz", '和传入一致,固定为gbiz'
    assert withdraw_receipt_info["withdraw_receipt_merchant_key"] == merchant_key, '和传入一致'
    # TODO 每个国家card_num规则不一样怎么写
    # assert withdraw_receipt_info[0]["withdraw_receipt_card_num"] == card_num, '虚拟卡号对应无误'
    assert withdraw_receipt_info["withdraw_receipt_amount"] == global_amount, '代付金额和传入一致'
    assert withdraw_receipt_info["withdraw_receipt_channel_name"] == channel_name, '代付通道一致'
    # channel_key代码随机生成的，暂不检查
    # assert withdraw_receipt_info[0]["withdraw_receipt_channel_key"] != "" , 'withdraw_receipt_channel_key不为空'
    assert withdraw_receipt_info["withdraw_receipt_trade_no"] == trade_no, 'trade_no一致'
    assert withdraw_receipt_info["withdraw_receipt_amount"] == global_amount, '代付金额和传入一致'
    if transfer_option:
        assert withdraw_receipt_info["withdraw_receipt_transfer_option"] == transfer_option, '和传入一致'
    else:
        return
    if transfer_mode:
        assert withdraw_receipt_info["withdraw_receipt_transfer_mode"] == transfer_mode, '和传入一致'
    else:
        return
    assert withdraw_receipt_info["withdraw_receipt_user_uuid"] == user_uuid, 'user_uuid和传入一致'
    assert withdraw_receipt_info["withdraw_receipt_card_uuid"] == card_uuid, 'card_uuid和传入一致'
    assert withdraw_receipt_info["withdraw_receipt_type"] == withdraw_type, '没有传入就默认是线上放款'


def assert_withdrawandreceipt_process(trade_no, merchant_key, code="", message=""):
    # 代付处理中状态检查  +  处理中不生成sendmsg + gbiz代付结果查询
    withdraw_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM withdraw LEFT JOIN withdraw_receipt ON withdraw_receipt_merchant_key=withdraw_merchant_key  " \
        "WHERE withdraw_receipt_merchant_key='%s'  order by withdraw_id desc limit 1" % merchant_key)[0]
    withdraw_receipt_info = \
        gc.PAYMENT_DB.do_sql("SELECT * FROM withdraw_receipt  WHERE withdraw_receipt_merchant_key='%s'order by "
                             "withdraw_receipt_id desc limit 1" % merchant_key)[0]
    Assert.assert_equal(withdraw_info["withdraw_status"], 1, '代付处理中')
    Assert.assert_equal(withdraw_receipt_info["withdraw_receipt_status"], 1, '代付处理中')
    assert withdraw_receipt_info["withdraw_receipt_channel_resp_code"] == code, 'code正确'
    assert withdraw_receipt_info["withdraw_receipt_channel_resp_message"] == message, 'message正确'
    # gbiz调用放款查询接口查询
    req, resp = global_withdraw_query(merchant_key)
    # 断言
    assert resp['code'] == 2, "代付处理中"
    assert resp['data']['status'] == 1, "代付处理中内层status=1"


def assert_withdrawandreceipt_success(trade_no, merchant_key, code="", message="",
                                      resp_transfer_mode=gbpay_resp_transfer_mode):
    # 代付成功状态检查  +  sendmsg回调检查  + gbiz代付结果查询
    withdraw_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM withdraw LEFT JOIN withdraw_receipt ON withdraw_receipt_merchant_key=withdraw_merchant_key  " \
        "WHERE withdraw_receipt_merchant_key='%s'  order by withdraw_id desc limit 1" % merchant_key)[0]
    withdraw_receipt_info = \
        gc.PAYMENT_DB.do_sql("SELECT * FROM withdraw_receipt  WHERE withdraw_receipt_merchant_key='%s'order by "
                             "withdraw_receipt_id desc limit 1" % merchant_key)[0]
    assert withdraw_info["withdraw_status"] == 2, '代付成功'
    assert withdraw_receipt_info["withdraw_receipt_status"] == 2, '代付成功'
    assert withdraw_receipt_info["withdraw_receipt_channel_resp_code"] == code, 'code正确'
    assert withdraw_receipt_info["withdraw_receipt_channel_resp_message"] == message, 'message正确'
    assert withdraw_receipt_info["withdraw_receipt_resp_transfer_mode"] == resp_transfer_mode, 'mode 正确'
    sendmsg_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM sendmsg  WHERE sendmsg_order_no='%s'  order by sendmsg_create_at desc limit 1" % merchant_key)[0]
    Assert.assert_equal(sendmsg_info["sendmsg_order_no"], merchant_key, '放款完成生成了回调')
    Assert.assert_equal(sendmsg_info["sendmsg_type"], 'withdrawNotify', '放款完成生成了回调')
    #  json.loads()函数是将字符串转化为字典
    sendmsg_content_info = json.loads(sendmsg_info["sendmsg_content"])
    Assert.assert_equal(sendmsg_content_info["body"]["from_system"], "paysvr", 'paysvr 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["type"], "withdraw", 'withdraw 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_name"],
                        withdraw_receipt_info["withdraw_receipt_channel_name"], 'channel_name 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_code"], code, 'code一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_message"], message, 'message一致')
    country = get_sysconfig("--country")
    if country != 'mexico':
        Assert.assert_equal(sendmsg_content_info["body"]["data"]["finished_at"],
                            withdraw_receipt_info["withdraw_receipt_finished_at"], 'finished_at 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_key"],
                        withdraw_receipt_info["withdraw_receipt_channel_key"], 'channel_key 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["amount"], global_amount, 'amount 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["status"], 2, 'status一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["merchant_key"], merchant_key, 'merchant_key一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["trade_no"], trade_no, 'trade_no一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["baseUrl"], global_gbiz_callback, '回调地址和gbiz传入一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["method"], "POST", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["toSystem"], "gbiz", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["sendType"], "API", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["successCode"], "0", '一致')
    # gbiz调用放款查询接口查询
    req, resp = global_withdraw_query(merchant_key)
    # 断言
    assert resp['code'] == 0, "代付成功"
    assert resp['data']['status'] == 2, "代付成功内层status=2"
    assert resp['message'] == "交易成功", "交易成功"
    assert resp['data']['platform_code'] == "E20000", "交易成功错误码"


def assert_withdrawandreceipt_fail(trade_no, merchant_key, code="", message=""):
    # 代付失败状态检查  +  sendmsg回调检查  + gbiz代付结果查询
    withdraw_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM withdraw LEFT JOIN withdraw_receipt ON withdraw_receipt_merchant_key=withdraw_merchant_key  " \
        "WHERE withdraw_receipt_merchant_key='%s'  order by withdraw_id desc limit 1" % merchant_key)[0]
    withdraw_receipt_info = \
        gc.PAYMENT_DB.do_sql("SELECT * FROM withdraw_receipt  WHERE withdraw_receipt_merchant_key='%s'order by "
                             "withdraw_receipt_id desc limit 1" % merchant_key)[0]
    Assert.assert_equal(withdraw_info["withdraw_status"], 3, '代付失败')
    Assert.assert_equal(withdraw_receipt_info["withdraw_receipt_status"], 3, '代付失败')
    assert withdraw_receipt_info["withdraw_receipt_channel_resp_code"] == code, 'code正确'
    assert withdraw_receipt_info["withdraw_receipt_channel_resp_message"] == message, 'message正确'
    sendmsg_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM sendmsg  WHERE sendmsg_order_no='%s'  order by sendmsg_create_at desc limit 1" % merchant_key)[0]
    Assert.assert_equal(sendmsg_info["sendmsg_order_no"], merchant_key, '放款完成生成了回调')
    Assert.assert_equal(sendmsg_info["sendmsg_type"], 'withdrawNotify', '放款完成生成了回调')
    #  json.loads()函数是将字符串转化为字典
    sendmsg_content_info = json.loads(sendmsg_info["sendmsg_content"])
    Assert.assert_equal(sendmsg_content_info["body"]["from_system"], "paysvr", 'paysvr 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["type"], "withdraw", 'withdraw 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_name"],
                        withdraw_receipt_info["withdraw_receipt_channel_name"], 'channel_name 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_code"], code, 'code一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_message"], message, 'message一致')
    country = get_sysconfig("--country")
    if country != 'mexico':
        Assert.assert_equal(sendmsg_content_info["body"]["data"]["finished_at"],
                            withdraw_receipt_info["withdraw_receipt_finished_at"], 'finished_at 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_key"],
                        withdraw_receipt_info["withdraw_receipt_channel_key"], 'channel_key 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["amount"], global_amount, 'amount 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["status"], 3, 'status一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["merchant_key"], merchant_key, 'merchant_key一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["trade_no"], trade_no, 'trade_no一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["baseUrl"], global_gbiz_callback, '回调地址和gbiz传入一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["method"], "POST", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["toSystem"], "gbiz", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["sendType"], "API", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["successCode"], "0", '一致')
    # gbiz调用放款查询接口查询
    req, resp = global_withdraw_query(merchant_key)
    # 断言
    assert resp['code'] == 1, "交易失败"
    assert resp['data']['status'] == 3, "放款失败内层status=3"


def assert_check_withhold_withholdreceipt_initinfo(merchant_key, channel_name,
                                                   user_uuid, card_uuid="6300000000000000000",
                                                   card_num="enc_04_4106612382062092288_439",
                                                   channel_redirect="", operator="USER",
                                                   payment_option="", payment_mode=""
                                                   , description="", channel_key=""
                                                   , channel_inner_key=""):
    # 断言：检查代扣成功后withhold和withhold_receipt表数据统一检查
    withhold_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM withhold LEFT JOIN withhold_receipt ON withhold_receipt_merchant_key=withhold_merchant_key  " \
        "WHERE withhold_receipt_merchant_key='%s'  order by withhold_id desc limit 1" % merchant_key)[0]
    withhold_receipt_info = \
        gc.PAYMENT_DB.do_sql("SELECT * FROM withhold_receipt  WHERE withhold_receipt_merchant_key='%s'order by "
                             "withhold_receipt_id desc limit 1" % merchant_key)[0]
    assert withhold_info["withhold_merchant_name"] == "rbiz", '和传入一致,固定为rbiz'
    assert withhold_info["withhold_merchant_key"] == merchant_key, '和传入一致'
    assert withhold_info["withhold_card_uuid"] == card_uuid, '一致'
    assert withhold_info["withhold_card_num"] == card_num, '一致'
    assert withhold_info["withhold_status_stage"] == 0, '一致'
    assert withhold_info["withhold_amount"] == global_amount, '代扣金额和传入一致'
    assert withhold_info["withhold_callback"] == global_rbiz_callback, '和传入一致'
    assert withhold_info["withhold_remark"] == user_ip_withhold_remark, '和传入一致'
    assert withhold_info["withhold_capital"] == "", '和传入一致'
    assert withhold_info["withhold_operator"] == operator, '和传入一致'
    assert withhold_info["withhold_redirect"] == global_rbiz_redirect, '和传入一致'
    assert withhold_info["withhold_ruleset_code"] == None, '和传入一致'
    assert withhold_info["withhold_account_no"] == "", '和传入一致'
    assert withhold_info["withhold_user_uuid"] == user_uuid, '和传入一致'
    assert withhold_info["withhold_original_amount"] == global_amount, '和传入一致'

    assert withhold_receipt_info["withhold_receipt_merchant_name"] == "rbiz", '和传入一致,固定为rbiz'
    assert withhold_receipt_info["withhold_receipt_merchant_key"] == merchant_key, '和传入一致'
    assert withhold_receipt_info["withhold_receipt_channel_name"] == channel_name, '代扣通道一致'
    # channel_key代码随机生成的，暂不检查
    # assert withhold_receipt_info[0]["withhold_receipt_channel_key"] != "", 'withhold_receipt_channel_key不为空'
    if channel_key == "":
        return  # channel_key代码随机生成的，没传就不检查
    else:
        assert withhold_receipt_info["withhold_receipt_channel_key"] == channel_key, 'channel_key正确'
    if channel_inner_key == "":
        return  # payloro发起代扣无法mock，channel_inner_key无法检查，没传就不检
    else:
        assert withhold_receipt_info["withhold_receipt_channel_inner_key"] == channel_inner_key, 'channel_inner_key正确'
    assert withhold_receipt_info["withhold_receipt_card_num"] == card_num, '虚拟卡号对应无误'
    assert withhold_receipt_info["withhold_receipt_amount"] == global_amount, '一致'
    assert withhold_receipt_info["withhold_receipt_status_stage"] == 0, '一致'
    assert withhold_receipt_info["withhold_receipt_redirect"] == channel_redirect, '一致'
    assert withhold_receipt_info["withhold_receipt_ruleset_code"] == "", '一致'
    assert withhold_receipt_info["withhold_receipt_payment_option"] == payment_option, '和传入一致'
    assert withhold_receipt_info["withhold_receipt_payment_mode"] == payment_mode, '和传入一致'
    # xendit会将通道返回的付款码保存到description中
    assert withhold_receipt_info["withhold_receipt_description"] == description, '和传入一致'


def assert_withholdandreceipt_process(merchant_key, code="", message=""):
    # 代扣处理中状态检查  +  处理中不生成sendmsg + rbiz代扣结果查询
    withhold_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM withhold LEFT JOIN withhold_receipt ON withhold_receipt_merchant_key=withhold_merchant_key  " \
        "WHERE withhold_receipt_merchant_key='%s'  order by withhold_id desc limit 1" % merchant_key)[0]
    withhold_receipt_info = \
        gc.PAYMENT_DB.do_sql("SELECT * FROM withhold_receipt  WHERE withhold_receipt_merchant_key='%s'order by "
                             "withhold_receipt_id desc limit 1" % merchant_key)[0]
    Assert.assert_equal(withhold_info["withhold_status"], 1, '代扣处理中')
    Assert.assert_equal(withhold_receipt_info["withhold_receipt_status"], 1, '代扣处理中')
    assert withhold_receipt_info["withhold_receipt_channel_resp_code"] == code, 'channel_resp_codecode正确'
    assert withhold_receipt_info["withhold_receipt_channel_resp_message"] == message, 'message正确'
    # rbiz调用放款查询接口查询
    req, resp = global_withhold_query(merchant_key)
    # 断言
    assert resp['code'] == 2, "代扣处理中"
    assert resp['data']['status'] == 1, "代扣处理中内层status=1"


def assert_withholdandreceipt_success(merchant_key, code="", message="", option=None, mode="", platform_code="E20000"):
    # 代扣成功状态检查  +  sendmsg回调检查  + rbiz代扣结果查询
    withhold_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM withhold LEFT JOIN withhold_receipt ON withhold_receipt_merchant_key=withhold_merchant_key  " \
        "WHERE withhold_receipt_merchant_key='%s'  order by withhold_id desc limit 1" % merchant_key)[0]
    withhold_receipt_info = \
        gc.PAYMENT_DB.do_sql("SELECT * FROM withhold_receipt  WHERE withhold_receipt_merchant_key='%s'order by "
                             "withhold_receipt_id desc limit 1" % merchant_key)[0]
    assert withhold_info["withhold_status"] == 2, '代扣成功'
    assert withhold_receipt_info["withhold_receipt_status"] == 2, '代扣成功'
    assert withhold_receipt_info["withhold_receipt_channel_resp_code"] == code, 'code正确'
    assert withhold_receipt_info["withhold_receipt_channel_resp_message"] == message, 'message正确'
    assert withhold_receipt_info["withhold_receipt_resp_payment_option"] == option, 'option正确'
    assert withhold_receipt_info["withhold_receipt_resp_payment_mode"] == mode, 'mode正确'
    sendmsg_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM sendmsg  WHERE sendmsg_order_no='%s'  order by sendmsg_create_at desc limit 1" % merchant_key)[0]
    Assert.assert_equal(sendmsg_info["sendmsg_order_no"], merchant_key, '代扣完成生成了回调')
    Assert.assert_equal(sendmsg_info["sendmsg_type"], 'withholdNotify', '代扣完成生成了回调')
    #  json.loads()函数是将字符串转化为字典
    sendmsg_content_info = json.loads(sendmsg_info["sendmsg_content"])
    Assert.assert_equal(sendmsg_content_info["body"]["from_system"], "paysvr", 'paysvr 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["type"], "withhold", 'withhold 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_name"],
                        withhold_receipt_info["withhold_receipt_channel_name"], 'channel_name 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_code"], code, 'code一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_message"], message, 'message一致')
    # TODO xendit的回调时间会差1s，先不检查
    # Assert.assert_equal(sendmsg_content_info["body"]["data"]["finished_at"], withhold_receipt_info["withhold_receipt_finished_at"], 'finished_at一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["merchant_key"], merchant_key, 'merchant_key一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_key"],
                        withhold_receipt_info["withhold_receipt_channel_key"], 'channel_key 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["amount"], global_amount, 'amount 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["card_uuid"], withhold_info["withhold_card_uuid"],
                        'card_uuid 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["status"], 2, 'status一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["payment_mode"],
                        withhold_receipt_info["withhold_receipt_payment_mode"], 'mode一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["baseUrl"], global_rbiz_callback, '回调地址和rbiz传入一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["method"], "POST", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["toSystem"], "rbiz", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["sendType"], "API", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["successCode"], "0", '一致')
    # rbiz调用放款查询接口查询
    req, resp = global_withhold_query(merchant_key)
    # 断言
    assert resp['code'] == 0, "代扣成功"
    assert resp['data']['status'] == 2, "代扣成功内层status=2"
    assert resp['message'] == "交易成功", "交易成功"
    assert resp['data']['platform_code'] == platform_code, "交易成功错误码"


def assert_withholdandreceipt_fail(merchant_key, code="", message="", amount=""):
    # 代扣失败状态检查  +  sendmsg回调检查  + rbiz代扣结果查询
    withhold_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM withhold LEFT JOIN withhold_receipt ON withhold_receipt_merchant_key=withhold_merchant_key  " \
        "WHERE withhold_receipt_merchant_key='%s'  order by withhold_id desc limit 1" % merchant_key)[0]
    withhold_receipt_info = \
        gc.PAYMENT_DB.do_sql("SELECT * FROM withhold_receipt  WHERE withhold_receipt_merchant_key='%s'order by "
                             "withhold_receipt_id desc limit 1" % merchant_key)[0]
    Assert.assert_equal(withhold_info["withhold_status"], 3, '代扣失败')
    Assert.assert_equal(withhold_receipt_info["withhold_receipt_status"], 3, '代扣失败')
    assert withhold_receipt_info["withhold_receipt_channel_resp_code"] == code, 'code正确'
    assert withhold_receipt_info["withhold_receipt_channel_resp_message"] == message, 'message正确'
    sendmsg_info = gc.PAYMENT_DB.do_sql(
        "SELECT * FROM sendmsg  WHERE sendmsg_order_no='%s'  order by sendmsg_create_at desc limit 1" % merchant_key)[0]
    Assert.assert_equal(sendmsg_info["sendmsg_order_no"], merchant_key, '代扣完成生成了回调')
    Assert.assert_equal(sendmsg_info["sendmsg_type"], 'withholdNotify', '代扣完成生成了回调')
    #  json.loads()函数是将字符串转化为字典
    sendmsg_content_info = json.loads(sendmsg_info["sendmsg_content"])
    Assert.assert_equal(sendmsg_content_info["body"]["from_system"], "paysvr", 'paysvr 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["type"], "withhold", 'withhold 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_name"],
                        withhold_receipt_info["withhold_receipt_channel_name"], 'channel_name 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_code"], code, 'code一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_message"], message, 'message一致')
    # TODO xendit的回调时间会差1s，先不检查
    # Assert.assert_equal(sendmsg_content_info["body"]["data"]["finished_at"], withhold_receipt_info["withhold_receipt_finished_at"], 'finished_at一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["merchant_key"], merchant_key, 'merchant_key一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["channel_key"],
                        withhold_receipt_info["withhold_receipt_channel_key"], 'channel_key 一致')
    if amount == "":
        return  # 传空则不检查
    else:
        Assert.assert_equal(sendmsg_content_info["body"]["data"]["amount"], global_amount, 'amount 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["card_uuid"], withhold_info["withhold_card_uuid"],
                        'card_uuid 一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["status"], 3, 'status一致')
    Assert.assert_equal(sendmsg_content_info["body"]["data"]["payment_mode"],
                        withhold_receipt_info["withhold_receipt_payment_mode"], 'mode一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["baseUrl"], global_rbiz_callback, '回调地址和rbiz传入一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["method"], "POST", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["toSystem"], "rbiz", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["sendType"], "API", '一致')
    Assert.assert_equal(sendmsg_content_info["externalApi"]["successCode"], "0", '一致')
    # rbiz调用放款查询接口查询
    req, resp = global_withhold_query(merchant_key)
    # 断言
    assert resp['code'] == 1, "交易失败"
    assert resp['data']['status'] == 3, "放款失败内层status=3"


def check_data(data, **kwargs):
    for key, value in kwargs.items():
        Assert.assert_equal(value, data[key], "%s数据有误" % key)


def check_withdraw_data(merchant_key, withdraw_status, withdraw_receipt_status, withdraw_receipt_resp_code="", withdraw_receipt_resp_message=""):
    """
    检查代付数据
    """
    withdraw = get_withdraw_by_merchant_key(merchant_key)
    withdraw_receipt = get_withdraw_receipt_by_merchant_key(merchant_key)
    Assert.assert_equal(withdraw_status, withdraw[0]["withdraw_status"])
    Assert.assert_equal(withdraw_receipt_status, withdraw_receipt[-1]["withdraw_receipt_status"])
    if withdraw_receipt_resp_code != "":
        Assert.assert_equal(withdraw_receipt_resp_code, withdraw_receipt[-1]["withdraw_receipt_channel_resp_code"])
    if withdraw_receipt_resp_message != "":
        Assert.assert_equal(withdraw_receipt_resp_message, withdraw_receipt[-1]["withdraw_receipt_channel_resp_message"])


def check_withhold_data(merchant_key, withhold_status, withhold_receipt_status, withhold_receipt_resp_code="", withhold_receipt_resp_message=""):
    """
    检查代扣数据
    """
    withhold = get_withhold_by_merchant_key(merchant_key)
    withhold_receipt = get_withhold_receipt_by_merchant_key(merchant_key)
    Assert.assert_equal(withhold_status, withhold[0]["withhold_status"])
    Assert.assert_equal(withhold_receipt_status, withhold_receipt[-1]["withhold_receipt_status"])
    if withhold_receipt_resp_code != "":
        Assert.assert_equal(withhold_receipt_resp_code, withhold_receipt[-1]["withhold_receipt_channel_resp_code"])
    if withhold_receipt_resp_message != "":
        Assert.assert_equal(withhold_receipt_resp_message, withhold_receipt[-1]["withhold_receipt_channel_resp_message"])


def check_binding_data(card_uuid, merchant_key, binding_status, binding_request_status, binding_merchant_request_status, binding_request_channel_code="", binding_request_channel_message=""):
    """
    检查绑卡数据
    """
    binding = get_binding_by_card_uuid(card_uuid)
    binding_request = get_binding_request_by_merchant_key(merchant_key)
    binding_merchant_request = get_binding_merchant_request_by_merchant_key(merchant_key)
    Assert.assert_equal(binding_status, binding[0]["binding_status"])
    Assert.assert_equal(binding_request_status, binding_request[0]["binding_request_status"])
    Assert.assert_equal(binding_merchant_request_status, binding_merchant_request[0]["binding_merchant_request_status"])
    if binding_request_channel_code != "":
        Assert.assert_equal(binding_request_channel_code, binding_request[0]["binding_request_channel_code"])
    if binding_request_channel_message != "":
        Assert.assert_equal(binding_request_channel_message, binding_request[0]["binding_request_channel_message"])


def check_fusing_data(channel_name, fusing_level, fusint_status):
    """
    检查熔断数据
    """
    fusing = get_fusing_latest(channel_name)
    fusing_log = get_fusing_log_by_trace_no(fusing["fusing_trace_no"])
    Assert.assert_equal(fusing_level, fusing["fusing_level"])
    Assert.assert_equal(fusint_status, fusing["fusing_status"])
    return fusing["fusing_trace_no"]
