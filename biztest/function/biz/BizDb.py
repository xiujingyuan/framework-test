from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import *


class BizDbCls(object):
    def __init__(self, env=1):
        """
        初始化
        :param env:biz环境1～9
        """
        self.env = env
        # biz环境
        self.db = DataBase("biz".format(env))
        # 数据库链接

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

    def get_biz_capital_asset_tran_by_item_no(self, item_no):
        sql = "select * from capital_transaction where capital_transaction_item_no='%s'" % item_no
        capital_transaction = self.db.query(sql)
        return capital_transaction

    def set_capital_loan_condition(self, channel, period_type, period_count):
        if period_count == "1":
            period_day = 30
        else:
            period_day = 0
        sql = "delete from capital_loan_condition where " \
              "capital_loan_condition_channel='%s' and capital_loan_condition_day='%s' " \
              "and capital_loan_condition_period_count='%s'" % (channel, get_date(fmt="%Y-%m-%d"), period_count)
        self.db.delete(sql)
        sql = "INSERT INTO `capital_loan_condition` (`capital_loan_condition_day`, " \
              "`capital_loan_condition_channel`, `capital_loan_condition_amount`, " \
              "`capital_loan_condition_from_system`, " \
              "`capital_loan_condition_sub_type`, `capital_loan_condition_period_count`, " \
              "`capital_loan_condition_period_type`, `capital_loan_condition_period_days`, " \
              "`capital_loan_condition_description`, `capital_loan_condition_update_memo`) " \
              "VALUES ('%s', '%s', 300000000, 'dsq', 'multiple', %s, '%s', '%s', '%s期自动化创建', '自动化创建');" % \
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
              "capital_asset  WHERE capital_asset_item_no='%s' and capital_asset_channel='%s');" % (item_no, channel)
        self.db.delete(sql)
