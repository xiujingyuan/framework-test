import pytest

from biztest.interface.cmdb.cmdb_interface import *
from biztest.util.asserts.assert_util import Assert

rate_list = {
    6: [
        {"rate_number": "trqjj_6m_20220308", "loan_channel": "tongrongqianjingjing", "from_system": ["banana", "strawberry"]},
        {"rate_number": "hhqjj_6_m_20210709", "loan_channel": "haohanqianjingjing", "from_system": ["banana", "strawberry"]},
    ],
    12: [
        {"rate_number": "dxalzy_12m_20230110", "loan_channel": "daxinganling_zhongyi", "from_system": ["banana", "strawberry", "pitaya"]},
        {"rate_number": "trqjj_12m_20230616", "loan_channel": "tongrongqianjingjing", "from_system": ["banana", "strawberry"]},
        {"rate_number": "hhqjj_12_m_20210709", "loan_channel": "haohanqianjingjing", "from_system": ["banana", "strawberry"]},
    ]
}


class TestCmdbRateRoute:
    @pytest.mark.cmdb
    @pytest.mark.parametrize("from_system, source_type, period_count",
                            [("strawberry", "apr36", 6),
                             ("strawberry", "apr36", 12),
                             ("banana", "apr36", 6),
                             ("banana", "apr36", 12),
                             ("pitaya", "real36", 6),
                             ("pitaya", "real36", 12),
                            ])
    def test_cmdb_rate_route(self, from_system, source_type, period_count):
        """
        路由费率
        """
        resp = cmdb_rate_route_v6(from_system, source_type, period_count, 3000)
        actual_rate_list = resp['data']['rateList'] if resp['data'] is not None else []
        expect_rate_list = [{"rate_number": x["rate_number"], "loan_channel": x["loan_channel"]}
                            for x in rate_list[period_count] if from_system in x['from_system']]
        actual_set = {frozenset(row.items()) for row in actual_rate_list}
        expect_set = {frozenset(row.items()) for row in expect_rate_list}
        Assert.assert_equal(set(), expect_set - actual_set)

    @pytest.mark.cmdb
    @pytest.mark.parametrize("from_system, source_type, period_count, loan_channel, amount, expect_rate_number",
                            [("strawberry", "apr36", 6, "qinnong", 3000, ""),
                             ("strawberry", "apr36", 12, "qinnong", 3000, ""),
                             ("strawberry", "irr36_quanyi", 6, "qinnong", 3000, "qinnong_6_m_20210818"),
                             ("banana", "irr36_quanyi", 12, "qinnong", 3000, "qinnong_12_m_20210818"),
                             ("strawberry", "irr36", 6, "qinnong", 3000, "qinnong_6_m_20210818"),
                             #("banana", "irr36", 12, "qinnong", 3000, "qinnong_12_m_20210818"),
                             #("strawberry", "real36", 6, "qinnong", 3000, ""),
                             ("strawberry", "lieyin", 5, "noloan", 100, "noloan_quanyi_5_m_20210818"),
                            ])
    def test_cmdb_rate_route_with_channel(self, from_system, source_type, period_count, loan_channel, amount, expect_rate_number):
        """
        带channel路由费率
        """
        resp = cmdb_rate_route_v6(from_system, source_type, period_count, amount, loan_channel)
        if expect_rate_number:
            Assert.assert_equal(0, resp['code'])
            Assert.assert_equal(expect_rate_number, resp['data']['rateList'][0]['rate_number'])
        else:
            Assert.assert_equal(1, resp['code'])
            Assert.assert_equal("不能找到合适的费率编号", resp['message'])
