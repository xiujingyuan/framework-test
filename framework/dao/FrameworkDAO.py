# -*- coding: utf-8 -*-
# @Title: CommCls
# @ProjectName framework-test
# @Description: TODO
# @author fyi zhang
# @date 2018/11/2922:29


from common.tools.XmlTools import XmlTools
from common.tools.SqlTools import SqlTools
from common.tools.BaseUtils import BaseUtils,strisnull
from bussiness.biz.FinlabCaseBiz import FinlabCaseBiz

class FrameworkDAO(XmlTools,SqlTools):


    def __init__(self):
        self.xmltools = XmlTools()
        self.sqltools = SqlTools()




    def get_mock_response_byid(self,case_id,step_id):
        params ={"case_id":case_id,"step_id":step_id}
        sqlEntity = self.xmltools.get_complete_sqlentity("case.xml","get_mock_response_by_caseid",params)
        mock_entity = self.sqltools.queryoneBySqlEntity(sqlEntity)
        return BaseUtils.transfer_dict_to_entity(mock_entity)


    def get_special_keyvalue(self,key):
        params = {"key":key}
        sql_eneity = self.xmltools.get_complete_sqlentity("case.xml","get_special_keyvalue",params)
        result = self.sqltools.queryoneBySqlEntity(sql_eneity)
        return BaseUtils.transfer_dict_to_entity(result)

    def get_init_bycaseid(self,case_id,init_type):
        params = {"case_id":case_id,"init_type":init_type}
        sql_entity = self.xmltools.get_complete_sqlentity("case.xml","get_init_bycaseid",params)
        result = self.sqltools.queryallBySqlEntity(sql_entity)
        case_inits = BaseUtils.transfer_dict_to_entity(result)
        return list(case_inits)

    def get_init_byinitid(self,init_id,init_type):
        params = {"init_id":init_id,"init_type":init_type}
        sql_entity = self.xmltools.get_complete_sqlentity("case.xml","get_init_byinitid",params)
        result = self.sqltools.queryallBySqlEntity(sql_entity)
        case_inits = BaseUtils.transfer_dict_to_entity(result)
        return case_inits

    def get_prev_bycaseid(self,case_id,type):
        params ={"case_id":case_id,"type":type}
        sql_entity = self.xmltools.get_complete_sqlentity("case.xml","get_prev_by_tasktype",params)
        result = self.sqltools.queryallBySqlEntity(sql_entity)
        case_prev_conditions = BaseUtils.transfer_dict_to_entity(result)
        return case_prev_conditions


    def exec_init_sql(self,sql_statement,sql_database,sql_params):
        sql_entity = self.xmltools.get_actual_sqlentity(sql_statement,sql_params,sql_database)
        result = self.sqltools.uaiBySqlEntity(sql_entity)
        return BaseUtils.transfer_dict_to_entity(result)


    @strisnull
    def get_case_mock_response(self,case_id):
        sql_params={"case_id":case_id}
        sql_entity = self.xmltools.get_complete_sqlentity("case.xml","get_case_mock_response",sql_params)
        mock_model = SqlTools.queryoneBySqlEntity(sql_entity)
        return BaseUtils.transfer_dict_to_entity(mock_model)

    def get_prev_byonlycaseid(self,case_id):
        params ={"case_id":case_id}
        sql_entity = self.xmltools.get_complete_sqlentity("case.xml","get_prevs_bycaseid",params)
        result = self.sqltools.queryallBySqlEntity(sql_entity)
        case_prev_conditions = BaseUtils.transfer_dict_to_entity(result)
        return case_prev_conditions



    @strisnull
    def get_cases(self,system_name):
        sql_params = {"from_system":system_name}
        sql_entity = self.xmltools.get_complete_sqlentity("case.xml","get_cases",sql_params)
        cases=SqlTools.queryallBySqlEntity(sql_entity)
        return BaseUtils.transfer_dict_to_entity(cases)


    def exec_common_query(self,sql_statement,sql_database,sql_params):
        sql_entity = self.xmltools.get_actual_sqlentity(sql_statement,sql_params,sql_database)
        result = self.sqltools.queryallBySqlEntity(sql_entity)
        return BaseUtils.transfer_dict_to_entity(result)

    def exec_common_query_dict(self,sql_statement,sql_database,sql_params):
        sql_entity = self.xmltools.get_actual_sqlentity(sql_statement,sql_params,sql_database)
        result = self.sqltools.queryallBySqlEntity(sql_entity)
        return result

    # @strisnull
    # def get_sub_case(self,case):
    #     sql_params = {"case_exec_group":case.case_exec_group,"from_system":case.case_from_system}
    #     sql_entity = self.xmltools.get_complete_sqlentity("case.xml","get_sub_cases",sql_params)
    #     cases=SqlTools.queryallBySqlEntity(sql_entity)
    #     return BaseUtils.transfer_dict_to_entity(cases)
    @strisnull
    def get_sub_case(self,case):
        result = FinlabCaseBiz.Query_Sub_Case(case.case_exec_group, case.case_belong_business)
        return result



    def get_summery_report(self,run_id):
        sql_params ={"run_id_1":run_id,"run_id_2":run_id,"run_id_3":run_id,"run_id_4":run_id,"run_id_5":run_id,"run_id_6":run_id}
        sql_entity = self.xmltools.get_complete_sqlentity("case.xml","get_summary_support",sql_params)
        result=SqlTools.queryoneBySqlEntity(sql_entity)
        return BaseUtils.transfer_dict_to_entity(result)
