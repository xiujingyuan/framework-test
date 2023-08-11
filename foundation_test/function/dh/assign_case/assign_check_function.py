import json

import re

from foundation_test.function.dh.assign_case.assign_db_function import get_collector_level_count, get_mission_strategy, get_collector_count, \
    get_mission_log_total_amount, get_collector_name, get_assigned_mission_log, get_af_current_month_assigned_amount, \
    get_bf_current_month_collector_name, get_bf_current_month_assigned_amount, get_current_month_online_days
from foundation_test.function.dh.assign_case.assign_get_data import *
from foundation_test.function.dh.assign_case.base_data_make_function import import_cn_cases
from foundation_test.util.asserts.assert_util import Assert
from foundation_test.util.log.log_util import LogUtil
import foundation_test.config.dh.db_const as dc
import pandas as pd
from pandas._testing import assert_frame_equal


# 预估分案个数
def estimate_assigned_count(mission_strategy=None, bigger_than_strategy=None):
    expect_list = []
    collector_count = 0
    strategy_info = get_mission_strategy(mission_strategy)[0]["content"]
    LogUtil.log_info("################ 解析得到分案策略：%s" % strategy_info)
    strategy_info = json.loads(strategy_info)
    LogUtil.log_info("################ 反序列化后得到分案策略：%s" % strategy_info["strategies"])
    overdue_days = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["condition"][0]["expr"]
    overdue_days = int(re.sub("\D", "", overdue_days))

    if mission_strategy == "newCombineSeveralIntoOne":
        group_list_info = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["groups"]
        group_list = []
        for item in group_list_info:
            for k, v in item.items():
                if k == "groupName":
                    group_list.append(v)
        LogUtil.log_info("策略中业务组=%s" % group_list)
        count = 37
        # unassigned_case_num：生成未分案D1债务数
        unassigned_case_num = import_cn_cases(overdue_days, "新用户", 1, False, dc.ENV, count, "草莓")
        LogUtil.log_info("#### 获取到分案前未分配的债务数量=%s" % unassigned_case_num)
        # 计算催员在线人数
        for group in group_list:
            collector_count += get_collector_count(group)[0]["collector_num"]
        LogUtil.log_info("#### 业务组在线总人数=%s" % collector_count)

        # 取整
        expect_avg_integer = int(unassigned_case_num / collector_count)
        LogUtil.log_info("#### 向下取整=%s" % expect_avg_integer)
        # 取余
        expect_avg_reminder = unassigned_case_num % collector_count
        LogUtil.log_info("#### 取余=%s" % expect_avg_reminder)
        for i in range(expect_avg_reminder):
            expect_list.append(expect_avg_integer + 1)
        for i in range(collector_count - expect_avg_reminder):
            expect_list.append(expect_avg_integer)
        # 预估 每个催员分到手的债务数量分布，降序排列
        expect_list.sort(reverse=True)
        LogUtil.log_info("#### 预估每个催员分到手的债务数量分布=%s" % expect_list)

    if mission_strategy == "newAT_BaseCommonToGroup_AvgAmount":
        # 获取策略配置的可分配比例
        strategy_percent = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["percent"]
        LogUtil.log_info("### 获取策略配置的可分配比例=%s" % strategy_percent)
        # 获取策略配置的小组人均最大平均数
        max_avg_amount = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["max_avg_amount"]
        LogUtil.log_info("### 获取策略配置的小组人均最大平均数=%s" % max_avg_amount)
        # 获取策略配置的业务组名
        group_name = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["groupName"]
        # 在线催员
        collector_count = get_collector_count(group_name)[0]["collector_num"]
        LogUtil.log_info("### 当前配置中业务组=%s 的在线人数=%s" % (group_name, collector_count))
        # 计算 策略配置的小组人均最大平均数*小组在线人数
        can_strategy_assign_num = max_avg_amount * collector_count
        LogUtil.log_info("### 策略允许分配的最大债务数=%s" % can_strategy_assign_num)
        if bigger_than_strategy is True:
            # 生成符合分案策略的源债务
            count = int(can_strategy_assign_num / strategy_percent) + 1
            LogUtil.log_info("#### bigger_than_strategy is True，需要未分配债务数=%s" % count)
            import_cn_cases(overdue_days, "新用户", 1, True, dc.ENV, count, "草莓")
            # 可分案到组的债务数量 大于 策略配置的小组人均最大平均数*小组在线人数，小组最终可分到的债务数量取 策略配置的小组人均最大平均数*小组在线人数
            for i in range(collector_count):
                expect_list.append(max_avg_amount)
            unassigned_case_num = can_strategy_assign_num
        if bigger_than_strategy is False:
            # 生成符合分案策略的源债务
            count = int(can_strategy_assign_num / strategy_percent) - 1
            LogUtil.log_info("#### bigger_than_strategy is False，需要未分配债务数=%s" % count)
            unassigned_case_num = import_cn_cases(overdue_days, "新用户", 1, True, dc.ENV, count, "草莓")
            # 可分案到组的债务数量unassigned_case_num 小于 策略配置的小组人均最大平均数*小组在线人数，小组最终可分到的债务数量取 可分案到组的债务数量unassigned_case_num
            unassigned_case_num = int(unassigned_case_num * strategy_percent)
            LogUtil.log_info("#### 可分案到组的债务数量unassigned_case_num=%s" % unassigned_case_num)
            # 取整
            expect_avg_integer = int(unassigned_case_num / collector_count)
            LogUtil.log_info("#### 向下取整=%s" % expect_avg_integer)
            # 取余
            expect_avg_reminder = unassigned_case_num % collector_count
            LogUtil.log_info("#### 取余=%s" % expect_avg_reminder)
            for i in range(expect_avg_reminder):
                expect_list.append(expect_avg_integer + 1)
            for i in range(collector_count - expect_avg_reminder):
                expect_list.append(expect_avg_integer)
        # 预估 每个催员分到手的债务数量分布，降序排列
        expect_list.sort(reverse=True)
        LogUtil.log_info("#### 预估每个催员分到手的债务数量分布=%s" % expect_list)

    if mission_strategy == "newAT_extract_quality":
        count_new = 21
        count_old = count_null = 12
        # 生成未分案的债务数
        unassigned_new_num = import_cn_cases(overdue_days, "新用户", "", False, dc.ENV, count_new, "草莓")
        unassigned_old_num = import_cn_cases(overdue_days, "老用户", "", False, dc.ENV, count_old, "草莓")
        unassigned_null_num = import_cn_cases(overdue_days, "", "", False, dc.ENV, count_null, "草莓")
        unassigned_case_num = [{
            "unassigned_new_num": unassigned_new_num,
            "unassigned_old_num": unassigned_old_num,
            "unassigned_null_num": unassigned_null_num
        }]
        LogUtil.log_info("#### 获取到分案前未分配的债务数量=%s" % unassigned_case_num)

    if mission_strategy == "newAT_extract_c_card":
        c_card_1 = 13
        c_card_2 = 12
        c_card_null = 10
        # 生成未分案的债务数
        unassigned_c_card_1 = import_cn_cases(overdue_days, "新用户", 1, False, dc.ENV, c_card_1, "草莓")
        unassigned_c_card_2 = import_cn_cases(overdue_days, "新用户", 2, False, dc.ENV, c_card_2, "草莓")
        unassigned_c_card_null = import_cn_cases(overdue_days, "新用户", "", False, dc.ENV, c_card_null, "草莓")
        unassigned_case_num = [{
            "unassigned_c_card_1": unassigned_c_card_1,
            "unassigned_c_card_2": unassigned_c_card_2,
            "unassigned_c_card_null": unassigned_c_card_null
        }]
        LogUtil.log_info("#### 获取到分案前未分配的债务数量=%s" % unassigned_case_num)
    return expect_list, unassigned_case_num


