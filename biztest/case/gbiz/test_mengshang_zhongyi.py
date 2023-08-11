from biztest.interface.gbiz.gbiz_interface import *
from biztest.config.gbiz.gbiz_kv_config import update_gbiz_payment_config
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import
from biztest.util.easymock.gbiz.mengshang_zhongyi import MengShangZhongYiMock
from biztest.function.gbiz.gbiz_check_function import check_wait_change_capital_data, check_asset_tran_valid_status,\
    check_wait_blacklistcollect_data
from biztest.config.gbiz.gbiz_mengshang_zhongyi_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount,\
    update_router_capital_plan_amount
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock



@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_mengshang_zhongyi
class TestMengshangZhongyi(BaseTestCapital):
    def init(self):
        super(TestMengshangZhongyi, self).init()
        self.channel = "mengshang_zhongyi"
        self.capital_mock = MengShangZhongYiMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_mengshang_zhongyi()
        update_gbiz_capital_mengshang_zhongyi_const()
        update_all_channel_amount()


    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        """
        开户类似众邦中际的开户，都是走paysvr开户，需要指定通道并且需要协议号
        所以此处copy的是众邦开户
        """
        # 提前修改签约通道为未签约，避免开户绑卡报错
        self.payment_mock.query_protocol_channels_need_bind_for_zhongbang_zhongji()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='tq', step_type='PAYSVR_PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.payment_mock.bind_success(four_element)
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='tq', step_type='PAYSVR_PROTOCOL', seq=sms_seq)
        self.payment_mock.query_protocol_channels_get_protocol_info()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 上传文件到FTP,需要上传合同：37000\37001\37002\37003
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply_get_route()
        self.capital_mock.update_loan_apply_new()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要上传合同37004、37009
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_query(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        # 去资方ftp下载
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("香蕉", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                             ])
    def test_mengshang_zhongyi_loan_success(self, case, app, source_type, count):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, count, 10000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_mengshang_zhongyi_conloan_fail(self, case, app, source_type, count):
        """
        canloan fail
        :return:
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, app, source_type)
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
        check_wait_change_capital_data(item_no, 4, "mengshang_zhongyi->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_mengshang_zhongyi_not_open_account_conloan_fail(self, case, app, source_type, count):
        """
        canloan fail（未开户）
        :return:
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, count, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 4,
                                       "mengshang_zhongyi->资金路由系统校验失败: 校验用户账户状态必须为成功:;",
                                       "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_mengshang_zhongyi_applynew_fail(self, case, app, source_type, count):
        """
        授信申请失败切资方
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 上传文件到FTP,需要上传合同：37000\37001\37002\37003
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply_get_route()
        self.capital_mock.update_loan_apply_new(code=0, message='mock借款审核失败', respcd='0001', resptx='MOCK的申请借款审核失败',
                                                bus_number='')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 切换资金方任务会调用这个接口，所以此处要mock为失败才可以
        self.capital_mock.update_loan_apply_query(code=0, message='test失败', respcd='9999', resptx='MOCK审核查询失败')
        check_wait_change_capital_data(item_no, 10001, "MOCK的申请借款审核失败", 'LoanApplySyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 10001, "MOCK的申请借款审核失败", "id_card")


    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_mengshang_zhongyi_applynew_fail_01(self, case, app, source_type, count):
        """
        授信申请失败(进件路由接口调用失败)
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 上传文件到FTP,需要上传合同：37000\37001\37002\37003
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply_get_route(code=0, message='test失败', respcd='0003', resptx='mock进件路由失败')
        self.capital_mock.update_loan_apply_new()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query(code=0, message='test失败', respcd='9999', resptx='MOCK审核查询失败')
        check_wait_change_capital_data(item_no, 10003, "mock进件路由失败", 'LoanApplySyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 10003, "mock进件路由失败", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_mengshang_zhongyi_applyquery_fail(self, case, app, source_type, count):
        """
        授信查询失败切资方
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 上传文件到FTP,需要上传合同：37000\37001\37002\37003
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply_get_route()
        self.capital_mock.update_loan_apply_new()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query(code=111, message='mock借款审核查询外层失败', respcd='0000', resptx='MOCK外层失败')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10000, "0000-MOCK外层失败", 'LoanApplyAsyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 10000, "0000-MOCK外层失败", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_mengshang_zhongyi_applyconfirm_fail(self, case, app, source_type, count):
        """
        申请借款失败切资方
        """
        four_element = get_four_element(id_num_begin="44")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 上传文件到FTP,需要上传合同：37000\37001\37002\37003
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply_get_route()
        self.capital_mock.update_loan_apply_new()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要上传合同37004、37009
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_apply(code=0, message='test失败', respcd='0700', resptx='Mock失败测试')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query(code=1, message='test失败', respcd='0000', resptx='Mock外层放款失败测试')
        check_wait_change_capital_data(item_no, 20700, "0700-Mock失败测试", 'ConfirmApplySyncFailedEvent')

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_mengshang_zhongyi_confirmquery_fail(self, case, app, source_type, count):
        """
        放款查询失败切资方
        """
        four_element = get_four_element(id_num_begin="52")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 上传文件到FTP,需要上传合同：37000\37001\37002\37003
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply_get_route()
        self.capital_mock.update_loan_apply_new()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要上传合同37004、37009
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_query(code=0, message='test失败', respcd='0008', resptx='Mock内层code放款失败测试')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20008, "0008-Mock内层code放款失败测试", 'GrantFailedEvent')
