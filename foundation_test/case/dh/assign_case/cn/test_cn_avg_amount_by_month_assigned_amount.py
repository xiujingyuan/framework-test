import pytest

from foundation_test.function.dh.assign_case.assign_check_function import check_v3_assigned_amount
from foundation_test.function.dh.assign_case.assign_db_function import *
from foundation_test.function.dh.assign_case.assign_get_data import get_assign_info, get_assigned_users_current_assigned_amount
from foundation_test.function.dh.assign_case.base_data_make_function import import_cn_cases
from foundation_test.util.db.db_util import DataBase
from foundation_test.util.log.log_util import LogUtil


class TestCnAvgAmountByMonthAssignedAmount(object):
    #
    # 分案到组：BASE_COMMON_TO_GROUP，直接分到组，基础的分案到组方式
    # 分案到人：AVG_AMOUNT_WITH_MONTH_ASSIGN_AMOUNT_PRE_SORT，第一次排序根据当月分案金额，剩下的都根据当日分案金额排序
    #
    @classmethod
    def setup_method(cls):
        # env=1,country=china,environment=test
        # dc.init_dh_env(1, "china", "dev")
        dc.init_dh_env(dc.ENV, dc.COUNTRY, dc.ENVIRONMENT)
        LogUtil.log_info("#### 当前环境env=%s，country=%s，environment=%s" % (dc.ENV, dc.COUNTRY, dc.ENVIRONMENT))
        # 导入数据前，先清空库中符合条件的资产，防止因为资产或债务刷新任务未执行残留脏数据，导致分案失败
        update_unassigned_cases("现金贷多期", 7, 7)

    @classmethod
    def teardown_method(cls):
        DataBase.close_connects()

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_avg_amount_by_month_assigned_amount
    def test_cn_avg_amount_by_month_assigned_amount(self):
        mission_strategy = "newAT_AvgAmountByMonthAssignedAmount"
        # 获取策略配置中的业务组
        group_name = ['自动化测试_IVR组']
        # 分案前获取业务组在线催员 本月的分案总金额/在线天数 排序，按 本月的分案总金额/在线天数 升序排列
        cur_month_assigned_amount_sort = get_assigned_users_current_assigned_amount(group_name)
        # 导入测试资产，逾期7天，14笔
        # dc.ENV = 1
        import_cn_cases(7, "新用户", 1, False, dc.ENV, 14, "草莓")
        # 分案 并 获取实际分案结果
        actual_list, case_behavior_info = get_assign_info(mission_strategy)
        # 检查分案金额是否根据 bi当月已分分案总额/当月在线天数 升序排列，当月已分金额最少的优先派发金额最大的
        check_v3_assigned_amount(case_behavior_info, cur_month_assigned_amount_sort)
