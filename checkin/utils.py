from flask import current_app
from redis import StrictRedis


class Redis:

    @staticmethod
    def _get_r():
        pool = current_app.config['REDIS_POOL']
        return StrictRedis(connection_pool=pool)

    @classmethod
    def set(cls, key: str, value: str, expire=60) -> None:
        """
        写入键值对
        :param key:
        :param value:
        :param expire:
        :return:
        """
        r = cls._get_r()
        r.set(key, value, ex=expire)

    @classmethod
    def get(cls, key: str) -> str:
        """
        读取键值对内容
        :param key:
        :return:
        """
        r = cls._get_r()
        value = r.get(key)
        return value

    @classmethod
    def delete(cls, *names: str) -> None:
        """
        删除一个或者多个
        :param names:
        :return:
        """
        r = cls._get_r()
        r.delete(*names)
