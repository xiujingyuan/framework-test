# @Time    : 2020/7/30 12:45 下午
# @Author  : yuanxiujing
# @File    : dh_check_function.py
# @Software: PyCharm
from datetime import datetime

from pandas._testing import assert_frame_equal

from foundation_test.function.dh.asset_sync.dh_db_function import *
from foundation_test.util.asserts.assert_util import Assert

import pandas as pd

# asset表核对
from foundation_test.util.tools.tools import change_into_other_date, md5


def check_asset_data(item_no, data_info, asset_status):
    asset_info = get_asset_info_by_item_no(item_no)
    if not asset_info:
        raise AssertionError('asset表无数据！')
    import_asset_from_app = data_info["asset"]["asset_from_app"]
    if import_asset_from_app == '草莓':
        expect_asset_from_system_name = '借款大王'
    if import_asset_from_app == '香蕉':
        expect_asset_from_system_name = '芸豆分'
    Assert.assert_equal(expect_asset_from_system_name, asset_info[0]["asset_from_system_name"],
                        "资产来源系统名称错误！预期：%s，实际：%s" % (expect_asset_from_system_name, asset_info[0]["asset_from_system_name"]))
    Assert.assert_equal(import_asset_from_app, asset_info[0]["asset_from_app"],
                        "资产来源app错误！预期：%s，实际：%s" % (import_asset_from_app, asset_info[0]["asset_from_app"]))
    Assert.assert_equal("现金贷多期", asset_info[0]["asset_type"],
                        "资产类型错误！预期：现金贷多期，实际：%s" % asset_info[0]["asset_type"])
    Assert.assert_equal(data_info["asset"]["asset_version"], asset_info[0]["asset_version"],
                        "版本号错误！预期：%s，实际：%s" % (data_info["asset"]["asset_version"], asset_info[0]["asset_version"]))
    # 核对资产状态、逾期状态、逾期天数
    asset_late_info = pd.DataFrame.from_records(data=asset_info, columns=['asset_status', 'asset_late_days', 'asset_late_status'])
    exp_asset_late = {
        'asset_status': asset_status,
        'asset_late_days': 1,
        'asset_late_status': 'm1'
    }
    exp_asset_late_info = pd.DataFrame.from_records(data=exp_asset_late, columns=['asset_status', 'asset_late_days', 'asset_late_status'], index=[0])
    assert_frame_equal(exp_asset_late_info, asset_late_info)
    # asset表，资产总应还、总已还，数据准备：dict-->DataFrame
    asset_amount = pd.DataFrame.from_records(data=asset_info, columns=['asset_principal_amount', 'asset_repaid_principal_amount',
                                                                       'asset_interest_amount', 'asset_repaid_interest_amount',
                                                                       'asset_fee_amount', 'asset_repaid_fee_amount',
                                                                       'asset_penalty_amount', 'asset_repaid_penalty_amount',
                                                                       'asset_decrease_penalty_amount'])
    mapper = {
        'asset_principal_amount': '应还本金',
        'asset_repaid_principal_amount': '已还本金',
        'asset_interest_amount': '应还利息',
        'asset_repaid_interest_amount': '已还利息',
        'asset_fee_amount': '应还费用',
        'asset_repaid_fee_amount': '已还费用',
        'asset_penalty_amount': '应还违约金',
        'asset_repaid_penalty_amount': '已还违约金',
        'asset_decrease_penalty_amount': '已减免违约金'
    }
    asset_amount.rename(columns=mapper, inplace=True)
    # 导入json中，asset节点资产总应还、已还，数据准备：dict-->DataFrame
    import_asset_amount = pd.DataFrame.from_records(data=data_info["asset"], columns=['asset_principal_amount', 'asset_repaid_principal_amount',
                                                                                      'asset_interest_amount', 'asset_repaid_interest_amount',
                                                                                      'asset_fee_amount', 'asset_repaid_fee_amount',
                                                                                      'asset_penalty_amount', 'asset_repaid_penalty_amount',
                                                                                      'asset_decrease_penalty_amount'], index=[0])
    mapper = {
        'asset_principal_amount': '应还本金',
        'asset_repaid_principal_amount': '已还本金',
        'asset_interest_amount': '应还利息',
        'asset_repaid_interest_amount': '已还利息',
        'asset_fee_amount': '应还费用',
        'asset_repaid_fee_amount': '已还费用',
        'asset_penalty_amount': '应还违约金',
        'asset_repaid_penalty_amount': '已还违约金',
        'asset_decrease_penalty_amount': '已减免违约金'
    }
    import_asset_amount.rename(columns=mapper, inplace=True)
    # 对比导入json、asset表的资产金额
    assert_frame_equal(import_asset_amount, asset_amount)

    # asset表，资产逾期中的应还，数据准备：dict-->DataFrame
    overdue_amount = pd.DataFrame.from_records(data=asset_info, columns=['overdue_principal_amount', 'overdue_interest_amount',
                                                                         'overdue_fee_amount', 'overdue_penalty_amount'])
    mapper = {
        'overdue_principal_amount': '逾期应还本金',
        'overdue_interest_amount': '逾期应还利息',
        'overdue_fee_amount': '逾期应还费用',
        'overdue_penalty_amount': '逾期应还违约金'
    }
    overdue_amount.rename(columns=mapper, inplace=True)
    if asset_status == 'repay':
        expect_overdue_amount = {
            'overdue_principal_amount': 200000,
            'overdue_interest_amount': 3333,
            'overdue_fee_amount': 14776,
            'overdue_penalty_amount': 6888
        }
    if asset_status == 'payoff':
        expect_overdue_amount = {
            'overdue_principal_amount': 0,
            'overdue_interest_amount': 0,
            'overdue_fee_amount': 0,
            'overdue_penalty_amount': 0
        }
    import_overdue_amount = pd.DataFrame.from_records(data=expect_overdue_amount, columns=['overdue_principal_amount', 'overdue_interest_amount',
                                                                                           'overdue_fee_amount', 'overdue_penalty_amount'], index=[0])
    mapper = {
        'overdue_principal_amount': '逾期应还本金',
        'overdue_interest_amount': '逾期应还利息',
        'overdue_fee_amount': '逾期应还费用',
        'overdue_penalty_amount': '逾期应还违约金'
    }
    import_overdue_amount.rename(columns=mapper, inplace=True)
    # 对比逾期应还金额
    assert_frame_equal(import_overdue_amount, overdue_amount)

    # asset表，资产逾期中的已还，数据准备：dict-->DataFrame
    recovery_amount = pd.DataFrame.from_records(data=asset_info, columns=['recovery_principal_amount', 'recovery_interest_amount',
                                                                          'recovery_fee_amount', 'recovery_penalty_amount'])
    mapper = {
        'recovery_principal_amount': '逾期中已还本金',
        'recovery_interest_amount': '逾期中已还利息',
        'recovery_fee_amount': '逾期中已还费用',
        'recovery_penalty_amount': '逾期中已还违约金'
    }
    recovery_amount.rename(columns=mapper, inplace=True)
    expect_recovery_amount = {
        'recovery_principal_amount': 0,
        'recovery_interest_amount': 0,
        'recovery_fee_amount': 0,
        'recovery_penalty_amount': 0
    }
    import_recovery_amount = pd.DataFrame.from_records(data=expect_recovery_amount, columns=['recovery_principal_amount', 'recovery_interest_amount',
                                                                                             'recovery_fee_amount', 'recovery_penalty_amount'], index=[0])
    mapper = {
        'recovery_principal_amount': '逾期中已还本金',
        'recovery_interest_amount': '逾期中已还利息',
        'recovery_fee_amount': '逾期中已还费用',
        'recovery_penalty_amount': '逾期中已还违约金'
    }
    import_recovery_amount.rename(columns=mapper, inplace=True)
    assert_frame_equal(import_recovery_amount, recovery_amount)

    # 资产客户归属
    act_asset_customer = asset_info[0]["original_customer_id"]
    import_customer = get_customer_info_by_from_system_name(expect_asset_from_system_name)
    Assert.assert_equal(import_customer[0]['id'], act_asset_customer, "客户归属错误！预期：%s，实际：%s" % (import_customer[0]['id'], act_asset_customer))


