#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template,
    redirect, url_for,
    jsonify, request
)

from momeet.models.industry import get_all_industry, get_industry
from momeet.utils.view import flash
from momeet.constants.city import CITY_DATA
from momeet.utils.upload import save_upload_file_to_qiniu

from ._base import BaseView
from momeet.forms.industry import IndustryForm


bp = Blueprint('dashboard', __name__)


class IndexView(BaseView):

    def get(self):
        return render_template(
            "dashboard/index.html",
        )


class IndustryView(BaseView):

    template_name = "dashboard/misc/industry.html"
    redirect_url = 'dashboard.industry'

    def page_data(self):
        items = get_all_industry()
        return dict(items=items)

    def render(self, form, **kwargs):
        return render_template(self.template_name, form=form, **kwargs)

    def get(self):
        form = IndustryForm()
        return self.render(form, **self.page_data())

    def post(self):
        form = IndustryForm()
        if form.validate_on_submit():
            form.save()
            return redirect(url_for(self.redirect_url))
        else:
            return self.render(form, **self.page_data())


class IndustryItemView(BaseView):

    redirect_url = 'dashboard.industry'

    def post(self, i_id):
        i = get_industry(i_id)
        if not i:
            return jsonify(dict(code=-1, message="改行业已被删除"))
        # TODO 需要验证一下是否有这个行业的用户 如果有不许删除
        i.delete()
        flash(u'%s删除成功' % i.name)
        return jsonify(dict(code=0))


class CitiesView(BaseView):

    def get(self):
        return jsonify(dict(data=CITY_DATA))


class UploadImgView(BaseView):

    def post(self):
        file = request.files['file']
        src = save_upload_file_to_qiniu(file)
        return jsonify(
            dict(
                code=0,
                src=src,
                message="success",
            )
        )


class TestView(BaseView):

    def get(self):
        return render_template(
            "dashboard/test.html",
        )


bp.add_url_rule("", view_func=IndexView.as_view("index"))
bp.add_url_rule("industry/", view_func=IndustryView.as_view("industry"))
bp.add_url_rule("industry/<int:i_id>/", view_func=IndustryItemView.as_view("industry.item"))
bp.add_url_rule("cities/", view_func=CitiesView.as_view("cities"))
bp.add_url_rule("upload_img/", view_func=UploadImgView.as_view("upload_img"))
bp.add_url_rule("test/", view_func=TestView.as_view("test"))
