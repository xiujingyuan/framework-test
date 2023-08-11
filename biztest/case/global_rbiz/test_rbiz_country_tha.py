
from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.config.easymock.easymock_config import global_rbiz_mock
from biztest.config.global_rbiz.global_rbiz_interface_params_config import global_asset
from biztest.config.global_rbiz.global_rbiz_kv_config import update_tha_rbiz_paysvr_config, update_rbiz_decrease_config, \
    update_rbiz_refresh_fee_conf, update_rbiz_config
from biztest.function.global_gbiz.gbiz_global_db_function import get_borrower_from_asset_card, \
    get_loan_record_from_asset, get_trans_from_asset_tran, get_asset_from_asset
from biztest.function.global_rbiz.global_rbiz_common_function import asset_import_auto, asset_import_auto_no_loan
from biztest.function.global_rbiz.rbiz_global_check_function import *
from biztest.function.global_rbiz.rbiz_global_db_function import get_withhold_by_item_no
from biztest.interface.gbiz_global.gbiz_global_interface import asset_import
from biztest.interface.rbiz.rbiz_global_interface import paysvr_callback, trade_withhold, run_FoxAdvancePushJob_by_api

from biztest.util.db.db_util import DataBase
from biztest.util.easymock.payment_global import PaymentGlobalMock
from biztest.util.log.log_util import LogUtil
from biztest.util.task.task import TaskGlobal
from biztest.util.task.task import TaskGlobalRepay


