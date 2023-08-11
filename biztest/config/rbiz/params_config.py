# -*- coding: utf-8 -*-
from biztest.util.tools.tools import get_guid, get_guid4, get_date
import random

# 进件参数 - 大单
asset_import_info_loan_channel = {
    "type": "DSQAssetImport",
    "key": get_guid(),
    "from_system": "banana",
    "data": {
        "asset": {
            "item_no": "",
            "type": "paydayloan",
            "name": "name_#{item_no}",
            "product_name": "贷上钱",
            "ref_item_no": "",
            "period_type": "month",
            "period_count": 3,
            "period_day": 0,
            "repayment_type": "other",
            "fee_rate": 0,
            "interest_rate": 0,
            "secure_rate": 0,
            "manage_rate": 0,
            "withhold_rate": 0,
            "withhold_multi_period": 0,
            "amount": 4000,
            "first_channel": "Paydayloan",
            "second_channel": "",
            "province": "湖北省",
            "city": "孝感市",
            "province_district_code": "370000",
            "city_district_code": "370200",
            "due_at": "",
            "first_payat": "",
            "payoff_at": "",
            "grant_at": "#{system_date}",
            "secure_amount": 0,
            "manage_amount": 0,
            "sign_at": "1000-01-01 00:00:00",
            "interest_amount": "",
            "sub_type": "multiple",
            "loan_channel": "manaowan",
            "channel_verification_code": "",
            "cmdb_product_number": "",
            "decrease_amount": "",
            "loan_usage": "1",
            "charge_type": 1,
            "is_face_recognised": 1,
            "source_type": "youxi_bill",
            "source_number": "manaowan_#{item_no}_noloan",
            "withholding_amount": 0,
            "sub_order_type": "",
            "risk_level": 2,
            "hit_channel": "",
            "from_system_name": "dsq",
            "from_app": "dsq"
        },
        "asset_extend": {
            "distribute_type": 1
        },
        "borrower": {
            "name_encrypt": "enc_04_1723850_411",
            "idnum_encrypt": "enc_02_1723860_422",
            "gender": "f",
            "tel_encrypt": "enc_01_1723870_533",
            "mate_name_encrypt": "",
            "mate_tel_encrypt": "",
            "workmate_name_encrypt": "",
            "workmate_tel_encrypt": "",
            "credit_score": "",
            "id_type": 1,
            "residence": "山东省青岛市胶州市铺集镇吴家庄",
            "workplace": "山东省青岛市胶州市铺集镇吴家庄",
            "corp_name": "利郎男装专卖",
            "corp_tel_encrypt": "",
            "relative_name_encrypt": "enc_04_799640_910",
            "relative_tel_encrypt": "enc_01_895870_745",
            "relative_relation": 8,
            "second_relative_name_encrypt": "enc_04_799660_386",
            "second_relative_tel_encrypt": "enc_01_799670_679",
            "second_relative_relation": 6,
            "school_name": "",
            "school_place": "",
            "enrollment_time": "",
            "marriage": 1,
            "education": 4,
            "corp_trade": 10,
            "duty": 0,
            "id_addr": "山东省青岛市胶州市铺集镇吴家庄",
            "nation": "汉",
            "income": "5001-8000",
            "email": "13797103222@139.com",
            "payment_source": "",
            "career_type": "上班族",
            "idnum_expire_day": "2028-03-04",
            "idnum_begin_day": "2008-03-04",
            "idnum_cert_office": "安陆市公安局"
        },
        "repayer": {
            "name_encrypt": "enc_04_1723850_411",
            "idnum_encrypt": "enc_02_1723860_422",
            "gender": "f",
            "tel_encrypt": "enc_01_1723870_533",
            "mate_name_encrypt": "",
            "mate_tel_encrypt": "",
            "workmate_name_encrypt": "",
            "workmate_tel_encrypt": "",
            "credit_score": "",
            "id_type": 1,
            "residence": "山东省青岛市胶州市铺集镇吴家庄",
            "workplace": "山东省青岛市胶州市铺集镇吴家庄",
            "corp_name": "利郎男装专卖",
            "corp_tel_encrypt": "",
            "relative_name_encrypt": "enc_04_799640_910",
            "relative_tel_encrypt": "enc_01_895870_745",
            "relative_relation": 8,
            "second_relative_name_encrypt": "enc_04_799660_386",
            "second_relative_tel_encrypt": "enc_01_799670_679",
            "second_relative_relation": 6,
            "school_name": "",
            "school_place": "",
            "enrollment_time": "",
            "marriage": 1,
            "education": 4,
            "corp_trade": 10,
            "duty": 0,
            "id_addr": "山东省青岛市胶州市铺集镇吴家庄",
            "nation": "汉",
            "income": "5001-8000",
            "email": "13797103222@139.com",
            "payment_source": "",
            "career_type": "上班族",
            "idnum_expire_day": "2028-03-04",
            "idnum_begin_day": "2008-03-04",
            "idnum_cert_office": "安陆市公安局"
        },
        "repay_card": {
            "bankname": "中国建设银行",
            "bank_code": "ccb",
            "username_encrypt": "enc_04_1723850_411",
            "phone_encrypt": "enc_01_1723870_533",
            "individual_idnum_encrypt": "enc_02_1723860_422",
            "credentials_type": "0",
            "credentials_num_encrypt": "enc_02_1723860_422",
            "account_type": "debit",
            "account_num_encrypt": "enc_03_1723840_984"
        },
        "receive_card": {
            "name": "中国建设银行",
            "num_encrypt": "enc_03_1723840_984",
            "bank": "中国建设银行",
            "bank_code": "ccb",
            "type": "individual",
            "owner_id_encrypt": "enc_02_1723860_422",
            "owner_name_encrypt": "enc_04_1723850_411",
            "account_name_encrypt": "enc_04_1723850_411",
            "phone_encrypt": "enc_01_1723870_533"
        },
        "dtransactions": [],
        "fees": [],
        "attachments": [
            {
                "attachment_type": 1,
                "attachment_type_text": "身份证正面照片",
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/20190528/5ceca12696c3c15590116227507.jpe",
                "attachment_upload_at": "2018-12-23 14:38:37",
                "attachment_quality_score": "19"
            },
            {
                "attachment_type": 2,
                "attachment_type_text": "身份证反面照片",
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/20190528/5ceca12836d8015590116244662.jpe",
                "attachment_upload_at": "2018-12-23 14:38:37",
                "attachment_quality_score": "23"
            },
            {
                "attachment_type": 29,
                "attachment_type_text": "活体识别照片",
                "attachment_url": "http://paydayloandevv4-1251122539.cossh.myqcloud.com/20170725/ff79e74355a8370bb44b27f86ac85ae1.jpe",
                "attachment_upload_at": "2019-11-13 10:18:57",
                "attachment_quality_score": 48
            }
        ],
        "risk_encrypted": "",
        "borrower_extend": {
            "address_district_code": 420982,
            "agreement": "Y",
            "idnum_begin_day": "2008-03-04",
            "idnum_expire_day": "2028-03-04",
            "idnum_cert_office": "安陆市公安局"
        }
    }
}

