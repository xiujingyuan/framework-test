from biztest.util.tools.tools import get_guid, get_date, get_guid4

gbiz_monitor_check_url = "/monitor/check"
gbiz_asset_import_url = "/paydayloan/asset-sync-new"
biz_asset_import_url = "/central/asset-sync"
gbiz_asset_route_url = "/asset/loan-channel-new"
gbiz_asset_route_url_new = "/router/v1/locate"
gbiz_capital_withdraw_url = "/capital/withdraw-new"
gbiz_capital_regiest_url = "/account/register-account"
gbiz_capital_regiest_url_query_url = "/account/register-query"
gbiz_get_sms_verifycode_url = "/capital/get-sms-verifycode-new"
gbiz_preloan_confirm_url = "/capital/preloan-confirm-new"
gbiz_postloan_confirm_url = "/capital/postloan-confirm-new"
gbiz_userloan_confirm_url = "/paydayloan/user-loan-confirm"
gbiz_update_card_url = "/paydayloan/update-receive-card"
gbiz_withdraw_url = '/capital/withdraw'
gbiz_withdraw_query_url = '/capital/withdraw-result'
lianlian_callback_url = '/lianlian/callback'
reverse_callback_url = '/asset/reverse'
huabei_audit_callback_url = '/capital/callback/audit/huabei_runqian'
huabei_grant_callback_url = '/capital/callback/grant/huabei_runqian'
hamitianshan_callback_url = '/zhongji/callback/ASSET_HANDLE_NOTIFY'
yxrs_reverse_callback = '/capital/callback/reverse/yixin_rongsheng'
dxal_zy_grant_callback = '/capital/callback/Grant/daxinganling_zhongyi'
data_cancel_url = '/data/cancel'
certificate_apply_url = '/attachment/certificate-apply'
circuit_break_update_url = '/circuitBreak/update'
payment_callback_url = '/payment/callback'

hamitianshan_callback_info = {
    "loanRequestNo": "S202006053391316293433351",
    "imgData": {
        "1FDB": "http://cashtest-1251122539.cossh.myqcloud.com/20190528/5ceca12836d8015590116244662.jpe"
    }
}

yixin_rongsheng_callback_info = {
    "from_system": "biz-gateway",
    "key": get_guid(),
    "type": "YixinRongshengCallback",
    "data": "{\"applyStatus\":\"LEND_FAILED\",\"msg\":\"银行退票，放款失败\",\"outOrderNo\":\"20221661483276871609\",\"userId\":\"KN_enc_02_4086019665292691456_804\"}"
}

