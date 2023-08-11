from biztest.case.gbiz.base_test_capital import BaseTestCapital
import pytest
from biztest.config.gbiz.gbiz_kv_config import update_grouter_channel_route_config, \
    update_grouter_channel_change_config, incremental_update_config
from biztest.function.gbiz.gbiz_check_function import check_route_log, check_data, check_router_load_record, \
    check_router_load_record_data
from biztest.config.gbiz.gbiz_zhongyuan_zunhao_config import *
from biztest.function.gbiz.gbiz_db_function import update_router_weight_inactive, delete_capital_rule_code, \
    update_router_weight_first_route_status_inactive, update_router_cp_amount_all_to_zero, \
    router_capital_rule_notrelease, update_router_capital_plan_by_rule_code, \
    update_asset_loan_record_by_item_no, update_router_weight_by_channel, get_asset_loan_record_by_item_no, \
    delete_router_capital_plan, update_router_load_total, get_router_load_record_by_key, \
    update_router_load_record_by_key, wait_task_appear, get_router_capital_rule, \
    update_router_capital_plan_amount_all_to_zero, update_all_channel_amount
from biztest.function.gbiz.gbiz_common_function import init_router_rule_data, run_terminated_task, init_capital_plan, \
    get_rule_code
from biztest.interface.gbiz.gbiz_interface import asset_route, asset_import
from biztest.util.easymock.gbiz.jinmeixin_hanchen import JinmeixinHanchenMock
from biztest.util.easymock.gbiz.payment import PaymentMock
from biztest.util.tools.tools import get_four_element, get_calc_date_base_today, get_guid, date_to_timestamp, get_date
from biztest.util.asserts.assert_util import Assert
import common.global_const as gc
from biztest.config.easymock.easymock_config import gbiz_mock


