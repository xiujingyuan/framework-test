from urllib.parse import urlencode

from biztest.config.dcs.url_config import dcs_base_url
from biztest.config.dcs.xxljob_config import global_compensate_params, global_finalToTran_params, global_repay_params, \
    global_repay_settle_params, global_compensate_settle_params
from biztest.function.global_dcs.dcs_global_db import dcs_run_task_by_order_no, update_dcs_global_task_open, \
    update_dcs_global_task_next_run_at, update_clearing_tran_create_at, get_dcs_asset_tran_due_at
from biztest.interface.gbiz_global.gbiz_global_interface import http, get_date_before_today, get_date, time


class DcsRunXxlJob:

    def __init__(self, item_no, channel):
        """
        :param item_no: 本次流程的资产编号
        :param channel: 本次流程的资金方
        :param job_type: 本次流程的类型 代偿或还款
        """
        self.item_no = item_no
        self.channel = channel
        self.header = {"Content-Type": "application/json"}

    def run_job_get(self, job_handle, param):
        get_params = {
            "jobType": job_handle,
            "param": param
        }
        print("get_params", get_params)
        get_url = dcs_base_url + "/job/run?" + urlencode(get_params)
        ret = http.http_get(get_url, self.header)
        return ret
        # xxl_job = XxlJob(gc.GLOBAL_JOB_GROUP_MAPPING_ENV["dcs_tha"],
        #                  job_handle,
        #                  password="123456", xxl_job_type='global_taiguo_xxl_job')
        # xxl_job.trigger_job(param)

    # 通过接口执行dcs的job
    def run_clearing_jobs_post(self, handle_task, job_type="repay", serial_no="", channel="tha_picocapital_plus"):
        """
        :param handle_task: job名字
        :param job_type: job类型
        :return: 没有返回值
        """
        # 海外job清分-第一步落final，生成任务 splitRepayToFinal、repayToFinalProcess、repayFinalToClearingProcess/CompensateFinalToClearingProcess
        if handle_task == "biz_dcs_RepayToFinalJob":
            global_repay_params["processDate"] = get_date()[:10]
            global_repay_params["assetItemNo"] = self.item_no
            self.run_job_get(handle_task, global_repay_params)
            # job执行后执行task
            dcs_run = DcsRunXxlJob(self.item_no, "noloan")
            for i in range(4):
                dcs_run.run_clearing_jobs_post("dbTaskJob")
            time.sleep(2)

        # # 还款/代偿 清分finalToTran，生成任务 splitFinalToClearing、CompensateFinalToClearingProcess
        # if handle_task == "biz_dcs_FinalToClearingTranJob": #该JOB已废弃
        #     global_finalToTran_params["bizType"] = job_type
        #     self.run_job_get(handle_task, global_finalToTran_params)
        #     # job执行后执行task
        #     dcs_run = DcsRunXxlJob(self.item_no, "noloan")
        #     for i in range(2):
        #         dcs_run.run_clearing_jobs_post("dbTaskJob")
        #     time.sleep(2)

        # 结算【默认处理今日创建的状态为new的】，
        # 生成任务splitAutoSettlement、lockClearingTrans、newSettlement、settlementAccountTransfer、newAccountTransfer、applyAccountTransfer、settlementCallbackOfTransfer
        if handle_task == "biz_dcs_AutoSettlementJob":
            update_clearing_tran_create_at(self.item_no)
            time.sleep(2)
            global_repay_settle_params["assetItemNo"] = self.item_no
            self.run_job_get(handle_task, global_repay_settle_params)
            # job执行后执行task
            dcs_run = DcsRunXxlJob(self.item_no, "noloan")
            for i in range(10):
                dcs_run.run_clearing_jobs_post("dbTaskJob")
            time.sleep(2)

        # 代偿splitCompensateToFinal、postponeCompensateProcess（按照资金方生成有多个）、compensateToFinalProcess
        if handle_task == "biz_dcs_CompensateCleanFinalJob":
            asset_tran_info = get_dcs_asset_tran_due_at(self.item_no)
            global_compensate_params["dueDate"] = asset_tran_info[0]['due_at']
            global_compensate_params["assetItemNo"] = self.item_no
            self.run_job_get(handle_task, global_compensate_params)
            # job执行后执行task
            dcs_run = DcsRunXxlJob(self.item_no, "noloan")
            for i in range(5):
                dcs_run.run_clearing_jobs_post("dbTaskJob")
            time.sleep(2)

        if handle_task == "biz_dcs_CompensateSettlementJob":
            # 代偿结算task ==》splitCompensateSettlement、compensateSettlement
            update_clearing_tran_create_at(self.item_no)
            time.sleep(3)
            global_compensate_settle_params["assetItemNo"] = self.item_no
            global_compensate_settle_params["channel"] = self.channel
            global_compensate_settle_params["startDate"] = get_date()[:10]
            global_compensate_settle_params["endDate"] = get_date()[:10]
            global_compensate_settle_params["leastAmount"] = 0  # KV#dcs_loan_config中所有出户的余额必须大于JOB传入的leastAmount金额才会创建代偿
            self.run_job_get(handle_task, global_compensate_settle_params)
            # job执行后执行task
            dcs_run = DcsRunXxlJob(self.item_no, "noloan")
            for i in range(10):
                dcs_run.run_clearing_jobs_post("dbTaskJob")
            time.sleep(2)

        if handle_task == "biz_dcs_SplitWithholdJob":
            dcs_run = DcsRunXxlJob(self.item_no, "noloan")
            for i in range(5):
                dcs_run.run_clearing_jobs_post("dbTaskJob")
            global_repay_params["processDate"] = get_date()[:10]
            global_repay_params["assetItemNo"] = self.item_no
            self.run_job_get(handle_task, global_repay_params)
            # job执行后执行task
            for i in range(5):
                dcs_run.run_clearing_jobs_post("dbTaskJob")

        if handle_task == "biz_dcs_CollectingJob":
            dcs_run = DcsRunXxlJob(self.item_no, "noloan")
            for i in range(5):
                dcs_run.run_clearing_jobs_post("dbTaskJob")
            global_repay_params["processDate"] = get_date()[:10]
            global_repay_params["assetItemNo"] = self.item_no
            self.run_job_get(handle_task, global_repay_params)
            # job执行后执行task
            for i in range(5):
                dcs_run.run_clearing_jobs_post("dbTaskJob")
            time.sleep(1)

        if handle_task == "biz_dcs_WithholdCostJob":
            dcs_run = DcsRunXxlJob(self.item_no, "noloan")
            update_dcs_global_task_next_run_at(1)
            for i in range(5):
                dcs_run.run_clearing_jobs_post("dbTaskJob")
            global_withhold_cost_params["startDate"] = get_date()[:10]
            global_withhold_cost_params["endDate"] = get_date()[:10]
            global_withhold_cost_params["limit"] = 1000
            global_withhold_cost_params["serialNoList"][0] = serial_no
            self.run_job_get(handle_task, global_withhold_cost_params)
            for i in range(5):
                dcs_run.run_clearing_jobs_post("dbTaskJob")

        if handle_task == "dbTaskJob":
            update_dcs_global_task_next_run_at(1)
            global_repay_params["withInHour"] = 5
            global_repay_params["delayMinute"] = 0
            global_repay_params["priority"] = 1
            global_repay_params["limit"] = 1000
            self.run_job_get(handle_task, global_repay_params)
            time.sleep(1)