daxinganling_zhongyi_callback_info = {
    "from_system": "gate",
    "key": get_guid4(),
    "type": "GrantCallback",
    "data": "{\"loanBankWholeName\":\"大兴安岭农村商业银行股份有限公司\",\"repayPlan\":[{\"amount\":86296,\"period\":1,\"interest\":5417,\"principal\":80879,\"repayDate\":\"2023-02-12\"},{\"amount\":86296,\"period\":2,\"interest\":4979,\"principal\":81317,\"repayDate\":\"2023-03-12\"},{\"amount\":86296,\"period\":3,\"interest\":4538,\"principal\":81758,\"repayDate\":\"2023-04-12\"},{\"amount\":86296,\"period\":4,\"interest\":4095,\"principal\":82201,\"repayDate\":\"2023-05-12\"},{\"amount\":86296,\"period\":5,\"interest\":3650,\"principal\":82646,\"repayDate\":\"2023-06-12\"},{\"amount\":86296,\"period\":6,\"interest\":3202,\"principal\":83094,\"repayDate\":\"2023-07-12\"},{\"amount\":86296,\"period\":7,\"interest\":2752,\"principal\":83544,\"repayDate\":\"2023-08-12\"},{\"amount\":86296,\"period\":8,\"interest\":2300,\"principal\":83996,\"repayDate\":\"2023-09-12\"},{\"amount\":86296,\"period\":9,\"interest\":1845,\"principal\":84451,\"repayDate\":\"2023-10-12\"},{\"amount\":86296,\"period\":10,\"interest\":1387,\"principal\":84909,\"repayDate\":\"2023-11-12\"},{\"amount\":86296,\"period\":11,\"interest\":927,\"principal\":85369,\"repayDate\":\"2023-12-12\"},{\"amount\":86285,\"period\":12,\"interest\":449,\"principal\":85836,\"repayDate\":\"2024-01-10\"}],\"loanBillingDate\":\"2023-01-12\",\"accountingDate\":\"2023-01-11\",\"contractNo\":\"W2022041673436059\",\"contractPreviewUrl\":\"https://testsignapi.wsmtec.com/platform/api/home/fileinfo/get?code=2020230111054595-41d926ae2fec48bff67e55fd93040c5c&contractNo=2020230111054595&handle=redirect\",\"sign\":\"6aecade114e1adfa1f4bb3bd5c1861df\",\"contractDownloadUrl\":\"https://testsignapi.wsmtec.com/platform/api/home/fileinfo/get?code=2020230111054595-41d926ae2fec48bff67e55fd93040c5c&contractNo=2020230111054595\",\"merchantOrderNo\":\"W2022041673436059\",\"assetNotifyUrl\":\"http://biz-gateway-api.k8s-ingress-nginx.kuainiujinke.com/pub-daxinganling-zhongyi/grant/callback\",\"billingDate\":\"2023-01-12\",\"contractSignedDate\":\"2023-01-11\",\"loanDate\":\"2023-01-11\",\"state\":\"success\",\"loanRate\":0.065,\"totalInterest\":35541}"
}
daxinganling_zhongyi_callback_info2 = {
    "from_system": "gate",
    "key": get_date(fmt="%Y%m%d%H%M%S"),
    "type": "GrantCallback",
    "data": "{\"assetNotifyUrl\":\"http://biz-gateway-api.k8s-ingress-nginx.kuainiujinke.com/pub-daxinganling-zhongyi/grant/callback\",\"sign\":\"a9b557c554c9846b363496abd246cb93\",\"errorCode\":\"4041\",\"state\":\"error\",\"merchantOrderNo\":\"W2022041673433267\",\"errorMsg\":\"交易失败\"}"
}

GLOBAL_GBIZ_SYNC_ASSET_FROM_GRANT = '/sync/asset/from-grant'
GLOBAL_GBIZ_ASSET_IMPORT_URL = '/paydayloan/asset-sync'
# GLOBAL_GBIZ_AUTO_GRANT_URL = 'http://testing-framework.kuainiu.io/gbiz-loan-to-success'
GLOBAL_GBIZ_AUTO_GRANT_URL = '/gbiz-loan-to-success'
lianlian_callback_info = {
    "loanId": 5001324170,
    "memberId": 21149885,
    "amount": "10000.00",
    "reversalAt": "2020-05-09 12:12:12",
    "eventType": "WithdrawReversal",
    "messageType": "Event",
    "timestamp": 0,
    "sign": "3fe486c7136d48084b217691bc3ce091"
}

reverse_callback_info = {
    "type": "AssetReverse",
    "key": "ZZ_reverse_{{$guid}}",
    "from_system": "BIZ",
    "data": [
        "ZZ_sj_0512_6qi3734loan"
    ]
}

huabei_grant_callback_info = {
    "from_system": "gate",
    "key": get_guid(),
    "type": "GrantCallback",
    "data": "{\"approvalCode\":\"01\",\"doLoanList\":[{\"businessNum\":\"2021HYXJ6967\",\"contractTotalAmt\":10000.0,\"pnlItr\":0.1,\"customerNum\":\"A01P22111546845\",\"orderNum\":\"ph_hbrq_4814871311\",\"coopGuestName\":\"kuainiu\",\"customerName\":\"enc_04_4889080_987\",\"productName\":\"快牛-敞口消费分期业务\",\"cusNum\":\"enc_02_3696385023554357248_309\",\"rateYear\":13.0,\"dueNum\":\"2021HYXJ6967\",\"contractSignDate\":\"2022-11-15\",\"loanDate\":\"2022-11-15 00:00:00\",\"repayDate\":\"\",\"padUpAmt\":10000.0,\"certificateNum\":\"enc_02_3685925260605523968_274\",\"startDate\":\"2022-11-15\",\"certificateType\":\"1\",\"channelCode\":\"kuainiu\",\"expirationDate\":\"2023-11-15\"}]}"
}

