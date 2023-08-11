# -*- coding: utf-8 -*-
# @Time    : 公元18-11-27 下午8:42
# @Author  : 张廷利
# @Site    : 
# @File    : testBaseUtils.py
# @Software: IntelliJ IDEA
import pytest
from common.tools.BaseUtils import strisnull

class TestBaseUtils(object):

    @strisnull
    def string_is_null(self,p1,p2,p3,p4=12,p5=None):
        pass

    @pytest.fixture(scope="function",params=[
        [2,1,None],[2,1,""],[2,1,3,""],[2,1,3,"test"],[2,1,3,"test",None]]
    )
    def data_provider(self,request):
        return request.param

    def test_string_is_null(self,data_provider):
        if len(data_provider) ==3:
            res = self.string_is_null(data_provider[0],data_provider[1],data_provider[2])
            assert isinstance(res,str)
        elif len(data_provider) == 4:
            if data_provider[3] is None:
                res = self.string_is_null(data_provider[0],data_provider[1],data_provider[2],p4=data_provider[3])
                assert isinstance(res,bool)
        else:
            res = self.string_is_null(data_provider[0],data_provider[1],data_provider[2],p4=data_provider[3],p5=data_provider[4])
            assert isinstance(res,str)

if __name__=="__main__":
    pytest.main(" testBaseUtils.py testHttpUtils.py --capture=no")