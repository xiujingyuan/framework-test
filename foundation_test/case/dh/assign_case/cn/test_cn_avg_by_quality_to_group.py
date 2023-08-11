import pytest
from pandas._testing import assert_frame_equal

import foundation_test.config.dh.db_const as dc
from foundation_test.function.dh.assign_case.assign_check_function import estimate_quality_to_group
from foundation_test.function.dh.assign_case.assign_db_function import update_unassigned_cases, modify_online_collector
from foundation_test.function.dh.assign_case.assign_get_data import get_assign_info
from foundation_test.util.db.db_util import DataBase
from foundation_test.util.log.log_util import LogUtil
import pandas as pd


class TestCnAvgByQualityToGroup(object):
    #
    # 分案到组：AVG_BY_QUALITY_TO_GROUP，根据新老客组间配平
    # 分案到人：AVG_AMOUNT，金额均分
    #
    # 前提：
    # > 计算『总人均案件数Z』：总债务数 / (新用户组人数 + 老用户组人数 + 混催组人数)
    # > 计算『新人均案件数X』：新用户组人数若为0，则X = Z + 1，否则X = 新用户债务数 / 新用户组人数
    # > 计算『老人均案件数Y』：老用户组人数若为0，则Y = Z + 1，否则Y = 老用户债务数 / 老用户组人数
    #
    # 规定的最大平均债务数，取KV中key = newMissionMostAverageNum
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

    # X <= Z & Z < newMissionMostAverageNum
    # 1、新用户债务全部分给新用户组，即新用户组的人均分案数为 X；
    # 2、老用户债务分给老用户组、混合组，即老用户组和混催组的人均案件数 A=老用户债务数 / ( 老用户组人数 + 混催组人数 )。
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_avg_by_quality_to_group_x_smaller
    def test_cn_avg_by_quality_to_group_x_smaller(self):
        mission_strategy = "newAT_avgByQualityToGroup"
        # 导入测试数据 并 获取预估新老客组间配平结果
        expect_list = estimate_quality_to_group(mission_strategy, "x_smaller_than_z")
        # 执行分案 并 获取实际分案结果
        actual_list, case_behavior_info = get_assign_info(mission_strategy)
        # 转pandas对比
        actual_info = pd.DataFrame.from_records(data=actual_list)
        actual_info["assigned_count_new"] = actual_info["assigned_count_new"].astype(int)
        actual_info["assigned_count_old"] = actual_info["assigned_count_old"].astype(int)
        expect_info = pd.DataFrame.from_records(data=expect_list)
        # 检查各个业务组的分案结果
        assert_frame_equal(expect_info, actual_info)

    # Y <= Z & Z < newMissionMostAverageNum
    # 1、老用户债务全部分给老用户组，即老用户组的人均分案数为 Y；
    # 2、新用户债务分给新用户组、混合组，即新用户组和混催组的人均案件数 B=新用户债务数 / ( 新用户组人数 + 混催组人数 )。
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_avg_by_quality_to_group_y_smaller
    def test_cn_avg_by_quality_to_group_y_smaller(self):
        mission_strategy = "newAT_avgByQualityToGroup"
        # 导入测试数据 并 获取预估新老客组间配平结果
        expect_list = estimate_quality_to_group(mission_strategy, "y_smaller_than_z")
        # 执行分案 并 获取实际分案结果
        actual_list, case_behavior_info = get_assign_info(mission_strategy)
        # 转pandas对比
        actual_info = pd.DataFrame.from_records(data=actual_list)
        actual_info["assigned_count_new"] = actual_info["assigned_count_new"].astype(int)
        actual_info["assigned_count_old"] = actual_info["assigned_count_old"].astype(int)
        expect_info = pd.DataFrame.from_records(data=expect_list)
        # 检查各个业务组的分案结果
        assert_frame_equal(expect_info, actual_info)

    # X > Z & Y > Z
    # Z < newMissionMostAverageNum
    # 新用户组和老用户组的人均分案数皆为 Z，混催组可分案件数=总债务数-Z*新用户组人数-Z*老用户组人数
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_avg_by_quality_to_group_z_smaller
    def test_cn_avg_by_quality_to_group_z_smaller(self):
        mission_strategy = "newAT_avgByQualityToGroup"
        # 导入测试数据 并 获取预估新老客组间配平结果
        expect_list = estimate_quality_to_group(mission_strategy, "x_y_bigger_than_z")
        # 执行分案 并 获取实际分案结果
        actual_list, case_behavior_info = get_assign_info(mission_strategy)
        # 转pandas对比
        actual_info = pd.DataFrame.from_records(data=actual_list)
        actual_info["assigned_count_new"] = actual_info["assigned_count_new"].astype(int)
        actual_info["assigned_count_old"] = actual_info["assigned_count_old"].astype(int)
        expect_info = pd.DataFrame.from_records(data=expect_list)
        # 检查各个业务组的分案结果
        assert_frame_equal(expect_info, actual_info)

    # 新、老组在线催员人数=0，X=Y=Z+1
    # X > Z & Y > Z
    # Z < newMissionMostAverageNum
    # 混催组可分案件数=总债务数
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_avg_by_quality_to_group_z_smaller_02
    def test_cn_avg_by_quality_to_group_z_smaller_02(self):
        # 修改新、老组在线人数为0
        modify_online_collector("自动化测试_A1组", 1, 3)
        modify_online_collector("自动化测试_A2组", 1, 3)

        mission_strategy = "newAT_avgByQualityToGroup"
        # 导入测试数据 并 获取预估新老客组间配平结果
        expect_list = estimate_quality_to_group(mission_strategy, "only_mix")
        # 执行分案 并 获取实际分案结果
        actual_list, case_behavior_info = get_assign_info(mission_strategy)
        # 转pandas对比
        actual_info = pd.DataFrame.from_records(data=actual_list)
        actual_info["assigned_count_new"] = actual_info["assigned_count_new"].astype(int)
        actual_info["assigned_count_old"] = actual_info["assigned_count_old"].astype(int)
        expect_info = pd.DataFrame.from_records(data=expect_list)
        # 检查各个业务组的分案结果
        assert_frame_equal(expect_info, actual_info)

        # 测试完成改回去，避免影响其他测试
        modify_online_collector("自动化测试_A1组", 3, 1)
        modify_online_collector("自动化测试_A2组", 3, 1)
