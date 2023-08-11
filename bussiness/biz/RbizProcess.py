# -*- coding: utf-8 -*-
# @Title: BizProcess
# @ProjectName framework-test
# @Description: TODO
# @author fyi zhang
# @date 2018/12/12 19:42

from bussiness.biz.CommonProcess import CommonProcess
from framework.dao.BizProcessDAO import BizProcessDAO
from common.tools.CommUtils import CommUtils
from common.tools.BaseUtils import BaseUtils
from common.tools.HttpUtils import HttpUtils
from common.tools.BusTools import BusTools
from framework.dao.FrameworkDAO import FrameworkDAO


class RbizProcess(CommonProcess):

    def __init__(self):
        self.biz_dao = BizProcessDAO()
        self.dao = FrameworkDAO()
        self.common_util = CommUtils()
        self.bustools = BusTools()
        self.http_util = HttpUtils()

    def prev_sync_withdrawsuccess(self,prev,case,case_vars):
        key_value = prev.prev_expression
        request_params = case.case_api_params
        main_requestbody_dict =BaseUtils.transfer_string_to_dict(case_vars)
        request_params_dict=BaseUtils.extend_value_target(main_requestbody_dict,request_params,key_value);
        request_params_dict = BaseUtils.transfer_string_to_dict(request_params_dict)
        if 'small_request' in main_requestbody_dict.keys():
            asset_item_no = main_requestbody_dict['small_request']['data']['asset']['item_no'];
            main_request_dtransactions = main_requestbody_dict['small_request']['data']['dtransactions']
            main_request_fees = main_requestbody_dict['small_request']['data']['fees']
        else:
            asset_item_no = main_requestbody_dict['main_request']['data']['asset']['item_no'];
            main_request_dtransactions = main_requestbody_dict['main_request']['data']['dtransactions']
            main_request_fees = main_requestbody_dict['main_request']['data']['fees']

        loan_records = request_params_dict['data']['loan_record']
        dtransaction = request_params_dict['data']['dtransactions']
        fees = request_params_dict['data']['fees']

        #TODO ID 开头的时间戳
        loan_records['identifier'] = "ID"+BaseUtils.get_uuid()
        #TODO RN 开头的时间戳
        loan_records['trade_no'] = "RN"+BaseUtils.get_uuid();

        for dtran in dtransaction:
            dtran['asset_item_no']=asset_item_no
            if dtran['period'] ==0:
                #TODO 当前时间
                for main_request_dtran in main_request_dtransactions:
                    if main_request_dtran['dtransaction_period'] ==0:
                        dtran['amount']=main_request_dtran['dtransaction_total_amount'] *100
                        dtran['total_amount']=main_request_dtran['dtransaction_total_amount'] *100
                        dtran['due_at'] =main_request_dtran['dtransaction_expect_finish_time']
                        dtran['finish_at']=main_request_dtran['dtransaction_expect_finish_time']
                        dtran['trade_at'] =main_request_dtran['dtransaction_expect_finish_time']

            else:
                for main_request_dtran in main_request_dtransactions:
                    if main_request_dtran['dtransaction_period'] ==dtran['period'] and dtran['type'] in main_request_dtran['dtransaction_type']:
                        dtran['amount']=str(int(main_request_dtran['dtransaction_amount'] *100))
                        dtran['total_amount']=str(int(main_request_dtran['dtransaction_total_amount'] *100))
                        dtran['due_at'] =main_request_dtran['dtransaction_expect_finish_time']

        for fee in fees:
            fee['asset_item_no']=asset_item_no
            for main_request_fee in main_request_fees:
                if fee['period'] == main_request_fee['fee_period'] and fee['type'] in main_request_fee['fee_type']:
                    fee['amount']=str(int(main_request_fee['fee_amount'] *100))
                    fee['total_amount']=str(int(main_request_fee['fee_total_amount'] *100))
                    fee['due_at'] =main_request_fee['fee_expect_finish_time']
        request_params_dict['key'] = BaseUtils.get_uuid()
        request_params_dict['data']['asset']['interest_amount'] = str(int(request_params_dict['data']['asset']['interest_amount'] *100))
        request_params = BaseUtils.transfer_dict_to_string(request_params_dict)
        case.case_api_params = self.bustools.repalce_system_params(request_params,vars=case_vars)

        return case


    def prev_get_withhold_amount(self,prev,case,case_vars):
        key_value = prev.prev_expression
        main_requestbody_dict =BaseUtils.transfer_string_to_dict(case_vars)
        asset_item_no = main_requestbody_dict['main_request']['data']['asset']['item_no'];
        asset_item_no_sub = main_requestbody_dict['main_request']['data']['asset']['source_number'];
        request_params_dict = BaseUtils.transfer_string_to_dict(case.case_api_params)
        database = self.bustools.repalce_system_params(prev.prev_sql_database,vars=case_vars)
        if request_params_dict['type']!='PaydayloanComboActiveRepay':
            case = self.process_otherwithhold_params(main_requestbody_dict,case,prev)
            return case
        project_list = request_params_dict['data']['project_list']
        request_params_dict['key'] =BaseUtils.get_uuid()
        project_list_len=0
        if isinstance(project_list,list):
            project_list_len = len(project_list)
        request_params_dict = BaseUtils.extend_value_target(case_vars,request_params_dict,key_value);
        request_params_dict = BaseUtils.transfer_string_to_dict(request_params_dict)
        if project_list_len == 2:
            main_amount = self.get_withhold_amount(asset_item_no,database)
            sub_amount = self.get_withhold_amount(asset_item_no_sub,database)
            total_amount = main_amount + sub_amount
            priority = []
            for project in project_list:
                priority.append(project['priority']);
            priority.sort()

            for project in project_list:
                if priority[0] == project['priority']:
                    project['amount'] = sub_amount
                    project['project_num'] = asset_item_no_sub
                else:
                    project['amount'] = main_amount
                    project['project_num'] = asset_item_no
            request_params_dict['data']['total_amount'] = total_amount
            request_params_dict['data']['project_list'] =project_list
            request_params = BaseUtils.transfer_dict_to_string(request_params_dict)
            case.case_api_params = request_params
        elif project_list_len ==1 :
            main_amount = self.get_withhold_amount(asset_item_no,database)
            total_amount = main_amount
            for project in project_list:
                project['amount'] = main_amount
                project['project_num'] = asset_item_no
            request_params_dict['data']['total_amount'] = total_amount
        request_params_dict['data']['project_list'] =project_list
        case.case_api_params = BaseUtils.transfer_dict_to_string(self.bustools.repalce_system_params(request_params_dict,vars=case_vars))
        return case


    def process_otherwithhold_params(self,main_request_dict ,case,prev_condition):
        request_params_dict = BaseUtils.transfer_string_to_dict(case.case_api_params)
        key_value = prev_condition.prev_expression
        database = self.bustools.repalce_system_params(prev_condition.prev_sql_database)
        type = request_params_dict['type']
        asset_item_no = main_request_dict['main_request']['data']['asset']['item_no'];
        if type =='FoxManualWithhold':
            request_params_dict = BaseUtils.extend_value_target(main_request_dict,request_params_dict,key_value)
            request_params_dict = BaseUtils.transfer_string_to_dict(request_params_dict)
            withhold_amount = self.get_withhold_amount(asset_item_no,database)
            request_params_dict['data']['amount'] = withhold_amount
            case.case_api_params = self.bustools.repalce_system_params(request_params_dict)
            return case




    def get_withhold_amount(self,asset_item_no,database):
        result = self.biz_dao.get_withhold_amount(asset_item_no,database)
        amount = int(result['amount'])
        return amount







