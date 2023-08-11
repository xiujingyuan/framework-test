#!/usr/bin/python
# -*- coding: UTF-8 -*-
source_type_map = {
    "apr36": ["rongdan"],
    "irr36": ["rongdan_irr"],
    "irr36_rongshu": ["rongdan_irr"],
    "irr36_lexin": ["rongdan_irr"],
    "irr36_quanyi": ["rongdan_irr", "lieyin"],
    "real36": [],
    "real24": [],
    "": ["normal"],
    "apr36_huaya": ["rongdan"]
}

capital_plan = {
    "tongrongqianjingjing": [
    #     {
    #         "channel": "tongrongqianjingjing",
    #         "rule_code": "tongrongqianjingjing_0",
    #         "rule_desc": "通融钱京京0期总量",
    #         "rule_family": "通融钱京京-兜底",
    #         "rule_content": "{\"name\":\"通融钱京京总量\",\"rules\":[{\"name\":\"通融钱京京总量\"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongqianjingjing\"}}",
    #         "rule_type": "supply",
    #         "rule_activation_group": "",
    #         "rule_limit_type": "strict",
    #         "rule_weight": 0,
    #         "rule_allow_overflow_rate": 0,
    #         "rule_product_code": "",
    #         "weight_value": 0,
    #         "weight_status": "active",
    #         "weight_first_route_status": "active",
    #         "weight_second_route_status": "active"
    #     },
    #     {
    #         "channel": "tongrongqianjingjing",
    #         "rule_code": "tongrongqianjingjing_12m",
    #         "rule_desc": "通融12期兜底",
    #         "rule_family": "通融钱京京-兜底",
    #         "rule_content": "{\"name\":\"通融钱京京12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12  \"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongqianjingjing\"}}",
    #         "rule_activation_group": "tongrongqianjingjing",
    #     },
    #     {
    #         "channel": "tongrongqianjingjing",
    #         "rule_code": "tongrongqianjingjing_6m",
    #         "rule_desc": "通融6期兜底",
    #         "rule_family": "通融钱京京-兜底",
    #         "rule_content": "{\"name\":\"通融钱京京6期\",\"rules\":[{\"name\":\"通融钱京京6期\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 \"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongqianjingjing\"}}",
    #         "rule_activation_group": "tongrongqianjingjing",
    #     },
    #     {
    #         "channel": "tongrongqianjingjing",
    #         "rule_code": "tongrongqianjingjing_6m_12m",
    #         "rule_desc": "通融钱京京1次控量",
    #         "rule_family": "通融钱京京1次控量",
    #         "rule_content": "{\"name\":\"通融钱京京1次控量\",\"rules\":[{\"name\":\"通融钱京京6期&12期\",\"rule\":\"asset.periodType==\\'month\\' \"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongqianjingjing\"}}",
    #         "rule_activation_group": "tongrongqianjingjing",
    #     },
    #     {
    #         "channel": "tongrongqianjingjing",
    #         "rule_code": "tongrongqianjingjing_0dc",
    #         "rule_desc": "通融在贷0笔兜底",
    #         "rule_family": "通融钱京京-兜底",
    #         "rule_content": "{\"name\":\"通融在贷0笔兜底\",\"rules\":[{\"name\":\"通融在贷0笔兜底\",\"rule\":\"asset.periodType==\\'month\\' and assetExtend.totalDebtCount==0 \"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongqianjingjing\"}}",
    #         "rule_activation_group": "tongrongqianjingjing",
    #         "weight_first_route_status": "inactive",
    #     },
    #     # {
    #     #     "channel": "tongrongqianjingjing",
    #     #     "rule_code": "tongrongqianjingjing_6m_newUser",
    #     #     "rule_desc": "通融6期（新客）",
    #     #     "rule_family": "通融钱京京",
    #     #     "rule_content": "{\"name\":\"通融6期（新客）\",\"rules\":[{\"name\":\"通融6期（新客）\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and assetExtend.customerType==\\'new\\'\"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongqianjingjing\"}}",
    #     #     "rule_type": "supply",
    #     #     "rule_activation_group": "",
    #     #     "rule_limit_type": "strict",
    #     #     "rule_weight": 0,
    #     #     "rule_allow_overflow_rate": 0,
    #     #     "rule_product_code": "",
    #     #     "weight_value": 0,
    #     #     "weight_status": "active",
    #     #     "weight_first_route_status": "active",
    #     #     "weight_second_route_status": "active"
    #     # },
    #     # {
    #     #     "channel": "tongrongqianjingjing",
    #     #     "rule_code": "tongrongqianjingjing_6m_oldUser",
    #     #     "rule_desc": "通融6期（老客）",
    #     #     "rule_family": "通融钱京京",
    #     #     "rule_content": "{\"name\":\"通融6期（老客）\",\"rules\":[{\"name\":\"通融6期（老客）\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and assetExtend.customerType==\\'old\\'\"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongqianjingjing\"}}",
    #     # },
    #     # {
    #     #     "channel": "tongrongqianjingjing",
    #     #     "rule_code": "tongrongqianjingjing_12m_newUser",
    #     #     "rule_desc": "通融12期（新客）",
    #     #     "rule_family": "通融钱京京",
    #     #     "rule_content": "{\"name\":\"通融12期（新客）\",\"rules\":[{\"name\":\"通融12期（新客）\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and assetExtend.customerType==\\'new\\'\"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongqianjingjing\"}}",
    #     # },
    #     # {
    #     #     "channel": "tongrongqianjingjing",
    #     #     "rule_code": "tongrongqianjingjing_12m_oldUser",
    #     #     "rule_desc": "通融12期（老客）",
    #     #     "rule_family": "通融钱京京",
    #     #     "rule_content": "{\"name\":\"通融12期（老客）\",\"rules\":[{\"name\":\"通融12期（老客）\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and assetExtend.customerType==\\'old\\'\"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongqianjingjing\"}}",
    #     # },
     ],
    "haohanqianjingjing": [
        # {
        #     "channel": "haohanqianjingjing",
        #     "rule_code": "haohanqianjingjing_6m_newUser",
        #     "rule_desc": "浩瀚6期（新客）",
        #     "rule_family": "浩瀚钱京京",
        #     "rule_content": "{\"name\":\"浩瀚6期（新客）\",\"rules\":[{\"name\":\"浩瀚6期（新客）\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and assetExtend.customerType==\\'new\\'\"}],\"output\":{\"key\":\"channel\",\"value\":\"haohanqianjingjing\"}}",
        # },
        # {
        #     "channel": "haohanqianjingjing",
        #     "rule_code": "haohanqianjingjing_6m_oldUser",
        #     "rule_desc": "浩瀚6期（老客）",
        #     "rule_family": "浩瀚钱京京",
        #     "rule_content": "{\"name\":\"浩瀚6期（老客）\",\"rules\":[{\"name\":\"浩瀚6期（老客）\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and assetExtend.customerType==\\'old\\'\"}],\"output\":{\"key\":\"channel\",\"value\":\"haohanqianjingjing\"}}",
        # },
        # {
        #     "channel": "haohanqianjingjing",
        #     "rule_code": "haohanqianjingjing_12m_newUser",
        #     "rule_desc": "浩瀚12期（新客）",
        #     "rule_family": "浩瀚钱京京",
        #     "rule_content": "{\"name\":\"浩瀚12期（新客）\",\"rules\":[{\"name\":\"浩瀚12期（新客）\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and assetExtend.customerType==\\'new\\'\"}],\"output\":{\"key\":\"channel\",\"value\":\"haohanqianjingjing\"}}",
        # },
        # {
        #     "channel": "haohanqianjingjing",
        #     "rule_code": "haohanqianjingjing_12m_noldUser",
        #     "rule_desc": "浩瀚12期（老客）",
        #     "rule_family": "浩瀚钱京京",
        #     "rule_content": "{\"name\":\"浩瀚12期（老客）\",\"rules\":[{\"name\":\"浩瀚12期（老客）\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and assetExtend.customerType==\\'old\\'\"}],\"output\":{\"key\":\"channel\",\"value\":\"haohanqianjingjing\"}}",
        # },
        # {
        #     "channel": "haohanqianjingjing",
        #     "rule_code": "haohanqianjingjing_6m",
        #     "rule_desc": "浩瀚6期兜底",
        #     "rule_family": "浩瀚钱京京-兜底",
        #     "rule_content": "{\"name\":\"浩瀚钱京京6期\",\"rules\":[{\"name\":\"浩瀚钱京京6期\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 \"}],\"output\":{\"key\":\"channel\",\"value\":\"haohanqianjingjing\"}}",
        #     "rule_activation_group": "haohanqianjingjing",
        # },
        {
            "channel": "haohanqianjingjing",
            "rule_code": "haohanqianjingjing_0dc",
            "rule_desc": "浩瀚在贷0笔兜底",
            "rule_family": "浩瀚钱京京-兜底",
            "rule_content": "{\"name\":\"浩瀚在贷0笔兜底\",\"rules\":[{\"name\":\"浩瀚在贷0笔兜底\",\"rule\":\"asset.periodType==\\'month\\' and assetExtend.totalDebtCount==0 \"}],\"output\":{\"key\":\"channel\",\"value\":\"haohanqianjingjing\"}}",
            "rule_activation_group": "haohanqianjingjing",
            "weight_first_route_status": "inactive",
        },
        {
            "channel": "haohanqianjingjing",
            "rule_code": "haohanqianjingjing_0",
            "rule_desc": "浩瀚钱京京0期总量",
            "rule_family": "浩瀚钱京京-兜底",
            "rule_content": "{\"name\":\"浩瀚钱京京总量\",\"rules\":[{\"name\":\"浩瀚钱京京总量\"}],\"output\":{\"key\":\"channel\",\"value\":\"haohanqianjingjing\"}}",
            "rule_type": "supply",
            "rule_activation_group": "",
            "rule_limit_type": "strict",
            "rule_weight": 0,
            "rule_allow_overflow_rate": 0,
            "rule_product_code": "",
            "weight_value": 0,
            "weight_status": "active",
            "weight_first_route_status": "active",
            "weight_second_route_status": "active"
        },
        {
            "channel": "haohanqianjingjing",
            "rule_code": "haohanqianjingjing_12m",
            "rule_desc": "浩瀚12期兜底",
            "rule_family": "浩瀚钱京京-兜底",
            "rule_content": "{\"name\":\"浩瀚钱京京12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12  \"}],\"output\":{\"key\":\"channel\",\"value\":\"haohanqianjingjing\"}}",
            "rule_activation_group": "haohanqianjingjing",
        },
        {
            "channel": "haohanqianjingjing",
            "rule_code": "haohanqianjingjing_6m_12m",
            "rule_desc": "浩瀚钱京京1次控量",
            "rule_family": "浩瀚钱京京1次控量",
            "rule_content": "{\"name\":\"浩瀚钱京京1次控量\",\"rules\":[{\"name\":\"浩瀚钱京京6期&12期\",\"rule\":\"asset.periodType==\\'month\\' \"}],\"output\":{\"key\":\"channel\",\"value\":\"haohanqianjingjing\"}}",
            "rule_activation_group": "haohanqianjingjing",
        }
    ],
    # "qinnong": [
    #     {
    #         "channel": "qinnong",
    #         "rule_code": "qinnong_6m",
    #         "rule_desc": "秦农6期",
    #         "rule_family": "秦农",
    #         "rule_content": "{\"name\":\"秦农6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"qinnong\"}}",
    #     },
    #     {
    #         "channel": "qinnong",
    #         "rule_code": "qinnong_12m",
    #         "rule_desc": "秦农12期",
    #         "rule_family": "秦农",
    #         "rule_content": "{\"name\":\"秦农12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"qinnong\"}}",
    #     },
    # ],
    # "qinnong_jieyi": [
    #     {
    #         "channel": "qinnong_jieyi",
    #         "rule_code": "qinnong_jieyi_6m",
    #         "rule_desc": "秦农杰益6期",
    #         "rule_family": "秦农杰益",
    #         "rule_content": "{\"name\":\"秦农杰益6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"qinnong_jieyi\"}}",
    #     },
    #     {
    #         "channel": "qinnong_jieyi",
    #         "rule_code": "qinnong_jieyi_12m",
    #         "rule_desc": "秦农杰益12期",
    #         "rule_family": "秦农杰益",
    #         "rule_content": "{\"name\":\"秦农杰益12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"qinnong_jieyi\"}}",
    #     },
    # ],
    # "qinnong_dingfeng": [
    #     {
    #         "channel": "qinnong_dingfeng",
    #         "rule_code": "qinnong_dingfeng_6m",
    #         "rule_desc": "秦农鼎丰6期",
    #         "rule_family": "秦农鼎丰",
    #         "rule_content": "{\"name\":\"秦农鼎丰6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"qinnong_dingfeng\"}}",
    #     },
    #     {
    #         "channel": "qinnong_dingfeng",
    #         "rule_code": "qinnong_dingfeng_12m",
    #         "rule_desc": "秦农鼎丰12期",
    #         "rule_family": "秦农鼎丰",
    #         "rule_content": "{\"name\":\"秦农鼎丰12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"qinnong_dingfeng\"}}",
    #     },
    # ],
    # "weishenma_daxinganling": [
    #     {
    #         "channel": "weishenma_daxinganling",
    #         "rule_code": "weishenma_daxinganling_6m",
    #         "rule_desc": "微神马6期",
    #         "rule_family": "微神马",
    #         "rule_content": "{\"name\":\"微神马6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"weishenma_daxinganling\"}}",
    #     },
    #     {
    #         "channel": "weishenma_daxinganling",
    #         "rule_code": "weishenma_daxinganling_12m",
    #         "rule_desc": "微神马12期",
    #         "rule_family": "微神马",
    #         "rule_content": "{\"name\":\"微神马12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"weishenma_daxinganling\"}}",
    #     },
    # ],
    # "zhongke_lanzhou": [
    #     {
    #         "channel": "zhongke_lanzhou",
    #         "rule_code": "zhongke_lanzhou_6m",
    #         "rule_desc": "中科兰州6期",
    #         "rule_family": "中科兰州",
    #         "rule_content": "{\"name\":\"中科兰州6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongke_lanzhou\"}}",
    #     },
    #     {
    #         "channel": "zhongke_lanzhou",
    #         "rule_code": "zhongke_lanzhou_12m",
    #         "rule_desc": "中科兰州12期",
    #         "rule_family": "中科兰州",
    #         "rule_content": "{\"name\":\"中科兰州12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongke_lanzhou\"}}",
    #     },
    # ],
    # "lanzhou_dingsheng_zkbc2": [
    #     {
    #         "channel": "lanzhou_dingsheng_zkbc2",
    #         "rule_code": "lanzhou_dingsheng_zkbc2_6m",
    #         "rule_desc": "兰州鼎盛6期",
    #         "rule_family": "兰州鼎盛",
    #         "rule_content": "{\"name\":\"兰州鼎盛6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_dingsheng_zkbc2\"}}",
    #     },
    #     {
    #         "channel": "lanzhou_dingsheng_zkbc2",
    #         "rule_code": "lanzhou_dingsheng_zkbc2_12m",
    #         "rule_desc": "兰州鼎盛12期",
    #         "rule_family": "兰州鼎盛",
    #         "rule_content": "{\"name\":\"兰州鼎盛12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_dingsheng_zkbc2\"}}",
    #     },
    # ],
    "lanzhou_haoyue": [
        # {
        #     "channel": "lanzhou_haoyue",
        #     "rule_code": "lanzhou_haoyue_6m",
        #     "rule_desc": "兰州昊悦6期（非甘肃）",
        #     "rule_family": "兰州昊悦",
        #     "rule_content": "{\"name\":\"兰州昊悦6期-非甘肃\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and (borrowerExtend.district.idNumDistrict!=\\'甘肃省\\' and borrowerExtend.district.idAddrDistrict!=\\'甘肃省\\' and borrowerExtend.district.residentialDistrict!=\\'甘肃省\\' and borrowerExtend.district.workplaceDistrict!=\\'甘肃省\\' and borrowerExtend.district.mobileDistrict!=\\'甘肃省\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_haoyue\"}}",
        #     "rule_product_code": "not_gansu",
        # },
        # {
        #     "channel": "lanzhou_haoyue",
        #     "rule_code": "lanzhou_haoyue_6m_gansu",
        #     "rule_desc": "兰州昊悦6期（甘肃）",
        #     "rule_family": "兰州昊悦",
        #     "rule_content": "{\"name\":\"兰州昊悦6期-甘肃\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and (borrowerExtend.district.idNumDistrict==\\'甘肃省\\' or borrowerExtend.district.idAddrDistrict==\\'甘肃省\\'or borrowerExtend.district.residentialDistrict==\\'甘肃省\\' or borrowerExtend.district.workplaceDistrict==\\'甘肃省\\' or borrowerExtend.district.mobileDistrict==\\'甘肃省\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_haoyue\"}}",
        #     "rule_product_code": "gansu",
        # },
        # {
        #     "channel": "lanzhou_haoyue",
        #     "rule_code": "lanzhou_haoyue_12m",
        #     "rule_desc": "兰州昊悦12期（非甘肃）",
        #     "rule_family": "兰州昊悦",
        #     "rule_content": "{\"name\":\"兰州昊悦12期-非甘肃\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and (borrowerExtend.district.idNumDistrict!=\\'甘肃省\\' and borrowerExtend.district.idAddrDistrict!=\\'甘肃省\\' and borrowerExtend.district.residentialDistrict!=\\'甘肃省\\' and borrowerExtend.district.workplaceDistrict!=\\'甘肃省\\' and borrowerExtend.district.mobileDistrict!=\\'甘肃省\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_haoyue\"}}",
        #     "rule_product_code": "not_gansu",
        # },
        # {
        #     "channel": "lanzhou_haoyue",
        #     "rule_code": "lanzhou_haoyue_12m_gansu",
        #     "rule_desc": "兰州昊悦12期（甘肃）",
        #     "rule_family": "兰州昊悦",
        #     "rule_content": "{\"name\":\"兰州昊悦12期-甘肃\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and (borrowerExtend.district.idNumDistrict==\\'甘肃省\\' or borrowerExtend.district.idAddrDistrict==\\'甘肃省\\'or borrowerExtend.district.residentialDistrict==\\'甘肃省\\' or borrowerExtend.district.workplaceDistrict==\\'甘肃省\\' or borrowerExtend.district.mobileDistrict==\\'甘肃省\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_haoyue\"}}",
        #     "rule_product_code": "gansu",
        # },
        {
            "channel": "lanzhou_haoyue",
            "rule_code": "lanzhou_haoyue_12m_zk2",
            "rule_desc": "兰州昊悦12期（zk2）",
            "rule_family": "兰州昊悦",
            "rule_content": "{\"name\":\"兰州昊悦12期（zk2）12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_haoyue\"}}",
            "rule_product_code": "zk2",
        },
    ],
    # "hami_tianshan_tianbang": [
    #     {
    #         "channel": "hami_tianshan_tianbang",
    #         "rule_code": "hami_tianshan_tianbang_6m",
    #         "rule_desc": "哈密天邦6期",
    #         "rule_family": "哈密天邦",
    #         "rule_content": "{\"name\":\"哈密天邦6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"hami_tianshan_tianbang\"}}",
    #     },
    #     {
    #         "channel": "hami_tianshan_tianbang",
    #         "rule_code": "hami_tianshan_tianbang_12m",
    #         "rule_desc": "哈密天邦12期",
    #         "rule_family": "哈密天邦",
    #         "rule_content": "{\"name\":\"哈密天邦12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"hami_tianshan_tianbang\"}}",
    #     },
    # ],
    # "hamitianbang_xinjiang": [
    #     {
    #         "channel": "hamitianbang_xinjiang",
    #         "rule_code": "hamitianbang_xinjiang_12m",
    #         "rule_desc": "哈密天邦新疆12期",
    #         "rule_family": "哈密天邦新疆",
    #         "rule_content": "{\"name\":\"哈密天邦新疆12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"hamitianbang_xinjiang\"}}",
    #         "rule_product_code": "",
    #     },
    #     {
    #         "channel": "hamitianbang_xinjiang",
    #         "rule_code": "hamitianbang_xinjiang_6m",
    #         "rule_desc": "哈密天邦新疆6期（全国）",
    #         "rule_family": "哈密天邦新疆",
    #         "rule_content": "{\"name\":\"哈密天邦新疆6期-全国\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"hamitianbang_xinjiang\"}}",
    #         "rule_product_code": "hmtlf",
    #     }
    # ],
    # "mozhi_beiyin_zhongyi": [
    #     {
    #         "channel": "mozhi_beiyin_zhongyi",
    #         "rule_code": "mozhi_beiyin_zhongyi_6m",
    #         "rule_desc": "墨智北银6期",
    #         "rule_family": "墨智北银",
    #         "rule_content": "{\"name\":\"墨智北银6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"mozhi_beiyin_zhongyi\"}}",
    #     },
    #     {
    #         "channel": "mozhi_beiyin_zhongyi",
    #         "rule_code": "mozhi_beiyin_zhongyi_12m",
    #         "rule_desc": "墨智北银12期",
    #         "rule_family": "墨智北银",
    #         "rule_content": "{\"name\":\"墨智北银12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"mozhi_beiyin_zhongyi\"}}",
    #     },
    # ],
    "beiyin_tianbang": [
        {
            "channel": "beiyin_tianbang",
            "rule_code": "beiyin_tianbang_6m",
            "rule_desc": "北银天邦6期",
            "rule_family": "北银天邦",
            "rule_content": "{\"name\":\"北银天邦6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"beiyin_tianbang\"}}",
        },
        {
            "channel": "beiyin_tianbang",
            "rule_code": "beiyin_tianbang_12m",
            "rule_desc": "北银天邦12期",
            "rule_family": "北银天邦",
            "rule_content": "{\"name\":\"北银天邦12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"beiyin_tianbang\"}}",
        },
    ],
    # "huabei_runqian": [
    #     {
    #         "channel": "huabei_runqian",
    #         "rule_code": "huabei_runqian_6m",
    #         "rule_desc": "华北润乾6期",
    #         "rule_family": "华北润乾",
    #         "rule_content": "{\"name\":\"华北润乾6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"huabei_runqian\"}}",
    #     },
    #     {
    #         "channel": "huabei_runqian",
    #         "rule_code": "huabei_runqian_12m",
    #         "rule_desc": "华北润乾12期",
    #         "rule_family": "华北润乾",
    #         "rule_content": "{\"name\":\"华北润乾12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"huabei_runqian\"}}",
    #     },
    # ],
    # "longjiang_daqin": [
    #     {
    #         "channel": "longjiang_daqin",
    #         "rule_code": "longjiang_daqin_6m",
    #         "rule_desc": "龙江大秦6期",
    #         "rule_family": "龙江大秦",
    #         "rule_content": "{\"name\":\"龙江大秦6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"longjiang_daqin\"}}",
    #     },
    #     {
    #         "channel": "longjiang_daqin",
    #         "rule_code": "longjiang_daqin_12m",
    #         "rule_desc": "龙江大秦12期",
    #         "rule_family": "龙江大秦",
    #         "rule_content": "{\"name\":\"龙江大秦12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"longjiang_daqin\"}}",
    #     },
    # ],
    # "siping_jiliang": [
    #     {
    #         "channel": "siping_jiliang",
    #         "rule_code": "siping_jiliang_6m",
    #         "rule_desc": "四平吉良6期",
    #         "rule_family": "四平吉良",
    #         "rule_content": "{\"name\":\"四平吉良6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"siping_jiliang\"}}",
    #     },
    #     {
    #         "channel": "siping_jiliang",
    #         "rule_code": "siping_jiliang_12m",
    #         "rule_desc": "四平吉良12期",
    #         "rule_family": "四平吉良",
    #         "rule_content": "{\"name\":\"四平吉良12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"siping_jiliang\"}}",
    #     },
    # ],
    # "mozhi_jinmeixin": [
    #     {
    #         "channel": "mozhi_jinmeixin",
    #         "rule_code": "mozhi_jinmeixin_6m_irr",
    #         "rule_desc": "墨智金美信6期（IRR）",
    #         "rule_family": "墨智金美信",
    #         "rule_content": "{\"name\":\"墨智金美信6期（irr）\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and (asset.refOrderType==\\'irr36\\' || asset.refOrderType==\\'irr36_quanyi\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"mozhi_jinmeixin\"}}",
    #     },
    #     {
    #         "channel": "mozhi_jinmeixin",
    #         "rule_code": "mozhi_jinmeixin_6m_apr",
    #         "rule_desc": "墨智金美信6期（APR）",
    #         "rule_family": "墨智金美信",
    #         "rule_content": "{\"name\":\"墨智金美信6期（apr）\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and (asset.refOrderType==\\'apr36\\' || asset.refOrderType==\\'real36\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"mozhi_jinmeixin\"}}",
    #     },
    #     {
    #         "channel": "mozhi_jinmeixin",
    #         "rule_code": "mozhi_jinmeixin_12m_irr",
    #         "rule_desc": "墨智金美信12期（IRR）",
    #         "rule_family": "墨智金美信",
    #         "rule_content": "{\"name\":\"墨智金美信12期（irr）\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and (asset.refOrderType==\\'irr36\\' || asset.refOrderType==\\'irr36_quanyi\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"mozhi_jinmeixin\"}}",
    #     },
    #     {
    #         "channel": "mozhi_jinmeixin",
    #         "rule_code": "mozhi_jinmeixin_12m_apr",
    #         "rule_desc": "墨智金美信12期（APR）",
    #         "rule_family": "墨智金美信",
    #         "rule_content": "{\"name\":\"墨智金美信12期（apr）\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and (asset.refOrderType==\\'apr36\\' || asset.refOrderType==\\'real36\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"mozhi_jinmeixin\"}}",
    #     }
    # ],
    # "zhongke_hegang": [
    #     {
    #         "channel": "zhongke_hegang",
    #         "rule_code": "zhongke_hegang_12m",
    #         "rule_desc": "中科鹤岗12期(非黑龙江)",
    #         "rule_family": "中科鹤岗",
    #         "rule_content": "{\"name\":\"中科鹤岗12期-非黑龙江\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and (borrowerExtend.district.idNumDistrict!=\\'黑龙江省\\' and borrowerExtend.district.idAddrDistrict!=\\'黑龙江省\\' and borrowerExtend.district.residentialDistrict!=\\'黑龙江省\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongke_hegang\"}}",
    #         "rule_product_code": "KN1-CL-NOT-HLJ",
    #     },
    #     {
    #         "channel": "zhongke_hegang",
    #         "rule_code": "zhongke_hegang_12m_hlj",
    #         "rule_desc": "中科鹤岗12期(黑龙江)",
    #         "rule_family": "中科鹤岗",
    #         "rule_content": "{\"name\":\"中科鹤岗12期-黑龙江\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12 and (borrowerExtend.district.idNumDistrict==\\'黑龙江省\\' or borrowerExtend.district.idAddrDistrict==\\'黑龙江省\\'or borrowerExtend.district.residentialDistrict==\\'黑龙江省\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongke_hegang\"}}",
    #         "rule_product_code": "KN1-CL-HLJ",
    #     },
    #     {
    #         "channel": "zhongke_hegang",
    #         "rule_code": "zhongke_hegang_6m",
    #         "rule_desc": "中科鹤岗6期(非黑龙江)",
    #         "rule_family": "中科鹤岗",
    #         "rule_content": "{\"name\":\"中科鹤岗6期-非黑龙江\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and (borrowerExtend.district.idNumDistrict!=\\'黑龙江省\\' and borrowerExtend.district.idAddrDistrict!=\\'黑龙江省\\' and borrowerExtend.district.residentialDistrict!=\\'黑龙江省\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongke_hegang\"}}",
    #         "rule_product_code": "KN1-CL-NOT-HLJ",
    #     },
    #     {
    #         "channel": "zhongke_hegang",
    #         "rule_code": "zhongke_hegang_6m_hlj",
    #         "rule_desc": "中科鹤岗6期(黑龙江)",
    #         "rule_family": "中科鹤岗",
    #         "rule_content": "{\"name\":\"中科鹤岗6期-黑龙江\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6 and (borrowerExtend.district.idNumDistrict==\\'黑龙江省\\' or borrowerExtend.district.idAddrDistrict==\\'黑龙江省\\'or borrowerExtend.district.residentialDistrict==\\'黑龙江省\\')\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongke_hegang\"}}",
    #         "rule_product_code": "KN1-CL-HLJ",
    #     }
    # ],
    # "haishengtong_daqin": [
    #     {
    #         "channel": "haishengtong_daqin",
    #         "rule_code": "haishengtong_daqin_GTQH01",
    #         "rule_desc": "海胜通大秦6&12期_GTQH01信托计划",
    #         "rule_family": "海胜通大秦",
    #         "rule_content": "{\"name\":\"海胜通大秦6&12期_GTQH01信托计划\",\"rules\":[{\"name\":\"海胜通大秦6&12期_GTQH01\",\"rule\":\"asset.periodType==\\'month\\' and ((asset.periodCount==6 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2020-01-01\\')) or (asset.periodCount==12 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-01-01\\')))\"}],\"output\":{\"key\":\"channel\",\"value\":\"haishengtong_daqin\"}}",
    #         "rule_type": "supply",
    #         "rule_activation_group": "haishengtong_daqin",
    #         "rule_product_code": "GTQH01",
    #     },
    #     {
    #         "channel": "haishengtong_daqin",
    #         "rule_code": "haishengtong_daqin_GTQH02",
    #         "rule_desc": "海胜通大秦6&12期_GTQH02信托计划",
    #         "rule_family": "海胜通大秦",
    #         "rule_content": "{\"name\":\"海胜通大秦6&12期_GTQH02信托计划\",\"rules\":[{\"name\":\"海胜通大秦6&12期_GTQH02\",\"rule\":\"asset.periodType==\\'month\\' and ((asset.periodCount==6 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-01-01\\')) or (asset.periodCount==12 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2020-01-01\\')))\"}],\"output\":{\"key\":\"channel\",\"value\":\"haishengtong_daqin\"}}",
    #         "rule_type": "supply",
    #         "rule_activation_group": "haishengtong_daqin",
    #         "rule_product_code": "GTQH02",
    #     },
    #     {
    #         "channel": "haishengtong_daqin",
    #         "rule_code": "haishengtong_daqin_GTQH03",
    #         "rule_desc": "海胜通大秦6&12期_GTQH03信托计划",
    #         "rule_family": "海胜通大秦",
    #         "rule_content": "{\"name\":\"海胜通大秦6&12期_GTQH03信托计划\",\"rules\":[{\"name\":\"海胜通大秦6&12期_GTQH03\",\"rule\":\"asset.periodType==\\'month\\' and ((asset.periodCount==6 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-05-14\\')) or (asset.periodCount==12 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-09-24\\')))\"}],\"output\":{\"key\":\"channel\",\"value\":\"haishengtong_daqin\"}}",
    #         "rule_type": "supply",
    #         "rule_activation_group": "haishengtong_daqin",
    #         "rule_product_code": "GTQH03",
    #     },
    #     {
    #         "channel": "haishengtong_daqin",
    #         "rule_code": "haishengtong_daqin_6m",
    #         "rule_desc": "海胜通大秦6期总量控量",
    #         "rule_family": "海胜通大秦",
    #         "rule_content": "{\"name\":\"海胜通大秦6期-总量\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"haishengtong_daqin\"}}",
    #         "rule_type": "demand",
    #         "rule_activation_group": "",
    #         "rule_product_code": "",
    #     },
    #     {
    #         "channel": "haishengtong_daqin",
    #         "rule_code": "haishengtong_daqin_12m",
    #         "rule_desc": "海胜通大秦12期总量控量",
    #         "rule_family": "海胜通大秦",
    #         "rule_content": "{\"name\":\"海胜通大秦12期-总量\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"haishengtong_daqin\"}}",
    #         "rule_type": "demand",
    #         "rule_activation_group": "",
    #         "rule_product_code": "",
    #     }
    # ],
    # "shanxixintuo": [
    #     {
    #         "channel": "shanxixintuo",
    #         "rule_code": "shanxixintuo_SXXT01",
    #         "rule_desc": "山西信托6&12期_SXXT01信托计划",
    #         "rule_family": "山西信托",
    #         "rule_content": "{\"name\":\"山西信托6&12期_SXXT01信托计划\",\"rules\":[{\"name\":\"山西信托6&12期_SXXT01\",\"rule\":\"asset.periodType==\\'month\\' and ((asset.periodCount==6 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-01-01\\')) or (asset.periodCount==12 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-01-01\\')))\"}],\"output\":{\"key\":\"channel\",\"value\":\"shanxixintuo\"}}",
    #         "rule_type": "supply",
    #         "rule_activation_group": "shanxixintuo",
    #         "rule_product_code": "SXXT01",
    #     },
    #     {
    #         "channel": "shanxixintuo",
    #         "rule_code": "shanxixintuo_SXXT02",
    #         "rule_desc": "山西信托6&12期_SXXT02信托计划",
    #         "rule_family": "山西信托",
    #         "rule_content": "{\"name\":\"山西信托6&12期_SXXT02信托计划\",\"rules\":[{\"name\":\"山西信托6&12期_SXXT02\",\"rule\":\"asset.periodType==\\'month\\' and ((asset.periodCount==6 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-01-01\\')) or (asset.periodCount==12 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-01-01\\')))\"}],\"output\":{\"key\":\"channel\",\"value\":\"shanxixintuo\"}}",
    #         "rule_type": "supply",
    #         "rule_activation_group": "shanxixintuo",
    #         "rule_product_code": "SXXT02",
    #     },
    #     {
    #         "channel": "shanxixintuo",
    #         "rule_code": "shanxixintuo_SXXT03",
    #         "rule_desc": "山西信托6&12期_SXXT03信托计划",
    #         "rule_family": "山西信托",
    #         "rule_content": "{\"name\":\"山西信托6&12期_SXXT03信托计划\",\"rules\":[{\"name\":\"山西信托6&12期_SXXT03\",\"rule\":\"asset.periodType==\\'month\\' and ((asset.periodCount==6 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-01-01\\')) or (asset.periodCount==12 and T(qsq.biz.grant.framework.client.util.DateTimeUtil).lt(\\'2030-01-01\\')))\"}],\"output\":{\"key\":\"channel\",\"value\":\"shanxixintuo\"}}",
    #         "rule_type": "supply",
    #         "rule_activation_group": "shanxixintuo",
    #         "rule_product_code": "SXXT03",
    #     },
    #     {
    #         "channel": "shanxixintuo",
    #         "rule_code": "shanxixintuo_6m",
    #         "rule_desc": "山西信托6期总量控量",
    #         "rule_family": "山西信托",
    #         "rule_content": "{\"name\":\"山西信托6期-总量\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"shanxixintuo\"}}",
    #         "rule_type": "demand",
    #         "rule_activation_group": "",
    #         "rule_product_code": "",
    #     },
    #     {
    #         "channel": "shanxixintuo",
    #         "rule_code": "shanxixintuo_12m",
    #         "rule_desc": "山西信托12期总量控量",
    #         "rule_family": "山西信托",
    #         "rule_content": "{\"name\":\"山西信托12期-总量\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"shanxixintuo\"}}",
    #         "rule_type": "demand",
    #         "rule_activation_group": "",
    #         "rule_product_code": "",
    #     }
    # ],
    # "tongrongbiaonei": [
    #     {
    #         "channel": "tongrongbiaonei",
    #         "rule_code": "tongrongbiaonei_6m",
    #         "rule_desc": "通融表内6期",
    #         "rule_family": "通融表内",
    #         "rule_content": "{\"name\":\"通融表内6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongbiaonei\"}}",
    #     },
    #     {
    #         "channel": "tongrongbiaonei",
    #         "rule_code": "tongrongbiaonei_12m",
    #         "rule_desc": "通融表内12期",
    #         "rule_family": "通融表内",
    #         "rule_content": "{\"name\":\"通融表内12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"tongrongbiaonei\"}}",
    #     },
    # ],
    "jinmeixin_daqin": [
        {
            "channel": "jinmeixin_daqin",
            "rule_code": "jinmeixin_daqin_6m",
            "rule_desc": "金美信大秦6期",
            "rule_family": "金美信大秦",
            "rule_content": "{\"name\":\"金美信大秦6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"jinmeixin_daqin\"}}",
        },
        {
            "channel": "jinmeixin_daqin",
            "rule_code": "jinmeixin_daqin_12m",
            "rule_desc": "金美信大秦12期",
            "rule_family": "金美信大秦",
            "rule_content": "{\"name\":\"金美信大秦12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"jinmeixin_daqin\"}}",
        },
    ],
    "yilian_dingfeng": [
        {
            "channel": "yilian_dingfeng",
            "rule_code": "yilian_dingfeng_6m",
            "rule_desc": "亿联鼎丰6期（DF）",
            "rule_family": "亿联鼎丰",
            "rule_content": "{\"name\":\"亿联鼎丰6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"yilian_dingfeng\"}}",
            "rule_product_code": "df",
            "rule_activation_group": "yilian"
        },
        {
            "channel": "yilian_dingfeng",
            "rule_code": "yilian_dingfeng_12m",
            "rule_desc": "亿联鼎丰12期（DF）",
            "rule_family": "亿联鼎丰",
            "rule_content": "{\"name\":\"亿联鼎丰12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"yilian_dingfeng\"}}",
            "rule_product_code": "df",
            "rule_activation_group": "yilian"
        },
        {
            "channel": "yilian_dingfeng",
            "rule_code": "yilian_dingfeng_6m_df2",
            "rule_desc": "亿联鼎丰6期（DF2）",
            "rule_family": "亿联鼎丰",
            "rule_content": "{\"name\":\"亿联鼎丰6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"yilian_dingfeng\"}}",
            "rule_product_code": "df2",
            "rule_activation_group": "yilian"
        },
        {
            "channel": "yilian_dingfeng",
            "rule_code": "yilian_dingfeng_12m_df2",
            "rule_desc": "亿联鼎丰12期（DF2）",
            "rule_family": "亿联鼎丰",
            "rule_content": "{\"name\":\"亿联鼎丰12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"yilian_dingfeng\"}}",
            "rule_product_code": "df2",
            "rule_activation_group": "yilian"
        }
    ],
    "weipin_zhongwei": [
        {
            "channel": "weipin_zhongwei",
            "rule_code": "weipin_zhongwei_6m",
            "rule_desc": "唯品中为6期",
            "rule_family": "唯品中为",
            "rule_content": "{\"name\":\"唯品中为6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"weipin_zhongwei\"}}",
        },
        {
            "channel": "weipin_zhongwei",
            "rule_code": "weipin_zhongwei_12m",
            "rule_desc": "唯品中为12期",
            "rule_family": "唯品中为",
            "rule_content": "{\"name\":\"唯品中为12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"weipin_zhongwei\"}}",
        }
    ],
    "jincheng_hanchen": [
        {
            "channel": "jincheng_hanchen",
            "rule_code": "jincheng_hanchen_6m",
            "rule_desc": "锦程汉辰6期",
            "rule_family": "锦程汉辰",
            "rule_content": "{\"name\":\"锦程汉辰6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"jincheng_hanchen\"}}",
        },
        {
            "channel": "jincheng_hanchen",
            "rule_code": "jincheng_hanchen_12m",
            "rule_desc": "锦程汉辰12期",
            "rule_family": "锦程汉辰",
            "rule_content": "{\"name\":\"锦程汉辰12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"jincheng_hanchen\"}}",
        },
    ],
    "lanzhou_haoyue_qinjia": [
        {
            "channel": "lanzhou_haoyue_qinjia",
            "rule_code": "lanzhou_haoyue_qinjia_12m",
            "rule_desc": "兰州昊悦（亲家）12期",
            "rule_family": "兰州昊悦（亲家）",
            "rule_content": "{\"name\":\"兰州昊悦（亲家）12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_haoyue_qinjia\"}}",
        }

    ],
    "zhongyuan_zunhao": [
        {
            "channel": "zhongyuan_zunhao",
            "rule_code": "zhongyuan_zunhao_6m",
            "rule_desc": "中原樽昊6期",
            "rule_family": "中原樽昊",
            "rule_content": "{\"name\":\"中原樽昊6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==6\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongyuan_zunhao\"}}",
        },
        {
            "channel": "zhongyuan_zunhao",
            "rule_code": "zhongyuan_zunhao_12m",
            "rule_desc": "中原樽昊12期",
            "rule_family": "中原樽昊",
            "rule_content": "{\"name\":\"中原樽昊12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongyuan_zunhao\"}}",
        },
    ],
    "beiyin_daqin": [
        {
            "channel": "beiyin_daqin",
            "rule_code": "beiyin_daqin_12m",
            "rule_desc": "北银大秦12期",
            "rule_family": "北银大秦",
            "rule_content": "{\"name\":\"北银大秦12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"beiyin_daqin\"}}",
        },
    ],
    "jinmeixin_hanchen": [
        {
            "channel": "jinmeixin_hanchen",
            "rule_code": "jinmeixin_hanchen_12m",
            "rule_desc": "金美信汉辰12期",
            "rule_family": "金美信汉辰",
            "rule_content": "{\"name\":\"金美信汉辰12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"jinmeixin_hanchen\"}}",
        },
    ],
    "yixin_rongsheng": [
        {
            "channel": "yixin_rongsheng",
            "rule_code": "yixin_rongsheng_6m",
            "rule_desc": "宜信荣晟6期",
            "rule_family": "宜信荣晟",
            "rule_content": "{\"name\":\"宜信荣晟6期\",\"rules\":[{\"name\":\"6期产品\",\"rule\":\"asset.periodType==\\'month\\' \"}],\"output\":{\"key\":\"channel\",\"value\":\"yixin_rongsheng\"}}",
            "rule_activation_group": "yixin_rongsheng",
            "router_capital_rule_limit_type": "nonstrict",
            "rule_product_code": "yxrs_6m"
        },
        {
            "channel": "yixin_rongsheng",
            "rule_code": "yixin_rongsheng_12m",
            "rule_desc": "宜信荣晟12期",
            "rule_family": "宜信荣晟",
            "rule_content": "{\"name\":\"宜信荣晟12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"yixin_rongsheng\"}}",
            "rule_activation_group": "yixin_rongsheng",
            "router_capital_rule_weight": 20,
            "router_capital_rule_limit_type": "nonstrict",
            "rule_product_code": "yxrs_12m"
        }

    ],
    "yumin_zhongbao": [
        {
            "channel": "yumin_zhongbao",
            "rule_code": "yumin_zhongbao_12m",
            "rule_desc": "裕民中保12期",
            "rule_family": "裕民中保",
            "rule_content": "{\"name\":\"裕民中保12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"yumin_zhongbao\"}}",
        },
    ],
    "jiexin_taikang_xinheyuan": [
        {
            "channel": "jiexin_taikang_xinheyuan",
            "rule_code": "jiexin_taikang_xinheyuan_12m",
            "rule_desc": "捷信泰康信合元12期",
            "rule_family": "捷信泰康信合元",
            "rule_content": "{\"name\":\"捷信泰康信合元12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"jiexin_taikang_xinheyuan\"}}",
        },
    ],
    "jiexin_taikang": [
        {
            "channel": "jiexin_taikang",
            "rule_code": "jiexin_taikang_12m",
            "rule_desc": "捷信泰康12期",
            "rule_family": "捷信泰康",
            "rule_content": "{\"name\":\"捷信泰康12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"jiexin_taikang\"}}",
        },
    ],
    "jinmeixin_hanchen_jf": [
            {
                "channel": "jinmeixin_hanchen_jf",
                "rule_code": "jinmeixin_hanchen_jf_12m",
                "rule_desc": "金美信汉辰京发12期",
                "rule_family": "金美信汉辰京发",
                "rule_content": "{\"name\":\"金美信汉辰京发12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"jinmeixin_hanchen_jf\"}}",
            },
        ],
    "zhenong_rongsheng": [
            {
                "channel": "zhenong_rongsheng",
                "rule_code": "zhenong_rongsheng_12m",
                "rule_desc": "浙农荣晟12期",
                "rule_family": "浙农荣晟",
                "rule_content": "{\"name\":\"浙农荣晟12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhenong_rongsheng\"}}",
            }
        ],
    "lanhai_zhongshi_qj": [
        {
            "channel": "lanhai_zhongshi_qj",
            "rule_code": "lanhai_zhongshi_qj_12m",
            "rule_desc": "蓝海中世亲家12期",
            "rule_family": "蓝海中世亲家",
            "rule_content": "{\"name\":\"蓝海中世亲家12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanhai_zhongshi_qj\"}}",
        },
    ],
    "lanzhou_haoyue_chongtian": [
        {
            "channel": "lanzhou_haoyue_chongtian",
            "rule_code": "lanzhou_haoyue_chongtian_12m",
            "rule_desc": "兰州昊悦（崇天）12期",
            "rule_family": "兰州昊悦（崇天）",
            "rule_content": "{\"name\":\"兰州昊悦（崇天）12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_haoyue_chongtian\"}}",
        },
    ],
    "changyin_mingdonghua_rl": [
        {
            "channel": "changyin_mingdonghua_rl",
            "rule_code": "changyin_mingdonghua_rl_12m",
            "rule_desc": "长银明东华润楼12期",
            "rule_family": "长银明东华润楼",
            "rule_content": "{\"name\":\"长银明东华润楼12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"changyin_mingdonghua_rl\"}}",
        }
    ],
    "zhongbang_zhongji": [
        {
            "channel": "zhongbang_zhongji",
            "rule_code": "zhongbang_zhongji_12m",
            "rule_desc": "众邦中际12期",
            "rule_family": "众邦中际",
            "rule_content": "{\"name\":\"众邦中际12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongbang_zhongji\"}}",
        }
    ],
    "daxinganling_zhongyi": [
        {
            "channel": "daxinganling_zhongyi",
            "rule_code": "daxinganling_zhongyi_12m",
            "rule_desc": "大兴安岭中裔12期",
            "rule_family": "大兴安岭中裔",
            "rule_content": "{\"name\":\"大兴安岭中裔12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"daxinganling_zhongyi\"}}",
        }
    ],
    "zhenxing_zhongzhixin_jx": [
        {
            "channel": "zhenxing_zhongzhixin_jx",
            "rule_code": "zhenxing_zhongzhixin_jx_12m",
            "rule_desc": "振兴中智信捷信12期",
            "rule_family": "振兴中智信捷信",
            "rule_content": "{\"name\":\"振兴中智信捷信12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhenxing_zhongzhixin_jx\"}}",
        }
    ],
    # "hebei_wenshun_ts": [
    #     {
    #         "channel": "hebei_wenshun_ts",
    #         "rule_code": "hebei_wenshun_ts_12m",
    #         "rule_desc": "河北稳顺12期",
    #         "rule_family": "河北稳顺",
    #         "rule_content": "{\"name\":\"河北稳顺12期12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"hebei_wenshun_ts\"}}",
    #     }
    # ],
    "lanhai_zhilian": [
        {
            "channel": "lanhai_zhilian",
            "rule_code": "lanhai_zhilian_12m",
            "rule_desc": "蓝海直连12期",
            "rule_family": "蓝海直连",
            "rule_content": "{\"name\":\"蓝海直连12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanhai_zhilian\"}}",
        }
    ],
    "changyin_junxin": [
        {
            "channel": "changyin_junxin",
            "rule_code": "changyin_junxin_12m",
            "rule_desc": "长银钧信12期",
            "rule_family": "长银钧信",
            "rule_content": "{\"name\":\"长银钧信12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"changyin_junxin\"}}",
        }
    ],
    "weipin_zhongzhixin": [
        {
            "channel": "weipin_zhongzhixin",
            "rule_code": "weipin_zhongzhixin",
            "rule_desc": "唯品中智信12期",
            "rule_family": "唯品中智信",
            "rule_content": "{\"name\":\"唯品中智信12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"weipin_zhongzhixin\"}}",
        }
    ],
    "hebei_jiahexing_ts": [
        {
            "channel": "hebei_jiahexing_ts",
            "rule_code": "hebei_jiahexing_ts_12m",
            "rule_desc": "河北嘉合兴(中科泰山)12期",
            "rule_family": "河北嘉合兴(中科泰山)",
            "rule_content": "{\"name\":\"河北嘉合兴(中科泰山)12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"hebei_jiahexing_ts\"}}",
        }
    ],
    "zhongbang_haoyue_rl": [
        {
            "channel": "zhongbang_haoyue_rl",
            "rule_code": "zhongbang_haoyue_rl_12m",
            "rule_desc": "众邦昊悦润楼12期",
            "rule_family": "众邦昊悦润楼",
            "rule_content": "{\"name\":\"众邦昊悦润楼12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongbang_haoyue_rl\"}}",
        }
    ],
    "hayin_zhongbao": [
        {
            "channel": "hayin_zhongbao",
            "rule_code": "hayin_zhongbao_12m",
            "rule_desc": "哈银中保12期",
            "rule_family": "哈银中保",
            "rule_content": "{\"name\":\"哈银中保12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"hayin_zhongbao\"}}",
        }
    ],
    "weipin_hanchen_jf": [
        {
            "channel": "weipin_hanchen_jf",
            "rule_code": "weipin_hanchen_jf_12m",
            "rule_desc": "唯品汉辰京发12期",
            "rule_family": "唯品汉辰京发",
            "rule_content": "{\"name\":\"唯品汉辰京发12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"weipin_hanchen_jf\"}}",
        }
    ],
    "xiaomi_zhongji": [
        {
            "channel": "xiaomi_zhongji",
            "rule_code": "xiaomi_zhongji_12m",
            "rule_desc": "小米中际12期",
            "rule_family": "小米中际",
            "rule_content": "{\"name\":\"小米中际12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"xiaomi_zhongji\"}}",
        }
    ],
    "lanhai_zhongbao_rl": [
        {
            "channel": "lanhai_zhongbao_rl",
            "rule_code": "lanhai_zhongbao_rl_12m",
            "rule_desc": "蓝海中保润楼12期",
            "rule_family": "蓝海中保润楼",
            "rule_content": "{\"name\":\"蓝海中保润楼12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanhai_zhongbao_rl\"}}",
        }
    ],
    "haier_changtai": [
        {
            "channel": "haier_changtai",
            "rule_code": "haier_changtai_12m",
            "rule_desc": "海尔昌泰12期",
            "rule_family": "海尔昌泰",
            "rule_content": "{\"name\":\"海尔昌泰12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"haier_changtai\"}}",
        }
    ],
    "zhongyuan_zhongbao": [
        {
            "channel": "zhongyuan_zhongbao",
            "rule_code": "zhongyuan_zhongbao_12m",
            "rule_desc": "中原中保12期",
            "rule_family": "中原中保",
            "rule_content": "{\"name\":\"中原中保12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongyuan_zhongbao\"}}",
        }
    ],
    "zhongbang_zhongji_h5": [
        {
            "channel": "zhongbang_zhongji_h5",
            "rule_code": "zhongbang_zhongji_h5_12m",
            "rule_desc": "众邦中际h512期",
            "rule_family": "众邦中际h5",
            "rule_content": "{\"name\":\"众邦中际h512期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongbang_zhongji_h5\"}}",
        }
    ],
    "tcl_zhongji": [
        {
            "channel": "tcl_zhongji",
            "rule_code": "tcl_zhongji_12m",
            "rule_desc": "TCL中际12期",
            "rule_family": "TCL中际",
            "rule_content": "{\"name\":\"TCL中际12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"tcl_zhongji\"}}",
        }
    ],
    "mengshang_zhongyi": [
        {
            "channel": "mengshang_zhongyi",
            "rule_code": "mengshang_zhongyi_12m",
            "rule_desc": "蒙商中裔12期",
            "rule_family": "蒙商中裔",
            "rule_content": "{\"name\":\"蒙商中裔12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"mengshang_zhongyi\"}}",
        }
    ],
    "zhongyuan_haoyue_rl": [
        {
            "channel": "zhongyuan_haoyue_rl",
            "rule_code": "zhongyuan_haoyue_rl_12m",
            "rule_desc": "中原昊悦润楼12期",
            "rule_family": "中原昊悦润楼",
            "rule_content": "{\"name\":\"中原昊悦润楼12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"zhongyuan_haoyue_rl\"}}",
        }
    ],
    "langfang_hengrun_qj": [
        {
            "channel": "langfang_hengrun_qj",
            "rule_code": "langfang_hengrun_qj_12m",
            "rule_desc": "廊坊恒润亲家12期",
            "rule_family": "廊坊恒润亲家",
            "rule_content": "{\"name\":\"廊坊恒润亲家12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"langfang_hengrun_qj\"}}",
        }
    ],
    "lanzhou_haoyue_zk3": [
        {
            "channel": "lanzhou_haoyue_zk3",
            "rule_code": "lanzhou_haoyue_zk3_12m",
            "rule_desc": "兰州昊悦zk3 12期",
            "rule_family": "兰州昊悦",
            "rule_content": "{\"name\":\"兰州昊悦zk3 12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanzhou_haoyue_zk3\"}}",
            "rule_product_code": "zk3",
        }
    ],
    "lanhai_zhongbao_hy": [
        {
            "channel": "lanhai_zhongbao_hy",
            "rule_code": "lanhai_zhongbao_hy_12m",
            "rule_desc": "蓝海中保哈银12期",
            "rule_family": "蓝海中保哈银",
            "rule_content": "{\"name\":\"蓝海中保哈银12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanhai_zhongbao_hy\"}}",
        }
    ],
    "lanhai_zhongbao_puan": [
        {
            "channel": "lanhai_zhongbao_puan",
            "rule_code": "lanhai_zhongbao_puan_12m",
            "rule_desc": "蓝海中保普安12期",
            "rule_family": "蓝海中保普安",
            "rule_content": "{\"name\":\"蓝海中保普安12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanhai_zhongbao_puan\"}}",
        }
    ],
    "yuanfengqianjingjing": [
        {
            "channel": "yuanfengqianjingjing",
            "rule_code": "yuanfengqianjingjing_0dc",
            "rule_desc": "元丰钱京京0笔兜底",
            "rule_family": "元丰钱京京-兜底",
            "rule_content": "{\"name\":\"元丰在贷0笔兜底\",\"rules\":[{\"name\":\"元丰在贷0笔兜底\",\"rule\":\"asset.periodType==\\'month\\' and assetExtend.totalDebtCount==0 \"}],\"output\":{\"key\":\"channel\",\"value\":\"yuanfengqianjingjing\"}}",
            "rule_activation_group": "yuanfengqianjingjing",
            "weight_first_route_status": "inactive",
        },
        {
            "channel": "yuanfengqianjingjing",
            "rule_code": "yuanfengqianjingjing_0",
            "rule_desc": "元丰钱京京0期总量",
            "rule_family": "元丰钱京京-兜底",
            "rule_content": "{\"name\":\"元丰钱京京总量\",\"rules\":[{\"name\":\"元丰钱京京总量\"}],\"output\":{\"key\":\"channel\",\"value\":\"yuanfengqianjingjing\"}}",
            "rule_type": "supply",
            "rule_activation_group": "",
            "rule_limit_type": "strict",
            "rule_weight": 0,
            "rule_allow_overflow_rate": 0,
            "rule_product_code": "",
            "weight_value": 0,
            "weight_status": "active",
            "weight_first_route_status": "active",
            "weight_second_route_status": "active"
        },
        {
            "channel": "yuanfengqianjingjing",
            "rule_code": "yuanfengqianjingjing_12m",
            "rule_desc": "元丰钱京京12期兜底",
            "rule_family": "元丰钱京京-兜底",
            "rule_content": "{\"name\":\"元丰钱京京12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12  \"}],\"output\":{\"key\":\"channel\",\"value\":\"yuanfengqianjingjing\"}}",
            "rule_activation_group": "yuanfengqianjingjing",
        }
    ],
    # "lanhai_guomao_tb": [
    #     {
    #         "channel": "lanhai_guomao_tb",
    #         "rule_code": "lanhai_guomao_tb_12m",
    #         "rule_desc": "蓝海国贸通宝12期",
    #         "rule_family": "蓝海国贸通宝",
    #         "rule_content": "{\"name\":\"蓝海国贸通宝12期\",\"rules\":[{\"name\":\"12期产品\",\"rule\":\"asset.periodType==\\'month\\' and asset.periodCount==12\"}],\"output\":{\"key\":\"channel\",\"value\":\"lanhai_guomao_tb\"}}",
    #     }
    # ]
}


