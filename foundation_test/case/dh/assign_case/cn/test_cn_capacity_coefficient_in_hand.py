from foundation_test.function.dh.assign_case.assign_check_function import *
from foundation_test.function.dh.assign_case.assign_db_function import get_collector_id_list, update_unassigned_cases
from foundation_test.function.dh.assign_case.assign_get_data import get_assign_info
from foundation_test.util.db.db_util import DataBase
from foundation_test.util.tools.tools import *
import foundation_test.config.dh.db_const as dc

group_name = ['自动化测试_A1组', '自动化测试_A2组']


class TestCnCapacityCoefficientInHand(object):
    #
    # 分案到组：BASE_COMMON_TO_GROUP，直接分到组
    # 分案到人：CAPACITY_COEFFICIENT_IN_HAND，能力系数+在手案件
    #
    # 存在多个能力系数时，
    # 每个系数能分到的案件占比 = 系数a * 催员人数 / (系数a * 对应的催员人数 + 系数b * 对应的催员人数 + ... + 系数n * 对应的催员人数)，
    # 每个系数可分到的案件数 = 占比 * 总债务数
    # 占比四舍五入，最后一个系数取剩下的案件数
    # 每个催员可分到的案件数最大不超过 在手限制
    #
    @classmethod
    def setup_method(cls):
        # env=1,country=china,environment=test
        # dc.init_dh_env(1, "china", "dev")
        dc.init_dh_env(dc.ENV, dc.COUNTRY, dc.ENVIRONMENT)
        LogUtil.log_info("#### 当前环境env=%s，country=%s，environment=%s"
                         % (dc.ENV, dc.COUNTRY, dc.ENVIRONMENT))
        # 避免数据影响，测试前清空催员在手
        user_info = get_collector_id_list(group_name)
        for item in user_info:
            for k, sys_user_id in item.items():
                if k == "id":
                    withdraw_mission(1, sys_user_id, "all")
        # 导入数据前，先清空库中符合条件的资产，防止因为资产或债务刷新任务未执行残留脏数据，导致分案失败
        update_unassigned_cases("现金贷多期", 1, 999)

    @classmethod
    def teardown_method(cls):
        DataBase.close_connects()

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_capacity_coefficient_in_hand_smaller_than_hand
    def test_cn_capacity_coefficient_in_hand_smaller_than_hand(self):
        mission_strategy = "newAT_abilityCoefficientInHand"
        # 导入测试数据 并 获取预估分案结果，没有超出在手限制
        expect_level_list, strategy_in_hand_limit = estimate_collector_level(mission_strategy, group_name, True)
        # 调用quartz任务，目前分案策略执行方式只支持quartz
        # 获取实际分案结果
        actual_list, actual_max_assigned = get_assign_info(mission_strategy)
        # 核对每个系数的分案数量
        Assert.assert_list_equal(expect_level_list, actual_list, "#### 每个系数可分到的案件数分布与预期不相同，预期=%s，实际=%s"
                                 % (expect_level_list, actual_list))
        # 核对催员分到的最大案件数是否超过在手限制
        assert actual_max_assigned <= strategy_in_hand_limit, "#### 催员分到的最大案件数 超过 在手限制"

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_capacity_coefficient_in_hand_bigger_than_hand
    def test_cn_capacity_coefficient_in_hand_bigger_than_hand(self):
        mission_strategy = "newAT_abilityCoefficientInHand"
        # 导入测试数据 并 获取预估分案结果，超出在手限制
        expect_level_list, strategy_in_hand_limit = estimate_collector_level(mission_strategy, group_name, False)
        # 调用quartz任务，目前分案策略执行方式只支持quartz
        # 获取实际分案结果
        actual_list, actual_max_assigned = get_assign_info(mission_strategy)
        # 核对每个系数的分案数量
        Assert.assert_list_equal(expect_level_list, actual_list, "#### 每个系数可分到的案件数分布与预期不相同，预期=%s，实际=%s"
                                 % (expect_level_list, actual_list))
        # 核对催员分到的最大案件数是否超过在手限制
        assert actual_max_assigned <= strategy_in_hand_limit, "#### 催员分到的最大案件数 超过 在手限制"

