#!/usr/bin/python
# -*- coding: UTF-8 -*-
from biztest.config.dcs.url_config import gbiz_asset_import_url
from biztest.interface.gbiz.gbiz_interface import capital_regiest_query, capital_regiest, asset_import
from biztest.function.gbiz.gbiz_db_function import get_asset_import_data_by_item_no
from biztest.util.task.task import GbizTask
from biztest.util.msg.msg import GbizMsg
from biztest.util.asserts.assert_util import Assert
from biztest.util.jaeger.jaeger import Jaeger
from biztest.util.es.es import ES
import common.global_const as gc
from biztest.util.tools.tools import get_four_element, get_date, encry_data, decrypt_data, encry_data_except


class BaseTestCapital(object):
    def init(self):
        self.task = GbizTask()
        self.msg = GbizMsg()
        self.jaeger = Jaeger("gbiz%s" % gc.ENV)
        self.es = ES("gbiz%s" % gc.ENV)

    def register(self, item_no, four_element):
        return

    def payment_register(self, mock, channel, four_element, item_no, way='qianjingjing'):
        mock.query_protocol_channels_need_bind(sign_company=way)
        mock.auto_bind_sms_success()
        result = capital_regiest_query(channel, four_element, item_no, from_system='strawberry')
        Assert.assert_equal(int(result['data']['status']), 4, '未开户的状态不正确')
        result = capital_regiest(channel, four_element, item_no, way=way, from_system='strawberry',
                                 action_type='GetSmsVerifyCode',
                                 step_type='PAYSVR_PROTOCOL', seq='')
        sms_seq = result['data']['actions'][0]['extra_data']['seq']
        mock.bind_success(four_element)
        capital_regiest(channel, four_element, item_no, way=way, from_system='strawberry',
                        action_type='CheckSmsVerifyCode',  step_type='PAYSVR_PROTOCOL',
                        seq=sms_seq)
        mock.query_protocol_channels_need_bind(bind_status='1', protocol_info='T@id', sign_company=way)
        result = capital_regiest_query(channel, four_element, item_no, from_system='strawberry')
        Assert.assert_equal(int(result['data']['status']), 0, '开户成功状态不正确')

    def loan_to_success(self, item_no):
        pass

    def noloan_to_success(self, item_no_noloan):
        asset_info = get_asset_import_data_by_item_no(item_no_noloan)
        self.task.run_task(item_no_noloan, "AssetImport", excepts={"code": 0})
        self.task.run_task(item_no_noloan, "AssetImportVerify", excepts={"code": 0})
        if asset_info["data"]["asset"]["source_type"] in ["rongdan", "rongdan_irr", "normal"]:
            self.task.run_task(item_no_noloan, "RongDanAllocate")
        self.task.run_task(item_no_noloan, "RefreshNoLoan", excepts={"code": 0})
        self.msg.run_msg(item_no_noloan, "AssetImportSync", excepts={"code": 0})
        self.msg.run_msg(item_no_noloan, "AssetWithdrawSuccess")

    def manual_grant_capital(self, channel, count, amount, app, source_type, bank_code, extend):
        four_element = get_four_element(bank_name=bank_code, id_num_begin="43")
        for key, value in extend.items():
            if not value or key == 'item_no':
                continue
            four_element['data'][key] = decrypt_data(value) if value.startswith('enc_') else value
            four_element['data'][f'{key}_encrypt'] = value if value.startswith('enc_') else encry_data_except(key, value)
        item_no, _ = asset_import(channel, four_element, count, amount, from_system_name=app,
                                  source_type=source_type, insert_router_record=False, get_info=False)
        if channel not in ('lanhai_zhongbao_rl', 'lanhai_zhilian'):
            # 前置开户
            try:
                self.register(item_no, four_element)
            except Exception as e:
                print(e)
                pass
        return {'item_no': item_no, 'element': four_element}