# 对比分案数量分布
def check_assigned_count(expect_list, actual_list, unassigned_case_num, case_behavior_info):
    Assert.assert_list_equal(expect_list, actual_list, "#### 分案结果分布与预期不相同，预期=%s，实际=%s"
                             % (expect_list, actual_list))
    Assert.assert_equal(unassigned_case_num, case_behavior_info[0]["debtor_amount"], "实际已分配债务数量与预期不符，预期=%s，实际=%s"
                        % (unassigned_case_num, case_behavior_info[0]["debtor_amount"]))


# 检查染色结果
def check_dye(mission_strategy, unassigned_case_num=0, quality_type="", begin_time=None, source_type=None):
    strategy_info = json.loads(get_mission_strategy(mission_strategy)[0]["content"])
    # 获取策略配置的分案染色
    expect_assigned_dye = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["ranse"]
    LogUtil.log_info("### 获取策略配置的分案染色=%s" % expect_assigned_dye)

    if mission_strategy == "newAT_BaseCommonToGroup_AvgAmount":
        # 获取实际染色结果
        actual_assigned_dye_count = get_actual_extract_dye_info(expect_assigned_dye["assign_case_tag_type"],
                                                                expect_assigned_dye["assign_case_tag_color"],
                                                                begin_time,
                                                                unassigned_case_num,
                                                                source_type,
                                                                quality_type)
        # 对比
        Assert.assert_equal(unassigned_case_num, actual_assigned_dye_count, "实际可分案案件的染色数量与预期不符，预期=%s，实际=%s"
                            % (unassigned_case_num, actual_assigned_dye_count))

    if mission_strategy in ("newAT_extract_quality", "newAT_extract_c_card"):
        # 获取策略配置的可分配比例
        strategy_info_percent = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["extract"]["percent_map"][str(quality_type)]
        LogUtil.log_info("### 获取策略配置的抽比，用户类型或C卡等级=%s 的抽比=%s" % (str(quality_type), strategy_info_percent))
        expect_assigned_count = round(strategy_info_percent * unassigned_case_num)
        expect_unassigned_count = unassigned_case_num - expect_assigned_count
        # 获取实际染色结果
        actual_assigned_dye_count = get_actual_extract_dye_info(expect_assigned_dye["assign_case_tag_type"],
                                                                expect_assigned_dye["assign_case_tag_color"],
                                                                begin_time,
                                                                expect_assigned_count,
                                                                source_type,
                                                                quality_type)
        actual_unassigned_dye_count = get_actual_extract_dye_info(expect_assigned_dye["unassign_case_tag_type"],
                                                                  expect_assigned_dye["unassign_case_tag_color"],
                                                                  begin_time,
                                                                  expect_unassigned_count,
                                                                  source_type,
                                                                  quality_type)
        # 对比
        Assert.assert_equal(expect_assigned_count, actual_assigned_dye_count, "实际可分案案件的染色数量与预期不符，预期=%s，实际=%s"
                            % (expect_assigned_count, actual_assigned_dye_count))
        Assert.assert_equal(expect_unassigned_count, actual_unassigned_dye_count, "实际未分案案件的染色数量与预期不符，预期=%s，实际=%s"
                            % (expect_unassigned_count, actual_unassigned_dye_count))


