# coding: utf-8

from elixir import *
from sqlalchemy import DateTime, INTEGER, VARCHAR
import datetime


class RunCase(Entity):

    run_id = Field(INTEGER(), primary_key=True)
    run_from_system = Field(VARCHAR(11))
    run_status = Field(BOOLEAN)
    run_report = Field(VARCHAR(255))
    run_case_count = Field(INTEGER())
    run_success = Field(INTEGER())
    run_fail = Field(INTEGER())
    run_skip = Field(INTEGER())
    run_success_rate = Field(FLOAT())
    run_durations = Field(INTEGER())
    run_created_at = Field(DateTime, required=True, default=datetime.datetime.now())
    using_options(tablename='run_cases')

    # def __cmp__(self, other):
    #     return cmp(self.case_id.toLower(), other.case_id.toLower())

    def __repr__(self):
        return "{0}".format(self.run_id)

    # @staticmethod
    # def Query(run_id=None, project_system_name=None):
    #     query_return = []
    #     try:
    #         query = RunCase.query.filter()
    #         if run_id is not None:
    #             query = query.filter(RunCase.run_id == run_id)
    #         if project_system_name is not None:
    #             query = query.filter(RunCase.run_from_system == project_system_name)
    #         query_return = query.order_by(RunCase.run_id).all()
    #     except Exception as err:
    #         print(err)
    #     finally:
    #         session.commit()
    #         return query_return
    #
    # @staticmethod
    # def Query_Max_ID():
    #     query_return=0
    #     try:
    #         results = session.query(func.max(RunCase.run_id)).all()
    #         query_return = results[0][0] +1
    #     except Exception as err:
    #         print(err)
    #     finally:
    #         session.commit()
    #         return query_return


