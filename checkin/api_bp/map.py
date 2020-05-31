from flask import Blueprint
from requests import get

from checkin.api_error import APIError
from checkin.common import get_request_body, response_json
from checkin.token import login_required

map_bp = Blueprint("map", __name__)


@login_required
@map_bp.route("/BD09", methods=["POST"])
def bd09():
    try:
        res = get("https://api.map.baidu.com/geoconv/v1/", params={
            "coords": get_request_body("coords")[0],
            "from": 1,
            "to": 5,
            "ak": "wLuKgNcAIRmMwpSXpugPRrj8wYYi2ySR"
        }).json()
    except OSError:
        raise APIError("获取坐标失败")

    if res["status"] == 0:
        return response_json(dict(longitude=res["result"][0]["x"], latitude=res["result"][0]["y"]))
    else:
        raise APIError("获取坐标失败")
