from biztest.function.gbiz.gbiz_db_function import update_router_capital_plan_amount
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.longjiang_daqin import LongjiangDaqinMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.function.gbiz.gbiz_common_function import prepare_attachment, fake_asset_data
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.function.contract.contract_check_function import check_contract


# @pytest.mark.gbiz_auto_test
# @pytest.mark.gbiz_longjiang_daqin
class TestLongjiangDaqin(BaseTestCapital):
    """
              gbiz_longjiang_daqin
              author: zhimengxue
              date: 20210615
              """

    def init(self):
        super(TestLongjiangDaqin, self).init()
        self.channel = "longjiang_daqin"
        self.dq_mock = LongjiangDaqinMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_longjiang_daqin()
        update_gbiz_capital_longjiang_daqin_const()
        update_gbiz_payment_config(self.payment_mock.url)

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel, four_element, item_no)

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.dq_mock.update_push_attachment_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.dq_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.dq_mock.update_applyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.dq_mock.update_push_attachment_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.dq_mock.update_comfirm_success(asset_info)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.dq_mock.update_comfirmquery_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.dq_mock.update_repayplan_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_longjiang_daqin_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 # ("草莓", "apr36", 12),
                                 ("香蕉", "irr36_quanyi", 12),
                                 # ("香蕉", "irr36_quanyi", 12),
                             ])
    def test_longjiang_daqin_loan_success(self, case, app, source_type, count):
        """
        放款成功
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 10000, app, source_type)

        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("count", [12])
    def test_longjiang_daqin_canloan_fail(self, case, count):
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
        check_wait_change_capital_data(item_no, 4, "longjiang_daqin->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("count", [12])
    def test_longjiang_daqin_apply_fail(self, case, count):
        """
        LoanApplyNew失败切换资金方
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
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.dq_mock.update_push_attachment_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.dq_mock.update_apply_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 提前修改切换资金方任务将要调用的接口为失败状态
        self.dq_mock.update_applyquery_not_exist()
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 1, "mock失败", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("count", [6])
    def test_longjiang_daqin_applyquery_fail(self, case, count):
        """
        LoanApplyQuery失败切换资金方(code!=0)
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
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.dq_mock.update_push_attachment_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.dq_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.dq_mock.update_applyquery_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 1, "mock测试失败", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("count", [6])
    def test_longjiang_daqin_applyquery_refused(self, case, count):
        """
        LoanApplyQuery失败切换资金方(code=0,status=refused)
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
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.dq_mock.update_push_attachment_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.dq_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.dq_mock.update_applyquery_refused(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 11, "风控审核拒绝", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("count", [12])
    def test_longjiang_daqin_applyconfirm_fail(self, case, count):
        """
        LoanApplyConfirm失败切换资金方
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
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.dq_mock.update_push_attachment_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.dq_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.dq_mock.update_applyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.dq_mock.update_push_attachment_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.dq_mock.update_comfirm_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        # 提前修改切换资金方任务将要调用的接口为失败状态
        self.dq_mock.update_applyquery_fail(asset_info)
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 1, "mock LoanApplyConfirm 失败", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("count", [6])
    def test_longjiang_daqin_confirmquery_fail(self, case, count):
        """
        LoanConfirmQuery失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000)
        self.register(item_no, four_element)

        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.dq_mock.update_push_attachment_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.dq_mock.update_apply_success(asset_info)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.dq_mock.update_applyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.dq_mock.update_push_attachment_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.dq_mock.update_comfirm_success(asset_info)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        # LoanApplyQuery和LoanConfirmQuery调用的同一个接口
        self.dq_mock.update_confirmquery_fail(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        # 提前修改切换资金方任务将要调用的接口为失败状态
        self.dq_mock.update_confirmquery_fail(asset_info)
        # 切资方任务生成
        check_wait_change_capital_data(item_no, 21, "放款失败", "GrantFailedEvent")

    @pytest.mark.gbiz_certificate
    def test_longjiang_daqin_certificate_success(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        self.dq_mock.update_certificate_apply_fail(item_no)
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 2})
        self.dq_mock.update_certificate_apply_success()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")

    @pytest.mark.gbiz_certificate
    def test_longjiang_daqin_certificate_exist(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        # 因为龙江大秦没有校验申请是否已经存在，可以重复申请，所以这里mock接口直接为成功即可
        self.dq_mock.update_certificate_apply_success()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")
