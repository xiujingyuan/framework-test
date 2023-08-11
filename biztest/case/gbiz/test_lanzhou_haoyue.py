from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.lanzhou_haoyue import LanzhouHaoyueMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.gbiz.gbiz_lanzhou_haoyue_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount, update_router_cp_amount_all_to_zero, \
    update_asset_due_bill_no
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


class TestLanzhouHaoyue(BaseTestCapital):
    """
       gbiz_lanzhou_haoyue
       author: zhimengxue
       date: 20210824
       """

    def init(self):
        super(TestLanzhouHaoyue, self).init()
        self.channel = "lanzhou_haoyue"
        self.capital_mock = LanzhouHaoyueMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_lanzhou_haoyue()
        update_gbiz_capital_lanzhou_haoyue_const()
        # 修改回滚策略配置，回滚Case会用到
        update_gbiz_manual_task_auto_process_config()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel, four_element, item_no, way='tq')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_creditapplyquery_success(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_creditapplyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repay_plan(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.capital_mock.update_contract_signature()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.gbiz_lanzhou_haoyue_loan_success
    @pytest.mark.parametrize("app, source_type, count, product_code",
                             [
                                 # ("香蕉", "apr36", 6, "gansu"),
                                 # ("草莓", "irr36", 6, "not_gansu"),
                                 # ("草莓", "apr36", 12, "not_gansu"),
                                 # ("草莓", "irr36", 12, "gansu"),
                                 # ("重庆草莓", "irr36_quanyi", 12, "not_gansu"),
                                 # ("草莓", "irr36", 12, "zk2"),
                                 ("香蕉", "apr36", 12, "zk2"),
                             ])
    def test_lanzhou_haoyue_loan_success(self, case, app, source_type, count, product_code):
        """
        放款成功，默认7.5%
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, app, source_type, product_code=product_code)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # check_request_log_by_channel(item_no, self.channel)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_loan_success_other_rate(self, case, count):
        """
        放款成功，其他费率，此case就不进件小单，只检验费率是否正确即可
        """
        rates = [7.45, 7.4, 7.3]
        for rate in rates:
            four_element = get_four_element()
            item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "香蕉", "apr36")
            self.register(item_no, four_element)
            self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
            self.msg.run_msg(item_no, "AssetImportSync")
            self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
            self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
            prepare_attachment(self.channel, item_no)
            self.capital_mock.update_file_notice()
            self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
            self.capital_mock.update_customer_info_push()
            self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
            self.capital_mock.update_customer_face_query_success()
            self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
            self.capital_mock.update_file_notice()
            self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
            self.capital_mock.update_creditapply_success()
            self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
            self.capital_mock.update_creditapplyquery_success_other_rate(asset_info, rate)
            self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
            self.capital_mock.update_creditapplyquery_success_other_rate(asset_info, rate)
            self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
            self.capital_mock.update_file_notice()
            self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
            self.capital_mock.update_loan_apply()
            self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
            self.capital_mock.update_loan_query_success_other_rate(asset_info, rate)
            self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
            self.capital_mock.update_repay_plan(asset_info)
            self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
            self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
            self.task.run_task(item_no, "RongDanIrrTrial")
            self.task.run_task(item_no, "CapitalDataNotify")
            self.task.run_task(item_no, "GrantSuccessNotify")
            self.msg.run_msg_by_order_no(item_no)
            check_asset_tran_data(item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "香蕉", "irr36")
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
        check_wait_change_capital_data(item_no, 4, "lanzhou_haoyue->校验资金量失败;")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_loanapplynew_fail(self, case, count):
        """
        LoanApplyNew失败切换资金方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 10000, "香蕉", "apr36")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push_fail()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 9000, "交易接收失败")


    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_loanapplyquery_fail(self, case, count):
        """
        LoanApplyQuery失败切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "草莓", "irr36")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 1900002, "客户信息推送-处理失败")


    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_loancreditapply_fail(self,case,count):
        '''
        LoanCreditApply 同步授信失败，成功切资方
        :return:
        '''
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "香蕉", "apr36")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_fail()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 1})
        self.capital_mock.update_creditapplyquery_no_order()
        check_wait_change_capital_data(item_no, 9000, "有未使用授信，不可重复授信")



    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_loancreditquery_fail(self, case, count):
        """
        LoanCreditQuery失败切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "香蕉", "apr36")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_creditapplyquery_fail()
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 2999903, "授信申请-mock-测试失败")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.test_lanzhou_haoyue_loan_fail
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_loan_fail(self, case, count):
        """
        放款支用失败切资方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "香蕉", "apr36")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_customer_info_push()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_customer_face_query_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_creditapply_success()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_creditapplyquery_success(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_creditapplyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})

        check_wait_change_capital_data(item_no, 3999909, "贷款支用查询-交易处理成功")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.parametrize("count", [12])
    def test_lanzhou_haoyue_loanapplyquery_fail_assetvoid_rollback(self, case, count):
        """
        客户信息推送失败切资方,取消资产,取消任务回滚到切换资金方
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "草莓", "apr36")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
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

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_lanzhou_haoyue
    @pytest.mark.gbiz_certificate
    def test_lanzhou_haoyue_certificate(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        update_asset_due_bill_no(item_no)
        self.capital_mock.update_certificate_apply()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        # self.capital_mock.update_certificate_down()
        # # 调用接口之后需要去FTP上下载，FTP无法mock生成，此处屏蔽
        # self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        # check_contract(item_no, "ContractDownload", [24])
        # check_sendmsg_exist(item_no, "CertificateSuccessNotify")
