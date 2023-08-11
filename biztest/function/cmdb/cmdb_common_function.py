import numpy as np
import numpy_financial as npf
from biztest.interface.cmdb.cmdb_interface import cmdb_standard_calc_v6
from biztest.util.asserts.assert_util import Assert
from biztest.function.cmdb.cmdb_db_function import *
from biztest.util.tools.tools import quantize, get_date
import datetime, decimal
from dateutil.relativedelta import relativedelta
import calendar


def cacle_v1(total_amount, total_count, info):
    total_amount = -total_amount
    result = {}
    for count in range(1, total_count + 1):
        result[str(count)] = {}
        # 本金计算方法，前几期本金是息费总额减去利息，最后一期先算本金(剩余本金)， 后算利息
        if count != total_count:
            result[str(count)]["interest"] = \
                round(float(npf.ipmt(info["interest"]["计算规则"] / 12, count, total_count, total_amount)), 2)
            result[str(count)]["principal"] = \
                round(round(float(npf.pmt(info["interest"]["计算规则"] / 12, total_count, total_amount)), 2) - \
                      round(float(npf.ipmt(info["interest"]["计算规则"] / 12, count, total_count, total_amount)), 2), 2)
        else:
            result[str(count)]["principal"] = 0
            principal_tmp = 0
            for _, b in result.items():
                principal_tmp = principal_tmp + b["principal"]
            result[str(count)]["principal"] = round(-total_amount - principal_tmp, 2)
            result[str(count)]["interest"] = \
                round(round(float(npf.pmt(info["interest"]["计算规则"] / 12, total_count, total_amount)), 2) -
                      (-total_amount - principal_tmp), 2)

        # 计算剩余的费用
        for item, item_info in info.items():
            if item_info["计算方式"] == "等额本息":
                if item != "interest":
                    result[str(count)][item] = round(float(npf.ipmt(item_info["计算规则"] / 12, count, total_count, total_amount)), 2)
            # 等额本息差额，需要先减后进位
            elif item_info["计算方式"] == "等额本息差额":
                result[str(count)][item] = round(float(npf.pmt(item_info["计算规则"][0] / 12, total_count, total_amount) - \
                                                       npf.pmt(item_info["计算规则"][1] / 12, total_count, total_amount)), 2)
            elif item_info["计算方式"] == "倒减":
                if count != total_count:
                    temp = round(float(npf.pmt(info[item_info["计算规则"][0]]["计算规则"] / 12, total_count, total_amount)), 2)
                    for value in item_info["计算规则"][1:]:
                        temp = temp - result[str(count)][value]
                    result[str(count)][item] = round(temp, 2)
                else:
                    temp = round(float(npf.pmt(info[item_info["计算规则"][0]]["计算规则"] / 12, total_count, total_amount)), 2)
                    for value in item_info["计算规则"][1:]:
                        temp = temp - result[str(count)][value]
                    result[str(count)][item] = round(temp, 2)
            else:
                raise Exception("暂未实现该算法")
    # 将所有的值转化为分
    for key1, value1 in result.items():
        for key2, value2 in value1.items():
            result[key1][key2] = round(value2 * 100, 2)
    return result


def get_fee_info_by_period(rate_info, period_num):
    fee_info = {}
    for item in rate_info['data']['calculate_result']['principal']:
        if item['period'] == period_num:
            fee_info['principal'] = item['amount']
            fee_info['date'] = item['date']
    for item in rate_info['data']['calculate_result']['interest']:
        if item['period'] == period_num:
            fee_info['interest'] = item['amount']
    for fee_type, fee_lt in rate_info['data']['calculate_result']['fee'].items():
        for item in fee_lt:
            if item['period'] == period_num:
                fee_info[fee_type] = item['amount']
    return fee_info


