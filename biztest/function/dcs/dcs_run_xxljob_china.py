from urllib.parse import urlencode

from biztest.config.dcs.url_config import dcs_base_url
from biztest.config.dcs.xxljob_config import global_compensate_params, global_finalToTran_params, global_repay_params, \
    global_repay_settle_params, clearing_handle_params_new, dbtaskjob_params_new, retry_collect_params, \
    auto_collect_params, auto_settlement_params, auto_buyback_params
from biztest.function.dcs.capital_database import update_dcs_china_task_next_run_at
from biztest.function.global_dcs.dcs_global_db import dcs_run_task_by_order_no, update_dcs_global_task_open, \
    update_dcs_global_task_next_run_at, update_clearing_tran_create_at, get_dcs_asset_tran_due_at
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count
from biztest.interface.gbiz_global.gbiz_global_interface import http, get_date_before_today, get_date, time, \
    get_date_after


class DcsRunXxlJobChina:

    def __init__(self, item_no=None, channel=None, retry_id=None):
        """
        :param item_no: 本次流程的资产编号
        :param channel: 本次流程的资金方
        :param job_type: 本次流程的类型 代偿或还款
        """
        self.item_no = item_no
        self.channel = channel
        self.retry_id = retry_id
        self.header = {"Content-Type": "application/json"}

    def run_job_post(self, job_handle, body):
        """
        海外项目代扣
           :param
           :return: json
               example:
        """
        request_body = {
            "jobType": job_handle,
            "param": body
        }
        get_url = dcs_base_url + "/job/run"
        http.http_post(get_url, request_body, self.header)
        return request_body

    # 通过接口执行dcs的job
    def run_clearing_jobs_post(self, handle_task, loanType="BIG"):
        """
        :param handle_task: job名字
        :param job_type: job类型
        :return: 没有返回值
        """
        # 代偿job->生成任务splitCapitalCompensateToPending、singleCapitalCompensateToPending、capitalCompensateToPendingProcess、capitalCompensateToFinalProcess
        # 、loadCompensateConfig、clearingTransProcess
        if handle_task == "biz_dcs_CapitalCompensateToPendingJob":
            clearing_handle_params_new["jobType"] = "biz_dcs_CapitalCompensateToPendingJob"
            clearing_handle_params_new["processDate"] = get_date_before_today()[:10]
            clearing_handle_params_new["includeAssetItemNos"][0] = self.item_no
            clearing_handle_params_new["includeLoanChannels"][0] = self.channel
            self.run_job_post(handle_task, clearing_handle_params_new)
            # job执行后执行task
            job_run = DcsRunXxlJobChina(self.item_no, "")
            for i in range(10):
                time.sleep(1)
                job_run.run_clearing_jobs_post("dbTaskJob")

        if handle_task == "dbTaskJob":
            update_dcs_china_task_next_run_at(2)
            self.run_job_post(handle_task, dbtaskjob_params_new)

        # dcs-job#资金归集入口biz_dcs_CollectD1Job该job为D1资金归集入口（默认归集大于等于昨天小于今天代扣成功的数据）
        if handle_task == "biz_dcs_CollectD1Job":
            auto_collect_params["jobType"] = "biz_dcs_CollectD1Job"
            auto_collect_params["startDate"] = get_date_before_today()[:10] # 获取今天
            auto_collect_params["endDate"] = get_date_after(get_date_before_today()[:10], day=1)  # 获取明天
            self.run_job_post(handle_task, auto_collect_params)
            # job执行后执行task
            job_run = DcsRunXxlJobChina(self.item_no, "")
            for i in range(2):
                time.sleep(1)
                job_run.run_clearing_jobs_post("dbTaskJob")

        # 回购JOB#biz_dcs_BuybackToPendingJob===>生成task-capitalBuybackFlow执行后生成asyncChainExecutable(task_order_no=资产编号)
        if handle_task == "biz_dcs_BuybackToPendingJob":
            auto_buyback_params["jobType"] = "biz_dcs_BuybackToPendingJob"
            auto_buyback_params["processDate"] = get_date_before_today()[:10]   # 获取今天
            auto_buyback_params["includeAssetItemNos"][0] = self.item_no
            auto_buyback_params["includeLoanChannels"][0] = self.channel
            self.run_job_post(handle_task, auto_buyback_params)
            # job执行后执行task
            job_run = DcsRunXxlJobChina(self.item_no, "")
            for i in range(4):
                time.sleep(1)
                job_run.run_clearing_jobs_post("dbTaskJob")

        # dcs-job#资金归集失败重新归集入口biz_dcs_CollectFailRetryJob(只有自动归集支持重试)
        if handle_task == "biz_dcs_CollectFailRetryJob":
            retry_collect_params["jobType"] = "biz_dcs_CollectFailRetryJob"
            retry_collect_params["orderId"] = self.retry_id
            self.run_job_post(handle_task, retry_collect_params)
            # job执行后执行task
            job_run = DcsRunXxlJobChina(self.item_no, "")
            for i in range(10):
                time.sleep(1)
                job_run.run_clearing_jobs_post("dbTaskJob")

        # dcs-job# 大小单自动结算入口：
        # 1.先查询需要结算的数据，按照transfer_out和transfer_in进行分组
        # 2.创建task#newSettlement、genericDealTransactionNew、genericDealTransactionApply请求存管进行结算
        if handle_task == "biz_dcs_AutoSettlementJob":
            auto_settlement_params["jobType"] = "biz_dcs_AutoSettlementJob"
            auto_settlement_params["loanType"] = loanType   # BIG、PRECHARGE
            # auto_settlement_params["includeTransferIns"][0] = self.transfer_in
            self.run_job_post(handle_task, auto_settlement_params)
            # job执行后执行task
            job_run = DcsRunXxlJobChina(self.item_no, "")
            for i in range(10):
                time.sleep(1)
                job_run.run_clearing_jobs_post("dbTaskJob")

        # # dcs-job# 小单自动结算入口：
        # # 1.先查询需要结算的数据，按照transfer_out和transfer_in进行分组
        # # 2.创建task#newSettlement、genericDealTransactionNew、genericDealTransactionApply请求存管进行结算
        # if handle_task == "biz_dcs_AutoSettlementJob_noloan":
        #     auto_settlement_params["jobType"] = "biz_dcs_AutoSettlementJob"
        #     auto_settlement_params["loanType"] = "PRECHARGE"
        #     # auto_settlement_params["includeTransferIns"][0] = self.transfer_in
        #     self.run_job_post(handle_task, auto_settlement_params)
        #     # job执行后执行task
        #     job_run = DcsRunXxlJobChina(self.item_no, "")
        #     for i in range(10):
        #         time.sleep(1)
        #         job_run.run_clearing_jobs_post("dbTaskJob")
