#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import (
    abort, request,
    jsonify, redirect
)

from flask.views import View
from momeet.models.engagement import Engagement, Theme
from momeet.models.user import EduExperience, WorkExperience, UserPhoto


class BaseView(View):
    methods = ['GET', 'POST', 'PUT', 'DELETE']

    def dispatch_request(self, *args, **kwargs):
        request_method = request.method
        method = getattr(self, request_method.lower())(*args, **kwargs)
        return method

    def get(self, *args, **kwargs):
        abort(405)

    def post(self, *args, **kwargs):
        abort(405)

    def put(self, *args, **kwargs):
        abort(405)

    def delete(self, *args, **kwargs):
        abort(405)


class FlagView(BaseView):
    MODIFY_IS_ACTIVE = True  # 如果为 true 只改变 is_active 的值 否则 delete 掉
    REDIRECT = False
    SAVE_RES = True

    def check_delete(self, res):
        return dict(code=0)

    def check_update(self, res):
        return dict(code=0)

    def custom(self, res_id):
        return dict(code=0)

    def post(self, res_id):
        flag = request.form.get('flag', 'update')
        if flag == 'del':
            return self.delete(res_id)
        elif flag == 'update':
            return self.update(res_id)
        else:
            return self.custom(res_id)

    def exec_method(self, process, res):
        _before = getattr(self, process, None)
        if _before and callable(_before):
            _before(res)

    def update(self, res_id):
        res = self.get_res(res_id)
        if not res:
            abort(404)
        checked = self.check_update(res)
        if not isinstance(checked, dict):
            return checked
        if checked.get('code') == 0:
            self.exec_method('before_update', res)
            if self.SAVE_RES:
                res.save()
            self.exec_method('after_update', res)

        if self.REDIRECT:
            return redirect(self.redirect_url)
        else:
            return jsonify(checked)

    def delete(self, res_id, is_revert=False):
        res = self.get_res(res_id)
        if not res:
            abort(404)
        checked = self.check_delete(res)
        if not isinstance(checked, dict):
            return checked
        if checked.get('code') == 0:
            self.exec_method('before_delete', res)
            if self.MODIFY_IS_ACTIVE:
                res.is_active = False
                res.save()
            else:
                WorkExperience.query.filter_by(user_id=res_id).delete()
                EduExperience.query.filter_by(user_id=res_id).delete()
                UserPhoto.query.filter_by(user_id=res_id).delete()

                engagements = Engagement.query.filter_by(user_id=res_id).all()
                for _ in engagements:
                    Theme.query.filter_by(engagement_id=_.id).delete()
                    _.delete()
                res.delete()
            self.exec_method('after_delete', res)
        return jsonify(checked)
