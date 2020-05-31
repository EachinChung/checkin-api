from checkin.extensions import db


class User(db.Model):
    """
    用户表
    """
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    pwd = db.Column(db.String)
    open_id = db.Column(db.String)
    cookies = db.Column(db.String)


class Task(db.Model):
    """
    任务表
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    course_name = db.Column(db.String)
    course_id = db.Column(db.Integer)
    class_id = db.Column(db.Integer)
    weekday = db.Column(db.Integer)
    start_hour = db.Column(db.Integer)
    end_hour = db.Column(db.Integer)
    address = db.Column(db.String)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)


class Log(db.Model):
    """
    日志表
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    task_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    active_id = db.Column(db.Integer)
    datetime = db.Column(db.DateTime)
    status = db.Column(db.String)
    checkin_type = db.Column(db.String)
    task = db.relationship("Task")
