import json

import pandas as pd

from biztest.function.dcs.check_precharge import check_data
from biztest.function.dcs.dcs_db_function import get_clean_scenes_receive_by_item_no, get_clean_accrual_tran_by_item_no, \
    get_clean_precharge_clearing_tran_by_item_no
from biztest.util.asserts.assert_util import Assert
import common.global_const as gc


def check_principal(item_no, **kwargs):
    """
    检查本金，取自表clean_accrual_tran：
    1、
    :param item_no:
    :return:
    """
    part_account_no = kwargs.get("part_account_no", 'v_qianzhao')
    guarantee_account_no = kwargs.get("guarantee_account_no", 'v_hefei_weidu_bobei')
    scenes_account_no = kwargs.get("scenes_account_no", 'v_cj_liexiong')
    limit_account_no = kwargs.get("limit_account_no", 'v_px_fangtao')
    accrual_tran = get_clean_accrual_tran_by_item_no(item_no, period=1)
    df_tran = pd.DataFrame.from_records(data=accrual_tran)
    principal_amount = 11586

    # 按费用类型来检查
    # part
    accrual_tran_part = df_tran.loc[df_tran['accrual_type'] == 'part'].iloc[0].to_dict()
    check_data(accrual_tran_part, account_no=part_account_no)
    # guarantee
    accrual_tran_guarantee = df_tran.loc[df_tran['accrual_type'] == 'guarantee'].iloc[0].to_dict()
    check_data(accrual_tran_guarantee, account_no=guarantee_account_no)
    # scenes
    accrual_tran_scenes = df_tran.loc[df_tran['accrual_type'] == 'scenes'].iloc[0].to_dict()
    check_data(accrual_tran_scenes, account_no=scenes_account_no, scenes_type='lieyin')
    # limit
    # accrual_tran_limit = df_tran.loc[df_tran['accrual_type'] == 'limit'].iloc[0].to_dict()
    # check_data(accrual_tran_limit, account_no=limit_account_no)
    Assert.assert_equal(df_tran['allocated_amount'].sum(), df_tran['original_amount'].sum(), '权责分配的amount检查不通过')
    Assert.assert_equal(principal_amount, df_tran['original_amount'].sum(), '权责分配的本金总额amount检查不通过')


def check_interest(item_no, **kwargs):
    """
    检查本金，取自表clean_accrual_tran：
    1、
    :param item_no:
    :return:
    """
    part_account_no = kwargs.get("part_account_no", 'v_qianzhao')


if __name__ == '__main__':
    gc.init_env("3", "china", "dev")
    is_compensate = {
        "is_scenes_compensate": "cancel",
        "scenes_type": "lieyin"

    }
check_principal("noloan_qn_20201627007038739804", **is_compensate)
