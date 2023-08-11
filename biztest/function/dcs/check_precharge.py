import json

import pandas as pd

from biztest.function.dcs.dcs_db_function import get_clean_scenes_receive_by_item_no, get_clean_accrual_tran_by_item_no, \
    get_clean_precharge_clearing_tran_by_item_no
from biztest.util.asserts.assert_util import Assert
import common.global_const as gc


def check_data(data, **kwargs):
    for key, value in kwargs.items():
        Assert.assert_equal(value, data[key], "%s数据有误" % key)


def check_clean_scenes_receive(item_no, **kwargs):
    rs = get_clean_scenes_receive_by_item_no(item_no)
    check_data(rs[0], **kwargs)


def check_clean_accrual_tran(item_no, **kwargs):
    """
    检查权责数据，取自表clean_accrual_tran：
    1、权责数据总共5期，在放款成功后即会分配
    2、场景方权责数据
    :param item_no:
    :return:
    """
    accrual_tran = get_clean_accrual_tran_by_item_no(item_no, period=1)
    if not accrual_tran:
        raise AssertionError('accrual_tran无数据！')
    part_account_no = kwargs.get("part_account_no", 'v_ruiying')
    guarantee_account_no = kwargs.get("guarantee_account_no", 'v_hefei_weidu_bobei')
    scenes_account_no = kwargs.get("scenes_account_no", 'v_cj_liexiong')
    limit_account_no = kwargs.get("limit_account_no", 'v_px_fangtao')
    exp_scenes_type = kwargs.get("exp_scenes_type", 'lieyin')
    principal_amount = kwargs.get("principal_amount", 11586)
    df_tran = pd.DataFrame.from_records(data=accrual_tran)
    # 按费用类型来检查
    # part
    accrual_tran_part = df_tran.loc[df_tran['accrual_type'] == 'part'].iloc[0].to_dict()
    check_data(accrual_tran_part, account_no=part_account_no)
    # guarantee
    accrual_tran_guarantee = df_tran.loc[df_tran['accrual_type'] == 'guarantee'].iloc[0].to_dict()
    check_data(accrual_tran_guarantee, account_no=guarantee_account_no)
    # scenes
    accrual_tran_scenes = df_tran.loc[df_tran['accrual_type'] == 'scenes'].iloc[0].to_dict()
    check_data(accrual_tran_scenes, account_no=scenes_account_no, scenes_type=exp_scenes_type)
    # limit
    # accrual_tran_limit = df_tran.loc[df_tran['accrual_type'] == 'limit'].iloc[0].to_dict()
    # check_data(accrual_tran_limit, account_no=limit_account_no)
    Assert.assert_equal(df_tran['allocated_amount'].sum(), df_tran['original_amount'].sum(), '权责分配的amount检查不通过')
    Assert.assert_equal(principal_amount, df_tran['original_amount'].sum(), '权责分配的本金总额amount检查不通过')


def check_repay_after_compensate_precharge_clearing_tran(item_no, **kwargs):
    """
    检查小单代偿后还款清分明细：
    1、compensate
    2、repay_before_compensate
    :param item_no:
    :return:
    """
    precharge_clearing_tran = get_clean_precharge_clearing_tran_by_item_no(item_no, trans_type='repay_after_compensate')

    if not precharge_clearing_tran:
        raise AssertionError('precharge_clearing_tran无数据！')

    exp_transfer_out = kwargs.get("exp_transfer_out", 'v_qjj_hk')
    exp_transfer_in = kwargs.get("exp_transfer_in", 'v_hefei_weidu_bobei')
    exp_status = kwargs.get("exp_status", 'new')
    principal_amount = kwargs.get("principal_amount", 11586)

    df_tran = pd.DataFrame.from_records(data=precharge_clearing_tran)
    # 按费用类型来检查
    # principal
    accrual_tran_part = df_tran.loc[df_tran['amount_type'] == 'principal'].iloc[0].to_dict()
    check_data(accrual_tran_part, transfer_in=exp_transfer_in, transfer_out=exp_transfer_out, status=exp_status,
               is_need_settlement='Y')
    # late_interest
    accrual_tran_part = df_tran.loc[df_tran['amount_type'] == 'late_interest'].iloc[0].to_dict()
    check_data(accrual_tran_part, transfer_in=exp_transfer_in, transfer_out=exp_transfer_out, status=exp_status,
               is_need_settlement='Y')
    # 金额验证
    Assert.assert_equal(df_tran.loc[0, 'origin_amount'], df_tran.loc[0, 'amount'], '清分trans本金分配的amount检查不通过')
    Assert.assert_equal(principal_amount, df_tran.loc[1, 'amount'], '清分trans本金分配的amount检查不通过')