def check_fee_info(rate_info, cacle_info):
    temp = {}
    for value in rate_info['data']['calculate_result']['principal']:
        temp[str(value['period'])] = {}
        temp[str(value['period'])]['principal'] = value['amount']
    for value in rate_info['data']['calculate_result']['interest']:
        temp[str(value['period'])]['interest'] = value['amount']
    if 'fee' in rate_info['data']['calculate_result'].keys():
        if 'service' in rate_info['data']['calculate_result']['fee'].keys():
            for value in rate_info['data']['calculate_result']['fee']['service']:
                temp[str(value['period'])]['service'] = value['amount']
        if 'technical_service' in rate_info['data']['calculate_result']['fee'].keys():
            for value in rate_info['data']['calculate_result']['fee']['technical_service']:
                temp[str(value['period'])]['technical_service'] = value['amount']
        if 'after_loan_manage' in rate_info['data']['calculate_result']['fee'].keys():
            for value in rate_info['data']['calculate_result']['fee']['after_loan_manage']:
                temp[str(value['period'])]['after_loan_manage'] = value['amount']
    Assert.assert_match_json(temp, cacle_info, "费率计算错误")


def parse_clear_day(clear_rule):
    """
    解析结清日规则
    :param clear_rule: D+ / D- / D$
    :return:
    """
    mode = clear_rule[:2]
    day_str = clear_rule[2:]
    if "D>" in day_str:
        day, offset = day_str.split("D>")
    else:
        day = day_str
        offset = 0
    return mode, int(day), int(offset)


def calc_repay_day_by_clear_rule(grant_day, period, month_clear_day, clear_day, p):
    """
    根据结清日规则计算还款日
    :param grant_day:
    :param period:
    :param month_clear_day:
    :param clear_day:
    :param p:
    :return:
    """
    if month_clear_day == "":
        month_clear_day = "D+0"
    if clear_day == "":
        clear_day = "D+0"

    if p == period:
        mode, day, offset = parse_clear_day(clear_day)
    elif p < period:
        mode, day, offset = parse_clear_day(month_clear_day)
    else:
        raise Exception("错误的期次->p")

    repay_day = grant_day
    if mode == "D+":
        repay_day = repay_day + relativedelta(days=+day)
    elif mode == "D-":
        repay_day = repay_day + relativedelta(days=-day)
    elif mode == "D$":
        if repay_day.day >= day:
            if offset == 0:
                repay_day = repay_day.replace(day=day)
            else:
                repay_day = repay_day.replace(day=offset).replace(month=repay_day.month+1)
    else:
        raise Exception("不支持的月结日/结清日规则->%s" % mode)

    return repay_day


def calc_same_day_of_repay_day(refer_day, p, is_end_of_month=False):
    """
    计算第p期的还款日
    :param refer_day:
    :param p:
    :param is_end_of_month: True-月底对日，False-对日
    :return:
    """
    p_repay_day = refer_day + relativedelta(months=+p)
    if is_end_of_month:
        # 如果基准日是月底，则还款日取月底日
        if refer_day.day == calendar.monthrange(refer_day.year, refer_day.month)[1]:
            p_repay_day = p_repay_day.replace(day=calendar.monthrange(p_repay_day.year, p_repay_day.month)[1])
    return p_repay_day


def get_p_repay_day(grant_day, period, month_clear_day, clear_day, p, repay_date_formula):
    """
    获取第p期的还款日
    :param grant_day: 放款日
    :param period: 总期次
    :param month_clear_day: 月结日规则 D+ / D- / D$
    :param clear_day: 结清日规则 D+ / D- / D$
    :param p: 第几期
    :return: 第p期的还款日
    """
    if p == 0:
        return grant_day
    # 先计算基准日再取对日
    if repay_date_formula == "calDateThenSameDay":
        refer_day = calc_repay_day_by_clear_rule(grant_day, period, month_clear_day, clear_day, p)
        p_repay_day = calc_same_day_of_repay_day(refer_day, p)
    # 先计算基准日再取月底对日
    elif repay_date_formula == "calDateThenSameDayOfEOM":
        refer_day = calc_repay_day_by_clear_rule(grant_day, period, month_clear_day, clear_day, p)
        p_repay_day = calc_same_day_of_repay_day(refer_day, p, is_end_of_month=True)
    # 先取对日再计算还款日
    elif repay_date_formula == "sameDayThenCalDate":
        p_repay_day = calc_same_day_of_repay_day(grant_day, p)
        p_repay_day = calc_repay_day_by_clear_rule(p_repay_day, period, month_clear_day, clear_day, p)
    else:
        raise Exception("不支持的还款日算法->%s" % repay_date_formula)

    return p_repay_day


