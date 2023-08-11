#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import common.global_const as gc


def get_contract_by_item_no(item_no):
    sql = "select * from contract where contract_asset_item_no = '%s'" % item_no
    contract = gc.CONTRACT_DB.query(sql)
    return contract


def get_contract_by_item_no_opportunity(item_no, contract_sign_opportunity, status=None):
    table = get_contract_table(item_no)
    sql = "select * from %s where contract_asset_item_no = '%s' and contract_sign_opportunity = '%s'" \
          % (table, item_no, contract_sign_opportunity)
    if status is not None:
        sql += " and contract_status = '%s'" % status
    sql += " group by contract_type"
    contract = gc.CONTRACT_DB.query(sql)
    return contract


def get_contract(item_no, contract_sign_opportunity, contract_type):
    table = get_contract_table(item_no)
    sql = "select * from %s where contract_asset_item_no = '%s' and contract_sign_opportunity = '%s' " \
          "and contract_type = '%s' order by contract_id asc" % (table, item_no, contract_sign_opportunity, contract_type)
    contract = gc.CONTRACT_DB.query(sql)
    return contract


def get_open_task_by_item_no(item_no):
    sql = "select * from task where task_order_no = '%s' and task_status = 'open'" % item_no
    contract = gc.CONTRACT_DB.query(sql)
    return contract


def get_open_task_by_item_no_and_task_type(item_no, task_type):
    sql = "select * from task where task_order_no = '%s' and task_status = 'open' and task_type = '%s'" % (item_no, task_type)
    contract = gc.CONTRACT_DB.query(sql)
    return contract


def create_contract(item_no, contract_type, contract_type_text, url, opportunity=None):
    table = get_contract_table(item_no)
    sql = "INSERT INTO %s (contract_create_at, contract_asset_item_no, contract_type, contract_type_text, " \
          "contract_url, contract_status, contract_from_system, contract_code, contract_apply_id, contract_flow_key, " \
          "contract_ref_item_no, contract_sign_at, contract_update_at, contract_sign_opportunity, contract_provider, " \
          "contract_subject) " \
          " VALUES (now(), '%s', '%s', '%s', " \
          "'%s', 'SUCCESS', 'dsq', " \
          "'BIZ111276200422034951', '20201587498579320992-20713-1587498591702', 'auth1_manman_flow', '%s_noloan', " \
          "now(), now(), '%s', 'YUN', '苏州')"\
          % (table, item_no, contract_type, contract_type_text, url, item_no, opportunity)
    contract = gc.CONTRACT_DB.insert(sql)
    return contract


def create_change_channel_task(item_no, old_channel, new_channel):
    sql = "INSERT INTO task (task_order_no, task_type, task_status, task_next_run_at, task_request_data, " \
          "task_response_data, task_memo, task_create_at, task_update_at, task_version, task_priority, " \
          "task_retrytimes) " \
          "VALUES ('%s', 'ChangeChannel', 'open', '2020-07-01 02:42:57', " \
          "'{\\\"apply_code\\\" : \\\"%s\\\",\\\"loan_channel\\\" : \\\"%s\\\",\\\"route_channel\\\" : \\\"%s\\\", " \
          "\\\"old_channel\\\" : \\\"%s\\\",\\\"version\\\" : 1593542576551,\\\"need_register\\\" : 1}', " \
          "'', '', '2020-07-01 02:42:57', '2020-07-01 02:42:57', 0, 1, 0)"\
            % (item_no, item_no, new_channel, new_channel, old_channel)
    result = gc.CONTRACT_DB.insert(sql)
    return result


def create_asset_import_task(item_no, channel):
    sql = "INSERT INTO task (task_order_no, task_type, task_status, task_next_run_at, task_request_data, " \
          "task_response_data, task_memo, task_create_at, task_update_at, task_version, task_priority, " \
          "task_retrytimes) VALUES ('%s', 'AssetImport', 'open', NOW(), " \
          "'{\\\"from_system\\\" : \\\"banana\\\",\\\"key\\\" : \\\"%s%s\\\"," \
          "\\\"type\\\" : \\\"DSQAssetImport\\\",\\\"data\\\" : {  \\\"configId\\\" : null,  \\\"type\\\" : null,  " \
          "\\\"capital\\\" : \\\"%s\\\",  \\\"scope\\\" : \\\"youxi_bill\\\",  \\\"fromSystemName\\\" : null,  " \
          "\\\"periodCount\\\" : 6,  \\\"signOpportunity\\\" : \\\"AssetImport\\\",  \\\"signType\\\" : null,  " \
          "\\\"condition\\\" : {\\\"loan_channel\\\" : null,\\\"source_type\\\" : null," \
          "\\\"from_system_name\\\" : null,\\\"period_count\\\" : null,\\\"sub_type\\\" : null  },  " \
          "\\\"itemNo\\\" : \\\"%s\\\",  \\\"refItemNo\\\" : \\\"%s_noloan\\\",  " \
          "\\\"cover\\\" : false,  \\\"constMap\\\" : { },  \\\"sequenceList\\\" : null}\\\n}', " \
          "'', '', NOW(), NOW(), 0, 2, 0)"\
          % (item_no, item_no, channel, channel, item_no, item_no)
    result = gc.CONTRACT_DB.insert(sql)
    return result


def get_sendmsg(item_no, sendmsg_type):
    sql = "select * from sendmsg where sendmsg_order_no = '%s' and sendmsg_type = '%s' " \
          "order by sendmsg_id asc" % (item_no, sendmsg_type)
    result = gc.CONTRACT_DB.query(sql)
    return result


def contract_create_attachment_by_item_no(item_no, channel, attachment_type, attachment_name, attachment_url):
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    table = get_contract_table(item_no)
    sql = "INSERT INTO %s" \
          " ( `contract_create_at`, `contract_asset_item_no`, `contract_type`, `contract_type_text`, `contract_url`, " \
          "`contract_status`, `contract_from_system`, `contract_code`, `contract_apply_id`, `contract_flow_key`, " \
          "`contract_ref_item_no`, `contract_sign_at`, `contract_update_at`, `contract_sign_opportunity`, " \
          "`contract_provider`, `contract_subject`, `contract_channel`, `contract_version`) VALUES( " \
          "'%s', '%s', %s, '%s', " \
          "'%s', 'SUCCESS', 'strawberry'," \
          " FLOOR(RAND() * 10000), '%s-30300-1611906119811', 'tpl2007301443234707AE', " \
          "'%s', '%s', '%s', 'AssetImport', 'YUN', '如皋智萃', " \
          "'%s', 1);" % \
          (table, now_time, item_no, attachment_type, attachment_name, attachment_url, item_no, item_no, now_time, now_time, channel )
    result = gc.CONTRACT_DB.insert(sql)
    return result


def get_contract_table(item_no):
    if item_no[0:4] == 'enc_':
        table = 'contract_enc'
    else:
        if item_no[0:4].isupper():
            table = 'contract_' + str(item_no[1:5])
        else:
            table = 'contract_' + str(item_no[0:4])
    return table


if __name__ == '__main__':
    print(get_contract_by_item_no("20201585883351257122"))
