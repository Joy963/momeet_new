#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Blueprint, jsonify, request
from momeet.views.base import BaseView
from momeet.models.user import (
    get_user,
    get_user_info,
    EduExperience,
    WorkExperience,
    UserInfoProcess,
    UserDetail
)
from momeet.forms.user import (
    UserBaseInfoUpdateForm,
    UserAvatarForm,
    UserEduInfoForm,
    UserWorkInfoForm,
    UserSystemInfoForm,
    UserCoverPhotoForm,
    UserDescriptionForm,
    UserDetailForm
)
from momeet.utils.qnutil import QiniuHelper

bp = Blueprint('user_info', __name__)


class UserBaseInfoView(BaseView):
    def get(self, uid):
        user = get_user(uid)
        return jsonify(user.to_dict_ext() if user else {})

    def post(self, uid):
        form = UserBaseInfoUpdateForm(csrf_enabled=False)
        if form.validate_on_submit() and form.save(uid):
            return jsonify({"success": True})
        return jsonify({"success": False})


class UserExtInfoView(BaseView):
    def get(self, uid):
        process = UserInfoProcess(uid)
        u_info = process.get_userinfo()
        result = dict()
        if u_info:
            result = u_info.to_dict()
            u_detail = u_info.detail.all()
            result['detail'] = map(lambda x: x.to_dict_ext(), u_detail)
        return jsonify({"success": True, "user_info": result})


class UserDetailView(BaseView):
    def post(self, uid):
        user_info = get_user_info(uid)
        form = UserDetailForm(csrf_enabled=False, obj=user_info)
        if form.validate_on_submit():
            detail = form.save(request.files)
            return jsonify({"success": True, "detail_id": detail.id} if detail else {{"success": False}})
        return jsonify({"success": False})

    def delete(self, uid=None):
        if not uid:
            return jsonify({"success": False, "msg": "delete user_detail failed"})
        detail = UserDetail.query.get(int(uid))
        detail.delete() if detail else None
        return jsonify({"success": True, "msg": "delete user detail success"})

    def put(self, uid=None):
        form = UserDetailForm(csrf_enabled=False)
        if uid and form.validate_on_submit() and \
                form.update(int(uid), files=request.files.getlist('photo')):
            return jsonify({"success": True, "msg": "update user detail success"})
        return jsonify({"success": False, "msg": "update user detail failed"})


class UserDescriptionView(BaseView):
    def post(self, uid):
        user_info = get_user_info(uid)
        form = UserDescriptionForm(csrf_enabled=False, obj=user_info)
        if form.validate_on_submit() and form.save():
            return jsonify({"success": True})
        return jsonify({"success": False})


class UserCoverPhotoView(BaseView):
    def post(self, uid):
        user_info = get_user_info(uid)
        form = UserCoverPhotoForm(csrf_enabled=False, obj=user_info)
        if form.validate_on_submit():
            uri = form.save(uid)
            if uri:
                return jsonify({"success": True, "cover": uri, "msg": ""})
        return jsonify({"success": False, "msg": "failed update cover!"})


class UserAvatarView(BaseView):
    def post(self, uid):
        form = UserAvatarForm(csrf_enabled=False)
        if form.validate_on_submit():
            avatar_uri = form.save(uid)
            if avatar_uri:
                return jsonify({"success": True, "avatar": avatar_uri})
        return jsonify({"success": False, "msg": "failed update avatar!"})


