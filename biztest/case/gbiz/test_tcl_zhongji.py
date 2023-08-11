from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.tcl_zhongji import TclZhongjiMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.gbiz.gbiz_tcl_zhongji_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


class TestTclZhongji(BaseTestCapital):


    def init(self):
        super(TestTclZhongji, self).init()
        self.channel = "tcl_zhongji"
        self.capital_mock = TclZhongjiMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_tcl_zhongji_const()
        update_gbiz_capital_tcl_zhongji()
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
        self.capital_mock.update_creditapply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditapply_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_apply(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query(item_no, asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        prepare_attachment(self.channel, item_no)
        # self.capital_mock.update_contract_down()
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        # self.capital_mock.update_contract_push()
        # self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_tcl_zhongji
    @pytest.mark.gbiz_tcl_zhongji_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_tcl_zhongji_loan_success(self, case, app, source_type, count):
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, count, 10000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # check_asset_tran_data(item_no)
        # check_request_log_by_channel(item_no, self.channel)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tcl_zhongji
    @pytest.mark.parametrize("count", [12])
    def test_tcl_zhongji_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "香蕉", "apr36")
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
        check_wait_change_capital_data(item_no, 4, "tcl_zhongji->校验资金量失败;")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tcl_zhongji
    @pytest.mark.parametrize("count", [12])
    def test_tcl_zhongji_loanapply_new_fail(self, case, count):
        """
        LoanApplyNew失败切换资金方
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, count, 10000, "香蕉", "apr36")

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_creditapply(item_no, retCode='000000', status='02')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_no_order()
        check_wait_change_capital_data(item_no, 1000000, "000000-成功-02")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tcl_zhongji
    @pytest.mark.parametrize("count", [12])
    def test_tcl_zhongji_loanapply_query_fail(self, case, count):
        """
        LoanApplyQuery失败切资方
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "草莓", "apr36")
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_creditapply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditapply_query(item_no, retCode='000000', status='02')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1000000, "000000-02-null-成功")
        check_wait_blacklistcollect_data(item_no, asset_info, 1000000, "000000-02-null-成功","id_card")



    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tcl_zhongji
    @pytest.mark.parametrize("count", [12])
    def test_tcl_zhongji_loan_fail(self, case, count):
        """
        放款支用失败切资方
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, "香蕉", "apr36")
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_creditapply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditapply_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_apply(item_no, retCode='000000', status=4)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_no_order()
        check_wait_change_capital_data(item_no, 2000000, "000000-4-null-成功")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_tcl_zhongji
    @pytest.mark.parametrize("count", [12])
    def test_tcl_zhongji_loan_query_fail(self, case, count):
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "草莓", "apr36")
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_creditapply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_creditapply_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_apply(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query(item_no, asset_info, retCode='000000', status=4)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2000000, "成功-4-null")

