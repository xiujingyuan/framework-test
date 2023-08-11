# @Time    : 2020/7/30 12:32 下午
# @Author  : yuanxiujing
# @File    : test_import_asset.py
# @Software: PyCharm
# -*- coding: utf-8 -*-
from foundation_test.function.dh.asset_sync.dh_check_function import *
from foundation_test.interface.dh.dh_interface import *
from foundation_test.util.db.db_util import DataBase
import foundation_test.config.dh.db_const as dc


class TestImportAsset(object):
    @classmethod
    def setup_class(cls):
        # env=1,country=china,environment=test
        # dc.init_dh_env(1, "china", "dev")
        dc.init_dh_env(dc.ENV, dc.COUNTRY, dc.ENVIRONMENT)

    @classmethod
    def teardown_method(cls):
        DataBase.close_connects()

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_import_asset
    @pytest.mark.dh_new_asset
    def test_new_asset(self):
        """
        新资产：第一次进件
        """
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')

        # asset表核对
        check_asset_data(item_no, data_info, 'repay')
        # 对比内外标识
        check_inner_outer(item_no, 'inner')
        # 还款计划核对
        check_transaction_data(overdue_days, item_no, data_info)
        # 债务人核对
        check_debtor_data(item_no, data_info)
        # 借款人信息核对
        check_individual_data(data_info)
        # 债务概览信息核对
        check_debtor_arrears_data(item_no, data_info, 'repay')
        # 债务人资产信息核对
        check_debtor_asset_data(item_no, data_info)
        # 资产与借款人的关联关系核对
        check_asset_ref_subject(item_no, data_info)
        time.sleep(2)
        # 最新跟进信息核对
        check_debtor_collect(item_no, data_info)

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_import_asset
    @pytest.mark.dh_payoff_asset
    def test_payoff_asset(self):
        """
        资产结清
        """
        overdue_days = 1
        # 导入一笔还款中资产
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        # 结清该笔资产
        payoff_item_no, payoff_data_info = asset_import(overdue_days, '草莓', '', 'payoff', item_no, data_info)
        # asset表核对
        check_asset_data(payoff_item_no, payoff_data_info, "payoff")
        # 对比内外标识
        check_inner_outer(payoff_item_no, "inner")
        # 还款计划核对
        check_transaction_data(overdue_days, payoff_item_no, payoff_data_info)
        # 债务概览信息核对
        check_debtor_arrears_data(payoff_item_no, payoff_data_info, "payoff")

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_import_asset
    @pytest.mark.dh_exchange_app
    def test_exchange_app(self):
        """
        导流
        """
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '香蕉', '', 'repay', '', '')
        exchange_item_no, exchange_data_info = asset_import(overdue_days, '草莓', '草莓', 'repay', item_no, data_info)
        # asset表核对
        check_asset_data(exchange_item_no, exchange_data_info, "repay")
        # 债务人核对
        check_debtor_data(exchange_item_no, exchange_data_info)
        # 债务概览信息核对
        check_debtor_arrears_data(exchange_item_no, exchange_data_info, 'repay')
        # 债务人资产信息核对
        check_debtor_asset_data(exchange_item_no, exchange_data_info)

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_import_asset
    @pytest.mark.dh_void_asset
    def test_void_asset(self):
        """
        作废资产
        """
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        void_item_no, void_data_info = asset_import(overdue_days, '草莓', '', 'void', item_no, data_info)
        # asset表核对
        check_void_or_writeoff_asset(void_item_no, 'void')

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_import_asset
    @pytest.mark.dh_writeoff_asset
    def test_writeoff_asset(self):
        """
        注销资产
        """
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        void_item_no, void_data_info = asset_import(overdue_days, '草莓', '', 'writeoff', item_no, data_info)
        # asset表核对
        check_void_or_writeoff_asset(void_item_no, 'writeoff')


if __name__ == '__main__':
    pytest.main(["-s", "test_import_asset.py", "--env=fox", "--environment=test"])
