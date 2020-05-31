from flask import Blueprint, g, request
from flask.views import MethodView

from checkin.api_error import APIError
from checkin.common import get_request_body, response_json
from checkin.extensions import db
from checkin.models import Task
from checkin.token import login_required

tasks_bp = Blueprint("tasks", __name__)


@tasks_bp.route("")
@login_required
def get_tasks():
    page = request.args.get('page', default=1, type=int)

    def _decode(item):
        return dict(
            id=item.id,
            course_name=item.course_name,
            weekday=item.weekday,
            start_hour=item.start_hour,
            end_hour=item.end_hour
        )

    tasks = Task.query.filter_by(user_id=g.id).paginate(page=page, per_page=20)
    items = list(map(_decode, tasks.items))

    return response_json(dict(
        items=items,
        page=tasks.page,
        finished=not tasks.has_next
    ))


class TasksAPI(MethodView):
    decorators = [login_required]

    @staticmethod
    def get(task_id):
        def _decode(item):
            return dict(
                id=item.id,
                course_name=item.course_name,
                course_id=item.course_id,
                class_id=item.class_id,
                weekday=item.weekday,
                start_hour=item.start_hour,
                end_hour=item.end_hour,
                address=item.address,
                longitude=item.longitude,
                latitude=item.latitude
            )

        task = Task.query.get(task_id)
        if task is None: raise APIError("该任务不存在")
        if task.user_id != g.id: raise APIError("你无权访问该任务")
        return response_json(_decode(task))

    @staticmethod
    def patch(task_id):
        task = Task.query.get(task_id)
        if task is None: raise APIError("该任务不存在")
        if task.user_id != g.id: raise APIError("你无权访问该任务")

        address, longitude, latitude = get_request_body("address", "longitude", "latitude")
        task.address = address
        task.longitude = longitude
        task.latitude = latitude

        db.session.add(task)
        db.session.commit()
        return response_json(msg="设置成功")


tasks_bp.add_url_rule(rule="/<int:task_id>", view_func=TasksAPI.as_view("tasks"), methods=("GET", "PATCH"))
