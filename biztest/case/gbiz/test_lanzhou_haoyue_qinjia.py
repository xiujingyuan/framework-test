from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.lanzhou_haoyue_qinjia import LanzhouHaoyueQinjiaMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.gbiz.gbiz_lanzhou_haoyue_qinjia_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_asset_due_bill_no, update_all_channel_amount
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.contract.contract_check_function import check_contract


class TestLanzhouHaoyueQinjia(BaseTestCapital):
    """
       gbiz_lanzhou_haoyue_qinjia
       author: zhimengxue
       date: 20220601
       """

    def init(self):
        super(TestLanzhouHaoyueQinjia, self).init()
        self.channel = "lanzhou_haoyue_qinjia"
        self.capital_mock = LanzhouHaoyueQinjiaMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_lanzhou_haoyue_qinjia()
        update_gbiz_capital_lanzhou_haoyue_qinjia_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()


    def register(self, item_no, four_element):
        self.payment_mock.query_protocol_channels_need_bind()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.payment_mock.auto_bind_sms_success()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='qjhy', step_type='PAYSVR_PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.payment_mock.bind_success(four_element)
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='qjhy', step_type='PAYSVR_PROTOCOL', seq=sms_seq)
        self.payment_mock.query_protocol_channels_need_bind(bind_status='1', protocol_info='T@id')
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanbaseinfo_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_upload_file()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_creditapplyquery_success(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_loanapplytrial_success()
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirmquery_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_queryrepayplan_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        #self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.msg.run_msg_by_order_no(item_no)
        self.capital_mock.update_repayplanpush_success()
        self.task.run_task(item_no, "CapitalRepayPlanPush", excepts={"code": 0})
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_lanzhou_haoyue_qinjia
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("香蕉", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                                 # ("重庆草莓", "irr36_quanyi", 12),
                                 # ("草莓", "apr36_huaya", 12),  # 花鸭只能草莓的进件
                             ])
    def test_lanzhou_haoyue_qinjia_loan_success(self, case, app, source_type, count):
        """
        放款成功,默认利率是7.20
        """
        four_element = get_four_element(id_num_begin="62")
        # ⬆️实际上资金方并不是只要甘肃的身份证号码进件，只是排除了部分地区，但为了避免失败，固定为甘肃地区身份证号

        item_no, asset_info = asset_import(self.channel, four_element, count, 13000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # check_asset_tran_data(item_no) -----会报错不支持acpi算法，先屏蔽
        # check_request_log_by_channel(item_no, self.channel)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)


    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_lanzhou_haoyue_qinjia
    # @pytest.mark.parametrize("count", [12])
    # def test_lanzhou_haoyue_qinjia_loan_success_other_rate(self, case, count):
    #     """
    #     放款成功，其他费率，此case就不进件小单，只检验费率是否正确即可
    #     """
    #     rates = [7.3, 7.4, 7.5]
    #     for rate in rates:
    #         four_element = get_four_element(id_num_begin="62")
    #         item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "香蕉", "irr36_quanyi")
    #         self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #         self.msg.run_msg(item_no, "AssetImportSync")
    #         self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #         self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #         prepare_attachment(self.channel, item_no)
    #         self.capital_mock.update_loanbaseinfo_push()
    #         self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
    #         # 空实现，不调用接口
    #         self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
    #         self.capital_mock.update_upload_file()
    #         self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
    #         self.capital_mock.update_creditapply_success()
    #         self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
    #         self.capital_mock.update_creditapplyquery_success(asset_info)
    #         self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
    #         self.capital_mock.update_loanapplytrial_other_rate_success(rate)
    #         self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
    #         self.capital_mock.update_loanapplyconfirm_success()
    #         self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
    #         self.capital_mock.update_loanapplyconfirmquery_other_rate_success(asset_info, rate)
    #         self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
    #         self.capital_mock.update_queryrepayplan_success(asset_info)
    #         self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
    #         # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
    #         self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
    #         self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
    #         self.msg.run_msg_by_order_no(item_no)
    #         self.capital_mock.update_repayplanpush_success()
    #         self.task.run_task(item_no, "CapitalRepayPlanPush", excepts={"code": 0})
    #         self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
    #         self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
    #         self.task.run_task(item_no, "RongDanIrrTrial")
    #         self.task.run_task(item_no, "CapitalDataNotify")
    #         self.task.run_task(item_no, "GrantSuccessNotify")
    #         self.msg.run_msg_by_order_no(item_no)
    #

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue_qinjia
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_qinjia_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element(id_num_begin="62")
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
        check_wait_change_capital_data(item_no, 4, "lanzhou_haoyue_qinjia->校验资金量失败;", "AssetCanLoanFailedEvent")


    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue_qinjia
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_qinjia_loancreditquery_fail(self, case, count):
        """
        授信查询失败切换资金方
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, 12, 6000)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanbaseinfo_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_upload_file()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_loancreditquery_fail()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 1000000, "02-9999-成功-测试mock")
        check_wait_blacklistcollect_data(item_no, asset_info, 1000000, "02-9999-成功-测试mock", "id_card")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue_qinjia
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_qinjia_loanconfirmquery_fail(self, case, count):
        """
        放款查询失败切换资金方
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, 12, 6000)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanbaseinfo_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_upload_file()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_creditapplyquery_success(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_loanapplytrial_success()
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirmquery_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 1000000, "02-0007-成功-此产品暂不支持当前利率")


    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue_qinjia
    @pytest.mark.gbiz_certificate
    def test_lanzhou_haoyue_qinjia_certificate(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        update_asset_due_bill_no(item_no)
        self.capital_mock.update_certificateapply_success()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        self.capital_mock.update_certificatedownload_success()
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")