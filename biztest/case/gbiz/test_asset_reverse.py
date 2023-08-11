from biztest.function.gbiz.gbiz_check_function import check_asset_tran_data, check_wait_assetvoid_data
from biztest.interface.gbiz.gbiz_interface import *
from biztest.util.msg.msg import GbizMsg
from biztest.util.task.task import GbizTask
from biztest.function.gbiz.gbiz_db_function import *
import pytest
import common.global_const as gc


def lianlian_reverse_callback(asset_info, four_element, item_no):
    pass


class TestAssetReverse(object):
    """
    gbiz_assetreverse
    author: zhimengxue
    date: 20200501
    """
    @pytest.fixture()
    def case(self):
        pass

    # 矢隆四平、哈密天山、哈密天邦新疆、微神马大兴安岭3家资金方因为都是12期，且冲正方式一致，故集成到一个case中
    # 涉及配置为："manual_reverse_allowed": true, 存在于每个资金方自己的配置中
    # @pytest.mark.gbiz_auto_test
    @pytest.mark.gbiz_assetreverse
    @pytest.mark.parametrize("count", [12])
    def test_manual_assetreverse_success(self, case, count):
        task = GbizTask()
        msg = GbizMsg()
        #此处去掉shilong_siping是因为融担优化时，shilong没有配置新的费率编号，而以下资金方是配置了的，shilong需要有场景才能进件成功
        channels = ['yixin_rongsheng']
        for capital_channel in channels:
            four_element = get_four_element()
            item_no, asset_info = asset_import(capital_channel, four_element, count, 8000)
            task.run_task(item_no, "AssetImport", excepts={"code": 0})
            task.run_task(item_no, "AssetImportVerify", excepts={"code": 0})
            msg.run_msg(item_no, "AssetImportSync", excepts={"code": 0})
            # 获取item_no，修改资产状态、放款时间等
            item_no = (asset_info['data']['asset']['item_no'])
            sql = "update gbiz%s.asset set asset_status='repay',asset_actual_grant_at=now() where asset_item_no='%s';" % \
                  (gc.ENV, item_no)
            gc.GRANT_DB.update(sql)
            sql2 = "update gbiz%s.asset_loan_record set asset_loan_record_status=6,asset_loan_record_grant_at=now()," \
                   "asset_loan_record_finish_at=now(),asset_loan_record_push_at=now() where " \
                   "asset_loan_record_asset_item_no='%s';" % (gc.ENV, item_no)
            gc.GRANT_DB.update(sql2)
            # 调用清结算使用接口，生成冲正任务（和首金是一个原理）
            reverse_callback(asset_info)

            # 判断冲正任务是否是open的，是open再执行
            sql = "select task_status from gbiz%s.task where task_order_no='%s' and task_type='CapitalAssetReverse' " \
                  "order by task_id desc limit 1;" % (gc.ENV, item_no)
            result = gc.GRANT_DB.query(sql)
            task_status = result[0]["task_status"]
            if task_status == 'open':
                task.run_task(item_no, "CapitalAssetReverse", excepts={"code": 0})
                msg.run_msg(item_no, "AssetReverseNotifyV2", excepts={"code": 0})
                check_wait_assetvoid_data(item_no, code=14, message="发生冲正,作废资产")
            else:
                update_CapitalAssetReverse_status = "update gbiz%s.task set task_status='open' where task_order_no='%s'" \
                                                    " and task_type='CapitalAssetReverse' ;" % (gc.ENV, item_no)
                gc.GRANT_DB.update(update_CapitalAssetReverse_status)
                task.run_task(item_no, "CapitalAssetReverse", excepts={"code": 0})
                msg.run_msg(item_no, "AssetReverseNotifyV2", excepts={"code": 0})
                check_wait_assetvoid_data(item_no, code=14, message="发生冲正,作废资产")
                task.run_task(item_no, "GrantFailedLoanRecordSync", excepts={"code": 0})
                # 推送风控失败原因的没有将冲正配置到不捞取中，所以会在此时生成该通知
                msg.run_msg(item_no, "CapitalFailedLoanRecordSync", excepts={"code": 0})
                #取消的通知
                msg.run_msg(item_no, "AssetGrantCancelNotifyMQV2", excepts={"code": 0})



if __name__ == "__main__":
    pytest.main(["-s", "/Users/fenlai/code/framework-test/biztest/case/gbiz/qnn_lm.py", "--env=9"])