# asset_transaction表还款计划核对
def check_transaction_data(overdue_days, item_no, data_info):
    transaction_info = get_transaction_info_by_asset(item_no)
    if not transaction_info:
        raise AssertionError('asset_transaction表无数据！')
    # asset_transaction表，还款计划核对，数据准备：dict-->DataFrame
    repay_plan = pd.DataFrame.from_records(data=transaction_info, columns=['asset_transaction_type', 'asset_transaction_amount',
                                                                           'asset_transaction_status', 'asset_transaction_expect_finish_time',
                                                                           'asset_transaction_period',
                                                                           'asset_transaction_decrease_amount', 'asset_transaction_repaid_amount'])
    mapper = {
        'asset_transaction_type': '费用类型',
        'asset_transaction_amount': '应还金额',
        'asset_transaction_status': '状态',
        'asset_transaction_expect_finish_time': '预期还款时间',
        'asset_transaction_period': '期次',
        'asset_transaction_decrease_amount': '已减免金额',
        'asset_transaction_repaid_amount': '已还金额'
    }
    repay_plan.rename(columns=mapper, inplace=True)
    repay_plan['费用类型'] = repay_plan.费用类型.apply(
        lambda x: '本金' if x == 'repayprincipal'
        else '利息' if x == 'repayinterest'
        else '贷后管理费' if x == 'repayafter_loan_manage'
        else '技术服务费' if x == 'repaytechnical_service'
        else '服务费' if x == 'repayservice'
        else '逾期利息' if x == 'repaylateinterest'
        else 'fee')
    repay_plan['已还金额'] = repay_plan['已还金额'].astype(int)
    # 导入json中，asset_transactions节点还款计划，数据准备：dict-->DataFrame
    import_repay_plan = pd.DataFrame.from_records(data=data_info["asset_transactions"], columns=['asset_transaction_type', 'asset_transaction_amount',
                                                                                                 'asset_transaction_status',
                                                                                                 'asset_transaction_expect_finish_time',
                                                                                                 'asset_transaction_period',
                                                                                                 'asset_transaction_decrease_amount',
                                                                                                 'asset_transaction_repaid_amount'])
    mapper = {
        'asset_transaction_type': '费用类型',
        'asset_transaction_amount': '应还金额',
        'asset_transaction_status': '状态',
        'asset_transaction_expect_finish_time': '预期还款时间',
        'asset_transaction_period': '期次',
        'asset_transaction_decrease_amount': '已减免金额',
        'asset_transaction_repaid_amount': '已还金额'
    }
    import_repay_plan.rename(columns=mapper, inplace=True)
    import_repay_plan['费用类型'] = import_repay_plan.费用类型.apply(
        lambda x: '本金' if x == 'repayprincipal'
        else '利息' if x == 'repayinterest'
        else '贷后管理费' if x == 'repayafter_loan_manage'
        else '技术服务费' if x == 'repaytechnical_service'
        else '服务费' if x == 'repayservice'
        else '逾期利息' if x == 'repaylateinterest'
        else 'fee')
    import_repay_plan.sort_values(["期次", "费用类型"])
    # 对比导入json、asset_transaction表的还款计划
    assert_frame_equal(import_repay_plan, repay_plan)
    # 核对逾期等级、逾期天数
    late_status = pd.DataFrame.from_records(data=transaction_info, columns=['asset_transaction_period', 'asset_transaction_late_status',
                                                                            'asset_transaction_late_days'])
    mapper = {
        'asset_transaction_period': '期次',
        'asset_transaction_late_status': '逾期等级',
        'asset_transaction_late_days': '逾期天数'
    }
    late_status.rename(columns=mapper, inplace=True)
    late_st = late_status[["逾期等级"]].max().values[0]
    Assert.assert_equal('m1', late_st, '逾期等级错误!预期：m1，实际：%s' % late_st)
    late_da = late_status[['逾期天数']].max().values[0]
    Assert.assert_equal(overdue_days, late_da, '逾期天数错误!预期：%s，实际：%s' % (overdue_days, late_da))


# debtor表债务人核对
def check_debtor_data(item_no, data_info):
    asset_info = get_asset_info_by_item_no(item_no)
    asset_customer = asset_info[0]["original_customer_id"]
    d_enc_idnum = data_info['borrower']['enc_individual_idnum']
    d_info = get_debtor_info(asset_customer, d_enc_idnum)
    if not d_info:
        raise AssertionError('debtor表无数据！')
    # debtor表，债务人信息核对，数据准备：dict-->DataFrame
    debtor_info = pd.DataFrame.from_records(data=d_info, columns=['enc_name',
                                                                  'enc_idnum', 'nation',
                                                                  'enc_tel',
                                                                  'gender', 'residence', 'workplace', 'permanent', 'company',
                                                                  'enc_work_tel',
                                                                  'enc_residence_tel'])
    mapper = {
        'enc_name': "密文姓名", 'enc_idnum': "密文身份证",
        'nation': "民族", 'enc_tel': "密文电话号码", 'gender': "性别",
        'residence': "居住地址", 'workplace': "工作地址", 'permanent': "户籍地址", 'company': "单位名称",
        'enc_work_tel': "密文工作地电话", 'enc_residence_tel': "密文居住地电话"
    }
    debtor_info.rename(columns=mapper, inplace=True)
    # 导入json中，borrower节点选取信息，数据准备：dict-->DataFrame
    import_debtor_info = pd.DataFrame.from_records(data=data_info["borrower"], columns=['enc_individual_name',
                                                                                        'enc_individual_idnum',
                                                                                        'individual_nation',
                                                                                        'enc_individual_tel',
                                                                                        'individual_gender',
                                                                                        'individual_residence',
                                                                                        'individual_workplace',
                                                                                        'individual_permanent',
                                                                                        'individual_company',
                                                                                        'enc_individual_work_tel',
                                                                                        'enc_individual_residence_tel'],
                                                   index=[0])
    mapper = {
        'enc_individual_name': "密文姓名", 'enc_individual_idnum': "密文身份证",
        'individual_nation': "民族",
        'enc_individual_tel': "密文电话号码", 'individual_gender': "性别", 'individual_residence': "居住地址",
        'individual_workplace': "工作地址", 'individual_permanent': "户籍地址", 'individual_company': "单位名称",
        'enc_individual_work_tel': "密文工作地电话",
        'enc_individual_residence_tel': "密文居住地电话"
    }
    import_debtor_info.rename(columns=mapper, inplace=True)
    # 对比导入json、debtor表债务人信息
    assert_frame_equal(import_debtor_info, debtor_info)


