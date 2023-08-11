#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @author: snow
 @software: PyCharm  
 @time: 2018/10/30
 @file: BaseDb.py
 @site:
 @email:
"""
from elixir import session
from elixir.entity import EntityDescriptor
from sqlalchemy.exc import IntegrityError


def get_kwargs(obj):
    attrs = obj.__dict__
    kwargs = {}
    for key, value in attrs.items():
        index = key.find('__') + 2 if key.find('__') > -1 else 0
        key = key[index:]
        kwargs[key] = value
    return kwargs


def commit(func):
    """
    每个sql创建后添加提交commit的修饰器
    """

    def _deco(*args, **kwargs):
        ret = func(*args, **kwargs)
        try:
            session.commit()
        except IntegrityError as err:
            print(err)

        return ret

    return _deco


class ClsBaseTb(object):

    def print_attr(self):
        for attr in self.__dict__:
            if not attr.startswith("_"):
                value = self.__getattribute__(attr)
                print(attr, value)

    def get_attrs(self):
        ret = []
        for attr in self.__dict__:
            if not attr.startswith("_"):
                ret.append(attr)
        return ret

    @classmethod
    @commit
    def update(cls, obj):
        data = get_kwargs(obj)
        cls.update_or_create(data)

    @classmethod
    @commit
    def create(cls, obj):
        kwargs = get_kwargs(obj)
        try:
            cls(**kwargs)
        except IntegrityError as err:
            print(err)
            return False
        else:
            return True

    @classmethod
    @commit
    def delete(cls, primary_value):
        my_cls = EntityDescriptor(cls)
        query = cls.query.filter(my_cls.primary_keys[0] == primary_value)
        ret = query.all()
        if ret:
            ret[0].delete()

    @classmethod
    @commit
    def delete_by_attr(cls, **kwargs):
        for kwarg, value in kwargs.items():
            query = cls.query.filter(cls.__dict__[kwarg] == value)
        ret = query.all()
        for item in ret:
            item.delete()

    @classmethod
    def Query(cls, **kwargs):
        query = cls.query.filter()
        for key in kwargs:
            if hasattr(cls, key):
                query = query.filter(getattr(cls, key) == kwargs[key])
        ret = query.all()
        return ret
