from biztest.interface.gbiz.gbiz_interface import *
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import
from biztest.util.easymock.gbiz.hayin_zhongbao import HayinZhongbaoMock
from biztest.function.gbiz.gbiz_check_function import check_wait_change_capital_data, check_asset_tran_valid_status,\
    check_wait_blacklistcollect_data, check_asset_event_exist
from biztest.config.gbiz.gbiz_hayin_zhongbao_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment, fake_asset_data
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount,\
    update_router_capital_plan_amount, update_asset_due_bill_no
import pytest
from biztest.util.tools.tools import get_four_element


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_hayin_zhongbao
class TestHayinZhongbao(BaseTestCapital):
    def init(self):
        super(TestHayinZhongbao, self).init()
        self.channel = "hayin_zhongbao"
        self.capital_mock = HayinZhongbaoMock(gbiz_mock)
        update_gbiz_capital_hayin_zhongbao()
        update_gbiz_capital_hayin_zhongbao_const()
        update_all_channel_amount()


    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        self.capital_mock.update_open_account_query()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_account_bind_apply()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='hayin_zhongbao', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_account_bind_confirm()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='hayin_zhongbao', step_type='PROTOCOL', seq=sms_seq)
        # self.capital_mock.update_open_account_query()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 该任务调用接口后，还要上传一部分文件到FTP,需要上传合同35301, 35302,35303,35304
        self.capital_mock.update_image_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "HYZB_CREDIT_FILE_ID_LIST")
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要上传合同35305, 35306
        self.capital_mock.update_image_upload_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "HYZB_USE_FILE_ID_LIST")
        self.capital_mock.update_loanconfirm_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_query(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_query(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        # 去资方ftp下载
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        # #  ContractDown成功之后会生成以下两个任务去上传担保文件给担保方，但是因为测试环境一般都下载合同都不成功，所以此处屏蔽
        # #  以下两个任务未调用任何接口，都是直接上传到SFTP的
        # self.task.run_task(item_no, "GuaranteeUpload", excepts={"code": 0})
        # self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        # 推送是推送到ftp，推送35307
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
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
    def test_hayin_zhongbao_loan_success(self, case, app, source_type, count):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, count, 13000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hayin_zhongbao_old_user_open_account(self, case, app, source_type, count):
        """
        老用户开户
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, count, 10000, app, source_type)
        self.capital_mock.update_old_user_open_account_query(four_element)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hayin_zhongbao_conloan_fail(self, case, app, source_type, count):
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
        check_wait_change_capital_data(item_no, 4, "hayin_zhongbao->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hayin_zhongbao_applynew_fail(self, case, app, source_type, count):
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
        # 该任务调用接口后，还要上传一部分文件到FTP
        self.capital_mock.update_image_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock. update_credit_apply(item_no, retCode="F1000", retMsg="mock授信申请拒绝", risCode="90000")
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info,  risCode=90000, retCode="0", retMsg="mock授信查询失败")
        check_wait_change_capital_data(item_no, 1, "F1000_mock授信申请拒绝", 'LoanApplySyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info,  1, "F1000_mock授信申请拒绝", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hayin_zhongbao_applyquery_fail(self, case, app, source_type, count):
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
        # 该任务调用接口后，还要上传一部分文件到FTP
        self.capital_mock.update_image_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info, risCode=90000, retCode="0", retMsg="mock授信查询失败")
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "0_mock授信查询失败_90000_null_null", 'LoanApplyAsyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 1, "0_mock授信查询失败_90000_null_null", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hayin_zhongbao_applyquery_fail_overdue(self, case, app, source_type, count):
        """
        授信查询到额度过期切资方
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 该任务调用接口后，还要上传一部分文件到FTP
        self.capital_mock.update_image_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info,  endDt='2023-04-10', risCode=10000, retCode="0", retMsg="mock授信查询失败")
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "0_mock授信查询失败_10000_null_null_当前日期不在授信有效期内", 'LoanApplyAsyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 1, "0_mock授信查询失败_10000_null_null_当前日期不在授信有效期内", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hayin_zhongbao_applyconfirm_fail(self, case, app, source_type, count):
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
        # 该任务调用接口后，还要上传一部分文件到FTP
        self.capital_mock.update_image_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_image_upload_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_apply(retCode="F1099", retMsg="mock用信申请失败")
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_query(asset_info, risCode="90000", dnSts=400)
        check_wait_change_capital_data(item_no, 2, "F1099_mock用信申请失败", 'ConfirmApplySyncFailedEvent')

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_hayin_zhongbao_confirmquery_fail(self, case, app, source_type, count):
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
        # 该任务调用接口后，还要上传一部分文件到FTP
        self.capital_mock.update_image_upload_success()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_image_upload_success()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_query(asset_info, risCode="10000", dnSts=900)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2, "0_成功_10000_null_null_900", 'GrantFailedEvent')

    @pytest.mark.gbiz_certificate
    def test_hayin_zhongbao_certificate(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        update_asset_due_bill_no(item_no)
        self.capital_mock.update_certificate_apply()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        # 是从哈银的sftp上下载，不好mock，屏蔽
        # self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        # check_contract(item_no, "ContractDownload", [24])
        # check_sendmsg_exist(item_no, "CertificateSuccessNotify")