# -*- coding: utf-8 -*-
# @Title: BizProcessDAO
# @ProjectName framework-test
# @Description: TODO
# @author fyi zhang
# @date 2018/12/12 19:47
from common.tools.XmlTools import XmlTools
from common.tools.SqlTools import SqlTools
from common.tools.BaseUtils import BaseUtils,strisnull

class BizProcessDAO(object):

    def __init__(self):
        self.xmltool = XmlTools()
        self.sqltool = SqlTools()

    def get_prevs_bycaseid(self,case_id,prev_setup_type,prev_task_type):
        params = {"prev_case_id":case_id,"prev_setup_type":prev_setup_type,"prev_task_type":prev_task_type}
        sql_entity = self.xmltool.get_complete_sqlentity("bizcore.xml","get_prevs_bycaseid",params)
        result = SqlTools.queryallBySqlEntity(sql_entity)
        return BaseUtils.transfer_dict_to_entity(result)

    def judge_prev_exists(self,case_id):
        params = {"prev_case_id":case_id,}
        sql_entity = self.xmltool.get_complete_sqlentity("bizcore.xml","judge_prev_exists",params)
        result = SqlTools.queryallBySqlEntity(sql_entity)
        return BaseUtils.transfer_dict_to_entity(result)



    def update_task_by_taskid(self,task_id,db_server):
        params = {"task_id":task_id}
        sql_entity = self.xmltool.get_complete_sqlentity("bizcore.xml","update_task_by_taskid",params)
        result = SqlTools.uaiBySqlEntity(sql_entity,db_server)
        return BaseUtils.transfer_dict_to_entity(result)

    def update_msg_by_taskid(self,sendmsg_id,db_server):
        params = {"sendmsg_id":sendmsg_id}
        sql_entity = self.xmltool.get_complete_sqlentity("bizcore.xml","update_task_by_msgid",params)
        result = SqlTools.uaiBySqlEntity(sql_entity,db_server)
        return result

    def get_prev_condition_by_tasktype(self,case_id,task_type,setup_type):
        params = {"task_type":task_type,"case_id":case_id,"setup_type":setup_type}
        sql_entity = self.xmltool.get_complete_sqlentity("bizcore.xml","get_prev_by_tasktype",params)
        result = SqlTools.queryallBySqlEntity(sql_entity)
        case_prev_conditions = BaseUtils.transfer_dict_to_entity(result)
        return case_prev_conditions

    def gettaskandmsg_bycase_id(self,case_id,setup_type):
        params = {"task_type":"task","msg_type":"msg","case_id":case_id,"setup_type":setup_type}
        sql_entity = self.xmltool.get_complete_sqlentity("bizcore.xml","gettaskmsg_bycase_id",params)
        result = SqlTools.queryallBySqlEntity(sql_entity)
        case_prev_conditions = BaseUtils.transfer_dict_to_entity(result)
        return case_prev_conditions


    def get_withhold_amount(self,item_no,dbserver):
        params = {"asset_item_no":item_no,"asset_item_no_1":item_no}
        sql_entity = self.xmltool.get_complete_sqlentity("repay.xml","get_withhold_amount",params)
        result = SqlTools.queryoneBySqlEntity(sql_entity)
        params_rbiz = {"asset_item_no":item_no}
        sql_entity_rbiz = self.xmltool.get_complete_sqlentity('repay.xml','get_withhold_amount_rbiz',params_rbiz)
        result_rbiz = SqlTools.queryoneBySqlEntity(sql_entity_rbiz,dbserver)
        if result is not None:
            biz_amount = int(result['amount'])
        rbiz_amount =0
        if result_rbiz['amount'] is not None:
            rbiz_amount = int(result_rbiz['amount'])
        if biz_amount > rbiz_amount:
            return result
        else:
            return result_rbiz

