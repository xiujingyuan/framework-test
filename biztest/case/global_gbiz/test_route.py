#!/usr/bin/python
# -*- coding: UTF-8 -*-

from biztest.interface.gbiz_global.gbiz_global_interface import asset_route, asset_import
from biztest.config.global_gbiz.global_gbiz_kv_config import update_grouter_channel_route_config, \
    incremental_update_config
from biztest.function.global_gbiz.gbiz_global_common_function import init_router_rule_data, init_capital_plan, \
    get_rule_code, run_terminated_task
from biztest.function.global_gbiz.gbiz_global_check_function import check_router_load_record, check_data
from biztest.function.global_gbiz.gbiz_global_db_function import get_asset_loan_record_by_item_no, \
    delete_router_capital_plan, update_router_load_total, update_router_capital_plan_by_rule_code, \
    update_router_weight_by_channel, update_asset_loan_record_by_item_no, update_router_load_record_by_key
from biztest.util.db.db_util import DataBase
from biztest.util.tools.tools import get_four_element_global, get_guid, get_calc_date_base_today
from biztest.util.asserts.assert_util import Assert
from biztest.case.global_gbiz.global_base_test_capital import BaseTestCapital
import pytest
import common.global_const as gc


@pytest.mark.global_gbiz_thailand
@pytest.mark.global_gbiz_route
class TestRoute(BaseTestCapital):
    period = 1
    period_day = 7
    period_type = "day"
    amount = 500000
    from_system = "tha"
    from_app = "mango"
    source_type = "mileVIPstore_bill"
    expect_channel = "picocp_ams1"
    fees = {"interest": 35.77}
    late_num = "late0.098%"

    @classmethod
    def setup_class(cls):
        init_capital_plan(gc.COUNTRY)
        update_grouter_channel_route_config()

    @classmethod
    def teardown_class(cls):
        init_capital_plan(gc.COUNTRY)
        update_grouter_channel_route_config()
        DataBase.close_connects()

    @pytest.fixture()
    def rule_1(self):
        super(TestRoute, self).init()
        self.four_element = get_four_element_global()
        self.route_key = get_guid()
        self.rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400],
                        "routed_amount": 0,
                        "plan_amount": 1000000000000000
                    }
                ]
            }
        ]
        init_router_rule_data(self.rule_data_lt)
        update_grouter_channel_route_config()

    @pytest.fixture()
    def rule_2(self):
        super(TestRoute, self).init()
        self.four_element = get_four_element_global()
        self.route_key = get_guid()
        self.rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [600],
                        "routed_amount": 0,
                        "plan_amount": 10000000000000
                    }
                ]
            },
            {
                "channel": "picoqr_ams1",
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [500],
                        "routed_amount": 0,
                        "plan_amount": 10000000000000
                    }
                ]
            }
        ]
        init_router_rule_data(self.rule_data_lt)
        update_grouter_channel_route_config()

    def test_first_route_01_normal(self, rule_1):
        """
        正常一次路由
        """
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, self.four_element, key=self.route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(self.expect_channel, channel, "路由结果异常")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "routed", hit_rule_idx_lt=[0])

    def test_first_route_02_weight_status_off(self, rule_1):
        """
        权重总开关未开，路由为空
        """
        update_router_weight_by_channel(self.rule_data_lt[0]["channel"], router_weight_status="inactive")
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, self.four_element, key=self.route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(None, channel, "路由结果异常")

    def test_first_route_03_first_weight_status_off(self, rule_1):
        """
        一次权重未开，路由为空
        """
        update_router_weight_by_channel(self.rule_data_lt[0]["channel"], router_weight_first_route_status="inactive")
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, self.four_element, key=self.route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(None, channel, "路由结果异常")

    def test_first_route_04_amount_check_01(self):
        """
        全部为严格控量: 所有规则资金量充足，路由命中，2条路由记录
        """
        rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400, 500],
                        "routed_amount": 0,
                        "plan_amount": 10000000000000000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "strict",
                        "weight": [600],
                        "routed_amount": 5000,
                        "plan_amount": 10000000000000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element_global()
        route_key = get_guid()
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, four_element, key=route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(self.expect_channel, channel, "路由结果异常")
        check_router_load_record(rule_data_lt, route_key, four_element, self.amount, "routed", hit_rule_idx_lt=[0, 1])

    def test_first_route_04_amount_check_02(self):
        """
        全部为严格控量: 部分规则资金量充足、部分不足，路由为空
        """
        rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400, 500],
                        "routed_amount": 0,
                        "plan_amount": 10000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "strict",
                        "weight": [600],
                        "routed_amount": 6000,
                        "plan_amount": 10000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element_global()
        route_key = get_guid()
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, four_element, key=route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(None, channel, "路由结果异常")

    def test_first_route_04_amount_check_03(self):
        """
        全部为非严格控量: 部分规则资金量充足、部分不足，路由命中，1条路由记录
        """
        rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "nonstrict",
                        "weight": [400],
                        "routed_amount": 0,
                        "plan_amount": 10000000000000000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "nonstrict",
                        "weight": [600],
                        "routed_amount": 9000,
                        "plan_amount": 1000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element_global()
        route_key = get_guid()
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, four_element, key=route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(self.expect_channel, channel, "路由结果异常")
        check_router_load_record(rule_data_lt, route_key, four_element, self.amount, "routed", hit_rule_idx_lt=[0])

    def test_first_route_04_amount_check_04(self):
        """
        全部为非严格控量: 所有规则资金量都不足，路由为空
        """
        rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "nonstrict",
                        "weight": [400],
                        "routed_amount": 10000,
                        "plan_amount": 10000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "nonstrict",
                        "weight": [600],
                        "routed_amount": 9000,
                        "plan_amount": 10000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element_global()
        route_key = get_guid()
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, four_element, key=route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(None, channel, "路由结果异常")

    def test_first_route_04_amount_check_05(self):
        """
        严格控量+非严格控量混合: 所有严格控量规则资金量都满足（非严格资金量已不足），路由命中
        """
        rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "nonstrict",
                        "weight": [400],
                        "routed_amount": 6000,
                        "plan_amount": 1000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "strict",
                        "weight": [600],
                        "routed_amount": 5000,
                        "plan_amount": 10000000000000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element_global()
        route_key = get_guid()
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, four_element, key=route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(self.expect_channel, channel, "路由结果异常")
        check_router_load_record(rule_data_lt, route_key, four_element, self.amount, "routed", hit_rule_idx_lt=[1])

    def test_first_route_04_amount_check_06(self):
        """
        严格控量+非严格控量混合: 有一个严格控量规则资金量不足（非严格资金量充足），路由为空
        """
        rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [400],
                        "routed_amount": 6000,
                        "plan_amount": 10000
                    },
                    {
                        "rule_code": "1",
                        "rule_limit_type": "nonstrict",
                        "weight": [600],
                        "routed_amount": 5000,
                        "plan_amount": 10000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element_global()
        route_key = get_guid()
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, four_element, key=route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(None, channel, "路由结果异常")

    def test_first_route_04_amount_check_07_overflow_rate(self):
        """
        溢出率
        """
        rule_data_lt = [
            {
                "channel": self.expect_channel,
                "period": self.period,
                "period_day": self.period_day,
                "period_type": self.period_type,
                "rule_lt": [
                    {
                        "rule_code": "0",
                        "rule_limit_type": "strict",
                        "weight": [600],
                        "overflow_rate": 0.1,
                        "routed_amount": 6000,
                        "plan_amount": 10000000000000000
                    }
                ]
            }
        ]
        init_router_rule_data(rule_data_lt)
        four_element = get_four_element_global()
        route_key = get_guid()
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, four_element, key=route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(self.expect_channel, channel, "路由结果异常")
        check_router_load_record(rule_data_lt, route_key, four_element, self.amount, "routed", hit_rule_idx_lt=[0])

    def test_first_route_05_white_list_route_success(self, rule_1):
        """
        一次路由配置了白名单，普通用户路由不中，白名单用户路由命中
        """
        update_grouter_channel_route_config(picocp_ams1=self.four_element["data"]["mobile_encrypt"])
        # 普通用户路由不中
        four_element = get_four_element_global()
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, four_element, key=self.route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(None, channel, "路由结果异常")
        # 白名单用户路由命中
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, self.four_element, key=self.route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(self.expect_channel, channel, "路由结果异常")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "routed", hit_rule_idx_lt=[0])
        update_grouter_channel_route_config()

    def test_first_route_05_white_list_route_fail(self, rule_1):
        """
        一次路由配置了白名单，权重未开启，白名单用户路由不中
        """
        update_grouter_channel_route_config(picocp_ams1=self.four_element["data"]["mobile_encrypt"])
        update_router_weight_by_channel(self.rule_data_lt[0]["channel"], router_weight_status="inactive")
        channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                              self.from_app, self.source_type, self.four_element, key=self.route_key,
                              fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(None, channel, "路由结果异常")
        update_grouter_channel_route_config()

    def prepare_route_data(self, route_type):
        """
        准备进件路由和二次路由的数据。
        :param route_type:
        :return:
        """
        # 一次路由：routed
        routed_channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                                     self.from_app, self.source_type, self.four_element, key=self.route_key,
                                     late_num="late0.098%", fees={"interest": 35.77})
        Assert.assert_equal(self.rule_data_lt[0]["channel"], routed_channel, "路由结果异常")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "routed", hit_channel_idx=0)
        rule_code = get_rule_code(self.rule_data_lt, 0)
        # 进件：imported
        item_no, asset_info = asset_import(routed_channel, self.period, self.period_day, self.period_type, self.amount,
                                           self.from_system, self.from_app, self.source_type, self.four_element,
                                           route_uuid=self.route_key, insert_router_record=False,
                                           late_num="late0.098%", fees={"interest": 35.77})
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)
        # 走到canloan失败
        self.task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
        if route_type == 2:
            update_router_capital_plan_by_rule_code(rule_code, 0)
            self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        return item_no

    def test_import_route_01_normal(self, rule_2):
        """
        正常进件路由成功
        """
        item_no = self.prepare_route_data(route_type=3)
        # 进件路由
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        alr_record = get_asset_loan_record_by_item_no(item_no)
        check_data(alr_record[0], asset_loan_record_status=1)

    def test_import_route_02_weight_off_does_not_matter(self, rule_2):
        """
        进件路由：权重未开启->不影响，依然进件路由成功
        """
        item_no = self.prepare_route_data(route_type=3)
        update_router_weight_by_channel(self.rule_data_lt[0]["channel"], router_weight_status="inactive",
                                        router_weight_first_route_status="inactive",
                                        router_weight_second_route_status="inactive")
        # 进件路由
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        alr_record = get_asset_loan_record_by_item_no(item_no)
        check_data(alr_record[0], asset_loan_record_status=1)

    def test_import_route_03_amount_check_fail_imported_amount_limit(self, rule_2):
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

    def test_import_route_04_amount_check_fail_no_plan(self, rule_2):
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

    def test_import_route_05_white_list_fail(self, rule_2):
        """
        进件路由：当日资金计划没配置->一次路由白名单也需要过规则->资金量校验失败
        """
        item_no = self.prepare_route_data(route_type=3)
        delete_router_capital_plan()
        update_grouter_channel_route_config(picocp_ams1=self.four_element["data"]["mobile_encrypt"])
        # 进件路由
        self.task.run_task(item_no, "ApplyCanLoan", excepts={"code": 0})
        alr_record = get_asset_loan_record_by_item_no(item_no)
        check_data(alr_record[0], asset_loan_record_status=5,
                   asset_loan_record_memo="{}->校验资金量失败;".format(self.rule_data_lt[0]["channel"]))

    def test_second_route_01_normal(self, rule_2):
        """
        正常二次路由场景：切资方成功  //海外资方不能互切，先不管
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"]],
                                  against_channel_map={})
        route_key_2 = item_no
        # 二次路由：changed+routed
        run_terminated_task(item_no, "ChangeCapital")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "changed", item_no, hit_channel_idx=0)
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount,
                                 "routed", hit_channel_idx=1)

    def test_second_route_02_against_map(self, rule_2):
        """
        资方与当前资方互斥，二次路由为空
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"]],
                                  against_channel_map={
                                      self.rule_data_lt[0]["channel"]: [self.rule_data_lt[1]["channel"]]})
        # 二次路由：切资方失败
        run_terminated_task(item_no, "ChangeCapital", expect_code=1)
        run_terminated_task(item_no, "AssetVoid", expect_code=0)
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    def test_second_route_03_channel_not_allowed(self, rule_2):
        """
        资方不允许二次路由，二次路由为空
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[],
                                  against_channel_map={})
        # 二次路由：切资方失败
        run_terminated_task(item_no, "ChangeCapital", expect_code=1)
        run_terminated_task(item_no, "AssetVoid", expect_code=0)
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    def test_second_route_04_max_elapsed_time(self, rule_2):
        """
        超过资方允许最大时间，二次路由为空
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"], ],
                                  against_channel_map={},
                                  forbid_channel_config={"max_elapsed_hours": "12",
                                                         "channels": [self.rule_data_lt[1]["channel"]]})
        update_asset_loan_record_by_item_no(item_no, asset_loan_record_create_at=get_calc_date_base_today(day=-1))
        # 二次路由：切资方失败
        run_terminated_task(item_no, "ChangeCapital", expect_code=1)
        run_terminated_task(item_no, "AssetVoid", expect_code=0)
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    def test_second_route_05_weight_status_off(self, rule_2):
        """
        资方权重总开关未开，二次路由为空
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"], ],
                                  against_channel_map={})
        update_router_weight_by_channel(self.rule_data_lt[1]["channel"], router_weight_status="inactive")
        # 二次路由：切资方失败
        run_terminated_task(item_no, "ChangeCapital", expect_code=1)
        run_terminated_task(item_no, "AssetVoid", expect_code=0)
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    def test_second_route_06_second_weight_status_off(self, rule_2):
        """
        资方二次权重未开，二次路由为空
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"], ],
                                  against_channel_map={})
        update_router_weight_by_channel(self.rule_data_lt[1]["channel"], router_weight_second_route_status="inactive")
        # 二次路由：切资方失败
        run_terminated_task(item_no, "ChangeCapital", expect_code=1)
        run_terminated_task(item_no, "AssetVoid", expect_code=0)
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    def test_second_route_07_amount_check_fail(self, rule_2):
        """
        资方资金量不足，二次路由为空
        """
        item_no = self.prepare_route_data(route_type=2)
        incremental_update_config("grouter", "grouter_channel_change_config",
                                  allowed_channel_list=[self.rule_data_lt[1]["channel"], ],
                                  against_channel_map={})
        update_router_load_total(get_rule_code(self.rule_data_lt, 1),
                                 router_load_total_routed_amount=self.rule_data_lt[1]["rule_lt"][0][
                                                                     "plan_amount"] - self.amount + 1)
        # 二次路由：切资方失败
        run_terminated_task(item_no, "ChangeCapital", expect_code=1)
        run_terminated_task(item_no, "AssetVoid", expect_code=0)
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    def test_import_with_route_key_00_normal(self, rule_1):
        """
        进件不传route_uuid，成功匹配到路由记录
        """
        routed_channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                                     self.from_app, self.source_type, self.four_element, key=self.route_key,
                                     fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(self.rule_data_lt[0]["channel"], routed_channel, "路由结果异常")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "routed", hit_channel_idx=0)
        # 进件：imported
        item_no, asset_info = asset_import(routed_channel, self.period, self.period_day, self.period_type, self.amount,
                                           self.from_system, self.from_app, self.source_type, self.four_element,
                                           insert_router_record=False, fees=self.fees, late_num=self.late_num)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    def test_import_with_route_key_01_normal(self, rule_1):
        """
        正确的route_uuid进件，成功匹配到路由记录
        """
        routed_channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                                     self.from_app, self.source_type, self.four_element, key=self.route_key,
                                     fees=self.fees, late_num=self.late_num)
        Assert.assert_equal(self.rule_data_lt[0]["channel"], routed_channel, "路由结果异常")
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "routed", hit_channel_idx=0)
        # 进件：imported
        item_no, asset_info = asset_import(routed_channel, self.period, self.period_day, self.period_type, self.amount,
                                           self.from_system, self.from_app, self.source_type, self.four_element,
                                           route_uuid=self.route_key, insert_router_record=False,
                                           fees=self.fees, late_num=self.late_num)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, self.route_key, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=0)

    def test_import_with_route_key_02_no_route_error(self, rule_1):
        """
        进件route_uuid没有路由记录，AssetImport报错
        """
        item_no, asset_info = asset_import(self.expect_channel, self.period, self.period_day, self.period_type,
                                           self.amount,
                                           self.from_system, self.from_app, self.source_type, self.four_element,
                                           route_uuid=get_guid(), insert_router_record=False,
                                           fees=self.fees, late_num=self.late_num)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 2})

    def test_import_with_route_key_03_status_error(self, rule_1):
        """
        进件route_uuid路由状态不是routed，AssetImport报错
        """
        routed_channel = asset_route(self.period, self.period_day, self.period_type, self.amount, self.from_system,
                                     self.from_app, self.source_type, self.four_element, key=self.route_key,
                                     fees=self.fees, late_num=self.late_num)
        update_router_load_record_by_key(self.route_key, router_load_record_status="imported")
        item_no, asset_info = asset_import(routed_channel, self.period, self.period_day, self.period_type, self.amount,
                                           self.from_system, self.from_app, self.source_type, self.four_element,
                                           route_uuid=self.route_key, insert_router_record=False,
                                           fees=self.fees, late_num=self.late_num)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 2})

    def test_import_with_route_key_04_change_capital_auto_import(self, rule_2):
        """
        切资方+自动进件，route_key=item_no  //海外资方不能互切，先不管
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
        self.msgsender.run_msg_by_order_no_list([item_no, ])
        import time
        time.sleep(1)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=1)

    def test_import_with_route_key_05_change_capital_bc_import(self, rule_2):
        """
        切资方+bc进件，前端传入一次路由route_uuid，找到正确路由记录  //海外资方不能互切，先不管
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
        item_no, asset_info = asset_import(self.rule_data_lt[1]["channel"], self.period, self.period_day,
                                           self.period_type, self.amount, self.from_system, self.from_app,
                                           self.source_type, self.four_element, item_no=item_no,
                                           route_uuid=self.route_key, insert_router_record=False,
                                           fees=self.fees, late_num=self.late_num)
        self.task.run_task(item_no, "AssetImport", excepts={"code": 0})
        check_router_load_record(self.rule_data_lt, route_key_2, self.four_element, self.amount,
                                 "imported", item_no, hit_channel_idx=1)
