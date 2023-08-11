# -*- coding: UTF-8 -*-
import biztest.function.gbiz.gbiz_db_function as gbiz_db_function
from biztest.config.gbiz import gbiz_kv_config
from biztest.function.rbiz import rbiz_db_function, rbiz_common_function
from biztest.function.rbiz.CreateData import AssetImportFactory
from biztest.function.rbiz.rbiz_common_function import asset_import_and_loan_to_success
from biztest.interface.gbiz import gbiz_interface
from biztest.interface.gbiz.gbiz_interface import *
from biztest.interface.rbiz import rbiz_interface
from biztest.interface.rbiz.rbiz_interface import *
from biztest.util.db.db_util import DataBase, time, get_four_element
from biztest.util.msg.msg import Msg, GbizMsg
from biztest.util.task.task import Task, GbizTask
from biztest.util.log.log_util import LogUtil
import common.global_const as gc


def get_loan_channel_by_item_no(item_no):
    """
    获取大单资方
    :param item_no:
    :return:
    """
    asset = gbiz_db_function.get_asset_import_data_by_item_no(item_no)
    if asset is None:
        return ""
    loan_channel = asset['data']['asset']['loan_channel']
    source_number = asset['data']['asset']['source_number']
    if loan_channel != "noloan":
        return loan_channel
    else:
        return get_loan_channel_by_item_no(source_number)


def rbiz_loan_tool(env, item_no, url=None):
    """
    自动放款工具 有进件的情况
    :param env: 环境1-9
    :param item_no: 资产编号
    :param url: 放款成功通知的地址
    :return: 0-放款成功，1-放款失败
    """
    LogUtil.log_info("rbiz_loan_tool...env=%s, item_no=%s" % (env, item_no))
    # 模块中定义的全局变量需要修改，改为接口传入的环境
    # 通过资产编号查询大单资方
    loan_channel = get_loan_channel_by_item_no(item_no)
    if loan_channel == "":
        return 1, "资产不存在"
    try:
        # 执行进件task&同步数据至rbiz
        gbiz_task = GbizTask()
        gbiz_task.run_task(item_no, "AssetImport", excepts={"code": 0})
        gbiz_msg = GbizMsg()
        gbiz_msg.run_msg(item_no, 'AssetImportSync', 1)
        time.sleep(10)
        asset_grant_success_to_rbiz(item_no)
        # 小单没有资方还款计划
        if loan_channel != 'noloan':
            capital_asset_success_to_rbiz(item_no)
        if url is not None:
            asset_grant_success_to_rbiz(item_no, url)
    except Exception as e:
        LogUtil.log_info("%s, 放款失败：%s" % (item_no, e))
        return 1, "放款失败：%s" % e


def rbiz_loan_tool_auto_import(env, channel_name, count=6):
    """
    自动放款工具自动进件
    :param env: 环境1-9
    :param channel_name: 资金方
    :param count:
    :return: 0-放款成功，1-放款失败
    """
    LogUtil.log_info("rbiz_loan_tool_auto_import...env=%s, channel_name=%s" % (env, channel_name))
    four_element = get_four_element()
    try:
        item_no, item_no_noloan = asset_import_and_loan_to_success(channel_name, four_element)
        LogUtil.log_info("大单资产编号：%s" % item_no)
        LogUtil.log_info("小单资产编号：%s" % item_no_noloan)
    except Exception as e:
        LogUtil.log_info("%s, 资产生成失败：%s" % (item_no, e))
        return 1, "资产生成失败：%s" % e
    return item_no, item_no_noloan


