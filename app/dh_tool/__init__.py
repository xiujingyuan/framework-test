from flask import Blueprint

api_dh = Blueprint('api_dh', __name__)

from . import dh_tool
