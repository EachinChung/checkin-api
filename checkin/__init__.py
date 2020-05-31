from datetime import datetime
from traceback import format_exc

from flask import Flask, request

from checkin.api_bp.logs import logs_bp
from checkin.api_bp.map import map_bp
from checkin.api_bp.oauth import oauth_bp
from checkin.api_bp.tasks import tasks_bp
from checkin.api_error import APIError
from checkin.common import response_json
from checkin.extensions import db


def create_app(config_name=None) -> Flask:
    """
    加载基本配置
    :return:
    """
    app = Flask('checkin')
    app.config.from_pyfile('settings.py')

    # 本地开发由 flask-cors 提供 CORS
    if config_name is None:
        from flask_cors import CORS
        CORS(app)

    register_blueprints(app)
    register_extensions(app)
    register_errors(app)
    return app


def register_blueprints(app) -> None:
    """
    加载蓝本
    :param app:
    :return:
    """
    app.register_blueprint(logs_bp, url_prefix="/logs")
    app.register_blueprint(oauth_bp, url_prefix="/oauth")
    app.register_blueprint(tasks_bp, url_prefix="/tasks")
    app.register_blueprint(map_bp, url_prefix="/map")


def register_extensions(app) -> None:
    """
    初始化拓展
    :param app:
    :return:
    """
    db.init_app(app)


def register_errors(app) -> None:
    """
    加载错误页
    :param app:
    :return:
    """

    @app.errorhandler(400)
    def bad_request(e) -> response_json:
        return response_json(err=400, msg="请求报文存在语法错误"), 400

    @app.errorhandler(401)
    def unauthorized(e) -> response_json:
        return response_json(err=401, msg="没有权限"), 401

    @app.errorhandler(404)
    def not_found(e) -> response_json:
        return response_json(err=404, msg="找不到此资源"), 404

    @app.errorhandler(405)
    def method_not_allowed(e) -> response_json:
        return response_json(err=405, msg="方法不被允许"), 405

    @app.errorhandler(Exception)
    def the_api_error(e) -> response_json:
        if isinstance(e, APIError):
            return response_json(err=e.code, msg=e.message)

        with open("err.log", "a") as f:
            f.write(f"\n{request.url} - {request.remote_addr} - {request.method}\n")
            f.write(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
            f.write(f"\n{format_exc()}")
            f.write("\n")

        return response_json(err=500, msg="服务器内部错误"), 500
