# -*- coding: utf-8 -*-

rbiz_monitor_check_url = "/monitor/check"
# 国内rbiz所有的接口列表--start
combo_active_path = "/paydayloan/repay/combo-active-encrypt"
combo_query_key_path = '/paydayloan/repay/combo-query-key'
combo_query_order_path = '/paydayloan/repay/combo-query-order'
transaction_confirm_path = "/paydayloan/repay/transaction-confirm"
project_repay_query_path = '/paydayloan/projectRepayQuery?project_num={}&project_type={}'
update_repay_card_path = "/paydayloan/update-repay-card-encrypt"
update_asset_repayment_app_path = "/paydayloan/update-asset-repayment-app"
update_query_asset_overdue_count_path = "/paydayloan/query-asset-overdue-count"
update_query_exist_withhold_path = "/paydayloan/repay/existWithhold"
bind_sms_path = "/paydayloan/repay/bindSms"
withhold_order_query_path = "/paydayloan/withhold-record-query"
repay_trial_path = "/paydayloan/repay-trial"
manual_withhold_path = "/manual/withhold-encrypt"
four_factor_withhold_path = '/manual/withhold-without-project-encrypt'
fox_manual_withhold_path = "/fox/manual-withhold-encrypt"
fox_manual_withhold_query_path = '/fox/manual-withhold-query'
fox_deadline_asset_query_path = '/fox/deadline-asset-query-encrypt'
asset_overdue_view_for_fox_path = '/asset/overdue-view-for-fox?asset_item_no={}'
# TODO
fox_withhold_path = '/fox/withhold'
fox_withhold_query_path = '/fox/withhold-query?req_key={}'
fox_overdue_view_for_fox_path = "/fox/overdue-view-for-fox?itemNo={}"
fox_query_new_overdue_path = "/fox/query-new-overdue?start_date={}&end_date={}"
fox_query_new_overdue_asset_detail_path = '/fox/query-new-overdue-asset-detail'
fox_query_asset_repay_path = '/fox/query-asset-repay'
fox_query_asset_repay_detail_path = '/fox/query-asset-repay-detail?item_no={}&repay_date={}'
fox_query_withhold_records_path = "/fox/query-withhold-records"
fox_query_card_list_path = '/fox/query-card-list-encrypt'
asset_bill_decrease_path = '/asset/bill/decrease'
asset_buyback_path = '/asset/buy-back'
asset_settle_debt_path = "/asset/settleDebt"
fox_cancel_and_decrease_path = "/fox/cancel-and-decrease"

fk_asset_info_path = '/fk/asset-info'
trade_withhold_path = '/trade/withhold-order-encrypt'
trade_withhold_query_path = "/trade/withhold-order-query"
withhold_refund_path = '/repeatedWithhold/refund'
mozhi_apply_path = '//mozhibeiyin/repay.apply'
mozhi_query_path = '//mozhibeiyin/repay.query'
# 国内rbiz所有的接口列表--end

# 线下卡对卡还款接口
offline_withhold_apply = "/paydayloan/offline/withhold-apply"
offline_withhold_confirm = "/paydayloan/offline/withhold-confirm"
offline_withhold_query = "/paydayloan/offline/withhold-query"
offline_withhold_deal = "/paydayloan/offline/withhold-deal"
run_msg_by_id_path = "/msg/run?msgId={}"
run_task_by_id_path = "/task/run?taskId={}"
run_task_by_order_no_path = '/task/run?orderNo={}'
run_msg_by_order_no_path = '/msg/run?orderNo={}'

refresh_late_fee_path = "/asset/refreshLateFee"
asset_void_withhold_path = "/trade/asset-void-withhold-encrypt"

paysvr_callback_path = "/paysvr/callback"
paysvr_trade_callback_path = "/paysvr/trade/callback"
weishenma_callback_path = "/weishenma/daxinganling/repay-callback"
mozhi_callback_path = "/mozhibeiyin/repay-callback"

grant_withdraw_url = 'http://testing-api.kuainiu.io/grant/withdraw-success'
global_grant_withdraw_url = 'http://testing-api.kuainiu.io/grant-global/withdraw-success'
global_sync_asset_from_grant_path = '/sync/asset/from-grant'
global_gbiz_asset_import_path = "/paydayloan/asset-sync"

