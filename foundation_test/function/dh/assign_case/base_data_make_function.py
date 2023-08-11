import random

from foundation_test.config.dh.url_config import *
from foundation_test.function.dh.assign_case.assign_db_function import get_unassigned_cases
from foundation_test.util.http.http_util import Http
from foundation_test.util.log.log_util import LogUtil

http = Http()


# 导入国内 测试数据
def import_cn_cases(overdue_days, quality_type, d3_level, specified_overdue_amount, env, count, asset_from_app, overdue_amount=200000):
    LogUtil.log_info("需要准备的债务数量=%s" % count)
    fails = 0
    for i in range(count+60):
        # 获取未分案D1债务数，确认数据是否准备完成
        unassigned_case_info = get_unassigned_cases("现金贷多期", overdue_days, overdue_days, quality_type, d3_level, asset_from_app)
        assignable_case_list = []
        for item in unassigned_case_info:
            for k, v in item.items():
                if k == "debtor_id":
                    assignable_case_list.append(v)
        unassigned_case_num = len(assignable_case_list)
        LogUtil.log_info("#### 当前未分案D1债务数：%s" % unassigned_case_num)
        if unassigned_case_num == count:
            LogUtil.log_info("数据准备成功，当前未分案D1债务数：%s" % unassigned_case_num)
            break
        if unassigned_case_num < count:
            r_url = jc_mock_url + mock_cn_asset_uri
            if specified_overdue_amount is True:
                overdue_amount = random.randint(100000, 400000)
            request_info = {
                "asset_from_app": [asset_from_app],
                "overdue_days": overdue_days,
                "item_cust_flg": [quality_type],
                "d3_level": [d3_level],
                "count": 1,
                "specified_overdue_amount": specified_overdue_amount,
                "overdue_amount": overdue_amount,
                "env": env
            }
            http.http_post(r_url, request_info)
            fails += 1
            LogUtil.log_info("数据尚未准备完成，等待中，等待时间：%s" % fails)
    if fails == 60:
        print("#### 请检查测试环境是否正常运行。")
        return
    return unassigned_case_num
