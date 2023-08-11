# @Time    : 2020/7/29 5:44 下午
# @Author  : yuanxiujing
# @File    : dh_interface.py.py
# @Software: PyCharm
from numpy import long

from foundation_test.config.dh.url_config import *
from foundation_test.function.dh.asset_sync.dh_db_function import get_debtor_asset_by_item_no, get_summary_recovery, get_debtor_arrears_info
from foundation_test.util.tools.tools import *

http = Http()


def asset_bean(overdue_days=1, asset_from_system_name="草莓", asset_repayment_app="", asset_status="repay", item_no=''):
    timestamp = long(int(time.time() * 1000))
    if item_no:
        pass
    else:
        item_no = "dh_auto_test_" + time.strftime("%Y%m%d", time.localtime()) + str(int(time.time() * 1000))

    if asset_from_system_name == "草莓":
        from_system = "strawberry"
    elif asset_from_system_name == "香蕉":
        from_system = "banana"
    else:
        from_system = "dsq"

    body = {
        "asset_item_number": item_no,
        "asset_from_system": from_system,
        "asset_from_app": asset_from_system_name,
        "asset_type": "现金贷",
        "asset_sub_type": "multiple",
        "asset_name": item_no,
        "asset_sign_at": get_date_before_today(day=(overdue_days + 31 * 1)),
        "asset_grant_at": get_date_before_today(day=(overdue_days + 31 * 1)),
        "asset_due_at": get_date_after_today(day=(31 * 2 - overdue_days)),
        "asset_channel": "Paydayloan",
        "asset_interest_amount": 9999,
        "asset_principal_amount": 600000,
        "asset_penalty_amount": 6888,
        "asset_decrease_penalty_amount": 0,
        "asset_fee_amount": 44328,
        "asset_city_code": 652200,
        "asset_status": asset_status,
        "asset_loan_channel": "hengfeng",
        "asset_period_type": "month",
        "asset_period_count": 3,
        "asset_period_days": 0,
        "asset_ref_order_no": "",
        "asset_ref_order_type": "game_bill",
        "asset_risk_level": "2",
        "asset_sub_order_type": "",
        "asset_product_name": "元宝钱包",
        "asset_actual_grant_at": get_date_before_today(day=(overdue_days + 31 * 1)),
        "asset_owner": "KN",
        "asset_version": timestamp,
        "asset_credit_term": 0,
        "asset_repayment_app": asset_repayment_app,
        "ref_order_loan_channel": ""
    }
    if asset_status == 'repay' or asset_status == 'void' or asset_status == 'writeoff':
        amount_body = {
            "asset_repaid_interest_amount": 0,
            "asset_repaid_principal_amount": 0,
            "asset_repaid_penalty_amount": 0,
            "asset_repaid_fee_amount": 0,
            "asset_repaid_amount": 0
        }
    if asset_status == 'payoff':
        amount_body = {
            "asset_repaid_interest_amount": 3333,
            "asset_repaid_principal_amount": 200000,
            "asset_repaid_penalty_amount": 6888,
            "asset_repaid_fee_amount": 14776,
            "asset_repaid_amount": 224997
        }
    body.update(amount_body)
    return json.dumps(body, ensure_ascii=False)


def individual_bean():
    three_element = get_three_element()
    enc_user_name = three_element["enc_user_name"]
    enc_id_number = three_element["enc_id_number"]
    enc_mobile = three_element["enc_mobile"]
    body = {
        "enc_individual_name": enc_user_name,
        "enc_individual_idnum": enc_id_number,
        "enc_individual_tel": enc_mobile,
        "enc_individual_work_tel": "enc_01_2987735343379777536_174",
        "enc_individual_residence_tel": "enc_01_2987735343631435776_220",
        "enc_individual_mate_name": "enc_04_2987735343815985152_591",
        "enc_individual_mate_tel": "enc_01_2987735344000534528_740",
        "enc_individual_relative_name": "enc_04_2987735344235415552_975",
        "enc_individual_relative_tel": "enc_01_2987735344470296576_510",
        "enc_individual_workmate_name": "enc_04_2987735344688400384_334",
        "enc_individual_workmate_tel": "enc_01_2987735344923281408_563",

        "code_individual_name": "",
        "code_individual_idnum": "",
        "code_individual_tel": "",
        "code_individual_work_tel": "",
        "code_individual_residence_tel": "",
        "code_individual_mate_name": "",
        "code_individual_mate_tel": "",
        "code_individual_relative_name": "",
        "code_individual_relative_tel": "",
        "code_individual_workmate_name": "",
        "code_individual_workmate_tel": "",

        "individual_name": "",
        "individual_idnum": "",
        "individual_tel": "",
        "individual_work_tel": "",
        "individual_residence_tel": "",
        "individual_mate_name": "",
        "individual_mate_tel": "",
        "individual_relative_name": "",
        "individual_relative_tel": "",
        "individual_workmate_name": "",
        "individual_workmate_tel": "",

        "individual_gender": random.choice(['f', 'm']),
        "individual_residence": "广东省广州市番禺区大石镇辛田大街11号",
        "individual_workplace": "广东省广州市番禺区广州番禺南桥店",
        "individual_permanent": "广东省雷州市附城镇岚北村027号吴东巷",
        "individual_company": "聚轩休闲会所有限公司",
        "individual_relative_relation": "3",
        "individual_remark": "",
        "individual_nation": "汉",
        "individual_email": three_element["mobile"] + "@qq.com"
    }
    return json.dumps(body, ensure_ascii=False)