# individual表借款人信息核对
def check_individual_data(data_info):
    i_enc_idnum = data_info['borrower']['enc_individual_idnum']
    i_info = get_individual_info(i_enc_idnum)
    if not i_info:
        raise AssertionError('individual表无数据！')
    # individual表，债务人信息核对，数据准备：dict-->DataFrame
    individual_info = pd.DataFrame.from_records(data=i_info, columns=[
        'enc_individual_name', 'enc_individual_idnum', 'individual_gender', 'individual_nation',
        'individual_residence', 'individual_workplace', 'individual_permanent', 'individual_company', 'enc_individual_tel',
        'enc_individual_residence_tel', 'enc_individual_mate_name', 'enc_individual_mate_tel',
        'enc_individual_relative_name', 'individual_relative_relation',
        'enc_individual_relative_tel', 'enc_individual_workmate_name',
        'enc_individual_workmate_tel'
    ])
    # 导入json中，borrower节点选取信息，数据准备：dict-->DataFrame
    import_individual_info = pd.DataFrame.from_records(data=data_info["borrower"], columns=[
        'enc_individual_name', 'enc_individual_idnum', 'individual_gender', 'individual_nation',
        'individual_residence', 'individual_workplace', 'individual_permanent', 'individual_company', 'enc_individual_tel',
        'enc_individual_residence_tel', 'enc_individual_mate_name', 'enc_individual_mate_tel',
        'enc_individual_relative_name', 'individual_relative_relation',
        'enc_individual_relative_tel', 'enc_individual_workmate_name',
        'enc_individual_workmate_tel'],
                                                       index=[0])
    # 对比导入json、debtor表债务人信息
    assert_frame_equal(import_individual_info, individual_info)


# debtor_arrears表债务概览信息核对
def check_debtor_arrears_data(item_no, data_info, asset_status):
    asset_info = get_asset_info_by_item_no(item_no)
    asset_customer = asset_info[0]["original_customer_id"]
    d_enc_idnum = data_info['borrower']['enc_individual_idnum']
    das_info = get_debtor_arrears_info(asset_customer, d_enc_idnum)
    m_asset_info = get_main_asset_info(asset_customer, d_enc_idnum)
    if not das_info:
        raise AssertionError('debtor_arrears表无数据！')
    if asset_status == 'repay':
        main_asset_info = pd.DataFrame.from_records(data=das_info, columns=[
            'status', 'asset_count', 'asset_id', 'asset_type', 'late_status', 'late_days', 'inner_outer'])
        expect_main_asset_info = pd.DataFrame.from_records(data=m_asset_info, columns=[
            'status', 'asset_count', 'asset_id', 'asset_type', 'late_status', 'late_days', 'inner_outer'])
    if asset_status == 'payoff':
        exp_main_asset = {
            'status': 'payoff',
            'asset_count': 0,
            'asset_id': 0,
            'asset_type': '',
            'late_status': '',
            'late_days': 0,
            'inner_outer': 'inner'
        }
        main_asset_info = pd.DataFrame.from_records(data=das_info, columns=[
            'status', 'asset_count', 'asset_id', 'asset_type', 'late_status', 'late_days', 'inner_outer'])
        expect_main_asset_info = pd.DataFrame.from_records(data=exp_main_asset, columns=[
            'status', 'asset_count', 'asset_id', 'asset_type', 'late_status', 'late_days', 'inner_outer'], index=[0])
    # 1、主资产对比
    assert_frame_equal(expect_main_asset_info, main_asset_info)
    # 2、债务金额对比，总资产应还、已还、逾期应还、逾期已还
    expect_calculate_das_amount = get_calculate_das_amount(asset_customer, d_enc_idnum)
    # debtor_arrears表，总资产应还
    das_amount = pd.DataFrame.from_records(data=das_info, columns=[
        'principal_amount', 'interest_amount', 'fee_amount', 'penalty_amount', 'arrears_total_amount'])
    # debtor_arrears表，总资产已还
    das_repaid_amount = pd.DataFrame.from_records(data=das_info, columns=[
        'repaid_principal_amount', 'repaid_interest_amount', 'repaid_fee_amount', 'repaid_penalty_amount', 'repaid_total_amount'])
    # debtor_arrears表，逾期应还
    das_overdue_amount = pd.DataFrame.from_records(data=das_info, columns=[
        'overdue_principal_amount', 'overdue_interest_amount', 'overdue_fee_amount', 'overdue_penalty_amount', 'overdue_total_amount'])
    # debtor_arrears表，逾期已还
    das_recovery_amount = pd.DataFrame.from_records(data=das_info, columns=[
        'recovery_principal_amount', 'recovery_interest_amount', 'recovery_fee_amount', 'recovery_penalty_amount', 'recovery_total_amount'])
    if asset_status == 'repay':
        # 根据债务下子资产计算，总资产应还
        expect_das_amount = pd.DataFrame.from_records(data=expect_calculate_das_amount, columns=[
            'principal_amount', 'interest_amount', 'fee_amount', 'penalty_amount', 'arrears_total_amount']).astype(int)
        # 根据债务下子资产计算，总资产已还
        expect_das_repaid_amount = pd.DataFrame.from_records(data=expect_calculate_das_amount, columns=[
            'repaid_principal_amount', 'repaid_interest_amount', 'repaid_fee_amount', 'repaid_penalty_amount', 'repaid_total_amount']).astype(int)
        # 根据债务下子资产计算，逾期应还
        expect_das_overdue_amount = pd.DataFrame.from_records(data=expect_calculate_das_amount, columns=[
            'overdue_principal_amount', 'overdue_interest_amount', 'overdue_fee_amount', 'overdue_penalty_amount',
            'overdue_total_amount']).astype(int)
        # 根据债务下子资产计算，逾期已还
        expect_das_recovery_amount = pd.DataFrame.from_records(data=expect_calculate_das_amount, columns=[
            'recovery_principal_amount', 'recovery_interest_amount', 'recovery_fee_amount', 'recovery_penalty_amount',
            'recovery_total_amount']).astype(int)
    if asset_status == 'payoff':
        # 债务的总资产应还
        exp_das_amount = {
            'principal_amount': 0, 'interest_amount': 0, 'fee_amount': 0, 'penalty_amount': 0, 'arrears_total_amount': 0
        }
        expect_das_amount = pd.DataFrame.from_records(data=exp_das_amount, columns=[
            'principal_amount', 'interest_amount', 'fee_amount', 'penalty_amount', 'arrears_total_amount'], index=[0])
        # 债务的总资产已还
        exp_das_repaid_amount = {
            'repaid_principal_amount': 0, 'repaid_interest_amount': 0, 'repaid_fee_amount': 0, 'repaid_penalty_amount': 0, 'repaid_total_amount': 0
        }
        expect_das_repaid_amount = pd.DataFrame.from_records(data=exp_das_repaid_amount, columns=[
            'repaid_principal_amount', 'repaid_interest_amount', 'repaid_fee_amount', 'repaid_penalty_amount', 'repaid_total_amount'], index=[0])
        # 债务的总资产逾期应还
        exp_das_overdue_amount = {
            'overdue_principal_amount': 0, 'overdue_interest_amount': 0, 'overdue_fee_amount': 0, 'overdue_penalty_amount': 0,
            'overdue_total_amount': 0
        }
        expect_das_overdue_amount = pd.DataFrame.from_records(data=exp_das_overdue_amount, columns=[
            'overdue_principal_amount', 'overdue_interest_amount', 'overdue_fee_amount', 'overdue_penalty_amount', 'overdue_total_amount'], index=[0])
        # 债务的总资产逾期已还
        exp_das_recovery_amount = {
            'recovery_principal_amount': 0, 'recovery_interest_amount': 0, 'recovery_fee_amount': 0, 'recovery_penalty_amount': 0,
            'recovery_total_amount': 0
        }
        expect_das_recovery_amount = pd.DataFrame.from_records(data=exp_das_recovery_amount, columns=[
            'recovery_principal_amount', 'recovery_interest_amount', 'recovery_fee_amount', 'recovery_penalty_amount',
            'recovery_total_amount'], index=[0])
    assert_frame_equal(expect_das_amount, das_amount)
    assert_frame_equal(expect_das_repaid_amount, das_repaid_amount)
    assert_frame_equal(expect_das_overdue_amount, das_overdue_amount)
    assert_frame_equal(expect_das_recovery_amount, das_recovery_amount)


