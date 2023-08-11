# -*- coding: utf-8 -*-
# @Time    : 公元18-11-28 上午9:30
# @Author  : 张廷利
# @Site    : 
# @File    : HttpMockDb.py
# @Software: IntelliJ IDEA

import copy

class HttpMockDb(object):


    def __init__(self,db_dict):
        _entity = []
        if isinstance(db_dict,(tuple,list,set)):
            for db in db_dict:
                _temp_entity=Entity(db)
                _entity.append(copy.deepcopy(_temp_entity))
            self =_entity
        elif isinstance(db_dict,dict):
            self= Entity(dict)

class Entity(object):
    def __init__(self,object):
        self.__dict__.update(object)