# 检查分案金额是否均分，不考虑当月已分案金额，本次策略执行中已分金额最少的优先派发金额最大的
def check_assigned_amount(case_behavior_info, mission_strategy):
    # 获取分案行为ID
    case_behavior_id = case_behavior_info[0]["id"]
    # 获取已分案的债务金额
    mission_log_info = get_assigned_mission_log(case_behavior_id)
    debtor_amount_list = []
    for item in mission_log_info:
        for k, v in item.items():
            if k == "assign_overdue_total_amount":
                debtor_amount_list.append(v)
    debtor_amount_list.sort(reverse=True)
    LogUtil.log_info("### 债务金额从大到小排序后，分布=%s" % debtor_amount_list)
    strategy_info = json.loads(get_mission_strategy(mission_strategy)[0]["content"])
    # 获取策略配置的业务组名
    group_name = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["groupName"]
    # 获取在线催员姓名
    assigned_info = get_collector_name(group_name)
    LogUtil.log_info("### 初始化已分案情况：assigned_info=%s" % assigned_info)
    expect_assigned_info = pd.DataFrame.from_records(data=assigned_info)
    # 开始金额均分预估
    for i in range(len(debtor_amount_list)):
        # 每次分配前，重新按已分金额升序排序
        expect_assigned_info = expect_assigned_info.sort_values(by="today_assigned_amount", ascending=True)
        LogUtil.log_info("### 催员已分金额从小到大排序，当前已分金额最小的是=%s，已分金额=%s" % (expect_assigned_info.iloc[0, 0], expect_assigned_info.iloc[0, 1]))
        # 未分案件金额最大的 分给 已分金额最少的催员
        expect_assigned_info.iloc[0, 1] += debtor_amount_list[0]
        LogUtil.log_info("### 第%s次分配，当前未分配债务金额中最大的是=%s" % (i + 1, debtor_amount_list[0]))
        expect_assigned_info["today_assigned_amount"] = expect_assigned_info["today_assigned_amount"].astype(int)
        # 分出去的案件排除
        del debtor_amount_list[0]
        LogUtil.log_info("### 第%s次分配，expect_assigned_info=%s" % (i + 1, expect_assigned_info))
    # 全部分配完，再次排序
    expect_assigned_info = expect_assigned_info.sort_values(by="today_assigned_amount", ascending=True)
    expect_assigned_info = expect_assigned_info.reset_index(drop=True)
    LogUtil.log_info("### 预估分配完成，expect_assigned_info=%s" % expect_assigned_info)

    # 获取实际分案金额统计结果
    mission_log_amount_info = get_mission_log_total_amount(case_behavior_id)
    actual_assigned_info = pd.DataFrame.from_records(data=mission_log_amount_info)
    actual_assigned_info["today_assigned_amount"] = actual_assigned_info["today_assigned_amount"].astype(int)
    LogUtil.log_info("### 实际，actual_assigned_info=%s" % actual_assigned_info)

    # 对比，因为分案时获取的用户排序是随机的，无法精确到具体的催员能分到什么样的债务，但是金额分布情况是固定的
    # 最终只对比金额汇总情况
    assert_frame_equal(expect_assigned_info[["today_assigned_amount"]], actual_assigned_info[["today_assigned_amount"]])


# 新算法，只有国内使用
# 检查分案金额是否根据当月已分分案总额均分，当月已分金额最少的优先派发金额最大的
def check_v1_assigned_amount(case_behavior_info, mission_strategy):
    # 获取分案行为ID
    case_behavior_id = case_behavior_info[0]["id"]
    # 获取参与本次分案的债务金额
    mission_log_info = get_assigned_mission_log(case_behavior_id)
    debtor_amount_list = []
    for item in mission_log_info:
        for k, v in item.items():
            if k == "assign_overdue_total_amount":
                debtor_amount_list.append(v)
    debtor_amount_list.sort(reverse=True)
    LogUtil.log_info("### 债务金额从大到小排序后，分布=%s" % debtor_amount_list)
    strategy_info = json.loads(get_mission_strategy(mission_strategy)[0]["content"])
    # 获取策略配置的业务组名
    group_name = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["groupName"]
    # 获取在线催员姓名、本次分案前本月已分案金额
    assigned_info = get_bf_current_month_collector_name(group_name, case_behavior_id)
    LogUtil.log_info("### 获取分案前 当月已分案情况：assigned_info=%s" % assigned_info)
    expect_assigned_info = pd.DataFrame.from_records(data=assigned_info)
    # 开始金额均分预估
    for i in range(len(debtor_amount_list)):
        # 金额字段转int
        expect_assigned_info["bf_current_month_assigned_amount"] = expect_assigned_info["bf_current_month_assigned_amount"].astype(int)
        # 每次分配前，重新按已分金额升序排序
        expect_assigned_info = expect_assigned_info.sort_values(by="bf_current_month_assigned_amount", ascending=True)
        LogUtil.log_info("### 催员已分金额从小到大排序，当前已分金额最小的是=%s，已分金额=%s" % (expect_assigned_info.iloc[0, 0], expect_assigned_info.iloc[0, 1]))
        # 未分案件金额最大的 分给 已分金额最少的催员
        expect_assigned_info.iloc[0, 1] += debtor_amount_list[0]
        LogUtil.log_info("### 第%s次分配，当前未分配债务金额中最大的是=%s" % (i + 1, debtor_amount_list[0]))
        expect_assigned_info["bf_current_month_assigned_amount"] = expect_assigned_info["bf_current_month_assigned_amount"].astype(int)
        # 分出去的案件排除
        del debtor_amount_list[0]
        LogUtil.log_info("### 第%s次分配，expect_assigned_info=%s" % (i + 1, expect_assigned_info))
    # 全部分配完，再次排序
    expect_assigned_info = expect_assigned_info.sort_values(by="bf_current_month_assigned_amount", ascending=True)
    expect_assigned_info = expect_assigned_info.reset_index(drop=True)
    expect_assigned_info.rename(columns={"bf_current_month_assigned_amount": "af_current_month_assigned_amount"}, inplace=True)
    LogUtil.log_info("### 预估分配完成，expect_assigned_info=%s" % expect_assigned_info)

    # 获取实际分案金额统计结果
    mission_log_amount_info = get_af_current_month_assigned_amount(group_name)
    actual_assigned_info = pd.DataFrame.from_records(data=mission_log_amount_info)
    actual_assigned_info["af_current_month_assigned_amount"] = actual_assigned_info["af_current_month_assigned_amount"].astype(int)
    LogUtil.log_info("### 实际，actual_assigned_info=%s" % actual_assigned_info)

    # 对比，因为分案时获取的用户排序是随机的，无法精确到具体的催员能分到什么样的债务，但是金额分布情况是固定的
    # 最终只对比金额汇总情况
    assert_frame_equal(expect_assigned_info[["af_current_month_assigned_amount"]], actual_assigned_info[["af_current_month_assigned_amount"]])


