# -*- coding: utf-8 -*-
from biztest.case.gbiz.gbiz_loan_tool import gbiz_loan_tool
from biztest.case.global_gbiz.global_gbiz_loan_tool import global_gbiz_loan_tool
from biztest.config.rbiz.params_config import *
from biztest.util.db.db_util import PyMysql
from biztest.util.log.log_util import LogUtil
from biztest.util.msg.msg import GbizMsg
from biztest.util.tools.tools import get_item_no, get_calc_date_base_today, get_calc_date
from biztest.config.gbiz.gbiz_interface_params_config import gbiz_asset_import_url, GLOBAL_GBIZ_SYNC_ASSET_FROM_GRANT, \
    GLOBAL_GBIZ_ASSET_IMPORT_URL, GLOBAL_GBIZ_AUTO_GRANT_URL
from biztest.util.task.task import GbizTask
from biztest.function.rbiz.rbiz_common_function import gbiz_withdraw_to_rbiz, get_four_element_in_rbiz
import requests
from biztest.config.rbiz.url_config import project_repay_query_path
from biztest.util.tools.tools import parse_resp_body
import copy
import json
import math
import datetime
import calendar as c
import time


class AssetImportFactory(object):
    @staticmethod
    def get_import_obj(env, country, db_env):
        if country is None or country == "":
            country == "china"
        if country == "china":
            return AssetImportChina(env, db_env=db_env)
        elif country == "thailand":
            return AssetImportTha(env, db_env=db_env)
        elif country == 'india':
            return AssetImportInd(env, db_env=db_env)
        elif country == 'philippines':
            return AssetImportPhl(env, db_env=db_env)
        elif country == 'mexico':
            return AssetImportMex(env, db_env=db_env)
        else:
            raise ValueError("not found the country: {0}'s object".format(country))


class ToolBase(object):
    def __init__(self, env_test, db_env, country="china"):
        self.country = country
        self.env_test = env_test
        self.init_db(self.country, db_env)
        self.init_url(self.country)

    def init_db(self, country, db_env):
        self.db_rbiz = PyMysql("rbiz{}".format(self.env_test), db_env, country=country)
        self.db_biz = PyMysql('biz{}'.format(self.env_test), db_env, country=country)
        self.db_gbiz = PyMysql("gbiz{}".format(self.env_test), db_env, country=country)

    def init_url(self, country):
        self.biz_base_url = BIZ_BASE_URL[country].format(self.env_test)
        self.gbiz_base_url = GBIZ_BASE_URL[country].format(self.env_test)
        self.rbiz_base_url = RBIZ_BASE_URL[country].format(self.env_test)

    def __del__(self):
        print("__del__")
        if hasattr(self, 'db_biz'):
            self.db_biz.close_conn()
        if hasattr(self, 'db_gbiz'):
            self.db_gbiz.close_conn()
        if hasattr(self, 'db_rbiz'):
            self.db_rbiz.close_conn()


