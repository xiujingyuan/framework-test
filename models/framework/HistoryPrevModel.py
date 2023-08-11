# -*- coding: utf-8 -*-
# @Title: CaseModel
# @ProjectName gaea-api
# @Description: TODO
# @author fyi zhang
# @date 2019/1/5 0:46

from datetime import datetime
from elixir import *


class HistoryPrevModel(Entity):

    history_id = Field(Integer,primary_key=True)
    run_id = Field(Integer)
    prev_id = Field(Integer)
    prev_case_id=Field(Integer)
    prev_task_type=Field(String(255))
    prev_name=Field(String(255))
    prev_description=Field(String(255))
    prev_flag=Field(String(255))
    prev_setup_type=Field(String(255))
    prev_api_address=Field(String(255))
    prev_api_method=Field(String(255))
    prev_api_params=Field(Text)
    prev_api_header=Field(String(255))
    prev_api_expression=Field(Text)
    prev_sql_statement=Field(Text)
    prev_sql_params=Field(Text)
    prev_sql_database=Field(String(255))
    prev_sql_expression=Field(Text)
    prev_expression=Field(Text)
    prev_params=Field(Text)
    prev_except_expression=Field(Text)
    prev_except_value=Field(Text)
    prev_in_user=Field(String(255))
    prev_last_user=Field(String(255))
    prev_in_date=Field(DateTime,default=datetime.now())
    prev_last_date=Field(DateTime,default=datetime.now(),onupdate=datetime.now())
    using_options(tablename='history_prev_condition')
    def __repr__(self):
        return '<finlab_cases %r>' % self.history_id

