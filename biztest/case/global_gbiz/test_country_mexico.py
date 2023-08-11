from biztest.function.global_gbiz.gbiz_global_common_function import run_terminated_task, init_capital_plan
from biztest.interface.gbiz_global.gbiz_global_interface import asset_import
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
from biztest.function.global_gbiz.gbiz_global_check_function import check_asset_data, check_wait_change_capital_data
from biztest.config.global_gbiz.global_gbiz_kv_config import update_gbiz_capital_channel
import pytest
from biztest.function.global_gbiz.gbiz_global_db_function import update_all_channel_amount
from biztest.util.tools.tools import get_four_element_global


@pytest.mark.global_gbiz_mexico
class TestCountryMexico(BaseTestCapital):
    def init(self):
        super(TestCountryMexico, self).init()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    params = ["channel", "source_type", "count", "day", "late_num", "fees"]
    values = [
        ("mangguo", "pl01", 1, 7, "late5%", {"fin_service": 30.00, "interest": 36.00}),
        ("mangguo", "pl01", 1, 7, "late5%", {"fin_service": 54.00, "interest": 36.00})
    ]

    @pytest.mark.parametrize(params, values)
    def test_mexico_loan_success(self, case, channel, source_type, count, day, late_num, fees):
        update_gbiz_capital_channel(channel)
        element = get_four_element_global()
        item_no, asset_info = asset_import(channel, count, day, "day", 50000, "mex", "maple", source_type, element,
                                           fees=fees, late_num=late_num)
        self.loan_to_success(item_no)
        check_asset_data(asset_info)