# 放款卡
def receive_card():
    body = {
        "card_bank_code": "icbc",
        "card_bank_name": "中国工商银行",
        "card_num_encrypt": "enc_03_3562749239715432448_081"
    }
    return json.dumps(body, ensure_ascii=False)


# 仅第一期逾期
def transaction_bean(overdue_days='1', asset_status='repay'):
    transactions = []
    # 2、3期抽出作为公共数据
    for i in range(1, 3):
        repayprincipal = {
            "asset_transaction_type": "repayprincipal",
            "asset_transaction_amount": 200000,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, -i),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": i + 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repayinterest = {
            "asset_transaction_type": "repayinterest",
            "asset_transaction_amount": 3333,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, -i),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": i + 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repayafter_loan_manage = {
            "asset_transaction_type": "repayafter_loan_manage",
            "asset_transaction_amount": 10000,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, -i),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": i + 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repaytechnical_service = {
            "asset_transaction_type": "repaytechnical_service",
            "asset_transaction_amount": 2888,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, -i),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": i + 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repayservice = {
            "asset_transaction_type": "repayservice",
            "asset_transaction_amount": 1888,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, -i),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": i + 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        transactions.append(repayprincipal)
        transactions.append(repayinterest)
        transactions.append(repayafter_loan_manage)
        transactions.append(repaytechnical_service)
        transactions.append(repayservice)
    # 第1期单独处理
    if asset_status == 'repay':
        repayprincipal = {
            "asset_transaction_type": "repayprincipal",
            "asset_transaction_amount": 200000,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repayinterest = {
            "asset_transaction_type": "repayinterest",
            "asset_transaction_amount": 3333,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repayafter_loan_manage = {
            "asset_transaction_type": "repayafter_loan_manage",
            "asset_transaction_amount": 10000,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repaytechnical_service = {
            "asset_transaction_type": "repaytechnical_service",
            "asset_transaction_amount": 2888,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repayservice = {
            "asset_transaction_type": "repayservice",
            "asset_transaction_amount": 1888,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        repaylateinterest = {
            "asset_transaction_type": "repaylateinterest",
            "asset_transaction_amount": 6888,
            "asset_transaction_status": "unfinish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": "",
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 0
        }
        transactions.append(repayprincipal)
        transactions.append(repayinterest)
        transactions.append(repayafter_loan_manage)
        transactions.append(repaytechnical_service)
        transactions.append(repayservice)
        transactions.append(repaylateinterest)
    if asset_status == 'payoff':
        finish_at = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        repayprincipal = {
            "asset_transaction_type": "repayprincipal",
            "asset_transaction_amount": 200000,
            "asset_transaction_status": "finish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": finish_at,
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 200000
        }
        repayinterest = {
            "asset_transaction_type": "repayinterest",
            "asset_transaction_amount": 3333,
            "asset_transaction_status": "finish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": finish_at,
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 3333
        }
        repayafter_loan_manage = {
            "asset_transaction_type": "repayafter_loan_manage",
            "asset_transaction_amount": 10000,
            "asset_transaction_status": "finish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": finish_at,
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 10000
        }
        repaytechnical_service = {
            "asset_transaction_type": "repaytechnical_service",
            "asset_transaction_amount": 2888,
            "asset_transaction_status": "finish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": finish_at,
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 2888
        }
        repayservice = {
            "asset_transaction_type": "repayservice",
            "asset_transaction_amount": 1888,
            "asset_transaction_status": "finish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": finish_at,
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 1888
        }
        repaylateinterest = {
            "asset_transaction_type": "repaylateinterest",
            "asset_transaction_amount": 6888,
            "asset_transaction_status": "finish",
            "asset_transaction_expect_finish_time": get_before_date(overdue_days, 0),
            "asset_transaction_finish_at": finish_at,
            "asset_transaction_period": 1,
            "asset_transaction_remark": "",
            "asset_transaction_decrease_amount": 0,
            "asset_transaction_repaid_amount": 6888
        }
        transactions.append(repayprincipal)
        transactions.append(repayinterest)
        transactions.append(repayafter_loan_manage)
        transactions.append(repaytechnical_service)
        transactions.append(repayservice)
        transactions.append(repaylateinterest)
    return json.dumps(transactions, ensure_ascii=False)


def asset_import(overdue_days='1', asset_from_system_name='草莓', asset_repayment_app='', asset_status='repay',
                 item_no="", data_info=''):
    key = str(int(time.time() * 1000))
    asset_info = asset_bean(overdue_days, asset_from_system_name, asset_repayment_app, asset_status, item_no)
    if data_info:
        individual_info = data_info["borrower"]
    else:
        individual_info = json.loads(individual_bean())
    transaction_info = transaction_bean(overdue_days, asset_status)
    data_info = {
        "asset": json.loads(asset_info),
        "borrower": individual_info,
        "repayer": individual_info,
        "receive_card": json.loads(receive_card()),
        "asset_transactions": json.loads(transaction_info)
    }
    import_info = {
        "type": "AssetImport",
        "key": key,
        "from_system": "Rbiz",
        "data": data_info
    }
    asset_import_url = dh_sync_base_url + sync_uri
    print(json.dumps(import_info))
    resp = http.http_post(asset_import_url, import_info)
    print(resp)
    if resp['code'] == 0:
        time.sleep(2)

    item_no = import_info["data"]["asset"]["asset_item_number"]

    fails = 0
    for i in range(120):
        print("当前时间：", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        da_info = get_debtor_asset_by_item_no(item_no)
        if asset_status == "repay" and asset_repayment_app == '':
            if da_info[0]["count"] == 1:
                print('Sync Success!')
                break
            if da_info[0]["count"] == 0:
                time.sleep(1)
                fails += 1
                print('导入尚未成功，等待中，等待时间：', fails)
        if asset_status != "repay" or asset_repayment_app != '':
            da_create_at = da_info[0]["create_at"]
            da_create_at_timestamp = get_timestamp_by_datetime(da_create_at)
            da_update_at = da_info[0]["update_at"]
            da_update_at_timestamp = get_timestamp_by_datetime(da_update_at)
            if da_create_at_timestamp < da_update_at_timestamp:
                print('非新资产(payoff or 导流资产 or 注销 or 作废) Sync Success!')
                break
            else:
                time.sleep(1)
                fails += 1
                print('payoff资产导入尚未成功，等待中，等待时间：', fails)
    if fails == 120 and get_debtor_asset_by_item_no(item_no)[0]["count"] == 0:
        print("导入失败，请检查测试环境是否正常运行！！！")
        return ""
    else:
        return item_no, data_info


def refresh_debtor_arrears(asset_customer, d_enc_id_num, debtor_id):
    # 获取刷新债务概览前，债务创建时间
    before_refresh_debtor_arrears_info = get_debtor_arrears_info(asset_customer, d_enc_id_num)
    before_refresh_create_at = before_refresh_debtor_arrears_info[0]["create_at"]
    before_timestamp = get_timestamp_by_datetime(before_refresh_create_at)
    print("发出债务概览前，债务创建时间：", before_refresh_create_at)
    time.sleep(2)
    # 开始请求刷新概览
    refresh_url = dh_sync_base_url + debtor_refresh_uri + "?debtorId=%s" % debtor_id
    resp = http.http_get(refresh_url)
    fails = 0
    for i in range(120):
        # 获取刷新债务概览后，债务创建时间
        after_refresh_debtor_arrears_info = get_debtor_arrears_info(asset_customer, d_enc_id_num)
        after_refresh_create_at = after_refresh_debtor_arrears_info[0]["create_at"]
        after_timestamp = get_timestamp_by_datetime(after_refresh_create_at)
        print("请求债务概览后，债务创建时间：", after_refresh_create_at)
        if after_timestamp > before_timestamp:
            print('债务概览刷新成功!')
            break
        else:
            time.sleep(1)
            fails += 1
            print('刷新债务概览尚未成功，等待中，等待时间：', fails)
    return resp


def recovery_asset_bean(item_no, asset_status):
    timestamp = long(int(time.time() * 1000))
    late_interest_decrease_amount = 7000
    finish_at = get_date()
    body = {
        "type": "paydayloan",
        "status": asset_status,
        "decreaseAmount": late_interest_decrease_amount,
        "version": timestamp,
        "asset_item_no": item_no,
        "asset_owner": "KN",
        "sub_type": "multiple",
        "period_type": "month",
        "period_count": 3,
        "product_category": "0",
        "cmdb_product_number": "zjf_6_1m_20200228",
        "grant_at": "2020-03-06 13:44:28",
        "effect_at": "2020-03-06 13:44:28",
        "actual_grant_at": "2020-03-06 13:49:07",
        "due_at": "2020-09-06 00:00:00",
        "payoff_at": finish_at,
        "from_system": "dsq",
        "principal_amount": 400000,
        "granted_principal_amount": 400000,
        "loan_channel": "hengfeng",
        "alias_name": item_no,
        "interest_amount": 6684,
        "fee_amount": 17551,
        "balance_amount": 0,
        "repaid_amount": 142100,
        "total_amount": 142100,
        "interest_rate": "0.000",
        "charge_type": 1,
        "ref_order_no": "",
        "ref_order_type": "game_bill",
        "withholding_amount": "",
        "sub_order_type": "",
        "actual_payoff_at": finish_at,
        "ref_item_no": "",
        "product_name": "",
        "order_to_asset": False,
        "late_amount": 3546,
        "repaid_late_amount": 0,
        "repaid_fee_amount": 21776,
        "decrease_fee_amount": 0,
        "decrease_late_amount": 7000,
        "from_app": "草莓"
    }
    return json.dumps(body, ensure_ascii=False)


def recovery_dtransactions_bean(item_no, overdue_days, repay_status=""):
    """
    分3种情况
    1、逾期期次部分还款----overdue_repay_period_part----第1期息费全还、本金部分还款，2、3不还
    2、逾期期次全部还款----overdue_repay_period_payoff----第1期本息费全还，2、3不还
    3、逾期期次+非逾期期次----overdue_repay_all_payoff----1、2、3本息费全部还款
    假设第1期逾期，2、3未逾期
    """
    dtransactions = []
    principal_amount = 132228
    interest_amount = 3333
    finish_at = get_date()
    if repay_status:
        pass
    else:
        repay_status = "overdue_repay_period_payoff"
    repay_principal_1 = {
        "asset_item_no": item_no,
        "type": "repayprincipal",
        "description": "偿还本金",
        "amount": principal_amount,
        "decrease_amount": 0,
        "total_amount": principal_amount,
        "balance_amount": 0,
        "due_at": get_before_date(overdue_days, 0),
        "period": 1,
        "late_status": "late",
        "remark": "",
        "repay_priority": 90,
        "category": "principal"
    }
    if repay_status == "overdue_repay_period_part":
        repay_principal_1_sub = {
            "repaid_amount": 30000,
            "status": "nofinish",
            "finish_at": "1000-01-01 00:00:00",
            "trade_at": finish_at,
        }
    if repay_status == "overdue_repay_period_payoff" or repay_status == "overdue_repay_all_payoff":
        repay_principal_1_sub = {
            "repaid_amount": principal_amount,
            "status": "finish",
            "finish_at": finish_at,
            "trade_at": finish_at,
        }
    repay_principal_1.update(repay_principal_1_sub)
    dtransactions.append(repay_principal_1)

    for i in range(1, 3):
        repay_principal = {
            "asset_item_no": item_no,
            "type": "repayprincipal",
            "description": "偿还本金",
            "amount": principal_amount,
            "decrease_amount": 0,
            "total_amount": principal_amount,
            "balance_amount": 0,
            "due_at": get_before_date(overdue_days, -i),
            "period": i + 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 80,
            "category": "principal",
        }
        if repay_status == "overdue_repay_period_part" or repay_status == "overdue_repay_period_payoff":
            repay_principal_sub = {
                "repaid_amount": 0,
                "status": "nofinish",
                "finish_at": "1000-01-01 00:00:00",
                "trade_at": "1000-01-01 00:00:00"
            }
        if repay_status == "overdue_repay_all_payoff":
            repay_principal_sub = {
                "repaid_amount": principal_amount,
                "status": "finish",
                "finish_at": finish_at,
                "trade_at": finish_at
            }
        repay_principal.update(repay_principal_sub)
        dtransactions.append(repay_principal)

    repay_interest_1 = {
        "asset_item_no": item_no,
        "type": "repayinterest",
        "description": "偿还利息",
        "amount": interest_amount,
        "decrease_amount": 0,
        "repaid_amount": interest_amount,
        "status": "finish",
        "finish_at": finish_at,
        "trade_at": finish_at,
        "total_amount": interest_amount,
        "balance_amount": 0,
        "due_at": get_before_date(overdue_days, 0),
        "period": 1,
        "late_status": "late",
        "remark": "",
        "repay_priority": 80,
        "category": "interest"
    }
    dtransactions.append(repay_interest_1)

    for i in range(1, 3):
        repay_interest = {
            "asset_item_no": item_no,
            "type": "repayinterest",
            "description": "偿还利息",
            "amount": interest_amount,
            "decrease_amount": 0,
            "total_amount": interest_amount,
            "balance_amount": 0,
            "due_at": get_before_date(overdue_days, -i),
            "period": i + 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 80,
            "category": "interest",
        }
        if repay_status == "overdue_repay_period_part" or repay_status == "overdue_repay_period_payoff":
            repay_interest_sub = {
                "repaid_amount": 0,
                "status": "nofinish",
                "finish_at": "1000-01-01 00:00:00",
                "trade_at": "1000-01-01 00:00:00"
            }
        if repay_status == "overdue_repay_all_payoff":
            repay_interest_sub = {
                "repaid_amount": interest_amount,
                "status": "finish",
                "finish_at": finish_at,
                "trade_at": finish_at
            }
        repay_interest.update(repay_interest_sub)
        dtransactions.append(repay_interest)
    return dtransactions


def recovery_fees(item_no, overdue_days, repay_status=""):
    """
    分3种情况
    1、逾期期次部分还款----overdue_repay_period_part----第1期息费全还、本金部分还款，2、3不还
    2、逾期期次全部还款----overdue_repay_period_payoff----第1期本息费全还，2、3不还
    3、逾期期次+非逾期期次----overdue_repay_all_payoff----1、2、3本息费全部还款
    假设第1期逾期，2、3未逾期
    """
    fees = []
    service_amount = 5851
    late_interest_amount = 3456
    late_interest_decrease_amount = 7000
    finish_at = get_date()
    if repay_status:
        pass
    else:
        repay_status = "overdue_repay_period_payoff"

    late_interest_1 = {
        "asset_item_no": item_no,
        "type": "lateinterest",
        "description": "罚息",
        "amount": late_interest_amount,
        "decrease_amount": late_interest_decrease_amount,
        "repaid_amount": late_interest_amount,
        "total_amount": late_interest_amount + late_interest_decrease_amount,
        "balance_amount": 0,
        "status": "finish",
        "due_at": get_before_date(overdue_days, 0),
        "finish_at": finish_at,
        "period": 1,
        "late_status": "late",
        "remark": "",
        "repay_priority": 70,
        "trade_at": finish_at,
        "category": "late"
    }
    service_1 = {
        "asset_item_no": item_no,
        "type": "technical_service",
        "description": "技术服务费",
        "amount": service_amount,
        "decrease_amount": 0,
        "repaid_amount": service_amount,
        "total_amount": service_amount,
        "balance_amount": 0,
        "status": "finish",
        "due_at": get_before_date(overdue_days, 0),
        "finish_at": finish_at,
        "period": 1,
        "late_status": "late",
        "remark": "",
        "repay_priority": 70,
        "trade_at": finish_at,
        "category": "fee"
    }
    fees.append(late_interest_1)
    fees.append(service_1)

    for i in range(1, 3):
        service = {
            "asset_item_no": item_no,
            "type": "technical_service",
            "description": "技术服务费",
            "amount": service_amount,
            "decrease_amount": 0,
            "total_amount": service_amount,
            "balance_amount": 0,
            "due_at": get_before_date(overdue_days, -i),
            "period": i + 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 70,
            "category": "fee",
            "trade_at": finish_at,
        }
        if repay_status == "overdue_repay_period_part" or repay_status == "overdue_repay_period_payoff":
            service_sub = {
                "repaid_amount": 0,
                "status": "nofinish",
                "finish_at": "1000-01-01 00:00:00"
            }
        if repay_status == "overdue_repay_all_payoff":
            service_sub = {
                "repaid_amount": service_amount,
                "status": "finish",
                "finish_at": finish_at
            }
        service.update(service_sub)
        fees.append(service)
    return fees


def recovery_tran_logs(item_no, repay_status="", is_repay_after_today=False):
    """
    分3种情况
    1、逾期期次部分还款----overdue_repay_period_part----第1期息费全还、本金部分还款，2、3不还
    2、逾期期次全部还款----overdue_repay_period_payoff----第1期本息费全还，2、3不还
    3、逾期期次+非逾期期次----overdue_repay_all_payoff----1、2、3本息费全部还款
    假设第1期逾期，2、3未逾期
    """
    tran_logs = []
    principal_amount = 132228
    interest_amount = 3333
    late_interest_amount = 3456
    service_amount = 5851
    if is_repay_after_today is True:
        finish_at = get_date_after_today(day=1)
    if is_repay_after_today is False:
        finish_at = get_date()

    if repay_status:
        pass
    else:
        repay_status = "overdue_repay_period_payoff"

    late_interest_logs = {
        "id": 10001,
        "asset_item_no": item_no,
        "asset_tran_no": "157280220",
        "operate_type": "withhold_repay",
        "amount": -late_interest_amount,
        "operate_flag": "normal",
        "comment": "代扣还款",
        "from_system": "rbiz",
        "ref_no": "39898462",
        "operator_id": 0,
        "operator_name": "",
        "create_at": finish_at,
        "update_at": finish_at,
        "withhold_finish_at": finish_at,
        "tran_type": "lateinterest",
        "period": 1
    }
    service_logs_1 = {
        "id": 10002,
        "asset_item_no": item_no,
        "asset_tran_no": "83528298",
        "operate_type": "withhold_repay",
        "amount": -service_amount,
        "operate_flag": "normal",
        "comment": "代扣还款",
        "from_system": "rbiz",
        "ref_no": "39898463",
        "operator_id": 0,
        "operator_name": "",
        "create_at": finish_at,
        "update_at": finish_at,
        "withhold_finish_at": finish_at,
        "tran_type": "technical_service",
        "period": 1
    }
    repay_interest_logs_1 = {
        "id": 10003,
        "asset_item_no": item_no,
        "asset_tran_no": "83528295",
        "operate_type": "withhold_repay",
        "amount": -interest_amount,
        "operate_flag": "normal",
        "comment": "代扣还款",
        "from_system": "rbiz",
        "ref_no": "39898464",
        "operator_id": 0,
        "operator_name": "",
        "create_at": finish_at,
        "update_at": finish_at,
        "withhold_finish_at": finish_at,
        "tran_type": "repayinterest",
        "period": 1
    }
    tran_logs.append(late_interest_logs)
    tran_logs.append(service_logs_1)
    tran_logs.append(repay_interest_logs_1)

    if repay_status == "overdue_repay_period_part":
        repay_principal_logs = {
            "id": 10004,
            "asset_item_no": item_no,
            "asset_tran_no": "83528292",
            "operate_type": "withhold_repay",
            "amount": -30000,
            "operate_flag": "normal",
            "comment": "代扣还款",
            "from_system": "rbiz",
            "ref_no": "39898465",
            "operator_id": 0,
            "operator_name": "",
            "create_at": finish_at,
            "update_at": finish_at,
            "withhold_finish_at": finish_at,
            "tran_type": "repayprincipal",
            "period": 1
        }
        tran_logs.append(repay_principal_logs)

    if repay_status == "overdue_repay_period_payoff":
        repay_principal_logs = {
            "id": 10004,
            "asset_item_no": item_no,
            "asset_tran_no": "83528292",
            "operate_type": "withhold_repay",
            "amount": -principal_amount,
            "operate_flag": "normal",
            "comment": "代扣还款",
            "from_system": "rbiz",
            "ref_no": "39898465",
            "operator_id": 0,
            "operator_name": "",
            "create_at": finish_at,
            "update_at": finish_at,
            "withhold_finish_at": finish_at,
            "tran_type": "repayprincipal",
            "period": 1
        }
        tran_logs.append(repay_principal_logs)
    if repay_status == "overdue_repay_all_payoff":
        for i in range(1, 4):
            repay_principal_logs = {
                "id": 100000 + i,
                "asset_item_no": item_no,
                "asset_tran_no": "83528292",
                "operate_type": "withhold_repay",
                "amount": -principal_amount,
                "operate_flag": "normal",
                "comment": "代扣还款",
                "from_system": "rbiz",
                "ref_no": "39898465",
                "operator_id": 0,
                "operator_name": "",
                "create_at": finish_at,
                "update_at": finish_at,
                "withhold_finish_at": finish_at,
                "tran_type": "repayprincipal",
                "period": i
            }
            tran_logs.append(repay_principal_logs)
        for i in range(2, 4):
            service_logs = {
                "id": 20000 + i,
                "asset_item_no": item_no,
                "asset_tran_no": "83528298",
                "operate_type": "withhold_repay",
                "amount": -service_amount,
                "operate_flag": "normal",
                "comment": "代扣还款",
                "from_system": "rbiz",
                "ref_no": "39898463",
                "operator_id": 0,
                "operator_name": "",
                "create_at": finish_at,
                "update_at": finish_at,
                "withhold_finish_at": finish_at,
                "tran_type": "technical_service",
                "period": i
            }
            repay_interest_logs = {
                "id": 30000 + i,
                "asset_item_no": item_no,
                "asset_tran_no": "83528295",
                "operate_type": "withhold_repay",
                "amount": -interest_amount,
                "operate_flag": "normal",
                "comment": "代扣还款",
                "from_system": "rbiz",
                "ref_no": "39898464",
                "operator_id": 0,
                "operator_name": "",
                "create_at": finish_at,
                "update_at": finish_at,
                "withhold_finish_at": finish_at,
                "tran_type": "repayinterest",
                "period": i
            }
            tran_logs.append(service_logs)
            tran_logs.append(repay_interest_logs)
    return tran_logs


def inverse_dtransactions(item_no, overdue_days):
    """
    还款逆操作
    """
    dtransactions = []
    principal_amount = 132228
    interest_amount = 3333

    repay_principal_1 = {
        "asset_item_no": item_no,
        "type": "repayprincipal",
        "description": "偿还本金",
        "amount": principal_amount,
        "decrease_amount": 0,
        "total_amount": principal_amount,
        "balance_amount": 0,
        "due_at": get_before_date(overdue_days, 0),
        "period": 1,
        "late_status": "late",
        "remark": "",
        "repay_priority": 90,
        "category": "principal",
        "repaid_amount": 0,
        "status": "nofinish",
        "finish_at": "1000-01-01 00:00:00",
        "trade_at": "1000-01-01 00:00:00"
    }
    dtransactions.append(repay_principal_1)

    repay_interest_1 = {
        "asset_item_no": item_no,
        "type": "repayinterest",
        "description": "偿还利息",
        "amount": interest_amount,
        "decrease_amount": 0,
        "repaid_amount": 0,
        "status": "nofinish",
        "finish_at": "1000-01-01 00:00:00",
        "trade_at": "1000-01-01 00:00:00",
        "total_amount": interest_amount,
        "balance_amount": 0,
        "due_at": get_before_date(overdue_days, 0),
        "period": 1,
        "late_status": "late",
        "remark": "",
        "repay_priority": 80,
        "category": "interest"
    }
    dtransactions.append(repay_interest_1)

    for i in range(1, 3):
        repay_interest = {
            "asset_item_no": item_no,
            "type": "repayinterest",
            "description": "偿还利息",
            "amount": interest_amount,
            "decrease_amount": 0,
            "total_amount": interest_amount,
            "balance_amount": 0,
            "status": "nofinish",
            "due_at": get_before_date(overdue_days, -i),
            "period": i + 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 80,
            "category": "interest",
            "repaid_amount": 0,
            "finish_at": "1000-01-01 00:00:00",
            "trade_at": "1000-01-01 00:00:00"
        }
        dtransactions.append(repay_interest)
    return dtransactions


def inverse_fees(item_no, overdue_days):
    """
    还款逆操作
    """
    fees = []
    service_amount = 5851
    lateinterest_amount = 3456
    lateinterest_decrease_amount = 7000

    lateinterest_1 = {
        "asset_item_no": item_no,
        "type": "lateinterest",
        "description": "罚息",
        "amount": lateinterest_amount,
        "decrease_amount": lateinterest_decrease_amount,
        "repaid_amount": 0,
        "total_amount": lateinterest_amount + lateinterest_decrease_amount,
        "balance_amount": 0,
        "status": "nofinish",
        "due_at": get_before_date(overdue_days, 0),
        "finish_at": "1000-01-01 00:00:00",
        "period": 1,
        "late_status": "late",
        "remark": "",
        "repay_priority": 70,
        "trade_at": "1000-01-01 00:00:00",
        "category": "late"
    }
    service_1 = {
        "asset_item_no": item_no,
        "type": "technical_service",
        "description": "技术服务费",
        "amount": service_amount,
        "decrease_amount": 0,
        "repaid_amount": 0,
        "total_amount": service_amount,
        "balance_amount": 0,
        "status": "nofinish",
        "due_at": get_before_date(overdue_days, 0),
        "finish_at": "1000-01-01 00:00:00",
        "period": 1,
        "late_status": "late",
        "remark": "",
        "repay_priority": 70,
        "trade_at": "1000-01-01 00:00:00",
        "category": "fee"
    }
    fees.append(lateinterest_1)
    fees.append(service_1)

    for i in range(1, 3):
        service = {
            "asset_item_no": item_no,
            "type": "technical_service",
            "description": "技术服务费",
            "amount": service_amount,
            "decrease_amount": 0,
            "total_amount": service_amount,
            "balance_amount": 0,
            "due_at": get_before_date(overdue_days, -i),
            "period": i + 1,
            "late_status": "normal",
            "remark": "",
            "repay_priority": 70,
            "category": "fee",
            "trade_at": "1000-01-01 00:00:00",
            "repaid_amount": 0,
            "status": "nofinish",
            "finish_at": "1000-01-01 00:00:00"
        }
        fees.append(service)
    return fees


def inverse_tran_logs(item_no, is_repay_after_today=False):
    """
    还款逆操作
    """
    tran_logs = []
    principal_amount = 132228
    interest_amount = 3333
    late_interest_amount = 3456
    service_amount = 5851
    if is_repay_after_today is True:
        inverse_at = get_date_after_today(day=1)
    if is_repay_after_today is False:
        inverse_at = get_date()

    repay_principal_logs = {
        "id": 40001,
        "asset_item_no": item_no,
        "asset_tran_no": "176658810",
        "operate_type": "repay_inverse",
        "amount": principal_amount,
        "operate_flag": "normal",
        "comment": "还款逆操作",
        "from_system": "rbiz",
        "ref_no": "672576445",
        "operator_id": 0,
        "operator_name": "",
        "create_at": inverse_at,
        "update_at": inverse_at,
        "withhold_finish_at": inverse_at,
        "tran_type": "repayprincipal",
        "period": 1
    }
    repay_interest_logs = {
        "id": 40002,
        "asset_item_no": item_no,
        "asset_tran_no": "83528295",
        "operate_type": "repay_inverse",
        "amount": interest_amount,
        "operate_flag": "normal",
        "comment": "还款逆操作",
        "from_system": "rbiz",
        "ref_no": "39898464",
        "operator_id": 0,
        "operator_name": "",
        "create_at": inverse_at,
        "update_at": inverse_at,
        "withhold_finish_at": inverse_at,
        "tran_type": "repayinterest",
        "period": 1
    }
    service_logs = {
        "id": 40003,
        "asset_item_no": item_no,
        "asset_tran_no": "83528298",
        "operate_type": "repay_inverse",
        "amount": service_amount,
        "operate_flag": "normal",
        "comment": "还款逆操作",
        "from_system": "rbiz",
        "ref_no": "39898463",
        "operator_id": 0,
        "operator_name": "",
        "create_at": inverse_at,
        "update_at": inverse_at,
        "withhold_finish_at": inverse_at,
        "tran_type": "technical_service",
        "period": 1
    }
    late_interest_logs = {
        "id": 40004,
        "asset_item_no": item_no,
        "asset_tran_no": "157280220",
        "operate_type": "repay_inverse",
        "amount": late_interest_amount,
        "operate_flag": "normal",
        "comment": "还款逆操作",
        "from_system": "rbiz",
        "ref_no": "39898462",
        "operator_id": 0,
        "operator_name": "",
        "create_at": inverse_at,
        "update_at": inverse_at,
        "withhold_finish_at": inverse_at,
        "tran_type": "lateinterest",
        "period": 1
    }
    tran_logs.append(repay_principal_logs)
    tran_logs.append(repay_interest_logs)
    tran_logs.append(service_logs)
    tran_logs.append(late_interest_logs)
    return tran_logs


def biz_recovery(overdue_days, item_no, asset_status, repay_status="", is_inverse=False, is_repay_after_today=False):
    if repay_status:
        pass
    else:
        repay_status = "overdue_repay_period_payoff"
    if is_inverse is False:
        key = str(int(time.time() * 1000))
        asset_info = recovery_asset_bean(item_no, asset_status)
        dtransactions_info = recovery_dtransactions_bean(item_no, overdue_days, repay_status)
        fees_info = recovery_fees(item_no, overdue_days, repay_status)
        tran_logs_info = recovery_tran_logs(item_no, repay_status, is_repay_after_today)
        data_info = {
            "action": "tran_repay",
            "type": "assetAccountSync",
            "asset": json.loads(asset_info),
            "dtransactions": dtransactions_info,
            "fees": fees_info,
            "tran_logs": tran_logs_info
        }
        recovery_info = {
            "type": "AssetChangeNotify",
            "key": "AssetChangeFR_" + key,
            "from_system": "BIZ",
            "data": data_info
        }
    if is_inverse is True:
        key = str(int(time.time() * 1000))
        asset_info = recovery_asset_bean(item_no, asset_status)
        dtransactions_info = inverse_dtransactions(item_no, overdue_days)
        fees_info = inverse_fees(item_no, overdue_days)
        tran_logs_info = inverse_tran_logs(item_no, is_repay_after_today)
        data_info = {
            "action": "repay_inverse",
            "type": "assetAccountSync",
            "asset": json.loads(asset_info),
            "dtransactions": dtransactions_info,
            "fees": fees_info,
            "tran_logs": tran_logs_info
        }
        recovery_info = {
            "type": "AssetChangeNotify",
            "key": "AssetChangeFR_" + key,
            "from_system": "BIZ",
            "data": data_info
        }
    asset_recovery_url = dh_sync_base_url + recovery_uri
    http.http_post(asset_recovery_url, recovery_info)
    repay_date = tran_logs_info[0]["withhold_finish_at"]

    fails = 0
    for i in range(120):
        summary_recovery_info = get_summary_recovery(item_no)
        if summary_recovery_info[0]["count"] > 0:
            print('Recovery Success!')
            break
        else:
            time.sleep(1)
            fails += 1
            print('回款尚未成功，等待中，等待时间：', fails)
    # 回款改为入账明细后，可能出现所有的明细不能同时入库，等2秒
    time.sleep(2)
    return repay_date


def sync_tool_package(app_name, tool_app_name, channel, system, status):
    req_data = [{
        "app_name": app_name,
        "tool_app_name": tool_app_name,
        "channel": channel,
        "os": system,
        "status": status
    }]
    sync_tool_url = dh_sync_base_url + tool_package_uri
    resp = http.http_post(sync_tool_url, req_data)
    if resp['code'] == "200":
        time.sleep(2)
    return resp