# debtor_asset表债务人资产信息核对
def check_debtor_asset_data(item_no, data_info):
    # 获取debtor_asset表信息
    da_info = get_debtor_asset_by_item_no(item_no)
    if not da_info:
        raise AssertionError('debtor_asset表无数据！')
    da_das_id = da_info[0]['debtor_arrears_id']
    da_d_id = da_info[0]['debtor_id']
    da_enc_idnum = da_info[0]['enc_debtor_idnum']
    da_asset_id = da_info[0]['asset_id']
    # 准备期望值
    asset_info = get_asset_info_by_item_no(item_no)
    asset_customer = asset_info[0]["original_customer_id"]
    expect_enc_idnum = data_info['borrower']['enc_individual_idnum']
    das_info = get_debtor_arrears_info(asset_customer, expect_enc_idnum)
    expect_das_id = das_info[0]['id']
    expect_d_id = das_info[0]['debtor_id']
    expect_asset_id = asset_info[0]['asset_id']
    Assert.assert_equal(expect_das_id, da_das_id, '债务概览ID错误！预期：%s，实际：%s' % (expect_das_id, da_das_id))
    Assert.assert_equal(expect_d_id, da_d_id, '债务人ID错误！预期：%s，实际：%s' % (expect_d_id, da_d_id))
    Assert.assert_equal(expect_enc_idnum, da_enc_idnum, '债务人身份证号码错误！预期：%s，实际：%s' % (expect_enc_idnum, da_enc_idnum))
    Assert.assert_equal(expect_asset_id, da_asset_id, '资产ID错误！预期：%s，实际：%s' % (expect_asset_id, da_asset_id))


# asset_ref_subject表资产与借款人的关联关系核对
def check_asset_ref_subject(item_no, data_info):
    d_enc_idnum = data_info['borrower']['enc_individual_idnum']
    individual_info = get_individual_info(d_enc_idnum)
    asset_info = get_asset_info_by_item_no(item_no)
    ars_info = get_asset_ref_subject(asset_info[0]['asset_id'])
    if not ars_info:
        raise AssertionError('asset_ref_subject表无数据！')
    Assert.assert_equal("borrow", ars_info[0]['asset_ref_subject_type'], '借款人类型错误！预期：borrow，实际：%s'
                        % ars_info[0]['asset_ref_subject_type'])
    Assert.assert_equal("repay", ars_info[1]['asset_ref_subject_type'], '借款人类型错误！预期：repay，实际：%s'
                        % ars_info[1]['asset_ref_subject_type'])
    Assert.assert_equal(individual_info[0]['individual_id'], ars_info[0]['asset_ref_subject_ref_id'], '借款人ID关联错误！预期：%s，实际：%s'
                        % (individual_info[0]['individual_id'], ars_info[0]['asset_ref_subject_ref_id']))
    Assert.assert_equal('individual', ars_info[0]['asset_ref_subject_ref_type'], '借款人ID关联错误！预期：individual，实际：%s'
                        % ars_info[0]['asset_ref_subject_ref_type'])


