#!/usr/bin/python
# -*- coding: UTF-8 -*-
import common.global_const as gc


def update_contract_sign_config():
    content = {
        "from_app_white_list": ["香蕉", "草莓", "重庆草莓", "火龙果", "杭州草莓"],
        "immediate_sign_contract_type_list": [
            20760,
            20761,
            20762,
            20763,
            20764,
            20765,
            20766
        ],
        "credit_agency_contract_type_list":  {
            "zhongyi": [
                20760,
                20761
            ],
            "huarong": [
                20762,
                20763,
                20764
            ],
            "guohuai": [
                20765,
                20766
            ]
        },
        "allocate_benefit_contract_type_list": {
            "rongdan": [
                20711
            ],
            "quanyi": [
                20716
            ]
        },
        "no_seal_contract_temp_path": {
            "LongJiangRepayPlan6": "/template/LongJiangRepayPlanTemp6.pdf",
            "LongJiangRepayPlan12": "/template/LongJiangRepayPlanTemp12.pdf",
            "HanchenFinancialInfoAuth": "/template/HanchenFinancialInfoAuth.pdf"
        },
        "contract_default_value": {
            "service_amount_b3_day": [
                {
                    "default_value": 50,
                    "start_at": "2018-01-01 00:00:00",
                    "end_at": "2020-10-31 23:59:59"
                },
                {
                    "default_value": 40,
                    "start_at": "2020-11-01 00:00:00",
                    "end_at": "2021-06-30 23:59:59"
                },
                {
                    "default_value": 60,
                    "start_at": "2021-07-01 00:00:00",
                    "end_at": "2021-08-31 23:59:59"
                },
                {
                    "default_value": 110,
                    "start_at": "2021-09-01 00:00:00",
                    "end_at": "2022-05-31 23:59:59"
                },
                {
                    "default_value": 120,
                    "start_at": "2022-06-01 00:00:00",
                    "end_at": "2022-10-31 23:59:59"
                },
                {
                    "default_value": 90,
                    "start_at": "2022-11-01 00:00:00",
                    "end_at": "2029-12-31 23:59:59"
                }
            ]
        }
    }
    return gc.NACOS.update_configs("contract%s" % gc.ENV, "contract_sign_config", content)


def update_contract_capital_config():
    content = {
              "huabeixiaodai_zhitou": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#item_no#",
                  "guarantee_sign": "sign_auto_shzhuaqi",
                  "guarantee_company": "深圳市花旗融资担保集团有限公司"
                }
              },
              "weishenma_daxinganling": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#item_no#",
                  "guarantee_sign": "sign_auto_shzhzhongyi",
                  "guarantee_company": "深圳市中裔信息工程融资担保有限公司"
                }
              },
              "qinnong": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "KN#item_no#",
                  "guarantee_sign": "sign_auto_shxtianbang",
                  "guarantee_company": "陕西天邦融资担保有限公司"
                }
              },
              "qinnong_jieyi": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "KN#item_no#",
                  "guarantee_sign": "sign_auto_shxjieyi",
                  "guarantee_company": "陕西杰益融资担保有限公司"
                }
              },
              "qinnong_dingfeng": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "KN#item_no#",
                  "guarantee_sign": "sign_auto_yndingfeng",
                  "guarantee_company": "云南鼎丰融资担保有限公司"
                }
              },
              "yunxin_quanhu": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "【云信信2019-969-DK（ #item_no# ）】",
                  "guarantee_sign": "sign_auto_shxtianbang",
                  "guarantee_company": "陕西天邦融资担保有限公司"
                }
              },
              "shilong_siping": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "四平市城区农村信用合作联社个网贷借字第【#item_no#】",
                  "guarantee_sign": "sign_auto_shzhuaqi",
                  "guarantee_company": "深圳市花旗融资担保集团有限公司"
                }
              },
              "zhongke_lanzhou": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#item_no#",
                  "guarantee_sign": "sign_auto_hljdingsheng",
                  "guarantee_company": "黑龙江鼎盛融资担保有限公司"
                }
              },
              "lanzhou_dingsheng_zkbc2": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#item_no#",
                  "guarantee_sign": "sign_auto_hljdingsheng",
                  "guarantee_company": "黑龙江鼎盛融资担保有限公司"
                }
              },
              "lanzhou_haoyue": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#item_no#",
                  "guarantee_sign": "sign_auto_sxhaoyue",
                  "guarantee_company": "陕西昊悦融资担保有限公司"
                }
              },
              "hami_tianshan_tianbang": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#contract_code#",
                  "loan_contact_type": 30181,
                  "guarantee_sign": "sign_auto_shxtianbang",
                  "guarantee_company": "陕西天邦融资担保有限公司"
                }
              },
              "hamitianbang_xinjiang": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#contract_code#",
                  "loan_contact_type": 30181,
                  "guarantee_sign": "sign_auto_shxtianbang",
                  "guarantee_company": "陕西天邦融资担保有限公司"
                }
              },
              "huabei_runqian": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#item_no#",
                  "guarantee_sign": "sign_auto_shzhrunqian",
                  "guarantee_company": "深圳市润乾融资担保有限公司"
                }
              },
              "longjiang_daqin": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#item_no#",
                  "guarantee_sign": "sign_auto_shxdqsilu",
                  "guarantee_company": "陕西大秦丝路融资担保有限公司"
                }
              },
              "weipin_zhongwei": {
                "fox_contract_sign_params": {
                  "loan_contract_code_format": "#item_no#_01",
                  "guarantee_sign": "sign_auto_shxzwrongzi",
                  "guarantee_company": "陕西中为融资担保有限公司"
                },
                "user_contract_query": [
                  28,
                31801,
                31802
                ]
              },
              "jinmeixin_daqin": {
                "verify_pdf_eseal_list": [
                  {
                    "contract_type": 28,
                    "subject_keyWord": "金美信"
                  }
                ]
              },
              "jinmeixin_hanchen": {
                "verify_pdf_eseal_list": [
                  {
                    "contract_type": 28,
                    "subject_keyWord": "金美信"
                  }
                ]
              },
              "zhongbang_zhongji": {
                "user_contract_query": [
                  28,
                  34300,
                  34301
                ]
              }
            }
    return gc.NACOS.update_configs("contract%s" % gc.ENV, "contract_capital_config", content)


def update_contract_common_params_config():
    content = {
        "sign_User":{
            "identity":"#borrower.idnumEncrypt",
            "mobile":"#borrower.telEncrypt",
            "name":"#borrower.nameEncrypt",
            "encrypted":"'1'"
        }
    }
    return gc.NACOS.update_configs("contract%s" % gc.ENV, "contract_common_params_config", content)


if __name__ == "__main__":
    gc.init_env(9, "china", "dev")
    update_contract_sign_config()
    update_contract_capital_config()
    update_contract_common_params_config()
