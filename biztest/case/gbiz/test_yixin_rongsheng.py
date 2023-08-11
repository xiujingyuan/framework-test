from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.yixin_rongsheng import YiXinRongShengMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_yixin_rongsheng_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount, update_router_load_record_by_key, \
    update_router_capital_plan_amount_all_to_zero
import pytest
from biztest.util.tools.tools import get_four_element
from biztest.util.easymock.gbiz.payment import PaymentMock


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_yixin_rongsheng
class TestYixinRongsheng(BaseTestCapital):
    """
       gbiz_yixin_rongsheng
       author: zhimengxue
       date: 20220812
       """

    def init(self):
        super(TestYixinRongsheng, self).init()
        self.channel = "yixin_rongsheng"
        self.capital_mock = YiXinRongShengMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_yixin_rongsheng()
        update_gbiz_capital_yixin_rongsheng_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()


    def register(self, item_no, four_element):
        self.capital_mock.update_query_bankcard_new_user()
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_account_get_msg_code_success(four_element)
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='yixin_rongsheng', step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_account_bind_verify(four_element)
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='yixin_rongsheng', step_type='PROTOCOL', seq=sms_seq)
        self.capital_mock.update_query_bankcard_success(four_element)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetApplyTrailSuccess")
        self.capital_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery_success()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.capital_mock.update_repayplan_success(item_no, asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        check_asset_tran_valid_status(item_no, grant_status=0, other_status=1)
        # self.capital_mock.update_contractdown_success()
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_yixin_rongsheng_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                   ("香蕉", "apr36", 12),
                                 # ("草莓", "irr36", 12),
                                 # ("火龙果", "real36", 12),
                                 # ("草莓", "apr36_huaya", 12),  # 花鸭只能草莓进件
                                 # ("火龙果", "irr36_rongshu", 12),
                             ])
    def test_yixin_rongsheng_loan_success_12m(self, case, app, source_type, period):
        """
        放款成功，该资金方涉及产品线变更，目前只会用12期路由进件
        12期进件之后会有可能转为6期
        2022-12-01：目前线上只放12期的，因现在没有副产品了，线上去掉了12期副产品的校验
        """
        # 走纯12期流程，注意：12期的现在不校验副产品了，路由规则也去掉了副产品校验，没有副产品也可以放款成功（但12期有副产品也可以放款成功！）
        four_element = get_four_element(id_num_begin="31")
        # 因为有路由准入，所以此处，调用一下路由接口，方便走资金方时使用自动化脚本进件
        self.capital_mock.update_user_access_success()
        update_router_capital_plan_amount_all_to_zero(self.channel)
        asset_route(four_element, period, 13000, "strawberry", source_type)
        # 路由完成后，恢复资金量
        update_all_channel_amount()

        item_no, asset_info = asset_import(self.channel, four_element, period, 13000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)


    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_yixin_rongsheng_loan_success
    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12),
                                # ("草莓", "irr36", 12),
                             ])
    def test_yixin_rongsheng_loan_success_6m(self, case, app, source_type, period):
        """
        放款成功，该资金方涉及产品线变更，目前只会用12期路由进件
        12期进件之后会有可能转为6期
        2022-12-01：目前线上只放12期的，因现在没有副产品了，线上去掉了12期副产品的校验
        """
        # 走12期切换6期流程
        # 6期测试时必须加上路由规则对副产品的校验，6期一定会校验副产品的，副产品为空会在LoanApplyNew/LoanApplyQuery报错
        four_element = get_four_element(id_num_begin="31")
        # ⚠️以下这个金额6666，若是更改需要变更进件参数的条件，此金额无必要不要更改！！！
        item_no, asset_info = asset_import(self.channel, four_element, period, 6666, app, source_type)
        self.register(item_no, four_element)
        # 为了走12期转换为6期流程，因为自动化里直接插入了路由记录，所以此处需手动变更，方便验证12变6的流程
        route_key = item_no + self.channel
        update_router_load_record_by_key(route_key, router_load_record_rule_code="yixin_rongsheng_6m",
                                             router_load_record_product_code="yxrs_6m")
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)


    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yixin_rongsheng_conloan_fail(self, case, app, source_type, period):
        """
        canloan fail
        :return:
        """
        four_element = get_four_element(id_num_begin="42")
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
        check_wait_change_capital_data(item_no, 4, "yixin_rongsheng->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yixin_rongsheng_loanapplynew_fail(self, case, app, source_type, period):
        """
        进件同步失败
        :return:
        """
        four_element = get_four_element(id_num_begin="63")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_fail()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock失败--1-mock的", 'LoanApplySyncFailedEvent')

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_yixin_rongsheng_loanapplyquery_fail(self, case, app, source_type, period):
        """
        进件查询失败
        :return:
        """
        four_element = get_four_element(id_num_begin="50")
        item_no, asset_info = asset_import(self.channel, four_element, period, 7000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_fail()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock失败-REFUSE-null", 'LoanApplyAsyncFailedEvent')

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("草莓", "apr36", 12)
                             ])
    def test_yixin_rongsheng_loanapplyconfirm_fail(self, case, app, source_type, period):
        """
        放款申请同步失败
        :return:
        """
        four_element = get_four_element(id_num_begin="51")
        item_no, asset_info = asset_import(self.channel, four_element, period, 9000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetApplyTrailSuccess")
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_fail()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock 失败-1-mock 失败")

    @pytest.mark.parametrize("app, source_type, period",
                             [
                                 ("香蕉", "apr36", 12)
                             ])
    def test_yixin_rongsheng_loanaconfirmquery_fail(self, case, app, source_type, period):
        """
        放款失败
        :return:
        """
        four_element = get_four_element(id_num_begin="62")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        self.capital_mock.update_loanapplynew_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loanapplyquery_success()
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyTrial", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetApplyTrailSuccess")
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.capital_mock.update_loanapplyconfirm_success()
        self.task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        self.capital_mock.update_loanconfirmquery_fail()
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 0, "mock失败-LEND_FAILED-放款失败", 'GrantFailedEvent')

    @pytest.mark.gbiz_assetreverse
    @pytest.mark.parametrize("app, source_type, period",
                                 [
                                     ("香蕉", "apr36", 12)
                                 ])
    def test_yixin_rongsheng_assetreverse(self, case, app, source_type, period):
        """
        放款成功后冲正,此处走了真正的12期放款
        """
        four_element = get_four_element(id_num_begin="31")
        item_no, asset_info = asset_import(self.channel, four_element, period, 13000, app, source_type)
        self.register(item_no, four_element)
        self.loan_to_success(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

        # 冲正回调
        yixin_rongsheng_reverse_callback(asset_info)
        self.task.run_task(item_no, "CapitalCallback", excepts={"code": 0})

        run_terminated_task(item_no, "CapitalAssetReverse", expect_code=0)
        self.msg.run_msg(item_no, "AssetReverseNotifyV2", excepts={"code": 0})

        check_wait_assetvoid_data(item_no, code=14, message="发生冲正,作废资产")
        self.task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
        self.msg.run_msg(item_no, "CapitalFailedLoanRecordSync", excepts={"code": 0})
        # 取消的通知
        self.msg.run_msg(item_no, "AssetGrantCancelNotifyMQV2", excepts={"code": 0})
        check_asset(item_no, asset_status='void')
        check_asset_loan_record(item_no, asset_loan_record_status=5, asset_loan_record_memo="发生冲正")
        # 冲正小单也会有通知
        for noloan_item_no in noloan_item_no_lt:
            self.msg.run_msg(noloan_item_no, "AssetReverseNotifyV2", excepts={"code": 0})
            self.msg.run_msg(noloan_item_no, "AssetGrantCancelNotifyMQV2", excepts={"code": 0})
            check_asset(noloan_item_no, asset_status='void')



    # @pytest.mark.parametrize("app, source_type, period",
    #                          [
    #                              ("香蕉", "irr36", 12)
    #                          ])
    # def test_yixin_rongsheng_loancancel_success(self, case, app, source_type, period):
    #     """
    #     用户确认超时失败,走资金方取消成功
    #     :return:
    #     """
    #     four_element = get_four_element(id_num_begin="66")
    #     item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
    #     self.register(item_no, four_element)
    #     # 修改超时配置以便失败
    #     update_gbiz_capital_yixin_rongsheng(raise_limit_over_time_seconds=0)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.capital_mock.update_loanapplynew_success()
    #     self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
    #     self.capital_mock.update_loanapplyquery_success()
    #     self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
    #     check_asset_confirm(item_no, "LOAN_PRODUCT_CHANGE", 2)
    #     self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
    #     self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
    #     self.capital_mock.update_loancancelsuccess()
    #     self.task.run_task(item_no, "LoanGrantStatusPush", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 10005, "确认类型\\[LOAN_PRODUCT_CHANGE\\]已超时", 'UserConfirmTimeOutEvent')
    #     # case跑完恢复配置
    #     update_gbiz_capital_yixin_rongsheng()
    #
    #
    # @pytest.mark.parametrize("app, source_type, period",
    #                          [
    #                              ("香蕉", "irr36", 12)
    #                          ])
    # def test_yixin_rongsheng_loancancel_fail(self, case, app, source_type, period):
    #     """
    #     用户确认超时失败,走资金方取消失败
    #     :return:
    #     """
    #     four_element = get_four_element(id_num_begin="66")
    #     item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
    #     self.register(item_no, four_element)
    #     # 修改超时配置以便失败
    #     update_gbiz_capital_yixin_rongsheng(raise_limit_over_time_seconds=0)
    #     self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
    #     self.msg.run_msg(item_no, "AssetImportSync")
    #     self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
    #     self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
    #     self.capital_mock.update_loanapplynew_success()
    #     self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
    #     self.capital_mock.update_loanapplyquery_success()
    #     self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
    #     check_asset_confirm(item_no, "LOAN_PRODUCT_CHANGE", 2)
    #     self.msg.run_msg(item_no, "UserLoanConfirmNotifyMQ")
    #     self.task.run_task(item_no, "AssetConfirmOverTimeCheck", excepts={"code": 0})
    #     check_wait_change_capital_data(item_no, 10005, "确认类型\\[LOAN_PRODUCT_CHANGE\\]已超时", 'UserConfirmTimeOutEvent')
    #     self.capital_mock.update_loancancel_fail()
    #     self.task.run_task(item_no, "LoanGrantStatusPush", excepts={"code": 1})
    #     # case跑完恢复配置
    #     update_gbiz_capital_yixin_rongsheng()
