#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import json
from contextlib import contextmanager

from sqlalchemy.types import TypeDecorator, VARCHAR
from flask.ext.sqlalchemy import SQLAlchemy, BaseQuery as _BaseQuery

from momeet.utils import FancyDict

from .crypto import id_encrypt


db = SQLAlchemy()


class JsonType(TypeDecorator):
    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value else None

    def process_result_value(self, value, dialect):
        return json.loads(value) if value else None


@contextmanager
def session_scope():
    session = db.session
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise


class BaseQuery(_BaseQuery):

    def as_list(self):
        return list(self)


db.Model.query_class = BaseQuery


class SessionMixin(object):

    def save(self, **kwargs):
        try:
            # 针对于可能存在的批量入库问题，这里增加判断是否传递了commit参数
            commit = kwargs.get('commit', True)
            db.session.add(self)
            if commit:
                db.session.commit()
            return self
        except:
            db.session.rollback()
            raise

    def delete(self, **kwargs):
        try:
            db.session.delete(self)
            db.session.commit()
            return self
        except:
            db.session.rollback()
            raise


class DefaultModel(db.Model):
    __abstract__ = True
    __table_args__ = {'mysql_charset': 'utf8', 'mysql_engine': 'InnoDB'}


class BaseModel(DefaultModel, SessionMixin):
    __abstract__ = True

    dict_default_columns = []

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def to_dict(self, columns=None):
        dct = FancyDict()
        if columns is None:
            columns = self.dict_default_columns
        for col in columns:
            if col == 'id' or col in getattr(self, 'encrypt_attrs', []):
                value = id_encrypt(getattr(self, col))
            else:
                value = getattr(self, col)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%Y-%m-%d')
            if isinstance(value, BaseModel):
                value = value.to_dict()
            if value is None:
                value = ''
            dct[col] = value
        return dct
