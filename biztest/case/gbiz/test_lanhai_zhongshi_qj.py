from biztest.interface.gbiz.gbiz_interface import *
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import
from biztest.util.easymock.gbiz.lanhai_zhongshi_qj import LanhaiZhongshiQjMock
from biztest.function.gbiz.gbiz_check_function import check_wait_change_capital_data,\
    check_wait_blacklistcollect_data, check_asset_event_exist, check_asset_tran_valid_status
from biztest.config.gbiz.gbiz_lanhai_zhongshi_qj_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment, fake_asset_data
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount, \
    update_router_capital_plan_amount, update_asset_due_bill_no
import pytest
from biztest.util.tools.tools import get_four_element

@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_lanhai_zhongshi_qj
class TestLanhaiZhongshiQj(BaseTestCapital):
    def init(self):
        super(TestLanhaiZhongshiQj, self).init()
        self.channel = "lanhai_zhongshi_qj"
        self.capital_mock = LanhaiZhongshiQjMock(gbiz_mock)
        update_gbiz_capital_lanhai_zhongshi_qj()
        update_gbiz_capital_lanhai_zhongshi_qj_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_get_sms_success()
        self.capital_mock.update_checkcmsverifycode_success()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_checkcmsverifycode_success()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        time.sleep(5)
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_info_push_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZSQJ_IMAGE_FILE_PUSHED")
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZSQJ_LOAN_ROUTER_SUCCESS")
        self.capital_mock.update_credit_query_success_old_user()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_create_success()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        self.capital_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 2})
        check_asset_event_exist(item_no, self.channel, "LHZSQJ_LOAN_CONTRACT_PUSHED")
        self.capital_mock.update_contractpush_query_success()
        # 因为这个任务会分别调用两个接口，会执行两次。故此处写了两个这个任务
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_success(asset_info, item_no)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        #self.task.run_task(item_no, "ContractDown")
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)


    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_lanhai_zhongshi_qj_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [("香蕉", "apr36", 12),
                              # ("草莓", "irr36", 12),
                              ])
    def test_lanhai_zhongshi_qj_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 8000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        #check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongshi_qj_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
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
        update_router_capital_plan_amount(10000000000, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "lanhai_zhongshi_qj->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongshi_qj_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_info_push_fail()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create_fail()
        check_wait_change_capital_data(item_no, 1000000, "02-0000-mock失败-sendmsg失败", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongshi_qj_route_fail(self, case, app, source_type, period):
        """
        LoanCreditApply 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="33")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_info_push_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_fail()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 1})
        self.capital_mock.update_credit_query_fail()
        check_wait_change_capital_data(item_no, 1000000, "02-9999-mock失败-路由mock失败", "LoanCreditApplySyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 1000000, "02-9999-mock失败-路由mock失败", "id_card")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongshi_qj_route_query_fail_01(self, case, app, source_type, period):
        """
            LoanCreditQuery 授信金额不足失败切资方
            :param app:
            :param source_type:
            :param period:
            :return:
        """
        four_element = get_four_element(id_num_begin="25")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_info_push_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_success_old_user(creditamt='0.00', enddate='2036-12-12')
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9000, "当前资产待放金额\\[600000\\]大于查询返回授信成功金额\\[0\\]", "LoanCreditFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 9000, "当前资产待放金额\\[600000\\]大于查询返回授信成功金额\\[0\\]", "id_card")

    #
    # @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    # def test_lanhai_zhongshi_qj_route_query_fail_02(self, case, app, source_type, period):
    #     """
    #         LoanCreditQuery 授信日期失效失败切资方
    #         :param app:
    #         :param source_type:
    #         :param period:
    #         :return:
    #     """
    #     four_element = get_four_element(id_num_begin="52")
    #     item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
    #     self.register(item_no, four_element)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.capital_mock.update_info_push_success()
    #     self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
    #     self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
    #     prepare_attachment(self.channel, item_no)
    #     self.capital_mock.update_postapply_success()
    #     self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
    #     self.capital_mock.update_creditapply_success()
    #     self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
    #     self.capital_mock.update_credit_query_success_old_user(creditamt='20000.00', enddate='2021-12-12')
    #     self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 1000000, "03-mock请求失败", "LoanApplyAsyncFailedEvent")
    #     check_wait_blacklistcollect_data(item_no, asset_info, 1000000, "03-mock请求失败", "id_card")


    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_lanhai_zhongshi_qj_route_query_fail_03(self, case, app, source_type, period):
        """
            LoanCreditQuery 授信失败切资方
            :param app:
            :param source_type:
            :param period:
            :return:
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_info_push_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_fail()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1000000, "02-0004-mock授信失败-", "LoanCreditFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 1000000, "02-0004-mock授信失败-", "id_card")


    @pytest.mark.parametrize("app, source_type, period", [("草莓", "irr36", 12)])
    def test_lanhai_zhongshi_qj_confirm_fail(self, case, app, source_type, period):
        """
            LoanApplyConfirm 失败切资方
            :param app:
            :param source_type:
            :param period:
            :return:
        """
        four_element = get_four_element(id_num_begin="42")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_info_push_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_success_old_user()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_create_success()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        self.capital_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 2})
        self.capital_mock.update_contractpush_query_success()
        # 因为这个任务会分别调用两个接口，会执行两次。故此处写了两个这个任务
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_fail()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery_fail()
        check_wait_change_capital_data(item_no, 1000000, "02-1002-mock失败-", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("草莓", "irr36", 12)])
    def test_lanhai_zhongshi_qj_confirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery 失败切资方
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_info_push_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_query_success_old_user()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_create_success()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        self.capital_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 2})
        self.capital_mock.update_contractpush_query_success()
        # 因为这个任务会分别调用两个接口，会执行两次。故此处写了两个这个任务
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1000000, "02-1001-mock失败-", "GrantFailedEvent")


    @pytest.mark.gbiz_certificate
    def test_lanhai_zhongshi_qj_certificate(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        update_asset_due_bill_no(item_no)
        self.capital_mock.update_certificate_apply()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        # self.capital_mock.update_certificate_download()
        # self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        # check_contract(item_no, "ContractDownload", [24])
        # check_sendmsg_exist(item_no, "CertificateSuccessNotify")
