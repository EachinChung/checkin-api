from os import getenv

from flask import Blueprint, abort, redirect, request
from flask.views import MethodView
from requests import get

from checkin.common import get_request_body, response_json, safe_md5
from checkin.models import User
from checkin.token import create_token
from checkin.utils import Redis

oauth_bp = Blueprint("oauth", __name__)


class OauthAPI(MethodView):
    @staticmethod
    def get():
        try:
            url = 'https://api.nfuca.com/openLoginGetInfo'

            name = request.args.get("name", default="")
            the_time = request.args.get("time", default="")
            openid = request.args.get("openid", default="")
            nonce = request.args.get("nonce", default="")
            sign = safe_md5(name + the_time + openid + nonce + getenv("NFUCA_KEY"))

            response = get(url, params=dict(name=name, time=the_time, openid=openid, nonce=nonce, sign=sign),
                           timeout=10)
            nfuca_data = response.json()

            if nfuca_data['code'] != 0: abort(401)
            if nfuca_data['data']['no'] is None: abort(401)
            openid = request.args.get("openid")
            if openid is None: abort(401)

            Redis.set(sign, openid)
            return redirect(f"{getenv('FRONT_END_URL')}/oauth?sign={sign}")

        except OSError:
            abort(401)

    @staticmethod
    def post():
        sign = get_request_body("sign")[0]
        openid = Redis.get(sign)
        if openid is None: abort(401)
        Redis.delete(sign)

        user = User.query.filter_by(open_id=openid).first_or_404()
        return response_json(create_token(user))


oauth_bp.add_url_rule(rule="", view_func=OauthAPI.as_view("oauth"), methods=("GET", "POST"))