class AssetImportBase(ToolBase):
    def __init__(self, env_test, db_env, country="china"):
        super(AssetImportBase, self).__init__(env_test, country=country, db_env=db_env)

    def caldays(self, str1, str2):
        date1 = datetime.datetime.strptime(str1[0:10], "%Y-%m-%d") if isinstance(str1, str) else str1
        date2 = datetime.datetime.strptime(str2[0:10], "%Y-%m-%d") if isinstance(str2, str) else str2
        num = (date2 - date1).days
        return num

    def calmonths(self, startdate, enddate):
        # 计算两个日期相隔月差
        try:
            samemonthdate = datetime.date(enddate.year, enddate.month, startdate.day)
        except:
            samemonthdate = datetime.date(enddate.year, enddate.month, c.monthrange(enddate.year, enddate.month)[1])
        holdmonths = 0
        decimalmonth = 0.0
        if samemonthdate > enddate:
            if enddate.month > 1:
                try:
                    premanthdate = datetime.date(enddate.year, enddate.month - 1, startdate.day)
                except:
                    premanthdate = datetime.date(enddate.year, enddate.month - 1, c.monthrange(enddate.year,
                                                                                               enddate.month - 1)[1])
            else:
                try:
                    premanthdate = datetime.date(enddate.year - 1, 12, startdate.day)
                except:
                    premanthdate = datetime.date(enddate.year - 1, 12, c.monthrange(enddate.year - 1, 1)[1])
            currmonthdays = (samemonthdate - premanthdate).days
            holdmonths = (premanthdate.year - startdate.year) * 12 + premanthdate.month - startdate.month
            decimalmonth = (enddate - premanthdate).days / currmonthdays
        elif samemonthdate < enddate:
            if enddate.month < 12:
                try:
                    nextmonthdate = datetime.date(enddate.year, enddate.month + 1, startdate.day)
                except:
                    nextmonthdate = datetime.date(enddate.year, enddate.month + 1, c.monthrange(enddate.year,
                                                                                                enddate.month + 1)[1])
            else:
                try:
                    nextmonthdate = datetime.date(enddate.year + 1, 1, startdate.day)
                except:
                    nextmonthdate = datetime.date(enddate.year + 1, 1, c.monthrange(enddate.year + 1, 1)[1])
            currmonthdays = (nextmonthdate - samemonthdate).days
            holdmonths = (samemonthdate.year - startdate.year) * 12 + samemonthdate.month - startdate.month
            decimalmonth = (enddate - samemonthdate).days / currmonthdays
        else:
            holdmonths = (enddate.year - startdate.year) * 12 + enddate.month - startdate.month
        return int(math.modf(holdmonths + decimalmonth)[-1])

    def gbiz_loan_success(self, env, item_no, country=""):
        if env == "" or item_no == "":
            raise ValueError("env or item_no not null")
        elif country == "":
            code, message = gbiz_loan_tool(env, item_no)
        else:
            code, message = global_gbiz_loan_tool(country, env, item_no)
        resp = {
            "code": 0,
            "msg": "ok",
            "data": {"code": code, "message": message}
        }
        assert code == 0, f"gbiz资产放款失败, 资产编号为{item_no},接口返回为{resp}"
        LogUtil.log_info(f"response: {resp}")
        return resp

    def create_asset(self, advance_month, loan_channel, is_grant_day=False, advance_day=-1, amount_big=4000,
                     amount_small=200, count=6, from_system_name="香蕉", source_type="youxi_bill", period_day=0,
                     noloan=True):
        """
        创建资产
        :param advance_month: 提前多少个月，以当期时间为放款日，
        :param loan_channel: 通道，对于具体的资金方
        :param is_grant_day: 是否放款日
        :param advance_day: 提前多少天
        :param amount_big: 大单金额
        :param amount_small: 小单金额
        :param count: 期次
        :param from_system_name: 来源系统
        :param source_type: 适用场景
        :param period_day:天数
        :param noloan:是否有小单
        :return:
        """
        item_no, item_no_x, four_element = self.create_normal_asset(loan_channel,
                                                                    amount_big=amount_big,
                                                                    amount_small=amount_small,
                                                                    count=count,
                                                                    from_system_name=from_system_name,
                                                                    source_type=source_type,
                                                                    period_day=period_day,
                                                                    noloan=noloan)
        self.change_asset(advance_month, item_no, item_no_x, is_grant_day=is_grant_day, advance_day=advance_day)
        return item_no, item_no_x, four_element

    def create_normal_asset(self, loan_channel, amount_big=4000, amount_small=1000, count=6,
                            from_system_name="香蕉",
                            source_type="youxi_bill",
                            period_day=0,
                            noloan=True):
        """
        根据当前日期作为放款成功日期，生成资产相关信息
        :param loan_channel: 资金通道
        :param amount_big: 大单放款金额
        :param amount_small: 小单放款金额
        :param count: 放款期次
        :param from_system_name:来源系统，香蕉，草莓，火龙果
        :param source_type: 使用场景
        :param period_day: 天数 1期资产才会有·
        :param noloan: 是否有小单
        :return:
        """
        # 大单资产编号
        asset_item_no = loan_channel[0:4] + get_item_no() if len(loan_channel) > 3 else \
            (loan_channel + "____")[0:4] + get_item_no()
        # 小单资产编号
        asset_item_no_x = asset_item_no + "_noloan"
        # 获取四要素
        four_element = get_four_element_in_rbiz()

        # 大单进件
        if source_type:
            source_type = source_type
        elif loan_channel in self.source_type:
            source_type = random.choice(self.source_type[loan_channel])
        else:
            source_type = random.choice(self.source_type)
        item_no = self.create_data(four_element, asset_item_no, asset_item_no_x, loan_channel,
                                   amount_big, source_type, count, from_system_name, period_day=period_day)

        # 小单进件
        item_no_x = self.create_data(four_element, asset_item_no_x, asset_item_no, "noloan",
                                     amount_small, source_type + "_split", count, from_system_name,
                                     period_day=period_day) if noloan else ""
        return item_no, item_no_x, four_element

    def change_asset_new(self, advance_month, item_no, item_no_x, is_grant_day=False, advance_day=-1,
                         compensate_time=None,
                         change_cp=True):
        """
        修改资产放款时间及资产还款计划的到日期
        :param advance_month: 提前多少个月, 负数，推后是正数
        :param advance_day: 提前多少天, 负数，推后是正数
        :param item_no: 大单资产编号
        :param item_no_x: 小单资产编号
        :param compensate_time: 资方还款计划代偿日
        :param is_grant_day: 是否是放款日
        :param change_cp: 是否是放款日
        :return:
        """
        count_str = 'select asset_period_count, asset_product_category from asset where asset_item_no="{0}"'.format(
            item_no)
        count, period_day = self.db_rbiz.query_mysql(count_str)[0]
        period_day = int(period_day)
        if count == 1:
            grant_time = get_calc_date_base_today(day=0) if is_grant_day else \
                get_calc_date_base_today(day=advance_day)
        else:
            grant_time = get_calc_date_base_today(month=advance_month) if is_grant_day else \
                get_calc_date_base_today(month=advance_month, day=advance_day)

        # 获取biz数据库中的资方还款计划中的id
        if self.country == "china":
            biz_asset_id_str = 'select capital_asset_id from capital_asset where ' \
                               'capital_asset_item_no in ("{0}")'.format(item_no)
            biz_asset_id = self.db_biz.query_mysql(biz_asset_id_str)
            biz_asset_id = biz_asset_id[0][0] if biz_asset_id else None
        for period in range(1, count + 1):
            due_delay_month = period + advance_month
            if count == 1:
                due_time = get_calc_date_base_today(day=period_day, fmt="%Y-%m-%d") if is_grant_day else \
                    get_calc_date_base_today(day=period_day + advance_day, fmt="%Y-%m-%d")
            else:
                due_time = get_calc_date_base_today(month=due_delay_month, fmt="%Y-%m-%d") if is_grant_day else \
                    get_calc_date_base_today(month=due_delay_month, day=advance_day, fmt="%Y-%m-%d")
            cap_due_time = due_time[:-2] + compensate_time if compensate_time else due_time
            for item in (item_no, item_no_x):
                # 如果资产编号为空，则跳过
                if not item:
                    continue
                if period == 1:
                    # 第一期的时候，更新asset记录
                    item_no_str = 'update asset set asset_grant_at = "{0}", asset_effect_at = ' \
                                  '"{0}", asset_actual_grant_at = "{0}"' \
                                  ' where asset_item_no = "{1}"'.format(grant_time,
                                                                        item)
                    self.db_rbiz.execute_mysql(item_no_str)

                    capital_item_no_str = 'update capital_asset set capital_asset_granted_at = "{0}", ' \
                                          'capital_asset_push_at = "{0}" where capital_asset_item_no = "{1}"' \
                                          ''.format(grant_time, item)
                    if self.country == "china":
                        self.db_biz.execute_mysql(capital_item_no_str)
                    self.db_rbiz.execute_mysql(capital_item_no_str)

                # 更新asset_tran记录
                item_no_period_first = 'update asset_tran set asset_tran_due_at = "{0}" ' \
                                       'where asset_tran_asset_item_no = "{1}" and ' \
                                       'asset_tran_period = {2}'.format(due_time, item, period)
                self.db_rbiz.execute_mysql(item_no_period_first)
                if item == item_no_x:
                    continue
                if self.country == "china" and change_cp:
                    # 更新capital_transaction记录
                    capital_tran = 'UPDATE capital_transaction SET capital_transaction_expect_finished_at = "{0}" ' \
                                   'WHERE capital_transaction_item_no = "{1}" AND ' \
                                   'capital_transaction_period = {2}'.format(cap_due_time, item, period)
                    self.db_rbiz.execute_mysql(capital_tran)

                    sel_str = 'select capital_transaction_expect_finished_at from capital_transaction where ' \
                              'capital_transaction_asset_id="{0}" and capital_transaction_period={1} and' \
                              ' capital_transaction_type = "principal"' \
                              ''.format(biz_asset_id, period)
                    get_time = self.db_biz.query_mysql(sel_str)[0][0]
                    get_time_day = get_time.day
                    cap_due_time_year = int(cap_due_time.split("-")[0])  # 获取年份
                    cap_due_time_month = int(cap_due_time.split("-")[1])  # 获取月份
                    cap_due_time_day = int(cap_due_time.split("-")[2])
                    cap_due_time_date = datetime.date(cap_due_time_year, cap_due_time_month, cap_due_time_day)
                    change_month = self.calmonths(get_time, cap_due_time_date)
                    # change_day = cap_due_time_day - get_time_day
                    change_day = self.caldays(cap_due_time, str(get_time))
                    # 更新biz里面的capital_transaction记录

                    capital_tran = 'UPDATE capital_transaction SET capital_transaction_expect_finished_at = "{0}" ' \
                                   'WHERE capital_transaction_asset_id = "{1}" AND ' \
                                   'capital_transaction_period = {2}'.format(cap_due_time, biz_asset_id, period)
                    self.db_biz.execute_mysql(capital_tran)

                    # 更新biz里面的asset_tran记录
                    self.db_biz.execute_mysql(item_no_period_first)
                    # 更新用户还款时间，结清时间
                    print(item, period, cap_due_time, get_time, change_month, change_day)
                    self.update_other_time(change_month, change_day, biz_asset_id, period)
                    # 更新biz里面的dtransaction记录
                    # sql_dtr_biz = 'UPDATE dtransaction INNER JOIN asset on dtransaction_asset_id = asset_id ' \
                    #               'SET dtransaction_expect_finish_time="{0}" ' \
                    #               'WHERE asset_item_no="{1}" AND dtransaction_period={2} '.format(cap_due_time,
                    #                                                                               item,
                    #                                                                               period)
                    # 更新biz里面的ftransaction记录
                    # self.db_biz.execute_mysql(sql_dtr_biz)
                    # sql_ftr_biz = 'UPDATE ftransaction INNER JOIN asset on ftransaction_asset_id = asset_id ' \
                    #               'SET ftransaction_expect_finish_time="{0}" ' \
                    #               'WHERE asset_item_no="{1}" AND ftransaction_period={2} '.format(cap_due_time,
                    #                                                                               item,
                    #                                                                               period)
                    # self.db_biz.execute_mysql(sql_ftr_biz)

        return item_no, item_no_x, ""

    def upate_capital_asset_grant_time(self, item, advance_month, advance_day):
        """
        更新biz的capital_asset的放款时间
        :param advance_month: 放款时间
        :param advance_day: 放款时间
        :param item: 资产编号
        :return:
        """
        grant_time = self.get_update_str(advance_month, advance_day, "capital_asset_granted_at")
        push_at_time = self.get_update_str(advance_month, advance_day, "capital_asset_push_at")
        capital_item_no_str = 'update capital_asset set capital_asset_granted_at = {0}, ' \
                              'capital_asset_push_at = {1} where capital_asset_item_no = "{2}"' \
                              ''.format(grant_time, push_at_time, item)
        if self.country == "china":
            self.db_biz.execute_mysql(capital_item_no_str)
        self.db_rbiz.execute_mysql(capital_item_no_str)

    def update_asset_grant_time(self, item, advance_month, advance_day):
        # 第一期的时候，更新asset记录
        grant_time = self.get_update_str(advance_month, advance_day, "asset_grant_at")
        asset_effect_time = self.get_update_str(advance_month, advance_day, "asset_effect_at")
        actual_grant_time = self.get_update_str(advance_month, advance_day, "asset_actual_grant_at")
        item_no_str = 'update asset set asset_grant_at = {0}, asset_effect_at = ' \
                      '{1}, asset_actual_grant_at = {2}' \
                      ' where asset_item_no = "{3}"'.format(grant_time, asset_effect_time, actual_grant_time, item)
        if self.country == 'china':
            self.db_biz.execute_mysql(item_no_str)
        self.db_rbiz.execute_mysql(item_no_str)

    def update_asset_tran_due_at(self, item, advance_month, advance_day):
        # 更新asset_tran记录
        update_str = self.get_update_str(advance_month, advance_day, "asset_tran_due_at")
        item_no_period_first = 'update asset_tran set asset_tran_due_at = {0} ' \
                               'where asset_tran_asset_item_no = "{1}"'.format(update_str, item)
        if self.country == 'china':
            self.db_biz.execute_mysql(item_no_period_first)
        self.db_rbiz.execute_mysql(item_no_period_first)

    # dt 和 ft 不用了，屏蔽此方法
    # def update_biz_trans_due_at(self, item, advance_month, advance_day):
    #     # 更新asset_tran记录
    #     update_dtransaction_str = self.get_update_str(advance_month, advance_day, "dtransaction_expect_finish_time")
    #     update_ftransaction_str = self.get_update_str(advance_month, advance_day, "ftransaction_expect_finish_time")
    #     item_no_period_first_dt = 'update dtransaction set dtransaction_expect_finish_time = {0} WHERE ' \
    #                               'dtransaction_asset_id IN(SELECT asset_id FROM asset WHERE asset_item_no="{1}") ' \
    #                               ''.format(update_dtransaction_str, item)
    #     item_no_period_first_ft = 'update ftransaction set ftransaction_expect_finish_time = {0} WHERE ' \
    #                               'ftransaction_asset_id IN(SELECT asset_id FROM asset WHERE asset_item_no="{1}") ' \
    #                               ''.format(update_ftransaction_str, item)
    #     print('update_d_tran_due_at: ', item_no_period_first_dt)
    #     print('update_d_tran_due_at: ', item_no_period_first_ft)
    #     self.db_biz.execute_mysql(item_no_period_first_dt)
    #     self.db_biz.execute_mysql(item_no_period_first_ft)

    def update_rbiz_capital_tran_due_at(self, item, advance_month, advance_day):
        # 更新capital_tran记录
        update_str = self.get_update_str(advance_month, advance_day, "capital_transaction_expect_finished_at")
        item_no_period_first = 'update capital_transaction set capital_transaction_expect_finished_at={0} ' \
                               'where capital_transaction_item_no = "{1}"'.format(update_str, item)
        self.db_rbiz.execute_mysql(item_no_period_first)

    def update_biz_capital_tran_due_at(self, item, advance_month, advance_day):
        expect_finished_at_str = self.get_update_str(advance_month, advance_day,
                                                     "capital_transaction_expect_finished_at")
        expect_operate_at_str = self.get_update_str(advance_month, advance_day, "capital_transaction_expect_operate_at")
        user_repay_at_str = self.get_update_str(advance_month, advance_day, "capital_transaction_user_repay_at")
        actual_operate_at_str = self.get_update_str(advance_month, advance_day, "capital_transaction_actual_operate_at")
        update_biz_capital_str = 'update capital_transaction set capital_transaction_expect_finished_at={0}, ' \
                                 'capital_transaction_expect_operate_at={1}, ' \
                                 'capital_transaction_user_repay_at=(case capital_transaction_user_repay_at ' \
                                 'when "1000-01-01 00:00:00" then "1000-01-01 00:00:00" else {2} end),' \
                                 'capital_transaction_actual_operate_at=(case capital_transaction_actual_operate_at ' \
                                 'when "1000-01-01 00:00:00" then "1000-01-01 00:00:00" else {3} end) ' \
                                 'where capital_transaction_asset_item_no = "{4}"'.format(expect_finished_at_str,
                                                                                          expect_operate_at_str,
                                                                                          user_repay_at_str,
                                                                                          actual_operate_at_str,
                                                                                          item)
        if self.country == 'china':
            self.db_biz.execute_mysql(update_biz_capital_str)

    def change_asset(self, advance_month, item_no, item_no_x, advance_day=-1, change_cp=True, compensate_time=None):
        """
        修改资产放款时间及资产还款计划的到日期
        :param advance_month: 提前多少个月, 负数，推后是正数
        :param advance_day: 提前多少天, 负数，推后是正数
        :param item_no: 大单资产编号
        :param item_no_x: 小单资产编号
        :param change_cp: 是否是放款日
        :param compensate_time: 代偿时间,相比asset_tran的到期日多往前推多少天时间
        :return:
        """
        for item in (item_no, item_no_x):
            if not item_no_x:
                continue
            asset_tran_str = 'select asset_tran_due_at from asset_tran where asset_tran_asset_item_no = "{0}"' \
                             ' and asset_tran_period = 1 and asset_tran_type = "repayprincipal"'.format(item)
            asset_tran_due_at = self.db_rbiz.query_mysql(asset_tran_str)[0][0]
            asset_tran_due_date = datetime.date(asset_tran_due_at.year, asset_tran_due_at.month, asset_tran_due_at.day)
            real_now = get_calc_date(datetime.date.today(), month=advance_month + 1, day=advance_day, is_str=False)
            cal_advance_month = self.calmonths(asset_tran_due_date, real_now)
            cal_due_date = get_calc_date(asset_tran_due_date, month=cal_advance_month, is_str=False)
            cal_advance_day = self.caldays(cal_due_date, real_now)
            if compensate_time is not None and isinstance(compensate_time, int):
                compensate_real_now = get_calc_date(datetime.date.today(),
                                                    month=advance_month + 1,
                                                    day=advance_day - compensate_time,
                                                    is_str=False)
                compensate_cal_advance_month = self.calmonths(asset_tran_due_date, compensate_real_now)
                compensate_cal_advance_day = self.caldays(cal_due_date, compensate_real_now)
            else:
                compensate_cal_advance_month, compensate_cal_advance_day = cal_advance_month, cal_advance_day
            # 如果资产编号为空，则跳过
            if not item:
                continue
            # 更新rbiz的asset,capital_asset, biz的asset,capital_asset的放款时间
            self.update_asset_grant_time(item, cal_advance_month, cal_advance_day)
            # 更新asset_tran记录
            # self.update_biz_trans_due_at(item, cal_advance_month, cal_advance_day)
            self.update_asset_tran_due_at(item, cal_advance_month, cal_advance_day)
            # 如果是小单过滤掉
            if item == item_no_x:
                continue
            # 更新capital_transaction
            if change_cp:
                self.upate_capital_asset_grant_time(item, compensate_cal_advance_month, compensate_cal_advance_day)
                self.update_biz_capital_tran_due_at(item, compensate_cal_advance_month, compensate_cal_advance_day)
                self.update_rbiz_capital_tran_due_at(item, compensate_cal_advance_month, compensate_cal_advance_day)
        return item_no, item_no_x, ''


    @staticmethod
    def get_update_str(advance_month, advance_day, col_name):
        update_date_str = '(date_add' if advance_month > 0 else '(date_sub'
        update_date_str += '(date_add' if advance_day > 0 else '(date_sub'
        update_date_str += '({0}, interval {1} day), interval {2} month))'
        user_update_str = update_date_str.format(col_name, abs(advance_day), abs(advance_month))
        return user_update_str

    def wait_biz_capital_tran_changed(self, asset_tran_due_at,
                                      compensate_cal_advance_month,
                                      compensate_cal_advance_day,
                                      item_no):
        biz_capital_tran_str = 'select capital_transaction_expect_finished_at from capital_transaction where ' \
                               'capital_transaction_asset_item_no = "{0}"' \
                               ' and capital_transaction_period = 1 and ' \
                               'capital_transaction_type = "principal"'.format(item_no)
        biz_capital_tran_due_at_real = get_calc_date(asset_tran_due_at,
                                                     month=compensate_cal_advance_month,
                                                     day=compensate_cal_advance_day,
                                                     is_str=False).date()
        print('count: with {0}, {1}'.format(asset_tran_due_at, biz_capital_tran_due_at_real))
        while True:
            time.sleep(0.1)
            biz_capital_tran = self.db_biz.query_mysql(biz_capital_tran_str)[0][0]
            print('count: with {0}, {1}'.format(biz_capital_tran, biz_capital_tran_due_at_real))
            if biz_capital_tran_due_at_real == biz_capital_tran:
                break
        return biz_capital_tran_due_at_real

    def update_other_time(self, advance_month, advance_day, biz_asset_id, period):
        # 更新biz里面captial_transaction中用户还款时间和结清时间
        user_update_str = self.get_update_str(advance_month, advance_day, "capital_transaction_user_repay_at")
        actual_update_str = self.get_update_str(advance_month, advance_day, "capital_transaction_actual_operate_at")
        expect_operate_str = self.get_update_str(advance_month, advance_day, "capital_transaction_expect_operate_at")

        user_tran = 'UPDATE capital_transaction SET capital_transaction_user_repay_at = {0} ' \
                    'WHERE capital_transaction_asset_id = "{1}" ' \
                    'AND capital_transaction_user_repay_at != "1000-01-01 00:00:00" ' \
                    'and capital_transaction_period = {2}'.format(user_update_str,
                                                                  biz_asset_id,
                                                                  period)
        self.db_biz.execute_mysql(user_tran)
        actual_tran = 'UPDATE capital_transaction SET capital_transaction_actual_operate_at = {0} ' \
                      'WHERE capital_transaction_asset_id = "{1}" ' \
                      'AND capital_transaction_actual_operate_at != "1000-01-01 00:00:00" ' \
                      'and capital_transaction_period = {2}'.format(actual_update_str,
                                                                    biz_asset_id,
                                                                    period)
        self.db_biz.execute_mysql(actual_tran)

        except_tran = 'UPDATE capital_transaction SET capital_transaction_expect_operate_at = {0} ' \
                      'WHERE capital_transaction_asset_id = "{1}" AND ' \
                      'capital_transaction_period = {2}'.format(expect_operate_str, biz_asset_id, period)
        self.db_biz.execute_mysql(except_tran)

    def run_rbiz_task(self, task_id):
        url = self.rbiz_base_url + "/task/run?taskId={0}".format(task_id)
        return self.send_req(url)

    def run_gbiz_task(self, task_id):
        url = self.gbiz_base_url + "/task/run?taskId={0}".format(task_id)
        return self.send_req(url)

    @staticmethod
    def send_req(url):
        req = requests.get(url)
        req_json = json.loads(req.text)[0] if req.status_code == 200 else {}
        if req.status_code == 200 and (("code" in req and req["code"] == 0)
                                       or "code" not in req):
            return True, ""
        else:
            return False, req_json

    def run_rbiz_msg(self, msg_id):
        url = self.rbiz_base_url + "/msg/run?msgId={0}".format(msg_id)
        return self.send_req(url)

    def run_gbiz_msg(self, msg_id):
        url = self.gbiz_base_url + "/msg/run?msgId={0}".format(msg_id)
        return self.send_req(url)


