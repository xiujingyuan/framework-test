from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.daxinganling_zhongyi import DaxinganlingZhongyiMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_daxinganling_zhongyi_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no, \
    update_router_capital_plan_amount, update_all_channel_amount

from biztest.util.tools.tools import get_four_element


@pytest.mark.gbiz_auto_test
@pytest.mark.gbiz_daxinganling_zhongyi
class TestDaxinganlingZhongyi(BaseTestCapital):
    def init(self):
        super(TestDaxinganlingZhongyi, self).init()
        self.channel = "daxinganling_zhongyi"
        self.capital_mock = DaxinganlingZhongyiMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_daxinganling_zhongyi()
        update_gbiz_capital_daxinganling_zhongyi_const()
        update_all_channel_amount()

    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
        # 没有开户查询接口
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
        self.capital_mock.update_protocol_sms_success()
        sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way='daxinganling_zhongyi', step_type='PROTOCOL',
                                  seq='')[
            'data']['actions'][0]['extra_data']['seq']
        self.capital_mock.update_protocol_confirm_success()
        capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way='daxinganling_zhongyi', step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query_success(item_no, asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        time.sleep(5)
        # 还款计划查询与合同下载都是使用的放款查询接口，缓存回来的结果，除非缓存失效，否则全部使用缓存的结果，所以还款计划和合同下载一般情况下不会再调用接口
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.capital_mock.update_repay_plan_push_success()
        self.task.run_task(item_no, "CapitalRepayPlanPush", excepts={"code": 0})
        wait_biz_asset_appear(item_no)
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.capital_mock.update_contractpush_success(item_no)
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)

    @pytest.mark.gbiz_loan_success
    @pytest.mark.gbiz_daxinganling_zhongyi_loan_success
    @pytest.mark.parametrize("app, source_type, count",
                             [
                                 ("草莓", "apr36", 12),
                                 # ("香蕉", "irr36", 12),
                                 # ("火龙果", "real36", 12),
                                 # ("草莓", "apr36_huaya", 12),  # 花鸭只能草莓进件
                                 # ("火龙果", "irr36_rongshu", 12),
                             ])
    def test_daxinganling_zhongyi_loan_success(self, case, app, source_type, count):
        """
        放款成功
        :param four_element:
        :param case:
        :param count:
        :return:
        """
        self.four_element = get_four_element(id_num_begin="43")
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 13000, app, source_type)
        self.register(item_no, self.four_element)
        self.loan_to_success(item_no)
        #check_asset_tran_data(item_no)
        # 小单部分
        noloan_item_no_lt = common_noloan_import(asset_info, irr_rongdan_noloan=False)
        for noloan_item_no in noloan_item_no_lt:
            self.noloan_to_success(noloan_item_no)

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_daxinganling_zhongyi_canloan_fail(self, case, app, source_type, period):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 5000, app, source_type)
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
        update_router_capital_plan_amount(3333333333, today, self.channel)
        check_wait_change_capital_data(item_no, 4, "daxinganling_zhongyi->校验资金量失败;", "AssetCanLoanFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_daxinganling_zhongyi_apply_fail(self, case, app, source_type, period):
        """
        LoanApplyNew 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="32")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_apply_fail()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query_fail(item_no)
        check_wait_change_capital_data(item_no, 1, "大兴安岭-中裔,订单提交\\(进件\\),返回code=1000,msg=mock 请求失败", "LoanApplySyncFailedEvent")


    @ pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_daxinganling_zhongyi_applyquery_fail(self, case, app, source_type, period):
        """
        LoanApplyQuery 失败切资方
        :param app:
        :param source_type:
        :param period:
        :return:
        """
        four_element = get_four_element(id_num_begin="12")
        item_no, asset_info = asset_import(self.channel, four_element, period, 6000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.capital_mock.update_loan_apply_query_fail(item_no)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 4040, "error_4040_内层mock 失败测试_null", "LoanApplyAsyncFailedEvent")

    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_dxalzy_callback_grant_success(self, case, app, source_type, period):
        """
        回调放款成功
        资产状态变更之后再次接收到放款成功回调
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        daxinganling_zhongyi_grant_callback_success(asset_info)
        time.sleep(5)
        self.task.run_task(item_no, "CapitalCallback", excepts={"code": 0})
        # 回调执行之后还会创建一个查询任务，因为查询任务才会修改alr/asset表的状态
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        #因为回调了放款成功，所以此处不处理查询的结果了
        self.capital_mock.update_loan_apply_query_success(item_no, asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 此时再次回调成功，不处理
        daxinganling_zhongyi_grant_callback_success(asset_info, key="Suc1"+get_random_str())
        # 因为回调没有mock还款计划，以下先做屏蔽处理
        # self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        # self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        # self.capital_mock.update_repay_plan_push_success()
        # self.task.run_task(item_no, "CapitalRepayPlanPush", excepts={"code": 0})
        # self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        # self.capital_mock.update_contractpush_success(item_no)
        # # self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        # self.task.run_task(item_no, "RongDanIrrTrial")
        # self.task.run_task(item_no, "CapitalDataNotify")
        # self.task.run_task(item_no, "GrantSuccessNotify")
        # self.msg.run_msg_by_order_no(item_no)


    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_dxalzy_callback_grant_fail(self, case, app, source_type, period):
        """
        回调放款失败，查询也是放款失败
        回调失败之后再次接收到失败的回调和成功的回调
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        time.sleep(5)
        daxinganling_zhongyi_grant_callback_fail(item_no)
        time.sleep(5)
        self.task.run_task(item_no, "CapitalCallback", excepts={"code": 0})
        # 回调执行之后还会创建一个查询任务，因为查询任务才会修改alr/asset表的状态
        self.capital_mock.update_loan_apply_query_fail(item_no) #回调失败，还是会以查询回来的结果为准，不会管回调的结果
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        #因为回调生成了查询任务，所以此处任务不做处理
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 4040, "error_4040_内层mock 失败测试_null", "LoanApplyAsyncFailedEvent")
        # 失败之后回调失败，不会生成任务
        daxinganling_zhongyi_grant_callback_fail(item_no)
        # 失败之后回调成功，属于异常场景 ，会报错：资方回调放款成功,但我方已为放款失败,请注意，不会生成任务
        daxinganling_zhongyi_grant_callback_success(asset_info)

    @pytest.mark.gbiz_daxinganling_zhongyi1
    @pytest.mark.parametrize("app, source_type, period", [("香蕉", "apr36", 12)])
    def test_dxalzy_callback_fail_query_success(self, case, app, source_type, period):
        """
        回调放款失败之后，但是查询到放款成功，按放款成功处理
        回调成功之后，再次回调失败/回调成功
        """
        four_element = get_four_element(id_num_begin="22")
        item_no, asset_info = asset_import(self.channel, four_element, period, 10000, app, source_type)
        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.capital_mock.update_loan_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        daxinganling_zhongyi_grant_callback_fail(item_no)
        time.sleep(5)
        self.task.run_task(item_no, "CapitalCallback", excepts={"code": 0})
        # 回调执行之后还会创建一个查询任务，因为查询任务才会修改alr/asset表的状态
        self.capital_mock.update_loan_apply_query_success(item_no, asset_info)#回调失败，还是会以查询回来的结果为准，不会管回调的结果
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        # 因为回调生成了查询任务，所以此处任务不做处理
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        self.capital_mock.update_repay_plan_push_success()
        self.task.run_task(item_no, "CapitalRepayPlanPush", excepts={"code": 0})
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.capital_mock.update_contractpush_success(item_no)
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        self.task.run_task(item_no, "CapitalDataNotify")
        self.task.run_task(item_no, "GrantSuccessNotify")
        self.msg.run_msg_by_order_no(item_no)
        # 放款成功之后再回调成功-----会生成回调任务
        daxinganling_zhongyi_grant_callback_success(asset_info, key="Suc2"+get_random_str())
        self.task.run_task(item_no, "CapitalCallback", excepts={"code": 0})
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        time.sleep(5)
        # 放款成功之后再回调失败，属于冲正场景 ，-----不处理，不生成任务，但是应该发送提示"资方回调放款失败,但我方已为放款成功,请注意"
        daxinganling_zhongyi_grant_callback_fail(item_no)



