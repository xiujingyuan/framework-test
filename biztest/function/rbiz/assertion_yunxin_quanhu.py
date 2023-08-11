# -*- coding: utf-8 -*-
from biztest.function.rbiz.assertion import Assertion, get_withhold_by_request_no


class AssertionYunxinQuanHu(Assertion):
    def __init__(self, db_rbiz, db_biz, period, item_num_loan_channel=None, item_num_no_loan=None,
                 amount_loan_channel=None, amount_no_loan=None, **kwargs):
        super(AssertionYunxinQuanHu, self).__init__(db_rbiz, db_biz, period, item_num_loan_channel, item_num_no_loan,
                                                    amount_loan_channel, amount_no_loan, **kwargs)

    def assertion_active_withhold_single_normal(self, **kwargs):
        amount_capital = int(kwargs.get("amount", None))
        count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
            self.db_rbiz,
            self.request_no)

        if self.item_num_loan_channel and self.item_num_no_loan:
            self.assertion(3, count, '==', 'request_no为{}的在withhold中的拆单数不正确'.format(self.request_no))
            self.assertion(withhold_serial_no_list[0], withhold_serial_no_list[1], '!=',
                           "request_no为{}的在withhold中的拆单的serial_no相同".format(self.request_no))

        if (self.item_num_no_loan and self.item_num_loan_channel is None) or (
                self.item_num_loan_channel and self.item_num_no_loan is None):
            self.assertion(1, count, '==', 'request_no为{}的在withhold中数量不正确'.format(self.request_no))

        for status in withhold_status_list:
            self.assertion('success', status, '==', 'request_no为{}的在withhold状态不为success'.format(self.request_no))

        if 'yunxin_quanhu' in withhold_channel_list:
            withhold_channel_list.remove('yunxin_quanhu')
        if 'baidu_tq3_quick' in withhold_channel_list:
            withhold_channel_list.remove('baidu_tq3_quick')
            withhold_channel_list.remove('baidu_tq3_quick')
        self.assertion(0, len(withhold_channel_list), '==', '代扣通道不正确')

        if amount_capital in withhold_amount_list:
            withhold_amount_list.remove(amount_capital)
        amount_own = self.amount_loan_channel - amount_capital
        if amount_own in withhold_amount_list:
            withhold_amount_list.remove(amount_own)
        if self.amount_no_loan in withhold_amount_list:
            withhold_amount_list.remove(self.amount_no_loan)

        self.assertion(0, len(withhold_amount_list), '==',
                       'request_no为{}的在withhold中的金额不正确'.format(self.request_no))

    def assertion_active_withhold_settle_advance(self, split_amount_first, split_amount_second):
        count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
            self.db_rbiz,
            self.request_no)

        if self.item_num_loan_channel and self.item_num_no_loan:
            self.assertion(3, count, '==', 'request_no为{}的在withhold中的拆单数不正确'.format(self.request_no))
            self.assertion(withhold_serial_no_list[0], withhold_serial_no_list[1], '!=',
                           "request_no为{}的在withhold中的拆单的serial_no相同".format(self.request_no))

        if (self.item_num_no_loan and self.item_num_loan_channel is None) or (
                self.item_num_loan_channel and self.item_num_no_loan is None):
            self.assertion(1, count, '==', 'request_no为{}的在withhold中数量不正确'.format(self.request_no))

        for status in withhold_status_list:
            self.assertion('success', status, '==', 'request_no为{}的在withhold状态不为success'.format(self.request_no))
        print(withhold_channel_list)
        if 'yunxin_quanhu' in withhold_channel_list:
            withhold_channel_list.remove('yunxin_quanhu')
        if 'baidu_tq3_quick' in withhold_channel_list:
            withhold_channel_list.remove('baidu_tq3_quick')
        if 'baidu_tq3_quick' in withhold_channel_list:
            withhold_channel_list.remove('baidu_tq3_quick')
        self.assertion(0, len(withhold_channel_list), '==', '代扣通道不正确')

        if split_amount_first in withhold_amount_list:
            withhold_amount_list.remove(split_amount_first)
        if self.amount_no_loan in withhold_amount_list:
            withhold_amount_list.remove(self.amount_no_loan)
        if split_amount_second in withhold_amount_list:
            withhold_amount_list.remove(split_amount_second)
        self.assertion(0, len(withhold_amount_list), '==',
                       'request_no为{}的在withhold中的金额不正确'.format(self.request_no))

    def assertion_active_withhold_settle_normal(self, split_amount_one, split_amount_two, split_amount_three,
                                                withhold_count=3):
        count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
            self.db_rbiz,
            self.request_no)

        if self.item_num_loan_channel and self.item_num_no_loan:
            self.assertion(withhold_count, count, '==', 'request_no为{}的在withhold中的拆单数不正确'.format(self.request_no))
            self.assertion(withhold_serial_no_list[0], withhold_serial_no_list[1], '!=',
                           "request_no为{}的在withhold中的拆单的serial_no相同".format(self.request_no))
            self.assertion(withhold_serial_no_list[1], withhold_serial_no_list[2], '!=',
                           "request_no为{}的在withhold中的拆单的serial_no相同".format(self.request_no))
            self.assertion(withhold_serial_no_list[0], withhold_serial_no_list[2], '!=',
                           "request_no为{}的在withhold中的拆单的serial_no相同".format(self.request_no))

        for status in withhold_status_list:
            self.assertion('success', status, '==', 'request_no为{}的在withhold状态不为success'.format(self.request_no))
        if 'baidu_tq3_quick' in withhold_channel_list:
            withhold_channel_list.remove('baidu_tq3_quick')
            withhold_channel_list.remove('baidu_tq3_quick')
        self.assertion(withhold_channel_list[0] == withhold_channel_list[1])
        if 'yunxin_quanhu' in withhold_channel_list:
            withhold_channel_list.remove('yunxin_quanhu')
            withhold_channel_list.remove('yunxin_quanhu')
        self.assertion(0, len(withhold_channel_list), '==', '代扣通道不正确')

        if split_amount_one in withhold_amount_list:
            withhold_amount_list.remove(split_amount_one)

        if split_amount_two in withhold_amount_list:
            withhold_amount_list.remove(split_amount_two)

        if split_amount_three in withhold_amount_list:
            withhold_amount_list.remove(split_amount_three)

        if self.amount_no_loan in withhold_amount_list:
            withhold_amount_list.remove(self.amount_no_loan)

        self.assertion(0, len(withhold_amount_list), '==',
                       'request_no为{}的在withhold中的金额不正确'.format(self.request_no))

    def assertion_void_withhold_by_quanhu(self):
        count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
            self.db_rbiz,
            self.request_no)

        self.assertion(1, count, '==', 'request_no={}的资产在withhold中数量不正确'.format(self.request_no))

        for status in withhold_status_list:
            self.assertion('success', status, '==', 'request_no={}的资产在withhold状态不为success'.format(self.request_no))
        for channel in withhold_channel_list:
            self.assertion('yunxin_quanhu', channel, '==',
                           'request_no={}的资产在withhold中的代扣通道不正确'.format(self.request_no))

        if self.amount_loan_channel in withhold_amount_list:
            withhold_amount_list.remove(self.amount_loan_channel)
        self.assertion(0, len(withhold_amount_list), '==',
                       'request_no={}的资产在withhold中的金额不正确'.format(self.request_no))