huabei_audit_callback_info = {
    "from_system": "gate",
    "key": get_guid(),
    "type": "AuditCallback",
    "data": "{\"cusNum\":\"enc_02_3696385023554357248_309\",\"businessNum\":\"2021HYXJ6966\",\"approvalCode\":\"01\",\"customerNum\":\"A01P22111546845\",\"orderNum\":\"ph_hbrq_4625262693\",\"customerName\":\"enc_04_4889080_987\",\"approvalOpinion\":\"审批通过\"}"
}

regiest_info = {
    "from_system": "strawberry",
    "key": get_guid(),
    "type": "GetSmsVerifyCode",
    "data": {
        "channel": "zhongke_lanzhou",
        "way": "zhongke_lanzhou",
        "item_no": "S2021041396727970800",
        "step_type": "PROTOCOL",
        "action_type": "GetSmsVerifyCode",
        "mobile_encrypt": "enc_01_4881910_819",
        "id_num_encrypt": "enc_02_3351131557460445184_382",
        "username_encrypt": "enc_04_3351131557225564160_029",
        "card_num_encrypt": "enc_03_3361465936304932864_074",
        "extend": {
            "bank_code": "CCB",
            "code": "123456",
            "seq": "169844856220549120"
        }
    }
}

regiest_query_info = {
    "from_system": "strawberry",
    "key": get_guid(),
    "type": "AccountRegisterQuery",
    "data": {
        "channel": "zhongke_lanzhou",
        "item_no": "S2021041381497152883",
        "id_num_encrypt": "enc_02_3351131557460445184_382",
        "card_num_encrypt": "enc_03_3361210580014204928_250",
        "mobile_encrypt": "enc_01_4881910_819",
        "username_encrypt": "enc_04_3351131557225564160_029"
    }
}

get_sms_verifycode_info = {
    "key": get_guid(),
    "from_system": "DSQ",
    "type": "GetSmsVerifyCode",
    "data": {
        "item_no": "",
        "channel": "",
        "source_type": "",
        "mobile_encrypt": "",
        "id_num_encrypt": "",
        "username_encrypt": "",
        "card_num_encrypt": "",
        "bank_code": "COMM"
    }
}

preloan_confirm_info = {
    "from_system": "DSQ",
    "key": get_guid(),
    "type": "PreLoanConfirm",
    "data": {
        "item_no": "",
        "user_factor": {
            "mobile_encrypt": "enc_01_5551500_392",
            "id_num_encrypt": "enc_02_5551470_824",
            "user_name_encrypt": "enc_04_5551490_974",
            "card_num_encrypt": "enc_04_5551490_974",
            "bank_code": "ICBC"
        },
        "asset_extend": {
            "amount": "",
            "channel": "",
            "industry": 1,
            "grant_at": get_date(),
            "loan_usage": 1,
            "period_type": 0,
            "period_term": 30,
            "payment_source": 1
        },
        "action_type": "PreLoanConfirm",
        "device_type": "ios",
        "return_url": "http://paydayloanliying.testing2.kuainiujinke.com/vue/*****"
    }
}
postloan_confirm_info = {
    "from_system": "DSQ",
    "key": get_guid(),
    "type": "PostLoanConfirm",
    "data": {
        "item_no": "",
        "user_factor": {
            "mobile_encrypt": "enc_01_5551500_392",
            "id_num_encrypt": "enc_02_5551470_824",
            "user_name_encrypt": "enc_04_5551490_974",
            "card_num_encrypt": "enc_04_5551490_974"
        },
        "asset_extend": {
            "amount": "",
            "channel": "",
            "industry": 1,
            "grant_at": get_date(),
            "loan_usage": 1,
            "period_type": 0,
            "period_term": 30,
            "payment_source": 1
        },
        "action_type": "PostLoanConfirm",
        "device_type": "ios",
        "return_url": "http://paydayloanliying.testing2.kuainiujinke.com/vue/*****"
    }
}

