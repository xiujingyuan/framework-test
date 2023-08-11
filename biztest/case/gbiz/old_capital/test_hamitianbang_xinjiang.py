from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.function.gbiz.gbiz_db_function import update_router_capital_plan_amount, update_all_channel_amount, \
    update_router_cp_amount_all_to_zero, update_task_by_item_no_task_type
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.hami_tianshan import HamiTianShanMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment, fake_asset_data
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import time
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.function.contract.contract_check_function import check_contract


class TestHamitianbangXinjiang(BaseTestCapital):
    """
       gbiz_hamitianbang_xinjiang
       author: zhimengxue
       date: 20210630
       """

    def init(self):
        super(TestHamitianbangXinjiang, self).init()
        self.channel_hami_xinjiang = "hamitianbang_xinjiang"
        self.hami_mock = HamiTianShanMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_hamitianbang_xinjiang()
        update_gbiz_capital_hami_tianbang_const()
        update_gbiz_payment_config(self.payment_mock.url)
        # 修改回滚策略配置，回滚Case会用到
        update_gbiz_manual_task_auto_process_config()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.payment_register(self.payment_mock, self.channel_hami_xinjiang, four_element, item_no)

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel_hami_xinjiang, item_no)
        self.hami_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.hami_mock.update_applyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.hami_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.hami_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.hami_mock.update_loanconfirmquery_success(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.hami_mock.update_capitalrepayplanquery_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_hamitianbang_xinjiang
    @pytest.mark.gbiz_hamitianbang_xinjiang_loan_success
    @pytest.mark.parametrize("app, source_type, count,product_code",
                             [
                                 ("草莓", "apr36", 12, ""),
                                 ("香蕉", "irr36_quanyi", 6, "hmtlf")
                             ])
    def test_hamitianbang_xinjiang_loan_success(self, case, app, source_type, count, product_code):
        """
        放款成功
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element(id_num_begin="6522")
        item_no, asset_info = asset_import(self.channel_hami_xinjiang, four_element, count, 8000, app, source_type, '',
                                           '110000',product_code=product_code)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 因为用的接口和哈密天邦一样的，所以这里检查channel先写的天邦
        # check_request_log_by_channel(item_no, "hami_tianshan_tianbang")
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_hamitianbang_xinjiang
    @pytest.mark.parametrize("count,product_code", [(6, "hmtlf")])
    def test_hamitianbang_xinjiang_canloan_fail(self, case, count, product_code):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element(id_num_begin="6522")
        item_no, asset_info = asset_import(self.channel_hami_xinjiang, four_element, count, 8000, "香蕉", "apr36", '',
                                           '110000', product_code=product_code)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        # canloan失败准备工作
        today = time.strftime("%Y-%m-%d", time.localtime())
        update_router_capital_plan_amount(0, today, self.channel_hami_xinjiang)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        # canloan执行之后恢复
        update_router_capital_plan_amount(3333333333, today, self.channel_hami_xinjiang)
        check_wait_change_capital_data(item_no, 4, "hamitianbang_xinjiang->校验资金量失败;", "AssetCanLoanFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_hamitianbang_xinjiang
    @pytest.mark.parametrize("count,product_code", [(6, "hmtlf")])
    def test_hamitianbang_xinjiang_apply_fail(self, case, count,product_code):
        """
        进件查询失败切换资金方，LoanApplyQuery失败
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element(id_num_begin="6522")
        item_no, asset_info = asset_import(self.channel_hami_xinjiang, four_element, count, 8000, "香蕉", "apr36", '',
                                           '110000', product_code=product_code)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel_hami_xinjiang, item_no)
        self.hami_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 进件查询失败
        self.hami_mock.update_applyquery_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10002, "交易成功", "LoanApplyAsyncFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, code=10002, message="交易成功")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_hamitianbang_xinjiang
    @pytest.mark.parametrize("count,product_code", [(6, "hmtlf")])
    def test_hamitianbang_xinjiang_apply_fail_assetvoid_rollback(self, case, count, product_code):
        """
        进件查询失败切换资金方,取消资产，取消任务回滚到切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element(id_num_begin="6522")
        item_no, asset_info = asset_import(self.channel_hami_xinjiang, four_element, count, 8000, "香蕉", "apr36", '',
                                           '110000', product_code=product_code)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel_hami_xinjiang, item_no)
        self.hami_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 进件查询失败
        self.hami_mock.update_applyquery_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 将所有资金方的金额修改为0，便于切换资金方任务切换失败，生成取消任务
        update_router_cp_amount_all_to_zero()
        update_task_by_item_no_task_type(item_no, "ChangeCapital", task_status="open")
        self.task.run_task(item_no, "ChangeCapital", excepts={"code": 1})
        check_wait_blacklistcollect_data(item_no, asset_info, code=10002, message="交易成功")
        # 通过接口调用job回滚任务
        run_job("manualTaskAutoProcessJob",
                {"taskTypeList": ["ChangeCapital", "AssetVoid", "CapitalAssetReverse", "BlacklistCollect"]})
        time.sleep(5)
        # 恢复所有资金方的金额
        update_all_channel_amount()
        # 检查回滚生成的切换资金方任务参数并执行
        check_rollback_changecapital_data(item_no, 10000, "AssetVoid回滚到ChangeCapital自动执行", "LoanApplyAsyncFailedEvent")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_hamitianbang_xinjiang
    @pytest.mark.parametrize("count,product_code", [(6, "hmtlf")])
    def test_hamitianbang_xinjiang_loan_fail(self, case, count, product_code):
        """
        放款失败切资方，LoanConfirmQuery失败
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element(id_num_begin="6522")
        item_no, asset_info = asset_import(self.channel_hami_xinjiang, four_element, count, 8000, "香蕉", "apr36", '',
                                           '110000', product_code=product_code)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel_hami_xinjiang, item_no)
        self.hami_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.hami_mock.update_applyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.hami_mock.update_postapply_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.hami_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.hami_mock.update_loanconfirmquery_fail(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2, "交易成功", "GrantFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, code=2, message="交易成功")

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_hamitianbang_xinjiang
    @pytest.mark.gbiz_certificate
    def test_hamitianbang_xinjiang_certificate(self, case):
        item_no = fake_asset_data(self.channel_hami_xinjiang, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel_hami_xinjiang, "CERTIFICATE_GENERATE_EVENT")
        self.hami_mock.update_postapply_success()
        self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        check_contract(item_no, "ContractDownload", [24])
        check_sendmsg_exist(item_no, "CertificateSuccessNotify")