def rbiz_auto_repay_internal(env, item_no, status):
    """
    国内测试环境根据资产编号还款
    :param env: 环境1-9
    :param item_no: 资产编号
    :param status: 2-成功，3-失败
    :return: 0-还款成功，1-还款失败
    """
    LogUtil.log_info("rbiz_loan_tool...env=%s, item_no=%s" % (env, item_no))
    # 模块中定义的全局变量需要修改，改为接口传入的环境
    rbiz_msg = Msg("rbiz%s" % env)
    rbiz_task = Task("rbiz%s" % env)
    order_list = rbiz_db_function.get_withhold_order_by_item_no(item_no)
    print("order_list", order_list)
    for order in order_list:
        withhold_order_list = rbiz_db_function.get_withhold_order_by_serial_no(order["withhold_order_serial_no"])
        withhold_list = rbiz_db_function.get_withhold_by_serial_no(order["withhold_order_serial_no"])
        rbiz_interface.paysvr_callback(order["withhold_order_serial_no"], int(status))
        time.sleep(2)
        for withhold in withhold_list:
            rbiz_task.run_task_by_order_no_count(item_no)
            rbiz_msg.run_msg_by_id_and_search_by_order_no(withhold["withhold_serial_no"])
            rbiz_task.run_task_by_order_no_count(withhold["withhold_serial_no"])
        for withhold_order in withhold_order_list:
            rbiz_msg.run_msg_by_id_and_search_by_order_no(withhold_order["withhold_order_reference_no"])
    rbiz_msg.run_msg_by_id_and_search_by_order_no(withhold_list[0]["withhold_user_idnum"])


def rbiz_auto_apply_repay(env, item_no, period=None, amount=None):
    """
        国内测试环境根据资产编号还款
        :param env: 环境1-9
        :param item_no: 资产编号
        :param period: 1-当期，None-全部还
        :return: 0-还款成功，1-还款失败
    """
    LogUtil.log_info("rbiz_auto_apply_repay...env=%s, item_no=%s" % (env, item_no))
    asset_extend = get_asset_extend_val_by_item_no(item_no)
    item_no_x = asset_extend[0]['asset_extend_val'] if asset_extend else None
    if amount is None:
        asset_tran_amount = rbiz_db_function.get_asset_tran_balance_amount_by_item_no_and_period(item_no, period)
        amount = asset_tran_amount["asset_tran_balance_amount"]

    params_combo_active = {
        "project_num_loan_channel_amount": amount
    }
    if item_no_x is not None:
        asset_tran_amount_no_loan = rbiz_db_function.get_asset_tran_balance_amount_by_item_no_and_period(item_no_x,
                                                                                                         period)
        params_combo_active['project_num_no_loan_amount'] = asset_tran_amount_no_loan["asset_tran_balance_amount"]
    resp, request_body = rbiz_interface.simple_active_repay(item_no, **params_combo_active)
    return resp['content']


def rbiz_auto_overdue_asset(env, item_no, month=-1, day=-1, env_db="test"):
    """
    1. 修改资产到期日
    2. 刷罚息
    3. 重发mq消息
    :param env: 环境1-9
    :param item_no: 资产编号
    :param month: 逾期月数
    :param day: 逾期天数
    :param env_db: db配置
    :return: 0-还款成功，1-还款失败
    """
    LogUtil.log_info("rbiz_overdue_asset...env=%s, item_no=%s" % (env, item_no))
    # 模块中定义的全局变量需要修改，改为接口传入的环境
    rbiz_msg = Msg("rbiz%s" % env)
    asset_import = AssetImportFactory.get_import_obj(env, "china", env_db)
    asset_import.change_asset(
        month,
        item_no,
        "",
        advance_day=day,
    )
    rbiz_interface.refresh_late_fee(item_no)
    rbiz_interface.fix_status_asset_change_mq_sync(item_no)
    rbiz_msg.run_msg_by_id_and_search_by_order_no(item_no)


if __name__ == '__main__':
    # rbiz_loan_tool(3, "ss2020121606912198")
    # rbiz_loan_tool_auto_import(3, "shilong_siping", 12)
    # rbiz_auto_repay_internal(3, "sp20201609391086856494", 3)
    # rbiz_auto_apply_repay(3, "20201609746035441646", 1)
    rbiz_auto_overdue_asset(1, "20201617245250706784")
