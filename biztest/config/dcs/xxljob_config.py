job_group_dcs = 116

job_group_biz = {
    "biz3": {
        "group_id": 106,
        "settle_job_id": 1465,
        "buyback_job_id": 1526,
        "capital_tran_job_id": 1477,
        "task_job_id": 1423
    },
    "biz4": {
        "group_id": 107,
        "settle_job_id": 1482
    },
    "biz2": {
        "group_id": 105,
        "settle_job_id": 1614,
        "buyback_job_id": 1638
    }
}

# 还款清分的 task
repay_tasks = {
    "task": [
        "accountChangeNotifySync",  # 一次至少两个task
        "accountRepaySave",  # 一次 一个task
        "bigRepayClearing",  # 一次 一个task
        "capitalRepayToPendingProcess",  # 一个资产一个期次 一个task（多期还款时有多个）
        "capitalRepayToFinalProcess",  # 一个资产一个期次 一个task（多期还款时有多个）
        "loadRepayConfig",  # 一个资产一个期次 一个task（多期还款时有多个）
        "clearingTransProcess"  # 一个资产一个期次 一个task（多期还款时有多个）
    ]
}

# 代偿清分的job／task
compensate_handle_tasks = {
    "id": 1442,
    "handle": "biz_dcs_CapitalCompensateToPendingJob",
    "task": [
        "splitCapitalCompensateToPending",  # 一个task
        "singleCapitalCompensateToPending",  # 一个task
        "capitalCompensateToPendingProcess",  # 一个task
        "capitalCompensateToFinalProcess",
        "loadCompensateConfig",  # 一个资产一个期次 一个task（多期还款时有多个）
        "clearingTransProcess"  # 一个资产一个期次 一个task（多期还款时有多个）
    ]
}

# 小单代偿清分的job／task
noloan_compensate_handle_tasks = {
    "id": 1581,
    "handle": "biz_dcs_precharg_compensate_clearing_job",
    "task": [
        "prechargeCollectCompensate",  # 一个task
        "prechargeCompensateClearing"  # 一个task
    ]
}

# 权益过期作废的job／task
not_received_handle_tasks = {
    "id": 1582,
    "handle": "biz_dcs_not_received_clearing_fix_job",
    "task": [
        "notReceivedCollectTran",  # 一个task
        "notReceivedFixTran"  # 一个task
    ]
}

# 权益过期作废的job／task
auto_settlement_handle_tasks = {
    "id": 1448,
    "handle": "biz_dcs_AutoSettlementJob",
    "task": [
        "lockClearingTrans",  # 多个task
        "newSettlement",  # 多个task
        "newTransfer",  # 多个task
        "applyTransfer"
    ]
}

# 还款／代偿 清分job 的参数
clearing_handle_params = {
    "processDate": "2020-05-06",
    "includeAssetItemNos": [
        "1111"
    ],
    "includeLoanChannels": [
        "1111"
    ]
}

# 还款／代偿 清分job 的参数
clearing_handle_params_new = {
    "excludeLoanChannels": [],
    "processDate": "2022-11-10",
    "includeAssetItemNos": [
        "111"
    ],
    "includeLoanChannels": [
        "loanchannel"
    ]
}

# 自动归集参数
auto_collect_params = {
    "startDate": "2022-11-29",  # 代扣完成时间，默认前一天
    "endDate": "2022-11-30",  # 代扣完成时间，默认当天
    "version": "v1",  # 防止重复归集版本号，默认填写v1，重跑时需更改此值
    "withholdTypes": [  # 需要归集的代扣类型
        "loan",
        "precharge"
    ],
    "withholdResultIds": []  # 代扣id，重跑时使用
}
# 回归参数
auto_buyback_params = {
    "processDate": "2022-06-14",  #processDate是buyback_create_at
    "includeAssetItemNos": [
        "B20221655195916"
    ],
    "includeLoanChannels": [
        "jinmeixin_daqin"
    ]
}

# 资金归集失败重新归集入口
retry_collect_params = {
    "orderId": 39337
}
# 大小单自动结算参数
auto_settlement_params = {
    "loanType": "BIG",  #大单BIG，小单PRECHARGE
    "includeAccrualTypes": [],
    "excludeAccrualTypes": [],
    "includeTransferIns": [
        # "v_bx_qingnong_jy",
        # "v_hefei_weidu_reserve",
        # "v_hefei_weidu_bobei"
    ],
    "excludeTransferIns": [],
    "includeTransferOuts": [],
    "excludeTransferOuts": []
}

# dcs执行task-job
dbtaskjob_params_new = {
    "withInHour": 5,
    "delayMinute": 0,
    "priority": 2,
    "limit": 50
}

