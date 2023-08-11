import time

import pandas as pd

from biztest.function.biz.biz_db_class import BizDbBase
from biztest.util.asserts.assert_util import Assert


class BizCheckBase(object):
    db = BizDbBase()

    @staticmethod
    def check_data(data, **kwargs):
        for key, value in kwargs.items():
            Assert.assert_equal(data[key], value, "%s数据有误" % key)

    def check_capital_notify(self, item_no, **kwargs):
        rs = self.db.get_capital_notify_by_asset_item_no(item_no)
        self.check_data(rs[0], **kwargs)
        return rs[0]['capital_notify_id']

    def check_compensate_not_exist(self, task_order_no, task_type, create_at, timeout=60):
        """
        执行代偿任务后，检查代偿不存在，在一分钟内
        :param task_order_no: task_order_no
        :param task_type: 类型
        :param create_at: 创建时间
        :param timeout: 超时
        :return:
        """
        i = 0
        while True:
            task_list = self.db.get_central_task_by_task_type_and_create_at(task_type, create_at)
            if task_list:
                break
            i += 1
            if i >= timeout:
                raise ValueError('执行代偿任务失败，没有生成任何代偿数据')
            time.sleep(1)
        task = self.db.get_central_task_by_task_order_no_and_task_type(task_order_no, task_type)
        Assert.assert_equal((), task, '线下还款已经推送，但是代偿了')

    def check_capital_notify_not_exist(self, item_no,
                                       notify_type='compensate,advance,early_settlement,overdue,normal',
                                       start_period=1, end_period=1, status='open'):
        if not isinstance(notify_type, str):
            raise TypeError('notify arg need str but "{0}" type found!'.format(type(notify_type)))
        rs = self.db.get_capital_notify_record(item_no,
                                               start_period,
                                               end_period,
                                               notify_type,
                                               status)
        Assert.assert_equal(rs, (), "%s资产推送生成了推送记录" % item_no)

    def check_task_memo(self, task_id, except_memo):
        rs = self.db.get_central_task_by_id(task_id)
        if not rs:
            raise ValueError('not found the task where task_id={0}'.format(task_id))
        Assert.assert_equal(rs[0]['task_memo'], except_memo, "%stask的memo不一致" % task_id)

    def check_capital_asset(self, item_no, **kwargs):
        rs = self.db.get_biz_capital_asset_by_item_no(item_no)
        self.check_data(rs[0], **kwargs)

    @staticmethod
    def check_capital_transaction_col(item_no, df_capital_tran, col_name, col_value,
                                      start_p, end_p, fee_type_in=(), fee_type_not_in=()):
        if col_value is not None:
            if fee_type_in and isinstance(fee_type_in, tuple):
                col_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                    range(start_p, end_p + 1)) & df_capital_tran.capital_transaction_type.isin(fee_type_in), col_name] \
                            == col_value
            elif fee_type_not_in and isinstance(fee_type_not_in, tuple):
                col_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                    range(start_p, end_p + 1)) & ~df_capital_tran.capital_transaction_type.isin(fee_type_not_in),
                                                col_name] == col_value
            else:
                col_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                    range(start_p, end_p + 1)), col_name] == col_value
            Assert.assert_equal(col_check.all(), True,
                                f'{item_no}的{col_name}应为{col_value}')

    @staticmethod
    def check_capital_transaction_withhold_result_channel(item_no, df_capital_tran, withhold_result_channel_asset,
                                                          withhold_result_channel_fee_type, start_p, end_p):
        # 判断通道，拆分本息（可能资方扣，可能我方扣），其它费用-我方扣
        if withhold_result_channel_asset is not None:
            withhold_result_channel_asset_checkout = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                range(start_p, end_p + 1)) & df_capital_tran.capital_transaction_type.isin(withhold_result_channel_fee_type),
                                       'capital_transaction_withhold_result_channel'] == withhold_result_channel_asset
            Assert.assert_equal(withhold_result_channel_asset_checkout.all(), True,
                                f'{item_no}的capital_transaction_withhold_result_channel应为{withhold_result_channel_asset}')

            withhold_result_channel_paysvr_checkout = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                range(start_p, end_p + 1)) & ~df_capital_tran.capital_transaction_type.isin(
                withhold_result_channel_fee_type), 'capital_transaction_withhold_result_channel'] == 'qsq'
        else:
            withhold_result_channel_paysvr_checkout = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                range(start_p, end_p + 1)), 'capital_transaction_withhold_result_channel'] == 'qsq'
        Assert.assert_equal(withhold_result_channel_paysvr_checkout.all(), True,
                            f'{item_no}的capital_transaction_withhold_result_channel应为qsq')

    def check_capital_transaction_all(self, item_no, condition, excepts):
        capital_tran = self.db.get_biz_capital_asset_tran_by_item_no(item_no)
        df_capital_tran = pd.DataFrame.from_records(data=capital_tran)
        df_capital_tran.loc[df_capital_tran.capital_transaction_period, []]

    def check_capital_transaction_for_fee_type(self,
                                               item_no,
                                               expect_data,
                                               expect_cols,
                                               period_start,
                                               period_end):
        """
        根据其次和费用类型同时检查需要检查的列的值
        :param item_no: 资产编号
        :param expect_data:还款信息pd
        :param expect_cols:check的列名
        :param period_start:period的列名
        :param period_end:period的列名
        :return:
        """
        expect_data = expect_data if isinstance(expect_data, pd.DataFrame) \
            else pd.DataFrame.from_records(data=expect_data)
        fee_type_set = set(expect_data.capital_transaction_type)
        for fee_type in fee_type_set:
            user_repay_and_channel_period = list(set(expect_data.loc[expect_data.capital_transaction_type ==
                                                                     fee_type, 'capital_transaction_period']))
            self.check_capital_transaction(item_no, start_p=period_start,
                                           end_p=period_end,
                                           fee_type=fee_type,
                                           expect_data=expect_data,
                                           expect_cols=expect_cols)
        return list(fee_type_set)

    def check_capital_transaction(self, item_no, **kwargs):
        capital_tran = self.db.get_biz_capital_asset_tran_by_item_no(item_no)
        if not capital_tran:
            raise ValueError("not fount the capital transaction's info with {0}".format(item_no))
        # capital_tran数据准备：dict-->DataFrame
        df_capital_tran = pd.DataFrame.from_records(data=capital_tran)
        # df_capital_tran['capital_transaction_user_repay_at'] = df_capital_tran.capital_transaction
        # _user_repay_at.apply(
        #     lambda x: x[:10])
        # df_capital_tran = df_capital_tran.sort_values(by=['capital_transaction_period']).set_index(
        #     ['capital_transaction_period'])
        # 获取参数
        start_p = kwargs.get("start_p", 1)
        end_p = kwargs.get("end_p", 12)
        fee_type = kwargs.get('fee_type', None)
        expect_cols = kwargs.get("expect_cols", None)
        expect_data = kwargs.get("expect_data", None)
        # 开始校验

        # withhold_result_channel_asset不为None,表示要检查withhold_result_channel
        # withhold_result_channel_fee_type为资方代扣费用类型集合，为None表示都是走的我方代扣
        if expect_cols is not None:
            expect_value = expect_data.loc[expect_data.capital_transaction_period.isin(range(start_p, end_p + 1)) &
                                           (expect_data.capital_transaction_type == fee_type), expect_cols]
            actual_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                range(start_p, end_p + 1)) & (df_capital_tran.capital_transaction_type == fee_type), expect_cols]

        else:
            expect_value = expect_data.loc[df_capital_tran.capital_transaction_period.isin(
                range(start_p, end_p + 1)), expect_cols]
            actual_check = df_capital_tran.loc[df_capital_tran.capital_transaction_period.isin(
                range(start_p, end_p + 1)), expect_cols]
        res = expect_value.values == actual_check.values
        Assert.assert_equal(res.all(), True,
                            f'{item_no}的{expect_value[res == True]}应为{actual_check[res == True]}')