class AssetImportChina(AssetImportBase):
    """
    构建数据基础类
    """

    def __init__(self, env_test, db_env):
        """
        初始化自己导入类
        :param env_test: 测试环境
        """
        super(AssetImportChina, self).__init__(env_test, country="china", db_env=db_env)
        self.source_type = ["youxi_bill"]

    def create_data(self, four_element, asset_item_no, asset_item_no_x, loan_channel, amount, source_type, count,
                    from_system_name, period_day=0):
        self.asset_import(four_element, asset_item_no, asset_item_no_x, loan_channel,
                          amount, source_type, count, from_system_name, period_day=period_day)
        self.run_gbiz_asset_import_msg(asset_item_no)
        # self.gbiz_loan_success(self.env_test, asset_item_no)
        self.sync_asset_to_rbiz(asset_item_no)
        return asset_item_no

    def asset_import(self, four_element, asset_item_no, asset_item_no_x, loan_channel, amount,
                     source_type, count, from_system_name, period_day=0):
        asset_import_params = copy.deepcopy(asset_import_info_no_loan) if loan_channel == 'noloan' else \
            copy.deepcopy(asset_import_info_loan_channel)

        asset_import_params["key"] = get_guid() + "n" if loan_channel == 'noloan' else get_guid()
        # 设置四要素
        bank_code_encrypt = four_element["bank_code_encrypt"]
        id_number_encrypt = four_element["id_number_encrypt"]
        phone_number_encrypt = four_element["phone_number_encrypt"]
        user_name_encrypt = four_element["user_name_encrypt"]

        asset_import_params['data']['asset']['source_number'] = asset_item_no_x
        asset_import_params['data']['asset']['item_no'] = asset_item_no
        asset_import_params['data']['asset']['name'] = "name_" + asset_item_no
        asset_import_params['data']['asset']['source_type'] = source_type

        if count == 1:
            asset_import_params['data']['asset']['period_type'] = "day"
            asset_import_params['data']['asset']['period_day'] = period_day
        else:
            asset_import_params['data']['asset']['period_type'] = "month"
            asset_import_params['data']['asset']['period_day'] = 0
        asset_import_params['data']['asset']['period_count'] = count

        asset_import_params['data']['asset']['amount'] = amount
        asset_import_params['data']['asset']['grant_at'] = get_calc_date_base_today()
        asset_import_params['data']['asset']['loan_channel'] = loan_channel
        asset_import_params['data']['asset']['source_number'] = asset_item_no_x

        asset_import_params['data']['repay_card']['username_encrypt'] = user_name_encrypt
        asset_import_params['data']['receive_card']['owner_name_encrypt'] = user_name_encrypt
        asset_import_params['data']['repay_card']['username_encrypt'] = user_name_encrypt
        asset_import_params['data']['receive_card']['account_name_encrypt'] = user_name_encrypt
        asset_import_params['data']['borrower']['name_encrypt'] = user_name_encrypt
        asset_import_params['data']['repayer']['name_encrypt'] = user_name_encrypt

        asset_import_params['data']['repay_card']['phone_encrypt'] = phone_number_encrypt
        asset_import_params['data']['receive_card']['phone_encrypt'] = phone_number_encrypt
        asset_import_params['data']['borrower']['tel_encrypt'] = phone_number_encrypt
        asset_import_params['data']['repayer']['tel_encrypt'] = phone_number_encrypt

        asset_import_params['data']['repay_card']['individual_idnum_encrypt'] = id_number_encrypt
        asset_import_params['data']['repay_card']['credentials_num_encrypt'] = id_number_encrypt
        asset_import_params['data']['receive_card']['owner_id_encrypt'] = id_number_encrypt
        asset_import_params['data']['borrower']['idnum_encrypt'] = id_number_encrypt
        asset_import_params['data']['repayer']['idnum_encrypt'] = id_number_encrypt

        asset_import_params['data']['repay_card']['account_num_encrypt'] = bank_code_encrypt
        asset_import_params['data']['receive_card']['num_encrypt'] = bank_code_encrypt

        asset_import_params['data']['asset']['from_system_name'] = from_system_name

        asset_import_url = self.gbiz_base_url + gbiz_asset_import_url
        resp = parse_resp_body(
            requests.request(method='post', url=asset_import_url, headers={"Content-Type": "application/json"},
                             json=asset_import_params))
        LogUtil.log_info(f'gbiz进件结束:{resp}, \n request data is :{json.dumps(asset_import_params, ensure_ascii=False)}')
        if not resp["status_code"] == 200 or (resp["status_code"] == 200 and resp["content"]["code"] != 0):
            raise ValueError("gbiz进件失败, 接口返回为{0}".format(resp))
        if not resp['content']['data']['asset_item_no'] == asset_item_no:
            raise ValueError("gbiz进件失败,接口参数为{0},接口返回为{1}".format(asset_import_params, resp))
        return asset_import_params

    def run_gbiz_asset_import_msg(self, asset_item_no):
        # 执行进件task&同步数据至rbiz
        task = GbizTask()
        task.run_task(asset_item_no, "AssetImport", excepts={"code": 0})
        msg = GbizMsg()
        msg.run_msg(asset_item_no, "AssetImportSync")
        time.sleep(1)
        gbiz_withdraw_to_rbiz(self.env_test, asset_item_no)
        time.sleep(2)

    def get_id_num(self, asset_item_no):
        get_card_no = "select card_asset_card_no from card_asset where card_asset_asset_item_no = '{0}'".format(
            asset_item_no)
        card_no = self.db_rbiz.query_mysql(get_card_no)[0][0]
        get_id_num = "select card_acc_id_num_encrypt from card where card_no = '{0}'".format(card_no)
        id_num = self.db_rbiz.query_mysql(get_id_num)[0][0]
        return id_num

    def get_order_serial_list(self, asset_item_no, status='all', query_col="withhold_order_serial_no"):
        order_str = ""
        get_order = "select {1} from withhold_order where withhold_order_reference_no in ('{0}', '{0}_noloan')".format(
            asset_item_no, query_col)
        if status != 'all':
            get_order += " and withhold_order_withhold_status in ({0})".format(status)
        order_list = self.db_rbiz.query_mysql(get_order)
        for order in order_list:
            order_str += '"{0}",'.format(order[0])
            if len(order) > 1 and order[1] not in order_str:
                order_str += '"{0}",'.format(order[1])
        return order_str

    def run_rbiz_withhold_task(self, asset_item_no):
        order_str = self.get_order_serial_list(asset_item_no,
                                               query_col="withhold_order_serial_no, withhold_order_request_no")
        task_order_no = '"{0}", "{0}_noloan", {1}'.format(asset_item_no, order_str[0:-1]) \
            if order_str else '"{0}", "{0}_noloan"'.format(asset_item_no)
        sel_task = "select task_id from task where task_status != 'close' " \
                   "and task_order_no in ({0})".format(task_order_no)
        task_list = self.db_rbiz.query_mysql(sel_task)
        for task in task_list:
            self.run_rbiz_task(task[0])

    def run_rbiz_withhold_msg(self, asset_item_no):
        id_num = self.get_id_num(asset_item_no)
        order_str = self.get_order_serial_list(asset_item_no)
        sendmsg_order_no = '"{0}", "{0}_noloan", "{1}", {2}'.format(asset_item_no, id_num, order_str[0:-1]) \
            if order_str else '"{0}", "{0}_noloan", "{1}"'.format(asset_item_no, id_num)
        sel_msg = "select sendmsg_id from sendmsg where sendmsg_status != 'close' " \
                  "and sendmsg_order_no in ({0})".format(sendmsg_order_no)
        msg_list = self.db_rbiz.query_mysql(sel_msg)
        for msg in msg_list:
            self.run_rbiz_msg(msg[0])

    def project_repay_query(self, project_num, project_type="paydayloan"):
        url = self.rbiz_base_url + project_repay_query_path.format(project_num, project_type)
        resp = parse_resp_body(requests.request(method='get', url=url))
        LogUtil.log_info(f"Dsq发起查询成功，url:{url},resp：{resp}")
        return resp

    def sync_asset_to_rbiz(self, asset_item_no):
        # 查询rbiz还款计划,如果返回不为0，则重试一次
        item_no = ""
        for x in range(0, 50):
            content = self.project_repay_query(asset_item_no)["content"]
            if "code" in content and content["code"] == 0:
                break
            time.sleep(0.1)


