from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(session_options={"autocommit": True})


def create_app():
    app = Flask(__name__)
    db.init_app(app, )

    from app.gbiz_tool import gbiz_tool as gbiz_tool_blueprint
    app.register_blueprint(gbiz_tool_blueprint, url_prefix="/")

    from app.rbiz_tool import rbiz_tool as rbiz_tool_blueprint
    app.register_blueprint(rbiz_tool_blueprint, url_prefix="/")

    from app.tool import common_tool as common_tool_blueprint
    app.register_blueprint(common_tool_blueprint, url_prefix="/")

    from app.create_data import create_data as create_data_blueprint
    app.register_blueprint(create_data_blueprint, url_prefix="/api/rbiz")

    from app.list_auto_data_cases import list_auto_data_cases as list_auto_data_cases_blueprint
    app.register_blueprint(list_auto_data_cases_blueprint, url_prefix="/api/auto_test")

    from app.contract_tool import contract_tool as contract_tool_blueprint
    app.register_blueprint(contract_tool_blueprint, url_prefix="/")

    return app
