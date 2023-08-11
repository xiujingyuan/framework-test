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
from models.framework.HistoryPrevModel import HistoryPrevModel

class HistoryPrevBiz(object):

    @staticmethod
    def add_history_prev(history_prev):
        try:
            session.add(history_prev)
        except Exception as e:
            print(str(e))
        finally:
            session.commit()


    @staticmethod
    def query_history_bycaseid(case_id):

        try:
            query = HistoryPrevModel.query.filter()
            if case_id is not None:
                query = query.filter(HistoryPrevModel.prev_case_id==case_id)
            result = query.order_by(HistoryPrevModel.history_id).first()
            return result
        except Exception as err:
            print(err)