# 新算法，检查分案金额是否均分，分案前根据 当月已分案金额/当月分案数量 升序排序，本次策略执行中已分金额最少的优先派发金额最大的
# 每轮分案中，不再按 当月分案金额/当月分案数量 升序排序，按照当前已分金额升序排序
# 第一次排序根据 当月分案金额/当月分案数量，剩下的都根据当日分案金额排序
def check_v2_assigned_amount(case_behavior_info, mission_strategy):
    # 获取分案行为ID
    case_behavior_id = case_behavior_info[0]["id"]
    # 获取已分案的债务金额
    mission_log_info = get_assigned_mission_log(case_behavior_id)
    debtor_amount_list = []
    for item in mission_log_info:
        for k, v in item.items():
            if k == "assign_overdue_total_amount":
                debtor_amount_list.append(v)
    debtor_amount_list.sort(reverse=True)
    LogUtil.log_info("### 债务金额从大到小排序后，分布=%s" % debtor_amount_list)
    strategy_info = json.loads(get_mission_strategy(mission_strategy)[0]["content"])
    # 获取策略配置的业务组名
    group_name = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["groupName"]
    # 获取在线催员姓名、本次分案前 当月分案金额/当月分案数量 升序排序
    assigned_info = get_bf_current_month_collector_name(group_name, case_behavior_id)
    LogUtil.log_info("### 获取分案前 当月已分案情况：assigned_info=%s" % assigned_info)
    expect_assigned_info = pd.DataFrame.from_records(data=assigned_info, columns=["name"])
    expect_assigned_info.insert(loc=1, column="today_assigned_amount", value=0)
    LogUtil.log_info("### 分案前 初始化当前已分案情况：expect_assigned_info=%s" % expect_assigned_info)
    # 开始金额均分预估
    for i in range(len(debtor_amount_list)):
        # 未分案件金额最大的 分给 已分金额最少的催员
        expect_assigned_info.iloc[0, 1] += debtor_amount_list[0]
        LogUtil.log_info("### 第%s次分配，当前未分配债务金额中最大的是=%s" % (i + 1, debtor_amount_list[0]))
        expect_assigned_info["today_assigned_amount"] = expect_assigned_info["today_assigned_amount"].astype(int)
        # 分出去的案件排除
        del debtor_amount_list[0]
        LogUtil.log_info("### 第%s次分配，expect_assigned_info=%s" % (i + 1, expect_assigned_info))
        # 除了第一次分配，每次分配前，重新按已分金额升序排序
        expect_assigned_info = expect_assigned_info.sort_values(by="today_assigned_amount", ascending=True)
        LogUtil.log_info("### 催员已分金额从小到大排序，当前已分金额最小的是=%s，已分金额=%s" % (expect_assigned_info.iloc[0, 0], expect_assigned_info.iloc[0, 1]))
    # 全部分配完，再次排序
    expect_assigned_info = expect_assigned_info.sort_values(by="today_assigned_amount", ascending=True)
    expect_assigned_info = expect_assigned_info.reset_index(drop=True)
    LogUtil.log_info("### 预估分配完成，expect_assigned_info=%s" % expect_assigned_info)

    # 获取实际分案金额统计结果
    mission_log_amount_info = get_mission_log_total_amount(case_behavior_id)
    actual_assigned_info = pd.DataFrame.from_records(data=mission_log_amount_info)
    actual_assigned_info["today_assigned_amount"] = actual_assigned_info["today_assigned_amount"].astype(int)
    LogUtil.log_info("### 实际，actual_assigned_info=%s" % actual_assigned_info)

    # 对比 催员及分到的总金额
    # 最终只对比金额汇总情况
    assert_frame_equal(expect_assigned_info, actual_assigned_info)


