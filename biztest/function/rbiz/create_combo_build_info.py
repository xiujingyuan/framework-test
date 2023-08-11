from uuid import uuid1

from biztest.function.rbiz.CreateData import ToolBase

SEND_DATA = {
            "type": "CombineWithholdTaskHandler",
            "key": uuid1(),
            "from_system": "DSQ",
            "extend1": "",
              "data": {
                "card_num_encrypt": "enc_03_3221162075884095488_851",
                "card_user_id_encrypt": "enc_02_3221162077561817088_863",
                "card_user_name_encrypt": "enc_04_3633790_489",
                "card_user_phone_encrypt": "enc_01_3221162079155652608_641",
                "total_amount": "93688",
                "user_ip": "123.122.41.23",
                "project_list": [
                  {
                    "priority": "11",
                    "project_num": "20201609933921597973_noloan",
                    "amount": 92299,
                    "coupon_num": "",
                    "coupon_amount": None,
                    "couponType": "principal"
                  },
                  {
                    "priority": "1",
                    "project_num": "20201609933921597973",
                    "amount": 1389,
                    "coupon_num": "",
                    "coupon_amount": None,
                    "couponType": "principal"
                  }
                ],
                "order_no": "",
                "verify_code": "123456",
                "verify_seq": "202101062034235348796686157"
              }
        }


class BuildBase(ToolBase):

    def __init__(self, env_test, country, db_env):
        super(BuildBase, self).__init__(env_test, country=country, db_env=db_env)


class BuildCombineWithhold(BuildBase):
    send_type = "post"
    send_url = "/paydayloan/repay/combo-active-encrypt"
    send_data = SEND_DATA

    def __init__(self, item_no, period, env_test, country='china', db_env='test'):
        """

        :param item_no: 合并代扣的资产，格式 :item_no,item_no_noloan
        :param period: 还款期次
        :param env_test: 工具环境
        :param country: 所在国家
        :param db_env: 测试环境
        """
        super(BuildCombineWithhold, self).__init__(env_test, country=country, db_env=db_env)
        self.item_no = item_no
        self.period = period

    def calc_amount(self, item):
        get_item_str = 'select asset_tran_asset_item_no, sum(asset_tran_balance_amount) from ' \
                       'asset_tran where asset_tran_asset_item_no = "{0}" ' \
                       'and asset_tran_period in ({1})'.format(item, self.period)
        item_no_list = self.db_rbiz.execute_mysql(get_item_str)[0]
        return item_no_list[0] if item_no_list else 0

    def update_element_four(self, element):
        self.send_data["data"]["card_num_encrypt"] = element["card_num_encrypt"]
        self.send_data["data"]["card_user_id_encrypt"] = element["card_user_id_encrypt"]
        self.send_data["data"]["card_user_name_encrypt"] = element["card_user_name_encrypt"]
        self.send_data["data"]["card_user_phone_encrypt"] = element["card_user_phone_encrypt"]

    def update_agreement_repay(self):
        pass

    def update_item_no_and_amount(self):
        for item in self.item_no.split(","):
            asset_amount = self.calc_amount(item)
            self.send_data["data"]["project_list"][0]["project_num"] = item
            self.send_data["data"]["project_list"][0]["amount"] = asset_amount

    def get_build_info(self):
        self.update_element_four()
        self.update_item_no_and_amount()
        return self.send_data, self.send_type, self.send_url
