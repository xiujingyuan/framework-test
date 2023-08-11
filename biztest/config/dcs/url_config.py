import common.global_const as gc

# cmdb
cmdb_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-cmdb1/v6/rate/repay/calculate"

# gbiz - grant
gbiz_base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/grant%s" % gc.ENV
gbiz_asset_import_url = "/paydayloan/asset-sync-new"

# rbiz - repay
rbiz_base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/repay%s" % gc.ENV
rbiz_repay_url = "/paydayloan/repay/combo-active-encrypt"
rbiz_asset_void_url = "/trade/asset-void-withhold-encrypt"
rbiz_repay_callback_url = "/paysvr/callback"
rbiz_capital_plan_url = "/capital-asset/grant"
rbiz_latefee_url = "/asset/refreshLateFee"
rbiz_noloan_grant_url = "/sync/asset-withdraw-success"

# biz
biz_base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz%s-api" % gc.ENV
biz_asset_import_url = "/central/asset-sync"
biz_asset_grant_url = "/central/withdraw-success-receive"
biz_capital_plan_url = "/capital-asset/asset-loan"
biz_noloan_grant_url = "/central/asset-data-sync"

biz_advanced_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz%s-api/central/settle-reduce-sync" % gc.ENV
rbiz_compensate_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/repay%s/yunxinquanhu/pre-compensate-callback" % gc.ENV
rbiz_refresh_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/repay%s/asset/refreshLateFee" % gc.ENV
biz_account_url = "/central/receive-rbiz-account-sync"
biz_asset_change_url = "/central/receive-rbiz-asset-sync"

# dcs
dcs_base_url = gc.BASE_URL[gc.COUNTRY]['biz-dcs'].format(gc.ENV)
capital_settlement_notify_url = dcs_base_url + "/capital/settlement-notify"
run_task_url = dcs_base_url + "/task/run"
run_job_url = dcs_base_url + "/job/run?"

# biz_central
biz_central_base_url = "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/central%s" % gc.ENV
biz_central_asset_import_url = "/asset/import"
biz_central_asset_grant_url = "/asset/withdrawSuccess"
biz_central_capital_plan_url = "/capital-asset/import"


