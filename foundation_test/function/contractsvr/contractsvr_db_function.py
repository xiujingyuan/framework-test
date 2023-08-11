#!/usr/bin/python
# -*- coding: UTF-8 -*-
from foundation_test.util.db.db_util import DataBase

db = DataBase("contractsvr")


def get_contract_by_contract_id(contract_id):
    sql = "select * from contract where contract_id = '%s'" % contract_id
    result = db.query(sql)
    return result


def get_contract_apply_by_apply_id(apply_id):
    sql = "select * from contract_apply where apply_id = '%s'" % apply_id
    result = db.query(sql)
    return result


def get_latest_contract_apply_by_apply_id_prefix(apply_id_prefix):
    sql = "select * from contract_apply where apply_id like '{0}%' order by id desc limit 1".format(apply_id_prefix)
    result = db.query(sql)
    return result


def get_contract_id_by_apply_id(apply_id):
    sql = "select * from contract where contract_apply_id = '%s'" % apply_id
    result = db.query(sql)
    return result[0]['contract_id']


def add_seal_log(contract_id):
    sql = "INSERT INTO contract_seal_log (trans_id, contract_id, contract_individual_id, contract_provider, " \
          "seal_key, seal_type, status, retry, created_at, finish_at) " \
          "VALUES " \
          "('', '%s', 0, '', 'phtest_seal', 1, 1, 0, '2020-09-02 10:47:04', '2020-09-02 10:47:06')" \
          % contract_id
    print(sql)
    db.update(sql)