# 进件参数 - 小单
asset_import_info_no_loan = {
    "type": "DSQAssetImport",
    "key": get_guid() + "n",
    "from_system": "banana",
    "data": {
        "asset": {
            "item_no": "",
            "type": "paydayloan",
            "name": "name_#{item_no}",
            "product_name": "贷上钱",
            "ref_item_no": "",
            "period_type": "month",
            "period_count": 3,
            "period_day": 0,
            "repayment_type": "other",
            "fee_rate": 0,
            "interest_rate": 0,
            "secure_rate": 0,
            "manage_rate": 0,
            "withhold_rate": 0,
            "withhold_multi_period": 0,
            "amount": 4000,
            "first_channel": "Paydayloan",
            "second_channel": "",
            "province": "四川省",
            "city": "成都市",
            "province_district_code": "370000",
            "city_district_code": "370200",
            "due_at": "",
            "first_payat": "",
            "payoff_at": "",
            "grant_at": "#{system_date}",
            "secure_amount": 0,
            "manage_amount": 0,
            "sign_at": "1000-01-01 00:00:00",
            "interest_amount": "",
            "sub_type": "multiple",
            "loan_channel": "manaowan",
            "channel_verification_code": "",
            "cmdb_product_number": "",
            "decrease_amount": "",
            "loan_usage": "1",
            "charge_type": 1,
            "is_face_recognised": 1,
            "source_type": "youxi_bill_split",
            "source_number": "manaowan_#{item_no}_noloan",
            "withholding_amount": 0,
            "sub_order_type": "",
            "risk_level": 2,
            "hit_channel": "",
            "from_system_name": "dsq",
            "from_app": "dsq"
        },
        "asset_extend": {
            "distribute_type": 1
        },
        "borrower": {
            "name_encrypt": "enc_04_1723850_411",
            "idnum_encrypt": "enc_02_1723860_422",
            "gender": "f",
            "tel_encrypt": "enc_01_1723870_533",
            "mate_name_encrypt": "",
            "mate_tel_encrypt": "",
            "workmate_name_encrypt": "",
            "workmate_tel_encrypt": "",
            "credit_score": "",
            "id_type": 1,
            "residence": "山东省青岛市胶州市铺集镇吴家庄",
            "workplace": "山东省青岛市胶州市金尔路1号",
            "corp_name": "利郎男装专卖",
            "corp_tel_encrypt": "",
            "relative_name_encrypt": "enc_04_799640_910",
            "relative_tel_encrypt": "enc_01_895870_745",
            "relative_relation": 8,
            "second_relative_name_encrypt": "enc_04_799660_386",
            "second_relative_tel_encrypt": "enc_01_799670_679",
            "second_relative_relation": 6,
            "school_name": "",
            "school_place": "",
            "enrollment_time": "",
            "marriage": 1,
            "education": 4,
            "corp_trade": 10,
            "duty": 0,
            "id_addr": "山东省胶州市铺集镇吴家庄村45号",
            "nation": "汉",
            "income": "5001-8000",
            "email": "13797103222@139.com",
            "payment_source": "",
            "career_type": "上班族",
            "idnum_expire_day": "2028-03-04",
            "idnum_begin_day": "2008-03-04",
            "idnum_cert_office": "兴文县公安"
        },
        "repayer": {
            "name_encrypt": "enc_04_1723850_411",
            "idnum_encrypt": "enc_02_1723860_422",
            "gender": "f",
            "tel_encrypt": "enc_01_1723870_533",
            "mate_name_encrypt": "",
            "mate_tel_encrypt": "",
            "workmate_name_encrypt": "",
            "workmate_tel_encrypt": "",
            "credit_score": "",
            "id_type": 1,
            "residence": "山东省青岛市胶州市铺集镇吴家庄",
            "workplace": "山东省青岛市胶州市铺集镇吴家庄",
            "corp_name": "利郎男装专卖",
            "corp_tel_encrypt": "",
            "relative_name_encrypt": "enc_04_799640_910",
            "relative_tel_encrypt": "enc_01_895870_745",
            "relative_relation": 8,
            "second_relative_name_encrypt": "enc_04_799660_386",
            "second_relative_tel_encrypt": "enc_01_799670_679",
            "second_relative_relation": 6,
            "school_name": "",
            "school_place": "",
            "enrollment_time": "",
            "marriage": 1,
            "education": 4,
            "corp_trade": 10,
            "duty": 0,
            "id_addr": "山东省胶州市铺集镇吴家庄村45号",
            "nation": "汉",
            "income": "5001-8000",
            "email": "13797103222@139.com",
            "payment_source": "",
            "career_type": "上班族",
            "idnum_expire_day": "2028-03-04",
            "idnum_begin_day": "2008-03-04",
            "idnum_cert_office": "安陆市公安局"
        },
        "repay_card": {
            "bankname": "中国建设银行",
            "bank_code": "ccb",
            "username_encrypt": "enc_04_1723850_411",
            "phone_encrypt": "enc_01_1723870_533",
            "individual_idnum_encrypt": "enc_02_1723860_422",
            "credentials_type": "0",
            "credentials_num_encrypt": "enc_02_1723860_422",
            "account_type": "debit",
            "account_num_encrypt": "enc_03_1723840_984"
        },
        "receive_card": {
            "name": "中国建设银行",
            "num_encrypt": "enc_03_1723840_984",
            "bank": "中国建设银行",
            "bank_code": "ccb",
            "type": "individual",
            "owner_id_encrypt": "enc_02_1723860_422",
            "owner_name_encrypt": "enc_04_1723850_411",
            "account_name_encrypt": "enc_04_1723850_411",
            "phone_encrypt": "enc_01_1723870_533"
        },
        "dtransactions": [],
        "fees": [],
        "attachments": [
            {
                "attachment_type": 1,
                "attachment_type_text": "身份证正面照片",
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/20190528/5ceca12696c3c15590116227507.jpe",
                "attachment_upload_at": "2018-12-23 14:38:37",
                "attachment_quality_score": "19"
            },
            {
                "attachment_type": 2,
                "attachment_type_text": "身份证反面照片",
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/20190528/5ceca12836d8015590116244662.jpe",
                "attachment_upload_at": "2018-12-23 14:38:37",
                "attachment_quality_score": "23"
            },
            {
                "attachment_type": 29,
                "attachment_type_text": "活体识别照片",
                "attachment_url": "http://paydayloandevv4-1251122539.cossh.myqcloud.com/20170725/ff79e74355a8370bb44b27f86ac85ae1.jpe",
                "attachment_upload_at": "2019-11-13 10:18:57",
                "attachment_quality_score": 48
            }
        ],
        "risk_encrypted": "",
        "borrower_extend": {
            "address_district_code": 420982,
            "agreement": "Y",
            "idnum_begin_day": "2008-03-04",
            "idnum_expire_day": "2028-03-04",
            "idnum_cert_office": "安陆市公安局"
        }
    }
}

