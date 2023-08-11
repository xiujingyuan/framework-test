# @Time    : 2021/1/7 4:58 下午
# @Author  : yuanxiujing
# @File    : KeyValueDb.py
# @Software: PyCharm
from sqlalchemy import Column, DateTime, Enum, String, TIMESTAMP, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from app import db

Base = declarative_base()
metadata = Base.metadata


class KeyValue(db.Model):
    __tablename__ = 'key_value'

    id = Column(INTEGER(11), primary_key=True, comment='自增id')
    key = Column(String(100), nullable=False, server_default=text("''"), comment='key')
    value = Column(Text, comment='value')
    memo = Column(Text, comment='备注')
    status = Column(Enum('active', 'inactive'), nullable=False, server_default=text("'active'"), comment='状态')
    create_at = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"), comment='创建时间')
    update_at = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), comment='更新时间')