# 新算法，检查分案金额是否均分，分案前根据 当月已分案金额/当月上线分案天数 升序排序，本次策略执行中已分金额最少的优先派发金额最大的
# 每轮分案中，不再按 当月分案金额/当月上线分案天数 升序排序，按照当前已分金额升序排序
# 第一次排序根据 当月分案金额/当月上线分案天数，剩下的都根据当日分案金额排序
def check_v3_assigned_amount(case_behavior_info, expect_assigned_info):
    # 获取分案行为ID
    case_behavior_id = case_behavior_info[0]["id"]
    # 获取已分案的债务金额
    mission_log_info = get_assigned_mission_log(case_behavior_id)
    debtor_amount_list = []
    for item in mission_log_info:
        for k, v in item.items():
            if k == "assign_overdue_total_amount":
                debtor_amount_list.append(v)
    debtor_amount_list.sort(reverse=True)
    LogUtil.log_info("### 债务金额从大到小排序后，分布=%s" % debtor_amount_list)

    expect_assigned_info.insert(loc=1, column="today_assigned_amount", value=0)
    LogUtil.log_info("### 分案前 初始化当前已分案情况：expect_assigned_info=%s" % expect_assigned_info)
    # 开始金额均分预估
    for i in range(len(debtor_amount_list)):
        # 未分案件金额最大的 分给 已分金额最少的催员
        expect_assigned_info.iloc[0, 1] += debtor_amount_list[0]
        LogUtil.log_info("### 第%s次分配，当前未分配债务金额中最大的是=%s" % (i + 1, debtor_amount_list[0]))
        expect_assigned_info["today_assigned_amount"] = expect_assigned_info["today_assigned_amount"].astype(int)
        # 分出去的案件排除
        del debtor_amount_list[0]
        LogUtil.log_info("### 第%s次分配，expect_assigned_info=%s" % (i + 1, expect_assigned_info))
        # 除了第一次分配，每次分配前，重新按已分金额升序排序
        expect_assigned_info = expect_assigned_info.sort_values(by="today_assigned_amount", ascending=True)
        LogUtil.log_info("### 催员已分金额从小到大排序，当前已分金额最小的是=%s，已分金额=%s" % (expect_assigned_info.iloc[0, 0], expect_assigned_info.iloc[0, 1]))
    # 全部分配完，再次排序
    # expect_assigned_info = expect_assigned_info.sort_values(by=["name", "today_assigned_amount"], ascending=True)
    expect_assigned_info = expect_assigned_info.sort_values(by=expect_assigned_info.columns.tolist(), ascending=True)
    expect_assigned_info = expect_assigned_info.reset_index(drop=True)
    LogUtil.log_info("### 预估分配完成，expect_assigned_info=%s" % expect_assigned_info)

    # 获取实际分案金额统计结果
    mission_log_amount_info = get_mission_log_total_amount(case_behavior_id)
    actual_assigned_info = pd.DataFrame.from_records(data=mission_log_amount_info)
    actual_assigned_info["today_assigned_amount"] = actual_assigned_info["today_assigned_amount"].astype(int)
    actual_assigned_info = actual_assigned_info.sort_values(by=actual_assigned_info.columns.tolist(), ascending=True)
    actual_assigned_info = actual_assigned_info.reset_index(drop=True)
    LogUtil.log_info("### 实际，actual_assigned_info=%s" % actual_assigned_info)

    # 对比 催员及分到的总金额
    # 最终只对比金额汇总情况
    assert_frame_equal(expect_assigned_info, actual_assigned_info)


