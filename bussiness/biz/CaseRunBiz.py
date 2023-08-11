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
from models.framework.RunCaseDb import RunCase

class CaseRunBiz(object):

    @staticmethod
    def add_run_case(run_case):
        try:
            session.add(run_case)
            session.flush()
            run_id = run_case.run_id
            session.commit()
            return run_id
        except Exception as error:
            print(error)
        finally:
            session.commit()



    @staticmethod
    def update_run_case(run_case_temp,run_id):
        try:
            query = RunCase.query.filter()
            query = query.filter(RunCase.run_id == run_id)
            query.first()
        except Exception as error:
            print(error)
        finally:
            session.commit()