from functools import wraps
from os import getenv

from flask import g, request
from itsdangerous import BadSignature, TimedJSONWebSignatureSerializer

from checkin.api_error import APIError


def get_token() -> str:
    """
    从请求头获取token
    :return:
    """

    try:
        token_type, token = request.headers["Authorization"].split(None, 1)
    except (KeyError, ValueError):
        raise APIError("请重新登录", code=401)

    if token == "null" or token_type.lower() != "bearer":
        raise APIError("请重新登录", code=401)

    return token


def create_token(user) -> dict:
    return dict(token=generate_token({"id": user.id}))


def generate_token(data: dict, *, token_type: str = "TOKEN", expires_in: int = 31536000) -> str:
    """
    生成令牌
    :param data: 令牌的内容
    :param token_type: 令牌的类型，每一个类型对应不同的密钥
    :param expires_in: 有效时间
    :return: 令牌
    """
    s = TimedJSONWebSignatureSerializer(getenv(token_type), expires_in=expires_in)
    token = s.dumps(data).decode("ascii")
    return token


def validate_token(token: str, token_type: str = "TOKEN") -> dict:
    """
    验证令牌
    :param token: 令牌
    :param token_type: 令牌类型
    """
    s = TimedJSONWebSignatureSerializer(getenv(token_type))
    try:
        data = s.loads(token)
    except BadSignature:
        raise APIError("请重新登录", code=401)
    else:
        return data


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kw):
        token = get_token()
        g.id = validate_token(token)["id"]
        return func(*args, **kw)

    return wrapper
