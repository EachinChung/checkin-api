from os import getenv
from time import time

from flask import Blueprint, abort, redirect, request
from flask.views import MethodView

from checkin.common import get_request_body, response_json, safe_md5
from checkin.models import User
from checkin.token import create_token
from checkin.utils import Redis

oauth_bp = Blueprint("oauth", __name__)


class OauthAPI(MethodView):
    @staticmethod
    def get():
        openid = request.args.get("openid")
        if openid is None: abort(401)

        sign = safe_md5(f"{openid}{time()}")
        Redis.set(sign, openid)
        return redirect(f"{getenv('FRONT_END_URL')}/oauth?sign={sign}")

    @staticmethod
    def post():
        sign = get_request_body("sign")[0]
        openid = Redis.get(sign)
        if openid is None: abort(401)
        Redis.delete(sign)

        user = User.query.filter_by(open_id=openid).first_or_404()
        return response_json(create_token(user))


oauth_bp.add_url_rule(rule="", view_func=OauthAPI.as_view("oauth"), methods=("GET", "POST"))
