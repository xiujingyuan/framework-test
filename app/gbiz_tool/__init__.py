from flask import Blueprint

gbiz_tool = Blueprint('gbiz_tool', __name__)

from . import GbizTool
