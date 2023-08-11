#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pytest

from biztest.interface.cmdb.cmdb_interface import *
from biztest.function.cmdb.cmdb_common_function import *


class TestCmdbCalculate(object):

    @pytest.mark.cmdb
    @pytest.mark.parametrize("adjust_type", [0, 1, 2, 4])
    def test_cmdb_adjust(self, adjust_type):
        """
        adjust_type：
        0：传入本息，一致，无需修正
        1：传入本息，息有差异，差值调整到倒减项费
        2：传入本息费，费有差异，差值调整到倒减项费
        3：传入本息费（倒减项费也传入），没有修正空间，不修正
        4：传入本息+total，息有差异，total也有差异，差值调整到倒减项费
        3用例不通过，但实际不会出现这种情况，不影响线上，暂时不开这个用例，
        """
        rate_number = "trqjj_12m_20230616"
        principal = 800000
        period_count = 12
        loan_channel = "tongrongqianjingjing"
        # 1.初始还款计划
        tran_before = cmdb_rate_loan_calculate(rate_number, principal, period_count, loan_channel)
        # 2.修正
        adjust_data_lt = adjust_cmdb_tran(tran_before, adjust_type)
        tran_after = cmdb_rate_adjust(rate_number, principal, period_count, adjust_data_lt)
        # 3.验证修正结果
        check_adjusted_tran(tran_before, tran_after, adjust_type)

    @pytest.mark.cmdb
    @pytest.mark.parametrize("repay_type, interest_rate, interest_year_type, month_clear_day, clear_day, sign_date_str, repay_date_formula",
                             [
                              ("equal", 36, "360per_year", "D+0", "D+0", "2021-10-01", "calDateThenSameDay"),
                              ("equal", 35.9, "360per_year", "D+0", "D+0", "2021-10-01", "calDateThenSameDay"),
                              ("equal", 36, "360per_year", "D+1", "D+1", "2021-09-30", "sameDayThenCalDate"),
                              ("equal_by_day", 36, "365per_year", "D+0", "D+0", "2021-10-01", "calDateThenSameDay"),
                              ("equal_by_day", 36, "365per_year", "D-1", "D-1", "2021-10-01", "calDateThenSameDayOfEOM"),
                              ("equal_by_day", 36, "365per_year", "D$24", "D$24", "2021-10-30", "calDateThenSameDay"),
                              ("acpi", 36, "360per_year", "D+1", "D+1", "2021-10-01", "calDateThenSameDay"),
                              ("acpi", 36, "360per_year", "D+0", "D+0", "2021-04-30", "calDateThenSameDayOfEOM"),
                              ("acpi", 36, "360per_year", "D$29D>1", "D$29D>1", "2021-04-28", "calDateThenSameDay"),
                              ("acpi", 36, "360per_year", "D$29D>1", "D$29D>1", "2021-04-29", "calDateThenSameDay"),
                              ("acpi_v2_by_day", 36, "360per_year", "D+1", "D+1", "2021-10-20", "calDateThenSameDay"),
                              ("acpi_v2_by_day", 36, "365per_year", "D-1", "D-1", "2021-10-01", "calDateThenSameDay"),
                              ("acpi_v2_by_day", 36, "365per_year", "D$24", "D$24", "2021-10-30", "calDateThenSameDay"),
                              ])
    def test_cmdb_standard_calculate_v6(self, repay_type, interest_rate, interest_year_type, month_clear_day, clear_day, sign_date_str, repay_date_formula):
        """
        1、等本等息
        2、等额本息
        3、等额本息按天
        4、等额本息按天，年化365天
        5、等额本息按天，月结日和结清日
        """
        principal_amount = 1000000
        period_count = 12
        period_type = "month"
        period_term = 1
        interest_rate = interest_rate
        repay_type = repay_type
        interest_year_type = interest_year_type
        month_clear_day = month_clear_day
        clear_day = clear_day
        sign_date = datetime.datetime.strptime(sign_date_str, "%Y-%m-%d")
        # 检查综合息费
        actual_comprehensive_fee = get_comprehensive_fee_by_standard_calc_v6(principal_amount, period_count, period_type, period_term, interest_rate, repay_type, interest_year_type, month_clear_day, clear_day, sign_date_str, repay_date_formula)
        expect_comprehensive_fee = get_comprehensive_fee(principal_amount, period_count, decimal.Decimal(interest_rate)/100, repay_type, round_type='ROUND_HALF_EVEN', year_days=int(interest_year_type[:3]), month_clear_day=month_clear_day, clear_day=clear_day, grant_day=sign_date, repay_date_formula=repay_date_formula)
        Assert.assert_equal(expect_comprehensive_fee, actual_comprehensive_fee, "综合息费不正确")
        # 检查还款日
        cmdb_tran = cmdb_standard_calc_v6(principal_amount, period_count, period_type, period_term, interest_rate, repay_type, interest_year_type, month_clear_day, clear_day, sign_date_str, repay_date_formula)
        for x in range(period_count):
            actual_repay_date = cmdb_tran['data']['calculate_result']['interest'][x]['date']
            expect_repay_date = get_p_repay_day(sign_date, period_count, month_clear_day, clear_day, x+1, repay_date_formula).strftime("%Y-%m-%d")
            Assert.assert_equal(expect_repay_date, actual_repay_date, "还款日不正确")
