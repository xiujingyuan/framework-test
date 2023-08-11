from flask import request, jsonify
from app.contract_tool import contract_tool
from biztest.util.task.task import TaskContract
from biztest.interface.contract.contract_interface import contract_query
import common.global_const as gc
from biztest.util.log.log_util import LogUtil


@contract_tool.route('/contract-sign', methods=['POST'])
def contract_sign():
    LogUtil.log_info("request：%s" % request.json)
    request_params = request.json
    country = request_params.get("country", "china")
    environment = request_params.get("environment", "test")
    env = request_params.get("env", "1")
    item_no = request_params.get("item_no", "")

    if env == "" or item_no == "":
        code, message = 1, "参数不能为空"
    elif country != "china":
        code, message = 1, "不支持的国家"
    else:
        gc.init_env(env, country, environment)
        try:
            task = TaskContract()
            task.run_task_until_close_or_timeout(item_no, times=10)
            contract_data = contract_query(item_no)
            code, message = 0, "成功"
        except Exception as e:
            code, message = 1, "签约失败：%s" % e
    resp = {
        "code": code,
        "message": message,
        "data": None
    }
    if code == 0:
        resp["data"] = contract_data["data"]
    LogUtil.log_info("response: %s" % resp)
    return jsonify(resp)
