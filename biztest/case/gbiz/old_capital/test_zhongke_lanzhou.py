from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.zhongke_lanzhou import ZhongkeLanzhouMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_router_capital_plan_amount,\
    update_all_channel_amount, update_router_cp_amount_all_to_zero
import pytest
from biztest.util.tools.tools import get_four_element


# @pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_zhongke_lanzhou
class TestZhongkeLanzhou(BaseTestCapital):

    def init(self):
        super(TestZhongkeLanzhou, self).init()
        self.channel = "zhongke_lanzhou"
        self.capital_mock = ZhongkeLanzhouMock(gbiz_mock)
        update_gbiz_capital_zhongke_lanzhou()
        update_gbiz_capital_zhongke_lanzhou_const()
        # 修改回滚策略配置，回滚Case会用到
        update_gbiz_manual_task_auto_process_config()
        update_all_channel_amount()


    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.capital_mock.update_tied_card_query_nodata()
        self.capital_mock.update_pre_tied_card()
        self.capital_mock.update_pretiedcardquey_success()
        self.capital_mock.update_tied_card()
        self.capital_mock.update_tied_card_query_success()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='zhongke_lanzhou', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='zhongke_lanzhou', step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_rate_query()
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.capital_mock.update_ftp_upload_success()
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_face_recognition()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repay_plan(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_zhongke_lanzhou_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 # ("香蕉", "irr36_quanyi", 6),
                                 ("草莓", "irr36_quanyi", 12),
                             ])
    def test_zhongke_lanzhou_loan_success(self, case, app, source_type, count):
        """
        放款成功
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # check_request_log_by_channel(item_no, self.channel)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("count", [12])
    def test_zhongke_lanzhou_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        # canloan失败准备工作
        today = time.strftime("%Y-%m-%d", time.localtime())
        update_router_capital_plan_amount(0, today, self.channel)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        time.sleep(2)
        # canloan执行之后恢复
        update_router_capital_plan_amount(3333333333, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "zhongke_lanzhou->校验资金量失败;")

    @pytest.mark.parametrize("count", [12])
    def test_zhongke_lanzhou_customer_fail(self, case, count):
        """
        客户信息推送失败切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_rate_query()
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 1900002, "客户信息推送-处理失败")

    @pytest.mark.parametrize("count", [12])
    def test_zhongke_lanzhou_customer_fail_assetvoid_rollback(self, case, count):
        """
        客户信息推送失败切资方,取消资产,取消任务回滚到切换资金方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_rate_query()
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 将所有资金方的金额修改为0，便于切换资金方任务切换失败，生成取消任务
        update_router_cp_amount_all_to_zero()
        update_task_by_item_no_task_type(item_no, "ChangeCapital", task_status="open")
        self.task.run_task(item_no, "ChangeCapital", excepts={"code": 1})
        time.sleep(3)
        # 通过接口调用job回滚任务
        run_job("manualTaskAutoProcessJob",
                {"taskTypeList": ["ChangeCapital", "AssetVoid", "CapitalAssetReverse", "BlacklistCollect"]})
        # 恢复所有资金方的金额
        update_all_channel_amount()
        # 检查回滚生成的切换资金方任务参数并执行
        check_rollback_changecapital_data(item_no, 10000, "AssetVoid回滚到ChangeCapital自动执行", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("count", [12])
    def test_zhongke_lanzhou_face_fail(self, case, count):
        """
        人脸识别失败切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_rate_query()
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_face_recognition()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_fail()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 2900002, "人脸识别-处理失败")

    @pytest.mark.test_zhongke_lanzhou_loan_fail
    @pytest.mark.parametrize("count", [12])
    def test_zhongke_lanzhou_loan_fail(self, case, count):
        """
        放款支用失败切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_rate_query()
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_face_recognition()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 3999909, "贷款支用查询-支付失败")

    @pytest.mark.capital_account
    def test_register_send_sms_fail_01(self, case):
        """
        兰州预绑卡接口异常，发短信失败
        """
        four_element = get_four_element()
        item_no = get_item_no()
        # 开户查询
        resp = capital_regiest_query(self.channel, four_element, item_no)
        Assert.assert_equal(0, resp['code'])
        # 执行开户：发短信
        self.capital_mock.update_pre_tied_card_fail()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='GetSmsVerifyCode')
        # 断言：步骤状态为2，发短信环节失败2
        Assert.assert_equal(0, resp['code'])
        check_data(resp['data'], status=2, way=self.channel, step_type="PROTOCOL", interaction_type="SMS")
        check_data(resp['data']['actions'][0], action_type='GetSmsVerifyCode', status=2)
        check_data(resp['data']['actions'][1], action_type='CheckSmsVerifyCode', status=4)
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=4, step_status=2)

    @pytest.mark.capital_account
    def test_register_check_sms_fail_01(self, case):
        """
        兰州绑卡接口异常，短信验证失败
        """
        four_element = get_four_element()
        item_no = get_item_no()
        # 开户查询
        resp = capital_regiest_query(self.channel, four_element, item_no)
        Assert.assert_equal(0, resp['code'])
        # 执行开户：发短信
        self.capital_mock.update_pre_tied_card()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='GetSmsVerifyCode')
        Assert.assert_equal(0, resp['code'])
        sms_seq = resp['data']['actions'][0]['extra_data']['seq']
        # 执行开户：验证短信
        self.capital_mock.update_tied_card_fail()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='CheckSmsVerifyCode', seq=sms_seq)
        Assert.assert_equal(0, resp['code'])
        # 断言：步骤状态为2，验证环节失败2
        check_data(resp['data'], status=2, way=self.channel, step_type="PROTOCOL", interaction_type="SMS")
        check_data(resp['data']['actions'][0], action_type='GetSmsVerifyCode', status=0)
        check_data(resp['data']['actions'][1], action_type='CheckSmsVerifyCode', status=2)
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=4, step_status=2)

    @pytest.mark.capital_account
    def test_register_check_sms_fail_02(self, case):
        """
        兰州绑卡查询异常-绑卡失败，短信验证失败
        """
        four_element = get_four_element()
        item_no = get_item_no()
        # 开户查询
        resp = capital_regiest_query(self.channel, four_element, item_no)
        Assert.assert_equal(0, resp['code'])
        # 执行开户：发短信
        self.capital_mock.update_pre_tied_card()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='GetSmsVerifyCode')
        Assert.assert_equal(0, resp['code'])
        sms_seq = resp['data']['actions'][0]['extra_data']['seq']
        # 执行开户：验证短信
        self.capital_mock.update_tied_card()
        self.capital_mock.update_tied_card_query_fail()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='CheckSmsVerifyCode', seq=sms_seq)
        Assert.assert_equal(0, resp['code'])
        # 断言：步骤状态为2，验证环节失败2
        check_data(resp['data'], status=2, way=self.channel, step_type="PROTOCOL", interaction_type="SMS")
        check_data(resp['data']['actions'][0], action_type='GetSmsVerifyCode', status=0)
        check_data(resp['data']['actions'][1], action_type='CheckSmsVerifyCode', status=2)
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=4, step_status=2)

    @pytest.mark.capital_account
    def test_register_check_sms_fail_03(self, case):
        """
        兰州绑卡查询异常-无绑卡记录，短信验证失败
        """
        four_element = get_four_element()
        item_no = get_item_no()
        # 开户查询
        resp = capital_regiest_query(self.channel, four_element, item_no)
        Assert.assert_equal(0, resp['code'])
        # 执行开户：发短信
        self.capital_mock.update_pre_tied_card()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='GetSmsVerifyCode')
        Assert.assert_equal(0, resp['code'])
        sms_seq = resp['data']['actions'][0]['extra_data']['seq']
        # 执行开户：验证短信
        self.capital_mock.update_tied_card()
        self.capital_mock.update_tied_card_query_nodata()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='CheckSmsVerifyCode', seq=sms_seq)
        Assert.assert_equal(0, resp['code'])
        # 断言：步骤状态为2
        check_data(resp['data'], status=2, way=self.channel, step_type="PROTOCOL", interaction_type="SMS")
        check_data(resp['data']['actions'][0], action_type='GetSmsVerifyCode', status=0)
        check_data(resp['data']['actions'][1], action_type='CheckSmsVerifyCode', status=4)
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=4, step_status=2)

    @pytest.mark.capital_account
    def test_register_success_01_normal(self, case):
        """
        兰州开户成功
        """
        four_element = get_four_element()
        item_no = get_item_no()
        # 开户查询
        resp = capital_regiest_query(self.channel, four_element, item_no)
        Assert.assert_equal(0, resp['code'])
        # 账户状态为4-未开户
        Assert.assert_equal(4, resp['data']['status'])
        # 步骤状态为4-未开户
        Assert.assert_equal(1, len(resp['data']['steps']))
        check_data(resp['data']['steps'][0], step_type="PROTOCOL", interaction_type="SMS", status=4, way=self.channel)
        # 环节状态为4-未开户
        Assert.assert_equal(2, len(resp['data']['steps'][0]['actions']))
        check_data(resp['data']['steps'][0]['actions'][0], action_type='GetSmsVerifyCode', status=4)
        check_data(resp['data']['steps'][0]['actions'][1], action_type='CheckSmsVerifyCode', status=4)
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=4, step_status=4)
        # 执行开户：发短信
        self.capital_mock.update_pre_tied_card()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='GetSmsVerifyCode')
        Assert.assert_equal(0, resp['code'])
        sms_seq = resp['data']['actions'][0]['extra_data']['seq']
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=4, step_status=2)
        # 执行开户：验证短信
        self.capital_mock.update_tied_card()
        self.capital_mock.update_tied_card_query_success()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='CheckSmsVerifyCode', seq=sms_seq)
        Assert.assert_equal(0, resp['code'])
        # 断言：步骤和环节状态为0-成功
        check_data(resp['data'], status=0, way=self.channel, step_type="PROTOCOL", interaction_type="SMS")
        check_data(resp['data']['actions'][0], action_type='GetSmsVerifyCode', status=0)
        check_data(resp['data']['actions'][1], action_type='CheckSmsVerifyCode', status=0)
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=4, step_status=0,
                                   user_key=sms_seq)
        # 开户查询
        resp = capital_regiest_query(self.channel, four_element, item_no)
        Assert.assert_equal(0, resp['code'])
        # 断言：账户、步骤、环节状态都为0-成功
        Assert.assert_equal(0, resp['data']['status'])
        Assert.assert_equal(1, len(resp['data']['steps']))
        check_data(resp['data']['steps'][0], status=0, step_type="PROTOCOL", interaction_type="SMS", way=self.channel)
        Assert.assert_equal(2, len(resp['data']['steps'][0]['actions']))
        check_data(resp['data']['steps'][0]['actions'][0], action_type='GetSmsVerifyCode', status=0)
        check_data(resp['data']['steps'][0]['actions'][1], action_type='CheckSmsVerifyCode', status=0)
        check_capital_account_data(item_no, four_element,  self.channel, self.channel, account_status=0, step_status=0,
                                   user_key=sms_seq)

    @pytest.mark.capital_account
    def test_register_success_02_without_seq(self, case):
        """
        兰州绑卡，不提交seq，也可以开户成功
        """
        four_element = get_four_element()
        item_no = get_item_no()
        # 开户查询
        resp = capital_regiest_query(self.channel, four_element, item_no)
        Assert.assert_equal(0, resp['code'])
        check_capital_account_data(item_no, four_element,  self.channel, self.channel, account_status=4, step_status=4)
        # 执行开户：发短信
        self.capital_mock.update_pre_tied_card()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='GetSmsVerifyCode')
        Assert.assert_equal(0, resp['code'])
        sms_seq = resp['data']['actions'][0]['extra_data']['seq']
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=4, step_status=2)
        # 执行开户：验证短信，不提交seq
        self.capital_mock.update_tied_card()
        self.capital_mock.update_tied_card_query_success()
        resp = capital_regiest(self.channel, four_element, item_no, way=self.channel, step_type='PROTOCOL',
                               action_type='CheckSmsVerifyCode')
        Assert.assert_equal(0, resp['code'])
        # 断言：步骤和环节状态为0-成功
        check_data(resp['data'], status=0, way=self.channel, step_type="PROTOCOL", interaction_type="SMS")
        check_data(resp['data']['actions'][0], action_type='GetSmsVerifyCode', status=0)
        check_data(resp['data']['actions'][1], action_type='CheckSmsVerifyCode', status=0)
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=4, step_status=0,
                                   user_key=sms_seq)
        # 开户查询
        resp = capital_regiest_query(self.channel, four_element, item_no)
        Assert.assert_equal(0, resp['code'])
        # 断言：账户、步骤、环节状态都为0-成功
        Assert.assert_equal(0, resp['data']['status'])
        Assert.assert_equal(1, len(resp['data']['steps']))
        check_data(resp['data']['steps'][0], status=0, step_type="PROTOCOL", interaction_type="SMS", way=self.channel)
        Assert.assert_equal(2, len(resp['data']['steps'][0]['actions']))
        check_data(resp['data']['steps'][0]['actions'][0], action_type='GetSmsVerifyCode', status=0)
        check_data(resp['data']['steps'][0]['actions'][1], action_type='CheckSmsVerifyCode', status=0)
        check_capital_account_data(item_no, four_element, self.channel, self.channel, account_status=0, step_status=0,
                                   user_key=sms_seq)
