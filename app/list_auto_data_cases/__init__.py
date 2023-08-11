from flask import Blueprint

list_auto_data_cases = Blueprint('list_auto_data_cases', __name__)

from . import ListAutoDataCasesApi
