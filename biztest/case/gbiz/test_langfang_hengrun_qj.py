from biztest.interface.gbiz.gbiz_interface import *
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import
from biztest.util.easymock.gbiz.langfang_hengrun_qj import LangfangHengrunQjMock
from biztest.function.gbiz.gbiz_check_function import check_wait_change_capital_data,\
    check_wait_blacklistcollect_data, check_asset_event_exist, check_asset_tran_valid_status
from biztest.config.gbiz.gbiz_langfang_hengrun_qj_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment, run_terminated_task
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount, \
    update_router_capital_plan_amount
from biztest.function.biz.biz_db_function import wait_biz_asset_appear
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_langfang_hengrun_qj
class TestLangfangHengrunQj(BaseTestCapital):
    def init(self):
        super(TestLangfangHengrunQj, self).init()
        self.channel = "langfang_hengrun_qj"
        self.capital_mock = LangfangHengrunQjMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_langfang_hengrun_qj()
        update_gbiz_capital_langfang_hengrun_qj_const()
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
        time.sleep(5)
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)  # 需要Biz出现资产才可以执行成功，所以此处等待
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LF_HR_QJ_PRE_APPLY")
        # 需要合同35200,35201,35202,35203
        prepare_attachment(self.channel, item_no)  # ⚠️如果走资金方联测，需要屏蔽此处，因为合同需要是走合同系统签约出来的才可以
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LF_HR_QJ_POST_APPLY")
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel,  "LF_HR_QJ_ROUTER_SUCCESS")
        self.capital_mock.update_credit_apply_query(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_sign_ature()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "HR_GUARANTEE_SIGNATURE")
        # 需要存在35204合同，但是此合同必须是在任务ContractSignature执行成功之后执行合同任务签约出来才可以
        self.capital_mock.update_guarantee_apply()
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "HR_GUARANTEE_SIGNATURE_APPLY")
        self.capital_mock.update_guarantee_down()
        self.task.run_task(item_no, "GuaranteeDown", excepts={"code": 0})
        # # 需要合同：35205、35206、35207、35208
        self.capital_mock.update_file_notice()  # 和LoanPostApply调用的一样的接口
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        check_asset_event_exist(item_no, self.channel, "LF_HR_QJ_PRE_LOAN_CONFORM")
        self.capital_mock.update_loan_apply_confirm()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_apply_confirm_query(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_success(asset_info, item_no)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        self.capital_mock.update_contract_down()  # 下载28借款合同
        self.task.run_task(item_no, "ContractDown")
        self.capital_mock.update_loan_prove_down()
        self.task.run_task(item_no, "ElectronicReceiptDown", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)


    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_langfang_hengrun_qj_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [("香蕉", "apr36", 12),
                              #("草莓", "irr36", 12),
                              ])
    def test_langfang_hengrun_qj_loan_success(self, case, app, source_type, period):
        """
        放款成功
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 15000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        #check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=True)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
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
        update_router_capital_plan_amount(10000000000, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "langfang_hengrun_qj->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_langfang_hengrun_qj_not_open_account_conloan_fail(self, case, app, source_type, count):
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
                                       "langfang_hengrun_qj->资金路由系统校验失败: 校验用户账户状态必须为成功:;",
                                       "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply(sendflag='02', errocode='999999', sendcode='0001', sendmsg='mock失败',
                                            errormsg='失败测试')
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 因为跳过了二次校验，此处没有mock查询接口的失败，因为此资金方的查询也不建议失败（查询是走的合同的东西，非业务的）
        check_wait_change_capital_data(item_no, 1999999, "02_0001_失败测试_mock失败", "LoanApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_applyquery_fail(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败重试，因为此接口是查询合同回来，不关业务，所以此接口不能走切换资金方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="21")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create(sendflag='02', errocode='000003', sendcode='9999',
                                                 sendmsg='查询失败test', errormsg='失败测试')
        wait_biz_asset_appear(item_no)  # 需要Biz出现资产才可以执行成功，所以此处等待
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 2})
        # check_wait_change_capital_data(item_no, 2, "0_交易成功！_2_null_null", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_route_fail(self, case, app, source_type, period):
        """
        LoanCreditApply 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="33")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply(sendflag='02', errocode='000007', sendcode='9999', sendmsg='路由失败',
                                              errormsg='mock失败测试')
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 1})
        self.capital_mock.update_credit_apply_query(asset_info, sendflag='02', errocode='000008', sendcode='0006',
                                                     errormsg='mock失败test', sendmsg='路由查询失败测试')
        run_terminated_task(item_no, 'ChangeCapital', expect_code=2)
        # 此处因为失败没有事件：LF_HR_QJ_ROUTER_SUCCESS，会导致在切换资金方任务中调用路由查询接口时报错：没有事件，
        # 所以切换资金方任务不能执行成功，此处先屏蔽，线上考虑可以配置跳过切换资金方校验
        # check_wait_change_capital_data(item_no, 2000007, "02_9999_mock失败测试_路由失败", "LoanCreditApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_route_query_fail_01(self, case, app, source_type, period):
        """
            LoanCreditQuery 失败切资方(接口业务失败)
            :param app:
            :param source_type:
            :param period:
            :return:
        """
        four_element = get_four_element(id_num_begin="25")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_query(asset_info, sendflag='02', errocode='000005', sendcode='0004',
                                                    errormsg='mock失败', sendmsg='路由查询失败test')
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2000005, "02_0004_mock失败_路由查询失败test", "LoanCreditFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 2000005, "02_0004_mock失败_路由查询失败test", "id_card")


    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_route_query_fail_02(self, case, app, source_type, period):
        """
            LoanCreditQuery 授信失败切资方(因为授信金额不足，失败)
            :param app:
            :param source_type:
            :param period:
            :return:
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要附件35200,35201,35202,35203
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_query_fail(creditamt='100', enddate='20400606')  # enddate字段代码中没有做校验
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 9999, "当前资产待放金额.*大于查询返回授信成功金额.*", "LoanCreditFailedEvent")
        check_wait_blacklistcollect_data(item_no, asset_info, 9999, "当前资产待放金额.*大于查询返回授信成功金额.*", "id_card")


    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_contract_signature_fail(self, case, app, source_type, period):
        """
        ContractSignature失败，不允许切换资金方，只能重试
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要附件35200,35201,35202,35203
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_query(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_sign_ature(sendflag='02', errocode='000001', sendcode='9999',
                                                     sendmsg='处理失败', errormsg='mock失败')
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 2})

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_guarantee_apply_fail(self, case, app, source_type, period):
        """
        GuaranteeApply 失败，不允许切换资金方，只能重试
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要附件35200,35201,35202,35203
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_query(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_sign_ature()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        # 需要存在35204合同，但是此合同必须是在任务ContractSignature执行成功之后执行合同任务签约出来才可以
        self.capital_mock.update_guarantee_apply(code=0, status='500', message='mock失败', msg='内层mock成功')
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 2})

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_guarantee_down_fail(self, case, app, source_type, period):
        """
        GuaranteeDown 失败，不允许切换资金方，只能重试
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要附件35200,35201,35202,35203
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_query(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_sign_ature()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        self.capital_mock.update_guarantee_apply()
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        self.capital_mock.update_guarantee_down(code=0, status='500', message='失败测试', msg='mock内层失败')
        self.task.run_task(item_no, "GuaranteeDown", excepts={"code": 2})

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_langfang_hengrun_qj_loan_post_credit_fail(self, case, app, source_type, period):
        """
        LoanPostCredit 失败，不允许切换资金方，只能重试
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 需要附件35200,35201,35202,35203
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_query(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_sign_ature()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        self.capital_mock.update_guarantee_apply()
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        self.capital_mock.update_guarantee_down()
        self.task.run_task(item_no, "GuaranteeDown", excepts={"code": 0})
        self.capital_mock.update_file_notice(sendflag='02', errocode='000001', sendcode='4000', errormsg='失败测试')
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 2})

    @pytest.mark.parametrize("app, source_type, period", [("草莓", "irr36", 12)])
    def test_langfang_hengrun_qj_confirm_fail(self, case, app, source_type, period):
        """
            LoanApplyConfirm 失败切资方
            :param app:
            :param source_type:
            :param period:
            :return:
        """
        four_element = get_four_element(id_num_begin="42")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_query(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_sign_ature()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        self.capital_mock.update_guarantee_apply()
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        self.capital_mock.update_guarantee_down()
        self.task.run_task(item_no, "GuaranteeDown", excepts={"code": 0})
        self.capital_mock.update_file_notice()  # 和LoanPostApply调用的一样的接口
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loan_apply_confirm(sendflag='02', message='fail 测试', sendcode='0007',
                                                    errocode='000007', errormsg='内层失败msg')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_apply_confirm_query(asset_info, sendflag='02', message='放款失败测试', sendcode='0002',
                                                          errocode='000009', errormsg='内层失败测试')
        check_wait_change_capital_data(item_no, 3000007, "02_0007_内层失败msg_null", "ConfirmApplySyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("草莓", "irr36", 12)])
    def test_langfang_hengrun_qj_confirmquery_fail(self, case, app, source_type, period):
        """
        LoanConfirmQuery 失败切资方
        """
        four_element = get_four_element(id_num_begin="36")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_apply()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_contract_create()
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_file_notice()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply()
        self.task.run_task(item_no, "LoanCreditApply", excepts={"code": 0})
        self.capital_mock.update_credit_apply_query(asset_info)
        self.task.run_task(item_no, "LoanCreditQuery", excepts={"code": 0})
        self.capital_mock.update_contract_sign_ature()
        self.task.run_task(item_no, "ContractSignature", excepts={"code": 0})
        self.capital_mock.update_guarantee_apply()
        self.task.run_task(item_no, "GuaranteeApply", excepts={"code": 0})
        self.capital_mock.update_guarantee_down()
        self.task.run_task(item_no, "GuaranteeDown", excepts={"code": 0})
        self.capital_mock.update_file_notice()  # 和LoanPostApply调用的一样的接口
        self.task.run_task(item_no, "LoanPostCredit", excepts={"code": 0})
        self.capital_mock.update_loan_apply_confirm()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_apply_confirm_query(asset_info, sendflag='01', message='查询失败测试',
                                                          sendcode='0011', errocode='000077', errormsg='内层失败测试')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 3000077, "01_0011_内层失败测试_null", "GrantFailedEvent")

