# -*- coding: utf-8 -*-
# @ProjectName:    framework-test$
# @Package:        $
# @ClassName:      HistoryCaseBiz$
# @Description:    描述
# @Author:         Fyi zhang
# @CreateDate:     2019/2/25$ 22:17$
# @UpdateUser:     更新者
# @UpdateDate:     2019/2/25$ 22:17$
# @UpdateRemark:   更新内容
# @Version:        1.0

from elixir import *
from models.framework.HistoryFinlabCaseDb import HistoryFinlabCase

class HistoryCaseBiz(object):

    @staticmethod
    def add_history_case(history_case):
        try:
            session.add(history_case)
        finally:
            session.commit()


    @staticmethod
    def query_history_bycaseid(case_id):

        try:
            query = HistoryFinlabCase.query.filter()
            if case_id is not None:
                query = query.filter(HistoryFinlabCase.history_case_id==case_id)
                query = query.filter(HistoryFinlabCase.run_id != 0)
            result = query.order_by(HistoryFinlabCase.history_id.desc()).first()
            return result
        except Exception as err:
            print(err)