def get_comprehensive_fee(amount, period, rate_value, calculate_type, round_type='ROUND_HALF_EVEN', year_days=360,
                          month_clear_day='D+0', clear_day='D+0', grant_day=datetime.date.today(),
                          repay_date_formula="calDateThenSameDay"):
    """
    计算年化综合息费总额
    :param amount: 本金，单位分
    :param period: 期次
    :param rate_value: 利率，比如0.36
    :param calculate_type: 费用计算方式，acpi / acpi_v2 / acpi_v2_by_day / equal / equal_by_day / acpi_p1_by_day
    :return: 息费总额，单位分
    """
    comprehensive_fee = -1
    # 等额本息算法V1
    if calculate_type == 'acpi':
        pmt = quantize(str(npf.pmt(rate_value / 12, period, -amount)), round_type)
        comprehensive_fee = pmt * period
    # 等额本息（首期按天计息）算法
    if calculate_type == 'acpi_p1_by_day':
        pmt = quantize(str(npf.pmt(rate_value / 12, period, -amount)), round_type)
        p1_interest = quantize(amount * rate_value / 12, round_type)
        p1_days = (get_p_repay_day(grant_day, period, month_clear_day, clear_day, 1, repay_date_formula) -
                       get_p_repay_day(grant_day, period, month_clear_day, clear_day, 0, repay_date_formula)).days
        p1_interest_by_day = quantize(amount * rate_value / year_days * p1_days, round_type)
        comprehensive_fee = pmt * period - p1_interest + p1_interest_by_day
    # 等额本息算法V2
    elif calculate_type == 'acpi_v2':
        pmt = quantize(str(npf.pmt(rate_value / 12, period, -amount)), round_type)
        principal_rest = amount
        high_precision_interest_lt = []
        interest_lt = []
        principal_lt = []
        for p in range(1, period + 1):
            high_precision_interest = principal_rest * rate_value / 12
            interest = quantize(high_precision_interest + decimal.Decimal(np.sum(high_precision_interest_lt) - np.sum(interest_lt)), round_type)
            if p == period:
                principal = principal_rest
            else:
                principal = pmt - interest
            principal_rest -= principal
            high_precision_interest_lt.append(high_precision_interest)
            interest_lt.append(interest)
            principal_lt.append(principal)
        comprehensive_fee = np.sum(interest_lt) + np.sum(principal_lt)
    # 等额本息v2(按天计息)
    elif calculate_type == "acpi_v2_by_day":
        pmt = quantize(str(npf.pmt(rate_value / 12, period, -amount)), round_type)
        principal_rest = amount
        high_precision_interest_lt = []
        interest_lt = []
        principal_lt = []
        for p in range(1, period + 1):
            period_days = (get_p_repay_day(grant_day, period, month_clear_day, clear_day, p, repay_date_formula) -
                           get_p_repay_day(grant_day, period, month_clear_day, clear_day, p-1, repay_date_formula)).days
            high_precision_interest = principal_rest * rate_value / year_days * period_days
            interest = quantize(high_precision_interest + decimal.Decimal(np.sum(high_precision_interest_lt) - np.sum(interest_lt)), round_type)
            if p == period:
                principal = principal_rest
            else:
                principal = pmt - interest
            principal_rest -= principal
            high_precision_interest_lt.append(high_precision_interest)
            interest_lt.append(interest)
            principal_lt.append(principal)
        comprehensive_fee = np.sum(interest_lt) + np.sum(principal_lt)
    # 等本等息算法
    elif calculate_type == "equal":
        interest = quantize(amount * rate_value, round_type)
        comprehensive_fee = amount + interest
    # 等本等息按天
    elif calculate_type == "equal_by_day":
        period_days = (get_p_repay_day(grant_day, period, month_clear_day, clear_day, period, repay_date_formula) -
                       get_p_repay_day(grant_day, period, month_clear_day, clear_day, 0, repay_date_formula)).days
        interest = quantize(amount * rate_value / year_days * period_days, round_type)
        comprehensive_fee = amount + interest
    else:
        print("暂不支持%s算法" % calculate_type)
        pass

    return comprehensive_fee