# 预估新老客组间配平结果
def estimate_quality_to_group(mission_strategy, which_smaller):
    # 获取策略配置
    strategy_info = json.loads(get_mission_strategy(mission_strategy)[0]["content"])
    LogUtil.log_info("################ 反序列化后得到分案策略：%s" % strategy_info["strategies"])
    overdue_days = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["condition"][0]["expr"]
    # 获取逾期天数
    overdue_days = int(re.sub("\D", "", overdue_days))

    # 获取催员在线人数
    collector_info_new = get_collector_count("自动化测试_A1组")
    collector_info_old = get_collector_count("自动化测试_A2组")
    collector_info_mix = get_collector_count("自动化测试_A3组")
    if not collector_info_new:
        collector_count_new = 0
    else:
        collector_count_new = collector_info_new[0]["collector_num"]

    if not collector_info_old:
        collector_count_old = 0
    else:
        collector_count_old = collector_info_old[0]["collector_num"]

    if not collector_info_mix:
        collector_count_mix = 0
    else:
        collector_count_mix = collector_info_mix[0]["collector_num"]

    if which_smaller == "x_smaller_than_z":
        # x=2，y=5.5，z=2.15
        # 导入测试数据
        new_count = 10
        old_count = 33
        unassigned_new_case_num = import_cn_cases(overdue_days, "新用户", 1, False, dc.ENV, new_count, "草莓")
        LogUtil.log_info("#### 获取到分案前未分配的新客债务数量=%s" % unassigned_new_case_num)
        unassigned_old_case_num = import_cn_cases(overdue_days, "老用户", 1, False, dc.ENV, old_count, "草莓")
        LogUtil.log_info("#### 获取到分案前未分配的老客债务数量=%s" % unassigned_old_case_num)

        # 新用户债务全部分给新用户组
        expect_new_count = unassigned_new_case_num
        # 老用户债务分给老用户组、混合组
        expect_old_count = int(unassigned_old_case_num / (collector_count_old + collector_count_mix) * collector_count_old) + 1
        expect_mix_count = unassigned_old_case_num - expect_old_count
        expect_info = [
            {
                "assigned_group_name": "自动化测试_A1组",
                "assigned_count_new": expect_new_count,
                "assigned_count_old": 0
            },
            {
                "assigned_group_name": "自动化测试_A2组",
                "assigned_count_new": 0,
                "assigned_count_old": expect_old_count
            },
            {
                "assigned_group_name": "自动化测试_A3组",
                "assigned_count_new": 0,
                "assigned_count_old": expect_mix_count
            }
        ]

    if which_smaller == "y_smaller_than_z":
        # x=6.8，y=1，z=2
        # 导入测试数据
        new_count = 34
        old_count = 6
        unassigned_new_case_num = import_cn_cases(overdue_days, "新用户", 1, False, dc.ENV, new_count, "草莓")
        LogUtil.log_info("#### 获取到分案前未分配的新客债务数量=%s" % unassigned_new_case_num)
        unassigned_old_case_num = import_cn_cases(overdue_days, "老用户", 1, False, dc.ENV, old_count, "草莓")
        LogUtil.log_info("#### 获取到分案前未分配的老客债务数量=%s" % unassigned_old_case_num)

        # 老用户债务全部分给老用户组
        expect_old_count = unassigned_old_case_num
        # 新用户债务分给新用户组、混合组
        expect_new_count = int(unassigned_new_case_num / (collector_count_new + collector_count_mix) * collector_count_new) + 1
        expect_mix_count = unassigned_new_case_num - expect_new_count
        expect_info = [
            {
                "assigned_group_name": "自动化测试_A1组",
                "assigned_count_new": expect_new_count,
                "assigned_count_old": 0
            },
            {
                "assigned_group_name": "自动化测试_A2组",
                "assigned_count_new": 0,
                "assigned_count_old": expect_old_count
            },
            {
                "assigned_group_name": "自动化测试_A3组",
                "assigned_count_new": expect_mix_count,
                "assigned_count_old": 0
            }
        ]

    if which_smaller == "x_y_bigger_than_z":
        # x=4，y=3，z=1.9 →→→ 2
        # 导入测试数据
        new_count = 20
        old_count = 18
        unassigned_new_case_num = import_cn_cases(overdue_days, "新用户", 1, False, dc.ENV, new_count, "草莓")
        LogUtil.log_info("#### 获取到分案前未分配的新客债务数量=%s" % unassigned_new_case_num)
        unassigned_old_case_num = import_cn_cases(overdue_days, "老用户", 1, False, dc.ENV, old_count, "草莓")
        LogUtil.log_info("#### 获取到分案前未分配的老客债务数量=%s" % unassigned_old_case_num)

        # 向上取整
        z_count = int((unassigned_new_case_num + unassigned_old_case_num) / (collector_count_new + collector_count_old + collector_count_mix)) + 1
        LogUtil.log_info("#### X>Z&Y>Z，z_count=%s" % z_count)
        # 新用户组和老用户组的人均分案数皆为 Z
        expect_new_count = z_count * collector_count_new
        expect_old_count = z_count * collector_count_old
        # 混合组取剩余案件
        expect_mix_count_new = unassigned_new_case_num - expect_new_count
        expect_mix_count_old = unassigned_old_case_num - expect_old_count
        expect_info = [
            {
                "assigned_group_name": "自动化测试_A1组",
                "assigned_count_new": expect_new_count,
                "assigned_count_old": 0
            },
            {
                "assigned_group_name": "自动化测试_A2组",
                "assigned_count_new": 0,
                "assigned_count_old": expect_old_count
            },
            {
                "assigned_group_name": "自动化测试_A3组",
                "assigned_count_new": expect_mix_count_new,
                "assigned_count_old": 0
            },
            {
                "assigned_group_name": "自动化测试_A3组",
                "assigned_count_new": 0,
                "assigned_count_old": expect_mix_count_old
            }
        ]

    if which_smaller == "only_mix":
        # x=3，y=3，z=2
        # 导入测试数据
        new_count = 9
        old_count = 9
        unassigned_new_case_num = import_cn_cases(overdue_days, "新用户", 1, False, dc.ENV, new_count, "草莓")
        LogUtil.log_info("#### 获取到分案前未分配的新客债务数量=%s" % unassigned_new_case_num)
        unassigned_old_case_num = import_cn_cases(overdue_days, "老用户", 1, False, dc.ENV, old_count, "草莓")
        LogUtil.log_info("#### 获取到分案前未分配的老客债务数量=%s" % unassigned_old_case_num)

        expect_mix_count_new = unassigned_new_case_num
        expect_mix_count_old = unassigned_old_case_num
        expect_info = [
            {
                "assigned_group_name": "自动化测试_A3组",
                "assigned_count_new": expect_mix_count_new,
                "assigned_count_old": 0
            },
            {
                "assigned_group_name": "自动化测试_A3组",
                "assigned_count_new": 0,
                "assigned_count_old": expect_mix_count_old
            }
        ]

    LogUtil.log_info("#### 预估新老客组间配平结果，expect_info=%s" % expect_info)
    return expect_info


