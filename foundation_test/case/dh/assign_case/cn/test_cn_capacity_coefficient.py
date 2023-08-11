from foundation_test.function.dh.assign_case.assign_check_function import *
from foundation_test.function.dh.assign_case.assign_db_function import update_unassigned_cases
from foundation_test.function.dh.assign_case.assign_get_data import get_assign_info
from foundation_test.util.db.db_util import DataBase
from foundation_test.util.tools.tools import *
import foundation_test.config.dh.db_const as dc


class TestCnCapacityCoefficient(object):
    #
    # 分案到组：MORE_GROUP_AS_ONE_GROUP，将多个业务组当成一个整体，案件在整体上分
    # 分案到人：CAPACITY_COEFFICIENT，能力系数
    #
    # 存在多个能力系数时，
    # 每个系数能分到的案件占比 = 系数a * 催员人数 / (系数a * 对应的催员人数 + 系数b * 对应的催员人数 + ... + 系数n * 对应的催员人数)，
    # 每个系数可分到的案件数 = 占比 * 总债务数
    # 占比四舍五入，最后一个系数取剩下的案件数
    #
    @classmethod
    def setup_method(cls):
        # env=1,country=china,environment=test
        dc.init_dh_env(dc.ENV, dc.COUNTRY, dc.ENVIRONMENT)
        # dc.init_dh_env(1, "china", "dev")
        LogUtil.log_info("#### 当前环境env=%s，country=%s，environment=%s"
                         % (dc.ENV, dc.COUNTRY, dc.ENVIRONMENT))
        # 导入数据前，先清空库中符合条件的资产，防止因为资产或债务刷新任务未执行残留脏数据，导致分案失败
        update_unassigned_cases("现金贷多期", 4, 4)

    @classmethod
    def teardown_method(cls):
        DataBase.close_connects()

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_capacity_coefficient
    def test_cn_capacity_coefficient(self):
        mission_strategy = "newAT_abilityCoefficient"
        group_name = ['自动化测试_A1组', '自动化测试_A2组']
        # 导入测试数据 并 获取预估分案结果
        expect_level_list, in_hand_limit = estimate_collector_level(mission_strategy, group_name, True)
        # 调用quartz任务，目前分案策略执行方式只支持quartz
        # 获取实际分案结果
        actual_list, actual_max_assigned = get_assign_info(mission_strategy)
        # 核对每个系数的分案数量
        Assert.assert_list_equal(expect_level_list, actual_list, "#### 每个系数可分到的案件数分布与预期不相同，预期=%s，实际=%s"
                                 % (expect_level_list, actual_list))

