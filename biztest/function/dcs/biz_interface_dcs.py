from copy import deepcopy
import requests
from biztest.config.dcs.params_config import capital_settlement_notify, rbiz_compensateList, rbiz_compensate
from biztest.config.dcs.url_config import capital_settlement_notify_url, rbiz_compensate_url
from biztest.function.dcs.biz_database import get_one_repay_plan, get_one_repay_plan_ft, get_asset_loan_record
from biztest.util.tools.tools import get_date_before_today, get_random_str, parse_resp_body, get_random_num, get_date, \
    get_timestamp


class BizInterfaceDcs:
    def __init__(self, item_no, channel, period_count, env):
        self.env_test = env
        self.item_no = item_no
        self.channel = channel
        self.period_count = period_count

    # 模拟 biz-central 发起请求
    # https://biz-gateway-proxy.k8s-ingress-nginx.kuainiujinke.com/biz-dcs-1/capital/settlement-notify
    def capital_settlement_notify(self, period_min, period_max, operate_type, withhold_channel, is_partly_amount,
                                  amount_type, expect_operate_at):
        advanced_params = deepcopy(capital_settlement_notify)
        advanced_params.update(key="haha_" + get_random_str())
        advanced_params["data"]["loan_channel"] = self.channel
        advanced_params["data"]["asset_item_no"] = self.item_no
        advanced_params["data"]["version"] = get_timestamp()
        # 拼接 capital_transactions ， 肯定有本金和利息，利息可能会有减免，担保费是到期日结算 ， 通过还款计划取金额和到期日
        principal_repay_plan = get_one_repay_plan(self.item_no, "repayprincipal", period_min, period_max)
        for jj in range(0, len(principal_repay_plan)):
            capital_transactions = {}
            capital_transactions["period"] = principal_repay_plan[jj]["asset_tran_period"]
            capital_transactions["amount_type"] = "principal"
            capital_transactions["operate_type"] = operate_type
            capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                "origin_amount"] = principal_repay_plan[jj]["asset_tran_amount"]
            capital_transactions["user_repay_at"] = get_date_before_today()
            capital_transactions["expect_finish_at"] = principal_repay_plan[jj]["asset_tran_due_at"]
            capital_transactions["expect_operate_at"] = expect_operate_at
            capital_transactions["withhold_channel"] = withhold_channel
            advanced_params["data"]["capital_transactions"].append(capital_transactions)
        # 拼接 capital_transactions ， 肯定有本金和利息，利息可能会有减免，担保费是到期日结算 ， 通过还款计划取金额和到期日
        interest_repay_plan = get_one_repay_plan(self.item_no, "repayinterest", period_min, period_max)
        for ii in range(0, len(interest_repay_plan)):
            capital_transactions = {}
            capital_transactions["period"] = interest_repay_plan[ii]["asset_tran_period"]
            capital_transactions["amount_type"] = "interest"
            capital_transactions["operate_type"] = operate_type
            if operate_type == "chargeback":
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = 0
            elif is_partly_amount == "N" and interest_repay_plan[ii]["asset_tran_period"] == period_min:
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = interest_repay_plan[ii][
                    "asset_tran_amount"]
            elif is_partly_amount == "Y" and interest_repay_plan[ii]["asset_tran_period"] == period_min:  # 最小期次可能有减免
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = interest_repay_plan[ii][
                                                                                             "asset_tran_amount"] / 2.5
            elif is_partly_amount == "Over" and interest_repay_plan[ii]["asset_tran_period"] == period_min:
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = interest_repay_plan[ii][
                                                                                             "asset_tran_amount"]
            else:
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = 0
            capital_transactions["origin_amount"] = interest_repay_plan[ii]["asset_tran_amount"]
            capital_transactions["user_repay_at"] = get_date_before_today()
            capital_transactions["expect_finish_at"] = interest_repay_plan[ii]["asset_tran_due_at"]
            capital_transactions["expect_operate_at"] = expect_operate_at
            capital_transactions["withhold_channel"] = withhold_channel
            advanced_params["data"]["capital_transactions"].append(capital_transactions)
        # 拼接 capital_transactions ， 新增贴息，用利息的值作为贴息
        interest_subsidy_repay_plan = get_one_repay_plan(self.item_no, "repayinterest", period_min, period_max)
        for jj in range(0, len(interest_subsidy_repay_plan)):
            capital_transactions = {}
            capital_transactions["period"] = interest_subsidy_repay_plan[jj]["asset_tran_period"]
            capital_transactions["amount_type"] = "interest_subsidy"  # 用还款计划中的利息作为贴息
            capital_transactions["operate_type"] = operate_type
            # capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
            #     "origin_amount"] = interest_subsidy_repay_plan[jj]["asset_tran_amount"]
            # capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
            #     "origin_amount"] = 0
            if operate_type == "advance":  # 提前还款默认没有贴息
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                    "origin_amount"] = 0
            # N表示=原利息
            elif is_partly_amount == "N" and interest_subsidy_repay_plan[ii]["asset_tran_period"] == period_min:  # 最小期次
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                    "origin_amount"] = 0
            # Over表示>原利息
            elif is_partly_amount == "Over" and interest_subsidy_repay_plan[ii][
                "asset_tran_period"] == period_min:  # 最小期次，加上贴息会超过原利息，多加100保证一定超过原利息
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = \
                interest_subsidy_repay_plan[ii]["asset_tran_amount"]*0.01 + 100
                capital_transactions["origin_amount"] = 0  # biz-central推送贴息金额大于0时,origin_amount=0
            # Y就表示<原利息
            elif is_partly_amount == "Y" and interest_subsidy_repay_plan[ii]["asset_tran_period"] == period_min:
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                    "origin_amount"] = -100
            else:
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                    "origin_amount"] = 0
            capital_transactions["user_repay_at"] = get_date_before_today()
            capital_transactions["expect_finish_at"] = interest_subsidy_repay_plan[jj]["asset_tran_due_at"]
            capital_transactions["expect_operate_at"] = expect_operate_at
            capital_transactions["withhold_channel"] = withhold_channel
            advanced_params["data"]["capital_transactions"].append(capital_transactions)
        # 拼接 capital_transactions ， 新增罚息，用利息的值作为罚息
        lateinterest_repay_plan = get_one_repay_plan(self.item_no, "repayinterest", period_min, period_max)
        for jj in range(0, len(lateinterest_repay_plan)):
            capital_transactions = {}
            capital_transactions["period"] = lateinterest_repay_plan[jj]["asset_tran_period"]
            capital_transactions["amount_type"] = "late_interest"  # 用还款计划中的利息作为罚息
            capital_transactions["operate_type"] = operate_type
            # capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
            #     "origin_amount"] = lateinterest_repay_plan[jj]["asset_tran_amount"]
            # capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
            #     "origin_amount"] = 0
            # capital_transactions["amount"] = 0
            if operate_type == "advance":  # 提前还款默认没有罚息
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                    "origin_amount"] = 0
            # N表示=原利息
            elif is_partly_amount == "N" and lateinterest_repay_plan[ii]["asset_tran_period"] == period_min:  # 最小期次
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                    "origin_amount"] = 0
            # Over表示>原利息
            elif is_partly_amount == "Over" and lateinterest_repay_plan[ii][
                "asset_tran_period"] == period_min:  # 最小期次，加上贴息会超过原利息
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                    "origin_amount"] = lateinterest_repay_plan[ii]["asset_tran_amount"]*0.01 + 100  # 多加100保证一定超过原利息
            # Y就表示<原利息
            elif is_partly_amount == "Y" and lateinterest_repay_plan[ii]["asset_tran_period"] == period_min:
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                    "origin_amount"] = -100
            else:
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = capital_transactions[
                    "origin_amount"] = 0
            capital_transactions["user_repay_at"] = get_date_before_today()
            capital_transactions["expect_finish_at"] = lateinterest_repay_plan[jj]["asset_tran_due_at"]
            capital_transactions["expect_operate_at"] = expect_operate_at
            capital_transactions["withhold_channel"] = withhold_channel
            advanced_params["data"]["capital_transactions"].append(capital_transactions)
        # 拼接 capital_transactions ， 肯定有本金和利息，利息可能会有减免，担保费是到期日结算 ， 通过还款计划取金额和到期日
        if amount_type == "guarantee":
            repay_plan = get_one_repay_plan_ft(self.item_no, "guarantee", period_min, period_max)
            for ii in range(0, len(repay_plan)):
                capital_transactions = {}
                capital_transactions["period"] = repay_plan[ii]["asset_tran_period"]
                capital_transactions["amount_type"] = "guarantee"
                capital_transactions["operate_type"] = operate_type
                if operate_type == "chargeback":
                    capital_transactions["amount"] = capital_transactions["repaid_amount"] = 0
                elif repay_plan[ii]["asset_tran_period"] == period_min:  # 后续期次可能有减免
                    capital_transactions["amount"] = capital_transactions["repaid_amount"] = repay_plan[ii][
                        "asset_tran_amount"]
                else:
                    capital_transactions["amount"] = capital_transactions["repaid_amount"] = 0
                capital_transactions["origin_amount"] = repay_plan[ii]["asset_tran_amount"]
                capital_transactions["user_repay_at"] = get_date_before_today()
                capital_transactions["expect_finish_at"] = capital_transactions["expect_operate_at"] = repay_plan[ii][
                    "asset_tran_due_at"]
                capital_transactions["withhold_channel"] = withhold_channel
                advanced_params["data"]["capital_transactions"].append(capital_transactions)
        # 拼接 capital_transactions ， 肯定有本金和利息，technical_service 通过还款计划取金额和到期日
        if amount_type == "technical_service":
            technical_service_repay_plan = get_one_repay_plan(self.item_no, "technical_service", period_min, period_max)
            for ii in range(0, len(technical_service_repay_plan)):
                capital_transactions = {}
                capital_transactions["period"] = technical_service_repay_plan[ii]["asset_tran_period"]
                capital_transactions["amount_type"] = "technical_service"
                capital_transactions["operate_type"] = operate_type
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = technical_service_repay_plan[ii][
                    "asset_tran_amount"]
                capital_transactions["origin_amount"] = technical_service_repay_plan[ii]["asset_tran_amount"]
                capital_transactions["user_repay_at"] = get_date_before_today()
                capital_transactions["expect_finish_at"] = technical_service_repay_plan[ii]["asset_tran_due_at"]
                capital_transactions["expect_operate_at"] = expect_operate_at
                capital_transactions["withhold_channel"] = withhold_channel
                advanced_params["data"]["capital_transactions"].append(capital_transactions)
        if amount_type == "technical_service_guarantee":
            repay_plan = get_one_repay_plan_ft(self.item_no, "guarantee", period_min, period_max)
            for ii in range(0, len(repay_plan)):
                capital_transactions = {}
                capital_transactions["period"] = repay_plan[ii]["asset_tran_period"]
                capital_transactions["amount_type"] = "guarantee"
                capital_transactions["operate_type"] = operate_type
                if operate_type == "chargeback":
                    capital_transactions["amount"] = capital_transactions["repaid_amount"] = 0
                elif repay_plan[ii]["asset_tran_period"] == period_min:  # 后续期次可能有减免
                    capital_transactions["amount"] = capital_transactions["repaid_amount"] = repay_plan[ii][
                        "asset_tran_amount"]
                else:
                    capital_transactions["amount"] = capital_transactions["repaid_amount"] = 0
                capital_transactions["origin_amount"] = repay_plan[ii]["asset_tran_amount"]
                capital_transactions["user_repay_at"] = get_date_before_today()
                capital_transactions["expect_finish_at"] = capital_transactions["expect_operate_at"] = repay_plan[ii][
                    "asset_tran_due_at"]
                capital_transactions["withhold_channel"] = withhold_channel
                advanced_params["data"]["capital_transactions"].append(capital_transactions)
            technical_service_repay_plan = get_one_repay_plan(self.item_no, "technical_service", period_min, period_max)
            for ii in range(0, len(technical_service_repay_plan)):
                capital_transactions = {}
                capital_transactions["period"] = technical_service_repay_plan[ii]["asset_tran_period"]
                capital_transactions["amount_type"] = "technical_service"
                capital_transactions["operate_type"] = operate_type
                capital_transactions["amount"] = capital_transactions["repaid_amount"] = \
                technical_service_repay_plan[ii][
                    "asset_tran_amount"]
                capital_transactions["origin_amount"] = technical_service_repay_plan[ii]["asset_tran_amount"]
                capital_transactions["user_repay_at"] = get_date_before_today()
                capital_transactions["expect_finish_at"] = technical_service_repay_plan[ii]["asset_tran_due_at"]
                capital_transactions["expect_operate_at"] = expect_operate_at
                capital_transactions["withhold_channel"] = withhold_channel
                advanced_params["data"]["capital_transactions"].append(capital_transactions)

        print("advanced_params, : ", advanced_params)
        resp = parse_resp_body(requests.request(method='post', url=capital_settlement_notify_url,
                                                headers={'Content-Type': 'application/json'}, json=advanced_params))
        print(f"url: {capital_settlement_notify_url} response: {resp['content']}")
        return advanced_params

    # 回购
    # http://kong-api-test.kuainiujinke.com/rbiz3/yunxinquanhu/pre-compensate-callback
    def rbiz_buyback(self, period_min, period_max):
        trans_principal = get_one_repay_plan(self.item_no, 'repayprincipal', period_min, period_max)
        trans_interest = get_one_repay_plan(self.item_no, 'repayinterest', period_min, period_max)
        trans_credit = get_one_repay_plan_ft(self.item_no, 'credit_fee', period_min, period_max)
        rbiz_compensateList_params = deepcopy(rbiz_compensateList)
        for period_i in range(0, len(rbiz_compensateList_params)):
            # 先处理每期的本金和利息，都需要算满
            if trans_principal[period_i]["asset_tran_period"] == period_i + 1:
                rbiz_compensateList_params[period_i]["principal"] = trans_principal[period_i][
                                                                        "asset_tran_amount"] / 100
                rbiz_compensateList_params[period_i]["interest"] = trans_interest[period_i][
                                                                       "asset_tran_amount"] / 100
            # 然后处理当期的授信费，这个地方可能有坑，授信费可能查出来一条也可能查出来两条
            if rbiz_compensateList_params[period_i]["term"] == period_min:
                print(trans_credit)
                rbiz_compensateList_params[period_i]["odInterest"] = trans_credit[0]["asset_tran_amount"] / 100
            # 然后在处理每期总和
            rbiz_compensateList_params[period_i]["totalAmount"] = rbiz_compensateList_params[period_i]["principal"] \
                                                                  + rbiz_compensateList_params[period_i]["interest"] \
                                                                  + rbiz_compensateList_params[period_i]["odInterest"]
        # 然后截取需要的期次，比如从第2期开始回购，就不用第1期的数据了
        rbiz_compensate_params = deepcopy(rbiz_compensate)
        rbiz_compensate_params["compensateList"] = rbiz_compensateList_params[(period_min - 1):]
        rbiz_compensate_params["compensateTime"] = get_date_before_today()
        # 获取uniqueId
        asset_loan_record = get_asset_loan_record(self.item_no)
        rbiz_compensate_params["uniqueId"] = asset_loan_record["asset_loan_record_trade_no"]
        parse_resp_body(
            requests.request(method='post', url=rbiz_compensate_url, headers={"Content-Type": "application/json"},
                             json=rbiz_compensate_params))

        # 执行biz的job，使credit_fee进入资方还款计划表
        # xxl_job = XxlJob(job_group_biz[test_biz]["group_id"], "", password="123456", xxl_job_type="xxl_job_k8s")
        # job_params = "1 yunxin_quanhu " + get_date()[:10]
        # xxl_job.trigger_job_for_id(job_group_biz[test_biz]["capital_tran_job_id"], job_params)
