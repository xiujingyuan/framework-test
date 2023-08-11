import random

from app.dh_tool import api_dh
from flask import request


@api_dh.route('/', methods=['GET', 'POST'])
def hello_world():
    return 'Hello Dh!'


