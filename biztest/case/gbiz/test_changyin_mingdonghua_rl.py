from biztest.function.contract.contract_check_function import check_contract
from biztest.interface.gbiz.gbiz_interface import *
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_changyin_mingdonghua_rl_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount, update_asset_due_bill_no
import pytest
from biztest.util.easymock.gbiz.changyin_mingdonghua_rl import ChangyinMingdonghuaRlMock
from biztest.util.tools.tools import get_four_element


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_changyin_mingdonghua_rl
class TestChangyinMingdonghuaRl(BaseTestCapital):
    def init(self):
        super(TestChangyinMingdonghuaRl, self).init()
        self.channel = "changyin_mingdonghua_rl"
        self.capital_mock = ChangyinMingdonghuaRlMock(gbiz_mock)
        update_gbiz_capital_changyin_mingdonghua_rl()
        update_gbiz_capital_changyin_mingdonghua_rl_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, four_element, item_no):
        self.capital_mock.update_card_query()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_card_sign()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_card_sign_check()
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
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_disbursement_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_disbursement_query(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayment_schedule_query(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=0)
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        #接口返回的是字节流不好mock
        self.capital_mock.update_image_download()
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.capital_mock.update_business_apply()
        # 担保文件上传
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_changyin_mingdonghua_rl_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [("香蕉", "apr36", 12),
                              # ("草莓", "irr36", 12),
                              ])
    def test_changyin_mingdonghua_rl_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(four_element, item_no)
        self.loan_to_success(item_no)
        # check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_mingdonghua_rl_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="62")
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
        check_wait_change_capital_data(item_no, 4, "changyin_mingdonghua_rl->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_mingdonghua_rl_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(status='F')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query_notorder()
        check_wait_change_capital_data(item_no, 10000, "0_Success_F", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_mingdonghua_rl_applyquery_fail(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, status='F', outRiskMsg="授信失败")
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10000, "0_Success_F_授信失败", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_mingdonghua_rl_not_balance(self, case, app, source_type, period):
        """
        授信额度不足，失败切换资金方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no, baseLimit=1000)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10000, "授信金额小于资产本金", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_mingdonghua_rl_confirm_fail(self, case, app, source_type, period):
        """
        LoanApplyConfirm 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:

        有问题
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_disbursement_apply(status='F')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_disbursement_query_fail()
        check_wait_change_capital_data(item_no, 20000, "0_Success_F", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_changyin_mingdonghua_rl_confirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(four_element, item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_disbursement_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_disbursement_query(item_no, status='F', payMsg='放款失败')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20000, "0_Success_F_放款失败",  "GrantFailedEvent")


    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_certificate
    def test_changyin_mingdonghua_rl_certificate(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        update_asset_due_bill_no(item_no)
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        self.capital_mock.update_loan_assis_cy_settlement_cert_apply()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        self.capital_mock.update_loan_assis_cy_settlement_cert_query()
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")