import common.global_const as gc


def get_clean_scenes_receive_by_item_no(item_no):
    sql = "select * from clean_scenes_receive where asset_item_no='%s'" % item_no
    clean_scenes_receive = gc.DCS_DB.query(sql)
    return clean_scenes_receive


def get_clean_precharge_clearing_tran_by_item_no(item_no, period=None, trans_type=None, amount_type=None,
                                                 accrual_type=None):
    """
    trans_type：还款类型：repay_before_compensate-代偿前还款，repay_after_compensate-代偿后还款，compensate-代偿
    amount_type：费用类型,principal:偿还本金, lateinterest:罚息
    accrual_type：权责类型 guarantee,scenes,part,limit,warning
    """
    sql = "select * from clean_precharge_clearing_tran where asset_item_no='%s'" % item_no
    if period is not None:
        sql += " and period = %s" % period
    if trans_type is not None:
        sql += " and trans_type = '%s'" % trans_type
    if amount_type is not None:
        sql += " and amount_type = '%s'" % amount_type
    if accrual_type is not None:
        sql += " and accrual_type = '%s'" % accrual_type
    precharge_clearing_tran = gc.DCS_DB.query(sql)
    return precharge_clearing_tran


def get_clean_accrual_tran_by_item_no(item_no, period=1, accrual_type=None):
    sql = "select * from clean_accrual_tran where asset_item_no='%s'" % item_no
    if period is not None:
        sql += " and period = %s" % period
    if accrual_type is not None:
        sql += " and accrual_type = '%s'" % accrual_type
    accrual_tran = gc.DCS_DB.query(sql)
    return accrual_tran


def get_dcs_asset_info_by_item_no(item_no):
    sql = "select * from asset where item_no='%s'" % item_no
    asset_info = gc.DCS_DB.query(sql)
    return asset_info


def get_dcs_clean_withdraw_order(business_no):
    sql = "SELECT * FROM  clean_withdraw_order WHERE  order_no ='%s' ORDER BY id DESC " % business_no
    withdraw_order_info = gc.DCS_DB.query(sql)
    return withdraw_order_info


def get_dcs_clean_deposit_withdraw_order(business_no):
    sql = "SELECT * FROM  clean_deposit_withdraw_order WHERE  order_no ='%s' ORDER BY id DESC " % business_no
    withdraw_order_info = gc.DCS_DB.query(sql)
    return withdraw_order_info


def get_dcs_clean_generic_deal_order(business_no):
    sql = "SELECT * FROM  clean_generic_deal_order WHERE  business_no ='%s' ORDER BY id DESC " % business_no
    deal_order_info = gc.DCS_DB.query(sql)
    return deal_order_info


def get_dcs_task_capitalAuditCallback(business_no):
    sql = "SELECT * FROM  clean_task WHERE  task_order_no ='%s' and  task_type='capitalAuditCallback' ORDER BY task_id DESC " % business_no
    task_info = gc.DCS_DB.query(sql)
    return task_info


def get_dcs_clean_generic_deal_trade(business_no):
    sql = "select  * from clean_generic_deal_trade WHERE order_no IN" \
          " ( SELECT order_no FROM  clean_generic_deal_order  WHERE  business_no='%s' ) order by  id desc " % business_no
    deal_trade_info = gc.DCS_DB.query(sql)
    return deal_trade_info


def get_dcs_clean_withhold_concentration_info(serial_no):
    sql = "SELECT * FROM  clean_withhold_concentration WHERE id>0  AND  serial_no='%s' order by id desc " % serial_no
    concentration_info = gc.DCS_DB.query(sql)
    return concentration_info


def get_dcs_clean_withhold_concentration_info_by_item_no(item_no):
    sql = "SELECT * FROM  clean_withhold_concentration WHERE id>0  AND  asset_item_no='%s' order by id desc " % item_no
    concentration_info = gc.DCS_DB.query(sql)
    return concentration_info


def get_clean_clearing_trans_settlement_info(item_no):
    sql = "SELECT batch_no FROM  clean_clearing_trans WHERE id>0  AND  item_no='%s'  GROUP BY batch_no   order by id desc " % item_no
    trans_info = gc.DCS_DB.query(sql)
    return trans_info