def adjust_cmdb_tran(tran, adjust_type):
    """
    修正还款计划，仅适用于：fee中只含reserve、consult的费率编号
    :param tran:
    :param adjust_type:
    :return:
    """
    period_count = tran['data']['calculate_conditions']['data']['period_count']
    adjust_data_lt = []
    for x in range(period_count):
        fee_info = {
            "period": x + 1,
            "principal": tran['data']['calculate_result']['principal'][x]['amount'],
            "interest": tran['data']['calculate_result']['interest'][x]['amount'],
            "fee": {
                "reserve": tran['data']['calculate_result']['fee']['reserve'][x]['amount'],
                "consult": tran['data']['calculate_result']['fee']['consult'][x]['amount']
            },
            "total": tran['data']['calculate_result']['principal'][x]['amount']
                     + tran['data']['calculate_result']['interest'][x]['amount']
                     + tran['data']['calculate_result']['fee']['reserve'][x]['amount']
                     + tran['data']['calculate_result']['fee']['consult'][x]['amount']
        }
        adjust_data_lt.append(fee_info)
    # 0: 不修正
    if adjust_type == 0:
        adjust_data_lt[0].pop('fee')
        adjust_data_lt[0].pop('total')
    # 1: 传入本息，第1期利息+10
    elif adjust_type == 1:
        adjust_data_lt[0].pop('fee')
        adjust_data_lt[0].pop('total')
        adjust_data_lt[0]['interest'] += 10
    # 2: 传入本息费，第1期费用-10
    elif adjust_type == 2:
        adjust_data_lt[0].pop('total')
        adjust_data_lt[0]['fee'].pop('consult')
        adjust_data_lt[0]['fee']['reserve'] -= 10
    # 3: 传入本息费（倒减项费用也传入），第1期倒减项费用-20
    elif adjust_type == 3:
        adjust_data_lt[0].pop('total')
        adjust_data_lt[0]['fee']['consult'] -= 20
    # 4: 传入本息+total，第1期息+10，total+20
    elif adjust_type == 4:
        adjust_data_lt[0].pop('fee')
        adjust_data_lt[0]['interest'] += 10
        adjust_data_lt[0]['total'] += 20

    return adjust_data_lt


def check_adjusted_tran(tran_before, tran_after, type):
    """
    检查修正后的还款计划是否正确
    :param tran_before:
    :param tran_after:
    :param type:
    :return:
    """
    tran_before = tran_before['data']['calculate_result']
    tran_after = tran_after['data']['calculate_result']
    # 0: 不修正
    if type == 0:
        check_tran_equal(tran_before, tran_after)
    # 1: 传入本息，第1期利息+10
    elif type == 1:
        tran_before['interest'][0]['amount'] += 10
        tran_before['fee']['consult'][0]['amount'] -= 10
        check_tran_equal(tran_before, tran_after)
    # 2: 传入本息费，第1期费用-10，差值调整到倒减项费用+10
    elif type == 2:
        tran_before['fee']['reserve'][0]['amount'] -= 10
        tran_before['fee']['consult'][0]['amount'] += 10
        check_tran_equal(tran_before, tran_after)
    # 3: 传入本息费（倒减项费用也传入），第1期倒减项费用-20，没有修正空间，预期不修正
    elif type == 3:
        tran_before['fee']['consult'][0]['amount'] -= 20
        check_tran_equal(tran_before, tran_after)
    # 4: 传入本息+total，息有差异，total也有差异，第1期息+10，total+20，差值调整到倒减项费（consult+10）
    elif type == 4:
        tran_before['interest'][0]['amount'] += 10
        tran_before['fee']['consult'][0]['amount'] += 10
        check_tran_equal(tran_before, tran_after)


def check_tran_equal(tran_1, tran_2):
    for x in range(len(tran_1['principal'])):
        Assert.assert_equal(tran_1['principal'][x]['amount'], tran_2['principal'][x]['amount'], '费用不等')
        Assert.assert_equal(tran_1['interest'][x]['amount'], tran_2['interest'][x]['amount'], '费用不等')
        for fee in tran_1['fee'].keys():
            Assert.assert_equal(tran_1['fee'][fee][x]['amount'], tran_2['fee'][fee][x]['amount'], '费用不等')


