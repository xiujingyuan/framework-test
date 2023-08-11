import unittest, pytest
import pandas as pd
from biztest.function.dcs.capital_database import get_final_all, get_db_time, get_pending_all, get_final_sum
from biztest.util.tools.tools import get_date_after, get_date_before_today
import common.global_const as gc


class CheckDcsFinal:
    def __init__(self, item_no, period, clearing_type, repay_channel, one_one_repay='N'):
        """
        :param item_no:  资产编号
        :param period:  期次，只能一期一期的来
        :param clearing_type:  还款还是代偿
        :param repay_channel:  还款或代偿的通道，代偿直接传qsq
        :param one_one_repay:  是否为一期一期的还款，不是就传N
        """
        self.env_test = gc.ENV
        self.item_no = item_no
        self.period = period
        self.clearing_type = clearing_type
        self.repay_channel = repay_channel
        self.one_one_repay = one_one_repay

    def assert_equal(self, excepts, actual, msg):
        unittest.TestCase().assertEqual(excepts, actual, msg)
        pass

    def check_final_all(self):
        final_all = get_final_all(self.item_no, self.period, self.clearing_type)
        print("###############", final_all, "###############")
        if not final_all:
            print("###############", get_db_time(), "###############")
            raise AssertionError('final无数据！')
        for final_i in range(0, len(final_all)):
            if final_all[final_i]["amount_type"] == "principal":
                final_principal = final_all[final_i]
        pending_all = get_pending_all(self.item_no, self.period, self.clearing_type)
        for pending_i in range(0, len(pending_all)):
            if pending_all[pending_i]["amount_type"] == "principal":
                pending_principal = pending_all[pending_i]
        # 1、检查 biz_type
        if self.clearing_type == 'compensate':
            self.assert_equal('compensate', final_principal["biz_type"], '代偿biz_type不正确')
            print("检查 biz_type 通过")
        else:
            self.assert_equal('repay', final_principal["biz_type"], '还款biz_type不正确')
            print("检查 biz_type 通过")
        # 2、检查 biz_sub_type ，因为有特殊逻辑，所以需要依赖 pending 的数据来判断还款类型
        if self.clearing_type == 'repay':
            if pending_principal["actual_finish_time"][:10] == pending_principal["expect_finish_time"][:10]:
                self.assert_equal('normal_repay', final_principal["biz_sub_type"], '正常还款类型不正确')
                print("检查 biz_sub_type 通过")
            elif pending_principal["actual_finish_time"][:10] < pending_principal["expect_finish_time"][:10]:
                self.assert_equal('advance_repay', final_principal["biz_sub_type"], '提前还款类型不正确')
                print("检查 biz_sub_type 通过")
            else:
                self.assert_equal('overdue_repay', final_principal["biz_sub_type"], '逾期还款类型不正确')
                print("检查 biz_sub_type 通过")
        # 3、检查是否为代偿后还款
        advance_compensate_list = ["lianlian", "baijin", "xingrui", "xingruinew"]
        d4_list = ["hami_tianshan_tianbang", "hami_tianshan", "hamitianbang_xinjiang"]
        final_compensate = get_final_all(self.item_no, self.period, "compensate")
        if self.clearing_type == 'repay' and final_compensate:
            self.assert_equal("1000-01-01 00:00:00", final_principal["expect_compensate_time"], '预计代偿时间不正确')
            self.assert_equal('Y', final_principal["compensated"], '已有代偿记录则为代偿后')
            print("检查 是否为代偿后还款 通过")
        if self.clearing_type == 'repay' and final_principal["asset_loan_channel"] in advance_compensate_list:
            self.assert_equal("1000-01-01 00:00:00", final_principal["expect_compensate_time"], '预计代偿时间不正确')
            self.assert_equal('Y', final_principal["compensated"], 'T-1资方直接为代偿判断错误')
            print("检查 是否为代偿后还款 通过")
        if final_principal["asset_loan_channel"] in d4_list:
            compensate_time_at = get_date_after(final_principal["expect_finish_time"][:10], day=4)
            if self.clearing_type == 'repay' and compensate_time_at > final_principal["actual_finish_time"][:10]:
                self.assert_equal("1000-01-01 00:00:00", final_principal["expect_compensate_time"], '预计代偿时间不正确')
                self.assert_equal('N', final_principal["compensated"], '哈密d4代偿判断错误')
                print("检查 是否为代偿后还款 通过")
            if self.clearing_type == 'repay' and compensate_time_at <= final_principal["actual_finish_time"][:10]:
                self.assert_equal("1000-01-01 00:00:00", final_principal["expect_compensate_time"], '预计代偿时间不正确')
                self.assert_equal('Y', final_principal["compensated"], '哈密d4代偿后判断错误')
                print("检查 是否为代偿后还款 通过")
            if self.clearing_type == 'compensated':
                self.assert_equal('N', final_principal["compensated"], '代偿的compensated直接为N判断错误')
                self.assert_equal(compensate_time_at, final_principal["expect_compensate_time"][:10], '预计代偿时间不正确')
                print("检查 是否为代偿后还款 通过")
        if final_principal["asset_loan_channel"] not in d4_list and self.clearing_type == 'compensated':
            self.assert_equal('N', final_principal["compensated"], '代偿的compensated直接为N判断错误')
            self.assert_equal(get_date_before_today(), final_principal["expect_compensate_time"][:10], '预计代偿时间不正确')
            print("检查 是否为代偿后还款 通过")
        # 4、检查代扣通道
        if self.repay_channel != "qsq" and final_principal["asset_loan_channel"] not in ['mozhi_beiyin_zhongyi',
                                                                                         'beiyin_tianbang']:
            self.assert_equal(final_principal["asset_loan_channel"], final_principal["withhold_result_channel"],
                              '本金代扣通道判断错误')
            print("检查 代扣通道 通过")
        # 5、检查 partly 字段
        if self.clearing_type == 'repay':
            if final_principal["asset_loan_channel"] in final_principal["withhold_result_channel"]:
                self.assert_equal('Y', final_principal["partly"], '资方代扣本息partly判断错误')
                print("检查 partly 通过")
            else:
                self.assert_equal('N', final_principal["partly"], '资方未代扣本息partly判断错误')
                print("检查 partly 通过")
        else:
            if final_principal:
                self.assert_equal('N', final_principal["partly"], '需要代偿本息partly判断错误')
                print("检查 partly 通过")
            else:
                self.assert_equal('Y', final_principal["partly"], '不需要代偿本息partly判断错误')
                print("检查 partly 通过")
        # 6、完成时间和到期日的检查 , 20210204 rewrite_actual_finish_time 改为代码固定
        rewrite_actual_finish_time = ["huabeixiaodai_zhitou", "qinnong", "qinnong_jieyi"]
        if self.clearing_type == 'repay' and final_principal["compensated"] == 'N':
            if self.one_one_repay == 'N':
                if final_principal["asset_loan_channel"] in rewrite_actual_finish_time:
                    self.assert_equal(final_principal["expect_finish_time"][:10],
                                      final_principal["actual_finish_time"][:10], '完成时间不正确')
                    print("检查 完成时间和到期日 通过")
                else:
                    self.assert_equal(get_date_before_today()[:10], final_principal["actual_finish_time"][:10],
                                      '完成时间不正确')
                    print("检查 完成时间和到期日 通过")
            else:
                print("但是有那种一期一期还款的场景的还款时间则不为当日")
        elif final_principal["compensated"] == 'Y':
            self.assert_equal(get_date_before_today()[:10], final_principal["actual_finish_time"][:10], '完成时间不正确')
            print("检查 完成时间和到期日 通过")
        else:
            self.assert_equal(get_date_before_today()[:10], final_principal["actual_finish_time"][:10], '完成时间不正确')
            print("检查 完成时间和到期日 通过")
        # 7、金额的校验

    def check_final_amount(self, capital_trans):
        # 存在利息多条代扣记录，所以和还款计划对比的数据需要按照费用类型求和再比较
        final_sum = get_final_sum(self.item_no, self.period, self.clearing_type)
        # 取出需要的列组装二维数组
        final_pd = pd.DataFrame(final_sum, columns=['asset_item_no', 'amount_type', 'amount'])
        capital_pd = pd.DataFrame(capital_trans, columns=['capital_asset_item_no', 'capital_transaction_type',
                                                          'capital_transaction_amount'])
        # merchant_service 需要转变为 service 再用
        final_merchant_pd = final_pd[final_pd['amount_type'].isin(['merchant_service'])]
        final_merchant_pd['amount_type'] = 'service'
        final_service_pd = final_pd[~final_pd['amount_type'].isin(['merchant_service'])]
        final_service_pd = final_service_pd.append(final_merchant_pd)
        # 排序
        final_sort = final_service_pd.sort_values(by=["amount_type"])
        capital_sort = capital_pd.sort_values(by=["capital_transaction_type"])
        # 需要代偿的类型 reverse费用和after_loan_manage无需代偿
        compensate_type = ['principal', 'interest', 'guarantee', 'consult']
        # 拨备还款无需清分reverse费用和after_loan_manage
        provision_type = ['arbitration', 'capital_decrease', 'provison_decrease']
        if self.clearing_type == 'compensate' or final_sum[0]['withhold_result_channel'] in provision_type:
            capital_sort = capital_sort[capital_sort['capital_transaction_type'].isin(compensate_type)]
        # 资方还款计划没有罚息，对比单个金额的时候就需要去掉这个罚息再对比
        final_risk_sort = final_sort[~final_sort['amount_type'].isin(['risk_manage'])]
        compare_result = capital_sort.values == final_risk_sort.values
        print("#########capital_sort###########")
        print(capital_sort.values)
        print("##########final_risk_sort##########")
        print(final_risk_sort.values)
        print(compare_result)
        self.assert_equal(compare_result.all(), True, '费用金额不正确')
        # 求和且返回和  axis 0为列，1为行
        capital_total_amount = capital_sort.filter(regex='capital_transaction_amount').sum(axis=0)
        final_total_amount = final_risk_sort.filter(regex='amount').sum(axis=0)
        return capital_total_amount["capital_transaction_amount"], final_total_amount["amount"]