# debtor_collect表债务进件日期核对
def check_debtor_collect(item_no, data_info):
    asset_info = get_asset_info_by_item_no(item_no)
    asset_customer = asset_info[0]["original_customer_id"]
    d_enc_idnum = data_info['borrower']['enc_individual_idnum']
    d_info = get_debtor_info(asset_customer, d_enc_idnum)
    new_debtor_time_info = get_debtor_collect(d_info[0]['id'])
    if not new_debtor_time_info:
        raise AssertionError('debtor_collect表无数据！')
    new_debtor_time = new_debtor_time_info[0]['new_debtor_time']
    expect_new_debtor_time = datetime.now().strftime("%Y-%m-%d")
    actual_new_debtor_time = datetime.strptime(new_debtor_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
    # 对比债务进件时间，只比日期
    Assert.assert_equal(expect_new_debtor_time, actual_new_debtor_time,
                        '债务进件时间错误！预期：%s，实际：%s' % (expect_new_debtor_time, actual_new_debtor_time))


# asset_inner_outer表资产内外状态
def check_inner_outer(item_no, inner_outer_state):
    state_info = get_inner_outer(item_no)
    if not state_info:
        raise AssertionError('asset_inner_outer表无数据！')
    act_state = state_info[0]["state"]
    # 对比内外标识是否正确
    Assert.assert_equal(inner_outer_state, act_state,
                        'asset_inner_outer状态错误！预期：%s，实际：%s' % (inner_outer_state, act_state))


# asset_history表统计资产历史信息
def check_asset_history(item_no, data_info):
    asset_info = get_asset_info_by_item_no(item_no)
    asset_customer = asset_info[0]["original_customer_id"]
    d_enc_idnum = data_info['borrower']['enc_individual_idnum']
    d_info = get_debtor_info(asset_customer, d_enc_idnum)
    # debtor表，取债务人信息，数据准备：dict-->DataFrame
    exp_debtor_info = pd.DataFrame.from_records(data=d_info, columns=['enc_name', 'enc_idnum', 'enc_tel'])
    asset_history_info = get_asset_history(item_no)
    if not asset_history_info:
        raise AssertionError('asset_history表无数据！')
    act_history_debtor_info = pd.DataFrame.from_records(data=asset_history_info, columns=['enc_borrow_name',
                                                                                          'enc_borrow_idnum', 'enc_borrow_tel'
                                                                                          ])
    mapper = {
        'enc_borrow_name': 'enc_name',
        'enc_borrow_idnum': 'enc_idnum',
        'enc_borrow_tel': 'enc_tel',
    }
    act_history_debtor_info.rename(columns=mapper, inplace=True)
    # 核对asset_history中的债务人信息
    assert_frame_equal(exp_debtor_info, act_history_debtor_info)
    act_history_decrease_penalty_amount = asset_history_info[0]["asset_decrease_penalty_amount"]
    Assert.assert_equal(asset_info[0]["asset_decrease_penalty_amount"], act_history_decrease_penalty_amount,
                        '总减免金额错误！预期：%s，实际：%s' % (asset_info[0]["asset_decrease_penalty_amount"], act_history_decrease_penalty_amount))
    act_history_late_days = asset_history_info[0]["asset_late_days"]
    Assert.assert_equal(asset_info[0]["asset_late_days"], act_history_late_days,
                        '逾期天数错误！预期：%s，实际：%s' % (asset_info[0]["asset_late_days"], act_history_late_days))


# 特殊资产：注销、作废，核对
def check_void_or_writeoff_asset(item_no, asset_status):
    """
    资产注销、作废，逾期中已还清零、资产状态变更
    """
    asset_info = get_asset_info_by_item_no(item_no)
    act_asset_status = asset_info[0]["asset_status"]
    Assert.assert_equal(asset_status, act_asset_status,
                        '资产状态错误！预期：%s，实际：%s' % (asset_status, act_asset_status))
    Assert.assert_equal(0, asset_info[0]["recovery_principal_amount"],
                        '逾期中已还本金错误！预期：0，实际：%s' % asset_info[0]["recovery_principal_amount"])
    Assert.assert_equal(0, asset_info[0]["recovery_interest_amount"],
                        '逾期中已还利息错误！预期：0，实际：%s' % asset_info[0]["recovery_interest_amount"])
    Assert.assert_equal(0, asset_info[0]["recovery_fee_amount"],
                        '逾期中已还费用错误！预期：0，实际：%s' % asset_info[0]["recovery_fee_amount"])
    Assert.assert_equal(0, asset_info[0]["recovery_penalty_amount"],
                        '逾期中已还违约金错误！预期：0，实际：%s' % asset_info[0]["recovery_penalty_amount"])


# asset_summary_recovery表总资产变动表
def check_asset_summary_recovery(item_no, repay_date, asset_status, repay_status='', is_inverse=False):
    summary_recovery_info = get_summary_recovery(item_no)
    print("###  summary_recovery_info=", summary_recovery_info)
    if not summary_recovery_info:
        raise AssertionError('asset_summary_recovery表无数据！')
    # 核对当前回款流水中，还款时间
    Assert.assert_equal(repay_date, summary_recovery_info[0]["repay_date"],
                        '还款时间错误！预期：%s，实际：%s' % (repay_date, summary_recovery_info[0]["repay_date"]))
    if is_inverse is False:
        # 1、逾期期次部分还款----overdue_repay_period_part----第1期息费全还、本金部分还款，2、3不还
        if asset_status == "repay" and repay_status == "overdue_repay_period_part":
            act_summary_recovery_info = pd.DataFrame.from_records(data=summary_recovery_info, columns=[
                'principal_amount', 'recovery_principal_amount',
                'interest_amount', 'recovery_interest_amount',
                'penalty_amount', 'decrease_penalty_amount', 'recovery_penalty_amount',
                'fee_amount', 'recovery_fee_amount',
                'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount',
                'repaid_fee_amount', 'repaid_penalty_amount'])
            cols = list(act_summary_recovery_info)
            for col in cols:
                print("#### act_summary_recovery_info:\n", act_summary_recovery_info[col].name, act_summary_recovery_info[col].values)
            exp_summary_recovery_info = {
                'principal_amount': 132228, 'recovery_principal_amount': 30000,
                'interest_amount': 0, 'recovery_interest_amount': 0,
                'penalty_amount': 10456, 'decrease_penalty_amount': 7000, 'recovery_penalty_amount': 3456,
                'fee_amount': 0, 'recovery_fee_amount': 0, 'repaid_total_amount': 42640,
                'repaid_principal_amount': 30000, 'repaid_interest_amount': 3333,
                'repaid_fee_amount': 5851, 'repaid_penalty_amount': 3456
            }
            expect_summary_recovery_info = pd.DataFrame.from_records(data=exp_summary_recovery_info, columns=[
                'principal_amount', 'recovery_principal_amount',
                'interest_amount', 'recovery_interest_amount',
                'penalty_amount', 'decrease_penalty_amount', 'recovery_penalty_amount',
                'fee_amount', 'recovery_fee_amount',
                'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount',
                'repaid_fee_amount', 'repaid_penalty_amount'], index=[0])
            # 对比当次回款中，逾期中应还、逾期中已还、本次催回
            act_summary_recovery_info = act_summary_recovery_info.astype(int)
            assert_frame_equal(expect_summary_recovery_info, act_summary_recovery_info)
            """
            回款流水的asset节点下status=repay 或 当前回款流水中有逾期中的还款计划（逾期天数不等于0）时：
            1、asset_status=repay、
            2、late_status=对应的逾期等级（逾期等级 m1(1-30);m2(31-60);m3(61-90);m4(91-180);m5(181-360);m6(361-720);m7(720+)）
            3、late_days=当前回款流水中，未完成状态还款计划的最大逾期天数
            """
            # 核对当前回款流水中，资产状态
            check_status_late_days(asset_status, item_no, summary_recovery_info)

        # 2、逾期期次全部还款----overdue_repay_period_payoff----第1期本息费全还，2、3不还
        if asset_status == "repay" and repay_status == "overdue_repay_period_payoff":
            asset_status = "payoff"
            summary_recovery_info = get_summary_recovery(item_no)
            act_summary_recovery_info = pd.DataFrame.from_records(data=summary_recovery_info, columns=[
                'principal_amount', 'recovery_principal_amount',
                'interest_amount', 'recovery_interest_amount',
                'penalty_amount', 'decrease_penalty_amount', 'recovery_penalty_amount',
                'fee_amount', 'recovery_fee_amount',
                'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount',
                'repaid_fee_amount', 'repaid_penalty_amount'])
            exp_summary_recovery_info = {
                'principal_amount': 0, 'recovery_principal_amount': 0,
                'interest_amount': 0, 'recovery_interest_amount': 0,
                'penalty_amount': 0, 'decrease_penalty_amount': 0, 'recovery_penalty_amount': 0,
                'fee_amount': 0, 'recovery_fee_amount': 0, 'repaid_total_amount': 144868,
                'repaid_principal_amount': 132228, 'repaid_interest_amount': 3333,
                'repaid_fee_amount': 5851, 'repaid_penalty_amount': 3456
            }
            expect_summary_recovery_info = pd.DataFrame.from_records(data=exp_summary_recovery_info, columns=[
                'principal_amount', 'recovery_principal_amount',
                'interest_amount', 'recovery_interest_amount',
                'penalty_amount', 'decrease_penalty_amount', 'recovery_penalty_amount',
                'fee_amount', 'recovery_fee_amount',
                'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount',
                'repaid_fee_amount', 'repaid_penalty_amount'], index=[0])
            # 对比当次回款中，逾期中应还、逾期中已还、本次催回
            act_summary_recovery_info = act_summary_recovery_info.astype(int)
            assert_frame_equal(expect_summary_recovery_info, act_summary_recovery_info)
            """
            回款流水的asset节点下status=payoff 或 当前回款流水中没有逾期中的还款计划（逾期天数=0）时：
            1、asset_status=payoff、
            2、late_status=asset表的asset_late_status、
            3、late_days=asset表的asset_late_days
            """
            # 核对当前回款流水中，资产状态
            check_status_late_days(asset_status, item_no, summary_recovery_info)

            # 3、逾期期次+非逾期期次----overdue_repay_all_payoff----1、2、3本息费全部还款
            if asset_status == "payoff" and repay_status == "overdue_repay_all_payoff":
                summary_recovery_info = get_summary_recovery(item_no)
                act_summary_recovery_info = pd.DataFrame.from_records(data=summary_recovery_info, columns=[
                    'principal_amount', 'recovery_principal_amount',
                    'interest_amount', 'recovery_interest_amount',
                    'penalty_amount', 'decrease_penalty_amount', 'recovery_penalty_amount',
                    'fee_amount', 'recovery_fee_amount',
                    'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount',
                    'repaid_fee_amount', 'repaid_penalty_amount'])
                exp_summary_recovery_info = {
                    'principal_amount': 0, 'recovery_principal_amount': 0,
                    'interest_amount': 0, 'recovery_interest_amount': 0,
                    'penalty_amount': 0, 'decrease_penalty_amount': 0, 'recovery_penalty_amount': 0,
                    'fee_amount': 0, 'recovery_fee_amount': 0, 'repaid_total_amount': 427692,
                    'repaid_principal_amount': 396684, 'repaid_interest_amount': 9999,
                    'repaid_fee_amount': 17553, 'repaid_penalty_amount': 3456
                }
                expect_summary_recovery_info = pd.DataFrame.from_records(data=exp_summary_recovery_info, columns=[
                    'principal_amount', 'recovery_principal_amount',
                    'interest_amount', 'recovery_interest_amount',
                    'penalty_amount', 'decrease_penalty_amount', 'recovery_penalty_amount',
                    'fee_amount', 'recovery_fee_amount',
                    'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount',
                    'repaid_fee_amount', 'repaid_penalty_amount'], index=[0])
                # 对比当次回款中，逾期中应还、逾期中已还、本次催回
                act_summary_recovery_info = act_summary_recovery_info.astype(int)
                assert_frame_equal(expect_summary_recovery_info, act_summary_recovery_info)
                """
                回款流水的asset节点下status=payoff 或 当前回款流水中没有逾期中的还款计划（逾期天数=0）时：
                1、asset_status=payoff、
                2、late_status=asset表的asset_late_status、
                3、late_days=asset表的asset_late_days
                """
                # 核对当前回款流水中，资产状态
                check_status_late_days(asset_status, item_no, summary_recovery_info)

    if is_inverse is True:
        act_summary_recovery_info = pd.DataFrame.from_records(data=summary_recovery_info, columns=[
            'principal_amount', 'recovery_principal_amount',
            'interest_amount', 'recovery_interest_amount',
            'penalty_amount', 'decrease_penalty_amount', 'recovery_penalty_amount',
            'fee_amount', 'recovery_fee_amount',
            'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount',
            'repaid_fee_amount', 'repaid_penalty_amount'])
        exp_summary_recovery_info = {
            'principal_amount': 132228, 'recovery_principal_amount': 0,
            'interest_amount': 3333, 'recovery_interest_amount': 0,
            'penalty_amount': 10456, 'decrease_penalty_amount': 7000, 'recovery_penalty_amount': 0,
            'fee_amount': 5851, 'recovery_fee_amount': 0, 'repaid_total_amount': -144868,
            'repaid_principal_amount': -132228, 'repaid_interest_amount': -3333,
            'repaid_fee_amount': -5851, 'repaid_penalty_amount': -3456
        }
        expect_summary_recovery_info = pd.DataFrame.from_records(data=exp_summary_recovery_info, columns=[
            'principal_amount', 'recovery_principal_amount',
            'interest_amount', 'recovery_interest_amount',
            'penalty_amount', 'decrease_penalty_amount', 'recovery_penalty_amount',
            'fee_amount', 'recovery_fee_amount',
            'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount',
            'repaid_fee_amount', 'repaid_penalty_amount'], index=[0])
        # 对比当次回款中，逾期中应还、逾期中已还、本次催回
        act_summary_recovery_info = act_summary_recovery_info.astype(int)
        assert_frame_equal(expect_summary_recovery_info, act_summary_recovery_info)
        """
        回款流水的asset节点下status=repay 或 当前回款流水中有逾期中的还款计划（逾期天数不等于0）时：
        1、asset_status=repay、
        2、late_status=对应的逾期等级（逾期等级 m1(1-30);m2(31-60);m3(61-90);m4(91-180);m5(181-360);m6(361-720);m7(720+)）、
        3、late_days=当前回款流水中，未完成状态还款计划的最大逾期天数
        """
        # 核对当前回款流水中，资产状态
        check_status_late_days(asset_status, item_no, summary_recovery_info)


def check_status_late_days(asset_status, item_no, summary_recovery_info):
    # 核对当前回款流水中，资产状态
    Assert.assert_equal(asset_status, summary_recovery_info[0]["asset_status"],
                        '当前回款流水中，资产状态错误！预期：%s，实际：%s' % (asset_status, summary_recovery_info[0]["asset_status"]))
    asset_info = get_asset_info_by_item_no(item_no)
    expect_late_status = asset_info[0]["asset_late_status"]
    expect_late_days = asset_info[0]["asset_late_days"]
    # 核对当前回款流水中，逾期中还款计划的最大逾期天数
    Assert.assert_equal(expect_late_days, summary_recovery_info[0]["late_days"],
                        '当前回款流水中，逾期中还款计划的最大逾期天数错误！预期：%s，实际：%s' % (
                        expect_late_days, summary_recovery_info[0]["late_days"]))
    # 核对当前回款流水中，逾期等级
    Assert.assert_equal(expect_late_status, summary_recovery_info[0]["late_status"],
                        '逾期等级错误！预期：%s，实际：%s' % (expect_late_status, summary_recovery_info[0]["late_status"]))


# asset_period_recovery表资产按期次的变动回款表
def check_asset_period_recovery(item_no, repay_status='', repay_date=''):
    summary_recovery_info = get_summary_recovery(item_no)
    asset_period_recovery_info = get_period_recovery(item_no)
    if not asset_period_recovery_info:
        raise AssertionError('asset_period_recovery表无数据！')

    act_period_status = asset_period_recovery_info[0]["period_status"]
    act_repay_date = asset_period_recovery_info[0]["repay_date"]
    expect_repay_date = repay_date
    # 核对期次状态
    if repay_status == "overdue_repay_period_payoff" or repay_status == "overdue_repay_all_payoff":
        expect_period_status = "payoff"
    else:
        expect_period_status = "repay"
    Assert.assert_equal(expect_period_status, act_period_status,
                        '期次状态错误！预期：%s，实际：%s' % (expect_period_status, act_period_status))
    Assert.assert_equal(expect_repay_date, act_repay_date,
                        '还款时间错误！预期：%s，实际：%s' % (expect_repay_date, act_repay_date))

    # 核对除期次状态以外的信息
    if repay_status != "overdue_repay_all_payoff":
        act_period_recovery_info = pd.DataFrame.from_records(data=asset_period_recovery_info, columns=[
            'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount', 'repaid_fee_amount',
            'repaid_penalty_amount', 'late_days', 'late_status', 'asset_status'])
        exp_period_recovery_info = pd.DataFrame.from_records(data=summary_recovery_info, columns=[
            'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount', 'repaid_fee_amount',
            'repaid_penalty_amount', 'late_days', 'late_status', 'asset_status'])
        # 对比asset_period_recovery的非期次信息是否与asset_summary_recovery一致
        assert_frame_equal(exp_period_recovery_info, act_period_recovery_info)
    if repay_status == "overdue_repay_all_payoff":
        act_period_recovery_info = pd.DataFrame.from_records(data=asset_period_recovery_info, columns=[
            'repaid_period',
            'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount', 'repaid_fee_amount',
            'repaid_penalty_amount', 'late_days', 'late_status', 'asset_status'])
        expect_period_recovery_info_1 = [
            {'repaid_period': 1, 'repaid_total_amount': 144868, 'repaid_principal_amount': 132228,
             'repaid_interest_amount': 3333, 'repaid_fee_amount': 5851,
             'repaid_penalty_amount': 3456,
             'late_days': 1, 'late_status': 'm1', 'asset_status': 'payoff'},
            {'repaid_period': 2, 'repaid_total_amount': 141412, 'repaid_principal_amount': 132228,
             'repaid_interest_amount': 3333, 'repaid_fee_amount': 5851,
             'repaid_penalty_amount': 0,
             'late_days': 0, 'late_status': '', 'asset_status': 'payoff'},
            {'repaid_period': 3, 'repaid_total_amount': 141412, 'repaid_principal_amount': 132228,
             'repaid_interest_amount': 3333, 'repaid_fee_amount': 5851,
             'repaid_penalty_amount': 0,
             'late_days': 0, 'late_status': '', 'asset_status': 'payoff'}
        ]
        expect_period_recovery_info = pd.DataFrame.from_records(data=expect_period_recovery_info_1, columns=[
            'repaid_period',
            'repaid_total_amount', 'repaid_principal_amount', 'repaid_interest_amount', 'repaid_fee_amount',
            'repaid_penalty_amount', 'late_days', 'late_status', 'asset_status'])
        # exp_period_recovery_info_2 = pd.DataFrame.from_records(data=summary_recovery_info, columns=[
        #     'late_days', 'late_status', 'asset_status', 'repay_date'])
        # # 拼接3期的非金额信息
        # exp_period_recovery_info_3 = exp_period_recovery_info_2.append([exp_period_recovery_info_2,
        #                                                                 exp_period_recovery_info_2])
        # # 删除原来索引，重新建立从0开始的索引
        # exp_period_recovery_info_right = exp_period_recovery_info_3.reset_index(drop=True)
        # # 拼接金额、非金额信息
        # expect_period_recovery_info = pd.concat([exp_period_recovery_info_left, exp_period_recovery_info_right], axis=1)
        # 对比asset_period_recovery的非期次信息是否与asset_summary_recovery一致
        act_period_recovery_info['repaid_total_amount'] = act_period_recovery_info['repaid_total_amount'].astype(int)
        act_period_recovery_info['repaid_principal_amount'] = act_period_recovery_info['repaid_principal_amount'].astype(int)
        act_period_recovery_info['repaid_interest_amount'] = act_period_recovery_info['repaid_interest_amount'].astype(int)
        act_period_recovery_info['repaid_fee_amount'] = act_period_recovery_info['repaid_fee_amount'].astype(int)
        act_period_recovery_info['repaid_penalty_amount'] = act_period_recovery_info['repaid_penalty_amount'].astype(int)
        assert_frame_equal(expect_period_recovery_info, act_period_recovery_info)


# collect_recovery表催收员关联逾期催回表
def check_collect_recovery(item_no, repay_date, is_repay_after_today=False):
    collect_recovery_info = get_collect_recovery(item_no)
    print("########  collect_recovery_info=", collect_recovery_info)
    # 撤案后，T + 1日的回款 不计入催员回款
    if is_repay_after_today is True:
        cr_count = get_count_collect_recovery(item_no)
        Assert.assert_equal(0, cr_count[0]["count"],
                            '催员回款记录数错误！预期：0，实际：%s' % cr_count[0]["count"])
    if is_repay_after_today is False:
        summary_recovery_info = get_summary_recovery(item_no)
        print("########  summary_recovery_info=", summary_recovery_info)
        expect_collect_recovery_info = pd.DataFrame.from_records(data=summary_recovery_info, columns=[
            'principal_amount', 'interest_amount', 'fee_amount', 'penalty_amount', 'decrease_penalty_amount', 'repaid_total_amount',
            'repaid_principal_amount', 'repaid_interest_amount', 'repaid_fee_amount', 'repaid_penalty_amount',
            'late_days', 'late_status', 'asset_status', 'repay_date'
        ])
        expect_collect_recovery_info["principal_amount"] = expect_collect_recovery_info["principal_amount"].astype(int)
        expect_collect_recovery_info["interest_amount"] = expect_collect_recovery_info["interest_amount"].astype(int)
        expect_collect_recovery_info["fee_amount"] = expect_collect_recovery_info["fee_amount"].astype(int)
        expect_collect_recovery_info["penalty_amount"] = expect_collect_recovery_info["penalty_amount"].astype(int)
        expect_collect_recovery_info["decrease_penalty_amount"] = expect_collect_recovery_info["decrease_penalty_amount"].astype(int)
        expect_collect_recovery_info["repaid_total_amount"] = expect_collect_recovery_info["repaid_total_amount"].astype(int)
        expect_collect_recovery_info["repaid_principal_amount"] = expect_collect_recovery_info["repaid_principal_amount"].astype(int)
        expect_collect_recovery_info["repaid_interest_amount"] = expect_collect_recovery_info["repaid_interest_amount"].astype(int)
        expect_collect_recovery_info["repaid_fee_amount"] = expect_collect_recovery_info["repaid_fee_amount"].astype(int)
        expect_collect_recovery_info["repaid_penalty_amount"] = expect_collect_recovery_info["repaid_penalty_amount"].astype(int)

        actual_collect_recovery_info = pd.DataFrame.from_records(data=collect_recovery_info, columns=[
            'principal_amount', 'interest_amount', 'fee_amount', 'penalty_amount', 'decrease_penalty_amount', 'repaid_total_amount',
            'repaid_principal_amount', 'repaid_interest_amount', 'repaid_fee_amount', 'repaid_penalty_amount',
            'late_days', 'late_status', 'asset_status', 'repay_date'
        ])
        actual_collect_recovery_info["principal_amount"] = actual_collect_recovery_info["principal_amount"].astype(int)
        actual_collect_recovery_info["interest_amount"] = actual_collect_recovery_info["interest_amount"].astype(int)
        actual_collect_recovery_info["fee_amount"] = actual_collect_recovery_info["fee_amount"].astype(int)
        actual_collect_recovery_info["penalty_amount"] = actual_collect_recovery_info["penalty_amount"].astype(int)
        actual_collect_recovery_info["decrease_penalty_amount"] = actual_collect_recovery_info["decrease_penalty_amount"].astype(int)
        actual_collect_recovery_info["repaid_total_amount"] = actual_collect_recovery_info["repaid_total_amount"].astype(int)
        actual_collect_recovery_info["repaid_principal_amount"] = actual_collect_recovery_info["repaid_principal_amount"].astype(int)
        actual_collect_recovery_info["repaid_interest_amount"] = actual_collect_recovery_info["repaid_interest_amount"].astype(int)
        actual_collect_recovery_info["repaid_fee_amount"] = actual_collect_recovery_info["repaid_fee_amount"].astype(int)
        actual_collect_recovery_info["repaid_penalty_amount"] = actual_collect_recovery_info["repaid_penalty_amount"].astype(int)
        left_cols = list(expect_collect_recovery_info)
        for col in left_cols:
            print("######## expect_collect_recovery_info:\n", expect_collect_recovery_info[col].name, expect_collect_recovery_info[col].values)
        right_cols = list(actual_collect_recovery_info)
        for col in right_cols:
            print("######## actual_collect_recovery_info:\n", actual_collect_recovery_info[col].name, actual_collect_recovery_info[col].values)
        # 对比collect_recovery表与asset_summary_recovery表的金额信息
        assert_frame_equal(expect_collect_recovery_info, actual_collect_recovery_info)
        # 核对非金额信息
        asset_info = get_asset_info_by_item_no(item_no)
        company_info = get_company()
        user_parents_info = get_user_parents()
        mission_log_info = get_mission_log(asset_info[0]["asset_id"], repay_date)
        expect_mission_log_id = mission_log_info[0]["mission_log_id"]
        actual_mission_log_id = collect_recovery_info[0]["mission_log_id"]
        # 核对mission_log_id
        Assert.assert_equal(expect_mission_log_id, actual_mission_log_id,
                            '分案日志id关联错误！预期：%s，实际：%s' % (expect_mission_log_id, actual_mission_log_id))
        # 核对分案日期
        expect_assigned_date = mission_log_info[0]["mission_log_assigned_date"]
        exp_assigned_date = change_into_other_date(expect_assigned_date)
        Assert.assert_equal(exp_assigned_date, str(collect_recovery_info[0]["assigned_date"]),
                            '分配日期关联错误！预期：%s，实际：%s' % (exp_assigned_date, str(collect_recovery_info[0]["assigned_date"])))
        # 核对催员的组织关系
        Assert.assert_equal(mission_log_info[0]["mission_log_assigned_user_id"], collect_recovery_info[0]["user_id"],
                            '所属催收员Id关联错误！预期：%s，实际：%s'
                            % (mission_log_info[0]["mission_log_assigned_user_id"], collect_recovery_info[0]["user_id"]))
        Assert.assert_equal(mission_log_info[0]["mission_log_assigned_user_name"], collect_recovery_info[0]["user_name"],
                            '所属催收员姓名关联错误！预期：%s，实际：%s'
                            % (mission_log_info[0]["mission_log_assigned_user_name"], collect_recovery_info[0]["user_name"]))
        Assert.assert_equal(company_info[0]["company_id"], collect_recovery_info[0]["company_id"],
                            '所属催收员公司ID关联错误！预期：%s，实际：%s'
                            % (company_info[0]["company_id"], collect_recovery_info[0]["company_id"]))
        Assert.assert_equal(company_info[0]["company_name"], collect_recovery_info[0]["company_name"],
                            '所属催收员公司名称关联错误！预期：%s，实际：%s'
                            % (company_info[0]["company_name"], collect_recovery_info[0]["company_name"]))
        Assert.assert_equal(user_parents_info[0]["sys_user_id"], collect_recovery_info[0]["sys_user_id"],
                            '被分配人id关联错误！预期：%s，实际：%s'
                            % (user_parents_info[0]["sys_user_id"], collect_recovery_info[0]["sys_user_id"]))
        Assert.assert_equal(user_parents_info[0]["sys_user_name"], collect_recovery_info[0]["sys_user_name"],
                            '被分配人名字关联错误！预期：%s，实际：%s'
                            % (user_parents_info[0]["sys_user_name"], collect_recovery_info[0]["sys_user_name"]))
        Assert.assert_equal(user_parents_info[0]["group_leader_id"], collect_recovery_info[0]["group_leader_id"],
                            '被分配人组长id关联错误！预期：%s，实际：%s'
                            % (user_parents_info[0]["group_leader_id"], collect_recovery_info[0]["group_leader_id"]))
        Assert.assert_equal(user_parents_info[0]["group_leader_name"], collect_recovery_info[0]["group_leader_name"],
                            '被分配人组长姓名关联错误！预期：%s，实际：%s'
                            % (user_parents_info[0]["group_leader_name"], collect_recovery_info[0]["group_leader_name"]))
        Assert.assert_equal(user_parents_info[0]["director_id"], collect_recovery_info[0]["director_id"],
                            '被分配人主管id关联错误！预期：%s，实际：%s'
                            % (user_parents_info[0]["director_id"], collect_recovery_info[0]["director_id"]))
        Assert.assert_equal(user_parents_info[0]["director_name"], collect_recovery_info[0]["director_name"],
                            '被分配人主管姓名关联错误！预期：%s，实际：%s'
                            % (user_parents_info[0]["director_name"], collect_recovery_info[0]["director_name"]))
        Assert.assert_equal(user_parents_info[0]["manager_id"], collect_recovery_info[0]["manager_id"],
                            '被分配人经理id关联错误！预期：%s，实际：%s'
                            % (user_parents_info[0]["manager_id"], collect_recovery_info[0]["manager_id"]))
        Assert.assert_equal(user_parents_info[0]["manager_name"], collect_recovery_info[0]["manager_name"],
                            '被分配人经理姓名关联错误！预期：%s，实际：%s'
                            % (user_parents_info[0]["manager_name"], collect_recovery_info[0]["manager_name"]))


# asset_tool_package表资产工具包
def check_tool_package(app_name, tool_app_name, channel, system, status):
    value = app_name + tool_app_name + channel + system
    hash_value = md5(value)
    tool_info = get_tool_package(hash_value)
    if app_name == '草莓':
        expect_app_name = '借款大王'
    if app_name == '香蕉':
        expect_app_name = '芸豆借款'
    Assert.assert_equal(expect_app_name, tool_info[0]["app_name"], '主包名错误！预期：%s，实际：%s'
                        % (expect_app_name, tool_info[0]["app_name"]))
    Assert.assert_equal(expect_app_name, tool_info[0]["tool_app_name"], '工具包名错误！预期：%s，实际：%s'
                        % (expect_app_name, tool_info[0]["tool_app_name"]))
    Assert.assert_equal(channel, tool_info[0]["channel"], '工具包渠道错误！预期：%s，实际：%s'
                        % (channel, tool_info[0]["channel"]))
    Assert.assert_equal(system, tool_info[0]["system"], '工具包系统错误！预期：%s，实际：%s'
                        % (system, tool_info[0]["system"]))
    Assert.assert_equal(status, tool_info[0]["status"], '工具包当前状态错误！预期：%s，实际：%s'
                        % (status, tool_info[0]["status"]))
