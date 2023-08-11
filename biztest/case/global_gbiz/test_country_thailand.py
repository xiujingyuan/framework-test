from biztest.function.global_gbiz.gbiz_global_check_function import check_asset_data
from biztest.interface.gbiz_global.gbiz_global_interface import asset_import, asset_import_noloan
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_info_by_item_no, update_all_channel_amount
from biztest.config.global_gbiz.global_gbiz_kv_config import update_grouter_channel_change_config, \
    update_gbiz_capital_channel, update_gbiz_capital_channel_user_cancel
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element_global


@pytest.mark.global_gbiz_thailand
class TestCountryThailand(BaseTestCapital):
    def init(self):
        super(TestCountryThailand, self).init()
        update_grouter_channel_change_config()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    params = ["channel", "source_type", "count", "day", "amount", "rulecode", "late_num", "fees"]
    values = [("picocp_ams1", "game_bill", 4, 7, 500000, "", "late0.098%", {"interest": 35.77}),
              ("picoqr_ams1", "game_bill", 4, 7, 500000, "picoqr_ams1_bangkok_0", "late0.098%", {"interest": 35.77}),
              ("picoqr_ams1", "game_bill", 4, 7, 500000, "picoqr_ams1_saraburi_0", "late0.098%", {"interest": 35.77}),
              ("picocp_ams2", "game_bill", 1, 15, 300000, "", "late0.098%", {"interest": 35.77}),  # 这个资金方现在被限制只能放1期的
              ("picoqr_ams2", "game_bill", 1, 14, 300000, "", "late0.098%", {"interest": 35.77}),  # 这个资金方现在被限制只能放1期的
              ("pico_bangkok", "game_bill", 4, 7, 500000, "", "late0.098%", {"interest": 35.77})
              ]

    @pytest.mark.parametrize(params, values)
    def test_thailand_loan_success(self, case, channel, source_type, count, day, amount, rulecode, late_num, fees):
        update_gbiz_capital_channel(channel)
        element = get_four_element_global(id_num_begin='110')
        item_no, asset_info = asset_import(channel, count, day, "day", amount, "tha", "THA053", source_type, element,
                                           rlue_code=rulecode, fees=fees, late_num=late_num)
        self.loan_to_success(item_no)

        # 放款数据检查
        asset = get_asset_info_by_item_no(item_no)
        asset_info['data']['asset']['cmdb_product_number'] = asset[0]["asset_cmdb_product_number"]
        check_asset_data(asset_info)
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
        # 判断是否有小单
        if item_no_noloan:
            self.noloan_to_success(item_no_noloan)

    params = ["channel", "source_type", "count", "day", "rulecode", "late_num", "fees"]
    values = [
        ("picoqr_ams1", "game_bill", 3, 7, "picoqr_ams1_saraburi_0", "late0.098%", {"interest": 35.77}),
        ("picocp_ams1", "game_bill", 3, 7, "", "late0.098%", {"interest": 35.77}),
        ("pico_bangkok", "game_bill", 1, 7, "pico_bangkok_0", "late0.098%", {"interest": 35.77}),
    ]

    @pytest.mark.parametrize(params, values)
    def test_thailand_loan_cancel(self, case, channel, source_type, count, day, rulecode, late_num, fees):
        element = get_four_element_global(id_num_begin='110')
        if channel == 'picocp_ams1':
            update_gbiz_capital_channel(channel)
            item_no, asset_info = asset_import(channel, count, day, "day", 500000, "tha", "THA053", source_type,
                                               element, rlue_code=rulecode, fees=fees, late_num=late_num)
            self.loan_cancel_01(item_no)

        if channel == 'picoqr_ams1':
            update_gbiz_capital_channel_user_cancel(channel)
            item_no, asset_info = asset_import(channel, count, day, "day", 500000, "tha", "THA053", source_type,
                                               element, rlue_code=rulecode, fees=fees, late_num=late_num)
            self.loan_cancel_02(item_no)

        # if channel == 'pico_bangkok':
        #     update_gbiz_capital_channel(channel)
        #     item_no, asset_info = asset_import(channel, count, day, "day", 500000, "tha", "THA053", source_type,
        #                                        element, rlue_code=rulecode, fees=fees, late_num=late_num)
        #     self.loan_cancel_03(item_no)
