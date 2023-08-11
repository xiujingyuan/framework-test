# -*- coding: utf-8 -*-
# @Title: CaseModel
# @ProjectName gaea-api
# @Description: TODO
# @author fyi zhang
# @date 2019/1/5 0:46

from datetime import datetime
from elixir import *


class HistoryInitModel(Entity):
    history_id = Field(Integer,primary_key=True)
    case_init_case_id = Field(Integer)
    case_init_id = Field(Integer)
    run_id = Field(Integer)
    case_init_type = Field(String(255))
    case_init_name= Field(String(255))
    case_init_description= Field(String(255))
    case_init_api_address= Field(String(255))
    case_init_api_method= Field(String(255))
    case_init_api_params= Field(String(255))
    case_init_api_header= Field(String(255))
    case_init_api_expression= Field(Text)
    case_init_sql= Field(Text)
    case_init_sql_params= Field(Text)
    case_init_sql_expression= Field(Text)
    case_init_sql_database= Field(String(255))
    case_init_indate=Field(DateTime,default=datetime.now())
    case_init_inuser = Field(String(255))
    case_init_lastuser= Field(String(255))
    case_init_lastdate=Field(DateTime,default=datetime.now(),onupdate=datetime.now())

    using_options(tablename='history_cases_init')


    def __repr__(self):
        return '<finlab_cases %r>' % self.history_id



