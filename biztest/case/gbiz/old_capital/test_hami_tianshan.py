from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.function.gbiz.gbiz_db_function import update_router_capital_plan_amount
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.hami_tianshan import HamiTianShanMock
from biztest.util.easymock.gbiz.zhongji import ZhongjiMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import time
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.function.contract.contract_check_function import check_contract


class TestHamiTianshan(BaseTestCapital):
    """
       gbiz_hami_tianshan
       author: zhimengxue
       date: 20200609
       """

    def init(self):
        super(TestHamiTianshan, self).init()
        self.channel_hami = "hami_tianshan"
        self.channel_zhongji = "zhongji"
        self.hami_mock = HamiTianShanMock(gbiz_mock)
        self.zhongji_mock = ZhongjiMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        # update_hami_tianshan_paydayloan()
        # update_zhongji_paydayloan()
        # update_gbiz_payment_config(self.payment_mock.url)
        # update_grouter_hami_tianshan_paydayloan()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel_hami, four_element, item_no)

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel_hami, item_no)
        self.hami_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.hami_mock.update_applyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.hami_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.zhongji_mock.update_guaranteeapply_success()
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        self.zhongji_mock.update_guaranteeapplyquery_success()
        self.task.run_task(item_no, "GuaranteeApplyQuery", excepts={"code": 0})
        self.zhongji_mock.update_guaranteeupload_success()
        self.task.run_task(item_no, "GuaranteeUpload", excepts={"code": 0})
        # 哈密中吉回调，但是不会生成异步任务，只会生成同步任务，这个回调会触发生成下一个任务：GuaranteeDown
        hamitianshan_zhongji_callback(asset_info)
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "GuaranteeDown", excepts={"code": 0})
        self.hami_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.hami_mock.update_loanconfirmquery_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.hami_mock.update_capitalrepayplanquery_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.zhongji_mock.update_guaranteestatussync_success()
        self.task.run_task(item_no, "GuaranteeStatusSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_hami_tianshan
    @pytest.mark.parametrize("count", [12])
    def test_hami_tianshan_loan_success(self, case, count):
        """
        放款成功
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel_hami, four_element, count, 8000, "香蕉", "", '', '110000')

        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
        self.noloan_to_success(item_no_noloan)

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_hami_tianshan
    @pytest.mark.parametrize("count", [12])
    def test_hami_tianshan_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel_hami, four_element, count, 8000, "香蕉", "", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        # canloan失败准备工作
        today = time.strftime("%Y-%m-%d", time.localtime())
        # amount = select_router_capital_plan_amount(today)[0]["router_capital_plan_amount"]
        update_router_capital_plan_amount(0, today, self.channel_hami)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # canloan执行之后恢复
        update_router_capital_plan_amount(3333333333, today, self.channel_hami)
        check_wait_change_capital_data(item_no, 4, "hami_tianshan->校验资金量失败;")

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_hami_tianshan
    @pytest.mark.parametrize("count", [12])
    def test_hami_tianshan_apply_fail(self, case, count):
        """
        进件查询失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel_hami, four_element, count, 8000, "香蕉", "", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel_hami, item_no)
        self.hami_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 进件查询失败
        self.hami_mock.update_applyquery_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "GuaranteeApplyRevoke", excepts={"code": 1})
        check_wait_change_capital_data(item_no, 10002, "交易成功")

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_hami_tianshan
    @pytest.mark.parametrize("count", [12])
    def test_hami_tianshan_guarantee_fail(self, case, count):
        """
        担保失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel_hami, four_element, count, 8000, "香蕉", "", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel_hami, item_no)
        self.hami_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.hami_mock.update_applyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.hami_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.zhongji_mock.update_guaranteeapply_success()
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        self.zhongji_mock.update_guaranteeapplyquery_fail()
        self.task.run_task(item_no, "GuaranteeApplyQuery", excepts={"code": 1})
        check_wait_change_capital_data(item_no, 1, "审批拒绝")

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_hami_tianshan
    @pytest.mark.parametrize("count", [12])
    def test_hami_tianshan_loan_fail(self, case, count):
        """
        放款失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel_hami, four_element, count, 8000, "香蕉", "", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel_hami, item_no)
        self.hami_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.hami_mock.update_applyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.hami_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.zhongji_mock.update_guaranteeapply_success()
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        self.zhongji_mock.update_guaranteeapplyquery_success()
        self.task.run_task(item_no, "GuaranteeApplyQuery", excepts={"code": 0})
        self.zhongji_mock.update_guaranteeupload_success()
        self.task.run_task(item_no, "GuaranteeUpload", excepts={"code": 0})
        # 哈密中吉回调，但是不会生成异步任务，只会生成同步任务，这个回调会触发生成下一个任务：GuaranteeDown
        hamitianshan_zhongji_callback(asset_info)
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "GuaranteeDown", excepts={"code": 0})
        self.hami_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.hami_mock.update_loanconfirmquery_fail(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.zhongji_mock.update_guaranteeapplyrevoke_success()
        self.task.run_task(item_no, "GuaranteeApplyRevoke", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2, "交易成功")

    @pytest.mark.gbiz_hami_tianshan
    @pytest.mark.gbiz_certificate
    def test_hami_tianshan_certificate(self, case):
        item_no = fake_asset_data(self.channel_hami, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel_hami, "CERTIFICATE_GENERATE_EVENT")
        self.hami_mock.update_postapply_success()
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")
