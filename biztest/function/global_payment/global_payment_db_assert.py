# from biztest.config.payment.url_config import global_rbiz_callback, global_rbiz_redirect, global_amount, \
#     global_rbiz_merchant_name, global_sign_company_yomoyo, \
#     global_gbiz_callback, global_gbiz_merchant_name, \
#     global_razorpay_collect_paid_amount, global_razorpay_collect_channel_key1, \
#     global_razorpay_collect_cardnum_encrypt, global_razorpay_collect_payment_mode_upi, \
#     global_razorpay_collect_name_encrypt, global_razorpay_collect_mobile_encrypt, \
#     global_razorpay_collect_ifsc, global_razorpay_collect_payment_mode_other, global_razorpay_in_account_no, \
#     cashfree_ebank_settlement_id, global_ebank_payurl, global_cashfree_sdk_token, global_cashfree_sdk_appid, \
#     channel_notify_base_url, global_cashfree_sdk_channel_name, sdk_payment_option, global_razorpay_verifyid, \
#     global_cashfree_verifyid, global_paytm_in_account_no
# from biztest.function.global_payment.global_payment_db_operation import get_global_sendmsg_info_by_merchant_key, json, \
#     get_global_withhold_channel_request_log_by_channel_key, \
#     get_global_card_info_by_card_account, get_global_account_info_by_card_num, get_global_binding_info_by_card_num, \
#     get_global_binding_request_info_by_card_num, update_global_task_next_run_at, get_global_withdraw_info_by_trade_no, \
#     get_global_withdraw_receipt_info_by_trade_no, get_global_withdraw_channel_request_log_by_channel_key, \
#     get_task_order_no_by_card_num, get_withhold_by_merchant_key, \
#     get_withhold_receipt_by_merchant_key, get_global_withholdaccountinfo_by_accountno, \
#     get_razorpay_accountregister_channelrequestlog_by_customerid, get_razorpay_customerregister_channelrequestlog, \
#     update_task_order_no, get_channel_reconci_by_settlement_id, get_channel_settlement_by_settlement_id
# from biztest.interface.payment.payment_interface import global_withhold_query, \
#     global_bindResult, run_task_by_task_order_no, global_withdraw_query, global_autoWithdraw, \
#     global_withhold_autoSubscribe, global_subscribeResult, global_transfer_query
# from biztest.util.asserts.assert_util import Assert
# import time
#
#
# def assert_accountverify_check_cardandaccount_auth_mode(global_db, bank_account_encrypt):
#     # 绑卡模式：account=银行账户 card=银行卡  upi=统一支付接口
#     card_info = get_global_card_info_by_card_account(global_db, bank_account_encrypt)
#     account_info = get_global_account_info_by_card_num(global_db, card_info[0]["card_num"])
#     assert card_info[0]["card_auth_mode"] == "account"  # 前提是必须用这个绑卡"bank_account_encrypt"
#     assert account_info[0]["account_auth_mode"] == "account"  # 前提是必须用这个绑卡"bank_account_encrypt"
#
#
# def assert_upiverify_check_cardandaccount_auth_mode(global_db, bank_account_encrypt):
#     # 绑卡模式：account=银行账户 card=银行卡  upi=统一支付接口
#     card_info = get_global_card_info_by_card_account(global_db, bank_account_encrypt)
#     account_info = get_global_account_info_by_card_num(global_db, card_info[0]["card_num"])
#     assert card_info[0]["card_auth_mode"] == "upi"  # 前提是必须用这个绑卡"upi_encrypt"
#     assert account_info[0]["account_auth_mode"] == "upi"  # 前提是必须用这个绑卡"upi_encrypt"
#
#
# def assert_cardSubscribe_check_cardandaccount_auth_mode(global_db, bank_account_encrypt):
#     # 绑卡模式：account=银行账户 card=银行卡  upi=统一支付接口
#     card_info = get_global_card_info_by_card_account(global_db, bank_account_encrypt)
#     account_info = get_global_account_info_by_card_num(global_db, card_info[0]["card_num"])
#     assert card_info[0]["card_auth_mode"] == "card"  # 前提是必须用这个绑卡"card_num_encrypt"
#     assert account_info[0]["account_auth_mode"] == "card"  # 前提是必须用这个绑卡"card_num_encrypt"
#
#
# def assert_verify_check_card_account_binding_bindingrequest(global_db, bank_account_encrypt, resp_autobind,
#                                                             user_name_encrypt, mobile_encrypt, ifsc,
#                                                             email_encrypt, address_encrypt):
#     # 绑卡完成后检验card、account、binding、binding_reuqest四张表的字段保存是否正确，字段统一检查
#     params_card_account = bank_account_encrypt  # 卡号是存到card.card_account字段的
#     card_info = get_global_card_info_by_card_account(global_db, params_card_account)
#     params_card_num = card_info[0]["card_num"]  # 找到系统生成的虚拟卡号，其他表都用这个关联
#     account_info = get_global_account_info_by_card_num(global_db, params_card_num)
#     binding_info = get_global_binding_info_by_card_num(global_db, params_card_num)
#     binding_request_info = get_global_binding_request_info_by_card_num(global_db, params_card_num)
#     assert card_info[0]["card_account"] == bank_account_encrypt  # 真实卡号
#     assert card_info[0]["card_username"] == user_name_encrypt
#     assert card_info[0]["card_mobile"] == mobile_encrypt
#     assert card_info[0]["card_bank_code"] == ifsc
#     assert card_info[0]["card_email"] == email_encrypt
#     assert card_info[0]["card_address"] == address_encrypt
#     assert account_info[0]["account_card_uuid"] == account_info[0]["account_card_uuid"]
#     assert account_info[0]["account_card_num"] == params_card_num
#     assert binding_info[0]["binding_card_num"] == params_card_num
#     assert binding_info[0]["binding_channel_name"] == resp_autobind["content"]["data"]["channel_name"], "绑卡通道"
#     assert binding_request_info[0]["binding_request_channel"] == resp_autobind["content"]["data"][
#         "channel_name"], "绑卡通道"
#     assert binding_request_info[0]["binding_request_name"] == user_name_encrypt
#     assert binding_request_info[0]["binding_request_mobile"] == mobile_encrypt
#     assert binding_request_info[0]["binding_request_card_num"] == params_card_num
#
#
# def assert_verify_success(global_db, bank_account_encrypt):
#     params_card_account = bank_account_encrypt  # 卡号是存到card.card_account字段的
#     card_info = get_global_card_info_by_card_account(global_db, params_card_account)
#     params_card_num = card_info[0]["card_num"]  # 找到系统生成的虚拟卡号，其他表都用这个关联
#     binding_info = get_global_binding_info_by_card_num(global_db, params_card_num)
#     binding_request_info = get_global_binding_request_info_by_card_num(global_db, params_card_num)
#     assert binding_request_info[0]["binding_request_status"] == 0, "绑卡请求成功"
#     assert binding_info[0]["binding_status"] == 1, "绑卡成功"
#     assert card_info[0]["card_status"] == 1, "绑卡成功"
#     if binding_request_info[0]["binding_request_channel"] == "razorpay_yomoyo_verify":
#         assert binding_request_info[0]["binding_request_channel_inner_key"] == global_razorpay_verifyid, "绑卡id，成本对账需要"
#     elif binding_request_info[0]["binding_request_channel"] == "cashfree_yomoyo1_verify" and card_info[0]["card_auth_mode"] == "account":
#         assert binding_request_info[0]["binding_request_channel_inner_key"] == global_cashfree_verifyid, "绑卡id，成本对账需要"
#     elif binding_request_info[0]["binding_request_channel"] == "cashfree_yomoyo1_verify" and card_info[0]["card_auth_mode"] == "upi":
#         assert binding_request_info[0]["binding_request_channel_inner_key"] == "", "upi无id"
#     else:
#         pass
#
#
# def assert_verify_fail(global_db, bank_account_encrypt):
#     params_card_account = bank_account_encrypt  # 卡号是存到card.card_account字段的
#     card_info = get_global_card_info_by_card_account(global_db, params_card_account)
#     params_card_num = card_info[0]["card_num"]  # 找到系统生成的虚拟卡号，其他表都用这个关联
#     binding_info = get_global_binding_info_by_card_num(global_db, params_card_num)
#     binding_request_info = get_global_binding_request_info_by_card_num(global_db, params_card_num)
#     assert binding_request_info[0]["binding_request_status"] == 1, "绑卡失败"
#     assert binding_info[0]["binding_status"] == 2, "绑卡失败"
#     assert card_info[0]["card_status"] == 0, "绑卡失败"
#
#
# def assert_verify_process(global_db, bank_account_encrypt):
#     params_card_account = bank_account_encrypt  # 卡号是存到card.card_account字段的
#     card_info = get_global_card_info_by_card_account(global_db, params_card_account)
#     params_card_num = card_info[0]["card_num"]  # 找到系统生成的虚拟卡号，其他表都用这个关联
#     binding_info = get_global_binding_info_by_card_num(global_db, params_card_num)
#     binding_request_info = get_global_binding_request_info_by_card_num(global_db, params_card_num)
#     assert binding_request_info[0]["binding_request_status"] == 2, "绑卡处理中"
#     assert binding_info[0]["binding_status"] == 0, "绑卡处理中"
#     assert card_info[0]["card_status"] == 0, "绑卡未成功"
#
#
# def autobind_result_success_query(merchant_key):
#     # 组装绑卡结果查询参数
#     params_bindResult = {
#         "merchant_key": merchant_key
#     }
#     # dsq发起绑卡结果查询
#     resp_bindResult = global_bindResult(**params_bindResult)
#     # 断言
#     assert resp_bindResult["content"]["code"] == 0, "查询到绑卡结果成功"
#     assert resp_bindResult["content"]["data"][0]["status"] == 1, "binding表状态为绑卡成功"
#
#
# def autobind_result_fail_query(merchant_key):
#     # 组装绑卡结果查询参数
#     params_bindResult = {
#         "merchant_key": merchant_key
#     }
#     # dsq发起绑卡结果查询
#     resp_bindResult = global_bindResult(**params_bindResult)
#     # 断言
#     assert resp_bindResult["content"]["code"] == 1, "查询到绑卡结果失败"
#     assert resp_bindResult["content"]["data"][0]["status"] == 2, "binding表状态为绑卡失败"
#
#
# def autobind_result_process_query(merchant_key):
#     # 组装绑卡结果查询参数
#     params_bindResult = {
#         "merchant_key": merchant_key
#     }
#     # dsq发起绑卡结果查询
#     resp_bindResult = global_bindResult(**params_bindResult)
#     # 断言
#     assert resp_bindResult["content"]["code"] == 2, "查询到绑卡处理中"
#     assert resp_bindResult["content"]["data"][0]["status"] == 0, "binding表状态为绑卡中"
#
#
# def autoSubscribe_result_fail_query(merchant_key):
#     # 组装订阅结果查询参数
#     params_subscribeResult = {
#         "merchant_name": "dsq",
#         "merchant_key": merchant_key
#     }
#     # dsq发起绑卡结果查询
#     resp_subscribeResult = global_subscribeResult(**params_subscribeResult)
#     # 断言
#     assert resp_subscribeResult["content"]["code"] == 1, "查询到绑卡结果失败"
#     assert resp_subscribeResult["content"]["data"][0]["status"] == 2, "binding表状态为绑卡失败"
#
#
# def autoSubscribe_result_success_query(merchant_key):
#     # 组装订阅结果查询参数
#     params_subscribeResult = {
#         "merchant_name": "dsq",
#         "merchant_key": merchant_key
#     }
#     # dsq发起绑卡结果查询
#     resp_subscribeResult = global_subscribeResult(**params_subscribeResult)
#     # 断言
#     assert resp_subscribeResult["content"]["code"] == 0, "查询到绑卡结果成功"
#     assert resp_subscribeResult["content"]["data"][0]["status"] == 1, "binding表状态为绑卡成功"
#
#
# def autoSubscribe_result_process_query(merchant_key):
#     # 组装绑卡结果查询参数
#     params_subscribeResult = {
#         "merchant_key": merchant_key
#     }
#     # dsq发起绑卡结果查询
#     resp_subscribeResult = global_subscribeResult(**params_subscribeResult)
#     # 断言
#     assert resp_subscribeResult["content"]["code"] == 2, "查询到绑卡处理中"
#     assert resp_subscribeResult["content"]["data"][0]["status"] == 0, "binding表状态为绑卡中"
#
#
# def assert_check_withhold_withholdreceipt(global_db, card_uuid, merchant_key, card_num,
#                                           resp_withhold_autopay):
#     # 断言：检查代扣成功后withhold和withhold_receipt以及channel_request_log表的数据
#     withhold_info = get_withhold_by_merchant_key(global_db, merchant_key)
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#     assert withhold_info[0]["withhold_merchant_key"] == merchant_key, "代扣"
#     assert withhold_info[0]["withhold_card_uuid"] == card_uuid, "代扣"
#     assert withhold_info[0]["withhold_card_num"] == card_num, "代扣"
#     assert withhold_info[0]["withhold_callback"] == global_rbiz_callback, "代扣"
#     assert withhold_info[0]["withhold_redirect"] == global_rbiz_redirect, "代扣"
#     assert withhold_info[0]["withhold_amount"] == global_amount, "代扣"
#     assert withhold_receipt_info[0]["withhold_receipt_merchant_name"] == global_rbiz_merchant_name, "代扣"
#     assert withhold_receipt_info[0]["withhold_receipt_merchant_key"] == merchant_key, "代扣"
#     assert withhold_receipt_info[0]["withhold_receipt_channel_name"] == resp_withhold_autopay['content']['data'][
#         'channel_name'], "代扣"
#     assert withhold_receipt_info[0]["withhold_receipt_card_num"] == card_num, "代扣"
#     assert withhold_receipt_info[0]["withhold_receipt_amount"] == global_amount, "代扣"
#
#
# def assert_withhold_success(global_db, merchant_key, channel_key, channel_name, card_uuid, amount):
#     # 代扣成功状态检查  +  sendmsg回调检查  + rbiz代扣结果查询
#     withhold_info = get_withhold_by_merchant_key(global_db, merchant_key)
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#     assert withhold_info[0]["withhold_status"] == 2, "代扣成功"
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_status"], 2, '代扣成功')
#     # Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_message"],global_withhold_successed_msg, '代扣成功') # 代扣成功的不需要校验message，每个通道不一样
#     sendmsg_order_no = merchant_key
#     sendmsg_info = get_global_sendmsg_info_by_merchant_key(global_db, sendmsg_order_no)
#     #  json.loads()函数是将字符串转化为字典
#     sendmsg_content_info = json.loads(sendmsg_info[0]["sendmsg_content"])
#     assert sendmsg_info[0]["sendmsg_order_no"] == sendmsg_order_no, '还款完成生成了代扣回调'
#     assert sendmsg_content_info["body"]["callbackUrl"] == global_rbiz_callback, '回调地址和rbiz给的配置一致'
#     assert sendmsg_content_info["body"]["notifyDto"]["channel_name"] == channel_name, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["merchant_key"] == merchant_key, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["channel_key"] == channel_key, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["account_no"] == "", '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["card_uuid"] == card_uuid, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["amount"] == amount, '线下还款金额'
#     assert sendmsg_content_info["body"]["notifyDto"]["status"] == 2, '代扣成功状态为2'
#
#     # rbiz调用代扣查询接口查询，组装代扣查询参数
#     params_withhold_query = {
#         "merchant_key": merchant_key
#     }
#     # rbiz发起代扣结果查询
#     resp_withhold_query = global_withhold_query(**params_withhold_query)
#     # 断言
#     assert resp_withhold_query['content']['code'] == 0, "代扣成功"
#     assert resp_withhold_query['content']['data']['status'] == 2, "代扣成功内层status=2"
#
#
# def assert_withhold_fail(global_db, merchant_key, channel_key, channel_name, card_uuid, amount):
#     # 代扣失败状态检查  +  sendmsg回调检查  + rbiz代扣结果查询
#     withhold_info = get_withhold_by_merchant_key(global_db, merchant_key)
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#     Assert.assert_equal(withhold_info[0]["withhold_status"], 3, "代扣失败")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_status"], 3, '代扣失败')
#     sendmsg_order_no = merchant_key
#     sendmsg_info = get_global_sendmsg_info_by_merchant_key(global_db, sendmsg_order_no)
#     #  json.loads()函数是将字符串转化为字典
#     sendmsg_content_info = json.loads(sendmsg_info[0]["sendmsg_content"])
#     Assert.assert_equal(sendmsg_info[0]["sendmsg_order_no"], sendmsg_order_no, '代扣完成生成了代扣回调')
#     Assert.assert_equal(sendmsg_content_info["body"]["callbackUrl"], global_rbiz_callback, '回调地址和rbiz传入一致')
#     assert sendmsg_content_info["body"]["notifyDto"]["channel_name"] == channel_name, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["merchant_key"] == merchant_key, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["channel_key"] == channel_key, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["account_no"] == "", '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["card_uuid"] == card_uuid, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["amount"] == amount, '线下还款金额'
#     assert sendmsg_content_info["body"]["notifyDto"]["status"] == 3, '代扣失败状态为3'
#
#     # rbiz调用代扣查询接口查询，组装代扣查询参数
#     params_withhold_query = {
#         "merchant_key": merchant_key
#     }
#     # rbiz发起代扣结果查询
#     resp_withhold_query = global_withhold_query(**params_withhold_query)
#     # 断言
#     assert resp_withhold_query['content']['code'] == 1, "代扣失败"
#     assert resp_withhold_query['content']['data']['status'] == 3, "代扣失败内层status=3"
#
#
# def assert_withhold_process(global_db, merchant_key):
#     # 代扣处理中状态检查，处理中不会生成sendmsg  + rbiz代扣结果查询
#     withhold_info = get_withhold_by_merchant_key(global_db, merchant_key)
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#     Assert.assert_equal(withhold_info[0]["withhold_status"], 1, "代扣处理中")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_status"], 1, '代扣处理中')
#
#     # rbiz调用代扣查询接口查询，组装代扣查询参数
#     params_withhold_query = {
#         "merchant_key": merchant_key
#     }
#     # rbiz发起代扣结果查询
#     resp_withhold_query = global_withhold_query(**params_withhold_query)
#     # 断言
#     assert resp_withhold_query['content']['code'] == 2, "代扣处理中"
#     assert resp_withhold_query['content']['data']['status'] == 1, "代扣处理中内层status=1"
#
#
# def assert_check_razorpay_channelrequestlog(global_db, merchant_key):
#     # 断言：检查channel_request_log表的数据，主要看金额，razorpay通道金额字段是amount单位是派士
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#
#     # 检查传给razorpay的金额单位是派士
#     channel_request_log_info = get_global_withhold_channel_request_log_by_channel_key(global_db,
#                                                                                       withhold_receipt_info[0][
#                                                                                           "withhold_receipt_channel_key"])
#     #  json.loads()函数是将字符串转化为字典
#     channel_request_log_request = json.loads(channel_request_log_info[0]["channel_request_log_request"])
#     Assert.assert_equal(int(channel_request_log_request["amount"]), int(global_amount),
#                         'razorpay单位是派士')
#
#
# def assert_check_cashfree_channelrequestlog(global_db, merchant_key):
#     # 断言：检查channel_request_log表的数据，主要看金额，rcashfree通道金额字段是orderAmount单位是卢比
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#
#     # 检查传给razorpay的金额单位是派士
#     channel_request_log_info = get_global_withhold_channel_request_log_by_channel_key(global_db,
#                                                                                       withhold_receipt_info[0][
#                                                                                           "withhold_receipt_channel_key"])
#     #  json.loads()函数是将字符串转化为字典
#     channel_request_log_request = json.loads(channel_request_log_info[0]["channel_request_log_request"])
#     Assert.assert_equal(int(channel_request_log_request["orderAmount"]), int(global_amount / 100), 'cashfree单位是卢比')
#
#
# def assert_check_flinpay_channelrequestlog(global_db, merchant_key):
#     # 断言：检查channel_request_log表的数据，主要看金额，rcashfree通道金额字段是orderAmount单位是卢比
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#
#     # 检查传给razorpay的金额单位是派士
#     channel_request_log_info = get_global_withhold_channel_request_log_by_channel_key(global_db,
#                                                                                       withhold_receipt_info[0][
#                                                                                           "withhold_receipt_channel_key"])
#     #  json.loads()函数是将字符串转化为字典
#     channel_request_log_request = json.loads(channel_request_log_info[0]["channel_request_log_request"])
#     Assert.assert_equal(int(channel_request_log_request["payMoney"]), int(global_amount), 'Flinpay单位是印尼盾')
#
#
# def assert_check_cashfree_subscribe_channelrequestlog(global_db, merchant_key):
#     # cashfree订阅代扣(自动代扣)，断言：检查channel_request_log表的数据，主要看金额，rcashfree通道金额字段是amount单位是卢比
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#
#     # 检查传给razorpay的金额单位是派士
#     channel_request_log_info = get_global_withhold_channel_request_log_by_channel_key(global_db,
#                                                                                       withhold_receipt_info[0][
#                                                                                           "withhold_receipt_channel_key"])
#     #  json.loads()函数是将字符串转化为字典
#     channel_request_log_request = json.loads(channel_request_log_info[0]["channel_request_log_request"])
#     Assert.assert_equal(int(channel_request_log_request["amount"]), int(global_amount / 100), 'cashfree单位是卢比')
#
#
# def assert_check_withdraw_withdrawreceipt(global_db, resp_autowithdraw, merchant_key, card_uuid, ifsc,
#                                           card_num, card_account, three_element):
#     # 断言：检查代扣成功后withdraw和withdraw_receipt表数据统一检查
#     params_withdraw_receipt_trade_no = resp_autowithdraw["content"]["data"][
#         "trade_no"]  # 从返回中获取trade_no，关联到withdraw和withdraw_receipt
#     withdraw_info = get_global_withdraw_info_by_trade_no(global_db, params_withdraw_receipt_trade_no)
#     assert withdraw_info[0]["withdraw_merchant_key"] == merchant_key, '和传入一致'
#     assert withdraw_info[0]["withdraw_card_uuid"] == card_uuid, '和传入一致'
#     assert withdraw_info[0]["withdraw_callback"] == global_gbiz_callback, '和传入一致'
#     assert withdraw_info[0]["withdraw_receiver_bank_code"] == ifsc, '和传入一致'
#     assert withdraw_info[0]["withdraw_amount"] == global_amount, '代付金额和传入一致'
#     assert withdraw_info[0]["withdraw_channels"] == resp_autowithdraw["content"]["data"]["channel_name"], "代付通道一致"
#     assert withdraw_info[0]["withdraw_card_num"] == card_num, '虚拟卡号对应无误'
#     assert withdraw_info[0]["withdraw_receiver_no"] == card_account, '真是代付卡号和传入一致'
#     assert withdraw_info[0]["withdraw_receiver_name"] == three_element[0]["card_username"], '代付姓名和传入一致'
#     withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(global_db, params_withdraw_receipt_trade_no)
#     assert withdraw_receipt_info[0]["withdraw_receipt_merchant_key"] == merchant_key, '和传入一致'
#     assert withdraw_receipt_info[0]["withdraw_receipt_card_num"] == card_num, '虚拟卡号对应无误'
#     assert withdraw_receipt_info[0]["withdraw_receipt_amount"] == global_amount, '代付金额和传入一致'
#     assert withdraw_receipt_info[0]["withdraw_receipt_channel_name"] == resp_autowithdraw["content"]["data"][
#         "channel_name"], '代付通道一致'
#     if withdraw_info[0]["withdraw_card_uuid"] == global_razorpay_in_account_no:
#         assert withdraw_info[0]["withdraw_receiver_type"] == 2, '对公代付'
#     elif withdraw_info[0]["withdraw_card_uuid"] == global_paytm_in_account_no:
#         assert withdraw_info[0]["withdraw_receiver_type"] == 2, '对公代付'
#     else:
#         assert withdraw_info[0]["withdraw_receiver_type"] == 1, '对私代付'
#
#
# def assert_check_cashfree_withdraw_channelrequestlog(global_db, params_withdraw_receipt_trade_no):
#     withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(global_db,
#                                                                          params_withdraw_receipt_trade_no)
#     # 检查传给cashfree的金额单位是卢比
#     channel_request_log_info = get_global_withdraw_channel_request_log_by_channel_key(global_db,
#                                                                                       withdraw_receipt_info[0][
#                                                                                           "withdraw_receipt_channel_key"])
#     #  json.loads()函数是将字符串转化为字典
#     channel_request_log_request = json.loads(channel_request_log_info[0]["channel_request_log_request"])
#     Assert.assert_equal(int(channel_request_log_request["amount"]), int(global_amount / 100), 'cashfree代付金额单位卢比')
#
#
# def assert_check_flinpay_withdraw_channelrequestlog(global_db, params_withdraw_receipt_trade_no):
#     withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(global_db,
#                                                                          params_withdraw_receipt_trade_no)
#     # 检查传给cashfree的金额单位是卢比
#     channel_request_log_info = get_global_withdraw_channel_request_log_by_channel_key(global_db,
#                                                                                       withdraw_receipt_info[0][
#                                                                                           "withdraw_receipt_channel_key"])
#     #  json.loads()函数是将字符串转化为字典
#     channel_request_log_request = json.loads(channel_request_log_info[0]["channel_request_log_request"])
#     Assert.assert_equal(int(channel_request_log_request["money"]), int(global_amount), '代付金额单位印尼盾')
#
#
# def assert_check_razorpay_withdraw_channelrequestlog(global_db, params_withdraw_receipt_trade_no):
#     withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(global_db,
#                                                                          params_withdraw_receipt_trade_no)
#     # 检查传给cashfree的金额单位是卢比
#     channel_request_log_info = get_global_withdraw_channel_request_log_by_channel_key(global_db,
#                                                                                       withdraw_receipt_info[0][
#                                                                                           "withdraw_receipt_channel_key"])
#     #  json.loads()函数是将字符串转化为字典
#     channel_request_log_request = json.loads(channel_request_log_info[0]["channel_request_log_request"])
#     Assert.assert_equal(int(channel_request_log_request["amount"]), int(global_amount), 'razorpay代付金额单位卢比')
#
#
# def assert_withdraw_fail(global_db, params_withdraw_receipt_trade_no, merchant_key, three_element):
#     # 代付失败状态检查  +  sendmsg回调检查  + biz代扣结果查询
#     withdraw_info = get_global_withdraw_info_by_trade_no(global_db, params_withdraw_receipt_trade_no)
#     withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(global_db, params_withdraw_receipt_trade_no)
#     Assert.assert_equal(withdraw_info[0]["withdraw_status"], 3, '代付失败')
#     Assert.assert_equal(withdraw_receipt_info[0]["withdraw_receipt_status"], 3, '代付失败')
#     sendmsg_order_no = merchant_key  # sendmsg_order_no = global_gbiz_merchant_name + "_" + merchant_key
#     sendmsg_info = get_global_sendmsg_info_by_merchant_key(global_db, sendmsg_order_no)
#     #  json.loads()函数是将字符串转化为字典
#     sendmsg_content_info = json.loads(sendmsg_info[0]["sendmsg_content"])
#     Assert.assert_equal(sendmsg_info[0]["sendmsg_order_no"], sendmsg_order_no, '放款完成生成了代扣回调')
#     Assert.assert_equal(sendmsg_content_info["body"]["callbackUrl"], global_gbiz_callback, '回调地址和gbiz传入一致')
#     if withdraw_info[0]["withdraw_receiver_type"] == 1:
#         # gbiz调用放款查询接口查询
#         resp_withdraw_query = global_withdraw_query(merchant_key)
#         # 断言
#         assert resp_withdraw_query['content']['code'] == 1, "交易失败"
#         assert resp_withdraw_query['content']['data']['status'] == 3, "放款失败内层status=3"
#     else:
#         resp_transfer_query = global_transfer_query(merchant_key)
#         assert resp_transfer_query['content']['code'] == 1, "转账失败"
#         assert resp_transfer_query['content']['data']['status'] == 3, "转账失败内层status=3"
#
#
# def assert_withdraw_process(global_db, params_withdraw_receipt_trade_no, merchant_key, three_element):
#     # 代付处理中状态检查  +  处理中不生成sendmsg + biz代扣结果查询
#     withdraw_info = get_global_withdraw_info_by_trade_no(global_db, params_withdraw_receipt_trade_no)
#     withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(global_db, params_withdraw_receipt_trade_no)
#     Assert.assert_equal(withdraw_info[0]["withdraw_status"], 1, '代付处理中')
#     Assert.assert_equal(withdraw_receipt_info[0]["withdraw_receipt_status"], 1, '代付处理中')
#     if withdraw_info[0]["withdraw_receiver_type"] == 1:
#         # gbiz调用放款查询接口查询
#         resp_withdraw_query = global_withdraw_query(merchant_key)
#         # 断言
#         assert resp_withdraw_query['content']['code'] == 2, "代付处理中"
#         assert resp_withdraw_query['content']['data']['status'] == 1, "代付处理中内层status=1"
#     else:
#         resp_transfer_query = global_transfer_query(merchant_key)
#         assert resp_transfer_query['content']['code'] == 2, "转账交易处理中"
#         assert resp_transfer_query['content']['data']['status'] == 1, "代付处理中内层status=1"
#
#
# def assert_withdraw_success(global_db, params_withdraw_receipt_trade_no, merchant_key, three_element):
#     # 代付成功状态检查  +  sendmsg回调检查  + biz代扣结果查询
#     withdraw_info = get_global_withdraw_info_by_trade_no(global_db, params_withdraw_receipt_trade_no)
#     withdraw_receipt_info = get_global_withdraw_receipt_info_by_trade_no(global_db, params_withdraw_receipt_trade_no)
#     assert withdraw_info[0]["withdraw_status"] == 2, '代付成功'
#     assert withdraw_receipt_info[0]["withdraw_receipt_status"] == 2, '代付成功'
#     sendmsg_order_no = merchant_key  # sendmsg_order_no = global_gbiz_merchant_name + "_" + merchant_key
#     sendmsg_info = get_global_sendmsg_info_by_merchant_key(global_db, sendmsg_order_no)
#     #  json.loads()函数是将字符串转化为字典
#     sendmsg_content_info = json.loads(sendmsg_info[0]["sendmsg_content"])
#     Assert.assert_equal(sendmsg_info[0]["sendmsg_order_no"], sendmsg_order_no, '放款完成生成了代扣回调')
#     Assert.assert_equal(sendmsg_content_info["body"]["callbackUrl"], global_gbiz_callback, '回调地址和gbiz传入一致')
#     if withdraw_info[0]["withdraw_receiver_type"] == 1:
#         # gbiz调用放款查询接口查询
#         resp_withdraw_query = global_withdraw_query(merchant_key)
#         # 断言
#         assert resp_withdraw_query['content']['code'] == 0, "代付成功"
#         assert resp_withdraw_query['content']['data']['status'] == 2, "代付成功内层status=2"
#         assert resp_withdraw_query['content']['message'] == "交易成功", "交易成功"
#         assert resp_withdraw_query['content']['data']['platform_code'] == "E20000", "交易成功错误码"
#     else:
#         resp_transfer_query = global_transfer_query(merchant_key)
#         assert resp_transfer_query['content']['code'] == 0, "转账成功"
#         assert resp_transfer_query['content']['data']['status'] == 2, "转账成功内层status=2"
#
#
# def withhold_autoSubscribe(merchant_key, card_uuid, card_num_encrypt, user_name_encrypt, mobile_encrypt,
#                            email_encrypt, address_encrypt, ifsc):
#     # 组装绑卡参数
#     params_autobind = {
#         "merchant_key": merchant_key,
#         "sign_company": global_sign_company_yomoyo,
#         "card_uuid": card_uuid,
#         "card_num_encrypt": card_num_encrypt,
#         "user_name_encrypt": user_name_encrypt,
#         "mobile_encrypt": mobile_encrypt,
#         "email_encrypt": email_encrypt,
#         "address_encrypt": address_encrypt,  # account绑卡
#         "ifsc": ifsc
#     }
#     # 发起绑卡
#     resp_autoSubscribe = global_withhold_autoSubscribe(**params_autobind)
#     return resp_autoSubscribe
#
#
# def withdraw_autoWithdraw(card_uuid, merchant_key):
#     # 【代付】组装放款参数
#     params_autowithdraw = {
#         "merchant_key": merchant_key,
#         "amount": global_amount,
#         "sign_company": global_sign_company_yomoyo,
#         "card_uuid": card_uuid,
#         "merchant_name": global_gbiz_merchant_name
#     }
#     # 发起代付请求
#     resp_autowithdraw = global_autoWithdraw(**params_autowithdraw)
#     return resp_autowithdraw
#
#
# def run_task_bindingQuery(global_db, bank_account_encrypt):
#     # 手动执行task-bindingQuery
#     update_global_task_next_run_at(global_db)
#     card_info = get_global_card_info_by_card_account(global_db, bank_account_encrypt)
#     card_num = card_info[0]["card_num"]
#     process_binding_request_info = get_task_order_no_by_card_num(global_db, card_num)
#     orderNo = process_binding_request_info[0]["binding_request_merchant_key"]
#     params_task_order_no = {
#         "orderNo": orderNo
#     }
#     run_task_by_task_order_no(**params_task_order_no)
#     time.sleep(1)
#
#
# def run_task_withholdReceipt_withholdcharge_and_chargequery(global_db, merchant_key):
#     for i in range(6):
#         update_global_task_next_run_at(global_db)
#         # 自动代扣：手动执行task-withholdReceipt、withholdCharge、withholdChargeQuery、withholdUpdate、withholdChannelSwitchRouteThree，注意和主动还款不一样
#         params_task_order_no = {
#             "orderNo": merchant_key
#         }
#         run_task_by_task_order_no(**params_task_order_no)
#         time.sleep(1)
#
#
# def run_task_by_merchantkey_channelkey(global_db, merchant_key):
#     # 主动还款执行task-withholdCharge、withholdChargeQuery
#     update_global_task_next_run_at(global_db)
#     process_withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#     orderNo = merchant_key
#     orderNo2 = process_withhold_receipt_info[0]["withhold_receipt_channel_key"]
#     for i in range(3):
#         # 手动执行task-withholdCharge、withholdChargeQuery、withholdUpdate
#         params_task_order_no = {
#             "orderNo": orderNo2
#         }
#         run_task_by_task_order_no(**params_task_order_no)
#         time.sleep(1)
#         params_task_order_no = {
#             "orderNo": orderNo
#         }
#         run_task_by_task_order_no(**params_task_order_no)
#         time.sleep(1)
#
#
# def run_task_withdraw_and_withdrawquery(global_db, merchant_key):
#     # 执行withdraw，更新task_next_run_at=current_time
#     for i in range(3):
#         update_global_task_next_run_at(global_db)
#         # 手动执行task-withdraw、withdrawQuery、withdrawUpdate
#         params_task_order_no = {
#             "orderNo": merchant_key
#         }
#         run_task_by_task_order_no(**params_task_order_no)
#         time.sleep(1)
#
#
# def run_task_collectWithholdChargeQuery(global_db, account_no):
#     update_global_task_next_run_at(global_db)
#     for i in range(3):
#         # 手动执行task-collectWithholdChargeQuery
#         params_task_order_no = {
#             "orderNo": account_no
#         }
#         run_task_by_task_order_no(**params_task_order_no)
#         time.sleep(1)
#
#
# def run_reconci_task(global_db, task_order_no):
#     # 执行withdraw，更新task_next_run_at=current_time
#     update_global_task_next_run_at(global_db)
#     for i in range(5):
#         update_task_order_no(global_db, task_order_no)
#         # 手动执行task
#         params_task_order_no = {
#             "orderNo": task_order_no
#         }
#         run_task_by_task_order_no(**params_task_order_no)
#         time.sleep(1)
#
#
# def assert_autoRegister_chaneck_withholdaccount(global_db, account_no, card_uuid, user_uuid, individual_uuid, user_name,
#                                                 mobile, email, resp_withhold_autoRegister):
#     # 开户统一检查：withhold_account
#     withhold_account_info = get_global_withholdaccountinfo_by_accountno(global_db, account_no)
#     assert withhold_account_info[0]["withhold_account_card_uuid"] == card_uuid
#     assert withhold_account_info[0]["withhold_account_user_uuid"] == user_uuid
#     assert withhold_account_info[0]["withhold_account_individual_uuid"] == individual_uuid
#     assert withhold_account_info[0]["withhold_account_no"] == account_no
#     assert withhold_account_info[0]["withhold_account_cust_name"] == user_name
#     assert withhold_account_info[0]["withhold_account_cust_mobile"] == mobile
#     assert withhold_account_info[0]["withhold_account_cust_email"] == email
#     assert withhold_account_info[0]["withhold_account_receiver_channel"] == \
#            resp_withhold_autoRegister['content']['data']['channel_name']
#
#
# def assert_razorpay_autoRegister_fail(global_db, account_no, resp_withhold_autoRegister):
#     # 开户失败检查 + 返回给dsq状态检查
#     global_autoRegister_failstatus = "closed"
#     withhold_account_info = get_global_withholdaccountinfo_by_accountno(global_db, account_no)
#     assert withhold_account_info[0]["withhold_account_status"] == global_autoRegister_failstatus
#     assert resp_withhold_autoRegister['content']['code'] == 1
#     assert resp_withhold_autoRegister['content']['data']['account_status'] == global_autoRegister_failstatus
#
#
# def assert_razorpay_autoRegister_success(global_db, account_no, resp_withhold_autoRegister):
#     # 开户失败检查 + 返回给dsq状态检查
#     global_autoRegister_successstatus = "active"
#     withhold_account_info = get_global_withholdaccountinfo_by_accountno(global_db, account_no)
#     assert withhold_account_info[0]["withhold_account_status"] == global_autoRegister_successstatus
#     assert withhold_account_info[0]["withhold_account_status"] == global_autoRegister_successstatus
#     # razorpay线下还款开户成功，取channel_request_log返回虚户信息与withhold_account对比
#     customerregister_channel_request_log_info = get_razorpay_customerregister_channelrequestlog(global_db)
#     customerregister_channel_request_log_request = json.loads(
#         customerregister_channel_request_log_info[0]["channel_request_log_response"])  # json.loads()函数是将字符串转化为字典
#     customer_id = customerregister_channel_request_log_request["id"]  # 创建联系人返回的id用于下一步开户的入参
#     accountregister_channel_request_log_info = get_razorpay_accountregister_channelrequestlog_by_customerid(global_db,
#                                                                                                             customer_id)
#     channel_request_log_response = json.loads(
#         accountregister_channel_request_log_info[0]["channel_request_log_response"])  # json.loads()函数是将字符串转化为字典
#     assert channel_request_log_response["id"] in withhold_account_info[0]["withhold_account_inner_no"], '虚户号'
#     assert channel_request_log_response["receivers"][0]["entity"] == withhold_account_info[0][
#         "withhold_account_type"], '虚拟账户类型'
#     assert channel_request_log_response["receivers"][0]["account_number"] == withhold_account_info[0][
#         "withhold_account_receiver_account"], '收款银行账户'
#     assert channel_request_log_response["receivers"][0]["name"] == withhold_account_info[0][
#         "withhold_account_receiver_name"], '收款银行账户名称'
#     assert channel_request_log_response["receivers"][0]["bank_name"] == withhold_account_info[0][
#         "withhold_account_receiver_bank"], '收款银行名称'
#     assert channel_request_log_response["receivers"][0]["ifsc"] == withhold_account_info[0][
#         "withhold_account_receiver_ifsc"], '收款银行IFSC'
#     # razorpay线下还款开户成功，取channel_request_log返回虚户信息与返回给dsq的字段对比
#     assert resp_withhold_autoRegister['content']['code'] == 0
#     assert resp_withhold_autoRegister['content']['data']['account_status'] == global_autoRegister_successstatus
#     assert channel_request_log_response["receivers"][0]["entity"] == resp_withhold_autoRegister["content"]["data"][
#         "receiver_type"], '虚拟账户类型'
#     assert channel_request_log_response["receivers"][0]["account_number"] == \
#            resp_withhold_autoRegister["content"]["data"]["receiver_account"], '收款银行账户'
#     assert channel_request_log_response["receivers"][0]["name"] == resp_withhold_autoRegister["content"]["data"][
#         "receiver_name"], '收款银行账户名称'
#     assert channel_request_log_response["receivers"][0]["bank_name"] == resp_withhold_autoRegister["content"]["data"][
#         "receiver_bank"], '收款银行名称'
#     assert channel_request_log_response["receivers"][0]["ifsc"] == resp_withhold_autoRegister["content"]["data"][
#         "receiver_ifsc"], '收款银行IFSC'
#     assert withhold_account_info[0]["withhold_account_receiver_channel"] == \
#            resp_withhold_autoRegister['content']['data']['channel_name'], '开户通道'
#
#
# def assert_razorpay_collect_haverepaycard(global_db):
#     # 打款明细中返回了还款卡，卡号保存检查
#     withhold_info = get_withhold_by_merchant_key(global_db, global_razorpay_collect_channel_key1)
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db,
#                                                                              global_razorpay_collect_channel_key1)
#     card_info = get_global_card_info_by_card_account(global_db, global_razorpay_collect_cardnum_encrypt)
#     Assert.assert_equal(withhold_info[0]["withhold_card_num"], card_info[0]["card_num"], "还款卡号")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_card_num"], card_info[0]["card_num"], "还款卡号")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_mode"],
#                         global_razorpay_collect_payment_mode_upi, "代扣")
#     Assert.assert_equal(card_info[0]["card_status"], 0, "线下还款保存的卡号都是置为无效状态")
#     Assert.assert_equal(card_info[0]["card_account"], global_razorpay_collect_cardnum_encrypt, "线下还款保存卡号")
#     Assert.assert_equal(card_info[0]["card_username"], global_razorpay_collect_name_encrypt, "线下还款保存姓名")
#     Assert.assert_equal(card_info[0]["card_mobile"], global_razorpay_collect_mobile_encrypt, "线下还款保存手机号")
#     Assert.assert_equal(card_info[0]["card_bank_code"], global_razorpay_collect_ifsc, "线下还款保存银行编号")
#
#
# def assert_razorpay_collect_norepaycard(global_db):
#     # 打款明细没有返回还款卡
#     withhold_info = get_withhold_by_merchant_key(global_db, global_razorpay_collect_channel_key1)
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db,
#                                                                              global_razorpay_collect_channel_key1)
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_payment_mode"],
#                         global_razorpay_collect_payment_mode_other, "代扣")
#     Assert.assert_equal(withhold_info[0]["withhold_card_num"], "", "还款卡号")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_card_num"], "", "还款卡号")
#
#
# def assert_razorpay_collect_withhold_withholdreceipt_sendmsg(global_db, merchant_key, account_no, card_uuid,
#                                                              channel_name, global_rbiz_callbackurl):
#     # 线下还款成功withhold、withhold_receipt表统一检查(线下还款只会保存成功的记录)  +  sendmsg回调rbiz检查
#     withhold_info = get_withhold_by_merchant_key(global_db, merchant_key)
#     withhold_receipt_info = get_withhold_receipt_by_merchant_key(global_db, merchant_key)
#     Assert.assert_equal(withhold_info[0]["withhold_merchant_key"], merchant_key, "代扣")
#     assert withhold_info[0]["withhold_card_uuid"] == card_uuid, "代扣uuid"
#     Assert.assert_equal(withhold_info[0]["withhold_callback"], global_rbiz_callbackurl, "回调rbiz地址")
#     Assert.assert_equal(withhold_info[0]["withhold_amount"], global_razorpay_collect_paid_amount, "代扣")
#     Assert.assert_equal(withhold_info[0]["withhold_account_no"], account_no, "资产编号")
#     Assert.assert_equal(withhold_info[0]["withhold_status"], 2, "代扣")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_merchant_name"], global_rbiz_merchant_name, "代扣")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_merchant_key"], merchant_key, "代扣")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_name"], channel_name, "代扣")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_amount"], global_razorpay_collect_paid_amount, "代扣")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_status"], 2, "代扣")
#     Assert.assert_equal(withhold_receipt_info[0]["withhold_receipt_channel_resp_code"], "KN_COLLECT_SUCCESS", "代扣")
#     # 回调参数字段检查
#     sendmsg_order_no = merchant_key
#     sendmsg_info = get_global_sendmsg_info_by_merchant_key(global_db, sendmsg_order_no)
#     sendmsg_content_info = json.loads(sendmsg_info[0]["sendmsg_content"])  # json.loads()函数是将字符串转化为字典
#     assert sendmsg_info[0]["sendmsg_order_no"] == sendmsg_order_no, '线下还款完成生成了代扣回调'
#     assert sendmsg_content_info["body"]["callbackUrl"] == global_rbiz_callbackurl, '回调地址和rbiz给的配置一致'
#     assert sendmsg_content_info["body"]["notifyDto"]["channel_name"] == channel_name, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["merchant_key"] == merchant_key, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["channel_key"] == merchant_key, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["account_no"] == account_no, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["card_uuid"] == card_uuid, '还款通道回调配置'
#     assert sendmsg_content_info["body"]["notifyDto"]["amount"] == global_razorpay_collect_paid_amount, '线下还款金额'
#     assert sendmsg_content_info["body"]["notifyDto"]["status"] == 2, '代扣成功状态为2'
#
#
# def assert_check_cashfree_channel_reconciandsettlement(global_db):
#     channel_reconci_info = get_channel_reconci_by_settlement_id(global_db, cashfree_ebank_settlement_id)
#     channel_settlement_info = get_channel_settlement_by_settlement_id(global_db, cashfree_ebank_settlement_id)
#     if channel_reconci_info[0]["channel_reconci_channel_key"] == "RBIZ406113390126376318":
#         assert channel_reconci_info[0]["channel_reconci_channel_key"] == "RBIZ406113390126376318", "第一个流水"
#         assert channel_reconci_info[0]["channel_reconci_amount"] == 205400, "代扣总额"
#         assert channel_reconci_info[0]["channel_reconci_settlement_amount"] == 204810, "结算金额"
#         assert channel_reconci_info[0]["channel_reconci_fees"] == 590, "总费用"
#         assert channel_reconci_info[0]["channel_reconci_service_charge"] == 500, "服务费"
#         assert channel_reconci_info[0]["channel_reconci_service_tax"] == 90, "税"
#         assert channel_reconci_info[1]["channel_reconci_channel_key"] == "RBIZ406115960479098974", "第二个流水"
#         assert channel_reconci_info[1]["channel_reconci_amount"] == 151050, "代扣总额"
#         assert channel_reconci_info[1]["channel_reconci_settlement_amount"] == 150460, "结算金额"
#         assert channel_reconci_info[1]["channel_reconci_fees"] == 590, "总费用"
#         assert channel_reconci_info[1]["channel_reconci_service_charge"] == 500, "服务费"
#         assert channel_reconci_info[1]["channel_reconci_service_tax"] == 90, "税"
#     else:
#         assert channel_reconci_info[1]["channel_reconci_channel_key"] == "RBIZ406113390126376318", "第一个流水"
#         assert channel_reconci_info[1]["channel_reconci_amount"] == 205400, "代扣总额"
#         assert channel_reconci_info[1]["channel_reconci_settlement_amount"] == 204810, "结算金额"
#         assert channel_reconci_info[1]["channel_reconci_fees"] == 590, "总费用"
#         assert channel_reconci_info[1]["channel_reconci_service_charge"] == 500, "服务费"
#         assert channel_reconci_info[1]["channel_reconci_service_tax"] == 90, "税"
#         assert channel_reconci_info[0]["channel_reconci_channel_key"] == "RBIZ406115960479098974", "第二个流水"
#         assert channel_reconci_info[0]["channel_reconci_amount"] == 151050, "代扣总额"
#         assert channel_reconci_info[0]["channel_reconci_settlement_amount"] == 150460, "结算金额"
#         assert channel_reconci_info[0]["channel_reconci_fees"] == 590, "总费用"
#         assert channel_reconci_info[0]["channel_reconci_service_charge"] == 500, "服务费"
#         assert channel_reconci_info[0]["channel_reconci_service_tax"] == 90, "税"
#     assert channel_reconci_info[0]["channel_reconci_status"] == 2, "成功状态"
#     assert channel_reconci_info[0]["channel_reconci_provider_code"] == "cashfree", "渠道"
#     assert channel_reconci_info[0]["channel_reconci_merchant_no"] == "yomoyo2", "商户号"
#     assert channel_reconci_info[0]["channel_reconci_settlement_id"] == "262907", "结算id"
#     assert channel_reconci_info[0]["channel_reconci_channel_name"] == "cashfree_yomoyo2_ebank", "代扣通道"
#     assert channel_reconci_info[1]["channel_reconci_status"] == 2, "成功状态"
#     assert channel_reconci_info[1]["channel_reconci_provider_code"] == "cashfree", "渠道"
#     assert channel_reconci_info[1]["channel_reconci_merchant_no"] == "yomoyo2", "商户号"
#     assert channel_reconci_info[1]["channel_reconci_settlement_id"] == "262907", "结算id"
#     assert channel_reconci_info[1]["channel_reconci_channel_name"] == "cashfree_yomoyo2_ebank", "代扣通道"
#
#     assert channel_settlement_info[0]["channel_settlement_settlement_id"] == "262907", "结算表"
#     assert channel_settlement_info[0]["channel_settlement_amount"] == 356450, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_fees"] == 1180, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_service_charge"] == 1000, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_service_tax"] == 180, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_settlement_amount"] == 355270, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_adjustment_amount"] == 0, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_settled_amount"] == 355270, "结算表"
#
#
# def assert_check_razorpay_channel_reconciandsettlement(global_db):
#     channel_reconci_info = get_channel_reconci_by_settlement_id(global_db, "setl_EVd17tCHzrE3NE")
#     channel_settlement_info = get_channel_settlement_by_settlement_id(global_db, "setl_EVd17tCHzrE3NE")
#     if channel_reconci_info[0]["channel_reconci_channel_key"] == "RBIZ403226980514596029":
#         assert channel_reconci_info[0]["channel_reconci_channel_key"] == "RBIZ403226980514596029", "第一个流水"
#         assert channel_reconci_info[0]["channel_reconci_amount"] == 205400, "代扣总额"
#         assert channel_reconci_info[0]["channel_reconci_settlement_amount"] == 204810, "结算金额"
#         assert channel_reconci_info[0]["channel_reconci_fees"] == 590, "总费用"
#         assert channel_reconci_info[0]["channel_reconci_service_charge"] == 500, "服务费"
#         assert channel_reconci_info[0]["channel_reconci_service_tax"] == 90, "税"
#         assert channel_reconci_info[1]["channel_reconci_channel_key"] == "RBIZ403228392065164683", "第二个流水"
#         assert channel_reconci_info[1]["channel_reconci_amount"] == 151050, "代扣总额"
#         assert channel_reconci_info[1]["channel_reconci_settlement_amount"] == 150460, "结算金额"
#         assert channel_reconci_info[1]["channel_reconci_fees"] == 590, "总费用"
#         assert channel_reconci_info[1]["channel_reconci_service_charge"] == 500, "服务费"
#         assert channel_reconci_info[1]["channel_reconci_service_tax"] == 90, "税"
#     else:
#         assert channel_reconci_info[1]["channel_reconci_channel_key"] == "RBIZ403226980514596029", "第一个流水"
#         assert channel_reconci_info[1]["channel_reconci_amount"] == 205400, "代扣总额"
#         assert channel_reconci_info[1]["channel_reconci_settlement_amount"] == 204810, "结算金额"
#         assert channel_reconci_info[1]["channel_reconci_fees"] == 590, "总费用"
#         assert channel_reconci_info[1]["channel_reconci_service_charge"] == 500, "服务费"
#         assert channel_reconci_info[1]["channel_reconci_service_tax"] == 90, "税"
#         assert channel_reconci_info[0]["channel_reconci_channel_key"] == "RBIZ403228392065164683", "第二个流水"
#         assert channel_reconci_info[0]["channel_reconci_amount"] == 151050, "代扣总额"
#         assert channel_reconci_info[0]["channel_reconci_settlement_amount"] == 150460, "结算金额"
#         assert channel_reconci_info[0]["channel_reconci_fees"] == 590, "总费用"
#         assert channel_reconci_info[0]["channel_reconci_service_charge"] == 500, "服务费"
#         assert channel_reconci_info[0]["channel_reconci_service_tax"] == 90, "税"
#
#     assert channel_reconci_info[0]["channel_reconci_status"] == 2, "成功状态"
#     assert channel_reconci_info[0]["channel_reconci_provider_code"] == "razorpay", "渠道"
#     assert channel_reconci_info[0]["channel_reconci_merchant_no"] == "ECGW0RlTS1NOb3", "商户号"
#     assert channel_reconci_info[0]["channel_reconci_settlement_id"] == "setl_EVd17tCHzrE3NE", "结算id"
#     assert channel_reconci_info[0]["channel_reconci_channel_name"] == "razorpay_yomoyo_ebank", "代扣通道"
#     assert channel_reconci_info[1]["channel_reconci_status"] == 2, "成功状态"
#     assert channel_reconci_info[1]["channel_reconci_provider_code"] == "razorpay", "渠道"
#     assert channel_reconci_info[1]["channel_reconci_merchant_no"] == "ECGW0RlTS1NOb3", "商户号"
#     assert channel_reconci_info[1]["channel_reconci_settlement_id"] == "setl_EVd17tCHzrE3NE", "结算id"
#     assert channel_reconci_info[1]["channel_reconci_channel_name"] == "razorpay_yomoyo_ebank", "代扣通道"
#
#     assert channel_settlement_info[0]["channel_settlement_settlement_id"] == "setl_EVd17tCHzrE3NE", "结算表"
#     assert channel_settlement_info[0]["channel_settlement_amount"] == 356450, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_fees"] == 1180, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_service_charge"] == 1000, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_service_tax"] == 180, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_settlement_amount"] == 355270, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_adjustment_amount"] == 0, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_settled_amount"] == 355270, "结算表"
#     assert channel_settlement_info[0]["channel_settlement_provider_code"] == "razorpay", "渠道"
#     assert channel_settlement_info[0]["channel_settlement_merchant_no"] == "ECGW0RlTS1NOb3", "商户号"
#
#
# def assert_check_autopay_resp_data(resp_withhold_autopay, payment_type):
#     assert resp_withhold_autopay['content']['code'] == 2, "交易处理中"
#     assert resp_withhold_autopay['content']['data']['status'] == 1, "网关支付"
#     if payment_type == "ebank":
#         assert resp_withhold_autopay['content']['data']['payment_type'] == payment_type, "网关支付"
#         assert resp_withhold_autopay['content']['data']['payment_data']['redirect_url'] == global_ebank_payurl, "网关支付跳转地址"
#     elif payment_type == "sdk":
#         assert resp_withhold_autopay['content']['data']['payment_type'] == payment_type, "网关支付"
#         assert resp_withhold_autopay['content']['data']['payment_option'] == sdk_payment_option, "网关支付"
#         assert resp_withhold_autopay['content']['data']['payment_data']['token'] == global_cashfree_sdk_token, "网关支付跳转地址"
#         assert resp_withhold_autopay['content']['data']['payment_data']['notify_url'] == channel_notify_base_url + global_cashfree_sdk_channel_name, "网关支付"
#         assert resp_withhold_autopay['content']['data']['payment_data']['app_id'] == global_cashfree_sdk_appid, "网关支付"
