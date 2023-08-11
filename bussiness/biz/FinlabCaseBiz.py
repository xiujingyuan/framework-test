# -*- coding: utf-8 -*-
# @ProjectName:    framework-test$
# @Package:        $
# @ClassName:      CaseRunBiz$
# @Description:    描述
# @Author:         Fyi zhang
# @CreateDate:     2019/2/25$ 22:20$
# @UpdateUser:     更新者
# @UpdateDate:     2019/2/25$ 22:20$
# @UpdateRemark:   更新内容
# @Version:        1.0

from elixir import *
from models.framework.FinlabCaseDb import FinlabCase
from sqlalchemy import or_
from common.tools.BaseUtils import BaseUtils,strisnull

class FinlabCaseBiz(object):

    @staticmethod
    def Query(case_id=None, project_system_name=None):
        query_return = []
        try:
            query = FinlabCase.query.filter()
            if case_id is not None:
                query = query.filter(FinlabCase.case_id == case_id)
            if project_system_name is not None:
                query = query.filter(FinlabCase.case_belong_business == project_system_name)

            query = query.filter(FinlabCase.case_is_exec == 1)
            query = query.filter(or_(FinlabCase.case_exec_group_priority == 'main',
                                     FinlabCase.case_exec_group == None,
                                     FinlabCase.case_exec_group == ''))
            query_return = query.order_by(FinlabCase.case_id).all()
            return query_return
        except Exception as err:
            print(err)

    @staticmethod
    def Query_Cases(case_ids):
        query_return = []
        try:
            query = FinlabCase.query.filter()
            if case_ids is not None:
                query = query.filter(FinlabCase.case_id.in_(case_ids))
            query = query.filter(FinlabCase.case_is_exec==1)
            query = query.filter(or_(FinlabCase.case_exec_group_priority=='main',FinlabCase.case_exec_group ==None,FinlabCase.case_exec_group ==''))
            query_return = query.order_by(FinlabCase.case_id).all()
            return query_return
        except Exception as err:
            print(err)


    @staticmethod
    def Query_Sub_Case(case_exec_group, project_system_name=None):
        # print("Query_Sub_Case", case_exec_group, project_system_name)
        query_return = []
        try:
            query = FinlabCase.query.filter()
            query = query.filter(FinlabCase.case_exec_group == case_exec_group)
            if project_system_name is not None:
                query = query.filter(FinlabCase.case_belong_business == project_system_name)
            query = query.filter(FinlabCase.case_is_exec==1)
            query = query.filter(FinlabCase.case_exec_group_priority=='sub')

            query_return = query.order_by(FinlabCase.case_exec_priority).all()
            return query_return
        except Exception as err:
            print(err)


    @staticmethod
    def Query_Case_By_Id(case_id):
        query_return = []
        try:
            query = FinlabCase.query.filter()
            if case_id is not None:
                query = query.filter(FinlabCase.case_id == case_id)
            query_return = query.order_by(FinlabCase.case_exec_priority).first()
            return query_return
        except Exception as err:
            print(err)


    @staticmethod
    def Update_Case(case,case_id):
        try:
            query =FinlabCase.query.filter()
            query.filter(FinlabCase.case_id==case_id)
        except Exception as err:
            print(err)
        finally:
            session.commit()



