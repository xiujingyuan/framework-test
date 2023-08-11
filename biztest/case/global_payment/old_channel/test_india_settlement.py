import pytest

from biztest.config.payment_global.global_payment_kv_config import update_cashfree_reconci
from biztest.function.global_payment.global_payment_check_function import check_reconci_task, check_cashfree_reconci
from biztest.function.global_payment.global_payment_db_operation import delete_channel_reconci, \
    delete_channel_settlement, delete_task
from biztest.interface.payment_global.payment_global_interface import global_run_job, run_task, run_task_by_order_no
from biztest.util.db.db_util import DataBase
from biztest.util.easymock.global_payment.global_payment_cashfree import CashfreeMock
from biztest.util.tools.tools import get_date


class TestIndiaSettlement:
    def setup_class(self):
        self.sign_company = "yomoyo3"
        self.channel_name = "cashfree_%s_ebank" % self.sign_company
        self.cashfree_mock = CashfreeMock('18355257123', '123456', "5e9807281718270057767a3e")
        update_cashfree_reconci(self.sign_company, "5e9807281718270057767a3e")

    def teardown_class(self):
        update_cashfree_reconci(self.sign_company)
        DataBase.close_connects()

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_cashfree
    @pytest.mark.global_payment_cashfree_settlement
    def test_cashfree_ebank_nodata(self):
        init_order_no = self.channel_name + "_" + get_date(fmt="%Y-%m-%d")
        d_task_order_no = "d_%s_ebank_Settlement_%s" % (self.channel_name, get_date(fmt="%Y-%m-%d"))
        # 删除历史task
        for task in [init_order_no, d_task_order_no]:
            delete_task(task_order_no=task)
        # 更新对账单kv
        self.cashfree_mock.update_cashfree_reconic_total_nodata()
        self.cashfree_mock.update_cashfree_reconic_detail_nodata()
        # 调度对账job-下载对账单
        global_run_job("reconciTaskJob",
                       {"recon_date": get_date(fmt="%Y-%m-%d"),
                        "channel_name": self.channel_name})

        run_task(init_order_no, "reconciDownloadFile")
        run_task_by_order_no(d_task_order_no)

    @pytest.mark.global_payment_india
    @pytest.mark.global_payment_cashfree
    @pytest.mark.global_payment_cashfree_settlement
    def test_cashfree_ebank_settlement(self):
        init_order_no = self.channel_name + "_" + get_date(fmt="%Y-%m-%d")
        d_settlement_order_no = "d_%s_ebank_Settlement_%s" % (self.channel_name, get_date(fmt="%Y-%m-%d"))
        s_settlement_order_no = "s_%s_ebank_Settlement_%s" % (self.channel_name, get_date(fmt="%Y-%m-%d"))
        d_transaction_order_no = "d_%s_ebank_Transaction_%s" % (self.channel_name, get_date(fmt="%Y-%m-%d"))
        s_transaction_order_no = "s_%s_ebank_Transaction_%s" % (self.channel_name, get_date(fmt="%Y-%m-%d"))
        u_transaction_order_no = "u_%s_ebank_Transaction_%s" % (self.channel_name, get_date(fmt="%Y-%m-%d"))
        # 删除历史task
        for task in [init_order_no, d_settlement_order_no, s_settlement_order_no, d_transaction_order_no,
                     s_transaction_order_no, u_transaction_order_no]:
            delete_task(task_order_no=task)
        delete_channel_reconci(channel_reconci_settlement_id=262907)
        delete_channel_settlement(channel_settlement_settlement_id=262907)
        # 调度对账job-下载对账单
        global_run_job("reconciTaskJob",
                       {"recon_date": get_date(fmt="%Y-%m-%d"),
                        "channel_name": self.channel_name})

        # 下载结算账单
        self.cashfree_mock.update_cashfree_reconic_total_havadata()
        run_task(init_order_no, "reconciDownloadFile")
        run_task_by_order_no(d_settlement_order_no)
        run_task_by_order_no(s_settlement_order_no)
        self.cashfree_mock.update_cashfree_reconic_total_nodata()
        run_task_by_order_no(d_settlement_order_no)

        # 下载账单明细
        self.cashfree_mock.update_cashfree_reconic_detail_havedata(data_id=1)
        run_task(d_transaction_order_no, "reconciHttpBatchDownload")
        run_task_by_order_no(s_transaction_order_no)

        self.cashfree_mock.update_cashfree_reconic_detail_havedata(data_id=2)
        run_task(d_transaction_order_no, "reconciHttpBatchDownload")
        run_task_by_order_no(s_transaction_order_no)

        self.cashfree_mock.update_cashfree_reconic_detail_nodata()
        run_task(d_transaction_order_no, "reconciHttpBatchDownload")
        run_task(u_transaction_order_no, "reconciHttpBatchUpdateSettlement")

        # 检查数据
        check_reconci_task([init_order_no, d_settlement_order_no, s_settlement_order_no, d_transaction_order_no,
                            s_transaction_order_no, u_transaction_order_no])
        check_cashfree_reconci()

    # @pytest.mark.global_payment_india
    # @pytest.mark.global_payment_india_settlement
    # def test_razorpay_ebank_reconci_nodata(self):
    #     delete_channel_reconciandsettlement(self.db_test_payment, "setl_EVd17tCHzrE3NE")
    #     # 更新对账单kv
    #     global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
    #     global_payment_mock.update_razorpay_reconic_total_nodata()
    #     global_payment_mock.update_razorpay_reconic_detail_nodata()
    #     # 调度对账job-下载对账单
    #     global_job_run_reconci(india_razorpay_ebank_channel_name)
    #     # 通过调度job批量执行task
    #     update_global_task_next_run_at(self.db_test_payment)
    #     time.sleep(1)
    #     global_job_runtask(1)
    #     for i in range(3):
    #         update_global_task_next_run_at(self.db_test_payment)
    #         time.sleep(1)
    #         global_job_runtask(1)
    #     channel_reconci_info = get_channel_reconci_by_settlement_id(self.db_test_payment, "setl_EVd17tCHzrE3NE")
    #     channel_settlement_info = get_channel_settlement_by_settlement_id(self.db_test_payment, "setl_EVd17tCHzrE3NE")
    #     assert channel_reconci_info == (), "不会保存对账数据"
    #     assert channel_settlement_info == (), "不会保存对账数据"
    #
    # @pytest.mark.global_payment_india
    # @pytest.mark.global_payment_india_settlement
    # def test_razorpay_ebank_reconci_havadata(self):
    #     delete_channel_reconciandsettlement(self.db_test_payment, "setl_EVd17tCHzrE3NE")
    #     # 更新对账单kv
    #     global_payment_mock = RazorpayMock('18355257123', '123456', "5e9807281718270057767a3e")
    #     global_payment_mock.update_razorpay_reconic_total_havadata()
    #     global_payment_mock.update_razorpay_reconic_detail_havedata()
    #     # 调度对账job-下载对账单
    #     global_job_run_reconci(india_razorpay_ebank_channel_name)
    #     # 通过调度job批量执行task
    #     update_global_task_next_run_at(self.db_test_payment)
    #     time.sleep(2)
    #     global_job_runtask(1)
    #     for i in range(3):
    #         update_global_task_next_run_at(self.db_test_payment)
    #         time.sleep(3)
    #         global_job_runtask(1)
    #         global_payment_mock.update_razorpay_reconic_total_nodata()
    #     # 让对账单下载结束
    #     global_payment_mock.update_razorpay_reconic_detail_nodata()
    #     for i in range(3):
    #         update_global_task_next_run_at(self.db_test_payment)
    #         time.sleep(1)
    #         global_job_runtask(1)
    #     # 断言：检查保存的数据：jenkins环境跑总有问题，先不检查，TODO
    #     # assert_check_razorpay_channel_reconciandsettlement(self.db_test_payment)
