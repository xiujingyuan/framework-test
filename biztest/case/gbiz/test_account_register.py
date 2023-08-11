from biztest.util.easymock.gbiz.beiyin_daqin import beiyinDaqinMock
from biztest.util.easymock.gbiz.zhongyuan_zunhao import ZhongYuanZunHaoMock
from biztest.util.easymock.gbiz.zhongke_lanzhou import ZhongkeLanzhouMock
from biztest.util.easymock.gbiz.yixin_rongsheng import YiXinRongShengMock
from biztest.util.easymock.gbiz.weipin_zhongwei import WeipinZhongweiMock
from biztest.util.easymock.gbiz.jincheng_hanchen import JinchengHanchenMock
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.function.gbiz.gbiz_check_function import *
from biztest.config.gbiz.gbiz_kv_config import *
from biztest.function.gbiz.gbiz_db_function import update_capital_account_step_update_time
from biztest.config.easymock.easymock_config import gbiz_mock
from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.util.tools.tools import get_four_element



class TestAccountRegister(BaseTestCapital):
    """
      capital_account
      author: zhimengxue
      date: 20220811
      """
    def init(self):
        super(TestAccountRegister, self).init()
        update_gbiz_payment_config(self.payment_mock.url)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.capital_account
    @pytest.mark.parametrize("channel, way",
                             [
                              ("haohanqianjingjing", "qianjingjing"),
                              ("tongrongqianjingjing", "qianjingjing"),
                              ("lanzhou_haoyue_qinjia", "qjhy"),
                              ("zhongbang_zhongji", "tq"),
                              ("hebei_wenshun_ts", "wenshun")
                             ])
    def test_paysvr_protocol_register_success(self, channel, way):
        '''
        所有走paysvr开户的资金方开户成功
        :return:
        haohanqianjingjing,tongrongqianjingjing,lanzhou_haoyue_qinjia,zhongbang_zhongji,hebei_wenshun_ts
        '''
        self.payment_mock = PaymentMock(gbiz_mock)
        four_element = get_four_element()
        item_no, asset_info = asset_import(channel, four_element, 12, 4000, '草莓', 'apr36')
        self.payment_register(self.payment_mock, channel, four_element, item_no, way)


    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.capital_account
    # def test_ref_accounts_register_success(self):
    #     '''
    #     关联WSM开户成功
    #     :return:
    #     '''
    #     four_element = get_four_element()
    #     item_no = get_item_no()
    #     channel = 'hamitianbang_xinjiang'
    #     self.payment_mock = PaymentMock(gbiz_mock)
    #     self.payment_register(self.payment_mock, channel, four_element, item_no)
    #     self.wsm_mock = WeishenmaDaxinganlingMock(gbiz_mock)
    #     wsm_channel_01 = 'wsm_dxal_account'
    #     wsm_channel_02 = 'weishenma_daxinganling'
    #     self.wsm_mock.update_protocol_sms_success()
    #     self.wsm_mock.update_protocol_confirm_success()
    #     capital_regiest_query(wsm_channel_01, four_element, item_no, from_system='strawberry')
    #     sms_seq = capital_regiest(wsm_channel_02, four_element, item_no, from_system='strawberry',
    #                               action_type='GetSmsVerifyCode', way='yeepay_weishenma_daxinganling',
    #                               step_type='PROTOCOL', seq='')[
    #         'data']['actions'][0]['extra_data']['seq']
    #     capital_regiest(wsm_channel_02, four_element, item_no, from_system='strawberry',
    #                     action_type='CheckSmsVerifyCode', way='yeepay_weishenma_daxinganling', step_type='PROTOCOL',
    #                     seq=sms_seq)
    #     capital_regiest_query(wsm_channel_01, four_element, item_no, from_system='strawberry')
    #     check_capital_account_data(item_no, four_element, "hamitianbang_xinjiang", way='tq', account_status=4,
    #                                step_status=4, account_step='PAYSVR_PROTOCOL')
    #     check_capital_account_data(item_no, four_element, 'weishenma_daxinganling', way='yeepay_weishenma_daxinganling',
    #                                account_status=0, step_status=0, account_step='PROTOCOL')

    @pytest.mark.gbiz_auto_test
    @pytest.mark.capital_account
    def test_capitalaccount_register_success(self):
        '''
        走资金方开户成功
        :return:
        '''
        four_element = get_four_element()
        # 先修改各个资金方开户的mock接口，以便开户成功
        self.beiyin_mock = beiyinDaqinMock(gbiz_mock)
        self.beiyin_mock.update_bindCard_ceck()
        self.beiyin_mock.update_bindCard_verify()
        self.beiyin_mock.update_bindCard_confirm()

        self.jchc_mock = JinchengHanchenMock(gbiz_mock)
        self.jchc_mock.update_bindCard_ceck()
        self.jchc_mock.update_bindCard_verify()
        self.jchc_mock.update_bindCard_confirm()

        self.wpzw = WeipinZhongweiMock(gbiz_mock)
        self.wpzw.update_card_pre_binding()
        self.wpzw.update_card_binding()

        self.yxrs_mock = YiXinRongShengMock(gbiz_mock)
        self.yxrs_mock.update_query_bankcard_new_user()
        self.yxrs_mock.update_account_get_msg_code_success(four_element)
        self.yxrs_mock.update_account_bind_verify(four_element)
        self.yxrs_mock.update_query_bankcard_success(four_element)

        self.zklz_mock = ZhongkeLanzhouMock(gbiz_mock)
        self.zklz_mock.update_tied_card_query_nodata()
        self.zklz_mock.update_pre_tied_card()
        self.zklz_mock.update_pretiedcardquey_success()
        self.zklz_mock.update_tied_card()
        self.zklz_mock.update_tied_card_query_success()


        for channel in ['beiyin_daqin', 'jincheng_hanchen', 'weipin_zhongwei', 'zhongyuan_zunhao']:
            item_no = get_item_no()
            if channel == 'zhongyuan_zunhao':
                self.zyzh_mock = ZhongYuanZunHaoMock(gbiz_mock)
                self.zyzh_mock.update_query_bind_card_new_user()
                self.zyzh_mock.update_pre_bind_card()
                capital_regiest_query(channel, four_element, item_no, from_system='strawberry')
                self.zyzh_mock.update_query_bind_card(four_element)
                sms_seq = capital_regiest(channel, four_element, item_no, from_system='strawberry',
                                          action_type='GetSmsVerifyCode', way='zhongyuan_zunhao', step_type='PROTOCOL',
                                          seq='')[
                    'data']['actions'][0]['extra_data']['seq']
                self.zyzh_mock.update_bind_card()
                self.zyzh_mock.update_query_bind_card_after_openaccount(four_element)
                capital_regiest(channel, four_element, item_no, from_system='strawberry',
                                action_type='CheckSmsVerifyCode', way='zhongyuan_zunhao', step_type='PROTOCOL',
                                seq=sms_seq)
                capital_regiest_query(channel, four_element, item_no, from_system='strawberry')
            else:
                capital_regiest_query(channel, four_element, item_no, from_system='strawberry')
                sms_seq = capital_regiest(channel, four_element, item_no, from_system='strawberry',
                                          action_type='GetSmsVerifyCode', way=channel, step_type='PROTOCOL', seq='')[
                    'data']['actions'][0]['extra_data']['seq']
                capital_regiest(channel, four_element, item_no, from_system='strawberry',
                                action_type='CheckSmsVerifyCode', way=channel, step_type='PROTOCOL', seq=sms_seq)
                capital_regiest_query(channel, four_element, item_no, from_system='strawberry')

                if channel in['yixin_rongsheng']:
                    check_capital_account_data(item_no, four_element, channel, channel, account_status=0, step_status=0,
                                               account_step='PROTOCOL', user_key=sms_seq)
                else:
                    check_capital_account_data(item_no, four_element, channel, channel, account_status=0, step_status=0,
                                           account_step='PROTOCOL')

    @pytest.mark.gbiz_auto_test
    @pytest.mark.capital_account
    def test_capitalaccount_register_overdue(self):
        '''
        开户时间已经过期，导致开户失败
        :return:
        '''
        # 创建测试数据，只能使用有查询接口的资金方，若无查询接口则会查询本地，本case会失败
        four_element = get_four_element()
        channel = 'beiyin_daqin'
        item_no = get_item_no()
        self.beiyin_mock = beiyinDaqinMock(gbiz_mock)
        self.beiyin_mock.update_bindCard_ceck()
        self.beiyin_mock.update_bindCard_verify()
        self.beiyin_mock.update_bindCard_confirm()

        capital_regiest_query(channel, four_element, item_no, from_system='strawberry')
        sms_seq = capital_regiest(channel, four_element, item_no, from_system='strawberry',
                                  action_type='GetSmsVerifyCode', way=channel, step_type='PROTOCOL', seq='')[
            'data']['actions'][0]['extra_data']['seq']
        capital_regiest(channel, four_element, item_no, from_system='strawberry',
                        action_type='CheckSmsVerifyCode', way=channel, step_type='PROTOCOL', seq=sms_seq)
        capital_regiest_query(channel, four_element, item_no, from_system='strawberry')
        # 修改开户步骤表时间为2天之前
        update_capital_account_step_update_time(four_element, channel, item_no)
        time.sleep(15)
        # 再次调用查询开户并检查开户状态等
        item_no_new = get_item_no()
        self.beiyin_mock.update_bindCard_ceck()
        resp = capital_regiest_query(channel, four_element, item_no_new, from_system='strawberry')
        Assert.assert_equal(0, resp['code'])
        # 账户状态为4-未开户
        Assert.assert_equal(4, resp['data']['status'])
        # 步骤状态为4-未开户
        Assert.assert_equal(1, len(resp['data']['steps']))
        check_data(resp['data']['steps'][0], step_type="PROTOCOL", interaction_type="SMS", status=4, way=channel)
        # 环节状态为4-未开户
        Assert.assert_equal(2, len(resp['data']['steps'][0]['actions']))
        check_data(resp['data']['steps'][0]['actions'][0], action_type='GetSmsVerifyCode', status=4)
        check_data(resp['data']['steps'][0]['actions'][1], action_type='CheckSmsVerifyCode', status=4)

if __name__ == "__main__":
    pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/qnn_lm.py", "--env=9"])
