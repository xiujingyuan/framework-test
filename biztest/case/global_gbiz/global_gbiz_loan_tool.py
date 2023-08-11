# -*- coding: UTF-8 -*-
import biztest.function.global_gbiz.gbiz_global_db_function as gbiz_global_db_function
import biztest.function.global_gbiz.gbiz_global_common_function as gbiz_global_common_function
from app.tool.common_tools import formatter
from biztest.config.global_gbiz.global_gbiz_kv_config import update_gbiz_capital_channel
from biztest.function.gbiz.gbiz_db_function import update_router_capital_plan_amount_all_to_zero
from biztest.util.log.log_util import LogUtil
from biztest.util.msgsender.msgsender import Msgsender
from biztest.util.task.task import TaskGlobal
import traceback
import common.global_const as gc


def get_order_type(item_no):
    """
    获取订单是大单还是小单
    :param item_no:
    :return: 大单-loan，小单-noloan
    """
    asset = gbiz_global_db_function.get_asset_import_data_by_item_no(item_no)
    if asset is None:
        return ""
    loan_channel = asset['data']['asset']['loan_channel']
    if loan_channel == "noloan":
        return "noloan"
    else:
        return "loan"


def loan_success(class_obj, item_no):
    asset = gbiz_global_db_function.get_asset_import_data_by_item_no(item_no)
    loan_type = asset.get("data").get("borrower").get("withdraw_type")
    if get_order_type(item_no) != "noloan":
        if loan_type == 'offline':
            class_obj.loan_to_success_offline(item_no)
        else:
            class_obj.loan_to_success(item_no)
    else:
        # 小单
        class_obj.noloan_to_success(item_no)
    msgsender = Msgsender("rbiz")
    msgsender.run_msg_by_order_no(item_no)
    LogUtil.log_info("%s, 放款成功" % item_no)
    return 0, "操作成功：资产已放款成功"


def loan_fail(class_obj, item_no):
    class_obj.loan_to_fail(item_no)
    loan_channel = get_loan_channel_by_item_no(item_no)
    if loan_channel:
        update_router_capital_plan_amount_all_to_zero(loan_channel)
        gbiz_global_common_function.run_terminated_task(item_no, "ChangeCapital", 1)
        gbiz_global_common_function.run_terminated_task(item_no, "AssetVoid")
        LogUtil.log_info("%s, 已通知放款失败" % item_no)
        return 0, "操作成功：资产已放款失败"
    else:
        return 1, "操作失败：发生异常"


def update_card(class_obj, item_no):
    class_obj.before_update_card_process(item_no)
    asset = gbiz_global_db_function.get_asset_info_by_item_no(item_no)[0]
    update_gbiz_capital_channel(asset["asset_loan_channel"], allow_update_card="true")
    TaskGlobal().run_task(item_no, "LoanConfirmQuery", excepts={"code": 0, "message": "放款失败,需换卡"})
    LogUtil.log_info("%s, 换卡通知已发送" % item_no)
    return 0, "操作成功：资产已发送换卡通知"


def get_loan_channel_by_item_no(item_no):
    """
    获取大单资方
    :param item_no:
    :return:
    """
    asset = gbiz_global_db_function.get_asset_import_data_by_item_no(item_no)
    if asset is None:
        return ""
    loan_channel = asset['data']['asset']['loan_channel']
    source_number = asset['data']['asset']['source_number']
    if loan_channel != "noloan":
        return loan_channel
    else:
        return get_loan_channel_by_item_no(source_number)


def global_gbiz_loan_tool(country, env, environment, item_no, status):
    LogUtil.log_info("gbiz_loan_tool...env=%s, item_no=%s, country=%s" % (env, item_no, country))
    # 环境初始化
    gc.init_env(env, country, environment)
    # 通过资产编号查询大单资方
    loan_channel = get_loan_channel_by_item_no(item_no)
    if loan_channel == "":
        return 1, "资产不存在"

    gbiz_global_common_function.init_capital_plan(country, loan_channel)
    function_map = {"loanSuccess": loan_success, "loanFail": loan_fail, "updateCard": update_card}

    # 导入模块
    module_name = "biztest.case.global_gbiz.test_country_" + country
    class_name = 'TestCountry' + formatter(country)
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
        code, msg = function_map[status](class_obj, item_no)
        return code, msg
    except Exception as e:
        LogUtil.log_error(traceback.format_exc())
        LogUtil.log_info("%s, 放款失败：%s" % (item_no, str(traceback.format_exc())))
        return 1, "操作失败：发生异常：%s" % e
    finally:
        class_obj.teardown_method()


def global_gbiz_route_tool(country, env, environment, channel):
    if channel is None or len(channel) == 0:
        return 1, "设置失败，资方为空"
    LogUtil.log_info("gbiz_route_tool...env=%s, country=%s, channel=%s" % (env, country, channel))
    # 环境初始化
    gc.init_env(env, country, environment)

    try:
        gbiz_global_common_function.init_capital_plan(country, channel)
        gbiz_global_db_function.update_all_channel_amount()
        gbiz_global_db_function.update_router_capital_plan_amount_all_to_zero(channel)
        return 0, "资金方%s路由设置成功" % channel
    except Exception as e:
        LogUtil.log_error(traceback.format_exc())
        LogUtil.log_info("资金方%s路由设置失败" % channel)
        return 1, "资金方%s路由设置失败: %s" % (channel, str(e))
