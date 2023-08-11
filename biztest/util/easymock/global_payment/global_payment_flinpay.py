# -*- coding: utf-8 -*-
import time
from datetime import datetime

from biztest.config.payment.url_config import global_razorpay_collect_inner_no, global_razorpay_collect_channel_key1, \
    global_razorpay_collect_paid_amount, global_razorpay_collect_payment_mode_other, \
    global_razorpay_collect_payment_mode_upi, global_razorpay_collect_cardnum, global_razorpay_collect_mobile, \
    global_razorpay_collect_ifsc, global_razorpay_collect_name, global_razorpay_collect_channel_key2, \
    global_razorpay_ebank_channel_key, global_razorpay_ebank_payment_mode, \
    global_razorpay_ebank_fail_message, global_razorpay_verifyid, global_withdraw_failed_message, \
    global_razorpay_withdraw_balance, global_razorpay_withdraw_fail_rejected, global_razorpay_withdraw_fail_cancelled, \
    global_razorpay_withdraw_fail_reversed, global_razorpay_withdraw_mode, global_razorpay_withdraw_inner_key, \
    global_razorpay_withdraw_success_processed, global_razorpay_withdraw_process_processing, \
    global_razorpay_withdraw_process_queued, global_razorpay_withdraw_process_pending, \
    global_razorpay_withdraw_contact_id, global_razorpay_withdraw_fund_account_id
from biztest.interface.payment.payment_interface import get_timestamp
from biztest.util.easymock.easymock import Easymock


class FlinpayMock(Easymock):

    def update_flinpay_paycode_success(self):
        api = "/v1/contacts"  # razorpay创建联系人失败，即绑卡失败
        mode = {
            "id": "cont_@word(15)",
            "entity": "contact",
            "name": "@first @middle @last",
            "contact": "",
            "email": "wangxiaoming@google.com",
            "type": "customer",
            "reference_id": "",
            "batch_id": None,
            "active": "false",  # true 创建成功，false 创建失败
            "notes": {
                "product": "contact"
            },
            "created_at": "1583303041"
        }
        self.update(api, mode)


if __name__ == "__main__":
    pass
