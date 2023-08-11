# -*- coding: utf-8 -*-
from copy import deepcopy

from biztest.config.gbiz.gbiz_interface_params_config import gbiz_asset_import_url
from biztest.config.rbiz.params_config import *
from biztest.function.gbiz.gbiz_db_function import insert_router_load_record
from biztest.interface.rbiz.rbiz_interface import get_date_before_today, asset_grant_success_to_rbiz, \
    capital_asset_success_to_rbiz
from biztest.util.msg.msg import GbizMsg
from biztest.util.task.task import GbizTask
import requests
from biztest.util.tools.tools import parse_resp_body
import common.global_const as gc
import time
# env = get_sysconfig("--env")


class AssetImport:
    def __init__(self, item_no, channel, source_type, amount, source_number, **kwargs):
        self.item_no = item_no
        self.channel = channel
        self.source_type = source_type
        self.amount = amount
        self.source_number = source_number
        self.kwargs = kwargs
        self.env_test = gc.ENV
        self.asset_import()
        self.sync_asset_to_rbiz()

    def asset_import(self):
        if self.channel == 'noloan':
            asset_import_params = deepcopy(asset_import_info_no_loan)
            asset_import_params.update(key=get_guid() + "n")
        else:
            asset_import_params = deepcopy(asset_import_info_loan_channel)
            asset_import_params.update(key=get_guid())
            keys = {"router_load_record_key": self.item_no + self.channel,
                    "router_load_record_rule_code": self.channel + "_" + str(self.kwargs["count"]) + "month",
                    "router_load_record_principal_amount": self.amount * 100,
                    "router_load_record_status": "routed",
                    "router_load_record_channel": self.channel,
                    "router_load_record_sub_type": "multiple",
                    "router_load_record_period_count": self.kwargs["count"],
                    "router_load_record_period_type": "month",
                    "router_load_record_period_days": "0",
                    "router_load_record_sub_order_type": "",
                    "router_load_record_route_day": get_date(fmt="%Y-%m-%d"),
                    "router_load_record_idnum": asset_import_params['data']['repayer']['idnum_encrypt']}
            insert_router_load_record(**keys)

        bank_code_encrypt = self.kwargs["bank_code_encrypt"]
        id_number_encrypt = self.kwargs["id_number_encrypt"]
        phone_number_encrypt = self.kwargs["phone_number_encrypt"]
        user_name_encrypt = self.kwargs["user_name_encrypt"]
        from_system_name = self.kwargs["from_system_name"]
        count = self.kwargs["count"]

        asset_import_params['data']['asset']['source_number'] = self.source_number
        asset_import_params['data']['asset']['item_no'] = self.item_no
        asset_import_params['data']['asset']['name'] = "name_" + self.item_no
        asset_import_params['data']['asset']['source_type'] = self.source_type
        if count == 1:
            asset_import_params['data']['asset']['period_type'] = "day"
            asset_import_params['data']['asset']['period_count'] = count
            asset_import_params['data']['asset']['period_day'] = 30
        else:
            asset_import_params['data']['asset']['period_type'] = "month"
            asset_import_params['data']['asset']['period_count'] = count
            asset_import_params['data']['asset']['period_day'] = 0
        asset_import_params['data']['asset']['amount'] = self.amount
        asset_import_params['data']['asset']['grant_at'] = get_date_before_today(day=16)
        asset_import_params['data']['asset']['loan_channel'] = self.channel
        asset_import_params['data']['asset']['source_number'] = self.source_number

        asset_import_params['data']['repay_card']['username_encrypt'] = asset_import_params['data']['receive_card'][
            'owner_name_encrypt'] = \
            asset_import_params['data']['receive_card']['account_name_encrypt'] = \
            asset_import_params['data']['borrower'][
                'name_encrypt'] = \
            asset_import_params['data']['repayer']['name_encrypt'] = user_name_encrypt

        asset_import_params['data']['repay_card']['phone_encrypt'] = asset_import_params['data']['receive_card'][
            'phone_encrypt'] = \
            asset_import_params['data']['borrower']['tel_encrypt'] = asset_import_params['data']['repayer'][
            'tel_encrypt'] = phone_number_encrypt

        asset_import_params['data']['repay_card']['individual_idnum_encrypt'] = \
            asset_import_params['data']['repay_card'][
                'credentials_num_encrypt'] = \
            asset_import_params['data']['receive_card']['owner_id_encrypt'] = asset_import_params['data']['borrower'][
            'idnum_encrypt'] = \
            asset_import_params['data']['repayer']['idnum_encrypt'] = id_number_encrypt

        asset_import_params['data']['repay_card']['account_num_encrypt'] = asset_import_params['data']['receive_card'][
            'num_encrypt'] = bank_code_encrypt
        asset_import_params['data']['asset']['from_system_name'] = from_system_name

        asset_import_url = gc.GRANT_URL + gbiz_asset_import_url
        resp = parse_resp_body(
            requests.request(method='post', url=asset_import_url, headers={"Content-Type": "application/json"},
                             json=asset_import_params))
        print("gbiz进件返回", resp)
        assert resp['content']['data'][
                   'asset_item_no'] == self.item_no, f"gbiz进件失败,接口参数为{asset_import_params},接口返回为{resp}"

    def sync_asset_to_rbiz(self):
        # 执行进件task&同步数据至rbiz
        gbiz_task = GbizTask()
        gbiz_task.run_task(self.item_no, "AssetImport", excepts={"code": 0})
        # time.sleep(2)
        gbiz_msg = GbizMsg()
        gbiz_msg.run_msg(self.item_no, "AssetImportSync", excepts={"code": 0})
        time.sleep(2)
        # 直接从gbiz mock放款成功的数据
        asset_grant_success_to_rbiz(self.item_no)
        # 小单没有资方还款计划
        if self.channel != 'noloan':
            capital_asset_success_to_rbiz(self.item_no)