userloan_confirm_info = {
    "from_system": "strawberry",
    "key": get_guid(),
    "type": "UserLoanConfirm",
    "data": {
        "action": "CONFIRM_LOAN_AMOUNT",
        "status": 0,
        "message": "确认提额",
        "asset": {
            "amount": 1000000,
            "channel": "qinnong"
        },
        "extra_data": {
            "sub_action": "SendSmsCode",
            "confirm_code": "665815"
        },
        "item_no": "ph_qn_0218949075"
    }
}

update_receive_card_info = {
    "from_system": "DSQ",
    "key": get_guid(),
    "type": "UpdateCard",
    "data": {
        "card_bank_code": "ICBC",
        "card_bank": "中国工商银行",
        "card_num_encrypt": "",
        "project_num": "",
        "card_account_name_encrypt": "",
        "operater": "dsq",
        "card_phone_encrypt": ""
    }
}

withdraw_info = {
    "from_system": "DSQ",
    "key": get_guid(),
    "type": "WithdrawToCard",
    "data": {
        "item_no": "",
        "return_url": "http://balabaa.com",
        "callback_url": "http://balabaa.com",
        "device_type": "iOS"
    }
}

withdraw_query_info = {
    "from_system": "DSQ",
    "key": get_guid(),
    "type": "WithdrawToCardResult",
    "data": {
        "item_no": ""
    }
}

