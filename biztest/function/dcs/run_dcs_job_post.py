import time, requests
from urllib.parse import urlencode
from biztest.config.dcs.url_config import run_job_url, run_task_url
from biztest.config.dcs.xxljob_config import clearing_handle_params, buyback_clearing_params, \
    advance_clearing_params, auto_settlement_handle_params
from biztest.function.dcs.capital_database import get_task_dcs, update_task_at_dcs, get_task_dcs_close, \
    get_task_dcs_by_order_no_and_type
from biztest.function.dcs.dcs_common import get_is_holiday, wait_dcs_record_appear, run_dcs_task_until_disappear, \
    run_dcs_task_by_type_until_disappear
from biztest.interface.dcs.biz_dcs_interface import run_dcs_task_by_count, deposit_run_task_by_order_no, \
    update_deposit_orderandtrade_and_run_task
from biztest.util.tools.tools import parse_resp_body, get_date_before_today, get_date_before


class RunDcsJobPost:

    def __init__(self, item_no, channel, type, loan_type="PRECHARGE"):
        '''
        :param item_no: 本次流程的资产编号
        :param channel: 本次流程的资金方
        :param type: 本次流程的清分类型，还款或者代偿
        :param loan_type: 结算类型，大单 BIG，PRECHARGE
        '''
        self.item_no = item_no
        self.channel = channel
        self.type = type
        self.loan_type = loan_type

    def run_job_get(self, jobType, param):
        get_params = {
            "jobType": jobType,
            "param": param
        }
        print("get_params", get_params)
        get_url = run_job_url + urlencode(get_params)
        req = parse_resp_body(
            requests.request(
                method='get',
                url=get_url,
                headers={'Content-Type': 'application/json'}
            )
        )
        print("get_url", get_url)
        print("req", req)

    # 通过接口执行dcs的job-还款
    def run_clearing_jobs_post(self, handle_task, repay_period):
        '''
        :param handle_task: job以及job生成的task组成的字典
        :param repay_period: 是一个存有全部期次的元祖，元祖的元素可能只有一个，可能有多个
        :param is_one_repay: 是否一期一期的还，目前只有华北小贷在使用这个字段
        :return: 没有返回值
        '''
        # time.sleep(60)  # 可能存在消息延迟，此时等待一会儿，暂时补救一下，实际上并没有从根本上解决问题
        open_task = "select * from clean_task where task_order_no='%s' and task_type='accountChangeNotifySync' and " \
                    "task_status='open'" % self.item_no
        wait_dcs_record_appear(open_task)
        run_dcs_task_until_disappear(self.item_no)
        # for task_i in range(0, 3):
        #     for i in range(0, 50):
        #         task_count_status = self.check_task_count_status(handle_task["task"][task_i])
        #         print(task_count_status)
        #         if task_count_status["task_count"] >= 1:
        #             if task_count_status["task_status"] == "open":  # task还没有被执行完
        #                 # update_task_at_dcs(handle_task["task"][task_i])
        #                 run_dcs_task_by_count(self.item_no)
        #             else:
        #                 break
        # run_dcs_task_by_order_no(self.item_no)
        # for task_ii in range(3, len(handle_task["task"])):
        #     for i in range(0, 50):
        #         task_count_status = self.check_task_count_status(handle_task["task"][task_ii])
        #         print(task_count_status)
        #         if task_count_status["task_count"] >= len(repay_period):
        #             if task_count_status["task_status"] == "open":  # task还没有被执行完
        #                 # update_task_at_dcs(handle_task["task"][task_ii])
        #                 run_dcs_task_by_count(self.item_no)
        #             else:
        #                 break

    # 通过接口执行dcs的job-代偿
    def run_clearing_jobs_post_compensate(self, handle_task, repay_period, is_one_repay='N'):
        '''
        :param handle_task: job以及job生成的task组成的字典
        :param repay_period: 是一个存有全部期次的元祖，元祖的元素可能只有一个，可能有多个
        :param is_one_repay: 是否一期一期的还，目前只有华北小贷在使用这个字段
        :return: 没有返回值
        '''
        # 修改代偿job的参数，并执行job
        if handle_task["handle"] == "biz_dcs_CapitalCompensateToPendingJob":
            clearing_handle_params["processDate"] = get_date_before_today()[:10]
            clearing_handle_params["includeAssetItemNos"] = [self.item_no]
            clearing_handle_params["includeLoanChannels"] = [self.channel]
            self.run_job_get(handle_task["handle"], clearing_handle_params)
        # 修改小单代偿job的参数，并执行job
        if handle_task["handle"] == "biz_dcs_precharg_compensate_clearing_job":
            clearing_handle_params["processDate"] = get_date_before_today()[:10]
            clearing_handle_params["includeAssetItemNos"] = [self.item_no]
            clearing_handle_params["includeLoanChannels"] = [self.channel]
            self.run_job_get(handle_task["handle"], clearing_handle_params)
        # 修改回购job的参数，并执行job
        if handle_task["handle"] == "biz_dcs_BuybackToPendingJob":
            clearing_handle_params["processDate"] = get_date_before_today()[:10]
            # clearing_handle_params["processDate"] = "2020-07-08"
            clearing_handle_params["includeAssetItemNos"] = [self.item_no]
            clearing_handle_params["includeLoanChannels"] = [self.channel]
            self.run_job_get(handle_task["handle"], clearing_handle_params)

        # 修改权益过期作废job的参数，并执行job
        if handle_task["handle"] == "biz_dcs_not_received_clearing_fix_job":
            clearing_handle_params["processDate"] = get_date_before_today()[:10]
            clearing_handle_params["includeAssetItemNos"] = [self.item_no]
            clearing_handle_params["includeLoanChannels"] = [self.channel]
            self.run_job_get(handle_task["handle"], clearing_handle_params)

        for i in range(0, 50):
            task_count_status = self.check_task_count_status(handle_task["task"][0], "")
            print(task_count_status)
            if task_count_status["task_count"] >= 1:
                if task_count_status["task_status"] == "open":  # 若task还没有被执行完，那就修改时间然后再执行task
                    update_task_at_dcs(handle_task["task"][0])
                    self.run_task_post(handle_task["task"][0], task_count_status["task_lists"])
                    run_dcs_task_by_count(self.item_no)
                else:
                    break
        # 执行task执行后生成的task
        for task_i in range(1, len(handle_task["task"])):
            for i in range(0, 50):
                task_count_status = self.check_task_count_status(handle_task["task"][task_i], "")
                print(task_count_status)
                if task_count_status["task_count"] >= len(repay_period):
                    if task_count_status["task_status"] == "open":  # task还没有被执行完
                        update_task_at_dcs(handle_task["task"][task_i])
                        self.run_task_post(handle_task["task"][task_i], task_count_status["task_lists"])
                        run_dcs_task_by_count(self.item_no)
                    else:
                        break

    # 通过接口执行dcs的结算job
    def run_clearing_jobs_post_settlement(self, handle_task):
        '''
        :param handle_task: job以及job生成的task组成的字典
        :param repay_period: 是一个存有全部期次的元祖，元祖的元素可能只有一个，可能有多个
        :param is_one_repay: 是否一期一期的还，目前只有华北小贷在使用这个字段
        :return: 没有返回值
        '''
        # 修改原自动结算job的参数，并执行job
        if handle_task["handle"] == "biz_dcs_AutoSettlementJob":
            auto_settlement_handle_params["loanType"] = self.loan_type
            self.run_job_get(handle_task["handle"], auto_settlement_handle_params)

        open_task = "select * from clean_task where task_type='newSettlement' and task_status='open'"
        wait_dcs_record_appear(open_task)
        # run_dcs_task_by_type_until_disappear("lockClearingTrans")
        run_dcs_task_by_type_until_disappear("newSettlement")
        run_dcs_task_by_type_until_disappear("genericDealTransactionNew")
        run_dcs_task_by_type_until_disappear("genericDealTransactionApply")
        # deposit执行task,并将具体的订单状态改为成功
        deposit_run_task_by_order_no()
        update_deposit_orderandtrade_and_run_task(status=2)
        run_dcs_task_by_type_until_disappear("genericDealTransactionQuery")
        run_dcs_task_by_type_until_disappear("cleanSettlementBusinessProcess")

        if self.channel == "noloan":
            run_dcs_task_by_type_until_disappear("accrualSettlementProcess")

        # for i in range(0, 100):
        #     task_count_status = self.check_task_count_status(handle_task["task"][0], "Settlement")
        #     print(task_count_status)
        #     if task_count_status["task_count"] >= 1:
        #         if task_count_status["task_status"] == "open":  # 若task还没有被执行完，那就修改时间然后再执行task
        #             update_task_at_dcs(handle_task["task"][0])
        #             self.run_task_post(handle_task["task"][0], task_count_status["task_lists"])
        #         else:
        #             break
        # # 执行task执行后生成的task
        # for task_i in range(1, len(handle_task["task"])):
        #     for i in range(0, 100):
        #         task_count_status = self.check_task_count_status(handle_task["task"][task_i], "Settlement")
        #         print(task_count_status)
        #         if task_count_status["task_count"] >= len(repay_period):
        #             if task_count_status["task_status"] == "open":  # task还没有被执行完
        #                 update_task_at_dcs(handle_task["task"][task_i])
        #                 self.run_task_post(handle_task["task"][task_i], task_count_status["task_lists"])
        #             else:
        #                 break
        #
        # for task_i in range(1, len(handle_task["task"])):
        #     for i in range(0, 100):
        #         task_count_status = self.check_task_count_status(handle_task["task"][task_i], "Settlement")
        #         print(task_count_status)
        #         if task_count_status["task_count"] >= len(repay_period):
        #             if task_count_status["task_status"] == "open":  # task还没有被执行完
        #                 update_task_at_dcs(handle_task["task"][task_i])
        #                 self.run_task_post(handle_task["task"][task_i], task_count_status["task_lists"])
        #                 # deposit执行task,并将具体的订单状态改为成功
        #                 deposit_run_task_by_order_no()
        #             else:
        #                 break

    # 通过接口执行dcs的job
    def run_clearing_job_post(self, handle_task, processdate=''):
        '''
        :param handle_task: job以及job生成的task组成的字典
        :return: 没有返回值
        '''
        if handle_task["handle"] == "biz_dcs_AdvanceClearingGuaranteeJob":
            advance_clearing_params["processDate"] = processdate
            advance_clearing_params["assetItemNo"] = self.item_no
            advance_clearing_params["loanChannel"] = self.channel
            advance_clearing_params["dateType"] = "actual_finish_time"
            advance_clearing_params["holidayAdvance"] = "false"
            advance_clearing_params["defaultDateValue"] = "before"
            self.run_job_get(handle_task["handle"], advance_clearing_params)
        if handle_task["handle"] == "biz_dcs_BuyBackGuaranteeJob":
            buyback_clearing_params["processDate"] = get_date_before_today()[:10]
            # clearing_handle_params["processDate"] = "2020-07-08"
            buyback_clearing_params["assetItemNos"] = [self.item_no]
            buyback_clearing_params["loanChannels"] = [self.channel]
            self.run_job_get(handle_task["handle"], buyback_clearing_params)
        if handle_task["handle"] == "biz_dcs_AdvanceClearingJob" and self.channel == "huabeixiaodai_zhitou":
            date_new = processdate
            # 这里需要有节假日的判断，如果当前为节假日，job执行后并不会生成task
            for time_i in range(1, 100):
                holiday_date = get_is_holiday(date_new)
                if holiday_date == 1:
                    # 如果是节假日，就需要提前处理，直到上一个工作日
                    date_new = get_date_before(date_new, day=1)
                else:
                    break
            advance_clearing_params["processDate"] = date_new
            advance_clearing_params["assetItemNo"] = self.item_no
            advance_clearing_params["loanChannel"] = self.channel
            advance_clearing_params["dateType"] = "actual_finish_time"
            advance_clearing_params["holidayAdvance"] = "true"
            advance_clearing_params["defaultDateValue"] = "now"
            self.run_job_get(handle_task["handle"], advance_clearing_params)

        for i in range(0, 20):
            task_count_status = self.check_task_count_status(handle_task["task"][0], "")
            print(task_count_status)
            if task_count_status["task_count"] >= 1:
                if task_count_status["task_status"] == "open":
                    update_task_at_dcs(handle_task["task"][0])
                    self.run_task_post(handle_task["task"][0], task_count_status["task_lists"])
                    run_dcs_task_by_count(self.item_no)
                else:
                    break

    def check_task_count_status(self, task_type, task_request_data="N"):
        # 查询task，并返回task的数量和状态
        if task_request_data:
            task_list = get_task_dcs(task_type, self.item_no, task_request_data)  # task_list 是列表嵌套字典的格式：[{},{}]
        else:
            task_list = get_task_dcs(task_type, self.item_no, "")  # task_list 是列表嵌套字典的格式：[{},{}]
        if task_list:
            task_count = len(task_list)
        else:
            task_count = 0
        task_lists = task_list
        if task_request_data:
            task_close_list = get_task_dcs_close(task_type, self.item_no,
                                                 task_request_data)  # task_close_list 是列表嵌套字典的格式：[{},{}]
        else:
            task_close_list = get_task_dcs_close(task_type, self.item_no, "")  # task_close_list 是列表嵌套字典的格式：[{},{}]
        if task_close_list:
            task_status = "open"
        else:
            task_status = "close"
        return {"task_count": task_count, "task_status": task_status, "task_lists": task_lists}

    def run_task_post(self, task_type, id_list):
        id_lists = []
        if isinstance(id_list, int):
            id_lists = [id_list]
        else:
            for ii in range(0, len(id_list)):
                id_lists.append(id_list[ii]["task_id"])
        resp = parse_resp_body(requests.request(
            method='post', url=run_task_url, headers={'Content-Type': 'application/json'}, json=id_lists))
        print("task是{0}，task_id为{1}，执行情况为{2}".format(task_type, id_lists, resp["content"]))

    def run_task_by_task_type(self, task_type):
        task_list = get_task_dcs_by_order_no_and_type(task_type, self.item_no)
        id_lists = []
        if isinstance(task_list, int):
            id_lists = [task_list]
        else:
            for ii in range(0, len(task_list)):
                id_lists.append(task_list[ii]["task_id"])
        print("task_list:", task_list)
        print("id_lists:", id_lists)
        resp = parse_resp_body(requests.request(
            method='post', url=run_task_url, headers={'Content-Type': 'application/json'}, json=id_lists))
        print("task是{0}，task_id为{1}，执行情况为{2}".format(task_type, id_lists, resp["content"]))

    def run_capital_settlement_task(self, handle_task):
        for task_i in range(0, len(handle_task["task"])):
            for i in range(0, 20):
                task_count_status = self.check_task_count_status(handle_task["task"][task_i])
                print(task_count_status)
                if task_count_status["task_count"] >= 1:
                    if task_count_status["task_status"] == "open":  # task还没有被执行完
                        update_task_at_dcs(handle_task["task"][task_i])
                        run_dcs_task_by_count(self.item_no)
                    else:
                        break