# 泰国进件参数
ASSET_IMPORT_INFO_THA = {
    "type": "DSQAssetImport",
    "key": "asset_sync_0001",
    "from_system": "DSQ",
    "data": {
        "asset": {
            "item_no": "ph_fairy7_0615_000001",
            "type": "paydayloan",
            "product_name": "fairyfruit",
            "period_type": "day",
            "period_count": 1,
            "period_day": "7",
            "amount": 2000000,
            "loan_at": "2020-06-15 10:31:27",
            "loan_channel": "tha_bankcard",
            "loan_usage": 1,
            "is_face_recognised": 1,
            "source_type": "fee_20_normal",
            "source_number": "",
            "risk_level": "1",
            "hit_channel": "",
            "repayment_type": "",
            "owner": "tailand",
            "from_app": "fairyfruit",
            "from_system": "DSQ",
            "from_system_name": "fairyfruit"
        },
        "borrower": {
            "id_num": "enc_02_2919417036084348928_507",
            "mobile": "enc_01_2919417036419893248_042",
            "borrower_uuid": "borrower_uuid_2400009",
            "individual_uuid": "individual_uuid_2400009",
            "borrower_card_uuid": "584087996517533"
        },
        "attachments": []
    }
}

# 印度进件参数
ASSET_IMPORT_INFO_IND = {
    "type": "DSQAssetImport",
    "key": "{{key}}",
    "from_system": "DSQ",
    "data": {
        "asset": {
            "item_no": "{{item_no}}",
            "type": "paydayloan",
            "product_name": "NBFC",
            "period_type": "day",
            "period_count": 1,
            "period_day": "7",
            "amount": 50000,
            "loan_at": "{{grant_at}}",
            "loan_channel": "nbfc_sino",
            "loan_usage": 1,
            "is_face_recognised": 1,
            "source_type": "{{source_type}}",
            "source_number": "",
            "risk_level": "1",
            "hit_channel": "",
            "repayment_type": "",
            "owner": "ft1",
            "from_app": "masala",
            "from_system": "DSQ",
            "from_system_name": "masala"
        },
        "borrower": {
            "borrower_uuid": "110112199405106872",
            "id_num": "enc_02_2977410198345883648_474",
            "mobile": "enc_01_2977410198312329216_388",
            "borrower_card_uuid": "1020070600000015906",
            "individual_uuid": "110112199405106872"
        },
        "attachments": [
        ]
    }
}

