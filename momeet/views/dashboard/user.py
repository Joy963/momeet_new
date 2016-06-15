#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import (
    Blueprint, render_template,
    request, url_for, abort,
    redirect, jsonify
)
from momeet.forms.engagement import EngagementForm
from momeet.forms.user import *
from momeet.models.engagement import UserEngagementProcess
from momeet.models.user import *
from momeet.utils import logger
from momeet.utils import safe_int, Pagination, flash
from momeet.views.base import BaseView, FlagView

bp = Blueprint('dashboard.user', __name__)


class UserListView(BaseView):

    template_name = "dashboard/user/list.html"

    def page_data(self):
        page = safe_int(request.args.get("page", 1))
        items, count = get_user_list_by_page(page=page, **request.args)
        pagination = Pagination(page, USER_PER_PAGE_COUNT, count)
        return dict(
            items=items,
            pagination=pagination,
            gender_desc=USER_GENDER_DESC
        )

    def get(self):
        return render_template(self.template_name, **self.page_data())


class CreateUserView(BaseView):
    template_name = "dashboard/user/user.html"

    def get(self):
        form = UserForm()
        return render_template(self.template_name, form=form)

    def post(self):
        form = UserForm()
        if form.validate_on_submit():
            form.save()
            return redirect(url_for('dashboard.user.list'))
        else:
            return render_template(self.template_name, form=form)


class UserView(FlagView):
    template_name = "dashboard/user/user.html"
    REDIRECT = True
    MODIFY_IS_ACTIVE = False
    SAVE_RES = False
    _form = None
    redirect_url = None

    def get_res(self, res_id):
        return get_user(res_id)

    def get(self, res_id):
        user = self.get_res(res_id)
        if not user:
            abort(404)
        form = UserForm(obj=user)
        # form.process()
        return render_template(self.template_name, user=user, form=form)

    def check_update(self, user):
        form = UserForm(obj=user)
        if not form.validate_on_submit():
            return render_template(self.template_name, user=user, form=form)
        else:
            self._form = form
            return dict(code=0)

    def before_update(self, user):
        self._form.save()

    def after_update(self, user):
        flash(u"%s修改成功" % user.user_name, level='success')
        self.redirect_url = url_for("dashboard.user.item", res_id=user.id)

    def after_delete(self, user):
        flash(u"用户[%s]被删除" % user.user_name, level='success')


class UserPhotoView(BaseView):

    template_name = "dashboard/user/photo.html"

    def get(self, user_id):
        user = get_user(user_id)
        if not user:
            abort(404)
        process = UserInfoProcess(user_id)
        photos = process.get_photos()
        form = UserPhotoForm()
        return render_template(self.template_name, photos=photos, form=form, user=user)

    def post(self, user_id):
        form = UserPhotoForm()
        if form.validate_on_submit():
            form.save(user_id)
            return redirect(url_for('dashboard.user.photos', user_id=user_id))
        else:
            return render_template(self.template_name, form=form)


class UserPhotoDelView(BaseView):
    def post(self, user_id):
        user = get_user(user_id)
        if not user:
            abort(404)
        process = UserInfoProcess(user_id)
        photo = request.form.get("photo", "")
        logger.debug(request.form)
        logger.debug(photo)
        if photo:
            process.del_photo(photo)
        return jsonify(dict(code=0))


class UserDescriptionView(BaseView):
    template_name = "dashboard/user/detail.html"

    def post(self, user_id):
        user_info = get_user_info(user_id)
        form = UserDescriptionForm(obj=user_info)
        if form.validate_on_submit():
            form.save()
            flash(u"提交成功", level='success')
            return redirect(url_for('dashboard.user.detail', user_id=user_id))
        else:
            return render_template(self.template_name, form=form)


class UserCoverPhotoView(BaseView):
    template_name = "dashboard/user/detail.html"

    def post(self, user_id):
        user_info = get_user_info(user_id)
        form = UserCoverPhotoForm(obj=user_info)
        if form.validate_on_submit():
            form.save(user_id)
            flash(u"提交成功", level='success')
            return redirect(url_for('dashboard.user.detail', user_id=user_id))
        else:
            return render_template(self.template_name, form=form)


