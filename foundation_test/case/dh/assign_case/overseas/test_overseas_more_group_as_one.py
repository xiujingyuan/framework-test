
from foundation_test.util.db.db_util import DataBase
from foundation_test.util.tools.tools import *
import foundation_test.config.dh.db_const as dc


# class TestOverseasMoreGroupAsOne(object):
#     @classmethod
#     def setup_class(cls):
#         # country=thailand,environment=test
#         dc.init_dh_env(dc.ENV, dc.COUNTRY, dc.ENVIRONMENT)
#
#     @classmethod
#     def teardown_method(cls):
#         DataBase.close_connects()
#
#     @pytest.mark.dh_auto_test
#     @pytest.mark.dh_overseas_assign
#     @pytest.mark.dh_overseas_more_as_one_avg_num
#     def test_overseas_more_group_avg_num(self):
#         # 调用quartz任务，目前分案策略执行方式只支持quartz
#         # 先写国内。。。
#         run_quartz(2, "newCombineSeveralIntoOne")
#         1

