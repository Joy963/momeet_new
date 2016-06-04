#!/usr/bin/env python
# -*- coding: utf-8 -*-


from wtforms import StringField
from wtforms.validators import DataRequired

from momeet.forms.base import BaseForm
from momeet.views.dashboard.error import ErrorsEnum
from momeet.models.industry import Industry, get_industry_by_name

from .fields_name import IndustryFields


class IndustryForm(BaseForm):

    name = StringField(
        IndustryFields.NAME,
        validators=[
            DataRequired(
                message=ErrorsEnum.INDUSTRY_NAME_REQUIRED.describe()
            ),
        ],
    )

    def __init__(self, *args, **kwargs):
        super(IndustryForm, self).__init__(*args, **kwargs)

    def validate_name(self, field):
        name = field.data.strip()
        i = get_industry_by_name(name)
        if i:
            raise ValueError(ErrorsEnum.INDUSTRY_NAME_EXISTS.describe())

    def save(self):
        i = Industry()
        i.name = self.name.data
        i.save()
        return i