# 预估人工兜底结果
def estimate_bottom_to_group(mission_strategy, which_smaller):
    # 获取策略配置
    strategy_info = json.loads(get_mission_strategy(mission_strategy)[0]["content"])
    LogUtil.log_info("################ 反序列化后得到分案策略：%s" % strategy_info["strategies"])
    overdue_days = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["condition"][0]["expr"]
    # 获取逾期天数
    overdue_days = int(re.sub("\D", "", overdue_days))
    # 获取策略参数：小组人均最大平均数
    a1_assigned_avg_num = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["max_avg_amount"]
    a2_assigned_avg_num = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][1]["max_avg_amount"]
    LogUtil.log_info("#### 获取策略参数：小组人均最大平均数，a1_assigned_avg_num=%s，a2_assigned_avg_num=%s"
                     % (a1_assigned_avg_num, a2_assigned_avg_num))
    # 获取策略参数：最大分案平均数
    assign_avg_num = strategy_info["strategies"][1]["assetsToGroupStrategy"]["params"][0]["assignAvgNum"]
    LogUtil.log_info("#### 获取策略参数：最大分案平均数，assign_avg_num=%s" % assign_avg_num)
    # 获取催员在线人数
    # 5人
    a1_collector_info = get_collector_count("自动化测试_A1组")
    # 6人
    a2_collector_info = get_collector_count("自动化测试_A2组")
    if not a1_collector_info:
        raise AssertionError("自动化测试_A1组 在线催员人数不能为0！")
    else:
        a1_collector_num = a1_collector_info[0]["collector_num"]
        LogUtil.log_info("#### 自动化测试_A1组在线催员人数=%s" % a1_collector_num)

    if not a2_collector_info:
        raise AssertionError("自动化测试_A2组 在线催员人数不能为0！")
    else:
        a2_collector_num = a2_collector_info[0]["collector_num"]
        LogUtil.log_info("#### 自动化测试_A2组在线催员人数=%s" % a2_collector_num)
    # 计算已分案件的平均数
    assigned_avg_num = int((a1_assigned_avg_num * a1_collector_num + a2_assigned_avg_num * a2_collector_num) / (a1_collector_num + a2_collector_num))
    if which_smaller == "bottom_smaller":
        # 已分案件的平均数=1
        # 已分案件的平均个数assignedAvgNum 1< 最大分案平均数assignAvgNum 3
        if assigned_avg_num < assign_avg_num:
            pass
        # 计算可以兜底的数量
        # 可以兜底的数量bottomNum=(最大分案平均数 - 已分案件的平均数)*已分案催员人数
        # 可以兜底的数量bottomNum=22，预设符合条件的案件数=23
        bottom_num = (assign_avg_num - assigned_avg_num) * (a1_collector_num + a2_collector_num)
        # 最终可分配的案件数取兜底数量的案件数=22
        final_bottom_num = bottom_num
        # 预期总共能分下去 33
        expect_assigned_count = assigned_avg_num * (a1_collector_num + a2_collector_num) + final_bottom_num
        LogUtil.log_info("#### 预期总共能分下去=%s" % expect_assigned_count)
        # 导入测试数据，34
        count = expect_assigned_count + 1
        import_cn_cases(overdue_days, "", 1, False, dc.ENV, count, "草莓")

    if which_smaller == "bottom_bigger":
        # 已分案件的平均数=1
        # 已分案件的平均个数assignedAvgNum 1< 最大分案平均数assignAvgNum 3
        if assigned_avg_num < assign_avg_num:
            pass
        # 计算可以兜底的数量
        # 可以兜底的数量bottomNum=(最大分案平均数 - 已分案件的平均数)*已分案催员人数
        # 可以兜底的数量bottomNum=22，预设符合条件的案件数=16
        bottom_num = (assign_avg_num - assigned_avg_num) * (a1_collector_num + a2_collector_num)
        # 最终可分配的案件数取兜底数量的案件数=符合条件的案件数=16
        final_bottom_num = 16
        # 预期总共能分下去 27
        expect_assigned_count = assigned_avg_num * (a1_collector_num + a2_collector_num) + final_bottom_num
        # 导入测试数据，27
        count = expect_assigned_count
        import_cn_cases(overdue_days, "", 1, False, dc.ENV, count, "草莓")

    if which_smaller == "without_bottom":
        # 已分案件的平均数=2
        # 已分案件的平均个数assignedAvgNum 2 >= 最大分案平均数assignAvgNum 1
        if assigned_avg_num > assign_avg_num:
            pass
        # 最终可分配的案件数取兜底数量的案件数=0
        final_bottom_num = 0
        # 预期总共能分下去 22
        expect_assigned_count = assigned_avg_num * (a1_collector_num + a2_collector_num) + final_bottom_num
        # 导入测试数据，25
        count = expect_assigned_count + 3
        import_cn_cases(overdue_days, "", 1, False, dc.ENV, count, "草莓")

    LogUtil.log_info("#### 预估兜底后的分案结果，expect_assigned_count=%s" % expect_assigned_count)
    return expect_assigned_count


