# coding: utf-8

from elixir import *
from sqlalchemy import DateTime, INTEGER, String, Text, VARCHAR,or_


class FinlabCase(Entity):

    case_id = Field(INTEGER(), primary_key=True)
    case_from_system = Field(VARCHAR(100))
    case_belong_business = Field(VARCHAR(100))
    case_name = Field(VARCHAR(500))
    case_description = Field(VARCHAR(500))
    case_category = Field(VARCHAR(50))
    case_exec_group = Field(String(45))
    case_exec_group_priority = Field(String(45))
    case_exec_priority = Field(INTEGER())
    case_api_address = Field(VARCHAR(500))
    case_api_method = Field(VARCHAR(10))
    case_api_params = Field(Text)
    case_api_header = Field(VARCHAR(500))
    case_check_method = Field(VARCHAR(10))
    case_except_value = Field(Text)
    case_sql_actual_statement = Field(Text)
    case_sql_actual_database = Field(String(50))
    case_sql_params = Field(String(500))
    case_ref_tapd_id = Field(String(200))
    case_is_exec = Field(INTEGER())
    case_next_msg = Field(String(50))
    case_next_task = Field(VARCHAR(50))
    case_replace_expression = Field(Text)
    case_init_id = Field(String(500), default="0")
    case_wait_time = Field(INTEGER())
    case_vars_name =  Field(VARCHAR(50))
    case_author = Field(VARCHAR(50))
    case_in_date = Field(DateTime)
    case_in_user = Field(VARCHAR(50))
    case_last_date = Field(DateTime)
    case_last_user = Field(VARCHAR(50))
    case_executor = Field(VARCHAR(50))
    case_mock_flag = Field(Enum('Y','N'))

    using_options(tablename='finlab_cases')

    def get_attrs(self):
        ret = []
        for attr in self.__dict__:
            if not attr.startswith("_"):
                ret.append(attr)
        return ret

    # def __cmp__(self, other):
    #     return cmp(self.case_id.toLower(), other.case_id.toLower())

    # def __repr__(self):
    #     return self.case_description
    #
    # @staticmethod
    # def Query(case_id=None, project_system_name=None, system_module=None):
    #     query_return = []
    #     try:
    #         query = FinlabCase.query.filter()
    #         if case_id is not None:
    #             query = query.filter(FinlabCase.case_id == case_id)
    #         if project_system_name is not None:
    #             query = query.filter(FinlabCase.case_from_system == project_system_name)
    #         # if system_module is not None:
    #         #     query = query.filter(FinlabCase.case_executor == system_module)
    #         query = query.filter(FinlabCase.case_is_exec==1)
    #         query = query.filter(or_(FinlabCase.case_exec_group_priority=='main',FinlabCase.case_exec_group ==None))
    #         query_return = query.order_by(FinlabCase.case_id).all()
    #     except Exception as err:
    #         print(err)
    #     finally:
    #         return query_return
    #
    # @strisnull
    # def get_case_by_systemname(self,case_from_system):
    #     query_retrun=[]
    #     try:
    #         query = FinlabCase.query.filter(FinlabCase.case_is_exec==1,FinlabCase.case_from_system==case_from_system).\
    #             filter(or_(FinlabCase.case_exec_group == None,FinlabCase.case_exec_group==""))
    #
    #     except Exception as e:
    #         print(e)








#
# if __name__ == "__main__":
#     ip, port, user, pwd, database = "127.0.0.1", 3317, "root", "Coh8Beyiusa7", "gaea_framework"
#     init_mysql(ip, port, user, pwd, database)
#     mycls = RunCase()
#     mycls.run_report = "save_report"
#     # 保存本次运行的用例情况
#     mycls.run_from_system = "stem_name"
#     mycls.run_case_count = 2
#     mycls.run_status = 1
#     mycls.run_success = 2
#     mycls.run_fail = 0
#     mycls.run_skip = 0
#     mycls.run_success_rate = 100.00
#     mycls.run_durations = 5
#     mycls.print_attr()