class TestRbizthaPicocapitalPlus(BaseGlobalRepayTest):
    """
       picocp_ams1 repay
    """

    @classmethod
    def setup_class(cls):
        update_tha_rbiz_paysvr_config()
        update_asset_to_payoff_by_date()
        update_rbiz_config(auto_tolerance=True)
        cls.task = TaskGlobalRepay()
        cls.mock = PaymentGlobalMock(global_rbiz_mock)

    @classmethod
    def teardown_class(cls):
        DataBase.close_connects()
        update_tha_rbiz_paysvr_config()

    @pytest.fixture(scope="function")
    def setup(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass

        request.addfinalizer(teardown)
        update_tha_rbiz_paysvr_config()
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type,
                                                     self.four_element)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    @pytest.fixture(scope="function")
    def setup_4(self, request):
        def teardown():
            try:
                DataBase.close_connects()
            except Exception as e:
                print(e)
                pass

        request.addfinalizer(teardown)
        update_rbiz_refresh_fee_conf()
        update_rbiz_decrease_config(can_decrease_day=0)
        update_tha_rbiz_paysvr_config("5e46037fd53ef1165b98246e")
        self.four_element = get_four_element_global()
        self.item_no, asset_info = asset_import_auto(self.loan_channel, 7, self.from_system, self.from_app,
                                                     self.source_type, self.four_element, 4)
        self.item_no_x = asset_import_auto_no_loan(asset_info)

    @pytest.mark.global_rbiz_thailand_pico_plus
    def test_active_advance_repay(self, setup):
        """
        主动还款 - 提前还款
        """
        self.update_asset_due_at(-1)
        self.mock.update_withhold_autopay_ebank_url_success()
        # 发起主动代扣
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)

        self.mock.update_withhold_query_success(self.item_no, 2, "auto_thailand_channel")
        # 执行所有task
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        request_no = get_withhold_by_item_no(self.item_no)[0]["withhold_request_no"]
        self.task.run_task_by_order_no_count(request_no)
        self.task.run_task_by_order_no_count(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(order_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.item_no)
        self.msg.run_msg_by_id_and_search_by_order_no(self.four_element['data']["id_number_encrypt"])
        time.sleep(3)
        # 验证数据 代扣相关
        withhold = {
            "withhold_amount": 553500,
            "withhold_card_num": self.four_element['data']['card_num'],
            "withhold_payment_mode": "AUTOTEST",
            "withhold_channel": "auto_thailand_channel",
            "sign_company": "amberstar1",
            "repay_type": "advance"
        }
        check_asset_data(self.item_no, repaid_principal_amount=500000, repaid_interest_amount=3500,
                         repaid_amount=503500, asset_status="payoff")
        check_asset_data(self.item_no_x, repaid_principal_amount=50000, repaid_amount=50000, asset_status="payoff")
        check_withhold_success_data(order_no, **withhold)
        check_asset_tran_data(self.item_no)

    @pytest.mark.test_for_new_repay
    def test_for_new_repay(self):
        self.four_element = get_four_element_global()
        item_no, asset_info = asset_import(self.loan_channel, 4, 7, "day", 500000, "tha", "mango", "mileVIPstore_bill",
                                           self.four_element)
        gbiz_task = TaskGlobal()
        gbiz_task.run_task(item_no, "AssetImport", excepts={"code": 0})

        url = ""
        asset_info = deepcopy(global_asset)
        asset = get_asset_from_asset(item_no)
        trans = get_trans_from_asset_tran(item_no)
        loan_record = get_loan_record_from_asset(item_no)
        borrower = get_borrower_from_asset_card(item_no)
        asset_info["data"]['asset'] = asset[0]
        asset_info["key"] = item_no + get_random_str(3)
        if asset[0]['loan_channel'] != 'noloan':
            asset_info["data"]['loan_record'] = loan_record[0]
        asset_info["data"]['trans'].extend(trans)
        asset_info["data"]['borrower'] = borrower[0]

        resp = parse_resp_body(
            requests.request(method='post', url=url, headers={"content-type": "application/json"},
                             json=asset_info))
        LogUtil.log_info(f"放款成功资产同步rbiz成功，url:{url}, request：{item_no}，resp：{resp}")

    @pytest.mark.global_rbiz_thailand_pico_plus1
    def test_active_advance_repay111(self, setup_4):
        # 发起还款，但是还款失败
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no, period=1)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x, period=1)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount)
        self.update_asset_due_at(-1, period=1, refresh=True)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1, 2, 3, 4], delay_days=3,
                       four_element=self.four_element)
        self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2})
        self.update_asset_due_at(-5, period=1, refresh=True)

        self.repay_normal({"item_no": self.item_no, "amount": 0, "status": 2})


        self.update_asset_due_at(-1, period=2, refresh=True)

        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2, finished_at=get_date(day=-1))

        update_rbiz_config(need_decrease_late=True)
        trade_withhold(self.item_no, "asset_delay", 1500, "barcode", period_list=[1], delay_days=3,
                       four_element=self.four_element)
        merchant_key = \
            self.repay_trade({"item_no": self.item_no, "amount": 1500, "status": 2, "finish_at": get_date(day=-5)})
        # 逾期两天

        self.update_asset_due_at(-1, period=1, refresh=True)

        # 发起还款，但是还款失败
        project_num_loan_channel_amount = get_asset_tran_balance_amount_by_item_no(self.item_no, period=1)
        project_num_no_loan_amount = get_asset_tran_balance_amount_by_item_no(self.item_no_x, period=1)
        coupon_num = "coupon_" + get_random_str(10)
        resp_combo_active = self.combo_active_repay_apply(project_num_loan_channel_amount, project_num_no_loan_amount,
                                                          coupon_amount=6000, coupon_num=coupon_num)
        self.repay_normal({"item_no": self.item_no, "amount": 558000, "repay_type": "asset", "finish_at": get_date(), "status": 2})
        self.repay_collect({"item_no": self.item_no, "amount": 558000, "repay_type": "asset", "finish_at": get_date()})

        self.update_asset_due_at(-1, period=4, refresh=True)
        order_no = resp_combo_active["content"]["data"]["project_list"][0]["order_no"]
        paysvr_callback(order_no, 141100, 2, finished_at=get_date(day=-1))
        # paysvr_callback(order_no, 139863, 2, finished_at=get_date(day=-1))  # 减免
        # paysvr_callback(order_no, 139862, 2, finished_at=get_date(day=-1))  # 不减免



        # 回调成功
        # update_withhold(order_no, withhold_create_at=get_date(day=-4, timezone=get_tz()))
        # paysvr_callback(order_no, int(project_num_loan_channel_amount) + int(project_num_no_loan_amount), 2)
        self.run_all_task_after_repay_success()
        # 数据检查
        check_asset_data(self.item_no, repaid_principal_amount=125000, repaid_interest_amount=3500,
                         repaid_amount=128500, late_amount=500, balance_amount=386000, asset_status="repay")
        check_asset_data(self.item_no_x, repaid_principal_amount=12500,
                         repaid_amount=12500, late_amount=48, balance_amount=37548, asset_status="repay")