asset_import_info = {
    "type": "BCAssetImport",
    "key": get_guid(),
    "from_system": "DSQ",
    "data": {
        "route_uuid": "",
        "asset": {
            "item_no": "",
            "type": "paydayloan",
            "name": "name_#{item_no}",
            "product_name": "",
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
            "province": "上海",
            "city": "上海市",
            "province_district_code": "310000",
            "city_district_code": "310000",
            "due_at": "",
            "first_payat": "",
            "payoff_at": "",
            "grant_at": "#{system_date}",
            "secure_amount": 0,
            "manage_amount": 0,
            "sign_at": "1000-01-01 00:00:00",
            "interest_amount": "",
            "sub_type": "multiple",
            "loan_channel": "",
            "channel_verification_code": "",
            "cmdb_product_number": "",
            "decrease_amount": "",
            "loan_usage": "1",
            "charge_type": 1,
            "is_face_recognised": 1,
            "source_type": "youxi_bill",
            "source_number": "manaowan_#{item_no}_noloan",
            "withholding_amount": 0,
            "sub_order_type": "rongdan_tianbang",
            "risk_level": 2,
            "hit_channel": "",
            "from_system": "",
            "from_app": ""
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
            #"residence": "陕西省白水县北塬乡潘村二社",
            "residence": "上海上海市闵行区滨浦新苑二村38号楼38单元601",
            "workplace": "山东省胶州市铺集镇吴家庄村45号",
            "corp_name": "利郎男装专卖",
            "corp_tel_encrypt": "",
            "relative_name_encrypt": "enc_04_799640_910",  # 正常联系人姓名
            #"relative_name_encrypt": "enc_04_3497844152073717760_674",  # 特殊字符联系人姓名
            "relative_tel_encrypt": "enc_01_895870_745",
            "relative_relation": 1,
            "second_relative_name_encrypt": "enc_04_799660_386",
            "second_relative_tel_encrypt": "enc_01_799670_679",
            "second_relative_relation": 6,
            "school_name": "",
            "school_place": "",
            "enrollment_time": "",
            "marriage": 1,
            "education": 4,
            "corp_trade": 10,
            "duty": 3,
            "id_addr": "山东省胶州市铺集镇吴家庄村46号",
            "nation": "汉",
            "income": "3001-5000",
            #"income": "10000-0",
            "email": "13797103222@139.com",
            "email_encrypt": "enc_05_3526762867259344896_719",
            "payment_source": "",
            "career_type": "1",
            "idnum_begin_day": "2020-03-04",
            "idnum_expire_day": "2040-03-04",
            "idnum_cert_office": "安陆市公安局"
        },
        "borrower_extend": {
            "work_case": "",
            "income_source": "",
            "debt_case": "",
            "repay_guarantee": "",
            "other_netloan_case": "",
            "other_finance_case": "",
            "credit_report_info": "",
            "use_case": "",
            "borrower_repayment": "",
            "complain_case": "",
            "punishment_case": "",
            "agreement": "Y",
            "idnum_begin_day": "2020-09-24",
            "idnum_expire_day": "2030-09-24",
            #"idnum_expire_day": "长期",
            "idnum_cert_office": "黄浦区公安局",
            "address_district_code": "310101",
            "residence_district": "黄浦区",
            "device_ip": "192.168.1.109",
            "device_mac": "00:fdaf:fdas:00",
            "longitude": "114.321541",
            "latitude": "30.587309",
            "device_sys": "iOS",
            "a_card_level_score": "888",
            "ip_province_district_code": "",
            "ip_city_district_code": "",
            "face_recog_score": "99",
            "contract_redirect_url": "https://www.baidu.com/",
            "device_id": "1234",
            "device_network_type": "5G"
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
            "residence": "山东省胶州市铺集镇吴家庄村45号",
            "workplace": "山东省胶州市铺集镇吴家庄村45号",
            "corp_name": "利郎男装专卖",
            "corp_tel_encrypt": "",
            "relative_name_encrypt": "enc_04_799640_910",
            "relative_tel_encrypt": "enc_01_895870_745",
            "relative_relation": 1,
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
            "email_encrypt": "enc_05_3526762867259344896_719",
            "payment_source": "",
            "career_type": "1",
            "idnum_expire_day": "2028-03-04",
            "idnum_begin_day": "2008-03-04",
            "idnum_cert_office": "安陆市公安局"
        },
        "repay_card": {
            "bankname": "中国建设银行",
            "bank_code": "CCB",
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
            "bank_code": "CCB",
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
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/2022/04/19/0419_193132_395efae7-8652-4834-ae36-5406d31380c8.jpg",
                "attachment_upload_at": "2018-12-23 14:38:37",
                "attachment_quality_score": "19"
            },
            {
                "attachment_type": 2,
                "attachment_type_text": "身份证反面照片",
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/2022/04/19/0419_193139_1d176523-25cd-4541-8477-c85d64771cd6.jpg",
                "attachment_upload_at": "2018-12-23 14:38:37",
                "attachment_quality_score": "23"
            },
            {
                "attachment_type": 29,
                "attachment_type_text": "活体识别照片",
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/2022-04-19/16503679565C70V7DBX6aV6XLLZvqdnf.png",
                #"attachment_url": "https://bizfiles-10000035.cossh.myqcloud.com/zztest7M.jpeg",
                "attachment_upload_at": "2019-11-13 10:18:57",
                "attachment_quality_score": 48
            }
        ],
        "risk_encrypted": "af8d036c149b0a6191d147f53f1116b819a522280b34d2e903a67e93bcdea2c7f2a047b5c53c80f4690bc04aa517c1b9578ae0f5f85d163d756d1c7e28c919af229f527f3741f6efde5a6d48d270977cc29bdd824eca5b04ddb7951f51d941a5dca59c256b65391f01e6e82e1fd50e6dc4cc3485db5e10dc775a8ee6e5f6cc879f3020b22f13c2bba753c5f8180b37c84a5f299d3fa871f8e1697617ca2d11098b6199e7f0578feab12d0faaa80333bb54b84dc8f679d8c74a66c25173bd4acac7b53dde3bff716e821343ecc183bc9aabaf0c50e7ce5c3de1fa4b55fd6eaeb92c371ed405f412c94c2dfef60557910189bfed1fb8c490569641d46ee45653fa0ce52319375f111a106b23054a62594ce9e5de553f987d499d0f98849fd5c7e29bf73fb027911f506ff9630d1484f64a570ae893d8634c38b534d6948420d284f1b341aee109f16386f5f53207c07c06c8f35d529e3705c5448db73d885f38ced92f327880a2e9dfc878059a1c2967938fce55589e5220a50e7b92346ef8d572",
         "asset_extend": {
          "distribute_type": 1,
           "sub_asset": {
                        "amount": 8000,
                        "period_type": "month",
                        "period_count": 6,
                        "period_day": 0
                      }
         }
    }
}

