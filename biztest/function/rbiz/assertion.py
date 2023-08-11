# -*- coding: utf-8 -*-
from biztest.function.rbiz.database_operation import *


class Assertion:
    def __init__(self, db_rbiz, db_biz, period, item_num_loan_channel=None, item_num_no_loan=None,
                 amount_loan_channel=None, amount_no_loan=None, **kwargs):
        """
        如果是手动或者自动代扣，大小单分开断言，按请求次数断言
        如果是主动代扣，则传大单表示只用大单发起了请求，传小单表示只用小单发起了请求
        资方有自己的代扣通道,但不拆单
        :param db_rbiz:
        :param db_biz:
        :param period:
        :param item_num_loan_channel:
        :param item_num_no_loan:
        """
        self.db_rbiz = db_rbiz
        self.db_biz = db_biz
        self.item_num_loan_channel = item_num_loan_channel
        self.item_num_no_loan = item_num_no_loan
        self.period = period
        self.amount_loan_channel = amount_loan_channel
        self.amount_no_loan = amount_no_loan
        self.kwargs = kwargs
        self.request_no = self.get_request_no()

    def get_request_no(self):
        repay_type = self.kwargs.get("repay_type", None)
        if repay_type != "not_withhold":
            if self.item_num_loan_channel:
                request_no = get_request_no_by_item_no(self.db_rbiz, self.item_num_loan_channel)
            elif self.item_num_no_loan:
                request_no = get_request_no_by_item_no(self.db_rbiz, self.item_num_no_loan)
            else:
                request_no = None
        else:
            request_no = None
        return request_no

    def assertion(self, expect=None, actual=None, rule=None, msg=None):
        if rule == '==':
            assert expect == actual, msg
        if rule == 'in':
            assert expect in actual, msg
        if rule == '!=':
            assert actual != expect, msg
        if rule == 'is not None':
            assert actual is not None, msg
        if rule == 'is None':
            assert actual is None, msg

    def assertion_card_bind(self, serial_no):
        card_bind_status = get_card_bind_staus_by_serial_no(self.db_rbiz, serial_no)
        self.assertion('success', card_bind_status, '==', "serial_no={}的资产在card_bind中状态不为success".format(serial_no))

    def assertion_withhold_request(self, amount, request_no=None):
        if request_no:
            self.request_no = request_no
        count, withhold_request_amount, withhold_request_status = get_withold_request_by_request_no(self.db_rbiz,
                                                                                                    self.request_no)
        self.assertion(amount, withhold_request_amount, '==',
                       'request_no={}的资产在withhold_request中的金额与传入金额不一致'.format(self.request_no))
        self.assertion('finish', withhold_request_status, '==',
                       'request_no={}的资产在withhold_request表中状态不为finish'.format(self.request_no))
        self.assertion(1, count, '==', 'request_no={}的资产在withhold_request中请求记录数不为1'.format(self.request_no))

    def assertion_auto_withhold_request(self, amount_list, request_no_list, withhold_count=2):
        amount_list = amount_list
        for request_no in request_no_list:
            count, withhold_request_amount, withhold_request_status = get_withold_request_by_request_no(self.db_rbiz,
                                                                                                        request_no)
            self.assertion('finish', withhold_request_status, '==',
                           'request_no={}在withhold_request表中状态不为finish'.format(request_no))
            self.assertion(1, count, '==', 'request_no={}在withhold_request中请求记录数不为1'.format(request_no))
            if withhold_request_amount in amount_list:
                amount_list.remove(withhold_request_amount)
        self.assertion(0, len(amount_list), '==',
                       "自动代扣withhold_request拆单数量不正确，request_no_list:{}".format(request_no_list))
        self.assertion(withhold_count, len(request_no_list), '==',
                       "自动代扣withhold_request拆单数量不正确，request_no_list:{}".format(request_no_list))

    def assertion_withhold_order(self, serial_no=None):
        status_list_total = []
        if self.item_num_loan_channel:
            status_list_loan_channel = get_withhold_order_by_item_no(self.db_rbiz, self.item_num_loan_channel,
                                                                     serial_no)
            status_list_total.extend(status_list_loan_channel)

        if self.item_num_no_loan:
            status_list_no_loan = get_withhold_order_by_item_no(self.db_rbiz, self.item_num_no_loan)
            status_list_total.extend(status_list_no_loan)
        print("status_list_total", f'{status_list_total}')
        for status in status_list_total:
            self.assertion('success', status, '==',
                           f'request_no={self.request_no}在withhold_order表的状态不为success')

    def assertion_active_withhold_not_split_has_withhold_channel(self, grant_by_my=False, withhold_count=2,
                                                                 withhold_channel="baidu_tq3_quick"):
        count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
            self.db_rbiz,
            self.request_no)

        if self.item_num_loan_channel and self.item_num_no_loan:
            self.assertion(withhold_count, count, '==',
                           f'request_no={self.request_no}的资产在withhold中的拆单数不正确')
            if withhold_count > 1:
                self.assertion(withhold_serial_no_list[0], withhold_serial_no_list[1], '!=',
                               "request_no={}的资产在withhold中的拆单的serial_no相同".format(self.request_no))
            if grant_by_my:
                self.assertion('my,my1', sign_company_list, 'in',
                               'request_no={}的资产在withhold中传的主体不为my'.format(self.request_no))
        if (self.item_num_no_loan and self.item_num_loan_channel is None) or (
                self.item_num_loan_channel and self.item_num_no_loan is None):
            self.assertion(1, count, '==', 'request_no={}的资产在withhold中数量不正确'.format(self.request_no))
            if self.item_num_loan_channel:
                if grant_by_my:
                    self.assertion('my,my1', sign_company_list[0], '==',
                                   'request_no={}的资产在withhold中传的主体不为my'.format(self.request_no))

        for status in withhold_status_list:
            self.assertion('success', status, '==', 'request_no={}的资产在withhold状态不为success'.format(self.request_no))
        for channel in withhold_channel_list:
            self.assertion(withhold_channel, channel, '==',
                           'request_no={}的资产在withhold中的代扣通道不正确'.format(self.request_no))
        print("withhold_amount_list", withhold_amount_list)
        print("self.amount_loan_channel", self.amount_loan_channel)
        print("self.amount_no_loan", self.amount_no_loan)
        if self.amount_loan_channel in withhold_amount_list:
            withhold_amount_list.remove(self.amount_loan_channel)
        if self.amount_no_loan in withhold_amount_list:
            withhold_amount_list.remove(self.amount_no_loan)
        self.assertion(0, len(withhold_amount_list), '==',
                       'request_no={}的资产在withhold中的金额不正确'.format(self.request_no))

    def assertion_active_withhold_not_split_without_withhold_channel(self):
        count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
            self.db_rbiz,
            self.request_no)

        if self.item_num_loan_channel and self.item_num_no_loan:
            self.assertion(2, count, '==', 'request_no={}的资产在withhold中的拆单数不正确'.format(self.request_no))

        if (self.item_num_no_loan and self.item_num_loan_channel is None) or (
                self.item_num_loan_channel and self.item_num_no_loan is None):
            self.assertion(2, count, '==', 'request_no={}的资产在withhold中数量不正确'.format(self.request_no))

        for status in withhold_status_list:
            self.assertion('success', status, '==', 'request_no={}的资产在withhold状态不为success'.format(self.request_no))
        for channel in withhold_channel_list:
            self.assertion('baidu_tq3_quick', channel, '==',
                           'request_no={}的资产在withhold中的代扣通道不正确'.format(self.request_no))

        if self.amount_loan_channel in withhold_amount_list:
            withhold_amount_list.remove(self.amount_loan_channel)
        if self.amount_no_loan in withhold_amount_list:
            withhold_amount_list.remove(self.amount_no_loan)

        self.assertion(0, len(withhold_amount_list), '==',
                       'request_no={}的资产在withhold中的金额不正确'.format(self.request_no))

    def assertion_void_withhold_by_paysvr(self, channel_name="baidu_tq3_quick"):
        count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
            self.db_rbiz,
            self.request_no)

        self.assertion(1, count, '==', 'request_no={}的资产在withhold中数量不正确'.format(self.request_no))

        for status in withhold_status_list:
            self.assertion('success', status, '==', 'request_no={}的资产在withhold状态不为success'.format(self.request_no))
        for channel in withhold_channel_list:
            self.assertion(channel_name, channel, '==',
                           'request_no={}的资产在withhold中的代扣通道不正确'.format(self.request_no))

        if self.amount_loan_channel in withhold_amount_list:
            withhold_amount_list.remove(self.amount_loan_channel)
        self.assertion(0, len(withhold_amount_list), '==',
                       'request_no={}的资产在withhold中的金额不正确'.format(self.request_no))

    def assertion_auto_withhold_not_split_has_withhold_channel(self, request_no_list, channel_name='baidu_tq3_quick'):
        for request_no in request_no_list:
            count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
                self.db_rbiz,
                request_no)

            for status in withhold_status_list:
                self.assertion('success', status, '==', 'request_no={}的资产的在withhold状态不为success'.format(request_no))
            for channel in withhold_channel_list:
                self.assertion(channel_name, channel, '==',
                               'request_no={}的资产在withhold中的代扣通道不正确'.format(request_no))

    def assertion_auto_withhold_has_withhold_channel(self, request_no, channel_name='baidu_tq3_quick'):
        count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
            self.db_rbiz,
            request_no)
        for status in withhold_status_list:
            self.assertion('success', status, '==', 'request_no={}的资产的在withhold状态不为success'.format(request_no))
        for channel in withhold_channel_list:
            self.assertion(channel_name, channel, '==',
                           'request_no={}的资产在withhold中的代扣通道不正确'.format(request_no))

    def assertion_withhold_detail_not_split(self, serial_no=None):
        if self.item_num_loan_channel:
            loan_channel_amount, loan_channel_status_list = get_withhold_detail_by_item_no(self.db_rbiz,
                                                                                           self.item_num_loan_channel,
                                                                                           self.period, serial_no)
            serial_no
            self.assertion(self.amount_loan_channel, loan_channel_amount, '==',
                           'item_no={}的资产在withhold_detail中的金额不正确'.format(self.item_num_loan_channel))
            for status in loan_channel_status_list:
                self.assertion('finish', status, '==',
                               'item_no={}的资产在withhold_detail中的状态不正确'.format(self.item_num_loan_channel))
        if self.item_num_no_loan:
            no_loan_amount, no_loan_channel_status_list = get_withhold_detail_by_item_no(self.db_rbiz,
                                                                                         self.item_num_no_loan,
                                                                                         self.period)
            self.assertion(self.amount_no_loan, no_loan_amount, '==',
                           'item_no={}的资产在withhold_detail中的金额不正确'.format(self.item_num_no_loan))
            for status in no_loan_channel_status_list:
                self.assertion('finish', status, '==',
                               'request_no={}的资产在withhold_detail中的状态不正确'.format(self.item_num_no_loan))

    def assertion_recharge_and_repay(self, request_no=None):
        if request_no:
            self.request_no = request_no
        channel_key_list = get_channel_key_by_request_no(self.db_rbiz, self.request_no)
        for channel_key in channel_key_list:
            self.assertion(get_withhold_amount_by_channel_key(self.db_rbiz, channel_key),
                           get_recharge_amount_by_channel_key(self.db_rbiz, channel_key),
                           '==', 'request_no={}的资产的充值金额与代扣金额不一致'.format(self.request_no))

    def assertion_provision(self):
        asset_tran_amount_not_repayprincipal = get_repaid_amount_from_asset_tran_where_asset_type_type_is_not_some_type(
            self.db_rbiz, self.item_num_loan_channel, 'repayprincipal', period=None)
        provision_amount = get_provision_amount_by_item_no(self.db_rbiz, self.item_num_loan_channel)
        self.assertion(asset_tran_amount_not_repayprincipal, provision_amount, '==',
                       f'item_no={self.item_num_loan_channel}的拨备充值金额不正确')

    def assertion_asset_tran(self, tran_type=None, tran_status="finish"):
        item_no_list = []
        if self.item_num_loan_channel:
            item_no_list.append(self.item_num_loan_channel)
        if self.item_num_no_loan:
            item_no_list.append(self.item_num_no_loan)
        for item_no in item_no_list:
            asset_tran_status_list = get_asset_tran_status_by_item_no(self.db_rbiz, item_no, self.period, tran_type)
            LogUtil.log_info(f'{asset_tran_status_list}')
            for status in asset_tran_status_list:
                self.assertion(tran_status, status, '==', 'item_no={}的资产在rbiz.asset_tran中的状态不正确'.format(item_no))

    def assertion_asset_tran_in_biz(self, tran_type=None):
        item_no_list = []
        if self.item_num_loan_channel:
            item_no_list.append(self.item_num_loan_channel)
        if self.item_num_no_loan:
            item_no_list.append(self.item_num_no_loan)
        for item_no in item_no_list:
            asset_tran_status_list = get_asset_tran_status_by_item_no(self.db_biz, item_no, self.period, tran_type)

            for status in asset_tran_status_list:
                self.assertion('finish', status, '==', 'item_no={}的资产在biz.asset_tran中的状态不正确'.format(item_no))

    def assertion_dtran_in_biz(self, tran_type=None):
        item_no_list = []
        if self.item_num_loan_channel:
            item_no_list.append(self.item_num_loan_channel)
        if self.item_num_no_loan:
            item_no_list.append(self.item_num_no_loan)
        for item_no in item_no_list:
            asset_tran_status_list = get_dtran_status_by_item_no(self.db_biz, item_no, self.period, tran_type)

            for status in asset_tran_status_list:
                self.assertion('finish', status, '==', 'item_no={}的资产在biz.asset_tran中的状态不正确'.format(item_no))

    def assertion_asset_tran_in_gbiz(self):
        db_gbiz = self.kwargs['db_test_global_gbiz']
        item_no_list = []
        if self.item_num_loan_channel:
            item_no_list.append(self.item_num_loan_channel)
        if self.item_num_no_loan:
            item_no_list.append(self.item_num_no_loan)
        for item_no in item_no_list:
            asset_tran_status_list = get_asset_tran_status_by_item_no(db_gbiz, item_no, self.period)

            for status in asset_tran_status_list:
                self.assertion('finish', status, '==', 'item_no={}的资产在biz.asset_tran中的状态不正确'.format(item_no))

    def assertion_withhold_result_and_tran_in_biz(self, type=None):
        serial_no_list = get_serial_no_by_request_no(self.db_rbiz, self.request_no)
        for serial_no in serial_no_list:
            withhold_result_amount_list, withhold_result_id_list, withhold_result_status_list = get_withhold_result_in_biz_by_serial_no(
                self.db_biz, serial_no)
            withhold_result_amount_sum = 0
            withhold_amount = get_withhold_amount_by_serial_no(self.db_rbiz, serial_no)
            for withhold_result_amount in withhold_result_amount_list:
                withhold_result_amount_sum = withhold_result_amount + withhold_result_amount_sum
            self.assertion(withhold_result_amount_sum, withhold_amount, '==',
                           'request_no={}的资产在biz.withhold_result中的金额不正确'.format(self.request_no))
            for withhold_result_status in withhold_result_status_list:
                self.assertion('success', withhold_result_status, '==',

                               'request_no={}的资产在biz.withhold_result中的状态不正确'.format(self.request_no))
            if type != "trade":
                for withhold_result_id in withhold_result_id_list:
                    withhold_result_transaction = get_withhold_transaction_in_biz_by_withhold_result_id(self.db_biz,
                                                                                                        withhold_result_id)
                    self.assertion(actual=withhold_result_transaction, rule='is not None',
                                   msg='request_no={}的资产在biz.withhold_result_tran中同步失败'.format(self.request_no))

    def assertion_asset_status_in_asset_void(self):
        loan_channel_asset_status = get_asset_from_asset_by_item_no(self.db_rbiz, self.item_num_loan_channel)
        no_loan_asset_status = get_asset_from_asset_by_item_no(self.db_rbiz, self.item_num_loan_channel + "_noloan")
        self.assertion('writeoff', loan_channel_asset_status, '==',
                       f"item_no={self.item_num_loan_channel}在rbiz.asset中的状态不正确")
        self.assertion('void', no_loan_asset_status, f"item_no={self.item_num_no_loan}在rbiz.asset中的状态不正确")

    def assertion_withhold_status_in_withhold_by_serial_no(self, status):
        serial_no = self.kwargs.get("withhold_serial_no")
        withhold_status = get_withhold_status_from_rbiz_by_serial_no(self.db_rbiz, serial_no)

        self.assertion(withhold_status == status, 'serial_no={}的在withhold中的状态不为{}'.format(serial_no, status))

    def assertion_unlock(self, item_no):
        asset_operation_auth = get_asset_operation_auth(self.db_rbiz, item_no)
        withhold_asset_detail_lock = get_withhold_asset_detail_lock(self.db_rbiz, item_no)
        self.assertion(expect=[], actual=asset_operation_auth, rule='==',
                       msg="asset_operation_auth解锁失败,item_no:{}".format(item_no))
        self.assertion(expect=[], actual=withhold_asset_detail_lock, rule='==',
                       msg="withhold_asset_detail_lock,item_no:{}".format(item_no))

    def assertion_recharge_and_repay_offline(self, id_num):
        account_no = get_account_from_rbiz_by_id_num(self.db_rbiz, id_num)
        recharge_amount = get_amount_from_account_recharge_by_account_no(self.db_rbiz, account_no)
        self.assertion(expect=self.amount_loan_channel, actual=recharge_amount, rule='==',
                       msg=f'account_recharge中account_no={account_no}充值不正确')
        recharge_log_amount = get_amount_from_account_recharge_log_by_account_no(self.db_rbiz, account_no)
        self.assertion(expect=self.amount_loan_channel, actual=recharge_log_amount, rule='==',
                       msg=f'account_recharge_log中account_no={account_no}充值不正确')

        amount_repay = get_amount_from_account_repay_by_account_no(self.db_rbiz, account_no)
        amount_beging_repay_log, amount_end_repay_log = get_amount_from_account_repay_log_by_account_no(self.db_rbiz,
                                                                                                        account_no)
        self.assertion(expect=self.amount_loan_channel, actual=amount_repay, rule='==',
                       msg=f'account_repay中account_no={account_no}还款金额不正确')

        self.assertion(expect=self.amount_loan_channel, actual=amount_beging_repay_log, rule='==',
                       msg=f'account_repay_log中account_no={account_no}起始还款金额不正确')
        self.assertion(expect=0, actual=amount_end_repay_log, rule='==',
                       msg=f'account_repay_log中account_no={account_no}终止还款金额不正确')

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

    def assertion_refund_request_in_rbiz(self, serial_no, channel_key):
        channel_key_actual = get_serial_no_from_refund_request_by_serial_no(self.db_rbiz, serial_no)
        self.assertion(channel_key, channel_key_actual, '==', f'refund_request没有值{serial_no}')

    def assertion_refund_in_rbiz(self, serial_no):
        serial_no_actual = get_serial_no_from_refund_by_serial_no(self.db_rbiz, serial_no)
        self.assertion(serial_no, serial_no_actual, '==', f'refund表没有值{serial_no}')

    def assertion_refund_detail_in_rbiz(self, serial_no, operate_type="inverse"):
        operate_type_list = get_operate_type_from_refund_detail_by_serial_no(self.db_rbiz, serial_no)
        for actual_type in operate_type_list:
            self.assertion(operate_type, actual_type, '==', f'serial_no为{serial_no}的在refund_detail状态不为{operate_type}')

    def assertion_withdraw_in_rbiz(self, serial_no):
        withdraw_status = get_withdraw_status_from_withdraw_by_serial_no(self.db_rbiz, serial_no)
        self.assertion("success", withdraw_status, '==', f'{serial_no} withdraw表状态不对')

    def assertion_active_withhold_capital_depart(self, **kwargs):
        amount_capital = int(kwargs.get("amount", None))
        withhold_count = int(kwargs.get("withhold_count", 3))
        count, withhold_amount_list, withhold_status_list, withhold_channel_list, withhold_serial_no_list, sign_company_list = get_withhold_by_request_no(
            self.db_rbiz,
            self.request_no)

        if self.item_num_loan_channel and self.item_num_no_loan:
            self.assertion(withhold_count, count, '==', 'request_no为{}的在withhold中的拆单数不正确'.format(self.request_no))
            if withhold_count > 1:
                self.assertion(withhold_serial_no_list[0], withhold_serial_no_list[1], '!=',
                               "request_no为{}的在withhold中的拆单的serial_no相同".format(self.request_no))

        if (self.item_num_no_loan and self.item_num_loan_channel is None) or (
                self.item_num_loan_channel and self.item_num_no_loan is None):
            self.assertion(1, count, '==', 'request_no为{}的在withhold中数量不正确'.format(self.request_no))

        for status in withhold_status_list:
            self.assertion('success', status, '==', 'request_no为{}的在withhold状态不为success'.format(self.request_no))
        LogUtil.log_info(f'withhold_amount_list{withhold_amount_list}')
        LogUtil.log_info(f'amount_capital{amount_capital}')
        if amount_capital in withhold_amount_list:
            withhold_amount_list.remove(amount_capital)
        amount_own = self.amount_loan_channel - amount_capital
        if amount_own in withhold_amount_list:
            withhold_amount_list.remove(amount_own)
        if self.amount_no_loan in withhold_amount_list:
            withhold_amount_list.remove(self.amount_no_loan)
        self.assertion(0, len(withhold_amount_list), '==',
                       'request_no为{}的在withhold中的金额不正确'.format(self.request_no))

    def assertion_active_withhold_sign_company(self, sign_company_list):
        ac_sign_company_list = get_sign_company_in_withhold_by_request_no(self.db_rbiz, self.request_no)
        print("ac_sign_company_list", ac_sign_company_list)
        print("sign_company_list", sign_company_list)
        for x in range(0, len(ac_sign_company_list)):
            self.assertion(sign_company_list[x], ac_sign_company_list[x], '==',
                           'request_no={}的资产在withhold[0]中传的主体不为{}'.format(self.request_no, sign_company_list[x]))
