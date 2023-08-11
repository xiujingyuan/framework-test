from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital

from biztest.function.global_gbiz.gbiz_global_check_function import check_asset_data, check_withdraw_data, \
    check_sendmsg_exist, check_wait_assetreverse_data
from biztest.function.global_gbiz.gbiz_global_db_function import get_task_by_item_no_and_task_type, get_order_no, \
    get_withdraw_order_by_item_no, update_withdraw_order, update_task_by_item_no_task_type, update_all_channel_amount
from biztest.util.db.db_util import DataBase
from biztest.config.global_gbiz.global_gbiz_kv_config import update_gbiz_payment_config, update_gbiz_capital_channel
from biztest.util.tools.tools import get_calc_date_base_today
from biztest.util.asserts.assert_util import Assert
import pytest


@pytest.mark.global_gbiz_thailand
@pytest.mark.global_gbiz_mexico
@pytest.mark.global_gbiz_philippines
@pytest.mark.global_gbiz_pakistan
@pytest.mark.global_gbiz_withdraw
class TestWithdraw(BaseTestCapital):
    @classmethod
    def teardown_method(cls):
        update_gbiz_payment_config()
        DataBase.close_connects()

    def setup(self):
        # 用例初始化，每个用例执行之前执行，避免脏数据
        super(TestWithdraw, self).init()
        update_all_channel_amount()

    def test_global_withdraw_query_success(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        check_withdraw_data(item_no, "ready", "ready")
        self.mock.update_withdraw_apply_process()

        # PaymentWithdraw相关数据检测
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")
        self.mock.update_withdraw_query_status(asset_info, "process", "process")
        self.task.run_task(item_no, "PaymentWithdrawQuery",
                           excepts={"code": 2, "message": r"资产\[.*w\],代付订单号\[.*\],代付查询为处理中,"
                                                          r"继续重试查询,返回code\[2-E20002\],message\[Transfer request.*"})
        check_withdraw_data(item_no, "process", "process")

        # PaymentWithdrawQuery 未匹配到策略
        self.mock.update_withdraw_query_status(asset_info, "success", "success", False, "test", "test")
        self.task.run_task(item_no, "PaymentWithdrawQuery",
                           excepts={"code": 2, "message": r"未能匹配到任务\[PaymentWithdrawQuery\]的完成策略，"
                                                          r"平台返回错误码\[0-test\]，错误信息\[test\]，任务已terminated，请关注并尽快手动处理!"})
        check_withdraw_data(item_no, "process", "process")
        update_task_by_item_no_task_type(item_no, "PaymentWithdrawQuery", task_status="open")

        self.mock.update_withdraw_query_status(asset_info, "success", "success", False, "test")
        self.task.run_task(item_no, "PaymentWithdrawQuery",
                           excepts={"code": 2, "message": r"未能匹配到任务\[PaymentWithdrawQuery\]的完成策略，"
                                                          r"平台返回错误码\[0-test\]，错误信息\[Transfer completed"})
        check_withdraw_data(item_no, "process", "process")
        update_task_by_item_no_task_type(item_no, "PaymentWithdrawQuery", task_status="open")

        self.mock.update_withdraw_query_status(asset_info, "success", "success", False, "E20000", "test")
        self.task.run_task(item_no, "PaymentWithdrawQuery",
                           excepts={"code": 2, "message": r"未能匹配到任务\[PaymentWithdrawQuery\]的完成策略，"
                                                          r"平台返回错误码\[0-E20000\]，错误信息\[test\]，"
                                                          r"任务已terminated，请关注并尽快手动处理!"})
        check_withdraw_data(item_no, "process", "process")
        update_task_by_item_no_task_type(item_no, "PaymentWithdrawQuery", task_status="open")

        # PaymentWithdrawQuery 返回放款成功
        self.mock.update_withdraw_query_status(asset_info, "success", "success", False)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 0, "message": r"资产\[.*\],代付成功"})
        check_withdraw_data(item_no, "success", "success")
        check_sendmsg_exist(item_no, "PaymentWithdrawSuccess")

        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalDataNotify", excepts={"code": 0})
        self.task.run_task(item_no, "GrantSuccessNotify", excepts={"code": 0})
        # self.msg.run_msg_by_order_no(item_no)

        # 放款数据检查
        check_asset_data(asset_info)

    def test_global_withdraw_callback_success(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")

        order_no = get_withdraw_order_by_item_no(asset_info['data']['asset']['item_no'] + 'w')[-1][
            "withdraw_order_no"]
        self.mock.update_withdraw_query_status(asset_info, "success", "success")
        self.mock.set_withdraw_callback_success(item_no)

        self.task.run_task_by_order_no(item_no)
        check_withdraw_data(item_no, "success", "success")

        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery", 1)
        Assert.assert_equal(task_info["task_memo"], r"资产[%sw],代付成功" % item_no, "memo不正确")
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery", 2)
        Assert.assert_equal(task_info["task_memo"],
                            r"资产[%s],代付订单号[%s],检查本地代付订单状态为[success],与检查状态[process]不匹配" % (item_no, order_no),
                            "memo不正确")

        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})

        # 放款数据检查
        check_asset_data(asset_info)

    def test_global_withdraw_callback_reverse(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")
        self.mock.update_withdraw_query_status(asset_info, "success", "success")
        self.mock.set_withdraw_callback_success(item_no)
        self.task.run_task_by_order_no(item_no)
        check_withdraw_data(item_no, "success", "success")
        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        self.task.run_task(item_no, "CapitalRepayPlanGenerate", excepts={"code": 0})
        # 冲正回调
        self.mock.set_withdraw_callback_reverse(item_no)
        check_withdraw_data(item_no, "fail", "fail")
        check_wait_assetreverse_data(item_no, code=14, message="发生冲正,作废资产")

    def test_global_withdraw_query_fail(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")

        self.mock.update_withdraw_query_status(asset_info, "fail", "fail")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        check_withdraw_data(item_no, "fail", "fail")

    def test_global_withdraw_apply_fail(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_fail()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 1})
        check_withdraw_data(item_no, "fail", "fail", "1", "风险交易: 疑似重复放款")

    def test_global_withdraw_retry_amount_not_enough(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_balance_not_enouth()
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 2})
        check_withdraw_data(item_no, "ready", "ready")

        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdraw")
        Assert.assert_match(task_info["task_memo"],
                            r"资产\[%s\],代付账户余额查询,返回最大余额通道\[.*\]可用金额\[10\]小于本次代付金额\[.*\],延迟代付" % item_no,
                            "memo不正确")
        Assert.assert_equal(task_info["task_status"], "open", "status不正确")
        self.mock.update_withdraw_balance_enough()

    def test_global_withdraw_retry_beyond_warn_amount(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        update_gbiz_payment_config(self.mock.url, 20000000000)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 2})
        check_withdraw_data(item_no, "ready", "ready")

        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdraw")
        Assert.assert_match(task_info["task_memo"], r"资产\[%s\],查询到.*的可用余额\[.*\],已小于预警值\[.*\],延迟代付" % item_no,
                            "memo不正确")
        Assert.assert_equal(task_info["task_status"], "open", "status不正确")

    def test_global_withdraw_skip_amount_check(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_balance_not_enouth()
        update_gbiz_payment_config(self.mock.url, 20000000000, True)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")
        self.mock.update_withdraw_balance_enough()

    def test_global_withdraw_query_terminated(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")

        order_no = get_order_no(item_no + "w")
        self.mock.update_withdraw_query_not_exist()
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        check_withdraw_data(item_no, "ready", "void")

        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery")
        Assert.assert_equal(task_info["task_memo"],
                            r"资产[%s],代付订单号[%s],代付查询为[交易不存在],请人工核对!返回code[3],message[交易不存在]" % (item_no, order_no),
                            "memo不正确")
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawNew")
        Assert.assert_equal(task_info["task_status"], "terminated", "status不正确")
        check_withdraw_data(item_no, "ready", "void")

    def test_global_withdraw_query_retry(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")

        order_no = get_order_no(item_no + "w")
        self.mock.update_withdraw_query_status(asset_info, "fail", "fail", True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery")
        Assert.assert_match(task_info["task_memo"], r"资产\[%sw\],代付订单号\[%s\],代付查询为失败,延迟至\[.*\]创建下次代付,"
                                                    r"错误码\[1-rejected\],错误消息\[Payout failed. Reinitiate transfer "
                                                    r"after 30 min.\]" % (item_no, order_no), "memo不正确")
        check_withdraw_data(item_no, "ready", "fail")

        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawNew")
        Assert.assert_equal(task_info["task_status"], "open", "status不正确")

    def test_global_withdraw_query_final_fail_to_change_capital(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")

        self.mock.update_withdraw_query_status(asset_info, "fail", "fail", False)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery")
        Assert.assert_match(task_info["task_memo"], r"资产\[%sw\],代付失败为最终失败消息,错误码\[1-KN_RISK_CONTROL\],错误消息\[Risk"
                                                    r" control intercepts and exceeds trading limits\]" % item_no,
                            "memo不正确")
        check_withdraw_data(item_no, "fail", "fail")

        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        task_info = get_task_by_item_no_and_task_type(item_no, "ChangeCapital")
        Assert.assert_match(task_info["task_status"], "terminated", "memo不正确")

    def test_global_withdraw_query_final_fail_to_change_card(self):
        """
        目前只有菲律宾支持换卡，菲律宾资方case中已包含各种换卡场景，此处不再多写，如果后期其他国家也支持换卡，可以单独拎出来写
        :return:
        """
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")

        self.mock.update_withdraw_query_status(asset_info, "fail", "fail", platform_code="KN_INVALID_ACCOUNT",
                                               platform_message="Invalid account, please check it")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery")
        Assert.assert_match(task_info["task_memo"],
                            r"资产\[%sw\],代付失败为最终失败消息,错误码\[1-KN_INVALID_ACCOUNT\],错误消息\["
                            r"Invalid account, please check it\]" % item_no,
                            "memo不正确")
        check_withdraw_data(item_no, "fail", "fail")
        update_gbiz_capital_channel(asset_info["data"]["asset"]["loan_channel"])
        self.task.run_task(item_no, "LoanConfirmQuery",
                           excepts={"code": 0, "message": "放款失败,需换卡"})

    def test_global_withdraw_query_fail_max_to_change_capital(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")

        self.mock.update_withdraw_query_status(asset_info, "fail", "fail", True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        order_no = get_order_no(item_no + "w")
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery")
        Assert.assert_match(task_info["task_memo"], r"资产\[%sw\],代付订单号\[%s\],代付查询为失败,延迟至\[.*\]创建下次代付,"
                                                    r"错误码\[1-rejected\],错误消息\[Payout failed. Reinitiate transfer "
                                                    r"after 30 min.\]" % (item_no, order_no), "memo不正确")
        check_withdraw_data(item_no, "ready", "fail")

        self.task.run_task(item_no, "PaymentWithdrawNew", excepts={"code": 0})
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        self.mock.update_withdraw_query_status(asset_info, "fail", "fail", True)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery")
        Assert.assert_match(task_info["task_memo"], r"资产\[%sw\],payment代付,已超过最大允许的失败次数" % item_no, "memo不正确")
        check_withdraw_data(item_no, "fail", "fail", "rejected",
                            "Payout failed. Reinitiate transfer after 30 min.")

        self.task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        task_info = get_task_by_item_no_and_task_type(item_no, "ChangeCapital")
        Assert.assert_match(task_info["task_status"], "terminated", "memo不正确")

    def test_global_withdraw_query_fail_over_time(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")
        update_withdraw_order(item_no + "w", withdraw_order_create_at=get_calc_date_base_today(day=-2))
        self.mock.update_withdraw_query_status(asset_info, "fail", "fail", True, "E20001")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 1})
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery")
        Assert.assert_match(task_info["task_memo"], r"资产\[%sw\],payment代付,已超过最大允许代付时间" % item_no, "memo不正确")
        check_withdraw_data(item_no, "fail", "fail", "E20001", "Payout failed. Reinitiate transfer after 30 min.")

    def test_global_withdraw_diff_status1(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")

        self.mock.update_withdraw_query_status(asset_info, "success", "fail", False)
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 2})
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery")
        Assert.assert_match(task_info["task_memo"],
                            r"message:代付订单号\[%sw\],代付查询订单状态成功但明细没有一条成功.*" %
                            item_no, "memo不正确")
        Assert.assert_equal(task_info["task_status"], "open", "status不正确")
        check_withdraw_data(item_no, "process", "process")

    def test_global_withdraw_diff_status2(self):
        item_no, asset_info = self.asset_import_data()
        self.process_to_withdraw(item_no)
        self.mock.update_withdraw_apply_process()
        self.task.run_task(item_no, "PaymentWithdraw", excepts={"code": 0})
        check_withdraw_data(item_no, "process", "process")

        self.mock.update_withdraw_query_status(asset_info, "process", "process")
        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 2})
        check_withdraw_data(item_no, "process", "process")
        self.mock.update_withdraw_query_status(asset_info, "fail", "success", False)

        self.task.run_task(item_no, "PaymentWithdrawQuery", excepts={"code": 2})
        task_info = get_task_by_item_no_and_task_type(item_no, "PaymentWithdrawQuery")
        Assert.assert_match(task_info["task_memo"],
                            r"message:代付订单号\[%sw\],代付查询订单状态失败,但明细不全为失败.*" %
                            item_no, "memo不正确")
        Assert.assert_equal(task_info["task_status"], "open", "status不正确")
        check_withdraw_data(item_no, "process", "process")
