"""
海外dcs的主要接口
"""
from biztest.function.global_dcs.dcs_global_db import dcs_run_job_by_jobtype
from biztest.util.tools.tools import get_guid, get_date

dcs_asset_payment_success_url = "/paydayloan/withdraw/notify"
dcs_asset_withdraw_success_url = "/paydayloan/grant/notify"
dcs_capital_asset_url = "/paydayloan/capital/asset/notify"
dcs_refund_result_url = "/paydayloan/refund/notify"
dcs_capital_asset_success_url = ""
asset_withdraw = {
    "from_system": "MQ",
    "key": get_guid(),
    "type": "PaymentWithdrawSuccess",
    "data": {
        "merchant_id": None,
        "merchant_key": "",
        "account": "autotest_channel",  # 先写死
        "amount": 500000,
        "reason": "代付500000分",
        "receiver_type": 1,
        "receiver_name_encrypt": "",
        "receiver_account_encrypt": "6213944797824967",
        "receiver_identity_encrypt": "2102111978100537040",
        "receiver_bank_code": None,
        "receiver_bank_branch": None,
        "receiver_bank_subbranch": None,
        "receiver_bank_province": None,
        "receiver_bank_city": None,
        "channel": "autotest_channel",
        "status": "success",
        "type": "withdraw",
        "comment": "Transfer completed successfully",
        "create_at": get_date(),
        "update_at": get_date(),
        "request_data": None,
        "response_data": None,
        "finish_at": get_date(),
        "version": None,
        "channel_key": get_guid(),
        "order_no": ""
    }
}


def run_dbTaskJob_api(priority=1, limit=2):
    job_type = "dbTaskJob"
    job_params = {"priority": priority, "delayMinute": 0, "limit": limit, "withInHour": 24}
    dcs_run_job_by_jobtype(job_type, job_params)


def run_UpAccountingTranJob_by_api():
    job_type = "UpAccountingTranJob"
    job_params = {}
    dcs_run_job_by_jobtype(job_type, job_params)


def run_OfflineFeeStatisticsJob_by_api():
    job_type = "OfflineFeeStatisticsJob"
    job_params = {}
    dcs_run_job_by_jobtype(job_type, job_params)


def run_dcs_RepayToFinalJob_by_api(item_no=None):
    job_type = "biz_dcs_RepayToFinalJob"
    job_params = {"processDate": "2021-09-17"}
    dcs_run_job_by_jobtype(job_type, job_params)


def run_dcs_TransferProvisionJob_by_api(start_date=None, end_date=None):
    job_type = "biz_dcs_TransferProvisionJob"
    if start_date is None:
        start_date = get_date(day=-1)
    if end_date is None:
        end_date = get_date()
    job_params = {
        "startDate": start_date,
        "endDate": end_date
    }
    dcs_run_job_by_jobtype(job_type, job_params)


if __name__ == "__main__":
    run_UpAccountingTranJob_by_api()
