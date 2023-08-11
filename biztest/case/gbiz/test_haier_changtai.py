from biztest.interface.gbiz.gbiz_interface import *
from biztest.config.gbiz.gbiz_kv_config import update_gbiz_payment_config
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import
from biztest.util.easymock.gbiz.haier_changtai import HaierChangtaiMock
from biztest.function.gbiz.gbiz_check_function import check_wait_change_capital_data, check_asset_tran_valid_status,\
    check_wait_blacklistcollect_data, check_asset_event_exist
from biztest.config.gbiz.gbiz_haier_changtai_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount,\
    update_router_capital_plan_amount
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_haier_changtai
class TestHaierChangtai(BaseTestCapital):
    def init(self):
        super(TestHaierChangtai, self).init()
        self.channel = "haier_changtai"
        self.capital_mock = HaierChangtaiMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_haier_changtai()
        update_gbiz_capital_haier_changtai_const()
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
        four_element = get_four_element(id_num_begin="36")
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_preapply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要上传身份证正反面/活体照，合同：35700、35701、35702、35703、35704、35705
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "HECT_POST_APPLY")
        self.capital_mock.update_loanconfirm_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_query()
        self.capital_mock.update_repayplan_query_tmp(asset_info)  # 因为放款查询接口没有返回放款成功的时间，所以此处需要调用还款计划接口获取放款成功时间
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
                                 ("草莓", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                             ])
    def test_haier_changtai_loan_success(self, case, app, source_type, count):
        """
        放款成功
        """
        four_element = get_four_element(bank_name='建设银行', id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, count, 13000, app, source_type)
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
    def test_haier_changtai_conloan_fail(self, case, app, source_type, count):
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
        check_wait_change_capital_data(item_no, 4, "haier_changtai->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_haier_changtai_preapply_fail(self, case, app, source_type, count):
        """
        LoanPreApply失败切资方
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_preapply(code='00000', message='处理成功', rtnCode='00001', rtnMsg='mock内层失败')
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10000, "00000_处理成功_00001_mock内层失败_null_nul", 'LoanPreApplySyncFailedEvent')

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_haier_changtai_applyconfirm_fail(self, case, app, source_type, count):
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
        self.capital_mock.update_loan_preapply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 需要上传身份证正反面/活体照，合同：35700、35701、35702、35703、35704、35705
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_apply(code='00000', message='处理成功', status='-1', msg2='mock支用申请失败',
                                                   code2="LA333")
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_query(code='00001', message='mock外层失败', status='1')
        check_wait_change_capital_data(item_no, 20000, "00000_处理成功_-1_LA333_mock支用申请失败", 'ConfirmApplySyncFailedEvent')

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_haier_changtai_confirmquery_fail(self, case, app, source_type, count):
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
        self.capital_mock.update_loan_preapply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 需要上传身份证正反面/活体照，合同：35700、35701、35702、35703、35704、35705
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_query(code='00000', message='处理成功', status='-1', msg2='mock支用查询失败',
                                                   code2='LA666')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20000, "00000_处理成功_-1_LA666_mock支用查询失败", 'GrantFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 20000, "00000_处理成功_-1_LA666_mock支用查询失败", "id_card")
