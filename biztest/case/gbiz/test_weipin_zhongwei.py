from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.weipin_zhongwei import WeipinZhongweiMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_weipin_zhongwei_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_router_capital_plan_amount, \
    update_all_channel_amount
import pytest
from biztest.util.tools.tools import get_four_element

class TestWeipinZhongwei(BaseTestCapital):

    def init(self):
        super(TestWeipinZhongwei, self).init()
        self.channel = "weipin_zhongwei"
        self.wpzw = WeipinZhongweiMock(gbiz_mock)
        update_gbiz_capital_weipin_zhongwei()
        update_gbiz_capital_weipin_zhongwei_const()
        update_all_channel_amount()

    def setup(self):
        self.init()

    def teardown(self):
        update_gbiz_capital_weipin_zhongwei()
        update_all_channel_amount()

    def register(self, item_no, four_element):
        self.wpzw.update_card_pre_binding()
        self.wpzw.update_card_binding()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.wpzw.update_account_open()
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.wpzw.update_image_upload(item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.wpzw.update_credit_apl(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.wpzw.update_credit_apl_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.wpzw.update_loan_apl(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.wpzw.update_loan_apl_query(item_no)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.wpzw.update_repayplan_query(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        # self.wpzw.update_contract_download(item_no)
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_weipin_zhongwei
    @pytest.mark.gbiz_weipin_zhongwei_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                             ])
    def test_weipin_zhongwei_loan_success(self, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_weipin_zhongwei
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_weipin_zhongwei_canloan_fail(self, app, source_type, period):
        '''
        canloan失败切资方
        :param case:
        :param app:
        :param source_type:
        :param period:
        :return:
        '''
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.register(item_no, four_element)
        # canloan失败准备工作
        today = time.strftime("%Y-%m-%d", time.localtime())
        update_router_capital_plan_amount(0, today, self.channel)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        time.sleep(2)
        # canloan执行之后恢复
        update_router_capital_plan_amount(10000000000, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "weipin_zhongwei->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_weipin_zhongwei
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_weipin_zhongwei_preapply_fail(self, app, source_type, period):
        '''
        LoanPreApply失败切资方
        :param case:
        :param app:
        :param source_type:
        :param period:
        :return:
        '''
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.register(item_no, four_element)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.wpzw.update_image_upload(item_no, respCode='90001', respMessage='mock上传异常情况')
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "成功_90001_mock上传异常情况", "LoanPreApplySyncFailedEvent")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_weipin_zhongwei
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_weipin_zhongwei_apple_fail(self, app, source_type, period):
        '''
        LoanApplyNew 失败切资方
        :param case:
        :param app:
        :param source_type:
        :param period:
        :return:
        '''
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.register(item_no, four_element)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.wpzw.update_image_upload(item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.wpzw.update_credit_apl(item_no, status="F")
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.wpzw.update_credit_apl_query(item_no, status="F", respCode='107000', respMessage='风控拒绝')
        check_wait_change_capital_data(item_no, 10000000, "成功_000000_F_渠道处理成功", "LoanApplySyncFailedEvent")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_weipin_zhongwei
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_weipin_zhongwei_applequery_fail(self, app, source_type, period):
        '''
        LoanApplyQuery 失败切资方
        :param case:
        :param app:
        :param source_type:
        :param period:
        :return:
        '''
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.register(item_no, four_element)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.wpzw.update_image_upload(item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.wpzw.update_credit_apl(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.wpzw.update_credit_apl_query(item_no, respCode='100003', respMessage='渠道处理中', status='P')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 2})
        self.wpzw.update_credit_apl_query(item_no, respCode='107000', respMessage='风控拒绝', status='F')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 10107000, "成功_107000_F_风控拒绝", "LoanApplyAsyncFailedEvent")


    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_weipin_zhongwei
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_weipin_zhongwei_confirm_fail(self, app, source_type, period):
        '''
        LoanApplyConfirm 失败切资方
        :param case:
        :param app:
        :param source_type:
        :param period:
        :return:
        '''
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.register(item_no, four_element)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.wpzw.update_image_upload(item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.wpzw.update_credit_apl(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.wpzw.update_credit_apl_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.wpzw.update_loan_apl(item_no, status="F")
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.wpzw.update_loan_apl_query(item_no, disbursementStatus='02', failreason="mock放款同步失败")
        check_wait_change_capital_data(item_no, 20000000, "成功_000000_F_成功", "ConfirmApplySyncFailedEvent")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_weipin_zhongwei
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_weipin_zhongwei_confirmquery_fail(self, app, source_type, period):
        '''
        LoanConfirmQuery 失败切资方
        :param case:
        :param app:
        :param source_type:
        :param period:
        :return:
        '''
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.register(item_no, four_element)
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.wpzw.update_image_upload(item_no)
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.wpzw.update_credit_apl(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.wpzw.update_credit_apl_query(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.wpzw.update_loan_apl(item_no)
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.wpzw.update_loan_apl_query(item_no, disbursementStatus='03')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 2})
        self.wpzw.update_loan_apl_query(item_no, disbursementStatus='02', failreason='mock放款异步查询失败')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 20000000, "成功_000000_02_成功_mock放款异步查询失败", "GrantFailedEvent")

    #唯品的结清证明下载，因为接口返回的是base64太大，导致无法mock测试
    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_weipin_zhongwei
    # @pytest.mark.gbiz_certificate
    # def test_weipin_zhongwei_certificate(self):
    #     item_no = fake_asset_data(self.channel, status="payoff")
    #     resp = certificate_apply(item_no)
    #     Assert.assert_equal(0, resp["code"])
    #     check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
    #     self.wpzw.update_certificate_apply()
    #     self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
    #     self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
    #     check_contract(item_no, "ContractDownload", [24])
    #     check_sendmsg_exist(item_no, "CertificateSuccessNotify")