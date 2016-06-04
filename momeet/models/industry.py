#!/usr/bin/env python
# -*- coding: utf-8 -*-


from momeet.lib import (
    BaseModel, db
)

from momeet.utils import utf8, to_unicode


class Industry(BaseModel):
    """
    行业
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)

    def __str__(self):
        return to_unicode(self.name)

    def __repr__(self):
        return utf8(self.name)


def get_industry_by_name(name):
    return Industry.query.filter_by(name=name).first()


def get_industry(i_id):
    return Industry.query.get(i_id)


def get_all_industry():
    return Industry.query.order_by(Industry.id.asc()).all()
