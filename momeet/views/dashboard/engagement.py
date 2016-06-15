from flask import Blueprint, request, render_template
from momeet.views.base import BaseView
from momeet.models.engagement import *


bp = Blueprint('dashboard.engagement', __name__)


class EngagementOrderView(BaseView):
    template_name = "dashboard/engagement/order.html"

    def get(self, order_id=None):
        if not order_id:
            page = safe_int(request.args.get("page", 1))
            status = safe_int(request.args.get("status", 0))
            host = safe_int(request.args.get("host", 0))
            guest = safe_int(request.args.get("guest", 0))

            items, pagination = get_engagement_order_list_by_page(
                page=page, status=status, host=host, guest=guest)
            data = dict(items=map(lambda x: x.to_dict_ext(), items), pagination=pagination)
            return render_template(self.template_name, **data)
        else:
            item = get_engagement_order(order_id)
            return render_template(self.template_name, **{"items": [item.to_dict_ext()]})


bp.add_url_rule("", view_func=EngagementOrderView.as_view("orders"))
bp.add_url_rule("<string:order_id>", view_func=EngagementOrderView.as_view("order"))
