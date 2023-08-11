from biztest.function.gbiz.gbiz_db_function import update_router_capital_plan_amount, update_task_by_item_no_task_type
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.huabei_runqian import HhabeirunqianMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.function.gbiz.gbiz_common_function import prepare_attachment
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element


# @pytest.mark.gbiz_auto_test
# @pytest.mark.gbiz_huabei_runqian
class TestHuabeiRunqian(BaseTestCapital):
    """
              gbiz_huabei_runqian
              author: zhimengxue
              date: 20210601
              """

    def init(self):
        super(TestHuabeiRunqian, self).init()
        self.channel = "huabei_runqian"
        self.hbrq_mock = HhabeirunqianMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_huabei_runqian()
        update_gbiz_capital_huabei_runqian_const()
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
        self.hbrq_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.hbrq_mock.update_audit_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.hbrq_mock.update_loan_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.hbrq_mock.update_repay_plan(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        # self.hbrq_mock.update_contract_success()
        # wait_biz_asset_appear(item_no)
        # self.hbrq_mock.update_repay_plan(asset_info)
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_huabei_runqian_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                                 # ("香蕉", "irr36_quanyi", 6),
                             ])
    def test_huabei_runqian_loan_success(self, case, app, source_type, count):
        """
        放款成功
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("count", [6])
    def test_huabei_runqian_apply_exist(self, case, count):
        """
        订单编号已存在
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 3000, "香蕉", "irr36_quanyi", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 订单编号已存在
        self.hbrq_mock.update_apply_exist()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.hbrq_mock.update_audit_success(asset_info)
        self.hbrq_mock.update_loan_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})

    @pytest.mark.parametrize("count", [12])
    def test_huabei_runqian_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "香蕉", "irr36_quanyi", '', '110000')
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
        check_wait_change_capital_data(item_no, 4, "huabei_runqian->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("count", [6])
    def test_huabei_runqian_apply_fail(self, case, count):
        """
        进件失败切资方（LoanApplyNew失败）
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "香蕉", "irr36_quanyi", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 进件失败
        self.hbrq_mock.update_apply_fail()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 方便切换资金方顺利切走，需提前将审核查询mock为失败
        self.hbrq_mock.update_audit_fail(asset_info)
        check_wait_change_capital_data(item_no, -1, "进件失败", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("count", [6])
    def test_huabei_runqian_audit_fail(self, case, count):
        """
        审核失败切资方（LoanApplyQuery失败）
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "香蕉", "irr36_quanyi", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.hbrq_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 待审核
        self.hbrq_mock.update_audit_wait()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 2})
        update_task_by_item_no_task_type(item_no, "LoanApplyQuery", task_status="open")
        # 审核失败
        self.hbrq_mock.update_audit_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10003, "审核失败", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("count", [6])
    def test_huabei_runqian_loan_fail(self, case, count):
        """
        放款失败切资方（LoanConfirmQuery失败）
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "香蕉", "apr36", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.hbrq_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 审核通过，待放款
        self.hbrq_mock.update_audit_success(asset_info)
        huabei_audit_callback(asset_info, "01")
        self.task.run_task(item_no, "CapitalCallback", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        # 放款失败
        self.hbrq_mock.update_loan_fail(asset_info)
        huabei_grant_callback(asset_info, "03")
        self.task.run_task(item_no, "CapitalCallback", excepts={"code": 0})
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 3, "放款失败", "GrantFailedEvent")
