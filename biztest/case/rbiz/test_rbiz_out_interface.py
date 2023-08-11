# -*- coding: utf-8 -*-

from biztest.case.rbiz.base_repay_test import BaseRepayTest
from biztest.config.rbiz.rbiz_nacos_kv_config import update_repay_paysvr_config
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.function.rbiz.rbiz_check_function import *
from biztest.function.rbiz.rbiz_db_function import *
from biztest.util.easymock.rbiz.paysvr import *
from biztest.interface.rbiz.rbiz_interface import *
from biztest.util.msg.msg import Msg
from biztest.util.task.task import Task
from biztest.function.rbiz.assertion import *
import common.global_const as gc


class TestRbizOutInterface(BaseRepayTest):
    """
    提供给外部的接口，回归时使用
    接口文档：https://www.tapd.cn/20584621/markdown_wikis/show/#1120584621001004827
    BC中心调用还款系统接口列表
    paydayloan/repay/combo-active-encrypt 用户主动还款接口(合并代扣)
    paydayloan/repay/combo-query-key 根据请求key查询代扣结果
    paydayloan/projectRepayQuery 根据资产编号查询资产的还款情况列表
    paydayloan/repay/bindSms 发送短信
    sync/withhold-card-encrypt 代扣卡同步
    trade/asset-void-withhold-encrypt 资产取消接口 -- 在haohanqianjingjing有实现

    """

    loan_channel = "haohanqianjingjing"
    exp_sign_company = "tq,tqa,tqb"
    exp_sign_company_no_loan = "tq,tqa,tqb"
    pricipal_amount = 800000

    @classmethod
    def setup_class(cls):
        monitor_check()
        update_repay_paysvr_config(mock_project['rbiz_auto_test']['id'])
        cls.paysvr_mock = PaysvrMock(rbiz_mock)
        cls.task = Task("rbiz{0}".format(gc.ENV))
        cls.msg = Msg("rbiz{0}".format(gc.ENV))

    def setup_method(self):
        # mock代扣成功
        self.paysvr_mock.update_query_protocol_channels_bind_sms()
        self.paysvr_mock.update_auto_pay_withhold_process()
        self.paysvr_mock.update_withhold_query(2)
        self.four_element = get_four_element()
        # 大小单进件
        self.item_no, self.item_num_no_loan = asset_import_and_loan_to_success(self.loan_channel, self.four_element)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.out_interface
    def test_repay_combo_query_key(self):
        """
        该测试用例涉及了根据key查询代扣记录
        :return:
        """
        # step 1 修改资产到期日
        self.change_asset_due_at(0, -10)
        # step 2 发起主动代扣
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        withhold_request = get_withhold_request_by_item_no(self.item_no)
        query_before, req_body, url = repay_combo_query_key(withhold_request[0]['withhold_request_req_key'])
        check_json_rs_data(query_before['content'], code=0, message='请求成功')
        check_json_rs_data(query_before['content']['data'][0], status=2, memo='处理中', project_num=self.item_num_no_loan)
        check_json_rs_data(query_before['content']['data'][1], status=2, memo='处理中', project_num=self.item_no)
        # step 3 执行task和msg
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        self.check_response_after_apply_success(repay_resp, withhold, withhold_no_loan)
        query_after, req_body, url = repay_combo_query_key(withhold_request[0]['withhold_request_req_key'])
        check_json_rs_data(query_after['content'], code=0, message='请求成功')
        check_json_rs_data(query_after['content']['data'][0], status=0, memo='自动化测试', project_num=self.item_num_no_loan,
                           order_no=withhold_no_loan[0]['withhold_serial_no'])
        check_json_rs_data(query_after['content']['data'][1], status=0, memo='自动化测试', project_num=self.item_no,
                           order_no=withhold[0]['withhold_serial_no'])

    @pytest.mark.rbiz_auto_test
    @pytest.mark.out_interface
    def test_project_repay_query(self):
        """
        该测试用例涉及了根据资产编号查询还款计划
        :return:
        """
        # step 1 修改资产到期日
        one_period_amount = 65153
        late_amount = 264
        one_period_amount_x = 10297
        late_amount_x = 42
        self.change_asset_due_at(-1, -10)
        # 代扣前检查
        # 大单
        query_before = project_repay_query(self.item_no)
        check_json_rs_data(query_before['content'], code=0, message='')
        check_json_rs_data(query_before['content']['data']['principal']['period_1'], period=1, amount=one_period_amount,
                           status='unfinished', repaid_amount=0)
        check_json_rs_data(query_before['content']['data']['late_interest']['period_1'], period=1, amount=late_amount,
                           status='unfinished', repaid_amount=0)
        # 小单
        query_before_no_loan = project_repay_query(self.item_num_no_loan)
        check_json_rs_data(query_before_no_loan['content'], code=0, message='')
        check_json_rs_data(query_before_no_loan['content']['data']['principal']['period_1'], period=1,
                           amount=one_period_amount_x,
                           status='unfinished', repaid_amount=0)
        check_json_rs_data(query_before_no_loan['content']['data']['late_interest']['period_1'], period=1,
                           amount=late_amount_x,
                           status='unfinished', repaid_amount=0)

        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        repay_resp = self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)

        # 代扣中检查
        # 大单
        query_in = project_repay_query(self.item_no)

        check_json_rs_data(query_in['content'], code=0, message='')
        check_json_rs_data(query_in['content']['data']['principal']['period_1'], period=1, amount=one_period_amount,
                           status='repaying', repaid_amount=0)
        check_json_rs_data(query_in['content']['data']['late_interest']['period_1'], period=1, amount=late_amount,
                           status='repaying', repaid_amount=0)
        # 小单
        query_in_no_loan = project_repay_query(self.item_num_no_loan)
        check_json_rs_data(query_in_no_loan['content'], code=0, message='')
        check_json_rs_data(query_in_no_loan['content']['data']['principal']['period_1'], period=1,
                           amount=one_period_amount_x,
                           status='repaying', repaid_amount=0)
        check_json_rs_data(query_in_no_loan['content']['data']['late_interest']['period_1'], period=1,
                           amount=late_amount_x,
                           status='repaying', repaid_amount=0)
        # step 3 执行task和msg
        withhold, withhold_no_loan = self.run_all_task_after_repay_success()
        self.check_response_after_apply_success(repay_resp, withhold, withhold_no_loan)
        # 代扣后查询
        query_after = project_repay_query(self.item_no)
        check_json_rs_data(query_after['content'], code=0, message='')
        check_json_rs_data(query_after['content']['data']['principal']['period_1'], period=1, amount=one_period_amount,
                           status='finish', repaid_amount=one_period_amount)
        check_json_rs_data(query_after['content']['data']['late_interest']['period_1'], period=1, amount=late_amount,
                           status='finish', repaid_amount=late_amount)
        query_after_no_loan = project_repay_query(self.item_num_no_loan)
        check_json_rs_data(query_after_no_loan['content'], code=0, message='')
        check_json_rs_data(query_after_no_loan['content']['data']['principal']['period_1'], period=1,
                           amount=one_period_amount_x,
                           status='finish', repaid_amount=one_period_amount_x)
        check_json_rs_data(query_after_no_loan['content']['data']['late_interest']['period_1'], period=1,
                           amount=late_amount_x,
                           status='finish', repaid_amount=late_amount_x)

    '''
    FOX(贷后)调用还款系统接口列表
    fox/deadline-asset-query-encrypt 查询到期日资产列表
    asset/overdue-view-for-fox 根据资产编号查询还款计划(目前在biz维护)
    fox/query-new-overdue 查询最新入催的资产列表(用于贷后系统对账) --TODO 
    fox/query-new-overdue-asset-detail 根据资产编号查询新入催的资产详情(用于贷后系统对账) --TODO 
    fox/query-asset-repay 查询入催最近2天资产还款资产(用于贷后系统对账) --TODO 
    fox/query-asset-repay-detail 根据资产编号和还款日期查询资产还款情况(用于贷后系统对账) --TODO 
    assetTran/decrease 罚息减免  --TODO 
    fox/manual-withhold-encrypt 手动代扣接口 --TODO 
    fox/manual-withhold-query 代扣结果查询。  --- --TODO 
    fox/query-card-list-encrypt 查询用户卡列表


    风控系统调用还款系统接口列表
    fk/asset-info 根据资产编号查询还款计划
    '''

    @pytest.mark.rbiz_auto_test
    @pytest.mark.out_interface
    def test_fox_deadline_asset_query(self):
        """
        该测试用例涉及了 查询到期日资产列表
        :return:
        """
        self.change_asset_due_at(-1, -1)
        resp = fox_deadline_asset_query()
        result = False
        for item in resp["content"]["data"]:
            if item["asset_item_no"] in (self.item_no, self.item_num_no_loan):
                Assert.assert_match_json({"status": "nofinish",
                                          "type": "paydayloan",
                                          "owner": "KN",
                                          "asset_item_no": self.item_no + "|" + self.item_num_no_loan,
                                          "asset_extend_ref_order_no": self.item_no + "|" + self.item_num_no_loan},
                                         item)
                result = True
        Assert.assert_equal(result, True, "无数据")

    # @pytest.mark.out_interface
    def test_biz_asset_overdue_view_for_fox(self):
        """
        该测试用例涉及了 根据资产编号查询还款计划(目前在biz维护)
        :return:
        """
        resp = asset_overdue_view_for_fox(self.item_no)
        check_json_rs_data(resp['content'], code=0)
        check_json_rs_data(resp['content']['data']['asset'], asset_item_number=self.item_no)

    @pytest.mark.rbiz_auto_test
    @pytest.mark.out_interface
    def test_fox_query_card_list(self):
        """
        该测试用例涉及了 查询用户卡列表
        :return:
        """
        resp = fox_query_card_list(self.four_element['data']['id_number_encrypt'])
        check_json_rs_data(resp['content'], code=0, message='ok')
        check_json_rs_data(resp['content']['data'][0],
                           account_name_encrypt=self.four_element['data']['user_name_encrypt'],
                           id_number_encrypt=self.four_element['data']['id_number_encrypt'])

    @pytest.mark.rbiz_auto_test
    @pytest.mark.out_interface
    def test_decrease_late_fee(self):
        """
        该测试用例涉及了减免罚息 减免未还
        :return:
        """
        # 修改大小单还款时间
        self.change_asset_due_at(-1, -1)
        # 刷新罚息
        self.refresh_late_fee(self.item_no)
        check_asset_tran_by_item_no_and_type_and_period(self.item_no, "lateinterest", 1, asset_tran_amount=26,
                                                        asset_tran_status='nofinish')
        resp, req_body, url = asset_tran_decrease(self.item_no, 100, 1, "lateinterest")
        check_json_rs_data(resp['content'], code=0, message='减免成功！')
        check_asset_tran_by_item_no_and_type_and_period(self.item_no, "lateinterest", 1, asset_tran_amount=0,
                                                        asset_tran_status='finish')

    @pytest.mark.rbiz_auto_test
    @pytest.mark.out_interface
    def test_decrease_late_fee_after_repay(self):
        """
        该测试用例涉及了减免罚息 减免已还
        :return:
        """
        # 修改大小单还款时间
        self.change_asset_due_at(-1, -1)
        # 刷新罚息
        self.refresh_late_fee(self.item_no)
        self.refresh_late_fee(self.item_num_no_loan)
        check_asset_tran_by_item_no_and_type_and_period(self.item_no, "lateinterest", 1, asset_tran_amount=26,
                                                        asset_tran_status='nofinish')
        asset_tran_amount = get_asset_tran_balance_amount_by_item_no_and_period(self.item_no, 1)
        asset_tran_amount_no_loan = get_asset_tran_balance_amount_by_item_no_and_period(self.item_num_no_loan, 1)
        self.repay_apply_success(asset_tran_amount, asset_tran_amount_no_loan)
        self.run_all_task_after_repay_success()
        # self.run_all_msg_after_repay_success()

        resp, req_body, url = asset_tran_decrease(self.item_no, 100, 1, "lateinterest")
        check_json_rs_data(resp['content'], code=0, message='减免成功！')
        check_asset_tran_by_item_no_and_type_and_period(self.item_no, "lateinterest", 1, asset_tran_amount=0,
                                                        asset_tran_status='finish')
        check_asset_tran_by_item_no_and_type_and_period(self.item_no, "reserve", 2, asset_tran_repaid_amount=26,
                                                        asset_tran_status='nofinish')

    @pytest.mark.rbiz_auto_test
    @pytest.mark.out_interface
    def test_fix_status_asset_change_mq_sync(self):
        """
        该测试用例涉及了根据key查询代扣记录
        :return:
        """
        resp = fix_status_asset_change_mq_sync(self.item_no)
        check_json_rs_data(resp['content'], code=0, message='mq发送成功')

    @pytest.mark.rbiz_auto_test
    @pytest.mark.out_interface
    def test_fk_asset_info(self):
        """
        该测试用例涉及了根据key查询代扣记录
        :return:
        """
        resp = fk_asset_info(self.item_no)
        check_json_rs_data(resp['content'], code=0, message='ok')
        check_json_rs_data(resp['content']['data']['grant'], apply_source='paydayloan', loan_amount=800000)

    # @pytest.mark.rbiz_auto_test
    @pytest.mark.out_interface
    def test_run_job(self):
        """
        该测试用例涉及了执行各种job
        assetRelateHistoryMove
        withholdRelateHistoryMove
        pushOverdueToFox

        :return:
        """

        run_job_by_api("withholdRelateHistoryMove", {"paramWithholdId": 30})
        # resp = fk_asset_info(self.item_no)
        # check_json_rs_data(resp['content'], code=0, message='ok')
        # check_json_rs_data(resp['content']['data']['grant'], apply_source='paydayloan', loan_amount=800000)
