import random

import pytest

from foundation_test.function.dh.assign_case.assign_check_function import estimate_assigned_count, check_assigned_count, check_dye, \
    check_assigned_amount
from foundation_test.function.dh.assign_case.assign_db_function import *
from foundation_test.function.dh.assign_case.assign_get_data import get_assign_info
from foundation_test.util.db.db_util import DataBase
from foundation_test.util.log.log_util import LogUtil
from foundation_test.util.tools.tools import get_date


class TestCnBaseCommonAvgAmount(object):
    #
    # 分案到组：BASE_COMMON_TO_GROUP，直接分到组，基础的分案到组方式
    # 分案到人：AVG_AMOUNT，金额均分
    #
    @classmethod
    def setup_method(cls):
        # env=1,country=china,environment=test
        # dc.init_dh_env(1, "china", "dev")
        dc.init_dh_env(dc.ENV, dc.COUNTRY, dc.ENVIRONMENT)
        LogUtil.log_info("#### 当前环境env=%s，country=%s，environment=%s"
                         % (dc.ENV, dc.COUNTRY, dc.ENVIRONMENT))
        # 导入数据前，先清空库中符合条件的资产，防止因为资产或债务刷新任务未执行残留脏数据，导致分案失败
        update_unassigned_cases("现金贷多期", 2, 3)

    @classmethod
    def teardown_method(cls):
        DataBase.close_connects()

    # 可分案到组的债务数量 大于 策略配置的小组人均最大平均数*小组在线人数
    # 小组最终可分到的债务数量 等于 策略配置的小组人均最大平均数*小组在线人数
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_base_common_avg_amount_01
    def test_cn_base_common_avg_amount_01(self):
        mission_strategy = "newAT_BaseCommonToGroup_AvgAmount"
        # 导入测试数据 并 获取预估分案结果
        expect_list, unassigned_case_num = estimate_assigned_count(mission_strategy, True)
        begin_time = get_date()
        # 分案 并 获取实际分案结果
        actual_list, case_behavior_info = get_assign_info(mission_strategy)
        # 核对分案数量
        check_assigned_count(expect_list, actual_list, unassigned_case_num, case_behavior_info)
        # 检查染色结果
        check_dye(mission_strategy, unassigned_case_num, "", begin_time, "")
        # 检查分案金额是否均分
        check_assigned_amount(case_behavior_info, mission_strategy)

    # 可分案到组的债务数量 小于 策略配置的小组人均最大平均数*小组在线人数
    # 小组最终可分到的债务数量 等于 可分案到组的债务数量
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_base_common_avg_amount_02
    def test_cn_base_common_avg_amount_02(self):
        mission_strategy = "newAT_BaseCommonToGroup_AvgAmount"
        # 导入测试数据 并 获取预估分案结果
        expect_list, unassigned_case_num = estimate_assigned_count(mission_strategy, False)
        begin_time = get_date()
        # 分案 并 获取实际分案结果
        actual_list, case_behavior_info = get_assign_info(mission_strategy)
        # 核对分案数量
        check_assigned_count(expect_list, actual_list, unassigned_case_num, case_behavior_info)
        # 检查染色结果
        check_dye(mission_strategy, unassigned_case_num, "", begin_time, "")
        # 检查分案金额是否均分
        check_assigned_amount(case_behavior_info, mission_strategy)

    # 按用户类型抽比，"extract_type": "QUALITY_EXTRACT_TYPE"
    # 新用户、老用户、null（无用户类型数据）
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_extract_quality
    def test_cn_extract_quality(self):
        mission_strategy = "newAT_extract_quality"
        # 导入测试数据 并 获取预估分案结果
        expect_list, unassigned_case_num = estimate_assigned_count(mission_strategy, None)
        unassigned_new_num = unassigned_case_num[0]["unassigned_new_num"]
        unassigned_old_num = unassigned_case_num[0]["unassigned_old_num"]
        unassigned_null_num = unassigned_case_num[0]["unassigned_null_num"]
        # 分案前，获取当前时间
        begin_time = get_date()
        # 分案
        get_assign_info(mission_strategy)
        # 检查新客的染色结果
        check_dye(mission_strategy, unassigned_new_num, "新用户", begin_time, "asset_quality")
        # 检查老客的染色结果
        check_dye(mission_strategy, unassigned_old_num, "老用户", begin_time, "asset_quality")
        # 检查无用户类型的染色结果
        check_dye(mission_strategy, unassigned_null_num, "null", begin_time, "asset_quality")

    # 按C卡等级抽比，"extract_type": "C_CARD_EXTRACT_TYPE"
    # C卡等级1或2或null
    @pytest.mark.dh_auto_test
    @pytest.mark.dh_cn_assign
    @pytest.mark.dh_cn_extract_c_card
    def test_cn_extract_c_card(self):
        mission_strategy = "newAT_extract_c_card"
        # 导入测试数据 并 获取预估分案结果
        expect_list, unassigned_case_num = estimate_assigned_count(mission_strategy, None)
        unassigned_c_card_1 = unassigned_case_num[0]["unassigned_c_card_1"]
        unassigned_c_card_2 = unassigned_case_num[0]["unassigned_c_card_2"]
        unassigned_c_card_null = unassigned_case_num[0]["unassigned_c_card_null"]
        # 分案前，获取当前时间
        begin_time = get_date()
        # 分案
        get_assign_info(mission_strategy)
        # 检查C卡等级1的染色结果
        check_dye(mission_strategy, unassigned_c_card_1, 1, begin_time, "c_card")
        # 检查C卡等级2的染色结果
        check_dye(mission_strategy, unassigned_c_card_2, 2, begin_time, "c_card")
        # 检查无C卡等级的染色结果
        check_dye(mission_strategy, unassigned_c_card_null, -1, begin_time, "c_card")
