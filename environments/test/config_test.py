# @Time    : 2021/1/7 5:31 下午
# @Author  : yuanxiujing
# @File    : config_test.py
# @Software: PyCharm
import json

from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.jc_mock.KeyValueDb import KeyValue

app = Flask(__name__)


def test_config():
    """配置参数"""
    # sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = create_engine("mysql+pymysql://root:Coh8Beyiusa7@10.1.0.15:3306/jc-mock?charset=utf8")
    # 设置成 True，SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 创建DBSession类型:
    DBSession = sessionmaker(bind=SQLALCHEMY_DATABASE_URI)
    # 创建session对象:
    session = DBSession()
    key_value = session.query(KeyValue).filter(KeyValue.key == 'report_email_recipients').one()
    config_info = json.loads(key_value.value)
    receiver = config_info["recipients"]
    session.close()
    return receiver
