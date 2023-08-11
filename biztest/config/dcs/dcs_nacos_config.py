import common.global_const as gc


def update_nacos_dcs_generic_deal(order_no):
    value = {
        "fail_order_no_list": [
            order_no
        ],
        "black_order_types": [

        ]
    }
    # gc.NACOS.update_configs("biz-dcs" + str(gc.ENV), "dcs_generic_deal", value, "KV")
    gc.NACOS.update_configs("biz-dcs1", "dcs_generic_deal", value, "KV")


def update_nacos_dcs_payment_cost_config(payment_channel="test", st_cost_rate="0.23",
                                          wh_cost_fee="100"):
    value = {
        payment_channel: {  # 默认归集没有成本
            "settlement_cost_rate": st_cost_rate,
            "withdraw_cost_single_fee": wh_cost_fee
        }
    }
    gc.NACOS.update_configs("biz-dcs1", "dcs_payment_cost_config", value, "KV")


def update_nacos_dcs_deposit_config(withhold_channel="qsq_sumpay_qjj_protocol"):
    value = {
        "zz_rongsheng": {
            "sync_info_flow": True,
            "hk_channel_code": "v_tengqiao_hk_zz_rongsheng",
            "support_payment_channel": [
                "qsq_cpcn_rs_quick",
                "qsq_sumpay_rs_protocol",
                "qsq_yeepay_rs_protocol",
                "qsq_sumpay_qjj_protocol",
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_2750897755970342912_407",
                "receiver_account": "enc_03_3486377530544884736_394",
                "receiver_identity": "enc_02_3019355097026529280_119",
                "receiver_bank_code": "ZAZBANK",
                "receiver_bank_branch": "枣庄银行股份有限公司",
                "receiver_bank_subbranch": "",
                "receiver_bank_province": "山东省",
                "receiver_bank_city": "枣庄市"
            }
        },
        "zz_tengqiao": {
            "sync_info_flow": True,
            "hk_channel_code": "v_tengqiao_hk_zz_tengqiao",
            "support_payment_channel": [
                "qsq_cpcn_tq_quick",
                "qsq_yeepay_tq1",
                "qsq_sumpay_tq_protocol",
                "qsq_baofoo_tq_protocol",
                "qsq_sumpay_qjj_protocol",
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_100922050_208",
                "receiver_account": "enc_03_3464548883970395136_384",
                "receiver_identity": "enc_02_100922100_769",
                "receiver_bank_code": "ZAZBANK",
                "receiver_bank_branch": "枣庄银行股份有限公司营业部",
                "receiver_bank_subbranch": "",
                "receiver_bank_province": "山东省",
                "receiver_bank_city": "枣庄市"
            }
        },
        "qs_tengqiao": {
            "sync_info_flow": True,
            "hk_channel_code": "v_tengqiao_hk_qs_tengqiao",
            "support_payment_channel": [
                "qsq_cpcn_tq_quick",
                "qsq_umf_tq_protocol",
                "qsq_yeepay_tq1",
                "qsq_sumpay_tq_protocol",
                "qsq_llpay_tq_protocol",
                "qsq_baofoo_tq_protocol",
                "qsq_sumpay_qjj_protocol",
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_100922050_208",
                "receiver_account": "enc_03_3004958793261385728_732",
                "receiver_identity": "enc_02_100922100_769",
                "receiver_bank_code": "QSBANK",
                "receiver_bank_branch": "齐商银行股份有限公司济南济阳支行",
                "receiver_bank_subbranch": "",
                "receiver_bank_province": "山东省",
                "receiver_bank_city": "淄博市"
            }
        },
        "jining": {
            "sync_info_flow": True,
            "hk_channel_code": "v_tengqiao_hf_hk_jining",
            "support_payment_channel": [
                "qsq_cpcn_tq_quick",
                "qsq_umf_tq_protocol",
                "qsq_yeepay_tq1",
                "qsq_sumpay_tq_protocol",
                "qsq_llpay_tq_protocol",
                "qsq_baofoo_tq_protocol",
                "qsq_sumpay_qjj_protocol",
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_29873061060_339",
                "receiver_account": "enc_03_3863069600_234",
                "receiver_identity": "enc_02_100922100_769",
                "receiver_bank_code": "JNBANK",
                "receiver_bank_branch": "济宁银行股份有限公司火炬路支行",
                "receiver_bank_subbranch": "",
                "receiver_bank_province": "山东省",
                "receiver_bank_city": "济宁市"
            }
        },
        "qs_qianjingjing": {
            "sync_info_flow": True,
            "hk_channel_code": "v_qjj_hk_qs_qianjingjing",
            "support_payment_channel": [
                withhold_channel,
                "qsq_cpcn_qjj_quick",
                "qsq_yeepay_qjj_protocol",
                "qsq_llpay_qjj_protocol",
                "qsq_baofoo_qjj_protocol",
                "qsq_sumpay_qjj_protocol",
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_101619080_478",
                "receiver_account": "enc_03_3163158347214490624_072",
                "receiver_identity": "enc_02_35650768940_632",
                "receiver_bank_code": "QSBANK",
                "receiver_bank_branch": "齐商银行股份有限公司济南济阳支行营业部",
                "receiver_bank_subbranch": "",
                "receiver_bank_province": "山东省",
                "receiver_bank_city": "济宁市"
            }
        },
        "qs_weidu": {
            "sync_info_flow": True,
            "hk_channel_code": "v_hefei_weidu_reserve_qs_weidu",
            "support_payment_channel": [
                "qsq_sumpay_wd_protocol",
                "qsq_sumpay_qjj_protocol",
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_952262030_254",
                "receiver_account": "enc_03_3601831711102995456_135",
                "receiver_identity": "enc_02_2693366056336495616_164",
                "receiver_bank_code": "QSBANK",
                "receiver_bank_branch": "齐商银行股份有限公司中心路支行",
                "receiver_bank_subbranch": "",
                "receiver_bank_province": "山东省",
                "receiver_bank_city": "济宁市"
            }
        },
        "ht_qianjingjing": {
            "sync_info_flow": False,
            "hk_channel_code": "v_qjj_hk_ht_qianjingjing",
            "support_payment_channel": [
                "qsq_sumpay_qjj_protocol",
                "qsq_cpcn_qjj_quick",
                "qsq_yeepay_qjj_protocol",
                "qsq_llpay_qjj_protocol",
                "qsq_baofoo_qjj_protocol",
                "qsq_sumpay_qjj_protocol",
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_101619080_478",
                "receiver_account": "enc_03_3798026279916668928_547",
                "receiver_identity": "enc_03_3858333327052769280_683",
                "receiver_bank_code": "ONEBANK",
                "receiver_bank_branch": "福建华通银行",
                "receiver_bank_subbranch": "福建华通银行股份有限公司",
                "receiver_bank_province": "福建省",
                "receiver_bank_city": "福州市"
            }
        },
        "ht_tengqiao": {
            "sync_info_flow": False,
            "hk_channel_code": "v_tengqiao_hk_ht_tengqiao",
            "support_payment_channel": [
                "qsq_cpcn_tq_quick",
                "qsq_yeepay_tq1",
                "qsq_sumpay_tq_protocol",
                "qsq_llpay_tq_protocol",
                "qsq_baofoo_tq_protocol",
                "qsq_baofu_4_baidu",
                "qsq_baidu_tq3_quick",
                withhold_channel,
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_100922050_208",
                "receiver_account": "enc_04_3881826410339764224_803",
                "receiver_identity": "enc_03_3858333327052769280_683",
                "receiver_bank_code": "ONEBANK",
                "receiver_bank_branch": "福建华通银行",
                "receiver_bank_subbranch": "福建华通银行股份有限公司",
                "receiver_bank_province": "福建省",
                "receiver_bank_city": "福州市"
            }
        },
        "qs_hange": {
            "sync_info_flow": True,
            "hk_channel_code": "v_qishanghange_02_qs_hange",
            "support_payment_channel": [
                "qsq_cpcn_tq_quick",
                "qsq_yeepay_tq1",
                "qsq_sumpay_tq_protocol",
                "qsq_llpay_tq_protocol",
                "qsq_baofoo_tq_protocol",
                "qsq_sumpay_qjj_protocol",
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_100922050_208",
                "receiver_account": "enc_04_3881826410339764224_803",
                "receiver_identity": "enc_03_3858333327052769280_683",
                "receiver_bank_code": "ONEBANK",
                "receiver_bank_branch": "福建华通银行",
                "receiver_bank_subbranch": "福建华通银行股份有限公司",
                "receiver_bank_province": "福建省",
                "receiver_bank_city": "福州市"
            }
        },
        "ht_hange": {
            "sync_info_flow": False,
            "hk_channel_code": "v_qishanghange_02_qs_hange",
            "support_payment_channel": [
                "qsq_cpcn_tq_quick",
                "qsq_yeepay_tq1",
                "qsq_sumpay_tq_protocol",
                "qsq_llpay_tq_protocol",
                "qsq_baofoo_tq_protocol",
                "qsq_sumpay_qjj_protocol",
                "qsq_yeepay_hange_protocol"
            ],
            "deposit_info": {
                "receiver_type": 2,
                "receiver_name": "enc_04_100922050_208",
                "receiver_account": "enc_04_3881826410339764224_803",
                "receiver_identity": "enc_03_3858333327052769280_683",
                "receiver_bank_code": "ONEBANK",
                "receiver_bank_branch": "福建华通银行",
                "receiver_bank_subbranch": "福建华通银行股份有限公司",
                "receiver_bank_province": "福建省",
                "receiver_bank_city": "福州市"
            }
        }
    }
    gc.NACOS.update_configs("biz-dcs1", "dcs_deposit_config", value, "KV")


