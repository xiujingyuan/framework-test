from flask import Blueprint

rbiz_tool = Blueprint('rbiz_tool', __name__)

from . import Rbiztool
