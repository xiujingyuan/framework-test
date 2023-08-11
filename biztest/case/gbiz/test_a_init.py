from biztest.config.gbiz.gbiz_kv_config import update_gbiz_msg_client_config, update_gbiz_base_config
from biztest.function.gbiz.gbiz_common_function import init_capital_plan
from biztest.function.gbiz.gbiz_db_function import clear_terminated_task
from biztest.interface.gbiz.gbiz_interface import monitor_check, asset_route
from biztest.util.dmp.dmp import publish_dmp_package
import pytest
import time

from biztest.util.es.es import ES
from biztest.util.tools.tools import get_four_element


class TestAInit(object):

    @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_init
    def test_gbiz_init(self):
        init_capital_plan()
        update_gbiz_base_config()
        update_gbiz_msg_client_config()
        publish_dmp_package()
        monitor_check()
        ES.clear_log(3)
        four_element = get_four_element()
        clear_terminated_task()
        try:
            asset_route(four_element, 6, 8000, "香蕉", "", '', '110000')
        except:
            pass
        time.sleep(10)