# 泰国同步放款到还款参数
ASSET_SYNC_INFO_THA = {
    "type": "AssetWithdrawSuccess",
    "key": "gb_{{$guid}}",
    "data": {
        "asset": {
            "asset_item_no": "{{item_no}}",
            "type": "paydayloan",
            "sub_type": "multiple",
            "period_type": "day",
            "period_count": 1,
            "product_category": "7",
            "cmdb_product_number": "tha_bankcard_1_7d_20200601_20",
            "grant_at": "2020-06-06 14:09:39",
            "effect_at": "2020-06-06 14:09:39",
            "actual_grant_at": "2020-06-06 14:09:39",
            "due_at": "2020-06-13 00:00:00",
            "payoff_at": "2020-06-06 00:00:00",
            "status": "repay",
            "principal_amount": 50000,
            "granted_principal_amount": 40000,
            "loan_channel": "tha_bankcard",
            "alias_name": "",
            "interest_amount": 350,
            "fee_amount": 0,
            "balance_amount": 0,
            "repaid_amount": 0,
            "total_amount": 50350,
            "version": "{{ctime}}",
            "interest_rate": 0.01,
            "charge_type": 1,
            "ref_order_no": "",
            "ref_order_type": "",
            "sub_order_type": None,
            "overdue_guarantee_amount": 0,
            "info": "",
            "owner": "TAILAND",
            "from_app": "fairyfruit",
            "from_system_name": "fairyfruit",
            "from_system": "dsq",
            "product_name": "NBFC",
            "risk_level": "1"
        },
        "loan_record": {
            "asset_item_no": "{{item_no}}",
            "amount": 50000,
            "withholding_amount": 10000,
            "channel": "tha_bankcard",
            "status": 6,
            "identifier": "ID402145321383522946",
            "trade_no": "RN{{item_no}}",
            "due_bill_no": "dbn{{item_no}}",
            "commission_amount": None,
            "pre_fee_amount": None,
            "service_fee_amount": None,
            "is_deleted": None,
            "finish_at": "2020-06-06 14:09:39",
            "trans_property": None,
            "pre_interest": None,
            "commission_amt_interest": None,
            "grant_at": "2020-06-06 14:09:39",
            "push_at": "2020-06-06 12:09:37"
        },
        "trans": [
            {
                "asset_item_no": "{{item_no}}",
                "type": "repayinterest",
                "description": "偿还利息",
                "amount": 350,
                "decrease_amount": 0,
                "repaid_amount": 0,
                "balance_amount": 0,
                "total_amount": 350,
                "status": "nofinish",
                "due_at": "2020-06-13 00:00:00",
                "finish_at": "2020-06-06 00:00:00",
                "period": 1,
                "late_status": "normal",
                "remark": "",
                "repay_priority": 11,
                "trade_at": "2020-06-06 14:09:39",
                "category": "interest"
            },
            {
                "asset_item_no": "{{item_no}}",
                "type": "repayprincipal",
                "description": "偿还本金",
                "amount": 50000,
                "decrease_amount": 0,
                "repaid_amount": 0,
                "balance_amount": 0,
                "total_amount": 50000,
                "status": "nofinish",
                "due_at": "2020-06-13 00:00:00",
                "finish_at": "2020-06-06 00:00:00",
                "period": 1,
                "late_status": "normal",
                "remark": "",
                "repay_priority": 1,
                "trade_at": "2020-06-06 14:09:39",
                "category": "principal"
            }
        ],
        "borrower": {
            "borrower_uuid": "borrower_uuid_0000002",
            "id_num": "enc_02_2574411798044739584_650",
            "mobile": "enc_01_2574411798095071232_327",
            "borrower_card_uuid": "borrower_card_uuid_0000002",
            "individual_uuid": "individual_uuid_0000002"
        }
    },
    "from_system": "GBIZ"
}

