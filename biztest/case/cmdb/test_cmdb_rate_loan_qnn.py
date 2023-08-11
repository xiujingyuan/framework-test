from biztest.interface.cmdb.cmdb_interface import *
from biztest.function.cmdb.cmdb_common_function import *
from biztest.util.tools.tools import get_item_no



asset_info = {
    'data': {
        'asset': {
            'item_no': get_item_no(),
            'amount': 0,
            'period_count': 6,
            'period_term': '1',
            'period_type': 'month',
            'loan_channel': 'qnn',
            'source_type': 'youxi_bill',
            'cmdb_product_number': 'qnn_lm_6_1m_20190103'
        }
    }
}

cacle_rule_dsq = {
    "comprehensive_interest": {
        "name": "年化综合息费",
        "计算方式": "等额本息",
        "计算规则": 0.36},
    "qnn_24": {
        "name": "钱牛牛_24",
        "计算方式": "等额本息",
        "计算规则": 0.24},
    "capital_cost": {
        "name": "资方成本费用",
        "计算方式": "等额本息",
        "计算规则": 0.16},
    "interest": {
        "name": "利息",
        "计算方式": "等额本息",
        "计算规则": 0.10},
    "service": {
        "name": "资方服务费",
        "计算方式": "等额本息差额",
        "计算规则": (0.16, 0.10)},
    "after_loan_manage": {
        "name": "贷后管理费",
        "计算方式": "等额本息差额",
        "计算规则": (0.24, 0.16)},
    "technical_service": {
        "name": "技术服务费",
        "计算方式": "倒减",
        "计算规则": ("comprehensive_interest", "principal", "interest", "after_loan_manage", "service")}
}

cacle_rule_cm = {
    "comprehensive_interest": {
        "name": "年化综合息费",
        "计算方式": "等额本息",
        "计算规则": 0.36},
    "capital_cost": {
        "name": "资方成本费用",
        "计算方式": "等额本息",
        "计算规则": 0.16},
    "interest": {
        "name": "利息",
        "计算方式": "等额本息",
        "计算规则": 0.10},
    "service": {
        "name": "资方服务费",
        "计算方式": "等额本息差额",
        "计算规则": (0.16, 0.10)},
    "after_loan_manage": {
        "name": "贷后管理费",
        "计算方式": "倒减",
        "计算规则": ("comprehensive_interest", "principal", "interest", "service")}
}

class TestCmdbRateLoanQnn:

    def test_qnn_6_function(self):
        count = 6
        amount_list = [2000, 3000, 3500, 6000, 8000]
        cmdb_product_number = "qnn_lm_6_1m_20190103"
        for amount in amount_list:
            asset_info['data']['asset']['amount'] = amount
            asset_info['data']['asset']['period_count'] = count
            asset_info['data']['asset']['cmdb_product_number'] = cmdb_product_number

            # 先获取cmdb的费率
            rate_info = cmdb_rate_loan_calculate_v6(asset_info)
            # 自己计算费率
            cacle_info = cacle_v1(amount, count, cacle_rule_dsq)
            # 进行对比
            check_fee_info(rate_info, cacle_info)

    def test_qnn_3_function(self):
        count = 3
        amount_list = [2000, 3000, 3500, 6000, 8000]
        cmdb_product_number = "qnn_lm_3_1m_20190103"
        for amount in amount_list:
            asset_info['data']['asset']['amount'] = amount
            asset_info['data']['asset']['period_count'] = count
            asset_info['data']['asset']['cmdb_product_number'] = cmdb_product_number

            # 先获取cmdb的费率
            rate_info = cmdb_rate_loan_calculate_v6(asset_info)
            # 自己计算费率
            cacle_info = cacle_v1(amount, count, cacle_rule_dsq)
            # 进行对比
            check_fee_info(rate_info, cacle_info)

    def test_cm_qnn_6_function(self):
        count = 6
        amount_list = [2000, 3000, 3500, 6000, 8000]
        cmdb_product_number = "cm_qnn_lm_6_1m_20191106"
        for amount in amount_list:
            asset_info['data']['asset']['amount'] = amount
            asset_info['data']['asset']['period_count'] = count
            asset_info['data']['asset']['source_type'] = 'lieyin_bill'
            asset_info['data']['asset']['cmdb_product_number'] = cmdb_product_number

            # 先获取cmdb的费率
            rate_info = cmdb_rate_loan_calculate_v6(asset_info)
            # 自己计算费率
            cacle_info = cacle_v1(amount, count, cacle_rule_cm)
            # 进行对比
            check_fee_info(rate_info, cacle_info)
