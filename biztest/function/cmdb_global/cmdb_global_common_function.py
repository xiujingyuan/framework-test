from biztest.interface.cmdb_global.cmdb_global_interface import cmdb_rate_repay_calculate_v6
from copy import deepcopy


def get_fee_info_for_data_check(asset_info):
    repay_calculate = cmdb_rate_repay_calculate_v6(asset_info)
    return_temp = []
    temp = {"fee_type": None,
            "period": None,
            "amount": None,
            "due_at": None}
    for i in range(1, int(repay_calculate["data"]["calculate_conditions"]["data"]["period_count"]) + 1):
        for key, value in repay_calculate["data"]["calculate_result"].items():
            if key in ["interest", "principal"]:
                for fee in value:
                    if fee["period"] == i:
                        temp["fee_type"] = "repayinterest" if key == "interest" else "repayprincipal"
                        temp["period"] = fee["period"]
                        temp["amount"] = fee["amount"]
                        temp["due_at"] = fee["date"]
                        return_temp.append(deepcopy(temp))
            if key in ["fee", ]:
                for fee_key, fee_value in value.items():
                    for fee in fee_value:
                        if fee["period"] == i:
                            temp["fee_type"] = fee_key
                            temp["period"] = fee["period"]
                            temp["amount"] = fee["amount"]
                            temp["due_at"] = fee["date"]
                            return_temp.append(deepcopy(temp))
    return_fee = sorted(return_temp, key=lambda x: (x['fee_type'], x['period']), reverse=False)
    return return_fee