invoked_api = {
    "tongrongmiyang": {
        "LoanApplyNew": ["/tongrongmiyang/tongrongmiyang/loanApply"],
        "LoanApplyQuery": ["/tongrongmiyang/tongrongmiyang/loanApplyQuery"],
        "PaymentWithdraw": [
            "/withdraw/balance",
            "/withdraw/autoWithdraw"
        ],
        "PaymentWithdrawQuery": ["/withdraw/query"],
        "ContractDown": ["/tongrongmiyang/tongrongmiyang/loanApplyQuery"],
        "PaymentTransfer": [
            "/withdraw/balance",
            "/withdraw/autoWithdraw"
        ],
        "PaymentTransferQuery": ["/withdraw/query"],
        "BondContractSign ": ["/tongrongmiyang/tongrongmiyang/bondTransfer"],
        "BondContractDown": ["/tongrongmiyang/tongrongmiyang/loanApplyQuery"],
    }
}

attachment = {
    "shoujin": [
        (30151, '个人信息使用授权书',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86042200207111432.pdf'),
        (30152, '首金-借款合同',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86042200207111432.pdf'),
        (30153, '首金-个人借款服务协议',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86042200207111432.pdf'),
        (30154, '个人征信授权书',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86042200207111432.pdf')
    ],
    "huabei_runqian": [
        (30791, '华北润乾保函',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30792, '华北润乾委托担保协议',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "longshangmiyang": [
        (30131, '龙商小贷-借款合同如皋智萃',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200212/SaveToCos/BIZ86234200212113837.pdf'),
        (30132, '龙商小贷-债转合同',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200212/SaveToCos/BIZ86239200212113839.pdf')
    ],
    "baijin": [
        (30102, "借款协议(我方签约版)-白金",
         "http://bizfiles-10000035.cossh.myqcloud.com/attachments/temp/baijin/ZZ_bj_0529_6qi6213loan_bee2063a2ea048b7ab547fb30071a792.pdf"),
        (30103, "白金-个人征信授权书", "http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ113378200529162356.pdf"),
        (30104, "白金-个人征信授权书-百行", "http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ113379200529162357.pdf"),
        (30105, "白金-授权委托书（三）", "http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ113379200529162357.pdf"),
        (30106, "白金-注册协议", "http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ113376200529162356.pdf"),
    ],
    "zhenjinfu": [
        (27, '技术服务协议',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86041200207111432.pdf'),
        (30121, '真金服-征信授权书(人行)',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86043200207111432.pdf'),
        (30122, '真金服-征信授权书(百行)',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86040200207111431.pdf'),
        (30123, '真金服-电子签章授权书',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86042200207111432.pdf')
    ],
    "shilong_siping": [
        (30171, '征信查询授权书-矢隆四平',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86043200207111432.pdf'),
        (30172, '借款合同-我方签约版',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86040200207111431.pdf'),
        (30173, '担保服务协议-矢隆四平',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86042200207111432.pdf'),
        (30174, '委托担保合同-矢隆四平',
         'http://contractsvrcostest-1251122539.cos.ap-shanghai.myqcloud.com/20200207/SaveToCos/BIZ86042200207111432.pdf')
    ],
    "yunxin_quanhu": [
        (30141, '征信授权文件（全互融通）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ110859200415230443.pdf'),
        (30142, '委托保证合同-云信全互', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ110857200415230442.pdf'),
        (
            30143, '云信全互-信托贷款合同-我方签约版云智',
            'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ108653200318111351.pdf'),
    ],
    "hami_tianshan": [
        (30181, '借款合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30182, '个人信息使用授权书-哈密天山', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "hami_tianshan_tianbang": [
        (30181, '借款合同', 'https://contractsvr.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30182, '个人信息使用授权书-哈密天山', 'https://contractsvr.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30710, '借款合同', 'http://rgcloud-biz-contract-prod.oss-cn-shanghai.aliyuncs.com/202012/09/S202012073510364670'
                        '433150/28/哈密天山借款合同78614722788091494417444720201209082833.pdf.zip'),
    ],
    "daxinganling_zhongyi": [
        (34500, '微神马（新）-个人征信信息查询授权书及个人信息使用授权书','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252964230111173025.pdf'),
        (34501, '微神马（新）-委托担保合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252964230111173025.pdf'),
        (34502, '微神马（新）-委托担保合同','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252964230111173025.pdf'),
        (34503, '微神马（新）-B1融担咨询服务合同（金融机构+外部融担）','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252964230111173025.pdf'),
        (34504, '微神马（新）-B2风险保障计划协议书（外部融担通用版）','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252964230111173025.pdf'),

    ],
    "qinnong": [
        (30401, '委托保证合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "qinnong_jieyi": [
        (30702, '秦农杰益-担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30703, '秦农杰益-委托担保协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "jingque_haikou": [
        (30720, '手动插入-mock测试',
         'http://paydayloandevv4-1251122539.cossh.myqcloud.com/20170725/ff79e74355a8370bb44b27f86ac85ae1.jpe'),
        (30721, '手动插入-mock测试',
         'http://paydayloandevv4-1251122539.cossh.myqcloud.com/20170725/ff79e74355a8370bb44b27f86ac85ae1.jpe'),
    ],
    "zhongke_lanzhou": [
        (30601, '兰州-个人消费性贷款电子协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30602, '兰州-委托代扣授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30603, '兰州-征信授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30604, '兰州-信息查询授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30605, '兰州-个人委托担保合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30606, '兰州-不可撤销担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "zhongke_hegang": [
        (30740, '鹤岗-信息使用授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30741, '鹤岗-借款合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30742, '鹤岗-征信授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30743, '鹤岗-委托担保合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30744, '鹤岗-不可撤销担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30745, '鹤岗-委托扣款协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30746, '鹤岗-借款凭证', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30747, '鹤岗-担保咨询合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),

    ],
    "mozhi_beiyin_zhongyi": [
        (30770, '墨智北银-中裔-委托担保协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30771, '墨智北银-中裔-委托担保协议补充协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30772, '墨智北银-中裔-担保贷后管理服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30773, '墨智北银-中裔-融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30774, '墨智北银-中裔-【线上C】融担咨询服务合同',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "beiyin_tianbang": [
        (31400, '北银天邦-委托担保协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "tieling_zhongyi": [
        (30730, '首金铁岭-借款协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30731, '首金铁岭-个人征信授权书（首金）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30732, '首金铁岭-个人征信授权书（银行）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "qinnong_dingfeng": [
        (30780, '秦农鼎丰-担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30781, '秦农鼎丰-委托担保协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "longjiang_daqin": [
        (30801, '大秦龙江-委托保证合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30802, '大秦龙江-担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30807, '大秦龙江-非学生承诺函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30808, '大秦龙江-授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30809, '大秦龙江-委托扣款服务三方协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30810, '大秦龙江-融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "hamitianbang_xinjiang": [
        (30181, '借款合同', 'https://contractsvr.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30182, '个人信息使用授权书-哈密天山', 'https://contractsvr.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30710, '借款合同', 'http://rgcloud-biz-contract-prod.oss-cn-shanghai.aliyuncs.com/202012/09/S202012073510364670'
                        '433150/28/哈密天山借款合同78614722788091494417444720201209082833.pdf.zip'),
    ],
    "mozhi_jinmeixin": [
        (31010, '墨智金美信-委托担保协议',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31011, '墨智金美信-委托担保协议补充协议',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31012, '墨智金美信-担保贷后管理服务合同',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31013, '墨智金美信-融资担保咨询服务合同',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31014, '墨智金美信-【线上B3】融担咨询服务合同',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31015, '智金美信-征信授权协议',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31016, '智金美信-【线上B4】融担咨询服务合同',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf')
    ],
    "lanzhou_haoyue": [
        (31100, '兰州昊悦-征信查询授权书-test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31101, '兰州昊悦-委托担保合同-test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30601, '兰州-个人消费性贷款电子协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30602, '兰州-委托代扣授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30603, '兰州-征信授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30604, '兰州-信息查询授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "lanzhou_dingsheng_zkbc2": [
        (30601, '兰州-个人消费性贷款电子协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30602, '兰州-委托代扣授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30603, '兰州-征信授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30604, '兰州-信息查询授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30605, '兰州-个人委托担保合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (30606, '兰州-不可撤销担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "siping_jiliang": [
        (31203, '委托担保合同-四平吉良', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31202, '担保服务协议-四平吉良', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31201, '征信授权协议-四平吉良', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31200, '借款协议-四平吉良-我方签约版', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "haishengtong_daqin": [
        (31300, '海胜通大秦-测试', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31301, '海胜通大秦-测试', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31302, '海胜通大秦-测试', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31303, '海胜通大秦-测试', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
    ],
    "yilian_dingfeng": [
        (31700, '亿联鼎丰-个人借款额度合同【我方签章版本】', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31715, '亿联鼎丰-个人信息查询授权书（银行）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31716, '亿联鼎丰-个人信息使用授权书（银行）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31703, '亿联鼎丰-个人征信客户授权书（银行）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31704, '亿联鼎丰-个人信查询和使用授权书（亲家）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31714, '亿联鼎丰-新个人借款借据（银行）【我方签章版本】', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31706, '亿联鼎丰-委托扣款协议（银行）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31708, '亿联鼎丰-委托保证合同（融担）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31709, '亿联鼎丰-担保函（银行）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),
        (31717, '亿联鼎丰-非学生承诺函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ206650220325043523.pdf'),

    ],
    "lanzhou_haoyue_qinjia": [
        (30504, '风险保障计划协议书（外部融担通用版）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ222065220606160957.pdf'),
        (30505, '融担咨询服务合同（金融机构+外部融担）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ222067220606160958.pdf'),
        (32005, '兰州昊悦(亲家)-个人消费性贷款电子协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ222076220606171344.pdf'),
        (32007, '兰州昊悦(亲家)-个人信息查询和使用授权书（亲家）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ222062220606144920.pdf'),
        (32008, '兰州昊悦(亲家)-委托保证合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ222066220606160958.pdf'),
        (32009, '兰州昊悦(亲家)-融担咨询服务合同（三方）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ222077220606172442.pdf'),
        (32011, '兰州昊悦(亲家)个人信用报告查询授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ222077220606172442.pdf'),
        (32012, '兰州昊悦(亲家)-个人信息查询及使用授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ222077220606172442.pdf')
    ],
    "zhongyuan_zunhao": [
        (33010, '众智融中原消金-委托扣款授权书(融担)', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224086220617143432.pdf'),
        (33006, '众智融中原消金-个人信息处理授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33007, '众智融中原消金-委托担保合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224087220617143433.pdf'),
        (33008, '众智融中原消金-B1-融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224088220617143433.pdf')

    ],
    "beiyin_daqin": [
        (33107, '北银大秦-【B】融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224086220617143432.pdf')
    ],
    "jinmeixin_daqin": [
        (30508, 'A—融担咨询服务合同 （金融机构+外部融担）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224086220617143432.pdf')
    ],
    "yixin_hengrun": [
        (33205, '宜信恒润-担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224086220617143432.pdf'),
        (33206, '宜信恒润-委托保证合同（融担）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (30505, '融担咨询服务合同（金融机构+外部融担）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224087220617143433.pdf'),
        (30508, 'A—融担咨询服务合同 （金融机构+外部融担）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224088220617143433.pdf'),
        (33504, '风险保障计划协议书（外部融担通用版）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224088220617143433.pdf')
    ],
    "jincheng_hanchen": [
        (31908, '锦程汉辰-融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224086220617143432.pdf'),
        (31906, '锦程汉辰-融资担保咨询服务合同【资方下载】', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224086220617143432.pdf')
    ],
    "jinmeixin_hanchen": [
        (33311, '金美信汉辰-融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224086220617143432.pdf')
    ],
    "yixin_rongsheng": [
        (33405, '宜信荣晟-担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224086220617143432.pdf'),
        (33406, '宜信荣晟-委托保证合同（融担）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33407, '宜信荣晟-B3融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33408, '宜信荣晟-B1融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
       ],
    "yumin_zhongbao": [
        (33501, '宜信荣晟-担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224086220617143432.pdf'),
        (33502, '宜信荣晟-委托保证合同（融担）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33503, '宜信荣晟-B3融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33506, '宜信荣晟-B1融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33505, '宜信荣晟-委托保证合同（融担）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33500, '宜信荣晟-B3融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33504, '宜信荣晟-B1融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33507, '宜信荣晟-B1融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
       ],
    "jiexin_taikang_xinheyuan": [
        (33605, '捷信泰康信合元-B1融资担保咨询服务合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
    ],
    "jiexin_taikang": [
        (33700, '捷信泰康-个人授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33701, '捷信泰康-额度授信合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
    ],
    "jinmeixin_hanchen_jf": [
        (33800, '金美信汉辰京发-消费金融借款合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33801, '金美信汉辰京发-综合授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33802, '金美信汉辰京发-委托扣款授权书1', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33803, '金美信汉辰京发-委托扣款授权书2', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33804, '金美信汉辰京发-金融信息服务授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (33805, '金美信汉辰京发-金融信息服务授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
    ],
    "lanhai_zhongshi_qj": [
        (34000, '蓝海中世亲家mock', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (34001, '蓝海中世亲家mock', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (34002, '蓝海中世亲家mock', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (34003, '蓝海中世亲家mock', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (34004, '蓝海中世亲家mock', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf'),
        (34005, '委托保证合同（我方签章）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ249575221128150426.pdf'),
        (34006, '个人借款合同（我方签章）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ249576221128150427.pdf'),
        (34011, '蓝海中世亲家-地域承诺函mock', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ249576221128150427.pdf'),
        (34012, '蓝海中世亲家-担保咨询服务合同（我方签章）mock', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ249576221128150427.pdf'),
    ],
    "zhenong_rongsheng": [
        (33900, '浙农荣晟-信息使用及账户划扣授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ224085220617143308.pdf')
    ],
    "changyin_mingdonghua_rl": [
        (34200, '长银明东华润楼-综合授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34201, '长银明东华润楼-个人贷款用途承诺书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34202, '长银明东华润楼-非学生身份承诺函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34203, '长银明东华润楼-数字证书授权使用协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34204, '长银明东华润楼-个人客户扣款授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
    ],
    "zhenxing_zhongzhixin_jx": [
        (34601, '振兴中智信-个人授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34602, '振兴中智信-捷信额度授信合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
    ],
     "hebei_wenshun_ts": [
        (34400, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34401, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34402, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34403, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34404, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34405, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34406, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf')
    ],
    "changyin_junxin": [
        (34800, '长银钧信-委托保证合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34801, '长银钧信-综合授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34802, '长银钧信-非在校学生承诺函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34803, '长银钧信-个人贷款用途承诺书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (34807, '长银钧信-个人客户扣款授权书（新）','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf')
    ],
    "weipin_zhongzhixin": [
        (34900, '唯品中智信-委托保证合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf')
    ],
    "hebei_jiahexing_ts": [
        (35000, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35001, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35002, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35003, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35004, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35005, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35006, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35007, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf')
    ],
    "hayin_zhongbao": [
        (35301, '哈银中保-个人信息授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35302, '哈银中保-个人征信授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35303, '哈银中保-非学生承诺函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35304, '哈银中保-个人借款额度合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35305, '哈银中保-账户委托扣款授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35306, '哈银中保-个人额度借款支用协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35307, '哈银中保-个人委托担保合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
    ],
    "weipin_hanchen_jf": [
        (35400, '唯品汉辰京发-金融信息服务授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35401, '唯品汉辰京发-委托扣款协议2', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35402, '唯品汉辰京发-委托保证合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf')
    ],
    "xiaomi_zhongji": [
        (35500, '小米中际-循环授信额度合同-资方未签章', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35501, '小米中际-个人征信授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35502, '小米中际-非学生承诺函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35503, '小米中际-个人消费贷款合同-资方未签章', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35509, '小米中际-test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf')
    ],
    "lanhai_zhongbao_rl": [
        (35601, '蓝海中保润楼-个人信息共享授权书（人行银行）', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35602, '蓝海中保润楼-三方信息授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35603, '蓝海中保润楼-借款人声明', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35604, '蓝海中保润楼-个人消费贷款借款合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35605, '蓝海中保润楼-担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35606, '蓝海中保润楼-委托划扣授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35607, '蓝海中保润楼-个人消费贷款额度合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35608, '蓝海中保润楼-委托保证合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
    ],
    "haier_changtai": [
        (35700, '海尔昌泰-征信授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35701, '海尔昌泰-消费信贷服务用户使用协议-资方未签章',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ249576221128150427.pdf'),
        (35702, '海尔昌泰-非学生承诺函',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35703, '海尔昌泰-借款合同-资方未签章',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ249576221128150427.pdf'),
        (35704, '海尔昌泰-委托担保合同',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (35705, '海尔昌泰-个人信息授权书',
         'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
    ],
    "zhongyuan_zhongbao": [  # 该资金方没有需要进件之后签约的合同
    ],
    "tcl_zhongji": [
        (36005, 'TCL中际-委托保证合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (36006, 'TCL中际-担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (36007, 'TCL中际-账户委托扣款授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf')
    ],
    "mengshang_zhongyi": [
            (37000, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (37001, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (37002, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (37003, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (37004, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (37009, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        ],
    "langfang_hengrun_qj": [
            (35200, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (35201, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (35202, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (35203, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (35204, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (35205, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (35206, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
            (35207, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        ],
    "lanzhou_haoyue_zk3": [
        (31101, 'test-兰州昊悦-不可撤销担保函', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (30601, 'test-兰州-个人消费性贷款电子协议', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (30604, 'test-兰州-信息查询授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (30603, 'test-兰州-征信授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37300, 'test-兰州-征信授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
    ],
    "lanhai_zhongbao_hy": [
        (37400, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37401, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37402, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37403, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37404, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37405, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37406, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37408, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
    ],
    "lanhai_zhongbao_puan":[
        (37100, '蓝海中保普安-小康贷授信额度合同', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37102, '蓝海中保普安-三方数据授权书', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37103, '蓝海中保普安-借款人申明','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37104, '蓝海中保普安-个人信用信息查询', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37105, '蓝海中保普安-个人信息授权书（融担）','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37106, '蓝海中保普安-委托划扣授权书（融担）','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37107, '蓝海中保普安-委托保证合同','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37108, '蓝海中保普安-担保函','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37101, '蓝海中保普安-小康贷借款合同','http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf')
    ],
    "yuanfengqianjingjing": [
        (37500, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37503, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
        (37504, 'test', 'http://contractsvr.testing.kuainiujinke.com/getdocs/BIZ252034221212153858.pdf'),
    ]


}

