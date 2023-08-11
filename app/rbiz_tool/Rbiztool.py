import json
import traceback
from flask import request, jsonify, Response
from app.rbiz_tool import rbiz_tool
from biztest.case.global_rbiz.base_global_repay_test import BaseGlobalRepayTest
from biztest.case.rbiz.rbiz_loan_tool import rbiz_loan_tool_auto_import, rbiz_auto_repay_internal, \
    rbiz_auto_apply_repay, rbiz_auto_overdue_asset
from biztest.function.dcs.biz_interface_dcs import BizInterfaceDcs
from biztest.interface.dcs.biz_dcs_interface import run_task_in_biz_dcs
from biztest.interface.gbiz_global import gbiz_global_interface
from biztest.interface.rbiz import rbiz_global_interface
from biztest.util.db.db_util import DataBase, get_four_element_global
from biztest.util.log.log_util import LogUtil
import biztest.config.global_rbiz.global_rbiz_interface_params_config as global_param_config
from biztest.util.msgsender.msgsender import Msgsender
from biztest.util.task.task import TaskGlobal
import common.global_const as gc


@rbiz_tool.route('/')
def hello_world():
    LogUtil.log_info("/hello_world")
    return 'hello world'


@rbiz_tool.route('/run-repay-task-msg', methods=['POST'])
def run_repay_task_msg():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    env = request_params.get("env", 1)
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "test")
    gc.init_env(env, country, environment)
    item_no = request_params.get("item_no", "")
    serial_no = request_params.get("serial_no", "")

    try:
        rbiz_base = BaseGlobalRepayTest()
        rbiz_base.init()
        rbiz_base.item_no = item_no
        rbiz_base.run_all_task_by_serial_no(serial_no)
        rbiz_base.run_all_msg_after_repay_success()
        code, message = 0, "支付状态更改成功"
    except Exception as e:
        code, message = 1, str(e)
    resp = {"code": code, "message": message}
    return jsonify(resp)


@rbiz_tool.route('/rbiz-auto-repay', methods=['POST'])
def rbiz_auto_repay():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    env = request_params.get("env", 1)
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "test")
    gc.init_env(env, country, environment)

    item_no = request_params.get("item_no", "")
    status = request_params.get("status", 3)
    if not env or not item_no:
        code, message = 1, "缺少参数"
    else:
        gc.init_env(env, country, environment)
        if country == "china":
            rbiz_auto_repay_internal(env, item_no, status)
            code, message = 0, "支付状态更改成功"
        else:
            rbiz_base = BaseGlobalRepayTest()
            rbiz_base.init()
            rbiz_base.item_no = item_no
            try:
                rbiz_base.repay_asset(request_params)
                code, message = 0, "支付状态更改成功"
            except Exception as e:
                code, message = 1, str(e)
    resp = {"code": code, "message": message}
    return jsonify(resp)


@rbiz_tool.route('/rbiz-overdue-asset', methods=['POST'])
def rbiz_overdue_asset():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    env = request_params.get("env", 1)
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "test")
    gc.init_env(env, country, environment)

    item_no = request_params.get("item_no", "")
    day = int(request_params.get("day", 0))
    month = int(request_params.get("month", 0))
    period = int(request_params.get("period", 1))
    refresh = request_params.get("refresh", True)
    gc.init_env(env, country, environment)
    try:
        if not country or country == "china":
            rbiz_auto_overdue_asset(env, item_no, month, day, environment)
        else:
            rbiz_base = BaseGlobalRepayTest()
            rbiz_base.init()
            rbiz_base.item_no = item_no
            rbiz_base.update_asset_due_at(day, month, period, refresh)
        code, message = 0, "逾期资产消息发送成功"
    except Exception as e:
        code, message = 1, "逾期资产消息发送成功失败，%s" % str(e)
    finally:
        DataBase.close_connects()

    resp = {
        "code": 0,
        "msg": "ok",
        "data": {"code": code, "message": message}
    }
    return jsonify(resp)


