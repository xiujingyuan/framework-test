import pytest
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
from biztest.function.global_gbiz.gbiz_global_check_function import check_wait_assetreverse_data
from biztest.function.global_gbiz.gbiz_global_db_function import update_all_channel_amount
from biztest.interface.gbiz_global.gbiz_global_interface import payment_callback


@pytest.mark.global_gbiz_thailand
@pytest.mark.global_gbiz_mexico
@pytest.mark.global_gbiz_philippines
@pytest.mark.global_gbiz_pakistan
@pytest.mark.global_gbiz_assetreverse
class TestAssetReverse(BaseTestCapital):
    def setup(self):
        super(TestAssetReverse, self).init()
        update_all_channel_amount()

    def test_asset_reverse(self):
        """
        发生冲正,执行CapitalAssetReverse后，资产状态置为void
        :param case:
        :return:
        """
        item_no, asset_info = self.asset_import_data()
        self.loan_to_success(item_no)
        payment_callback(asset_info, 3)
        check_wait_assetreverse_data(item_no, 14, "发生冲正,作废资产")
