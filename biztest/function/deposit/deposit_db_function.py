import common.global_const as gc


def get_trade_order_by_order_no(order_no):
    sql = "select * from trade_order where order_no = '%s'" % order_no
    result = gc.DEPOSIT_DB.query(sql)
    return result


def get_trade_by_order_no(order_no):
    sql = "select * from trade where order_no = '%s'" % order_no
    result = gc.DEPOSIT_DB.query(sql)
    return result


def get_trade_by_trade_no(trade_no):
    sql = "select * from trade where trade_no = '%s'" % trade_no
    result = gc.DEPOSIT_DB.query(sql)
    return result


def get_account_by_channel_code(channel_code):
    sql = "select * from account where channel_code = '%s'" % channel_code
    result = gc.DEPOSIT_DB.query(sql)
    return result
