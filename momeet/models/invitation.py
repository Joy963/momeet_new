#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime
from momeet.utils.common import get_random_string
from momeet.lib import (
    BaseModel, db
)

PER_PAGE_COUNT = 15


class InvitationCode(BaseModel):
    """
    邀请码
    """
    dict_default_columns = ['code', 'is_used', 'created']
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(7), unique=True, index=True, nullable=False)  # 邀请码
    is_used = db.Column(db.Boolean, default=False)  # 是否使用
    created = db.Column(db.DateTime, default=datetime.now)


def get_invitation_code_list_by_page(page=1, is_used=False):
    query_kwargs = dict(is_used=is_used)
    codes = InvitationCode.query.filter_by(**query_kwargs)
    codes = codes.order_by(InvitationCode.id.desc()).paginate(page, PER_PAGE_COUNT)
    return codes.items, codes.total


def create_invitation_code():
    code = get_random_string(4)
    while InvitationCode.query.filter_by(code=code).first():
        code = get_random_string(4)

    invitation_code = InvitationCode()
    invitation_code.code = code
    invitation_code.save()
    return invitation_code


def get_invitation_code(code):
    if str(code).isdigit():
        return InvitationCode.query.get(code)
    return InvitationCode.query.filter_by(code=code).first()
