from biztest.interface.gbiz.gbiz_interface import *
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_changyin_junxin_config import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount, update_asset_due_bill_no, \
    update_router_cp_amount_all_to_zero
import pytest
from biztest.util.easymock.gbiz.changyin_junxin import ChangyinJunxinMock
from biztest.util.tools.tools import get_four_element
from biztest.function.contract.contract_check_function import check_contract


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_changyin_junxin
class TestChangyinJunxin(BaseTestCapital):
    def init(self):
        super(TestChangyinJunxin, self).init()
        self.channel = "changyin_junxin"
        self.capital_mock = ChangyinJunxinMock(gbiz_mock)
        update_gbiz_capital_changyin_junxin()
        update_gbiz_capital_changyin_junxin_const()
        update_all_channel_amount()
        # 修改回滚策略配置，回滚Case会用到
        update_gbiz_manual_task_auto_process_config()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, four_element, item_no):
        self.capital_mock.update_card_query()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_protocol_apply()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_protocol_confirm()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 为了签约合同（34807-长银钧信-个人客户扣款授权书）加的这个任务
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.capital_mock.update_confirm_apply(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query(item_no, asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_query(asset_info, item_no)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=0)
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        #self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_changyin_junxin_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [("香蕉", "apr36", 12),
                              # ("草莓", "irr36", 12),
                              ])
    def test_changyin_junxin_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(four_element, item_no)
        self.loan_to_success(item_no)
        # check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_junxin_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        # canloan失败准备工作
        today = time.strftime("%Y-%m-%d", time.localtime())
        update_router_capital_plan_amount(0, today, self.channel)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        time.sleep(2)
        # canloan执行之后恢复
        update_router_capital_plan_amount(10000000000, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "changyin_junxin->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_junxin_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败切资方（授信申请失败）
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="31")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_credit_apply(item_no, respCode='0001', respMsg='mock测试授信申请失败')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, respCode='0000', respMsg='交易成功！', outSts='02', baselimit=200000)
        check_wait_change_capital_data(item_no, 2, "0001_mock测试授信申请失败", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_junxin_applyquery_fail(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败切资方（授信查询授信拒绝)
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="21")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, respCode='0000', respMsg='交易成功！', outSts='02', baselimit=200000)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2, "0_交易成功！_2_null_null", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_junxin_not_balance(self, case, app, source_type, period):
        """
        LoanApplyQuery失败（因授信额度不足，失败切换资金方）
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="24")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, respCode='0000', respMsg='交易成功！', outSts='04',
                                              baselimit=0)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2, "0_交易成功！_授信金额小于资产本金_4_null_null", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_junxin_confirm_fail(self, case, app, source_type, period):
        """
        LoanApplyConfirm 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:

        有问题
        """
        four_element = get_four_element(id_num_begin="32")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.capital_mock.update_confirm_apply(item_no, dnsts=300)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query(item_no, asset_info, dnsts='300', payMsg='放款失败')
        check_wait_change_capital_data(item_no, 3, "0000_交易成功！_300", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_junxin_confirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.capital_mock.update_confirm_apply(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query(item_no, asset_info, dnsts='300', payMsg='放款失败')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 3, "0000_交易成功！_300_放款失败",  "GrantFailedEvent")

    @pytest.mark.gbiz_certificate
    def test_changyin_junxin_certificate(self, case):
        '''
        该结清证明是申请之后，查询需要从我方的ftp上下载
        所以如果查询到是成功，就一定会返回结清证明文件的sftp路径（存在于下载调用接口的参数imgUrl中），这样我们才能下载到
        若测试的文件不存在了，可能这个case会失败，需要屏蔽掉
        '''
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        update_asset_due_bill_no(item_no)
        self.capital_mock.update_certificate_apply()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        self.capital_mock.update_certificate_download()
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_junxin_fail_assetvoid_rollback(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败切资方（授信查询授信拒绝),取消资产，取消任务回滚到切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element(id_num_begin="21")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, respCode='0000', respMsg='交易成功！', outSts='02',
                                              baselimit=200000)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 将所有资金方的金额修改为0，便于切换资金方任务切换失败，生成取消任务
        update_router_cp_amount_all_to_zero()
        update_task_by_item_no_task_type(item_no, "ChangeCapital", task_status="open")
        self.task.run_task(item_no, "ChangeCapital", excepts={"code": 1})
        # 通过接口调用job回滚任务
        run_job("manualTaskAutoProcessJob",
                {"taskTypeList": ["ChangeCapital", "AssetVoid", "CapitalAssetReverse", "BlacklistCollect"]})
        time.sleep(10)
        # 避免失败，再执行一次
        run_job("manualTaskAutoProcessJob",
                {"taskTypeList": ["ChangeCapital", "AssetVoid", "CapitalAssetReverse", "BlacklistCollect"]})
        # 恢复所有资金方的金额
        update_all_channel_amount()
        time.sleep(5)
        # 检查回滚生成的切换资金方任务参数并执行
        check_rollback_changecapital_data(item_no, 10000, "AssetVoid回滚到ChangeCapital自动执行",
                                          "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_junxin_applynew_fail_changecapital_to_assetvoid(self, case, app, source_type, period):
        """
         LoanApplyNew 失败切资方（授信申请失败）,切换资金方时直接被取消掉
        """
        four_element = get_four_element(id_num_begin="31")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_credit_apply(item_no, respCode='0001', respMsg='mock测试授信申请失败')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, respCode='0000', respMsg='交易成功！', outSts='02',
                                              baselimit=200000)
        # 通过接口调用job回滚任务
        run_job("manualTaskAutoProcessJob",
                {"taskTypeList": ["ChangeCapital", "AssetVoid"]})
        time.sleep(10)
        # 避免失败，再执行一次
        run_job("manualTaskAutoProcessJob",
                {"taskTypeList": ["ChangeCapital", "AssetVoid"]})
        # 检查生成的取消任务参数等
        check_wait_assetvoid_data(item_no, code=2, message="0001_mock测试授信申请失败")
