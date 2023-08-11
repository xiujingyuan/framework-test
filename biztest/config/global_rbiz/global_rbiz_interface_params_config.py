from biztest.util.tools.tools import *


gbiz_asset_import_url = "/paydayloan/asset-sync"
route_loacle_url = "/router/locate"
payment_callback_url = "/payment/callback"

global_asset = {
    "type": "AssetWithdrawSuccess",
    "key": get_guid(),
    "data": {
        "asset": {
        },
        "loan_record": {
        },
        "trans": [],
        "borrower": {}
    },
    "from_system": "BIZ"
}