BIZ_BASE_URL = {
    "china": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz{0}-api",
    "india": "{0}",
    "indonesia": "{0}",
    "thailand": "{0}",
    "philippines": "{0}",
    "mexico": "{0}"
}

GBIZ_BASE_URL = {
    "china": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/grant{0}",
    "india": "http://biz-gateway-proxy.starklotus.com/ind_grant{0}",
    "thailand": "http://biz-gateway-proxy.starklotus.com/tha_grant{0}",
    "philippines": "http://biz-gateway-proxy.starklotus.com/phl_grant{0}",
    "mexico": "http://biz-gateway-proxy.starklotus.com/mex_grant{0}"
}

RBIZ_BASE_URL = {
    "china": "https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/repay{0}",
    "india": "http://biz-gateway-proxy.starklotus.com/ind_repay{0}",
    "thailand": "http://biz-gateway-proxy.starklotus.com/tha_repay{0}",
    "philippines": "http://biz-gateway-proxy.starklotus.com/phl_repay{0}",
    "mexico": "http://biz-gateway-proxy.starklotus.com/mex_repay{0}"
}

# 通道查询接口的mock 参数
mock_query_protocol_channels_mode = {
    "code": 0,
    "message": "查询代扣可用通道成功",
    "data": [
        {
            "data": [
                {
                    "channel_name": "baofoo_tq4_protocol",
                    "product_type": "protocol",
                    "bind_status": "-1",
                    "protocol_info": "@id"
                }
            ],
            "sign_company": "tq"
        }
    ]
}

# 绑卡短信接口的mock 参数
mock_bind_sms_mode = {
    "code": 0,
    "message": "绑卡短信发送成功！",
    "data": {
        "verify_seq": "1235880123367493",
        "need_sms": 0
    }
}

