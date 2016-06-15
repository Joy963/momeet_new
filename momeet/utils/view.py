#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import flash as flask_flash

from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms import RadioField, SelectField
from wtforms import widgets, SelectMultipleField, TextField


def flash(message, level='info', category='message'):
    flask_flash({'msg': message, 'level': level}, category=category)


class CustomRadioField(RadioField):

    def pre_validate(self, form):
        for v, _ in self.choices:
            if self.data == v:
                break
        else:
            if getattr(self, 'default_error', ''):
                raise ValueError(self.default_error or '')
            else:
                raise ValueError(self.gettext('Not a valid choice'))


class CustomQuerySelectField(QuerySelectField):

    selected = None

    def iter_choices(self):
        if self.allow_blank:
            yield ('__None', self.blank_text, self.data is None)

        for pk, obj in self._get_object_list():
            if self.selected is not None and self.selected.id == obj.id:
                yield (pk, self.get_label(obj), True)
            else:
                yield (pk, self.get_label(obj), False)


class CustomSelectField(SelectField):
    def iter_choices(self):
        for value, label, selected in self.choices:
            yield (value, label, selected, self.coerce(value) == self.data)


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

