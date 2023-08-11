import os
from app.list_auto_data_cases import list_auto_data_cases
from flask import jsonify

from app.tool.common_tools import get_method, formatter
from biztest.case.cmdb import *
from biztest.case.contract import *
from biztest.case.dcs import *
from biztest.case.gbiz import *
from biztest.case.global_gbiz import *
from biztest.case.global_payment import *
from biztest.case.global_rbiz import *
from biztest.case.payment import *
from biztest.case.rbiz import *


@list_auto_data_cases.route('/')
def hello_world():
    return 'hello auto test'


@list_auto_data_cases.route('/get_cases_list', methods=["GET"])
def get_cases_list():
    ret = {"code": 0, "message": "get case list success", "data": {}}
    for root, dirs, file in os.walk('biztest/case'):
        if dirs:
            for program in dirs:
                if "cache" not in program and "v" not in program:
                    ret["data"][program] = {}

        for file_name in file:
            if file_name.startswith("test_"):
                if file_name.endswith(".py"):
                    if "tool" not in file_name:
                        class_name = file_name.replace(".py", "")
                        fuc_name = get_method(formatter(class_name))
                        ret["data"][root.split("/")[-1]][file_name.replace(".py", "")] = fuc_name
    return jsonify(ret)