class AssetImportTha(AssetImportBase):
    def __init__(self, env_test, db_env):
        super(AssetImportTha, self).__init__(env_test, country="thailand", db_env=db_env)

        self.source_type = ["fee_20_normal"]

    def create_data(self, four_element, asset_item_no, asset_item_no_x, loan_channel, amount, source_type, count,
                    from_system_name, period_day=0):
        self.asset_import(four_element, asset_item_no, asset_item_no_x, loan_channel,
                          amount, source_type, count, from_system_name, period_day=period_day)
        self.gbiz_loan_success(self.env_test, asset_item_no, country=self.country)
        self.sync_asset_to_rbiz(asset_item_no)
        return asset_item_no

    def run_gbiz_asset_import_task(self, asset_item_no):
        """
        自动执行完成所有放款成功的task和msg
        :param asset_item_no:需要执行的task和msg的资产编号
        :return:
        """
        get_task_str = f'select task_id, task_type from task where task_order_no = "{asset_item_no}" and ' \
                       f'task_status="open"'
        self.check_and_add_grant_condition()
        while True:
            query_task = self.db_gbiz.query_mysql(get_task_str)
            if not query_task:
                break
            task_id, task_type = query_task[0]
            if task_type == "LoanApplyQuery":
                ret, msg = self.manual_grant_success(asset_item_no)
                if not ret:
                    raise ValueError("收到放款失败, {0}".format(msg))
            result, message = self.run_gbiz_task(task_id)
            if not result and "message" in message and '放款状态已经为成功,无需处理' not in message["message"]:
                raise ValueError("the task exec error, {0}".format(message))

    def sync_asset_to_rbiz(self, asset_item_no):
        get_msg_str = 'select sendmsg_id, sendmsg_type from sendmsg where sendmsg_order_no = "{0}" and ' \
                      'sendmsg_status="open"'.format(asset_item_no)
        msg_list = self.db_gbiz.query_mysql(get_msg_str)
        for msg_id, _ in msg_list:
            result, message = self.run_gbiz_msg(msg_id)
            if not result:
                raise ValueError("run msg'id {0} error, message is:{1}".format(result, message))

    def manual_grant_success(self, asset_item_no):
        """
        手动放款成功
        :param asset_item_no: 需要手动放款成功的资产编号
        :return:成功返回True,失败返回False
        """
        ret = False
        req_data = {
            "key": "manual_asset_{0}".format(get_guid()),
            "type": "ThaBankcardNotify",
            "from_system": "BIZ",
            "data": {
                "item_no": asset_item_no,
                "status": "repay",
                "finish_at": get_calc_date_base_today(),
                "err_msg": ""
            }
        }
        url = self.gbiz_base_url + "/tha_bankcard/changeStatus"
        req = requests.post(url, json=req_data)
        return_data = json.loads(req.text) if req.status_code == 200 else {}
        if req.status_code == 200 and return_data['code'] in (0, 1):
            ret = True
        return ret, return_data

    def check_and_add_grant_condition(self):
        """
        检查是否可以正常放款
        1、检查三张卡的当天额度是否配置，如果没有自动添加
        2、检查当天的资金渠道的计划是否配置，如果没有自动添加
        :return:无
        """
        # 1.检查额度
        grant_card = ["enc_03_2907707860035575808_482",
                      "enc_03_2905022461530087424_744",
                      "enc_03_2907707556133085184_449"]
        insert_sql = "INSERT INTO manual_account_plan(manual_account_plan_day, manual_account_plan_card_no, " \
                     "router_capital_plan_create_at, manual_account_plan_count) " \
                     "VALUES('{0}', '{1}', '{2}', 101)"
        now = get_calc_date_base_today(fmt="%Y-%m-%d")
        sel_sql = 'select count(*) from manual_account_plan where manual_account_plan_day = "{0}"'.format(now)
        count = self.db_gbiz.query_mysql(sel_sql)[0][0]
        if count < 1:
            # 当天没有额度，自动添加额度
            for card in grant_card:
                self.db_gbiz.execute_mysql(insert_sql.format(now, card))
        # 2.检查自己路由计划
        router_insert_sql = "INSERT INTO router_capital_plan(router_capital_plan_date, router_capital_plan_label, " \
                            "router_capital_plan_desc, router_capital_plan_amount, " \
                            "router_capital_plan_update_memo)VALUES('{0}', " \
                            "'tha_bankcard_7d', 'tha_bankcard7天',200000, '自动添加')".format(now)
        router_sel_sql = 'select count(*) from router_capital_plan where router_capital_plan_date = "{0}"'.format(now)
        router_count = self.db_gbiz.query_mysql(router_sel_sql)[0][0]
        if router_count < 1:
            # 当天没有计划，自动添加额度
            self.db_gbiz.execute_mysql(router_insert_sql)
        self.db_gbiz.commit_mysql()

    def asset_import(self, four_element, asset_item_no, asset_item_no_x, loan_channel, amount,
                     source_type, count, from_system_name, period_day=0):
        asset_import_params = copy.deepcopy(ASSET_IMPORT_INFO_THA)

        asset_import_params["key"] = get_guid()
        # 设置四要素
        bank_code_encrypt = four_element["bank_code_encrypt"]
        id_number_encrypt = four_element["id_number_encrypt"]
        phone_number_encrypt = four_element["phone_number_encrypt"]
        user_name_encrypt = four_element["user_name_encrypt"]

        asset_import_params['data']['asset']['item_no'] = asset_item_no
        # asset_import_params['data']['asset']['product_name'] = from_system_name
        asset_import_params['data']['asset']['source_type'] = source_type
        asset_import_params['data']['asset']['period_count'] = count
        if count == 1:
            asset_import_params['data']['asset']['period_type'] = "day"
            asset_import_params['data']['asset']['period_day'] = str(period_day)
        else:
            asset_import_params['data']['asset']['period_type'] = "month"
            asset_import_params['data']['asset']['period_day'] = 0
        asset_import_params['data']['asset']['amount'] = amount
        asset_import_params['data']['asset']['loan_at'] = get_calc_date_base_today()
        asset_import_params['data']['asset']['loan_channel'] = loan_channel
        asset_import_params['data']['asset']['source_number'] = ""
        # asset_import_params['data']['asset']['from_system_name'] = from_system_name

        asset_import_params['data']['borrower']['borrower_uuid'] = user_name_encrypt
        asset_import_params['data']['borrower']['mobile'] = phone_number_encrypt
        asset_import_params['data']['borrower']['id_num'] = id_number_encrypt
        asset_import_params['data']['borrower']['individual_uuid'] = bank_code_encrypt
        # asset_import_params['data']['borrower']['borrower_card_uuid'] = bank_code_encrypt

        asset_import_url = self.gbiz_base_url + GLOBAL_GBIZ_ASSET_IMPORT_URL
        resp = parse_resp_body(
            requests.request(method='post', url=asset_import_url, headers={"Content-Type": "application/json"},
                             json=asset_import_params))
        LogUtil.log_info(f'gbiz资产进件结束:{resp}, request is :{asset_import_params}')
        assert resp['content']['data'][
                   'asset_item_no'] == asset_item_no, f"gbiz资产进件失败,接口参数为{asset_import_params},接口返回为{resp}"
        return asset_import_params