# 预估能力系数分配结果
def estimate_collector_level(mission_strategy, group_name, is_smaller_than_in_hand=True):
    # 获取策略配置
    strategy_info = json.loads(get_mission_strategy(mission_strategy)[0]["content"])
    LogUtil.log_info("################ 反序列化后得到分案策略：%s" % strategy_info["strategies"])
    overdue_days = strategy_info["strategies"][0]["assetsToGroupStrategy"]["params"][0]["condition"][0]["expr"]
    # 获取逾期天数
    overdue_days = int(re.sub("\D", "", overdue_days))

    # 准备数据
    if mission_strategy == "newAT_abilityCoefficient":
        count = 10
    if mission_strategy == "newAT_abilityCoefficientInHand" and is_smaller_than_in_hand is True:
        count = 20
    if mission_strategy == "newAT_abilityCoefficientInHand" and is_smaller_than_in_hand is False:
        count = 26

    import_cn_cases(overdue_days, "", 1, False, dc.ENV, count, "草莓")

    # 获取在线催员能力系数分布
    collector_level_count_info = get_collector_level_count(group_name)
    # 系数a*对应的催员人数+系数b*对应的催员人数+...+系数n*对应的催员人数
    total_a = 0
    for item in collector_level_count_info:
        for k, v in item.items():
            if k == "level_sum":
                total_a += v
    pd_collector_level_count_info = pd.DataFrame.from_records(data=collector_level_count_info)
    # 新增列total_level_sum，等于所有系数与人数乘积之和
    pd_collector_level_count_info.insert(loc=3, column="total_level_sum", value=total_a)
    LogUtil.log_info("新增列total_level_sum，新增后pd_collector_level_count_info=%s" % pd_collector_level_count_info)
    # 新增列per_level_percent，每个系数能分到的案件占比
    pd_collector_level_count_info.eval('per_level_percent=level_sum/total_level_sum', inplace=True)
    # 保留4位小数，四舍五入
    pd_collector_level_count_info["per_level_percent"] = pd_collector_level_count_info["per_level_percent"].round(4)
    LogUtil.log_info("新增列per_level_percent，每个系数能分到的案件占比，保留4位小数，四舍五入，pd_collector_level_count_info=%s"
                     % pd_collector_level_count_info)
    # 计算每个系数可分到的案件数，向下取整
    pd_collector_level_count_info["assigned_num"] = pd_collector_level_count_info["per_level_percent"] * count
    pd_collector_level_count_info["assigned_num"] = pd_collector_level_count_info["assigned_num"].astype(int)
    LogUtil.log_info("#### 计算每个系数可分到的案件数，向下取整，pd_collector_level_count_info=%s" % pd_collector_level_count_info)
    # 提取列到新建表
    first_expect_list = pd_collector_level_count_info.loc[:, ["level", "per_level_num", "assigned_num"]]
    LogUtil.log_info("#### 提取列到新建表，first_expect_list=%s" % first_expect_list)
    # 计算除最后一个系数外的已分案件之和
    not_last_level_cases_sum = 0
    for i in range(first_expect_list.shape[0] - 1):
        not_last_level_cases_sum += first_expect_list.iloc[i, 2]
    # 最后一个系数可获得的案件数不用占比计算，倒减
    last_level_cases = count - not_last_level_cases_sum
    # 更新最后一个系数可分案件值
    first_expect_list.iloc[first_expect_list.shape[0] - 1, 2] = last_level_cases
    LogUtil.log_info("#### 最后一个系数可分到的案件数倒减，first_expect_list=%s" % first_expect_list)

    # 加列per_case_num，每个系数内人均案件数
    first_expect_list["per_case_num"] = first_expect_list["assigned_num"] / first_expect_list["per_level_num"]
    first_expect_list["per_case_num"] = first_expect_list["per_case_num"].astype(int)
    # 加列per_case_reminder，余数
    first_expect_list["reminder"] = first_expect_list["assigned_num"] % first_expect_list["per_level_num"]
    first_expect_list["reminder"] = first_expect_list["reminder"].astype(int)
    LogUtil.log_info("#### 加完新列后，first_expect_list=%s" % first_expect_list)

    if mission_strategy == "newAT_abilityCoefficient":
        in_hand_limit = 0
        final_expect_list = first_expect_list.loc[:, ["level", "assigned_num"]]
        LogUtil.log_info("#### first_expect_list=%s" % first_expect_list)
        # 转为字典列表后，final_expect_list=[{'level': 80, 'assigned_num': 2}, {'level': 90, 'assigned_num': 2},
        # {'level': 100, 'assigned_num': 2}, {'level': 120, 'assigned_num': 4}]
    if mission_strategy == "newAT_abilityCoefficientInHand" and is_smaller_than_in_hand is True:
        # 取策略的在手限制，在手限制=3
        in_hand_limit = strategy_info["strategies"][0]["assetsToCollectorStrategy"]["params"]["inHandLimit"]
        final_expect_list = first_expect_list.loc[:, ["level", "assigned_num"]]
        # 转为字典列表后，final_expect_list=[{'level': 80, 'assigned_num': 4}, {'level': 90, 'assigned_num': 5},
        # {'level': 100, 'assigned_num': 5}, {'level': 120, 'assigned_num': 6}]
    if mission_strategy == "newAT_abilityCoefficientInHand" and is_smaller_than_in_hand is False:
        # 取策略的在手限制，在手限制=3
        in_hand_limit = strategy_info["strategies"][0]["assetsToCollectorStrategy"]["params"]["inHandLimit"]
        # 前置：分案前所有催员在手=0，如果人均超过在手限制，可分案件数取在手限制
        for i in range(first_expect_list.shape[0]):
            if first_expect_list.iloc[i, 3] > in_hand_limit:
                LogUtil.log_info("#### %s系数 总在线人数=%s，人均=%s，超出在手限制，调整人均数量为在手数量"
                                 % (first_expect_list.iloc[i, 0],
                                    first_expect_list.iloc[i, 1],
                                    first_expect_list.iloc[i, 3]))
                first_expect_list.iloc[i, 3] = in_hand_limit
        # 最终每个系数可分到的案件=每个系数内人均案件数*人数+余数
        first_expect_list["assigned_num"] = first_expect_list["per_case_num"] * first_expect_list["per_level_num"] + first_expect_list["reminder"]
        LogUtil.log_info("#### first_expect_list=%s" % first_expect_list)
        final_expect_list = first_expect_list.loc[:, ["level", "assigned_num"]]
        # 转为字典列表后，final_expect_list=[{'level': 80, 'assigned_num': 5}, {'level': 90, 'assigned_num': 6},
        # {'level': 100, 'assigned_num': 7}, {'level': 120, 'assigned_num': 6}]
    # 转为字典列表，expect_level_list 预计每个系数可分到的案件数
    expect_level_list = final_expect_list.to_dict("records")
    LogUtil.log_info("#### expect_level_list=%s" % expect_level_list)
    return expect_level_list, in_hand_limit

# if __name__ == '__main__':
#     dc.init_dh_env(1, "china", "dev")
#     mission_strategy = "newMission8DaysJob"
#     # import_cn_cases(8, "新用户", 1, False, dc.ENV, 10, "草莓")
#     # 分案 并 获取实际分案结果
#     actual_list, case_behavior_info = get_assign_info(mission_strategy)
#     check_v2_assigned_amount(case_behavior_info, mission_strategy)
