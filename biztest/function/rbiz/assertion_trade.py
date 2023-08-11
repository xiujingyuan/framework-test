# -*- coding: utf-8 -*-
from biztest.function.rbiz.assertion import Assertion
from biztest.function.rbiz.database_operation import *


class AssertionTrade(Assertion):
    def __init__(self, db_rbiz, db_biz, period, item_num_loan_channel=None, item_num_no_loan=None,
                 amount_loan_channel=None, amount_no_loan=None, **kwargs):
        super(AssertionTrade, self).__init__(db_rbiz, db_biz, period, item_num_loan_channel, item_num_no_loan,
                                             amount_loan_channel, amount_no_loan, **kwargs)

    def asserttion_trade_in_rbiz(self, trade_no):
        trade_no_actual = get_trade_no_from_trade_by_trade_no(self.db_rbiz, trade_no)
        self.assertion(trade_no, trade_no_actual, '==', f'trade没有值{trade_no}')

    def assertion_trade_tran_in_rbiz(self, serial_no):
        serial_no_actual = get_serial_no_from_trade_tran_by_serial_no(self.db_rbiz, serial_no)
        self.assertion(serial_no, serial_no_actual, '==', f'trade_tran没有值{serial_no}')

    def asserttion_trade_in_biz(self, trade_no):
        trade_no_actual = get_trade_no_from_trade_order_by_trade_no(self.db_biz, trade_no)
        self.assertion(trade_no, trade_no_actual, '==', f'trade没有值{trade_no}')

    def assertion_trade_tran_in_biz(self, serial_no):
        serial_no_actual = get_serial_no_from_trade_order_tran_by_serial_no(self.db_biz, serial_no)
        self.assertion(serial_no, serial_no_actual, '==', f'trade_tran没有值{serial_no}')