asset_route_info = {
    "type": "DSQAssetImport",
    "key": get_guid(),
    "from_system": "DSQ",
    "data": {
        "asset": {
            "item_no": "",
            "type": "paydayloan",
            "name": "",
            "product_name": "",
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
            "province": "山东省",
            "city": "青岛市",
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
            "loan_channel": "",
            "channel_verification_code": "",
            "cmdb_product_number": "",
            "decrease_amount": "",
            "loan_usage": "1",
            "charge_type": 1,
            "is_face_recognised": 1,
            "source_type": "youxi_bill",
            "source_number": "",
            "withholding_amount": 0,
            "sub_order_type": "",
            "risk_level": 2,
            "hit_channel": "",
            "from_system_name": "",
            "from_app": ""
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
            "residence": "山东省胶州市铺集镇吴家庄村45号",
            "workplace": "山东省胶州市铺集镇吴家庄村45号",
            "corp_name": "利郎男装专卖",
            "corp_tel_encrypt": "",
            "relative_name_encrypt": "enc_04_799640_910",
            "relative_tel_encrypt": "enc_01_895870_745",
            "relative_relation": 1,
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
            "id_addr": "甘肃省天水市秦州区岷玉路罗玉小区市31幢3单元501室",
            "nation": "汉",
            "income": "50001-80000",
            "email": "13797103222@139.com",
            "payment_source": "",
            "career_type": "1",
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
            "residence": "山东省胶州市铺集镇吴家庄村45号",
            "workplace": "山东省胶州市铺集镇吴家庄村45号",
            "corp_name": "利郎男装专卖",
            "corp_tel_encrypt": "",
            "relative_name_encrypt": "enc_04_799640_910",
            "relative_tel_encrypt": "enc_01_895870_745",
            "relative_relation": 1,
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
            "id_addr": "甘肃省天水市秦州区岷玉路罗玉小区市31幢3单元501室",
            "nation": "汉",
            "income": "5001-8000",
            "email": "13797103222@139.com",
            "payment_source": "",
            "career_type": "1",
            "idnum_expire_day": "2028-03-04",
            "idnum_begin_day": "2008-03-04",
            "idnum_cert_office": "安陆市公安局"
        },
        "repay_card": {
            "bankname": "中国工商银行",
            "bank_code": "icbc",
            "username_encrypt": "enc_04_1723850_411",
            "phone_encrypt": "enc_01_1723870_533",
            "individual_idnum_encrypt": "enc_02_1723860_422",
            "credentials_type": "0",
            "credentials_num_encrypt": "enc_02_1723860_422",
            "account_type": "debit",
            "account_num_encrypt": "enc_03_1723840_984"
        },
        "receive_card": {
            "name": "中国工商银行",
            "num_encrypt": "enc_03_1723840_984",
            "bank": "中国工商银行",
            "bank_code": "icbc",
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
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/2018/11/09/1109_164248_4cc84186-e859-4332-abe5-51f13799583e.jpg",
                "attachment_upload_at": "2018-12-23 14:38:37",
                "attachment_quality_score": "19"
            },
            {
                "attachment_type": 2,
                "attachment_type_text": "身份证反面照片",
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/2018/11/09/1109_164248_4cc84186-e859-4332-abe5-51f13799583e.jpg",
                "attachment_upload_at": "2018-12-23 14:38:37",
                "attachment_quality_score": "23"
            },
            {
                "attachment_type": 29,
                "attachment_type_text": "活体识别照片",
                "attachment_url": "http://cashtest-1251122539.cossh.myqcloud.com/2018/11/09/1109_164248_4cc84186-e859-4332-abe5-51f13799583e.jpg",
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
            "idnum_cert_office": "安陆市公安局",
            "residence_district": "胶州市",
            "face_recog_score": "99"
        },
        "asset_extend": {
            "distribute_type": 1,
            "sub_asset": {
                "amount": 10000,
                "period_type": "month",
                "period_count": 6,
                "period_day": 0
            }
        }
    }
}


change_product_confirm_info = {
    "from_system": "strawberry",
    "key": "key",
    "type": "UserLoanConfirm",
    "data": {
        "item_no": "ZZ12_YX07125257",
        "action": "LOAN_PRODUCT_CHANGE",
        "channel": "yixin_hengrun",
        "status": 0,
        "asset": {
            "amount": "1500000",
            "period_type": "month",
            "period_day": 0,
            "period_count": 6
        }
    }}
