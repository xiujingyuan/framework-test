from foundation_test.function.dh.assign_case.assign_check_function import *
from foundation_test.function.dh.assign_case.assign_db_function import update_unassigned_cases
from foundation_test.function.dh.assign_case.assign_get_data import get_assign_info
from foundation_test.util.db.db_util import DataBase
from foundation_test.util.tools.tools import *
import foundation_test.config.dh.db_const as dc


class TestCnMoreGroupAsOne(object):
    #
    # 分案到组：MORE_GROUP_AS_ONE_GROUP，将多个业务组当成一个整体，案件在整体上分
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

    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_more_as_one_avg_num
    def test_cn_more_group_avg_num(self):
        mission_strategy = "newCombineSeveralIntoOne"
        # 导入测试数据 并 获取预估分案结果
        expect_list, unassigned_case_num = estimate_assigned_count(mission_strategy)
        # 调用quartz任务，目前分案策略执行方式只支持quartz
        # 获取实际分案结果
        actual_list, case_behavior_info = get_assign_info(mission_strategy)
        # 核对分案数量
        check_assigned_count(expect_list, actual_list, unassigned_case_num, case_behavior_info)

