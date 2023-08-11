import traceback

from app.create_data import create_data
from biztest.function.rbiz.CreateData import AssetImportFactory
from datetime import datetime
from flask import jsonify, request

from biztest.function.rbiz.create_combo_build_info import BuildCombineWithhold


@create_data.route('/')
def hello_world():
    return 'hello rbiz api'


@create_data.route('/create_normal_asset', methods=["GET"])
def create_normal_asset():
    ret = {
        "code": 1,
        "message": "create data failed",
        "data": {
            "item_no": "",
            "item_no_x": "",
        }
    }
    env, loan_channel = 2, "hami_tianshan"
    country = request.json["country"] if "country" in request.json else "china"
    day = request.json["day"] if "day" in request.json else 0
    asset_import = AssetImportFactory.get_import_obj(env, country)
    ret["data"]["item_no"], ret["data"]["item_no_x"], ret["data"]["four_element"] = asset_import.create_normal_asset(loan_channel,
                                                                                        count=12,
                                                                                        period_day=day)
    ret["code"] = 0
    ret["message"] = "create data success"
    return jsonify(ret)


@create_data.route('/create_asset', methods=["POST"])
def create_asset():
    ret = {
        "code": 1,
        "message": "create data failed",
        "data": {
            "item_no": "",
            "item_no_x": "",
        }
    }
    try:
        env = request.json["env"]
        loan_channel = request.json["loan_channel"]
        count = request.json["count"]
        advance_month = request.json["advance_month"]
        country = request.json["country"] if "country" in request.json else "china"
        source_type = request.json["source_type"] if "source_type" in request.json else None
        day = request.json["day"] if "day" in request.json else 0
        advance_day = request.json["advance_day"] if "advance_day" in request.json else -1
        noloan = request.json["noloan"] if "noloan" in request.json else True
        amount_big = request.json["amount_big"] if "amount_big" in request.json else 4000
        is_grant_day = request.json["is_grant_day"]
        asset_import = AssetImportFactory.get_import_obj(env, country)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ret["data"]["item_no"], ret["data"]["item_no_x"], ret["data"]["four_element"] = asset_import.create_asset(
            advance_month,
            loan_channel,
            advance_day=advance_day,
            count=count,
            period_day=day,
            is_grant_day=is_grant_day,
            source_type=source_type,
            noloan=noloan,
            amount_big=amount_big)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ret["code"] = 0
        ret["message"] = "create data success"
    except:
        ret["message"] = traceback.format_exc()
    finally:
        return jsonify(ret)


@create_data.route('/run_rbiz_withhold_msg', methods=["POST"])
def run_rbiz_withhold_msg():
    ret = {
        "code": 1,
        "message": "run rbiz withhold msg failed",
        "data": {
        }
    }
    try:
        env = request.json["env"]
        item_no = request.json["item_no"]
        db_env = request.json["db_env"] if "db_env" in request.json else "test"
        country = "china"
        asset = AssetImportFactory.get_import_obj(env, country, db_env=db_env)
        asset.run_rbiz_withhold_msg(item_no)
        ret["code"] = 0
        ret["message"] = "run rbiz withhold msg success"
    except:
        ret["message"] = traceback.format_exc()
    finally:
        return jsonify(ret)


@create_data.route('/run_rbiz_withhold_task', methods=["POST"])
def run_rbiz_withhold_task():
    ret = {
        "code": 1,
        "message": "run rbiz withhold task failed",
        "data": {
        }
    }
    try:
        env = request.json["env"]
        item_no = request.json["item_no"]
        db_env = request.json["db_env"] if "db_env" in request.json else "test"
        country = "china"
        asset = AssetImportFactory.get_import_obj(env, country, db_env=db_env)
        asset.run_rbiz_withhold_task(item_no)
        ret["code"] = 0
        ret["message"] = "run rbiz withhold task success"
    except:
        ret["message"] = traceback.format_exc()
    finally:
        return jsonify(ret)


@create_data.route('/change_asset', methods=["POST"])
def change_asset():
    ret = {
        "code": 1,
        "message": "change data failed",
        "data": {
            "item_no": "",
            "item_no_x": "",
        }
    }
    env = request.json["env"]
    db_env = request.json["db_env"] if "db_env" in request.json else "test"
    country = request.json["country"] if "country" in request.json else "china"
    asset_item_no = request.json["asset_item_no"]
    asset_item_no_x = request.json["asset_item_no_x"]
    advance_month = request.json["advance_month"]
    environment = request.json["environment"] if 'environment' in request.json else 'test'
    advance_day = request.json["advance_day"] if "advance_day" in request.json else -1
    is_grant_day = request.json["is_grant_day"]
    asset_import = AssetImportFactory.get_import_obj(env, country, db_env=environment)
    change_cp = request.json["change_cp"] if "change_cp" in request.json else True
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ret["data"]["item_no"], ret["data"]["item_no_x"], ret["data"]["four_element"] = asset_import.change_asset(
        advance_month,
        asset_item_no,
        asset_item_no_x,
        advance_day=advance_day,
        change_cp=change_cp
        )
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    ret["code"] = 0
    ret["message"] = "create data success"
    return jsonify(ret)


@create_data.route('/sync_asset', methods=["POST"])
def sync_asset():
    ret = {
        "code": 1,
        "message": "change data failed",
        "data": {
            "item_no": "",
            "item_no_x": "",
        }
    }
    try:
        env = request.json["env"]
        country = request.json["country"] if "country" in request.json else "china"
        asset_item_no = request.json["asset_item_no"]
        asset_item_no_x = request.json["asset_item_no_x"]
        asset_import = AssetImportFactory.get_import_obj(env, country)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        asset_import.sync_asset_to_rbiz(asset_item_no)
        asset_import.sync_asset_to_rbiz(asset_item_no_x)
        print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        ret["code"] = 0
        ret["message"] = "create data success"
    except:
        ret["message"] = traceback.format_exc()
    finally:
        return jsonify(ret)



