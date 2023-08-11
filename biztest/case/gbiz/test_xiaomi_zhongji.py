from biztest.interface.gbiz.gbiz_interface import *
from biztest.config.gbiz.gbiz_kv_config import update_gbiz_payment_config
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import
from biztest.util.easymock.gbiz.xiaomi_zhongji import XiaomiZhongjiMock
from biztest.function.gbiz.gbiz_check_function import check_wait_change_capital_data, check_asset_tran_valid_status,\
    check_wait_blacklistcollect_data, check_asset_event_exist
from biztest.config.gbiz.gbiz_xiaomi_zhongji_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment, fake_asset_data
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount,\
    update_router_capital_plan_amount, update_asset_due_bill_no
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_xiaomi_zhongji
class TestXiaomiZhongji(BaseTestCapital):
    """
       gbiz_xiaomi_zhongji
       author: zhimengxue
       date: 20230506
    """
    def init(self):
        super(TestXiaomiZhongji, self).init()
        self.channel = "xiaomi_zhongji"
        self.capital_mock = XiaomiZhongjiMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_payment_config(self.payment_mock.url)
        update_gbiz_capital_xiaomi_zhongji()
        update_gbiz_capital_xiaomi_zhongji_const()
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
        # 该任务需上传文件到资金方sftp，先调用接口，上传文件：身份证正反面，活体照、35500、35501、35502、35509
        self.capital_mock.update_loan_pre_apply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock. update_loan_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "XMZJ_CREDIT_APPLY")
        self.capital_mock.update_loan_apply_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "XMZJ_CREDIT_NO")
        self.capital_mock.update_loan_post_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "XMZJ_PRTOCOL_NO")
        # 若上一步有返回协议编号，则签约出来一起上传，否则只上传身份证正反面、活体照到FTP
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loan_apply_confirm()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "XMZJ_LOAN_APPLY")
        self.capital_mock.update_loan_apply_confirm_query(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_query(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        # # #2023-05-17删除了以下任务，因为资金方说后续通过别的方式批量给我们放款凭证，以下任务是申请下载放款凭证的
        # self.capital_mock.update_contract_signature_query()
        # self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        # check_asset_event_exist(item_no, self.channel, "XMZJ_LOAN_VOUCHER")
        # 上传35503合同
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        # 去资方sftp下载，不好mock，此处屏蔽（新用户下载28、35504；老用户下载28）
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_xiaomi_zhongji_loansuccess
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                                 #("草莓", "irr36", 12),
                                 #("火龙果", "irr36_lexin", 12),
                             ])
    def test_xiaomi_zhongji_loan_success(self, case, app, source_type, count):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="36")
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
    def test_xiaomi_zhongji_conloan_fail(self, case, app, source_type, count):
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
        check_wait_change_capital_data(item_no, 4, "xiaomi_zhongji->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_pre_apply_fail(self, case, app, source_type, count):
        """
       LoanPreApply失败，切换资金方， 额度信息查询失败
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_pre_apply(code="241081", message="mock额度查询失败")
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 100000, "241081_mock额度查询失败", "LoanPreApplySyncFailedEvent")
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_old_user_quota_active(self, case, app, source_type, count):
        """
        LoanPreApply 老用户已经存在授信额度，会直接跳过授信流程，就是LoanApplyNew、LoanApplyQuery不会调用接口了
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_pre_apply(code="000000", message="成功", limitState="0", remainLimit="20000",
                                                creditLimit="2000", endDate="2040-06-06", startDate="2023-05-05",
                                                credNo="C@id")
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "XMZJ_CREDIT_NO")
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_post_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "XMZJ_PRTOCOL_NO")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_old_user_quota_not_enough(self, case, app, source_type, count):
        """
        LoanPreApply 老用户因额度不足，重新走授信流程,remainLimit可用额度<>0,但金额小于进件金额
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_pre_apply(code="000000", message="成功", limitState="0", remainLimit="10",
                                                creditLimit="10000", endDate="2040-06-06", startDate="2023-05-06")
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "额度不可用,切资方!", "LoanPreApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_old_user_quota_equal_0(self, case, app, source_type, count):
        """
        LoanPreApply 老用户额度为0,remainLimit可用额度为0，切换资金方
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_pre_apply(code="000000", message="成功", limitState="0", remainLimit="0",
                                                creditLimit="10000", endDate="2040-06-06", startDate="2023-05-06")
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "额度不可用,切资方!", "LoanPreApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_old_user_quota_expire(self, case, app, source_type, count):
        """
        LoanPreApply 老用户因额度已经失效，重新走授信流程（endDate<进件当日）
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_pre_apply(code="000000", message="成功", limitState="0", remainLimit=20000,
                                                creditLimit=20000, endDate="2023-05-05", startDate="2022-05-06")
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "额度不可用,切资方!", "LoanPreApplySyncFailedEvent")
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_applynew_fail(self, case, app, source_type, count):
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
        self.capital_mock.update_loan_pre_apply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply(item_no, code="000000", result="F", message="mock授信申请失败")
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query(asset_info,  code="000000", result="F", message="mock授信查询失败")
        check_wait_change_capital_data(item_no, 100000, "000000_mock授信申请失败_F")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_applyquery_fail(self, case, app, source_type, count):
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
        self.capital_mock.update_loan_pre_apply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query(asset_info, code="000000", result="F", message="mock授信查询失败")
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 100000, "000000_mock授信查询失败_F_null_null")
        check_wait_blacklistcollect_data(item_no, asset_info, 100000, "000000_mock授信查询失败_F_null_null", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_applyquery_fail_01(self, case, app, source_type, count):
        """
        授信查询额度不足，失败切资方
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_pre_apply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "资方授信金额\\[10.00\\]小于我方进件金额\\[8000.00\\]")
        check_wait_blacklistcollect_data(item_no, asset_info, 9999, "资方授信金额\\[10.00\\]小于我方进件金额\\[8000.00\\]", "id_card")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_applyconfirm_fail(self, case, app, source_type, count):
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
        self.capital_mock.update_loan_pre_apply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.capital_mock.update_loan_post_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loan_apply_confirm(code="000000", result="F", message="放款申请失败")
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_apply_confirm_query(asset_info, code="000001", payStatus="S", message="mock放款查询外层失败")
        check_wait_change_capital_data(item_no, 200000, "000000_放款申请失败_F")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_xiaomi_zhongji_confirmquery_fail(self, case, app, source_type, count):
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
        self.capital_mock.update_loan_pre_apply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        self.capital_mock.update_loan_apply(item_no)
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "XMZJ_CREDIT_NO")
        self.capital_mock.update_loan_post_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "XMZJ_PRTOCOL_NO")
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loan_apply_confirm()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "XMZJ_LOAN_APPLY")
        self.capital_mock.update_loan_apply_confirm_query(asset_info, code="000000", payStatus="F", message="mock放款查询失败")
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 200000, "000000_mock放款查询失败_F_null")


    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_xiaomi_zhogji
    @pytest.mark.gbiz_certificate
    def test_xiaomi_zhogji_certificate(self, case):
        item_no = fake_asset_data(self.channel, status="payoff")
        resp = certificate_apply(item_no)
        Assert.assert_equal(0, resp["code"])
        check_asset_event_exist(item_no, self.channel, "CERTIFICATE_GENERATE_EVENT")
        update_asset_due_bill_no(item_no)
        self.capital_mock.update_certificateapply_success()
        self.task.run_task(item_no, "CertificateApply", excepts={"code": 0})
        # self.capital_mock.update_certificatedownload_success()  # 这个接口调用成功之后还会去FTP上下载，FTP不能mock，所以屏蔽以下
        # self.task.run_task(item_no, "CertificateDownload", excepts={"code": 0})
        # check_contract(item_no, "ContractDownload", [24])
        # check_sendmsg_exist(item_no, "CertificateSuccessNotify")