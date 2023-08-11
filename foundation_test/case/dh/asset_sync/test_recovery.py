# @Time    : 2020/9/22 2:41 下午
# @Author  : yuanxiujing
# @File    : test_recovery.py
# @Software: PyCharm
from foundation_test.function.dh.asset_sync.dh_check_function import check_asset_summary_recovery, check_asset_period_recovery, check_collect_recovery
from foundation_test.interface.dh.dh_interface import *
from foundation_test.util.db.db_util import DataBase
from foundation_test.util.log.log_util import logger
import foundation_test.config.dh.db_const as dc


class TestRecovery(object):
    @classmethod
    def setup_class(cls):
        # env=1,country=china,environment=test
        # dc.init_dh_env(1, "china", "dev")
        dc.init_dh_env(dc.ENV, dc.COUNTRY, dc.ENVIRONMENT)

    @classmethod
    def teardown_method(cls):
        DataBase.close_connects()

    """
    分3种情况
    1、逾期期次部分还款----overdue_repay_period_part----第1期息费全还、本金部分还款，2、3不还
    2、逾期期次全部还款----overdue_repay_period_payoff----第1期本息费全还，2、3不还
    3、逾期期次+非逾期期次----overdue_repay_all_payoff----1、2、3本息费全部还款
    假设第1期逾期，2、3未逾期
    """
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_recovery
    @pytest.mark.dh_repay_period_part
    def test_repay_period_part(self):
        """
        1、逾期期次部分还款----overdue_repay_period_part----第1期息费全还、本金部分还款，2、3不还
        """
        # 回款前先导入一笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        # 回款
        repay_date = biz_recovery(overdue_days, item_no, "repay", "overdue_repay_period_part", False, False)
        # 检查总回款asset_summary_recovery表
        check_asset_summary_recovery(item_no, repay_date, "repay", "overdue_repay_period_part", False)
        # 检查期次回款asset_period_recovery表
        check_asset_period_recovery(item_no, "overdue_repay_period_part", repay_date)

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_recovery
    @pytest.mark.dh_repay_period_payoff
    def test_repay_period_payoff(self):
        """
        1、逾期期次全部还款----overdue_repay_period_payoff----第1期本息费全还，2、3不还
        """
        # 回款前先导入一笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        # 回款
        repay_date = biz_recovery(overdue_days, item_no, "payoff", "overdue_repay_period_payoff", False, False)
        print("repay_date is ", repay_date)
        # 检查总回款asset_summary_recovery表
        check_asset_summary_recovery(item_no, repay_date, "repay", "overdue_repay_period_payoff", False)
        # 检查期次回款asset_period_recovery表
        check_asset_period_recovery(item_no, "overdue_repay_period_payoff", repay_date)

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_recovery
    @pytest.mark.dh_repay_all_payoff
    def test_repay_all_payoff(self):
        """
        1、逾期期次+非逾期期次----overdue_repay_all_payoff----1、2、3本息费全部还款
        """
        # 回款前先导入一笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        # 回款
        repay_date = biz_recovery(overdue_days, item_no, "payoff", "overdue_repay_all_payoff", False, False)
        # 检查总回款asset_summary_recovery表
        check_asset_summary_recovery(item_no, repay_date, "payoff", "overdue_repay_all_payoff", False)
        # 检查期次回款asset_period_recovery表
        check_asset_period_recovery(item_no, "overdue_repay_all_payoff", repay_date)

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_recovery
    @pytest.mark.dh_repay_inverse
    def test_repay_inverse(self):
        """
        1、第1期本息费逆还款
        """
        # 回款前先导入一笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        # 回款
        # 等资产同步消费完成，才能开始回款
        repay_date = biz_recovery(overdue_days, item_no, "repay", "", True, False)
        # 检查总回款asset_summary_recovery表
        check_asset_summary_recovery(item_no, repay_date, "repay", "", True)
        # 检查期次回款asset_period_recovery表
        check_asset_period_recovery(item_no, "", repay_date)

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_recovery
    @pytest.mark.dh_repay_after_unsigned
    def test_repay_after_unsigned(self):
        """
        1、案件撤案后，T+1日回款，不计入催员回款
        """
        # 回款前先导入一笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        # 获取debtor_id，分案给催员秋分
        da_info = get_debtor_asset_by_item_no(item_no)
        debtor_id = da_info[0]['debtor_id']
        # 分案
        assign_asset(debtor_id)
        # 撤案
        unsigned_asset(debtor_id)
        # 回款
        # 等资产同步消费完成，才能开始回款
        repay_date = biz_recovery(overdue_days, item_no, "repay", "", False, True)
        # 检查催收员关联逾期催回表collect_recovery表
        check_collect_recovery(item_no, repay_date, True)

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_recovery
    @pytest.mark.dh_repay_equal_unsigned_date
    def test_repay_equal_unsigned_date(self):
        """
        1、还款时间已撤案，且 撤案时间和还款时间在同一天，计入催员回款
        """
        # 回款前先导入一笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        # 获取debtor_id，分案给催员秋分
        da_info = get_debtor_asset_by_item_no(item_no)
        logger.info("item_no=%s,da_info=%s" % (item_no, da_info))
        debtor_id = da_info[0]['debtor_id']
        # 分案
        assign_asset(debtor_id)
        # 撤案
        unsigned_asset(debtor_id)
        # 回款
        # 等资产同步消费完成，才能开始回款
        repay_date = biz_recovery(overdue_days, item_no, "repay", "", False, False)
        # 检查催收员关联逾期催回表collect_recovery表
        check_collect_recovery(item_no, repay_date, False)

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_asset_sync
    @pytest.mark.dh_recovery
    @pytest.mark.dh_repay_before_unsigned
    def test_repay_before_unsigned(self):
        """
        1、还款时间之前没有撤案，计入催员回款
        """
        # 回款前先导入一笔资产
        overdue_days = 1
        item_no, data_info = asset_import(overdue_days, '草莓', '', 'repay', '', '')
        # 获取debtor_id，分案给催员秋分
        da_info = get_debtor_asset_by_item_no(item_no)
        debtor_id = da_info[0]['debtor_id']
        # 分案
        assign_asset(debtor_id)
        # 回款
        # 等资产同步消费完成，才能开始回款
        repay_date = biz_recovery(overdue_days, item_no, "repay", "", False, False)
        # 检查催收员关联逾期催回表collect_recovery表
        check_collect_recovery(item_no, repay_date, False)


if __name__ == '__main__':
    pytest.main(["-s", "test_recovery.py", "--env=fox", "--environment=test"])
