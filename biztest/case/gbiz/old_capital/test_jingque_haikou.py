from biztest.function.biz.biz_db_function import wait_biz_asset_appear
from biztest.function.gbiz.gbiz_db_function import update_router_capital_plan_amount
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.jingque_haikou import JingqueHaikouMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.function.gbiz.gbiz_common_function import *
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import time
import pytest
from biztest.util.tools.tools import get_four_element


class TestJingQueHaiKou(BaseTestCapital):
    """
      gbiz_jingque_haikou
      author: zhimengxue
      date: 20210119
      """


    def init(self):
        super(TestJingQueHaiKou, self).init()
        self.channel = "jingque_haikou"
        self.jingque_mock = JingqueHaikouMock(gbiz_mock)
        self.payment_mock = PaymentMock(gbiz_mock)
        update_gbiz_capital_jingque_haikou()
        update_gbiz_payment_config(self.jingque_mock.url)


    @pytest.fixture()
    def case(self):
        self.init()

    def register(self, item_no, four_element):
            self.jingque_mock.update_protocolquery_process()
            capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')
            self.jingque_mock.update_getsms_success()
            sms_seq = capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                                      action_type='GetSmsVerifyCode', way='jingque_haikou',
                                      step_type='PROTOCOL', seq='')[
                'data']['actions'][0]['extra_data']['seq']
            self.jingque_mock.update_protocol_success()
            capital_regiest(self.channel, four_element, item_no, from_system='strawberry',
                            action_type='CheckSmsVerifyCode', way='jingque_haikou', step_type='PROTOCOL',
                            seq=sms_seq)
            self.jingque_mock.update_protocolquery_success()
            capital_regiest_query(self.channel, four_element, item_no, from_system='strawberry')

    def loan_to_success(self, item_no):
        asset_info = get_asset_import_data_by_item_no(item_no)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.jingque_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.jingque_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.jingque_mock.update_applyquery_success(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        self.task.run_task(item_no, "RongDanIrrTrial")
        time.sleep(1)
        self.jingque_mock.update_repayplan_success(asset_info)
        self.task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        time.sleep(2)
        self.task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})
        wait_biz_asset_appear(item_no)
        self.jingque_mock.update_contractdown_success()
        self.task.run_task(item_no, "ContractDown", excepts={"code": 0})
        self.msg.run_msg_by_order_no(item_no)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_jingque_haikou
    @pytest.mark.gbiz_jingque_haikou_loan_success
    @pytest.mark.parametrize("count", [6, 12])
    def test_jingque_haikou_loan_success(self, case, count):
        """
        jingque_haikou放款成功
        :param four_element:
        :param case:
        :param count:
        :return:
        """
        self.four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, self.four_element, count, 5000, "香蕉", "", '')
        self.register(item_no, self.four_element)
        self.loan_to_success(item_no)
        check_asset_tran_data(item_no)
        # 小单部分
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
        self.noloan_to_success(item_no_noloan)

    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_jingque_haikou
    @pytest.mark.parametrize("count", [6, 12])
    def test_jingque_haikou_canloan_fail(self, case, count):
        """
        canloan失败切换资金方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 8000, "香蕉", "", '', '110000')
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
        check_wait_change_capital_data(item_no, 4, "jingque_haikou->校验资金量失败;")


    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_jingque_haikou
    @pytest.mark.parametrize("count", [6, 12])
    def test_jiequehaikou_loan_fail(self, case, count):
        """
        放款失败切资方
        :param case:
        :param count:
        :return:
        """
        four_element = get_four_element()
        item_no, asset_info = asset_import(self.channel, four_element, count, 5000, "香蕉", "", '', '110000')

        self.register(item_no, four_element)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetImportSync")
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        prepare_attachment(self.channel, item_no)
        self.jingque_mock.update_apply_success()
        self.task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})
        self.jingque_mock.update_contractpush_success()
        self.task.run_task(item_no, "ContractPush", excepts={"code": 0})
        self.jingque_mock.update_applyquery_fail(asset_info)
        self.task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})
        check_wait_change_capital_data(item_no, 40, "放款失败")

