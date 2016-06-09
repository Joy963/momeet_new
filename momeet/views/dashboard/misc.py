#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, jsonify, request
from momeet.constants.city import CITY_DATA
from momeet.utils.upload import save_upload_file_to_qiniu
from momeet.views.base import BaseView


bp = Blueprint('dashboard', __name__)


class IndexView(BaseView):
    def get(self):
        return render_template("dashboard/index.html")


class CitiesView(BaseView):
    def get(self):
        return jsonify(dict(data=CITY_DATA))


class UploadImgView(BaseView):
    def post(self):
        f = request.files['file']
        src = save_upload_file_to_qiniu(f)
        return jsonify(dict(code=0, src=src, message="success"))


class TestView(BaseView):
    def get(self):
        return render_template("dashboard/test.html")


bp.add_url_rule("", view_func=IndexView.as_view("index"))
bp.add_url_rule("cities/", view_func=CitiesView.as_view("cities"))
bp.add_url_rule("upload_img/", view_func=UploadImgView.as_view("upload_img"))
bp.add_url_rule("test/", view_func=TestView.as_view("test"))
