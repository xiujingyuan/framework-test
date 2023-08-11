from biztest.interface.gbiz.gbiz_interface import *
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import
from biztest.util.easymock.gbiz.lanhai_zhongbao_hy import LanhaiZhongbaoHyMock
from biztest.function.gbiz.gbiz_check_function import check_wait_change_capital_data, check_asset_tran_valid_status,\
    check_wait_blacklistcollect_data, check_asset_event_exist
from biztest.config.gbiz.gbiz_lanhai_zhongbao_hy_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment, fake_asset_data
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount,\
    update_router_capital_plan_amount, update_asset_due_bill_no
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.config.gbiz.gbiz_kv_config import update_gbiz_payment_config

@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_lanhai_zhongbao_hy
class TestLanHaiZhongBaoHy(BaseTestCapital):
    def init(self):
        super(TestLanHaiZhongBaoHy, self).init()
        self.channel = "lanhai_zhongbao_hy"
        self.capital_mock = LanhaiZhongbaoHyMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_lanhai_zhongbao_hy()
        update_gbiz_capital_lanhai_zhongbao_hy_const()
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
                                  action_type='GetSmsVerifyCode', way='lhzb', step_type='PAYSVR_PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.payment_mock.bind_success(four_element)
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='lhzb', step_type='PAYSVR_PROTOCOL', seq=sms_seq)
        self.payment_mock.query_protocol_channels_get_protocol_info()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')


    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 需要上传合同37400、37401、37402、37403、37408
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBHY_CREDIT_FILE_ID_LIST")
        self.capital_mock.update_credit_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 这个事件存在，代表此笔资产可以下载额度合同, 这个事件是因为LoanApplyQuery这个任务，调用授信查询这个接口的investorApplyId返回有值，若无值或无该字段，则不会记录这个事件
        check_asset_event_exist(item_no, self.channel, "LHZBHY_LMT_CONTRACT_DOWNLOAD")
        # 需要合同37404、37405、37406
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LHZBHY_USE_FILE_ID_LIST")
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
    def test_lanhai_zhongbao_hy_loan_success(self, case, app, source_type, count):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, count, 15000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_lanhai_zhongbao_hy_conloan_fail(self, case, app, source_type, count):
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
        check_wait_change_capital_data(item_no, 4, "lanhai_zhongbao_hy->校验资金量失败;", "AssetCanLoanFailedEvent")



    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_lanhai_zhongbao_hy_applynew_fail(self, case, app, source_type, count):
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
        # 需要上传合同37400、37401、37402、37403、37408
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no, retCode="F1000", retMsg="mock授信申请拒绝", risCode="90000")
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info,  risCode=90000, retCode="0", retMsg="mock授信查询失败",
                                              investorApplyId='')
        check_wait_change_capital_data(item_no, 1, "F1000_mock授信申请拒绝_90000_null_null", 'LoanApplySyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info,  1, "F1000_mock授信申请拒绝_90000_null_null", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_lanhai_zhongbao_hy_applynew_fail_01(self, case, app, source_type, count):
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
        # 需要上传合同37400、37401、37402、37403、37408
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no, risCode="90000")
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info,  risCode=90000, retCode="0", retMsg="mock授信查询失败",
                                              investorApplyId='')
        check_wait_change_capital_data(item_no, 1, "0_成功_90000_null_null", 'LoanApplySyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info,  1, "0_成功_90000_null_null", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_lanhai_zhongbao_hy_applyquery_fail(self, case, app, source_type, count):
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
        # 需要上传合同37400、37401、37402、37403、37408
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info, risCode=90000, retCode="0", retMsg="mock授信查询失败",
                                              investorApplyId='')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "0_mock授信查询失败_90000_null_null", 'LoanApplyAsyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 1, "0_mock授信查询失败_90000_null_null", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_lanhai_zhongbao_hy_applyquery_fail_overdue(self, case, app, source_type, count):
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
        # 需要上传合同37400、37401、37402、37403、37408
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info,  endDt='2023-07-24', risCode=10000, retCode="0",
                                              retMsg="mock授信查询失败", investorApplyId='')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "0_mock授信查询失败_10000_null_null_当前日期不在授信有效期内", 'LoanApplyAsyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 1, "0_mock授信查询失败_10000_null_null_当前日期不在授信有效期内", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_lanhai_zhongbao_hy_applyquery_fail_amount_not_enough(self, case, app, source_type, count):
        """
        授信查询到额度不足，授信失败
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        # 需要上传合同37400、37401、37402、37403、37408
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query_amount_not_enough(amount=10, investorApplyId='')
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 1, "0_成功_10000_null_null_授信金额小于申请金额", 'LoanApplyAsyncFailedEvent')
        check_wait_blacklistcollect_data(item_no, asset_info, 1, "0_成功_10000_null_null_授信金额小于申请金额", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_lanhai_zhongbao_hy_applyconfirm_fail(self, case, app, source_type, count):
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
        # 需要上传合同37400、37401、37402、37403、37408
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_apply(retCode="F1099", retMsg="mock用信申请失败")
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_query(asset_info, risCode="90000", dnSts=400)
        check_wait_change_capital_data(item_no, 2, "F1099_mock用信申请失败", 'ConfirmApplySyncFailedEvent')

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_lanhai_zhongbao_hy_confirmquery_fail(self, case, app, source_type, count):
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
        # 需要上传合同37400、37401、37402、37403、37408
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_credit_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_image_upload()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_apply()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirm_query(asset_info, risCode="10000", dnSts=900)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2, "0_成功_10000_null_null_900", 'GrantFailedEvent')

    #
    # @pytest.mark.parametrize("app, source_type, count",
    #                          [
    #                              ("草莓", "apr36", 12),
    #                          ])
    # def test_lanhai_zhongbao_hy_old_user_loan_success(self, case, app, source_type, count):
    #     """
    #     老用户放款成功，会跳过授信流程，因为已经有额度了
    #     """
    #     four_element = get_four_element(id_num_begin="11")
    #     item_no, asset_info = asset_import(self.channel, four_element, count, 2000, app, source_type)
    #     self.register(item_no, four_element)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.capital_mock.update_loan_pre_apply_old_user()
    #     self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
    #     check_asset_event_exist(item_no, self.channel, "LHZBHY_CREDIT_AMOUNT_ENOUGH")
    #     prepare_attachment(self.channel, item_no)
    #     # 跳过授信，不上传附件，也不用调用接口
    #     self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
    #     # 跳过授信步骤，此任务不调用接口
    #     self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
    #     # 需要合同37404、37405、37406
    #     self.capital_mock.update_image_upload()
    #     self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
    #     check_asset_event_exist(item_no, self.channel, "LHZBHY_USE_FILE_ID_LIST")
    #     self.capital_mock.update_loanconfirm_apply()
    #     self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
    #     self.capital_mock.update_loanconfirm_query(asset_info)
    #     self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
    #     self.capital_mock.update_repayplan_query(item_no, asset_info)
    #     self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
    #     self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
    #
    # @pytest.mark.parametrize("app, source_type, count",
    #                          [
    #                              ("草莓", "apr36", 12),
    #                          ])
    # def test_lanhai_zhongbao_hy_old_user_no_event(self, case, app, source_type, count):
    #     """
    #     老用户放款查询额度，没有返回lmtNo，不存事件，则会继续调用授信接口等(mock了额度失效时，继续调用授信)
    #     """
    #     four_element = get_four_element(id_num_begin="11")
    #     item_no, asset_info = asset_import(self.channel, four_element, count, 2000, app, source_type)
    #     self.register(item_no, four_element)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.capital_mock.update_loan_pre_apply_old_user_lose_effectiveness()
    #     self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
    #     prepare_attachment(self.channel, item_no)
    #     # 需要上传合同37400、37401、37402、37403、37408
    #     self.capital_mock.update_image_upload()
    #     self.capital_mock.update_credit_apply(item_no)
    #     self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
    #     check_asset_event_exist(item_no, self.channel, "LHZBHY_CREDIT_FILE_ID_LIST")
    #     self.capital_mock.update_credit_query(asset_info)
    #     self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
    # @pytest.mark.parametrize("app, source_type, count",
    #                          [
    #                              ("草莓", "apr36", 12),
    #                          ])
    # def test_lanhai_zhongbao_hy_loan_pre_apply_fail_01(self, case, app, source_type, count):
    #     """
    #     LoanPreApply失败，因为额度过期
    #     """
    #     four_element = get_four_element(id_num_begin="11")
    #     item_no, asset_info = asset_import(self.channel, four_element, count, 2000, app, source_type)
    #     self.register(item_no, four_element)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.capital_mock.update_loan_pre_apply_old_user(startDt='2019-01-01', endDt='2023-07-24 23:59:59')
    #     self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 0, "0_成功_04_当前日期不在授信有效期内", 'LoanPreApplySyncFailedEvent')
    #
    # @pytest.mark.parametrize("app, source_type, count",
    #                          [
    #                              ("草莓", "apr36", 12),
    #                          ])
    # def test_lanhai_zhongbao_hy_loan_pre_apply_fail_02(self, case, app, source_type, count):
    #     """
    #     LoanPreApply失败，因为授信剩余可用额度不足 （不会校验amount；只校验restAmount>=借款本金）
    #     """
    #     four_element = get_four_element(id_num_begin="11")
    #     item_no, asset_info = asset_import(self.channel, four_element, count, 2000, app, source_type)
    #     self.register(item_no, four_element)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.capital_mock.update_loan_pre_apply_old_user(restAmount=10, amount=60000)
    #     self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 0, "0_成功_04_剩余可用授信额度小于借款本金", 'LoanPreApplySyncFailedEvent')
    #
    # @pytest.mark.parametrize("app, source_type, count",
    #                          [
    #                              ("草莓", "apr36", 12),
    #                          ])
    # def test_lanhai_zhongbao_hy_loan_pre_apply_fail_03(self, case, app, source_type, count):
    #     """
    #     LoanPreApply失败，因为额度查询失败（额度冻结）
    #     """
    #     four_element = get_four_element(id_num_begin="11")
    #     item_no, asset_info = asset_import(self.channel, four_element, count, 10000, app, source_type)
    #     self.register(item_no, four_element)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.capital_mock.update_loan_pre_apply_old_user(lmtStatus='05')
    #     self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 0, "0_成功_05", 'LoanPreApplySyncFailedEvent')
    #
    # @pytest.mark.parametrize("app, source_type, count",
    #                          [
    #                              ("草莓", "apr36", 12),
    #                          ])
    # def test_lanhai_zhongbao_hy_loan_pre_apply_fail_04(self, case, app, source_type, count):
    #     """
    #     LoanPreApply失败，因为额度查询失败（外层code失败，接口调用失败）
    #     """
    #     four_element = get_four_element(id_num_begin="11")
    #     item_no, asset_info = asset_import(self.channel, four_element, count, 10000, app, source_type)
    #     self.register(item_no, four_element)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.capital_mock.update_loan_pre_apply_old_user(retCode='E1005', retMsg='mock额度查询外层code失败')
    #     self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 0, "E1005_mock额度查询外层code失败_04", 'LoanPreApplySyncFailedEvent')