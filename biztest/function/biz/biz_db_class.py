from biztest.function.gbiz.gbiz_db_function import get_asset_info_by_item_no
from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import *
import common.global_const as gc


class RepayDbBase(object):
    db = DataBase('rbiz{0}'.format(gc.ENV), gc.ENVIRONMENT)


class BizDbBase(object):
    db = DataBase('biz{0}'.format(gc.ENV), gc.ENVIRONMENT)

    def get_signal_amount_bond_by_item_no_period(self, item_no, period):
        """
        获取兰州单期本息+担保费
        :return:
        """
        sql = "select capital_transaction_type, capital_transaction_amount from biz2.capital_transaction " \
              "where capital_transaction_asset_item_no = '{0}' and capital_transaction_period = {1} and " \
              "capital_transaction_type in ('principal', 'interest', 'guarantee')".format(item_no,
                                                                                          period)
        fee_result = self.db.do_sql(sql)
        fee_result = list(map(lambda x: int(x['capital_transaction_amount']), fee_result))
        return float(fee_result[-1] / 100), float((fee_result[0] + fee_result[1]) / 100)

    def update_capital_notify_plan_at_by_id(self, capital_notify_id, plan_at):
        sql = 'update capital_notify set capital_notify_plan_at = "{0}" where capital_notify_id={1}'.format(
            plan_at,
            capital_notify_id)
        self.db.do_sql(sql)

    def get_biz_asset_info_by_item_no(self, item_no):
        sql = "select * from asset where asset_item_no='%s'" % item_no
        asset_info = self.db.query(sql)
        return asset_info

    def get_biz_asset_tran_by_item_no(self, item_no):
        sql = "select * from asset_tran where asset_tran_asset_item_no='%s' " \
              "group by asset_tran_period,asset_tran_amount" % item_no
        asset_tran = self.db.query(sql)
        return asset_tran

    def get_biz_capital_asset_by_item_no(self, item_no):
        sql = "select * from capital_asset where capital_asset_item_no='%s'" % item_no
        capital_asset = self.db.query(sql)
        return capital_asset

    def get_biz_capital_transaction_expect_by_item_no(self, item_no, period):
        sql = 'select capital_transaction_expect_finished_at from capital_transaction where ' \
              'capital_transaction_asset_item_no = "{0}"' \
              ' and capital_transaction_period = {1} and ' \
              'capital_transaction_type = "principal"'.format(item_no, period)
        capital_transaction_expect_finished_at = self.db.query(sql)[0]['capital_transaction_expect_finished_at']
        return capital_transaction_expect_finished_at

    def get_biz_capital_asset_tran_by_item_no(self, item_no):
        sql = "select * from capital_transaction where capital_transaction_asset_item_no='%s'" % item_no
        capital_transaction = self.db.query(sql)
        return capital_transaction

    def get_loan_id_by_item_no(self, item_no):
        sql = "select asset_loan_record_due_bill_no from asset_loan_record where " \
              "asset_loan_record_asset_id = (select asset_id from asset where asset_item_no = '{0}')".format(item_no)
        return self.db.query(sql)[0]

    def get_sum_amount(self, item_no, period, capital_type):
        capital_type = '","'.join(capital_type.split(","))
        sql = 'select sum(capital_transaction_amount) as total_amount from capital_transaction where ' \
              'capital_transaction_asset_item_no = "{0}" and capital_transaction_period = {1} ' \
              'and capital_transaction_type in ("{2}")'.format(item_no, period, capital_type)
        return self.db.query(sql)[0]

    def get_biz_capital_transaction_by_item_no_period(self, item_no, period):
        sql = "select capital_transaction_period, capital_transaction_type, capital_transaction_origin_amount " \
              "from capital_transaction " \
              "where capital_transaction_asset_item_no='{0}' " \
              "and capital_transaction_period={1}".format(item_no, period)
        capital_transaction = self.db.query(sql)
        return capital_transaction

    def set_capital_loan_condition(self, channel, period_type, period_count):
        period_day = 30 if int(period_count) == 1 else 0
        sql = "delete from capital_loan_condition where " \
              "capital_loan_condition_channel='%s' and capital_loan_condition_day='%s' " \
              "and capital_loan_condition_period_count='%s'" % (channel, get_date(fmt="%Y-%m-%d"), period_count)
        self.db.delete(sql)
        sql = "INSERT INTO `capital_loan_condition` (`capital_loan_condition_day`, " \
              "`capital_loan_condition_channel`, `capital_loan_condition_amount`, `capital_loan_condition_from_system`, " \
              "`capital_loan_condition_sub_type`, `capital_loan_condition_period_count`, " \
              "`capital_loan_condition_period_type`, `capital_loan_condition_period_days`, " \
              "`capital_loan_condition_description`, `capital_loan_condition_update_memo`) " \
              "VALUES ('%s', '%s', 300000000, 'dsq', 'multiple', %s, '%s', '%s', '%s期自动化创建', '自动化创建')" % \
              (get_date(fmt="%Y-%m-%d"), channel, period_count, period_type, period_day, period_count)
        self.db.insert(sql)

    def set_asset_contract_subject(self, item_no, subject):
        sql = "INSERT INTO asset_contract_subject" \
              "(asset_contract_subject_asset_id, asset_contract_subject_asset_item_no,asset_contract_subject_status, " \
              "asset_contract_subject_part, asset_contract_subject_create_at,asset_contract_subject_update_at, " \
              "asset_contract_subject_current_period,asset_contract_subject_share_benefit_period, " \
              "asset_contract_subject_benefit_company_name,asset_contract_subject_benefit_company_code)" \
              "VALUES (1111, '%s', 'unfinished', '%s', '2019-08-01 18:23:40', '2019-08-01 18:23:40', " \
              "0, 0,'云智对应APP公司', 'v_yunzhi_1')" % (item_no, subject)
        self.db.insert(sql)

    def set_asset_status(self, item_no, status):
        sql = "update asset set asset_status = '%s' where asset_item_no = '%s'" % (status, item_no)
        self.db.update(sql)

    def delete_capital_asset_by_item_no(self, item_no, channel='noloan'):
        sql = "delete from capital_asset where " \
              "capital_asset_item_no='%s' and capital_asset_channel='%s'" % (item_no, channel)
        self.db.delete(sql)

    def delete_capital_transaction_by_item_no(self, item_no, channel='noloan'):
        sql = "DELETE FROM capital_transaction WHERE capital_transaction_asset_id IN (SELECT capital_asset_id FROM " \
              "capital_asset  WHERE capital_asset_item_no='%s' and capital_asset_channel='%s')" % (item_no, channel)
        self.db.delete(sql)

    def create_attachment(self, item_no, attachment_type, attachment_name, attachment_url):
        sql = "INSERT INTO `asset_attachment` (" \
              "`asset_attachment_asset_item_no`, `asset_attachment_type`, `asset_attachment_contract_code`, " \
              "`asset_attachment_type_text`, `asset_attachment_url`, " \
              "`asset_attachment_status`, `asset_attachment_from_system`) " \
              "VALUES ('%s', %s, '%s', '%s', '%s', 1, 'contract')" % \
              (item_no, attachment_type, get_random_str(10), attachment_name, attachment_url)
        result = self.db.insert(sql)
        return result

    def set_asset_loan_channel(self, item_no, channel):
        sql = "update asset set asset_loan_channel = '%s' where asset_item_no = '%s'" % (channel, item_no)
        self.db.update(sql)

    def change_asset_due_at_in_biz(self, advance_month, item_no, item_no_x, is_grant_day=False, advance_day=-1,
                                   compensate_time=None):
        """
        修改资产放款时间及资产还款计划的到日期
        :param advance_month: 提前多少个月, 负数，推后是正数
        :param advance_day: 提前多少天, 负数，推后是正数
        :param item_no: 大单资产编号
        :param item_no_x: 小单资产编号
        :param compensate_time: 资方还款计划代偿日
        :param is_grant_day: 是否是放款日
        :return:
        """
        asset = get_asset_info_by_item_no(item_no)
        count = int(asset[0]["asset_period_count"])
        period_day = int(asset[0]["asset_product_category"])
        if count == 1:
            grant_time = get_calc_date_base_today(day=0) if is_grant_day else \
                get_calc_date_base_today(day=advance_day)
        else:
            grant_time = get_calc_date_base_today(month=advance_month) if is_grant_day else \
                get_calc_date_base_today(month=advance_month, day=advance_day)
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
                # 更新asset记录
                if item:
                    if period == 1:
                        item_no_str = 'update asset set asset_grant_at = "{0}", asset_effect_at = ' \
                                      '"{0}", asset_actual_grant_at = "{0}"' \
                                      ' where asset_item_no = "{1}"'.format(grant_time,
                                                                            item)
                        self.db.update(item_no_str)
                        # 更新capital_asset
                        capital_asset_str = 'update capital_asset set capital_asset_granted_at = "{0}" where ' \
                                            'capital_asset_item_no = "{1}"'.format(grant_time, item)
                        self.db.update(capital_asset_str)
                    # 更新asset_tran记录
                    item_no_period_first_dt = 'update dtransaction set dtransaction_expect_finish_time = "{0}" WHERE ' \
                                              'dtransaction_asset_id IN(SELECT asset_id FROM asset WHERE ' \
                                              'asset_item_no="{1}") and dtransaction_period = {2}'.format(due_time,
                                                                                                          item, period)
                    item_no_period_first_ft = 'update ftransaction set ftransaction_expect_finish_time = "{0}" WHERE ' \
                                              'ftransaction_asset_id IN(SELECT asset_id FROM asset WHERE ' \
                                              'asset_item_no="{1}") and ftransaction_period = {2}'.format(due_time,
                                                                                                          item, period)
                    self.db.update(item_no_period_first_dt)
                    self.db.update(item_no_period_first_ft)

                    item_no_period_first = 'update asset_tran set asset_tran_due_at = "{0}"  ' \
                                           'where asset_tran_asset_item_no = "{1}" and ' \
                                           'asset_tran_period = {2}'.format(due_time, item, period)
                    self.db.update(item_no_period_first)

                    capital_tran = 'UPDATE capital_transaction SET capital_transaction_expect_finished_at = "{0}" ' \
                                   'WHERE capital_transaction_asset_id in (SELECT capital_asset_id FROM capital_asset ' \
                                   'WHERE capital_asset_item_no= "{1}") AND capital_transaction_period = {2}'.format(
                        cap_due_time, item, period)
                    self.db.update(capital_tran)

        return item_no, item_no_x, ""

    def wait_biz_asset_appear(self, item_no, wait_time=120):
        result = False
        for i in range(wait_time):
            asset = self.get_biz_asset_info_by_item_no(item_no)
            if asset is not None and len(asset) > 0:
                result = True
                break
            else:
                time.sleep(1)
        return result

    def update_asset(self, item_no, **kwargs):
        sql_params = ""
        for key, value in kwargs.items():
            sql_params = sql_params + "`" + key + "`='" + value + "', "
        sql = "update asset set {0} where asset_item_no='{1}'".format(sql_params[:-2],
                                                                      item_no)
        self.db.update(sql)

    def update_asset_extend_by_item_no(self, item_no, **kwargs):
        asset = self.get_biz_asset_info_by_item_no(item_no)
        sql_params = ""
        for key, value in kwargs.items():
            sql_params = sql_params + "`" + key + "`='" + value + "', "
        sql = "update asset_extend set {0} where asset_extend_asset_id='{1}'".format(sql_params[:-2],
                                                                                     asset[0]['asset_id'])
        self.db.update(sql)

    def wait_central_task_appear(self, order_no, task_type, begin_time, timeout=60, is_one=False):
        task_list = []
        sql = "select task_id, task_type, task_status from central_task where " \
              "task_order_no='{0}' and task_status ='open' and task_type = '{1}' and task_create_at >='{2}' " \
              "order by task_id desc".format(order_no,
                                             task_type,
                                             begin_time
                                             )
        for i in range(timeout):
            task_list = self.db.query(sql)
            if task_list:
                return task_list
            time.sleep(1)
        if not task_list:
            raise Exception("no task found, task_order_no:%s, task_type:%s" % (order_no, task_type))
        if len(task_list) > 1 and is_one:
            raise ValueError("must need one task,but there found more than one with order is :{0}"
                             ", type is :{1}".format(order_no, task_type))

    def check_central_task_not_appear(self, order_no, task_type, timeout=60):
        task_list = []
        sql = "select task_id, task_type, task_status from central_task where task_order_no='{0}' " \
              "and task_status ='open' and task_type = '{1}' order by task_id desc".format(order_no, task_type)
        for i in range(timeout):
            task_list = self.db.query(sql)
            time.sleep(0.1)

        return task_list

    def wait_central_task_close_by_id(self, task_id, timeout=100):
        task_list = []
        sql = "select * from central_task where task_id='{0}' " \
              " and task_status ='close' ".format(task_id)
        for i in range(timeout):
            task_list = self.db.query(sql)
            if task_list:
                break
            time.sleep(0.1)
        if not task_list:
            raise Exception("no task found, task_id:{0}".format(task_id))

    def update_before_capital_tran_finish_by_item_no_and_period(self, item_no, period):
        sql = "update capital_transaction set capital_transaction_operation_type='compensate', " \
              "capital_transaction_repaid_amount=capital_transaction_origin_amount, " \
              "capital_transaction_status='finished', " \
              "capital_transaction_repaid_amount=capital_transaction_origin_amount" \
              " where capital_transaction_asset_item_no='{0}' " \
              "and capital_transaction_period < {1}".format(item_no, period)
        self.db.update(sql)

    def get_user_at_count(self, item_no):
        sql = "select count(1) as count from central_task where task_order_no in ('{0}') " \
              "and task_status='open' and task_type='CapitalAssetUserRepay'".format(item_no)
        return self.db.query(sql)[0]['count']

    def get_central_task_request_data(self, order_no, task_type):
        sql_str = "select task_id, task_request_data from central_task where task_order_no='{0}' " \
                  "and task_type = '{1}' and task_status='open'".format(order_no, task_type)
        task_ret = self.db.query(sql_str)
        for task in task_ret:
            task['repayList'] = json.loads(task['task_request_data'])["repayList"]
            task['assetItemNo'] = json.loads(task['task_request_data'])["assetItemNo"]
            task['rechargeList'] = json.loads(task['task_request_data'])["rechargeList"][0]["serialNo"]
        return task_ret

    def get_central_task_request_data_by_id(self, task_id):
        sql = "select task_id, task_request_data from central_task where task_id={0} ".format(task_id)
        task_ret = self.db.query(sql)
        for task in task_ret:
            task['repayList'] = json.loads(task['task_request_data'])["repayList"]
            task['assetItemNo'] = json.loads(task['task_request_data'])["assetItemNo"]
            task['rechargeList'] = json.loads(task['task_request_data'])["rechargeList"][0]["serialNo"]
        return task_ret[0]

    def get_central_task_by_id(self, task_id):
        sql = "select * from central_task where task_id={0} ".format(task_id)
        return self.db.query(sql)

    def get_central_task_id_by_order_no(self, order_no):
        sql = "update central_task set task_next_run_at = DATE_SUB(now(), interval 20 minute) " \
              "where task_order_no = '{0}'".format(order_no)
        self.db.update(sql)
        sql = "select task_id, task_status from central_task where task_order_no='{0}' " \
              "order by task_id desc".format(order_no)
        task_list = self.db.query(sql)
        return task_list

    def get_central_msg_id_by_order_no(self, order_no):
        sql = "select * from central_sendmsg where sendmsg_order_no='{0}'".format(order_no)
        msg_list = self.db.query(sql)
        return msg_list

    def get_capital_notify_by_asset_item_no(self, item_no, notify_status='open'):
        sql = 'select * from capital_notify where capital_notify_asset_item_no="{0}" and capital_notify_status="{1}"' \
              ''.format(item_no, notify_status)
        capital_notify = self.db.query(sql)
        return capital_notify

    def get_capital_notify_exist(self, item_no, period, notify_type):
        if not isinstance(notify_type, str):
            raise TypeError('need str, but {0} type found!'.format(notify_type))
        notify_type = tuple(notify_type.split(','))
        sql = 'select * from capital_notify where capital_notify_asset_item_no="{0}" and capital_notify_status=' \
              '"open" and capital_notify_period_start = {1} and capital_notify_type in {2}' \
              ''.format(item_no, period, notify_type)
        capital_notify = self.db.query(sql)
        return True if capital_notify else False

    def set_central_task_open(self, task_id):
        sql = "update central_task set task_status = 'open', " \
              "task_next_run_at = current_time where task_id = {0}".format(task_id)
        self.db.do_sql(sql)

    def get_holiday(self, date):
        sql = 'select holiday_status from holiday where holiday_date = "{0} 00:00:00"'.format(date)
        return self.db.query(sql)

    def set_holiday(self, date, is_holiday):
        is_holiday = 1 if is_holiday else 0
        sql = "insert into holiday (holiday_date, holiday_status) values ('{0} 00:00:00', {1})".format(date, is_holiday)
        self.db.do_sql(sql)

    def update_holiday(self, date, is_holiday):
        is_holiday = 1 if is_holiday else 0
        sql = 'update holiday set holiday_status={1} where holiday_date="{0}  00:00:00"'.format(date, is_holiday)
        self.db.do_sql(sql)

    def get_capital_notify_record(self, item_no, start_period, end_period, notify_type, status):
        notify_type = '","'.join(notify_type.split(',')) if ',' in notify_type else notify_type
        sql = 'select * from capital_notify where capital_notify_asset_item_no="{0}" and' \
              ' capital_notify_period_start={1} ' \
              'and capital_notify_period_end={2} and capital_notify_type in ("{3}") ' \
              'and capital_notify_status="{4}"'.format(item_no, start_period, end_period, notify_type, status)
        capital_notify = self.db.query(sql)
        return capital_notify

    def get_central_task_by_task_order_no(self, order_no):
        sql = 'select * from central_task where task_order_no="{0}"'.format(order_no)
        task = self.db.query(sql)
        return task

    def get_central_task_by_task_order_no_and_task_type(self, order_no, task_type):
        sql = 'select * from central_task where task_order_no="{0}" and task_type="{1}"'.format(order_no, task_type)
        task = self.db.query(sql)
        return task

    def get_central_task_by_task_type_and_create_at(self, task_type, create_at):
        sql = 'select * from central_task where task_create_at>="{0}" and task_type="{1}"'.format(create_at, task_type)
        task = self.db.query(sql)
        return task

    def get_central_sendmsg_by_order_no_and_type(self, order_no, msg_type):
        sql = 'select * from central_sendmsg where sendmsg_order_no="{0}" and sendmsg_type="{1}"'.format(order_no,
                                                                                                         msg_type)
        task = self.db.query(sql)
        return task

    def update_capital_notify_plan_at_by_item_no(self, item_no, count_hour=1):
        sql = "update capital_notify set capital_notify_plan_at=date_sub(now(),interval {0} hour) where " \
              "capital_notify_asset_item_no='{1}'" % (count_hour, item_no)
        self.db.update(sql)