class UserDetailView(BaseView):
    template_name = "dashboard/user/detail.html"

    def get(self, user_id):
        user = get_user(user_id)
        user_info = get_user_info(user_id)
        form_dsp = UserDescriptionForm(obj=user_info)
        form_dtl = UserDetailForm(obj=user_info)
        form_cover = UserCoverPhotoForm(obj=user_info)
        process = UserInfoProcess(user_id)
        user_details = process.get_details()
        return render_template(
            self.template_name,
            form_dsp=form_dsp,
            form_dtl=form_dtl,
            form_cover=form_cover,
            user=user,
            user_details=user_details)

    def post(self, user_id):
        user_info = get_user_info(user_id)
        form = UserDetailForm(obj=user_info)
        if form.validate_on_submit():
            form.save(request.files)
            flash(u"修改成功", level='success')
            return redirect(url_for('dashboard.user.detail', user_id=user_id))
        else:
            return render_template(self.template_name, form=form)


class UserDetailDelView(BaseView):
    def post(self, user_id):
        process = UserInfoProcess(user_id)
        detail_id = request.form.get("detail_id", "")
        process.del_detail(detail_id)
        return jsonify(dict(code=0))


class UserEngagementView(BaseView):
    template_name = "dashboard/user/invitation.html"

    def get(self, user_id):
        user = get_user(user_id)
        _obj = UserEngagementProcess(user_id).get_all_engagement_dict()
        e_form = EngagementForm(obj=_obj)
        return render_template(
            self.template_name,
            form=e_form,
            user=user)

    def post(self, user_id):
        user = get_user(user_id)
        _obj = UserEngagementProcess(user_id).get_all_engagement_dict()
        e_form = EngagementForm(obj=_obj)
        if e_form.validate_on_submit():
            e_form.save()
            flash(u"修改成功", level='success')
            return redirect(url_for('dashboard.user.invitation', user_id=user_id))
        else:
            return render_template(self.template_name, form=e_form, user=user)


class UserAuthView(BaseView):
    template_name = "dashboard/user/auth.html"

    def check(self, user_id):
        user = get_user(user_id)
        if not user:
            abort(404)
        info = get_user_info(user_id)
        return user, info

    def get(self, user_id):
        user, info = self.check(user_id)
        form = UserAuthForm(obj=info)
        return render_template(
            self.template_name,
            form=form,
            user=user
        )

    def post(self, user_id):
        user, info = self.check(user_id)
        form = UserAuthForm(obj=info)
        if form.validate_on_submit():
            form.save()
            flash(u"修改成功", level='success')
            return redirect(url_for('dashboard.user.auth', user_id=user_id))
        else:
            return render_template(self.template_name, form=form)


class PersonalLabelView(BaseView):
    template_name = "dashboard/user/personal_label.html"

    def get(self):
        page = safe_int(request.args.get("page", 1))
        items, count = get_personal_label_list_by_page(page=page)
        pagination = Pagination(page, USER_PER_PAGE_COUNT, count)
        personal_form = UserPersonalLabelForm(csrf_enabled=False)
        data = dict(
            items=items,
            pagination=pagination,
            personal_form=personal_form
        )
        return render_template(self.template_name, **data)

    def post(self):
        job_form = UserPersonalLabelForm(csrf_enabled=False)
        if job_form.validate_on_submit():
            job_form.save()
        return redirect(url_for('dashboard.user.personal_label'))


bp.add_url_rule("list/", view_func=UserListView.as_view("list"))
bp.add_url_rule("create/", view_func=CreateUserView.as_view("create"))
bp.add_url_rule("<int:res_id>/", view_func=UserView.as_view("item"))
bp.add_url_rule("<int:user_id>/photos/", view_func=UserPhotoView.as_view("photos"))
bp.add_url_rule("<int:user_id>/photo/delete/", view_func=UserPhotoDelView.as_view("photo.delete"))
bp.add_url_rule("<int:user_id>/detail/", view_func=UserDetailView.as_view("detail"))
bp.add_url_rule("<int:user_id>/detail/delete", view_func=UserDetailDelView.as_view("detail.delete"))
bp.add_url_rule("<int:user_id>/cover/", view_func=UserCoverPhotoView.as_view("cover"))
bp.add_url_rule("<int:user_id>/description/", view_func=UserDescriptionView.as_view("description"))
bp.add_url_rule("<int:user_id>/invitation/", view_func=UserEngagementView.as_view("invitation"))
bp.add_url_rule("<int:user_id>/auth/", view_func=UserAuthView.as_view("auth"))

bp.add_url_rule("personal_label", view_func=PersonalLabelView.as_view("personal_label"))
