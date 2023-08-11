from flask import Blueprint

common_tool = Blueprint('tool', __name__)

from . import common_tools
