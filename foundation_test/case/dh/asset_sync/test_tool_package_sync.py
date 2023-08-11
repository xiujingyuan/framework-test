# @Time    : 2020/9/25 5:12 下午
# @Author  : yuanxiujing
# @File    : test_tool_package_sync.py
# @Software: PyCharm
from foundation_test.function.dh.asset_sync.dh_check_function import check_tool_package, del_tool_package
from foundation_test.interface.dh.dh_interface import sync_tool_package
from foundation_test.util.db.db_util import DataBase, pytest
import foundation_test.config.dh.db_const as dc


class TestToolPackageSync(object):
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
    @pytest.mark.dh_tool_package_sync
    @pytest.mark.dh_sync_tool_package
    def test_sync_tool_package(self):
        # 同步工具包
        app_name = "草莓"
        tool_app_name = "草莓"
        channel = "官方"
        system = "iOS"
        status = 1
        # 同步工具包前，先清除已有
        del_tool_package()
        sync_tool_package(app_name, tool_app_name, channel, system, status)
        # asset_tool_package表资产工具包
        check_tool_package(app_name, tool_app_name, channel, system, status)

