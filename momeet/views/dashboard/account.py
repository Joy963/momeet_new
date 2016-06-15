#!/usr/bin/env python
# -*- coding: utf-8 -*-


from flask import (
    Blueprint, render_template,
    request, url_for,
    redirect
)

from momeet.models.invitation import (
    get_invitation_code_list_by_page,
    PER_PAGE_COUNT,
    create_invitation_code
)
from momeet.utils import safe_int, Pagination
from momeet.views.base import BaseView

bp = Blueprint('dashboard.account', __name__)


class InvitationCodeView(BaseView):
    template_name = "dashboard/account/invitationcode.html"

    def get(self):
        page = safe_int(request.args.get("page", 1))
        is_used = bool(safe_int(request.args.get("is_used", 0)))
        items, count = get_invitation_code_list_by_page(page=page, is_used=is_used)
        pagination = Pagination(page, PER_PAGE_COUNT, count)
        data = dict(
            items=items,
            pagination=pagination,
        )
        return render_template(self.template_name, **data)

    def post(self):
        create_invitation_code()
        return redirect(url_for('dashboard.account.code'))

bp.add_url_rule("code/", view_func=InvitationCodeView.as_view("code"))