class AssetImportPhl(AssetImportBase):
    def __init__(self, env_test, db_env):
        super(AssetImportPhl, self).__init__(env_test, country="philippines", db_env=db_env)
        self.source_type = {"nbfc_pioneer": ["service_25_normal"],
                            "nbfc_sino": ["service_25_normal"]}


class AssetImportMex(AssetImportBase):
    def __init__(self, env_test, db_env):
        super(AssetImportMex, self).__init__(env_test, country="mexico", db_env=db_env)
        self.source_type = {"nbfc_pioneer": ["service_25_normal"],
                            "nbfc_sino": ["service_25_normal"]}


class AssetImportInd(AssetImportBase):
    def __init__(self, env_test, db_env):
        super(AssetImportInd, self).__init__(env_test, country="india", db_env=db_env)
        self.source_type = {"nbfc_pioneer": ["service_25_normal"],
                            "nbfc_sino": ["service_25_normal"]}

    def asset_import(self, four_element, asset_item_no, asset_item_no_x, loan_channel, amount,
                     source_type, count, from_system_name, period_day=0):
        asset_import_params = copy.deepcopy(ASSET_IMPORT_INFO_IND)

        asset_import_params["key"] = get_guid()
        # 设置四要素
        bank_code_encrypt = four_element["bank_code_encrypt"]
        id_number_encrypt = four_element["id_number_encrypt"]
        phone_number_encrypt = four_element["phone_number_encrypt"]
        user_name_encrypt = four_element["user_name_encrypt"]

        asset_import_params['data']['asset']['item_no'] = asset_item_no
        # asset_import_params['data']['asset']['product_name'] = from_system_name
        asset_import_params['data']['asset']['source_type'] = source_type
        asset_import_params['data']['asset']['period_count'] = count
        if count == 1:
            asset_import_params['data']['asset']['period_type'] = "day"
            asset_import_params['data']['asset']['period_day'] = str(period_day)
        else:
            asset_import_params['data']['asset']['period_type'] = "month"
            asset_import_params['data']['asset']['period_day'] = 0
        asset_import_params['data']['asset']['amount'] = amount
        asset_import_params['data']['asset']['loan_at'] = get_calc_date_base_today()
        asset_import_params['data']['asset']['loan_channel'] = loan_channel
        asset_import_params['data']['asset']['source_number'] = ""
        # asset_import_params['data']['asset']['from_system_name'] = from_system_name

        asset_import_params['data']['borrower']['borrower_uuid'] = user_name_encrypt
        asset_import_params['data']['borrower']['mobile'] = phone_number_encrypt
        asset_import_params['data']['borrower']['id_num'] = id_number_encrypt
        asset_import_params['data']['borrower']['individual_uuid'] = bank_code_encrypt
        # asset_import_params['data']['borrower']['borrower_card_uuid'] = bank_code_encrypt

        asset_import_url = self.gbiz_base_url + GLOBAL_GBIZ_ASSET_IMPORT_URL
        resp = parse_resp_body(
            requests.request(method='post', url=asset_import_url, headers={"Content-Type": "application/json"},
                             json=asset_import_params))
        LogUtil.log_info(f'gbiz资产进件结束:{resp}, request is :{asset_import_params}')
        assert resp['content']['data'][
                   'asset_item_no'] == asset_item_no, f"gbiz资产进件失败,接口参数为{asset_import_params},接口返回为{resp}"
        return asset_import_params

    def sync_asset_to_rbiz(self, asset_item_no):
        get_msg_str = 'select sendmsg_id, sendmsg_type from sendmsg where sendmsg_order_no = "{0}" and ' \
                      'sendmsg_status="open"'.format(asset_item_no)
        msg_list = self.db_gbiz.query_mysql(get_msg_str)
        for msg_id, _ in msg_list:
            result, message = self.run_gbiz_msg(msg_id)
            if not result:
                raise ValueError("run msg'id {0} error, message is:{1}".format(result, message))

    def run_gbiz_asset_import_task(self, asset_item_no):
        asset_import_params = {
            "country": self.country,
            "env": self.env_test,
            "item_no": asset_item_no
        }
        resp = parse_resp_body(
            requests.request(method='post', url=GLOBAL_GBIZ_AUTO_GRANT_URL,
                             headers={"Content-Type": "application/json"},
                             json=asset_import_params))
        LogUtil.log_info(f'gbiz资产自动放款成功:{resp}, request is :{asset_import_params}')
        assert resp['status_code'] == 404, f"gbiz资产自动放款失败,接口参数为{asset_import_params},接口返回为{resp}"