# 结算job 的参数
auto_settlement_handle_params = {
    "loanType": "BIG",
    "includeAccrualTypes": [
    ],
    "excludeAccrualTypes": [
    ],
    "includeTransferIns": [
        # "v_hefei_weidu_bobei"
    ],
    "excludeTransferIns": [
    ],
    "includeTransferOuts": [
    ],
    "excludeTransferOuts": [
    ]
}

# 云信全互代偿清分的job／task
quanhu_compensate_handle_tasks = {
    "id": 1450,
    "handle": "biz_dcs_YunxinCompensateToPendingJob",
    "task": [
        "splitYunxinCompensateToPending",
        "checkYunxinCompensateToPending",
        "yunxinCompensateToPendingProcess",
        "capitalCompensateToFinalProcess",
        "loadCompensateConfig",
        "clearingTransProcess"
    ]
}

# 云信全互代偿 清分job 的参数
quanhu_compensate_handle_params = {
    "processDate": "2020-07-10",
    "includeAssetItemNos": [
        "ha_20201594378535366735_qh"
    ]
}

# 回购清分的job／task
buyback_handle_tasks = {
    "id": 1527,
    "handle": "biz_dcs_BuybackToPendingJob",
    "task": [
        "buybackToPending",
        "capitalCompensateToPendingProcess",
        "capitalCompensateToFinalProcess",
        "loadCompensateConfig",
        "clearingTransProcess"
    ]
}

# 回购 清分job 的参数
buyback_params = {
    "processDate": "2020-09-10",
    "includeAssetItemNos": [
        "ha_20201599719349691098_qn"
    ],
    "includeLoanChannels": [
        "qinnong"
    ]
}

# 回购和退单处理的job／task
buyback_clearing_job = {
    "id": 1646,
    "handle": "biz_dcs_BuyBackGuaranteeJob",
    "task": [
        "buyBackCapitalFee"
    ]
}

# 回购和退单处理 job 的参数
buyback_clearing_params = {
    "processDate": "2020-12-29",
    "assetItemNos": [
        "ha_20201609220468986833_wsm"
    ],
    "loanChannels": [
        "weishenma_daxinganling"
    ]
}

# 华北小贷提前结清的job
hbxd_advance_clearing_job = {
    "id": 1490,
    "handle": "biz_dcs_AdvanceClearingJob",
    "task": [
        "hbxdAdvanceClearing"
    ]
}
# 提前结清 job 的参数
advance_clearing_params = {
    "loanChannel": "huabeixiaodai_zhitou",
    "processDate": "2020-06-28",
    "assetItemNo": "11",
    "dateType": "create_time",
    "holidayAdvance": "true",
    "defaultDateValue": "before"
}

task_handle = {
    "id": 1668,
    "handle": "dbTaskJob"
}
task_job_params = {
    "withInHour": 5,
    "delayMinute": 0,
    "priority": 2,
    "limit": 50
}

capital_settlement_tasks = {
    "task": [
        "capitalSettlementPending",
        "capitalSettlementClearing"
    ]
}

quanhu_compensate_tasks = {
    "task": [
        "saveYunxinCompensate"
    ]
}

# # 海外代偿的job／task
# global_compensate_handle_tasks = {
#     "id": 28,
#     "handle": "biz_dcs_CompensateCleanFinalJob",
#     "task": [
#         "compensateToFinalProcess"
#     ]
# }

# 海外 代偿 清分job 的参数
global_compensate_params = {
    "loanChannels": [
        "tha_picocapital_plus",
        "tha_picocapital_qr",
        "noloan"
    ],
    "dueDate": "2021-07-08"
}

# 还款
global_repay_params = {
    "processDate": "2021-03-24",
    "assetItemNo": "C2021070662376312633"
}

# 还款结算
global_repay_settle_params = {
    "assetItemNo": "C2021070662376312633"
}

# 大单代偿结算
global_compensate_settle_params = {
    "assetItemNo": "C2021070662376312633",
    "channel": "",  # 必须指定，不是默认所有的
    "startDate": "",
    "endDate": "",
    "limit": 0,
    "leastAmount": 0  # 根据leastAmount过滤代偿结算,当账户余额小于配置的leastAmount就不会发起代偿--》
    # task#splitCompensateSettlement（KV#dcs_loan_config中所有出户的余额必须大于JOB传入的leastAmount金额才会创建这个task）
}

global_finalToTran_params = {
    "bizType": "repay"
}

# 代扣成本
global_withhold_cost_params = {
    "startDate": "2022-12-09",
    "endDate": "2022-12-09",
    "limit": 1000,
    "serialNoList": [
        "AUTO_C612098220492936172"
    ]
}
