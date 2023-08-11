# -*- coding: utf-8 -*-
import requests

from biztest.config.rbiz.url_config import grant_withdraw_url
from biztest.function.biz.biz_db_function import wait_biz_asset_appear, wait_biz_asset_tran_appear
from biztest.function.dcs.biz_database import update_asset_extend_ref_and_sub_order_type
from biztest.interface.gbiz.gbiz_interface import asset_import, asset_import_noloan
from biztest.interface.rbiz.biz_central_interface import run_msg_in_biz_central, run_task_in_biz_central, \
    run_type_task_biz_central
from biztest.interface.rbiz.rbiz_interface import asset_grant_success_to_rbiz, capital_asset_success_to_rbiz, \
    asset_import_success_to_rbiz_by_api, asset_withdraw_success_to_biz_by_api
from biztest.util.msg.msg import GbizMsg, Msg
from biztest.util.task.task import GbizTask
from biztest.util.tools.tools import get_four_element, parse_resp_body
import common.global_const as gc


def asset_import_and_loan_to_success(loan_channel, four_element=None, item_no='', asset_amount=8000, from_app='香蕉',
                                     count=12, sub_order_type='', script_system='rbiz'):
    if four_element is None:
        four_element = get_four_element()
    if loan_channel in ("qinnong", "qinnong_jieyi", "mozhi_jinmeixin"):
        source_type = "irr36_quanyi"
        noloan_source_type = "lieyin"
    else:
        source_type = "apr36"
        noloan_source_type = "rongdan"

    item_no, asset_info = asset_import(loan_channel, four_element, count, asset_amount, from_app, source_type,
                                       item_no=item_no,
                                       sub_order_type='')
    task_gbiz = GbizTask()
    msg_gbiz = GbizMsg()
    msg_rbiz = Msg("rbiz%s" % gc.ENV)
    task_gbiz.run_task(item_no, "AssetImport")
    msg_gbiz.run_msg(item_no, "AssetImportSync")
    asset_import_success_to_rbiz_by_api(item_no)
    run_type_task_biz_central("AssetImport", item_no)
    # biz大单同步过去之后，再同步放款成功消息
    if script_system == 'dcs':
        wait_biz_asset_appear(item_no)

    asset_grant_success_to_rbiz(item_no, source_type)
    msg_rbiz.run_msg_by_id_and_search_by_order_no(item_no)
    asset_withdraw_success_to_biz_by_api(item_no)
    run_type_task_biz_central("AssetWithdrawSuccess", item_no)
    capital_asset_success_to_rbiz(item_no)
    if script_system == 'dcs':
        wait_biz_asset_tran_appear(item_no)
    # 小单放款，小单没有资方还款计划
    item_no_noloan, asset_info_noloan = asset_import_noloan(asset_info, source_type=noloan_source_type)

    # 执行进件task&同步数据至rbiz
    task_gbiz.run_task(item_no_noloan, "AssetImport")
    msg_gbiz.run_msg(item_no_noloan, 'AssetImportSync', 1)
    asset_import_success_to_rbiz_by_api(item_no_noloan)
    run_type_task_biz_central("AssetImport", item_no_noloan)
    # biz小单同步过去之后，再同步放款成功消息
    if script_system == 'dcs':
        wait_biz_asset_appear(item_no_noloan)
    asset_grant_success_to_rbiz(item_no_noloan, sub_order_type=sub_order_type)
    msg_rbiz.run_msg_by_id_and_search_by_order_no(item_no_noloan)
    asset_withdraw_success_to_biz_by_api(item_no_noloan)
    run_type_task_biz_central("AssetWithdrawSuccess", item_no_noloan)
    if script_system == 'dcs':
        wait_biz_asset_tran_appear(item_no_noloan)
    return item_no, item_no_noloan


def gbiz_withdraw_to_rbiz(env_test, order_no):
    gbiz_withdraw_url = grant_withdraw_url
    request_body = {
        "call_back": "http://order.jmy.dsqtest.kuainiujinke.com/internal/apply/grant-notify",
        "env": "gbiz{}".format(env_test),
        "item_no": "{}".format(order_no)
    }
    resp = parse_resp_body(
        requests.request(method='post', url=gbiz_withdraw_url, headers={"Content-Type": "application/json"},
                         json=request_body))
    return resp


def get_four_element_in_rbiz():
    # 获取四要参数
    four_element_resp = get_four_element()
    four_element = {"bank_code_encrypt": four_element_resp["data"]["bank_code_encrypt"],
                    "id_number_encrypt": four_element_resp["data"]["id_number_encrypt"],
                    "phone_number_encrypt": four_element_resp["data"]["phone_number_encrypt"],
                    "user_name_encrypt": four_element_resp["data"]["user_name_encrypt"]
                    }

    return four_element
