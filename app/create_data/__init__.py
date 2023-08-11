from flask import Blueprint

create_data = Blueprint('create_data', __name__)

from . import RbizCreateDataApi