global_refund_online_path = '/page/asset/repeated-withhold/online-refund'
global_refund_offline_path = '/page/asset/repeated-withhold/offline-refund'
global_refund_query_path = '/page/asset/repeated-withhold/refunds?item_no={}&from_system={}'
force_refund_path = '/page/force-withhold-refund'
trade_refund_path = '/trade/order-refund-apply'
globak_refund_callback_path = '/paysvr/trade/refund/callback'
globak_withdraw_callback_path = "/paysvr/withdraw/callback"
withhold_cancel_path = '/paydayloan/cancel-withhold'
asset_withdraw_success = '/sync/asset-withdraw-success'
asset_withdraw_biz = '/central/withdraw-success-receive'
asset_withdraw_central = '/asset/withdrawSuccess'
capital_asset_success = '/capital-asset/grant'
capital_asset_biz = '/capital-asset/asset-loan'
capital_asset_central = '/capital-asset/import'

query_withhold_path = '/page/query-withhold-encrypt'
query_withhold_by_one_path = '/page/query-withhold-one-encrypt?item_no={}&serial_no={}'
asset_repay_period_path = '/asset/repayPeriod'
asset_repay_path = '/asset/repay'
asset_settle_period_path = '/asset/settlePeriod'
asset_tran_decrease_path = '/assetTran/decrease'
asset_tran_decrease_late_fee_path = '/assetTran/decreaseLateFee'
asset_repay_reverse_path = '/asset/repayReverse'
account_recharge_path = '/account/recharge-encrypt'
account_balance_clear_path = '/account/balance-clear-encrypt'
sync_withhold_card_path = "/sync/withhold-card-encrypt"
asset_provision_settle_path = "/asset/provision-settle-asset"
asset_void_from_mq = "/asset/void-asset-from-mq"
asset_cancel_from_mq = "/asset/cancel-asset-from-mq"
asset_tolerance_settle_path = "/asset/tolerance-settle-asset"

asset_change_mq = '/sync/asset-change-mq-sync-encrypt'

global_project_repay_query_path = '/paydayloan/project-repay-query?project_num={}&project_type={}'

global_paysvr_smart_collect_path = '/paysvr/offline-withhold/callback'
global_paysvr_query_tolerance_result_path = '/paysvr/query-tolerance-result?withhold_serial_no={}&actual_repay_amount={}'

mock_base_url = 'https://easy-mock.k8s-ingress-nginx.kuainiujinke.com/mock/5de5d515d1784d36471d6041/rbiz_auto_test'
mock_paysvr_query_protocol_channels_path = '/channel/queryProtocolChannels'
mock_paysvr_auto_pay_path = '/withhold/autopay'
mock_paysvr_transaction_query_path = '/transaction/query'
mock_paysvr_bind_sms_path = '/withhold/bindSms'

mock_global_paysvr_auto_pay_path = '/withhold/autoPay'
mock_global_paysvr_withhold_query_path = '/withhold/query'

xxl_job_url = "https://xxl-job-test-new.kuainiujinke.com/xxl-job-admin"
xxl_job_url_k8s = "https://biz-test-job.k8s-ingress-nginx.kuainiujinke.com/xxl-job-admin"
global_yindu_xxl_job_url = ""
global_taiguo_xxl_job_url = ""
global_phl_xxl_job_url = ""
global_xxl_job_new_url = ""

XXL_JOB_DICT = {
    "xxl_job": {'url': xxl_job_url, 'username': 'admin', 'password': 'MTIzNDU2'},
    "xxl_job_k8s": {'url': xxl_job_url_k8s, 'username': 'admin', 'password': '123456'},
    "global_yindu_xxl_job": {'url': global_yindu_xxl_job_url, 'username': 'admin', 'password': 'MTIzNDU2'},
    "global_taiguo_xxl_job": {'url': global_taiguo_xxl_job_url, 'username': 'admin', 'password': '123456'},
    "global_xxl_job_new": {'url': global_xxl_job_new_url, 'username': 'admin', 'password': '123456'}
}

