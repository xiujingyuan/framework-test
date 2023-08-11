import pytest

from biztest.function.global_gbiz.gbiz_global_common_function import init_capital_plan


class TestAGlobalInit(object):

    @pytest.mark.global_gbiz_india
    @pytest.mark.global_gbiz_india_init
    def test_gbiz_india_init(self):
        init_capital_plan("india")

    @pytest.mark.global_gbiz_thailand
    @pytest.mark.global_gbiz_thailand_init
    def test_gbiz_thailand_init(self):
        init_capital_plan("thailand")

    @pytest.mark.global_gbiz_philippines
    @pytest.mark.global_gbiz_philippines_init
    def test_gbiz_philippines_init(self):
        init_capital_plan("philippines")

    @pytest.mark.global_gbiz_mexico
    @pytest.mark.global_gbiz_mexico_init
    def test_gbiz_mexico_init(self):
        init_capital_plan("mexico")

    @pytest.mark.global_gbiz_pakistan
    @pytest.mark.global_gbiz_pakistan_init
    def test_gbiz_pakistan_init(self):
        init_capital_plan("pakistan")
