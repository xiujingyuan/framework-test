import json, pytest, requests, time

from biztest.config.dcs.params_config import cards_info_old
from biztest.config.dcs.url_config import rbiz_base_url, rbiz_capital_plan_url, rbiz_noloan_grant_url, \
    biz_central_base_url, biz_central_asset_import_url, biz_central_asset_grant_url, biz_central_capital_plan_url
from biztest.function.dcs.biz_database import get_old_asset, insert_old_asset_noloan, \
    update_grant_at, update_due_at, get_old_noloan, get_asset
from biztest.function.dcs.database_biz import get_sendmsg_content
from biztest.util.tools.tools import get_date_before_today, parse_resp_body, get_four_element


class AssetImportGrant:
    def __init__(self, channel, source_type, **kwargs):
        self.channel = channel
        self.source_type = source_type
        self.kwargs = kwargs
        if self.kwargs["system_type"] is None:
            self.kwargs["system_type"] = "strawberry"
        if self.kwargs["env_test"] is None:
            self.kwargs["env_test"] = pytest.config.getoption("--env") if hasattr(pytest, "config") else "1"
        self.gbiz_db = "gbiz" + self.kwargs["env_test"]
        self.old_asset_item_no = None  # 旧资产放款的时候用

    # 从数据库里查询数据来构建大单进件基础参数 AssetImportSync
    def get_old_AssetSync(self):
        # 查询大单目标数据，并获取新的进件参数 （ 借款金额固定 ）
        old_asset_item_no = get_old_asset(self.channel, self.kwargs["period_count"])
        old_AssetImportSync = get_sendmsg_content(self.gbiz_db, old_asset_item_no, "AssetImportSync")
        # 此处加工大单数据，小单的处理不在此处
        grant_params_dict = json.loads(old_AssetImportSync)["body"]
        grant_params_dict["key"] = grant_params_dict["data"]["asset"]["item_no"] = self.kwargs["item_no"]
        grant_params_dict["data"]["asset"]["source_number"] = self.kwargs["item_no_noloan"]
        # grant_params_dict["data"]["asset"]["sub_order_type"] = "zhongyi"  # 融担场景新增的字段
        self.old_asset_item_no = old_asset_item_no
        asset_repay_card = grant_params_dict["data"]["repay_card"]
        asset_receive_card = grant_params_dict["data"]["receive_card"]
        return grant_params_dict, asset_repay_card, asset_receive_card

    # 进件到 biz
    def asset_import_biz(self):
        time.sleep(5.5)  # 原本此步是通过MQ自动处理，但是MQ时常有延时，故改为直接调用接口，但是gbiz的消息自动执行和调接口撞到一起了，所以先等一会儿
        # {'code': 1, 'message': '有其他同步正在进行中，请稍后重试.'}
        if self.kwargs["old"] == "Y":
            biz_import_params = self.get_old_AssetSync()[0]
        # asset_import_biz_url = biz_base_url + biz_asset_import_url
        # resp = parse_resp_body(
        #     requests.request(method='post', url=asset_import_biz_url, headers={"Content-Type": "application/json"},
        #                      json=biz_import_params))
        # print("进件到 biz", resp['content'])
        asset_import_biz_url = biz_central_base_url + biz_central_asset_import_url
        resp = parse_resp_body(
            requests.request(method='post', url=asset_import_biz_url, headers={"Content-Type": "application/json"},
                             json=biz_import_params))
        print("进件到 biz_central", resp['content'])

    # 从数据库里查询数据来构建大单放款成功基础参数    AssetWithdrawSuccess
    def get_old_AssetGrant(self):
        old_item_no = self.old_asset_item_no
        old_AssetImportSync = get_sendmsg_content(self.gbiz_db, old_item_no, "AssetWithdrawSuccess")
        grant_params_dict = json.loads(old_AssetImportSync)["body"]
        grant_params_dict["key"] = self.kwargs["item_no"]
        # 加工 asset 基础数据
        asset_params = grant_params_dict["data"]["asset"]
        asset_params["asset_item_no"] = self.kwargs["item_no"]
        asset_params["owner"] = "KN"
        asset_params["ref_order_no"] = self.kwargs["item_no_noloan"]
        asset_params["sub_order_type"] = "zhongyi"  # 融担场景新增的字段
        # asset_params["cmdb_product_number"]  #  暂时不考虑修改资产编号
        asset_params["effect_at"] = asset_params["actual_grant_at"] = get_date_before_today()
        # asset_params["principal_amount"] = asset_params["granted_principal_amount"]    #  借款金额和原来的资产保持一致
        grant_params_dict["data"]["asset"] = asset_params
        # 加工 loan_record 基础数据
        loan_record = grant_params_dict["data"]["loan_record"]
        loan_record["asset_item_no"] = self.kwargs["item_no"]
        loan_record["identifier"] = "ID_" + self.kwargs["item_no"]
        loan_record["trade_no"] = "RN_" + self.kwargs["item_no"]
        loan_record["due_bill_no"] = "KN_" + self.kwargs["item_no"]
        # loan_record["amount"] #  借款金额和原来的资产保持一致
        loan_record["finish_at"] = loan_record["grant_at"] = loan_record["push_at"] = get_date_before_today()
        grant_params_dict["data"]["loan_record"] = loan_record
        # dtransactions 和 fees 基础数据暂时不处理
        dtrans = grant_params_dict["data"]["dtransactions"]
        for dtran in dtrans:
            dtran["asset_item_no"] = self.kwargs["item_no"]
        fees = grant_params_dict["data"]["fees"]
        for fee in fees:
            fee["asset_item_no"] = self.kwargs["item_no"]
        # 加工 cards_info 基础数据
        if "cards_info" in grant_params_dict["data"]:
            pass
        else:
            cards_info_old["repay_card"] = self.get_old_AssetSync()[1]
            cards_info_old["receive_card"] = self.get_old_AssetSync()[2]

            grant_params_dict["data"]["cards_info"] = cards_info_old

        return grant_params_dict

    # 大单放款
    def asset_grant_biz(self, grant_day=0):
        if self.kwargs["old"] == "Y":
            biz_grant_params = self.get_old_AssetGrant()

        # asset_grant_biz_url = biz_base_url + biz_asset_grant_url
        # resp = parse_resp_body(
        #     requests.request(method='post', url=asset_grant_biz_url, headers={"Content-Type": "application/json"},
        #                      json=biz_grant_params))
        # print("放款到biz", resp['content'])
        asset_grant_biz_url = biz_central_base_url + biz_central_asset_grant_url
        resp = parse_resp_body(
            requests.request(method='post', url=asset_grant_biz_url, headers={"Content-Type": "application/json"},
                             json=biz_grant_params))
        print("放款到biz_central", resp['content'])

        asset_grant_rbiz_url = rbiz_base_url + rbiz_noloan_grant_url
        resp = parse_resp_body(
            requests.request(method='post', url=asset_grant_rbiz_url, headers={"Content-Type": "application/json"},
                             json=biz_grant_params))
        print("放款到rbiz", resp['content'])

    # 从数据库里查询数据来构建资方还款计划的基础参数   GrantCapitalAsset
    def get_old_CapitalAsset(self):
        old_item_no = self.old_asset_item_no
        old_CapitalAsset = get_sendmsg_content(self.gbiz_db, old_item_no, "GrantCapitalAsset")
        capital_params_dict = json.loads(old_CapitalAsset)["body"]
        # 加工 capital_asset 基础数据
        capital_params_dict["item_no"] = self.kwargs["item_no"]
        capital_params_dict["push_at"] = capital_params_dict["granted_at"] = get_date_before_today()
        # capital_params_dict["granted_amount"] = cmdb_params["principal_amount"]     #  借款金额和原来的资产保持一致
        # 加工 capital_transactions 基础数据，其他数据暂时不处理
        for iii in range(0, len(capital_params_dict["capital_transactions"])):
            capital_params_dict["capital_transactions"][iii]["item_no"] = self.kwargs["item_no"]
        return capital_params_dict

    # 资方还款计划
    def asset_capital_plan_biz(self):
        if self.kwargs["old"] == "Y":
            capital_plan_params = self.get_old_CapitalAsset()
        # asset_capital_plan_url = biz_base_url + biz_capital_plan_url
        # resp = parse_resp_body(
        #     requests.request(method='post', url=asset_capital_plan_url, headers={"Content-Type": "application/json"},
        #                      json=capital_plan_params))
        # print("biz资方还款计划", resp['content'])
        asset_capital_plan_url = biz_central_base_url + biz_central_capital_plan_url
        resp = parse_resp_body(
            requests.request(method='post', url=asset_capital_plan_url, headers={"Content-Type": "application/json"},
                             json=capital_plan_params))
        print("biz_central资方还款计划", resp['content'])

        asset_capital_plan_url_rbiz = rbiz_base_url + rbiz_capital_plan_url
        resp2 = parse_resp_body(
            requests.request(method='post', url=asset_capital_plan_url_rbiz,
                             headers={"Content-Type": "application/json"},
                             json=capital_plan_params))
        print("rbiz资方还款计划", resp2['content'])

    # 小单放款
    def asset_grant_noloan(self, grant_day=0):
        if self.kwargs["old"] == "Y":
            # 随机查询一笔小单插入到rbiz数据库，保证大单能够正常还款
            old_noloan = get_old_noloan()
            insert_old_asset_noloan(old_noloan, self.kwargs["item_no_noloan"])
            # 等放款成功后，整体修改大单的还款计划
            # check_asset_grant(self.item_no, self.item_num_no_loan, "Y")
            for ii in range(1, 20):  # 检查biz，保证后续的清分
                asset = get_asset(self.kwargs["item_no"])
                if asset:
                    break
                else:
                    time.sleep(5)
                    # run_biz_tasks(self.kwargs["env_test"], "AssetWithdrawSuccess", self.kwargs["item_no"])
            update_grant_at(get_date_before_today(), self.kwargs["item_no"])
            for ii in range(1, self.kwargs["period_count"] + 1):
                update_due_at(get_date_before_today(month=-ii)[0:10], self.kwargs["item_no"], ii)
