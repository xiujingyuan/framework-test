# from biztest.config.gbiz.gbiz_kv_config import *
import pytest


class TestRun(object):
    @pytest.fixture(scope="function", params=[4, 5, 6])
    def case(self, request):
        ret = request.param
        yield
        print('yield start')
        print('yield end')

    @pytest.mark.testcase
    def test_run_cases1(self, case):
        """
        :param case: 本次执行的用例内容，类FinlabCase的一个实例
        :return:{0}
        """.format(case)
        print('aaaa')
        print(case)
        # update_gbiz_repay_plan_config()
        # update_biz_capital_paydayloan_list()
        # update_capital_order_period_loan_channel()
        # update_loan_condition_channels()
        # update_loan_condition_channels_from_system()
        # update_capital_allow_period_loan_channel()

    @pytest.mark.testcase
    def test_run_cases2(self, case):
        """
        :param case: 本次执行的用例内容，类FinlabCase的一个实例
        :return:{0}
        """.format(case)
        print('bbb')
        print(case)
        # update_gbiz_repay_plan_config()
        # update_biz_capital_paydayloan_list()
        # update_capital_order_period_loan_channel()
        # update_loan_condition_channels()
        # update_loan_condition_channels_from_system()
        # update_capital_allow_period_loan_channel()


if __name__ == "__main__":
    pass