def update_nacos_dcs_collect_rule():
    value = {
        "rules": [
            {
                "name": "大单-部分外部资方、历史资方归集至齐商腾桥",
                "priority": 50,
                "conditions": [
                    {
                        "paramName": "type",
                        "paramType": "String",
                        "value": "B",
                        "valueType": "String",
                        "operation": "eq"
                    },
                    {
                        "paramName": "loanChannel",
                        "paramType": "String",
                        "value": [
                            "shilong_siping",
                            "qinnong_jieyi",
                            "weishenma_daxinganling",
                            "qinnong",
                            "mozhi_beiyin_zhongyi",
                            "beiyin_tianbang",
                            "lanzhou_haoyue",
                            "hengfeng",
                            "hami_tianshan",
                            "yixin_huimin",
                            "yunxin_quanhu",
                            "huabeixiaodai_zhitou",
                            "shoujin",
                            "wsm",
                            "hainan",
                            "qnn",
                            "mindai",
                            "xingchenzx",
                            "lianlian",
                            "baijin",
                            "zhenjinfu",
                            "xingruinew"
                        ],
                        "valueType": "List",
                        "operation": "in"
                    }
                ],
                "result": {
                    "deposit": "qs_tengqiao"
                }
            },
            {
                "name": "大单-自有资方归集至齐商钱京京",
                "priority": 50,
                "conditions": [
                    {
                        "paramName": "type",
                        "paramType": "String",
                        "value": "B",
                        "valueType": "String",
                        "operation": "eq"
                    },
                    {
                        "paramName": "loanChannel",
                        "paramType": "String",
                        "value": "$ownerLoanChannel",
                        "valueType": "List",
                        "operation": "in"
                    }
                ],
                "result": {
                    "deposit": "qs_qianjingjing"
                }
            },
            {
                "name": "大单--归集至华通腾桥",
                "priority": 40,
                "conditions": [
                    {
                        "paramName": "type",
                        "paramType": "String",
                        "value": "B",
                        "valueType": "String",
                        "operation": "eq"
                    },
                    {
                        "paramName": "loanChannel",
                        "paramType": "String",
                        "value": "$ownerLoanChannel",
                        "valueType": "List",
                        "operation": "notIn"
                    }
                ],
                "result": {
                    "deposit": "ht_tengqiao"
                }
            },
            {
                "name": "小单-资产持有者如皋智萃、扬州锌旺归集至齐商钱京京",
                "priority": 40,
                "conditions": [
                    {
                        "paramName": "type",
                        "paramType": "String",
                        "value": "P",
                        "valueType": "String",
                        "operation": "eq"
                    },
                    {
                        "paramName": "part",
                        "paramType": "String",
                        "value": [
                            "如皋智萃",
                            "扬州锌旺",
                            "杭州犇瀛"
                        ],
                        "valueType": "List",
                        "operation": "in"
                    }
                ],
                "result": {
                    "deposit": "qs_qianjingjing"
                }
            },
            {
                "name": "小单-亲家亿联归集至齐商钱京京",
                "priority": 50,
                "conditions": [
                    {
                        "paramName": "type",
                        "paramType": "String",
                        "value": "P",
                        "valueType": "String",
                        "operation": "eq"
                    },
                    {
                        "paramName": "loanChannel",
                        "paramType": "String",
                        "value": [
                            "yilian_dingfeng"
                        ],
                        "valueType": "List",
                        "operation": "in"
                    }
                ],
                "result": {
                    "deposit": "qs_qianjingjing"
                }
            },
            {
                "name": "小单-资产持有者苏州归集至齐商腾桥",
                "priority": 40,
                "conditions": [
                    {
                        "paramName": "type",
                        "paramType": "String",
                        "value": "P",
                        "valueType": "String",
                        "operation": "eq"
                    },
                    {
                        "paramName": "part",
                        "paramType": "String",
                        "value": [
                            "苏州",
                            "乾昭",
                            "云桥",
                            "云智",
                            "醉梦者"
                        ],
                        "valueType": "List",
                        "operation": "in"
                    }
                ],
                "result": {
                    "deposit": "ht_tengqiao"
                }
            },
            {
                "name": "历史第三单-归集至济宁腾桥",
                "priority": 40,
                "conditions": [
                    {
                        "paramName": "type",
                        "paramType": "String",
                        "value": "T",
                        "valueType": "String",
                        "operation": "eq"
                    }
                ],
                "result": {
                    "deposit": "ht_tengqiao"
                }
            }
        ],
        "conditionValues": {
            "$ownerLoanChannel": [
                "tongrongmiyang",
                "duolaidianmiyang",
                "duolaidianmiyangnew",
                "longshangmiyang",
                "tongrongqianjingjing",
                "haohanqianjingjing"
            ]
        }
    }
    gc.NACOS.update_configs("biz-dcs1", "dcs_collect_rule", value, "KV")
