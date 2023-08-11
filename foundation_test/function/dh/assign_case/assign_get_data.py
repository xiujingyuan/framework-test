import json
import time

import pandas as pd

from foundation_test.function.dh.assign_case.assign_db_function import get_assigned_by_group_quality, get_assigned_distribution, \
    get_assigned_by_level, get_dye_info, get_extract_dye_info, get_collector_id_list, get_bi_bf_current_month_assigned_amount, \
    get_current_month_online_days, get_mission_strategy
from foundation_test.util.log.log_util import LogUtil
from foundation_test.util.tools.tools import run_quartz


# 根据行为ID获取分案结果
def get_assign_info(mission_strategy):
    # 执行分案 并 获取分案行为
    case_behavior_info = run_quartz(1, mission_strategy)
    # 获取分案行为ID
    case_behavior_id = case_behavior_info[0]["id"]
    # # 测试
    # case_behavior_id = 3138
    # case_behavior_info = []
    actual_list = []
    # 新老客组间配平，按业务组、用户类型分组 获取分案结果
    if mission_strategy == "newAT_avgByQualityToGroup":
        actual_list = get_assigned_by_group_quality(case_behavior_id)

    if mission_strategy in ("newCombineSeveralIntoOne", "newAT_BaseCommonToGroup_AvgAmount",
                            "newAT_extract_quality", "newAT_extract_c_card",
                            "newAT_AvgAmountByMonthAssignedAmount"):
        actual_list_info = get_assigned_distribution(case_behavior_id)
        for item in actual_list_info:
            for k, v in item.items():
                if k == "per_assigned_case_num":
                    actual_list.append(v)

    if mission_strategy in ("newAT_bottomToGroup", "newAT_bottomToGroupZero"):
        actual_list = case_behavior_info[0]["debtor_amount"]

    if mission_strategy in ("newAT_abilityCoefficient", "newAT_abilityCoefficientInHand"):
        actual_list = get_assigned_by_level(case_behavior_id)

        per_assigned_number_info = get_assigned_distribution(case_behavior_id)
        per_assigned_number = []
        for item in per_assigned_number_info:
            for k, v in item.items():
                if k == "per_assigned_case_num":
                    per_assigned_number.append(v)
        case_behavior_info = max(per_assigned_number)
        LogUtil.log_info("#### 本次分案中，催员分到的最大案件数量=%s" % case_behavior_info)

    LogUtil.log_info("实际分案结果=%s" % actual_list)
    return actual_list, case_behavior_info


# 获取染色结果
def get_actual_dye_info(case_behavior_id):
    fails = 0
    for i in range(120):
        # 获取染色结果，染色异步，分案完成后仍然需要一段时间染色
        actual_dye_info = get_dye_info(case_behavior_id)
        if not actual_dye_info:
            time.sleep(1)
            fails += 1
            LogUtil.log_info("染色尚未完成，等待中，等待时间：%s" % fails)
        if actual_dye_info:
            LogUtil.log_info("染色成功，获取到染色结果：%s" % actual_dye_info)
            break
    if fails == 120:
        print("#### 请检查测试环境fox是否正常运行。")
        return

    return actual_dye_info


# 获取染色结果
def get_actual_extract_dye_info(dye_type, dye_color, begin_time, unassigned_case_num, source_type, quality_type):
    actual_assigned_count = 0
    fails = 0
    for i in range(120):
        # 获取染色结果，染色异步，分案完成后仍然需要一段时间染色
        actual_extract_dye_info = get_extract_dye_info(dye_type, dye_color, begin_time, source_type)
        LogUtil.log_info("### 预期染色数量=%s" % unassigned_case_num)

        if source_type in ("asset_quality", "c_card"):
            for p in range(len(actual_extract_dye_info)):
                if actual_extract_dye_info[p]["quality_type"] == quality_type:
                    actual_assigned_count = actual_extract_dye_info[p]["count"]
        if source_type is None or source_type == "":
            actual_assigned_count = actual_extract_dye_info[0]["count"]

        if not actual_extract_dye_info or actual_assigned_count < unassigned_case_num:
            time.sleep(1)
            fails += 1
            LogUtil.log_info("染色尚未完成，等待中，等待时间：%s" % fails)
        if actual_extract_dye_info and unassigned_case_num == actual_assigned_count:
            LogUtil.log_info("染色成功，获取到染色结果：%s" % actual_extract_dye_info)
            break
    if fails == 120:
        print("#### 请检查测试环境fox是否正常运行。")
        return

    return actual_assigned_count


# 获取bi的当月分案金额、当月上线天数，计算出催员首次参与分案的顺序。返回expect_assigned_info，只有name列
def get_assigned_users_current_assigned_amount(group_name):
    # 获取在线催员
    online_user_id_info = get_collector_id_list(group_name)
    assigned_amount_info = []
    for item in online_user_id_info:
        for key, sys_user_id in item.items():
            if key == "id":
                # 获取当月分案金额，来源：bi
                amount_info = get_bi_bf_current_month_assigned_amount(sys_user_id)
                assigned_amount_info.extend(amount_info)
    pre_assigned_info = pd.DataFrame.from_records(data=assigned_amount_info, columns=["name", "bf_current_month_assigned_amount"])
    pre_assigned_info.insert(loc=2, column="online_days", value=0)
    for i in range(pre_assigned_info.shape[0]):
        collector_name = pre_assigned_info.iloc[i, 0]
        # 查询当月1号截止到今天的在线天数，包含今天
        collector_online_days = get_current_month_online_days(collector_name)
        pre_assigned_info.iloc[i, 2] = collector_online_days[0]["online_days"]
    LogUtil.log_info("### 1分案前 初始化当前已分案情况：pre_assigned_info=%s" % pre_assigned_info)
    pre_assigned_info.insert(loc=3, column="assigned_amount/online_days", value=0)
    pre_assigned_info["assigned_amount/online_days"] = pre_assigned_info["bf_current_month_assigned_amount"].astype(int) / pre_assigned_info[
        "online_days"]
    for i in range(pre_assigned_info.shape[0]):
        # 在线天数为0，当月分案金额/在线天数 结果置为0
        if pre_assigned_info.iloc[i, 2] == 0:
            pre_assigned_info.iloc[i, 3] = 0
    LogUtil.log_info("### 2分案前 初始化当前已分案情况：pre_assigned_info=%s" % pre_assigned_info)

    pre_assigned_info = pre_assigned_info.sort_values(by="assigned_amount/online_days", ascending=True)
    pre_assigned_info = pre_assigned_info.reset_index(drop=True)
    LogUtil.log_info("### 3分案前 初始化当前已分案情况：pre_assigned_info=%s" % pre_assigned_info)
    expect_assigned_info = pre_assigned_info[["name"]]
    LogUtil.log_info("### 4分案前 催员排序：expect_assigned_info=%s" % expect_assigned_info)
    return expect_assigned_info


# 获取策略里配置的分案业务组
def get_group_name(mission_strategy):
    strategy_info = json.loads(get_mission_strategy(mission_strategy)[0]["content"])
    # 获取策略配置的业务组名
    group_name = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["groupName"]
    return group_name
