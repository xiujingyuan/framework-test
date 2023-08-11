# -*- coding: utf-8 -*-
# @Time    : 公元18-12-18 上午8:40
# @Author  : 张廷利
# @Site    : 
# @File    : TestCatchException.py
# @Software: IntelliJ IDEA
import pytest
from common.tools.BaseUtils import catch_exception



class TestCatchException(object):


    @catch_exception
    def test_one(self):
        a = 10 /0

    @catch_exception

    def test_two(self):
        a = 10 /0


    @catch_exception

    def test_three(self):
        a = 10 /0


    @catch_exception
    def test_four(self):
        a = 10 /0


    @catch_exception

    def test_five(self):
        a = 10 /0

    @catch_exception
    def _six(self):
        a = 10 /0

    def _seven(self):
        self._six()

    def test_eight(self):
        self._seven()




if __name__=="__main__":
    pytest.main(" testCatchException.py --capture=no")
