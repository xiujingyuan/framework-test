# @Time    : 2020/9/18 2:59 下午
# @Author  : yuanxiujing
# @File    : test_refresh_debtor_arrears.py
# @Software: PyCharm
from foundation_test.function.dh.asset_sync.dh_check_function import *
from foundation_test.interface.dh.dh_interface import *
from foundation_test.util.db.db_util import DataBase
import foundation_test.config.dh.db_const as dc


class TestRefreshDebtorArrears(object):
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
    @pytest.mark.dh_refresh_debtor_arrears
    @pytest.mark.dh_normal_refresh_arrears
    def test_normal_refresh_arrears(self):
        """
        债务下存在多笔逾期中资产，刷新债务概览
        """
        # 1、同债务下导入两笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        item_no2, data_info2 = asset_import(overdue_days, '草莓', '', 'repay', '', data_info)
        # 2、修改债务概览金额
        asset_info = get_asset_info_by_item_no(item_no2)
        asset_customer = asset_info[0]["original_customer_id"]
        d_enc_id_num = data_info2['borrower']['enc_individual_idnum']
        set_arrears_amount(asset_customer, d_enc_id_num)
        d_info = get_debtor_info(asset_customer, d_enc_id_num)
        # 3、请求债务概览刷新接口
        refresh_debtor_arrears(asset_customer, d_enc_id_num, d_info[0]["id"])
        # 4、债务概览信息核对
        check_debtor_arrears_data(item_no2, data_info2, 'repay')

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_refresh_debtor_arrears
    @pytest.mark.dh_exist_stop_asset_refresh_arrears
    def test_exist_stop_asset_refresh_arrears(self):
        """
        债务下存在停催中资产，刷新债务概览
        """
        # 1、同债务下导入两笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        item_no2, data_info2 = asset_import(overdue_days, '草莓', '', 'repay', '', data_info)
        # 2、修改一笔资产为停催
        set_asset_inner_outer(item_no, 'stop')
        # 3、请求债务概览刷新接口，先获取债务人id
        asset_info = get_asset_info_by_item_no(item_no2)
        asset_customer = asset_info[0]["original_customer_id"]
        d_enc_id_num = data_info2['borrower']['enc_individual_idnum']
        set_arrears_amount(asset_customer, d_enc_id_num)
        d_info = get_debtor_info(asset_customer, d_enc_id_num)
        refresh_debtor_arrears(asset_customer, d_enc_id_num, d_info[0]["id"])
        time.sleep(2)
        # 4、债务概览信息核对
        check_debtor_arrears_data(item_no2, data_info2, 'repay')

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_refresh_debtor_arrears
    @pytest.mark.dh_exist_freeze_asset_refresh_arrears
    def test_exist_freeze_asset_refresh_arrears(self):
        """
        债务下存在冻结中资产，刷新债务概览
        """
        # 1、同债务下导入两笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        item_no2, data_info2 = asset_import(overdue_days, '草莓', '', 'repay', '', data_info)
        # 2、修改一笔资产为冻结
        set_asset_inner_outer(item_no, 'freeze')
        set_asset_freeze(item_no)
        # 3、请求债务概览刷新接口，先获取债务人id
        asset_info = get_asset_info_by_item_no(item_no2)
        asset_customer = asset_info[0]["original_customer_id"]
        d_enc_id_num = data_info2['borrower']['enc_individual_idnum']
        set_arrears_amount(asset_customer, d_enc_id_num)
        d_info = get_debtor_info(asset_customer, d_enc_id_num)
        refresh_debtor_arrears(asset_customer, d_enc_id_num, d_info[0]["id"])
        # 4、债务概览信息核对
        check_debtor_arrears_data(item_no2, data_info2, 'repay')

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_refresh_debtor_arrears
    @pytest.mark.dh_exist_freeze_debtor_refresh_arrears
    def test_exist_freeze_debtor_refresh_arrears(self):
        """
        债务人冻结，刷新债务概览
        """
        # 1、导入资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        # 2、修改债务人、资产为冻结
        set_asset_inner_outer(item_no, 'freeze')
        set_asset_freeze(item_no)
        asset_info = get_asset_info_by_item_no(item_no)
        asset_customer = asset_info[0]["original_customer_id"]
        d_enc_id_num = data_info['borrower']['enc_individual_idnum']
        d_enc_name = data_info['borrower']['enc_individual_name']
        d_enc_tel = data_info['borrower']['enc_individual_tel']
        set_asset_borrower_freeze(asset_customer, d_enc_name, d_enc_tel, d_enc_id_num)
        # 3、请求债务概览刷新接口，先获取债务概览的刷新时间
        d_info = get_debtor_info(asset_customer, d_enc_id_num)
        refresh_debtor_arrears(asset_customer, d_enc_id_num, d_info[0]["id"])
        # 4、获取接口请求后，债务概览的刷新时间
        after_das_info = get_debtor_arrears_info(asset_customer, d_enc_id_num)
        after_refresh_status = after_das_info[0]["status"]
        after_refresh_asset_count = after_das_info[0]["asset_count"]
        # 5、对比债务概览。债务人冻结，债务人名下资产全被冻结，债务概览统计到的有效资产应是0
        Assert.assert_equal("payoff", after_refresh_status,
                            '债务概览状态验证错误！预期：payoff，实际：%s' % after_refresh_status)
        Assert.assert_equal(0, after_refresh_asset_count,
                            '债务案件数量验证错误！预期：0，实际：%s' % after_refresh_asset_count)
