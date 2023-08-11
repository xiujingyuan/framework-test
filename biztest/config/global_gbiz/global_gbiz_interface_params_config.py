from biztest.util.tools.tools import *

gbiz_asset_import_url = "/paydayloan/asset-sync"
route_locate_url = "/router/locate"
payment_callback_url = "/payment/callback"
gbiz_update_card_url = "/paydayloan/update-receive-card"
data_cancel_url = '/data/cancel'
grant_at_update_url = '/asset/grant-at-update'

route_locate_info = {
    "from_system": "DSQ",
    "key": get_guid(),
    "type": "LoanChannel",
    "data": {
        "asset": {
            "amount": 500000,
            "from_app": "instarupee",
            "from_system": "dsq",
            "from_system_name": "Instarupee",
            "hit_channel": "",
            "loan_usage": 1,
            "owner": "ft1",
            "period_count": 1,
            "period_day": "7",
            "period_type": "day",
            "product_name": "",
            "risk_level": "-1",
            "source_number": "",
            "source_type": "",
            "type": "paydayloan"
        },
        "borrower": {
            "borrower_card_uuid": "1015825385259617434",
            "borrower_uuid": "30922084234297344",
            "id_num": "",
            "individual_uuid": 30928102175539200,
            "mobile": "enc_01_2770351501754245120_827"
        }
    }
}

asset_import_info = {
    "type": "DSQAssetImport",
    "key": get_guid(),
    "from_system": "DSQ",
    "data": {
        "route_uuid": "",
        "asset": {
            "item_no": "",
            "type": "paydayloan",
            "product_name": "",
            "amount": 500,
            "period_type": "day",
            "period_count": 1,
            "period_day": "7",
            "loan_at": get_date(),
            "loan_usage": 0,
            "loan_channel": "",
            "is_face_recognised": 0,
            "source_type": "",
            "source_number": "",
            "risk_level": "1",
            "hit_channel": "",
            "repayment_type": "other",
            "owner": "ft1",
            "from_app": "草莓",
            "from_system": "DSQ",
            "rate_info": {
                "late_num": "late7%",
                "fees": {
                    "fin_service": 50.00,
                    "interest": 36.00
                  }
                }
        },
        "borrower": {
            "borrower_uuid": "borrower_uuid_0000002",
            "id_num": "enc_02_2574411798044739584_649",
            "mobile": "enc_01_2574411798095071232_327",
            "borrower_card_uuid": "borrower_card_uuid_0000002",
            "individual_uuid": "individual_uuid_0000002",
            "withdraw_type": "",
            "extend_info": None,
            "card_extend_info": None
        },
        "attachments": [],
        "risk_encrypted": "abc"
    }
}

update_receive_card_info = {
    "from_system": "DSQ",
    "key": get_guid(),
    "type": "UpdateCard",
    "data": {
        "card_uuid": "",
        "id_num": "",
        "item_no": "",
        "time_out": "",
        "withdraw_type": "",
        "bank_code": "",
        "wallet_code": ""
    }
}

grant_at_update_info = {
    "from_system": "biz",
    "key": get_guid(),
    "type": "AssetGrantAtUpdate",
    "data": {
        "item_no": "P2023061255339156395",
        "grant_at": "2023-06-13 13:00:00",
        "channel_key": "450000199703192745",
        "loan_channel": "goldlion"
    }
}

payment_callback_info = {
    "from_system": "paysvr",
    "key": "get_guid()",
    "type": "withdraw",
    "data": {
        "amount": "",
        "status": 2,
        "platform_code": "E20000",
        "platform_message": "Transaction not permitted to beneficiary account.",
        "channel_name": "gbpay_cymo1_withdraw",
        "channel_key": "2222222",
        "channel_code": "KN_REVERSE_ORDER",
        "channel_message": "Transaction not permitted to beneficiary account.",
        "trade_no": "",
        "finished_at": "",
        "merchant_key": ""
    }
}
