from biztest.config.gbiz.gbiz_tongrongqianjingjing_config import update_gbiz_capital_tongrongqianjingjing
from biztest.function.gbiz.gbiz_common_function import init_capital_plan
from biztest.function.gbiz.gbiz_db_function import update_router_cp_amount_all_to_zero, update_all_channel_amount, \
    update_asset_create_time, update_task_by_item_no_task_type
from biztest.interface.gbiz.gbiz_interface import asset_import
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.util.msg.msg import GbizMsg
from biztest.util.task.task import GbizTask
import pytest
from biztest.util.tools.tools import get_four_element


class TestChangeCapital(object):
    """
        gbiz_changecapital
        author: zhimengxue
        date: 20210114
        """
    task = GbizTask()
    msg = GbizMsg()

    @classmethod
    def setup_class(cls):
        init_capital_plan()
        update_grouter_channel_change_config()
        update_gbiz_capital_tongrongqianjingjing()
        update_gbiz_capital_huabei_runqian()
        update_gbiz_capital_hamitianbang_xinjiang()

    @classmethod
    def teardown_class(cls):
        init_capital_plan()

    # @pytest.mark.gbiz_changecapital
    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.parametrize("count", [12])
    # def test_changecapital_success(self, count):
    #     """ 一笔资产连续因不同原因切换资金方成功的case
    #                     """
    #     # 1、【因为未开户切换资金方成功】-weishenma_daxinganling切换tongrongmiyang
    #     super(TestChangeCapital, self)
    #     self.channel = "jinmeixin_hanchen"
    #     self.capital_mock = WeishenmaDaxinganlingMock(gbiz_mock)
    #     update_weishenma_daxinganling_paydayloan()
    #     update_grouter_weishenma_daxinganling_paydayloan()
    #     # 避免因为金额不足脚本失败，先将所有资金方的金额恢复为有值再执行任务
    #     update_all_channel_amount()
    #     # 微神马进件gbiz因为开户超时而canloan失败
    #     self.four_element = get_four_element()
    #     item_no, asset_info = asset_import(self.channel, self.four_element, count, 8000, "香蕉")
    #     item_no_old = (asset_info['data']['asset']['item_no'])
    #     self.task.run_task(item_no_old, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no_old, "AssetImportSync")
    #     self.task.run_task(item_no_old, "AssetImportVerify", excepts={"code": 0})
    #     # 将资产创建时间变更，使资产canloan可以开户超时而失败
    #     update_asset_create_time(item_no_old)
    #     self.task.run_task(item_no_old, "ApplyCanLoan", excepts={"code": 0})
    #
    #     # 2、【量不足切换资金方】-tongrongqianjingjing切换huabei_runqian
    #     capital_channel1 = 'tongrongqianjingjing'
    #     update_all_channel_amount()
    #     update_router_capital_plan_amount_all_to_zero(capital_channel1)
    #     # 打开切换资金方任务
    #     check_wait_change_capital_data(item_no_old, 4, self.channel + "->资方校验失败: 校验用户账户状态必须为成功: 用户未开户;")
    #     self.task.run_task(item_no_old, "ChangeCapital", excepts={"code": 0})
    #     self.msg.run_msg(item_no_old, "AssetChangeLoanChannelMQ", excepts={"code": 0})
    #     self.task.run_task(item_no_old, "AssetAutoImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no_old, "AssetAutoImport", excepts={"code": 0})
    #     wait_task_appear(item_no, "AssetImport")
    #     self.task.run_task(item_no_old, "AssetImport", excepts={"code": 0})
    #     self.task.run_task(item_no_old, "AssetImportVerify", excepts={"code": 0})
    #     # 修改目标资金方金额也为0，才能canloan失败切换资金方，以下方法是把所有资金方金额改为0 ，因为这个方法现成的直接复用
    #     update_router_cp_amount_all_to_zero()
    #     self.task.run_task(item_no_old, "ApplyCanLoan", excepts={"code": 0})
    #
    #     # 3、【共债切换资金方】-huabei_runqian切换hamitianbang_xinjiang失败
    #     capital_channel2 = 'jiexin_taikang_xinheyuan'
    #     update_all_channel_amount()
    #     update_router_capital_plan_amount_all_to_zero(capital_channel2)
    #     # 打开切换资金方任务
    #     check_wait_change_capital_data(item_no_old, 4, "tongrongqianjingjing->校验资金量失败;")
    #     self.task.run_task(item_no_old, "ChangeCapital", excepts={"code": 0})
    #     self.msg.run_msg(item_no_old, "AssetChangeLoanChannelMQ", excepts={"code": 0})
    #     self.task.run_task(item_no_old, "AssetAutoImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no_old, "AssetAutoImport", excepts={"code": 0})
    #     wait_task_appear(item_no, "AssetImport")
    #     self.task.run_task(item_no_old, "AssetImport", excepts={"code": 0})
    #     self.task.run_task(item_no_old, "AssetImportVerify", excepts={"code": 0})
    #     # 提前进件一笔华北的资产，以便华北的canloan校验失败
    #     item_no, asset_info = asset_import(capital_channel2, self.four_element, count, 8000, "香蕉")
    #     item_no_new = (asset_info['data']['asset']['item_no'])
    #     self.task.run_task(item_no_new, "AssetImport", excepts={"code": 0})
    #     self.task.run_task(item_no_new, "AssetImportVerify", excepts={"code": 0})
    #     # 期望切换到哈密天邦新疆成功 --哈密天邦新疆取消了地区校验规则，所以可以切成功
    #     capital_channel3 = 'hamitianbang_xinjiang'
    #     update_all_channel_amount()
    #     update_router_capital_plan_amount_all_to_zero(capital_channel3)
    #     self.task.run_task(item_no_old, "ApplyCanLoan", excepts={"code": 0})
    #     update_task_by_item_no_task_type(item_no_old, "ChangeCapital", task_status="open")
    #     self.task.run_task(item_no_old, "ChangeCapital", excepts={"code": 0})
    #     # check_wait_assetvoid_data(item_no_old, code=12, message=capital_channel3+"->资方校验失败: 校验地区信息只能包含新疆地区;")
    #     # 恢复所有资金方的金额
    #     update_all_channel_amount()

    @pytest.mark.gbiz_changecapital
    @pytest.mark.gbiz_auto_test
    @pytest.mark.parametrize("count", [6, 12])
    def test_changecapital_fail_to_void(self, count):
        """ 因为没有可用资金方而在切换资金方时取消
                """
        four_element = get_four_element()
        item_no, asset_info = asset_import("tongrongqianjingjing", four_element, count, 8000, "草莓")
        # 把所有资金方的量设置为0
        update_router_cp_amount_all_to_zero()
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        update_asset_create_time(item_no)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # check_wait_change_capital_data(item_no, 4, "进件,路由系统返回空")
        # 判断切换资金方任务的状态并执行切换资金方之后生成取消任务
        update_task_by_item_no_task_type(item_no, "ChangeCapital", task_status="open")
        self.task.run_task(item_no, "ChangeCapital", excepts={"code": 1})
        check_wait_assetvoid_data(item_no, code=12, message="切资方,路由系统返回空")
        # 修改取消任务的状态
        self.task.run_task(item_no, "AssetVoid", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetGrantCancelNotifyMQV2", excepts={"code": 0})
        # 恢复所有资金方的金额
        update_all_channel_amount()


if __name__ == "__main__":
    pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/qnn_lm.py", "--env=9"])