@rbiz_tool.route('/rbiz-auto-loan', methods=['POST'])
def rbiz_auto_loan():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    env = request_params.get("env", "")
    count = request_params.get("count", 1)  # 期数
    channel = request_params.get("channel", "")
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "test")
    days = request_params.get("days", 7)

    item_no = ""
    item_no_noloan = ""
    gc.init_env(env, country, environment)
    if country == "thailand":
        from_system = "tha"
        from_app = "cherry"
        channel = "picocp_ams1"
        source_type = "mileVIPstore_bill"
    elif country == "philippines":
        from_system = "phl"
        from_app = "jasmine"
        channel = "copper_stone"
        source_type = "fee_30_normal"
    elif country == "mexico":
        from_system = "mex"
        from_app = "ginkgo"
        channel = "mangguo"
        source_type = "fee_25_normal"
    try:
        if not country or country == "china":
            item_no, item_no_noloan = rbiz_loan_tool_auto_import(env, channel, count)
        else:
            four_element = get_four_element_global()
            item_no, asset_info = gbiz_global_interface.asset_import(channel, 1, days, "day", 500000, from_system,
                                                                     from_app,
                                                                     source_type,
                                                                     four_element, withdraw_type='offline')
            gbiz_task = TaskGlobal()
            gbiz_task.run_task(item_no, "AssetImport", excepts={"code": 0})
            rbiz_global_interface.asset_grant_success_to_rbiz(item_no)
            rbiz_global_interface.capital_asset_success_to_rbiz(item_no)
            Msgsender("rbiz").run_msg_by_order_no(item_no)
            LogUtil.log_info("%s, 放款成功" % item_no)
            if country == "thailand":
                item_no_noloan, asset_info_no_loan = gbiz_global_interface.asset_import_noloan(asset_info)
                gbiz_task.run_task(item_no_noloan, "AssetImport", excepts={"code": 0})
                rbiz_global_interface.asset_grant_success_to_rbiz(item_no_noloan)
                LogUtil.log_info("%s, 放款成功" % item_no_noloan)
        code, message = 0, f"国家{country}、环境{env}、资方{channel}的资产生成成功，资产编号参见data"
    except Exception as e:
        # code, message = 1, "资产生成失败，%s" % str(e)
        code, message = 1, "资产生成失败，请检查国家是否输入错误,目前仅支持china、thailand和philippines，您的输入为：{0}, error msg: {1}".format(country, e)
    finally:
        DataBase.close_connects()

    resp = {
        "code": code,
        "message": message,
        "data": {
            "country": country,
            "asset_loan_channel": channel,
            "item_no": item_no,
            "item_no_no_loan": item_no_noloan
        }
    }
    LogUtil.log_info("response: %s" % resp)
    return Response(json.dumps(resp, ensure_ascii=False), mimetype='application/json')


@rbiz_tool.route('/capital-settle-notify', methods=['POST'])
def mock_capital_settle_notify():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    # 需要传的参数
    item_no = request_params.get("item_no")  # 资金方
    channel = request_params.get("channel", "zhongke_lanzhou")  # 资金方
    period_count = request_params.get("period_count", 12)
    period_min = request_params.get("period_min", 1)
    period_max = request_params.get("period_max", 1)
    repay_type = request_params.get("repay_type", "advance")
    withhold_channel = request_params.get("withhold_channel", "qsq")
    is_partly_amount = request_params.get("is_partly_amount", "N")
    amount_type = request_params.get("amount_type", "guarantee")
    expect_operate_at = request_params.get("expect_operate_at", global_param_config.get_date())
    # 默认参数
    env = request_params.get("env", 3)
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "test")
    gc.init_env(env, country, environment)

    try:
        advanced_clearing = BizInterfaceDcs(item_no, channel, period_count, env)
        advanced_params = advanced_clearing.capital_settlement_notify(period_min, period_max, repay_type,
                                                                      withhold_channel, is_partly_amount, amount_type,
                                                                      expect_operate_at)
        code, message = 0, ""
    except Exception as e:
        code, message = 1, "消息生成失败，%s" % str(e)
    finally:
        DataBase.close_connects()

    resp = {
        "code": code,
        "message": message,
        "data": advanced_params
    }
    LogUtil.log_info("response: %s" % resp)
    return Response(json.dumps(resp, ensure_ascii=False), mimetype='application/json')


@rbiz_tool.route('/rbiz-simple-apply-repay', methods=['POST'])
def rbiz_simple_apply_repay():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    env = request_params.get("env", "")
    item_no = request_params.get("item_no", "")
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "test")
    period = request_params.get("period", None)
    amount = request_params.get("amount", None)
    gc.init_env(env, country, environment)
    resp = []
    if env == "" or item_no == "" or period is None:
        code, message = 1, "env不能为空 item_no不能为空 period不能为空"
    else:
        try:
            resp = rbiz_auto_apply_repay(env, item_no, period, amount)
            code, message = 0, f"发起本人简易还款成功，请在rbiz{env}环境查看还款数据，资产编号为：{item_no}"
        except Exception as e:
            code, message = 1, "简易还款发起失败，%s" % str(e)
        finally:
            DataBase.close_connects()
    resp = {
        "code": code,
        "message": message,
        "data": resp
    }
    LogUtil.log_info("response: %s" % resp)
    return Response(json.dumps(resp, ensure_ascii=False), mimetype='application/json')


@rbiz_tool.route('/run_dcs_task', methods=['POST'])
def run_dcs_task():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    # 需要传的参数
    task_type = request_params.get("task_type")  # task_order_no
    item_no = request_params.get("item_no")  # task_order_no
    # 默认参数
    env = request_params.get("env", 1)
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "test")
    gc.init_env(env, country, environment)

    try:
        run_task_in_biz_dcs(task_type, item_no)
        code, message = 0, ""
    except Exception as e:
        code, message = 1, "消息生成失败，%s" % str(traceback.format_exc())
    finally:
        DataBase.close_connects()

    resp = {
        "code": code,
        "message": message
    }
    LogUtil.log_info("response: %s" % resp)
    return Response(json.dumps(resp, ensure_ascii=False), mimetype='application/json')