def get_comprehensive_fee_by_standard_calc_v6(principal_amount, period_count, period_type, period_term, interest_rate,
                                              repay_type, interest_year_type, month_clear_day, clear_day, sign_date, repay_date_formula):
    cmdb_tran = cmdb_standard_calc_v6(principal_amount, period_count, period_type, period_term, interest_rate,
                                      repay_type, interest_year_type, month_clear_day, clear_day, sign_date, repay_date_formula)
    total_interest = 0
    for item in cmdb_tran['data']['calculate_result']['interest']:
        total_interest += item['amount']
    total_amount = principal_amount + total_interest
    return total_amount


def get_total_amount(calc_type, principal_amount, period_count, period_type="month", period_term=1, interest_rate=36,
                     year_days=360, month_clear_day="D+0", clear_day="D+0", sign_date=get_date(fmt="%Y-%m-%d"),
                     repay_date_formula="calDateThenSameDay"):
    """
    通过cmdb标准计算接口计算总费用
    :param calc_type: apr / aprByDay / irr / irrByDay
    :param principal_amount:
    :param period_count:
    :param period_type:
    :param period_term:
    :param interest_rate:
    :param year_days:
    :param month_clear_day:
    :param clear_day:
    :param sign_date:
    :param repay_date_formula:
    :return:
    """
    repay_type = ""
    if calc_type == "apr":
        repay_type = "equal"
    elif calc_type == "irr":
        repay_type = "acpi"
    elif calc_type == "aprByDay":
        repay_type = "equal_by_day"
    elif calc_type == "irrByDay":
        repay_type = "acpi_v2_by_day"

    interest_year_type = "{}per_year".format(year_days)
    comprehensive_fee = get_comprehensive_fee_by_standard_calc_v6(principal_amount, period_count, period_type, period_term, interest_rate,
                                                                  repay_type, interest_year_type, month_clear_day, clear_day, sign_date,
                                                                  repay_date_formula)
    return comprehensive_fee


if __name__ == '__main__':
    gc.init_env(1, "china", "dev")
    # p_repay_day = get_p_repay_day(datetime.date(2021, 10, 30), 6, "D-1", "D-1", 1)
    # print(get_comprehensive_fee(1000000, 12, decimal.Decimal(0.36), "equal_by_day", round_type='ROUND_HALF_EVEN', year_days=365, month_clear_day='D-1', clear_day='D-1'))
    # print(get_comprehensive_fee(500000, 6, decimal.Decimal(0.36), "equal_by_day", round_type='ROUND_HALF_EVEN', year_days=365, month_clear_day='D$24', clear_day='D$24', grant_day=datetime.datetime.strptime("2021-11-30", "%Y-%m-%d")))
    # print(get_comprehensive_fee(500000, 6, decimal.Decimal(0.36), "equal_by_day", round_type='ROUND_HALF_EVEN', year_days=365, month_clear_day='D$24', clear_day='D$24', grant_day=datetime.datetime.strptime("2021-11-24", "%Y-%m-%d")))
    # print(get_comprehensive_fee(500000, 6, decimal.Decimal(0.36), "equal", round_type='ROUND_HALF_EVEN', year_days=365, month_clear_day='D$24', clear_day='D$24', grant_day=datetime.datetime.strptime("2020-03-01", "%Y-%m-%d")))
    # print(get_comprehensive_fee(1000000, 12, decimal.Decimal(0.36), "equal_by_day", round_type='ROUND_HALF_EVEN', year_days=365, month_clear_day='D+0', clear_day='D+0'))
    fee = get_comprehensive_fee(1000000, 12, decimal.Decimal(36)/100, "acpi_p1_by_day", round_type='ROUND_HALF_EVEN', year_days=365, month_clear_day="D+1", clear_day="D+1", grant_day=datetime.datetime.strptime("2021-09-30", "%Y-%m-%d"))
    print(fee)