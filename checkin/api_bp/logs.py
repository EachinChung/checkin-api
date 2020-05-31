from flask import Blueprint, g, request

from checkin.common import response_json
from checkin.models import Log
from checkin.token import login_required

logs_bp = Blueprint("logs", __name__)


@logs_bp.route("")
@login_required
def get_logs():
    page = request.args.get('page', default=1, type=int)

    def _decode(item):
        return dict(
            id=item.id,
            course_name=item.task.course_name,
            active_id=item.active_id,
            datetime=item.datetime.strftime("%Y-%m-%d %H:%M:%S"),
            status=item.status,
            checkin_type=item.checkin_type
        )

    logs = Log.query.filter_by(user_id=g.id).paginate(page=page, per_page=20)
    items = list(map(_decode, logs.items))

    return response_json(dict(
        items=items,
        page=logs.page,
        finished=not logs.has_next
    ))