def check_clean_precharge_clearing_tran(item_no, **kwargs):
    """
    检查小单清分明细：
    1、repay_before_compensate
    :param item_no:
    :return:
    """
    precharge_clearing_tran = get_clean_precharge_clearing_tran_by_item_no(item_no,
                                                                           trans_type='repay_before_compensate')
    if not precharge_clearing_tran:
        raise AssertionError('precharge_clearing_tran无数据！')

    exp_transfer_out = kwargs.get("exp_transfer_out", 'v_qjj_hk')
    exp_status = kwargs.get("exp_status", 'new')
    part_account_no = kwargs.get("part_account_no", 'v_ruiying')
    guarantee_account_no = kwargs.get("guarantee_account_no", 'v_hefei_weidu_bobei')
    scenes_account_no = kwargs.get("scenes_account_no", 'v_cj_liexiong')
    limit_account_no = kwargs.get("limit_account_no", 'v_px_fangtao_mapping')

    df_tran = pd.DataFrame.from_records(data=precharge_clearing_tran)
    # 按费用类型来检查
    # part
    accrual_tran_part = df_tran.loc[df_tran['accrual_type'] == 'part'].iloc[0].to_dict()
    check_data(accrual_tran_part, transfer_in=part_account_no, transfer_out=exp_transfer_out, status=exp_status,
               is_need_settlement='Y')
    # guarantee
    accrual_tran_guarantee = df_tran.loc[df_tran['accrual_type'] == 'guarantee'].iloc[0].to_dict()
    check_data(accrual_tran_guarantee, transfer_in=guarantee_account_no, transfer_out=exp_transfer_out,
               status=exp_status,
               is_need_settlement='Y')
    # scenes
    accrual_tran_scenes = df_tran.loc[df_tran['accrual_type'] == 'scenes'].iloc[0].to_dict()
    check_data(accrual_tran_scenes, transfer_in=scenes_account_no, scenes_type='lieyin', transfer_out=exp_transfer_out,
               status=exp_status,
               is_need_settlement='Y')
    # limit
    # accrual_tran_limit = df_tran.loc[df_tran['accrual_type'] == 'limit'].iloc[0].to_dict()
    # check_data(accrual_tran_limit, account_no=limit_account_no)
    # 金额验证
    Assert.assert_equal(df_tran.loc[0, 'origin_amount'], df_tran['amount'].sum(), '清分trans本金分配的amount检查不通过')


