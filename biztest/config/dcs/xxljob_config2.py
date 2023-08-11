
job_group_dcs = 127

job_group_biz = {
    "biz3": {
        "group_id": 106,
        "settle_job_id": 1465,
        "buyback_job_id": 1526,
        "capital_tran_job_id": 1477
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



# 还款清分的job／task 以及job的参数
repay_handle_task = {
    "id": 1600,
    "handle": "biz_dcs_CapitalRepayToPendingJob",
    "task": "capitalRepayToPending",
    "task_Process": "capitalRepayToPendingProcess"
}
# "includeLoanChannels": [] 由配置控制有哪些资金方
repay_handle_params = {
    "assetBizType": "repay_loan_order",
    "processDate": "2020-05-11",
    "includeAssetItemNos": [
        "1111"
    ],
    "includeLoanChannels": [
        "1111"
    ]
}



# 代偿清分的job／task 以及job的参数
compensate_handle_task = {
    "id": 1554,
    "handle": "biz_dcs_CapitalCompensateToPendingJob",
    "task": "splitCapitalCompensateToPending",
    "task_list": {
        "compensate_task_Config": "singleCapitalCompensateToPending"
    },
    "task_Process": "capitalCompensateToPendingProcess"
}
# "includeLoanChannels": [] 由配置控制走哪些资金方
compensate_handle_params = {
    "excludeLoanChannels": [
        "yunxin_quanhu",
        "qnn",
        "hengfeng"
    ],
    "processDate": "2020-05-06",
    "includeAssetItemNos": [
        "1111"
    ],
    "includeLoanChannels": [
        "1111"
    ]
}



# 云信全互代偿清分的job／task 以及job的参数
quanhu_compensate_handle_task = {
    "id": 1620,
    "handle": "biz_dcs_YunxinCompensateToPendingJob",
    "task": "splitYunxinCompensateToPending",
    "task_list": {
        "compensate_task_Config": "checkYunxinCompensateToPending"
    },
    "task_Process": "yunxinCompensateToPendingProcess"
}
quanhu_compensate_handle_params = {
    "processDate": "2020-07-10",
    "includeAssetItemNos": [
        "ha_20201594378535366735_qh"
    ]
}


# 回购
buyback_handle_task = {
    "id": 1609,
    "handle": "biz_dcs_BuybackToPendingJob",
    "task": "buybackToPending",
    "task_Process": "capitalCompensateToPendingProcess"
}
buyback_params = {
    "processDate": "2020-09-10",
    "includeAssetItemNos": [
        "ha_20201599719349691098_qn"
    ],
    "includeLoanChannels": [
        "qinnong"
    ]
}



# 还款落地final的job／task 以及job的参数
repay_final_handle_task = {
    "id": 1611,
    "handle": "biz_dcs_PendingToFinalJob",
    "task": "cleanPendingToFinal",
    "task_list": {
        "task_final": "capitalRepayToFinalProcess",
        "task_trans": "loadRepayConfig"
    },
    "task_Process": "clearingTransProcess"
}
repay_final_params = {
    "assetBizType": "repay_loan_order"
}


# 代偿落地final的job／task 以及job的参数
compensate_final_handle_task = {
    "id": 1555,
    "handle": "biz_dcs_PendingToFinalJob",
    "task": "cleanPendingToFinal",
    "task_list": {
        "task_final": "capitalCompensateToFinalProcess",
        "task_trans": "loadCompensateConfig"
    },
    "task_Process": "clearingTransProcess"
}
compensate_final_params = {
    "assetBizType": "compensate_loan_order"
}




#  华北小贷和哈密天山提前结清的job一样，彼此的task不一样
hbxd_advance_clearing_job = {
    "id": 1601,
    "handle": "biz_dcs_AdvanceClearingJob",
    "task": "hbxdAdvanceClearing"
}
advance_clearing_params = {
    "loanChannel": "huabeixiaodai_zhitou",
    "processDate": "2020-06-28",
    "assetItemNo": "11",
    "dateType": "create_time",
    "holidayAdvance": "true",
    "defaultDateValue": "before"
}






task_handle = {
    "id": 1603,
    "handle": "dbTaskJob"
}
task_job_params = {
    "withInHour": 5,
    "delayMinute": 0,
    "priority": 2,
    "limit": 50
}