class TestRoute(BaseTestCapital):
    """
       gbiz_route
       author: zhimengxue
       date: 20200628
       """
    period = 12
    period_type = "month"
    amount = 5000
    from_system = "香蕉"
    source_type = "apr36"
    expect_channel = "tongrongqianjingjing"

    @classmethod
    def teardown_class(cls):
        init_capital_plan()
        update_grouter_channel_route_config()
        update_grouter_channel_change_config()

    @classmethod
    def setup_class(cls):
        init_capital_plan()
        update_grouter_channel_route_config()
        update_grouter_channel_change_config()
        payment_mock = PaymentMock(gbiz_mock)
        payment_mock.query_protocol_channels_not_need_bind("1")

    def init(self):
        super(TestRoute, self).init()
        update_grouter_channel_route_config()
        update_grouter_channel_change_config()

    @pytest.fixture()
    def case(self):
        self.init()

    @pytest.fixture()
    def first_route_case(self):
        delete_router_capital_plan()

    @pytest.fixture()
    def rule_1(self):
        super(TestRoute, self).init()
        self.four_element = get_four_element()
        self.route_key = get_guid()
        self.rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400],
                        "routed_amount": 0,
                        "plan_amount": 1000000000
                    }
                ]
            }
        ]
        init_router_rule_data(self.rule_data_lt)
        update_grouter_channel_route_config()
        update_grouter_channel_change_config()

    @pytest.fixture()
    def rule_2(self):
        super(TestRoute, self).init()
        self.four_element = get_four_element()
        self.route_key = get_guid()
        self.rule_data_lt = [
            {
                "channel": "tongrongqianjingjing",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [500],
                        "routed_amount": 9500000,
                        "plan_amount": 10000000
                    }
                ]
            },
            {
                "channel": "haohanqianjingjing",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400],
                        "routed_amount": 9500000,
                        "plan_amount": 10000000
                    }
                ]
            },
            {
                "channel": "zhongke_lanzhou",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [300],
                        "routed_amount": 9500000,
                        "plan_amount": 10000000
                    }
                ]
            }
        ]
        init_router_rule_data(self.rule_data_lt)
        update_grouter_channel_route_config()
        update_grouter_channel_change_config()

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_route
    # @pytest.mark.parametrize("count, customer_type, rule_code",
    #                          [(6, "new", "tongrongqianjingjing_6m_newUser"),
    #                           (6, "old", "tongrongqianjingjing_6m_oldUser"),
    #                           (12, "new", "tongrongqianjingjing_12m_newUser"),
    #                           (12, "old", "tongrongqianjingjing_12m_oldUser"),
    #                           ])
    # def test_route_rule_01_customer_type(self, first_route_case, count, customer_type, rule_code):
    #     expect_channel = "tongrongqianjingjing"
    #     init_capital_plan(expect_channel)
    #
    #     four_element = get_four_element()
    #     if customer_type == "old":
    #         fake_asset_data(expect_channel, status="repay", four_element=four_element)
    #     # 路由
    #     route_key = get_guid()
    #     channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type, key=route_key)
    #     Assert.assert_equal(expect_channel, channel, "路由结果异常")
    #     check_router_load_record_data(route_key, router_load_record_rule_code=rule_code,
    #                                   router_load_record_principal_amount=self.amount*100,
    #                                   router_load_record_status="routed",
    #                                   router_load_record_channel=expect_channel,
    #                                   router_load_record_period_count=count,
    #                                   router_load_record_route_day=get_date(fmt="%Y-%m-%d"),
    #                                   router_load_record_product_code=get_router_capital_rule(rule_code)[0]["router_capital_rule_product_code"])

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count, source_type, rule_code",
                             [
                              (12, "irr36", "yilian_dingfeng_12m"),
                              #(12, "apr36", "yilian_dingfeng_12m_df2"),
                              ])
    def test_route_rule_02_source_type(self, first_route_case, count, source_type, rule_code):
        expect_channel = "yilian_dingfeng"
        init_capital_plan(expect_channel)

        four_element = get_four_element(id_num_begin='1')
        # 路由
        route_key = get_guid()
        channel = asset_route(four_element, count, self.amount, self.from_system, source_type, key=route_key)
        Assert.assert_equal(expect_channel, channel, "路由结果异常")
        check_router_load_record_data(route_key, router_load_record_rule_code=rule_code,
                                      router_load_record_principal_amount=self.amount*100,
                                      router_load_record_status="routed",
                                      router_load_record_channel=expect_channel,
                                      router_load_record_period_count=count,
                                      router_load_record_route_day=get_date(fmt="%Y-%m-%d"),
                                      router_load_record_product_code=get_router_capital_rule(rule_code)[0]["router_capital_rule_product_code"])

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_route
    # @pytest.mark.parametrize("count, district, rule_code",
    #                          [(6, "甘肃省天水市", "lanzhou_haoyue_6m_gansu"),
    #                           (6, "上海市上海市", "lanzhou_haoyue_6m"),
    #                           (12, "甘肃省天水市", "lanzhou_haoyue_12m_gansu"),
    #                           (12, "上海市上海市", "lanzhou_haoyue_12m"),
    #                           ])
    # def test_route_rule_03_district(self, first_route_case, count, district, rule_code):
    #     expect_channel = "lanzhou_haoyue"
    #     init_capital_plan(expect_channel)
    #
    #     four_element = get_four_element(id_num_begin="50")
    #     # 路由
    #     route_key = get_guid()
    #     channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type, key=route_key, id_addr=district)
    #     Assert.assert_equal(expect_channel, channel, "路由结果异常")
    #     check_router_load_record_data(route_key, router_load_record_rule_code=rule_code,
    #                                   router_load_record_principal_amount=self.amount*100,
    #                                   router_load_record_status="routed",
    #                                   router_load_record_channel=expect_channel,
    #                                   router_load_record_period_count=count,
    #                                   router_load_record_route_day=get_date(fmt="%Y-%m-%d"),
    #                                   router_load_record_product_code=get_router_capital_rule(rule_code)[0]["router_capital_rule_product_code"]
    #                                   )

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count, rule_codes",
                             [
                                (6, ("yilian_dingfeng_6m",)),
                                (12, ("yilian_dingfeng_12m",)),
                              ])
    def test_route_rule_04_time_frame(self, first_route_case, count, rule_codes):
        expect_channel = "yilian_dingfeng"
        init_capital_plan(expect_channel)
        four_element = get_four_element()
        # 路由
        route_key = get_guid()
        channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type, key=route_key)
        Assert.assert_equal(expect_channel, channel, "路由结果异常")
        for rule_code in rule_codes:
            check_router_load_record_data(route_key, rule_code,
                                          router_load_record_principal_amount=self.amount*100,
                                          router_load_record_status="routed",
                                          router_load_record_channel=expect_channel,
                                          router_load_record_period_count=count,
                                          router_load_record_route_day=get_date(fmt="%Y-%m-%d"),
                                          router_load_record_product_code=get_router_capital_rule(rule_code)[0]["router_capital_rule_product_code"]
            )

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count", [6])
    def test_first_route_fail_weight_01(self, first_route_case, count):
        """
        因为权重总开关未启用，路由失败
        """
        capital_channel = self.expect_channel
        init_capital_plan(capital_channel)
        # 关闭总权重开关
        update_router_weight_inactive(capital_channel)

        four_element = get_four_element()
        channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type)
        Assert.assert_equal(None, channel, "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count", [6])
    def test_first_route_fail_weight_02(self, first_route_case, count):
        """
        因为一次路由权重未启用，路由失败
        """
        capital_channel = self.expect_channel
        init_capital_plan(capital_channel)
        # 关闭一次路由权重
        update_router_weight_first_route_status_inactive(capital_channel)

        four_element = get_four_element()
        channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type)
        Assert.assert_equal(None, channel, "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count", [12])
    def test_first_route_fail_rule_code_01(self, first_route_case, count):
        """
        因为没有配置资金规则，路由失败
        """
        capital_channel = self.expect_channel
        init_capital_plan(capital_channel)
        # 删除资金规则
        delete_capital_rule_code(capital_channel)

        four_element = get_four_element()
        channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type)
        Assert.assert_equal(None, channel, "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count", [12])
    def test_first_route_fail_rule_code_02(self, first_route_case, count):
        """
        因为资金规则未启用，路由失败
        """
        capital_channel = self.expect_channel
        init_capital_plan(capital_channel)
        # 修改资金规则状态为：未启用
        router_capital_rule_notrelease(capital_channel)

        four_element = get_four_element()
        channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type)
        Assert.assert_equal(None, channel, "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count", [6])
    def test_first_route_fail_no_channel(self, first_route_case, count):
        """
        因为当日没有资金量，路由失败
        """
        capital_channel = self.expect_channel
        init_capital_plan(capital_channel)
        # 资金量置0
        update_router_cp_amount_all_to_zero()

        four_element = get_four_element()
        channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type)
        Assert.assert_equal(None, channel, "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_firstroute
    @pytest.mark.parametrize("count", [12])
    def test_first_route_fail_capital_debt(self, first_route_case, count):
        """
        超过资金方共债笔数路由失败
        :param case:
        :param count:
        :return:
        """
        channels = ['yumin_zhongbao']
        for capital_channel in channels:
            # 将所有其他资金方的金额设置为0，使其可以命中指定资金方
            capital_channel = self.expect_channel
            init_capital_plan(capital_channel)
            update_router_capital_plan_amount_all_to_zero(capital_channel)
            four_element = get_four_element()
            # 期望因为资金方共债，不能命中，以下为进件资产落地操作
            item_no, asset_info = asset_import(capital_channel, four_element, count, 8000, "草莓", "")
            self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
            channel = asset_route(four_element, count, 8000, "香蕉", self.source_type, '', '110000')
            # 此时应该没有资金方可以命中了，路由应该返回的是""
            if not channel:
                pass
            else:
                raise ValueError("失败")
            # 将所有资金方金额恢复
            update_all_channel_amount()
            idnum_encrypt = four_element['data']['id_number_encrypt']
            check_route_log(idnum_encrypt, capital_channel, "资方校验失败: 校验资产共债")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count", [12])
    def test_first_route_fail_time(self, first_route_case, count):
        """
        超过进件时间，路由失败
        """
        capital_channel = "zhongyuan_zunhao"
        init_capital_plan(capital_channel)
        # 修改路由时间段
        update_grouter_capital_rule_zhongyuan_zunhao('00:01')

        four_element = get_four_element()
        idnum_encrypt = four_element['data']['id_number_encrypt']
        channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type)
        Assert.assert_equal(None, channel, "路由结果异常")
        check_route_log(idnum_encrypt, capital_channel, "校验资方允许路由时间失败")
        # 恢复路由时间段
        update_grouter_capital_rule_zhongyuan_zunhao()

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count", [6])
    def test_first_route_fail_error_source_type(self, first_route_case, count):
        """
        因为source_type不支持路由失败
        """
        capital_channel = self.expect_channel
        init_capital_plan(capital_channel)

        four_element = get_four_element()
        channel = asset_route(four_element, count, self.amount, self.from_system, source_type="test001")
        Assert.assert_equal(None, channel, "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count", [6])
    def test_first_route_fail_more_than_money(self, first_route_case, count):
        """
        因为路由的金额超过所有资金方支持的最大金额，路由失败
        """
        capital_channel = self.expect_channel
        init_capital_plan(capital_channel)

        four_element = get_four_element()
        channel = asset_route(four_element, count, 99999, self.from_system, self.source_type)
        Assert.assert_equal(None, channel, "路由结果异常")

    # @pytest.mark.gbiz_auto_test
    # @pytest.mark.gbiz_route
    # @pytest.mark.parametrize("count", [12])
    # def test_first_route_fail_address(self, first_route_case, count):
    #     """
    #     因为路由用户的归属地址不在资金方支持范围内，路由失败
    #     """
    #     capital_channel = "weishenma_daxinganling"
    #     init_capital_plan(capital_channel)
    #
    #     four_element = get_four_element()
    #     idnum_encrypt = four_element['data']['id_number_encrypt']
    #     channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type)
    #     Assert.assert_equal(None, channel, "路由结果异常")
    #     check_route_log(idnum_encrypt, capital_channel, "资方校验失败: 校验身份证地址不允许:西藏,新疆,内蒙古,青海,宁夏,甘肃")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    @pytest.mark.parametrize("count", [12])
    def test_first_route_fail_access(self, first_route_case, count):
        """
        调资方准入接口失败
        """
        capital_channel = "jinmeixin_hanchen"
        init_capital_plan(capital_channel)
        capital_mock = JinmeixinHanchenMock(gbiz_mock)
        capital_mock.update_user_check('N')

        four_element = get_four_element()
        idnum_encrypt = four_element['data']['id_number_encrypt']
        channel = asset_route(four_element, count, self.amount, self.from_system, self.source_type)
        Assert.assert_equal(None, channel, "路由结果异常")
        check_route_log(idnum_encrypt, capital_channel, "资金路由系统校验失败: 校验用户是否可准入")
        capital_mock.update_user_check()

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_amount_check_01(self):
        """
        全部为严格控量: 所有规则资金量充足，路由命中，2条路由记录
        """
        rule_data_lt = [
            {
                "channel": "zhongyuan_zunhao",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400, 500],
                        "routed_amount": 1000000,
                        "plan_amount": 10000000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "strict",
                        "weight": [600],
                        "routed_amount": 1000000,
                        "plan_amount": 10000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element()
        period = 12
        amount = 6000
        route_key = get_guid()
        channel = asset_route(four_element, period, amount, key=route_key)
        Assert.assert_equal("zhongyuan_zunhao", channel, "路由结果异常")
        check_router_load_record(rule_data_lt, route_key, four_element, amount, "routed", hit_channel_idx=0,
                                 hit_rule_idx_lt=[0, 1])

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_amount_check_02(self):
        """
        全部为严格控量: 部分规则资金量充足、部分不足，路由为空 - 仅DB计量
        """
        rule_data_lt = [
            {
                "channel": "zhongyuan_zhongbao",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400, 500],
                        "routed_amount": 1000000,
                        "plan_amount": 10000000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "strict",
                        "weight": [600],
                        "routed_amount": 800000,
                        "plan_amount": 1000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element()
        period = 12
        amount = 6000
        route_key = get_guid()
        channel = asset_route(four_element, period, amount, key=route_key)
        Assert.assert_equal(None, channel, "路由结果异常")
        router_record = get_router_load_record_by_key(route_key)
        Assert.assert_equal(0, len(router_record), "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_amount_check_03(self):
        """
        全部为非严格控量: 部分规则资金量充足、部分不足，路由命中，1条路由记录
        """
        rule_data_lt = [
            {
                "channel": "jinmeixin_hanchen",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "nonstrict",
                        "weight": [400, 500],
                        "routed_amount": 1000000,
                        "plan_amount": 10000000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "nonstrict",
                        "weight": [600],
                        "routed_amount": 800000,
                        "plan_amount": 1000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element()
        period = 12
        amount = 6000
        route_key = get_guid()
        channel = asset_route(four_element, period, amount, key=route_key)
        Assert.assert_equal("jinmeixin_hanchen", channel, "路由结果异常")
        check_router_load_record(rule_data_lt, route_key, four_element, amount, "routed", hit_channel_idx=0,
                                 hit_rule_idx_lt=[0])

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_amount_check_04(self):
        """
        全部为非严格控量: 所有规则资金量都不足，路由为空
        """
        rule_data_lt = [
            {
                "channel": "jinmeixin_hanchen_jf",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "nonstrict",
                        "weight": [400, 500],
                        "routed_amount": 800000,
                        "plan_amount": 1000000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "nonstrict",
                        "weight": [600],
                        "routed_amount": 800000,
                        "plan_amount": 1000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        channel = asset_route(get_four_element(), 12, 6000, "香蕉")
        Assert.assert_equal(None, channel, "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_amount_check_05(self):
        """
        严格控量+非严格控量混合: 所有严格控量规则资金量都满足（非严格资金量已不足），路由命中
        """
        rule_data_lt = [
            {
                "channel": "yumin_zhongbao",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400, 500],
                        "routed_amount": 1000000,
                        "plan_amount": 10000000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "nonstrict",
                        "weight": [600],
                        "routed_amount": 800000,
                        "plan_amount": 1000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element()
        period = 12
        amount = 6000
        route_key = get_guid()
        channel = asset_route(four_element, period, amount, key=route_key, id_addr="江西省省天水市秦州区岷玉路罗玉小区市31幢3单元501室")
        Assert.assert_equal("yumin_zhongbao", channel, "路由结果异常")
        check_router_load_record(rule_data_lt, route_key, four_element, amount, "routed", hit_channel_idx=0,
                                 hit_rule_idx_lt=[0])

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_amount_check_06(self):
        """
        严格控量+非严格控量混合: 有一个严格控量规则资金量不足（非严格资金量充足），路由为空
        """
        rule_data_lt = [
            {
                "channel": "zhongyuan_zhongbao",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400, 500],
                        "routed_amount": 800000,
                        "plan_amount": 1000000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "nonstrict",
                        "weight": [600],
                        "routed_amount": 400000,
                        "plan_amount": 1000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        channel = asset_route(get_four_element(), 12, 6000, "香蕉")
        Assert.assert_equal(None, channel, "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_amount_check_07_overflow_rate(self):
        """
        溢出率
        """
        rule_data_lt = [
            {
                "channel": "zhongyuan_zunhao",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "overflow_rate": 0.4,
                        "weight": [400, 500],
                        "routed_amount": 800000,
                        "plan_amount": 1000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element()
        period = 12
        amount = 6000
        route_key = get_guid()
        channel = asset_route(four_element, period, amount, key=route_key)
        Assert.assert_equal("zhongyuan_zunhao", channel, "路由结果异常")
        check_router_load_record(rule_data_lt, route_key, four_element, amount, "routed", hit_channel_idx=0,
                                 hit_rule_idx_lt=[0])

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_amount_check_08_cache_amount(self):
        """
        全部为严格控量: 部分规则资金量充足、部分不足，路由为空 - DB+cache计量
        """
        rule_data_lt = [
            {
                "channel": "zhongyuan_zhongbao",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400, 500],
                        "routed_amount": 1000000,
                        "plan_amount": 10000000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "strict",
                        "weight": [600],
                        "routed_amount": 300000,
                        "cache_routed_amount": 300000,
                        "plan_amount": 1000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element()
        period = 12
        amount = 6000
        route_key = get_guid()
        channel = asset_route(four_element, period, amount, key=route_key)
        Assert.assert_equal(None, channel, "路由结果异常")

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_amount_check_09_past_cache_amount(self):
        """
        昨日的缓存量，不影响今日路由
        """
        rule_data_lt = [
            {
                "channel": "jinmeixin_hanchen",
                "period": 12,
                "period_type": "month",
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [600],
                        "routed_amount": 0,
                        "plan_amount": 1000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        capital_mock = JinmeixinHanchenMock(gbiz_mock)
        capital_mock.update_user_check()
        past_timestamp = date_to_timestamp(get_date(day=-1, fmt="%Y-%m-%d"), fmt="%Y-%m-%d")
        gc.GRANT_REDIS.setex("{}-routed-{}".format("jinmeixin_hanchen_12month_0", past_timestamp), value=1000000,
                             time=1800)
        four_element = get_four_element()
        period = 12
        amount = 6000
        route_key = get_guid()
        channel = asset_route(four_element, period, amount, key=route_key)
        Assert.assert_equal("jinmeixin_hanchen", channel, "路由结果异常")
        check_router_load_record(rule_data_lt, route_key, four_element, amount, "routed", hit_channel_idx=0,
                                 hit_rule_idx_lt=[0])

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_white_list_01_route_success(self, rule_1):
        """
        一次路由配置了白名单，普通用户路由不中，白名单用户路由命中
        """
        update_grouter_channel_route_config(tongrongqianjingjing=self.four_element["data"]["phone_number_encrypt"])
        # 普通用户路由不中
        four_element = get_four_element()
        channel = asset_route(four_element, self.period, self.amount, key=self.route_key)
        Assert.assert_equal(None, channel, "路由结果异常")
        # 白名单用户路由命中
        channel = asset_route(self.four_element, self.period, self.amount, key=self.route_key)
        Assert.assert_equal(self.expect_channel, channel, "路由结果异常")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "routed", hit_channel_idx=0)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_first_route_white_list_02_route_fail(self, rule_1):
        """
        一次路由配置了白名单，权重未开启，白名单用户路由不中
        """
        update_grouter_channel_route_config(tongrongqianjingjing=self.four_element["data"]["phone_number_encrypt"])
        update_router_weight_by_channel(self.rule_data_lt[0]["channel"], router_weight_status="inactive")
        channel = asset_route(self.four_element, self.period, self.amount, key=self.route_key)
        Assert.assert_equal(None, channel, "路由结果异常")

    def prepare_route_data(self, route_type):
        """
        准备进件路由和二次路由的数据。
        rule_data_lt结构不要变动。
        :param route_type:
        :return:
        """
        # 一次路由：routed
        routed_channel = asset_route(self.four_element, self.period, self.amount, key=self.route_key)
        Assert.assert_equal(self.rule_data_lt[0]["channel"], routed_channel, "路由结果异常")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "routed", hit_channel_idx=0)
        rule_code = get_rule_code(self.rule_data_lt, 0)
        today_timestamp = date_to_timestamp(get_date(fmt="%Y-%m-%d"), fmt="%Y-%m-%d")
        Assert.assert_equal(self.amount * 100,
                            int(gc.GRANT_REDIS.get("{}-routed-{}".format(rule_code, today_timestamp))))
        Assert.assert_equal(False, gc.GRANT_REDIS.exists("{}-imported-{}".format(rule_code, today_timestamp)))
        # 进件：imported
        item_no, asset_info = asset_import(routed_channel, self.four_element, self.period, self.amount,
                                           self.from_system,
                                           insert_router_record=False)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)
        Assert.assert_equal(self.amount * 100,
                            int(gc.GRANT_REDIS.get("{}-routed-{}".format(rule_code, today_timestamp))))
        Assert.assert_equal(self.amount * 100, int(gc.GRANT_REDIS.get("{}-imported-0".format(rule_code))))
        # 走到canloan失败
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        if route_type == 2:
            update_router_capital_plan_by_rule_code(rule_code, 0)
            self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        return item_no

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_second_route_01_normal(self, rule_2):
        """
        正常二次路由场景：切到权重最高的第一家资方
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"],
                                                        self.rule_data_lt[2]["channel"]],
                                  against_channel_map={})
        route_key_2 = item_no
        # 二次路由：changed+routed
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount, "changed", item_no,
                                 hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount, "routed",
                                 hit_channel_idx=1)
        rule_code_2 = get_rule_code(self.rule_data_lt, 1)
        today_timestamp = date_to_timestamp(get_date(fmt="%Y-%m-%d"), fmt="%Y-%m-%d")
        Assert.assert_equal(self.amount * 100,
                            int(gc.GRANT_REDIS.get("{}-routed-{}".format(rule_code_2, today_timestamp))))

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_second_route_02_against_map(self, rule_2):
        """
        第一家资方与当前资方互斥，切到第二家资方
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"],
                                                        self.rule_data_lt[2]["channel"]],
                                  against_channel_map={
                                      self.rule_data_lt[0]["channel"]: [self.rule_data_lt[1]["channel"]]})
        route_key_2 = item_no
        # 二次路由：changed+routed
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount, "changed", item_no,
                                 hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount, "routed",
                                 hit_channel_idx=2)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_second_route_03_channel_not_allowed(self, rule_2):
        """
        第一家资方不允许二次路由，切到第二家资方
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[2]["channel"]],
                                  against_channel_map={})
        route_key_2 = item_no
        # 二次路由：changed+routed
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount, "changed", item_no,
                                 hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount, "routed",
                                 hit_channel_idx=2)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_second_route_04_max_elapsed_time(self, rule_2):
        """
        超过第一家资方允许最大时间，切到第二家资方
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"],
                                                        self.rule_data_lt[2]["channel"]],
                                  against_channel_map={},
                                  forbid_channel_config={"max_elapsed_hours": "12",
                                                         "channels": [self.rule_data_lt[1]["channel"]]})
        update_asset_loan_record_by_item_no(item_no, asset_loan_record_create_at=get_calc_date_base_today(day=-1))
        route_key_2 = item_no
        # 二次路由：changed+routed
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount, "changed", item_no,
                                 hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount, "routed",
                                 hit_channel_idx=2)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_second_route_05_weight_status_off(self, rule_2):
        """
        第一家资方权重总开关未开，切到第二家资方
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"],
                                                        self.rule_data_lt[2]["channel"]],
                                  against_channel_map={})
        update_router_weight_by_channel(self.rule_data_lt[1]["channel"], router_weight_status="inactive")
        route_key_2 = item_no
        # 二次路由：changed+routed
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount, "changed", item_no,
                                 hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount, "routed",
                                 hit_channel_idx=2)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_second_route_06_second_weight_status_off(self, rule_2):
        """
        第一家资方二次权重未开，切到第二家资方
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"],
                                                        self.rule_data_lt[2]["channel"]],
                                  against_channel_map={})
        update_router_weight_by_channel(self.rule_data_lt[1]["channel"], router_weight_second_route_status="inactive")
        route_key_2 = item_no
        # 二次路由：changed+routed
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount, "changed", item_no,
                                 hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount, "routed",
                                 hit_channel_idx=2)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_second_route_07_amount_check_fail(self, rule_2):
        """
        第一家资方资金量不足，切到第二家资方
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"],
                                                        self.rule_data_lt[2]["channel"]],
                                  against_channel_map={})
        update_router_load_total(get_rule_code(self.rule_data_lt, 1),
                                 router_load_total_routed_amount=self.rule_data_lt[1]["rule_lt"][0][
                                                                     "plan_amount"] - self.amount * 100 + 100)
        route_key_2 = item_no
        # 二次路由：changed+routed
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount, "changed", item_no,
                                 hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount, "routed",
                                 hit_channel_idx=2)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_route_01_normal(self, rule_1):
        """
        进件路由：正常进件路由成功
        """
        item_no = self.prepare_route_data(route_type=3)
        # 进件路由
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        alr_record = get_asset_loan_record_by_item_no(item_no)
        check_data(alr_record[0], asset_loan_record_status=1)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_route_02_weight_off_does_not_matter(self, rule_1):
        """
        进件路由：权重未开启->不影响，依然进件路由成功
        """
        item_no = self.prepare_route_data(route_type=3)
        update_router_weight_by_channel(self.rule_data_lt[0]["channel"], router_weight_status="inactive",
                                        router_weight_second_route_status="inactive")
        # 进件路由
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        alr_record = get_asset_loan_record_by_item_no(item_no)
        check_data(alr_record[0], asset_loan_record_status=1)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_route_03_amount_check_fail_imported_amount_limit(self, rule_1):
        """
        进件路由：当日进件量已超过计划量->资金量校验失败
        """
        item_no = self.prepare_route_data(route_type=3)
        update_router_load_total(get_rule_code(self.rule_data_lt, 0),
                                 router_load_total_imported_amount=self.rule_data_lt[0]["rule_lt"][0][
                                                                       "plan_amount"] + 100)
        # 进件路由
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        alr_record = get_asset_loan_record_by_item_no(item_no)
        check_data(alr_record[0], asset_loan_record_status=5,
                   asset_loan_record_memo="{}->校验资金量失败;".format(self.rule_data_lt[0]["channel"]))

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_route_04_amount_check_fail_no_plan(self, rule_1):
        """
        进件路由：当日资金计划没配置->资金量校验失败
        """
        item_no = self.prepare_route_data(route_type=3)
        delete_router_capital_plan()
        # 进件路由
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        alr_record = get_asset_loan_record_by_item_no(item_no)
        check_data(alr_record[0], asset_loan_record_status=5,
                   asset_loan_record_memo="{}->校验资金量失败;".format(self.rule_data_lt[0]["channel"]))

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_route_05_white_list_fail(self, rule_1):
        """
        进件路由：当日资金计划没配置->一次路由白名单也需要过规则->资金量校验失败
        """
        item_no = self.prepare_route_data(route_type=3)
        delete_router_capital_plan()
        update_grouter_channel_route_config(tongrongqianjingjing=self.four_element["data"]["phone_number_encrypt"])
        # 进件路由
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        alr_record = get_asset_loan_record_by_item_no(item_no)
        check_data(alr_record[0], asset_loan_record_status=5,
                   asset_loan_record_memo="{}->校验资金量失败;".format(self.rule_data_lt[0]["channel"]))

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_with_route_key_00_normal(self, rule_1):
        """
        进件不传route_uuid，成功匹配到路由记录
        """
        routed_channel = asset_route(self.four_element, self.period, self.amount, self.from_system, key=self.route_key)
        Assert.assert_equal(self.rule_data_lt[0]["channel"], routed_channel, "路由结果异常")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "routed", hit_channel_idx=0)
        # 进件：imported
        item_no, asset_info = asset_import(routed_channel, self.four_element, self.period, self.amount,
                                           self.from_system,
                                           insert_router_record=False)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_with_route_key_01_normal(self, rule_1):
        """
        正确的route_uuid进件，成功匹配到路由记录
        """
        routed_channel = asset_route(self.four_element, self.period, self.amount, self.from_system, key=self.route_key)
        Assert.assert_equal(self.rule_data_lt[0]["channel"], routed_channel, "路由结果异常")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "routed", hit_channel_idx=0)
        # 进件：imported
        item_no, asset_info = asset_import(routed_channel, self.four_element, self.period, self.amount,
                                           self.from_system,
                                           route_uuid=self.route_key, insert_router_record=False)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_with_route_key_02_no_route_error(self, rule_1):
        """
        进件route_uuid没有路由记录，AssetImport报错
        """
        item_no, asset_info = asset_import(self.expect_channel, self.four_element, self.period, self.amount,
                                           self.from_system,
                                           route_uuid=get_guid(), insert_router_record=False)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 2})

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_with_route_key_03_status_error(self, rule_1):
        """
        进件route_uuid路由状态不是routed，AssetImport报错
        """
        routed_channel = asset_route(self.four_element, self.period, self.amount, self.from_system, key=self.route_key)
        update_router_load_record_by_key(self.route_key, router_load_record_status="imported")
        item_no, asset_info = asset_import(routed_channel, self.four_element, self.period, self.amount,
                                           self.from_system,
                                           route_uuid=self.route_key, insert_router_record=False)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 2})

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_with_route_key_04_change_capital_auto_import(self, rule_2):
        """
        切资方+自动进件，route_key=item_no
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"]],
                                  against_channel_map={})
        route_key_2 = item_no
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "changed", item_no, hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount,
                                 "routed", hit_channel_idx=1)
        self.task.run_task(item_no, "AssetAutoImport", excepts={"code": 0})
        self.msg.run_msg(item_no, "AssetAutoImport", excepts={"code": 0})
        wait_task_appear(item_no, "AssetImport")
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=1)

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_route
    def test_import_with_route_key_05_change_capital_bc_import(self, rule_2):
        """
        切资方+bc进件，前端传入一次路由route_uuid，找到正确路由记录
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"]],
                                  against_channel_map={})
        route_key_2 = item_no
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "changed", item_no, hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount,
                                 "routed", hit_channel_idx=1)
        item_no, asset_info = asset_import(self.rule_data_lt[1]["channel"], self.four_element, self.period,
                                           self.amount, self.from_system, item_no=item_no, route_uuid=self.route_key,
                                           insert_router_record=False)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=1)
