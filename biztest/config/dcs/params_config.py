
# # 首金／矢隆四平 提前结清的接口，repay 通过MQ通知 biz ， biz 通过接口通知 dcs
# biz_advanced_clearing_12 = {
#     "from_system": "Rbiz",
#     "key": "ZZ_slsp_0512_12qi435loan",
#     "type": "settleReductSync",
#     "data": [
#         {
#             "type": "interest",
#             "asset_period": 1,
#             "original_amount": 5667,
#             "withhold_amount": 0,
#             "withhold_at": "2020-05-18 14:58:00",
#             "push_at": "2020-05-18 15:16:42",
#             "asset_item_no": "ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type":"interest",
#             "asset_period":2,
#             "original_amount":5213,
#             "withhold_amount": 0,
#             "withhold_at":"2020-05-18 14:58:00",
#             "push_at":"2020-05-18 15:16:42",
#             "asset_item_no":"ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type":"interest",
#             "asset_period":3,
#             "original_amount":4755,
#             "withhold_amount": 0,
#             "withhold_at":"2020-05-18 14:58:00",
#             "push_at":"2020-05-18 15:16:42",
#             "asset_item_no":"ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type":"interest",
#             "asset_period":4,
#             "original_amount":4295,
#             "withhold_amount": 0,
#             "withhold_at":"2020-05-18 14:58:00",
#             "push_at":"2020-05-18 15:16:42",
#             "asset_item_no":"ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type":"interest",
#             "asset_period":5,
#             "original_amount":3831,
#             "withhold_amount": 0,
#             "withhold_at":"2020-05-18 14:58:00",
#             "push_at":"2020-05-18 15:16:42",
#             "asset_item_no":"ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type":"interest",
#             "asset_period":6,
#             "original_amount":3364,
#             "withhold_amount": 0,
#             "withhold_at":"2020-05-18 14:58:00",
#             "push_at":"2020-05-18 15:16:42",
#             "asset_item_no":"ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type":"interest",
#             "asset_period":7,
#             "original_amount":2893,
#             "withhold_amount": 0,
#             "withhold_at":"2020-05-18 14:58:00",
#             "push_at":"2020-05-18 15:16:42",
#             "asset_item_no":"ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type":"interest",
#             "asset_period":8,
#             "original_amount":2420,
#             "withhold_amount": 0,
#             "withhold_at":"2020-05-18 14:58:00",
#             "push_at":"2020-05-18 15:16:42",
#             "asset_item_no":"ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type": "interest",
#             "asset_period": 9,
#             "original_amount": 1942,
#             "withhold_amount": 0,
#             "withhold_at": "2020-05-18 14:58:00",
#             "push_at": "2020-05-18 15:16:42",
#             "asset_item_no": "ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type": "interest",
#             "asset_period": 10,
#             "original_amount": 1462,
#             "withhold_amount": 0,
#             "withhold_at": "2020-05-18 14:58:00",
#             "push_at": "2020-05-18 15:16:42",
#             "asset_item_no": "ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type": "interest",
#             "asset_period": 11,
#             "original_amount": 978,
#             "withhold_amount": 0,
#             "withhold_at": "2020-05-18 14:58:00",
#             "push_at": "2020-05-18 15:16:42",
#             "asset_item_no": "ZZ_slsp_0512_12qi435loan"
#         },
#         {
#             "type": "interest",
#             "asset_period": 12,
#             "original_amount": 492,
#             "withhold_amount": 0,
#             "withhold_at": "2020-05-18 14:58:00",
#             "push_at": "2020-05-18 15:16:42",
#             "asset_item_no": "ZZ_slsp_0512_12qi435loan"
#         }
#     ],
#     "sync_datetime": "null",
#     "busi_key": "null"
# }
# 新 biz 调用
capital_settlement_notify = {
    "from_system": "BIZ-CENTRAL",
    "key": "ha_20201609218837443373_lz",
    "type": "CapitalTransactionClearing",
    "data": {
        "loan_channel": "zhongke_lanzhou",
        "asset_item_no": "ha_20201609218837443373_lz",
        # "repay_type": "advance",
        # "withhold_channel": "qsq",
        "version": "1739276114799",
        "capital_transactions": []
    }
}





# 云信全互代偿
rbiz_compensate = {
    "uniqueId": "RN328e5426-c1d0-11ea-9d7e-5254006efd26",
    "compensateList": "compensateList",
    "compensateTime": "2020-07-09 13:13:13"
}
rbiz_compensateList = [
    {
             "term": 1,
             "principal": 634.10,
             "interest":  0.00,
             "odInterest": 0.00,
             "totalAmount": 724.10
         }, {
             "term": 2,
             "principal": 646.78,
             "interest":  0.00,
             "odInterest": 0.00,
             "totalAmount": 646.78
         }, {
             "term": 3,
             "principal": 659.72,
             "interest":  0.00,
             "odInterest": 0.00,
             "totalAmount": 659.72
         }, {
             "term": 4,
             "principal": 672.91,
             "interest":  0.00,
             "odInterest": 0.00,
             "totalAmount": 672.91
         }, {
             "term": 5,
             "principal": 686.37,
             "interest":  0.00,
             "odInterest": 0.00,
             "totalAmount": 686.37
         }, {
             "term": 6,
             "principal": 700.12,
             "interest":  0.00,
             "odInterest": 0.00,
             "totalAmount": 700.12
         }
    ]


# 旧资产的 cards_info
cards_info_old = {
    "repay_card": {
        "account_num_encrypt": "enc_03_3473198268291745792_344",
        "account_type": "debit",
        "bank_code": "CCB",
        "bankname": "中国建设银行",
        "credentials_num_encrypt": "enc_02_3473198268560181248_835",
        "credentials_type": "0",
        "individual_idnum_encrypt": "enc_02_3473198268560181248_835",
        "phone_encrypt": "enc_01_3473198268795062272_057",
        "username_encrypt": "enc_04_5708320_099"
    },
    "receive_card": {
        "account_name_encrypt": "enc_04_5708320_099",
        "bank": "中国建设银行",
        "bank_code": "CCB",
        "name": "中国建设银行",
        "num_encrypt": "enc_03_3473198268291745792_344",
        "owner_id_encrypt": "enc_02_3473198268560181248_835",
        "owner_name_encrypt": "enc_04_5708320_099",
        "type": "individual",
        "phone_encrypt": "enc_01_3473198268795062272_057",
        "factor_by": 4
    }
}


