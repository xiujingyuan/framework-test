# -*- coding: UTF-8 -*-
import traceback

import biztest.function.gbiz.gbiz_db_function as gbiz_db_function
import biztest.function.gbiz.gbiz_common_function as gbiz_common_function
from app.tool.common_tools import formatter
from biztest.util.msg.msg import Msg
from biztest.util.log.log_util import LogUtil
import common.global_const as gc


def get_order_type(item_no):
    """
    获取订单是大单还是小单
    :param item_no:
    :return: 大单-loan，小单-noloan
    """
    asset = gbiz_db_function.get_asset_import_data_by_item_no(item_no)
    if asset is None:
        return ""
    loan_channel = asset['data']['asset']['loan_channel']
    if loan_channel == "noloan":
        return "noloan"
    else:
        return "loan"


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


def gbiz_loan_tool(country, env, environment, item_no):
    """
    自动放款工具
    :param env: 环境1-9
    :param item_no: 资产编号
    :return: 0-放款成功，1-放款失败
    """
    LogUtil.log_info("gbiz_loan_tool...env=%s, item_no=%s" % (env, item_no))
    # 环境初始化
    gc.init_env(env, country, environment)
    # 通过资产编号查询大单资方
    loan_channel = get_loan_channel_by_item_no(item_no)
    if loan_channel == "":
        return 1, "资产不存在"
    # 初始化资金计划
    gbiz_common_function.init_capital_plan(loan_channel)
    # 动态导入资方模块
    module_name = "biztest.case.gbiz.test_" + loan_channel
    class_name = 'Test' + formatter(loan_channel)
    try:
        LogUtil.log_info("开始导入模块...%s.%s" % (module_name, class_name))
        module_obj = __import__(module_name, globals(), locals(), class_name, level=0)
        LogUtil.log_info("module_obj...%s" % module_name)
        class_obj = getattr(module_obj, class_name)()
        LogUtil.log_info("class_obj...%s" % class_obj)
    except Exception as e:
        LogUtil.log_error(traceback.format_exc())
        LogUtil.log_info("%s, 资方自动放款未实现：%s" % (loan_channel, str(traceback.format_exc())))
        return 1, "%s，资方自动放款未实现：%s" % (loan_channel, e)
    try:
        class_obj.init()
        LogUtil.log_info("开始资方放款流程...")
        # 大单
        if get_order_type(item_no) == "loan":
            class_obj.loan_to_success(item_no)
        # 小单
        else:
            class_obj.noloan_to_success(item_no)
        rbiz_msg = Msg("rbiz%s" % env)
        rbiz_msg.run_msg(item_no, 'AssetWithdrawSuccess', 1)
        LogUtil.log_info("%s, 放款成功" % item_no)
        return 0, "操作成功：资产已放款成功"
    except Exception as e:
        LogUtil.log_error(traceback.format_exc())
        LogUtil.log_info("%s, 放款失败：%s" % (item_no, str(traceback.format_exc())))
        return 1, "操作失败：发生异常：%s" % e


def gbiz_route_tool(country, env, environment, channel):
    """
    自动设置路由工具
    :param env: 环境1-9
    :param channel: 资金方
    :return: 0-路由设置成功，1-路由设置失败
    """
    # 环境初始化
    gc.init_env(env, country, environment)
    if not channel:
        channel = "tongrongqianjingjing"
    LogUtil.log_info("gbiz_route_tool...env=%s, channel=%s" % (env, channel))
    # 设置资金量使对应资金方可以路由成功
    try:
        gbiz_db_function.delete_router_capital_plan()
        gbiz_common_function.init_capital_plan(channel)
        return 0, "资金方%s路由设置成功" % channel
    except Exception as e:
        LogUtil.log_error(traceback.format_exc())
        LogUtil.log_info("资金方%s路由设置失败" % channel)
        return 1, "资金方%s路由设置失败：%s" % (channel, e)


if __name__ == '__main__':
    # gbiz_loan_tool(9, "ph_wsm_7805100981")
    gbiz_route_tool("china", 4, "dev", "haohanqianjingjing")
