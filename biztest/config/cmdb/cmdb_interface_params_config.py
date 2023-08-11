from biztest.util.tools.tools import *

rate_route_v6_info = {
    "from_system": "GBIZ",
    "key": get_guid(),
    "type": "Route",
    "data": {
        "scope": "youxi_bill",
        "domain": "paydayloan",
        "principal": 250000,
        "condition": {
            "source_type": "youxi_bill",
            "from_system": "strawberry",
            "risk_level": "2"
        },
        "period_count": 6,
        "period_term": 1,
        "period_type": "month",
        "loan_channel": None
    }
}

rate_adjust_v6_info = {
    "from_system": "GBIZ",
    "key": "RateAdjust_a722fee0-fc45-45e5-a6d4-48c60f5dce39",
    "type": "RateAdjust",
    "data": {
        "sign_date": "2019-11-27 14:40:48",
        "product_number": "qnn_lm_6_1m_20190103",
        "period_count": None,
        "principal_amount": 600000,
        "capital_result": []
    }
}

rate_loan_calculate_v6_info = {
    "from_system": "GBIZ",
    "key": get_guid(),
    "type": "LoanCalculateRepayPlan",
    "data": {
        "itemNo": "",
        "sign_date": get_date(fmt="%Y-%m-%d"),
        "apply_amount": 100000,
        "period_count": 6,
        "period_type": "month",
        "period_term": 1,
        "product_number": "trmy_6_1m_20190730",
        "interest_rate": None,
        "scope": "youxi_bill",
        "loan_channel": "tongrongmiyang"
    }
}

rate_repay_calculate_v6_info = {
    "from_system": "GBIZ",
    "key": get_guid(),
    "type": "RepayCalculateRepayPlan",
    "data": {
        "itemNo": "",
        "sign_date": get_date(fmt="%Y-%m-%d"),
        "apply_amount": 100000,
        "period_count": 6,
        "period_type": "month",
        "period_term": 1,
        "product_number": "qh_3_1m_20191218",
        "interest_rate": None,
        "scope": "youxi_bill",
        "loan_channel": "tongrongmiyang"
    }
}
