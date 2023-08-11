from flask import Blueprint

contract_tool = Blueprint('contract_tool', __name__)

from . import ContractTool
