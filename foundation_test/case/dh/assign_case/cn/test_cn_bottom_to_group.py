from foundation_test.function.dh.assign_case.assign_check_function import *
from foundation_test.function.dh.assign_case.assign_db_function import update_unassigned_cases
from foundation_test.function.dh.assign_case.assign_get_data import get_assign_info
from foundation_test.util.db.db_util import DataBase
from foundation_test.util.tools.tools import *
import foundation_test.config.dh.db_const as dc


class TestCnBottomToGroup(object):
    #
    # 分案到组：BASE_COMMON_TO_GROUP，直接分到组，基础的分案到组方式,最终分到组的方式是直接分到组
    # 分案到人：AVG_NUM，数量均分
    #
    @classmethod
    def setup_method(cls):
        # env=1,country=china,environment=test
        dc.init_dh_env(dc.ENV, dc.COUNTRY, dc.ENVIRONMENT)
        # dc.init_dh_env(1, "china", "dev")
        LogUtil.log_info("#### 当前环境env=%s，country=%s，environment=%s"
                         % (dc.ENV, dc.COUNTRY, dc.ENVIRONMENT))
        # 导入数据前，先清空库中符合条件的资产，防止因为资产或债务刷新任务未执行残留脏数据，导致分案失败
        update_unassigned_cases("现金贷多期", 1, 1)

    @classmethod
    def teardown_method(cls):
        DataBase.close_connects()

    # 1、已分案件的平均个数assignedAvgNum < 最大分案平均数assignAvgNum
    # 1.1 符合条件的案件数 > 兜底的数量bottomNum
    # 最终可分配的案件数取兜底数量的案件数bottomNum
    # 策略参数：组内人均最大件数=1，最大分案平均数=3
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_bottom_to_group_bottom_smaller
    def test_cn_bottom_to_group_bottom_smaller(self):
        mission_strategy = "newAT_bottomToGroup"
        # 导入测试数据 并 获取预估分案结果
        expect_assigned_count = estimate_bottom_to_group(mission_strategy, "bottom_smaller")
        # 调用quartz任务，目前分案策略执行方式只支持quartz
        # 获取实际分案结果
        actual_count, case_behavior_info = get_assign_info(mission_strategy)
        # 核对分案数量
        Assert.assert_equal(expect_assigned_count, actual_count, "#### 兜底后的分案数量与预期不相同，预期=%s，实际=%s"
                            % (expect_assigned_count, actual_count))

    # 1、已分案件的平均个数assignedAvgNum < 最大分案平均数assignAvgNum
    # 1.2 符合条件的案件数 <= 兜底的数量bottomNum
    # 最终可分配的案件数取符合条件的案件数
    # 策略参数：组内人均最大件数=1，最大分案平均数=3
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_bottom_to_group_bottom_bigger
    def test_cn_bottom_to_group_bottom_bigger(self):
        mission_strategy = "newAT_bottomToGroup"
        # 导入测试数据 并 获取预估分案结果
        expect_assigned_count = estimate_bottom_to_group(mission_strategy, "bottom_bigger")
        # 调用quartz任务，目前分案策略执行方式只支持quartz
        # 获取实际分案结果
        actual_count, case_behavior_info = get_assign_info(mission_strategy)
        # 核对分案数量
        Assert.assert_equal(expect_assigned_count, actual_count, "#### 兜底后的分案数量与预期不相同，预期=%s，实际=%s"
                            % (expect_assigned_count, actual_count))

    # 2、已分案件的平均个数assignedAvgNum >= 最大分案平均数assignAvgNum
    # 可以兜底的数量bottomNum=0
    # 策略参数：组内人均最大件数=2，最大分案平均数=1
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_bottom_to_group_without_bottom
    def test_cn_bottom_to_group_without_bottom(self):
        mission_strategy = "newAT_bottomToGroupZero"
        # 导入测试数据 并 获取预估分案结果
        expect_assigned_count = estimate_bottom_to_group(mission_strategy, "without_bottom")
        # 调用quartz任务，目前分案策略执行方式只支持quartz
        # 获取实际分案结果
        actual_count, case_behavior_info = get_assign_info(mission_strategy)
        # 核对分案数量
        Assert.assert_equal(expect_assigned_count, actual_count, "#### 兜底后的分案数量与预期不相同，预期=%s，实际=%s"
                            % (expect_assigned_count, actual_count))


