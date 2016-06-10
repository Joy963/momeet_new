from flask import Blueprint, jsonify, request
from momeet.views.base import BaseView
from momeet.lib.crypto import id_decrypt, id_encrypt
from momeet.models.user import (
    get_user,
    EduExperience,
    WorkExperience
)
from momeet.forms.user import (
    UserInfoUpdateForm,
    UserAvatarForm,
    UserEduInfoForm,
    UserWorkInfoForm,
    UserSystemInfoForm
)

bp = Blueprint('user_info', __name__)


class UserBaseInfo(BaseView):
    def get(self, uid):
        user = get_user(uid)
        return jsonify(user.to_dict_ext() if user else {})

    def post(self, uid):
        form = UserInfoUpdateForm(csrf_enabled=False)
        if form.validate_on_submit() and form.save(uid):
            return jsonify({"success": True})
        return jsonify({"success": False})


class UserAvatar(BaseView):
    def post(self, uid):
        form = UserAvatarForm(csrf_enabled=False)
        if form.validate_on_submit():
            avatar_uri = form.save(uid)
            if avatar_uri:
                return jsonify({"success": True, "avatar": avatar_uri})
        return jsonify({"success": False, "msg": "failed update avatar!"})


class UserEduInfo(BaseView):
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
                            'edu_id': id_encrypt(edu.id) if edu else None,
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


class UserWorkInfo(BaseView):
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
                            "work_id": id_encrypt(work.id) if work else None,
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


class UserSystemInfo(BaseView):
    def post(self, uid=None):
        form = UserSystemInfoForm(csrf_enabled=False)
        if uid and form.validate_on_submit():
            form.save(uid)
            return jsonify({"success": True, "msg": "OK"})
        return jsonify({"success": False, "msg": "ERROR"})


bp.add_url_rule("avatar/<string:uid>", view_func=UserAvatar.as_view("avatar"))
bp.add_url_rule("base_info/<string:uid>", view_func=UserBaseInfo.as_view("base_info"))
bp.add_url_rule("edu_info", view_func=UserEduInfo.as_view("edu_infos"))
bp.add_url_rule("edu_info/<string:eid>", view_func=UserEduInfo.as_view("edu_info"))
bp.add_url_rule("work_info", view_func=UserWorkInfo.as_view("work_infos"))
bp.add_url_rule("work_info/<string:wid>", view_func=UserWorkInfo.as_view("work_info"))
bp.add_url_rule("system_info/<string:uid>", view_func=UserSystemInfo.as_view("system_info"))
