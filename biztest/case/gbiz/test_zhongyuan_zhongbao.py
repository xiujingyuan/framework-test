from biztest.interface.gbiz.gbiz_interface import *
from biztest.interface.gbiz.gbiz_interface import asset_import, common_noloan_import
from biztest.util.easymock.gbiz.zhongyuan_zhongbao import ZhongYuanZhongBaoMock
from biztest.function.gbiz.gbiz_check_function import check_wait_change_capital_data, check_asset_tran_valid_status
from biztest.config.gbiz.gbiz_zhongyuan_zhongbao_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import prepare_attachment
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, update_all_channel_amount,\
    update_router_capital_plan_amount, update_router_capital_plan_amount_all_to_zero
import pytest
from biztest.util.tools.tools import get_four_element



@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_zhongyuan_zhongbao
class TestZhongyuanZhongbao(BaseTestCapital):
    def init(self):
        super(TestZhongyuanZhongbao, self).init()
        self.channel = "zhongyuan_zhongbao"
        self.capital_mock = ZhongYuanZhongBaoMock(gbiz_mock)
        update_gbiz_capital_zhongyuan_zhongbao()
        update_gbiz_capital_zhongyuan_zhongbao_const()
        update_all_channel_amount()


    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_get_sms()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_checkcmsverifycode()  # 该资金方开户只有一个接口，获取和验证是同一个接口，同步成功，无查询接口
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way=self.channel, step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
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
        # 该任务需要上传文件到资金方sftp，文件：身份证正反面，活体照
        self.capital_mock.update_post_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_confirm_get_lpr()
        self.capital_mock.update_loan_confirm()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_confirm_query(asset_info)
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_query(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        #去资方sftp下载
        #self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_zhongyuan_zhongbao_loansuccess
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                             ])
    def test_zhongyuan_zhongbao_loan_success(self, case, app, source_type, count):
        """
        放款成功
        """
        four_element = get_four_element(bank_name='建设银行', id_num_begin="36")
        # 因为有路由准入，所以此处，调用一下路由接口，方便走资金方时使用自动化脚本进件
        self.capital_mock.update_route_access()
        update_router_capital_plan_amount_all_to_zero(self.channel)
        asset_route(four_element, count, 13000, "strawberry", source_type)
        # 路由完成后，恢复资金量
        update_all_channel_amount()

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
    def test_zhongyuan_zhongbao_conloan_fail(self, case, app, source_type, count):
        """
        canloan fail(资金量不足)
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
        check_wait_change_capital_data(item_no, 4, "zhongyuan_zhongbao->校验资金量失败;", "AssetCanLoanFailedEvent")


    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_zhongyuan_zhongbao_not_open_account_conloan_fail(self, case, app, source_type, count):
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
        check_wait_change_capital_data(item_no, 4, "zhongyuan_zhongbao->资金路由系统校验失败: 校验用户账户状态必须为成功:;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_zhongyuan_zhongbao_preapply_fail(self, case, app, source_type, count):
        """
        LoanPreApply失败重试（不切换资金方，因为应该没有业务层面失败，该任务只能成功）
        """
        four_element = get_four_element(id_num_begin="11")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loan_preapply(code='0000001', message='mock 失败')
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 2})

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_zhongyuan_zhongbao_postapply_fail(self, case, app, source_type, count):
        """
        LoanPostApply失败，重试（不切换资金方，因为应该没有业务层面失败，该任务只能成功）
        """
        four_element = get_four_element(id_num_begin="51")
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
        # 该任务需要上传文件到资金方sftp，文件：身份证正反面，活体照
        self.capital_mock.update_post_apply(code='0000000', message='操作成功', retsinal='N')
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 2})



    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_zhongyuan_zhongbao_applyconfirm_fail_01(self, case, app, source_type, count):
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
        self.capital_mock.update_loan_preapply()
        self.task.run_task(item_no, "LoanPreApply", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        # 空实现，不调用接口
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 该任务需要上传文件到资金方sftp，文件：身份证正反面，活体照
        self.capital_mock.update_post_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_confirm_get_lpr()
        self.capital_mock.update_loan_confirm(code='0000000', message='操作成功', checkflag='N')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_confirm_query(asset_info, code='7000000', message='mock 外层失败')
        check_wait_change_capital_data(item_no, 2, "0000000_操作成功_N_null_null_null")

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_zhongyuan_zhongbao_applyconfirm_fail_02(self, case, app, source_type, count):
        """
        申请借款失败切资方(LPR定价查询失败，这个失败不会切换资金方，只会重试)
        """
        four_element = get_four_element(id_num_begin="44")
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, app, source_type)

        self.register(item_no, four_element)
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
        # 该任务需要上传文件到资金方sftp，文件：身份证正反面，活体照
        self.capital_mock.update_post_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_confirm_get_lpr(code='2000000', message='mock LPR定价查询失败')
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 2})

    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                             ])
    def test_zhongyuan_zhongbao_confirmquery_fail(self, case, app, source_type, count):
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
        # 该任务需要上传文件到资金方sftp，文件：身份证正反面，活体照
        self.capital_mock.update_post_apply()
        self.task.run_task(item_no, "LoanPostApply", excepts={"code": 0})
        self.capital_mock.update_confirm_get_lpr()
        self.capital_mock.update_loan_confirm()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loan_confirm_query(asset_info, code='0000000', message='操作成功', outSts='99',
                                                    endMark='02')
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 2, "0000000_操作成功_99_02_null_null")