# paysvr代扣接口的mock参数
mock_auto_pay_mode = {
    "code": 0,
    "message": "余额不足",
    "data": {
        "need_bind": 0,
        "need_sms": 0,
        "channel_code": "E30002",
        "channel_error": "余额不足",
        "channel_message": "余额不足",
        "channel_msg": "余额不足",
        "balance_not_enough": 0,
        "created_at": "@now",
        "finished_at": "@now",
        "withhold_receipt_list": [{
            "status": "1",
            "channel_code": "0000",
            "channel_message": "余额不足",
            "channel": "baidu_tq4_quick",
            "channel_key": "DSQ@id"
        }],
        "amount": "181412",
        "channel": "baidu_tq3_quick",
        "channel_key": "DSQ@id",
        "error_code": "E20000",
        "card_num": "6013823723467287491",
        "id_num": "110112198608156971",
        "username": "柳倩",
        "mobile": "15098440945"
    },
    "sign": "55902cb066f4285b85863c2951fa1463"
}

asset_import_source_type = "youxi_bill"

global_asset_import_info_loan_channel = {
    "type": "DSQAssetImport",
    "key": get_guid(),
    "from_system": "DSQ",
    "data": {
        "asset": {
            "item_no": "202002058828193443201569",
            "type": "paydayloan",
            "product_name": "",
            "period_type": "month",
            "period_count": 6,
            "period_day": "0",
            "repayment_type": "other",
            "amount": 1500,
            "loan_at": "1000-01-01 00:00:00",
            "loan_channel": "",
            "loan_usage": 1,
            "is_face_recognised": 1,
            "source_type": "",
            "source_number": "",
            "risk_level": "1",
            "hit_channel": "",
            "owner": "KN",
            "from_app": "草莓",
            "from_system": "DSQ",
            "from_system_name": "贷上钱",

        },
        "borrower": {
            "id_num": "enc_222",
            "borrower_uuid": "ABC111",
            "borrower_card_uuid": "BBB111",
            "mobile": "enc_456",
            "individual_uuid": "CCCC111",
        },
        "attachments": [],
        "risk_encrypted": "abc"
    }
}

global_asset_import_info_no_loan = {
    "type": "DSQAssetImport",
    "key": get_guid(),
    "from_system": "DSQ",
    "data": {
        "asset": {
            "item_no": "202002058828193443201569",
            "type": "paydayloan",
            "product_name": "",
            "period_type": "month",
            "period_count": 6,
            "period_day": "0",
            "repayment_type": "other",
            "amount": 1500,
            "loan_at": "1000-01-01 00:00:00",
            "loan_channel": "",
            "loan_usage": 1,
            "is_face_recognised": 1,
            "source_type": "",
            "source_number": "",
            "risk_level": "1",
            "hit_channel": "",
            "owner": "KN",
            "from_app": "草莓"
        },
        "borrower": {
            "id_num": "enc_222",
            "borrower_uuid": "ABC111",
            "borrower_card_uuid": "BBB111",
            "mobile": "enc_456"
        },
        "attachments": [

        ],
        "risk_encrypted": "abc"
    }
}

asset_grant = {
    "type": "AssetWithdrawSuccess",
    "key": get_guid(),
    "data": {
        "asset": {},
        "loan_record": {},
        "dtransactions": [],
        "fees": [],
        "cards_info": {
            "repay_card": {
            },
            "receive_card": {
            }
        }
    },
    "from_system": "BIZ"
}

capital_asset = {
    "channel": "weishenma_daxinganling",
    "status": "repay",
    "version": 0,
    "item_no": "S202012028927041375799764",
    "period_count": 12,
    "period_type": "month",
    "period_term": 1,
    "push_at": get_date(),
    "granted_at": get_date(),
    "due_at": "2021-12-01 00:00:00",
    "granted_amount": 1000000,
    "cmdb_no": "wsmdx_12_1m_20200824",
    "year_days": 360,
    "create_at": get_date(),
    "update_at": get_date(),
    "finish_at": "1000-01-01 00:00:00",
    "capital_transactions": []
}

refund_result = {
    "from_system": "Rbiz",
    # "key": get_guid()+10,
    "type": "refundSync",
    "data": {
        "status": "success",
        "channel": "skypay_copperstone_withdraw",
        "scene": "repeated_withhold",
        # "type": "rollback",
        "amount": 553500,
        "comment": "交易成功",
        "operator": "方昌芳",
        # "serial_no": "REFUND_5091830607353812121",
        # "withhold_serial_no": "AUTO_C509188320306855100",
        "trade_type": "online",
        "channel_key": "auto"+get_guid(),
        "finish_at": get_date(),
        "create_at": get_date(),
        "update_at": get_date()
    }
}
