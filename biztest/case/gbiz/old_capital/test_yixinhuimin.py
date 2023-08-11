from biztest.function.gbiz.gbiz_check_function import check_asset_tran_data
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.msg.msg import GbizMsg
from biztest.util.task.task import GbizTask
from biztest.util.easymock.gbiz.yixin_huimin import YixinHuiminMock
from biztest.function.gbiz.gbiz_db_function import *
import time
import pytest
import common.global_const as gc


class TestYixinhuimin(object):
    """
       gbiz_yixinhuimin
       author: zhimengxue
       date: 20200401
       """
    @pytest.fixture()
    def case(self):
        # update_yxhm_paydayloan("5e60ce34d53ef1165b98251e")
        pass

    # 放款成功
    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_yixinhuimin
    # @pytest.mark.parametrize("count", [6])
    def test_yixinhuimin_success(self, case, count):
        task = GbizTask()
        msg = GbizMsg()
        four_element = get_four_element()
        item_no, asset_info = asset_import("yixin_huimin", four_element, count, 8000, "草莓", "")
        asset_import_noloan(asset_info)

        mock = YixinHuiminMock('zhizhi', '123456', "5e60ce34d53ef1165b98251e")

        task.run_task(item_no, "AssetImport", excepts={"code": 0})
        task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})

        mock.update_loanriskquery_success_1()
        mock.update_loanriskquery_success_2()
        task.run_task(item_no, "LoanRiskQuery", excepts={"code": 0})
        mock.update_loanapplynew_success()
        task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})

        msg.run_msg(item_no, "AssetImportSync", excepts={"code": 0})
        # 进件后，后置开户步骤
        mock.update_account_open_success(four_element)
        mock.update_bindcard_success(four_element)
        mock.update_account_auth_success()
        mock.update_protocol_success(four_element)
        capital_regiest_query("yixin_huimin", four_element, item_no)
        time.sleep(2)
        capital_regiest_query("yixin_huimin", four_element, item_no)
        time.sleep(8)
        # 进件后提现密验
        mock.update_verifyPasswd_success()
        postloan_confirm(asset_info)
        mock.update_verifyquery_success()
        task.run_task(item_no, "AssetConfirmQuery", excepts={"code": 0})

        mock.update_loanwait_success(asset_info)
        task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})

        mock.update_loanApplyconfirm_success()
        task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})

        mock.update_loanconfirmquery_success(asset_info)
        task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        mock.update_repay_plan(asset_info)
        task.run_task(item_no, "CapitalRepayPlanQuery", excepts={"code": 0})
        time.sleep(2)
        task.run_task(item_no, "OurRepayPlanRefine", excepts={"code": 0})

        msg.run_msg(item_no, "GrantCapitalAsset", excepts={"code": 0})
        msg.run_msg(item_no, "AssetWithdrawSuccess", excepts={"code": 0})
        # 小单部分
        item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info)
        task.run_task(item_no_noloan, "AssetImport", excepts={"code": 0})
        task.run_task(item_no, "AssetImport", excepts={"code": 0})

        task.run_task(item_no_noloan, "AssetImportVerify", excepts={"code": 0})
        task.run_task(item_no_noloan, "RefreshNoLoan", excepts={"code": 0})
        msg.run_msg(item_no_noloan, "AssetImportSync", excepts={"code": 0})
        time.sleep(4)
        msg.run_msg(item_no_noloan, "AssetSyncNotify", excepts={"code": 0})

        # 数据检查
        check_asset_tran_data(item_no)

    # 放款失败
    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_yixinhuimin
    # @pytest.mark.parametrize("count", [6])
    def test_yixinhuimin_fail(self, case, count):
        task = GbizTask()
        msg = GbizMsg()
        four_element = get_four_element()
        item_no, asset_info = asset_import("yixin_huimin", four_element, count, 6000, "草莓", "")
        asset_import_noloan(asset_info)

        mock = YixinHuiminMock('zhizhi', '123456', "5e60ce34d53ef1165b98251e")

        task.run_task(item_no, "AssetImport", excepts={"code": 0})
        task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})

        mock.update_loanriskquery_success_1()
        mock.update_loanriskquery_success_2()
        task.run_task(item_no, "LoanRiskQuery", excepts={"code": 0})
        mock.update_loanapplynew_success()
        task.run_task(item_no, "LoanApplyNew", excepts={"code": 0})

        msg.run_msg(item_no, "AssetImportSync", excepts={"code": 0})
        # 开户步骤
        mock.update_account_open_success(four_element)
        mock.update_bindcard_success(four_element)
        mock.update_account_auth_success()
        mock.update_protocol_success(four_element)
        capital_regiest_query("yixin_huimin", four_element, item_no)
        time.sleep(10)
        # 进件开户成功后提现密验
        mock.update_verifyPasswd_success()
        postloan_confirm(asset_info)
        mock.update_verifyquery_success()
        task.run_task(item_no, "AssetConfirmQuery", excepts={"code": 0})

        mock.update_loanwait_success(asset_info)
        task.run_task(item_no, "LoanApplyQuery", excepts={"code": 0})

        mock.update_loanApplyconfirm_success()
        task.run_task(item_no, "LoanApplyConfirm", excepts={"code": 0})
        mock.update_loanconfirmquery_fail(asset_info)
        task.run_task(item_no, "LoanConfirmQuery", excepts={"code": 0})
        time.sleep(2)

        # 判断切换资金方任务的状态，是open之后再执行
        item_no = (asset_info['data']['asset']['item_no'])
        sql = "select task_status from gbiz%s.task where task_order_no='%s' and task_type='ChangeCapital'" % \
              (gc.ENV, item_no)
        task_status = str(gc.GRANT_DB.query(sql)[0]["task_status"])
        if task_status == 'open':
            task.run_task(item_no, "ChangeCapital", excepts={"code": 0})
            msg.run_msg(item_no, "AssetChangeLoanChannel", excepts={"code": 0})
        else:
            return "切换资金方任务状态非open,现在任务的状态是" + str(task_status)


if __name__ == "__main__":
    pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/qnn_lm.py", "--env=9"])
