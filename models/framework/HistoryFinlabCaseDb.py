# coding: utf-8

from elixir import *
from sqlalchemy import DateTime, INTEGER, VARCHAR
from sqlalchemy.dialects.mysql import TINYINT


class HistoryFinlabCase(Entity):
    history_id = Field(INTEGER(), primary_key=True)
    history_case_id = Field(INTEGER(), required=True)
    history_case_from_system = Field(Unicode(100), required=True)
    history_case_belong_business = Field(VARCHAR(100))
    run_id = Field(INTEGER())
    history_case_name = Field(VARCHAR(500))
    history_case_description = Field(VARCHAR(500))
    history_case_category = Field(VARCHAR(50))
    history_case_exec_group = Field(String(45))
    history_case_exec_group_priority = Field(String(45))
    history_case_exec_priority = Field(INTEGER())
    history_case_api_address = Field(VARCHAR(500))
    history_case_api_method = Field(VARCHAR(10))
    history_case_api_params = Field(Text)
    history_case_api_header = Field(VARCHAR(500))
    history_case_check_method = Field(VARCHAR(10))
    history_case_except_value = Field(Text, required=True)
    history_case_actual_value = Field(Text, required=True)
    history_case_result = Field(TINYINT, required=True)
    history_case_sql_actual_statement = Field(Text)
    history_case_sql_actual_database = Field(String(50))
    history_case_sql_params = Field(String(500))
    history_case_ref_tapd_id = Field(String(200))
    history_case_is_exec = Field(INTEGER())
    history_case_next_msg = Field(String(50))
    history_case_next_task = Field(VARCHAR(50))
    history_case_replace_expression = Field(Text)
    history_case_init_id = Field(String(500), default="0")
    history_case_wait_time = Field(INTEGER())
    history_case_vars_name = Field(Text)
    history_case_author = Field(VARCHAR(50))
    history_case_in_date = Field(DateTime)
    history_case_in_user = Field(VARCHAR(50))
    history_case_last_date = Field(DateTime)
    history_case_last_user = Field(VARCHAR(50))
    history_case_executor = Field(VARCHAR(50))
    history_case_mock_flag = Field(Enum('Y','N'))
    history_case_vars = Field(TEXT)
    # run_id = ManyToOne("RunCase")

    using_options(tablename='history_finlab_cases')

    #property()

    # def __cmp__(self, other):
    #     return cmp(self.case_id.toLower(), other.case_id.toLower())
    #
    def __repr__(self):
        return self.history_case_name

    # @staticmethod
    # def Query(history_case_id=None, run_case_id=None):
    #     query_return = []
    #     try:
    #         query = HistoryFinlabCase.query.filter()
    #         if history_case_id is not None:
    #             query = query.filter(HistoryFinlabCase.history_case_id == history_case_id)
    #         if run_case_id is not None:
    #             query = query.filter(HistoryFinlabCase.run_case_id == run_case_id)
    #         query_return = query.order_by(HistoryFinlabCase.history_case_id).all()
    #     except Exception as err:
    #         print(err)
    #     finally:
    #         session.commit()
    #         return query_return
    #
    # @staticmethod
    # def Query_One():
    #     query_return = []
    #     try:
    #         query = HistoryFinlabCase.query.filter()
    #         query = query.filter(HistoryFinlabCase.history_case_id == 0)
    #         query_return = query.order_by(HistoryFinlabCase.history_case_id).first()
    #     except Exception as err:
    #         print(err)
    #     finally:
    #         session.commit()
    #         return query_return
    #
    #
    # @staticmethod
    # def add_history(history_case):
    #
    #     try:
    #         session.add(history_case)
    #         session.commit()
    #     except Exception as err:
    #         print(err)
    #     finally:
    #         pass