def check_compensate_clean_precharge_clearing_tran(item_no, **kwargs):
    """
    检查小单清分明细：
    1、compensate
    :param item_no:
    :return:
    """
    precharge_clearing_tran = get_clean_precharge_clearing_tran_by_item_no(item_no, trans_type='compensate')

    if not precharge_clearing_tran:
        raise AssertionError('precharge_clearing_tran无数据！')

    exp_transfer_out = kwargs.get("exp_transfer_out", 'v_hefei_weidu_bobei')
    exp_status = kwargs.get("exp_status", 'new')
    part_account_no = kwargs.get("part_account_no", 'v_ruiying')
    guarantee_account_no = kwargs.get("guarantee_account_no", 'v_hefei_weidu_bobei')
    scenes_account_no = kwargs.get("scenes_account_no", 'v_cj_liexiong')
    limit_account_no = kwargs.get("limit_account_no", 'v_px_fangtao_mapping')
    is_compensate_scenes = kwargs.get("is_compensate_scenes", 'Y')

    df_tran = pd.DataFrame.from_records(data=precharge_clearing_tran)
    # 按费用类型来检查
    # part
    accrual_tran_part = df_tran.loc[df_tran['accrual_type'] == 'part'].iloc[0].to_dict()
    check_data(accrual_tran_part, transfer_in=part_account_no, transfer_out=exp_transfer_out, status=exp_status,
               is_need_settlement='Y')
    # guarantee 出入户一样，无需结算
    accrual_tran_guarantee = df_tran.loc[df_tran['accrual_type'] == 'guarantee'].iloc[0].to_dict()
    check_data(accrual_tran_guarantee, transfer_in=guarantee_account_no, transfer_out=exp_transfer_out,
               status='finished',
               is_need_settlement='N')
    # scenes
    if is_compensate_scenes == 'Y':
        accrual_tran_scenes = df_tran.loc[df_tran['accrual_type'] == 'scenes'].iloc[0].to_dict()
        check_data(accrual_tran_scenes, transfer_in=scenes_account_no, scenes_type='lieyin',
                   transfer_out=exp_transfer_out,
                   status=exp_status,
                   is_need_settlement='Y')
    elif is_compensate_scenes == 'N':
        accrual_tran_scenes = df_tran.loc[df_tran['accrual_type'] == 'scenes'].iloc[0].to_dict()
        check_data(accrual_tran_scenes, transfer_in=scenes_account_no, scenes_type='lieyin',
                   transfer_out=exp_transfer_out,
                   status=exp_status,
                   is_need_settlement='N')
    elif is_compensate_scenes == 'None':
        print("无场景")
    else:
        # 原来的cancel掉
        accrual_tran_scenes = df_tran.loc[df_tran['accrual_type'] == 'scenes'].iloc[0].to_dict()
        check_data(accrual_tran_scenes, transfer_in=scenes_account_no, scenes_type='lieyin',
                   transfer_out=exp_transfer_out,
                   status="cancel",
                   is_need_settlement='N')
        # 新建一条记录入拨备
        accrual_tran_scenes_bb = df_tran.loc[df_tran['accrual_type'] == 'scenes'].iloc[1].to_dict()
        check_data(accrual_tran_scenes_bb, transfer_in=exp_transfer_out, scenes_type='lieyin',
                   transfer_out=exp_transfer_out,
                   status="finished",
                   is_need_settlement='N')
    # limit
    # accrual_tran_limit = df_tran.loc[df_tran['accrual_type'] == 'limit'].iloc[0].to_dict()
    # check_data(accrual_tran_limit, account_no=limit_account_no)
    # 金额验证
    if is_compensate_scenes in ['Y', 'N', 'None']:
        Assert.assert_equal(df_tran.loc[0, 'origin_amount'], df_tran['amount'].sum(), '清分trans本金分配的amount检查不通过')


if __name__ == '__main__':
    gc.init_env("3", "china", "dev")
    # aaa = {
    #     "arr_status": "success",
    #     "trans_status": "finished"
    # }
    # check_precharge_auto_settlement("noloan_qn_20201626407240941073", **aaa)
    is_compensate = {
        "is_scenes_compensate": "cancel",
        "scenes_type": "lieyin"

    }

# check_compensate_clean_precharge_clearing_tran("noloan_qn_20201627007038739804", **is_compensate)
# check_request_log_by_channel("20201621217820224243", "tongrongqianjingjing")
# check_clean_accrual_tran("quanyi_qn_20211635316173154088")
# check_repay_before_compensate_clean_precharge_clearing_tran("quanyi_qn_20211637050690368078")
# check_compensate_clean_precharge_clearing_tran("quanyi_qn_20211637055118101388")