class UserEduInfoView(BaseView):
    def get(self, eid=None):
        if not eid:
            user = get_user(request.args.get('user_id'))
            if not user:
                return jsonify({"success": False, "msg": "invalid uid or openid!"})
            edus = EduExperience.query.filter_by(user_id=user.id).all()
            return jsonify({"success": True, "results": [_.to_dict() for _ in edus]})
        else:
            edu = EduExperience.get_edu_experience(int(eid))
            return jsonify({"success": True, "edu_experience": edu.to_dict() if edu else {}})

    def post(self):
        form = UserEduInfoForm(csrf_enabled=False)
        if form.validate_on_submit():
            edu = form.curd('add')
            return jsonify({"success": True,
                            'edu_id': edu.id if edu else None,
                            "msg": "add edu exprience success"})
        return jsonify({"success": False, "msg": "add edu exprience failed"})

    def put(self, eid=None):
        form = UserEduInfoForm(csrf_enabled=False)
        if eid and form.validate_on_submit() and form.curd('update', eid):
            return jsonify({"success": True, "msg": "update edu exprience success"})
        return jsonify({"success": False, "msg": "update edu exprience failed"})

    def delete(self, eid=None):
        if not eid:
            return jsonify({"success": False, "msg": "delete edu exprience failed"})
        edu = EduExperience.get_edu_experience(int(eid))
        edu.delete() if edu else None
        return jsonify({"success": True, "msg": "delete edu exprience success"})


class UserWorkInfoView(BaseView):
    def get(self, wid=None):
        if not wid:
            user = get_user(request.args.get('user_id'))
            if not user:
                return jsonify({"success": False, "msg": "invalid uid or openid!"})
            works = WorkExperience.query.filter_by(user_id=user.id).all()
            return jsonify({"success": True, "results": [_.to_dict() for _ in works]})
        else:
            work = WorkExperience.get_work_experience(int(wid))
            return jsonify({"success": True, "edu_experience": work.to_dict() if work else {}})

    def post(self):
        form = UserWorkInfoForm(csrf_enabled=False)
        if form.validate_on_submit():
            work = form.curd('add')
            return jsonify({"success": True,
                            "work_id": work.id if work else None,
                            "msg": "add work exprience success"})
        return jsonify({"success": False, "msg": "add work exprience failed"})

    def put(self, wid=None):
        form = UserWorkInfoForm(csrf_enabled=False)
        if wid and form.validate_on_submit() and form.curd('update', wid):
            return jsonify({"success": True, "msg": "update work exprience success"})
        return jsonify({"success": False, "msg": "update work exprience failed"})

    def delete(self, wid=None):
        if not wid:
            return jsonify({"success": False, "msg": "delete work exprience failed"})
        work = WorkExperience.get_work_experience(int(wid))
        work.delete() if work else None
        return jsonify({"success": True, "msg": "delete work exprience success"})


class UserSystemInfoView(BaseView):
    def post(self, uid=None):
        form = UserSystemInfoForm(csrf_enabled=False)
        if uid and form.validate_on_submit():
            form.save(uid)
            return jsonify({"success": True, "msg": "OK"})
        return jsonify({"success": False, "msg": "ERROR"})


class GetQiniuUploadToken(BaseView):
    def get(self):
        qn_heleper = QiniuHelper()
        return jsonify({'token': qn_heleper.get_upload_token()})


bp.add_url_rule("cover/<string:uid>", view_func=UserCoverPhotoView.as_view("cover"))
bp.add_url_rule("description/<string:uid>", view_func=UserDescriptionView.as_view("description"))
bp.add_url_rule("detail/<string:uid>", view_func=UserDetailView.as_view("detail"))
bp.add_url_rule("detail/<string:uid>", view_func=UserDetailView.as_view("detail.delete"))
bp.add_url_rule("ext_info/<string:uid>", view_func=UserExtInfoView.as_view("ext_info"))

bp.add_url_rule("avatar/<string:uid>", view_func=UserAvatarView.as_view("avatar"))
bp.add_url_rule("base_info/<string:uid>", view_func=UserBaseInfoView.as_view("base_info"))
bp.add_url_rule("edu_info", view_func=UserEduInfoView.as_view("edu_infos"))
bp.add_url_rule("edu_info/<string:eid>", view_func=UserEduInfoView.as_view("edu_info"))
bp.add_url_rule("work_info", view_func=UserWorkInfoView.as_view("work_infos"))
bp.add_url_rule("work_info/<string:wid>", view_func=UserWorkInfoView.as_view("work_info"))
bp.add_url_rule("system_info/<string:uid>", view_func=UserSystemInfoView.as_view("system_info"))

bp.add_url_rule("upload_token", view_func=GetQiniuUploadToken.as_view("upload_token"))


